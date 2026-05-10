# 第 3 章：数据清洗与变换

> **场景：** 老师又给了你一份新的数据——来自不同班级、格式不统一、有缺失值、有重复记录。真实世界的数据从来不是干净的。让我们用 tidyverse 工具包把杂乱数据整理成分析就绪的格式。

---

## 3.1 tidyverse：数据科学的瑞士军刀

tidyverse 是 R 最强大的数据处理生态，核心包包括：

| 包 | 用途 | 核心函数 |
|:---|:---|:---|
| **dplyr** | 数据变换 | `filter`, `select`, `mutate`, `summarise`, `arrange` |
| **tidyr** | 数据重塑 | `pivot_longer`, `pivot_wider`, `separate` |
| **ggplot2** | 数据可视化 | `ggplot`, `geom_*` |
| **readr** | 数据读取 | `read_csv`, `write_csv` |
| **stringr** | 字符串处理 | `str_detect`, `str_replace` |

```r
library(tidyverse)  # 一次性加载所有核心包
```

---

## 3.2 管道操作符：`%>%` 和 `|>`

管道让代码从左到右流动，像流水线一样清晰：

```r
# 不用管道：嵌套函数，从内向外读
summarise(group_by(filter(scores, 总评 >= 60), 性别), 平均分 = mean(总评))

# 用管道：从左到右，逻辑清晰
scores %>%
    filter(总评 >= 60) %>%
    group_by(性别) %>%
    summarise(平均分 = mean(总评))
```

**输出效果：** 两种写法结果相同，但管道版本每一步都清晰可读：筛选 → 分组 → 汇总。

---

## 3.3 dplyr 五大核心操作

```r
library(dplyr)

# 1. filter() —— 筛选行
scores %>% filter(总评 >= 85)                    # 成绩 ≥ 85
scores %>% filter(性别 == "女", 总评 >= 80)      # 女生且成绩 ≥ 80

# 2. select() —— 选择列
scores %>% select(姓名, 总评)                    # 只保留两列
scores %>% select(-学号)                         # 删除学号列
scores %>% select(starts_with("期"))             # 选择以"期"开头的列

# 3. mutate() —— 创建/修改列
scores %>%
    mutate(
        总评 = 平时 * 0.3 + 期中 * 0.3 + 期末 * 0.4,
        是否及格 = ifelse(总评 >= 60, "是", "否"),
        排名 = rank(-总评)                       # 降序排名
    )

# 4. arrange() —— 排序
scores %>% arrange(总评)                         # 升序
scores %>% arrange(desc(总评))                   # 降序

# 5. summarise() + group_by() —— 分组汇总
scores %>%
    group_by(性别) %>%
    summarise(
        人数 = n(),
        平均分 = mean(总评),
        最高分 = max(总评),
        最低分 = min(总评),
        标准差 = sd(总评)
    )
```

**输出效果：** 分组汇总结果以 tibble（增强型数据框）形式显示，列对齐美观，自动显示数据类型。

---

## 3.4 处理缺失值

```r
# 模拟含缺失值的数据
df <- data.frame(
    姓名 = c("张三", "李四", "王五", "赵六", "孙七"),
    成绩 = c(85, NA, 78, 92, NA),
    年龄 = c(20, 21, NA, 22, 19)
)

# 查看缺失值
is.na(df)                    # 每个位置是否为 NA
colSums(is.na(df))           # 每列缺失值数量

# 删除含缺失值的行
df %>% drop_na()

# 填充缺失值
df %>%
    mutate(
        成绩 = replace_na(成绩, mean(成绩, na.rm = TRUE)),
        年龄 = replace_na(年龄, median(年龄, na.rm = TRUE))
    )
```

**输出效果：** `colSums(is.na(df))` 显示每列缺失值计数。`replace_na` 用均值/中位数填充缺失值。

---

## 3.5 数据重塑：宽表 ↔ 长表

```r
library(tidyr)

# 宽表（常见格式）
scores_wide <- data.frame(
    姓名 = c("张三", "李四", "王五"),
    平时 = c(85, 92, 78),
    期中 = c(78, 88, 82),
    期末 = c(82, 95, 75)
)

# 宽表 → 长表（ggplot2 喜欢长表格式）
scores_long <- scores_wide %>%
    pivot_longer(
        cols = c(平时, 期中, 期末),
        names_to = "考试类型",
        values_to = "成绩"
    )

# 长表 → 宽表
scores_long %>%
    pivot_wider(
        names_from = "考试类型",
        values_from = "成绩"
    )
```

**输出效果：** 长表中每个学生的三次考试变成三行，新增"考试类型"和"成绩"两列。这种格式更适合 ggplot2 分组绘图。

---

## 3.6 实战：清洗真实数据

```r
library(tidyverse)

# 读取杂乱数据
raw <- read_csv("messy_scores.csv")

# 数据清洗流水线
clean <- raw %>%
    # 1. 重命名列（去掉空格和特殊字符）
    rename(
        学号 = `学生 ID`,
        姓名 = `姓名 `,
        平时成绩 = `平时 成绩`,
        期中成绩 = `期中 成绩`,
        期末成绩 = `期末 成绩`
    ) %>%

    # 2. 去除首尾空格
    mutate(across(where(is.character), str_trim)) %>%

    # 3. 处理缺失值
    mutate(across(ends_with("成绩"), ~ replace_na(.x, 0))) %>%

    # 4. 删除重复行
    distinct(学号, .keep_all = TRUE) %>%

    # 5. 计算总评
    mutate(总评 = 平时成绩 * 0.3 + 期中成绩 * 0.3 + 期末成绩 * 0.4) %>%

    # 6. 添加等级
    mutate(等级 = case_when(
        总评 >= 90 ~ "优秀",
        总评 >= 80 ~ "良好",
        总评 >= 70 ~ "中等",
        总评 >= 60 ~ "及格",
        TRUE ~ "不及格"
    ))

# 查看清洗结果
glimpse(clean)
summary(clean)
```

**输出效果：** `glimpse(clean)` 横向显示每列的名称、数据类型和前几个值。`summary(clean)` 显示每列的统计摘要。

---

## 3.7 连接多个数据表

```r
# 学生信息表
students <- data.frame(
    学号 = c("001", "002", "003", "004"),
    姓名 = c("张三", "李四", "王五", "赵六"),
    班级 = c("1班", "1班", "2班", "2班")
)

# 成绩表
scores <- data.frame(
    学号 = c("001", "002", "003", "004"),
    成绩 = c(85, 92, 78, 88)
)

# 左连接：保留 students 的所有行
students %>%
    left_join(scores, by = "学号")

# 内连接：只保留两表都有的行
students %>%
    inner_join(scores, by = "学号")
```

**输出效果：** 连接后的数据框包含两表的所有列，按学号匹配。

---

## 本章回顾

你现在可以处理真实世界的杂乱数据了！回顾掌握的技能：

- [x] 用 `%>%` 管道构建数据处理流水线
- [x] 用 `filter`/`select`/`mutate`/`arrange`/`summarise` 变换数据
- [x] 用 `group_by` + `summarise` 做分组汇总
- [x] 用 `drop_na`/`replace_na` 处理缺失值
- [x] 用 `pivot_longer`/`pivot_wider` 重塑数据
- [x] 用 `left_join`/`inner_join` 连接多表

---

👉 [进入第 4 章：完成数据分析报告 →](04-practice.md)