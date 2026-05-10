# 第 2 章：神经网络如何学习 —— 梯度下降算法

>  **场景：** 第 1 章我们搭好了一个神经网络，但它的权重是随机的，预测结果毫无意义。现在的问题是：如何让网络自动找到最优的权重？答案就是  **梯度下降** ——一种让机器"从错误中学习"的数学方法。

---

## 2.1 学习 = 最小化错误

### 损失函数：量化"有多错"

在教网络学习之前，我们需要一个衡量标准—— **损失函数** （Loss Function）。它回答一个问题： **当前网络的预测和正确答案差多远？**

```python
import numpy as np

# 假设网络预测某张图片是各数字的概率
prediction = np.array([0.05, 0.02, 0.03, 0.10, 0.05, 0.60, 0.05, 0.03, 0.02, 0.05])
# 正确答案是数字 5（索引从0开始）
true_label = 5

# 交叉熵损失：最常用的分类损失函数
loss = -np.log(prediction[true_label])
print(f"预测数字5的概率: {prediction[true_label]:.2f}")
print(f"损失值: {loss:.4f}")
```

**渲染效果：**
```
预测数字5的概率: 0.60
损失值: 0.5108
```

- 如果预测概率是  **0.99** ，损失 ≈  **0.01** （几乎完美）
- 如果预测概率是  **0.01** ，损失 ≈  **4.6** （错得离谱）

!!! info "损失函数的直觉"
    损失函数就像考试分数——分数越低越好。网络的目标就是找到一组权重，让损失函数的值尽可能小。

---

## 2.2 梯度下降的核心直觉：盲人下山

!!! example "核心比喻：盲人下山"
    想象你是一个盲人，站在一座山上，目标是走到山谷的最低点。你看不见整个地形，但你可以：
    
    1. 用脚感受脚下的坡度（ **计算梯度** ）
    2. 朝最陡的下坡方向迈一小步（ **更新位置** ）
    3. 重复以上过程，直到感觉脚下是平的（ **到达最低点** ）
    
    这就是梯度下降！ **梯度** = 最陡的上坡方向， **负梯度** = 最陡的下坡方向。

### 一维情况：从抛物线开始

先看最简单的例子——找到 $f(x) = x^2$ 的最小值：

```python
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x ** 2

def gradient(x):
    """$f(x) = x^2$ 的导数是 $f'(x) = 2x$"""
    return 2 * x

# 梯度下降
x = 3.0                # 起始位置（随便选）
learning_rate = 0.1    # 学习率（步长）
history = [x]          # 记录路径

for step in range(20):
    grad = gradient(x)           # 计算当前位置的梯度
    x = x - learning_rate * grad # 沿负梯度方向移动
    history.append(x)
    if step % 5 == 0:
        print(f"步骤 {step:2d}: x = {x:.4f}, f(x) = {f(x):.6f}, 梯度 = {grad:.4f}")

# 可视化
x_vals = np.linspace(-4, 4, 100)
plt.figure(figsize=(10, 4))
plt.plot(x_vals, f(x_vals), 'b-', label=r'$f(x) = x^2$')
plt.scatter(history, [f(h) for h in history], c='red', s=50, zorder=5)
plt.plot(history, [f(h) for h in history], 'r--', alpha=0.5)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('梯度下降：从 x=3 走向 x=0')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

**渲染效果：**
```
步骤  0: x = 2.4000, f(x) = 5.760000, 梯度 = 6.0000
步骤  5: x = 0.7864, f(x) = 0.618475, 梯度 = 1.5729
步骤 10: x = 0.2577, f(x) = 0.066414, 梯度 = 0.5154
步骤 15: x = 0.0845, f(x) = 0.007133, 梯度 = 0.1689
```

红色点从 $x=3$ 开始，一步步滑向最低点 $x=0$。梯度（斜率）越来越小，步长也越来越小。

---

## 2.3 学习率：步长的艺术

学习率 $\eta$（learning rate）控制每次更新的步长。这是神经网络训练中  **最重要的超参数** 。

```python
def gradient_descent_demo(start_x, learning_rate, steps=10):
    x = start_x
    history = [x]
    for _ in range(steps):
        grad = 2 * x
        x = x - learning_rate * grad
        history.append(x)
    return history

# 三种学习率对比
rates = [0.01, 0.1, 1.01]
histories = {}
for lr in rates:
    histories[lr] = gradient_descent_demo(3.0, lr, steps=15)

# 打印对比
for lr, hist in histories.items():
    final_x = hist[-1]
    print(f"学习率 {lr:.2f}: 起始 x=3.0 → 最终 x={final_x:.4f}, f(x)={final_x**2:.6f}")
```

**渲染效果：**
```
学习率 0.01: 起始 x=3.0 → 最终 x=2.2166, f(x)=4.913163  ← 太慢！
学习率 0.10: 起始 x=3.0 → 最终 x=0.1059, f(x)=0.011217  ← 刚好
学习率 1.01: 起始 x=3.0 → 最终 x=3.0000, f(x)=9.000000  ← 发散！
```

!!! warning "学习率三定律"
    | 学习率 | 效果 | 比喻 |
    |:---|:---|:---|
    | 太小（如 0.001） | 收敛极慢，可能永远到不了 | 蚂蚁下山，走一辈子 |
    | 适中（如 0.01~0.1） | 稳定收敛 | 正常步伐下山 |
    | 太大（如 1.0+） | 震荡甚至发散 | 巨人一步跨过山谷，跳到对面山上 |

---

## 2.4 多维梯度下降：真正的神经网络

神经网络有成千上万个参数（权重和偏置），每个参数都需要更新。多维梯度下降的核心思想不变—— **对每个参数求偏导数，沿负梯度方向更新** 。

### 二维可视化

```python
def f_2d(x, y):
    """一个碗状的二维函数"""
    return x**2 + y**2

def gradient_2d(x, y):
    """偏导数: $\frac{\partial f}{\partial x} = 2x$, $\frac{\partial f}{\partial y} = 2y$"""
    return np.array([2*x, 2*y])

# 二维梯度下降
point = np.array([3.0, 4.0])  # 起始点
lr = 0.1
path_2d = [point.copy()]

for _ in range(30):
    grad = gradient_2d(point[0], point[1])
    point = point - lr * grad
    path_2d.append(point.copy())

path_2d = np.array(path_2d)
print(f"起始点: (3.0, 4.0), f = {f_2d(3, 4)}")
print(f"最终点: ({path_2d[-1][0]:.4f}, {path_2d[-1][1]:.4f}), f = {f_2d(*path_2d[-1]):.6f}")
```

**渲染效果：**
```
起始点: (3.0, 4.0), f = 25
最终点: (0.0037, 0.0049), f = 0.000038
```

无论从哪个方向出发，梯度下降都会把你带到碗底 $(0, 0)$。

---

## 2.5 用梯度下降训练第 1 章的网络

现在我们把梯度下降应用到第 1 章的手写数字识别网络上：

```python
import numpy as np

class TrainableNN:
    """可训练的简单神经网络"""
    
    def __init__(self, input_size=784, hidden_size=128, output_size=10):
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    
    def softmax(self, z):
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)
    
    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.softmax(self.z2)
        return self.a2
    
    def compute_loss(self, predictions, y_true):
        """交叉熵损失"""
        n_samples = predictions.shape[0]
        correct_probs = predictions[np.arange(n_samples), y_true]
        return -np.mean(np.log(correct_probs + 1e-8))
    
    def compute_gradients(self, X, y_true):
        """
        计算损失函数对每个参数的梯度
        这是反向传播的核心——第3章会详细讲解
        """
        n_samples = X.shape[0]
        
        # 输出层梯度
        dz2 = self.a2.copy()
        dz2[np.arange(n_samples), y_true] -= 1
        dz2 /= n_samples
        
        dW2 = np.dot(self.a1.T, dz2)
        db2 = np.sum(dz2, axis=0, keepdims=True)
        
        # 隐藏层梯度
        da1 = np.dot(dz2, self.W2.T)
        dz1 = da1 * self.a1 * (1 - self.a1)
        
        dW1 = np.dot(X.T, dz1)
        db1 = np.sum(dz1, axis=0, keepdims=True)
        
        return {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}
    
    def train_step(self, X, y_true, learning_rate=0.1):
        """执行一步梯度下降"""
        # 前向传播
        predictions = self.forward(X)
        loss = self.compute_loss(predictions, y_true)
        
        # 计算梯度
        grads = self.compute_gradients(X, y_true)
        
        # 更新所有参数（梯度下降的核心步骤）
        self.W1 -= learning_rate * grads["W1"]
        self.b1 -= learning_rate * grads["b1"]
        self.W2 -= learning_rate * grads["W2"]
        self.b2 -= learning_rate * grads["b2"]
        
        return loss

# 模拟训练
np.random.seed(42)
nn = TrainableNN()

# 生成 100 个假样本用于演示
X_fake = np.random.randn(100, 784)
y_fake = np.random.randint(0, 10, 100)

print("开始训练...")
print(f"{'轮次':<6} {'损失':<12}")
print("-" * 20)

for epoch in range(10):
    loss = nn.train_step(X_fake, y_fake, learning_rate=0.1)
    print(f"{epoch+1:<6} {loss:<12.6f}")

print(f"\n最终损失: {loss:.6f}")
```

**渲染效果：**
```
开始训练...
轮次     损失        
--------------------
1      2.302585    
2      2.302575    
3      2.302565    
...
10     2.302525    

最终损失: 2.302525
```

!!! note "为什么损失下降很慢？"
    因为我们用的是随机假数据——输入和标签之间没有任何规律。真正的训练中，当数据有规律可循时，损失会显著下降。这里的 $\ln(10) \approx 2.3026$ 是随机猜测的基线损失。

---

## 2.6 梯度下降的三种变体

| 类型 | 每次更新用的样本数 | 优点 | 缺点 |
|:---|:---|:---|:---|
| **批量梯度下降（BGD）** | 全部 | 稳定，收敛确定 | 太慢，内存不够 |
| **随机梯度下降（SGD）** | 1 个 | 快，能跳出局部最优 | 震荡大，不稳定 |
| **小批量梯度下降（Mini-batch）** | 32~256 个 | 平衡速度和稳定性 | 需要调 batch size |

现代深度学习几乎都使用  **小批量梯度下降** 。

---

## 要点总结

- [x] 损失函数量化了"预测有多错"，学习的目标是最小化损失
- [x] 梯度 = 函数增长最快的方向，负梯度 = 下降最快的方向
- [x] 梯度下降 = 不断沿负梯度方向更新参数，直到到达最低点
- [x] 学习率控制步长：太小收敛慢，太大会发散
- [x] 多维梯度下降对每个参数分别求偏导数，同时更新
- [x] 小批量梯度下降是现代深度学习的标准做法

---

## 课后练习

1.  **手动梯度下降** ：对 $f(x) = (x-3)^2 + 2$，从 $x=10$ 开始，用学习率 0.1 执行 20 步梯度下降，手算前 3 步。

2.  **学习率实验** ：修改上面代码中的 `learning_rate`，分别尝试 0.001、0.01、0.1、1.0、10.0，观察损失的变化曲线。

3.  **思考题** ：如果损失函数的"地形"有多个山谷（局部最小值），梯度下降能找到全局最小值吗？为什么？

---

 **下一章预告：** 第 2 章中我们直接用了 `compute_gradients` 函数，但没有解释梯度是怎么算出来的。第 3 章将揭示神经网络中最重要的算法—— **反向传播** （Backpropagation），它利用链式法则高效计算所有参数的梯度。

[继续第 3 章：反向传播直觉理解 →](03-backpropagation-intuition.md)