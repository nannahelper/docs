# 第 3 章：管理参考文献与引用

> **场景：** 你的论文需要引用多篇参考文献，正文中要交叉引用前面的公式和图表。手动管理这些引用既繁琐又容易出错——LaTeX 的自动化引用系统正是为此而生。

---

## 3.1 交叉引用：让编号自动更新

在论文中，你经常需要引用前面的图表或公式。LaTeX 的 `\label` + `\ref` 机制让这一切自动化：

```latex
\section{方法}
\subsection{模型架构}
\begin{equation}
    \mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N} y_i \log(\hat{y}_i)
    \label{eq:loss}
\end{equation}

如图 \ref{fig:arch} 所示，模型包含 5 个卷积层。
损失函数见公式 \ref{eq:loss}。

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.6\textwidth]{architecture.pdf}
    \caption{模型架构图}
    \label{fig:arch}
\end{figure}
```

**渲染效果：** `\ref{fig:arch}` 自动显示为"图 1"，`\ref{eq:loss}` 显示为"公式 1"。即使你在前面插入新的图表，所有编号自动更新——只需重新编译即可。

!!! tip "引用命名规范"
    推荐使用前缀区分引用类型：
    - `\label{fig:xxx}` — 图片
    - `\label{tab:xxx}` — 表格
    - `\label{eq:xxx}` — 公式
    - `\label{sec:xxx}` — 章节

---

## 3.2 参考文献：BibTeX 自动管理

### 创建参考文献库

新建 `references.bib` 文件，按标准 BibTeX 格式录入：

```bibtex
@book{knuth1984,
    author    = {Donald E. Knuth},
    title     = {The TeXbook},
    year      = {1984},
    publisher = {Addison-Wesley}
}

@article{he2016deep,
    author  = {Kaiming He and Xiangyu Zhang and Shaoqing Ren and Jian Sun},
    title   = {Deep Residual Learning for Image Recognition},
    journal = {CVPR},
    year    = {2016},
    pages   = {770--778}
}

@inproceedings{vaswani2017attention,
    author  = {Ashish Vaswani and others},
    title   = {Attention Is All You Need},
    booktitle = {NeurIPS},
    year    = {2017}
}
```

### 在论文中引用

```latex
\section{引言}
深度学习在图像识别领域取得了突破性进展 \cite{he2016deep}。
Transformer 架构 \cite{vaswani2017attention} 进一步推动了 NLP 的发展。

% 文末自动生成参考文献列表
\bibliographystyle{plain}
\bibliography{references}
```

**渲染效果：** 正文中引用处显示为 `[1]`、`[2]`（plain 样式），文末自动生成按引用顺序排列的参考文献列表，格式统一规范。如果使用 `\cite{he2016deep,vaswani2017attention}` 则显示为 `[1, 2]`。

---

## 3.3 自定义命令：减少重复劳动

论文中经常出现相同的符号或格式，定义一次，全局使用：

```latex
% 在导言区定义
\newcommand{\R}{\mathbb{R}}           % 实数集 ℝ
\newcommand{\E}{\mathbb{E}}           % 期望 𝔼
\newcommand{\abs}[1]{\left|#1\right|} % 自适应高度的绝对值
\newcommand{\norm}[1]{\left\|#1\right\|} % 自适应高度的范数

% 在正文中使用
实数集 $\R$ 上的范数 $\norm{x}$ 定义为 $\abs{x}$。
```

**渲染效果：** `\R` 显示为黑板粗体的 ℝ，`\abs{x}` 显示为 |x|（竖线高度自动适应内容，如 `\abs{\frac{a}{b}}` 的竖线会变高）。

---

## 3.4 更多数学技巧

### 多行公式对齐

```latex
\begin{align}
    f(x) &= x^2 + 2x + 1 \\
    g(x) &= \sin(x) + \cos(x) \\
    h(x) &= \int_{0}^{x} f(t) dt
\end{align}
```

**渲染效果：** 三行公式在 `=` 号处对齐，每行自动编号 (1)、(2)、(3)。

### 定理环境

```latex
% 导言区
\usepackage{amsthm}
\newtheorem{theorem}{定理}[section]
\newtheorem{definition}{定义}[section]

% 正文
\begin{definition}[卷积]
卷积是一种数学运算，定义为
$(f * g)(t) = \int f(\tau)g(t-\tau)d\tau$。
\end{definition}

\begin{theorem}[卷积定理]
时域中的卷积等价于频域中的乘积。
\end{theorem}
```

**渲染效果：** 定理和定义自动编号（如"定义 2.1"、"定理 2.1"），标题加粗，内容使用斜体，排版符合数学出版物规范。

---

## 3.5 实战：为论文添加引用系统

把本章技能整合到论文中：

```latex
\documentclass{article}
\usepackage[UTF8]{ctex}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{hyperref}

% 自定义命令
\newcommand{\R}{\mathbb{R}}
\newcommand{\abs}[1]{\left|#1\right|}

% 定理环境
\newtheorem{theorem}{定理}[section]

\title{基于深度学习的图像分类方法研究}
\author{张三}
\date{}

\begin{document}
\maketitle

\begin{abstract}
本文提出了一种改进的卷积神经网络，在 CIFAR-10 数据集上
取得了 95.3\% 的分类准确率。
\end{abstract}

\section{引言}
图像分类是计算机视觉的基础任务 \cite{he2016deep}。
近年来，Transformer 架构 \cite{vaswani2017attention}
也被应用于视觉任务。

\section{方法}
\subsection{损失函数}
使用交叉熵损失函数：
\begin{equation}
    \mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N}\sum_{c=1}^{C}
    y_{ic}\log(\hat{y}_{ic})
    \label{eq:loss}
\end{equation}

\subsection{收敛性分析}
\begin{theorem}[梯度下降收敛性]
对于凸函数 $f: \R^n \to \R$，梯度下降以 $O(1/k)$ 的速率收敛。
\end{theorem}

\section{实验}
实验结果如表 \ref{tab:results} 所示。

\begin{table}[htbp]
    \centering
    \caption{分类准确率对比}
    \label{tab:results}
    \begin{tabular}{lc}
        \hline
        模型 & 准确率 (\%) \\
        \hline
        VGG-16 & 92.1 \\
        ResNet-18 \cite{he2016deep} & 93.5 \\
        本文方法 & \textbf{95.3} \\
        \hline
    \end{tabular}
\end{table}

\bibliographystyle{plain}
\bibliography{references}

\end{document}
```

**渲染效果：** 编译后生成完整学术论文 PDF：摘要、分节内容、编号公式 (1)、定理 2.1、表 1（带交叉引用）、参考文献列表 `[1]` `[2]`。

---

## 本章回顾

你的论文引用系统已就绪！回顾新掌握的技能：

- [x] 用 `\label` + `\ref` 实现交叉引用，编号自动更新
- [x] 用 BibTeX（`.bib` 文件）管理参考文献
- [x] 用 `\cite` 在正文中引用文献
- [x] 用 `\newcommand` 定义自定义命令
- [x] 用 `align` 环境对齐多行公式
- [x] 用 `\newtheorem` 创建定理环境

---

👉 [进入第 4 章：打造学术作品集 →](04-practice.md)