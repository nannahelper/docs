# 第 4 章：结构体与枚举 —— 自定义数据类型

> **场景：** 基本类型（`i32`、`String`）不够用——你需要描述一个"学生"（姓名 + 学号 + 成绩），或者一个"订单状态"（待支付 / 已支付 / 已发货 / 已完成）。结构体和枚举让你定义自己的数据类型，就像用积木搭建复杂结构。

---

## 4.1 结构体（Struct）

!!! example "核心比喻：结构体就像填写表格"
    你去医院挂号，护士给你一张表格：姓名、年龄、症状。你把信息填进去，就创建了一个"病人"记录。
    
    结构体就是这张表格的模板——定义了有哪些字段，每个字段是什么类型。创建结构体实例就是"填写表格"。

### 定义和创建结构体

```rust
// 定义结构体
struct Student {
    name: String,
    student_id: String,
    age: u32,
    score: f64,
}

fn main() {
    // 创建结构体实例
    let student1 = Student {
        name: String::from("张三"),
        student_id: String::from("2024001"),
        age: 20,
        score: 85.5,
    };
    
    // 访问字段
    println!("姓名: {}", student1.name);
    println!("学号: {}", student1.student_id);
    println!("年龄: {}", student1.age);
    println!("成绩: {}", student1.score);
}
```

**运行结果：**
```
姓名: 张三
学号: 2024001
年龄: 20
成绩: 85.5
```

### 可变结构体

```rust
fn main() {
    let mut student = Student {
        name: String::from("李四"),
        student_id: String::from("2024002"),
        age: 21,
        score: 78.0,
    };
    
    // 修改字段（整个实例必须是 mut）
    student.score = 92.0;
    println!("{} 的新成绩: {}", student.name, student.score);
}
```

### 字段初始化简写

```rust
fn create_student(name: String, student_id: String) -> Student {
    Student {
        name,         // 等同于 name: name
        student_id,   // 等同于 student_id: student_id
        age: 20,
        score: 0.0,
    }
}
```

### 结构体更新语法

```rust
fn main() {
    let student1 = Student {
        name: String::from("张三"),
        student_id: String::from("2024001"),
        age: 20,
        score: 85.5,
    };
    
    // 基于 student1 创建 student2，只修改部分字段
    let student2 = Student {
        name: String::from("张三丰"),
        student_id: String::from("2024003"),
        ..student1  // 其余字段从 student1 复制
    };
    
    println!("student2: {}, {}, {}", student2.name, student2.age, student2.score);
    // 注意：student1 的 name 和 student_id 仍然有效（它们没被移动）
    // 但 student1 不能再整体使用，因为 score 等字段可能被移动
}
```

---

## 4.2 元组结构体

元组结构体有结构体名字但没有字段名：

```rust
// 元组结构体
struct Color(u8, u8, u8);    // RGB
struct Point(f64, f64, f64); // 3D 坐标

fn main() {
    let red = Color(255, 0, 0);
    let origin = Point(0.0, 0.0, 0.0);
    
    // 通过索引访问
    println!("红色: ({}, {}, {})", red.0, red.1, red.2);
    println!("原点: ({}, {}, {})", origin.0, origin.1, origin.2);
}
```

---

## 4.3 结构体的方法

```rust
struct Student {
    name: String,
    student_id: String,
    score: f64,
}

impl Student {
    // 关联函数（类似静态方法）：没有 self 参数
    fn new(name: String, student_id: String) -> Student {
        Student {
            name,
            student_id,
            score: 0.0,
        }
    }
    
    // 方法：&self 表示不可变借用
    fn introduce(&self) {
        println!("我叫{}，学号{}", self.name, self.student_id);
    }
    
    // 方法：&mut self 表示可变借用
    fn take_exam(&mut self, new_score: f64) {
        self.score = new_score;
        println!("{} 参加了考试，成绩: {}", self.name, self.score);
    }
    
    // 方法：self 表示获取所有权
    fn into_name(self) -> String {
        self.name
    }
    
    // 判断是否及格
    fn is_passed(&self) -> bool {
        self.score >= 60.0
    }
    
    // 获取等级
    fn grade(&self) -> &str {
        if self.score >= 90.0 {
            "优秀"
        } else if self.score >= 80.0 {
            "良好"
        } else if self.score >= 70.0 {
            "中等"
        } else if self.score >= 60.0 {
            "及格"
        } else {
            "不及格"
        }
    }
}

fn main() {
    let mut student = Student::new(
        String::from("张三"),
        String::from("2024001"),
    );
    
    student.introduce();
    student.take_exam(85.5);
    
    println!("及格了吗？ {}", student.is_passed());
    println!("等级: {}", student.grade());
}
```

**运行结果：**
```
我叫张三，学号2024001
张三 参加了考试，成绩: 85.5
及格了吗？ true
等级: 良好
```

---

## 4.4 枚举（Enum）

!!! example "核心比喻：枚举就像多选题的选项"
    一道题有 A、B、C、D 四个选项，答案只能是其中之一。枚举就是定义"所有可能的取值"——一个订单的状态只能是"待支付、已支付、已发货、已完成"中的一个。

```rust
// 简单枚举
enum OrderStatus {
    Pending,    // 待支付
    Paid,       // 已支付
    Shipped,    // 已发货
    Completed,  // 已完成
}

// 带数据的枚举（Rust 的枚举非常强大）
enum Message {
    Quit,                           // 无数据
    Move { x: i32, y: i32 },       // 匿名结构体
    Write(String),                  // 包含 String
    ChangeColor(i32, i32, i32),    // 包含三个 i32
}

fn main() {
    let status = OrderStatus::Paid;
    
    let msg1 = Message::Write(String::from("hello"));
    let msg2 = Message::Move { x: 10, y: 20 };
    let msg3 = Message::ChangeColor(255, 0, 0);
}
```

---

## 4.5 Option 枚举 —— 替代 null

Rust 没有 `null`！取而代之的是 `Option<T>` 枚举：

```rust
// Option 的定义（标准库中）
// enum Option<T> {
//     None,       // 没有值
//     Some(T),    // 有值，包含类型 T 的数据
// }

fn main() {
    let some_number = Some(5);
    let some_string = Some("hello");
    let absent_number: Option<i32> = None;
    
    println!("some_number: {:?}", some_number);
    println!("absent_number: {:?}", absent_number);
}
```

```rust
fn divide(a: f64, b: f64) -> Option<f64> {
    if b == 0.0 {
        None  // 除数为 0，返回 None
    } else {
        Some(a / b)  // 正常结果
    }
}

fn main() {
    let result1 = divide(10.0, 2.0);
    let result2 = divide(10.0, 0.0);
    
    // 处理 Option
    match result1 {
        Some(value) => println!("10 / 2 = {}", value),
        None => println!("不能除以 0！"),
    }
    
    match result2 {
        Some(value) => println!("10 / 0 = {}", value),
        None => println!("不能除以 0！"),
    }
}
```

**运行结果：**
```
10 / 2 = 5
不能除以 0！
```

!!! tip "为什么 Rust 没有 null？"
    null 的发明者 Tony Hoare 称其为"十亿美元的错误"。null 的问题在于：当你使用一个可能为 null 的值时，编译器不会提醒你检查，导致运行时崩溃（NullPointerException）。
    
    Rust 的 `Option<T>` 强制你在使用值之前处理"没有值"的情况，编译器会检查你是否处理了 `None`。

---

## 要点总结

- [x] `struct` 定义结构体，`impl` 块定义方法
- [x] `&self` 不可变借用，`&mut self` 可变借用，`self` 获取所有权
- [x] 关联函数（无 `self`）用 `::` 调用，如 `Student::new()`
- [x] 元组结构体有名字但无字段名
- [x] `enum` 定义枚举，每个变体可以携带不同类型的数据
- [x] `Option<T>` 替代 null，强制处理"无值"情况
- [x] `Some(T)` 表示有值，`None` 表示无值

---

## 课后练习

1.  **图书结构体** ：定义 `Book` 结构体（书名、作者、价格、库存），实现 `new`、`display` 和 `is_available` 方法。

2.  **形状枚举** ：定义 `Shape` 枚举（Circle 带半径、Rectangle 带长宽、Triangle 带三边），实现 `area` 方法。

3.  **安全除法** ：用 `Option<f64>` 实现安全除法函数，除数为 0 时返回 `None`。

---

**下一章预告：** 枚举和 `Option` 通常配合 `match` 使用。模式匹配是 Rust 最强大的特性之一——让你优雅地处理各种情况，编译器还会检查你是否遗漏了某个分支。

[继续第 5 章：模式匹配 →](05-pattern-matching.md)