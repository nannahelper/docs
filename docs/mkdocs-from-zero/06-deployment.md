# 第 6 章：部署上线

> **让全世界看到你的文档** —— 将 MkDocs 站点部署到 GitHub Pages，实现推送代码即自动更新。

---

## 6.1 部署方案概览

GitHub Pages 是 GitHub 提供的免费静态网站托管服务。结合 GitHub Actions，可以实现 **推送代码 → 自动构建 → 自动部署** 的全自动化流程：

```mermaid
flowchart LR
    A["git push<br/>推送代码"] --> B["GitHub Actions<br/>自动触发"]
    B --> C["mkdocs build<br/>构建静态文件"]
    C --> D["部署到 gh-pages 分支"]
    D --> E["网站更新完成<br/>公网可访问"]
```

---

## 6.2 准备工作：初始化 Git 仓库

在项目根目录执行：

```bash
git init
```

### 创建 .gitignore

在项目根目录创建 `.gitignore` 文件，排除不需要提交的内容：

```gitignore
# Python 虚拟环境
venv/
__pycache__/
*.pyc

# MkDocs 构建产物
site/

# IDE 配置
.vscode/
.idea/
```

### 首次提交

```bash
git add .
git commit -m "初始化 MkDocs 项目"
```

---

## 6.3 创建 GitHub 远程仓库

1. 打开 **https://github.com/new**
2. 填写仓库名称（例如 `my-docs`）
3. 选择 **Public**（公开仓库，GitHub Pages 免费）
4. **不要**勾选 "Add a README file"（我们已有本地代码）
5. 点击 **"Create repository"**

创建后，GitHub 会显示推送命令，复制并执行：

```bash
git remote add origin https://github.com/你的用户名/my-docs.git
git branch -M main
git push -u origin main
```

!!! note "默认分支名称"

    较新的 GitHub 仓库默认分支名为 `main`。如果你的本地分支是 `master`，可以用 `git branch -M main` 重命名。

---

## 6.4 配置 GitHub Actions 自动部署

### 步骤 1：创建工作流文件

在项目根目录创建 `.github/workflows/` 文件夹和 `deploy.yml` 文件：

```bash
mkdir -p .github/workflows
```

### 步骤 2：编写部署工作流

创建 `.github/workflows/deploy.yml`，内容如下：

```yaml
name: Deploy MkDocs Site

on:
  push:
    branches:
      - main          # 当 main 分支有推送时触发

permissions:
  contents: write      # 允许写入 gh-pages 分支

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout 代码
        uses: actions/checkout@v4

      - name: 设置 Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: 安装依赖
        run: |
          pip install mkdocs
          pip install mkdocs-material

      - name: 构建并部署
        run: mkdocs gh-deploy --force
```

!!! info "工作流文件解读"

    | 配置项 | 说明 |
    |:---|:---|
    | `on.push.branches` | 监听 `main` 分支的推送事件 |
    | `permissions.contents: write` | 授权写入仓库内容（部署需要） |
    | `actions/checkout@v4` | 拉取仓库代码 |
    | `actions/setup-python@v5` | 安装指定版本的 Python |
    | `mkdocs gh-deploy --force` | 构建站点并推送到 `gh-pages` 分支 |

### 步骤 3：提交并推送

```bash
git add .github/workflows/deploy.yml
git commit -m "添加 GitHub Actions 自动部署工作流"
git push
```

推送后，GitHub 会自动触发工作流。你可以在仓库页面的 **"Actions"** 标签页查看构建进度。

---

## 6.5 启用 GitHub Pages

1. 进入仓库的 **"Settings"** → **"Pages"**
2. 在 **"Build and deployment"** 部分：
   - **Source**：选择 **"Deploy from a branch"**
   - **Branch**：选择 **`gh-pages`**，目录选择 **`/ (root)`**
3. 点击 **"Save"**

等待几分钟后，页面顶部会显示你的网站地址：

```
https://你的用户名.github.io/my-docs/
```

!!! tip "首次部署需要等待"

    首次部署可能需要 1~3 分钟。如果访问时看到 404 页面，请稍等片刻再刷新。你可以在 **Actions** 标签页确认工作流是否已完成。

---

## 6.6 更新 site_url

部署成功后，回到 `mkdocs.yml`，将 `site_url` 更新为实际的 GitHub Pages 地址：

```yaml
site_url: https://你的用户名.github.io/my-docs/
```

提交并推送这个修改：

```bash
git add mkdocs.yml
git commit -m "更新 site_url 为生产环境地址"
git push
```

!!! warning "site_url 很重要"

    如果不设置正确的 `site_url`，以下功能会出问题：
    
    - `sitemap.xml` 中的链接会指向错误的地址
    - 搜索功能的索引可能无法正常工作
    - 社交分享时的预览链接不正确

---

## 6.7 日常更新流程

部署完成后，日常更新文档只需三步：

```bash
# 1. 编辑 Markdown 文件（在 VS Code 中）
# 2. 本地预览确认效果
mkdocs serve

# 3. 提交并推送
git add .
git commit -m "更新文档内容"
git push
```

推送后，GitHub Actions 会自动构建并部署，约 1 分钟后网站即更新。

---

## 6.8 常见问题排查

### 部署失败：gh-pages 分支不存在

**现象：** Actions 日志显示 `gh-pages` 相关错误。

**解决：** 确保仓库 Settings → Pages 中已选择 `gh-pages` 分支作为部署源。首次部署时，`mkdocs gh-deploy` 会自动创建该分支。

### 网站样式丢失

**现象：** 页面显示但没有任何样式（纯白背景、无导航）。

**解决：** 检查 `mkdocs.yml` 中的 `site_url` 是否正确。如果仓库名不是 `用户名.github.io` 格式，需要确保 `site_url` 包含仓库名路径。

### 搜索功能不工作

**现象：** 搜索框输入后无结果。

**解决：** 
1. 确认 `site_url` 已正确设置
2. 确认 `plugins` 中包含了 `search` 插件
3. 重新推送触发完整构建

### 图片无法显示

**现象：** 本地预览正常，部署后图片显示为叉号。

**解决：** 检查图片路径是否使用了相对路径（如 `../assets/logo.png`）。MkDocs 中推荐使用相对于 `docs/` 目录的路径。

---

## 6.9 进阶：自定义域名

如果你想使用自己的域名（如 `docs.example.com`）：

1. 在 `docs/` 目录下创建 `CNAME` 文件，内容为你的域名：

```
docs.example.com
```

2. 在域名 DNS 服务商处添加 CNAME 记录，指向 `你的用户名.github.io`

3. 在 GitHub 仓库 Settings → Pages 中填写自定义域名

---

## 本章要点总结

- [ ] 初始化了 Git 仓库并创建了 `.gitignore`
- [ ] 在 GitHub 上创建了远程仓库并推送了代码
- [ ] 配置了 GitHub Actions 自动部署工作流
- [ ] 在 GitHub Pages 设置中启用了 `gh-pages` 分支部署
- [ ] 更新了 `site_url` 为生产环境地址
- [ ] 网站可通过公网 URL 正常访问
- [ ] 了解了日常更新流程和常见问题排查方法

---

## 🎉 恭喜你！

你已经完成了 MkDocs + GitHub Pages 的完整学习之旅。回顾一下你掌握的技能：

| 技能 | 说明 |
|:---|:---|
| 环境搭建 | Python、Git、VS Code 安装配置 |
| MkDocs 基础 | 项目创建、本地预览、构建 |
| 配置管理 | mkdocs.yml 导航、主题、扩展配置 |
| 内容创作 | Markdown 写作、弹窗、代码块、图表 |
| 主题定制 | 配色、字体、Logo、自定义 CSS |
| 自动部署 | GitHub Actions CI/CD、GitHub Pages |

现在，去创建属于你自己的文档网站吧！🚀

---

👉 [返回教程首页 →](index.md)