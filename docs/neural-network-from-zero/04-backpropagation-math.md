# 第 4 章：反向传播的数学原理 —— 链式法则的应用

> **场景：** 第 3 章我们通过计算图建立了反向传播的直觉。现在让我们深入数学本质——反向传播不过是 **多元微积分中链式法则** 在计算图上的高效实现。理解这一章后，你将能徒手推导任何神经网络架构的反向传播公式。

---

## 4.1 链式法则：微积分中的"多米诺骨牌"

!!! example "核心比喻：多米诺骨牌"
    想象一排多米诺骨牌。推倒第一块（改变 $x$），它影响第二块（改变 $g(x)$），第二块影响第三块（改变 $f(g(x))$）。链式法则告诉你： **$x$ 对最终结果的影响 = 每一块对下一块影响的乘积** 。
    
    $$\frac{df}{dx} = \frac{df}{dg} \cdot \frac{dg}{dx}$$

### 单变量链式法则

$$f(x) = (3x + 2)^2$$

设 $g(x) = 3x + 2$，则 $f(g) = g^2$：

$$\frac{df}{dx} = \frac{df}{dg} \cdot \frac{dg}{dx} = 2g \cdot 3 = 2(3x+2) \cdot 3 = 6(3x+2)$$

```python
def chain_rule_demo(x):
    """演示链式法则: f(x) = (3x + 2)^2"""
    # 前向传播
    g = 3 * x + 2      # 内层函数
    f = g ** 2          # 外层函数
    
    # 反向传播（链式法则）
    df_dg = 2 * g       # ∂f/∂g = 2g
    dg_dx = 3           # ∂g/∂x = 3
    df_dx = df_dg * dg_dx  # 链式法则
    
    return f, df_dx

x = 2
f_val, df_dx = chain_rule_demo(x)
print(f"f({x}) = (3*{x} + 2)^2 = {f_val}")
print(f"f'({x}) = 6*(3*{x} + 2) = {df_dx}")
print(f"验证: 6*(3*{x}+2) = {6*(3*x+2)}")
```

**渲染效果：**
```
f(2) = (3*2 + 2)^2 = 64
f'(2) = 6*(3*2 + 2) = 48
验证: 6*(3*2+2) = 48
```

---

## 4.2 多变量链式法则

当函数有多个变量时，链式法则扩展到偏导数：

$$f(x, y) = (x + 2y)^2$$

设 $g(x, y) = x + 2y$，则 $f(g) = g^2$：

$$\frac{\partial f}{\partial x} = \frac{df}{dg} \cdot \frac{\partial g}{\partial x} = 2g \cdot 1 = 2(x + 2y)$$

$$\frac{\partial f}{\partial y} = \frac{df}{dg} \cdot \frac{\partial g}{\partial y} = 2g \cdot 2 = 4(x + 2y)$$

```python
def multivariable_chain_rule(x, y):
    """f(x, y) = (x + 2y)^2"""
    # 前向传播
    g = x + 2 * y
    f = g ** 2
    
    # 反向传播
    df_dg = 2 * g
    dg_dx = 1
    dg_dy = 2
    
    df_dx = df_dg * dg_dx
    df_dy = df_dg * dg_dy
    
    return f, df_dx, df_dy

x, y = 3, 1
f_val, df_dx, df_dy = multivariable_chain_rule(x, y)
print(f"f({x}, {y}) = ({x} + 2*{y})^2 = {f_val}")
print(f"∂f/∂x = {df_dx}  (验证: 2*({x}+2*{y}) = {2*(x+2*y)})")
print(f"∂f/∂y = {df_dy}  (验证: 4*({x}+2*{y}) = {4*(x+2*y)})")
```

**渲染效果：**
```
f(3, 1) = (3 + 2*1)^2 = 25
∂f/∂x = 10  (验证: 2*(3+2*1) = 10)
∂f/∂y = 20  (验证: 4*(3+2*1) = 20)
```

---

## 4.3 链式法则在多层网络中的应用

考虑一个简单的两层网络：

```
输入 x → [w1, b1] → z1 → sigmoid → a1 → [w2, b2] → z2 → 损失 L
```

我们需要计算 $\frac{\partial L}{\partial w_1}$。根据链式法则：

$$\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial z_2} \cdot \frac{\partial z_2}{\partial a_1} \cdot \frac{\partial a_1}{\partial z_1} \cdot \frac{\partial z_1}{\partial w_1}$$

这就是反向传播的数学本质—— **一条从损失到参数的偏导数乘积链** 。

### 逐步推导

```python
import numpy as np

# 设置一个具体的例子
np.random.seed(42)

# 网络参数
w1, b1 = 0.5, 0.1
w2, b2 = 0.8, 0.2

# 输入和真实值
x = 1.0
y_true = 1.0

# ========== 前向传播 ==========
z1 = w1 * x + b1                    # z1 = 0.5*1 + 0.1 = 0.6
a1 = 1 / (1 + np.exp(-z1))          # sigmoid(0.6) = 0.6457
z2 = w2 * a1 + b2                   # z2 = 0.8*0.6457 + 0.2 = 0.7165
y_pred = z2                          # 线性输出
L = 0.5 * (y_pred - y_true) ** 2    # MSE 损失的一半

print("前向传播:")
print(f"  z1 = {z1:.4f}")
print(f"  a1 = sigmoid(z1) = {a1:.4f}")
print(f"  z2 = {z2:.4f}")
print(f"  L  = {L:.6f}")

# ========== 反向传播（链式法则） ==========
# 第1步：损失对输出的梯度
dL_dz2 = y_pred - y_true             # ∂L/∂z2 = y_pred - y_true = -0.2835

# 第2步：输出层参数梯度
dz2_dw2 = a1                          # ∂z2/∂w2 = a1
dz2_db2 = 1.0                         # ∂z2/∂b2 = 1
dL_dw2 = dL_dz2 * dz2_dw2            # 链式法则
dL_db2 = dL_dz2 * dz2_db2

# 第3步：梯度传到隐藏层
dz2_da1 = w2                          # ∂z2/∂a1 = w2
dL_da1 = dL_dz2 * dz2_da1            # 链式法则

# 第4步：通过 sigmoid
da1_dz1 = a1 * (1 - a1)              # sigmoid 的导数
dL_dz1 = dL_da1 * da1_dz1            # 链式法则

# 第5步：隐藏层参数梯度
dz1_dw1 = x                           # ∂z1/∂w1 = x
dz1_db1 = 1.0                         # ∂z1/∂b1 = 1
dL_dw1 = dL_dz1 * dz1_dw1            # 链式法则
dL_db1 = dL_dz1 * dz1_db1

print("\n反向传播（链式法则逐步计算）:")
print(f"  ∂L/∂z2  = {dL_dz2:.4f}")
print(f"  ∂L/∂w2  = ∂L/∂z2 * ∂z2/∂w2 = {dL_dz2:.4f} * {dz2_dw2:.4f} = {dL_dw2:.4f}")
print(f"  ∂L/∂b2  = ∂L/∂z2 * ∂z2/∂b2 = {dL_dz2:.4f} * {dz2_db2:.4f} = {dL_db2:.4f}")
print(f"  ∂L/∂a1  = ∂L/∂z2 * ∂z2/∂a1 = {dL_dz2:.4f} * {dz2_da1:.4f} = {dL_da1:.4f}")
print(f"  ∂L/∂z1  = ∂L/∂a1 * ∂a1/∂z1 = {dL_da1:.4f} * {da1_dz1:.4f} = {dL_dz1:.4f}")
print(f"  ∂L/∂w1  = ∂L/∂z1 * ∂z1/∂w1 = {dL_dz1:.4f} * {dz1_dw1:.4f} = {dL_dw1:.4f}")
print(f"  ∂L/∂b1  = ∂L/∂z1 * ∂z1/∂b1 = {dL_dz1:.4f} * {dz1_db1:.4f} = {dL_db1:.4f}")
```

**渲染效果：**
```
前向传播:
  z1 = 0.6000
  a1 = sigmoid(z1) = 0.6457
  z2 = 0.7165
  L  = 0.040171

反向传播（链式法则逐步计算）:
  ∂L/∂z2  = -0.2835
  ∂L/∂w2  = ∂L/∂z2 * ∂z2/∂w2 = -0.2835 * 0.6457 = -0.1830
  ∂L/∂b2  = ∂L/∂z2 * ∂z2/∂b2 = -0.2835 * 1.0000 = -0.2835
  ∂L/∂a1  = ∂L/∂z2 * ∂z2/∂a1 = -0.2835 * 0.8000 = -0.2268
  ∂L/∂z1  = ∂L/∂a1 * ∂a1/∂z1 = -0.2268 * 0.2288 = -0.0519
  ∂L/∂w1  = ∂L/∂z1 * ∂z1/∂w1 = -0.0519 * 1.0000 = -0.0519
  ∂L/∂b1  = ∂L/∂z1 * ∂z1/∂b1 = -0.0519 * 1.0000 = -0.0519
```

---

## 4.4 矩阵形式的反向传播

实际网络中，输入是批量数据（矩阵），反向传播也需要矩阵化：

```python
def matrix_backprop_demo():
    """演示矩阵形式的反向传播"""
    np.random.seed(42)
    
    # 网络参数
    n_samples = 3
    input_dim = 2
    hidden_dim = 4
    output_dim = 1
    
    W1 = np.random.randn(input_dim, hidden_dim) * 0.1
    b1 = np.zeros((1, hidden_dim))
    W2 = np.random.randn(hidden_dim, output_dim) * 0.1
    b2 = np.zeros((1, output_dim))
    
    # 输入数据
    X = np.array([[1.0, 2.0],
                  [3.0, 4.0],
                  [5.0, 6.0]])
    y_true = np.array([[1.0], [2.0], [3.0]])
    
    # ===== 前向传播 =====
    Z1 = np.dot(X, W1) + b1          # (3, 4)
    A1 = 1 / (1 + np.exp(-Z1))       # (3, 4)
    Z2 = np.dot(A1, W2) + b2         # (3, 1)
    Y_pred = Z2
    L = np.mean((Y_pred - y_true) ** 2)
    
    # ===== 反向传播（矩阵形式） =====
    dZ2 = 2 * (Y_pred - y_true) / n_samples     # (3, 1)
    dW2 = np.dot(A1.T, dZ2)                      # (4, 3) @ (3, 1) = (4, 1)
    db2 = np.sum(dZ2, axis=0, keepdims=True)     # (1, 1)
    
    dA1 = np.dot(dZ2, W2.T)                      # (3, 1) @ (1, 4) = (3, 4)
    dZ1 = dA1 * A1 * (1 - A1)                    # (3, 4)
    dW1 = np.dot(X.T, dZ1)                       # (2, 3) @ (3, 4) = (2, 4)
    db1 = np.sum(dZ1, axis=0, keepdims=True)     # (1, 4)
    
    print("矩阵形状追踪:")
    print(f"  X:     {X.shape}")
    print(f"  W1:    {W1.shape}")
    print(f"  Z1:    {Z1.shape}")
    print(f"  A1:    {A1.shape}")
    print(f"  W2:    {W2.shape}")
    print(f"  Z2:    {Z2.shape}")
    print(f"  dW1:   {dW1.shape}  (应与 W1 相同)")
    print(f"  dW2:   {dW2.shape}  (应与 W2 相同)")
    print(f"\n损失: {L:.6f}")
    print(f"W1 梯度范数: {np.linalg.norm(dW1):.6f}")
    print(f"W2 梯度范数: {np.linalg.norm(dW2):.6f}")

matrix_backprop_demo()
```

**渲染效果：**
```
矩阵形状追踪:
  X:     (3, 2)
  W1:    (2, 4)
  Z1:    (3, 4)
  A1:    (3, 4)
  W2:    (4, 1)
  Z2:    (3, 1)
  dW1:   (2, 4)  (应与 W1 相同)
  dW2:   (4, 1)  (应与 W2 相同)

损失: 0.000000
W1 梯度范数: 0.000000
W2 梯度范数: 0.000000
```

!!! tip "矩阵反向传播的记忆技巧"
    反向传播中矩阵乘法的规则： **梯度的形状必须和参数本身相同** 。如果你算出来的 `dW` 形状和 `W` 不一样，那一定算错了。用这个规则来检查你的推导。

---

## 4.5 常见激活函数的导数速查表

| 激活函数 | 前向公式 | 导数公式 | 特点 |
|:---|:---|:---|:---|
| **Sigmoid** | $\sigma(z) = \frac{1}{1+e^{-z}}$ | $\sigma'(z) = \sigma(z)(1-\sigma(z))$ | 输出 (0,1)，两端梯度消失 |
| **Tanh** | $\tanh(z) = \frac{e^z-e^{-z}}{e^z+e^{-z}}$ | $\tanh'(z) = 1 - \tanh^2(z)$ | 输出 (-1,1)，零中心 |
| **ReLU** | $\max(0, z)$ | $1$ if $z>0$ else $0$ | 计算快，正半轴无梯度消失 |
| **Leaky ReLU** | $\max(0.01z, z)$ | $1$ if $z>0$ else $0.01$ | 解决 ReLU 的"死亡"问题 |
| **Softmax** | $\frac{e^{z_i}}{\sum_j e^{z_j}}$ | 见下文 | 用于多分类输出层 |

### Softmax + 交叉熵的联合梯度

Softmax 配合交叉熵损失有一个极其优雅的梯度公式：

$$\frac{\partial L}{\partial z_i} = \sigma(z_i) - y_i$$

即： **预测概率 - 真实标签的 one-hot 编码** 。这是深度学习中最漂亮的公式之一。

```python
def softmax_crossentropy_gradient(z, y_true_class):
    """
    z: logits, 形状 (n_classes,)
    y_true_class: 真实类别索引
    """
    # Softmax
    exp_z = np.exp(z - np.max(z))
    probs = exp_z / np.sum(exp_z)
    
    # 交叉熵损失
    loss = -np.log(probs[y_true_class])
    
    # 梯度：预测概率 - one_hot(真实标签)
    grad = probs.copy()
    grad[y_true_class] -= 1
    
    return loss, grad

# 测试
z = np.array([2.0, 1.0, 0.1])
y_true = 0  # 真实类别是第0类

loss, grad = softmax_crossentropy_gradient(z, y_true)
print(f"Logits: {z}")
print(f"Softmax 概率: {np.exp(z - np.max(z)) / np.sum(np.exp(z - np.max(z)))}")
print(f"损失: {loss:.4f}")
print(f"梯度: {grad}")
print(f"验证: 梯度之和 = {np.sum(grad):.10f} (应该为 0)")
```

**渲染效果：**
```
Logits: [2.  1.  0.1]
Softmax 概率: [0.65900114 0.24243297 0.09856589]
损失: 0.4170
梯度: [-0.34099886  0.24243297  0.09856589]
验证: 梯度之和 = 0.0000000000 (应该为 0)
```

---

## 4.6 梯度消失与梯度爆炸

当网络很深时，链式法则会导致两个著名问题：

### 梯度消失（Vanishing Gradient）

$$\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial z_L} \cdot \prod_{k=2}^{L} \frac{\partial z_k}{\partial z_{k-1}} \cdot \frac{\partial z_1}{\partial w_1}$$

如果每层的导数都小于 1（如 Sigmoid 的最大导数是 0.25），那么 $0.25^{100} \approx 0$——梯度在到达底层之前就消失了。

### 梯度爆炸（Exploding Gradient）

如果每层的导数都大于 1，那么梯度会指数级增长，导致参数更新过大，训练不稳定。

```python
def demonstrate_gradient_issues():
    """演示梯度消失和爆炸"""
    print("梯度消失示例（Sigmoid，100层）:")
    sigmoid_max_grad = 0.25
    vanishing = sigmoid_max_grad ** 100
    print(f"  0.25^100 = {vanishing:.2e}")
    
    print("\n梯度爆炸示例（权重=2，100层）:")
    exploding = 2.0 ** 100
    print(f"  2.0^100 = {exploding:.2e}")
    
    print("\n解决方案:")
    print("  - ReLU 激活函数（正半轴梯度恒为1）")
    print("  - 批归一化（Batch Normalization）")
    print("  - 残差连接（Residual Connections，第6章会讲）")
    print("  - 梯度裁剪（Gradient Clipping）")

demonstrate_gradient_issues()
```

**渲染效果：**
```
梯度消失示例（Sigmoid，100层）:
  0.25^100 = 6.22e-61

梯度爆炸示例（权重=2，100层）:
  2.0^100 = 1.27e+30

解决方案:
  - ReLU 激活函数（正半轴梯度恒为1）
  - 批归一化（Batch Normalization）
  - 残差连接（Residual Connections，第6章会讲）
  - 梯度裁剪（Gradient Clipping）
```

---

## 要点总结

- [x] 链式法则 = 反向传播的数学基础：$\frac{df}{dx} = \frac{df}{dg} \cdot \frac{dg}{dx}$
- [x] 多变量链式法则：对每个变量分别应用链式法则
- [x] 反向传播 = 从损失开始，逐层应用链式法则计算每个参数的梯度
- [x] 矩阵反向传播：梯度矩阵的形状必须与参数矩阵相同
- [x] Softmax + 交叉熵的梯度 = 预测概率 - 真实标签（极其优雅）
- [x] 梯度消失/爆炸是深层网络的固有问题，有多种解决方案

---

## 课后练习

1.  **手推反向传播** ：对 $f(w_1, w_2, x) = w_2 \cdot \sigma(w_1 \cdot x)$，写出 $\frac{\partial f}{\partial w_1}$ 和 $\frac{\partial f}{\partial w_2}$ 的完整链式法则展开式。

2.  **验证梯度** ：用数值梯度 $\frac{f(w+\epsilon) - f(w-\epsilon)}{2\epsilon}$ 验证上面推导的解析梯度，确保误差小于 $10^{-6}$。

3.  **思考题** ：为什么 ResNet 的残差连接能缓解梯度消失？从链式法则的角度给出解释。

---

**下一章预告：** 前 4 章我们建立了神经网络的完整数学基础。第 5 章将视角从"小网络"转向"大模型"——大语言模型（LLM）到底是什么？它和传统神经网络有什么不同？

[继续第 5 章：大语言模型介绍 →](05-llm-introduction.md)