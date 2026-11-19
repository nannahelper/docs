# 代码实验区

这里保存《深度学习图解》的 NumPy 实验和 Notebook。实验统一采用：

```text
先手算 → 写出预期 → 运行代码 → 打印形状 → 检查误差 → 解释结果
```

代码能运行只是起点。每次实验至少要回答：

1. 每个变量的形状是什么？
2. 当前计算对应哪一条公式？
3. 输出和自己的预测是否一致？
4. 如果不一致，问题更可能出在数据、形状、公式还是更新顺序？

## 当前实验

| 实验 | 说明 | 入口 |
|:---|:---|:---|
| 前向传播 | 点积、两层线性计算和形状追踪 | [实验说明](03-forward-propagation.md) · [Python 文件](03-forward-propagation.py) |
| 梯度下降 | 单权重、多权重、逐样本和批量更新 | [实验说明](04-05-gradient-descent.md) · [Notebook](notebooks/04-05-gradient-descent.ipynb) |
| 反向传播 | 链式法则、多层网络和矩阵梯度 | [实验说明](06-backpropagation.md) · [Notebook](notebooks/06-backpropagation.ipynb) |
| 层抽象 | 把线性层、ReLU 和反向传播组织成可复用接口 | [Notebook](notebooks/07-layer-abstraction.ipynb) · [层实现](layers.py) |
| 正则化与批量训练 | 训练/验证误差、提前停止、Dropout 和曲线 | [Notebook](notebooks/08-regularization.ipynb) · [绘图基础](notebooks/08-matplotlib-basics.ipynb) |
| Softmax 与分类损失 | logits、概率、交叉熵和分类反向传播 | [Softmax Notebook](notebooks/09-softmax-classification.ipynb) · [分类反向传播 Notebook](notebooks/09-classification-loss-backprop.ipynb) |

Notebook 是可下载的原始实验资产；Markdown 页面负责解释实验目标、形状和验收问题。
