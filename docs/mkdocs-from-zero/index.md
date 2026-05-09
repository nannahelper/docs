# MkDocs 与 GitHub Pages 部署指南

> **从零搭建专业文档网站** —— 用 MkDocs Material 主题 + GitHub Pages，打造属于你自己的在线文档中心。

---

## 教程简介

MkDocs 是 Python 生态中最流行的静态文档站点生成器，配合 Material for MkDocs 主题，可以快速构建出外观专业、功能齐全的文档网站。本教程将带你走完从环境搭建到线上部署的完整流程，最终你将拥有一个可通过公网访问的、带搜索和导航功能的文档站点。

!!! info "为什么学 MkDocs + GitHub Pages？"

    - **完全免费**：MkDocs 开源免费，GitHub Pages 提供免费静态托管
    - **极速上手**：只需 Markdown 写作 + 一条命令即可生成站点
    - **专业外观**：Material 主题开箱即用，支持搜索、暗色模式、代码高亮
    - **自动化部署**：推送代码即自动更新网站，无需手动操作
    - **版本控制**：文档和代码一起纳入 Git 管理，历史可追溯

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 独立完成 MkDocs 文档站点的搭建、配置、内容编写与 GitHub Pages 部署 |
| **预计时长** | 4~6 小时 |
| **前置知识** | 基本的命令行操作、Git 基础（clone / add / commit / push） |
| **最终产出** | 一个可通过 `https://<你的用户名>.github.io/<仓库名>/` 访问的在线文档网站 |

---

## 章节导航

| 章节 | 内容 | 预计时长 |
|:---|:---|:---:|
| [第 1 章：环境准备](01-environment-setup.md) | Python、pip、Git、VS Code 安装与验证 | 45 分钟 |
| [第 2 章：MkDocs 入门](02-mkdocs-basics.md) | 安装 MkDocs、创建项目、本地预览 | 45 分钟 |
| [第 3 章：配置详解](03-configuration.md) | mkdocs.yml 深度配置：导航、主题、扩展 | 60 分钟 |
| [第 4 章：内容创作](04-content-creation.md) | Markdown 写作、弹窗组件、代码块、表格 | 60 分钟 |
| [第 5 章：主题定制](05-theme-customization.md) | Material 主题配色、字体、Logo、自定义 CSS | 45 分钟 |
| [第 6 章：部署上线](06-deployment.md) | GitHub 仓库创建、GitHub Actions CI/CD、发布上线 | 60 分钟 |

---

## 你将构建的站点预览

完成本教程后，你的文档站点将具备以下功能：

- 左侧可折叠的层级导航菜单
- 全站全文搜索
- 浅色 / 深色模式切换
- 代码块一键复制
- 响应式布局（适配手机、平板、桌面）
- 推送代码自动部署更新

```yaml
# 你最终完成的 mkdocs.yml 大致长这样
site_name: 我的文档站点
site_url: https://<用户名>.github.io/<仓库名>/
theme:
  name: material
  features:
    - navigation.sections
    - search.suggest
    - content.code.copy
nav:
  - 首页: index.md
  - 入门指南:
    - 快速开始: guide/quickstart.md
    - 安装说明: guide/installation.md
```

---

👉 [开始学习：第 1 章 · 环境准备 →](01-environment-setup.md)