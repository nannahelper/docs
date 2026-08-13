# 命令行开发环境配置

以 C/C++ 为主线，从一台刚装好的电脑开始，建立可以编译、运行、安装依赖和管理项目的开发环境。

## 📖 关于本教程

| 项目 | 内容 |
|:---|:---|
| 适合人群 | 不确定开发工具如何安装和验证的初学者 |
| 预计时长 | 8–10 小时（包含练习） |
| 适用版本 | Windows 11、macOS 14+、Ubuntu 22.04+；命令随版本变化 |
| 维护状态 | 维护中 |
| 最后更新 | 2026-08-13 |
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

## 🗺️ 学习路线

| 章节 | 主题 | 核心比喻 | 预计时长 |
|:---|:---|:---|:---:|
| [第 1 章：终端、命令和 PATH](01-terminal-and-path.md) | 认识终端与环境变量 | 给电脑一张地址簿 | 60 分钟 |
| [第 2 章：C/C++ 编译环境](02-cpp-toolchain.md) | 配置 C/C++ 编译环境 | 把施工图变成机器 | 90 分钟 |
| [第 3 章：Python 与包管理器](03-python-and-packages.md) | Python 与虚拟环境 | 给项目准备隔离工具箱 | 90 分钟 |
| [第 4 章：包管理器与常用开发工具](04-package-managers.md) | winget、Scoop、Homebrew、APT | 软件商店的命令行收银台 | 75 分钟 |
| [第 5 章：Node.js、npm 与前端工具链](05-node-and-npm.md) | npm、npx、pnpm、Bun | 清单、小票与工具箱 | 75 分钟 |
| [第 6 章：Git 与 Shell](04-git-and-shell.md) | 给项目装上存档和遥控器 | 版本库与命令组合 | 75 分钟 |
| [第 7 章：小黄鸭原则与排错](06-duck-principle.md) | 用证据描述和缩小问题 | 给不会回答的小黄鸭讲清楚 | 60 分钟 |
| [第 8 章：综合验收与排错](05-environment-check.md) | 完成一次开机自检 | 把工具串成可复现环境 | 120 分钟 |

## 🚀 快速开始

打开 PowerShell、Windows Terminal、Terminal 或你的 Linux shell，先执行：

```bash
git --version
python --version
```

如果某条命令不存在，不要直接复制一堆安装命令；先进入第 1 章确认系统、架构和 PATH。

## 📚 推荐教材

- [The C Programming Language](https://lilybre.lilystudio.space/book/994) —— 配合 C 编译实践。
- [Automate the Boring Stuff with Python](https://lilybre.lilystudio.space/book/34) —— 练习 Python 工具链。
