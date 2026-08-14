# 第 4 章：包管理器与常用开发工具 — 用一条命令安装软件

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 35 分钟 |
| 核心概念 | 系统包管理器、软件源、PATH、版本验证 |
| 核心比喻 | 包管理器是软件商店的命令行收银台 |
| 实践任务 | 用命令行安装 Git、Python 和 Node.js，并记录版本 |
| 难度等级 | ★★☆☆☆ |

## 包管理器解决的是“从哪里装、装什么版本”

命令行安装工具并不是把软件变成魔法。winget、Scoop、Homebrew 和 APT 都在维护一份软件来源与安装规则，帮助你查找、安装、升级和卸载程序；它们的仓库范围、权限模型和命令习惯却不同。先确认系统与来源，再复制命令，能避免把一套系统的教程误用到另一套系统。

软件安装完成后，还要验证命令是否真的可用。安装器成功退出，只能说明安装过程结束；新终端能找到版本号，才说明 PATH 和当前会话已经连接起来。遇到版本冲突时，先查实际调用路径，不要盲目重复安装。

## 4.1 先选择与你的系统匹配的工具

不要把不同系统的命令混在一起。包管理器负责“找到、下载、安装、升级和卸载”软件；它不是编译器，也不会替你理解项目代码。

| 系统 | 推荐入口 | 先验证 |
|:---|:---|:---|
| Windows | `winget`；熟悉后可选 `scoop` | `winget --version` |
| macOS | Homebrew | `brew --version` |
| Ubuntu / Debian | APT | `apt --version` |

!!! warning "安全边界"
    只从系统自带商店、官方文档或可信的软件源安装工具。看到要求关闭安全软件、粘贴陌生远程脚本或使用管理员权限的命令时，先停下来核对来源。

## 4.2 Windows：winget

`winget` 是 Windows 的命令行应用安装工具。先在 PowerShell 中执行：

```powershell
winget --version
winget search Git.Git
```

确认搜索结果后安装 Git：

```powershell
winget install --id Git.Git -e
git --version
```

再安装 Python 和 Node.js 长期支持版：

```powershell
winget install --id Python.Python.3.12 -e
winget install --id OpenJS.NodeJS.LTS -e
python --version
node --version
```

安装完成后，如果当前终端仍提示“找不到命令”，关闭并重新打开终端，让新的 PATH 生效。

## 4.3 Windows：Scoop

Scoop 适合希望把开发工具安装到用户目录、减少管理员权限依赖的学习者。请先打开 [Scoop 官方文档](https://scoop.sh/)，核对当前安装命令，再执行官方提供的脚本。

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
scoop --version
scoop bucket add main
scoop install git python nodejs-lts
```

!!! warning "为什么要先看官方文档"
    `irm ... | iex` 会下载并执行远程脚本。它适合学习命令行安装流程，但不应盲目复制任何陌生网站给出的同类命令。安装前检查域名、脚本内容和当前 PowerShell 窗口。

## 4.4 macOS 与 Linux

macOS 可以使用 Homebrew：

```bash
brew --version
brew install git python node
git --version
python3 --version
node --version
```

Ubuntu / Debian 可以使用 APT：

```bash
sudo apt update
sudo apt install git python3 python3-venv nodejs npm
git --version
python3 --version
node --version
npm --version
```

`sudo` 是临时借用管理员权限，不是“修复一切问题”的按钮。安装前先看清软件包名称，安装后立刻执行版本验证。

## 4.5 记录环境结果

把成功输出保存到项目的 `environment-report.txt`：

```text
系统：Windows / macOS / Ubuntu
终端：PowerShell / zsh / bash
Git：
Python：
Node.js：
npm：
安装方式：winget / scoop / brew / apt / 其他
```

## ✅ 验证步骤

分别执行本系统对应的版本命令；每条都能输出版本号后，再继续下一章。若某条失败，记录“命令、完整输出、当前目录、安装方式”，不要连续尝试多个来源。

## 📝 本章总结

- `winget`、`scoop`、Homebrew 和 APT 是安装软件的工具，不是语言本身。
- 安装后必须重新打开终端并验证 PATH。
- 远程安装脚本需要先审查来源，权限越高越要谨慎。

## ✏️ 课后练习

1. 用系统包管理器安装 Git，并把版本写入环境报告。
2. 对比 `winget search` 和 `scoop search` 的结果，说明它们的软件来源有什么不同。

## 🔮 下一章预告

下一章会用 Node.js、npm 和 `npx` 创建一个最小 JavaScript 项目，理解“安装包”和“运行工具”的区别。
