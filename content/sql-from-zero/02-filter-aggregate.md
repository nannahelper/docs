# 第 2 章：筛选、排序与聚合

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 35 分钟 |
| 核心概念 | WHERE、ORDER BY、LIMIT、GROUP BY、HAVING |
| 核心比喻 | 查询像给档案柜写一张精确的取件单 |
| 实践任务 | 找出高时长课程并统计分类投入 |
| 难度等级 | ★★☆☆☆ |

## 2.1 WHERE 筛选

```sql
SELECT name, hours
FROM courses
WHERE hours >= 8;
```

多个条件可以使用 `AND`、`OR`：

```sql
SELECT *
FROM courses
WHERE category = '编程语言' AND hours < 12;
```

## 2.2 排序和限制

```sql
SELECT name, hours
FROM courses
ORDER BY hours DESC
LIMIT 2;
```

## 2.3 聚合统计

```sql
SELECT category, COUNT(*) AS course_count, SUM(hours) AS total_hours
FROM courses
GROUP BY category;
```

`GROUP BY` 把行分组，`COUNT`、`SUM`、`AVG` 等函数对每组计算。

## 2.4 HAVING 与 WHERE 的区别

- `WHERE` 在分组前筛选行
- `HAVING` 在分组后筛选结果

```sql
SELECT category, SUM(hours) AS total_hours
FROM courses
GROUP BY category
HAVING total_hours >= 8;
```

## ✏️ 课后练习

查询学习时长最多的课程；再统计每个分类的平均学习时长，并按平均时长从高到低排序。

## ✅ 验证步骤

分别执行明细查询和分组查询，确认 `WHERE` 筛选行，`HAVING` 筛选分组后的结果；检查排序方向是否符合预期。

## 📝 本章总结

- `WHERE` 在分组前筛选行。
- `GROUP BY` 把行组织成分组，聚合函数计算每组结果。
- `HAVING` 用于筛选聚合后的分组。

## 🔮 下一章预告

下一章会把课程表和学习记录表连接起来回答跨表问题。
