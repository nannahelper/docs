# 第 1 章：认识 Rust —— 安全与速度的"双料冠军"

> **场景：** 你决定学习一门"不一样"的编程语言。Rust 不像 Java 那样有垃圾回收，也不像 C 那样需要手动管理内存——它用一种独特的方式（所有权系统）在编译时就确保内存安全。让我们从安装环境开始，运行你的第一个 Rust 程序。

---

## 1.1 Rust 是什么？

!!! example "核心比喻：Rust 就像一位严格的驾校教练"
    学车时，有些教练只在你撞车后才告诉你错了（运行时错误）。有些教练让你自己摸索，撞了再说（C/C++ 的内存 bug）。
    
    Rust 就像一位严格的驾校教练——在你上车之前就检查你的安全带、后视镜、座椅位置。如果你有危险操作，他根本不会让你发动汽车（编译时错误）。
    
    虽然学的时候觉得"管得真多"，但一旦上路，你几乎不会出事故。

Rust 由 Graydon Hoare 于 2006 年创建，Mozilla 于 2009 年赞助开发，2015 年发布 1.0 版本。

| 特性 | 说明 |
|:---|:---|
| **内存安全** | 所有权系统在编译时消除空指针、悬垂指针、双重释放 |
| **零成本抽象** | 高级语法不带来运行时开销，性能媲美 C/C++ |
| **无垃圾回收** | 不需要 GC，内存由所有权系统自动管理 |
| **并发安全** | 类型系统在编译时防止数据竞争 |
| **现代工具链** | Cargo（构建+包管理）、rustfmt（格式化）、clippy（代码检查） |

---

## 1.2 安装 Rust

Rust 使用 `rustup` 工具链管理器来安装和管理 Rust 版本。

=== "Windows"

    1. 打开浏览器，访问 [https://rustup.rs](https://rustup.rs)
    2. 下载并运行 `rustup-init.exe`
    3. 按照提示安装（选择默认选项即可）
    4. 安装完成后，打开 **命令提示符** 或 **PowerShell**，输入：

    ```cmd
    rustc --version
    cargo --version
    ```

=== "macOS / Linux"

    1. 打开终端，运行以下命令：

    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```

    2. 按照提示选择默认安装
    3. 安装完成后，重新加载环境变量：

    ```bash
    source ~/.cargo/env
    ```

    4. 验证安装：

    ```bash
    rustc --version
    cargo --version
    ```

**预期输出：**
```
rustc 1.77.0 (aedd173a2 2024-03-17)
cargo 1.77.0 (3fe68eabf 2024-03-15)
```

!!! info "Rust 工具链组成"
    | 工具 | 作用 |
    |:---|:---|
    | `rustc` | Rust 编译器 |
    | `cargo` | 包管理器和构建工具 |
    | `rustup` | Rust 工具链管理器（安装、更新、切换版本） |
    | `rustfmt` | 代码格式化工具 |
    | `clippy` | 代码检查工具（提供改进建议） |

---

## 1.3 你的第一个 Rust 程序

### 1.3.1 使用 Cargo 创建项目

Cargo 是 Rust 的构建系统和包管理器。用 Cargo 创建项目是最佳实践：

```bash
cargo new hello_world
cd hello_world
```

这会创建一个名为 `hello_world` 的目录，包含以下文件：

```
hello_world/
├── Cargo.toml      # 项目配置文件（类似 Java 的 pom.xml）
└── src/
    └── main.rs     # 程序入口文件
```

### 1.3.2 查看生成的代码

`src/main.rs` 中已经有一个默认的 Hello World 程序：

```rust
fn main() {
    println!("Hello, world!");
}
```

### 1.3.3 编译并运行

```bash
# 编译并运行（开发模式）
cargo run

# 只编译，不运行
cargo build

# 编译发布版本（优化性能）
cargo build --release
```

**运行结果：**
```
   Compiling hello_world v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 0.5s
     Running `target/debug/hello_world`
Hello, world!
```

---

## 1.4 改造 Hello World

让我们修改 `main.rs`，写一个更丰富的程序：

```rust
fn main() {
    // 打印问候语
    println!("===== Rust 初体验 =====");
    
    let name = "小破手";
    let year = 2026;
    
    println!("你好，{}！", name);
    println!("欢迎在 {} 年学习 Rust！", year);
    
    // 简单的计算
    let a = 10;
    let b = 20;
    let sum = a + b;
    
    println!("{} + {} = {}", a, b, sum);
    
    // Rust 的表达式特性
    let is_greater = if a > b {
        "a 大于 b"
    } else {
        "a 不大于 b"
    };
    println!("判断结果: {}", is_greater);
}
```

**运行结果：**
```
===== Rust 初体验 =====
你好，小破手！
欢迎在 2026 年学习 Rust！
10 + 20 = 30
判断结果: a 不大于 b
```

---

## 1.5 Rust 程序的基本结构

```rust
// 1. main 函数是程序入口
fn main() {
    // 2. 变量声明（默认不可变）
    let x = 5;
    
    // 3. 宏调用（以 ! 结尾的是宏）
    println!("x 的值是: {}", x);
    
    // 4. 表达式（以分号结尾的是语句）
    let y = {
        let a = 3;
        a + 1  // 注意：表达式不加分号，表示返回值
    };
    println!("y 的值是: {}", y);
}
```

| 组成部分 | 说明 |
|:---|:---|
| `fn main()` | 程序入口函数 |
| `let` | 变量声明关键字 |
| `println!()` | 宏（macro），`!` 表示这是宏而非普通函数 |
| `{}` | 占位符，用于格式化输出 |
| 表达式 vs 语句 | 表达式有返回值（不加分号），语句没有（加分号） |

!!! note "宏 vs 函数"
    `println!` 后面有 `!`，说明它是宏而不是函数。宏在编译时展开，比函数更灵活。初学阶段你只需要知道 `println!` 和 `vec!` 是宏即可。

---

## 1.6 Cargo.toml 配置文件

```toml
[package]
name = "hello_world"
version = "0.1.0"
edition = "2021"

[dependencies]
# 在这里添加第三方库依赖
```

| 字段 | 说明 |
|:---|:---|
| `[package]` | 项目元信息 |
| `name` | 项目名称 |
| `version` | 版本号（语义化版本） |
| `edition` | Rust 版本（2021 是目前最新） |
| `[dependencies]` | 第三方库依赖声明 |

---

## 要点总结

- [x] Rust 通过所有权系统在编译时保证内存安全
- [x] `rustup` 管理 Rust 工具链，`cargo` 管理项目
- [x] `cargo new` 创建项目，`cargo run` 编译并运行
- [x] `fn main()` 是程序入口
- [x] `println!()` 是宏，用于打印输出
- [x] `let` 声明变量，默认不可变
- [x] 表达式不加分号表示返回值，语句加分号

---

## 课后练习

1.  **修改问候语** ：修改 `main.rs`，让它打印你的名字、年龄和爱好。

2.  **探索 Cargo** ：尝试 `cargo build --release` 和 `cargo check`（只检查不编译），观察它们的区别。

3.  **表达式实验** ：写一段代码，测试在 `{}` 块中加分号和不加分号的区别。

---

**下一章预告：** 现在你知道了如何让 Rust 程序运行。第 2 章将学习变量与数据类型——Rust 的"储物规则"，包括独特的不可变性设计和丰富的数据类型。

[继续第 2 章：变量与数据类型 →](02-variables-and-types.md)