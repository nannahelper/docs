# 南哪助手应用教程汇总

> **小破手今天搓代码了吗？** —— 从零开始，用生活化比喻轻松掌握编程技能。

[![MkDocs](https://img.shields.io/badge/MkDocs-Material-4051b5?style=flat&logo=materialformkdocs)](https://squidfunk.github.io/mkdocs-material/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-在线预览-success)](https://nannahelper.github.io/docs/)

---

## 项目概述

**南哪助手应用教程汇总** 是一个面向零基础学习者的开源教程集合，旨在通过通俗易懂的生活化比喻、手把手的实操步骤和丰富的代码示例，帮助编程新手从零开始掌握现代软件开发的核心技能。

### 项目背景

在南哪学生社区中，我们发现大量同学对编程充满兴趣却苦于入门门槛过高——传统教程充斥着晦涩的专业术语、跳跃的知识结构，让初学者望而却步。本项目由此诞生，致力于打造一套 **"像朋友聊天一样学编程"** 的教程体系。

### 价值主张

- **零基础友好**：每个概念都配有生活化比喻，消除术语恐惧
- **手把手教学**：每一步都有验证方法，确保学习者能跟上节奏
- **实战导向**：每章配备实践任务，学完就能做出东西
- **持续更新**：基于学习者反馈不断迭代优化

---

## 教程内容

### 1. 零基础入门 LLM API 开发与应用

从零开始学习大语言模型（LLM）API 的开发与应用，使用 Python 语言，适合完全没有编程基础的新手。

| 章节 | 内容 |
|:---|:---|
| 环境准备 | Python 安装、虚拟环境配置、API 密钥获取 |
| API 集成入门 | 第一个 API 调用程序、理解请求与响应 |
| 核心概念 | Token、Temperature、System Prompt 等关键概念 |
| Chatbot 实战 | 构建一个完整的命令行聊天机器人 |
| 批量处理 | 批量调用 API、处理大规模数据 |
| 安全与展望 | API Key 安全、成本控制、进阶方向 |

### 2. Git 与 GitHub 团队协作指南

掌握版本控制和团队协作的核心技能，从单机操作到团队项目管理全覆盖。

| 章节 | 内容 |
|:---|:---|
| 认识版本控制 | Git 是什么、为什么需要版本控制 |
| 本地操作 | init、add、commit、log、.gitignore |
| 分支管理 | branch、checkout、merge、rebase |
| 远程操作 | clone、push、pull、fetch、remote |
| 团队协作 | Pull Request、Code Review、Fork 工作流 |
| 冲突解决 | merge conflict 的产生与解决 |
| 进阶自救 | reset、revert、stash、cherry-pick |
| 项目管理 | Projects、Discussions、敏捷开发实践 |

### 3. Linux 新手入门指南

用生活比喻轻松掌握命令行，消除对"黑窗口"的恐惧感。

| 章节 | 内容 |
|:---|:---|
| 认识 Linux | 遥控器 vs 语音控制——理解 Linux 哲学 |
| 搭建环境 | 虚拟机/WSL 安装，安全又简单 |
| 命令行初体验 | ls、cd、pwd 等基本命令 |
| 文件操作 | cp、mv、rm、find——整理数字抽屉 |
| 用户与权限 | chmod、chown——房间的钥匙和锁 |
| 实用技巧 | 管道、重定向、脚本自动化 |

### 4. 网络爬虫新手指南

从 HTTP 协议基础到工程化实战，掌握豆瓣电影 Top 250 全榜单数据抓取。

| 章节 | 内容 |
|:---|:---|
| 揭秘爬虫 | 浏览器背后的秘密——HTTP 协议入门 |
| 环境搭建 | requests、BeautifulSoup 库安装 |
| 精准解析 | CSS 选择器、XPath——像外科医生一样提取数据 |
| 数据持久化 | CSV、JSON、SQLite——将战利品存入仓库 |
| 应对反爬 | User-Agent、延时策略、代理 IP |
| 完整实战 | 抓取豆瓣 Top 250 全榜单 |

### 5. 《人月神话》软件工程入门

以 Fred Brooks 的经典著作《人月神话》为蓝本，系统讲解软件工程的核心思想与实践。

| 章节 | 内容 |
|:---|:---|
| 焦油坑 | 编程的乐趣与苦恼 |
| 人月神话 | 为什么加人不能加速项目 |
| 外科手术队伍 | 高效团队的组织方式 |
| 没有银弹 | 软件工程的本质困难 |
| ... | 共 19 章完整解读 |

---

## 技术架构

### 技术栈

| 层级 | 技术选型 | 说明 |
|:---|:---|:---|
| 静态站点生成 | [MkDocs](https://www.mkdocs.org/) | Python 生态最流行的文档生成器 |
| 主题 | [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) | 功能丰富的 Material Design 主题 |
| 托管部署 | [GitHub Pages](https://pages.github.com/) | 免费、稳定的静态站点托管 |
| 内容格式 | Markdown | 简洁、易读、版本控制友好 |
| CI/CD | GitHub Actions | 自动构建与部署 |

### 项目结构

```
docs/
├── mkdocs.yml                  # MkDocs 配置文件（站点导航、主题、插件）
├── requirements.txt            # Python 依赖清单
├── README.md                   # 项目说明文档
├── .gitignore                  # Git 忽略规则
├── prompt.md                   # AI 辅助写作的 Prompt 模板
└── docs/                       # 文档内容目录
    ├── index.md                # 站点首页
    ├── assets/                 # 静态资源（截图、图片等）
    ├── llm_from_zero_with_python/   # LLM API 开发教程
    ├── git_github_from_zero/        # Git 与 GitHub 教程
    ├── linux_from_zero/             # Linux 入门教程
    ├── web-crawler-from-zero/       # 网络爬虫教程
    └── mythical_man_month/          # 《人月神话》解读
```

### 架构设计

```
┌─────────────────────────────────────────────┐
│                  GitHub Pages                │
│            nannahelper.github.io/docs        │
└──────────────────┬──────────────────────────┘
                   │ 自动部署
┌──────────────────▼──────────────────────────┐
│              GitHub Actions                  │
│         mkdocs build → gh-deploy             │
└──────────────────┬──────────────────────────┘
                   │ 触发构建
┌──────────────────▼──────────────────────────┐
│            GitHub Repository                 │
│       github.com/nannahelper/docs            │
│  ┌──────────────────────────────────────┐   │
│  │         Markdown 源文件               │   │
│  │  (教程内容 + mkdocs.yml 配置)         │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 环境配置与安装

### 前置要求

- Python 3.9 或更高版本
- Git（用于版本控制和协作）
- pip（Python 包管理器，通常随 Python 一起安装）

### 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/nannahelper/docs.git
cd docs

# 2. 创建虚拟环境（推荐）
python -m venv .venv

# 3. 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 启动本地预览服务器
mkdocs serve
```

启动后，在浏览器中访问 `http://127.0.0.1:8000` 即可预览站点。修改文档内容后，浏览器会自动刷新。

### 构建静态站点

```bash
mkdocs build
```

构建产物将输出到 `site/` 目录，可直接部署到任意静态文件服务器。

---

## 使用指南

### 在线阅读

直接访问在线站点：**[https://nannahelper.github.io/docs/](https://nannahelper.github.io/docs/)**

### 本地阅读

按照上述"环境配置与安装"步骤启动本地服务器后，在浏览器中阅读。

### 贡献教程内容

如果你想为项目贡献新的教程或改进现有内容：

```bash
# 1. Fork 本仓库

# 2. 克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/docs.git
cd docs

# 3. 创建功能分支
git checkout -b feature/my-tutorial

# 4. 编写内容
# 在 docs/ 目录下创建新的教程文件夹
# 在 mkdocs.yml 的 nav 部分添加导航配置

# 5. 本地预览
mkdocs serve

# 6. 提交更改
git add .
git commit -m "docs: add my-tutorial"

# 7. 推送分支
git push origin feature/my-tutorial

# 8. 在 GitHub 上创建 Pull Request
```

### 写作规范

本项目遵循严格的排版规范，确保所有教程风格统一：

- **标题层级**：一级标题带趣味副标题，二级标题带数字标号
- **术语解释**：使用 `!!! info` 弹窗解释专业术语
- **生活化比喻**：使用 `!!! example` 弹窗提供类比理解
- **避坑指南**：使用 `!!! tip` / `!!! warning` 弹窗标注注意事项
- **多系统适配**：使用 Tabbed Content 语法区分 Windows/macOS 操作
- **代码注释**：所有代码块必须包含详细的中文注释

详细的写作规范请参考 [prompt.md](prompt.md)。

---

## 常见问题

### Q: 我完全没有编程基础，能学会吗？

A: 完全可以！本项目的核心理念就是"零基础友好"。每个概念都配有生活化比喻，每一步都有验证方法。建议从 LLM API 开发或 Linux 入门开始。

### Q: 教程内容会定期更新吗？

A: 会的。我们根据技术发展和学习者反馈持续更新教程内容。欢迎通过 Issue 或 PR 提出改进建议。

### Q: 如何报告教程中的错误？

A: 请在 [GitHub Issues](https://github.com/nannahelper/docs/issues) 中提交问题，描述错误位置和具体内容，我们会尽快修复。

### Q: 可以离线阅读吗？

A: 可以。克隆仓库后使用 `mkdocs serve` 启动本地服务器即可离线阅读。也可以使用 `mkdocs build` 生成静态文件。

### Q: 教程中的代码示例可以直接使用吗？

A: 可以。所有代码示例均经过验证，可直接复制运行。但请注意 API 调用可能产生费用，建议先了解相关平台的定价策略。

---

## 贡献指南

我们欢迎所有形式的贡献！无论是修正错别字、改进比喻、添加新章节，还是创建全新的教程。

### 贡献方式

1. **报告问题**：在 [Issues](https://github.com/nannahelper/docs/issues) 中提交 Bug 报告或功能建议
2. **改进内容**：Fork 仓库 → 修改 → 提交 Pull Request
3. **新增教程**：按照现有教程的结构创建新内容，确保遵循写作规范
4. **补充截图**：为教程添加操作截图，存放于 `docs/assets/` 目录

### 提交规范

- 提交信息格式：`docs: 简短描述` 或 `fix: 简短描述`
- 一个 PR 只做一件事，保持变更聚焦
- 新增教程需同步更新 `mkdocs.yml` 中的导航配置
- 确保本地 `mkdocs serve` 预览无报错

### 代码审查

所有 Pull Request 需要经过至少一位维护者审查后才能合并。审查重点包括：

- 内容准确性和教学逻辑
- 排版格式是否符合规范
- 代码示例是否可运行
- 比喻是否恰当易懂

---

## 开源许可

本项目采用 [MIT License](LICENSE) 开源协议。你可以自由地使用、修改和分发本项目的内容，但需保留原始版权声明。

---

## 致谢

- [MkDocs](https://www.mkdocs.org/) 和 [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 提供了优秀的文档框架
- [GitHub Pages](https://pages.github.com/) 提供了免费的站点托管
- 所有为本项目贡献内容的开发者们

---

**准备好开始你的学习之旅了吗？** [进入教程首页 →](https://nannahelper.github.io/docs/)
