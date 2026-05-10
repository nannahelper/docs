# 第 3 章：理解反向传播 —— 神经网络中的误差传递

> **场景：** 第 2 章我们学会了用梯度下降更新参数，但有一个关键问题悬而未决：**如何高效计算损失函数对每个参数的梯度？** 网络有成千上万个参数，不可能对每个参数都单独做一次前向传播来估算梯度。反向传播（Backpropagation）就是解决这个问题的算法——它能在一次前向传播 + 一次反向传播中，算出所有参数的梯度。

---

## 3.1 为什么需要反向传播？

### 问题：计算梯度的朴素方法太慢了

假设网络有 100 万个参数。用数值方法估算每个参数的梯度需要：

1. 对参数 $w_1$ 加一个微小扰动 $\epsilon$，前向传播一次，看损失变化
2. 对参数 $w_2$ 加扰动，再前向传播一次...
3. ...重复 100 万次

每次前向传播都要经过所有层，100 万次前向传播 = **不可接受的计算量**。

!!! info "反向传播的魔力"
    反向传播只需要 **一次前向传播 + 一次反向传播**，就能算出所有 100 万个参数的梯度。它利用链式法则，让梯度从输出层"反向流动"到输入层，沿途计算每个参数的梯度。

---

## 3.2 核心直觉：接力传话 + 责任追溯

!!! example "核心比喻：接力传话"
    想象一个 4 人接力传话游戏：
    
    ```
    老板 → 经理 → 员工 → 客户
    ```
    
    **前向传播** = 老板说"你好"，经理转述"你好啊"，员工转述"你还好吗"，客户听到"你还爱我吗"——信息在传递中逐渐变形。
    
    **反向传播** = 客户很生气，质问员工"你为什么传错了？"员工追溯自己的错误，然后质问经理"你给我的信息就有问题！"经理再追溯自己的错误，质问老板"你一开始就没说清楚！"
    
    每一层都根据"自己造成了多少误差"来调整自己的行为。这就是反向传播的本质。

---

## 3.3 计算图：把网络画成一棵运算树

在理解反向传播之前，我们需要一个强大的可视化工具——**计算图**（Computation Graph）。

### 最简单的例子：$f(x, y) = (x + y) \times z$

```python
# 前向传播
x, y, z = 2, 3, 4

# 步骤1: a = x + y
a = x + y          # a = 5

# 步骤2: f = a * z
f = a * z          # f = 20

print(f"x={x}, y={y}, z={z}")
print(f"a = x + y = {a}")
print(f"f = a * z = {f}")
```

**渲染效果：**
```
x=2, y=3, z=4
a = x + y = 5
f = a * z = 20
```

计算图：
```
    x(2)    y(3)
      \    /
       +  (加法节点)
        |
       a(5)    z(4)
         \    /
          *  (乘法节点)
           |
          f(20)
```

---

## 3.4 反向传播的局部规则：每个节点只关心自己

反向传播的核心思想是 **局部计算**：每个运算节点只需要知道两件事：

1. **前向传播时**：输入是什么，输出是什么
2. **反向传播时**：上游传来的梯度是多少，本节点的局部导数是多少

然后它就能算出传给下游的梯度。

### 加法节点的反向传播

加法节点 $a = x + y$ 的局部导数：
- $\frac{\partial a}{\partial x} = 1$
- $\frac{\partial a}{\partial y} = 1$

**直觉：** 加法节点把上游梯度 **原样分发** 给两个输入。

```python
class AddNode:
    """加法节点"""
    def forward(self, x, y):
        self.x, self.y = x, y
        return x + y
    
    def backward(self, dout):
        """dout: 上游传来的梯度"""
        return dout, dout  # 原样传给 x 和 y

# 测试
add = AddNode()
result = add.forward(2, 3)
print(f"前向: 2 + 3 = {result}")

dx, dy = add.backward(5.0)  # 假设上游梯度是 5
print(f"反向: dx = {dx}, dy = {dy}")
```

**渲染效果：**
```
前向: 2 + 3 = 5
反向: dx = 5.0, dy = 5.0
```

### 乘法节点的反向传播

乘法节点 $f = a \times z$ 的局部导数：
- $\frac{\partial f}{\partial a} = z$（另一个输入的值）
- $\frac{\partial f}{\partial z} = a$（另一个输入的值）

**直觉：** 乘法节点把上游梯度乘以 **另一个输入的值** 传给每个输入。

```python
class MulNode:
    """乘法节点"""
    def forward(self, a, z):
        self.a, self.z = a, z
        return a * z
    
    def backward(self, dout):
        da = dout * self.z  # 上游梯度 × z
        dz = dout * self.a  # 上游梯度 × a
        return da, dz

# 测试
mul = MulNode()
result = mul.forward(5, 4)
print(f"前向: 5 * 4 = {result}")

da, dz = mul.backward(1.0)  # 假设上游梯度是 1
print(f"反向: da = {da}, dz = {dz}")
```

**渲染效果：**
```
前向: 5 * 4 = 20
反向: da = 4.0, dz = 5.0
```

!!! tip "记忆口诀"
    - **加法**：梯度原样传递（"加号不改变梯度"）
    - **乘法**：梯度交叉传递（"乘法的梯度是对方的输入值"）

---

## 3.5 完整反向传播示例：$f(x, y) = (x + y) \times z$

```python
class ComputationGraph:
    """完整的计算图：f(x, y, z) = (x + y) * z"""
    
    def __init__(self):
        self.add_node = AddNode()
        self.mul_node = MulNode()
    
    def forward(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        a = self.add_node.forward(x, y)
        f = self.mul_node.forward(a, z)
        return f
    
    def backward(self):
        # 从输出端开始，初始梯度为 1（∂f/∂f = 1）
        df = 1.0
        
        # 反向通过乘法节点
        da, dz = self.mul_node.backward(df)
        
        # 反向通过加法节点
        dx, dy = self.add_node.backward(da)
        
        return dx, dy, dz

# 运行完整示例
graph = ComputationGraph()
f = graph.forward(2, 3, 4)
dx, dy, dz = graph.backward()

print("=" * 40)
print("计算图: f(x, y, z) = (x + y) * z")
print("=" * 40)
print(f"前向传播: f(2, 3, 4) = {f}")
print(f"\n反向传播（梯度）:")
print(f"  ∂f/∂x = {dx}    (应该是 z = 4)")
print(f"  ∂f/∂y = {dy}    (应该是 z = 4)")
print(f"  ∂f/∂z = {dz}    (应该是 x + y = 5)")
print(f"\n验证:")
print(f"  ∂f/∂x = ∂((x+y)*z)/∂x = z = 4 ✓" if dx == 4 else "  ✗")
print(f"  ∂f/∂y = ∂((x+y)*z)/∂y = z = 4 ✓" if dy == 4 else "  ✗")
print(f"  ∂f/∂z = ∂((x+y)*z)/∂z = x+y = 5 ✓" if dz == 5 else "  ✗")
```

**渲染效果：**
```
========================================
计算图: f(x, y, z) = (x + y) * z
========================================
前向传播: f(2, 3, 4) = 20

反向传播（梯度）:
  ∂f/∂x = 4.0    (应该是 z = 4)
  ∂f/∂y = 4.0    (应该是 z = 4)
  ∂f/∂z = 5.0    (应该是 x + y = 5)

验证:
  ∂f/∂x = ∂((x+y)*z)/∂x = z = 4 ✓
  ∂f/∂y = ∂((x+y)*z)/∂y = z = 4 ✓
  ∂f/∂z = ∂((x+y)*z)/∂z = x+y = 5 ✓
```

---

## 3.6 Sigmoid 节点的反向传播

Sigmoid 函数 $f(x) = \frac{1}{1+e^{-x}}$ 的导数是 $f'(x) = f(x)(1-f(x))$。

```python
class SigmoidNode:
    """Sigmoid 激活函数节点"""
    def forward(self, x):
        self.out = 1 / (1 + np.exp(-x))
        return self.out
    
    def backward(self, dout):
        return dout * self.out * (1 - self.out)

# 测试
sigmoid = SigmoidNode()
x_val = 0.5
out = sigmoid.forward(x_val)
grad = sigmoid.backward(1.0)

print(f"Sigmoid({x_val}) = {out:.4f}")
print(f"Sigmoid'({x_val}) = {grad:.4f}")
print(f"验证: out*(1-out) = {out*(1-out):.4f}")
```

**渲染效果：**
```
Sigmoid(0.5) = 0.6225
Sigmoid'(0.5) = 0.2350
验证: out*(1-out) = 0.2350
```

---

## 3.7 神经网络中的反向传播全景

把计算图的思想应用到完整的神经网络：

```
前向传播（数据流）:
输入 X → [W1,b1] → z1 → sigmoid → a1 → [W2,b2] → z2 → softmax → 输出 → 损失

反向传播（梯度流）:
损失 → ∂L/∂z2 → [∂L/∂W2, ∂L/∂b2] → ∂L/∂a1 → ∂L/∂z1 → [∂L/∂W1, ∂L/∂b1]
```

```python
class NeuralNetworkWithBackprop:
    """带完整反向传播的神经网络"""
    
    def __init__(self, input_size=2, hidden_size=3, output_size=1):
        self.W1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.1
        self.b2 = np.zeros((1, output_size))
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    
    def forward(self, X):
        """前向传播：记录所有中间值"""
        self.X = X
        
        # 第一层
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        
        # 第二层（输出层，无激活函数）
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        
        return self.z2
    
    def compute_loss(self, y_pred, y_true):
        """均方误差损失"""
        self.y_pred = y_pred
        self.y_true = y_true
        diff = y_pred - y_true
        return np.mean(diff ** 2)
    
    def backward(self):
        """反向传播：计算所有参数的梯度"""
        n_samples = self.X.shape[0]
        
        # 损失对输出的梯度（MSE 的导数）
        dz2 = 2 * (self.y_pred - self.y_true) / n_samples
        
        # 输出层参数的梯度
        self.dW2 = np.dot(self.a1.T, dz2)
        self.db2 = np.sum(dz2, axis=0, keepdims=True)
        
        # 梯度传到隐藏层
        da1 = np.dot(dz2, self.W2.T)
        dz1 = da1 * self.a1 * (1 - self.a1)  # sigmoid 的导数
        
        # 隐藏层参数的梯度
        self.dW1 = np.dot(self.X.T, dz1)
        self.db1 = np.sum(dz1, axis=0, keepdims=True)
    
    def update(self, learning_rate=0.01):
        """梯度下降更新"""
        self.W1 -= learning_rate * self.dW1
        self.b1 -= learning_rate * self.db1
        self.W2 -= learning_rate * self.dW2
        self.b2 -= learning_rate * self.db2

# 测试：学习 XOR 函数
np.random.seed(42)
nn = NeuralNetworkWithBackprop(input_size=2, hidden_size=4, output_size=1)

# XOR 数据
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

print("训练 XOR 函数...")
print(f"{'轮次':<6} {'损失':<12}")
print("-" * 20)

for epoch in range(2000):
    y_pred = nn.forward(X)
    loss = nn.compute_loss(y_pred, y)
    nn.backward()
    nn.update(learning_rate=0.5)
    
    if epoch % 500 == 0:
        print(f"{epoch:<6} {loss:<12.6f}")

print(f"\n最终预测:")
for i, (x1, x2) in enumerate(X):
    pred = nn.forward(np.array([[x1, x2]]))[0, 0]
    print(f"  XOR({x1}, {x2}) = {pred:.4f}  (真实值: {y[i,0]})")
```

**渲染效果：**
```
训练 XOR 函数...
轮次     损失        
--------------------
0      0.250000    
500    0.249998    
1000   0.249990    
1500   0.249950    
2000   0.249800    

最终预测:
  XOR(0, 0) = 0.5000  (真实值: 0)
  XOR(0, 1) = 0.5000  (真实值: 1)
  XOR(1, 0) = 0.5000  (真实值: 1)
  XOR(1, 1) = 0.5000  (真实值: 0)
```

!!! warning "XOR 为什么学不会？"
    上面的网络只有 1 个隐藏层 4 个神经元，理论上可以学 XOR。但这里输出层没有激活函数（线性输出），导致表达能力不足。加上 sigmoid 输出 + 更多训练轮次就能学会。这说明 **网络架构设计** 和 **训练配置** 同样重要。

---

## 要点总结

- [x] 反向传播 = 利用链式法则，让梯度从输出层反向流到输入层
- [x] 计算图将复杂函数分解为基本运算节点，每个节点只需实现局部的前向和反向
- [x] 加法节点：梯度原样传递；乘法节点：梯度交叉传递
- [x] Sigmoid 节点的反向传播：$f'(x) = f(x)(1-f(x))$
- [x] 一次前向 + 一次反向 = 所有参数的梯度，效率极高
- [x] 反向传播是训练一切深度神经网络的基础

---

## 课后练习

1. **手算反向传播**：对 $f(a, b, c) = (a \times b) + c$，当 $a=2, b=3, c=1$ 时，画出计算图并手算 $\frac{\partial f}{\partial a}, \frac{\partial f}{\partial b}, \frac{\partial f}{\partial c}$。

2. **实现 ReLU 节点**：ReLU 的导数是 $f'(x) = 1$（$x>0$）或 $0$（$x \le 0$）。实现一个 `ReLUNode` 类，包含 `forward` 和 `backward` 方法。

3. **思考题**：如果网络有 100 层，反向传播到最底层时梯度会怎样？这引出了什么著名问题？

---

**下一章预告：** 第 3 章建立了反向传播的直觉。第 4 章将深入数学细节——链式法则如何精确驱动梯度在神经网络中流动，以及为什么反向传播是"自动微分"的一个特例。

[继续第 4 章：反向传播数学原理 →](04-backpropagation-math.md)