# Agent 工具入门

从“聊天”进入“协作”：以 OpenCode Desktop 接入 DeepSeek API Key 为主线，理解 Agent 的模型、工具、权限、上下文和可审计工作流。

## 📖 关于本教程

| 项目 | 内容 |
|:---|:---|
| 适合人群 | 想使用 AI 编程助手，但不清楚 GUI、CLI、API Key 和权限边界的学习者 |
| 预计时长 | 约 4 小时（包含练习） |
| 适用版本 | OpenCode Desktop / CLI 以当前官方文档为准；DeepSeek API 兼容接口 |
| 维护状态 | 维护中 |
| 最后更新 | 2026-08-13 |
| 反馈入口 | [GitHub Issues](https://github.com/nannahelper/docs/issues) |

## 🎯 学习目标

- 能解释 Agent、模型、工具、上下文和权限之间的关系。
- 能在 OpenCode Desktop 中安全配置 DeepSeek API Key 并验证模型调用。
- 能使用 OpenCode CLI 执行受控任务，理解 `/connect`、`/models`、`run` 和 `auth`。
- 能为 Agent 划分只读、编辑、执行和联网权限，并在高风险操作前确认。
- 能比较 OpenCode、Claude Code、GitHub Copilot CLI、Cursor、Cline 等工具的使用边界。

## 📋 前置要求

- 已完成命令行开发环境配置，至少会使用终端和 Git。
- 拥有可用的 DeepSeek API Key，或准备使用其他兼容提供商。
- 理解 API 调用可能产生费用，不把密钥提交到仓库。

## 🗺️ 学习路线

| 章节 | 主题 | 核心比喻 | 预计时长 |
|:---|:---|:---|:---:|
| [第 1 章：Agent 是什么](01-agent-basics.md) | Agent 工作方式 | 有工具权限的协作者 | 25 分钟 |
| [第 2 章：OpenCode Desktop 接入 DeepSeek](02-opencode-desktop-deepseek.md) | GUI、Provider 与 API Key | 给协作者发工作证 | 45 分钟 |
| [第 3 章：OpenCode CLI](03-opencode-cli.md) | CLI、项目上下文与任务 | 用工单交代任务 | 35 分钟 |
| [第 4 章：权限、安全与成本](04-permissions-and-safety.md) | 权限、密钥与费用边界 | 给协作者划安全边界 | 30 分钟 |
| [第 5 章：工具选型与综合任务](05-tool-selection-project.md) | 诊断、验收与回滚 | 选择合适的工作台 | 35 分钟 |
| [第 6 章：小黄鸭原则与第一份 Agent 任务](06-duck-principle-and-first-task.md) | 零基础任务卡与只读实践 | 先向小黄鸭讲清楚 | 35 分钟 |
| [第 7 章：其他 Agent 工具与协作方式](07-other-agent-tools.md) | GUI、CLI、IDE 与任务矩阵 | 不同任务用不同工作台 | 30 分钟 |

## 🚀 快速开始

先准备一个不含敏感信息的测试项目，在 OpenCode Desktop 中打开它。第一次任务只要求读取并解释文件，不允许自动修改、删除或执行未知命令。

## 📚 推荐教材与官方文档

- [OpenCode 官方下载页](https://dev.opencode.ai/download) —— Desktop 与 Terminal 安装入口。
- [OpenCode Providers](https://opencode.ai/docs/providers) —— `/connect`、模型选择和提供商配置。
- [DeepSeek 首次调用 API](https://api-docs.deepseek.com/zh-cn/) —— API Key、兼容接口和模型信息。
