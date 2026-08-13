# 第 5 章：模式匹配 —— Rust 的"瑞士军刀"

> **场景：** 你有一个 `Option` 值，需要判断它是 `Some` 还是 `None`。你有一个枚举，需要根据不同的变体执行不同的逻辑。`match` 表达式是 Rust 中最强大的控制流工具——它不仅能匹配值，还能解构数据，而且编译器会检查你是否覆盖了所有情况。

---

## 5.1 match 表达式

!!! example "核心比喻：match 就像火车站的自动售票机"
    你投入一枚硬币，售票机根据硬币的面值（1 元、5 角、1 角）执行不同的操作。而且售票机有一个"其他"按钮——如果投入的不是硬币，它会退给你。
    
    `match` 就是这样一个"万能匹配器"：你给它一个值，它根据值的不同情况执行不同的代码。

```rust
fn main() {
    let coin = 5;
    
    match coin {
        1 => println!("一角钱"),
        5 => println!("五角钱"),
        10 => println!("一块钱"),
        _ => println!("不是硬币"),  // _ 匹配所有其他情况
    }
}
```

**运行结果：**
```
五角钱
```

### match 作为表达式

`match` 可以返回值：

```rust
fn main() {
    let score = 85;
    
    let grade = match score {
        90..=100 => "优秀",
        80..=89  => "良好",
        70..=79  => "中等",
        60..=69  => "及格",
        0..=59   => "不及格",
        _        => "无效成绩",
    };
    
    println!("{} 分 → {}", score, grade);
}
```

**运行结果：**
```
85 分 → 良好
```

---

## 5.2 匹配枚举

`match` 和枚举是绝配：

```rust
enum OrderStatus {
    Pending,
    Paid,
    Shipped,
    Completed,
    Cancelled(String),  // 取消原因
}

fn describe_status(status: &OrderStatus) -> String {
    match status {
        OrderStatus::Pending => 
            String::from("订单待支付"),
        OrderStatus::Paid => 
            String::from("已支付，准备发货"),
        OrderStatus::Shipped => 
            String::from("已发货，运输中"),
        OrderStatus::Completed => 
            String::from("订单已完成"),
        OrderStatus::Cancelled(reason) => 
            format!("订单已取消，原因: {}", reason),
    }
}

fn main() {
    let orders = vec![
        OrderStatus::Pending,
        OrderStatus::Paid,
        OrderStatus::Shipped,
        OrderStatus::Completed,
        OrderStatus::Cancelled(String::from("不想要了")),
    ];
    
    for (i, status) in orders.iter().enumerate() {
        println!("订单{}: {}", i + 1, describe_status(status));
    }
}
```

**运行结果：**
```
订单1: 订单待支付
订单2: 已支付，准备发货
订单3: 已发货，运输中
订单4: 订单已完成
订单5: 订单已取消，原因: 不想要了
```

---

## 5.3 匹配 Option

```rust
fn main() {
    let numbers = vec![Some(5), None, Some(10), Some(3), None];
    
    let mut sum = 0;
    let mut count = 0;
    
    for num in &numbers {
        match num {
            Some(value) => {
                sum += value;
                count += 1;
            }
            None => {
                // 跳过 None
            }
        }
    }
    
    println!("有效值个数: {}", count);
    println!("总和: {}", sum);
    println!("平均值: {}", if count > 0 { sum as f64 / count as f64 } else { 0.0 });
}
```

**运行结果：**
```
有效值个数: 3
总和: 18
平均值: 6
```

---

## 5.4 if let —— 简洁的条件匹配

当你只关心一种情况时，`if let` 比 `match` 更简洁：

```rust
fn main() {
    let config_max = Some(3u8);
    
    // 使用 match（啰嗦）
    match config_max {
        Some(max) => println!("最大值: {}", max),
        _ => (),  // 什么都不做
    }
    
    // 使用 if let（简洁）
    if let Some(max) = config_max {
        println!("最大值: {}", max);
    }
    
    // if let 也可以配合 else
    let value: Option<i32> = None;
    if let Some(v) = value {
        println!("有值: {}", v);
    } else {
        println!("没有值");
    }
}
```

**运行结果：**
```
最大值: 3
最大值: 3
没有值
```

---

## 5.5 解构与多重匹配

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let point = Point { x: 3, y: 7 };
    
    // 解构结构体
    match point {
        Point { x: 0, y: 0 } => println!("原点"),
        Point { x: 0, y }    => println!("在 y 轴上，y = {}", y),
        Point { x, y: 0 }    => println!("在 x 轴上，x = {}", x),
        Point { x, y }       => println!("坐标: ({}, {})", x, y),
    }
    
    // 匹配多个值
    let x = 2;
    match x {
        1 | 2 | 3 => println!("x 是 1、2 或 3"),
        _ => println!("x 是其他值"),
    }
    
    // 匹配范围
    let age = 25;
    match age {
        0..=12  => println!("儿童"),
        13..=17 => println!("青少年"),
        18..=59 => println!("成年人"),
        _       => println!("老年人"),
    }
    
    // 匹配守卫（额外条件）
    let pair = (3, -2);
    match pair {
        (x, y) if x == y      => println!("相等"),
        (x, y) if x + y == 0  => println!("互为相反数"),
        (x, y)                => println!("({}, {})", x, y),
    }
}
```

**运行结果：**
```
坐标: (3, 7)
x 是 1、2 或 3
成年人
互为相反数
```

---

## 5.6 while let —— 条件循环

```rust
fn main() {
    let mut stack = vec![1, 2, 3];
    
    // 当 pop() 返回 Some 时继续循环
    while let Some(top) = stack.pop() {
        println!("弹出: {}", top);
    }
    println!("栈空了！");
}
```

**运行结果：**
```
弹出: 3
弹出: 2
弹出: 1
栈空了！
```

---

## 要点总结

- [x] `match` 是穷尽的——编译器检查是否覆盖所有情况
- [x] `_` 是通配符，匹配所有其他情况
- [x] `match` 可以作为表达式返回值
- [x] `if let` 是只匹配一种情况的简洁写法
- [x] `while let` 在循环中匹配模式
- [x] 模式可以解构结构体、元组、枚举
- [x] 匹配守卫（`if` 条件）添加额外约束

---

## 课后练习

1.  **成绩等级** ：用 `match` 将百分制成绩转换为 A/B/C/D/F 等级。

2.  **计算器** ：定义 `Operation` 枚举（Add、Subtract、Multiply、Divide），用 `match` 实现计算。

3.  **Option 链** ：用 `match` 处理嵌套的 `Option<Option<i32>>`，提取最内层的值。

---

**下一章预告：** 你已经学会了如何定义数据（结构体/枚举）和处理数据（match）。接下来学习如何组织代码——函数、闭包，以及 Rust 独特的错误处理方式（`Result` 和 `?` 运算符）。

[继续第 6 章：函数与错误处理 →](06-functions-and-errors.md)