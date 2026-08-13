# SQL 新手指南

SQL 是和数据库沟通的语言。本教程用 SQLite 从查询开始，逐步学习连接、聚合、事务和索引，最后交付一个学习记录库。

| 项目 | 内容 |
|---|---|
| 适合人群 | 会使用电脑，想学习数据处理或后端基础的初学者 |
| 预计时长 | 约 3–4 小时（包含练习） |
| 适用版本 | SQLite 3.x；语法以 SQL 标准为主 |
| 维护状态 | 维护中 |
| 最后更新 | 2026-08-13 |
| 反馈入口 | [GitHub Issues](https://github.com/nannahelper/docs/issues) |

## 🎯 学习目标

- 能创建表并写出可读的查询。
- 能使用筛选、排序、聚合和多表连接回答问题。
- 能安全地修改数据，并理解事务和索引的作用。
- 完成一个记录课程学习时长的 SQLite 数据库。

## 📋 前置要求

- 会使用终端启动 SQLite。
- 能阅读简单的表格和字段定义。
- 不要求提前学习数据库。

## 📚 推荐教材

- [数据库系统概论](https://lilybre.lilystudio.space/book/423) —— 适合系统理解数据库概念
- [DAMA-DMBOK: Data Management Body of Knowledge](https://lilybre.lilystudio.space/book/465) —— 适合作为数据管理参考

## 🗺️ 学习路线

本课程用“课程库和学习记录”作为贯穿案例，每章都会在前一章的数据结构上继续扩展。

| 章节 | 核心目标 | 入口 |
|:---|:---|:---|
| 第 1 章 | 表与第一条查询 | [进入章节](01-select-basics.md) |
| 第 2 章 | 筛选、排序与聚合 | [进入章节](02-filter-aggregate.md) |
| 第 3 章 | 连接多张表 | [进入章节](03-joins.md) |
| 第 4 章 | 修改数据、事务与索引 | [进入章节](04-write-transactions-indexes.md) |
| 第 5 章 | 综合项目：学习记录库 | [进入章节](05-project.md) |

!!! warning "练习环境"
    本教程使用 SQLite 本地数据库。练习数据都是自己创建的，不要直接在生产数据库中尝试修改语句。

反馈入口：[GitHub Issues](https://github.com/nannahelper/docs/issues)
