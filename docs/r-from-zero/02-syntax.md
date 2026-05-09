# 第 2 章：核心语法

> **R 语言的四大数据结构** —— 向量、矩阵、列表、数据框，以及函数定义。

---

## 2.1 向量（Vector）

向量是 R 最基本的数据结构，是一组**相同类型**元素的集合。

```r
# 创建向量
numbers <- c(1, 2, 3, 4, 5)       # c() 是 combine 的缩写
names <- c("张三", "李四", "王五")
logical <- c(TRUE, FALSE, TRUE)

# 生成序列
1:10                              # 1 到 10 的整数序列
seq(0, 100, by = 10)              # 0, 10, 20, ..., 100
rep("A", 5)                       # 重复 "A" 5 次

# 向量运算（向量化操作，无需循环）
numbers * 2                       # 每个元素乘以 2
numbers + numbers                 # 对应元素相加
sqrt(numbers)                     # 每个元素开平方

# 索引（R 的索引从 1 开始，不是 0！）
numbers[1]                        # 第 1 个元素 → 1
numbers[c(1, 3, 5)]              # 第 1、3、5 个元素
numbers[numbers > 3]             # 条件筛选：大于 3 的元素
```

**运行效果：** 向量化运算是 R 的核心优势——`numbers * 2` 不需要写 for 循环，自动对每个元素执行乘法。索引从 1 开始是 R 区别于大多数编程语言的特点。

## 2.2 矩阵（Matrix）

矩阵是**二维**的、所有元素类型相同的结构。

```r
# 创建矩阵
m <- matrix(1:12, nrow = 3, ncol = 4)
print(m)
#      [,1] [,2] [,3] [,4]
# [1,]    1    4    7   10
# [2,]    2    5    8   11
# [3,]    3    6    9   12

# 矩阵运算
t(m)          # 转置
m %*% t(m)    # 矩阵乘法
rowSums(m)    # 每行求和
colMeans(m)   # 每列求均值

# 索引
m[2, 3]       # 第 2 行第 3 列 → 8
m[1, ]        # 第 1 行全部
m[, 2]        # 第 2 列全部
```

**运行效果：** 矩阵按列填充（默认），输出时带行列索引。矩阵乘法使用专用运算符 `%*%`。

## 2.3 列表（List）

列表是 R 中最灵活的数据结构，可以包含**不同类型**的元素。

```r
# 创建列表
student <- list(
    name = "张三",
    age = 20,
    scores = c(85, 92, 78),
    passed = TRUE
)

# 访问元素
student$name           # $ 符号访问 → "张三"
student[["scores"]]    # 双括号访问 → c(85, 92, 78)
student[[3]]           # 按位置访问 → c(85, 92, 78)

# 列表中可以嵌套列表
course <- list(
    name = "数据分析",
    students = list(
        list(name = "张三", score = 85),
        list(name = "李四", score = 92)
    )
)
```

**运行效果：** 列表像是一个"收纳箱"，每个元素可以有不同的类型和长度。`$` 符号是最常用的访问方式。

## 2.4 数据框（Data Frame）

数据框是 R 中**最重要**的数据结构，类似于 Excel 表格或 SQL 数据表。

```r
# 创建数据框
df <- data.frame(
    name = c("张三", "李四", "王五", "赵六"),
    age = c(20, 21, 19, 22),
    score = c(85, 92, 78, 88),
    stringsAsFactors = FALSE    # 字符串不作为因子
)

# 查看数据框
print(df)
head(df, 2)          # 前 2 行
tail(df, 2)          # 后 2 行
str(df)              # 结构概览
summary(df)          # 描述性统计

# 访问数据
df$name              # 访问列
df[1, 2]             # 第 1 行第 2 列
df[1:2, c("name", "score")]  # 前 2 行的 name 和 score 列

# 筛选
df[df$score > 85, ]  # 成绩大于 85 的行
subset(df, age >= 20 & score > 80)  # 年龄 ≥ 20 且成绩 > 80
```

**运行效果：** 数据框以表格形式展示，`summary()` 自动计算每列的均值、中位数、最大最小值等统计量。

## 2.5 函数定义

```r
# 定义函数
calculate_grade <- function(score) {
    if (score >= 90) {
        return("A")
    } else if (score >= 80) {
        return("B")
    } else if (score >= 70) {
        return("C")
    } else {
        return("D")
    }
}

# 调用函数
calculate_grade(85)   # → "B"

# 批量应用
df$grade <- sapply(df$score, calculate_grade)
print(df)
```

**运行效果：** `sapply()` 将函数应用到向量的每个元素，返回结果向量。这是 R 函数式编程风格的体现。

---

## 本章要点总结

- [ ] 掌握向量 `c()` 的创建和向量化运算
- [ ] 理解矩阵 `matrix()` 的创建和索引
- [ ] 会用列表 `list()` 存储异构数据
- [ ] 熟练掌握数据框 `data.frame()` 的操作
- [ ] 能定义和调用自定义函数

---

👉 [进入第 3 章：常用技巧 →](03-tips.md)