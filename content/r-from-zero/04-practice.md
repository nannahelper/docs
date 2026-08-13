# 第 4 章：完成数据分析报告

> **场景：** 你掌握了 R 的核心技能，现在来完成一个端到端的数据分析项目——从原始数据到精美的分析报告，展示你的完整能力。

---

## 4.1 项目：考试成绩综合分析

```r
# complete_analysis.R —— 考试成绩综合分析
library(tidyverse)

# ========== 1. 数据准备 ==========
set.seed(42)
n <- 100

scores <- tibble(
    学号 = sprintf("2024%03d", 1:n),
    姓名 = paste0("学生", 1:n),
    班级 = sample(c("1班", "2班", "3班"), n, replace = TRUE),
    性别 = sample(c("男", "女"), n, replace = TRUE, prob = c(0.55, 0.45)),
    平时 = round(rnorm(n, mean = 80, sd = 10)),
    期中 = round(rnorm(n, mean = 75, sd = 12)),
    期末 = round(rnorm(n, mean = 78, sd = 11))
) %>%
    mutate(
        across(c(平时, 期中, 期末), ~ pmax(0, pmin(100, .x))),
        总评 = 平时 * 0.3 + 期中 * 0.3 + 期末 * 0.4,
        等级 = case_when(
            总评 >= 90 ~ "优秀",
            总评 >= 80 ~ "良好",
            总评 >= 70 ~ "中等",
            总评 >= 60 ~ "及格",
            TRUE ~ "不及格"
        )
    )

# ========== 2. 统计摘要 ==========
cat("========== 考试成绩综合分析报告 ==========\n\n")

cat("--- 整体统计 ---\n")
scores %>%
    summarise(
        学生总数 = n(),
        平均分 = mean(总评),
        中位数 = median(总评),
        标准差 = sd(总评),
        及格率 = mean(总评 >= 60) * 100
    ) %>%
    print()

cat("\n--- 按班级统计 ---\n")
scores %>%
    group_by(班级) %>%
    summarise(
        人数 = n(),
        平均分 = round(mean(总评), 1),
        及格率 = round(mean(总评 >= 60) * 100, 1)
    ) %>%
    print()

cat("\n--- 按性别统计 ---\n")
scores %>%
    group_by(性别) %>%
    summarise(
        人数 = n(),
        平均分 = round(mean(总评), 1),
        标准差 = round(sd(总评), 1)
    ) %>%
    print()

# ========== 3. 统计检验 ==========
cat("\n--- 统计检验 ---\n")

# t 检验：男女生成绩是否有显著差异
t_test <- t.test(总评 ~ 性别, data = scores)
cat(sprintf("男女生成绩差异 t 检验：t = %.3f, p = %.4f\n",
            t_test$statistic, t_test$p.value))

# 方差分析：不同班级成绩是否有显著差异
anova_result <- aov(总评 ~ 班级, data = scores)
cat(sprintf("班级间差异 ANOVA：F = %.3f, p = %.4f\n",
            summary(anova_result)[[1]]$`F value`[1],
            summary(anova_result)[[1]]$`Pr(>F)`[1]))

# ========== 4. 可视化 ==========
# 图 1：成绩分布直方图 + 密度曲线
p1 <- ggplot(scores, aes(x = 总评)) +
    geom_histogram(aes(y = after_stat(density)),
                   binwidth = 5, fill = "steelblue",
                   color = "white", alpha = 0.7) +
    geom_density(color = "darkblue", linewidth = 1.2) +
    geom_vline(xintercept = 60, color = "red",
               linetype = "dashed", linewidth = 1) +
    labs(title = "成绩分布",
         x = "总评成绩", y = "密度") +
    theme_minimal()

# 图 2：按班级和性别的箱线图
p2 <- ggplot(scores, aes(x = 班级, y = 总评, fill = 性别)) +
    geom_boxplot(alpha = 0.7) +
    labs(title = "各班男女生成绩对比",
         x = "", y = "总评成绩") +
    scale_fill_manual(values = c("男" = "#4E79A7", "女" = "#E15759")) +
    theme_minimal()

# 图 3：各等级人数
p3 <- scores %>%
    count(班级, 等级) %>%
    ggplot(aes(x = 等级, y = n, fill = 班级)) +
    geom_col(position = "dodge") +
    labs(title = "各班级等级分布",
         x = "等级", y = "人数") +
    theme_minimal()

# 图 4：期中 vs 期末散点图
p4 <- ggplot(scores, aes(x = 期中, y = 期末, color = 总评)) +
    geom_point(size = 2, alpha = 0.7) +
    geom_smooth(method = "lm", se = TRUE, color = "darkred") +
    scale_color_gradient(low = "red", high = "green") +
    labs(title = "期中 vs 期末成绩",
         x = "期中成绩", y = "期末成绩",
         color = "总评") +
    theme_minimal()

# 组合显示
library(patchwork)
(p1 + p2) / (p3 + p4)

# 导出
ggsave("score_report.png", width = 12, height = 10, dpi = 300)

# ========== 5. 导出数据 ==========
write_csv(scores, "scores_analyzed.csv")
cat("\n分析完成！结果已保存至 scores_analyzed.csv\n")
```

**渲染效果：** 控制台输出完整统计报告（整体统计、班级统计、性别统计、t 检验和 ANOVA 结果）。图形窗口显示 2×2 组合图：成绩分布、箱线图、等级分布、散点图。

---

## 4.2 RMarkdown：一键生成分析报告

RMarkdown 将代码、结果和文字融为一体，一键生成 HTML/PDF/Word 报告。

新建 `report.Rmd` 文件：

````markdown
---
title: "考试成绩分析报告"
author: "张三"
date: "2026-05-10"
output: html_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE, warning = FALSE, message = FALSE)
library(tidyverse)
```

## 1. 数据概览

本次分析共包含 `r nrow(scores)` 名学生的成绩数据。

```{r}
glimpse(scores)
```

## 2. 描述性统计

```{r}
scores %>%
    summarise(
        平均分 = mean(总评),
        中位数 = median(总评),
        标准差 = sd(总评),
        及格率 = mean(总评 >= 60) * 100
    ) %>%
    knitr::kable(digits = 1)
```

## 3. 成绩分布

```{r, fig.width=8, fig.height=5}
ggplot(scores, aes(x = 总评)) +
    geom_histogram(binwidth = 5, fill = "steelblue",
                   color = "white", alpha = 0.7) +
    geom_vline(xintercept = 60, color = "red",
               linetype = "dashed", linewidth = 1) +
    labs(title = "成绩分布直方图",
         x = "总评成绩", y = "人数") +
    theme_minimal()
```

## 4. 结论

- 整体平均分为 `r round(mean(scores$总评), 1)` 分
- 及格率为 `r round(mean(scores$总评 >= 60) * 100, 1)`%
- 男女生成绩差异 `r ifelse(t_test$p.value < 0.05, "显著", "不显著")`
````

**渲染效果：** 点击 RStudio 的 "Knit" 按钮，生成 HTML 报告：标题页、目录、内嵌代码和输出、图表、格式化表格，所有内容自动整合。

---

## 4.3 学习旅程回顾

| 章节 | 场景 | 核心技能 |
|:---|:---|:---|
| 第 1 章 | 分析考试成绩 | 变量、向量、数据框、基本统计 |
| 第 2 章 | 制作数据图表 | ggplot2 图层语法、多种图表类型 |
| 第 3 章 | 整理杂乱数据 | dplyr、tidyr、管道、数据重塑 |
| 第 4 章 | 端到端项目 | 统计检验、RMarkdown、完整分析流程 |

---

## 课后练习

### 基础练习

1. 用 R 读取一份 CSV 数据，完成基本统计和可视化。
2. 用 dplyr 对数据进行分组汇总，并用 ggplot2 绘制结果。

### 进阶挑战

3. 下载一份公开数据集（如 Kaggle 上的 Titanic 数据），完成从清洗到建模的完整分析。
4. 用 RMarkdown 撰写一份数据分析报告，导出为 HTML 格式。

---

👉 [返回首页 →](index.md)