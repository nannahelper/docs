# 第 3 章：CSS3 布局与响应式设计——像搭积木一样排列页面

## 📺 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 掌握 Flexbox 和 Grid 两大现代布局系统，理解响应式设计原理，能阅读和理解不同屏幕尺寸下的布局代码 |
| **核心比喻** | **家具摆放（积木搭建）** —— 布局决定元素的位置关系，就像家具摆放决定房间的功能分区 |
| **预计时长** | 100 分钟 |
| **关键概念** | 文档流、Flexbox、Grid、媒体查询、响应式断点、移动优先 |
| **实践任务** | 阅读并分析一个响应式博客页面的布局代码，理解不同断点下的布局变化 |

---

如果说第 2 章学的是"如何给单个元素化妆"，那么这一章学的是"如何把多个元素排列整齐"。CSS 布局就像 **摆放家具**——沙发放哪里、茶几怎么摆、电视柜靠哪面墙，这些位置关系决定了房间好不好用。同样，网页元素的排列方式决定了用户体验的好坏。

---

## 3.1 文档流——布局的底层逻辑

### 3.1.1 什么是文档流？

**文档流（Normal Flow）** 是浏览器默认的布局方式——元素按照在 HTML 中出现的顺序，从上到下、从左到右依次排列。

```html
<div class="box1">盒子 1</div>
<div class="box2">盒子 2</div>
<div class="box3">盒子 3</div>
```

在没有 CSS 干预的情况下，这三个 `<div>` 会像叠罗汉一样从上到下排列，每个占满一行。

### 3.1.2 块级元素 vs 行内元素

理解这两种元素类型是掌握布局的前提：

| 特性 | 块级元素（Block） | 行内元素（Inline） |
|:---|:---|:---|
| **独占一行** | ✅ 是 | ❌ 否，与其他行内元素共处一行 |
| **可设置宽高** | ✅ 是 | ❌ 否（宽高由内容决定） |
| **可设置上下 margin** | ✅ 是 | ❌ 否（只有左右 margin 生效） |
| **常见标签** | `<div>`、`<p>`、`<h1>-<h6>`、`<section>`、`<article>`、`<header>`、`<footer>` | `<span>`、`<a>`、`<strong>`、`<em>`、`<img>`、`<code>` |

```css
/* 通过 display 属性可以改变元素的类型 */
span {
    display: block;      /* 变成块级元素 */
}

div {
    display: inline;     /* 变成行内元素 */
}

.item {
    display: inline-block;  /* 行内块：不独占一行，但可以设置宽高 */
}

.hidden {
    display: none;       /* 完全隐藏，不占空间 */
}
```

---

## 3.2 Flexbox 弹性布局——一维排列的利器

Flexbox（弹性盒子布局）是 CSS3 引入的最重要的布局模块之一。它专为 **一维排列** 设计——要么水平排，要么垂直排。

### 3.2.1 Flex 容器与 Flex 项目

```html
<div class="container">
    <div class="item">1</div>
    <div class="item">2</div>
    <div class="item">3</div>
</div>
```

```css
.container {
    display: flex;  /* 激活 Flexbox 布局 */
}
```

**代码解读：** 设置 `display: flex` 后，`.container` 成为 **Flex 容器**，它的直接子元素 `.item` 自动成为 **Flex 项目**。默认情况下，项目会从左到右水平排列。

### 3.2.2 容器属性（作用于父元素）

```css
.container {
    display: flex;

    /* 主轴方向 */
    flex-direction: row;            /* row（默认，水平） | column（垂直） */
    flex-direction: row-reverse;    /* 水平反向 */
    flex-direction: column;         /* 垂直排列 */

    /* 主轴对齐方式 */
    justify-content: flex-start;    /* 起点对齐（默认） */
    justify-content: flex-end;      /* 终点对齐 */
    justify-content: center;        /* 居中对齐 */
    justify-content: space-between; /* 两端对齐，中间均分 */
    justify-content: space-around;  /* 每个项目两侧间距相等 */
    justify-content: space-evenly;  /* 所有间距相等 */

    /* 交叉轴对齐方式 */
    align-items: stretch;           /* 拉伸填满（默认） */
    align-items: flex-start;        /* 起点对齐 */
    align-items: center;            /* 居中对齐 */
    align-items: flex-end;          /* 终点对齐 */

    /* 是否换行 */
    flex-wrap: nowrap;              /* 不换行（默认，可能溢出） */
    flex-wrap: wrap;                /* 换行 */
    flex-wrap: wrap-reverse;        /* 反向换行 */

    /* 多行时的行间距 */
    align-content: center;          /* 多行时在交叉轴上的对齐方式 */
}
```

!!! tip "主轴与交叉轴"

    - **主轴（Main Axis）**：由 `flex-direction` 决定。`row` 时主轴是水平方向，`column` 时主轴是垂直方向。
    - **交叉轴（Cross Axis）**：始终与主轴垂直。
    - 记住：`justify-content` 控制主轴，`align-items` 控制交叉轴。

### 3.2.3 项目属性（作用于子元素）

```css
.item {
    /* 放大比例（默认 0，不放大） */
    flex-grow: 1;          /* 所有项目等分剩余空间 */

    /* 缩小比例（默认 1，空间不足时等比例缩小） */
    flex-shrink: 0;        /* 不缩小 */

    /* 初始大小 */
    flex-basis: 200px;     /* 项目在主轴上占据的初始空间 */

    /* 简写（推荐） */
    flex: 1;               /* 等价于 flex: 1 1 0% */
    flex: 0 0 200px;       /* 不放大不缩小，固定 200px */

    /* 单独控制某个项目的交叉轴对齐 */
    align-self: center;    /* 覆盖容器的 align-items */
}
```

### 3.2.4 Flexbox 实战：导航栏

```html
<nav class="navbar">
    <div class="logo">MySite</div>
    <ul class="nav-links">
        <li><a href="#">首页</a></li>
        <li><a href="#">关于</a></li>
        <li><a href="#">服务</a></li>
        <li><a href="#">联系</a></li>
    </ul>
</nav>
```

```css
.navbar {
    display: flex;
    justify-content: space-between;  /* Logo 靠左，导航靠右 */
    align-items: center;             /* 垂直居中 */
    padding: 15px 30px;
    background-color: #2c3e50;
    color: white;
}

.navbar .logo {
    font-size: 22px;
    font-weight: bold;
}

.nav-links {
    display: flex;       /* 导航项也使用 Flex 水平排列 */
    list-style: none;
    gap: 25px;           /* CSS3 新属性：项目间距（推荐） */
}

.nav-links a {
    color: white;
    text-decoration: none;
    transition: opacity 0.3s ease;
}

.nav-links a:hover {
    opacity: 0.7;
}
```

### 3.2.5 Flexbox 实战：居中卡片

```css
/* 水平垂直居中——Flexbox 最经典的用法 */
body {
    display: flex;
    justify-content: center;  /* 水平居中 */
    align-items: center;      /* 垂直居中 */
    min-height: 100vh;        /* 至少占满整个视口高度 */
    margin: 0;
}

.card {
    width: 350px;
    padding: 30px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
```

---

## 3.3 Grid 网格布局——二维排列的终极方案

如果说 Flexbox 擅长 **一维排列**（单行或单列），那么 Grid 就是 **二维排列** 的王者——同时控制行和列。

### 3.3.1 Grid 容器与 Grid 项目

```css
.container {
    display: grid;

    /* 定义列：3 列，中间列自适应 */
    grid-template-columns: 200px 1fr 200px;

    /* 定义行：第一行 80px，后面行自适应 */
    grid-template-rows: 80px 1fr 60px;

    /* 行列间距 */
    gap: 20px;                    /* 行列统一间距 */
    gap: 15px 25px;               /* 行间距 列间距 */
}
```

**代码解读：**

- `1fr` 是 Grid 特有的单位，表示"一份剩余空间"。`200px 1fr 200px` 表示左右两列固定 200px，中间列占满剩余空间。
- `gap` 是行列间距的简写，比传统的 `margin` 方案更简洁。

### 3.3.2 经典页面布局：圣杯布局

```html
<div class="page-layout">
    <header class="page-header">页眉</header>
    <nav class="page-nav">导航</nav>
    <main class="page-main">主体内容</main>
    <aside class="page-sidebar">侧边栏</aside>
    <footer class="page-footer">页脚</footer>
</div>
```

```css
.page-layout {
    display: grid;
    grid-template-columns: 200px 1fr 250px;
    grid-template-rows: auto 1fr auto;
    grid-template-areas:
        "header  header  header"
        "nav     main    sidebar"
        "footer  footer  footer";
    min-height: 100vh;
    gap: 0;
}

.page-header  { grid-area: header;  background: #2c3e50; color: white; padding: 20px; }
.page-nav     { grid-area: nav;     background: #ecf0f1; padding: 20px; }
.page-main    { grid-area: main;    padding: 30px; }
.page-sidebar { grid-area: sidebar; background: #ecf0f1; padding: 20px; }
.page-footer  { grid-area: footer;  background: #2c3e50; color: white; padding: 15px; text-align: center; }
```

**代码解读：**

- `grid-template-areas` 是最直观的 Grid 布局方式——你直接在 CSS 中"画出"页面结构。
- 每个子元素通过 `grid-area` 指定自己占据哪个命名区域。
- 这种写法让 HTML 的顺序不再影响视觉布局，实现了 **结构与表现的彻底分离**。

### 3.3.3 Grid 实战：响应式卡片网格

```html
<div class="card-grid">
    <div class="card">卡片 1</div>
    <div class="card">卡片 2</div>
    <div class="card">卡片 3</div>
    <div class="card">卡片 4</div>
    <div class="card">卡片 5</div>
    <div class="card">卡片 6</div>
</div>
```

```css
.card-grid {
    display: grid;
    /* auto-fill：自动填充列数，minmax：每列最小 280px，最大 1fr */
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px;
    padding: 20px;
}

.card {
    background: white;
    border-radius: 8px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
```

!!! tip "`auto-fill` vs `auto-fit`"

    - `auto-fill`：尽可能多地创建列轨道，即使有些是空的。
    - `auto-fit`：将现有项目拉伸以填充可用空间。
    - 对于卡片网格，两者效果通常相似；当项目数量少时，`auto-fit` 会让卡片更大。

---

## 3.4 定位——让元素脱离文档流

当 Flexbox 和 Grid 无法满足需求时（如固定导航栏、悬浮按钮），可以使用 `position` 属性：

```css
/* 相对定位：相对于元素原本的位置偏移，仍占据原空间 */
.relative {
    position: relative;
    top: 10px;
    left: 20px;
}

/* 绝对定位：相对于最近的已定位祖先元素定位，脱离文档流 */
.absolute {
    position: absolute;
    top: 0;
    right: 0;
}

/* 固定定位：相对于浏览器视口定位，滚动时不动 */
.fixed-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1000;  /* 层级，数值越大越靠前 */
}

/* 粘性定位：滚动到一定位置后固定 */
.sticky-nav {
    position: sticky;
    top: 0;
    background: white;
    z-index: 100;
}
```

!!! warning "绝对定位的参照物"

    绝对定位的元素会相对于 **最近的已定位祖先**（即 `position` 不为 `static` 的祖先）进行定位。如果找不到，则相对于 `<body>` 定位。因此，通常会给父元素设置 `position: relative` 来创建一个"定位上下文"。

---

## 3.5 响应式设计——一套代码适配所有屏幕

### 3.5.1 什么是响应式设计？

**响应式设计（Responsive Design）** 的核心思想是：**同一套 HTML 和 CSS，在不同屏幕尺寸下自动调整布局**，让网页在手机、平板、电脑上都有良好的体验。

### 3.5.2 视口 Meta 标签

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**代码解读：** 这行代码告诉移动端浏览器："请使用设备的实际宽度作为视口宽度，初始缩放比例为 1"。**没有这行代码，移动端浏览器会以桌面端宽度渲染页面，导致文字极小。**

### 3.5.3 媒体查询——响应式的核心武器

```css
/* 基础样式：移动端优先（Mobile First） */
.card-grid {
    display: grid;
    grid-template-columns: 1fr;  /* 手机：单列 */
    gap: 16px;
}

/* 平板（宽度 ≥ 768px） */
@media (min-width: 768px) {
    .card-grid {
        grid-template-columns: repeat(2, 1fr);  /* 平板：两列 */
    }
}

/* 桌面（宽度 ≥ 1024px） */
@media (min-width: 1024px) {
    .card-grid {
        grid-template-columns: repeat(3, 1fr);  /* 桌面：三列 */
    }
}
```

**代码解读：**

- `@media (min-width: 768px)` 表示"当屏幕宽度 ≥ 768px 时，应用以下样式"。
- 采用 **移动优先（Mobile First）** 策略：基础样式为手机设计，然后用 `min-width` 逐步增强大屏体验。
- 常见的断点：576px（大手机）、768px（平板）、992px（小桌面）、1200px（大桌面）。

### 3.5.4 响应式排版

```css
html {
    /* 基础字号 16px */
    font-size: 16px;
}

/* 平板及以上适当增大字号 */
@media (min-width: 768px) {
    html {
        font-size: 18px;
    }
}

/* 使用 rem 单位，相对于根元素字号 */
h1 {
    font-size: 2rem;     /* 手机：32px，平板：36px */
}

p {
    font-size: 1rem;     /* 手机：16px，平板：18px */
    line-height: 1.6;
}
```

### 3.5.5 响应式图片

```css
/* 图片不超出容器 */
img {
    max-width: 100%;
    height: auto;
    display: block;
}
```

```html
<!-- 根据屏幕分辨率加载不同尺寸的图片 -->
<img
    src="image-400.jpg"
    srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
    sizes="(max-width: 768px) 100vw, 50vw"
    alt="响应式图片"
>
```

### 3.5.6 响应式导航栏（汉堡菜单）

```html
<nav class="responsive-nav">
    <div class="nav-brand">MySite</div>
    <button class="hamburger" aria-label="菜单">☰</button>
    <ul class="nav-menu">
        <li><a href="#">首页</a></li>
        <li><a href="#">关于</a></li>
        <li><a href="#">服务</a></li>
        <li><a href="#">联系</a></li>
    </ul>
</nav>
```

```css
.responsive-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    background: #2c3e50;
    color: white;
}

.nav-brand {
    font-size: 20px;
    font-weight: bold;
}

.hamburger {
    display: block;
    background: none;
    border: none;
    color: white;
    font-size: 24px;
    cursor: pointer;
}

.nav-menu {
    display: none;          /* 手机端默认隐藏 */
    flex-direction: column;
    list-style: none;
    position: absolute;
    top: 60px;
    left: 0;
    width: 100%;
    background: #34495e;
    padding: 15px 0;
}

.nav-menu.active {
    display: flex;          /* 点击汉堡按钮后显示 */
}

.nav-menu a {
    color: white;
    text-decoration: none;
    padding: 10px 20px;
    display: block;
}

/* 平板及以上：显示完整导航，隐藏汉堡按钮 */
@media (min-width: 768px) {
    .hamburger {
        display: none;
    }

    .nav-menu {
        display: flex;
        flex-direction: row;
        position: static;
        background: none;
        padding: 0;
    }

    .nav-menu a {
        padding: 0 15px;
    }
}
```

---

## 3.6 CSS 变量——让样式更灵活

CSS 变量（Custom Properties）让你可以定义可复用的值：

```css
:root {
    /* 定义全局 CSS 变量 */
    --primary-color: #4A90D9;
    --secondary-color: #764ba2;
    --text-color: #333333;
    --bg-color: #fafafa;
    --border-radius: 8px;
    --spacing-unit: 16px;
    --max-width: 1200px;
}

/* 使用变量 */
.button {
    background-color: var(--primary-color);
    border-radius: var(--border-radius);
    padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
}

/* 变量可以带默认值 */
.card {
    background: var(--card-bg, white);  /* 如果 --card-bg 未定义，使用 white */
}
```

**代码解读：**

- `:root` 选择器指向文档根元素（`<html>`），在这里定义的变量全局可用。
- 使用 `var(--变量名)` 引用变量。
- CSS 变量的最大优势：修改一个值，所有引用处自动更新，非常适合做主题切换。

---

## 3.7 实践任务：阅读并分析响应式布局

### 任务要求

下面是博客页面的响应式布局 CSS 代码。你的任务是 **逐段阅读并理解布局在不同屏幕下的变化**，回答以下问题：

- 移动端（< 768px）的 `grid-template-areas` 是如何排列各区域的？
- 平板端（≥ 768px）相比移动端，布局发生了什么变化？
- 桌面端（≥ 1024px）新增了哪个区域？三列分别是什么？
- CSS 变量（`--*`）在这个布局中起到了什么作用？
- 如果你想让平板端也显示三列，应该修改哪个媒体查询？

### 参考代码

```css
/* responsive-blog.css */
/* ========== CSS 变量 ========== */
:root {
    --primary: #4A90D9;
    --primary-dark: #357ABD;
    --bg: #f5f6fa;
    --card-bg: #ffffff;
    --text: #2c3e50;
    --text-light: #7f8c8d;
    --border: #ecf0f1;
    --radius: 8px;
    --shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    --max-width: 1200px;
}

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
    color: var(--text);
    background: var(--bg);
}

img {
    max-width: 100%;
    height: auto;
}

/* ========== 移动端优先（< 768px）========== */
.page-layout {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-areas:
        "header"
        "main"
        "sidebar"
        "footer";
    gap: 20px;
    padding: 15px;
    max-width: var(--max-width);
    margin: 0 auto;
}

/* 页眉 */
.page-header {
    grid-area: header;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 25px 20px;
    border-radius: var(--radius);
    text-align: center;
}

/* 主体 */
.page-main {
    grid-area: main;
}

/* 侧边栏 */
.page-sidebar {
    grid-area: sidebar;
}

/* 页脚 */
.page-footer {
    grid-area: footer;
    text-align: center;
    padding: 20px;
    color: var(--text-light);
    font-size: 14px;
}

/* 卡片通用样式 */
.card {
    background: var(--card-bg);
    border-radius: var(--radius);
    padding: 25px;
    box-shadow: var(--shadow);
    margin-bottom: 20px;
}

/* ========== 平板端（≥ 768px）========== */
@media (min-width: 768px) {
    .page-layout {
        grid-template-columns: 1fr 280px;
        grid-template-areas:
            "header  header"
            "main    sidebar"
            "footer  footer";
        gap: 24px;
        padding: 24px;
    }
}

/* ========== 桌面端（≥ 1024px）========== */
@media (min-width: 1024px) {
    .page-layout {
        grid-template-columns: 220px 1fr 300px;
        grid-template-areas:
            "header  header  header"
            "nav     main    sidebar"
            "footer  footer  footer";
        gap: 30px;
        padding: 30px;
    }

    .page-nav {
        grid-area: nav;
        display: block;
    }
}
```

### 验证步骤

1. 将 CSS 代码保存并引入到博客页面中。
2. 用浏览器打开页面，按 F12 打开开发者工具。
3. 点击"Toggle Device Toolbar"（Ctrl+Shift+M），切换不同设备预览。
4. 分别选择 iPhone、iPad、Desktop 三种预设，观察布局变化——注意 `grid-template-areas` 在不同断点下的切换。
5. 手动拖拽浏览器窗口宽度，观察布局在 768px 和 1024px 断点处的实时切换效果。

---

## 📋 本章要点总结

- [ ] 理解文档流，能区分块级元素和行内元素
- [ ] 掌握 `display` 属性的核心值：`block`、`inline`、`inline-block`、`none`、`flex`、`grid`
- [ ] 熟练使用 Flexbox：`justify-content`、`align-items`、`flex`、`gap`
- [ ] 理解主轴与交叉轴的概念
- [ ] 掌握 Grid 布局：`grid-template-columns`、`grid-template-areas`、`fr` 单位
- [ ] 能使用 `auto-fill` + `minmax` 创建自适应卡片网格
- [ ] 理解 `position` 的四种值：`relative`、`absolute`、`fixed`、`sticky`
- [ ] 掌握媒体查询 `@media` 的语法和常用断点
- [ ] 理解"移动优先"的设计策略
- [ ] 会使用 CSS 变量（`--*`）管理设计令牌
- [ ] 能独立实现一个响应式页面布局

---

## 📚 课后练习

### 基础练习

1. 使用 Flexbox 创建一个水平居中的导航栏，包含 5 个链接。
2. 使用 Grid 创建一个 3×2 的图片画廊（6 张图片均匀排列）。

### 进阶挑战

3. 使用 Grid + 媒体查询，创建一个"产品展示"页面：手机 1 列、平板 2 列、桌面 3 列。
4. 使用 `position: sticky` 创建一个"滚动时吸附在顶部"的导航栏。

---

👉 [进入第 4 章：JavaScript 基础语法 →](04-javascript-basics.md)
