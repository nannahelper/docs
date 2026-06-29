# 第 6 章：方法与接口

> **方法与接口** —— 方法为类型添加行为，接口定义类型的契约。Go 通过隐式实现（duck typing）使接口成为其类型系统的核心抽象机制。

---

## 6.1 方法

Go 中的方法（method）是附加在特定类型上的函数。方法定义中显式声明 **接收者（receiver）** 参数，表明该方法属于哪个类型。

### 6.1.1 基本语法

```go
package main

import "fmt"

// 定义一个结构体
type Rectangle struct {
    Width  float64
    Height float64
}

// 方法：接收者为 Rectangle 类型
func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

// 方法：计算周长
func (r Rectangle) Perimeter() float64 {
    return 2 * (r.Width + r.Height)
}

func main() {
    rect := Rectangle{Width: 10, Height: 5}
    fmt.Printf("面积: %.2f\n", rect.Area())      // 面积: 50.00
    fmt.Printf("周长: %.2f\n", rect.Perimeter())  // 周长: 30.00
}
```

### 6.1.2 可以为任意类型定义方法

方法可以定义在任意自定义类型上，不仅限于结构体。

```go
package main

import "fmt"

// 基于基本类型定义新类型
type Celsius float64
type Fahrenheit float64

func (c Celsius) ToFahrenheit() Fahrenheit {
    return Fahrenheit(c*9/5 + 32)
}

func (f Fahrenheit) ToCelsius() Celsius {
    return Celsius((f - 32) * 5 / 9)
}

func main() {
    c := Celsius(100)
    fmt.Printf("%.1f°C = %.1f°F\n", c, c.ToFahrenheit())

    f := Fahrenheit(212)
    fmt.Printf("%.1f°F = %.1f°C\n", f, f.ToCelsius())
}
```

---

## 6.2 值接收者与指针接收者

方法可以使用 **值接收者** 或 **指针接收者**，两者的行为语义有本质区别。

### 6.2.1 值接收者

值接收者对接收者的 **副本** 进行操作，不会影响原值。

```go
type Counter struct {
    Value int
}

func (c Counter) Increment() {
    c.Value++ // 修改的是副本，不影响原结构体
}

func main() {
    c := Counter{Value: 0}
    c.Increment()
    fmt.Println(c.Value) // 0 —— 未改变
}
```

### 6.2.2 指针接收者

指针接收者可以直接修改接收者的值。

```go
type Counter struct {
    Value int
}

func (c *Counter) Increment() {
    c.Value++ // 通过指针直接修改原结构体
}

func main() {
    c := Counter{Value: 0}
    c.Increment()
    fmt.Println(c.Value) // 1 —— 已改变
}
```

### 6.2.3 选择准则

| 场景 | 推荐接收者类型 |
|------|--------------|
| 方法内需要修改接收者 | 指针接收者 |
| 接收者是大型结构体（避免复制开销） | 指针接收者 |
| 接收者是 map/slice/函数等引用类型 | 值接收者 |
| 接收者是小型基本类型或结构体 | 值接收者 |
| 需要接收者不可变（语义明确） | 值接收者 |

**一致性原则**：如果一个类型有多个方法，应保持接收者类型一致。通常，若任一方法需要指针接收者，则所有方法都使用指针接收者。

```go
package main

import "fmt"

type User struct {
    Name  string
    Email string
}

// 指针接收者：修改字段
func (u *User) UpdateEmail(newEmail string) {
    u.Email = newEmail
}

// 指针接收者：虽然不修改，但保持与 UpdateEmail 一致
func (u *User) Display() string {
    return fmt.Sprintf("%s <%s>", u.Name, u.Email)
}

func main() {
    u := User{Name: "Alice", Email: "alice@old.com"}
    u.UpdateEmail("alice@new.com")
    fmt.Println(u.Display()) // Alice <alice@new.com>
}
```

---

## 6.3 接口

接口（interface）定义了一组方法签名，任何实现了这些方法的类型都自动满足该接口。

### 6.3.1 接口定义与隐式实现

Go 的接口采用 **隐式实现**（也称结构类型化或 duck typing），无需显式声明 `implements` 关键字。

```go
package main

import "fmt"

// 定义接口
type Shape interface {
    Area() float64
    Perimeter() float64
}

// 实现类型 1：Rectangle
type Rectangle struct {
    Width, Height float64
}

func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

func (r Rectangle) Perimeter() float64 {
    return 2 * (r.Width + r.Height)
}

// 实现类型 2：Circle
type Circle struct {
    Radius float64
}

func (c Circle) Area() float64 {
    return 3.14159 * c.Radius * c.Radius
}

func (c Circle) Perimeter() float64 {
    return 2 * 3.14159 * c.Radius
}

// 接受接口类型参数的函数
func printShapeInfo(s Shape) {
    fmt.Printf("面积: %.2f, 周长: %.2f\n", s.Area(), s.Perimeter())
}

func main() {
    r := Rectangle{Width: 10, Height: 5}
    c := Circle{Radius: 7}

    // Rectangle 和 Circle 都隐式实现了 Shape 接口
    printShapeInfo(r)
    printShapeInfo(c)
}
```

### 6.3.2 接口值

接口值由两个部分组成：**具体类型的指针** 和 **该类型值的指针**（或数据）。可以将接口值理解为（type, value）对。

```go
package main

import "fmt"

type Speaker interface {
    Speak() string
}

type Dog struct{}

func (d Dog) Speak() string {
    return "Woof!"
}

type Cat struct{}

func (c Cat) Speak() string {
    return "Meow!"
}

func main() {
    var s Speaker

    s = Dog{}
    fmt.Printf("(%T, %v)\n", s, s) // (main.Dog, {})

    s = Cat{}
    fmt.Printf("(%T, %v)\n", s, s) // (main.Cat, {})

    // 接口的零值是 nil
    var nilSpeaker Speaker
    fmt.Printf("nil 接口: (%T, %v)\n", nilSpeaker, nilSpeaker)
}
```

---

## 6.4 空接口

空接口 `interface{}` 不包含任何方法签名，因此 **任意类型** 都实现了空接口。

```go
package main

import "fmt"

func describe(v interface{}) {
    fmt.Printf("值: %v, 类型: %T\n", v, v)
}

func main() {
    describe(42)           // 值: 42, 类型: int
    describe("hello")      // 值: hello, 类型: string
    describe(3.14)         // 值: 3.14, 类型: float64
    describe([]int{1, 2})  // 值: [1 2], 类型: []int

    // 空接口可以存储任意类型的值
    var any interface{}
    any = 100
    any = "text"
    any = map[string]int{"a": 1}
    _ = any
}
```

> Go 1.18 引入了泛型，一定程度上减少了对空接口的依赖，但空接口在处理未知类型时仍广泛使用。

---

## 6.5 类型断言

类型断言用于提取接口值中底层具体类型的值。

### 6.5.1 基本语法

```go
package main

import "fmt"

func main() {
    var v interface{} = "hello"

    // 单返回值形式：若断言失败则 panic
    s := v.(string)
    fmt.Println(s) // hello

    // 双返回值形式：若断言失败返回零值且 ok = false（推荐）
    s, ok := v.(string)
    if ok {
        fmt.Println("字符串:", s)
    }

    n, ok := v.(int)
    if !ok {
        fmt.Printf("类型断言失败: 期望 int, 实际 %T\n", v)
    }
}
```

### 6.5.2 type switch

当需要针对接口值的多种可能类型分别处理时，使用 type switch 更为清晰。

```go
package main

import "fmt"

func classify(v interface{}) {
    switch v.(type) {
    case int:
        fmt.Println("整数类型")
    case string:
        fmt.Println("字符串类型")
    case bool:
        fmt.Println("布尔类型")
    case []int:
        fmt.Println("整数切片")
    default:
        fmt.Printf("未知类型: %T\n", v)
    }
}

func main() {
    classify(42)
    classify("hello")
    classify(true)
    classify([]int{1, 2, 3})
    classify(3.14)
}
```

---

## 6.6 常用标准接口

Go 标准库定义了大量接口，以下是四个最常用的例子。

### 6.6.1 fmt.Stringer

任何实现了 `String()` 方法的类型都可以自定义其在 `fmt.Print` 等函数中的输出格式。

```go
package main

import "fmt"

type Point struct {
    X, Y int
}

func (p Point) String() string {
    return fmt.Sprintf("(%d, %d)", p.X, p.Y)
}

func main() {
    p := Point{3, 4}
    fmt.Println(p) // (3, 4) —— 使用了自定义 String 方法
}
```

### 6.6.2 error 接口

`error` 是 Go 内置接口，是 Go 语言处理错误的标准方式。

```go
type error interface {
    Error() string
}
```

```go
package main

import (
    "errors"
    "fmt"
)

// 自定义错误类型
type ValidationError struct {
    Field string
    Value interface{}
}

func (e ValidationError) Error() string {
    return fmt.Sprintf("字段 %s 的值 %v 无效", e.Field, e.Value)
}

func validateAge(age int) error {
    if age < 0 || age > 150 {
        return ValidationError{Field: "age", Value: age}
    }
    return nil // nil 表示无错误
}

func main() {
    err := validateAge(200)
    if err != nil {
        fmt.Println(err) // 字段 age 的值 200 无效
    }

    // 使用标准库创建错误
    err2 := errors.New("发生了一个错误")
    _ = err2
}
```

### 6.6.3 io.Reader 与 io.Writer

`io.Reader` 和 `io.Writer` 是 Go I/O 操作的两大核心接口。

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}
```

```go
package main

import (
    "fmt"
    "io"
    "strings"
)

func main() {
    // strings.NewReader 返回实现了 io.Reader 的类型
    reader := strings.NewReader("Hello, Go!")

    buf := make([]byte, 5)
    for {
        n, err := reader.Read(buf)
        if err == io.EOF {
            break // 读取完毕
        }
        fmt.Printf("读取 %d 字节: %s\n", n, buf[:n])
    }
}
```

---

## 6.7 接口组合

Go 接口支持 **嵌入（embedding）**，可以将多个接口组合成新的接口。

```go
package main

import (
    "fmt"
    "io"
)

// 定义一个 Writer 接口（与 io.Writer 类似，仅为演示）
type Writer interface {
    Write(p []byte) (n int, err error)
}

// 定义一个 Closer 接口
type Closer interface {
    Close() error
}

// 接口组合：组合 Writer 和 Closer
type WriteCloser interface {
    Writer
    Closer
}

// 模拟实现
type File struct{}

func (f File) Write(p []byte) (n int, err error) {
    fmt.Println("写入数据:", string(p))
    return len(p), nil
}

func (f File) Close() error {
    fmt.Println("关闭文件")
    return nil
}

func main() {
    var wc WriteCloser = File{}

    // WriteCloser 拥有 Writer 和 Closer 的所有方法
    wc.Write([]byte("data"))
    wc.Close()

    // 标准库中的典型例子
    var _ io.ReadWriter // 组合了 io.Reader 和 io.Writer
}
```

---

## 6.8 本章小结

- **方法** 是附加在特定类型上的函数，通过接收者参数定义。
- **值接收者** 操作副本，**指针接收者** 可修改原值。选择时需考虑修改需求、结构体大小和一致性。
- **接口** 定义了一组方法签名，Go 采用 **隐式实现**，无需显式声明。
- **空接口** `interface{}` 可接收任意类型的值，但使用时需配合类型断言恢复具体类型。
- **类型断言** `x.(T)` 提取接口中的具体值，type switch 可处理多种可能的类型。
- 标准库提供了 `fmt.Stringer`、`error`、`io.Reader`、`io.Writer` 等常用接口。
- 接口可通过 **嵌入** 组合，形成更强大的抽象。

---

## 实践任务

1. 定义 `Shape3D` 接口（包含 `Volume()` 和 `SurfaceArea()` 方法），然后为 `Sphere` 和 `Cube` 类型实现该接口。

2. 实现一个日志系统：定义 `Logger` 接口（包含 `Log(message string)` 方法），分别用写入文件（模拟）和写入控制台两种方式实现。编写函数 `ProcessWithLogger(logger Logger)` 来测试。

3. 编写函数 `PrintAny(v interface{})`，使用 type switch 处理 `int`、`string`、`float64`、`bool` 和 `[]int` 五种类型，为每种类型提供不同的输出格式。

---

👉 [下一章：第 7 章 · 指针与内存 →](07-pointers-and-memory.md)
👉 [返回教程首页 →](index.md)
