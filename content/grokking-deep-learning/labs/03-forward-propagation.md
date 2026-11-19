# 实验 1：前向传播与形状

## 实验目标

用一个输入向量、两组权重矩阵和两次点积，观察一个简单网络如何从输入得到预测。

## 运行

在课程仓库根目录执行：

```bash
python content/grokking-deep-learning/labs/03-forward-propagation.py
```

预期会看到输入、第一层输出和最终输出的形状：

```text
(3,)
(4,)
(2,)
```

## 先预测，再运行

代码中：

```python
layer_1 = np.dot(inputs, weights_1)
prediction = np.dot(layer_1, weights_2)
```

先写下两次矩阵乘法的输入形状和输出形状，再运行文件验证。

## 小练习

1. 把 `inputs` 改成长度为 5 的向量，并把第一组权重改成 `(5, 4)`。
2. 只修改 `weights_2`，观察最终的两个输出怎样变化。
3. 把第二次 `np.dot` 临时改成 `layer_1 * weights_2`，记录错误或输出形状的变化。

完成后回到[第 3 章：前向传播](../chapters/03-forward-propagation.md)，用自己的话解释为什么输出是 `(2,)`。
