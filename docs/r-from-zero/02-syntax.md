# 第 2 章：让数据可视化

> **场景：** 老师看了你的统计报告说"数字不错，但画几张图会更直观"。R 的 ggplot2 是数据可视化领域的标杆——让我们用图层语法把数据变成精美的图表。

---

## 2.1 ggplot2 的图层语法

ggplot2 的核心思想是**图层叠加**：像搭积木一样，一层一层地构建图表。

```r
library(ggplot2)

# 基本模板
ggplot(data = <数据>, aes(x = <X轴>, y = <Y轴>)) +
    geom_<几何对象>() +
    labs(title = <标题>) +
    theme_<主题>()
```

**核心理念：** 每个 `+` 添加一个图层——数据映射、几何对象、标签、主题各自独立，组合灵活。

---

## 2.2 成绩分布可视化

```r
library(ggplot2)

scores <- read.csv("scores.csv")
scores$总评 <- scores$平时 * 0.3 + scores$期中 * 0.3 + scores$期末 * 0.4

# 直方图：看分数分布
ggplot(scores, aes(x = 总评)) +
    geom_histogram(binwidth = 5,
                   fill = "steelblue",
                   color = "white",
                   alpha = 0.8) +
    geom_vline(xintercept = 60, color = "red",
               linetype = "dashed", linewidth = 1) +
    annotate("text", x = 62, y = 8, label = "及格线",
             color = "red", hjust = 0) +
    labs(title = "成绩分布直方图",
         subtitle = paste("平均分：", round(mean(scores$总评), 1),
                          " | 及格率：", round(mean(scores$总评 >= 60) * 100, 1), "%"),
         x = "总评成绩", y = "人数") +
    theme_minimal()
```

**渲染效果：** 蓝色直方图展示分数分布，红色虚线标记 60 分及格线，标题包含平均分和及格率，使用简洁的 minimal 主题。

---

## 2.3 散点图：看变量关系

```r
# 期中 vs 期末成绩散点图
ggplot(scores, aes(x = 期中, y = 期末, color = 性别)) +
    geom_point(size = 3, alpha = 0.7) +
    geom_smooth(method = "lm", se = TRUE) +
    labs(title = "期中 vs 期末成绩",
         x = "期中成绩", y = "期末成绩",
         color = "性别") +
    theme_minimal()
```

**渲染效果：** 散点图中蓝色和红色点分别表示男女生，带回归线和置信区间阴影。`geom_smooth(method = "lm")` 自动添加线性回归线。

---

## 2.4 箱线图：看分组分布

```r
# 按性别分组的箱线图
ggplot(scores, aes(x = 性别, y = 总评, fill = 性别)) +
    geom_boxplot(width = 0.5, alpha = 0.7) +
    geom_jitter(width = 0.1, alpha = 0.5) +
    labs(title = "男女生成绩对比",
         x = "", y = "总评成绩") +
    theme_minimal() +
    theme(legend.position = "none")
```

**渲染效果：** 两个彩色箱线图并排，显示中位数、四分位数和异常值。散点叠加在箱线图上，展示每个数据点的分布。

---

## 2.5 柱状图：看分类统计

```r
# 各分数段人数
scores$等级 <- cut(scores$总评,
                   breaks = c(0, 60, 70, 80, 90, 100),
                   labels = c("不及格", "及格", "中等", "良好", "优秀"))

ggplot(scores, aes(x = 等级, fill = 等级)) +
    geom_bar() +
    geom_text(stat = "count", aes(label = after_stat(count)),
              vjust = -0.5) +
    labs(title = "各分数段人数分布",
         x = "等级", y = "人数") +
    theme_minimal() +
    theme(legend.position = "none")
```

**渲染效果：** 彩色柱状图，每个柱子上方标注具体人数，直观展示各等级分布。

---

## 2.6 常用图表类型速查

```r
# 折线图
ggplot(data, aes(x = 时间, y = 值)) +
    geom_line(color = "steelblue", linewidth = 1)

# 面积图
ggplot(data, aes(x = 时间, y = 值)) +
    geom_area(fill = "steelblue", alpha = 0.3)

# 小提琴图（比箱线图更丰富）
ggplot(data, aes(x = 类别, y = 值, fill = 类别)) +
    geom_violin(alpha = 0.7)

# 密度曲线
ggplot(data, aes(x = 值, fill = 类别)) +
    geom_density(alpha = 0.5)

# 分面：按类别拆分成多个子图
ggplot(data, aes(x = x, y = y)) +
    geom_point() +
    facet_wrap(~ 类别)
```

---

## 2.7 图形美化与导出

```r
p <- ggplot(scores, aes(x = 期中, y = 期末, color = 性别)) +
    geom_point(size = 3, alpha = 0.7) +
    geom_smooth(method = "lm", se = TRUE) +
    labs(title = "期中 vs 期末成绩分析",
         subtitle = "按性别分组，含线性回归趋势线",
         x = "期中成绩", y = "期末成绩",
         color = "性别",
         caption = "数据来源：2026 年春季学期") +
    scale_color_manual(values = c("男" = "#4E79A7", "女" = "#E15759")) +
    theme_minimal(base_size = 14) +
    theme(
        plot.title = element_text(face = "bold", size = 18),
        plot.subtitle = element_text(color = "gray50"),
        legend.position = "bottom"
    )

print(p)

# 导出图片
ggsave("score_scatter.png", p, width = 8, height = 6, dpi = 300)
```

**渲染效果：** 专业级散点图，自定义颜色方案，标题加粗，副标题灰色，图例在底部，脚注标注数据来源。`ggsave` 导出 300 DPI 高清 PNG。

---

## 本章回顾

你的数据现在有了专业级的可视化呈现！回顾掌握的技能：

- [x] 理解 ggplot2 的图层语法（`ggplot() + geom_xxx()`）
- [x] 用 `geom_histogram` 绘制直方图
- [x] 用 `geom_point` + `geom_smooth` 绘制散点图和回归线
- [x] 用 `geom_boxplot` 绘制箱线图
- [x] 用 `geom_bar` 绘制柱状图
- [x] 用 `facet_wrap` 创建分面图
- [x] 用 `labs()` 和 `theme()` 美化图表
- [x] 用 `ggsave` 导出高清图片

---

👉 [进入第 3 章：数据清洗与变换 →](03-tips.md)