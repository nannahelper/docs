# 第 2 章：断点、日志与最小复现

## 2.1 先让问题稳定重现

一个好 bug 报告应该能回答：

- 输入是什么
- 执行了哪条命令
- 实际结果是什么
- 期待结果是什么
- 是否每次都发生

如果问题无法稳定重现，先记录环境、版本和随机输入。

## 2.2 使用断点

```python
def calculate_total(records):
    total = 0
    breakpoint()
    for record in records:
        total += record["amount"]
    return total
```

运行到 `breakpoint()` 时，可以检查变量：

```text
p records
p total
n
c
```

## 2.3 用日志记录事实

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logging.info("开始加载 %d 条记录", len(records))
```

日志应记录状态变化、关键输入和错误上下文，不要打印密码、Token 或个人敏感数据。

## 本章练习

给记账本增加三个日志点：加载文件、保存文件、计算总额。让日志能帮助你判断程序卡在哪一步。
