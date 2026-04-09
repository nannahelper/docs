# 第五章：安全意识与未来展望

学会调用 API 只是开始。本章将帮你建立正确的安全习惯，避免代价高昂的错误，并为你指引下一步的学习方向。

---

## 1. API Key 安全：重中之重

### ❌ 危险做法：硬编码 Key

新手最常犯的错误就是直接把 API Key 写进代码：

```python
# ⚠️ 绝对不要这样做！
client = OpenAI(
    api_key="sk-abc123def456...",  # 硬编码！一旦上传 GitHub 就泄露了
    base_url="https://api.deepseek.com",
)
```

**后果：** 一旦这段代码被推送到 GitHub（哪怕是私有仓库出现配置错误），你的 Key 就可能被扫描机器人获取，导致账户余额被盗刷。

### ✅ 正确做法：环境变量 + `.env` 文件

**第一步：** 创建 `.env` 文件（在项目根目录）

```bash
# .env
DEEPSEEK_API_KEY=sk-你的真实Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

**第二步：** 将 `.env` 加入 `.gitignore`

```gitignore
# .gitignore
.env
```

**第三步：** 在代码中用 `python-dotenv` 读取

```python
import os
from dotenv import load_dotenv

load_dotenv()  # 从 .env 文件加载环境变量

api_key = os.getenv("DEEPSEEK_API_KEY")
```

!!! success "验证 .env 被 Git 忽略"
    在项目目录运行：
    ```bash
    git status
    ```
    `.env` 文件**不应该**出现在 `Untracked files` 或 `Changes` 列表中。如果出现了，说明 `.gitignore` 配置有问题，**不要提交！**

### 共享代码时用 `.env.example`

当你想把代码分享给他人时，提供一个去掉真实 Key 的模板文件：

```bash
# .env.example（可以提交到 GitHub）
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

其他人拿到代码后，复制 `.env.example` 为 `.env`，填入自己的 Key 即可。

---

## 2. GitHub 泄露风险警示

!!! danger "真实风险"
    GitHub 上有专门的自动化扫描机器人（如 GitGuardian），会在代码被推送后的**几秒钟内**扫描 API Key 格式的字符串。一旦发现，机器人会立即开始尝试用这个 Key 调用 API。

**常被泄露的场景：**

- 直接把 Key 硬编码提交到公开仓库
- 私有仓库不小心设置为公开
- 在 `.ipynb` Notebook 的输出中打印了 Key
- 把 `.env` 文件提交了（没有配置 `.gitignore`）

### 推荐：开启 GitHub Secret Scanning

如果你使用 GitHub，可以在仓库 `Settings → Security → Secret scanning` 中开启密钥扫描，一旦检测到泄露会立即邮件通知你。

### 如果 Key 已经泄露，立即这样做

1. **立即登录 DeepSeek 平台**，前往 API Keys 页面
2. **删除（作废）泄露的 Key**
3. **生成一个新 Key**，更新 `.env` 文件
4. 如果金额被盗刷，联系平台客服说明情况

---

## 3. Token 计费原理与成本监控

### 什么是 Token？

Token 是大模型收费和处理文本的基本单位——比单词更细，比字符稍粗。

粗略估算：
- 🇨🇳 中文：**1 个汉字 ≈ 1.5 个 token**
- 🇺🇸 英文：**1 个单词 ≈ 1 个 token**

模型分别对**输入（Input）**和**输出（Output）**计费：

| 计费项 | 说明 | DeepSeek-Chat 参考价 |
|--------|------|----------------------|
| Input Token | 你发送的 messages 总长度 | 较低 |
| Output Token | 模型返回的内容长度 | 较高 |

### 读取单次调用的 Token 消耗

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}]
)

# 查看本次消耗
usage = response.usage
print(f"输入 Token：{usage.prompt_tokens}")
print(f"输出 Token：{usage.completion_tokens}")
print(f"合计 Token：{usage.total_tokens}")
```

输出示例：
```
输入 Token：8
输出 Token：12
合计 Token：20
```

### 批处理中控制成本

在批处理任务中，设置 `max_tokens` 防止单次请求意外生成超长回复：

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": build_prompt(raw_text)}],
    temperature=0,
    max_tokens=200,  # 提取任务回复很短，200 token 完全够用
)
```

假设 3000 条数据，每条平均消耗 300 token，总计约 90 万 token。在 DeepSeek 的定价下，成本极低（通常几元人民币）。

### 查看账单

登录 [https://platform.deepseek.com](https://platform.deepseek.com) → 左侧 **"账单"** → 可以看到每日消耗的 Token 数量和对应费用。

!!! tip "养成好习惯"
    - 每次批处理前，用 1-2 条数据测试，确认 Prompt 有效后再跑全量
    - 设置 `max_tokens` 上限，防止意外超支
    - 定期检查账单，异常消耗立即排查

---

## 4. 未来展望：Agent 与 RAG

恭喜你完成了全部实战内容！让我们简单展望一下 AI 开发的下一站。

### 🤖 Agent（智能体）

你现在写的代码是这样的：**人类提问 → AI 回答**，一问一答。

Agent 是一种更高级的模式：**给 AI 一个目标，它自己决定怎么完成**。

Agent 可以：
- 自动调用工具（搜索网页、执行代码、读写文件）
- 拆解复杂任务为多个子任务
- 根据执行结果调整下一步行动

例如：你对 Agent 说"帮我找出今天科技新闻中提到次数最多的公司，写一份分析报告存到本地"。Agent 会自动：搜索新闻 → 统计词频 → 生成报告 → 保存文件，全程无需你干预。

常见框架：LangChain、AutoGen、CrewAI。

### 📚 RAG（检索增强生成）

大模型的知识是有截止日期的，它不知道你公司的内部文档、最新新闻，也不了解你私人的笔记。

RAG（Retrieval-Augmented Generation）解决了这个问题：

1. **事先**把你的文档切成小块，存入向量数据库
2. **用户提问时**，先从向量库中检索出最相关的内容
3. 把检索到的内容和用户问题一起发给 LLM
4. LLM 基于**你的文档**来回答

这就是很多公司的"企业知识库问答系统"的底层原理。

常见工具：LlamaIndex、LangChain、Chroma、Weaviate。

---

## 本章小结与结语

✅ 掌握了 `.env` + `.gitignore` 的 API Key 安全模式  
✅ 了解了 GitHub 泄露风险和应对措施  
✅ 能从 `response.usage` 读取 Token 消耗，知道如何控制成本  
✅ 了解了 Agent 和 RAG 的基本概念，知道下一步学什么  

---

### 🎉 恭喜完成全部课程！

你已经从一个只会使用网页版 AI 的用户，成长为能够用代码驱动大模型、自动化处理数据的开发者。

**你现在能做的事情**：
- ✅ 搭建 Python 编程环境，管理依赖
- ✅ 调用任何 OpenAI 兼容的大模型 API
- ✅ 构建有记忆的对话程序
- ✅ 批量清洗非结构化数据导出 Excel
- ✅ 安全管理 API Key，监控成本

**推荐的下一步**：
1. 改造第三章的 Chatbot，加入你自己工作场景的 `system` 提示词
2. 找一个真实的重复性工作，尝试用第四章的批处理框架自动化它
3. 探索 [LangChain 文档](https://python.langchain.com) 了解 Agent 开发

继续学习，继续构建，你会发现 AI 的能力边界比你想象的还要宽广。
