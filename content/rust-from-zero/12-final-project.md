# 第 12 章：综合项目实战 —— 命令行待办事项工具

> **场景：** 你已经学完了 Rust 的核心知识——所有权、结构体、枚举、模式匹配、集合、错误处理、模块、测试。现在是时候把它们全部整合起来，从零开发一个完整的命令行待办事项（Todo）工具。这个项目将是你 Rust 学习之路的"毕业设计"。

---

## 12.1 项目需求

开发一个命令行待办事项管理工具，支持以下功能：

| 功能 | 命令 | 说明 |
|:---|:---|:---|
| 添加任务 | `add <标题>` | 添加新的待办事项 |
| 列出任务 | `list` | 显示所有任务 |
| 完成任务 | `done <ID>` | 标记任务为已完成 |
| 删除任务 | `remove <ID>` | 删除指定任务 |
| 搜索任务 | `search <关键词>` | 按标题搜索 |
| 统计信息 | `stats` | 显示完成率等统计 |
| 保存/加载 | 自动 | 数据持久化到 JSON 文件 |

---

## 12.2 项目结构

```
todo_cli/
├── Cargo.toml
└── src/
    ├── main.rs          # 程序入口 + 命令解析
    ├── task.rs          # 任务数据结构
    ├── manager.rs       # 任务管理器
    └── storage.rs       # 文件读写
```

---

## 12.3 完整代码

### Cargo.toml

```toml
[package]
name = "todo_cli"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
chrono = "0.4"
```

### task.rs —— 任务数据结构

```rust
use serde::{Serialize, Deserialize};
use chrono::{Local, NaiveDateTime};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Task {
    pub id: u32,
    pub title: String,
    pub completed: bool,
    pub created_at: String,
    pub completed_at: Option<String>,
}

impl Task {
    pub fn new(id: u32, title: String) -> Task {
        Task {
            id,
            title,
            completed: false,
            created_at: Local::now().format("%Y-%m-%d %H:%M:%S").to_string(),
            completed_at: None,
        }
    }
    
    pub fn mark_done(&mut self) {
        self.completed = true;
        self.completed_at = Some(Local::now().format("%Y-%m-%d %H:%M:%S").to_string());
    }
    
    pub fn display(&self) -> String {
        let status = if self.completed { "✅" } else { "⬜" };
        let completed_info = match &self.completed_at {
            Some(time) => format!(" | 完成于: {}", time),
            None => String::new(),
        };
        format!(
            "{} [{}] {} (创建于: {}){}",
            status, self.id, self.title, self.created_at, completed_info
        )
    }
}
```

### storage.rs —— 文件读写

```rust
use std::fs;
use std::io;
use std::path::Path;
use crate::task::Task;

const DATA_FILE: &str = "tasks.json";

pub fn save_tasks(tasks: &[Task]) -> Result<(), io::Error> {
    let json = serde_json::to_string_pretty(tasks)
        .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;
    fs::write(DATA_FILE, json)?;
    Ok(())
}

pub fn load_tasks() -> Result<Vec<Task>, io::Error> {
    if !Path::new(DATA_FILE).exists() {
        return Ok(Vec::new());
    }
    
    let content = fs::read_to_string(DATA_FILE)?;
    let tasks: Vec<Task> = serde_json::from_str(&content)
        .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;
    Ok(tasks)
}
```

### manager.rs —— 任务管理器

```rust
use crate::task::Task;
use crate::storage;

pub struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
}

impl TaskManager {
    pub fn new() -> TaskManager {
        let tasks = storage::load_tasks().unwrap_or_else(|e| {
            eprintln!("加载数据失败: {}，使用空列表", e);
            Vec::new()
        });
        
        let next_id = tasks.iter()
            .map(|t| t.id)
            .max()
            .map(|id| id + 1)
            .unwrap_or(1);
        
        TaskManager { tasks, next_id }
    }
    
    pub fn add(&mut self, title: String) {
        let task = Task::new(self.next_id, title);
        println!("添加任务: {}", task.display());
        self.tasks.push(task);
        self.next_id += 1;
        self.save();
    }
    
    pub fn list(&self) {
        if self.tasks.is_empty() {
            println!("暂无任务。用 'add <标题>' 添加一个吧！");
            return;
        }
        
        println!("\n===== 待办事项（共 {} 项）=====", self.tasks.len());
        for task in &self.tasks {
            println!("{}", task.display());
        }
    }
    
    pub fn done(&mut self, id: u32) {
        match self.tasks.iter_mut().find(|t| t.id == id) {
            Some(task) => {
                if task.completed {
                    println!("任务 [{}] 已经完成了！", id);
                } else {
                    task.mark_done();
                    println!("完成任务: {}", task.display());
                    self.save();
                }
            }
            None => println!("找不到任务 [{}]", id),
        }
    }
    
    pub fn remove(&mut self, id: u32) {
        if let Some(pos) = self.tasks.iter().position(|t| t.id == id) {
            let task = self.tasks.remove(pos);
            println!("已删除: {}", task.display());
            self.save();
        } else {
            println!("找不到任务 [{}]", id);
        }
    }
    
    pub fn search(&self, keyword: &str) {
        let results: Vec<&Task> = self.tasks.iter()
            .filter(|t| t.title.contains(keyword))
            .collect();
        
        if results.is_empty() {
            println!("没有找到包含 '{}' 的任务", keyword);
        } else {
            println!("\n===== 搜索结果（{} 条）=====", results.len());
            for task in results {
                println!("{}", task.display());
            }
        }
    }
    
    pub fn stats(&self) {
        let total = self.tasks.len();
        let completed = self.tasks.iter().filter(|t| t.completed).count();
        let pending = total - completed;
        let rate = if total > 0 {
            (completed as f64 / total as f64) * 100.0
        } else {
            0.0
        };
        
        println!("\n===== 统计信息 =====");
        println!("总任务数: {}", total);
        println!("已完成:   {} ({:.1}%)", completed, rate);
        println!("待完成:   {}", pending);
        
        // 进度条
        let bar_width = 30;
        let filled = (rate / 100.0 * bar_width as f64) as usize;
        let empty = bar_width - filled;
        println!("进度: [{}{}]", "█".repeat(filled), "░".repeat(empty));
    }
    
    fn save(&self) {
        if let Err(e) = storage::save_tasks(&self.tasks) {
            eprintln!("保存失败: {}", e);
        }
    }
}
```

### main.rs —— 程序入口

```rust
mod task;
mod manager;
mod storage;

use manager::TaskManager;
use std::io::{self, Write};

fn main() {
    println!("========================================");
    println!("     Rust 待办事项管理器 v1.0");
    println!("========================================");
    println!("命令: add | list | done | remove | search | stats | help | exit");
    
    let mut manager = TaskManager::new();
    
    loop {
        print!("\n> ");
        io::stdout().flush().unwrap();
        
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        let input = input.trim();
        
        if input.is_empty() {
            continue;
        }
        
        let parts: Vec<&str> = input.splitn(2, ' ').collect();
        let command = parts[0].to_lowercase();
        let args = parts.get(1).unwrap_or(&"");
        
        match command.as_str() {
            "add" => {
                if args.is_empty() {
                    println!("用法: add <任务标题>");
                } else {
                    manager.add(args.to_string());
                }
            }
            "list" => manager.list(),
            "done" => {
                match args.parse::<u32>() {
                    Ok(id) => manager.done(id),
                    Err(_) => println!("用法: done <任务ID>"),
                }
            }
            "remove" | "rm" => {
                match args.parse::<u32>() {
                    Ok(id) => manager.remove(id),
                    Err(_) => println!("用法: remove <任务ID>"),
                }
            }
            "search" => {
                if args.is_empty() {
                    println!("用法: search <关键词>");
                } else {
                    manager.search(args);
                }
            }
            "stats" => manager.stats(),
            "help" => print_help(),
            "exit" | "quit" => {
                println!("再见！");
                break;
            }
            _ => println!("未知命令: '{}'。输入 'help' 查看帮助。", command),
        }
    }
}

fn print_help() {
    println!("\n===== 可用命令 =====");
    println!("  add <标题>    - 添加新任务");
    println!("  list          - 列出所有任务");
    println!("  done <ID>     - 标记任务为已完成");
    println!("  remove <ID>   - 删除任务");
    println!("  search <关键词> - 搜索任务");
    println!("  stats         - 显示统计信息");
    println!("  help          - 显示此帮助");
    println!("  exit          - 退出程序");
}
```

---

## 12.4 运行演示

```
========================================
     Rust 待办事项管理器 v1.0
========================================
命令: add | list | done | remove | search | stats | help | exit

> add 学习 Rust 所有权
添加任务: ⬜ [1] 学习 Rust 所有权 (创建于: 2026-05-10 14:30:00)

> add 完成课后练习
添加任务: ⬜ [2] 完成课后练习 (创建于: 2026-05-10 14:30:15)

> add 阅读 Rust Book
添加任务: ⬜ [3] 阅读 Rust Book (创建于: 2026-05-10 14:30:30)

> list

===== 待办事项（共 3 项）=====
⬜ [1] 学习 Rust 所有权 (创建于: 2026-05-10 14:30:00)
⬜ [2] 完成课后练习 (创建于: 2026-05-10 14:30:15)
⬜ [3] 阅读 Rust Book (创建于: 2026-05-10 14:30:30)

> done 1
完成任务: ✅ [1] 学习 Rust 所有权 (创建于: 2026-05-10 14:30:00) | 完成于: 2026-05-10 15:00:00

> stats

===== 统计信息 =====
总任务数: 3
已完成:   1 (33.3%)
待完成:   2
进度: [██████████░░░░░░░░░░░░░░░░░░░░]

> search Rust

===== 搜索结果（2 条）=====
✅ [1] 学习 Rust 所有权 (创建于: 2026-05-10 14:30:00) | 完成于: 2026-05-10 15:00:00
⬜ [3] 阅读 Rust Book (创建于: 2026-05-10 14:30:30)

> exit
再见！
```

---

## 12.5 项目总结

!!! tip "这个项目用到的知识点"
    | 知识点 | 在项目中的应用 |
    |:---|:---|
    | 结构体与方法 | `Task` 结构体 + `impl` 方法 |
    | 枚举 | `Option<String>` 表示可选的完成时间 |
    | 所有权与借用 | `&self`、`&mut self`、`&[Task]` |
    | 模式匹配 | `match` 解析命令和参数 |
    | 集合类型 | `Vec<Task>` 存储任务列表 |
    | 错误处理 | `Result` + `?` 运算符处理文件 I/O |
    | 迭代器 | `.iter().filter().collect()` 搜索任务 |
    | 模块系统 | `mod task; mod manager; mod storage;` |
    | 外部 Crate | `serde`、`serde_json`、`chrono` |
    | 文件 I/O | JSON 序列化/反序列化持久化数据 |

---

## 课后练习

1.  **功能扩展** ：添加"优先级"字段（高/中/低），支持按优先级排序。

2.  **截止日期** ：为任务添加截止日期，列出时高亮显示已过期的任务。

3.  **撤销完成** ：添加 `undo <ID>` 命令，将已完成的任务恢复为未完成。

---

🎉 **恭喜你完成了 Rust 新手指南的全部内容！** 你已经掌握了 Rust 编程的核心知识——所有权、借用、生命周期、泛型、Trait、错误处理、模块系统。接下来可以继续学习 Rust 高级特性（并发编程、异步 I/O、宏编程）或探索 WebAssembly、嵌入式开发等应用领域。