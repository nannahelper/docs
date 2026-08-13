# 第 4 章：测试边界、替身与持续集成

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 100 分钟 |
| 核心概念 | 参数化、替身、外部依赖、CI |
| 核心比喻 | CI 像每次提交后自动执行的验收流水线 |
| 实践任务 | 把测试接入 GitHub Actions |
| 难度等级 | ★★★☆☆ |

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

## ✏️ 课后练习

为一个读取 JSON 文件的函数设计替身测试；再把测试命令加入 GitHub Actions。

## ✅ 验证步骤

本地运行参数化测试和替身测试，再创建一次提交，确认 GitHub Actions 能自动执行相同的测试命令。

## 📝 本章总结

- 参数化测试适合验证同一行为的多组输入。
- 替身让测试不依赖真实网络和文件系统。
- CI 把本地验证变成团队共享的反馈。

## 🔮 下一章预告

最后一章会给记账本建立一套完整的质量验收清单。
