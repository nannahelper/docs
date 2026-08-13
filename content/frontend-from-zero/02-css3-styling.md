# 第 2 章：CSS3 样式与视觉美化——给网页穿上漂亮的"衣服"

## 📺 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 掌握 CSS3 的核心语法，理解选择器、盒模型、颜色与字体系统，能阅读和理解网页的样式代码 |
| **核心比喻** | **室内装修（墙纸、家具、灯光）** —— CSS 决定网页的外观，就像装修决定房子的颜值 |
| **预计时长** | 100 分钟 |
| **关键概念** | 选择器、优先级、盒模型、颜色系统、字体排版、背景与边框、过渡动画 |
| **实践任务** | 阅读并分析一个博客页面的 CSS 样式表，理解每条规则的作用 |

---

如果说 HTML 是房子的钢筋水泥骨架，那么 CSS 就是 **室内装修**——墙纸的颜色、家具的摆放、灯光的明暗，全都由 CSS 来决定。一个只有 HTML 的网页就像毛坯房，虽然结构完整，但毫无美感可言。在这一章中，我们将学习如何用 CSS3 为网页穿上漂亮的"衣服"。

---

## 2.1 CSS 是什么？—— 认识网页的"化妆师"

### 2.1.1 CSS 的全称与本质

CSS 的全称是 **Cascading Style Sheets**（层叠样式表）。拆开来看：

- **Cascading（层叠）**：多个样式规则可以叠加应用到同一个元素上，后定义的规则会覆盖先定义的规则（当优先级相同时）。
- **Style（样式）**：控制元素的外观——颜色、大小、位置、字体、背景等等。
- **Sheets（表）**：样式规则写在样式表中，可以是一个独立的 `.css` 文件，也可以写在 HTML 的 `<style>` 标签内。

!!! info "CSS 也不是编程语言"

    和 HTML 一样，CSS 也不是编程语言。它没有变量（CSS 变量是后来的增强）、没有逻辑判断、没有循环。CSS 是一种 **声明式语言**——你告诉浏览器"这个元素应该是什么样子"，浏览器就照做。

### 2.1.2 CSS 的三种引入方式

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>CSS 引入方式</title>

    <!-- 方式一：外部样式表（推荐） -->
    <link rel="stylesheet" href="styles.css">

    <!-- 方式二：内部样式表 -->
    <style>
        h1 {
            color: blue;
        }
    </style>
</head>
<body>
    <!-- 方式三：行内样式（不推荐） -->
    <p style="color: red; font-size: 18px;">这是一段红色文字。</p>
</body>
</html>
```

**代码解读：**

| 方式 | 写法 | 优点 | 缺点 | 推荐度 |
|:---|:---|:---|:---|:---:|
| **外部样式表** | `<link rel="stylesheet" href="styles.css">` | 样式与结构分离，可复用，易维护 | 需要额外 HTTP 请求 | ⭐⭐⭐⭐⭐ |
| **内部样式表** | `<style>...</style>` | 无需额外文件，适合单页演示 | 不能跨页面复用 | ⭐⭐⭐ |
| **行内样式** | `style="color: red"` | 优先级最高，直接生效 | 与 HTML 耦合，难以维护 | ⭐ |

---

## 2.2 CSS 语法基础

### 2.2.1 规则集的结构

一条 CSS 规则由 **选择器** 和 **声明块** 组成：

```css
选择器 {
    属性名: 属性值;
    属性名: 属性值;
}

/* 实际例子 */
h1 {
    color: #333333;
    font-size: 24px;
    text-align: center;
}
```

**代码解读：**

- `h1` 是 **选择器**，表示"选中页面中所有的 `<h1>` 元素"。
- `{ }` 内部是 **声明块**，包含一条或多条声明。
- 每条声明由 `属性名: 属性值;` 组成，**分号不能省略**（最后一条可以省略，但建议保留）。

### 2.2.2 CSS 注释

```css
/* 这是单行注释 */

/*
 * 这是多行注释
 * 可以跨越多行
 */
```

!!! warning "CSS 不支持 `//` 注释"

    与 JavaScript 不同，CSS 只支持 `/* */` 格式的注释。使用 `//` 会导致 CSS 解析错误。

---

## 2.3 CSS 选择器体系

选择器是 CSS 最核心的概念——你需要先"选中"元素，才能给它设置样式。CSS3 提供了丰富多样的选择器，掌握它们是读懂前端代码的关键。

### 2.3.1 基础选择器

```css
/* 1. 元素选择器：选中所有该类型的元素 */
p {
    line-height: 1.8;
}

/* 2. 类选择器：选中所有 class 包含该名称的元素（最常用） */
.highlight {
    background-color: yellow;
}

/* 3. ID 选择器：选中 id 为该名称的唯一元素 */
#main-title {
    font-size: 32px;
}

/* 4. 通配选择器：选中所有元素（慎用，性能较差） */
* {
    margin: 0;
    padding: 0;
}
```

**代码解读：**

- **类选择器** 以 `.` 开头，一个元素可以有多个 class（用空格分隔），同一个 class 可以用在多个元素上。
- **ID 选择器** 以 `#` 开头，一个页面中同一个 id 只能出现一次。
- 实际开发中，**类选择器使用最频繁**，ID 选择器主要用于 JavaScript 定位元素。

### 2.3.2 组合选择器

```css
/* 5. 后代选择器：选中所有后代（空格分隔） */
article p {
    color: #555;
}
/* 含义：选中 <article> 内部的所有 <p>，无论嵌套多深 */

/* 6. 子代选择器：只选中直接子元素（> 分隔） */
nav > a {
    margin-right: 15px;
}
/* 含义：只选中 <nav> 的直接子元素 <a>，不包含更深层的 <a> */

/* 7. 相邻兄弟选择器：选中紧邻的下一个兄弟（+ 分隔） */
h2 + p {
    font-weight: bold;
}
/* 含义：选中紧跟在 <h2> 后面的第一个 <p> */

/* 8. 通用兄弟选择器：选中后面所有兄弟（~ 分隔） */
h2 ~ p {
    text-indent: 2em;
}
/* 含义：选中 <h2> 后面的所有 <p> 兄弟元素 */

/* 9. 并集选择器：同时选中多个选择器（逗号分隔） */
h1, h2, h3 {
    font-family: "Microsoft YaHei", sans-serif;
}
```

### 2.3.3 属性选择器

```css
/* 选中具有某个属性的元素 */
[title] {
    cursor: help;
}

/* 选中属性值等于某值的元素 */
input[type="text"] {
    border: 1px solid #ccc;
}

/* 选中属性值以某值开头的元素 */
a[href^="https"] {
    color: green;
}

/* 选中属性值以某值结尾的元素 */
a[href$=".pdf"] {
    background: url(pdf-icon.png) no-repeat left center;
}

/* 选中属性值包含某值的元素 */
[class*="btn"] {
    border-radius: 4px;
}
```

### 2.3.4 伪类选择器

伪类用于定义元素的 **特殊状态**：

```css
/* 鼠标悬停状态 */
a:hover {
    color: orange;
    text-decoration: underline;
}

/* 未访问的链接 */
a:link {
    color: blue;
}

/* 已访问的链接 */
a:visited {
    color: purple;
}

/* 获得焦点时（常用于输入框） */
input:focus {
    border-color: #4A90D9;
    outline: none;
    box-shadow: 0 0 5px rgba(74, 144, 217, 0.5);
}

/* 第一个子元素 */
li:first-child {
    font-weight: bold;
}

/* 最后一个子元素 */
li:last-child {
    border-bottom: none;
}

/* 第 n 个子元素（n 从 1 开始） */
li:nth-child(2) {
    background-color: #f0f0f0;
}

/* 奇数/偶数行（表格斑马纹） */
tr:nth-child(odd) {
    background-color: #f9f9f9;
}
tr:nth-child(even) {
    background-color: #ffffff;
}
```

### 2.3.5 伪元素选择器

伪元素用于创建 **虚拟的元素**，它们不在 HTML 中实际存在：

```css
/* 在元素内容之前插入内容 */
.quote::before {
    content: "「";
    color: #999;
}

/* 在元素内容之后插入内容 */
.quote::after {
    content: "」";
    color: #999;
}

/* 选中文本的第一行 */
p::first-line {
    font-weight: bold;
}

/* 选中文本的第一个字母 */
p::first-letter {
    font-size: 2em;
    color: #c00;
}

/* 选中用户选中的文本 */
::selection {
    background-color: #ffeb3b;
    color: #333;
}
```

!!! tip "`::before` vs `:before`"

    CSS3 规范中伪元素使用双冒号 `::`，伪类使用单冒号 `:`。但为了兼容旧浏览器，`::before` 也可以写成 `:before`。建议统一使用双冒号以区分伪类和伪元素。

---

## 2.4 CSS 优先级（层叠规则）

当多个规则同时作用于同一个元素时，浏览器需要决定"听谁的"。这就是 CSS 的 **层叠（Cascading）** 机制。

### 2.4.1 优先级计算

优先级由四个级别组成，从高到低：

| 级别 | 选择器类型 | 权重值 |
|:---|:---|:---:|
| **A** | 行内样式 `style="..."` | 1000 |
| **B** | ID 选择器 `#id` | 0100 |
| **C** | 类选择器 `.class`、属性选择器 `[attr]`、伪类 `:hover` | 0010 |
| **D** | 元素选择器 `div`、伪元素 `::before` | 0001 |

```css
/* 优先级计算示例 */

/* 优先级：0001（1个元素选择器） */
p { color: black; }

/* 优先级：0010（1个类选择器） */
.intro { color: blue; }

/* 优先级：0011（1个类 + 1个元素） */
p.intro { color: green; }

/* 优先级：0101（1个ID + 1个元素） */
#content p { color: red; }

/* 优先级：0011（1个类 + 1个元素） */
div .intro { color: purple; }
```

### 2.4.2 `!important` —— 终极武器（慎用）

```css
p {
    color: red !important; /* 优先级高于一切普通规则 */
}
```

!!! danger "`!important` 是"核武器"，慎用！"

    使用 `!important` 会破坏 CSS 的层叠机制，让后续的样式覆盖变得极其困难。如果你的 CSS 中出现了大量 `!important`，通常意味着选择器设计有问题。**仅在需要覆盖第三方库样式时作为最后手段使用。**

---

## 2.5 盒模型——CSS 的基石

### 2.5.1 什么是盒模型？

在 CSS 中，**每个元素都是一个矩形盒子**。这个盒子由四个部分组成：

```
┌─────────────────────────────────────┐
│              margin                 │
│  ┌───────────────────────────────┐  │
│  │           border              │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │        padding          │  │  │
│  │  │  ┌───────────────────┐  │  │  │
│  │  │  │     content       │  │  │  │
│  │  │  │   (实际内容区域)    │  │  │  │
│  │  │  └───────────────────┘  │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**代码解读：**

| 层次 | 属性 | 含义 |
|:---|:---|:---|
| **content** | `width` / `height` | 内容的实际宽高 |
| **padding** | `padding` | 内边距，内容与边框之间的空白 |
| **border** | `border` | 边框，包裹在 padding 外面 |
| **margin** | `margin` | 外边距，元素与其他元素之间的距离 |

### 2.5.2 `box-sizing` —— 改变盒模型计算方式

```css
/* 默认盒模型：width 只包含 content */
.content-box {
    box-sizing: content-box;
    width: 300px;
    padding: 20px;
    border: 5px solid #333;
    /* 实际占用宽度 = 300 + 20*2 + 5*2 = 350px */
}

/* 边框盒模型：width 包含 content + padding + border（推荐） */
.border-box {
    box-sizing: border-box;
    width: 300px;
    padding: 20px;
    border: 5px solid #333;
    /* 实际占用宽度 = 300px（content 自动缩小） */
}
```

!!! tip "全局设置 border-box"

    在实际项目中，通常会在 CSS 开头设置：
    ```css
    *, *::before, *::after {
        box-sizing: border-box;
    }
    ```
    这样所有元素的 `width` 都表示"可见宽度"，布局计算更加直观。

---

## 2.6 颜色与背景

### 2.6.1 颜色的四种表示法

```css
.example {
    /* 1. 颜色名称（有限，不推荐） */
    color: red;

    /* 2. 十六进制（最常用） */
    color: #FF6B35;          /* 6位完整写法 */
    color: #F63;             /* 3位简写，等价于 #FF6633 */

    /* 3. RGB / RGBA */
    color: rgb(255, 107, 53);
    color: rgba(255, 107, 53, 0.8);  /* a = 透明度，0~1 */

    /* 4. HSL / HSLA（更直观） */
    color: hsl(16, 100%, 60%);        /* 色相 饱和度 亮度 */
    color: hsla(16, 100%, 60%, 0.8);
}
```

### 2.6.2 背景属性

```css
.hero {
    /* 背景颜色 */
    background-color: #f5f5f5;

    /* 背景图片 */
    background-image: url("hero-bg.jpg");

    /* 背景重复方式 */
    background-repeat: no-repeat;     /* no-repeat | repeat-x | repeat-y */

    /* 背景定位 */
    background-position: center center;

    /* 背景尺寸 */
    background-size: cover;           /* cover | contain | 具体尺寸 */

    /* 背景固定（视差效果） */
    background-attachment: fixed;

    /* 简写形式 */
    background: #f5f5f5 url("hero-bg.jpg") no-repeat center/cover fixed;
}

/* CSS3 渐变背景 */
.gradient-box {
    /* 线性渐变 */
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

    /* 径向渐变 */
    background: radial-gradient(circle, #ff6b6b, #c0392b);
}
```

---

## 2.7 字体与文本排版

### 2.7.1 字体属性

```css
body {
    /* 字体族（从前往后依次尝试，最后的 sans-serif 是通用备选） */
    font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", sans-serif;

    /* 字号 */
    font-size: 16px;

    /* 字重（粗细） */
    font-weight: 400;          /* 100~900，400=normal，700=bold */

    /* 行高（推荐使用无单位数值） */
    line-height: 1.6;          /* 1.6 倍字号 */

    /* 字体样式 */
    font-style: normal;        /* normal | italic */

    /* 简写形式 */
    font: 400 16px/1.6 "Microsoft YaHei", sans-serif;
}
```

### 2.7.2 文本排版属性

```css
.article {
    /* 文本颜色 */
    color: #333333;

    /* 文本对齐 */
    text-align: justify;       /* left | center | right | justify（两端对齐） */

    /* 文本缩进 */
    text-indent: 2em;          /* 首行缩进两个字符 */

    /* 文本装饰 */
    text-decoration: none;     /* none | underline | line-through */

    /* 字母间距 */
    letter-spacing: 0.5px;

    /* 单词间距 */
    word-spacing: 2px;

    /* 空白处理 */
    white-space: normal;       /* normal | nowrap（不换行） | pre（保留空格换行） */

    /* 文本溢出省略号（经典三件套） */
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
```

---

## 2.8 边框与阴影

```css
.card {
    /* 边框 */
    border: 1px solid #e0e0e0;
    /* 等价于：
    border-width: 1px;
    border-style: solid;
    border-color: #e0e0e0;
    */

    /* 圆角 */
    border-radius: 8px;                    /* 四个角统一 */
    border-radius: 8px 4px 8px 4px;        /* 左上 右上 右下 左下 */

    /* 圆形（宽高相等 + border-radius: 50%） */
    width: 80px;
    height: 80px;
    border-radius: 50%;

    /* 盒阴影 */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    /* 参数：水平偏移 垂直偏移 模糊半径 颜色 */

    /* 文字阴影 */
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}
```

---

## 2.9 CSS3 过渡动画

过渡（Transition）让样式变化变得平滑，是提升用户体验的重要手段：

```css
.button {
    background-color: #4A90D9;
    color: white;
    padding: 10px 24px;
    border: none;
    border-radius: 4px;
    cursor: pointer;

    /* 过渡属性：对哪些属性做动画 | 持续时间 | 缓动函数 | 延迟 */
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.button:hover {
    background-color: #357ABD;
    transform: translateY(-2px);    /* 向上移动 2px */
    box-shadow: 0 4px 12px rgba(74, 144, 217, 0.4);
}
```

**代码解读：**

- `transition` 让属性值的变化从"瞬间完成"变为"平滑过渡"。
- `ease` 是缓动函数，表示"慢→快→慢"的变化节奏。
- `transform` 是 CSS3 的变换属性，可以做位移、旋转、缩放等操作，**不会影响文档流**。

**渲染效果：** 当鼠标悬停在按钮上时，你会看到：
- 背景色从 `#4A90D9` 平滑过渡到 `#357ABD`（0.3 秒）
- 按钮整体向上移动 2px（0.2 秒），产生"浮起"的视觉效果
- 同时出现一个半透明的蓝色阴影，增强立体感
- 鼠标移开后，所有变化平滑恢复原状

---

## 2.10 实践任务：阅读并分析博客样式表

### 任务要求

下面是第 1 章博客页面的完整 CSS 样式表。你的任务是 **逐段阅读并理解每条规则的作用**，回答以下问题：

- 全局重置中 `box-sizing: border-box` 的作用是什么？
- 页眉使用了什么背景效果？导航链接的悬停效果是如何实现的？
- 代码块（`pre`）和行内代码（`code`）的样式有什么区别？
- 表单输入框获得焦点时（`:focus`）会发生什么视觉变化？
- 如果你想把页眉的渐变色从蓝紫改为红橙，应该修改哪一行？

### 参考代码

```css
/* styles.css */
/* ========== 全局重置 ========== */
*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
    font-size: 16px;
    line-height: 1.8;
    color: #333;
    background-color: #fafafa;
}

/* ========== 布局容器 ========== */
header, main, aside, footer {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

/* ========== 页眉 ========== */
header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 30px 20px;
    text-align: center;
}

header h1 {
    font-size: 28px;
    margin-bottom: 15px;
}

header nav a {
    color: rgba(255, 255, 255, 0.9);
    text-decoration: none;
    margin: 0 12px;
    font-size: 15px;
    transition: color 0.3s ease;
}

header nav a:hover {
    color: #fff;
    text-decoration: underline;
}

/* ========== 文章主体 ========== */
article {
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    margin-bottom: 30px;
}

article h2 {
    font-size: 24px;
    color: #2c3e50;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid #eee;
}

article h3 {
    font-size: 20px;
    color: #34495e;
    margin: 25px 0 12px;
}

article p {
    margin-bottom: 15px;
    text-align: justify;
}

/* ========== 代码块 ========== */
pre {
    background-color: #2d3436;
    color: #dfe6e9;
    padding: 20px;
    border-radius: 6px;
    overflow-x: auto;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 14px;
    line-height: 1.6;
    margin: 15px 0;
}

code {
    background-color: #f0f0f0;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 0.9em;
}

pre code {
    background: none;
    padding: 0;
}

/* ========== 侧边栏 ========== */
aside {
    background: white;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    margin-bottom: 30px;
}

aside h3 {
    font-size: 18px;
    color: #2c3e50;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #eee;
}

aside ul {
    list-style: none;
}

aside ul li {
    padding: 6px 0;
}

aside ul li a {
    color: #4A90D9;
    text-decoration: none;
    transition: color 0.3s ease;
}

aside ul li a:hover {
    color: #357ABD;
    text-decoration: underline;
}

/* ========== 表单 ========== */
form {
    background: white;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

form label {
    display: block;
    margin-bottom: 5px;
    font-weight: 600;
    color: #555;
}

form input[type="text"],
form textarea {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 15px;
    margin-bottom: 15px;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

form input[type="text"]:focus,
form textarea:focus {
    border-color: #4A90D9;
    outline: none;
    box-shadow: 0 0 0 3px rgba(74, 144, 217, 0.15);
}

form button {
    background-color: #4A90D9;
    color: white;
    padding: 10px 28px;
    border: none;
    border-radius: 4px;
    font-size: 15px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

form button:hover {
    background-color: #357ABD;
    transform: translateY(-1px);
}

/* ========== 页脚 ========== */
footer {
    text-align: center;
    padding: 25px 20px;
    color: #999;
    font-size: 14px;
    border-top: 1px solid #eee;
}
```

### 验证步骤

1. 将 CSS 代码保存为 `styles.css`，放在与 `blog-post.html` 同目录下。
2. 在 HTML 的 `<head>` 中添加 `<link rel="stylesheet" href="styles.css">`。
3. 用浏览器打开页面，观察样式变化——对比添加 CSS 前后的视觉差异。
4. 按 F12 打开开发者工具，在 Styles 面板中查看每个元素应用的 CSS 规则，尝试勾选/取消勾选某条规则观察变化。
5. 尝试修改颜色值（如将 `#667eea` 改为 `#e74c3c`），观察页面变化——这就是"修改代码"的起点。

---

## 📋 本章要点总结

- [ ] 理解 CSS 的三种引入方式（外部、内部、行内），推荐使用外部样式表
- [ ] 掌握 CSS 规则集的基本语法：`选择器 { 属性: 值; }`
- [ ] 熟练使用类选择器（`.class`）、元素选择器、后代选择器
- [ ] 理解伪类（`:hover`、`:focus`、`:nth-child`）和伪元素（`::before`、`::after`）
- [ ] 掌握 CSS 优先级计算规则，理解 `!important` 的风险
- [ ] 深入理解盒模型（content → padding → border → margin）
- [ ] 会使用 `box-sizing: border-box` 简化布局计算
- [ ] 掌握颜色表示法（十六进制、RGB、HSL）和背景属性
- [ ] 能设置字体、行高、文本对齐等排版属性
- [ ] 会使用 `border-radius`、`box-shadow` 美化元素
- [ ] 理解 `transition` 过渡动画的基本用法

---

## 📚 课后练习

### 基础练习

1. 创建一个"名片"卡片，包含头像（用 `border-radius: 50%` 做圆形）、姓名、职位和联系方式，使用 `box-shadow` 添加阴影效果。
2. 创建一个导航栏，包含 4 个链接，使用 `:hover` 伪类实现悬停变色效果。

### 进阶挑战

3. 使用 `linear-gradient` 创建一个渐变背景的横幅（Banner）区域，包含标题和副标题。
4. 为第 1 章的博客页面添加"返回顶部"按钮，使用 `position: fixed` 固定在右下角，并添加 `transition` 悬停动画。

---

👉 [进入第 3 章：CSS3 布局与响应式设计 →](03-css3-layout-responsive.md)
