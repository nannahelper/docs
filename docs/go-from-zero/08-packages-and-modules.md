# 第 8 章：包与模块

> **包与模块** —— 包（package）是 Go 代码的基本组织单元，模块（module）是 Go 包集合的版本化管理机制。两者共同构成了 Go 的代码组织与依赖管理体系。

---

## 8.1 包的概念

包（package）是 Go 中代码组织与复用的基本单位。每个 `.go` 源文件都属于某个包，同一目录下的源文件必须属于同一个包。

### 8.1.1 main 包 vs 库包

```go
// 文件路径：main.go
// main 包是可执行程序的入口
package main

import "fmt"

func main() {
    fmt.Println("这是一个可执行程序")
}
```

```go
// 文件路径：mathutil/mathutil.go
// 库包：被其他程序导入使用
package mathutil

// Add 返回两个整数的和
func Add(a, b int) int {
    return a + b
}

// subtract 以小写字母开头，是包外不可见的私有函数
func subtract(a, b int) int {
    return a - b
}
```

> `package main` 告诉 Go 编译器这是一个可执行程序，必须包含 `main()` 函数作为入口。其他包名则用于代码组织，不可直接运行。

---

## 8.2 import 导入

### 8.2.1 单行导入与多行导入

```go
package main

// 单行导入
import "fmt"

// 多行导入（推荐，风格更清晰）
import (
    "math"
    "strings"
)

func main() {
    fmt.Println(math.Sqrt(16))
    fmt.Println(strings.ToUpper("hello"))
}
```

### 8.2.2 导入别名

当包名冲突或过长时间，可以使用别名。

```go
package main

import (
    "fmt"
    "math/rand"
    cr "crypto/rand" // 别名 cr
)

func main() {
    // 使用 math/rand 包
    fmt.Println(rand.Intn(100))

    // 使用 crypto/rand 包（通过别名）
    b := make([]byte, 4)
    cr.Read(b)
    fmt.Println(b)
}
```

### 8.2.3 匿名导入

使用下划线 `_` 作为包别名，仅执行包的 `init` 函数但不引用包中的其他符号。

```go
package main

import (
    "fmt"
    _ "image/png" // 仅注册 PNG 解码器，不直接使用
)

func main() {
    fmt.Println("匿名导入仅执行 init 函数")
}
```

> 匿名导入的典型用途是注册数据库驱动或图像编解码器。

---

## 8.3 可见性规则

Go 的可见性控制非常简单：**大写字母开头的名字可以被导出（public），小写字母开头的名字是包私有的（private）**。

```go
package example

// === 导出（包外可访问） ===

// PI 是导出的常量
const PI = 3.14159

// Point 是导出的结构体类型
type Point struct {
    X, Y float64 // 字段 X, Y 也是导出的
}

// NewPoint 是导出的构造函数
func NewPoint(x, y float64) Point {
    return Point{X: x, Y: y}
}

// Distance 是导出的函数
func Distance(p1, p2 Point) float64 {
    return p1.distance(p2) // 内部调用私有方法
}

// === 非导出（包内可见） ===

// version 是包私有的常量
const version = "1.0.0"

// coordinate 是非导出类型
type coordinate struct {
    lat, lng float64
}

// distance 是包私有的方法
func (p Point) distance(other Point) float64 {
    return sqrt(pow(p.X-other.X) + pow(p.Y-other.Y))
}

// pow 是包私有的辅助函数
func pow(x float64) float64 {
    return x * x
}

// sqrt 是包私有的辅助函数
func sqrt(x float64) float64 {
    // 简易实现，实际应使用 math.Sqrt
    return x / 2
}
```

> **可见性规则仅作用于包级别**。同一个包内的不同文件可以互相访问私有标识符。

---

## 8.4 Go Modules

Go Modules 是 Go 1.11 引入的官方依赖管理机制，是现代 Go 项目的标准配置方式。

### 8.4.1 初始化模块

```bash
# 创建新模块
mkdir myproject
cd myproject
go mod init example.com/myproject
```

执行 `go mod init` 后，会生成 `go.mod` 文件：

```
module example.com/myproject

go 1.21
```

### 8.4.2 go.mod 文件结构

```go
module github.com/user/myproject

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/go-sql-driver/mysql v1.7.1
)

// 可选：替换模块（常用于本地开发或代理）
replace example.com/old => example.com/new v1.2.0

// 可选：排除特定版本
exclude example.com/bad v1.0.0
```

### 8.4.3 go.sum 文件

`go.sum` 记录每个依赖模块的预期内容哈希值，用于 **完整性校验**，防止依赖篡改。

```
github.com/gin-gonic/gin v1.9.1 h1:abcdeqL...
github.com/gin-gonic/gin v1.9.1/go.mod h1:...
```

> `go.sum` 应纳入版本控制（提交到 Git），以确保构建可复现。

---

## 8.5 依赖管理命令

### 8.5.1 go get

添加或更新依赖：

```bash
# 添加特定依赖
go get github.com/gin-gonic/gin

# 升级到特定版本
go get github.com/gin-gonic/gin@v1.8.0

# 升级所有依赖到最新小版本
go get -u ./...

# 移除未使用的依赖
go mod tidy
```

### 8.5.2 go mod tidy

`go mod tidy` 是最常用的依赖维护命令，它自动完成以下操作：

1. 添加代码中引用的但 `go.mod` 缺失的依赖
2. 移除 `go.mod` 中存在但代码中不再引用的依赖
3. 更新 `go.sum` 以匹配 `go.mod` 的内容

```bash
# 整理依赖
go mod tidy
```

### 8.5.3 go mod vendor

创建 `vendor` 目录，将所有依赖的源代码复制到项目内：

```bash
# 创建 vendor 目录
go mod vendor

# 使用 vendor 构建（不联网下载依赖）
go build -mod=vendor
```

> `vendor` 适用于离线环境或需要精确控制依赖的场景，但会增加仓库体积。

---

## 8.6 内部包（internal packages）

Go 提供 `internal` 包机制，用于限制包的导入范围：`internal` 包只能被其父目录树内的代码导入。

```
project/
├── internal/
│   └── auth/
│       └── token.go         # 包路径：project/internal/auth
├── admin/
│   ├── main.go               # 可导入 internal/auth
│   └── internal/
│       └── helper.go         # 包路径：project/admin/internal
├── api/
│   └── handler.go            # 可导入 internal/auth
└── cmd/
    └── tool/
        └── main.go           # **不可**导入 internal/auth
```

```go
// project/internal/auth/token.go
package auth

// Token 生成函数（只允许 project 内部的包使用）
func GenerateToken(userID string) string {
    return "token_" + userID
}
```

```go
// project/api/handler.go — 合法导入
package api

import "project/internal/auth"

func HandleLogin() {
    token := auth.GenerateToken("user123") // OK：处于 project 内部
    _ = token
}
```

> `internal` 是 Go 强制实施的导入限制，违反会导致编译错误。

---

## 8.7 标准库包结构概览

Go 标准库提供了丰富的包，涵盖 I/O、网络、加密、文本处理等各个领域。以下是常用包的分类概览。

### I/O 与文件操作

| 包路径 | 用途 |
|--------|------|
| `io` | 基本的 I/O 接口（Reader/Writer） |
| `os` | 操作系统功能（文件读写、环境变量、进程） |
| `bufio` | 缓冲 I/O |
| `ioutil`（1.16 前） | I/O 工具函数 |

### 文本与字符串

| 包路径 | 用途 |
|--------|------|
| `strings` | 字符串操作（查找、切割、替换） |
| `strconv` | 字符串与基本类型间的转换 |
| `fmt` | 格式化 I/O（Printf、Scanf） |
| `regexp` | 正则表达式 |
| `unicode` | Unicode 字符处理 |

### 网络与并发

| 包路径 | 用途 |
|--------|------|
| `net` | 网络连接（TCP、UDP、Unix socket） |
| `net/http` | HTTP 客户端与服务器 |
| `sync` | 同步原语（Mutex、WaitGroup） |
| `context` | 上下文传递与取消传播 |

### 数据结构与算法

| 包路径 | 用途 |
|--------|------|
| `container/list` | 双向链表 |
| `container/heap` | 堆操作接口 |
| `sort` | 排序函数 |
| `math` | 数学函数与常量 |

### 编码与序列化

| 包路径 | 用途 |
|--------|------|
| `encoding/json` | JSON 编解码 |
| `encoding/xml` | XML 编解码 |
| `encoding/base64` | Base64 编解码 |

> 完整标准库列表参见：https://pkg.go.dev/std

---

## 8.8 init 函数

`init` 函数是 Go 中在 `main` 执行之前自动运行的初始化函数。

### 8.8.1 基本特性

```go
package main

import "fmt"

// init 函数在 main 之前自动执行
func init() {
    fmt.Println("第二个 init")
}

// 同一个包中可以有多个 init 函数
func init() {
    fmt.Println("第一个 init")
}

func main() {
    fmt.Println("main 函数执行")
}

// 执行顺序：
// 第一个 init
// 第二个 init
// main 函数执行
```

### 8.8.2 执行顺序规则

```go
// 文件：a/pack1.go
package a

import _ "b"

func init() {
    fmt.Println("pack1 init")
}
```

```go
// 文件：b/pack2.go
package b

func init() {
    fmt.Println("pack2 init")
}
```

```
// 执行顺序：
// 1. 所有导入的依赖包先 init（按导入图拓扑排序）
// 2. 同一包内多个 init 按文件名的字典序执行
// 3. 最后执行 main 包的 init → main 函数
```

### 8.8.3 init 的典型用途

```go
package database

import (
    "database/sql"
    _ "github.com/go-sql-driver/mysql" // 匿名导入，执行 init 驱动注册
)

var db *sql.DB

func init() {
    var err error
    db, err = sql.Open("mysql", "user:password@tcp(localhost:3306)/db")
    if err != nil {
        panic("数据库连接失败: " + err.Error())
    }
}

func GetDB() *sql.DB {
    return db
}
```

> `init` 函数 **没有参数和返回值**，不能被显式调用，仅在包级别初始化时自动执行。

---

## 8.9 本章小结

- **包** 是 Go 代码组织的基本单位，`package main` 用于可执行程序，其他包名用于库代码。
- **import** 支持单行、多行、别名和匿名导入四种形式。
- **可见性规则** 简单：大写导出，小写私有。
- **Go Modules** 是官方依赖管理方案，`go.mod` 记录模块路径和依赖，`go.sum` 保证完整性。
- 常用命令包括 `go get`（添加依赖）、`go mod tidy`（整理依赖）、`go mod vendor`（生成 vendor 目录）。
- **internal 包** 限制导入范围为父目录树，用于实现包级封装。
- **标准库** 覆盖 I/O、网络、文本处理、数据结构等核心领域，是 Go 开发的基础工具。
- **init 函数** 在包初始化时自动执行，按依赖拓扑排序，适合注册驱动、初始化全局状态等场景。

---

## 实践任务

1. 创建一个名为 `stringutil` 的库包，包含 `Reverse(s string) string`（反转字符串）和 `IsPalindrome(s string) bool`（判断回文）两个可导出函数。编写 `main` 包导入并使用该库包。

2. 在项目中创建一个 `internal/validator` 包，包含一个 `ValidateEmail(email string) bool` 函数。验证 `main` 包可以访问，但项目外部的包 **无法** 访问该 internal 包。

3. 创建一个包含多个文件的包，在不同文件中定义不同的 `init` 函数。通过导入该包并观察输出，验证 `init` 函数的执行顺序。尝试同时引入 `vendor` 依赖管理并观察 `go mod tidy` 的效果。

---

👉 [下一章：第 9 章 · 错误处理 →](09-error-handling.md)
👉 [返回教程首页 →](index.md)
