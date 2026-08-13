# 调试与测试指南

调试是在问“程序为什么这样运行”，测试是在问“程序在这些条件下是否符合预期”。本课程以 Python 记账本为案例，把发现问题、复现问题和防止回归串成一条可重复的质量工作流。

| 项目 | 内容 |
|---|---|
| 适合人群 | 已经能写简单程序，想减少“改了这里又坏了那里”的学习者 |
| 预计时长 | 6–8 小时（包含练习） |
| 适用版本 | Python 3.11+、pytest 8+、GitHub Actions |
| 维护状态 | 维护中 |
| 最后更新 | 2026-08-13 |
| 反馈入口 | [GitHub Issues](https://github.com/nannahelper/docs/issues) |

## 🎯 学习目标

- 能从错误类型、位置和调用路径定位问题。
- 能使用断点、日志和最小复现缩小排查范围。
- 能用 pytest 编写正常、边界和替身测试。
- 能把测试接入 GitHub Actions，形成持续验证。

## 📋 前置要求

- 能读懂简单的 Python 函数和异常信息。
- 已安装 Python 3.11+。
- 建议先完成 Python 新手指南。

## 📚 推荐教材

- [Architecture Patterns with Python](https://lilybre.lilystudio.space/book/25) —— 将测试驱动开发放进真实架构中
- [The Mythical Man-Month](https://lilybre.lilystudio.space/book/454) —— 理解软件开发中的沟通、复杂度与维护

## 🗺️ 学习路线

学习路线遵循“看懂错误 → 稳定复现 → 编写测试 → 自动验证”的递进顺序。

1. [读懂错误与 Traceback](01-errors-tracebacks.md)
2. [断点、日志与最小复现](02-debugger-logs-repro.md)
3. [用 pytest 写第一组测试](03-pytest-basics.md)
4. [测试边界、替身与持续集成](04-test-design-ci.md)
5. [综合项目：给记账本加质量保障](05-project.md)

反馈入口：[GitHub Issues](https://github.com/nannahelper/docs/issues)
