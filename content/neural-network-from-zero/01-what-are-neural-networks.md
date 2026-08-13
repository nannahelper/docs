# 第 1 章：什么是神经网络 —— 从神经元到深度网络

> **场景：** 你面前有一堆照片，需要把它们分成"猫"和"狗"两类。你不可能为每张照片写一条 `if` 规则——猫的耳朵、狗鼻子、毛色千变万化。神经网络解决的就是这类"规则写不出来，但人看一眼就能判断"的问题。让我们从最基本的单元——神经元——开始。

---

## 1.1 生物神经元 vs 人工神经元

### 生物神经元如何工作？

你大脑里有大约 860 亿个神经元。每个神经元的工作方式出奇地简单：

1.  **接收信号** ：树突（dendrites）从其他神经元接收电化学信号
2.  **整合信号** ：细胞体将所有输入信号累加起来
3.  **做出决定** ：如果总信号超过某个阈值，神经元就"放电"（fire），通过轴突（axon）向下一个神经元发送信号
4.  **否则沉默** ：如果没超过阈值，什么都不做

!!! info "关键洞察"
    单个神经元做的事情极其简单——就是"累加 → 判断 → 决定是否输出"。但 860 亿个这样的简单单元组合在一起，就产生了意识。这就是  **涌现** （emergence）：简单规则 + 大规模组合 = 复杂行为。

### 人工神经元：一个数学抽象

1943 年，McCulloch 和 Pitts 把生物神经元抽象成了一个数学模型：

```
输入信号 → 加权求和 → 加偏置 → 激活函数 → 输出
```

用数学公式表示：

$$output = f(w_1 x_1 + w_2 x_2 + \dots + w_n x_n + b)$$

其中：

- $x_1, x_2, ..., x_n$ 是  **输入** （来自其他神经元或原始数据）
- $w_1, w_2, ..., w_n$ 是  **权重** （每个输入的重要性）
- $b$ 是  **偏置** （让神经元更容易或更难被激活）
- $f$ 是  **激活函数** （决定是否"放电"）

!!! example "生活化比喻：投票器"
    想象一个委员会在做决策。每个委员（输入 $x_i$）发表意见，但不是所有委员的话语权都一样——主席的话（高权重 $w_i$）比普通委员（低权重）更有分量。偏置 $b$ 相当于"主席天然倾向于同意"的程度。最后，激活函数 $f$ 就是投票规则：总得分超过某个值就通过，否则否决。

---

## 1.2 用 Python 实现一个神经元

让我们把上面的数学公式变成代码：

```python
import numpy as np

def neuron(inputs, weights, bias, activation="sigmoid"):
    """
    单个人工神经元
    
    参数:
        inputs:  输入信号列表 [x1, x2, ..., xn]
        weights: 权重列表 [w1, w2, ..., wn]
        bias:    偏置值 b
        activation: 激活函数类型
    
    返回:
        神经元的输出值
    """
    # 步骤1：加权求和 + 偏置
    z = np.dot(inputs, weights) + bias
    
    # 步骤2：通过激活函数
    if activation == "sigmoid":
        output = 1 / (1 + np.exp(-z))
    elif activation == "relu":
        output = max(0, z)
    elif activation == "step":
        output = 1 if z > 0 else 0
    else:
        output = z
    
    return output

# 示例：判断一张图片是否是"猫"
# 假设我们有 3 个特征：有尖耳朵(1/0)、有胡须(1/0)、体型小(1/0)
inputs  = np.array([1, 1, 1])      # 尖耳朵=有, 胡须=有, 体型小=是
weights = np.array([0.8, 0.5, 0.3]) # 尖耳朵最重要, 胡须次之, 体型再次之
bias    = -0.5                       # 稍微倾向于"不是猫"

result = neuron(inputs, weights, bias, activation="sigmoid")
print(f"这是猫的概率: {result:.4f}")  # 输出: 这是猫的概率: 0.7503
```

 **渲染效果：** 当输入 `[1, 1, 1]`（尖耳朵 + 有胡须 + 体型小）时，神经元输出约  **0.75** ，表示 75% 的把握认为这是猫。

---

## 1.3 激活函数：神经元的"决策规则"

激活函数决定了神经元在什么条件下"放电"。以下是三种最常用的激活函数：

### Sigmoid：平滑的开关

$$f(z) = \frac{1}{1 + e^{-z}}$$

```python
import numpy as np
import matplotlib.pyplot as plt

z = np.linspace(-10, 10, 100)
sigmoid = 1 / (1 + np.exp(-z))

plt.plot(z, sigmoid)
plt.axhline(y=0.5, color='gray', linestyle='--')
plt.axvline(x=0, color='gray', linestyle='--')
plt.title("Sigmoid 激活函数")
plt.xlabel("z (加权和)")
plt.ylabel("f(z)")
plt.grid(True, alpha=0.3)
plt.show()
```

**渲染效果：** 一条 S 形曲线，$z=0$ 时输出 0.5，$z$ 很大时趋近 1，$z$ 很小时趋近 0。像一个"软开关"。

!!! tip "Sigmoid 的特点"
    - 输出范围 (0, 1)，适合表示概率
    - 在两端梯度接近 0，会导致"梯度消失"问题（第 3 章会讲）
    - 历史上很流行，现代深度网络中较少使用

### ReLU：简单粗暴的过滤器

$$f(z) = \max(0, z)$$

```python
z = np.linspace(-10, 10, 100)
relu = np.maximum(0, z)

plt.plot(z, relu, color='green')
plt.title("ReLU 激活函数")
plt.xlabel("z (加权和)")
plt.ylabel("f(z)")
plt.grid(True, alpha=0.3)
plt.show()
```

**渲染效果：** 一条折线——负数全部变成 0，正数保持不变。简单到只有一行代码。

!!! tip "ReLU 的特点"
    - 计算极快（只是一个 `max` 操作）
    - 不会在正半轴产生梯度消失
    - 是现代深度网络的默认选择
    - 缺点：负数区域梯度为 0（"神经元死亡"问题）

---

## 1.4 从单个神经元到神经网络

单个神经元只能做简单的线性分类。但把很多神经元堆叠起来，就形成了  **神经网络** 。

### 网络结构：层

一个典型的神经网络由三种层组成：

```
输入层          隐藏层          输出层
  ○              ○              ○
  ○    ────     ○    ────     
  ○              ○              ○
  ○              ○              
                 ○              
```

-  **输入层** ：接收原始数据（如图片的像素值），不进行计算
-  **隐藏层** ：进行特征提取和变换，可以有多个
-  **输出层** ：产生最终结果（如"猫"的概率）

!!! example "生活化比喻：层层决策委员会"
    想象一个公司的决策流程：
    
    - **输入层** = 原始信息（市场数据、用户反馈）
    - **隐藏层 1** = 基层经理，每人从不同角度分析原始信息
    - **隐藏层 2** = 中层经理，综合基层的分析做进一步判断
    - **输出层** = CEO，做出最终决策
    
    每一层都在上一层的分析基础上提取更高级的特征。

---

## 1.5 用 NumPy 实现一个完整的神经网络

让我们实现一个能识别手写数字（0-9）的简单网络：

```python
import numpy as np

class SimpleNeuralNetwork:
    """
    一个简单的三层神经网络
    输入层: 784 个神经元 (28x28 像素)
    隐藏层: 128 个神经元
    输出层: 10 个神经元 (数字 0-9)
    """
    
    def __init__(self):
        # 随机初始化权重（小随机数打破对称性）
        self.W1 = np.random.randn(784, 128) * 0.01
        self.b1 = np.zeros((1, 128))
        self.W2 = np.random.randn(128, 10) * 0.01
        self.b2 = np.zeros((1, 10))
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def softmax(self, z):
        """将输出转换为概率分布"""
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)
    
    def forward(self, X):
        """
        前向传播：数据从输入层流向输出层
        
        参数:
            X: 输入数据，形状 (样本数, 784)
        
        返回:
            每个类别的概率，形状 (样本数, 10)
        """
        # 第一层：输入 → 隐藏层
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        
        # 第二层：隐藏层 → 输出层
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.softmax(self.z2)
        
        return self.a2

# 创建一个网络实例
nn = SimpleNeuralNetwork()
print(f"W1 形状: {nn.W1.shape}")  # (784, 128) —— 784个输入连接到128个隐藏神经元
print(f"W2 形状: {nn.W2.shape}")  # (128, 10)  —— 128个隐藏神经元连接到10个输出

# 模拟一张图片（784 个像素值，0-1 之间）
fake_image = np.random.rand(1, 784)
predictions = nn.forward(fake_image)
print(f"\n预测结果（10个数字的概率）:")
for i, prob in enumerate(predictions[0]):
    print(f"  数字 {i}: {prob:.4f}")
print(f"\n网络猜测这是数字: {np.argmax(predictions)}")
```

**渲染效果：**
```
W1 形状: (784, 128)
W2 形状: (128, 10)

预测结果（10个数字的概率）:
  数字 0: 0.1023
  数字 1: 0.0987
  数字 2: 0.1015
  ...
  数字 7: 0.1056  ← 概率最高（但因为是随机权重，每次运行结果不同）

网络猜测这是数字: 7
```

!!! warning "注意"
    此时网络还没有经过训练，权重是随机的，所以预测结果也是随机的。下一章我们将学习如何让网络"学习"——通过梯度下降算法调整权重，使预测越来越准确。

---

## 1.6 PyTorch 实现：更简洁的神经网络

上面的 NumPy 实现让我们理解了网络的底层原理。但在实际项目中，我们使用 PyTorch 来简化开发。下面是 **完全相同的网络** 的 PyTorch 版本：

```python
import torch
import torch.nn as nn

class SimpleNN(nn.Module):
    """与 1.5 节 NumPy 版本完全相同的三层神经网络"""
    def __init__(self):
        super(SimpleNN, self).__init__()
        
        self.fc1 = nn.Linear(784, 128)
        self.sigmoid = nn.Sigmoid()
        self.fc2 = nn.Linear(128, 10)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.sigmoid(x)
        x = self.fc2(x)
        return x

model = SimpleNN()
print(f"模型结构:\n{model}\n")

for name, param in model.named_parameters():
    print(f"{name}: {param.shape}")

fake_image = torch.randn(1, 784)
output = model(fake_image)

probs = torch.softmax(output, dim=1)
predicted = output.argmax(dim=1)

print(f"\n预测结果（10个数字的 logits）: {output}")
print(f"预测结果（10个数字的概率）: {probs}")
print(f"网络猜测这是数字: {predicted.item()}")
```

**运行结果：**
```
模型结构:
SimpleNN(
  (fc1): Linear(in_features=784, out_features=128, bias=True)
  (sigmoid): Sigmoid()
  (fc2): Linear(in_features=128, out_features=10, bias=True)
)

fc1.weight: torch.Size([128, 784])
fc1.bias: torch.Size([128])
fc2.weight: torch.Size([10, 128])
fc2.bias: torch.Size([10])

预测结果（10个数字的 logits）: tensor([[-0.0234,  0.0156, -0.0089, ...]])
预测结果（10个数字的概率）: tensor([[0.0987, 0.1023, 0.0998, ...]])
网络猜测这是数字: 1
```

!!! tip "NumPy vs PyTorch 对比"
    | 操作 | NumPy 实现 | PyTorch 实现 |
    |:---|:---|:---|
    | 定义权重 | `self.W1 = np.random.randn(784, 128)` | `nn.Linear(784, 128)` |
    | 加权求和 | `np.dot(X, self.W1) + self.b1` | `self.fc1(x)` |
    | 激活函数 | `self.sigmoid(self.z1)` | `self.sigmoid(x)` |
    | Softmax | 手动实现 | `torch.softmax(output, dim=1)` |
    | 反向传播 | 手动推导（第 3-4 章） | `loss.backward()` 自动完成 |

    可以看到，PyTorch 将大量样板代码封装成了简洁的 API，让我们专注于网络架构设计。

---

## 1.7 为什么神经网络能工作：通用近似定理

一个令人惊叹的数学事实： **只要隐藏层足够大，一个两层的神经网络可以以任意精度近似任何连续函数。**

!!! info "通用近似定理（Universal Approximation Theorem）"
    1989 年由 Cybenko 和 Hornik 等人证明：一个具有单隐藏层的前馈神经网络，只要隐藏层神经元足够多，就能以任意精度逼近任何连续函数。
    
    这意味着：理论上，神经网络可以学会任何"输入 → 输出"的映射关系——无论是识别猫狗、翻译语言、还是下围棋。

**直觉理解：** 想象你用很多小线段去逼近一条曲线。线段越多，逼近越精确。神经网络中的每个神经元就像一条"线段"（更准确地说，是一个非线性基函数），足够多的神经元组合起来就能逼近任何复杂的决策边界。

---

## 要点总结

- [x] 人工神经元 = 加权求和 + 偏置 + 激活函数，是生物神经元的数学抽象
- [x] 激活函数（Sigmoid、ReLU）引入非线性，让网络能学习复杂模式
- [x] 神经网络 = 多层神经元的堆叠：输入层 → 隐藏层 → 输出层
- [x] 前向传播 = 数据从输入层逐层流向输出层的过程
- [x] 通用近似定理保证了神经网络的理论能力
- [x] 随机权重的网络无法做出有意义的预测——需要"学习"

---

## 课后练习

1.  **修改权重实验** ：在上面的代码中，手动修改 `W1` 和 `W2` 的值，观察输出概率如何变化。你能让网络总是输出数字 3 吗？

2.  **手写神经元** ：不用 NumPy 的 `np.dot`，用纯 Python 的 `for` 循环实现一个神经元，输入 5 个特征，输出 sigmoid 激活后的值。

3.  **思考题** ：如果去掉激活函数（即 $f(z) = z$），多层神经网络会退化成什么？为什么激活函数如此重要？

---

**下一章预告：** 现在你知道了神经网络的结构，但随机权重的网络毫无用处。第 2 章将揭示神经网络如何"学习"——通过梯度下降算法，让网络自动找到最优的权重组合。

[继续第 2 章：梯度下降算法 →](02-gradient-descent.md)