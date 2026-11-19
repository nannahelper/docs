# 第 9 章：建模概率与非线性：激活函数

## 本章要解决的问题

为什么多层网络需要非线性？一组原始分数怎样变成概率？概率和标签之间的差异又怎样进入反向传播？本章把激活函数、Softmax 和交叉熵串成一条可验证的计算链。

## 为什么线性层还不够

如果网络只叠加线性计算，多层线性层仍然可以合并成一个更大的线性变换。没有非线性，网络就很难表达弯曲的决策边界，也无法真正利用“深度”。

激活函数插入在线性层之间，把原始值转换为新的表示。学习它们时不要只记住名称，还要观察输入范围、输出范围、导数大小以及极端输入下的行为。

## 从激活值到概率

分类网络最后通常先输出一组原始分数，也叫 `logits`：

```text
网络最后一层
    ↓
logits：每个类别的原始分数
    ↓ softmax
probabilities：和为 1 的概率分布
    ↓ argmax
predicted_class：预测类别
```

Softmax 的作用是把一行分数转换为概率分布；`argmax` 只负责选出最大值所在的类别。预测类别可以直接对 logits 做 `argmax`，因为 Softmax 不会改变它们的大小顺序。

数值实现时要先减去该行最大值，避免指数运算溢出：

```python
shifted = logits - logits.max(axis=-1, keepdims=True)
exp_scores = np.exp(shifted)
probabilities = exp_scores / exp_scores.sum(axis=-1, keepdims=True)
```

## 交叉熵连接预测与学习

对于 one-hot 标签，交叉熵只关心真实类别的概率：

```text
loss = -log(真实类别对应的概率)
```

模型越确信正确类别，损失越小；如果把很小的概率分给真实类别，损失就会明显变大。Softmax 与交叉熵组合后，logits 的梯度可以简化为：

```python
d_logits = (probabilities - labels) / batch_size
```

这条结果把“预测概率”和“真实标签”的差异直接交给反向传播，是从公式走向代码的重要一步。

## 常见激活函数

| 函数 | 直觉 | 需要注意 |
|:---|:---|:---|
| `tanh` | 把值压到 `[-1, 1]` | 极端输入处梯度可能变小 |
| `sigmoid` | 把值压到 `[0, 1]` | 极端输入容易饱和 |
| `ReLU` | 负数归零，正数保留 | 负区间梯度为零 |
| `softmax` | 把一组分数转成概率 | 沿类别维度计算 |

## 常见错误

- 忘记 Softmax 应该沿类别维度计算，导致不同样本之间相互归一化。
- 直接对很大的 logits 做 `np.exp`，产生溢出或 `nan`。
- 把 logits、概率和类别编号混为一谈。
- 以为 `argmax` 能告诉你模型有多确信，忽略概率分布本身。

## 动手实验

1. 运行[Softmax 与分类 Notebook](../labs/notebooks/09-softmax-classification.ipynb)，观察 logits、概率和类别的关系。
2. 运行[分类损失与反向传播 Notebook](../labs/notebooks/09-classification-loss-backprop.ipynb)，追踪 `d_logits`、`dW` 和 `db` 的形状。
3. 为至少两种激活函数输入正数、负数和接近零的值，预测后再打印结果。

## 验收问题

1. 为什么 Softmax 要沿最后一个维度计算？
2. 为什么预测类别可以直接对 logits 使用 `argmax`？
3. 激活函数给网络增加了什么能力？梯度过小又会造成什么问题？

👉 [进入第 10 章：关于边和角的神经学习 →](10-convolutional-neural-networks.md)
