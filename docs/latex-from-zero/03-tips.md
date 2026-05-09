# 第 3 章：常用技巧

> **LaTeX 的核心竞争力** —— 数学公式、交叉引用、参考文献管理。

---

## 3.1 数学公式

LaTeX 的数学排版能力是其最强大的特性。

### 行内公式

```latex
质能方程 $E = mc^2$ 是爱因斯坦最著名的公式。
```

**渲染效果：** 公式嵌入在文字行中，与周围文字高度协调。

### 独立公式

```latex
% 不带编号
\[
    \int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
\]

% 带编号
\begin{equation}
    \frac{d}{dx} \sin x = \cos x
    \label{eq:derivative}
\end{equation}
```

**渲染效果：** 独立公式居中显示，`equation` 环境自动在右侧添加编号（如 (1)），可通过 `\label` 交叉引用。

### 常用数学符号

```latex
% 希腊字母
$\alpha, \beta, \gamma, \delta, \epsilon, \theta, \lambda, \mu, \pi, \sigma, \phi, \omega$

% 上下标
$x^2, x^{10}, x_i, x_{ij}$

% 分数
$\frac{a}{b}, \frac{1}{1 + \frac{1}{x}}$

% 根号
$\sqrt{x}, \sqrt[3]{x}$

% 求和、积分
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

**渲染效果：** 希腊字母以标准数学字体显示；上下标位置精确；分数有清晰的分数线；根号自动适应内容高度；求和符号上下限位置正确；矩阵有圆括号包围；分段函数有大括号和条件对齐。

## 3.2 交叉引用

```latex
\section{引言}
\label{sec:intro}

如图 \ref{fig:example} 所示，详见第 \pageref{sec:intro} 页。

\begin{figure}
    \centering
    \includegraphics{image.png}
    \caption{示例图片}
    \label{fig:example}
\end{figure}
```

**渲染效果：** `\ref{fig:example}` 自动显示为"图 1"，`\pageref{sec:intro}` 显示该章节所在的页码。编号全自动，增删内容后只需重新编译即可更新。

## 3.3 参考文献

### 使用 BibTeX

```latex
% 在正文中引用
根据 \cite{knuth1984} 的研究...

% 参考文献样式
\bibliographystyle{plain}
\bibliography{references}    % 引用 references.bib 文件
```

`references.bib` 文件内容：

```bibtex
@book{knuth1984,
    author    = {Donald E. Knuth},
    title     = {The TeXbook},
    year      = {1984},
    publisher = {Addison-Wesley}
}

@article{einstein1905,
    author  = {Albert Einstein},
    title   = {Zur Elektrodynamik bewegter K\"orper},
    journal = {Annalen der Physik},
    volume  = {322},
    number  = {10},
    pages   = {891--921},
    year    = {1905}
}
```

**渲染效果：** 正文中引用处显示为 `[1]` 或 `[Knuth, 1984]`（取决于样式），文末自动生成参考文献列表，格式统一规范。

## 3.4 自定义命令

```latex
% 定义新命令（导言区）
\newcommand{\R}{\mathbb{R}}           % 实数集符号
\newcommand{\abs}[1]{\left|#1\right|} % 绝对值

% 使用
实数集 $\R$ 上的绝对值 $\abs{x}$。
```

**渲染效果：** `\R` 显示为黑板粗体的 ℝ，`\abs{x}` 显示为 |x|（竖线高度自动适应内容）。

---

## 本章要点总结

- [ ] 掌握行内公式 `$...$` 和独立公式 `\[...\]` 的写法
- [ ] 熟悉常用数学符号和结构（分数、根号、求和、矩阵）
- [ ] 理解 `\label` + `\ref` 交叉引用机制
- [ ] 了解 BibTeX 参考文献管理流程
- [ ] 会用 `\newcommand` 定义自定义命令

---

👉 [进入第 4 章：实战案例 →](04-practice.md)