# Go 语言新手指南

> **简洁高效，并发至上** —— 系统掌握 Go 语言的语法、并发模型与工程实践，开启现代后端开发之旅。

---

## 教程简介

Go（又称 Golang）是 Google 在 2009 年发布的开源编程语言，由 Rob Pike、Ken Thompson 和 Robert Griesemer 设计。它以 **简洁的语法**、**原生的并发支持** 和 **高效的编译速度** 著称，已成为云原生、微服务和 DevOps 领域的主流语言之一。

本教程面向编程新手，系统讲解 Go 的核心语法、并发模型和标准库使用。每章配有代码示例和实践任务，帮助你从零构建可运行的 Go 应用程序。

!!! info "为什么学习 Go？"

    - **语法简洁**：只有 25 个关键字，学习曲线平缓
    - **并发原生**：goroutine 和 channel 让并发编程变得直观
    - **编译高效**：编译为单一静态二进制文件，部署极其简单
    - **生态丰富**：Kubernetes、Docker、Prometheus 等核心基础设施均用 Go 编写
    - **就业前景**：云原生时代的首选语言之一，岗位需求持续增长

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 掌握 Go 语法、并发编程、标准库使用，能独立开发 RESTful API 服务 |
| **预计时长** | 12~15 小时 |
| **前置要求** | 基本的计算机操作知识，有其他编程语言基础更佳（非必需） |
| **最终产出** | 一个可运行的 HTTP API 服务，包含测试和部署配置 |

---

## 学习路径

| 章节 | 核心内容 | 难度 |
|:---|:---|:---:|
| [第 1 章：认识 Go](01-introduction.md) | 语言哲学、环境搭建、第一个程序 | ★ |
| [第 2 章：变量与数据类型](02-variables-and-types.md) | 基本类型、零值、类型推断、常量 | ★★ |
| [第 3 章：控制流程](03-control-flow.md) | if/else、for、switch、标签控制 | ★★ |
| [第 4 章：函数](04-functions.md) | 多返回值、可变参数、defer、闭包 | ★★★ |
| [第 5 章：复合类型](05-composite-types.md) | 数组、切片、映射、结构体 | ★★★ |
| [第 6 章：方法与接口](06-methods-and-interfaces.md) | 接收者、接口隐式实现、类型断言 | ★★★★ |
| [第 7 章：指针与内存](07-pointers-and-memory.md) | 取址/解引用、new/make、逃逸分析 | ★★★★ |
| [第 8 章：包与模块](08-packages-and-modules.md) | package、import、go mod、可见性 | ★★★ |
| [第 9 章：错误处理](09-error-handling.md) | error 接口、panic/recover、错误包装 | ★★★★ |
| [第 10 章：并发编程](10-concurrency.md) | goroutine、channel、select、sync 包 | ★★★★★ |
| [第 11 章：标准库概览](11-standard-library.md) | fmt、io、os、net/http、encoding/json | ★★★ |
| [第 12 章：综合实战](12-final-project.md) | RESTful API 服务 + 测试 + 编译部署 | ★★★★★ |

---

## 快速导航

- 🚀 **刚接触？** 从[第 1 章](01-introduction.md)开始，搭建 Go 环境并运行第一个程序
- 📦 **想了解类型系统？** 跳到[第 2 章](02-variables-and-types.md)学习变量和数据类型
- ⚡ **对并发感兴趣？** [第 10 章](10-concurrency.md)带你深入 goroutine 和 channel
- 🛠️ **想动手做项目？** [第 12 章](12-final-project.md)从零构建一个 HTTP API 服务

---

> **Go 语言** —— 少即是多，简约而不简单。
