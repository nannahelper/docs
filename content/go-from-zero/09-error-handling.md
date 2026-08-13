# 第 9 章：错误处理

> **严谨的错误处理** —— Go 通过显式的 error 返回值来强制开发者处理异常情况，而非依赖隐式的异常抛出机制

---

## 9.1 Go 的错误处理哲学

Go 语言在错误处理上采用了一条与众不同的路径：**错误是值（error as a value）**。函数通过返回 `error` 类型的值来报告异常，调用方有责任检查并处理这个值。这一设计哲学基于以下考量：

- **显式优于隐式**：错误路径在代码中明确可见，不会像 try-catch 那样隐藏控制流
- **强制处理**：忽略错误需要显式地使用 `_`，编译器不会自动吞没异常
- **可组合性**：error 是一个接口，可以自由扩展和包装

这与 Java/C++/Python 的异常机制形成鲜明对比。后者通过栈展开（stack unwinding）传递异常，调用方可能在不经意间遗漏处理。

> **对比**：在 Java 中，被检查异常（checked exception）虽然在方法签名中声明，但异常的实际抛出点和处理点可能相隔多个调用层级，导致中间函数被迫声明异常。Go 的方法是将错误直接作为返回值的一部分，让每个调用层级都能自主决定如何处理。

---

## 9.2 error 接口

### 9.2.1 接口定义

`error` 是 Go 预定义的接口类型，位于 `builtin` 包中：

```go
// builtin.go
type error interface {
    Error() string
}
```

任何实现了 `Error() string` 方法的类型都可以作为错误值使用。这是 Go 中为数不多的预定义接口之一，编译器对其有特殊识别。

### 9.2.2 基本用法

函数通过返回 `error` 来指示失败。按照惯例，`error` 总是返回值列表中的最后一个：

```go
package main

import (
    "fmt"
    "os"
)

// 打开一个文件并读取其内容
func readFile(path string) (string, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        // 将错误返回给调用方
        return "", err
    }
    return string(data), nil
}

func main() {
    content, err := readFile("non_existent.txt")
    if err != nil {
        // 处理错误：打印并退出
        fmt.Println("读取文件失败:", err)
        os.Exit(1)
    }
    fmt.Println(content)
}
```

关键约定：

- 成功时返回 `nil` 作为 error 值
- 失败时返回非 `nil` 的 error 值
- `error` 总是返回参数列表的最后一个
- 调用方必须先检查 error，再使用其他返回值

---

## 9.3 创建错误

### 9.3.1 errors.New

标准库 `errors` 包提供了 `New` 函数，用于创建包含固定文本的错误：

```go
package main

import (
    "errors"
    "fmt"
)

// 根据年龄判断是否成年
func checkAge(age int) error {
    if age < 0 {
        // 创建一个新的错误值
        return errors.New("年龄不能为负数")
    }
    if age < 18 {
        return errors.New("未满 18 岁")
    }
    return nil
}

func main() {
    err := checkAge(-5)
    if err != nil {
        fmt.Println("检查失败:", err)
    }

    err = checkAge(20)
    if err != nil {
        fmt.Println("检查失败:", err)
    } else {
        fmt.Println"检查通过")
out: fmt.Println("检查通过")
    }
}
```

### 9.3.2 fmt.Errorf

`fmt.Errorf` 提供了格式化错误文本的能力，支持 `%s`、`%d` 等格式化动词：

```go
package main

import (
    "fmt"
)

// 除法函数，处理除零错误
func divide(a, b int) (int, error) {
    if b == 0 {
        // 使用格式化创建包含上下文信息的错误
        return 0, fmt.Errorf("除法错误：除数不能为零 (被除数=%d)", a)
    }
    return a / b, nil
}

func main() {
    _, err := divide(10, 0)
    if err != nil {
        fmt.Println(err)
        // 输出：除法错误：除数不能为零 (被除数=10)
    }
}
```

---

## 9.4 错误包装（Error Wrapping）

### 9.4.1 问题背景

在实际项目中，错误往往需要沿调用链向上传播，同时保留原始的上下文信息。简单的做法是直接返回错误，但这样丢失了调用链的信息。将原始错误文本拼接到新字符串中虽然可以携带信息，却破坏了错误的结构化性质，使得调用方无法通过类型判断来区分错误种类。

### 9.4.2 %w 动词

Go 1.13 引入了错误包装机制。`fmt.Errorf` 的 `%w` 动词可以将一个错误 **包装** 到新的错误中：

```go
package main

import (
    "errors"
    "fmt"
    "os"
)

var ErrNotFound = errors.New("文件未找到")

// 尝试读取配置文件
func readConfig(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        // 将原始错误包装到新的上下文中
        return nil, fmt.Errorf("读取配置失败：%w", err)
    }
    return data, nil
}

func loadApp() error {
    config, err := readConfig("/app/config.yaml")
    if err != nil {
        // 进一步包装，形成错误链
        return fmt.Errorf("加载应用失败：%w", err)
    }
    _ = config
    return nil
}

func main() {
    err := loadApp()
    if err != nil {
        fmt.Println(err)
        // 输出：加载应用失败：读取配置失败：open /app/config.yaml: The system cannot find the file specified.
    }
}
```

`%w` 与 `%v` 的区别：

- `%w`：将错误包装，保留错误链，可供 `errors.Is` / `errors.As` 遍历
- `%v`：仅格式化文本，不保留错误链，原始错误信息丢失

### 9.4.3 errors.Is 和 errors.As

**errors.Is**：判断错误链中是否存在与目标匹配的错误（按值比较）：

```go
package main

import (
    "errors"
    "fmt"
    "os"
)

var ErrPermission = errors.New("权限不足")
var ErrDiskFull = errors.New("磁盘空间不足")

// 写入文件
func writeFile(path string, data []byte) error {
    // 模拟写入失败
    return fmt.Errorf("写入失败：%w", ErrDiskFull)
}

func main() {
    err := writeFile("/data/log.txt", []byte("hello"))

    // 使用 errors.Is 判断错误链中是否包含指定错误
    if errors.Is(err, ErrDiskFull) {
        fmt.Println("需要清理磁盘空间")
    }

    if errors.Is(err, ErrPermission) {
        fmt.Println("需要检查文件权限")
    }

    // 也适用于系统错误
    _, err = os.Open("no_such_file.txt")
    if errors.Is(err, os.ErrNotExist) {
        fmt.Println("文件不存在")
    }
}
```

**errors.As**：将错误链中的某个错误转换为特定类型（按类型匹配）：

```go
package main

import (
    "errors"
    "fmt"
    "net"
)

// 自定义错误类型
type NetworkError struct {
    Code    int
    Message string
    Source  string
}

func (e *NetworkError) Error() string {
    return fmt.Sprintf("[%d] %s (来源：%s)", e.Code, e.Message, e.Source)
}

// 执行网络请求
func fetchData(url string) error {
    return fmt.Errorf("请求失败：%w", &NetworkError{
        Code:    503,
        Message: "服务暂时不可用",
        Source:  "gateway.example.com",
    })
}

func main() {
    err := fetchData("https://api.example.com/data")

    var netErr *NetworkError
    // errors.As 会将错误链中匹配类型的值赋给 netErr
    if errors.As(err, &netErr) {
        fmt.Printf("网络错误代码：%d\n", netErr.Code)
        fmt.Printf("错误消息：%s\n", netErr.Message)
        fmt.Printf("来源：%s\n", netErr.Source)
    }

    // 也可以用于系统错误类型
    _, err = net.Dial("tcp", "192.0.2.1:80")
    var dnsErr *net.DNSError
    if errors.As(err, &dnsErr) {
        fmt.Printf("DNS 解析失败，名称：%s\n", dnsErr.Name)
    }
}
```

`errors.Is` 和 `errors.As` 都会遍历整个错误链，因此无论错误被包装了多少层，都能正确匹配。

---

## 9.5 panic 和 recover

### 9.5.1 panic

`panic` 是 Go 中的内建函数，用于触发运行时恐慌。当 `panic` 被调用时，函数会立即停止执行，开始执行延迟函数（defer），然后向上返回，直到程序崩溃。

**使用场景**：`panic` 仅应用于不可恢复的错误，例如：

- 程序初始化失败（无法绑定端口、无法连接数据库）
- 状态不一致（switch 的 default 分支理论上不应到达）
- 显式编程错误（nil 解引用、数组越界）

```go
package main

import "fmt"

// 只有在程序初始化阶段才应该使用 panic
func mustInit() {
    // 模拟一个必须成功的初始化操作
    initialized := false
    if !initialized {
        panic("初始化失败：系统无法继续运行")
    }
}

func main() {
    fmt.Println("程序启动")

    // 正常代码中不应使用 panic
    // mustInit()  // 取消注释会触发 panic

    fmt.Println("程序正常结束")
}
```

**不应使用 panic 的场景**：

- 用户输入验证失败（应返回 error）
- 网络请求超时（应返回 error）
- 文件不存在（应返回 error）

### 9.5.2 defer + recover

`recover` 是内建函数，用于捕获 `panic` 并将程序恢复为正常执行状态。`recover` 仅在 `defer` 调用的函数中有用。

```go
package main

import (
    "fmt"
)

// 安全的除法：捕获可能的 panic
func safeDivide(a, b int) (result int, err error) {
    // defer 中调用 recover 捕获 panic
    defer func() {
        if r := recover(); r != nil {
            // 将 panic 转换为 error 返回
            err = fmt.Errorf("panic 恢复：%v", r)
        }
    }()

    if b == 0 {
        // 这里应该用 error 而非 panic，此处仅为演示 recover
        panic("除数为零")
    }

    return a / b, nil
}

func main() {
    // 演示 recover 如何捕获 panic
    result, err := safeDivide(10, 0)
    if err != nil {
        fmt.Println("捕获到错误：", err)
    } else {
        fmt.Println("结果：", result)
    }

    fmt.Println("程序继续执行...")
}
```

**recover 的正确使用模式**：

1. `defer` 的匿名函数中调用 `recover`
2. 将 `panic` 恢复为 `error` 返回给调用方
3. 仅在 goroutine 的顶层使用，不要在普通函数中使用

### 9.5.3 典型场景：goroutine 中的 panic 保护

每个 goroutine 都应该有自己的 panic 保护机制，否则一个 goroutine 的 panic 会导致整个程序崩溃：

```go
package main

import (
    "fmt"
    "time"
)

// 在 goroutine 中执行任务，并捕获可能的 panic
func doTask(id int) {
    defer func() {
        if r := recover(); r != nil {
            fmt.Printf("任务 %d 发生 panic 并已恢复：%v\n", id, r)
        }
    }()

    // 模拟一个可能触发 panic 的操作
    if id == 3 {
        panic("任务 3 发生致命错误")
    }
    fmt.Printf("任务 %d 执行完毕\n", id)
}

func main() {
    for i := 1; i <= 5; i++ {
        go doTask(i)
    }

    // 等待 goroutine 执行完毕
    time.Sleep(time.Second)
    fmt.Println("主程序正常结束")
}
```

> **关键原则**：`panic` 和 `recover` 在 Go 中并不等同于其他语言的 try-catch。`panic-recover` 应该仅在极少数场景中使用，常规错误处理始终应该通过 error 返回值来完成。

---

## 9.6 自定义错误类型

### 9.6.1 实现 error 接口

通过实现 `Error() string` 方法，可以创建携带额外上下文信息的错误类型：

```go
package main

import (
    "fmt"
)

// ValidationError 自定义验证错误类型
type ValidationError struct {
    Field   string // 出错的字段名
    Value   any    // 导致错误的字段值
    Message string // 错误描述
}

// Error 实现 error 接口
func (e *ValidationError) Error() string {
    return fmt.Sprintf("字段 '%s' 验证失败：%s (当前值：%v)",
        e.Field, e.Message, e.Value)
}

// 验证用户年龄
func validateUserAge(age int) error {
    if age < 0 {
        return &ValidationError{
            Field:   "age",
            Value:   age,
            Message: "年龄不能为负数",
        }
    }
    if age > 150 {
        return &ValidationError{
            Field:   "age",
            Value:   age,
            Message: "年龄超出合理范围",
        }
    }
    return nil
}

func main() {
    err := validateUserAge(-5)
    if err != nil {
        // 调用 Error() 方法
        fmt.Println(err)
        // 输出：字段 'age' 验证失败：年龄不能为负数 (当前值：-5)
    }

    // 通过 errors.As 提取自定义错误类型
    var valErr *ValidationError
    if errors.As(err, &valErr) {
        fmt.Printf("字段名：%s\n", valErr.Field)
        fmt.Printf("当前值：%v\n", valErr.Value)
    }
}
```

### 9.6.2 带错误码的错误类型

在 API 服务中，通常需要包含错误码以便客户端进行程序化处理：

```go
package main

import (
    "errors"
    "fmt"
)

// ErrorCode 业务错误码
type ErrorCode int

const (
    ErrCodeNotFound    ErrorCode = 1001
    ErrCodePermission  ErrorCode = 1002
    ErrCodeValidation  ErrorCode = 1003
    ErrCodeRateLimit   ErrorCode = 1004
)

// AppError 应用级错误
type AppError struct {
    Code    ErrorCode // 错误码
    Message string    // 人类可读的消息
    Err     error     // 原始错误（可选）
}

// Error 实现 error 接口
func (e *AppError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("[%d] %s (原因：%v)", e.Code, e.Message, e.Err)
    }
    return fmt.Sprintf("[%d] %s", e.Code, e.Message)
}

// Unwrap 返回被包装的错误，使 errors.Is/As 可以遍历
func (e *AppError) Unwrap() error {
    return e.Err
}

// NewAppError 创建应用级错误
func NewAppError(code ErrorCode, msg string, err error) *AppError {
    return &AppError{Code: code, Message: msg, Err: err}
}

// 从数据库获取用户
func getUserFromDB(id int) (string, error) {
    // 模拟数据库查询失败
    return "", errors.New("记录不存在")
}

// 获取用户信息的业务逻辑
func GetUser(id int) (string, error) {
    user, err := getUserFromDB(id)
    if err != nil {
        return "", NewAppError(ErrCodeNotFound, "用户未找到", err)
    }
    return user, nil
}

func main() {
    _, err := GetUser(999)
    if err != nil {
        var appErr *AppError
        if errors.As(err, &appErr) {
            fmt.Printf("错误码：%d\n", appErr.Code)
            fmt.Printf("消息：%s\n", appErr.Message)

            // 根据错误码分支处理
            switch appErr.Code {
            case ErrCodeNotFound:
                fmt.Println("执行：返回 404 状态码")
            case ErrCodePermission:
                fmt.Println("执行：返回 403 状态码")
            }
        }
    }
}
```

---

## 9.7 最佳实践

### 9.7.1 不要忽略错误

```go
// 错误做法：忽略错误
// io.Copy(w, r)  // 忽略了可能发生的错误

// 正确做法：始终检查错误
// n, err := io.Copy(w, r)
// if err != nil {
//     log.Printf("复制失败，已写入 %d 字节：%v", n, err)
// }
```

只有在明确知道操作不会失败时（如 `strings.NewReader`），才可以忽略错误。即便如此，添加注释说明原因也是良好的习惯。

### 9.7.2 在边界处处理错误

错误的处理应遵循"在边界处处理"的原则：

- **内部函数**：遇到错误时，添加上下文并向上传递
- **边界函数**（API handler、main）：将错误转换为适合输出形式

```go
package main

import (
    "errors"
    "fmt"
    "log"
    "os"
)

// Config 应用配置
type Config struct {
    Host string
    Port int
}

// 读取并解析配置文件（内部函数）
func loadConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        // 添加上下文后向上传递
        return nil, fmt.Errorf("读取配置文件 %s 失败：%w", path, err)
    }

    // 模拟解析
    if len(data) == 0 {
        return nil, errors.New("配置文件为空")
    }

    return &Config{Host: "localhost", Port: 8080}, nil
}

// 启动服务
func startServer(cfg *Config) error {
    // 边界函数：将错误转换为用户可见的消息
    fmt.Printf("启动服务：%s:%d\n", cfg.Host, cfg.Port)
    return nil
}

func main() {
    // main 函数是程序的边界，在此处处理所有错误
    cfg, err := loadConfig("config.yaml")
    if err != nil {
        log.Fatalf("无法加载配置：%v", err)
    }

    if err := startServer(cfg); err != nil {
        log.Fatalf("启动服务失败：%v", err)
    }
}
```

### 9.7.3 错误只处理一次

一个错误应该只被处理一次。不要在函数中既打印日志又返回错误，这会导致上层再次打印日志时出现重复信息：

```go
// 错误做法：既打印又返回
// func readConfig(path string) ([]byte, error) {
//     data, err := os.ReadFile(path)
//     if err != nil {
//         log.Printf("读取失败：%v", err)  // 打印
//         return nil, err                 // 又返回
//     }
//     return data, nil
// }
//
// func main() {
//     data, err := readConfig("config.yaml")
//     if err != nil {
//         log.Fatalf("无法启动：%v", err)  // 再次打印
//     }
// }

// 正确做法：要么处理，要么返回
func readConfig(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("读取配置文件失败：%w", err)
    }
    return data, nil
}

func main() {
    data, err := readConfig("config.yaml")
    if err != nil {
        // 只在边界处处理一次
        log.Fatalf("无法启动：%v", err)
    }
    _ = data
}
```

### 9.7.4 选择合适的错误创建方式

| 场景 | 推荐方式 |
|------|----------|
| 静态错误文本 | `errors.New("text")` |
| 带格式化参数 | `fmt.Errorf("格式 %d", val)` |
| 包装错误 | `fmt.Errorf("上下文：%w", err)` |
| 携带额外结构化数据 | 自定义错误类型 |

---

## 9.8 本章小结

- Go 采用显式的 error 返回值而非隐式的异常抛出，错误路径在代码中可见
- `error` 是内建接口，任何实现了 `Error() string` 方法的类型都可以作为错误
- `errors.New` 创建静态错误，`fmt.Errorf` 创建格式化错误
- `%w` 动词实现错误包装，形成可遍历的错误链
- `errors.Is` 按值匹配错误链中的错误，`errors.As` 按类型匹配
- `panic` 仅用于不可恢复的错误，`recover` 在 defer 中捕获 panic
- 自定义错误类型通过实现 `error` 接口来携带额外上下文
- 最佳实践：不忽略错误、在边界处处理、错误只处理一次

---

## 实践任务

1. 实现一个 `DivError` 自定义错误类型，包含 `Dividend`、`Divisor` 和 `Message` 字段，在除零时返回该错误
2. 编写一个函数 `ParseInt(s string) (int, error)`，使用 `strconv.Atoi` 并包装其返回的错误，附加原始输入值
3. 实现一个包含三个层级（main → readData → readFile）的错误包装示例，使用 `errors.Is` 判断底层是否为 `os.ErrNotExist`
4. 编写一个 panic/recover 示例：启动 5 个 goroutine，每个都有可能 panic，通过 recover 确保主程序不会崩溃

---

👉 [下一章：第 10 章 · 并发编程 →](10-concurrency.md)
👉 [返回教程首页 →](index.md)
