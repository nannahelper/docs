# 第 10 章：并发编程

> **并发编程** —— Go 语言通过 goroutine 和 channel 提供了原生的并发编程支持，使编写高并发程序变得简洁而安全

---

## 10.1 并发与并行的概念

### 10.1.1 定义

**并发（Concurrency）** 和 **并行（Parallelism）** 是两个密切相关但本质不同的概念：

- **并发**：程序的 **结构** 属性。指程序被设计为多个独立执行的任务，这些任务可能在时间上交替执行。并发关注的是如何处理多个任务。
- **并行**：程序的 **执行** 属性。指多个任务在同一时刻同时执行。并行关注的是如何利用多核处理器加速执行。

Go 语言的设计哲学是：**通过并发结构来表达程序，运行时自行决定是否并行执行**。

### 10.1.2 类比

并发是程序设计的组织方式，而并行是物理执行方式。一个并发程序可以在单核 CPU 上通过时间片轮转执行（此时没有并行），也可以在多核 CPU 上真正同时执行（此时既有并发也有并行）。

> **关键区别**：并发关乎 **结构**，并行关乎 **执行**。编写并发程序利用的是 Go 的 goroutine 和 channel 机制；而并行执行则需要运行时的调度器将 goroutine 分布到多个 OS 线程上，这在 GOMAXPROCS > 1 时自动发生。

---

## 10.2 goroutine

### 10.2.1 什么是 goroutine

goroutine 是 Go 语言中的轻量级执行单元，由 Go 运行时管理。它的核心特征如下：

| 特征 | goroutine | OS 线程 |
|------|-----------|---------|
| 栈初始大小 | 约 4 KB | 约 1 MB（固定） |
| 栈扩展能力 | 按需增长（可达 1 GB） | 固定大小 |
| 创建成本 | 约几微秒 | 约几毫秒 |
| 上下文切换 | 用户态切换（约几十纳秒） | 内核态切换（约几微秒） |
| 调度方式 | M:N 调度（用户级） | 内核调度 |

### 10.2.2 M:N 调度模型

Go 的调度器实现了 **M:N 调度** 模型：

- **M**（Machine）：OS 线程
- **P**（Processor）：逻辑处理器，代表调度上下文
- **G**（Goroutine）：goroutine

调度器将 G 分配到 P 上执行，P 再绑定到 M 上运行。这种设计使得大量 goroutine 能够在少量 OS 线程上高效复用。

### 10.2.3 使用 go 关键字

创建 goroutine 只需要在函数调用前加上 `go` 关键字：

```go
package main

import (
    "fmt"
    "time"
)

// 在一个 goroutine 中执行的函数
func printNumbers(prefix string) {
    for i := 1; i <= 5; i++ {
        fmt.Printf("%s: %d\n", prefix, i)
        // 模拟耗时操作
        time.Sleep(100 * time.Millisecond)
    }
}

func main() {
    // 启动一个新的 goroutine 执行 printNumbers
    go printNumbers("goroutine A")
    go printNumbers("goroutine B")

    // 主 goroutine 也执行一次
    printNumbers("main")

    // 等待 goroutine 完成（不严谨的等待方式）
    time.Sleep(2 * time.Second)
    fmt.Println("所有 goroutine 执行完毕")
}
```

> **注意**：主 goroutine（即 `main` 函数所在的 goroutine）结束时，整个程序会立即终止，无论其他 goroutine 是否执行完毕。因此需要某种同步机制来等待其他 goroutine 完成。

---

## 10.3 channel

### 10.3.1 基本概念

Channel 是 Go 中 goroutine 之间的通信机制。它的设计遵循了 Go 的并发哲学：

> **不要通过共享内存来通信，应该通过通信来共享内存。**

Channel 是类型化的、带方向的、并发安全的 FIFO 队列。

### 10.3.2 创建和操作

```go
package main

import "fmt"

func main() {
    // 创建一个 int 类型的无缓冲 channel
    ch := make(chan int)

    // 启动一个 goroutine 向 channel 发送数据
    go func() {
        ch <- 42 // 发送操作：将 42 发送到 channel
    }()

    // 主 goroutine 从 channel 接收数据
    value := <-ch // 接收操作：从 channel 接收值
    fmt.Println("接收到：", value)

    // --- 有缓冲 channel ---
    buffered := make(chan string, 3) // 容量为 3 的缓冲 channel

    // 发送数据，不超过缓冲区则不会阻塞
    buffered <- "A"
    buffered <- "B"
    buffered <- "C"

    // 接收数据
    fmt.Println(<-buffered) // 输出：A
    fmt.Println(<-buffered) // 输出：B
    fmt.Println(<-buffered) // 输出：C
}
```

### 10.3.3 无缓冲 channel 与有缓冲 channel

**无缓冲 channel**（`make(chan T)`）：

- 发送操作会阻塞，直到有其他 goroutine 执行接收操作
- 接收操作会阻塞，直到有其他 goroutine 执行发送操作
- 提供同步保证：发送方和接收方在数据交换时会同步（rendezvous）

**有缓冲 channel**（`make(chan T, capacity)`）：

- 发送操作在缓冲区未满时不会阻塞
- 接收操作在缓冲区非空时不会阻塞
- 缓冲区满时，发送方阻塞；缓冲区空时，接收方阻塞

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 演示无缓冲 channel 的同步特性
    syncCh := make(chan bool)

    go func() {
        fmt.Println("goroutine：开始工作")
        time.Sleep(500 * time.Millisecond)
        fmt.Println("goroutine：工作完成")

        // 发送完成信号（无缓冲，会阻塞直到主 goroutine 接收）
        syncCh <- true
    }()

    // 主 goroutine 阻塞等待完成信号
    <-syncCh
    fmt.Println("main：goroutine 已完成，程序结束")
}
```

### 10.3.4 close 和 for range

发送方可以通过 `close` 关闭 channel，接收方通过 `for range` 持续接收直到 channel 关闭：

```go
package main

import "fmt"

// 生成器：向 channel 发送 N 个整数
func generateNumbers(count int, ch chan<- int) {
    for i := 0; i < count; i++ {
        ch <- i * 2
    }
    close(ch) // 关闭 channel，通知接收方不再有数据
}

func main() {
    ch := make(chan int, 5)

    go generateNumbers(5, ch)

    // 使用 for range 持续从 channel 接收数据
    // 当 channel 关闭且缓冲区为空时，循环自动结束
    for val := range ch {
        fmt.Println("接收到：", val)
    }

    // 检查 channel 状态
    value, ok := <-ch // 已关闭的 channel：ok 为 false，value 为零值
    fmt.Printf("从已关闭的 channel 接收：%d, 状态：%t\n", value, ok)
}
```

**channel 操作总结**：

| 操作 | 未关闭 | 已关闭 | nil |
|------|--------|--------|-----|
| 发送 `ch <- v` | 成功或阻塞 | panic | 永久阻塞 |
| 接收 `<-ch` | 成功或阻塞 | 返回零值（不阻塞） | 永久阻塞 |
| 关闭 `close(ch)` | 成功 | panic | panic |

---

## 10.4 select 多路复用

`select` 语句允许一个 goroutine 同时等待多个 channel 操作。它的语法类似于 `switch`，但每个 case 必须是一个 channel 的发送或接收操作。

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)

    // goroutine 1：每 200ms 发送一次
    go func() {
        for {
            time.Sleep(200 * time.Millisecond)
            ch1 <- "来自 ch1 的消息"
        }
    }()

    // goroutine 2：每 300ms 发送一次
    go func() {
        for {
            time.Sleep(300 * time.Millisecond)
            ch2 <- "来自 ch2 的消息"
        }
    }()

    // 使用 select 同时监听多个 channel
    for i := 0; i < 5; i++ {
        select {
        case msg := <-ch1:
            fmt.Println("ch1：", msg)
        case msg := <-ch2:
            fmt.Println("ch2：", msg)
        }
    }
}
```

### 10.4.1 default 分支

`default` 分支在所有 channel 操作都无法执行时立即执行，用于实现非阻塞操作：

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    ch := make(chan int, 1)
    ch <- 1

    // 非阻塞发送：缓冲区已满，执行 default
    select {
    case ch <- 2:
        fmt.Println("发送成功")
    default:
        fmt.Println("channel 已满，发送失败")
    }

    // 非阻塞接收：有数据可接收
    select {
    case val := <-ch:
        fmt.Println("接收到：", val)
    default:
        fmt.Println("无数据可接收")
    }

    // 再次尝试接收（channel 为空）
    select {
    case val := <-ch:
        fmt.Println("接收到：", val)
    default:
        fmt.Println("无数据可接收")
    }
}
```

### 10.4.2 超时控制

结合 `time.After` 实现 channel 操作的超时：

```go
package main

import (
    "fmt"
    "time"
)

// 模拟一个可能耗时过长的操作
func slowOperation(result chan<- string) {
    time.Sleep(3 * time.Second)
    result <- "操作完成"
}

func main() {
    result := make(chan string)

    go slowOperation(result)

    // 设置超时等待
    select {
    case res := <-result:
        fmt.Println(res)
    case <-time.After(1 * time.Second):
        fmt.Println("操作超时")
    }
}
```

---

## 10.5 sync 包

### 10.5.1 WaitGroup

`sync.WaitGroup` 用于等待一组 goroutine 完成。它是 goroutine 同步中最常用的工具之一：

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func worker(id int, wg *sync.WaitGroup) {
    // 在函数退出时通知 WaitGroup 该 goroutine 已完成
    defer wg.Done()

    fmt.Printf("Worker %d：开始工作\n", id)
    time.Sleep(time.Duration(id) * 200 * time.Millisecond)
    fmt.Printf("Worker %d：工作完成\n", id)
}

func main() {
    var wg sync.WaitGroup

    // 启动 5 个 goroutine
    for i := 1; i <= 5; i++ {
        wg.Add(1)                    // 增加等待计数器
        go worker(i, &wg)            // 传递指针，因为 wg 内部状态需要被修改
    }

    // 等待所有 goroutine 完成
    wg.Wait()
    fmt.Println("所有 worker 已完成")
}
```

**WaitGroup 的使用规范**：

1. `Add(delta)` 必须在 goroutine 启动前调用，而非在 goroutine 内部
2. `Done()` 是 `Add(-1)` 的简写，通常用 `defer` 调用
3. `Wait()` 阻塞直到计数器归零
4. WaitGroup 是值类型，传递给函数时必须使用指针

### 10.5.2 Mutex

`sync.Mutex` 提供互斥锁，保护共享资源的并发访问：

```go
package main

import (
    "fmt"
    "sync"
)

// Counter 线程安全的计数器
type Counter struct {
    mu    sync.Mutex
    value int
}

// Increment 原子增加计数
func (c *Counter) Increment() {
    c.mu.Lock()   // 获取锁
    c.value++     // 临界区
    c.mu.Unlock() // 释放锁
}

// Value 安全获取当前值
func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock() // 使用 defer 确保锁被释放
    return c.value
}

func main() {
    var counter Counter
    var wg sync.WaitGroup

    // 启动 1000 个 goroutine 并发增加计数器
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter.Increment()
        }()
    }

    wg.Wait()
    fmt.Printf("最终计数：%d (期望值：1000)\n", counter.Value())
}
```

### 10.5.3 RWMutex

`sync.RWMutex` 是读写锁，适用于 **读多写少** 的场景：

- 任意数量的读操作可以同时持有读锁
- 写操作必须独占写锁（所有读锁和写锁均释放后才能获得）
- 读锁和写锁互斥

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

// SafeCache 线程安全的缓存
type SafeCache struct {
    mu    sync.RWMutex
    data  map[string]string
}

// Get 读取缓存（使用读锁）
func (c *SafeCache) Get(key string) (string, bool) {
    c.mu.RLock()               // 读锁定
    defer c.mu.RUnlock()       // 读解锁

    val, ok := c.data[key]
    return val, ok
}

// Set 写入缓存（使用写锁）
func (c *SafeCache) Set(key, value string) {
    c.mu.Lock()                // 写锁定
    defer c.mu.Unlock()        // 写解锁

    c.data[key] = value
}

func main() {
    cache := &SafeCache{data: make(map[string]string)}
    var wg sync.WaitGroup

    // 并发读取（读操作可以同时进行）
    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            cache.Set(fmt.Sprintf("key-%d", id), fmt.Sprintf("value-%d", id))
        }(i)
    }

    // 并发读取
    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            val, ok := cache.Get(fmt.Sprintf("key-%d", id))
            if ok {
                fmt.Printf("goroutine %d 读取：%s\n", id, val)
            }
        }(i)
    }

    wg.Wait()
    time.Sleep(100 * time.Millisecond)
    fmt.Println("缓存操作完成")
}
```

**Mutex vs RWMutex 选择**：

| 场景 | 推荐 |
|------|------|
| 写操作频繁 | `sync.Mutex` |
| 读操作远多于写操作 | `sync.RWMutex` |
| 临界区执行时间很短 | `sync.Mutex` |

---

## 10.6 sync/atomic 包

`sync/atomic` 包提供底层原子内存操作，用于无锁编程。对于简单的计数器等场景，原子操作比使用 Mutex 具有更高的性能：

```go
package main

import (
    "fmt"
    "sync"
    "sync/atomic"
)

func main() {
    // 使用原子操作实现计数器
    var counter int64
    var wg sync.WaitGroup

    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            // 原子加 1（无需 Mutex）
            atomic.AddInt64(&counter, 1)
        }()
    }

    wg.Wait()
    fmt.Printf("原子计数：%d (期望值：1000)\n", counter)

    // 原子加载和存储
    var value atomic.Value
    value.Store("hello")
    fmt.Println(value.Load())

    // 比较并交换（CAS）
    var num int64 = 100
    swapped := atomic.CompareAndSwapInt64(&num, 100, 200)
    fmt.Printf("CAS 结果：%t, 值：%d\n", swapped, num)
}
```

**atomic 提供的操作类型**：

- `AddT`：原子增减（T 为 `Int32`、`Int64`、`Uint32`、`Uint64`）
- `LoadT`：原子读取
- `StoreT`：原子写入
- `SwapT`：原子交换
- `CompareAndSwapT`：比较并交换（CAS）
- `Value`：任意类型的原子存储

---

## 10.7 并发模式

### 10.7.1 Pipeline 模式

Pipeline 模式将数据处理分为多个阶段，每个阶段由独立的 goroutine 处理，通过 channel 连接：

```go
package main

import "fmt"

// 阶段 1：生成整数序列
func generate(numbers ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range numbers {
            out <- n
        }
        close(out)
    }()
    return out
}

// 阶段 2：计算平方
func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

// 阶段 3：乘以 2
func double(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * 2
        }
        close(out)
    }()
    return out
}

func main() {
    // 构建 pipeline：generate → square → double
    numbers := []int{1, 2, 3, 4, 5}

    // 串联各个阶段
    result := double(square(generate(numbers...)))

    // 输出最终结果
    for val := range result {
        fmt.Printf("结果：%d\n", val)
    }
}
```

### 10.7.2 Fan-Out / Fan-In 模式

**Fan-Out**：将同一数据分发给多个 goroutine 并行处理。
**Fan-In**：将多个 goroutine 的输出合并到一个 channel。

```go
package main

import (
    "fmt"
    "sync"
)

// 数据源：生成待处理的数据
func sourceData() <-chan int {
    out := make(chan int)
    go func() {
        for i := 1; i <= 10; i++ {
            out <- i
        }
        close(out)
    }()
    return out
}

// Worker：处理数据（模拟耗时计算）
func worker(id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
    defer wg.Done()
    for job := range jobs {
        result := job * job
        fmt.Printf("Worker %d 处理：%d → %d\n", id, job, result)
        results <- result
    }
}

// Fan-In：合并多个输出 channel
func fanIn(channels ...<-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup

    // 为每个输入 channel 启动一个转发 goroutine
    for _, ch := range channels {
        // 实际上这里简化了，常规的 fan-in 使用一个 channel
        _ = ch
    }

    // 这里是简化示例，直接返回一个合并后的 channel
    // 实际实现中需要合并多个 source
    return out
}

func main() {
    // 输入数据
    jobs := sourceData()

    // Fan-Out：启动 3 个 worker goroutine
    numWorkers := 3
    results := make(chan int, 10) // 有缓冲 channel 避免阻塞
    var wg sync.WaitGroup

    for i := 1; i <= numWorkers; i++ {
        wg.Add(1)
        go worker(i, jobs, results, &wg)
    }

    // 等待所有 worker 完成，然后关闭结果 channel
    go func() {
        wg.Wait()
        close(results)
    }()

    // Fan-In：收集所有结果
    sum := 0
    for result := range results {
        sum += result
    }
    fmt.Printf("最终总和：%d\n", sum)
}
```

---

## 10.8 context 包

`context` 包提供了在 goroutine 之间传递取消信号、超时信息和请求级元数据的能力。

### 10.8.1 context 的核心接口

```go
type Context interface {
    Deadline() (deadline time.Time, ok bool)
    Done() <-chan struct{}
    Err() error
    Value(key any) any
}
```

- `Done()`：返回一个 channel，当 context 被取消或超时时关闭
- `Err()`：返回 context 被取消的原因
- `Deadline()`：返回设定的截止时间
- `Value()`：获取绑定的键值对

### 10.8.2 超时控制

```go
package main

import (
    "context"
    "fmt"
    "time"
)

// 模拟一个可能超时的数据库查询
func queryDatabase(ctx context.Context, query string) (string, error) {
    // 创建一个用于模拟数据库操作的 channel
    result := make(chan string, 1)

    // 启动 goroutine 模拟数据库查询
    go func() {
        // 模拟耗时操作
        time.Sleep(2 * time.Second)
        result <- "查询结果：" + query
    }()

    // 使用 select 同时等待结果和 context 取消
    select {
    case res := <-result:
        return res, nil
    case <-ctx.Done():
        // context 被取消（超时或手动取消）
        return "", ctx.Err()
    }
}

func main() {
    // 创建一个 1 秒后超时的 context
    ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
    defer cancel() // 确保资源被释放

    result, err := queryDatabase(ctx, "SELECT * FROM users")
    if err != nil {
        fmt.Printf("查询失败：%v\n", err)
        return
    }
    fmt.Println(result)
}
```

### 10.8.3 取消传播

```go
package main

import (
    "context"
    "fmt"
    "time"
)

// 执行子任务
func subTask(ctx context.Context, name string, duration time.Duration) {
    select {
    case <-time.After(duration):
        fmt.Printf("%s：执行完毕\n", name)
    case <-ctx.Done():
        fmt.Printf("%s：被取消 (原因：%v)\n", name, ctx.Err())
    }
}

func main() {
    // 创建可取消的 context
    parentCtx := context.Background()
    ctx, cancel := context.WithCancel(parentCtx)

    // 启动多个子任务
    go subTask(ctx, "任务 A", 2*time.Second)
    go subTask(ctx, "任务 B", 3*time.Second)
    go subTask(ctx, "任务 C", 1*time.Second)

    // 1.5 秒后取消所有子任务
    time.Sleep(1500 * time.Millisecond)
    fmt.Println("取消所有子任务")
    cancel()

    // 等待子任务响应取消
    time.Sleep(500 * time.Millisecond)
    fmt.Println("主程序结束")
}
```

---

## 10.9 竞态检测

Go 内置了竞态检测器（race detector），可以在测试或运行时检测数据竞争。

```bash
# 运行时检测
go run -race main.go

# 测试时检测
go test -race ./...

# 编译时包含竞态检测
go build -race -o app.exe .
```

示例：存在数据竞争的代码：

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var counter int
    var wg sync.WaitGroup

    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter++ // 数据竞争：多个 goroutine 同时写入同一变量
        }()
    }

    wg.Wait()
    fmt.Println(counter)
}
```

使用 `go run -race counter.go` 运行上述代码时，会输出类似以下警告：

```
WARNING: DATA RACE
Read at 0x... by goroutine X
  main.main.func1()
      counter.go:14 +0x...

Previous write at 0x... by goroutine Y
  main.main.func1()
      counter.go:14 +0x...
```

修复方式：使用 Mutex 或原子操作。

---

## 10.10 本章小结

- **并发** 是程序的结构属性，**并行** 是执行属性，Go 通过 goroutine 表达并发结构
- goroutine 是轻量级执行单元，采用 M:N 调度模型，创建成本极低
- channel 提供类型化的 goroutine 间通信，遵循 **通过通信共享内存** 的哲学
- 无缓冲 channel 提供同步保障，有缓冲 channel 提供异步解耦
- `select` 语句实现多路 channel 复用，支持非阻塞操作和超时控制
- `sync.WaitGroup` 等待 goroutine 完成，`sync.Mutex` / `sync.RWMutex` 保护共享资源
- `sync/atomic` 包提供无锁的原子操作
- `context` 包提供取消传播、超时控制和元数据传递
- Pipeline 和 Fan-Out/Fan-In 是常用的并发编程模式
- 使用 `-race` 标志检测数据竞争，始终确保并发安全

---

## 实践任务

1. 使用 goroutine 和 channel 实现一个简单的 **工作池**：启动 5 个 worker goroutine，处理 20 个任务，每个任务打印 "处理任务 N"
2. 使用 Pipeline 模式构建一个文本处理流程：读取字符串 → 转为大写 → 添加后缀 "!" → 输出
3. 使用 `context.WithTimeout` 实现一个带有 500ms 超时的网络请求模拟
4. 创建一个 `safeCounter` 结构体，分别使用 Mutex 和 atomic 实现，对比两种实现方式的性能差异（可使用 `testing.Benchmark`）

---

👉 [下一章：第 11 章 · 标准库概览 →](11-standard-library.md)
👉 [返回教程首页 →](index.md)
