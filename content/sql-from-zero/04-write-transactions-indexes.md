# 第 4 章：修改数据、事务与索引

## 4.1 修改数据前先确认范围

```sql
UPDATE courses
SET hours = 12
WHERE name = 'Python';
```

`UPDATE` 或 `DELETE` 缺少 `WHERE` 可能影响整张表。先用同样条件执行 `SELECT` 检查目标行。

## 4.2 事务

```sql
BEGIN;

UPDATE courses SET hours = hours + 1 WHERE category = '编程语言';

-- 检查结果后确认
COMMIT;
-- 如果发现不对：ROLLBACK;
```

事务把多条修改绑定成一个整体：要么全部成功，要么全部撤销。

## 4.3 索引

```sql
CREATE INDEX idx_study_records_course_id
ON study_records(course_id);
```

索引像书的目录，能加快查找，但会占用空间，也会增加写入成本。不要给每一列都建索引。

## 本章练习

为 `studied_at` 建索引，用 `EXPLAIN QUERY PLAN` 观察查询是否使用了索引。
