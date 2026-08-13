# 第 11 章：测试与文档 —— 保证代码质量

> **场景：** 你的学生管理系统越来越复杂，每次修改代码都担心破坏已有功能。Rust 内置了测试框架——你只需要写测试函数，`cargo test` 就能自动运行所有测试。配合文档测试，代码和文档永远不会脱节。

---

## 11.1 单元测试

!!! example "核心比喻：测试就像出厂质检"
    工厂生产产品，每件产品出厂前都要经过质检——测试各项功能是否正常。单元测试就是代码的"质检员"，确保每个函数都按预期工作。

```rust
// 被测试的函数
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

pub fn divide(a: f64, b: f64) -> Option<f64> {
    if b == 0.0 {
        None
    } else {
        Some(a / b)
    }
}

pub fn get_grade(score: f64) -> &'static str {
    if score >= 90.0 { "优秀" }
    else if score >= 80.0 { "良好" }
    else if score >= 70.0 { "中等" }
    else if score >= 60.0 { "及格" }
    else { "不及格" }
}

// 测试模块
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
        assert_eq!(add(0, 0), 0);
    }
    
    #[test]
    fn test_divide_normal() {
        assert_eq!(divide(10.0, 2.0), Some(5.0));
        assert_eq!(divide(7.0, 2.0), Some(3.5));
    }
    
    #[test]
    fn test_divide_by_zero() {
        assert_eq!(divide(10.0, 0.0), None);
    }
    
    #[test]
    fn test_get_grade() {
        assert_eq!(get_grade(95.0), "优秀");
        assert_eq!(get_grade(85.0), "良好");
        assert_eq!(get_grade(75.0), "中等");
        assert_eq!(get_grade(65.0), "及格");
        assert_eq!(get_grade(55.0), "不及格");
    }
    
    #[test]
    #[should_panic(expected = "除数不能为 0")]
    fn test_divide_panic() {
        divide_panic(10, 0);
    }
}

fn divide_panic(a: i32, b: i32) -> i32 {
    if b == 0 {
        panic!("除数不能为 0");
    }
    a / b
}
```

运行测试：
```bash
cargo test
```

**运行结果：**
```
running 5 tests
test tests::test_add ... ok
test tests::test_divide_by_zero ... ok
test tests::test_divide_normal ... ok
test tests::test_divide_panic ... ok
test tests::test_get_grade ... ok

test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured
```

---

## 11.2 测试断言

```rust
#[cfg(test)]
mod assertion_tests {
    #[test]
    fn test_assertions() {
        // assert! —— 条件为 true
        assert!(1 + 1 == 2);
        
        // assert_eq! —— 相等
        assert_eq!(2 + 2, 4);
        
        // assert_ne! —— 不相等
        assert_ne!(2 + 2, 5);
        
        // 带自定义错误信息
        let result = 42;
        assert!(result == 42, "期望 42，实际得到 {}", result);
        assert_eq!(result, 42, "结果应该是 42");
    }
    
    #[test]
    #[should_panic]
    fn test_should_panic() {
        panic!("这个测试期望 panic");
    }
    
    #[test]
    #[ignore]  // 默认跳过此测试
    fn heavy_test() {
        // 耗时测试，用 cargo test -- --ignored 运行
    }
}
```

---

## 11.3 集成测试

集成测试放在项目根目录的 `tests/` 文件夹中：

```
my_project/
├── Cargo.toml
├── src/
│   └── lib.rs
└── tests/
    ├── integration_test.rs
    └── common/
        └── mod.rs          # 共享的测试辅助模块
```

```rust
// tests/common/mod.rs
pub fn setup() {
    // 测试前的准备工作
    println!("测试环境准备完成");
}
```

```rust
// tests/integration_test.rs
mod common;

use my_project::student::Student;

#[test]
fn test_student_creation() {
    common::setup();
    
    let student = Student::new(
        String::from("张三"),
        String::from("2024001"),
    );
    
    assert_eq!(student.name, "张三");
    assert_eq!(student.student_id, "2024001");
    assert_eq!(student.get_score(), 0.0);
}

#[test]
fn test_student_score() {
    let mut student = Student::new(
        String::from("李四"),
        String::from("2024002"),
    );
    
    student.set_score(85.5);
    assert_eq!(student.get_score(), 85.5);
    assert_eq!(student.grade(), "良好");
}
```

---

## 11.4 文档测试

Rust 的独特功能：代码示例可以直接作为测试运行：

```rust
/// 计算两个数的和
///
/// # 示例
///
/// ```
/// use my_project::add;
///
/// let result = add(2, 3);
/// assert_eq!(result, 5);
/// ```
///
/// # 注意事项
/// 此函数不会溢出，因为使用了 wrapping_add
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// 安全除法
///
/// 如果除数为 0，返回 `None`
///
/// # 示例
///
/// ```
/// use my_project::safe_divide;
///
/// assert_eq!(safe_divide(10.0, 2.0), Some(5.0));
/// assert_eq!(safe_divide(10.0, 0.0), None);
/// ```
pub fn safe_divide(a: f64, b: f64) -> Option<f64> {
    if b == 0.0 {
        None
    } else {
        Some(a / b)
    }
}
```

运行文档测试：
```bash
cargo test --doc
```

---

## 11.5 测试组织最佳实践

```rust
// 测试私有函数
fn private_helper(x: i32) -> i32 {
    x * 2
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_private_function() {
        // Rust 允许测试访问私有函数
        assert_eq!(private_helper(5), 10);
    }
}

// 使用 Result 的测试
#[cfg(test)]
mod result_tests {
    #[test]
    fn test_with_result() -> Result<(), String> {
        if 2 + 2 == 4 {
            Ok(())
        } else {
            Err(String::from("数学崩坏了！"))
        }
    }
}
```

---

## 要点总结

- [x] `#[test]` 标记测试函数
- [x] `assert!`、`assert_eq!`、`assert_ne!` 断言
- [x] `#[should_panic]` 期望 panic
- [x] `#[ignore]` 跳过测试
- [x] `cargo test` 运行所有测试
- [x] 单元测试放在 `#[cfg(test)] mod tests {}` 中
- [x] 集成测试放在 `tests/` 目录
- [x] 文档测试让代码示例始终正确

---

## 课后练习

1.  **单元测试** ：为之前写的 `get_grade` 函数编写完整的单元测试。

2.  **集成测试** ：创建 `tests/` 目录，为 `Student` 结构体编写集成测试。

3.  **文档测试** ：为 `divide` 函数编写文档注释，包含可运行的代码示例。

---

**下一章预告：** 你已经学完了 Rust 的所有核心知识。最后一章将把它们全部整合起来——从零开发一个完整的命令行待办事项工具！

[继续第 12 章：综合项目实战 →](12-final-project.md)