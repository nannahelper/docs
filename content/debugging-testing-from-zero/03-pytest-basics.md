# 第 3 章：用 pytest 写第一组测试

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

## 本章练习

为记账本的分类统计函数补充三个测试，并运行 pytest 确认全部通过。
