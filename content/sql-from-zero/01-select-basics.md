# 第 1 章：表与第一条查询

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

## 本章练习

创建 `students` 表，包含 `id`、`name`、`major` 三列，插入三名学生后查询全部姓名和专业。
