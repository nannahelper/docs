# 第 7 章：指针与内存

> **指针与内存** —— 指针存储变量的内存地址，是 Go 中实现引用语义和高效数据操作的基础。理解内存分配机制对编写高质量 Go 程序至关重要。

---

## 7.1 指针基础

指针是一个变量，其值是另一个变量的内存地址。通过指针可以间接读写目标变量的值。

### 7.1.1 & 和 * 操作符

```go
package main

import "fmt"

func main() {
    x := 42

    // &：取地址操作符，返回变量的内存地址
    p := &x
    fmt.Printf("x 的值: %d\n", x)
    fmt.Printf("x 的地址: %p\n", p)

    // *：解引用操作符，通过地址访问变量的值
    fmt.Printf("通过指针读取值: %d\n", *p)

    // 通过指针修改值
    *p = 100
    fmt.Printf("通过指针修改后 x 的值: %d\n", x) // 100
}
```

### 7.1.2 指针的类型

指针的类型为 `*T`，其中 `T` 是指向的目标类型。

```go
package main

import "fmt"

func main() {
    var p1 *int     // 指向 int 的指针
    var p2 *string  // 指向 string 的指针
    var p3 *float64 // 指向 float64 的指针

    a := 10
    b := "hello"
    c := 3.14

    p1 = &a
    p2 = &b
    p3 = &c

    fmt.Printf("%T, %T, %T\n", p1, p2, p3) // *int, *string, *float64
}
```

### 7.1.3 指针的零值

指针的零值是 `nil`，表示不指向任何有效的内存地址。

```go
package main

import "fmt"

func main() {
    var p *int
    fmt.Println(p)       // nil
    fmt.Printf("%T\n", p) // *int

    // 解引用 nil 指针会导致 panic
    if p != nil {
        fmt.Println(*p)
    } else {
        fmt.Println("指针为 nil，不能解引用")
    }
}
```

> **安全准则**：解引用指针前 **必须** 检查是否为 nil。

---

## 7.2 值传递与指针传递

Go 的函数参数传递方式为 **值传递**（pass by value），这意味着函数总是接收实参的副本。使用指针可以在函数内部修改外部变量。

### 7.2.1 值传递

```go
package main

import "fmt"

// 值传递：参数是原始值的副本
func incrementValue(x int) {
    x++ // 修改的是副本，不影响原变量
}

func main() {
    a := 10
    incrementValue(a)
    fmt.Println(a) // 10 —— 未改变
}
```

### 7.2.2 指针传递

```go
package main

import "fmt"

// 指针传递：可以通过指针修改原始变量
func incrementPointer(p *int) {
    *p++ // 通过指针修改原变量
}

func main() {
    a := 10
    incrementPointer(&a)
    fmt.Println(a) // 11 —— 已改变
}
```

### 7.2.3 内存语义对比

| 传递方式 | 实现机制 | 能否修改原值 | 内存开销 |
|---------|---------|-------------|---------|
| 值传递 | 复制整个值 | 否 | 复制开销（大结构体开销大） |
| 指针传递 | 复制地址（8 字节） | 是 | 固定 8 字节开销 |

```go
package main

import "fmt"

type LargeStruct struct {
    Data [1024]int
}

// 值传递：完整复制结构体（4096 字节复制）
func processByValue(ls LargeStruct) {
    _ = ls
}

// 指针传递：仅复制地址（8 字节）
func processByPointer(ls *LargeStruct) {
    _ = ls
}

func main() {
    obj := LargeStruct{}
    processByValue(obj)     // 复制整个数组
    processByPointer(&obj)  // 仅复制指针
    fmt.Println("无需传递大型结构体的副本时，应使用指针")
}
```

---

## 7.3 new 函数

`new` 是 Go 的内置函数，用于分配内存。它接受一个类型作为参数，分配足够容纳该类型值的零值内存，并返回指向该内存的指针。

```go
package main

import "fmt"

func main() {
    // new(int) 分配 int 类型的零值内存，返回 *int
    p := new(int)
    fmt.Printf("类型: %T\n", p) // *int
    fmt.Printf("值: %d\n", *p) // 0 （零值）

    *p = 42
    fmt.Printf("赋值后: %d\n", *p) // 42

    // 等价于以下写法
    var x int
    q := &x
    fmt.Println(p, q) // 语义等价，但 p 更简洁
}
```

---

## 7.4 make 函数

`make` 用于初始化 slice、map 和 channel 三种引用类型。与 `new` 不同，`make` **返回的是初始化后的值本身**（而非指针）。

```go
package main

import "fmt"

func main() {
    // make 初始化切片：指定长度和容量
    s := make([]int, 3, 5)
    fmt.Printf("切片: %v, len=%d, cap=%d\n", s, len(s), cap(s))

    // make 初始化映射
    m := make(map[string]int)
    m["key"] = 100
    fmt.Println(m)

    // make 初始化通道
    ch := make(chan int, 2)
    ch <- 1
    ch <- 2
    fmt.Println(<-ch)
    fmt.Println(<-ch)
}
```

> `make` 之所以不返回指针，是因为 slice、map、channel 本身就是引用类型，内部已经包含指向底层数据结构的指针。

---

## 7.5 new 与 make 的区别

这是 Go 初学者最容易混淆的概念之一。以下是两者的全面对比。

### 7.5.1 对比表格

| 维度 | `new` | `make` |
|------|-------|--------|
| 适用类型 | 任意类型 | 仅 slice、map、channel |
| 返回值 | `*T`（指向零值的指针） | `T`（初始化后的值） |
| 内存初始化 | 置为零值 | 分配并初始化内部数据结构 |
| 调用后状态 | `*p` 为零值，可直接赋值 | 切片/映射/通道可直接使用 |

### 7.5.2 代码演示

```go
package main

import "fmt"

func main() {
    // === new 的使用 ===
    p := new(int)        // *int，指向零值 0
    fmt.Println(*p)      // 0

    // === make 的使用 ===
    s := make([]int, 3)  // []int，零值切片，可直接使用
    s[0] = 10
    fmt.Println(s)       // [10 0 0]

    // === 错误示范：用 new 创建切片 ===
    sp := new([]int)     // *[]int，指针指向 nil 切片
    fmt.Println(*sp)     // nil
    // (*sp)[0] = 1      // panic：解引用 nil 切片

    // === 错误示范：用 make 创建 int ===
    // x := make(int)    // 编译错误：make 不能用于非引用类型

    // === 本质区别总结 ===
    // new(T)  ≈  var zero T; return &zero
    // make(T) ≈  allocate and initialize internal representation of T
}
```

> **记忆方法**：`new` 零值指针，`make` 引用初始化。

---

## 7.6 指针与结构体方法

指针接收者方法与指针类型密切相关。当通过指针调用方法时，Go 会自动解引用。

```go
package main

import "fmt"

type Counter struct {
    value int
}

// 值接收者：不能修改原值
func (c Counter) Value() int {
    return c.value
}

// 指针接收者：可以修改原值
func (c *Counter) Increment() {
    c.value++
}

// 指针接收者：可以修改原值
func (c *Counter) Reset() {
    c.value = 0
}

func main() {
    // 通过值调用
    c1 := Counter{value: 10}
    c1.Increment() // Go 自动取地址 (&c1).Increment()
    fmt.Println(c1.Value()) // 11

    // 通过指针调用
    c2 := &Counter{value: 20}
    c2.Increment()
    fmt.Println(c2.Value()) // 21

    // 方法集（method set）规则
    var p *Counter = &Counter{}
    // p.Increment()  // 合法：指针变量可以调用指针接收者方法
    // p.Value()      // 合法：指针变量也可以调用值接收者方法

    // var v Counter = Counter{}
    // v.Increment()  // 合法：值变量可以调用指针接收者方法（Go 自动取地址）
    // v.Value()      // 合法：值变量可以调用值接收者方法
}
```

### 6.2 节已经详细讨论了接收者选择准则，上述代码从指针的角度进行了补充说明。

---

## 7.7 逃逸分析简介

逃逸分析（escape analysis）是 Go 编译器在编译阶段进行的优化分析，用于确定变量应该分配在栈（stack）上还是堆（heap）上。

### 7.7.1 栈与堆

| 分配位置 | 特点 |
|---------|------|
| 栈 | 函数返回后自动回收，分配/回收速度快 |
| 堆 | 由垃圾回收器（GC）管理，分配和回收开销较大 |

### 7.7.2 逃逸的典型场景

```go
package main

import "fmt"

// 场景 1：返回局部变量的指针 —— 变量逃逸到堆
func createInt() *int {
    x := 42
    return &x // x 不能留在栈上，必须逃逸到堆
}

// 场景 2：将指针传递给外部函数
func escapeExample() {
    data := make([]int, 100) // 当切片容量较大时，可能在堆上分配
    fmt.Println(data)        // fmt 包的函数接收 interface{}，可能引起逃逸
}

// 场景 3：接口类型的方法调用
type Speaker interface {
    Say() string
}

type Person struct {
    Name string
}

func (p Person) Say() string {
    return p.Name
}

func main() {
    // 调用 createInt 时，x 逃逸到堆
    p := createInt()
    println(*p) // 避免使用 fmt 减少干扰

    // 接口类型的方法调用通常导致逃逸
    var s Speaker = Person{Name: "Alice"}
    _ = s
}
```

### 7.7.3 逃逸分析的意义

- **性能优化**：尽量让对象分配在栈上，减少 GC 压力。
- **编译器透明**：逃逸分析由编译器自动完成，开发者无需手动管理内存。
- **观察方法**：使用 `go build -gcflags="-m"` 查看逃逸分析结果。

```bash
go build -gcflags="-m" main.go
```

> 虽然 Go 通过逃逸分析自动决定分配位置，但了解其机制有助于编写性能敏感的代码。

---

## 7.8 本章小结

- **指针** 存储变量的内存地址，`&` 取地址，`*` 解引用。指针的零值是 `nil`。
- **值传递** 复制整个值，**指针传递** 仅复制地址（固定 8 字节），后者可修改原值。
- **`new(T)`** 为任意类型分配零值内存，返回 `*T`。
- **`make(T)`** 仅用于 slice、map、channel，返回初始化后的值。
- `new` 返回指针，`make` 返回引用类型本身，这是两者的核心区别。
- **指针接收者方法** 可以修改结构体字段，Go 自动处理取地址和解引用。
- **逃逸分析** 是编译器优化，决定变量分配在栈还是堆上，对性能有重要影响。

---

## 实践任务

1. 实现 `swap` 函数，使用指针交换两个整数的值。验证调用后原变量的确被交换。

2. 编写 `double` 函数，接收 `*int` 指针，将其指向的值翻倍。写一个程序：从切片中取每个元素的地址，验证通过指针修改的效果。

3. （性能观察）创建一个包含 10000 个 `int` 的大型结构体，分别编写值接收者和指针接收者的方法，在实际代码中体会指针节省复制开销的意义。在可用环境下运行 `go build -gcflags="-m"` 观察逃逸分析输出。

---

👉 [下一章：第 8 章 · 包与模块 →](08-packages-and-modules.md)
👉 [返回教程首页 →](index.md)
