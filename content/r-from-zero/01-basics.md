# 第 1 章：你的第一次数据分析

> **场景：** 期末考试结束，老师给了全班 40 名同学的成绩数据（CSV 文件），让你帮忙做统计分析——计算平均分、标准差、分数分布，并找出需要补考的同学。打开 RStudio，让我们开始。

---

## 1.1 从一份成绩单开始

假设 `scores.csv` 内容如下：

| 学号 | 姓名 | 平时 | 期中 | 期末 | 性别 |
|:---|:---|:---|:---|:---|:---|
| 2024001 | 张三 | 85 | 78 | 82 | 男 |
| 2024002 | 李四 | 92 | 88 | 95 | 女 |
| ... | ... | ... | ... | ... | ... |

在 RStudio 中新建脚本 `score_analysis.R`：

```r
# score_analysis.R —— 考试成绩分析

# 1. 读取数据
scores <- read.csv("scores.csv")
head(scores)        # 查看前 6 行
str(scores)         # 查看数据结构

# 2. 计算总评成绩（平时 30% + 期中 30% + 期末 40%）
scores$总评 <- scores$平时 * 0.3 + scores$期中 * 0.3 + scores$期末 * 0.4

# 3. 基本统计
cat("========== 成绩统计 ==========\n")
cat("平均分：", mean(scores$总评), "\n")
cat("中位数：", median(scores$总评), "\n")
cat("标准差：", sd(scores$总评), "\n")
cat("最高分：", max(scores$总评), "\n")
cat("最低分：", min(scores$总评), "\n")

# 4. 分数段统计
scores$等级 <- cut(scores$总评,
                   breaks = c(0, 60, 70, 80, 90, 100),
                   labels = c("不及格", "及格", "中等", "良好", "优秀"))
table(scores$等级)

# 5. 找出需要补考的同学（总评 < 60）
need_retake <- scores[scores$总评 < 60, ]
cat("\n需要补考的同学：\n")
print(need_retake[, c("姓名", "总评")])
```

**输出效果：**

```
========== 成绩统计 ==========
平均分： 78.35 
中位数： 80.5 
标准差： 12.42 
最高分： 96 
最低分： 45 

        不及格   及格   中等   良好   优秀 
            3     5    12    14     6 

需要补考的同学：
    姓名   总评
5   王五   45.0
18  赵六   52.5
33  孙七   58.0
```

---

## 1.2 R 与 RStudio

| 组件 | 作用 |
|:---|:---|
| **R** | 编程语言和计算引擎（后台运行） |
| **RStudio** | 集成开发环境（IDE），提供代码编辑、数据查看、图表显示等功能 |

RStudio 界面分为四个面板：

| 面板 | 位置 | 功能 |
|:---|:---|:---|
| **脚本编辑器** | 左上 | 编写 `.R` 脚本文件 |
| **控制台** | 左下 | 执行代码，显示输出 |
| **环境/历史** | 右上 | 查看变量、命令历史 |
| **文件/绘图/帮助** | 右下 | 浏览文件、显示图表、查看文档 |

---

## 1.3 变量与赋值

R 使用 `<-` 作为赋值符号（也可以用 `=`）：

```r
x <- 42              # 推荐写法
y = 3.14             # 也可以，但 R 社区偏好 <-
name <- "R语言"      # 字符串
is_pass <- TRUE      # 逻辑值

# 查看变量
print(x)
x                    # 直接输入变量名也能显示
```

**输出效果：** 控制台显示 `[1] 42`。`[1]` 表示这是输出的第一个元素。

---

## 1.4 向量：R 的基本数据结构

R 中一切皆向量，单个数值也是长度为 1 的向量：

```r
# 创建向量
scores <- c(85, 92, 78, 88, 95)     # c() 是 combine 的缩写
names <- c("张三", "李四", "王五")

# 序列生成
1:10                                 # 1 到 10
seq(0, 100, by = 10)                 # 0, 10, 20, ..., 100
rep(1, times = 5)                    # 1, 1, 1, 1, 1

# 向量运算（自动向量化）
scores + 5                           # 每人加 5 分
scores * 1.2                         # 每人乘 1.2
sqrt(scores)                         # 开平方

# 索引（从 1 开始！）
scores[1]                            # 第 1 个 → 85
scores[1:3]                          # 第 1~3 个 → 85, 92, 78
scores[scores > 85]                  # 大于 85 的 → 92, 88, 95
```

**输出效果：** 向量运算对每个元素独立执行，结果是与输入等长的向量。索引从 1 开始（不是 0！）。

---

## 1.5 数据框：R 的表格结构

数据框（data.frame）是 R 中最常用的数据结构，类似 Excel 表格：

```r
# 创建数据框
students <- data.frame(
    姓名 = c("张三", "李四", "王五", "赵六"),
    年龄 = c(20, 21, 19, 22),
    成绩 = c(85, 92, 78, 88),
    性别 = c("男", "女", "男", "女"),
    stringsAsFactors = FALSE
)

# 查看数据
print(students)
str(students)        # 结构概览
summary(students)    # 统计摘要

# 访问列
students$成绩                        # $ 符号访问
students[, "成绩"]                   # 按列名
students[1, 3]                       # 第 1 行第 3 列

# 筛选行
students[students$成绩 >= 85, ]      # 成绩 ≥ 85 的学生
students[students$性别 == "女", ]    # 女生
```

**输出效果：** `print(students)` 以表格形式显示数据框。`summary(students)` 对数值列显示最小值、四分位数、中位数、均值、最大值；对字符列显示长度和类别。

---

## 1.6 基本统计函数

```r
scores <- c(85, 92, 78, 88, 95, 45, 72, 83, 90, 67)

mean(scores)         # 均值 → 79.5
median(scores)       # 中位数 → 84
sd(scores)           # 标准差 → 14.9
var(scores)          # 方差
min(scores)          # 最小值 → 45
max(scores)          # 最大值 → 95
range(scores)        # 范围 → 45 95
quantile(scores)     # 四分位数
summary(scores)      # 综合统计摘要
```

**输出效果：** `summary(scores)` 输出：

```
   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
  45.00   73.50   84.00   79.50   89.50   95.00 
```

---

## 1.7 完善成绩分析脚本

```r
# score_analysis_complete.R —— 完整成绩分析
library(ggplot2)

# 读取数据
scores <- read.csv("scores.csv")
scores$总评 <- scores$平时 * 0.3 + scores$期中 * 0.3 + scores$期末 * 0.4

# 统计摘要
cat("========== 成绩分析报告 ==========\n")
cat(sprintf("学生总数：%d\n", nrow(scores)))
cat(sprintf("平均分：%.1f\n", mean(scores$总评)))
cat(sprintf("中位数：%.1f\n", median(scores$总评)))
cat(sprintf("标准差：%.1f\n", sd(scores$总评)))
cat(sprintf("及格率：%.1f%%\n", mean(scores$总评 >= 60) * 100))

# 按性别分组统计
cat("\n--- 按性别统计 ---\n")
by_gender <- aggregate(总评 ~ 性别, data = scores,
                       FUN = function(x) c(均值 = mean(x), 标准差 = sd(x)))
print(by_gender)

# 分数分布直方图
ggplot(scores, aes(x = 总评)) +
    geom_histogram(binwidth = 5, fill = "steelblue", color = "white") +
    geom_vline(xintercept = mean(scores$总评), color = "red", linewidth = 1) +
    labs(title = "成绩分布直方图",
         subtitle = paste("平均分：", round(mean(scores$总评), 1)),
         x = "总评成绩", y = "人数") +
    theme_minimal()
```

**渲染效果：** 控制台输出完整统计报告。图形窗口显示蓝色直方图，红色竖线标记平均分位置。

---

## 本章回顾

你已经用 R 完成了第一次数据分析！回顾掌握的技能：

- [x] 用 `<-` 赋值，理解 R 的向量化特性
- [x] 用 `c()` 创建向量，用 `data.frame()` 创建表格
- [x] 用 `$` 和 `[]` 访问数据框的行列
- [x] 用 `mean()`、`sd()`、`summary()` 等做基本统计
- [x] 用 `read.csv()` 读取外部数据
- [x] 用 `aggregate()` 做分组统计

---

👉 [进入第 2 章：让数据可视化 →](02-syntax.md)