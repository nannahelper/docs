# 第 3 章：常用技巧

> **数据分析三板斧** —— 数据清洗（dplyr）、可视化（ggplot2）、统计分析。

---

## 3.1 数据清洗：dplyr 核心操作

`dplyr` 是 R 中最强大的数据操作包，提供五个核心动词：

```r
library(dplyr)

# 示例数据
students <- data.frame(
    name = c("张三", "李四", "王五", "赵六", "钱七"),
    class = c("A", "B", "A", "B", "A"),
    math = c(85, 92, 78, 88, 95),
    english = c(90, 85, 82, 91, 88)
)

# filter()：筛选行
students %>% filter(math > 85)

# select()：选择列
students %>% select(name, math)

# mutate()：创建新列
students %>% mutate(total = math + english)

# arrange()：排序
students %>% arrange(desc(math))

# summarise()：汇总统计
students %>% summarise(
    avg_math = mean(math),
    max_math = max(math)
)

# group_by() + summarise()：分组汇总
students %>%
    group_by(class) %>%
    summarise(
        count = n(),
        avg_math = mean(math),
        avg_english = mean(english)
    )
```

**运行效果：** `%>%` 是管道操作符，将左侧结果传递给右侧函数。代码从左到右读，逻辑清晰。分组汇总自动按班级计算各科平均分。

## 3.2 数据可视化：ggplot2

`ggplot2` 基于"图形语法"（Grammar of Graphics），用统一的语法构建各种图表。

```r
library(ggplot2)

# 散点图
ggplot(mtcars, aes(x = wt, y = mpg)) +
    geom_point(color = "blue", size = 3) +
    labs(title = "汽车重量与油耗关系",
         x = "重量（吨）", y = "油耗（英里/加仑）") +
    theme_minimal()

# 柱状图
ggplot(diamonds, aes(x = cut, fill = cut)) +
    geom_bar() +
    labs(title = "钻石切割质量分布") +
    theme_minimal()

# 箱线图
ggplot(mpg, aes(x = class, y = hwy, fill = class)) +
    geom_boxplot() +
    labs(title = "不同车型的高速油耗分布") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

# 分面图
ggplot(mpg, aes(x = displ, y = hwy)) +
    geom_point(alpha = 0.5) +
    facet_wrap(~ class) +
    labs(title = "不同车型的排量与油耗") +
    theme_minimal()
```

**渲染效果：** 散点图展示两个连续变量的关系；柱状图展示分类变量的频数；箱线图展示分布的中位数、四分位数和异常值；分面图按类别拆分为多个子图。

**代码解读：**

- `ggplot(data, aes(...))` 指定数据和美学映射（x 轴、y 轴、颜色等）
- `geom_*()` 添加几何图层（点、线、柱、箱线等）
- `labs()` 设置标题和轴标签
- `theme_*()` 设置主题样式
- 图层用 `+` 号叠加

## 3.3 统计分析

```r
# t 检验：比较两组均值是否有显著差异
t.test(math ~ class, data = students)

# 线性回归
model <- lm(mpg ~ wt + hp, data = mtcars)
summary(model)

# 查看回归结果
coefficients(model)    # 回归系数
fitted(model)          # 拟合值
residuals(model)       # 残差

# 方差分析（ANOVA）
aov_result <- aov(mpg ~ factor(cyl), data = mtcars)
summary(aov_result)

# 相关性分析
cor(mtcars$mpg, mtcars$wt)           # 单个相关系数
cor(mtcars[, c("mpg", "wt", "hp")])  # 相关系数矩阵
```

**运行效果：** `summary(model)` 输出回归系数、标准误、t 值、p 值、R² 等完整统计量。R 的统计输出格式是学术论文的标准格式。

---

## 本章要点总结

- [ ] 掌握 dplyr 五大核心操作：filter、select、mutate、arrange、summarise
- [ ] 理解管道操作符 `%>%` 的用法
- [ ] 能用 ggplot2 绘制散点图、柱状图、箱线图
- [ ] 了解 t 检验、线性回归、ANOVA 的基本用法

---

👉 [进入第 4 章：实战案例 →](04-practice.md)