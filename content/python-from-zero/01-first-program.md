# 第 1 章：从运行代码开始

本章目标：建立工作目录，运行第一个 Python 程序，并理解变量、类型和输入输出。

## 1.1 准备环境

在终端确认 Python 版本：

```bash
python --version
```

如果系统同时安装了多个版本，也可以使用：

```bash
python3 --version
```

创建一个工作目录：

```bash
mkdir python-practice
cd python-practice
```

## 1.2 第一个程序

新建 `hello.py`：

```python
name = input("你的名字是？ ")
print(f"你好，{name}！今天开始学 Python。")
```

运行：

```bash
python hello.py
```

这里发生了三件事：`input()` 读取文本，变量 `name` 保存结果，`print()` 把结果输出。

## 1.3 类型与转换

用户输入默认是字符串。如果要做数学运算，需要主动转换：

```python
age_text = input("你几岁？ ")
age = int(age_text)
print(f"明年你将满 {age + 1} 岁。")
```

常见基础类型：

| 类型 | 示例 | 用途 |
|---|---|---|
| `str` | `"hello"` | 文本 |
| `int` | `42` | 整数 |
| `float` | `3.14` | 小数 |
| `bool` | `True` | 真或假 |

## 1.4 小练习

写一个程序，输入商品价格和数量，输出总价。要求：

- 价格使用 `float`
- 数量使用 `int`
- 总价保留两位小数

```python
price = float(input("单价："))
quantity = int(input("数量："))
total = price * quantity
print(f"总价：{total:.2f} 元")
```

## 本章检查点

- 能在终端运行 `.py` 文件
- 知道输入为什么需要类型转换
- 能用 f-string 组合文本和变量
