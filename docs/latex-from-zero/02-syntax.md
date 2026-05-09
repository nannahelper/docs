# 第 2 章：核心语法

> **掌握 LaTeX 的基本元素** —— 章节、文字格式、列表、表格、图片，构建文档的六大基石。

---

## 2.1 章节命令

```latex
\section{一级标题}
\subsection{二级标题}
\subsubsection{三级标题}

\section*{不带编号的标题}     % 加 * 号取消自动编号
```

**渲染效果：** 章节标题自动编号（如 1、1.1、1.1.1），字号逐级递减，自动生成目录时按层级缩进。

## 2.2 文字格式

```latex
\textbf{粗体文字}
\textit{斜体文字}
\underline{下划线文字}
\texttt{等宽字体（代码风格）}
\textsc{小型大写字母}

{\large 大号文字}
{\small 小号文字}
{\tiny 极小文字}
```

**渲染效果：** 粗体加粗、斜体倾斜、下划线有底部横线、等宽字体适合展示代码。字号命令影响作用域内的所有文字。

## 2.3 段落与间距

```latex
这是第一段。
空一行开始新段落。

这是第二段。\\      % \\ 强制换行但不开始新段落
这是同一段的第二行。

\vspace{1cm}        % 插入 1 厘米垂直间距

\hspace{2cm}        % 插入 2 厘米水平间距
```

**渲染效果：** 段落之间自动缩进首行并有段间距。`\\` 换行后文字紧密排列。`\vspace` 和 `\hspace` 精确控制空白。

## 2.4 列表

### 无序列表

```latex
\begin{itemize}
    \item 第一项
    \item 第二项
    \begin{itemize}
        \item 子项 2.1
        \item 子项 2.2
    \end{itemize}
    \item 第三项
\end{itemize}
```

**渲染效果：** 第一层用实心圆点（●），第二层用短横线（–），第三层用星号（*），层次分明。

### 有序列表

```latex
\begin{enumerate}
    \item 第一步
    \item 第二步
    \begin{enumerate}
        \item 子步骤 2.1
        \item 子步骤 2.2
    \end{enumerate}
    \item 第三步
\end{enumerate}
```

**渲染效果：** 第一层用阿拉伯数字（1, 2, 3），第二层用小写字母（a, b），第三层用小写罗马数字（i, ii）。

## 2.5 表格

```latex
\begin{table}[htbp]
    \centering
    \caption{这是一个表格标题}
    \label{tab:example}
    \begin{tabular}{|l|c|r|}
        \hline
        左对齐 & 居中对齐 & 右对齐 \\
        \hline
        内容 1 & 内容 2 & 内容 3 \\
        内容 4 & 内容 5 & 内容 6 \\
        \hline
    \end{tabular}
\end{table}
```

**渲染效果：** 表格自动编号（如"表 1"），标题在表格上方居中。`|l|c|r|` 定义三列分别为左对齐、居中、右对齐，竖线表示列分隔线，`\hline` 画横线。

**代码解读：**

- `{tabular}` 中的 `l`、`c`、`r` 分别代表左对齐、居中、右对齐
- `|` 在列格式中表示画竖线
- `\hline` 画水平线
- `[htbp]` 是浮动位置参数：here（此处）、top（页顶）、bottom（页底）、page（单独一页）

## 2.6 图片

```latex
\usepackage{graphicx}    % 导言区引入

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.6\textwidth]{image.png}
    \caption{图片标题}
    \label{fig:example}
\end{figure}
```

**渲染效果：** 图片自动编号（如"图 1"），标题在图片下方居中。`width=0.6\textwidth` 将图片宽度设为页面文字宽度的 60%。

!!! tip "图片格式支持"

    - 使用 `xelatex` 编译时支持 PNG、JPG、PDF 格式
    - 推荐使用 PDF 格式的矢量图，放大不失真

---

## 本章要点总结

- [ ] 掌握 `\section`、`\subsection` 章节命令
- [ ] 会用 `\textbf`、`\textit` 等文字格式命令
- [ ] 熟练使用 `itemize` 和 `enumerate` 环境
- [ ] 理解 `tabular` 表格的列格式定义
- [ ] 会用 `\includegraphics` 插入图片
- [ ] 理解浮动体 `table` 和 `figure` 的作用

---

👉 [进入第 3 章：常用技巧 →](03-tips.md)