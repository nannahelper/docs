# 第 2 章：筛选、排序与聚合

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

## 本章练习

查询学习时长最多的课程；再统计每个分类的平均学习时长，并按平均时长从高到低排序。
