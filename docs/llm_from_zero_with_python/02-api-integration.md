# 第二章：API 集成入门——第一次和大模型"握手"

本章我们将完成第一次 API 调用，并深入理解调用背后的每一个细节。

---

## 1. 前置准备

### 安装必要的库

确保你已经在激活的虚拟环境中安装了以下两个库：

```bash
pip install openai python-dotenv
```

- `openai`：DeepSeek 完全兼容 OpenAI 的接口格式，我们可以直接使用这个库
- `python-dotenv`：从 `.env` 文件中加载 API Key 等敏感信息，避免硬编码

!!! info "名词解释：接口格式"
    **接口格式** 是指不同系统之间通信的"语言规范"。例如：

    - OpenAI API 格式规定：用 `messages` 列表来传递聊天内容，用 `model` 字段指定模型
    - DeepSeek 完全遵循这套规范，所以 OpenAI 的库也能直接调用 DeepSeek
    - 就像不同国家都用 USB 接口给手机充电，"接口格式统一"能让工具互通

!!! info "名词解释：硬编码"
    **硬编码** 是指把敏感信息（如密码、API Key）直接写在源代码里。例如：
    ```python
    # ❌ 硬编码（危险！）
    api_key = "sk-xxxxxxxxxxxx"  # Key 暴露在代码文件中
    ```
    这样做的危害：

    - 如果代码上传到 GitHub，你的 Key 就被泄露了
    - 任何人都能用你的 Key 偷跑你的余额
    - 正确做法：用 `.env` 文件或环境变量存储，代码中只引用变量名（如下所示）

### 获取 DeepSeek API Key

1. 打开浏览器，访问 [https://platform.deepseek.com](https://platform.deepseek.com)
2. 注册并登录账号
3. 点击左侧菜单 **"API Keys"**
4. 点击 **"创建 API Key"**，填写名称（如 `my-first-key`）
5. 复制生成的 Key（**注意：Key 只显示一次，请立即保存**）

![DeepSeek API Key 获取](assets/deepseek-api-key.png)

记下两个关键信息：

- **API Key**：类似 `sk-xxxxxxxxxxxxxxxx`
- **Base URL**：`https://api.deepseek.com`

---

## 2. 配置 `.env` 文件

我们用 `.env` 文件存储 API Key，而不是直接写在代码里（安全原因将在第五章详述）。

在项目根目录创建 `.env` 文件：

```
DEEPSEEK_API_KEY=sk-xxxxxxxxx < 你的真实API Key粘贴在这里
DEEPSEEK_BASE_URL=https://api.deepseek.com < API相应的接口链接
```

**同时确认 `.gitignore` 文件包含以下内容**（防止 Key 被上传到 GitHub）：

```gitignore
.env
```
!!! info "名词解释：.gitignore 文件"
    **`.gitignore`** 是 Git 版本控制工具的配置文件，用来指定哪些文件或文件夹应该被 Git **忽略**（不追踪、不上传到仓库）。

    例如：
    ```gitignore
    .env          # 忽略 .env 文件（包含敏s信息）
    __pycache__/  # 忽略 Python 缓存文件夹
    *.pyc         # 忽略所有 .pyc 文件
    venv/         # 忽略虚拟环境文件夹
    ```

    这样做的好处：

    - 防止敏感信息（如 API Key）被误上传到 GitHub
    - 减少仓库体积，避免上传不必要的缓存文件
    - 保持代码仓库的"干净"

    !!! note "进阶内容"
        Git到底是啥？Git 的详细用法将在后续课程中深入讲解。现在你只需记住：**`.env` 一定要加入 `.gitignore`**，这是保护 API Key 的第一道防线。


!!! warning "重要"
    永远不要把包含真实 Key 的 `.env` 文件上传到任何代码仓库！详见[第五章安全实践](05-security.md)。

---

## 3. 你的第一次 API 调用

在项目根目录创建文件 `hello_llm.py`，内容如下：

```python
# hello_llm.py —— 第一次调用大模型

import os
from openai import OpenAI
from dotenv import load_dotenv

# 从 .env 文件加载环境变量
load_dotenv()

# 初始化 Client（相当于"拨号"，建立与服务器的连接）
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),   # API 通行证
    base_url=os.getenv("DEEPSEEK_BASE_URL"),  # 服务器地址
)

try:
    # 发送消息并获取回复
    response = client.chat.completions.create(
        model="deepseek-chat",  # 使用的模型名称
        messages=[
            {"role": "user", "content": "你好！请用一句话介绍你自己。"}
        ],
    )

    # 提取回复文本
    reply = response.choices[0].message.content
    print("AI 回复：", reply)

except Exception as e:
    print(f"调用失败，请检查 .env 文件中的 API Key 是否正确。\n错误信息：{e}")
```

!!! note "说明"
    本文不再介绍 Python 基础语法，假设你已具备基本的 Python 知识。如需补习，请参考 [Python 官方文档](https://docs.python.org/zh-cn/)。


在虚拟环境下运行：

```bash
python hello_llm.py
```

如果看到 AI 的回复，恭喜你——你已经成功和大模型"握手"了！🎉

---

## 4. 角色系统（Roles）详解

`messages` 列表是与大模型交流的核心数据结构。它支持三种角色：

### `system`：给 AI "洗脑"，设定背景

`system` 消息在对话开始前就告诉 AI 它应该是谁、有什么约束。

```python
messages = [
    {
        "role": "system",
        "content": "你是一位专业的 Python 编程导师，专门帮助零基础同学学习编程。"
                   "回答时使用简单易懂的语言，多举生活中的例子。"
    },
    {
        "role": "user",
        "content": "什么是变量？"
    }
]
```

### `user`：用户发送的消息

```python
{"role": "user", "content": "帮我写一首关于春天的诗"}
```

### `assistant`：AI 的历史回复（用于构建多轮对话）

当你想让 AI "记住"之前的对话时，把历史回复也加入 `messages`：

```python
messages = [
    {"role": "user",      "content": "我叫小明"},
    {"role": "assistant", "content": "你好，小明！有什么我可以帮你的吗？"},
    {"role": "user",      "content": "你还记得我叫什么吗？"},
]
```

AI 会基于完整的 `messages` 列表来生成回复，所以它"知道"你叫小明。

!!! example "完整示例：带系统提示的对话"

    ```python
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system",    "content": "你是一位幽默的厨师助手，所有回答都要和烹饪相关。"},
            {"role": "user",      "content": "今天天气真好"},
            {"role": "assistant", "content": "是啊，这种天气最适合出门采购新鲜食材！"},
            {"role": "user",      "content": "那我该做什么菜？"},
        ]
    )
    print(response.choices[0].message.content)
    ```

---

## 5. 解析 API 返回结构

API 返回的是一个对象，而不是直接的字符串。让我们打印完整结构来理解它：

!!! info "什么是"对象"？"
    在编程中，**对象**是一种"夹心"的数据结构，汇总了这个数据类型的所有必要信息。例如 API 的返回值 `response` 就是一个对象，它包含了：

    - `id`：请求的唯一标识
    - `choices`：模型的输出选择
    - `usage`：token 使用统计
    - 等等。

    这样设计的好处是：所有相关信息都"打包"在一起，便于查询和使用。

    如果你想深入理解对象的设计原理，可以在掌握编程基础后学习**"面向对象编程（Object-Oriented Programming, OOP）"**的相关知识。虽然作者也没学会多少，但应该够用了。


```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "1+1等于几？"}]
)

# 打印完整的返回对象
print(response)
```

输出大致如下（已简化）：

```
ChatCompletion(
  id='chatcmpl-xxxx',       # 对话ID
  choices=[
    Choice(
      message=ChatCompletionMessage(
        role='assistant',
        content='1+1等于2。'    # ← 我们想要的文本在这里
      ),
      finish_reason='stop'
    )
  ],
  usage=CompletionUsage(
    prompt_tokens=15,      # 输入消耗的 token 数
    completion_tokens=8,   # 输出消耗的 token 数
    total_tokens=23
  )
)
```

**提取回复文本的标准写法：**

```python
text = response.choices[0].message.content
```

- `choices` 是一个列表（通常只有一个元素，取 `[0]`）
- `.message.content` 是 AI 回复的纯文本字符串

---

## 6. 模型参数详解

API 提供了几个"旋钮"一样的参数，让我们可以精细调控 AI 的输出行为：

### `temperature`（温度）— 控制随机性

```python
# temperature=0：严谨、确定性强，每次回复几乎相同
response_strict = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "写一句话描述太阳"}],
    temperature=0,
)

# temperature=1：创意十足，每次回复都不一样
response_creative = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "写一句话描述太阳"}],
    temperature=1,
)

print("严谨模式：", response_strict.choices[0].message.content)
print("创意模式：", response_creative.choices[0].message.content)
```

| temperature 值 | 适合场景 |
|----------------|----------|
| `0` | 数据提取、代码生成、事实问答 |
| `0.3 ~ 0.7` | 一般对话、摘要、翻译 |
| `0.8 ~ 1.0` | 创意写作、头脑风暴 |


!!! info  "`temperature` 值参考（DeepSeek 官方建议）"

    | 场景 | 推荐温度 |
    |------|---------|
    | 代码生成 / 数学解题 | `0.0` |
    | 数据抽取 / 分析 | `1.0` |
    | 通用对话 | `1.3` |
    | 翻译 | `1.3` |
    | 创意类写作 / 诗歌创作 | `1.5` |

    **默认值：** `temperature=1.0`

### `max_tokens` — 限制回复长度

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "写一篇关于Python的文章"}],
    max_tokens=200,  # 最多输出 200 个 token（约 100-150 个汉字）
)
```

!!! tip "什么是 Token？"
    Token 是模型处理文本的基本单位。粗略估算：**1 个汉字 ≈ 1.5 个 token**，**1 个英文单词 ≈ 1 个 token**。计费也按 token 数量计算。

### `top_p` — 采样范围

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "推荐一个旅游城市"}],
    top_p=0.9,  # 从概率最高的前 90% 词汇中采样
)
```

通常不需要同时调整 `temperature` 和 `top_p`，选其一即可。

---

## 7. 理解底层：用 `requests` 手动发送 POST 请求

`openai` 库只是对 HTTP 请求的封装。让我们看看"底层"长什么样：

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = f"{os.getenv('DEEPSEEK_BASE_URL')}/chat/completions"
headers = {
    "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
    "Content-Type": "application/json",
}
payload = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "你好"}]
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()
print(data["choices"][0]["message"]["content"])
```

这和用 `openai` 库的效果完全一样！

!!! info "架构科普"
    - **C/S 架构（Client/Server）**：我们的 Python 脚本是 **客户端（Client）**，DeepSeek 服务器是 **服务端（Server）**。我们发送 HTTP POST 请求，服务器返回 JSON 响应——这就是"请求-响应"闭环。
    - **B/S 架构（Browser/Server）**：网页版 DeepSeek 是浏览器端，本质上也是向同一个服务器发请求，只是通过浏览器而非 Python 脚本。

---

## 本章小结

✅ 成功配置 `.env` 文件并完成第一次 API 调用  
✅ 理解 `system` / `user` / `assistant` 三种角色的作用  
✅ 能够从 `response.choices[0].message.content` 提取回复文本  
✅ 掌握 `temperature`、`max_tokens`、`top_p` 参数的含义  
✅ 了解 API 调用的底层 HTTP 原理  

**下一章：** [概念与 Chatbot 实战 →](03-concepts.md) 我们将构建一个有记忆的对话机器人！
