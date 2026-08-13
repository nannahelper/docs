# 第 1 章：认识 Go

> **从零开始，认识一门为现代工程而生的编程语言** —— 了解 Go 的起源、设计哲学、安装方法，并编写你的第一个 Go 程序。

---

## 1.1 Go 语言的起源

Go 语言（又称 Golang）由 Google 的三位杰出工程师于 2007 年开始设计，并于 2009 年正式对外发布：

- **Rob Pike** —— 贝尔实验室 Unix 团队出身，参与设计 UTF-8 编码
- **Ken Thompson** —— Unix 操作系统和 B 语言的共同创造者，图灵奖得主
- **Robert Griesemer** —— 曾参与 Java 虚拟机（JVM）和 V8 JavaScript 引擎的工作

三位设计者的共同感受是：当时的编程语言在 **开发效率** 与 **运行性能** 之间存在两难选择。

- C/C++ 运行极快，但编译缓慢、内存管理复杂、语法过于底层
- Java 和 C# 有垃圾回收和丰富生态，但虚拟机启动开销大、类型系统臃肿
- Python 和 Ruby 开发效率高，但运行时性能难以满足大规模并发需求

Go 的目标是 **兼具 C 的运行效率、Python 的开发速度和 Java 的工程化能力**，同时从根本上简化语言规范——Go 的完整语言规范仅有约 60 页，而 C++ 的规范超过 1300 页。

## 1.2 设计哲学

Go 的设计始终围绕以下核心理念展开：

### 1.2.1 简洁至上

- 仅有 **25 个关键字**，远少于 C 语言的 32 个、C++ 的 84 个
- 没有类、继承、泛型（1.18 版本之前）、异常、三元运算符等复杂机制
- 强制统一的代码格式（`go fmt` 工具）
- 语法追求直白，不追求语法糖

### 1.2.2 高效编译

- Go 编译器在数秒内完成数十万行代码的编译
- 静态链接生成单个可执行文件，无需外部运行时依赖
- 交叉编译能力一流：在 Windows 上编译 Linux 可执行文件仅需设置环境变量

### 1.2.3 原生并发

- **goroutine**：轻量级用户态线程，初始栈仅 2 KB，单进程可创建数十万甚至数百万个
- **channel**：CSP（Communicating Sequential Processes）模型的通信机制
- `go` 关键字即可启动并发；语言层面而非库层面支持并发

```go
// goroutine 示例：仅需一个 go 关键字
go func() {
    fmt.Println("Hello from goroutine!")
}()
```

## 1.3 应用领域

Go 在以下领域得到了广泛采用：

| 领域 | 代表项目/用途 |
|------|-------------|
| **云原生基础设施** | Docker、Kubernetes、Etcd、Prometheus 均以 Go 编写 |
| **微服务** | 结合 gRPC 和 Protocol Buffers，构建高性能分布式系统 |
| **CLI 工具** | Hugo（静态站点生成器）、Cobra（命令行框架） |
| **DevOps** | Terraform、Vault、Consul 等 HashiCorp 全栈工具 |
| **网络编程** | 标准库 net/http 即可搭建生产级 HTTP 服务 |
| **数据库** | InfluxDB（时序数据库）、CockroachDB（分布式 SQL） |

由于 Go 编译为单个静态二进制文件，在容器化部署（Docker 镜像）环境中有天然优势——镜像体积小、启动快、无需安装运行时。

## 1.4 安装 Go

### 1.4.1 下载与安装

访问 [https://go.dev/dl](https://go.dev/dl)，选择对应操作系统的安装包：

**Windows**
- 下载 `.msi` 安装包，运行安装程序
- 默认安装路径为 `C:\Program Files\Go`
- 安装程序会自动将 Go 加入系统 PATH

**macOS**
- 下载 `.pkg` 安装包，运行安装程序
- 或使用 Homebrew：`brew install go`

**Linux**
- 下载 `.tar.gz` 压缩包，解压到 `/usr/local`：
```bash
wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
```

### 1.4.2 验证安装

打开终端（命令行），执行以下命令：

```bash
go version
```

预期输出类似：

```
go version go1.22.0 windows/amd64
```

若成功输出版本信息，则说明 Go 已正确安装。

## 1.5 GOPATH 与 Go Modules

### 1.5.1 GOPATH（历史背景）

在 Go 1.11 版本之前，所有 Go 代码必须存放在 `GOPATH/src` 目录下，且依赖通过 `go get` 命令下载到该目录中。这种方式在依赖管理方面存在诸多不便：

- 同一机器的不同项目无法使用同一个依赖的不同版本
- 缺乏显式的版本锁定机制

### 1.5.2 Go Modules（现代方式）

从 Go 1.11 引入、1.16 起默认启用的 **Go Modules** 机制解决了上述问题。

初始化一个新模块：

```bash
mkdir hello
cd hello
go mod init hello
```

上述命令会生成 `go.mod` 文件，内容类似：

```
module hello

go 1.22
```

`go.mod` 文件是模块的身份证，记录模块名称、Go 版本和外部依赖信息。后续添加依赖后，会自动生成 `go.sum` 文件记录依赖的哈希校验值。

**建议：** 从学习第一天起就使用 Go Modules，无需再为 GOPATH 的配置烦恼。

## 1.6 第一个 Go 程序

创建文件 `main.go`，输入以下内容：

```go
package main  // 每个 Go 文件必须以 package 声明开头

import "fmt"  // 导入标准库的 fmt 包，用于格式化输入输出

// main 函数是程序的入口点
func main() {
    fmt.Println("Hello, World!")  // 打印到控制台，自动换行
}
```

### 逐行解析

| 代码 | 说明 |
|------|------|
| `package main` | 声明该文件属于 `main` 包。可执行程序必须包含 `main` 包 |
| `import "fmt"` | 导入 `fmt` 标准库包，`fmt` 提供格式化 I/O 功能 |
| `func main()` | 定义 `main` 函数——每个可执行程序有且仅有一个 `main` 函数 |
| `fmt.Println(...)` | 调用 `fmt` 包的 `Println` 函数，输出字符串并换行 |

### 运行程序

**方式一：直接运行（不生成文件）**

```bash
go run main.go
```

输出：`Hello, World!`

**方式二：编译为可执行文件**

```bash
go build main.go
```

生成的可执行文件：
- Windows 下为 `main.exe`
- Linux/macOS 下为 `main`

然后单独运行：

```bash
# Linux/macOS
./main

# Windows
main.exe
```

**性能对比：** `go run` 适合开发调试阶段；`go build` 生成的可执行文件没有编译步骤，适合生产部署。

## 1.7 基本 Go 命令

以下是日常开发中最常用的 Go 命令：

| 命令 | 作用 |
|------|------|
| `go run <file>.go` | 编译并运行 Go 程序，不输出可执行文件 |
| `go build <file>.go` | 编译程序，输出可执行文件 |
| `go fmt <file>.go` | 格式化源代码，强制执行官方代码风格 |
| `go mod init <name>` | 初始化一个新的 Go 模块 |
| `go mod tidy` | 清理 `go.mod` 中未使用的依赖 |
| `go vet <file>.go` | 静态分析代码中的潜在问题 |
| `go test` | 运行单元测试 |

**重要习惯：** 每次保存代码后运行 `go fmt`，养成统一格式化的习惯。`go fmt` 的强制统一性是 Go 团队刻意设计的——消除关于代码风格的争论，让开发者专注于逻辑而非格式。

## 1.8 代码组织规则

Go 的代码组织遵循三条基本规则：

1. **一个目录下的所有 `.go` 文件必须属于同一个 package**
   - 名为 `main` 的 package 代表可执行程序
   - 其他名称的 package 代表可被导入的库

2. **可执行程序必须有 `func main()`**
   - `main` 函数不接受参数，不返回任何值
   - 命令行参数通过 `os.Args` 获取

3. **导入的包必须被使用**
   - 导入未使用的包会导致编译失败
   - 这一规则防止代码中积累无用依赖

```go
package main

import (
    "fmt"
    "math"  // 如果删掉下面使用 math.Sqrt 的代码，编译会报错
)

func main() {
    fmt.Printf("The square root of 16 is %v\n", math.Sqrt(16))
}
```

---

## 1.9 本章小结

- Go 由 Google 的 Rob Pike、Ken Thompson 和 Robert Griesemer 设计，于 2009 年发布
- 设计哲学围绕 **简洁、高效、原生并发** 展开
- 主要应用于云原生、微服务、CLI 工具、DevOps 等领域
- 安装后通过 `go version` 验证，建议使用 Go Modules 管理依赖
- 每个 Go 源文件以 `package` 声明开头，可执行程序必须包含 `func main()`
- `go run` 用于快速执行，`go build` 用于生成可执行文件
- `go fmt` 强制统一代码风格，消除格式争议

---

## 实践任务

1. 安装 Go 开发环境，验证 `go version` 命令正常工作
2. 创建任意目录，执行 `go mod init try-go`，观察生成的 `go.mod` 文件内容
3. 编写 "Hello, World" 程序，分别用 `go run` 和 `go build` 执行，对比两者的区别
4. 尝试在 `import` 中额外导入 `"os"` 但不在代码中使用，观察编译器的报错信息
5. 运行 `go fmt` 格式化你的代码，尝试改变缩进或括号位置，观察 `go fmt` 的修正效果

---

👉 [下一章：第 2 章 · 变量与数据类型 →](02-variables-and-types.md)
👉 [返回教程首页 →](index.md)
