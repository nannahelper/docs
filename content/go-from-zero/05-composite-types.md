# 第 5 章：复合类型

> **复合类型** —— 由基本类型组合而成的更高阶数据类型，包括数组、切片、映射、结构体等，是 Go 语言组织数据的核心工具。

---

## 5.1 数组

数组是 Go 中最基础的复合类型，它是一个 **固定长度**、元素类型相同的数据序列。

### 5.1.1 声明与初始化

数组类型由 `[n]T` 表示，其中 `n` 是长度（编译期常量），`T` 是元素类型。

```go
package main

import "fmt"

func main() {
    // 方式一：声明后默认零值初始化
    var arr1 [3]int
    fmt.Println(arr1) // [0 0 0]

    // 方式二：字面量初始化
    arr2 := [3]int{1, 2, 3}
    fmt.Println(arr2) // [1 2 3]

    // 方式三：由初始化元素数量推断长度
    arr3 := [...]int{10, 20, 30, 40}
    fmt.Println(arr3) // [10 20 30 40]

    // 方式四：指定索引初始化
    arr4 := [5]int{0: 100, 3: 200}
    fmt.Println(arr4) // [100 0 0 200 0]
}
```

### 5.1.2 数组是值类型

数组在 Go 中是 **值类型** 而非引用类型。将数组赋值给另一个变量或传递给函数时，会复制整个数组。

```go
package main

import "fmt"

func modifyArray(a [3]int) {
    a[0] = 999 // 修改的是副本，不影响原数组
}

func main() {
    original := [3]int{1, 2, 3}
    copyArr := original // 完全复制
    copyArr[0] = 100

    fmt.Println(original) // [1 2 3]，原数组不受影响
    fmt.Println(copyArr)  // [100 2 3]

    modifyArray(original)
    fmt.Println(original) // [1 2 3]，函数内修改不影响
}
```

> **重要**：由于数组是值类型，当数组元素较多时，复制会产生较大的性能开销。因此实际开发中更常用切片（slice）。

---

## 5.2 切片

切片（slice）是 Go 中最重要的复合类型之一，它是对底层数组的一个 **动态视图**。

### 5.2.1 声明与创建

```go
package main

import "fmt"

func main() {
    // 方式一：直接创建切片字面量
    s1 := []int{1, 2, 3, 4, 5}
    fmt.Println(s1)

    // 方式二：从数组切片
    arr := [5]int{10, 20, 30, 40, 50}
    s2 := arr[1:4] // 左闭右开区间 [1, 4)
    fmt.Println(s2) // [20 30 40]

    // 方式三：使用 make 创建
    s3 := make([]int, 3)     // len = 3, cap = 3
    s4 := make([]int, 3, 5)  // len = 3, cap = 5
    fmt.Println(s3, s4)
}
```

### 5.2.2 长度与容量

切片有两个核心属性：**长度（len）** 表示切片当前包含的元素个数，**容量（cap）** 表示从切片起始位置到底层数组末尾的元素个数。

```go
package main

import "fmt"

func main() {
    arr := [10]int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    s := arr[3:7] // 元素 [3, 7)，即 [3 4 5 6]

    fmt.Printf("len=%d, cap=%d\n", len(s), cap(s)) // len=4, cap=7
    // 容量为 7，因为底层数组从索引 3 到末尾共 7 个元素

    // 重新切片可以扩大范围（但不可超过 cap）
    s2 := s[:5]
    fmt.Println(s2) // [3 4 5 6 7]
}
```

### 5.2.3 append 与扩容

`append` 是向切片追加元素的内置函数。当切片容量不足时，Go 会自动分配一个新的底层数组并复制原有元素（即 **扩容**）。

```go
package main

import "fmt"

func main() {
    s := make([]int, 0, 2)
    fmt.Printf("初始: len=%d, cap=%d\n", len(s), cap(s))

    s = append(s, 10)
    s = append(s, 20)
    fmt.Printf("追加两次后: len=%d, cap=%d\n", len(s), cap(s))

    // 第三次追加：容量不足，触发扩容
    s = append(s, 30)
    fmt.Printf("三次追加后: len=%d, cap=%d, 元素=%v\n", len(s), cap(s), s)
}
```

> 扩容策略：当原容量小于 256 时，大致按 2 倍扩容；当原容量大于等于 256 时，按约 1.25 倍扩容。

### 5.2.4 copy

`copy` 用于将源切片的元素复制到目标切片中。复制的元素数量是 `len(src)` 与 `len(dst)` 中的较小值。

```go
package main

import "fmt"

func main() {
    src := []int{1, 2, 3, 4, 5}
    dst := make([]int, 3)

    n := copy(dst, src) // 复制 3 个元素
    fmt.Printf("复制了 %d 个元素\n", n)
    fmt.Println(dst) // [1 2 3]

    // 切片重叠复制也是安全的
    copy(src[2:], src[:3]) // 将前 3 个元素移动到索引 2 开始的位置
    fmt.Println(src)       // [1 2 1 2 3]
}
```

---

## 5.3 切片底层原理

切片在运行时由一个结构体表示，通常称为 **slice header**：

```go
type SliceHeader struct {
    Data unsafe.Pointer // 指向底层数组的指针
    Len  int            // 当前长度
    Cap  int            // 最大容量
}
```

### 5.3.1 切片共享底层数组

多个切片可以共享同一个底层数组，修改一个切片的元素会影响其他共享该底层数组的切片。

```go
package main

import "fmt"

func main() {
    arr := [5]int{1, 2, 3, 4, 5}
    s1 := arr[0:3] // [1, 2, 3]
    s2 := arr[1:4] // [2, 3, 4]

    s1[2] = 999 // 修改底层数组索引 2 的元素
    fmt.Println(s2) // [2, 999, 4]  —— s2 也受影响
}
```

### 5.3.2 扩容机制详解

当 `append` 导致容量不足时，Go 的运行时函数 `growslice` 执行以下步骤：

1. 计算新容量（按上述扩容策略）
2. 分配新的底层数组
3. 将旧元素逐字节复制到新数组
4. 返回指向新数组的新切片

扩容后，新切片与旧切片 **不再共享同一底层数组**。

```go
package main

import "fmt"

func main() {
    s1 := []int{1, 2, 3}
    s2 := s1

    s1 = append(s1, 4) // 扩容，s1 指向新数组
    s1[0] = 999

    fmt.Println(s2) // [1 2 3] —— s2 仍指向旧数组，不受影响
}
```

---

## 5.4 映射

映射（map）是键值对的无序集合，键类型必须是可比较的（即支持 `==` 操作）。

### 5.4.1 创建与基本操作

```go
package main

import "fmt"

func main() {
    // 方式一：使用 make
    scores := make(map[string]int)

    // 方式二：字面量
    ages := map[string]int{
        "Alice": 30,
        "Bob":   25,
    }

    // 增/改
    scores["Math"] = 95
    scores["English"] = 88
    scores["Math"] = 97 // 覆盖

    // 查
    fmt.Println(scores["Math"]) // 97

    // 删
    delete(scores, "English")
    fmt.Println(scores) // map[Math:97]

    // 检查键是否存在
    value, ok := scores["Physics"]
    if !ok {
        fmt.Println("Physics not found") // 输出此行
    } else {
        fmt.Println(value)
    }
}
```

### 5.4.2 遍历与注意事项

```go
package main

import "fmt"

func main() {
    scores := map[string]int{
        "Math":    95,
        "English": 88,
        "Physics": 92,
    }

    // for range 遍历，顺序不保证
    for key, value := range scores {
        fmt.Printf("%s: %d\n", key, value)
    }

    // 仅遍历键
    for key := range scores {
        fmt.Println(key)
    }
}
```

> **注意**：map 的遍历顺序是随机的。Go 语言特意引入了随机性，防止开发者依赖特定遍历顺序。

---

## 5.5 结构体

结构体（struct）是多个任意类型字段的集合，用于定义复合数据结构。

### 5.5.1 定义与实例化

```go
package main

import "fmt"

// 定义结构体类型
type Student struct {
    Name  string
    Age   int
    Score float64
}

func main() {
    // 方式一：按顺序初始化（不推荐，易出错）
    s1 := Student{"Alice", 20, 95.5}

    // 方式二：指定字段名（推荐）
    s2 := Student{
        Name:  "Bob",
        Age:   21,
        Score: 88.0,
    }

    // 方式三：声明后逐字段赋值
    var s3 Student
    s3.Name = "Charlie"
    s3.Age = 19
    s3.Score = 92.5

    // 方式四：部分字段初始化（未指定字段为零值）
    s4 := Student{Name: "David"}

    fmt.Println(s1, s2, s3, s4)
}
```

### 5.5.2 结构体是值类型

```go
package main

import "fmt"

type Point struct {
    X, Y int
}

func movePoint(p Point, dx, dy int) {
    p.X += dx // 修改的是副本
    p.Y += dy
}

func main() {
    p := Point{1, 2}
    movePoint(p, 10, 10)
    fmt.Println(p) // {1 2} —— 原结构体未被修改
}
```

### 5.5.3 匿名字段与嵌套

```go
package main

import "fmt"

// 嵌套结构体
type Address struct {
    City    string
    Street  string
    ZipCode string
}

type Person struct {
    Name    string
    Age     int
    Address Address // 具名字段嵌套
}

// 匿名字段（字段只有类型，没有名字）
type Animal struct {
    Name string
    Age  int
}

type Dog struct {
    Animal          // 匿名字段，类型名为字段名
    Breed string
}

func main() {
    // 嵌套结构体初始化
    p := Person{
        Name: "Alice",
        Age:  30,
        Address: Address{
            City:    "Beijing",
            Street:  "Haidian",
            ZipCode: "100000",
        },
    }
    fmt.Println(p)

    // 匿名字段：可以"提升"访问
    d := Dog{
        Animal: Animal{Name: "Buddy", Age: 3},
        Breed:  "Golden Retriever",
    }
    fmt.Println(d.Name) // 直接访问提升的字段
    fmt.Println(d.Breed)
}
```

---

## 5.6 make 与 new 初步对比

Go 提供了两个内置内存分配函数 `make` 和 `new`，其用途有本质区别。

| 特性 | `make` | `new` |
|------|--------|-------|
| 适用类型 | slice, map, channel | 任意类型 |
| 返回值 | 初始化后的引用类型本身（非指针） | 指向类型零值的指针 |
| 初始化行为 | 分配并初始化内部数据结构 | 分配内存并置为零值 |

```go
package main

import "fmt"

func main() {
    // make: 返回初始化后的值（非指针）
    s := make([]int, 3)  // 返回 []int
    m := make(map[string]int) // 返回 map[string]int

    // new: 返回指针
    p := new(int)   // 返回 *int
    *p = 42

    fmt.Println(s, m, *p)
}
```

> 第 7 章将深入对比 `make` 与 `new` 的内存语义。

---

## 5.7 for range 遍历复合类型

`for range` 可以遍历数组、切片、映射和字符串等复合类型。

```go
package main

import "fmt"

func main() {
    // 遍历数组/切片
    nums := []int{10, 20, 30}
    for i, v := range nums {
        fmt.Printf("索引 %d: %d\n", i, v)
    }

    // 仅使用值，忽略索引
    for _, v := range nums {
        fmt.Println(v)
    }

    // 遍历 map
    scores := map[string]int{"A": 95, "B": 88}
    for key, val := range scores {
        fmt.Printf("%s -> %d\n", key, val)
    }

    // 遍历字符串（按 rune 而非字节）
    for i, r := range "Go语言" {
        fmt.Printf("位置 %d: %c (U+%04X)\n", i, r, r)
    }
}
```

---

## 5.8 本章小结

- **数组** 是固定长度、元素类型一致的值类型序列，赋值或传参时复制整个数组。
- **切片** 是对底层数组的动态视图，包含指针、长度、容量三要素，是 Go 中最常用的序列类型。
- 切片通过 **append** 自动扩容，扩容后可能分配新底层数组并切断与原数组的共享关系。
- **映射（map）** 是键值对集合，遍历顺序不保证，使用 `delete` 删除元素，通过双值赋值检查键是否存在。
- **结构体（struct）** 将多个字段聚合成一个类型，支持匿名字段和嵌套，也是值类型。
- `make` 用于初始化 slice/map/channel，`new` 返回指向零值的指针。
- `for range` 可遍历数组、切片、映射和字符串，注意字符串按 rune 遍历。

---

## 实践任务

1. 编写一个函数，接收整数切片并返回去重后的切片。尝试分别用 map 和双重循环两种方式实现，并对比代码简洁性。

2. 定义一个 `Book` 结构体（字段：Title, Author, Price），创建一个包含 3 本书的切片。编写函数按价格排序（提示：可结合切片与结构体操作）。

3. 实现一个简易的单词计数程序：接收一段英文文本（字符串），返回每个单词出现的次数。要求忽略大小写和标点符号。

---

👉 [下一章：第 6 章 · 方法与接口 →](06-methods-and-interfaces.md)
👉 [返回教程首页 →](index.md)
