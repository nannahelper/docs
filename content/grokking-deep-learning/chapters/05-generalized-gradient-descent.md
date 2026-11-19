# 第 5 章：一次学习多个权重：泛化梯度下降

## 从一个权重扩展到多个权重

多个输入和多个权重可以写成：

```python
prediction = np.dot(inputs, weights)
```

此时一个误差会同时影响多个权重。每个权重对应一个输入特征，因此更新量也必须保持相同的形状。

## 从一个样本扩展到多个样本

多个样本可以组织成矩阵：

```text
inputs.shape  == (样本数, 特征数)
weights.shape == (特征数,)
predictions   == inputs @ weights
```

逐样本更新会在每个样本后立刻修改权重；批量梯度下降则先收集所有误差，再统一计算更新量。两者都在利用误差，只是反馈的时机不同。

## 动手实验

打开[第 4–5 章梯度下降实验](../labs/04-05-gradient-descent.md)，再运行[配套 Notebook](../labs/notebooks/04-05-gradient-descent.ipynb)。重点查看：

- `inputs.T @ errors` 为什么能把样本维度汇总掉。
- 逐样本更新和批量更新的结果有什么差异。
- 样本数量增加时，为什么常常要取平均。

## 验收

用一句话解释：为什么 `weights.shape == (特征数,)`，而不是 `(样本数,)`？

👉 [进入第 6 章：反向传播 →](06-backpropagation.md)
