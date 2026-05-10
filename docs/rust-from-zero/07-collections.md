# 第 7 章：集合类型 —— 数据的"动态仓库"

> **场景：** 数组大小固定，元组字段不能动态增减。你需要一个能自动扩容的列表（Vec）、一个能通过键快速查找的字典（HashMap）、一个能灵活修改的字符串（String）。Rust 的集合类型提供了这些能力，同时保持所有权规则。

---

## 7.1 Vec —— 动态数组

!!! example "核心比喻：Vec 就像一列火车"
    数组像固定长度的站台——建好就不能延长。Vec 像一列火车——你可以随时加挂车厢（push），也可以摘掉车厢（pop），还能在任意位置插入新车厢（insert）。

```rust
fn main() {
    // 创建 Vec
    let mut students: Vec<String> = Vec::new();
    
    // 添加元素
    students.push(String::from("张三"));
    students.push(String::from("李四"));
    students.push(String::from("王五"));
    
    // 使用 vec! 宏创建
    let scores = vec![85, 92, 78, 88, 95];
    
    // 访问元素
    println!("第一个学生: {}", &students[0]);
    println!("第三个成绩: {}", scores[2]);
    
    // 安全访问：get 返回 Option
    match students.get(10) {
        Some(name) => println!("第 11 个学生: {}", name),
        None => println!("没有第 11 个学生"),
    }
    
    // 遍历
    println!("\n===== 学生名单 =====");
    for (i, name) in students.iter().enumerate() {
        println!("{}. {}", i + 1, name);
    }
    
    // 修改元素
    students[0] = String::from("张三丰");
    
    // 删除元素
    students.remove(1);  // 删除索引 1 的元素
    let last = students.pop();  // 删除并返回最后一个元素
    
    println!("\n删除后:");
    for name in &students {
        println!("  {}", name);
    }
    println!("被弹出的: {:?}", last);
    
    // 常用操作
    println!("\n学生数: {}", students.len());
    println!("是否为空: {}", students.is_empty());
    println!("包含张三丰? {}", students.contains(&String::from("张三丰")));
}
```

**运行结果：**
```
第一个学生: 张三
第三个成绩: 78
没有第 11 个学生

===== 学生名单 =====
1. 张三
2. 李四
3. 王五

删除后:
  张三丰
  王五
被弹出的: Some("李四")

学生数: 2
是否为空: false
包含张三丰? true
```

!!! info "Vec 常用方法"
    | 方法 | 作用 |
    |:---|:---|
    | `.push(value)` | 在末尾添加 |
    | `.pop()` | 移除并返回最后一个（`Option`） |
    | `.insert(index, value)` | 在指定位置插入 |
    | `.remove(index)` | 移除指定位置元素 |
    | `.get(index)` | 安全访问（返回 `Option`） |
    | `.len()` | 元素个数 |
    | `.is_empty()` | 是否为空 |
    | `.contains(value)` | 是否包含 |

---

## 7.2 String —— 可变字符串

Rust 有两种字符串类型：

| 类型 | 存储位置 | 可变性 | 说明 |
|:---|:---|:---|:---|
| `&str` | 栈/静态区 | 不可变 | 字符串切片，借用 |
| `String` | 堆 | 可变 | 拥有所有权的字符串 |

```rust
fn main() {
    // 创建 String
    let mut s = String::from("Hello");
    
    // 追加
    s.push_str(", ");
    s.push_str("Rust");
    s.push('!');  // 追加单个字符
    
    println!("{}", s);
    
    // 拼接
    let s1 = String::from("Hello");
    let s2 = String::from("World");
    let s3 = s1 + " " + &s2;  // s1 的所有权被移动
    // println!("{}", s1);  // 编译错误！s1 已被移动
    println!("{}", s3);
    
    // 使用 format! 宏（不获取所有权）
    let s4 = String::from("tic");
    let s5 = String::from("tac");
    let s6 = String::from("toe");
    let game = format!("{}-{}-{}", s4, s5, s6);
    println!("{}", game);
    println!("s4 仍然有效: {}", s4);  // format! 不获取所有权
    
    // 索引与切片
    let hello = String::from("你好世界");
    // println!("{}", &hello[0]);  // 编译错误！不能直接索引
    println!("前 6 字节: {}", &hello[0..6]);  // "你好"
    
    // 遍历字符
    println!("\n逐字符遍历:");
    for c in hello.chars() {
        println!("  {}", c);
    }
    
    // 遍历字节
    println!("\n逐字节遍历:");
    for b in hello.bytes() {
        println!("  {}", b);
    }
}
```

**运行结果：**
```
Hello, Rust!
Hello World
tic-tac-toe
s4 仍然有效: tic
前 6 字节: 你好

逐字符遍历:
  你
  好
  世
  界

逐字节遍历:
  228
  189
  160
  229
  165
  189
  228
  184
  150
  231
  149
  140
```

!!! warning "为什么不能直接索引 String？"
    Rust 的 String 是 UTF-8 编码的。一个字符可能占 1~4 个字节，直接索引 `s[0]` 可能只拿到字符的一部分。Rust 强制你明确意图：是要字节切片（`&s[0..n]`）还是字符迭代（`s.chars()`）。

---

## 7.3 HashMap —— 键值对

```rust
use std::collections::HashMap;

fn main() {
    // 创建 HashMap
    let mut scores = HashMap::new();
    
    // 插入键值对
    scores.insert(String::from("张三"), 85);
    scores.insert(String::from("李四"), 92);
    scores.insert(String::from("王五"), 78);
    
    // 访问值
    let name = String::from("李四");
    match scores.get(&name) {
        Some(score) => println!("{} 的成绩: {}", name, score),
        None => println!("找不到 {}", name),
    }
    
    // 遍历
    println!("\n===== 所有成绩 =====");
    for (name, score) in &scores {
        println!("{}: {} 分", name, score);
    }
    
    // 更新值
    scores.insert(String::from("张三"), 90);  // 覆盖旧值
    println!("\n张三的新成绩: {}", scores.get("张三").unwrap());
    
    // 只在键不存在时插入
    scores.entry(String::from("赵六")).or_insert(88);
    scores.entry(String::from("张三")).or_insert(60);  // 张三已存在，不插入
    println!("张三的成绩（or_insert 后）: {}", scores.get("张三").unwrap());
    println!("赵六的成绩: {}", scores.get("赵六").unwrap());
    
    // 基于旧值更新
    let text = "hello world wonderful world";
    let mut word_count = HashMap::new();
    for word in text.split_whitespace() {
        let count = word_count.entry(word).or_insert(0);
        *count += 1;  // 解引用后修改
    }
    println!("\n词频统计: {:?}", word_count);
}
```

**运行结果：**
```
李四 的成绩: 92

===== 所有成绩 =====
王五: 78 分
张三: 85 分
李四: 92 分

张三的新成绩: 90
张三的成绩（or_insert 后）: 90
赵六的成绩: 88

词频统计: {"world": 2, "hello": 1, "wonderful": 1}
```

---

## 7.4 迭代器

迭代器是 Rust 处理集合的核心抽象：

```rust
fn main() {
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    
    // 创建迭代器
    let mut iter = numbers.iter();
    
    // 逐个消费
    println!("逐个消费:");
    while let Some(n) = iter.next() {
        println!("  {}", n);
    }
    
    // 迭代器适配器（惰性，不立即执行）
    let processed: Vec<i32> = numbers.iter()
        .filter(|&&x| x % 2 == 0)   // 过滤偶数
        .map(|&x| x * x)             // 平方
        .collect();                  // 收集到 Vec
    
    println!("\n偶数的平方: {:?}", processed);
    
    // 消费器（立即执行）
    let sum: i32 = numbers.iter().sum();
    let count = numbers.iter().count();
    let min = numbers.iter().min();
    let max = numbers.iter().max();
    
    println!("\n统计:");
    println!("  总和: {}", sum);
    println!("  个数: {}", count);
    println!("  最小: {:?}", min);
    println!("  最大: {:?}", max);
    
    // 链式操作
    let result: Vec<String> = numbers.iter()
        .filter(|&x| x % 2 != 0)  // 奇数
        .take(3)                    // 取前 3 个
        .map(|x| format!("No.{}", x))
        .collect();
    
    println!("\n前 3 个奇数: {:?}", result);
}
```

**运行结果：**
```
逐个消费:
  1
  2
  3
  4
  5
  6
  7
  8
  9
  10

偶数的平方: [4, 16, 36, 64, 100]

统计:
  总和: 55
  个数: 10
  最小: Some(1)
  最大: Some(10)

前 3 个奇数: ["No.1", "No.3", "No.5"]
```

---

## 要点总结

- [x] `Vec<T>` 是动态数组，用 `push`/`pop` 增删元素
- [x] `&str` 是字符串切片（不可变），`String` 是可变字符串
- [x] `String` 不能直接索引，用 `.chars()` 遍历字符
- [x] `HashMap<K, V>` 是键值对集合
- [x] `.entry().or_insert()` 在键不存在时插入默认值
- [x] 迭代器是惰性的，`.collect()` 触发执行
- [x] `.filter()`、`.map()` 等适配器链式组合

---

## 课后练习

1.  **成绩管理** ：用 `Vec` 存储成绩，实现添加、删除、计算平均分。

2.  **词频统计** ：用 `HashMap` 统计一段文本中每个单词出现的次数。

3.  **迭代器练习** ：用迭代器链式操作，从 1~100 中筛选出能被 3 或 5 整除的数，求它们的平方和。

---

**下一章预告：** 你写了一个排序函数，但只能用于 `i32`。如果要对 `f64` 或 `String` 排序，难道要重写一遍？泛型和 Trait 让你编写一次代码，适用于多种类型。

[继续第 8 章：泛型与 Trait →](08-generics-and-traits.md)