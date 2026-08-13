# 第 1 章：读懂错误与 Traceback

遇到错误时，第一反应不应该是复制最后一行去搜索，而是先定位：错误类型、发生位置、调用路径和触发输入。

## 1.1 语法错误和运行时错误

```python
print("hello"  # SyntaxError：括号没有闭合
```

语法错误通常在程序启动前被发现。运行时错误则发生在某条语句真正执行时：

```python
items = [1, 2]
print(items[3])  # IndexError
```

## 1.2 从 Traceback 从下往上读

Python 的 Traceback 通常包含：

1. 调用过哪些文件和函数
2. 最终出错的代码行
3. 异常类型和说明

最底部通常是当前异常，但上面的调用链告诉你它是从哪里被触发的。

## 1.3 不要盲目捕获异常

```python
try:
    amount = float(text)
except ValueError:
    print("金额格式不正确")
```

只捕获你能处理的异常。把所有异常都捕获并忽略，会让真正的 bug 变得不可见。

## 本章练习

故意制造 `NameError`、`TypeError`、`KeyError` 和 `FileNotFoundError`，分别记录：触发代码、异常类型、你会如何修复。
