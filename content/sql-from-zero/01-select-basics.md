# 第 1 章：表与第一条查询

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 90 分钟 |
| 核心概念 | 表、字段、行、主键、SELECT |
| 核心比喻 | 数据库像有目录的电子档案柜 |
| 实践任务 | 创建课程表并查询课程信息 |
| 难度等级 | ★☆☆☆☆ |

## 1.1 创建练习数据库

打开 SQLite，创建一张课程表：

```sql
CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    hours INTEGER NOT NULL
);
```

插入几条数据：

```sql
INSERT INTO courses (name, category, hours) VALUES
    ('Python', '编程语言', 10),
    ('Linux', '系统与平台', 6),
    ('SQL', '数据与计算', 8);
```

## 1.2 查询列

```sql
SELECT name, hours
FROM courses;
```

`SELECT` 选择要看的列，`FROM` 指定数据来自哪张表。

## 1.3 给结果起名字

```sql
SELECT name AS 课程名称, hours AS 预计小时
FROM courses;
```

## 1.4 表结构的三个问题

设计一张表前，先问：

1. 一行代表什么对象？
2. 哪一列能唯一标识这一行？
3. 哪些字段必须有值？

## ✏️ 课后练习

创建 `students` 表，包含 `id`、`name`、`major` 三列，插入三名学生后查询全部姓名和专业。

## ✅ 验证步骤

执行查询后确认结果只包含请求的列；检查表结构，确认每一行代表一门课程且 `id` 能唯一标识记录。

## 📝 本章总结

- 表由行和列组成，字段描述数据属性。
- `SELECT` 选择列，`FROM` 指定数据来源。
- 设计表前先明确一行代表什么以及如何唯一标识。

## 🔮 下一章预告

下一章会在查询结果上增加筛选、排序和分组统计。
