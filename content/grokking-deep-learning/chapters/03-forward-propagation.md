# 第 3 章：神经网络预测简介：前向传播

## 本章要解决的问题

前向传播只回答一个问题：给定输入和权重，网络如何算出预测值？这一章先不训练，只把计算路径和数组形状讲清楚。

## 一个神经元就是加权求和

对输入向量 `x` 和权重向量 `w`，最小的神经元可以写成：

$$
\hat{y}=x_1w_1+x_2w_2+\cdots+x_nw_n
$$

每个输入先乘上自己的权重，再把贡献相加。代码对应的是：

```python
prediction = np.dot(inputs, weights)
```

例如：

```python
inputs = np.array([2., 1., -1.])
weights = np.array([0.5, 0.2, 0.1])
prediction = np.dot(inputs, weights)
```

手算得到 `2×0.5 + 1×0.2 + (-1)×0.1 = 1.1`。

## `*`、`@` 和 `np.dot`

它们看起来都像“乘法”，但含义不同：

```python
inputs * weights          # 逐元素相乘，保留每个位置的贡献
inputs @ weights          # 点积，把贡献汇总成一个结果
np.dot(inputs, weights)   # 对这组一维向量也表示点积
```

`*` 不会自动完成求和。把逐元素贡献误当成预测值，是初学者最常见的错误之一。

## 形状决定运算能否成立

单个样本、一个输出节点时：

```text
inputs.shape  == (3,)
weights.shape == (3,)
prediction    == 标量
```

如果同一个输入连接到 4 个输出节点，权重矩阵的每一列对应一个节点：

```text
inputs.shape  == (3,)
weights.shape == (3, 4)
layer.shape   == (4,)
```

多个样本时，第一维表示样本数：

```text
inputs.shape      == (样本数, 特征数)
weights.shape     == (特征数,)
predictions       == inputs @ weights
predictions.shape == (样本数,)
```

看到一个矩阵乘法时，先说清楚每一维代表什么，再写代码。

## 两层线性网络

现有实验使用两层线性计算：

```text
输入 (3,)
  @ weights_1 (3, 4)
第一层输出 (4,)
  @ weights_2 (4, 2)
最终输出 (2,)
```

这就是为什么实验应该打印 `(3,)`、`(4,)`、`(2,)`。打印形状不是多余操作，而是在确认数据是否沿着预期的计算图流动。

## 动手实验

1. 先手算上一段中的一个输出节点。
2. 运行[前向传播实验说明](../labs/03-forward-propagation.md)和[`03-forward-propagation.py`](../labs/03-forward-propagation.py)。
3. 只修改一个权重，预测哪个输出会变化。
4. 把输入改成含负数的数组，重新判断“权重变大后预测是否一定变大”。

## 常见错误

- 把 `inputs * weights` 当成点积。
- 把样本数误当成权重向量的长度。
- 看到 NumPy 广播成功，就以为数学含义一定正确。
- 只打印最终预测，不打印中间层形状。

## 验收问题

1. `inputs.shape == (5,)`、`weights.shape == (5, 3)` 时输出形状是什么？
2. 为什么逐元素乘法不能替代点积？
3. 如果权重全变大，预测值一定会变大吗？输入中有负数时要怎样判断？

👉 [进入第 4 章：神经网络学习简介：梯度下降 →](04-gradient-descent.md)
