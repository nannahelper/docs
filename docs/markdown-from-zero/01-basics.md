# 第 1 章：基础概念

> **Markdown 是什么？** —— 理解标记语言的设计哲学，选好你的写作工具。

---

## 1.1 Markdown 的起源

2004 年，博客写作者 John Gruber 和 Aaron Swartz 共同创建了 Markdown。他们的目标是设计一种 **易读易写** 的纯文本格式，让普通人不用学习 HTML 也能写出结构化的网页内容。

!!! info "标记语言 vs 所见即所得"

    - **标记语言（Markdown）**：用特殊符号标记格式，如 `**粗体**`。优点是纯文本、版本控制友好、不依赖特定软件。
    - **所见即所得（Word）**：直接看到最终效果。优点是直观，但文件格式封闭、不易版本管理。

## 1.2 设计哲学

Markdown 的核心设计原则只有两条：

1. **易读性优先**：即使不渲染，纯文本形式的 Markdown 也应该清晰可读。
2. **可转换为 HTML**：Markdown 是 HTML 的简化写法，任何 Markdown 都能转为标准 HTML。

```markdown
# 这是 Markdown 写法
## 二级标题
**粗体文字**

<!-- 等价于以下 HTML -->
<h1>这是 Markdown 写法</h1>
<h2>二级标题</h2>
<strong>粗体文字</strong>
```

**渲染效果：** Markdown 源码本身就像一份结构清晰的纯文本大纲，即使不经过渲染也能轻松阅读。渲染后则变成带有层级标题和格式的网页。

## 1.3 常用编辑器

| 编辑器 | 平台 | 特点 |
|:---|:---|:---|
| **VS Code** | 全平台 | 免费、插件丰富、实时预览 |
| **Typora** | 全平台 | 所见即所得、导出功能强大 |
| **Obsidian** | 全平台 | 笔记管理、双向链接、知识图谱 |
| **Notion** | 全平台 | 在线协作、数据库功能 |
| **GitHub 网页端** | 浏览器 | 在线编辑、直接预览 |

!!! tip "推荐选择"

    如果你已经安装了 VS Code，直接在 VS Code 中写 Markdown 是最方便的选择。安装 `Markdown Preview Enhanced` 插件即可实时预览。

## 1.4 文件扩展名

Markdown 文件使用 `.md` 或 `.markdown` 扩展名。推荐使用 `.md`，更简洁通用。

```bash
# 常见的 Markdown 文件名
README.md          # 项目说明文档
CONTRIBUTING.md    # 贡献指南
CHANGELOG.md       # 更新日志
docs/index.md      # 文档首页
```

## 1.5 Markdown 的变体

由于原始 Markdown 语法过于简单，出现了多种扩展版本：

| 变体 | 扩展功能 | 使用场景 |
|:---|:---|:---|
| **GitHub Flavored Markdown (GFM)** | 表格、任务列表、删除线、自动链接 | GitHub 平台 |
| **CommonMark** | 标准化语法规范 | 跨平台兼容 |
| **MDX** | 嵌入 JSX 组件 | React 文档站点 |
| **R Markdown** | 嵌入 R 代码 | 数据分析报告 |

本教程以 **GitHub Flavored Markdown** 为主要标准，这也是最广泛使用的 Markdown 变体。

---

## 本章要点总结

- [ ] 理解 Markdown 是"易读易写的纯文本标记语言"
- [ ] 了解 Markdown 的设计哲学：易读优先、可转 HTML
- [ ] 选择适合自己的 Markdown 编辑器
- [ ] 知道 `.md` 是标准文件扩展名
- [ ] 了解 GFM 是最常用的 Markdown 变体

---

👉 [进入第 2 章：核心语法 →](02-syntax.md)