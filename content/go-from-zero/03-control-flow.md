# 第 3 章：控制流程

> **决定程序的执行路径** —— 掌握 Go 的条件判断、循环、分支跳转等控制结构。

---

## 3.1 if/else 条件语句

### 3.1.1 基本形式

Go 的 `if` 语句与 C 系语言类似，但有两个重要区别：

1. **条件表达式不需要括号 `()`**
2. **代码块必须紧跟花括号 `{}`，且左花括号与 `if` 在同一行**

```go
package main

import "fmt"

func main() {
    score := 85

    if score >= 90 {
        fmt.Println("优秀")
    } else if score >= 60 {
        fmt.Println("及格")
    } else {
        fmt.Println("不及格")
    }
}
```

### 3.1.2 带简短语句的 if

Go 允许在 `if` 条件之前执行一个简短语句，该语句声明的变量仅在 `if-else` 块内可见：

```go
func main() {
    // 在 if 条件前执行赋值语句
    if score := 85; score >= 60 {
        fmt.Println("及格，分数：", score)
    } else {
        fmt.Println("不及格，分数：", score)  // else 块中也能访问 score
    }
    // 此处 score 已超出作用域，无法访问
}
```

这是 Go 中非常常见的惯用法，特别适合在执行条件判断前先获取某个计算结果或函数返回值：

```go
if err := doSomething(); err != nil {
    fmt.Println("出错了：", err)
    return
}
```

**作用域规则：** 在 `if` 的简短语句中声明的变量，其作用域延伸到整个 `if-else` 块末尾。这一设计减少了变量的作用域范围，符合最小作用域原则。

## 3.2 for 循环

Go **只有一种循环结构**：`for`。但它可以以三种不同形式出现，覆盖了其他语言中 `for`、`while`、`do-while` 的全部功能。

### 3.2.1 经典 for 循环（C 风格）

```go
func main() {
    // 初始化语句; 条件表达式; 后置语句
    for i := 0; i < 5; i++ {
        fmt.Println("i =", i)
    }
}
```

三个部分：
- **初始化语句**：`i := 0`，在第一次迭代前执行（作用域仅限 for 块内）
- **条件表达式**：`i < 5`，每次迭代前计算，结果为 `false` 时退出
- **后置语句**：`i++`，每次迭代结束后执行

### 3.2.2 while 风格

省略初始化语句和后置语句，仅保留条件表达式，等价于其他语言的 `while`：

```go
func main() {
    sum := 0
    for sum < 100 {     // 相当于 while sum < 100
        sum += 10
    }
    fmt.Println(sum)    // 100
}
```

### 3.2.3 无限循环

省略条件表达式，形成无限循环：

```go
func main() {
    count := 0
    for {               // 无限循环，直到遇到 break 或 return
        count++
        if count >= 3 {
            break
        }
    }
    fmt.Println(count)  // 3
}
```

**适用场景：** 服务器监听循环、事件轮询等需要持续运行的程序。

## 3.3 for range 遍历

`for range` 是 Go 中遍历 **数组、切片、映射（map）、字符串** 的专用语法：

```go
func main() {
    // 遍历切片（slice）
    nums := []int{10, 20, 30}
    for index, value := range nums {
        fmt.Printf("nums[%d] = %d\n", index, value)
    }

    // 遍历字符串（按 rune 字符遍历，而非按字节）
    s := "Go 语言"
    for i, r := range s {
        fmt.Printf("s[%d] = %c (rune: %U)\n", i, r, r)
    }

    // 遍历映射（map）
    scores := map[string]int{"Alice": 95, "Bob": 87}
    for name, score := range scores {
        fmt.Printf("%s: %d\n", name, score)
    }
}
```

**range 的返回值：**

| 遍历对象 | 第一个返回值 | 第二个返回值 |
|----------|-------------|-------------|
| 数组/切片 | 索引（int） | 对应元素的值 |
| 字符串 | 字节索引（int） | rune 字符 |
| 映射（map） | 键（key） | 值（value） |
| 通道（channel） | 收到的值 | 无 |

使用 `_` 忽略不需要的返回值：

```go
func main() {
    nums := []int{10, 20, 30}

    // 忽略索引，只取值
    for _, v := range nums {
        fmt.Println(v)
    }

    // 忽略值，只取索引
    for i := range nums {   // 省略第二个变量等于是只取索引
        fmt.Println(i)
    }
}
```

**关于字符串 range 的重要细节：** `for range` 遍历字符串时是以 **rune** 为单位迭代的，而非以字节为单位。这意味着对于包含中文等 Unicode 字符的字符串，range 循环会正确识别每个字符，而直接使用 `s[i]` 索引访问得到的是原始字节。

## 3.4 switch 语句

Go 的 `switch` 与 C 系语言有显著不同，设计上更加灵活简洁。

### 3.4.1 基本 switch

```go
func main() {
    day := 3

    switch day {
    case 1:
        fmt.Println("星期一")
    case 2:
        fmt.Println("星期二")
    case 3:
        fmt.Println("星期三")
    case 4, 5:      // case 可匹配多个值，用逗号分隔
        fmt.Println("星期四或星期五")
    default:
        fmt.Println("周末")
    }
}
```

**关键区别：** Go 的 `case` 在匹配后 **自动 break**，不会向下穿透（fall through）。如需继续匹配，须显式使用 `fallthrough` 关键字。

### 3.4.2 无表达式的 switch

`switch` 后可以不跟表达式，此时每个 `case` 是一个布尔条件——等价于 `if-else if-else` 链，但可读性更好：

```go
func main() {
    score := 85

    switch {
    case score >= 90:
        fmt.Println("优秀")
    case score >= 80:
        fmt.Println("良好")
    case score >= 60:
        fmt.Println("及格")
    default:
        fmt.Println("不及格")
    }
}
```

### 3.4.3 fallthrough

Golang 中，使用 `fallthrough` 强制进入下一个 `case` 块（不匹配下一个 case 的条件，直接执行其代码体）：

```go
func main() {
    num := 1
    switch num {
    case 1:
        fmt.Println("one")
        fallthrough
    case 2:
        fmt.Println("two")   // 即使 num 是 1，也会执行
        fallthrough
    default:
        fmt.Println("default")
    }
    // 输出：one two default
}
```

**注意：** `fallthrough` 仅强制执行紧邻的下一个 `case`，不会继续穿透更多层。

## 3.5 break 与 continue

### 3.5.1 基本用法

- `break`：立即退出当前循环
- `continue`：跳过当前迭代的剩余语句，进入下一次迭代

```go
func main() {
    for i := 0; i < 10; i++ {
        if i == 3 {
            continue    // 跳过 i=3，不打印
        }
        if i == 7 {
            break       // 到达 i=7 时退出循环
        }
        fmt.Println(i)  // 输出：0,1,2,4,5,6
    }
}
```

### 3.5.2 标签（label）与跳出多层循环

Go 支持给循环语句加 **标签（label）**，`break` 和 `continue` 可以通过标签指定跳出或继续哪一层循环：

```go
func main() {
outer:                              // 标签定义
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 && j == 1 {
                break outer         // 跳出 outer 标记的外层循环
            }
            fmt.Printf("(%d,%d) ", i, j)
        }
    }
    // 输出：(0,0) (0,1) (0,2) (1,0)
}
```

```go
func main() {
outer:
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 && j == 1 {
                continue outer      // 继续 outer 标记的下一轮外层循环
            }
            fmt.Printf("(%d,%d) ", i, j)
        }
    }
    // 输出：(0,0) (0,1) (0,2) (1,0) (2,0) (2,1) (2,2)
}
```

**标签命名规范：** Go 中标签通常使用小写字母，且与使用它的循环语句相邻。标签的作用域是整个函数的词法块——即使标签定义在深层嵌套之外，也必须在其所在函数的范围内。

## 3.6 goto 语句

Go 支持 `goto`，但应谨慎使用，通常只在前向跳转到清理代码或错误处理时采用：

```go
func main() {
    i := 0

loopStart:           // 标签
    if i >= 3 {
        goto end     // 跳转到 end 标签处
    }
    fmt.Println(i)
    i++
    goto loopStart   // 跳转回 loopStart

end:                 // 结束标签
    fmt.Println("done")
}
// 输出：0 1 2 done
```

**使用限制：**

- `goto` 不能跳转到其他函数内部
- `goto` 不能跳过变量声明语句（即不能跳入一个变量尚未声明的区域）
- `goto` 不能跳入 `for`、`switch`、`select` 等代码块的内部

在实际项目中，`goto` 的使用场景非常有限。现代 Go 代码中，结构化编程（if/for/switch）几乎能够覆盖所有控制流程需求。

---

## 3.7 本章小结

- `if/else` 支持在条件前执行简短语句（如 `if score := calc(); score > 60`），声明的变量仅在条件块内可见
- Go 只有 `for` 一种循环结构，但能以经典形式、while 风格和无限循环三种方式使用
- `for range` 用于遍历数组、切片、映射和字符串；遍历字符串时以 rune 为单位
- `switch` 中每个 `case` 默认自动 break，不会穿透；多个匹配值用逗号分隔；支持无表达式 switch
- `break` 和 `continue` 配合标签（label）可以跳出或继续多层循环
- `goto` 在 Go 中受严格限制，应谨慎使用

---

## 实践任务

1. 编写一个程序，用 `for` 循环输出 1 到 100 之间的所有偶数（使用 `continue` 跳过奇数）
2. 使用带简短语句的 `if` 判断一个变量的绝对值：声明 `x := -5`，在同一行计算其绝对值并输出
3. 使用 `for range` 遍历一个字符串 `"Hello, 世界"`，分别输出每个字符的字节偏移量和该字符（rune）
4. 使用 `switch` 无表达式形式，将百分制分数（95、82、67、43）映射为 "优秀""良好""及格""不及格" 四个等级
5. 编写嵌套循环，使用标签在满足条件时跳出外层循环；将标签名改为 `myLabel` 并尝试在多层循环中使用

---

👉 [下一章：第 4 章 · 函数 →](04-functions.md)
👉 [返回教程首页 →](index.md)
