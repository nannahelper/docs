# 第 3 章：连接多张表

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

## 本章练习

查询每位学生完成了多少门课程；找出没有任何学习记录的课程。
