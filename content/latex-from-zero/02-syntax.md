# 第 2 章：让论文更专业

> **场景：** 你的课程报告需要插入实验数据表格、算法流程图和数学公式推导。这些正是 LaTeX 的强项——让我们把报告升级到学术论文的水准。

---

## 2.1 插入表格：展示实验数据

假设你的实验对比了三种算法的性能：

```latex
\begin{table}[htbp]
    \centering
    \caption{三种算法的性能对比}
    \label{tab:performance}
    \begin{tabular}{|l|c|c|r|}
        \hline
        算法 & 准确率 & 召回率 & 推理时间(ms) \\
        \hline
        Baseline & 92.1\% & 89.3\% & 45 \\
        方法 A & 94.5\% & 91.2\% & 52 \\
        方法 B & \textbf{96.8\%} & \textbf{94.1\%} & 48 \\
        \hline
    \end{tabular}
\end{table}
```

**渲染效果：** 表格自动编号为"表 1"，标题在表格上方居中。列格式 `|l|c|c|r|` 定义四列分别为左对齐、居中、居中、右对齐，竖线表示列分隔线，`\hline` 画横线。最佳结果用粗体突出。

**代码解读：**

| 列格式符 | 含义 |
|:---|:---|
| `l` | 左对齐 |
| `c` | 居中对齐 |
| `r` | 右对齐 |
| `|` | 画竖线 |
| `\hline` | 画水平线 |
| `[htbp]` | 浮动位置：here（此处）、top（页顶）、bottom（页底）、page（单独一页） |

---

## 2.2 插入图片：一图胜千言

```latex
% 导言区需要引入 graphicx 宏包
\usepackage{graphicx}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.6\textwidth]{model-architecture.pdf}
    \caption{模型架构示意图}
    \label{fig:architecture}
\end{figure}
```

**渲染效果：** 图片自动编号为"图 1"，标题在图片下方居中。`width=0.6\textwidth` 将图片宽度设为页面文字宽度的 60%，保持比例缩放。

!!! tip "图片格式建议"
    - 使用 `xelatex` 编译时支持 PNG、JPG、PDF 格式
    - 推荐使用 PDF 格式的矢量图，放大不失真
    - `\textwidth` 是页面文字宽度，用比例控制比写死像素更灵活

---

## 2.3 数学公式：LaTeX 的核心竞争力

这是 LaTeX 最强大的特性。让我们从实际论文场景中学习。

### 行内公式：嵌入文字中

```latex
均方误差定义为 $MSE = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$，
它是回归任务中最常用的损失函数。
```

**渲染效果：** 公式嵌入在文字行中，高度与周围文字协调，分数线、求和符号、上下标自动调整大小。

### 独立公式：居中展示

```latex
% 不带编号
\[
    \int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
\]

% 带编号（可交叉引用）
\begin{equation}
    \mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N}\sum_{c=1}^{C}
    y_{ic}\log(\hat{y}_{ic})
    \label{eq:cross-entropy}
\end{equation}
```

**渲染效果：** 独立公式居中显示，与上下文有适当间距。`equation` 环境自动在右侧添加编号（如 (1)），可通过 `\label` 交叉引用。

### 常用数学元素速查

```latex
% 希腊字母
$\alpha, \beta, \gamma, \delta, \epsilon, \theta, \lambda, \mu, \pi, \sigma, \phi, \omega$

% 上下标
$x^2, x^{10}, x_i, x_{ij}$

% 分数
$\frac{a}{b}, \frac{1}{1 + \frac{1}{x}}$

% 根号
$\sqrt{x}, \sqrt[3]{x}$

% 求和、求积、积分
$\sum_{i=1}^{n} x_i, \prod_{i=1}^{n} x_i, \int_{a}^{b} f(x) dx$

% 矩阵
\[
\begin{pmatrix}
    a & b \\
    c & d
\end{pmatrix}
\]

% 分段函数
\[
f(x) = \begin{cases}
    x^2, & x \geq 0 \\
    -x,  & x < 0
\end{cases}
\]
```

**渲染效果：** 希腊字母以标准数学斜体显示；上下标位置精确；分数线自动调整长度；根号自动适应内容高度；求和符号上下限在独立公式中位于符号正上方和正下方；矩阵有圆括号包围；分段函数有大括号和条件对齐。

---

## 2.4 完善你的课程报告

现在把表格、图片和公式整合到报告中：

```latex
\documentclass{article}
\usepackage[UTF8]{ctex}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{margin=2.5cm}

\title{基于深度学习的图像分类方法对比研究}
\author{张三 \\ 计算机科学系}
\date{2026 年 5 月}

\begin{document}
\maketitle

\section{引言}
图像分类是计算机视觉的基础任务。本文对比了三种主流方法
在 CIFAR-10 数据集上的表现。

\section{方法}
\subsection{卷积神经网络（CNN）}
CNN 通过卷积层提取图像的局部特征。卷积运算定义为：
\begin{equation}
    (f * g)(t) = \int_{-\infty}^{\infty} f(\tau)g(t-\tau)d\tau
    \label{eq:conv}
\end{equation}

\subsection{模型架构}
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{architecture.pdf}
    \caption{本文使用的 CNN 模型架构}
    \label{fig:arch}
\end{figure}

\section{实验结果}
实验结果如表 \ref{tab:results} 所示。

\begin{table}[htbp]
    \centering
    \caption{不同模型的分类准确率对比}
    \label{tab:results}
    \begin{tabular}{lcc}
        \hline
        模型 & Top-1 准确率 & Top-5 准确率 \\
        \hline
        VGG-16 & 92.1\% & 99.1\% \\
        ResNet-18 & 93.5\% & 99.3\% \\
        本文方法 & \textbf{95.3\%} & \textbf{99.6\%} \\
        \hline
    \end{tabular}
\end{table}

\section{结论}
本文提出的改进 CNN 模型在 CIFAR-10 上取得了 95.3\% 的准确率，
优于基线模型。未来工作将探索更大规模数据集上的表现。

\end{document}
```

**渲染效果：** 编译后生成标准学术风格的 PDF：标题页包含居中标题和作者信息；公式 (1) 带编号；图 1 和表 1 自动编号并带标题；正文中 `\ref{tab:results}` 自动显示为"表 1"。

---

## 本章回顾

你的报告已经具备学术论文的雏形！回顾新掌握的技能：

- [x] 用 `tabular` 环境创建表格，控制列对齐和边框
- [x] 用 `\includegraphics` 插入图片，控制缩放比例
- [x] 用 `$...$` 写行内公式，用 `\[...\]` 写独立公式
- [x] 掌握常用数学元素：分数、根号、求和、矩阵、分段函数
- [x] 理解浮动体 `table` 和 `figure` 的自动排版机制

---

👉 [进入第 3 章：管理参考文献与引用 →](03-tips.md)