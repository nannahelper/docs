# 第 10 章：模块与包管理 —— 组织大型项目

> **场景：** 你的学生管理系统代码越来越长，一个 `main.rs` 已经上千行。你需要把代码拆成多个文件——学生模块、成绩模块、文件模块。Rust 的模块系统让你清晰地组织代码，Cargo 让你轻松管理第三方依赖。

---

## 10.1 包（Package）和 Crate

!!! example "核心比喻：包和 Crate 就像出版社和书"
    - **Crate** 是一本书——可以是一本完整的小说（二进制 crate），也可以是一本参考手册（库 crate）
    - **Package** 是出版社——一个出版社可以出一本或多本书，但必须至少有一本
    - **Cargo.toml** 是出版计划——记录书名、版本、需要引用哪些其他书

```
my_project/          ← Package（包）
├── Cargo.toml       ← 包的配置文件
└── src/
    ├── main.rs      ← 二进制 crate 的根（可执行程序）
    └── lib.rs       ← 库 crate 的根（可被其他项目引用）
```

---

## 10.2 模块（Module）

模块让你把代码组织成层次结构：

```rust
// src/lib.rs

// 定义模块
mod student {
    // 默认私有的结构体
    pub struct Student {  // pub 使其公开
        pub name: String,      // pub 字段
        pub student_id: String,
        score: f64,            // 私有字段
    }
    
    impl Student {
        pub fn new(name: String, student_id: String) -> Student {
            Student {
                name,
                student_id,
                score: 0.0,
            }
        }
        
        pub fn set_score(&mut self, score: f64) {
            self.score = score;
        }
        
        pub fn get_score(&self) -> f64 {
            self.score
        }
        
        pub fn grade(&self) -> &str {
            if self.score >= 90.0 { "优秀" }
            else if self.score >= 80.0 { "良好" }
            else if self.score >= 70.0 { "中等" }
            else if self.score >= 60.0 { "及格" }
            else { "不及格" }
        }
    }
}

mod score_manager {
    use std::collections::HashMap;
    use super::student::Student;  // 使用父模块中的类型
    
    pub struct ScoreManager {
        students: HashMap<String, Student>,
    }
    
    impl ScoreManager {
        pub fn new() -> ScoreManager {
            ScoreManager {
                students: HashMap::new(),
            }
        }
        
        pub fn add_student(&mut self, name: String, id: String) {
            let student = Student::new(name, id.clone());
            self.students.insert(id, student);
        }
        
        pub fn set_score(&mut self, id: &str, score: f64) -> Result<(), String> {
            match self.students.get_mut(id) {
                Some(student) => {
                    student.set_score(score);
                    Ok(())
                }
                None => Err(format!("找不到学号: {}", id)),
            }
        }
        
        pub fn list_all(&self) {
            println!("\n===== 学生列表 =====");
            for (id, student) in &self.students {
                println!("{} | {} | {:.1} 分 | {}",
                    student.name, id, student.get_score(), student.grade());
            }
        }
    }
}

// 使用模块
pub fn run() {
    let mut manager = score_manager::ScoreManager::new();
    
    manager.add_student(String::from("张三"), String::from("2024001"));
    manager.add_student(String::from("李四"), String::from("2024002"));
    
    manager.set_score("2024001", 85.5).unwrap();
    manager.set_score("2024002", 92.0).unwrap();
    
    manager.list_all();
}
```

---

## 10.3 多文件模块

当模块变大时，可以拆到单独的文件中：

```
src/
├── main.rs
├── lib.rs
├── student.rs          ← student 模块
└── score_manager/
    ├── mod.rs          ← score_manager 模块的入口
    └── statistics.rs   ← score_manager 的子模块
```

```rust
// src/student.rs
pub struct Student {
    pub name: String,
    pub student_id: String,
    score: f64,
}

impl Student {
    pub fn new(name: String, student_id: String) -> Student {
        Student { name, student_id, score: 0.0 }
    }
    
    pub fn set_score(&mut self, score: f64) {
        self.score = score;
    }
    
    pub fn get_score(&self) -> f64 {
        self.score
    }
    
    pub fn grade(&self) -> &str {
        if self.score >= 90.0 { "优秀" }
        else if self.score >= 80.0 { "良好" }
        else if self.score >= 70.0 { "中等" }
        else if self.score >= 60.0 { "及格" }
        else { "不及格" }
    }
}
```

```rust
// src/main.rs
mod student;
mod score_manager;

fn main() {
    let mut manager = score_manager::ScoreManager::new();
    manager.add_student(String::from("张三"), String::from("2024001"));
    manager.add_student(String::from("李四"), String::from("2024002"));
    manager.set_score("2024001", 85.5).unwrap();
    manager.set_score("2024002", 92.0).unwrap();
    manager.list_all();
}
```

---

## 10.4 use 关键字

`use` 将路径引入作用域，减少重复书写：

```rust
// 引入路径
use std::collections::HashMap;
use std::io::{self, Read, Write};  // 同时引入多个
use std::fs::*;                     // 引入所有公开项（不推荐）

// 使用 as 重命名
use std::io::Result as IoResult;
use std::fmt::Result as FmtResult;

// 重新导出（pub use）
pub use student::Student;  // 外部可以直接 use crate::Student
```

---

## 10.5 使用外部 Crate

在 `Cargo.toml` 中添加依赖：

```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
chrono = "0.4"
```

```rust
use serde::{Serialize, Deserialize};
use chrono::Local;

#[derive(Debug, Serialize, Deserialize)]
struct Task {
    id: u32,
    title: String,
    completed: bool,
    created_at: String,
}

fn main() {
    let task = Task {
        id: 1,
        title: String::from("学习 Rust"),
        completed: false,
        created_at: Local::now().format("%Y-%m-%d %H:%M:%S").to_string(),
    };
    
    // 序列化为 JSON
    let json = serde_json::to_string_pretty(&task).unwrap();
    println!("JSON:\n{}", json);
    
    // 反序列化
    let parsed: Task = serde_json::from_str(&json).unwrap();
    println!("\n解析: {} - {}", parsed.id, parsed.title);
}
```

**运行结果：**
```
JSON:
{
  "id": 1,
  "title": "学习 Rust",
  "completed": false,
  "created_at": "2026-05-10 14:30:00"
}

解析: 1 - 学习 Rust
```

---

## 要点总结

- [x] Package 包含一个或多个 Crate
- [x] 二进制 crate 入口是 `main.rs`，库 crate 入口是 `lib.rs`
- [x] `mod` 声明模块，`pub` 控制可见性
- [x] `use` 引入路径，`as` 重命名
- [x] `pub use` 重新导出
- [x] `super::` 引用父模块
- [x] `Cargo.toml` 的 `[dependencies]` 管理外部 crate

---

## 课后练习

1.  **模块拆分** ：将学生管理系统拆分为 `student`、`manager`、`io` 三个模块。

2.  **外部 Crate** ：使用 `chrono` crate 在程序中显示当前日期时间。

3.  **JSON 序列化** ：使用 `serde` 和 `serde_json` 将学生数据序列化为 JSON。

---

**下一章预告：** 代码写完了，但它真的正确吗？测试是保证代码质量的关键。Rust 内置了测试框架，让你轻松编写单元测试、集成测试和文档测试。

[继续第 11 章：测试与文档 →](11-testing-and-docs.md)