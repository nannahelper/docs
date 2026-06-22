# 第 2 章：技能的获取与管理

> **工欲善其事，必先利其器** —— 掌握在不同 AI 助手中获取、安装和管理技能的方法。

---

## 2.1 前置要求

在开始使用技能之前，请确认：

| 要求 | 说明 |
|:---|:---|
| **AI 编程助手** | Claude Code、Cursor、Trae IDE 等支持技能的 IDE |
| **Git**（可选） | 用于从 GitHub 获取技能，版本 2.0+ |
| **网络连接** | 能够访问技能源（npm、GitHub 等） |

---

## 2.2 技能的获取渠道

技能可以从多种渠道获取：

### 社区技能市场

许多 AI 助手平台拥有自己的技能市场或注册中心：

- **Claude Code**：通过 `npx skills` 命令搜索和安装，或访问 [skills.sh](https://skills.sh) 浏览排行榜
- **Trae IDE**：社区通过 GitHub 仓库分享技能包
- **Cursor**：社区通过 Rules 模板分享

### GitHub 仓库

大量开源技能托管在 GitHub 上。直接搜索 `skills` 或 `claude-skills` 等关键词即可找到：

```bash
# 示例：搜索技能仓库
# 在 GitHub 搜索框中输入：
#   skills topic:claude-code
#   skills topic:cursor
```

### 自行创建

当现有技能无法满足需求时，你可以自行创建。详见[第 4 章：创作自定义技能](04-create-skills.md)。

---

## 2.3 在 Claude Code 中安装技能

Claude Code 提供了最便捷的技能安装体验。

### 方式一：通过 npx skills 安装

```bash
# 搜索技能
npx skills search <关键词>

# 安装技能
npx skills install <技能名>
```

安装后的技能存放在 `.claude/skills/` 目录下，Claude Code 会自动识别。

### 方式二：手动复制

从 GitHub 克隆或下载技能文件后，放入技能目录：

```bash
# 克隆技能仓库
git clone https://github.com/<作者>/<技能仓库>.git

# 将技能目录复制到 Claude Code 技能路径
cp -r <技能仓库> ~/.claude/skills/<技能名>
```

### 方式三：通过 /skill-creator 引导安装

在 Claude Code 对话中，某些技能可以引导你完成安装流程。

---

## 2.4 在 Trae IDE 中安装技能

Trae IDE 原生支持 Skills 机制：

### 步骤 1：找到技能目录

Trae IDE 的技能目录通常在：

- **Windows**：`C:\Users\<用户名>\.agents\skills\`
- **macOS / Linux**：`~/.agents/skills/`

### 步骤 2：复制技能文件

将从 GitHub 或其他渠道获取的技能目录复制到该路径：

```bash
# Windows PowerShell
Copy-Item -Path "D:\Projects\<技能目录>" -Destination "$env:USERPROFILE\.agents\skills\<技能名>" -Recurse

# macOS / Linux
cp -r ~/Downloads/<技能目录> ~/.agents/skills/<技能名>
```

### 步骤 3：重启验证

重启 Trae IDE，输入技能的触发关键词，如果加载成功说明安装完成。

---

## 2.5 在 Cursor 中使用技能

Cursor 通过 **Rules** 功能模拟技能机制：

1. 打开 **Cursor Settings → Rules**
2. 点击 **Add new rule**
3. 将技能的核心提示词内容粘贴进去
4. 设置触发条件（如文件类型匹配、目录匹配等）
5. 保存规则

你也可以将技能内容作为**项目级的 `.cursorrules`** 文件使用，这样整个团队的 AI 助手都会遵循相同的技能规范。

---

## 2.6 技能的激活方式

### 方式一：关键词自动触发

每种技能都定义了触发关键词，当你的输入匹配到这些关键词时，AI 助手会自动加载对应技能。

例如：
- 输入"生成教程" → 自动加载教程生成类技能
- 输入"审查代码" → 自动加载代码审查类技能

### 方式二：手动调用

在 Claude Code 中，通过 `/skill-name` 的方式手动调用指定技能；在 Trae IDE 中，可以通过 `Skill` 工具手动调用。

```
请使用 pdf 技能帮我提取这份文档的文字内容
```

---

## 2.7 技能目录结构

一个标准的技能通常包含以下文件：

```
my-skill/
├── SKILL.md           # 技能核心定义（必需）
│                       #   - 元数据（名称、描述、触发词）
│                       #   - 系统提示词（领域知识、工作流程）
│                       #   - 输出规范（格式要求、质量标准）
├── references/        # 参考资料（可选）
│   ├── workflow.md    #   详细工作流程
│   └── examples.md    #   示例输出
├── assets/            # 辅助资源（可选）
│   └── templates/     #   模板文件
└── ATTRIBUTIONS.md    # 归属声明（可选）
```

`SKILL.md` 是技能的心脏——它包含了该技能的完整定义和核心提示词。

---

## 2.8 技能管理

### 查看已安装技能

- **Claude Code**：`npx skills list` 或查看 `.claude/skills/` 目录
- **Trae IDE**：查看 `~/.agents/skills/` 目录
- **Cursor**：Settings → Rules 中查看

### 更新技能

从原始渠道重新获取最新版本并覆盖：

```bash
# GitHub 方式
cd <技能仓库目录>
git pull

# 然后重新复制到技能目录
```

### 移除技能

直接删除对应的技能目录即可：

```bash
# Claude Code
rm -rf ~/.claude/skills/<技能名>

# Trae IDE
rm -rf ~/.agents/skills/<技能名>
```

---

## 2.9 常见问题

### Q：安装后技能没有生效？

确保：
1. 技能文件已放入正确的目录
2. 已重启 AI 助手（部分平台需要）
3. 输入包含了正确的触发关键词

### Q：技能目录不存在怎么办？

手动创建即可：
```bash
# Claude Code
mkdir -p ~/.claude/skills

# Trae IDE
mkdir -p ~/.agents/skills
```

### Q：多个技能触发词冲突怎么办？

检查各技能的触发词定义，手动调整触发词或指定使用哪个技能。

---

## 2.10 本章小结

- 技能可以从社区市场、GitHub 仓库获取，也可以自行创建
- Claude Code 通过 `npx skills` 提供便捷的安装体验
- Trae IDE 和 Cursor 各有一套技能配置方式
- 技能的激活支持关键词触发和手动调用两种方式
- 每个技能的核心是 `SKILL.md` 文件

---

## 实践任务

1. 在你的 AI 助手中安装至少一个技能
2. 查看该技能的 `SKILL.md` 文件，了解其结构
3. 用触发词验证技能是否正常工作

---
