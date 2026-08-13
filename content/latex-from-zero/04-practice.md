# 第 4 章：打造学术作品集

> **场景：** 你掌握了 LaTeX 的核心技能，现在需要产出完整的学术作品——一篇格式规范的论文、一份专业的简历、一套答辩幻灯片。让我们把学到的所有技能融会贯通。

---

## 4.1 完整学术论文模板

以下是一个可直接使用的学术论文模板：

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[UTF8]{ctex}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{geometry}
\geometry{margin=2.5cm}

\title{基于深度学习的图像分类方法研究}
\author{张三\thanks{通信作者：zhangsan@example.com}}
\date{}

\begin{document}
\maketitle

\begin{abstract}
本文提出了一种基于改进卷积神经网络的图像分类方法。
在 CIFAR-10 数据集上取得了 95.3\% 的分类准确率，
相比基线模型提升了 3.2 个百分点。
\end{abstract}

\section{引言}
图像分类是计算机视觉领域的基础任务之一...

\section{相关工作}
近年来，深度学习在图像分类领域取得了显著进展...

\section{方法}
\subsection{模型架构}
本文提出的模型包含 5 个卷积层和 3 个全连接层...

\subsection{损失函数}
使用交叉熵损失函数：
\begin{equation}
    \mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N}\sum_{c=1}^{C}
    y_{ic}\log(\hat{y}_{ic})
    \label{eq:loss}
\end{equation}

\section{实验}
\subsection{数据集}
实验使用 CIFAR-10 数据集，包含 60,000 张 32×32 的彩色图片...

\subsection{结果分析}
实验结果如表 \ref{tab:results} 所示。

\begin{table}[htbp]
    \centering
    \caption{不同模型的分类准确率对比}
    \label{tab:results}
    \begin{tabular}{lc}
        \hline
        模型 & 准确率 (\%) \\
        \hline
        VGG-16 & 92.1 \\
        ResNet-18 & 93.5 \\
        本文方法 & \textbf{95.3} \\
        \hline
    \end{tabular}
\end{table}

\section{结论}
本文提出了一种改进的卷积神经网络...

\bibliographystyle{plain}
\bibliography{references}

\end{document}
```

**渲染效果：** 编译后生成标准学术论文 PDF，包含标题、摘要、分节内容、编号公式、表格和参考文献，排版符合学术出版规范。

---

## 4.2 制作专业简历

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[UTF8]{ctex}
\usepackage{geometry}
\geometry{margin=1.5cm}

\begin{document}

\begin{center}
    {\huge \textbf{张 三}} \\[0.3cm]
    电话：138-0000-0000 \quad 邮箱：zhangsan@example.com \\
    GitHub：github.com/zhangsan
\end{center}

\section*{教育背景}
\textbf{某某大学} \hfill 2022.09 -- 2026.06 \\
计算机科学与技术 · 本科 \hfill GPA: 3.8/4.0

\section*{技能}
\begin{itemize}
    \item 编程语言：Python、Java、C++
    \item 框架工具：PyTorch、Docker、Git
    \item 语言能力：英语 CET-6（580 分）
\end{itemize}

\section*{项目经历}
\textbf{在线教育平台} \hfill 2025.03 -- 2025.06 \\
\begin{itemize}
    \item 使用 Django + Vue.js 开发全栈 Web 应用
    \item 实现实时视频推流和在线白板功能
    \item 服务 500+ 用户，系统可用性 99.5\%
\end{itemize}

\section*{获奖情况}
\begin{itemize}
    \item 全国大学生数学建模竞赛 省级一等奖（2024）
    \item 校级优秀学生奖学金（2023、2024）
\end{itemize}

\end{document}
```

**渲染效果：** 简历排版紧凑专业，个人信息居中醒目，各板块用加粗标题分隔，时间线用 `\hfill` 右对齐排列，整体一页纸呈现。

---

## 4.3 制作答辩幻灯片（Beamer）

```latex
\documentclass{beamer}
\usepackage[UTF8]{ctex}
\usetheme{Madrid}

\title{基于深度学习的图像分类}
\author{张三}
\date{2026 年 5 月}

\begin{document}

\begin{frame}
    \titlepage
\end{frame}

\begin{frame}{目录}
    \tableofcontents
\end{frame}

\section{研究背景}
\begin{frame}{研究背景}
    \begin{itemize}
        \item 图像分类是 CV 的基础任务
        \item 深度学习大幅提升了分类准确率
        \item 但仍存在小样本、细粒度等挑战
    \end{itemize}
\end{frame}

\section{方法}
\begin{frame}{模型架构}
    \begin{figure}
        \centering
        \includegraphics[width=0.7\textwidth]{architecture.pdf}
        \caption{模型架构图}
    \end{figure}
\end{frame}

\section{实验结果}
\begin{frame}{实验结果}
    \begin{table}
        \begin{tabular}{lc}
            \hline
            模型 & 准确率 \\
            \hline
            Baseline & 92.1\% \\
            本文方法 & 95.3\% \\
            \hline
        \end{tabular}
    \end{table}
\end{frame}

\begin{frame}{}
    \centering
    \huge 谢谢！\\
    \vspace{1cm}
    \normalsize 联系方式：zhangsan@example.com
\end{frame}

\end{document}
```

**渲染效果：** 生成 PDF 幻灯片，每页一个 `frame`，有统一的 Madrid 主题样式（蓝色调），自动生成目录页，适合学术演讲和答辩。

---

## 4.4 学习旅程回顾

| 章节 | 场景 | 核心技能 |
|:---|:---|:---|
| 第 1 章 | 写课程作业 | 文档结构、章节、文字格式、列表 |
| 第 2 章 | 让论文更专业 | 表格、图片、数学公式 |
| 第 3 章 | 管理引用 | 交叉引用、BibTeX、自定义命令 |
| 第 4 章 | 打造作品集 | 完整论文、简历、幻灯片 |

---

## 课后练习

### 基础练习

1. 用 LaTeX 写一份课程报告，包含至少一个表格、一个公式和一张图片。
2. 用 LaTeX 制作你的个人简历。

### 进阶挑战

3. 在 Overleaf 上找一个学术会议模板，尝试填入你的内容。
4. 用 Beamer 制作一份 5 页以上的答辩幻灯片。

---

👉 [返回首页 →](index.md)