# 第 2 章：安装与环境配置

> **工欲善其事，必先利其器** —— 克隆 Dog-Skills 仓库，在 AI 助手中完成技能安装与激活。

---

## 2.1 前置要求

在安装 Dog-Skills 之前，请确保：

| 要求 | 说明 |
|:---|:---|
| **Git** | 用于克隆仓库，版本 2.0+ |
| **AI 编程助手** | 支持 Skills 机制的 IDE（如 Trae IDE） |
| **网络连接** | 能够访问 GitHub |

---

## 2.2 克隆仓库

打开终端（PowerShell / Terminal），执行以下命令：

```bash
# 克隆 Dog-Skills 仓库到本地
git clone https://github.com/ZhouYinLong-lab/Dog-Skills.git

# 进入仓库目录
cd Dog-Skills
```

克隆完成后，你会看到以下目录结构：

```
Dog-Skills/
├── README.md
├── dog-tutor/
│   ├── SKILL.md
│   ├── ATTRIBUTIONS.md
│   ├── references/
│   └── assets/
├── dog-frontier/
│   ├── SKILL.md
│   └── ...
├── find-skills/
│   ├── SKILL.md
│   └── ...
└── skill-creator/
    ├── SKILL.md
    └── ...
```

每个技能目录下的 `SKILL.md` 是技能的核心文件，包含了该技能的完整定义和提示词。

---

## 2.3 在 Trae IDE 中安装技能

Trae IDE 原生支持 Skills 机制。安装步骤如下：

### 步骤 1：找到技能目录

Trae IDE 的技能目录通常在：

- **Windows**：`C:\Users\<你的用户名>\.agents\skills\`
- **macOS / Linux**：`~/.agents/skills/`

### 步骤 2：复制技能文件

将 Dog-Skills 中的技能目录复制到 Trae IDE 的技能目录：

```bash
# Windows PowerShell
# 假设 Dog-Skills 克隆在 D:\Projects\Dog-Skills
Copy-Item -Path "D:\Projects\Dog-Skills\dog-tutor" -Destination "$env:USERPROFILE\.agents\skills\dog-tutor" -Recurse
Copy-Item -Path "D:\Projects\Dog-Skills\dog-frontier" -Destination "$env:USERPROFILE\.agents\skills\dog-frontier" -Recurse
Copy-Item -Path "D:\Projects\Dog-Skills\find-skills" -Destination "$env:USERPROFILE\.agents\skills\find-skills" -Recurse
Copy-Item -Path "D:\Projects\Dog-Skills\skill-creator" -Destination "$env:USERPROFILE\.agents\skills\skill-creator" -Recurse
```

### 步骤 3：验证安装

重启 Trae IDE，在与 AI 对话时输入触发词（如"生成教程"），如果 AI 响应中加载了对应的技能，说明安装成功。

---

## 2.4 在其他 AI 助手中使用

### Cursor

Cursor 使用 Rules 功能来模拟 Skills 机制。你可以将 `SKILL.md` 的内容作为 Rule 添加到 Cursor 中：

1. 打开 Cursor Settings → Rules
2. 新建 Rule，将 `SKILL.md` 的内容粘贴进去
3. 设置 Rule 的描述和触发条件

### 通用方法

即使你的 AI 助手不完全支持 Skills 机制，你也可以：

1. 打开 `SKILL.md` 文件
2. 将其内容作为**系统提示词**或**角色设定**粘贴到对话中
3. 按照技能定义的流程与 AI 交互

---

## 2.5 技能激活方式

Dog-Skills 的技能有两种激活方式：

### 方式一：关键词触发

每个技能都有预定义的触发关键词，当用户输入包含这些关键词时，AI 助手会自动加载对应的技能。

| 技能 | 触发关键词示例 |
|:---|:---|
| **dog-tutor** | "生成教程"、"创建教程"、"编制学习材料"、"写入门指南" |
| **dog-frontier** | "前端设计"、"UI 设计"、"落地页"、"dashboard"、"组件开发" |
| **find-skills** | "找技能"、"发现技能"、"安装技能"、"how do I" |
| **skill-creator** | "创建技能"、"新建技能"、"make a skill" |

### 方式二：手动调用

在 Trae IDE 中，可以通过 `Skill` 工具手动调用指定技能：

```
请使用 dog-tutor 技能帮我生成一个 Python 教程
```

---

## 2.6 验证安装

完成安装后，用以下方式验证各技能是否正常工作：

### 验证 Dog-Tutor

```
请帮我生成一个"Git 基础入门"教程，4 小时，零基础
```

AI 应该按照 Dog-Tutor 的 6 阶段流程开始工作。

### 验证 Dog-Frontier

```
请帮我设计一个博客网站的落地页
```

AI 应该按照 Dog-Frontier 的设计流程开始工作。

### 验证 Find-Skills

```
我想找一个能帮我处理 PDF 的技能
```

AI 应该启动 Find-Skills 技能进行搜索。

---

## 2.7 常见问题

### Q：技能没有自动加载？

确保：
1. 技能文件已正确复制到技能目录
2. 已重启 AI 助手
3. 输入包含了正确的触发关键词

### Q：技能目录不存在？

手动创建技能目录即可：
```bash
mkdir -p ~/.agents/skills
```

### Q：如何更新技能？

重新拉取 Dog-Skills 仓库并覆盖技能目录：
```bash
cd Dog-Skills
git pull
# 然后重新复制技能文件
```

---

## 2.8 本章小结

- 克隆 Dog-Skills 仓库获取技能文件
- 将技能目录复制到 AI 助手的技能目录中
- 通过关键词触发或手动调用激活技能
- 验证各技能是否正常工作

---

## 实践任务

1. 克隆 Dog-Skills 仓库到本地
2. 将至少两个技能安装到你的 AI 助手中
3. 用触发词验证技能是否正常加载

---