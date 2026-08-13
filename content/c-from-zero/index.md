# C 语言新手指南

C 语言让你更接近程序运行的底层：类型如何占用内存，指针如何访问地址，编译器如何把源代码变成可执行文件。

| 项目 | 内容 |
|---|---|
| 适合人群 | 已接触过一种编程语言，想学习系统编程、嵌入式或计算机底层的学习者 |
| 预计时长 | 约 4 小时（包含练习） |
| 适用版本 | C17；GCC 13+ 或 Clang 16+ |
| 维护状态 | 维护中 |
| 最后更新 | 2026-08-13 |
| 反馈入口 | [GitHub Issues](https://github.com/nannahelper/docs/issues) |

## 🎯 学习目标

- 能使用编译器构建并运行 C 程序。
- 能解释类型、数组、指针和动态内存的基本关系。
- 能按职责拆分头文件和源文件。
- 完成一个带文件持久化的命令行通讯录。

## 📋 前置要求

- 会使用终端进入目录和运行命令。
- 了解变量、条件和循环等基本编程概念。
- 准备 GCC 13+ 或 Clang 16+。

## 📚 推荐教材

- [C Programming: A Modern Approach](https://lilybre.lilystudio.space/book/233) —— 体系完整，适合主线学习
- [The C Programming Language](https://lilybre.lilystudio.space/book/994) —— C 语言经典参考

## 🗺️ 学习路线

本课程使用“从编译器到内存，再到可交付项目”的递进路线。

| 章节 | 核心目标 | 入口 |
|:---|:---|:---|
| 第 1 章 | 编译、类型与输入输出 | [进入章节](01-compile-types-io.md) |
| 第 2 章 | 流程、数组与字符串 | [进入章节](02-control-arrays-strings.md) |
| 第 3 章 | 指针与内存 | [进入章节](03-pointers-memory.md) |
| 第 4 章 | 结构体、文件与模块 | [进入章节](04-structs-files-modules.md) |
| 第 5 章 | 综合项目：通讯录 | [进入章节](05-project.md) |

!!! warning "安全练习"
    指针和内存练习请在自己的测试目录中进行。遇到崩溃时，先保存错误信息，不要反复执行不理解的内存操作。

反馈入口：[GitHub Issues](https://github.com/nannahelper/docs/issues)
