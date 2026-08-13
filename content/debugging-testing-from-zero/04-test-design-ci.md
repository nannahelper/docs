# 第 4 章：测试边界、替身与持续集成

## 4.1 参数化测试

```python
import pytest


@pytest.mark.parametrize(
    ("records", "expected"),
    [([], 0), ([{"amount": 3}], 3), ([{"amount": 1}, {"amount": 4}], 5)],
)
def test_total(records, expected):
    assert calculate_total(records) == expected
```

同一行为有多组输入时，参数化可以减少重复测试代码。

## 4.2 用替身隔离外部依赖

如果函数会读取网络或文件，测试不应依赖真实网络。把外部依赖作为参数传入，测试时传入一个可控的假对象。

```python
def load_names(reader):
    return [row["name"] for row in reader()]
```

## 4.3 在 CI 中自动运行

```yaml
name: test
on: [push, pull_request]
jobs:
  pytest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pytest
      - run: python -m pytest
```

持续集成的价值不是“让机器替你测试”，而是让每次提交都留下可重复的验证结果。

## 本章练习

为一个读取 JSON 文件的函数设计替身测试；再把测试命令加入 GitHub Actions。
