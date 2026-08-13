# 第 4 章：文件、异常与模块 — 给程序建立档案室

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 120 分钟 |
| 核心概念 | pathlib、JSON、异常、模块、职责 |
| 核心比喻 | 文件是档案，异常是档案室的异常情况报告 |
| 实践任务 | 保存并读取记账记录 |
| 难度等级 | ★★★☆☆ |

程序如果只能在内存里运行，关闭窗口后数据就消失了。本章把记录保存到 JSON 文件，并学习如何面对输入错误。

## 4.1 写入和读取 JSON

```python
import json
from pathlib import Path

path = Path("records.json")
records = [{"title": "午餐", "amount": 25.0}]
path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

loaded = json.loads(path.read_text(encoding="utf-8"))
print(loaded)
```

## 4.2 处理可预期的错误

```python
def read_amount():
    while True:
        try:
            amount = float(input("金额："))
            if amount <= 0:
                raise ValueError("金额必须大于 0")
            return amount
        except ValueError as error:
            print(f"输入无效：{error}，请重新输入。")
```

不要用一个裸 `except:` 把所有错误吞掉。错误信息是调试线索，不是噪声。

## 4.3 用模块组织代码

当一个文件越来越长，可以拆成：

```text
expense_tracker/
├── main.py       # 程序入口
├── storage.py    # 文件读写
└── reports.py    # 统计逻辑
```

模块拆分的判断标准是：一组函数是否围绕同一个职责工作。

## ✅ 验证步骤

运行读写代码后，确认目录中生成 records.json。删除该文件后再次运行，程序应能给出明确提示或创建空记录。

## 📝 本章总结

- 能使用 `pathlib` 读写文件
- 能使用 JSON 保存结构化数据
- 能区分输入错误和程序错误
- 能按职责拆分模块

## ✏️ 课后练习

1. 写两个函数 load_records() 和 save_records()。
2. 文件不存在时返回空列表，JSON 损坏时给出可读的错误提示。

## 🔮 下一章预告

最后一章会把输入、数据结构、持久化和统计组合成完整的命令行记账本。
