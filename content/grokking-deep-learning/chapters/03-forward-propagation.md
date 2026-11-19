# 第 3 章：神经网络预测简介：前向传播

## 输入和权重如何产生预测

前向传播就是从输入一路向前计算，得到预测值。最小的神经元可以写成：

$$
y = x_1w_1 + x_2w_2 + \cdots + x_nw_n
$$

这就是输入向量和权重向量的点积。每个输入先乘上对应权重，再把贡献加起来。

## 先想：形状比数字更重要

如果：

```text
inputs.shape  == (3,)
weights.shape == (3,)
```

那么 `inputs @ weights` 的结果是一个标量。如果有多个隐藏节点：

```text
inputs.shape   == (3,)
weights.shape  == (3, 4)
layer.shape    == (4,)
```

每一列对应一个隐藏节点，输出的长度因此变成 4。

## 动手实验

打开[前向传播实验说明](../labs/03-forward-propagation.md)，再运行[`03-forward-propagation.py`](../labs/03-forward-propagation.py)。重点观察：

- 输入、第一层输出和最终预测的形状。
- `@`、`np.dot` 和 `*` 的区别。
- 改变一个权重后，哪个输出发生了变化。

## 验证问题

1. `inputs.shape == (5,)`、`weights.shape == (5, 3)` 时输出形状是什么？
2. 为什么逐元素乘法不能替代点积？
3. 如果权重全变大，预测值一定会变大吗？输入中有负数时要怎样判断？

👉 [进入第 4 章：梯度下降 →](04-gradient-descent.md)
