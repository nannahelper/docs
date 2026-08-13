# 第四章：批量处理工作流——让 AI 替你处理千条数据

本章是本教程最具实战价值的一章。我们将用不到 100 行代码，自动清洗数千条杂乱的非结构化文本，并输出整洁的 Excel 文件。

---

## 1. 场景：非结构化数据的噩梦

假设你是一所大学的教务老师，手里有一份教材数据表，里面有 3000 条数据，格式混乱得像这样：

```
《高等数学（上册）》,同济大学数学系编,高等教育出版社,2021年第7版
线性代数 / 李尚志 著 — 北京 : 高等教育出版社, 2014.8
Python编程:从入门到实践[美]埃里克·马瑟斯(EricMatthes)著;袁国忠译2023年第3版人民邮电出版社
概率论与数理统计·浙大版·第四版·盛骤等编·高教社·2019
...
```

你需要把它整理成标准格式：

| 书名 | 作者 | 出版社 | 年份 |
|------|------|--------|------|
| 高等数学（上册） | 同济大学数学系 | 高等教育出版社 | 2021 |
| 线性代数 | 李尚志 | 高等教育出版社 | 2014 |
| Python编程：从入门到实践 | 埃里克·马瑟斯 | 人民邮电出版社 | 2023 |

**手动处理？** 3000 条 × 每条 5 分钟 = 250 小时，几乎不可能。  
**用 AI + Python？** 30 分钟写代码，再等待 30 分钟运行，全部搞定。

这就是 LLM 对非结构化数据的"降维打击" 🚀

---

## 2. Prompt 设计：让 AI 提取结构化字段

首先，我们需要设计一个好的 Prompt，让 AI 明确知道我们要什么。

### 关键原则

1. **明确指定输出格式**（JSON）
2. **列出所有字段名**
3. **说明找不到时的默认值**
4. **要求严格按格式输出，不加额外解释**

### Prompt 模板

```python
def build_prompt(raw_text: str) -> str:
    return f"""请从以下文本中提取教材信息，严格以JSON格式输出，不要添加任何多余说明。

输入文本：
{raw_text}

要求提取以下字段（找不到则填 null）：
- book_name: 书名（去除书名号《》）
- author: 作者姓名（多位作者用顿号分隔）
- publisher: 出版社名称
- year: 出版年份（4位数字，仅数字）

输出示例：
{{"book_name": "高等数学（上册）", "author": "同济大学数学系", "publisher": "高等教育出版社", "year": "2021"}}

只输出JSON，不要输出其他内容："""
```

测试一下这个 Prompt：

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)

raw = "《高等数学（上册）》,同济大学数学系编,高等教育出版社,2021年第7版"

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": build_prompt(raw)}],
    temperature=0,  # 数据提取任务用 temperature=0，结果最稳定
)
print(response.choices[0].message.content)
```

输出：
```json
{"book_name": "高等数学（上册）", "author": "同济大学数学系", "publisher": "高等教育出版社", "year": "2021"}
```

---

## 3. 强制 JSON 输出的两种方法

### 方法一：Prompt 指令法（推荐，兼容性最好）

在 Prompt 末尾明确要求：`只输出JSON，不要输出其他内容`。这是最通用的方式，适用于所有支持 OpenAI 格式的 API。

### 方法二：`response_format` 参数法

部分模型支持通过参数强制 JSON 输出：

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": build_prompt(raw)}],
    temperature=0,
    response_format={"type": "json_object"},  # 强制 JSON 模式
)
```

!!! warning "注意"
    使用 `response_format={"type": "json_object"}` 时，Prompt 中也必须提到"JSON"，否则部分模型会报错。

### 解析 JSON 回复

无论用哪种方法，都用 `json.loads()` 把字符串转为 Python 字典：

```python
import json

raw_reply = response.choices[0].message.content
try:
    data = json.loads(raw_reply)
    print(data["book_name"])  # → 高等数学（上册）
except json.JSONDecodeError as e:
    print(f"JSON 解析失败，原始回复：{raw_reply}")
```

---

## 4. 批处理主循环

现在把所有部分组合起来，构建完整的批处理脚本。

### 准备输入文件

创建 `data/raw_books.txt`，每行一条原始数据：

```
《高等数学（上册）》,同济大学数学系编,高等教育出版社,2021年第7版
线性代数 / 李尚志 著 — 北京 : 高等教育出版社, 2014.8
Python编程:从入门到实践[美]埃里克·马瑟斯著;袁国忠译2023年第3版人民邮电出版社
概率论与数理统计·浙大版·第四版·盛骤等编·高教社·2019
```

### 完整批处理脚本

创建 `batch_process.py`：

```python
# batch_process.py —— 批量清洗非结构化教材数据

import os
import json
import time
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)


def build_prompt(raw_text: str) -> str:
    """构建用于信息提取的 Prompt"""
    return f"""请从以下文本中提取教材信息，严格以JSON格式输出，不要添加任何多余说明。

输入文本：
{raw_text}

要求提取以下字段（找不到则填 null）：
- book_name: 书名（去除书名号《》）
- author: 作者姓名（多位作者用顿号分隔）
- publisher: 出版社名称
- year: 出版年份（4位数字，仅数字）

只输出JSON，不要输出其他内容："""


def extract_book_info(raw_text: str) -> dict | None:
    """调用 API 提取单条教材信息，失败返回 None"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": build_prompt(raw_text)}],
            temperature=0,
            max_tokens=200,  # 提取任务回复很短，限制 token 防止超支
        )
        raw_reply = response.choices[0].message.content.strip()
        return json.loads(raw_reply)

    except json.JSONDecodeError:
        # 模型没有严格输出 JSON，记录并跳过
        print(f"  ⚠️  JSON 解析失败，原始回复：{raw_reply[:80]}...")
        return None
    except Exception as e:
        # 网络超时、API 错误等
        print(f"  ❌ API 调用失败：{e}")
        return None


def main():
    input_file = "data/raw_books.txt"
    output_file = "data/cleaned_books.xlsx"

    # 读取所有原始数据
    with open(input_file, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    total = len(lines)
    print(f"📚 共 {total} 条数据，开始处理...\n")

    results = []
    failed_lines = []

    for i, raw_text in enumerate(lines, start=1):
        print(f"[{i}/{total}] 处理中：{raw_text[:40]}...")

        result = extract_book_info(raw_text)

        if result:
            result["raw_text"] = raw_text  # 保留原始文本，方便核查
            results.append(result)
            print(f"  ✅ 提取成功：{result.get('book_name')}")
        else:
            failed_lines.append({"line_no": i, "raw_text": raw_text})
            print(f"  ❌ 提取失败，已记录，跳过")

        # 礼貌间隔，避免请求过于频繁
        time.sleep(0.3)

    # 导出成功结果到 Excel
    if results:
        df = pd.DataFrame(results, columns=["book_name", "author", "publisher", "year", "raw_text"])
        df.to_excel(output_file, index=False, engine="openpyxl")
        print(f"\n✅ 已导出 {len(results)} 条数据到 {output_file}")

    # 导出失败记录（方便人工复查）
    if failed_lines:
        fail_df = pd.DataFrame(failed_lines)
        fail_df.to_excel("data/failed_lines.xlsx", index=False, engine="openpyxl")
        print(f"⚠️  {len(failed_lines)} 条失败，已记录到 data/failed_lines.xlsx")

    print(f"\n🎉 处理完成：{len(results)}/{total} 条成功")


if __name__ == "__main__":
    main()
```

运行：

```bash
# 先创建 data 目录
mkdir data

# 运行批处理
python batch_process.py
```

---

## 5. 异常处理详解

批处理中可能遇到的问题和对应的处理策略：

| 异常类型 | 原因 | 处理方式 |
|----------|------|----------|
| `json.JSONDecodeError` | 模型没有严格输出 JSON | 记录原始回复，跳过该条 |
| `openai.APIConnectionError` | 网络断开或超时 | 记录行号，跳过继续 |
| `openai.RateLimitError` | 请求太频繁（限速） | 加长 `time.sleep()` 间隔 |
| `openai.AuthenticationError` | API Key 无效 | 立即终止，提示检查 `.env` |

---

## 6. pandas 导出 Excel

`pandas` 是 Python 数据处理最常用的库：

```python
import pandas as pd

# 从字典列表创建 DataFrame（类似 Excel 中的一张表）
data = [
    {"book_name": "高等数学", "author": "同济大学", "publisher": "高教社", "year": "2021"},
    {"book_name": "线性代数", "author": "李尚志",   "publisher": "高教社", "year": "2014"},
]
df = pd.DataFrame(data)

# 导出为 Excel（需要 openpyxl）
df.to_excel("output.xlsx", index=False, engine="openpyxl")
print("导出完成！")
```

!!! warning "依赖提示"
    `df.to_excel()` 需要 `openpyxl` 库。如果报错 `ModuleNotFoundError: No module named 'openpyxl'`，运行：
    ```bash
    pip install openpyxl
    ```

---

## 本章小结

✅ 理解了 LLM 对非结构化数据的"降维打击"价值  
✅ 掌握了通过 Prompt 设计强制 AI 输出 JSON  
✅ 构建了完整的批处理循环（读取→调用→解析→积累→导出）  
✅ 添加了健壮的异常处理，确保单条失败不影响整体流程  
✅ 用 pandas 将结果导出为 Excel  

**下一章：** [安全与展望 →](05-security.md) 如何保护你的 API Key，以及 AI 开发的下一站。
