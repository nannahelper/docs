# 调试与测试指南

调试是在问“程序为什么这样运行”，测试是在问“程序在这些条件下是否符合预期”。两者结合，才能把修改变得可验证。

| 项目 | 内容 |
|---|---|
| 适合人群 | 已经能写简单程序，想减少“改了这里又坏了那里”的学习者 |
| 预计时长 | 6–8 小时（包含练习） |
| 适用版本 | Python 3.11+、pytest 8+、GitHub Actions |
| 维护状态 | 维护中 |
| 最后更新 | 2026-08-13 |

## 推荐教材

- [Architecture Patterns with Python](https://lilybre.lilystudio.space/book/25) —— 将测试驱动开发放进真实架构中
- [The Mythical Man-Month](https://lilybre.lilystudio.space/book/454) —— 理解软件开发中的沟通、复杂度与维护

## 学习路径

1. [读懂错误与 Traceback](01-errors-tracebacks.md)
2. [断点、日志与最小复现](02-debugger-logs-repro.md)
3. [用 pytest 写第一组测试](03-pytest-basics.md)
4. [测试边界、替身与持续集成](04-test-design-ci.md)
5. [综合项目：给记账本加质量保障](05-project.md)

反馈入口：[GitHub Issues](https://github.com/nannahelper/docs/issues)
