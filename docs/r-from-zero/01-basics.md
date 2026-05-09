# 第 1 章：基础概念

> **认识 R 语言** —— 了解 R 的定位、安装环境并熟悉 RStudio 工作界面。

---

## 1.1 R 语言的定位

R 语言是一门 **面向统计计算** 的编程语言。与 Python 这种通用语言不同，R 从诞生之初就专注于数据分析和统计建模。

| 对比维度 | R 语言 | Python |
|:---|:---|:---|
| **核心定位** | 统计计算与数据可视化 | 通用编程语言 |
| **数据分析** | 内置支持，语法自然 | 需借助 pandas、numpy 等库 |
| **可视化** | ggplot2（图形语法标杆） | matplotlib、seaborn |
| **统计模型** | 极其丰富，学术界标准 | scikit-learn、statsmodels |
| **学习曲线** | 统计思维友好 | 编程思维友好 |

!!! tip "R 还是 Python？"

    如果你主要做统计分析、学术研究和数据可视化，R 是更好的选择。如果你需要将数据分析嵌入到 Web 应用或生产系统中，Python 更合适。两者都学是最佳策略。

## 1.2 安装 R 和 RStudio

### 安装 R

1. 访问 [CRAN（R 官方镜像）](https://cran.r-project.org/)
2. 选择你的操作系统（Windows / Mac / Linux）
3. 下载并安装最新版本的 R

### 安装 RStudio

RStudio 是 R 语言最流行的集成开发环境（IDE），强烈推荐安装：

1. 访问 [RStudio 官网](https://posit.co/download/rstudio-desktop/)
2. 下载免费版 RStudio Desktop
3. 安装后打开 RStudio

## 1.3 RStudio 界面介绍

RStudio 界面分为四个主要区域：

| 区域 | 位置 | 功能 |
|:---|:---|:---|
| **脚本编辑器** | 左上 | 编写和保存 R 脚本（`.R` 文件） |
| **控制台（Console）** | 左下 | 交互式执行 R 命令，查看输出 |
| **环境/历史** | 右上 | 查看变量、数据框、函数等对象 |
| **文件/绘图/帮助** | 右下 | 浏览文件、显示图表、查看帮助文档 |

!!! tip "快捷键"

    - `Ctrl + Enter`：运行当前选中的代码行
    - `Ctrl + Shift + Enter`：运行整个脚本
    - `Ctrl + L`：清空控制台

## 1.4 第一个 R 程序

```r
# 这是我的第一个 R 程序
print("Hello, R!")

# 基本运算
2 + 3           # 加法 → 5
10 / 3          # 除法 → 3.333...
2^10            # 幂运算 → 1024
sqrt(16)        # 平方根 → 4

# 变量赋值
x <- 100        # 推荐使用 <- 赋值
y = 200         # 也可以用 =，但不推荐
name <- "张三"

# 查看变量
print(x)
print(paste("你好，", name))
```

**运行效果：** 控制台依次输出每行的计算结果。`<-` 是 R 语言特有的赋值符号（也可以用 `=`，但社区惯例推荐 `<-`）。

## 1.5 R 包管理

R 的强大来自其丰富的扩展包（packages）：

```r
# 安装包（只需执行一次）
install.packages("ggplot2")
install.packages("dplyr")
install.packages("tidyr")

# 加载包（每次使用前加载）
library(ggplot2)
library(dplyr)

# 查看已安装的包
installed.packages()

# 查看已加载的包
search()
```

---

## 本章要点总结

- [ ] 理解 R 语言是"面向统计计算"的编程语言
- [ ] 完成 R 和 RStudio 的安装
- [ ] 熟悉 RStudio 四区域界面布局
- [ ] 掌握 `<-` 赋值符号和基本运算
- [ ] 了解 `install.packages()` 和 `library()` 的用法

---

👉 [进入第 2 章：核心语法 →](02-syntax.md)