# 第 4 章：实战案例

> **完整数据分析项目** —— 从导入数据到生成分析报告，体验真实的数据分析流程。

---

## 4.1 案例：电商销售数据分析

### 项目背景

某电商平台提供了一份 2025 年销售数据，我们需要分析销售趋势、找出热销品类并给出业务建议。

### 步骤 1：导入数据

```r
library(readr)
library(dplyr)
library(ggplot2)

# 导入 CSV 数据
sales <- read_csv("sales_data.csv")

# 查看数据结构
glimpse(sales)
head(sales)
```

### 步骤 2：数据清洗

```r
# 检查缺失值
colSums(is.na(sales))

# 处理缺失值
sales <- sales %>%
    filter(!is.na(amount)) %>%        # 删除金额缺失的行
    mutate(
        quantity = ifelse(is.na(quantity), 1, quantity)  # 数量缺失填 1
    )

# 转换数据类型
sales <- sales %>%
    mutate(
        date = as.Date(date),
        category = as.factor(category),
        month = format(date, "%Y-%m")
    )
```

### 步骤 3：探索性分析

```r
# 月度销售趋势
monthly_sales <- sales %>%
    group_by(month) %>%
    summarise(
        total_amount = sum(amount),
        order_count = n(),
        avg_amount = mean(amount)
    ) %>%
    arrange(month)

print(monthly_sales)

# 品类分析
category_analysis <- sales %>%
    group_by(category) %>%
    summarise(
        total_amount = sum(amount),
        order_count = n(),
        avg_amount = mean(amount)
    ) %>%
    arrange(desc(total_amount))

print(category_analysis)
```

### 步骤 4：数据可视化

```r
# 月度销售趋势图
ggplot(monthly_sales, aes(x = month, y = total_amount, group = 1)) +
    geom_line(color = "#2196F3", size = 1.2) +
    geom_point(color = "#1976D2", size = 3) +
    labs(title = "2025 年月度销售趋势",
         x = "月份", y = "销售额（元）") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

# 品类销售占比（饼图）
category_analysis <- category_analysis %>%
    mutate(percentage = total_amount / sum(total_amount) * 100)

ggplot(category_analysis, aes(x = "", y = total_amount, fill = category)) +
    geom_bar(stat = "identity", width = 1) +
    coord_polar("y", start = 0) +
    geom_text(aes(label = paste0(round(percentage, 1), "%")),
              position = position_stack(vjust = 0.5)) +
    labs(title = "各品类销售占比", fill = "品类") +
    theme_void()

# 各品类月度趋势对比
sales %>%
    group_by(month, category) %>%
    summarise(total_amount = sum(amount), .groups = "drop") %>%
    ggplot(aes(x = month, y = total_amount, color = category, group = category)) +
    geom_line(size = 1) +
    labs(title = "各品类月度销售趋势对比",
         x = "月份", y = "销售额（元）", color = "品类") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

**渲染效果：** 折线图展示月度趋势变化；饼图展示品类占比（带百分比标签）；多线图对比不同品类的走势。

### 步骤 5：统计建模

```r
# 线性回归：预测销售额
model <- lm(amount ~ category + month, data = sales)
summary(model)

# 结论解读
# 查看 R² 值判断模型拟合度
# 查看各变量的 p 值判断显著性
```

### 步骤 6：生成分析报告

```r
# 使用 R Markdown 生成报告
# 在 RStudio 中：File → New File → R Markdown

# 报告结构：
# ---
# title: "电商销售数据分析报告"
# author: "张三"
# date: "2026-05-09"
# output: html_document
# ---
#
# ## 1. 数据概览
# ## 2. 销售趋势分析
# ## 3. 品类分析
# ## 4. 结论与建议
```

---

## 本章要点总结

- [ ] 掌握完整的数据分析流程：导入 → 清洗 → 分析 → 可视化 → 建模
- [ ] 能使用 dplyr 进行数据清洗和汇总
- [ ] 能用 ggplot2 创建多种可视化图表
- [ ] 了解 R Markdown 生成分析报告的方法

---

## 课后练习

### 基础练习

1. 使用 R 内置的 `iris` 数据集，完成以下分析：
   - 按物种分组计算各特征的平均值
   - 绘制花瓣长度与宽度的散点图（按物种着色）

2. 使用 `mtcars` 数据集：
   - 分析油耗（mpg）与重量（wt）的关系
   - 建立线性回归模型并解读结果

### 进阶挑战

3. 从 Kaggle 下载一个你感兴趣的数据集，完成完整的分析流程。
4. 用 R Markdown 撰写一份数据分析报告并导出为 HTML。

---

👉 [返回首页 →](index.md)