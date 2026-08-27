# 命令行开发环境配置

这是赛博扫盲的开发扩展课。以 C/C++ 为主线，从一台刚装好的电脑开始，建立可以编译、运行、安装依赖和管理项目的开发环境；如果你只是想正常上网、管理账号或查资料，不需要先学这门课。

开发环境不是“装好几个软件”这么简单。编辑器、编译器、解释器、包管理器和 Git 之间有各自的职责；它们能否协作，还取决于系统知道去哪寻找命令、项目依赖是否隔离、版本是否能被别人复现。少了其中任意一环，你都可能遇到“明明安装了却找不到”“在我的电脑上能运行”“换个终端就失效”等问题。

本教程会把一次安装过程变成一组可解释的检查。默认以 Windows 11 为主线，macOS 和 Linux 的差异放在对应小节；每执行一条命令，都先说明它会改变什么、应该看到什么、出现异常时保留什么证据。你最终得到的不是一台“碰巧能用”的电脑，而是一份自己能读懂、能排错、能交给同学复现的环境记录。

## 📖 关于本教程

| 项目 | 内容 |
|:---|:---|
| 适合人群 | 已决定开始写代码、但不知道如何安装和验证开发工具的初学者 |
| 预计时长 | 快速阅读约 45 分钟；完整安装按设备和网络情况安排 |
| 适用版本 | Windows 11、macOS 14+、Ubuntu 22.04+；命令随版本变化 |
| 维护状态 | 维护中 |
| 最后更新 | 2026-08-14 |
| 反馈入口 | [GitHub Issues](https://github.com/nannahelper/docs/issues) |

## 🎯 学习目标

- 能从命令行检查系统、终端和 PATH 环境变量。
- 能安装并验证 C/C++ 编译器，以 C17 和 C++20 编译小程序。
- 能安装 Python、Git 和常见包管理器，并理解它们的职责。
- 能创建隔离的项目目录，使用虚拟环境或锁定依赖。
- 能定位“命令找不到、编译失败、包安装失败”等常见环境问题。

## 📋 前置要求

- 会使用文件管理器和复制粘贴命令。
- 有管理员权限，或能请求管理员安装系统工具。
- 不要求提前会 C/C++ 或 Python。

## 🧭 学习前先做一个判断

这门课会安装编译器、Python、Node.js、Git 和包管理器，适合准备写代码的人，不适合作为第一次认识电脑的课程。你只需要会复制粘贴、看懂当前目录，并愿意在每条命令执行前确认范围；不会 C/C++、Python 或 Linux 不影响开始。

默认在空目录中练习，优先使用系统自带的 `winget`、官方安装器或官方文档。Scoop、Homebrew、APT、npm、pnpm 和 Bun 是不同场景下的工具，不需要一次全部安装；若命令涉及管理员权限、远程脚本、删除文件或修改系统设置，先停下来核对来源。

## 🗺️ 学习路线

| 章节 | 主题 | 核心比喻 | 预计时长 |
|:---|:---|:---|:---:|
| [第 1 章：终端、命令和 PATH](01-terminal-and-path.md) | 认识终端与环境变量 | 给电脑一张地址簿 | 8 分钟 |
| [第 2 章：C/C++ 编译环境](02-cpp-toolchain.md) | 配置 C/C++ 编译环境 | 把施工图变成机器 | 12 分钟 |
| [第 3 章：Python 与包管理器](03-python-and-packages.md) | Python 与虚拟环境 | 给项目准备隔离工具箱 | 10 分钟 |
| [第 4 章：包管理器与常用开发工具](04-package-managers.md) | winget、Scoop、Homebrew、APT | 软件商店的命令行收银台 | 10 分钟 |
| [第 5 章：Node.js、npm 与前端工具链](05-node-and-npm.md) | npm、npx、pnpm、Bun | 清单、小票与工具箱 | 10 分钟 |
| [第 6 章：Git 与 Shell](06-git-and-shell.md) | 给项目装上存档和遥控器 | 版本库与命令组合 | 8 分钟 |
| [第 7 章：问题描述与排错实践](07-duck-principle.md) | 用证据描述和缩小问题 | 把报修单写清楚 | 8 分钟 |
| [第 8 章：综合验收与排错](08-environment-check.md) | 完成一次开机自检 | 把工具串成可复现环境 | 12 分钟 |

## 🚀 快速开始

打开 PowerShell、Windows Terminal、Terminal 或你的 Linux shell，先确认自己在哪个目录：

```bash
pwd
```

Windows PowerShell 也可以执行 `Get-Location`。如果你还不知道终端是什么，先进入第 1 章；不要因为看到别人贴出的安装命令就一次安装所有工具。

## 📚 延伸阅读与资源

- [cppreference：C 语言参考](https://en.cppreference.com/c/language) / [C++ 语言参考](https://en.cppreference.com/cpp/language) —— 写代码时查语法、类型、标准版本和未定义行为。
- [Python Packaging User Guide](https://packaging.python.org/en/latest/) —— 学习虚拟环境、pip、`pyproject.toml` 和 Python 包发布的官方实践。
- [Pro Git](https://git-scm.com/book/en/v2) —— 从安装和首次配置开始，逐步理解提交、分支、远程仓库和协作。
- [npm Docs](https://docs.npmjs.com/) —— 查 npm、registry、包脚本和 CLI 命令；配合第 5 章使用。
- [Microsoft Learn：Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/) —— 了解 PowerShell、命令提示符、WSL 和多标签终端。
- [The C Programming Language](https://lilybre.lilystudio.space/book/994) —— 配合 C 编译实践阅读。
- [Automate the Boring Stuff with Python](https://lilybre.lilystudio.space/book/34) —— 用小项目练习 Python 工具链。

资源使用顺序建议是“本教程完成配置 → 用官方文档查命令 → 用教材做一个小项目”。安装器、编译器和包管理器的具体命令可能变化，遇到差异时以官方文档为准。
