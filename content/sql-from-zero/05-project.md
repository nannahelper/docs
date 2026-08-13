# 第 5 章：综合项目——学习记录库

完成一个小型数据库，支持：

- 维护课程信息
- 记录某天学习了某门课多少分钟
- 查询每门课累计学习时间
- 查询某个分类的学习投入

## 建议表结构

```text
courses
  id, name, category, hours

study_records
  id, course_id, minutes, studied_at
```

## 验收查询

```sql
SELECT
    c.name,
    COALESCE(SUM(r.minutes), 0) AS total_minutes
FROM courses AS c
LEFT JOIN study_records AS r ON r.course_id = c.id
GROUP BY c.id, c.name
ORDER BY total_minutes DESC;
```

## 继续升级

- 增加学生表并记录每位学生的学习情况
- 添加课程完成状态
- 为重复课程名增加唯一约束
- 把查询封装到 Python 程序中
- 给数据库初始化脚本加入版本号

完成后，你应该能解释每张表的职责、每个连接条件的含义，以及为什么某些查询需要索引。
