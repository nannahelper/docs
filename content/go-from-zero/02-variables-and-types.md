# 第 2 章：变量与数据类型

> **数据是程序的基石** —— 掌握 Go 的变量声明方式、基本数据类型、类型推断与转换，以及常量的使用。

---

## 2.1 变量声明

Go 提供两种变量声明方式：`var` 完整声明和 `:=` 短变量声明。

### 2.1.1 var 声明

`var` 是 Go 中最基本的变量声明方式，可在函数内部或包级别使用：

```go
package main

import "fmt"

// 包级别变量声明
var version = "1.0.0"

func main() {
    // 声明变量并指定类型
    var name string = "Go"

    // 声明变量，省略类型（类型推断）
    var year = 2009

    // 声明多个变量
    var x, y int = 10, 20

    // 先声明，后赋值
    var score int
    score = 95

    fmt.Println(name, year, x, y, score, version)
}
```

`var` 声明的通用形式：

```
var 变量名 类型 = 初始值
```

其中 **类型** 和 **= 初始值** 可以省略其一，但不能同时省略。

### 2.1.2 短变量声明 :=

在函数内部，可以使用 `:=` 进行短变量声明——同时完成声明和类型推断：

```go
func main() {
    // 短变量声明，省略 var 关键字和类型
    name := "Go"        // 推断为 string
    year := 2009        // 推断为 int
    version := 1.0      // 推断为 float64

    // 多个变量同时声明
    x, y := 10, 20

    // 交换两个变量的值
    x, y = y, x         // 此时 x=20, y=10
}
```

**限制条件：**

- `:=` 只能在函数内部使用，不可用于包级别声明
- `:=` 声明时至少有一个变量是 **新的**（即至少有一个左侧变量尚未被声明过）

```go
func main() {
    x := 10
    x, y := 20, 30   // 允许：x 已存在，但 y 是新变量
    // x := 20       // 编译错误：左侧没有新变量
}
```

### 2.1.3 变量声明的选择原则

| 场景 | 推荐方式 |
|------|---------|
| 包级别变量 | `var` 声明 |
| 函数内部局部变量 | `:=` 短声明 |
| 需要显式指定类型（如 `float32`） | `var` 带上类型 |
| 零值初始化 | `var score int`（无需赋值） |

## 2.2 基本数据类型

### 2.2.1 布尔型（bool）

`bool` 类型只有两个值：`true` 和 `false`。默认零值为 `false`。

```go
var isReady bool = true
var isDone bool   // 零值为 false
```

布尔值不能与整数进行隐式转换。在 Go 中，`if (1)` 是非法的——必须使用布尔表达式。

### 2.2.2 整数类型（int / uint）

Go 提供多种不同位宽的整数类型：

| 类型 | 位宽 | 取值范围 |
|------|------|----------|
| `int8` | 8 位 | -128 ~ 127 |
| `int16` | 16 位 | -32768 ~ 32767 |
| `int32` | 32 位 | -2^31 ~ 2^31-1 |
| `int64` | 64 位 | -2^63 ~ 2^63-1 |
| `int` | 平台相关 | 32 位系统上为 32 位，64 位系统上为 64 位 |
| `uint8` | 8 位 | 0 ~ 255 |
| `uint16` | 16 位 | 0 ~ 65535 |
| `uint32` | 32 位 | 0 ~ 2^32-1 |
| `uint64` | 64 位 | 0 ~ 2^64-1 |
| `uint` | 平台相关 | 32 位或 64 位 |
| `uintptr` | 平台相关 | 足以存储指针值的无符号整数 |

**最佳实践：** 大多数场景直接使用 `int` 即可。仅在需要明确位宽或优化内存占用时使用特定位宽类型。

```go
var a int = 42
var b uint8 = 255       // byte 的别名
var c int64 = 1 << 62   // 大整数
```

### 2.2.3 浮点类型（float）

| 类型 | 位宽 | 精度 |
|------|------|------|
| `float32` | 32 位 | 大约 7 位十进制有效数字 |
| `float64` | 64 位 | 大约 15 位十进制有效数字 |

```go
var pi float64 = 3.141592653589793
var e float32 = 2.71828
```

**默认推断规则：** 浮点数字面量（如 `3.14`）默认推断为 `float64`。

### 2.2.4 字符串（string）

字符串是 Go 中 **不可变** 的字节序列，使用 UTF-8 编码：

```go
var s1 string = "Hello, Go"
s2 := "字符串中的换行必须使用转义\n"
```

字符串的常见操作：

```go
func main() {
    s := "Hello, Go"

    // 获取字符串长度（字节数，而非字符数）
    fmt.Println(len(s))   // 输出：9

    // 索引访问（返回字节，而非字符）
    fmt.Println(s[0])     // 输出：72（H 的 ASCII 码值）

    // 子串截取
    fmt.Println(s[0:5])   // 输出：Hello

    // 字符串拼接
    fmt.Println(s + " 语言")  // 输出：Hello, Go 语言
}
```

**重要：** `len(s)` 返回的是字节数，而非字符（rune）数。对于包含中文、日文等多字节字符的字符串（如 `"Go 语言"`），`len` 的结果可能与肉眼看到的字符数不同。

### 2.2.5 byte 与 rune

这是 Go 中用于处理字符的两个特殊类型：

| 类型 | 本质 | 用途 | 字面量 |
|------|------|------|--------|
| `byte` | `uint8` 的别名 | 表示 ASCII 字符或原始字节 | `'A'`、`'\n'` |
| `rune` | `int32` 的别名 | 表示 Unicode 码点（一个字符） | `'中'`、`'中'` |

```go
func main() {
    var b byte = 'A'       // 97
    var r rune = '中'      // 20013 (Unicode U+4E2D)

    fmt.Printf("byte: %c, value: %d\n", b, b)   // byte: A, value: 65
    fmt.Printf("rune: %c, value: %d\n", r, r)   // rune: 中, value: 20013

    // 字符串由字节组成，转换为 rune 切片后才能按字符遍历
    s := "Go 语言"
    fmt.Println("byte length:", len(s))       // 输出：9

    runes := []rune(s)
    fmt.Println("rune count:", len(runes))     // 输出：5（G/o/ /语/言）
}
```

## 2.3 零值（Zero Value）

Go 中所有变量在声明且未显式赋值时，会被自动赋予该类型的 **零值**。这是 Go 的重要安全特性——不存在未初始化的变量。

| 类型 | 零值 |
|------|------|
| 所有数值类型（int、float 等） | `0` |
| bool | `false` |
| string | `""`（空字符串） |
| 指针、切片、映射、通道、接口、函数 | `nil` |

```go
func main() {
    var i int
    var f float64
    var b bool
    var s string

    fmt.Printf("int: %v\n", i)       // int: 0
    fmt.Printf("float64: %v\n", f)   // float64: 0
    fmt.Printf("bool: %v\n", b)      // bool: false
    fmt.Printf("string: '%v'\n", s)  // string: ''
}
```

## 2.4 类型推断

当使用 `:=` 或 `var` 声明且提供初始值时，Go 编译器会自动推断变量的数据类型：

```go
func main() {
    v1 := 42            // int
    v2 := 3.14          // float64
    v3 := "hello"       // string
    v4 := 3 + 4i        // complex128
    v5 := true          // bool

    fmt.Printf("v1: %T\n", v1)   // int
    fmt.Printf("v2: %T\n", v2)   // float64
}
```

类型推断规则（整数特殊情况）：

- 整数字面量 `42` 默认推断为 `int`
- 浮点数字面量 `3.14` 默认推断为 `float64`
- 若需要特定位宽类型，须显式声明

```go
var score float32 = 97.5   // 必须显式指定 float32，否则默认为 float64
```

## 2.5 类型转换

**Go 没有隐式类型转换。** 任何不同数据类型之间的转换都必须显式进行。这是 Go 安全设计的重要部分——防止数值精度意外丢失。

```go
func main() {
    var x int = 42
    var y float64 = float64(x)   // 显式 int -> float64

    var a float64 = 3.14
    var b int = int(a)           // 显式 float64 -> int（截断小数）
    fmt.Println(b)               // 输出：3

    // 编译错误：cannot use x (variable of type int) as type float64
    // var z float64 = x
}
```

类型转换的通用语法：**目标类型(表达式)**

```go
// 不同类型之间的运算须先统一类型
var m int = 10
var n int64 = 20

// 编译错误：invalid operation: m + n (mismatched types int and int64)
// fmt.Println(m + n)

fmt.Println(m + int(n))   // 正确：将 n 转换为 int
```

**字符串与整数之间的转换** 需要使用 `strconv` 包：

```go
import "strconv"

func main() {
    // 整数转字符串
    s := strconv.Itoa(42)
    fmt.Println(s)   // "42"

    // 字符串转整数
    n, err := strconv.Atoi("42")
    if err == nil {
        fmt.Println(n)   // 42
    }
}
```

## 2.6 常量

### 2.6.1 基本常量

常量使用 `const` 关键字声明，定义后不可修改：

```go
const Pi = 3.14159
const Language string = "Go"

func main() {
    const MaxRetries = 3
    fmt.Println(Pi, Language, MaxRetries)

    // 编译错误：cannot assign to MaxRetries
    // MaxRetries = 5
}
```

常量的特点：

- 声明时必须赋值
- 只能使用编译器可确定的表达式（如字面量、其他常量、内置函数 `len` 等）
- 常量不指定类型时属于 **无类型常量**，在上下文中根据需要推断类型

### 2.6.2 iota 枚举

`iota` 是 Go 中常量生成器，在一个 `const` 声明块中从 0 开始逐行递增：

```go
const (
    Sunday = iota     // 0
    Monday            // 1
    Tuesday           // 2
    Wednesday         // 3
    Thursday          // 4
    Friday            // 5
    Saturday          // 6
)

const (
    B = 1 << (iota * 10)   // iota = 0 → 1 << 0 = 1
    KB                     // iota = 1 → 1 << 10 = 1024
    MB                     // iota = 2 → 1 << 20 = 1048576
    GB                     // iota = 3 → 1 << 30 = 1073741824
)
```

关于 `iota` 的几点规则：

- `iota` 在每个 `const` 块中从 0 开始重新计数
- 每次新行 `iota` 的值加 1
- 可以使用 `_` 跳过某些值

```go
const (
    A = iota   // 0
    _          // 1 被跳过
    C          // 2
)
```

## 2.7 格式化输出

`fmt.Printf` 函数支持多种格式化占位符，用于输出变量的类型和值：

| 占位符 | 作用 | 示例输出 |
|--------|------|----------|
| `%v` | 值的默认格式 | `42`、`hello` |
| `%+v` | 对结构体输出字段名 | `{Name:Go, Year:2009}` |
| `%#v` | 输出 Go 语法表示 | `"hello"`、`42` |
| `%T` | 输出变量的类型 | `int`、`string` |
| `%d` | 十进制整数 | `42` |
| `%f` | 浮点数 | `3.141590` |
| `%s` | 字符串 | `hello` |
| `%t` | 布尔值 | `true` |
| `%q` | 带引号的字符串 | `"hello"` |

```go
func main() {
    name := "Go"
    year := 2009
    version := 1.22
    isStable := true

    fmt.Printf("name: %T = %v\n", name, name)        // name: string = Go
    fmt.Printf("year: %T = %d (%#v)\n", year, year, year)  // year: int = 42 (2009)
    fmt.Printf("version: %.1f\n", version)            // version: 1.2
    fmt.Printf("stable: %t\n", isStable)              // stable: true
    fmt.Printf("Go syntax: %#v\n", name)              // Go syntax: "Go"
}
```

---

## 2.8 本章小结

- 变量声明有两种方式：`var` 完整声明（包级别或函数内）和 `:=` 短声明（仅限函数内部）
- Go 是强类型语言，提供 `bool`、`int/uint`（多种位宽）、`float32/64`、`string`、`byte`、`rune` 等基本类型
- 每个类型都有零值：数值类型为 `0`，`bool` 为 `false`，`string` 为 `""`
- Go 自动进行类型推断，但不存在隐式类型转换——类型转换必须显式书写
- 常量使用 `const` 声明；`iota` 可在 `const` 块中生成递增枚举值
- `fmt.Printf` 配合 `%T`、`%v`、`%+v`、`%#v` 等占位符可以灵活输出变量信息

---

## 实践任务

1. 分别使用 `var` 和 `:=` 声明一个 `int`、一个 `string` 和一个 `float64` 变量，观察两者的语法差异
2. 声明一个 `int` 变量和一个 `int64` 变量，尝试直接相加，观察编译器的错误信息；然后使用类型转换使其正确运行
3. 使用 `iota` 定义一周七天的常量（从 Sunday = 0 到 Saturday = 6），并在 `main` 函数中输出它们
4. 声明一个包含中文的字符串，分别用 `len()` 和 `[]rune()` 计算其长度，观察差异
5. 对一个 `float64` 变量不使用任何格式化直接打印，再用 `%.2f` 格式化打印，观察输出效果

---

👉 [下一章：第 3 章 · 控制流程 →](03-control-flow.md)
👉 [返回教程首页 →](index.md)
