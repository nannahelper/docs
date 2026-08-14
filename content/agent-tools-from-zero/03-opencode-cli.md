# 第 3 章：OpenCode CLI — 用工单交代任务

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 35 分钟 |
| 核心概念 | CLI、TUI、run、auth、models、项目上下文 |
| 核心比喻 | CLI 像把任务写成可以重复执行的工单 |
| 实践任务 | 用 CLI 完成只读分析和受控修改 |
| 难度等级 | ★★☆☆☆ |

## CLI 的优势是过程更容易留下痕迹

图形界面适合观察状态和管理会话，命令行适合把同一套任务交给不同电脑、远程主机或脚本。CLI 不会因为“看起来像按钮”而自动替你理解风险；当前目录、认证方式和命令参数都需要你自己确认。因此，使用 CLI 的第一步永远是知道自己在哪个目录、将允许它做什么。

本章先做只读任务，再把任务写成可以复制的工单。可重复不等于无脑自动化：每次运行前仍然要检查目标目录和输入内容，每次运行后仍然要查看输出、Git diff 和费用记录。

## 3.1 安装和验证 CLI

OpenCode 官方提供安装脚本、npm、Bun、Homebrew 等方式。Windows 用户也可以使用官方 Desktop，或按官方文档选择兼容的 CLI 安装方式：

```bash
npm install -g opencode-ai
opencode --version
```

安装方式会随版本变化，优先查看[官方 CLI 文档](https://dev.opencode.ai/docs/cli/)。

## 3.2 连接 Provider 和查看模型

```bash
opencode auth login
opencode auth list
opencode models --refresh
```

在交互界面中也可以使用：

```text
/connect
/models
```

## 3.3 执行只读任务

```bash
opencode run "只读取 README.md，概括项目用途；不要修改文件、安装依赖或执行 Git 操作"
```

进入项目目录再执行命令，Agent 才会获得正确的上下文：

```bash
cd path/to/project
opencode
```

## 3.4 让任务可重复

把任务写成清晰的输入、范围和验收标准：

```text
目标：找出测试失败的原因
允许：读取源码和测试，运行单个测试命令
禁止：修改文件，删除数据，安装依赖，提交或推送
输出：根因、证据、最小修复建议
```

## ✅ 验证步骤

执行一次 `opencode run` 只读任务，确认输出包含项目证据；运行 `git diff --exit-code` 确认没有修改。再用交互模式执行 `/models`，确认能看到当前可用模型。

## 📝 本章总结

- CLI 适合脚本化、重复任务和远程终端。
- `auth` 管凭据，`models` 管模型，`run` 适合非交互任务。
- 明确禁止项能降低 Agent 越权操作风险。

## ✏️ 课后练习

1. 把一次只读代码审查写成可重复的 CLI 提示词。
2. 让 Agent 只运行一个指定测试，并要求输出命令和结果。

## 🔮 下一章预告

下一章会讨论权限、密钥、成本和停止边界。
