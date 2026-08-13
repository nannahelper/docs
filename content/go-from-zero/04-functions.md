# 第 4 章：函数

> **将逻辑组织为可复用的单元** —— 掌握 Go 的函数声明、多返回值、闭包、defer 等核心特性。

---

## 4.1 函数声明

Go 使用 `func` 关键字声明函数，基本格式为：

```
func 函数名(参数列表) 返回值类型 {
    函数体
    return 返回值
}
```

一个最简单的函数示例：

```go
package main

import "fmt"

// add 接受两个 int 参数，返回它们的和
func add(a int, b int) int {
    return a + b
}

func main() {
    result := add(3, 5)
    fmt.Println(result)  // 8
}
```

**参数类型简写：** 当连续多个参数具有相同类型时，可以省略前面参数的类型，仅在最后一个参数处标注：

```go
// 完整写法：a int, b int
// 简写形式：a, b int
func add(a, b int) int {
    return a + b
}
```

## 4.2 多返回值

Go 函数允许返回 **任意数量** 的返回值。这是 Go 区别于大多数 C 系语言的显著特性之一。

```go
// divide 返回商和余数
func divide(a, b int) (int, int) {
    quotient := a / b
    remainder := a % b
    return quotient, remainder
}

func main() {
    q, r := divide(17, 5)
    fmt.Printf("17 / 5 = %d 余 %d\n", q, r)  // 17 / 5 = 3 余 2
}
```

多返回值最常见的用途是 **返回结果和错误**：

```go
import (
    "fmt"
    "strconv"
)

func main() {
    // strconv.Atoi 返回两个值：转换后的整数和错误信息
    n, err := strconv.Atoi("42")
    if err != nil {
        fmt.Println("转换失败：", err)
        return
    }
    fmt.Println("转换成功：", n)
}
```

**最佳实践：** 在 Go 中，**错误总是作为最后一个返回值**。这一约定贯穿整个标准库和主流第三方库。

## 4.3 命名返回值

Go 允许为返回值指定 **变量名**。命名返回值在函数体中如同普通变量，无需在 `return` 语句中显式指明返回值：

```go
// divide 使用命名返回值
func divide(a, b int) (quotient, remainder int) {
    quotient = a / b      // 直接对命名返回值赋值
    remainder = a % b
    return                // 裸返回，自动返回 quotient 和 remainder
}
```

**命名返回值的特性：**

- 命名返回值在函数开始时会被自动初始化为 **零值**
- 使用命名返回值时，`return` 可以省略操作数，称为 **裸返回（naked return）**
- 裸返回仅在短函数中推荐使用；长函数中使用裸返回会降低代码可读性

```go
// 命名返回值自动初始化为零值
func split(sum int) (x, y int) {
    x = sum / 2
    y = sum - x
    return
}

func main() {
    fmt.Println(split(17))  // 8 9
}
```

## 4.4 可变参数

可变参数函数可以接受 **任意数量** 的同一类型参数，通过 `...` 操作符实现：

```go
// sum 接受任意数量的 int 参数
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}

func main() {
    fmt.Println(sum(1, 2))           // 3
    fmt.Println(sum(1, 2, 3, 4))     // 10
    fmt.Println(sum())               // 0（零个参数也可以）
}
```

**内部机制：** 可变参数在函数内部被转换为对应类型的 **切片（slice）**。上述 `nums ...int` 在函数内部等价于 `nums []int`。

**传递切片给可变参数：** 使用 `slice...` 语法将切片展开传入：

```go
func main() {
    values := []int{10, 20, 30}
    fmt.Println(sum(values...))   // 将切片展开后传入
}
```

**规则：** 可变参数必须放在参数列表的 **最后** 一个位置。

```go
// 正确：最后一个是可变参数
func format(prefix string, items ...int) string { ... }

// 编译错误：可变参数必须在最后
// func invalid(items ...int, suffix string) string { ... }
```

## 4.5 defer 延迟执行

`defer` 是 Go 中一个独特的关键字，用于 **延迟一个函数调用** 到当前函数返回之前执行。

### 4.5.1 基本用法

```go
func main() {
    defer fmt.Println("world")
    fmt.Println("hello")
}
// 输出：
// hello
// world
```

### 4.5.2 LIFO 顺序

多个 `defer` 按照 **后进先出（LIFO, Last In First Out）** 的顺序执行：

```go
func main() {
    defer fmt.Println("first")    // 第三个执行
    defer fmt.Println("second")   // 第二个执行
    defer fmt.Println("third")    // 第一个执行
}
// 输出：
// third
// second
// first
```

LIFO 顺序与栈的弹栈顺序一致——最后一次 `defer` 注册的函数最先执行。

### 4.5.3 常见用途：资源清理

`defer` 最主要的用途是确保资源被正确释放，即使函数中途发生了错误或提前返回：

```go
import (
    "fmt"
    "os"
)

func readFile(filename string) {
    // 打开文件
    file, err := os.Open(filename)
    if err != nil {
        fmt.Println("打开文件失败：", err)
        return
    }
    // 注册关闭操作，在函数返回前执行
    defer file.Close()

    // 读取文件内容...
    fmt.Println("正在读取文件：", filename)
    // file.Close() 会在函数返回时自动调用
}
```

`defer` 的其他常见用途：

- 关闭网络连接、数据库连接
- 解锁互斥锁（`sync.Mutex`）
- 记录函数执行时间、打印进入和离开日志

```go
func process() {
    // defer 追踪函数执行
    defer fmt.Println("process 函数结束")
    fmt.Println("process 开始执行")
}
```

### 4.5.4 参数求值时机

**`defer` 的参数在声明时就已经求值，而非在函数执行时：**

```go
func main() {
    x := 10
    defer fmt.Println("defer 中的 x：", x)   // x 在此时是 10
    x = 20
    fmt.Println("修改后的 x：", x)
}
// 输出：
// 修改后的 x：20
// defer 中的 x：10
```

这个行为是很多初学者的混淆点。如果希望在 `defer` 执行时捕获最新值，应使用闭包：

```go
func main() {
    x := 10
    defer func() {
        fmt.Println("defer 闭包中的 x：", x)   // 引用 x，取最终值
    }()
    x = 20
    fmt.Println("修改后的 x：", x)
}
// 输出：
// 修改后的 x：20
// defer 闭包中的 x：20
```

## 4.6 匿名函数与闭包

### 4.6.1 匿名函数

Go 支持 **匿名函数**——没有函数名的函数字面量，可以直接赋值给变量或立即调用：

```go
func main() {
    // 将匿名函数赋值给变量
    add := func(a, b int) int {
        return a + b
    }
    fmt.Println(add(3, 4))   // 7

    // 定义并立即调用（IIFE 模式）
    result := func(a, b int) int {
        return a * b
    }(3, 4)
    fmt.Println(result)      // 12
}
```

### 4.6.2 闭包

**闭包（closure）** 是一个函数值，它 **捕获并记住了其外部作用域中的变量**，即使该外部函数已经返回：

```go
// 计数器生成器
func counter() func() int {
    count := 0
    return func() int {
        count++               // 捕获外部变量 count
        return count
    }
}

func main() {
    c1 := counter()
    fmt.Println(c1())   // 1
    fmt.Println(c1())   // 2
    fmt.Println(c1())   // 3

    // c2 拥有独立的 count
    c2 := counter()
    fmt.Println(c2())   // 1（c2 的 count 从 0 开始）
}
```

**闭包的核心特性：**

- 闭包捕获的是 **变量的引用**，而非变量的副本
- 每次调用外层函数都会创建新的闭包实例，各自拥有独立的环境
- 闭包的生命周期可能长于外层函数——只要闭包还在使用，被捕获的变量就不会被回收

### 4.6.3 闭包的常见陷阱

循环中捕获循环变量的值是一个经典问题：

```go
func main() {
    var funcs []func()

    for i := 0; i < 3; i++ {
        funcs = append(funcs, func() {
            fmt.Println(i)   // 捕获的是变量 i 的引用，而非当前值
        })
    }

    for _, f := range funcs {
        f()
    }
}
// 输出（Go 1.22 之前）：3 3 3
// 输出（Go 1.22 之后）：0 1 2
```

**说明：** Go 1.22 版本改变了 `for` 循环变量的语义——每次迭代都会创建新的循环变量实例。在 Go 1.22 之前，所有闭包共享同一个循环变量，需要手动创建副本（`i := i`）来避免该问题。

## 4.7 函数作为值和参数

在 Go 中，函数是 **一等公民（first-class citizen）**——函数可以作为值赋值给变量，也可以作为参数传递给其他函数，还可以作为返回值返回。

```go
// 接受一个函数参数
func applyOperation(a, b int, op func(int, int) int) int {
    return op(a, b)
}

func add(a, b int) int { return a + b }
func mul(a, b int) int { return a * b }

func main() {
    fmt.Println(applyOperation(3, 4, add))   // 7
    fmt.Println(applyOperation(3, 4, mul))   // 12
    fmt.Println(applyOperation(3, 4, func(a, b int) int {
        return a - b
    }))                                       // -1（传入匿名函数）
}
```

**函数类型：** 在 Go 中，函数也是一种类型，完整的函数类型签名包括参数类型和返回值类型。

```go
// 定义一个函数类型
type operation func(int, int) int

// 使用自定义函数类型作为参数
func applyOp(a, b int, op operation) int {
    return op(a, b)
}
```

## 4.8 init 函数

`init` 函数是 Go 中一种 **特殊的函数**，由运行时在 `main` 函数之前自动调用：

```go
var dbName string

// init 函数在包初始化时自动执行
func init() {
    dbName = "my_database.db"
    fmt.Println("init 1：数据库名称已设置")
}

// 一个包中可以有多个 init 函数，按照出现顺序执行
func init() {
    fmt.Println("init 2：第二个 init 执行")
}

func main() {
    fmt.Println("main 函数执行，dbName =", dbName)
}
// 输出：
// init 1：数据库名称已设置
// init 2：第二个 init 执行
// main 函数执行，dbName = my_database.db
```

**init 函数的重要规则：**

- `init` 函数 **不接受参数，也不返回任何值**
- `init` 函数由运行时自动调用，**不可显式调用**
- 一个包中可以定义 **多个** `init` 函数，按代码中出现顺序执行
- 不同包的 `init` 函数按 **依赖关系** 确定执行顺序——被导入的包先初始化
- `init` 常用于设置初始状态、注册驱动、解析配置等需要在 `main` 之前完成的操作

```go
import (
    "fmt"
    _ "database/sql"   // 下划线导入：仅执行包的 init，不直接使用包中的导出符号
)
```

**包的初始化顺序：**

1. 导入依赖的包（递归初始化其依赖，再执行该包的初始化）
2. 声明包级别的变量（按声明顺序执行变量初始化表达式）
3. 执行 `init` 函数（按源文件编译顺序）

---

## 4.9 本章小结

- 函数使用 `func` 关键字声明，支持连续参数的类型简写
- 多返回值是 Go 函数的标志性特性，通常将错误作为最后一个返回值
- 命名返回值可以简化 `return` 语句，但裸返回仅在短函数中推荐使用
- 可变参数使用 `...` 操作符，函数内部作为切片处理，必须是参数列表的最后一个参数
- `defer` 延迟执行注册的函数，按 LIFO 顺序执行，最常用于资源释放和锁的解锁
- 匿名函数和闭包允许函数捕获外部变量，每个外层函数调用创建独立的闭包环境
- 函数在 Go 中是一等公民，可以作为值、参数和返回值使用
- `init` 函数在 `main` 之前自动执行，用于包级别的初始化工作

---

## 实践任务

1. 编写一个函数 `swap(a, b int) (int, int)`，利用多返回值交换两个整数，并在 `main` 中调用
2. 编写一个可变参数函数 `average(nums ...float64) float64`，计算任意数量浮点数的平均值
3. 写一个文件操作函数，使用 `defer` 确保文件被关闭（可使用 `os.Create` 创建临时文件）
4. 使用闭包实现斐波那契数列生成器：每次调用返回数列的下一个值
5. 验证 Go 1.22 循环变量语义：在 `for i := 0; i < 5; i++` 中创建 5 个闭包，观察 `i` 的最终值
6. 创建一个包级别变量并通过 `init` 函数初始化它，验证 `init` 在 `main` 之前执行

---

👉 [下一章：第 5 章 · 复合数据类型 →](05-composite-types.md)
👉 [返回教程首页 →](index.md)
