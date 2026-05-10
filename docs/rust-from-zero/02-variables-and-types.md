# 第 2 章：变量与数据类型 —— Rust 的"储物规则"

> **场景：** 你需要存储学生的姓名、年龄、成绩。在 Java 中，你声明一个变量然后随意修改。但在 Rust 中，变量默认是"只读"的——这是 Rust 安全哲学的第一课：默认不可变，明确才可变。

---

## 2.1 变量的不可变性

!!! example "核心比喻：Rust 的变量就像签了字的合同"
    在 Java 中，变量就像便利贴——写了可以擦掉重写。
    
    在 Rust 中，变量就像签了字的合同——一旦签署（赋值），就不能随意涂改。如果你想改，必须明确标注"这份合同允许修改"（加 `mut` 关键字）。
    
    这种设计让你在写代码时就明确知道：哪些数据会变，哪些不会。

```rust
fn main() {
    // 默认不可变
    let x = 5;
    println!("x = {}", x);
    
    // x = 6;  // 编译错误！x 是不可变的
    
    // 可变变量：加 mut 关键字
    let mut y = 10;
    println!("修改前: y = {}", y);
    y = 20;
    println!("修改后: y = {}", y);
    
    // 常量：用 const 声明，必须标注类型，全大写命名
    const MAX_STUDENTS: u32 = 50;
    println!("最大学生数: {}", MAX_STUDENTS);
}
```

**运行结果：**
```
x = 5
修改前: y = 10
修改后: y = 20
最大学生数: 50
```

| 对比 | `let` | `let mut` | `const` |
|:---|:---|:---|:---|
| 可变性 | 不可变 | 可变 | 永远不可变 |
| 类型标注 | 可省略（类型推断） | 可省略 | 必须标注 |
| 作用域 | 代码块内 | 代码块内 | 全局 |
| 运行时计算 | 可以 | 可以 | 只能是编译期常量 |

---

## 2.2 变量遮蔽（Shadowing）

Rust 允许用 `let` 重新声明同名变量，这会"遮蔽"之前的变量：

```rust
fn main() {
    let x = 5;
    println!("x = {}", x);  // 5
    
    let x = x + 1;  // 用 let 重新声明，遮蔽旧的 x
    println!("x = {}", x);  // 6
    
    // 甚至可以改变类型
    let spaces = "   ";           // &str 类型
    let spaces = spaces.len();    // usize 类型
    println!("空格数: {}", spaces);  // 3
    
    // 但 mut 不能改变类型
    let mut y = "hello";
    // y = y.len();  // 编译错误！类型不匹配
}
```

**运行结果：**
```
x = 5
x = 6
空格数: 3
```

!!! tip "遮蔽 vs mut"
    | 特性 | `let` 遮蔽 | `let mut` |
    |:---|:---|:---|
    | 改变值 | ✅ | ✅ |
    | 改变类型 | ✅ | ❌ |
    | 是否可变 | 新变量不可变 | 变量可变 |

---

## 2.3 标量类型

Rust 有四种基本标量类型：

### 整数类型

| 长度 | 有符号 | 无符号 |
|:---|:---|:---|
| 8 位 | `i8` | `u8` |
| 16 位 | `i16` | `u16` |
| 32 位 | `i32` | `u32` |
| 64 位 | `i64` | `u64` |
| 128 位 | `i128` | `u128` |
| 架构相关 | `isize` | `usize` |

```rust
fn main() {
    // 默认整数类型是 i32
    let a = 42;
    
    // 显式标注类型
    let b: u8 = 255;
    let c: i64 = -9_223_372_036_854_775_808;
    
    // 数字分隔符（提高可读性）
    let million = 1_000_000;
    let binary = 0b1111_0000;  // 二进制
    let octal = 0o77;           // 八进制
    let hex = 0xFF;             // 十六进制
    
    println!("a = {}, b = {}, c = {}", a, b, c);
    println!("million = {}, binary = {}, octal = {}, hex = {}", 
             million, binary, octal, hex);
}
```

**运行结果：**
```
a = 42, b = 255, c = -9223372036854775808
million = 1000000, binary = 240, octal = 63, hex = 255
```

!!! warning "整数溢出"
    在 debug 模式下，整数溢出会导致程序 panic（崩溃）。在 release 模式下，溢出会回绕（如 `255u8 + 1 = 0`）。

### 浮点类型

```rust
fn main() {
    let x = 2.0;        // 默认 f64
    let y: f32 = 3.0;   // f32
    
    let pi = 3.141592653589793;
    
    println!("x = {}, y = {}", x, y);
    println!("pi = {}", pi);
    println!("pi 保留两位: {:.2}", pi);
}
```

**运行结果：**
```
x = 2, y = 3
pi = 3.141592653589793
pi 保留两位: 3.14
```

### 布尔类型

```rust
fn main() {
    let is_rust_fun = true;
    let is_java_hard: bool = false;
    
    println!("Rust 有趣吗？ {}", is_rust_fun);
    println!("Java 难吗？ {}", is_java_hard);
}
```

### 字符类型

```rust
fn main() {
    let c = 'A';
    let z = '中';       // Rust 的 char 是 4 字节，支持 Unicode
    let emoji = '🦀';   // 甚至支持 emoji！
    
    println!("{} {} {}", c, z, emoji);
}
```

**运行结果：**
```
A 中 🦀
```

---

## 2.4 复合类型

### 元组（Tuple）

元组将多个不同类型的值组合在一起：

```rust
fn main() {
    // 创建元组
    let student: (&str, u32, f64) = ("张三", 20, 85.5);
    
    // 解构（拆开）
    let (name, age, score) = student;
    println!("姓名: {}, 年龄: {}, 成绩: {}", name, age, score);
    
    // 通过索引访问（从 0 开始）
    println!("姓名: {}", student.0);
    println!("年龄: {}", student.1);
    println!("成绩: {}", student.2);
    
    // 元组用于多返回值
    let (sum, diff) = calculate(10, 3);
    println!("和: {}, 差: {}", sum, diff);
}

fn calculate(a: i32, b: i32) -> (i32, i32) {
    (a + b, a - b)  // 返回元组
}
```

**运行结果：**
```
姓名: 张三, 年龄: 20, 成绩: 85.5
姓名: 张三
年龄: 20
成绩: 85.5
和: 13, 差: 7
```

### 数组（Array）

Rust 的数组是固定长度的，所有元素类型相同：

```rust
fn main() {
    // 创建数组
    let scores: [i32; 5] = [85, 92, 78, 88, 95];
    
    // 创建全 0 的数组（类型; 长度）
    let zeros = [0; 10];  // [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    // 访问元素
    println!("第一个成绩: {}", scores[0]);
    println!("数组长度: {}", scores.len());
    
    // 遍历数组
    println!("\n===== 所有成绩 =====");
    for (i, score) in scores.iter().enumerate() {
        println!("学生{}: {} 分", i + 1, score);
    }
    
    // 计算总分
    let sum: i32 = scores.iter().sum();
    let avg = sum as f64 / scores.len() as f64;
    println!("\n总分: {}, 平均: {:.1}", sum, avg);
}
```

**运行结果：**
```
第一个成绩: 85
数组长度: 5

===== 所有成绩 =====
学生1: 85 分
学生2: 92 分
学生3: 78 分
学生4: 88 分
学生5: 95 分

总分: 438, 平均: 87.6
```

!!! danger "数组越界"
    Rust 在运行时检查数组索引。访问 `scores[10]` 会导致程序 panic（崩溃），而不是像 C 那样读取到未知内存。这是 Rust 的安全保证之一。

---

## 2.5 类型转换

Rust 的类型转换非常严格，必须显式进行：

```rust
fn main() {
    let a: i32 = 42;
    let b: u8 = 10;
    
    // 使用 as 进行类型转换
    let c = a + b as i32;
    println!("a + b = {}", c);
    
    // 浮点转整数（截断小数部分）
    let pi = 3.14159;
    let pi_int = pi as i32;
    println!("pi 转整数: {}", pi_int);  // 3
    
    // 整数转浮点
    let x = 5;
    let y = 2;
    let result = x as f64 / y as f64;
    println!("{} / {} = {}", x, y, result);  // 2.5
}
```

**运行结果：**
```
a + b = 52
pi 转整数: 3
5 / 2 = 2.5
```

---

## 要点总结

- [x] 变量默认不可变（`let`），可变需加 `mut`
- [x] `const` 声明常量，必须标注类型
- [x] 变量遮蔽（Shadowing）允许用 `let` 重新声明同名变量
- [x] 整数默认 `i32`，浮点默认 `f64`
- [x] 元组可以存不同类型，数组只能存同类型且长度固定
- [x] 类型转换用 `as` 关键字，必须显式进行
- [x] Rust 在运行时检查数组越界，保证安全

---

## 课后练习

1.  **温度转换** ：将摄氏 37.5 度转换为华氏度（$F = C \times 1.8 + 32$），使用 `f64` 类型。

2.  **元组练习** ：创建一个元组存储一本书的信息（书名、作者、价格、库存），然后解构打印。

3.  **数组统计** ：创建一个包含 10 个成绩的数组，计算最高分、最低分和平均分。

---

**下一章预告：** 变量和数据类型是基础，但 Rust 最独特的概念是所有权——它让 Rust 在没有垃圾回收的情况下保证内存安全。这是 Rust 学习中最重要的一章。

[继续第 3 章：所有权与借用 →](03-ownership.md)