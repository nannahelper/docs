# 第三章：概念升级与 Chatbot 实战

本章我们先厘清"网页 AI"与"代码 AI"的本质区别，然后动手构建一个真正有记忆的终端 Chatbot。

---

## 1. 课程定位：你正在学什么？

完成前两章后，你已经能写几行代码调用大模型了。但也许你会问：**网页版 DeepSeek 用得好好的，为什么还要费力写代码？**

这一章就来回答这个问题。

---

## 2. 网页对话 vs API 调用：本质区别

| 维度 | 🌐 网页对话（Web UI） | 💻 API 调用（Programmatic） |
|------|----------------------|-----------------------------|
| **交互方式** | 手动输入，点对点交互，每次只能问一个问题 | 代码驱动，支持自动化循环处理 |
| **数据处理** | 只能一条一条手动复制粘贴 | 支持批量处理成千上万条数据 |
| **系统集成** | 独立网页，无法嵌入其他系统 | 可嵌入任何 App、网站或本地脚本 |
| **可控性** | 无法固定输出格式 | 可强制指定 JSON 等结构化输出 |
| **自动化** | 需要人工操作 | 可定时执行、批量处理、无人值守 |

!!! example "举个例子"
    你有 3000 条员工绩效文字，需要提取其中的关键词并整理成 Excel。
    
    - **网页版：** 手动复制每条 → 粘贴到网页 → 复制结果 → 粘贴到 Excel → 重复 3000 次，需要几天
    - **API 调用：** 写 50 行 Python 代码 → 运行 → 喝杯茶等待 → Excel 自动生成，30 分钟搞定

---

## 3. 构建终端 Chatbot

现在，让我们把第二章学到的知识组合起来，构建一个真正有**上下文记忆**的对话机器人。

### 核心原理

大模型本身是**无状态的**——每次 API 调用都是独立的，它不会自动"记住"上一次你说了什么。

**实现记忆的方法：** 把每一轮对话都追加到 `messages` 列表中，每次调用时把完整历史一起发送过去。

```
第1轮：messages = [user: "我叫小明"]
第2轮：messages = [user: "我叫小明", assistant: "你好小明", user: "我叫什么"]
第3轮：messages = [user: "我叫小明", assistant: "你好小明", user: "我叫什么", assistant: "你叫小明", user: "..."]
```

每次发送的是**完整的历史记录**，所以 AI 能"记住"上文。

### 完整代码

创建文件 `chatbot.py`：

```python
# chatbot.py —— 带记忆的终端 Chatbot

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)

# 初始化消息历史，system 消息设定 AI 的角色
messages = [
    {
        "role": "system",
        "content": "你是一个友好、耐心的 AI 助手。请用简洁清晰的语言回答问题。"
    }
]

print("=" * 50)
print("🤖 Chatbot 已启动！输入 quit 或 exit 退出。")
print("=" * 50)

while True:
    # 获取用户输入
    user_input = input("\n你：").strip()

    # 退出条件
    if user_input.lower() in ("quit", "exit", "退出", "q"):
        print("\n再见！下次见～ 👋")
        break

    # 跳过空输入
    if not user_input:
        continue

    # 将用户消息追加到历史
    messages.append({"role": "user", "content": user_input})

    try:
        # 发送完整历史，获取回复
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )

        # 提取回复
        assistant_reply = response.choices[0].message.content

        # 将 AI 回复也追加到历史（下次调用时一并发送）
        messages.append({"role": "assistant", "content": assistant_reply})

        print(f"\nAI：{assistant_reply}")

    except Exception as e:
        print(f"\n⚠️  请求失败：{e}")
        # 请求失败时移除刚才添加的 user 消息，避免历史污染
        messages.pop()
```

运行：

```bash
python chatbot.py
```

!!! example "示例对话"
    ```
    你：我今天买了一只猫，它叫饺子
    
    AI：太可爱了！欢迎饺子的到来～请问饺子是什么品种的猫咪？
    
    你：它喜欢什么食物？
    
    AI：猫咪的饮食方面，建议以猫粮为主……（后续根据猫咪相关知识回答）
    
    你：你还记得我的猫叫什么吗？
    
    AI：当然记得，你的猫叫**饺子**！🐱
    ```
    
    AI 能跨轮次记住"饺子"，因为完整的对话历史始终随着每次请求一起发送。

---

## 4. Chatbot vs 网页版的对比小结

|  | 网页版 DeepSeek | 我们构建的 Chatbot |
|--|----------------|--------------------|
| **使用方式** | 打开浏览器，鼠标操作 | 终端运行，命令行交互 |
| **记忆机制** | 自动维护（服务端） | 手动维护 `messages` 列表（完全可控） |
| **可编程性** | ❌ 无法用代码控制 | ✅ 可嵌入任意 Python 逻辑 |
| **批量处理** | ❌ 只能一问一答 | ✅ 可用 `for` 循环批量提问 |
| **历史清空** | 手动新建对话 | 重置 `messages` 列表即可 |

!!! tip "更进一步"
    你完全可以改造这个 Chatbot：
    - 在 `system` 消息里写入你的工作场景，打造专属 AI 助理
    - 加入 `if "总结" in user_input` 触发特殊逻辑
    - 定期把 `messages` 保存到文件，实现跨会话记忆

---

## 5. 运行本文档站点（附加：MkDocs 本地预览）

本教程本身就是用 MkDocs 构建的文档站点，你可以在本地预览：

```bash
# 在项目根目录运行（确保已安装 mkdocs-material）
mkdocs serve
```

然后在浏览器访问 `http://127.0.0.1:8000`，即可看到完整的文档站点。

修改任意 `.md` 文件后，页面会**自动刷新**，非常适合边写边看效果。

如果需要生成静态文件（部署到服务器或 GitHub Pages）：

```bash
mkdocs build
```

生成的文件在 `site/` 目录下。

---

## 本章小结

✅ 理解了网页对话与 API 调用在交互、批处理、集成方面的本质区别  
✅ 掌握了用 `messages` 列表维护上下文记忆的原理  
✅ 构建了一个可以运行的终端 Chatbot  
✅ 了解了如何本地预览 MkDocs 文档站点  

**下一章：** [批量处理工作流 →](04-batch-processing.md) 用 AI 自动清洗数千条非结构化数据！
