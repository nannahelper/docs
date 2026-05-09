# 第 1 章：环境准备

> **工欲善其事，必先利其器** —— 安装 Python、Git 和 VS Code，为 MkDocs 开发打下基础。

---

## 1.1 你需要安装什么

MkDocs 是基于 Python 的静态站点生成器，部署依赖 Git 和 GitHub。在开始之前，需要确保以下工具已正确安装：

| 工具 | 用途 | 最低版本 |
|:---|:---|:---|
| **Python** | MkDocs 运行环境 | 3.8+ |
| **pip** | Python 包管理器（安装 MkDocs） | 随 Python 自带 |
| **Git** | 版本控制 + 推送代码到 GitHub | 2.0+ |
| **VS Code**（推荐） | 编辑 Markdown 和配置文件 | 最新版 |

!!! tip "已有这些工具？"

    如果你已经安装了 Python 和 Git，可以直接跳到 [1.5 验证安装](#15-验证安装) 部分，确认版本符合要求后进入下一章。

---

## 1.2 安装 Python

### Windows

1. 访问 Python 官网：**https://www.python.org/downloads/**
2. 点击黄色的 **"Download Python 3.x.x"** 按钮下载安装包
3. **重要**：运行安装包时，务必勾选底部的 **"Add Python to PATH"** 复选框
4. 点击 **"Install Now"** 完成安装

!!! danger "别忘了勾选 Add Python to PATH！"

    如果不勾选这个选项，后续在命令行中输入 `python` 会提示"找不到命令"。如果忘记勾选，需要重新运行安装程序或手动配置环境变量。

### macOS

打开 **终端（Terminal）**，使用 Homebrew 安装：

```bash
# 如果还没安装 Homebrew，先执行：
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Python
brew install python@3.12
```

### Linux（Ubuntu/Debian）

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---

## 1.3 安装 Git

### Windows

访问 **https://git-scm.com/download/win**，下载安装包后一路默认选项安装即可。

### macOS

```bash
brew install git
```

### Linux（Ubuntu/Debian）

```bash
sudo apt install git
```

安装完成后，配置你的 Git 用户名和邮箱（与 GitHub 账号一致）：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

---

## 1.4 安装 VS Code（推荐编辑器）

VS Code 是目前最流行的代码编辑器，对 Markdown 有出色的支持。

1. 访问 **https://code.visualstudio.com/** 下载安装
2. 安装后，推荐安装以下扩展：

| 扩展名称 | 用途 |
|:---|:---|
| **Markdown Preview Enhanced** | 实时预览 Markdown 渲染效果 |
| **Markdown All in One** | 快捷键生成目录、自动补全 |
| **YAML** | YAML 语法高亮（编辑 mkdocs.yml 用） |
| **Python** | Python 语法支持 |

!!! tip "安装扩展的方法"

    打开 VS Code，点击左侧的 **扩展图标**（四个方块），在搜索框中输入扩展名称，点击 **"安装"** 即可。

---

## 1.5 验证安装

打开 **终端**（Windows 按 `Win + R`，输入 `cmd`；macOS 打开 Terminal），依次执行以下命令验证：

```bash
# 验证 Python（应显示 3.8 或更高版本）
python --version
# 预期输出：Python 3.12.x

# 验证 pip（应显示版本号）
pip --version
# 预期输出：pip 24.x from ... (python 3.12)

# 验证 Git（应显示 2.0 或更高版本）
git --version
# 预期输出：git version 2.44.x
```

**渲染效果：** 三条命令分别验证 Python、pip 和 Git 是否正确安装。如果每条命令都输出了版本号（而非报错），说明环境准备完成。

!!! note "python 命令找不到？"

    在 Windows 上，有时 `python` 命令不可用，试试 `python3` 或 `py`：
    
    ```bash
    python3 --version
    # 或
    py --version
    ```

---

## 1.6 创建项目文件夹

在你的电脑上选择一个合适的位置，创建项目文件夹：

```bash
# Windows（在 CMD 或 PowerShell 中）
mkdir D:\my-docs
cd D:\my-docs

# macOS / Linux
mkdir ~/my-docs
cd ~/my-docs
```

这个文件夹将作为你的 MkDocs 项目的根目录，后续所有操作都在此目录下进行。

---

## 本章要点总结

- [ ] Python 3.8+ 已安装并可在命令行中调用
- [ ] pip 已安装并可正常使用
- [ ] Git 已安装并配置了用户名和邮箱
- [ ] VS Code 已安装（可选但推荐）
- [ ] 项目文件夹已创建

---

👉 [进入第 2 章：MkDocs 入门 →](02-mkdocs-basics.md)