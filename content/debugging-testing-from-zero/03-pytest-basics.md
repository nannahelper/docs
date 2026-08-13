# 第 3 章：用 pytest 写第一组测试

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 90 分钟 |
| 核心概念 | 断言、测试函数、边界条件、测试命名 |
| 核心比喻 | 测试像给每个行为设置可重复的验收卡 |
| 实践任务 | 为记账函数补充正常和边界测试 |
| 难度等级 | ★★☆☆☆ |

测试的最小单位是：准备输入，执行行为，验证结果。

## 3.1 第一个测试

生产代码：

```python
def calculate_total(records):
    return sum(record["amount"] for record in records)
```

测试代码 `test_expenses.py`：

```python
from expenses import calculate_total


def test_calculate_total():
    records = [{"amount": 10}, {"amount": 2.5}]
    assert calculate_total(records) == 12.5
```

运行：

```bash
python -m pytest
```

## 3.2 测试空输入和边界

```python
def test_empty_records_total_is_zero():
    assert calculate_total([]) == 0
```

边界条件比“正常输入”更容易暴露实现假设。至少测试空列表、单条记录、负数和错误类型。

## 3.3 测试名称要说明行为

`test_empty_records_total_is_zero` 比 `test_1` 更有信息量。失败时，测试名称本身就是第一条线索。

## ✏️ 课后练习

为记账本的分类统计函数补充三个测试，并运行 pytest 确认全部通过。

## ✅ 验证步骤

执行 `python -m pytest`，确认所有测试通过；故意把一个期望值改错，观察失败信息是否能指出测试行为和实际结果。

## 📝 本章总结

- 测试通常包含准备、执行和验证三个阶段。
- 边界条件比单一正常输入更容易暴露假设。
- 测试名称应该描述行为，而不是编号。

## 🔮 下一章预告

下一章会学习参数化、替身和持续集成，把验证扩展到更多环境。
