# 第 1 章：基础概念

> **理解 LaTeX 的工作原理** —— 从编译流程到文档结构，建立正确的认知模型。

---

## 1.1 LaTeX vs Word

| 对比维度 | LaTeX | Word |
|:---|:---|:---|
| **排版理念** | 所想即所得（关注内容结构） | 所见即所得（关注视觉效果） |
| **文件格式** | 纯文本 `.tex` | 二进制 `.docx` |
| **数学公式** | 行业标准，极其精美 | 需要公式编辑器 |
| **参考文献** | BibTeX 自动管理 | 手动或插件辅助 |
| **版本控制** | Git 完美支持 | 难以 diff |
| **学习曲线** | 初期较陡 | 上手快但深入难 |
| **模板系统** | 丰富的学术模板 | 模板较少 |

## 1.2 编译流程

LaTeX 不是"打开即用"的软件，而是需要**编译**的排版系统：

```
.tex 源文件  →  LaTeX 编译器  →  PDF 输出
   (你写的)      (xelatex/pdflatex)    (最终文档)
```

```bash
# 编译命令（以 xelatex 为例）
xelatex my-document.tex    # 第一次编译
xelatex my-document.tex    # 第二次编译（生成目录和交叉引用）
```

!!! tip "为什么需要编译两次？"

    第一次编译生成 `.aux` 辅助文件（记录标签和引用位置），第二次编译读取这些信息生成正确的目录和交叉引用编号。

## 1.3 文档基本结构

每个 LaTeX 文档都遵循固定的结构：

```latex
% 1. 文档类声明（必须）
\documentclass{article}

% 2. 导言区：引入宏包、设置样式
\usepackage[UTF8]{ctex}      % 中文支持
\usepackage{amsmath}          % 数学公式
\usepackage{graphicx}         % 插入图片

% 3. 文档信息
\title{文档标题}
\author{作者名}
\date{\today}                 % 自动生成日期

% 4. 正文区（必须）
\begin{document}
\maketitle                    % 生成标题页

% 你的内容写在这里

\end{document}
```

**代码解读：**

- `\documentclass{article}` 声明文档类型，`article` 适合短篇文章和论文
- 导言区（preamble）在 `\begin{document}` 之前，用于全局设置
- `\begin{document}...\end{document}` 之间的内容才会出现在 PDF 中

## 1.4 常用文档类

| 文档类 | 用途 | 典型场景 |
|:---|:---|:---|
| `article` | 短篇文章 | 期刊论文、课程报告 |
| `report` | 长篇报告 | 学位论文、项目报告 |
| `book` | 书籍 | 教材、专著 |
| `beamer` | 幻灯片 | 学术演讲、答辩 |
| `letter` | 信件 | 正式信函 |

## 1.5 常用工具

| 工具 | 类型 | 特点 |
|:---|:---|:---|
| **TeX Live** | 编译器套装 | 跨平台、最完整的 LaTeX 发行版 |
| **MiKTeX** | 编译器套装 | Windows 友好、按需安装宏包 |
| **Overleaf** | 在线编辑器 | 无需安装、实时协作、模板丰富 |
| **VS Code + LaTeX Workshop** | 本地编辑器 | 免费、功能强大 |

!!! tip "新手推荐"

    如果你是第一次接触 LaTeX，强烈推荐从 **Overleaf** 开始。它无需安装任何软件，打开浏览器就能写，还有海量模板可以一键使用。

---

## 本章要点总结

- [ ] 理解 LaTeX 是"编译型"排版系统（`.tex` → PDF）
- [ ] 掌握文档基本结构：`\documentclass` → 导言区 → `\begin{document}`
- [ ] 知道常用文档类：`article`、`report`、`book`、`beamer`
- [ ] 了解 Overleaf 是最友好的入门工具

---

👉 [进入第 2 章：核心语法 →](02-syntax.md)