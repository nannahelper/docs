# 第 6 章：函数与错误处理 —— 组织代码与应对意外

> **场景：** 程序越来越长，你需要把代码拆成函数来组织。同时，程序运行中总会遇到意外——文件不存在、网络断开、用户输入错误。Rust 用 `Result` 和 `?` 运算符提供了一种优雅的错误处理方式，让错误处理代码既简洁又安全。

---

## 6.1 函数定义与返回值

!!! example "核心比喻：函数就像工厂的生产线"
    你给工厂送原料（参数），工厂经过加工（函数体），产出产品（返回值）。Rust 的函数签名就像工厂门口的标牌——明确告诉你需要什么原料、产出什么产品。

```rust
// 基本函数
fn greet(name: &str) {
    println!("你好，{}！", name);
}

// 带返回值的函数
fn add(a: i32, b: i32) -> i32 {
    a + b  // 最后一行不加分号 = 返回值
}

// 提前返回
fn absolute(x: i32) -> i32 {
    if x >= 0 {
        return x;  // 用 return 提前返回
    }
    -x  // 隐式返回
}

fn main() {
    greet("小破手");
    
    let sum = add(10, 20);
    println!("10 + 20 = {}", sum);
    
    println!("|5| = {}", absolute(5));
    println!("|-5| = {}", absolute(-5));
}
```

**运行结果：**
```
你好，小破手！
10 + 20 = 30
|5| = 5
|-5| = 5
```

---

## 6.2 闭包（Closure）

闭包是匿名函数，可以捕获环境中的变量：

```rust
fn main() {
    let multiplier = 3;
    
    // 闭包：捕获了外部的 multiplier
    let multiply = |x: i32| x * multiplier;
    
    println!("5 * {} = {}", multiplier, multiply(5));
    println!("10 * {} = {}", multiplier, multiply(10));
    
    // 闭包用于迭代器
    let numbers = vec![1, 2, 3, 4, 5];
    
    let doubled: Vec<i32> = numbers.iter()
        .map(|x| x * 2)
        .collect();
    println!("翻倍: {:?}", doubled);
    
    let evens: Vec<i32> = numbers.iter()
        .filter(|&&x| x % 2 == 0)
        .copied()
        .collect();
    println!("偶数: {:?}", evens);
}
```

**运行结果：**
```
5 * 3 = 15
10 * 3 = 30
翻倍: [2, 4, 6, 8, 10]
偶数: [2, 4]
```

---

## 6.3 Result 枚举 —— 可恢复的错误

`Result` 是 Rust 错误处理的核心：

```rust
// Result 的定义（标准库中）
// enum Result<T, E> {
//     Ok(T),    // 成功，包含结果值
//     Err(E),   // 失败，包含错误信息
// }

use std::fs::File;
use std::io::Read;

fn read_file_content(path: &str) -> Result<String, std::io::Error> {
    let mut file = File::open(path)?;  // ? 传播错误
    let mut content = String::new();
    file.read_to_string(&mut content)?;
    Ok(content)
}

fn main() {
    match read_file_content("存在.txt") {
        Ok(content) => println!("文件内容:\n{}", content),
        Err(e) => println!("读取失败: {}", e),
    }
}
```

---

## 6.4 ? 运算符 —— 错误传播

`?` 是 Rust 最优雅的错误处理语法：

```rust
use std::fs;
use std::io;

// 不使用 ?（啰嗦）
fn read_username_verbose() -> Result<String, io::Error> {
    let result = fs::read_to_string("username.txt");
    match result {
        Ok(content) => Ok(content.trim().to_string()),
        Err(e) => Err(e),
    }
}

// 使用 ?（简洁）
fn read_username() -> Result<String, io::Error> {
    let content = fs::read_to_string("username.txt")?;
    Ok(content.trim().to_string())
}

fn main() {
    match read_username() {
        Ok(name) => println!("用户名: {}", name),
        Err(e) => println!("读取失败: {}", e),
    }
}
```

!!! tip "? 运算符做了什么？"
    `expr?` 等价于：
    ```rust
    match expr {
        Ok(value) => value,     // 成功则取出值继续
        Err(e) => return Err(e.into()),  // 失败则提前返回错误
    }
    ```

---

## 6.5 组合 Option 和 Result

```rust
fn parse_number(s: &str) -> Option<i32> {
    s.parse().ok()  // Result 转 Option
}

fn safe_divide(a: i32, b: i32) -> Result<f64, String> {
    if b == 0 {
        Err(String::from("除数不能为 0"))
    } else {
        Ok(a as f64 / b as f64)
    }
}

fn main() {
    // 解析数字
    match parse_number("42") {
        Some(n) => println!("解析成功: {}", n),
        None => println!("解析失败"),
    }
    
    match parse_number("abc") {
        Some(n) => println!("解析成功: {}", n),
        None => println!("解析失败"),
    }
    
    // 安全除法
    let results = [
        safe_divide(10, 2),
        safe_divide(10, 0),
        safe_divide(15, 3),
    ];
    
    for result in &results {
        match result {
            Ok(value) => println!("结果: {}", value),
            Err(e) => println!("错误: {}", e),
        }
    }
}
```

**运行结果：**
```
解析成功: 42
解析失败
结果: 5
错误: 除数不能为 0
结果: 5
```

---

## 6.6 panic! —— 不可恢复的错误

```rust
fn main() {
    // panic! 会让程序立即终止
    // panic!("程序遇到了无法恢复的错误！");
    
    let v = vec![1, 2, 3];
    // v[99];  // 索引越界，panic!
    
    // 使用 unwrap 和 expect
    let x: Option<i32> = Some(5);
    println!("x = {}", x.unwrap());  // 安全，因为 x 是 Some
    
    let y: Option<i32> = None;
    // println!("{}", y.unwrap());  // panic! 因为 y 是 None
    
    // expect 可以自定义错误信息
    // println!("{}", y.expect("y 不应该是 None！"));
}
```

| 方法 | 行为 | 使用场景 |
|:---|:---|:---|
| `unwrap()` | 成功返回值，失败 panic | 快速原型、确定不会失败 |
| `expect(msg)` | 同上，但带自定义错误信息 | 同上，但提供更好的错误信息 |
| `unwrap_or(default)` | 失败时返回默认值 | 有合理的默认值 |
| `?` | 失败时传播错误 | 生产代码，错误需要向上传递 |

---

## 要点总结

- [x] 函数最后一行不加分号表示返回值
- [x] 闭包 `|参数| 表达式` 可以捕获环境变量
- [x] `Result<T, E>` 用于可恢复的错误（`Ok` / `Err`）
- [x] `?` 运算符传播错误，让代码简洁
- [x] `Option<T>` 用于值可能不存在的情况
- [x] `unwrap()` / `expect()` 在确定不会失败时使用
- [x] `panic!` 用于不可恢复的错误

---

## 课后练习

1.  **文件读取** ：编写函数读取文件内容，文件不存在时返回自定义错误信息。

2.  **数字解析** ：从字符串解析数字，处理解析失败和除零错误。

3.  **闭包练习** ：用闭包和迭代器对 `Vec<i32>` 进行过滤、映射和求和。

---

**下一章预告：** 数组大小固定，操作受限。Rust 的集合类型（Vec、HashMap、String）提供了动态、灵活的数据管理能力。

[继续第 7 章：集合类型 →](07-collections.md)