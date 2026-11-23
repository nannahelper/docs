# 南哪助手和你一起学《深度学习图解》

> 从一个数字、一个权重和一行 NumPy 代码开始，亲手走完神经网络从预测到学习的过程。

<div class="section-lead"><span class="eyebrow">GROKKING DEEP LEARNING</span><h2>先把每个数字讲明白，再把网络跑起来</h2><p>本课程以 Andrew W. Trask 的《深度学习图解》为主线，重点训练“公式 → 数组 → 代码 → 现象”的转换能力。</p></div>

## 这门课要解决什么问题

很多人能调用深度学习框架，却说不清一个预测值是怎样算出来的，也说不清一个权重为什么要向某个方向更新。本课程根据小助手读《深度学习图解》的记录和思考，把问题拆成可手算、可打印、可验证的小步骤，让有基础或没基础的大家读完之后都能对神经网络有所认识，并为可能的进一步学习打好基础。

## 课程信息

| 项目 | 内容 |
|:---|:---|
| 适合人群 | 想了解神经网络的学习者 |
| 前置要求 | 会读基础 Python；不会 NumPy 也可以边学边补 |
| 学习主线 | 手算最小例子 → NumPy 实现 → 解释结果 |
| 适用版本 | Python 3.x、NumPy 1.x/2.x；Notebook 以本地环境为准 |
| 维护状态 | 持续补充中 |
| 最后更新 | 2026-11-23 |
| 反馈入口 | [GitHub Issues](https://github.com/nannahelper/docs/issues) |

## 使用方式

每一章都按下面的闭环推进：

1. 先用自己的话说出本章要解决的问题。
2. 手算一个最小例子，预测代码会输出什么。
3. 把公式拆成数组、函数和中间变量。
4. 先写预期行为或小测试，再运行实现。
5. 解释一次失败结果：是数据、形状、公式还是更新顺序出了问题？
6. 在[章节笔记](notes.md)中完成一句话复述，并在[学习进度](progress.md)中更新状态。

## 章节地图

| 章节 | 核心问题 | 当前状态 |
|:---|:---|:---:|
| [第 1 章：深度学习简介：为什么应该学习深度学习](chapters/01-introduction.md) | 深度学习要解决什么问题？ | 导论 |
| [第 2 章：基本概念：机器如何学习](chapters/02-learning-basics.md) | “学习”在数学上意味着什么？ | 导论 |
| [第 3 章：神经网络预测简介：前向传播](chapters/03-forward-propagation.md) | 输入和权重如何产生预测？ | 重点 |
| [第 4 章：神经网络学习简介：梯度下降](chapters/04-gradient-descent.md) | 一个权重如何根据误差更新？ | 重点 |
| [第 5 章：一次学习多个权重：泛化梯度下降](chapters/05-generalized-gradient-descent.md) | 多个权重和多个样本如何一起学习？ | 重点 |
| [第 6 章：构建第一个深度神经网络：反向传播简介](chapters/06-backpropagation.md) | 误差如何传回更早的层？ | 重点 |
| [第 7 章：如何理解神经网络：在头脑中和纸上](chapters/07-understanding-networks.md) | 如何在纸上追踪网络内部变化？ | 补强 |
| [第 8 章：学习信号、忽略噪声：正则化与批量训练](chapters/08-regularization-and-batching.md) | 如何减少噪声和过拟合？ | 补强 |
| [第 9 章：建模概率与非线性：激活函数](chapters/09-activation-functions.md) | 非线性从哪里来？ | 补强 |
| [第 10 章：关于边和角的神经学习：卷积神经网络](chapters/10-convolutional-neural-networks.md) | 网络如何识别局部模式？ | 补强 |
| [第 11 章：理解语言的神经网络：词嵌入](chapters/11-word-embeddings.md) | 词如何变成可计算的向量？ | 补强 |
| [第 12 章：像莎士比亚一样写作：循环层](chapters/12-recurrent-layers.md) | 网络如何沿时间步保留上下文？ | 扩展 |
| [第 13 章：介绍自动优化：搭建深度学习框架](chapters/13-automatic-optimization.md) | 如何把层、梯度和优化器组织起来？ | 扩展 |
| [第 14 章：学习像莎士比亚一样写作：长短期记忆网络](chapters/14-long-short-term-memory.md) | 如何让序列模型保留长期信息？ | 扩展 |
| [第 15 章：在看不见的数据上做深度学习：联邦学习](chapters/15-federated-learning.md) | 数据不能集中时如何协作训练？ | 扩展 |
| [第 16 章：往哪里去：简要指引](chapters/16-where-to-go.md) | 学完全书后怎样选择下一步？ | 路线 |
| [第 12–16 章总览](chapters/12-16-roadmap.md) | 五章之间如何衔接？ | 导航 |

## 代码实验

<div class="chapter-route">
  <a class="route-step" href="labs/03-forward-propagation.md"><span class="route-index">01</span><strong>前向传播实验</strong><small>观察点积、两层线性计算和数组形状。</small></a>
  <a class="route-step" href="labs/04-05-gradient-descent.md"><span class="route-index">02</span><strong>梯度下降实验</strong><small>从一个权重扩展到多权重和批量更新。</small></a>
  <a class="route-step" href="labs/06-backpropagation.md"><span class="route-index">03</span><strong>反向传播实验</strong><small>追踪链式法则和多层网络的梯度流。</small></a>
</div>

完整的实验入口、Notebook 和运行约定见[代码实验区](labs/README.md)。

## 学习记录

- [学习进度](progress.md)：更新章节状态、信心等级和里程碑。
- [章节笔记](notes.md)：记录自己的理解、形状和失败案例。
- [问题日志](questions.md)：先写猜测，再用最小实验验证。
- [资源与环境](resources.md)：查看教材、代码仓库和本地环境约定。

## 从哪里开始

如果你已经会基本 Python，可以直接进入[第 3 章：前向传播](chapters/03-forward-propagation.md)。如果你对“模型为什么能学习”还没有整体概念，先看[第 1 章](chapters/01-introduction.md)和[第 2 章](chapters/02-learning-basics.md)，再回来做代码实验。

👉 [开始第 1 章：为什么学习深度学习 →](chapters/01-introduction.md)

小助手还推荐各位根据谷歌开发者教程过一遍哦：[Google 机器学习速成课程](https://developers.google.com/machine-learning/crash-course?hl=zh-cn)
