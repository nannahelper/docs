# 第 2 章：条件、循环与函数

程序的核心不是语法，而是把“遇到什么情况做什么事”写清楚。

## 2.1 条件判断

```python
score = 86

if score >= 90:
    level = "优秀"
elif score >= 60:
    level = "合格"
else:
    level = "需要继续练习"

print(level)
```

注意：Python 用缩进表示代码块。建议统一使用 4 个空格。

## 2.2 循环处理重复任务

```python
total = 0
for number in range(1, 6):
    total += number

print(total)  # 15
```

`range(1, 6)` 产生 1 到 5，不包含 6。

## 2.3 把重复逻辑封装成函数

```python
def calculate_total(price, quantity):
    """返回商品总价。"""
    if price < 0 or quantity < 0:
        raise ValueError("价格和数量不能为负数")
    return price * quantity


print(calculate_total(12.5, 3))
```

好的函数通常只负责一件事，并通过参数接收输入、通过 `return` 返回结果。

## 2.4 小练习：猜数字

使用 `random.randint(1, 100)` 生成答案，让用户最多猜 6 次，并提示“太大”或“太小”。

## 本章检查点

- 能写出 `if / elif / else`
- 能用 `for` 遍历一个范围
- 能把一段逻辑封装成函数
- 知道什么时候应该主动抛出异常
