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
| [第 6 章：任务描述与第一份 Agent 任务](06-duck-principle-and-first-task.md) | 零基础任务卡与只读实践 | 先把任务交代清楚 | 35 分钟 |
| [第 7 章：其他 Agent 工具与协作方式](07-other-agent-tools.md) | GUI、CLI、IDE 与任务矩阵 | 不同任务用不同工作台 | 30 分钟 |

## 🔭 追更：2026-08-13，DeepSeek Harness 进入公开开发者预览

本教程更新当天，DeepSeek 官方公开了 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)，命令行名称为 `dsh`。官方仓库当前将它标为 **Developer Preview**，也就是面向开发者的预览阶段；这和“稳定版”不同，官方明确提示可能出现不兼容变更。因此，本节记录的是截至 **2026-08-13** 能从官方仓库核实到的状态，不把社区预告或传言写成正式发布日期。

### 它是什么

DeepSeek Harness 是 DeepSeek AI 开发的开源 Agent Harness。官方介绍的核心架构是“everything is a plugin”：模型、工具、技能、会话、沙箱、文件系统、循环、编排和 UI 都可以作为插件组合。对学习者而言，可以先把它理解为“负责把模型、工具和执行流程组织起来的工作台”，而不仅是一种模型调用接口。

### 目前能确认的运行方式

官方 README 给出了基于 npm 的 Web UI 启动方式：

```bash
npx @deepseek-ai/dsh web
```

默认情况下，Web UI 在本机 `http://127.0.0.1:3080` 提供服务。也可以从源码运行：

```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

这些命令来自官方仓库；预览版可能变化，执行前应先查看仓库 README 和安全说明。不要在生产目录第一次运行，也不要把 DeepSeek API Key 写进命令、源码或提交记录。

### 和 OpenCode 的关系

OpenCode 是本课程的主线练习工具，DeepSeek Harness 是新增的官方工作台。二者都属于 Agent 工具层，但不能据此断言它们功能、稳定性或性能谁更强。合理的学习顺序是：先用 OpenCode 完成只读任务、权限控制和人工验收，再在隔离项目中试用 Harness，记录版本、模型、工具权限和实际结果。

| 对比项 | OpenCode | DeepSeek Harness 公开预览 |
|:---|:---|:---|
| 本教程定位 | 主线练习工具 | 追更观察对象 |
| 官方状态 | 以官方文档当前说明为准 | Developer Preview |
| 入口 | Desktop / CLI | npm Web UI 或源码运行 |
| 学习重点 | Provider、CLI、权限、验收 | 插件化架构、工作台与扩展边界 |
| 使用建议 | 先完成课程主线 | 在隔离项目中试用并记录变化 |

### 追更记录规则

后续更新本节时，只记录可核验事实：发布日期、官方仓库或文档链接、版本号、安装命令和已验证行为。社区帖子可以帮助发现线索，但如果没有官方来源或可复现实验，就标为“待核实”，不写成结论。

!!! warning "预览版安全提醒"
    Agent Harness 可能读取文件、执行命令、连接网络或调用 API。首次运行只使用无敏感信息的测试项目，保留 Git 状态，采用最小权限，并在每次执行后检查改动和费用。

## 🚀 快速开始

先准备一个不含敏感信息的测试项目，在 OpenCode Desktop 中打开它。第一次任务只要求读取并解释文件，不允许自动修改、删除或执行未知命令。

## 📚 推荐教材与官方文档

- [OpenCode 官方下载页](https://dev.opencode.ai/download) —— Desktop 与 Terminal 安装入口。
- [OpenCode Providers](https://opencode.ai/docs/providers) —— `/connect`、模型选择和提供商配置。
- [DeepSeek 首次调用 API](https://api-docs.deepseek.com/zh-cn/) —— API Key、兼容接口和模型信息。
- [DeepSeek Harness 官方仓库](https://github.com/deepseek-ai/deepseek-harness) —— 公开开发者预览、npm 启动方式与架构说明。
