# 第 8 章：泛型与 Trait —— 编写可复用的代码

> **场景：** 你写了一个找最大值的函数，但只能用于 `i32`。如果要对 `f64` 或 `String` 找最大值，难道要重写一遍？泛型让你写一次代码，适用于多种类型。Trait 定义了类型"能做什么"——就像 Java 的接口，但更强大。

---

## 8.1 泛型函数

!!! example "核心比喻：泛型就像自动售货机"
    一台售货机可以卖可乐、雪碧、矿泉水——它不关心具体卖什么，只要商品能放进货道就行。
    
    泛型函数就像这台售货机——它不关心具体类型，只要类型满足要求（实现了某个 Trait）就能工作。

```rust
// 不使用泛型：只能用于 i32
fn largest_i32(list: &[i32]) -> i32 {
    let mut largest = list[0];
    for &item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}

// 使用泛型：适用于任何可比较的类型
fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
    let mut largest = list[0];
    for &item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}

fn main() {
    let numbers = vec![34, 50, 25, 100, 65];
    println!("最大数字: {}", largest(&numbers));
    
    let chars = vec!['y', 'm', 'a', 'q'];
    println!("最大字符: {}", largest(&chars));
}
```

**运行结果：**
```
最大数字: 100
最大字符: y
```

---

## 8.2 泛型结构体

```rust
// 泛型结构体
struct Point<T> {
    x: T,
    y: T,
}

// 多个泛型参数
struct Pair<T, U> {
    first: T,
    second: U,
}

fn main() {
    let integer_point = Point { x: 5, y: 10 };
    let float_point = Point { x: 1.5, y: 4.2 };
    
    println!("整数点: ({}, {})", integer_point.x, integer_point.y);
    println!("浮点点: ({}, {})", float_point.x, float_point.y);
    
    let pair = Pair {
        first: String::from("张三"),
        second: 85,
    };
    println!("{} 的成绩: {}", pair.first, pair.second);
}
```

---

## 8.3 Trait —— 定义共享行为

Trait 告诉 Rust 编译器一个类型能做什么：

```rust
// 定义 Trait
trait Describable {
    fn describe(&self) -> String;
    
    // 默认实现
    fn summary(&self) -> String {
        format!("(详情请查看 describe)")
    }
}

// 为 Student 实现 Describable
struct Student {
    name: String,
    score: f64,
}

impl Describable for Student {
    fn describe(&self) -> String {
        format!("学生 {}，成绩 {:.1} 分", self.name, self.score)
    }
}

// 为 Book 实现 Describable
struct Book {
    title: String,
    author: String,
}

impl Describable for Book {
    fn describe(&self) -> String {
        format!("《{}》作者: {}", self.title, self.author)
    }
}

// 接受实现了 Describable 的类型
fn print_description(item: &impl Describable) {
    println!("{}", item.describe());
}

// 泛型写法（等价于上面）
fn print_description_generic<T: Describable>(item: &T) {
    println!("{}", item.describe());
}

fn main() {
    let student = Student {
        name: String::from("张三"),
        score: 85.5,
    };
    
    let book = Book {
        title: String::from("Rust 编程之道"),
        author: String::from("张汉东"),
    };
    
    print_description(&student);
    print_description(&book);
    
    // 使用默认实现
    println!("student summary: {}", student.summary());
}
```

**运行结果：**
```
学生 张三，成绩 85.5 分
《Rust 编程之道》作者: 张汉东
student summary: (详情请查看 describe)
```

---

## 8.4 常用标准 Trait

### Display 和 Debug

```rust
// Debug：自动派生，用于调试输出
#[derive(Debug)]
struct Student {
    name: String,
    score: f64,
}

// Display：手动实现，用于用户友好的输出
use std::fmt;

impl fmt::Display for Student {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} ({:.1} 分)", self.name, self.score)
    }
}

fn main() {
    let student = Student {
        name: String::from("张三"),
        score: 85.5,
    };
    
    println!("Display: {}", student);    // 用户友好
    println!("Debug: {:?}", student);    // 调试输出
    println!("美化 Debug: {:#?}", student);
}
```

**运行结果：**
```
Display: 张三 (85.5 分)
Debug: Student { name: "张三", score: 85.5 }
美化 Debug: Student {
    name: "张三",
    score: 85.5,
}
```

### Clone 和 Copy

```rust
#[derive(Debug, Clone, Copy)]  // Copy 要求所有字段都实现了 Copy
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug, Clone)]  // String 没有实现 Copy，所以只能 Clone
struct Person {
    name: String,
    age: u32,
}

fn main() {
    let p1 = Point { x: 1, y: 2 };
    let p2 = p1;  // Copy：p1 仍然有效
    println!("p1: {:?}, p2: {:?}", p1, p2);
    
    let person1 = Person {
        name: String::from("张三"),
        age: 20,
    };
    let person2 = person1.clone();  // Clone：显式克隆
    println!("person1: {:?}", person1);
    println!("person2: {:?}", person2);
}
```

---

## 8.5 Trait Bound —— 约束泛型参数

```rust
use std::fmt::Display;

// 要求 T 同时实现 Display 和 PartialOrd
fn compare_and_print<T: Display + PartialOrd>(a: T, b: T) {
    if a > b {
        println!("{} 大于 {}", a, b);
    } else if a < b {
        println!("{} 小于 {}", a, b);
    } else {
        println!("{} 等于 {}", a, b);
    }
}

// 使用 where 子句（更清晰）
fn complex_function<T, U>(t: T, u: U) -> String
where
    T: Display + Clone,
    U: Display + PartialOrd,
{
    format!("T: {}, U: {}", t, u)
}

fn main() {
    compare_and_print(10, 5);
    compare_and_print(3.14, 3.14);
    compare_and_print('a', 'z');
    
    println!("{}", complex_function(42, 3.14));
}
```

**运行结果：**
```
10 大于 5
3.14 等于 3.14
a 小于 z
T: 42, U: 3.14
```

---

## 要点总结

- [x] 泛型 `<T>` 让代码适用于多种类型
- [x] Trait 定义类型的行为契约
- [x] `impl Trait for Type` 为类型实现 Trait
- [x] `impl Trait` 作为参数类型（语法糖）
- [x] `#[derive(Debug, Clone)]` 自动实现常见 Trait
- [x] `Display` 用于用户输出，`Debug` 用于调试
- [x] `Copy` 是隐式复制（栈上数据），`Clone` 是显式克隆
- [x] `where` 子句让复杂的 Trait Bound 更清晰

---

## 课后练习

1.  **可比较的 Pair** ：定义泛型结构体 `Pair<T>`，实现 `largest` 方法返回较大的值。

2.  **自定义 Display** ：为 `Book` 结构体实现 `Display` Trait，格式为 `《书名》- 作者`。

3.  **Trait 练习** ：定义 `Area` Trait（计算面积），为 `Circle` 和 `Rectangle` 实现它。

---

**下一章预告：** 泛型和 Trait 让你编写灵活的代码。但引用的有效期如何保证？生命周期标注让编译器理解引用之间的关系，防止悬垂引用。

[继续第 9 章：生命周期 →](09-lifetimes.md)