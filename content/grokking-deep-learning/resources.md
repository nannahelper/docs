# 资源与环境

## 主资源

| 资源 | 类型 | 说明 |
|:---|:---|:---|
| 《深度学习图解》 | 中文教材 | Andrew W. Trask 著，王晓雷、严烈译，清华大学出版社 |
| [Grokking Deep Learning — 出版社页面](https://www.simonandschuster.com/books/Grokking-Deep-Learning/Andrew-Trask/9781617293702) | 官方出版信息 | 查看英文原版简介、作者信息和章节目录 |
| [作者主页](https://andrewtrask.ai/) | 作者页面 | 了解作者和本书的 Python + NumPy 入门路线 |

## 配套资源

- [Manning 样章](https://manning-content.s3.amazonaws.com/download/d/5d0f2b3-4591-4648-a869-6dafc6f38310/sample_ch01_Trask2_Grokking_Deep-Learning_corr_January06.pdf)：用于确认阅读风格和代码上下文。
- [作者代码仓库](https://github.com/iamtrask/Grokking-Deep-Learning)：先独立实现，再用作对照，不直接复制答案。

## 本地环境

课程主线使用 Python + NumPy，Notebook 使用 Jupyter 打开。PyTorch 放在后续框架映射阶段。

```bash
python -m venv .venv
python -m pip install numpy jupyter
```

如果已有环境，先运行：

```bash
python -c "import numpy; print(numpy.__version__)"
```

## 额外推荐

小助手还推荐各位根据谷歌开发者教程过一遍哦：[Google 机器学习速成课程](https://developers.google.com/machine-learning/crash-course?hl=zh-cn)

## 资产来源

本课程的代码实验和学习记录整理自 `Dog-Learn/Alexandria/reading/grokking-deep-learning`，主站只保留为课程展示所需的精选副本，原始学习目录不在本仓库中修改。
