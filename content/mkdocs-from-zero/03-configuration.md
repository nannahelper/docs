# 第 3 章：配置详解

> **掌控你的文档站点** —— 深入理解 `mkdocs.yml` 配置，打造结构清晰、功能齐全的导航系统。

---

## 3.1 mkdocs.yml 全景图

`mkdocs.yml` 是 MkDocs 项目的核心配置文件，控制着站点的所有行为。一个完整的配置通常包含以下几个部分：

```yaml
site_name: 站点名称              # 浏览器标签页标题
site_description: 站点描述       # HTML meta description
site_author: 作者名              # HTML meta author
site_url: https://example.com/   # 生产环境 URL（重要！）

theme:                           # 主题配置
  name: material                 # 使用 Material 主题
  language: zh                   # 界面语言
  features: []                   # 功能开关

nav:                             # 导航菜单
  - 首页: index.md

markdown_extensions: []          # Markdown 扩展

plugins: []                      # 插件列表
```

---

## 3.2 配置导航菜单（nav）

`nav` 是 MkDocs 最重要的配置项之一，它决定了侧边栏的结构。

### 平铺式导航

最简单的写法，所有页面平铺展示：

```yaml
nav:
  - 首页: index.md
  - 快速开始: guide/quickstart.md
  - 安装说明: guide/installation.md
  - API 参考: api/reference.md
```

### 层级式导航（推荐）

将相关页面分组，形成可折叠的层级结构：

```yaml
nav:
  - 首页: index.md
  - 入门指南:
    - 快速开始: guide/quickstart.md
    - 安装说明: guide/installation.md
    - 基本用法: guide/basics.md
  - API 参考:
    - 概述: api/overview.md
    - 认证: api/authentication.md
    - 接口列表: api/endpoints.md
  - 常见问题: faq.md
```

**渲染效果：** 层级式导航在侧边栏中显示为可折叠的分组。用户点击"入门指南"会展开其下的三个子页面，点击"API 参考"会展开另外三个子页面。这种结构让导航更加清晰，特别适合页面较多的文档站点。

!!! tip "导航标题 vs 页面标题"

    `nav` 中冒号左边的文字是 **导航标题**（显示在侧边栏），可以自由命名，不必与 Markdown 文件中的一级标题一致。这让你可以用更简洁的文字作为导航标签。

---

## 3.3 Material 主题功能开关（features）

Material for MkDocs 提供了丰富的功能开关，通过 `theme.features` 配置：

```yaml
theme:
  name: material
  features:
    - navigation.sections      # 侧边栏分组折叠
    - navigation.top           # 回到顶部按钮
    - navigation.tracking      # 地址栏自动更新当前页面锚点
    - search.suggest           # 搜索建议（输入时自动补全）
    - search.highlight         # 搜索结果高亮关键词
    - search.share             # 搜索链接分享
    - content.code.copy        # 代码块一键复制按钮
    - content.code.annotate    # 代码块行内注释
    - content.tabs.link        # 标签页链接共享
```

!!! info "常用功能推荐"

    | 功能 | 效果 |
    |:---|:---|
    | `navigation.sections` | 侧边栏顶层分组可折叠 |
    | `navigation.top` | 页面右下角显示"回到顶部"按钮 |
    | `search.suggest` | 搜索框输入时显示建议 |
    | `search.highlight` | 搜索结果中高亮匹配文字 |
    | `content.code.copy` | 每个代码块右上角显示复制按钮 |
    | `content.code.annotate` | 代码块中可添加行内注释标记 |

---

## 3.4 配置配色方案

Material 主题支持浅色和深色两种模式，以及丰富的主题色：

```yaml
theme:
  name: material
  palette:
    # 浅色模式
    - scheme: default
      primary: indigo          # 主色调
      accent: indigo           # 强调色
      toggle:
        icon: material/brightness-7
        name: 切换至深色模式

    # 深色模式
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: 切换至浅色模式
```

**可用的主色调（primary）：** `red`、`pink`、`purple`、`deep purple`、`indigo`、`blue`、`light blue`、`cyan`、`teal`、`green`、`light green`、`lime`、`yellow`、`amber`、`orange`、`deep orange`、`brown`、`grey`、`blue grey`、`black`、`white`

---

## 3.5 Markdown 扩展配置

MkDocs 通过 Python-Markdown 扩展来增强 Markdown 的渲染能力：

```yaml
markdown_extensions:
  - admonition            # 弹窗组件（!!! note、!!! warning 等）
  - attr_list             # 属性列表（给元素添加 class、id）
  - def_list              # 定义列表
  - footnotes             # 脚注
  - md_in_html            # HTML 中嵌套 Markdown
  - tables                # 增强表格
  - toc:                  # 目录
      permalink: true     # 标题旁显示锚点链接
  - pymdownx.highlight:   # 代码高亮
      anchor_linenums: true
  - pymdownx.superfences: # 嵌套代码块
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:      # 标签页
      alternate_style: true
  - pymdownx.tasklist:    # 任务列表
      custom_checkbox: true
  - pymdownx.emoji        # Emoji 支持
  - pymdownx.details      # 可折叠详情
```

!!! tip "最小推荐配置"

    如果你不确定需要哪些扩展，至少保留以下四个最常用的：
    
    ```yaml
    markdown_extensions:
      - admonition
      - pymdownx.highlight
      - pymdownx.superfences
      - pymdownx.tabbed
    ```

---

## 3.6 实战：配置你的第一个完整 mkdocs.yml

将以下内容复制到你的 `mkdocs.yml` 中，替换默认配置：

```yaml
site_name: 我的文档站点
site_description: 一个用 MkDocs Material 构建的专业文档网站
site_author: 你的名字
site_url: https://你的用户名.github.io/你的仓库名/

theme:
  name: material
  language: zh
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: 切换至深色模式
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: 切换至浅色模式
  features:
    - navigation.sections
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy
    - content.code.annotate

nav:
  - 首页: index.md
  - 入门指南:
    - 快速开始: guide/quickstart.md
    - 安装说明: guide/installation.md

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - toc:
      permalink: true
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
```

保存后运行 `mkdocs serve`，观察侧边栏的层级结构和搜索功能是否生效。

!!! note "site_url 暂时可以留空"

    在本地开发阶段，`site_url` 可以暂时留空或填写一个占位 URL。但在部署到 GitHub Pages 之前，必须填写正确的生产环境 URL，否则 sitemap.xml 和搜索索引会出错。

---

## 本章要点总结

- [ ] 理解 `mkdocs.yml` 的整体结构和各部分作用
- [ ] 能配置层级式导航菜单（nav）
- [ ] 了解 Material 主题的常用功能开关
- [ ] 能配置浅色 / 深色模式切换
- [ ] 了解常用的 Markdown 扩展及其作用
- [ ] 完成了一份可用的 `mkdocs.yml` 配置

---

👉 [进入第 4 章：内容创作 →](04-content-creation.md)