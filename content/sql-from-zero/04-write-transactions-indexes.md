# 第 4 章：修改数据、事务与索引

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 40 分钟 |
| 核心概念 | UPDATE、DELETE、事务、COMMIT、ROLLBACK、索引 |
| 核心比喻 | 事务像可撤销的批量操作，索引像档案柜的目录 |
| 实践任务 | 安全修改课程信息并观察查询计划 |
| 难度等级 | ★★★☆☆ |

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

## ✏️ 课后练习

为 `studied_at` 建索引，用 `EXPLAIN QUERY PLAN` 观察查询是否使用了索引。

## ✅ 验证步骤

修改数据前先用相同条件执行 `SELECT`；在事务中检查结果后分别测试 `COMMIT` 和 `ROLLBACK`，确认只有提交后修改才会保留。

## 📝 本章总结

- `UPDATE` 和 `DELETE` 必须确认影响范围。
- 事务让一组修改可以整体提交或撤销。
- 索引能加速查询，但会增加存储和写入成本。

## 🔮 下一章预告

最后一章会把表设计、连接、事务和查询组合成学习记录库。
