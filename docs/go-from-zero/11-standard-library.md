# 第 11 章：标准库概览

> **标准库概览** —— Go 的标准库提供了丰富的内置包，涵盖 I/O、网络、文本处理、时间操作等核心功能，是构建 Go 程序的基石

---

## 11.1 fmt 包

`fmt` 包实现了格式化 I/O 功能，类似于 C 的 `printf` 和 `scanf`，但类型安全。

### 11.1.1 格式化输出

```go
package main

import "fmt"

type Point struct {
    X, Y int
}

func main() {
    name := "Alice"
    age := 30
    pi := 3.1415926

    // Printf：格式化输出
    fmt.Printf("姓名：%s，年龄：%d\n", name, age)
    fmt.Printf("圆周率：%.2f\n", pi)       // 保留两位小数
    fmt.Printf("类型：%T，值：%v\n", pi, pi) // 输出类型和值

    p := Point{X: 10, Y: 20}

    // %v：默认格式
    fmt.Printf("默认格式：%v\n", p)  // {10 20}

    // %+v：包含字段名
    fmt.Printf("带字段名：%+v\n", p) // {X:10 Y:20}

    // %#v：Go 语法格式
    fmt.Printf("Go 语法：%#v\n", p) // main.Point{X:10, Y:20}
}
```

**常用格式化动词**：

| 动词 | 作用 |
|------|------|
| `%v` | 默认格式 |
| `%+v` | 包含字段名（结构体） |
| `%#v` | Go 语法表示 |
| `%T` | 值类型的 Go 语法表示 |
| `%d` | 十进制整数 |
| `%s` | 字符串 |
| `%f` | 浮点数（含小数部分） |
| `%.Nf` | 保留 N 位小数的浮点数 |
| `%t` | 布尔值（true/false） |
| `%p` | 指针地址 |

### 11.1.2 Stringer 接口

`fmt` 包通过 `Stringer` 接口为自定义类型提供格式化控制：

```go
package main

import "fmt"

// Stringer 定义在 fmt 包中
// type Stringer interface {
//     String() string
// }

// User 用户类型
type User struct {
    Name string
    Age  int
    Role string
}

// String 实现 fmt.Stringer 接口
func (u User) String() string {
    return fmt.Sprintf("用户[%s] - %d 岁, 角色: %s", u.Name, u.Age, u.Role)
}

func main() {
    u := User{Name: "张三", Age: 25, Role: "管理员"}
    fmt.Println(u) // 自动调用 String() 方法
    // 输出：用户[张三] - 25 岁, 角色: 管理员

    fmt.Printf("详细：%#v\n", u) // %#v 不受 Stringer 影响
}
```

### 11.1.3 输入扫描

```go
package main

import "fmt"

func main() {
    var name string
    var age int

    fmt.Print("请输入姓名和年龄：")
    // 从标准输入读取格式化数据
    n, err := fmt.Scanf("%s %d", &name, &age)
    if err != nil {
        fmt.Printf("输入错误：%v\n", err)
        return
    }
    fmt.Printf("成功读取 %d 个字段：姓名=%s, 年龄=%d\n", n, name, age)
}
```

---

## 11.2 io 包

`io` 包提供了 I/O 操作的基本接口和函数，是整个 Go I/O 体系的抽象层。

### 11.2.1 Reader 和 Writer 接口

```go
package main

import (
    "fmt"
    "io"
    "strings"
)

func main() {
    // Reader 接口定义 (io 包)
    // type Reader interface {
    //     Read(p []byte) (n int, err error)
    // }

    // Writer 接口定义
    // type Writer interface {
    //     Write(p []byte) (n int, err error)
    // }

    // strings.NewReader 返回一个实现了 io.Reader 的对象
    reader := strings.NewReader("Hello, Go 标准库!")

    // 创建缓冲区读取数据
    buf := make([]byte, 8) // 每次读取 8 字节
    for {
        n, err := reader.Read(buf)
        if err == io.EOF {
            break // 读取完毕
        }
        if err != nil {
            fmt.Printf("读取错误：%v\n", err)
            break
        }
        fmt.Printf("读取 %d 字节：%s\n", n, buf[:n])
    }
}
```

### 11.2.2 io.Copy

`io.Copy` 从 Reader 读取数据并直接写入 Writer：

```go
package main

import (
    "io"
    "os"
    "strings"
)

func main() {
    // 将字符串读取器中的数据复制到标准输出
    reader := strings.NewReader("这是通过 io.Copy 输出的内容\n")
    _, err := io.Copy(os.Stdout, reader)
    if err != nil {
        os.Stderr.WriteString("复制失败\n")
    }
}
```

### 11.2.3 组合接口

`io` 包通过组合小接口形成更强大的接口：

```go
package main

import (
    "bytes"
    "fmt"
    "io"
)

func main() {
    // io.ReadWriter：同时实现 Reader 和 Writer
    // type ReadWriter interface {
    //     Reader
    //     Writer
    // }

    // bytes.Buffer 实现了 io.ReadWriter
    var buf bytes.Buffer

    // 写入数据
    buf.WriteString("存储数据")

    // 读取数据
    readBuf := make([]byte, 4)
    n, _ := buf.Read(readBuf)
    fmt.Printf("读取：%s\n", readBuf[:n])

    // 通过 io.ReadWriter 接口使用
    var rw io.ReadWriter = &buf
    rw.Write([]byte(" 更多数据"))
    data, _ := io.ReadAll(rw)
    fmt.Printf("剩余数据：%s\n", data)
}
```

### 11.2.4 io.Pipe

`io.Pipe` 创建同步的内存管道，用于将 Writer 和 Reader 连接在一起：

```go
package main

import (
    "fmt"
    "io"
    "time"
)

func main() {
    // 创建管道
    pr, pw := io.Pipe()

    // 写入端 goroutine
    go func() {
        defer pw.Close()
        for i := 1; i <= 3; i++ {
            fmt.Fprintf(pw, "消息 %d\n", i)
            time.Sleep(100 * time.Millisecond)
        }
    }()

    // 读取端
    data, err := io.ReadAll(pr)
    if err != nil {
        fmt.Printf("读取错误：%v\n", err)
        return
    }
    fmt.Printf("接收到：\n%s", data)
}
```

---

## 11.3 os 包

`os` 包提供了操作系统无关的接口，用于文件操作、环境变量访问和进程控制。

### 11.3.1 文件操作

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // ---- 创建文件 ----
    file, err := os.Create("example.txt")
    if err != nil {
        fmt.Printf("创建文件失败：%v\n", err)
        return
    }

    // 写入数据
    content := "Hello, 文件操作!\n"
    _, err = file.WriteString(content)
    if err != nil {
        fmt.Printf("写入文件失败：%v\n", err)
    }
    file.Close()

    // ---- 读取文件 ----
    data, err := os.ReadFile("example.txt")
    if err != nil {
        fmt.Printf("读取文件失败：%v\n", err)
        return
    }
    fmt.Printf("文件内容：%s", data)

    // ---- 文件信息 ----
    info, err := os.Stat("example.txt")
    if err != nil {
        fmt.Printf("获取文件信息失败：%v\n", err)
        return
    }
    fmt.Printf("文件名：%s\n", info.Name())
    fmt.Printf("大小：%d 字节\n", info.Size())
    fmt.Printf("是否目录：%t\n", info.IsDir())
    fmt.Printf("权限：%v\n", info.Mode())

    // ---- 删除文件 ----
    err = os.Remove("example.txt")
    if err != nil {
        fmt.Printf("删除文件失败：%v\n", err)
    }
}
```

### 11.3.2 环境变量

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 获取环境变量
    gopath := os.Getenv("GOPATH")
    fmt.Printf("GOPATH：%s\n", gopath)

    // 获取环境变量（带默认值）
    mode := os.Getenv("APP_MODE")
    if mode == "" {
        mode = "development"
    }
    fmt.Printf("应用模式：%s\n", mode)

    // 设置环境变量
    os.Setenv("MY_APP_SECRET", "my-secret-value")

    // 获取所有环境变量
    for _, env := range os.Environ() {
        fmt.Println(env)
        break // 仅演示，实际使用时去掉 break
    }
}
```

### 11.3.3 命令行参数和进程

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // os.Args 包含命令行参数
    // Args[0] 是程序名
    fmt.Printf("程序名：%s\n", os.Args[0])
    fmt.Printf("参数数量：%d\n", len(os.Args)-1)

    // 遍历所有参数
    for i, arg := range os.Args[1:] {
        fmt.Printf("参数 %d：%s\n", i+1, arg)
    }

    // 退出码
    if len(os.Args) < 2 {
        fmt.Println("请至少提供一个参数")
        os.Exit(1) // 非零退出码表示错误
    }

    // 进程 ID
    fmt.Printf("当前进程 PID：%d\n", os.Getpid())
}
```

---

## 11.4 net/http 包

`net/http` 包提供了 HTTP 客户端和服务端的完整实现。

### 11.4.1 HTTP 服务端

```go
package main

import (
    "fmt"
    "log"
    "net/http"
)

// --- Handler 的三种实现方式 ---

// 方式 1：使用 HandleFunc 注册处理函数
func helloHandler(w http.ResponseWriter, r *http.Request) {
    // w：响应写入器，用于编写 HTTP 响应
    // r：HTTP 请求对象

    // 设置响应头
    w.Header().Set("Content-Type", "text/plain; charset=utf-8")

    // 写入响应体
    fmt.Fprintf(w, "你好，%s！", r.URL.Path)
}

// 自定义 Handler 类型
type greetingHandler struct {
    greeting string
}

// ServeHTTP 实现 http.Handler 接口
func (g *greetingHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "text/plain; charset=utf-8")
    fmt.Fprintf(w, "%s，欢迎访问！", g.greeting)
}

func main() {
    // 注册路由
    http.HandleFunc("/hello", helloHandler)
    http.Handle("/greet", &greetingHandler{greeting: "您好"})

    // 启动 HTTP 服务
    addr := ":8080"
    log.Printf("启动 HTTP 服务：http://localhost%s\n", addr)

    // ListenAndServe 阻塞监听
    err := http.ListenAndServe(addr, nil) // nil 表示使用默认路由器（DefaultServeMux）
    if err != nil {
        log.Fatalf("启动服务失败：%v", err)
    }
}
```

### 11.4.2 HTTP 客户端

```go
package main

import (
    "encoding/json"
    "fmt"
    "io"
    "log"
    "net/http"
    "time"
)

// APIResponse API 响应结构
type APIResponse struct {
    UserID    int    `json:"userId"`
    ID        int    `json:"id"`
    Title     string `json:"title"`
    Completed bool   `json:"completed"`
}

func main() {
    // 创建带超时设置的 HTTP 客户端
    client := &http.Client{
        Timeout: 10 * time.Second,
    }

    // 发起 GET 请求
    resp, err := client.Get("https://jsonplaceholder.typicode.com/todos/1")
    if err != nil {
        log.Fatalf("HTTP 请求失败：%v", err)
    }
    // 必须关闭响应体，否则资源泄漏
    defer resp.Body.Close()

    // 读取响应体
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        log.Fatalf("读取响应失败：%v", err)
    }

    // 解析 JSON 响应
    var todo APIResponse
    err = json.Unmarshal(body, &todo)
    if err != nil {
        log.Fatalf("JSON 解析失败：%v", err)
    }

    fmt.Printf("待办事项：%s (完成状态：%t)\n", todo.Title, todo.Completed)

    // --- POST 请求示例 ---
    // 构造请求体
    payload := map[string]any{
        "title":  "学习 Go 标准库",
        "userId": 1,
    }
    jsonData, _ := json.Marshal(payload)

    // 发送 POST 请求
    resp2, err := client.Post(
        "https://jsonplaceholder.typicode.com/todos",
        "application/json",
        io.NopCloser(bytes.NewReader(jsonData)),
    )
    if err != nil {
        log.Fatalf("POST 请求失败：%v", err)
    }
    defer resp2.Body.Close()

    fmt.Printf("POST 响应状态码：%d\n", resp2.StatusCode)
}

// 需要导入 bytes 包
var _ = bytes.NewReader
```

### 11.4.3 Middleware 模式

Middleware 是包装 http.Handler 的函数，用于在请求处理前后执行横切逻辑：

```go
package main

import (
    "fmt"
    "log"
    "net/http"
    "time"
)

// LoggingMiddleware 日志记录中间件
func LoggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        // 执行下一个 handler
        next.ServeHTTP(w, r)

        // 记录请求日志
        duration := time.Since(start)
        log.Printf("%s %s %v", r.Method, r.URL.Path, duration)
    })
}

// AuthMiddleware 简单认证中间件
func AuthMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if token == "" {
            http.Error(w, "未授权访问", http.StatusUnauthorized)
            return
        }
        next.ServeHTTP(w, r)
    })
}

func mainHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "欢迎访问受保护的资源")
}

func publicHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "这是一个公开接口")
}

func main() {
    mux := http.NewServeMux()

    // 公开路由
    mux.HandleFunc("/public", publicHandler)

    // 受保护路由：应用中间件链
    protected := LoggingMiddleware(AuthMiddleware(http.HandlerFunc(mainHandler)))
    mux.Handle("/protected", protected)

    log.Println("启动服务：:8080")
    http.ListenAndServe(":8080", mux)
}
```

---

## 11.5 encoding/json 包

### 11.5.1 Marshal / Unmarshal

```go
package main

import (
    "encoding/json"
    "fmt"
)

// Product 商品信息
type Product struct {
    ID       int     `json:"id"`                // 字段映射为 id
    Name     string  `json:"name"`              // 字段映射为 name
    Price    float64 `json:"price"`             // 字段映射为 price
    Tags     []string `json:"tags,omitempty"`   // omitempty：为空时忽略
    InStock  bool    `json:"in_stock"`          // 字段映射为 in_stock
    Secret   string  `json:"-"`                 // - 表示该字段不参与 JSON 序列化
}

func main() {
    // ---- 序列化 (Go struct → JSON) ----
    p := Product{
        ID:      1,
        Name:    "Go 语言编程",
        Price:   59.99,
        Tags:    []string{"编程", "Go"},
        InStock: true,
        Secret:  "内部信息",
    }

    jsonData, err := json.Marshal(p)
    if err != nil {
        fmt.Printf("序列化失败：%v\n", err)
        return
    }
    fmt.Printf("JSON：%s\n", jsonData)

    // 格式化输出
    prettyJSON, _ := json.MarshalIndent(p, "", "    ")
    fmt.Printf("格式化 JSON：\n%s\n", prettyJSON)

    // ---- 反序列化 (JSON → Go struct) ----
    input := `{"id":2,"name":"Golang 进阶","price":89.00,"tags":["进阶"],"in_stock":false}`

    var product Product
    err = json.Unmarshal([]byte(input), &product)
    if err != nil {
        fmt.Printf("反序列化失败：%v\n", err)
        return
    }
    fmt.Printf("商品：%+v\n", product)
}
```

### 11.5.2 流式读写

对于大型 JSON 数据，使用 `json.Decoder` 和 `json.Encoder` 进行流式处理：

```go
package main

import (
    "encoding/json"
    "fmt"
    "strings"
)

func main() {
    // 流式解码
    jsonStream := `{"name": "A"}{"name": "B"}{"name": "C"}`
    decoder := json.NewDecoder(strings.NewReader(jsonStream))

    for {
        var item map[string]string
        err := decoder.Decode(&item)
        if err != nil {
            break // 通常是 io.EOF
        }
        fmt.Printf("解码：%v\n", item)
    }
}
```

---

## 11.6 time 包

### 11.6.1 时间和 Duration

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // ---- 获取当前时间 ----
    now := time.Now()
    fmt.Printf("当前时间：%v\n", now)

    // ---- 创建时间 ----
    specific := time.Date(2024, time.January, 15, 10, 30, 0, 0, time.UTC)
    fmt.Printf("指定时间：%v\n", specific)

    // ---- 时间格式化和解析 ----
    // Go 的参考时间：Mon Jan 2 15:04:05 MST 2006
    // 格式字符串必须基于这个参考时间
    const layout = "2006-01-02 15:04:05"
    formatted := now.Format(layout)
    fmt.Printf("格式化：%s\n", formatted)

    // 解析字符串为时间
    parsed, err := time.Parse(layout, "2024-06-01 12:00:00")
    if err != nil {
        fmt.Printf("解析失败：%v\n", err)
    } else {
        fmt.Printf("解析结果：%v\n", parsed)
    }

    // ---- Duration ----
    duration := 2 * time.Hour + 30 * time.Minute + 15 * time.Second
    fmt.Printf("持续时长：%v\n", duration)
    fmt.Printf("分钟数：%.1f\n", duration.Minutes())
    fmt.Printf("秒数：%d\n", int(duration.Seconds()))

    // ---- 时间计算 ----
    future := now.Add(7 * 24 * time.Hour) // 7 天后
    fmt.Printf("7 天后：%v\n", future)

    diff := future.Sub(now)
    fmt.Printf("时间差：%v\n", diff)

    // 时间比较
    if now.Before(future) {
        fmt.Println("现在在将来之前")
    }
}
```

### 11.6.2 Ticker 和 Timer

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // ---- Timer：一次性定时器 ----
    timer := time.NewTimer(2 * time.Second)

    fmt.Println("等待 2 秒...")
    <-timer.C
    fmt.Println("定时器触发！")

    // ---- Ticker：周期性定时器 ----
    ticker := time.NewTicker(500 * time.Millisecond)

    // 启动一个 goroutine 读取 ticker 信号
    go func() {
        for t := range ticker.C {
            fmt.Println("Tick 时间：", t.Format("15:04:05.000"))
        }
    }()

    // 主 goroutine 等待 2 秒后停止 ticker
    time.Sleep(2 * time.Second)
    ticker.Stop()
    fmt.Println("Ticker 已停止")
    time.Sleep(500 * time.Millisecond) // 等待 ticker 协程结束
}
```

---

## 11.7 strings 和 strconv 包

### 11.7.1 strings 包

```go
package main

import (
    "fmt"
    "strings"
)

func main() {
    s := "  Hello, Go 语言世界!  "

    // 基本操作
    fmt.Println(strings.TrimSpace(s))      // 去除两端空白
    fmt.Println(strings.ToUpper(s))         // 转大写
    fmt.Println(strings.ToLower(s))         // 转小写
    fmt.Println(strings.Repeat("Go ", 3))   // 重复字符串
    fmt.Println(strings.Replace(s, "Go", "Golang", 1)) // 替换一次

    // 判断和查找
    fmt.Println(strings.Contains(s, "Go"))     // 是否包含子串
    fmt.Println(strings.HasPrefix(s, "  He"))  // 是否以前缀开头
    fmt.Println(strings.HasSuffix(s, "!  "))   // 是否以后缀结尾
    fmt.Println(strings.Index(s, "Go"))        // 子串位置（-1 表示未找到）

    // 分割和连接
    parts := strings.Split("a,b,c", ",")
    fmt.Printf("分割结果：%v\n", parts)
    fmt.Println(strings.Join(parts, "|"))      // 连接为 "a|b|c"

    // Builder：高效字符串拼接
    var builder strings.Builder
    builder.WriteString("Hello")
    builder.WriteString(" ")
    builder.WriteString("World")
    fmt.Println(builder.String()) // Hello World
}
```

### 11.7.2 strconv 包

```go
package main

import (
    "fmt"
    "strconv"
)

func main() {
    // ---- 字符串转基本类型 ----
    // string → int
    i, err := strconv.Atoi("42")
    if err != nil {
        fmt.Printf("转换失败：%v\n", err)
    } else {
        fmt.Printf("int：%d (类型：%T)\n", i, i)
    }

    // string → float64
    f, err := strconv.ParseFloat("3.14", 64)
    if err == nil {
        fmt.Printf("float64：%f\n", f)
    }

    // string → bool
    b, err := strconv.ParseBool("true")
    if err == nil {
        fmt.Printf("bool：%t\n", b)
    }

    // ---- 基本类型转字符串 ----
    s1 := strconv.Itoa(100)
    fmt.Printf("字符串：%s\n", s1)

    s2 := strconv.FormatFloat(3.14159, 'f', 2, 64)
    fmt.Printf("格式化的浮点数字符串：%s\n", s2)

    s3 := strconv.FormatBool(true)
    fmt.Printf("布尔字符串：%s\n", s3)

    // ---- 带进制转换的 ParseInt ----
    // 将十六进制字符串转为十进制整数
    hex, _ := strconv.ParseInt("FF", 16, 0)
    fmt.Printf("十六进制 FF = %d\n", hex)
}
```

---

## 11.8 sort 包

```go
package main

import (
    "fmt"
    "sort"
)

// Person 用于排序的示例结构体
type Person struct {
    Name string
    Age  int
}

// 实现 sort.Interface 以便自定义排序
// type Interface interface {
//     Len() int
//     Less(i, j int) bool
//     Swap(i, j int)
// }

// ByAge 按年龄排序的类型
type ByAge []Person

func (a ByAge) Len() int           { return len(a) }
func (a ByAge) Less(i, j int) bool { return a[i].Age < a[j].Age }
func (a ByAge) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }

func main() {
    // ---- 基本类型排序 ----
    nums := []int{42, 13, 7, 99, 25, 3}
    sort.Ints(nums)
    fmt.Println("排序后：", nums)

    // 降序排序
    sort.Sort(sort.Reverse(sort.IntSlice(nums)))
    fmt.Println("降序：", nums)

    // 字符串排序
    strs := []string{"banana", "apple", "cherry"}
    sort.Strings(strs)
    fmt.Println("字符串排序：", strs)

    // ---- 自定义排序 ----
    people := []Person{
        {"张三", 30},
        {"李四", 25},
        {"王五", 35},
    }

    // 使用 sort.Slice（推荐方式，无需实现接口）
    sort.Slice(people, func(i, j int) bool {
        return people[i].Age < people[j].Age
    })
    fmt.Println("按年龄排序：", people)

    // 也可使用 sort.Sort 配合接口实现
    sort.Sort(ByAge(people))
    fmt.Println("ByAge 排序：", people)

    // ---- 查找 ----
    // 二分查找（需要在有序切片上使用）
    sortedNums := []int{1, 3, 5, 7, 9, 11}
    index := sort.SearchInts(sortedNums, 7)
    fmt.Printf("数字 7 的位置：%d\n", index)

    // 自定义二分查找
    i := sort.Search(len(sortedNums), func(i int) bool {
        return sortedNums[i] >= 8
    })
    fmt.Printf("第一个 >= 8 的元素位置：%d\n", i)
}
```

---

## 11.9 log 包

### 11.9.1 标准日志

```go
package main

import (
    "log"
    "os"
)

func main() {
    // ---- 基本日志 ----
    log.Println("这是一条信息级别的日志")
    log.Printf("格式化日志：值=%d\n", 42)

    // ---- 日志前缀和标志 ----
    log.SetPrefix("[MyApp] ")
    log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
    log.Println("带前缀和行号的日志")

    // ---- 输出到文件 ----
    file, err := os.OpenFile("app.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
    if err != nil {
        log.Fatal("无法创建日志文件")
    }
    defer file.Close()

    logger := log.New(file, "[FileLogger] ", log.LstdFlags|log.Lshortfile)
    logger.Println("这条日志写入到文件中")

    // ---- Fatal 和 Panic ----
    // log.Fatal("致命错误")    // 打印日志并调用 os.Exit(1)
    // log.Panic("触发 panic")  // 打印日志并触发 panic
}
```

### 11.9.2 结构化日志 (log/slog)

Go 1.21 引入了 `log/slog` 包，提供结构化日志支持：

```go
package main

import (
    "log/slog"
    "os"
)

func main() {
    // 默认的文本格式日志
    slog.Info("服务启动", "port", 8080, "env", "production")
    slog.Warn("磁盘空间不足", "free", "1.2GB")
    slog.Error("数据库连接失败", "error", "timeout")

    // JSON 格式日志
    jsonLogger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
    jsonLogger.Info("JSON 格式日志", "user", "Alice", "action", "login")
}
```

---

## 11.10 flag 包

`flag` 包提供了命令行参数解析功能：

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    // 定义命令行参数
    // flag.Type(name, defaultValue, usage)
    host := flag.String("host", "localhost", "服务器主机名")
    port := flag.Int("port", 8080, "服务器端口")
    debug := flag.Bool("debug", false, "是否开启调试模式")
    name := flag.String("name", "", "用户名（必填）")

    // 自定义参数用法说明
    flag.Usage = func() {
        fmt.Fprintf(os.Stderr, "用法：%s [选项]\n", os.Args[0])
        flag.PrintDefaults()
    }

    // 解析命令行参数
    flag.Parse()

    // 使用解析后的值
    fmt.Printf("主机：%s\n", *host)
    fmt.Printf("端口：%d\n", *port)
    fmt.Printf("调试模式：%t\n", *debug)

    // 获取非选项参数
    fmt.Printf("其他参数：%v\n", flag.Args())

    // 运行示例：
    // go run main.go -host=example.com -port=9090 -debug=true -name=test extra1 extra2
}
```

---

## 11.11 本章小结

- `fmt` 包提供格式化的 I/O 操作，`Stringer` 接口控制自定义类型的输出格式
- `io.Reader` 和 `io.Writer` 是 Go I/O 体系的基石，通过接口组合实现灵活性
- `os` 包封装了操作系统调用，提供文件、环境变量和进程管理
- `net/http` 支持完整的 HTTP 服务端和客户端，Handler 接口是构建 Web 应用的核心
- `encoding/json` 提供了 JSON 序列化和反序列化，struct tag 控制映射行为
- `time` 包中的参考时间格式 `2006-01-02 15:04:05` 是 Go 特有的设计
- `strings` 和 `strconv` 覆盖了大部分字符串处理和类型转换需求
- `sort` 包通过接口抽象实现了灵活的自定义排序
- `log/slog` 提供了现代化的结构化日志
- `flag` 包用于解析命令行参数，是构建 CLI 工具的起点

---

## 实践任务

1. 使用 `net/http` 编写一个简单的 HTTP 服务器，提供 `/time` 和 `/echo` 两个端点，分别返回当前时间和回显请求参数
2. 使用 `encoding/json` 编写一个函数，将任意结构体序列化为缩进格式的 JSON 字符串，并处理嵌套结构
3. 创建一个 CLI 工具（使用 `flag` 包），支持 `-file` 和 `-count` 参数，读取指定文件并统计其中的行数
4. 使用 `log/slog` 替换程序中的标准 `log` 包输出，将结构化日志写入文件

---

👉 [下一章：第 12 章 · 综合实战 →](12-final-project.md)
👉 [返回教程首页 →](index.md)
