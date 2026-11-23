# 第 13 章：介绍自动优化：搭建深度学习框架

前面几章的 NumPy 代码已经能完成预测、计算误差、反向传播和参数更新，但每增加一层，就要手动写一组新的变量和梯度。代码能跑不等于结构清楚：如果前向和反向的顺序错了，模型可能仍然输出数字，却无法正确学习。

本章不急着使用 PyTorch，而是先搭一个足够小的深度学习框架，理解框架到底替我们管理了什么。

## 本章要解决的问题

一个训练步骤至少包含六个角色：

```text
数据 → 层的前向传播 → 损失 → 损失反向传播 → 各层反向传播 → 优化器更新参数
```

如果把这些逻辑全部写在一个大函数里，会出现三个问题：

- 很难替换某一层。
- 很难确认梯度属于哪个参数。
- 很难在训练、验证和推理之间复用同一套模型。

本章完成后，你应该能够：

- 说清楚一个层的 `forward`、`backward`、参数和梯度分别负责什么。
- 用 NumPy 写一个最小线性层、ReLU 层和 SGD 优化器。
- 解释为什么反向传播必须先缓存前向计算中的中间值。
- 把训练循环拆成可检查的阶段，而不是依赖“黑盒训练”。

## 1. 层的最小接口

把神经网络想成一条加工流水线。每个层知道如何加工输入，也知道当上游说“输出应该往哪个方向改变”时，如何把责任传回输入和参数。

| 接口 | 作用 | 典型输入/输出 |
|:---|:---|:---|
| `forward(x)` | 根据输入产生输出 | `x → y` |
| `backward(grad_y)` | 接收输出梯度并向前传递 | `dL/dy → dL/dx` |
| `params` | 保存可学习参数 | `W`、`b` |
| `grads` | 保存参数梯度 | `dL/dW`、`dL/db` |

层不负责决定学习率，也不负责知道整个模型有多少层；它只负责自己的局部计算。这样可以把线性层、激活层和卷积层用同一种训练循环串起来。

## 2. 用 NumPy 写线性层

对于 `x` 形状 `(B, D_in)`、权重 `W` 形状 `(D_in, D_out)` 和偏置 `b` 形状 `(D_out,)`：

$$
y=xW+b
$$

若上游传来 `grad_y = dL/dy`，则：

$$
\frac{\partial L}{\partial W}=x^T\frac{\partial L}{\partial y},\qquad
\frac{\partial L}{\partial b}=\sum_{batch}\frac{\partial L}{\partial y},\qquad
\frac{\partial L}{\partial x}=\frac{\partial L}{\partial y}W^T
$$

一个最小实现如下：

```python
import numpy as np


class Linear:
    def __init__(self, in_features, out_features, seed=0):
        rng = np.random.default_rng(seed)
        self.W = rng.normal(0, 0.1, (in_features, out_features))
        self.b = np.zeros(out_features)
        self.x = None
        self.grad_W = np.zeros_like(self.W)
        self.grad_b = np.zeros_like(self.b)

    def forward(self, x):
        self.x = x
        return x @ self.W + self.b

    def backward(self, grad_y):
        self.grad_W = self.x.T @ grad_y
        self.grad_b = grad_y.sum(axis=0)
        return grad_y @ self.W.T

    def parameters(self):
        return [(self.W, self.grad_W), (self.b, self.grad_b)]
```

`self.x` 是缓存。反向传播需要它来计算 `x.T @ grad_y`；如果只保存输出而没有保存输入，就无法在之后还原这一步的局部梯度。

## 3. ReLU 层和梯度开关

ReLU 的前向计算是：

$$
f(x)=\max(0,x)
$$

它的梯度在正数处为 1，在负数处为 0。实现时要缓存输入或布尔掩码：

```python
class ReLU:
    def __init__(self):
        self.mask = None

    def forward(self, x):
        self.mask = x > 0
        return np.maximum(x, 0)

    def backward(self, grad_y):
        return grad_y * self.mask

    def parameters(self):
        return []
```

ReLU 没有可学习参数，但仍然需要参与反向传播。不要把“没有参数”和“不需要 backward”混为一谈。

## 4. 优化器只做更新

层保存参数和梯度，优化器根据它们更新数值。最小 SGD 可以写成：

```python
class SGD:
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate

    def step(self, layers):
        for layer in layers:
            for parameter, gradient in layer.parameters():
                parameter -= self.learning_rate * gradient

    @staticmethod
    def zero_grad(layers):
        for layer in layers:
            for _, gradient in layer.parameters():
                gradient[...] = 0
```

这里把 `zero_grad` 单独写出来，是为了强调梯度是累积存储的。如果一个批次结束后不清零，下一批次会混入上一个批次的梯度，学习率的实际效果也会随批次数量改变。

## 5. 完整训练循环

假设模型由 `Linear → ReLU → Linear` 组成，一次训练可以明确写成：

```python
layers = [Linear(2, 4, seed=1), ReLU(), Linear(4, 1, seed=2)]
optimizer = SGD(learning_rate=0.05)

for step in range(100):
    prediction = features
    for layer in layers:
        prediction = layer.forward(prediction)

    loss = ((prediction - targets) ** 2).mean()
    grad = 2 * (prediction - targets) / targets.size

    for layer in reversed(layers):
        grad = layer.backward(grad)

    optimizer.step(layers)
    optimizer.zero_grad(layers)
```

这个版本没有自动求导，但已经出现了现代框架的核心结构：模块组合、缓存、反向传播、参数收集、优化器和梯度清零。框架做的事情，本质上是把这些容易重复、容易漏写的管理工作统一起来。

## 6. 先测局部，再测整体

建议按下面顺序验收：


1. 给 `Linear` 一个 `(3, 2)` 输入，检查输出是不是 `(3, 4)`。
2. 给 `backward` 一个 `(3, 4)` 梯度，检查返回值是不是 `(3, 2)`。
3. 用有限差分检查一个 `W[i, j]` 的梯度。
4. 让一个两层网络拟合少量合成数据，确认损失总体下降。
5. 把学习率改得很大，观察损失发散，从而确认优化器确实改变了参数。

有限差分的基本思想是：

$$
\frac{\partial L}{\partial w}\approx\frac{L(w+\epsilon)-L(w-\epsilon)}{2\epsilon}
$$

它不是高效训练方法，却是检查手写反向传播的好工具。

## 7. 常见错误

- **层之间的接口不一致**：上一层输出 `(B, D)`，下一层却按 `(D, B)` 解释。
- **反向传播顺序没有反转**：梯度必须从损失开始，沿前向路径的反方向传播。
- **忘记缓存输入**：线性层和 ReLU 的局部梯度都依赖前向阶段的信息。
- **梯度没有清零**：梯度累积有时是有意的，但这里的每个批次都应明确选择是否累积。
- **把参数更新写进层的 backward**：这样会让梯度计算和优化策略耦合，难以切换 SGD、Momentum 或 Adam。
- **只看训练损失**：框架能把训练损失降下来，不代表验证数据上的表现也变好。

## 动手任务

实现一个 `Sequential` 容器，让它接收任意层列表并提供 `forward`、`backward` 和 `parameters`。然后用它组合两层网络，完成一个小型回归问题。

最低验收标准：

- 能打印每层前向和反向的形状。
- 能证明更新前后至少一个参数发生改变。
- 能用有限差分核对一个参数梯度。
- 能说明 `zero_grad` 放在更新前和更新后分别有什么影响。

## 本章验收

1. 为什么层需要同时提供前向和反向接口？
2. 为什么优化器不应该把某一层写死？
3. `x.T @ grad_y` 为什么得到的是 `W` 的形状？
4. 如果不缓存前向输入，线性层的 `grad_W` 如何计算？
5. 自动求导框架替你隐藏了哪些步骤，但没有替你解决哪些建模问题？

完成后进入[第 14 章：学习像莎士比亚一样写作](14-long-short-term-memory.md)，把“状态传递”的想法推进到更能保留长期信息的 LSTM。

## 一句话复述

深度学习框架不是魔法，而是把层的局部计算、梯度管理和参数更新组织成可复用的训练循环。

