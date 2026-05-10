# 第 3 章：所有权与借用 —— Rust 的"灵魂"

> **场景：** 这是 Rust 最独特、最重要的概念。Java 用垃圾回收（GC）管理内存，C 让程序员手动 `malloc/free`。Rust 走了第三条路——所有权系统，在编译时就确定每块内存的"主人"是谁，何时释放。理解所有权，就理解了 Rust 的灵魂。

---

## 3.1 为什么需要所有权？

!!! example "核心比喻：所有权就像图书馆的借书制度"
    - **Java 的 GC** 就像图书馆有管理员，你借了书不用还，管理员会定期巡视，把没人看的书收回书架。方便，但管理员巡视时图书馆会暂停服务（GC 停顿）。
    - **C 的手动管理** 就像没有管理员，你借了书必须自己还。忘了还？书就丢了（内存泄漏）。还了两次？书架乱了（双重释放）。
    - **Rust 的所有权** 就像严格的借书规则：每本书同一时间只能有一个人持有。你把书借给朋友，你就不能再看了（所有权转移）。朋友看完还给你，你才能继续看。书在谁手里，谁负责还。

Rust 的所有权规则：

1. Rust 中的每个值都有一个 **所有者**（owner）
2. 同一时间只能有一个所有者
3. 当所有者离开作用域，值会被自动释放

---

## 3.2 所有权的基本规则

### 作用域与释放

```rust
fn main() {
    {                           // s 还不存在
        let s = String::from("hello");  // s 从这里开始有效
        println!("{}", s);
    }                           // s 离开作用域，内存自动释放
    // println!("{}", s);       // 编译错误！s 已经不存在了
}
```

### 所有权转移（Move）

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;  // 所有权从 s1 转移到 s2
    
    // println!("{}", s1);  // 编译错误！s1 已经失效
    println!("{}", s2);     // 正确，s2 现在是所有者
}
```

!!! info "String 类型"
    `String` 是存储在堆上的可变字符串类型。本章大量使用 `String` 来演示所有权，因为它涉及堆内存分配，能清晰展示所有权的转移。

### 栈上数据的复制（Copy）

对于存储在栈上的简单类型，赋值时会自动复制而不是转移：

```rust
fn main() {
    let x = 5;
    let y = x;  // x 的值被复制给 y，x 仍然有效
    
    println!("x = {}, y = {}", x, y);  // 两个都可以用
}
```

| 类型 | 行为 | 原因 |
|:---|:---|:---|
| `i32`、`f64`、`bool`、`char` | Copy（复制） | 大小固定，存在栈上 |
| `String`、`Vec` | Move（转移） | 大小不固定，存在堆上 |
| 元组（元素都可 Copy） | Copy | 整体大小固定 |

---

## 3.3 所有权与函数

```rust
fn main() {
    let s = String::from("hello");
    
    takes_ownership(s);  // s 的所有权转移到函数中
    // println!("{}", s);  // 编译错误！s 已经失效
    
    let x = 5;
    makes_copy(x);  // x 被复制，x 仍然有效
    println!("x 仍然是: {}", x);
}

fn takes_ownership(some_string: String) {
    println!("获得所有权: {}", some_string);
}  // some_string 离开作用域，内存释放

fn makes_copy(some_integer: i32) {
    println!("获得副本: {}", some_integer);
}  // some_integer 离开作用域，没什么特别的事
```

**运行结果：**
```
获得所有权: hello
获得副本: 5
x 仍然是: 5
```

### 返回值转移所有权

```rust
fn main() {
    let s1 = gives_ownership();  // 函数返回值转移给 s1
    println!("s1 = {}", s1);
    
    let s2 = String::from("hello");
    let s3 = takes_and_gives_back(s2);  // s2 转移进函数，返回值转移给 s3
    println!("s3 = {}", s3);
}

fn gives_ownership() -> String {
    let some_string = String::from("yours");
    some_string  // 返回，所有权转移给调用者
}

fn takes_and_gives_back(a_string: String) -> String {
    a_string  // 返回，所有权转移给调用者
}
```

**运行结果：**
```
s1 = yours
s3 = hello
```

---

## 3.4 引用与借用

每次都转移所有权太麻烦了。Rust 提供了 **引用**——允许你"借用"值而不获取所有权：

```rust
fn main() {
    let s1 = String::from("hello");
    
    let len = calculate_length(&s1);  // &s1 创建引用，不转移所有权
    
    println!("'{}' 的长度是 {}", s1, len);  // s1 仍然有效！
}

fn calculate_length(s: &String) -> usize {  // s 是 String 的引用
    s.len()
}  // s 离开作用域，但它不拥有数据，所以不会释放
```

**运行结果：**
```
'hello' 的长度是 5
```

!!! example "核心比喻：引用就像借书证"
    你把书借给朋友看，给他的是借书证（引用），书还在你手里。朋友通过借书证可以看书的内容，但不能在书上写字（不可变引用），除非你给了他一支笔（可变引用）。

### 可变引用

```rust
fn main() {
    let mut s = String::from("hello");
    
    change(&mut s);  // &mut 创建可变引用
    
    println!("修改后: {}", s);
}

fn change(some_string: &mut String) {
    some_string.push_str(", world!");  // 通过可变引用修改数据
}
```

**运行结果：**
```
修改后: hello, world!
```

---

## 3.5 引用的规则

!!! danger "引用的两条铁律"
    1. 在任意给定时间，**要么**只能有一个可变引用，**要么**只能有多个不可变引用
    2. 引用必须始终有效（不能有悬垂引用）

### 规则 1：不能同时有可变和不可变引用

```rust
fn main() {
    let mut s = String::from("hello");
    
    let r1 = &s;     // 不可变引用
    let r2 = &s;     // 不可变引用，可以有多个
    // let r3 = &mut s;  // 编译错误！不能同时有可变和不可变引用
    
    println!("{} and {}", r1, r2);
    // r1 和 r2 在这里之后不再使用
    
    let r3 = &mut s;  // 现在可以了，因为 r1 和 r2 已经"过期"
    r3.push_str(" world");
    println!("{}", r3);
}
```

### 规则 2：不能有悬垂引用

```rust
fn main() {
    let reference_to_nothing = dangle();
}

// fn dangle() -> &String {  // 编译错误！
//     let s = String::from("hello");
//     &s  // s 在函数结束时被释放，返回的引用指向已释放的内存
// }
```

---

## 3.6 切片（Slice）

切片是集合中部分元素的引用：

```rust
fn main() {
    let s = String::from("hello world");
    
    // 字符串切片
    let hello = &s[0..5];   // "hello"
    let world = &s[6..11];  // "world"
    let all = &s[..];       // "hello world"
    
    println!("{} {}", hello, world);
    
    // 数组切片
    let arr = [1, 2, 3, 4, 5];
    let slice = &arr[1..4];  // [2, 3, 4]
    println!("切片: {:?}", slice);
}
```

**运行结果：**
```
hello world
切片: [2, 3, 4]
```

---

## 要点总结

- [x] 每个值有且只有一个所有者
- [x] 所有者离开作用域，值被自动释放
- [x] 栈上简单类型自动 Copy，堆上类型 Move
- [x] `&T` 创建不可变引用（借用），不获取所有权
- [x] `&mut T` 创建可变引用，同一时间只能有一个
- [x] 不能同时存在可变引用和不可变引用
- [x] 引用必须始终有效，编译器防止悬垂引用
- [x] 切片是集合中部分元素的引用

---

## 课后练习

1.  **所有权追踪** ：写出以下代码中每行之后哪些变量有效：

    ```rust
    let s1 = String::from("hello");
    let s2 = s1;
    let s3 = s2.clone();
    ```

2.  **借用练习** ：编写一个函数，接受 `&String` 参数，返回字符串的第一个单词。

3.  **可变引用** ：编写一个函数，接受 `&mut String`，在字符串末尾追加 `"!!!"`。

---

**下一章预告：** 所有权和借用是 Rust 的基础。接下来学习如何用结构体和枚举定义自己的数据类型——构建程序的"积木块"。

[继续第 4 章：结构体与枚举 →](04-structs-and-enums.md)