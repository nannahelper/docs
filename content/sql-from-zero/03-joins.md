# 第 3 章：连接多张表

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 35 分钟 |
| 核心概念 | 外键、INNER JOIN、LEFT JOIN、连接条件 |
| 核心比喻 | JOIN 像按编号把两份档案拼成一张工作清单 |
| 实践任务 | 查询课程和学习记录的累计时长 |
| 难度等级 | ★★★☆☆ |

单张表只能回答局部问题。把课程和学习记录分开，再用连接组合信息。

## 3.1 创建学习记录

```sql
CREATE TABLE study_records (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    minutes INTEGER NOT NULL,
    studied_at TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

## 3.2 INNER JOIN

```sql
SELECT courses.name, study_records.minutes, study_records.studied_at
FROM study_records
JOIN courses ON courses.id = study_records.course_id;
```

`ON` 描述两张表如何对应。不要只凭列名相同就猜连接关系。

## 3.3 LEFT JOIN

如果希望把“还没有学习记录的课程”也列出来，使用 `LEFT JOIN`：

```sql
SELECT courses.name, COALESCE(SUM(study_records.minutes), 0) AS total_minutes
FROM courses
LEFT JOIN study_records ON study_records.course_id = courses.id
GROUP BY courses.id, courses.name;
```

## ✏️ 课后练习

查询每位学生完成了多少门课程；找出没有任何学习记录的课程。

## ✅ 验证步骤

准备一门没有学习记录的课程，分别执行 `INNER JOIN` 和 `LEFT JOIN`，确认只有后者会保留这门课程。

## 📝 本章总结

- 外键表达表之间的对应关系。
- `INNER JOIN` 只保留能匹配的记录。
- `LEFT JOIN` 会保留左表全部记录，适合找“没有关联数据”的对象。

## 🔮 下一章预告

下一章会学习如何安全修改数据，以及事务和索引怎样保护数据库。
