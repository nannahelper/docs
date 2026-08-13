# 第 3 章：列表、字典与数据处理

真实程序经常一次处理很多条数据。列表负责保存有顺序的一组值，字典负责表达“字段名 → 字段值”。

## 3.1 列表

```python
expenses = [12.5, 8, 35.2]
expenses.append(16)

for amount in expenses:
    print(f"支出：{amount:.2f} 元")

print(f"合计：{sum(expenses):.2f} 元")
```

## 3.2 字典

```python
record = {
    "title": "午餐",
    "amount": 25.0,
    "category": "餐饮",
}

print(record["title"])
```

## 3.3 用列表保存多条记录

```python
records = [
    {"title": "午餐", "amount": 25.0, "category": "餐饮"},
    {"title": "地铁", "amount": 3.0, "category": "交通"},
]

food_total = sum(
    item["amount"] for item in records if item["category"] == "餐饮"
)
print(food_total)
```

## 3.4 小练习

给每条记录增加日期字段，编写一个函数，输入分类名称，返回该分类的总金额。

## 本章检查点

- 能新增、读取和遍历列表元素
- 能用字典表达一条结构化记录
- 能使用条件表达式筛选数据
- 能把列表处理逻辑封装为函数
