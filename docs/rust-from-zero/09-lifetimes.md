# 第 9 章：生命周期 —— 引用的"保质期"

> **场景：** 你写了一个函数，接受两个字符串引用，返回较短的那个。但编译器报错了——它不知道返回的引用来自哪个参数，无法确定引用的有效期。生命周期标注就是告诉编译器"这些引用之间的关系"，让它能验证内存安全。

---

## 9.1 为什么需要生命周期？

!!! example "核心比喻：生命周期就像食品的保质期"
    你去超市买牛奶，会看保质期。如果一瓶牛奶的保质期到明天，另一瓶到下周，你肯定选保质期长的。
    
    Rust 的编译器就像严格的质检员——它检查每个引用的"保质期"，确保你不会在牛奶过期后还喝它（使用已释放的内存）。

```rust
// 这个函数编译不通过！
// fn longest(x: &str, y: &str) -> &str {
//     if x.len() > y.len() { x } else { y }
// }
// 错误：编译器不知道返回的引用来自 x 还是 y
```

---

## 9.2 生命周期标注语法

生命周期标注以 `'` 开头，通常用小写字母：

```rust
// 'a 表示：x、y 和返回值都拥有相同的生命周期
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

fn main() {
    let string1 = String::from("abcd");
    let string2 = String::from("xyz");
    
    let result = longest(&string1, &string2);
    println!("较长的字符串: {}", result);
}
```

**运行结果：**
```
较长的字符串: abcd
```

!!! info "生命周期标注不改变引用的实际有效期"
    生命周期标注只是告诉编译器引用之间的关系，让编译器能检查。它不会让引用活得更久或死得更早。

---

## 9.3 生命周期省略规则

Rust 编译器有三条省略规则，在很多情况下可以自动推断生命周期：

1. 每个引用参数都有独立的生命周期：`fn foo<'a, 'b>(x: &'a str, y: &'b str)`
2. 如果只有一个输入生命周期，它被赋给所有输出生命周期
3. 如果有 `&self` 或 `&mut self`，它的生命周期被赋给所有输出生命周期

```rust
// 规则 2 的例子：只有一个引用参数，编译器自动推断
fn first_word(s: &str) -> &str {  // 自动推断为 fn first_word<'a>(s: &'a str) -> &'a str
    let bytes = s.as_bytes();
    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }
    &s[..]
}

// 规则 3 的例子：方法中的 &self
struct Student {
    name: String,
}

impl Student {
    fn get_name(&self) -> &str {  // 自动推断生命周期
        &self.name
    }
}
```

---

## 9.4 结构体中的生命周期

当结构体包含引用时，必须标注生命周期：

```rust
// 结构体持有引用，需要生命周期标注
struct Excerpt<'a> {
    part: &'a str,  // Excerpt 的生命周期不能超过 part 引用的有效期
}

fn main() {
    let novel = String::from("从前有座山，山里有座庙...");
    let first_sentence = novel.split('。').next().expect("找不到句号");
    
    let excerpt = Excerpt {
        part: first_sentence,
    };
    
    println!("摘录: {}", excerpt.part);
}
```

---

## 9.5 静态生命周期

`'static` 是一个特殊的生命周期，表示引用在整个程序运行期间都有效：

```rust
fn main() {
    // 字符串字面量拥有 'static 生命周期
    let s: &'static str = "Hello, world!";
    println!("{}", s);
    
    // 常量也拥有 'static 生命周期
    const GREETING: &str = "你好，世界！";
    println!("{}", GREETING);
}
```

---

## 9.6 综合示例

```rust
// 结构体 + 生命周期 + 泛型 + Trait Bound
use std::fmt::Display;

fn longest_with_announcement<'a, T>(
    x: &'a str,
    y: &'a str,
    ann: T,
) -> &'a str
where
    T: Display,
{
    println!("公告: {}", ann);
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

fn main() {
    let s1 = String::from("hello");
    let s2 = String::from("world!");
    
    let result = longest_with_announcement(&s1, &s2, "比较两个字符串");
    println!("较长的: {}", result);
    
    // 生命周期约束示例
    let string1 = String::from("long string is long");
    {
        let string2 = String::from("xyz");
        let result = longest(&string1, &string2);
        println!("较长的: {}", result);
    }  // string2 在这里释放
    
    // 下面的代码编译不通过：
    // let string1 = String::from("long string is long");
    // let result;
    // {
    //     let string2 = String::from("xyz");
    //     result = longest(&string1, &string2);
    // }  // string2 释放，但 result 还引用着它
    // println!("较长的: {}", result);  // 编译错误！
}
```

**运行结果：**
```
公告: 比较两个字符串
较长的: world!
较长的: long string is long
```

---

## 要点总结

- [x] 生命周期标注 `'a` 描述引用之间的关系
- [x] 生命周期不改变引用的实际有效期
- [x] 编译器有三条省略规则，很多情况不需要手动标注
- [x] 结构体包含引用时必须标注生命周期
- [x] `'static` 表示整个程序运行期间有效
- [x] 生命周期、泛型和 Trait Bound 可以组合使用

---

## 课后练习

1.  **最长字符串** ：实现 `longest` 函数，返回两个字符串切片中较长的那个。

2.  **结构体引用** ：定义 `Sentence` 结构体，包含一个 `&str` 字段，标注生命周期。

3.  **组合练习** ：实现一个函数，接受两个引用和一个泛型参数，返回引用并打印泛型参数。

---

**下一章预告：** 项目越来越大，一个 `main.rs` 放不下所有代码。模块系统让你把代码拆成多个文件，Cargo 让你管理第三方依赖。

[继续第 10 章：模块与包管理 →](10-modules-and-crates.md)