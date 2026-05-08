# 第 1 章：HTML5 语义化与文档结构——搭建网页的"钢筋骨架"

## 📺 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 理解 HTML 的本质与作用，掌握 HTML5 语义化标签，能阅读和理解任意网页的 HTML 源码 |
| **核心比喻** | **房屋骨架（钢筋水泥）** —— HTML 定义网页的结构，就像钢筋水泥定义建筑的框架 |
| **预计时长** | 90 分钟 |
| **关键概念** | 标签、元素、属性、语义化、DOM 树、HTML5 文档结构 |
| **实践任务** | 阅读并分析一个博客文章页面的 HTML 结构，理解每个标签的作用 |

---

如果把一个网页比作一栋房子，那么 HTML 就是这栋房子的**钢筋水泥骨架**。没有骨架，房子就立不起来；同样，没有 HTML，网页就无从谈起。在这一章中，我们将从零开始，理解 HTML 的本质，并学会用 HTML5 的语义化标签搭建出结构清晰、含义明确的网页。

---

## 1.1 什么是 HTML？—— 认识网页的"骨架"

### 1.1.1 HTML 的全称与本质

HTML 的全称是 **HyperText Markup Language**（超文本标记语言）。拆开来看：

- **HyperText（超文本）**：不仅仅是纯文字，还可以包含链接、图片、视频等多媒体内容。点击一个链接就能跳转到另一个页面——这就是"超"的含义。
- **Markup（标记）**：用特定的符号（标签）来"标记"内容的含义。比如用 `<h1>` 标记"这是一级标题"，用 `<p>` 标记"这是一个段落"。
- **Language（语言）**：它是一套有规则的语法体系，浏览器能读懂并按照规则渲染出页面。

!!! info "关键认知：HTML 不是编程语言"

    HTML 是一种**标记语言**，不是编程语言。它没有"逻辑判断"（if-else）、没有"循环"（for/while），它只负责**描述内容的结构和含义**。你可以把它理解为一种"文档格式"，就像 Word 文档的 .docx 格式一样——只不过 HTML 是给浏览器看的。

### 1.1.2 一个最简单的 HTML 页面

让我们从一个最简化的例子开始，感受 HTML 的基本形态：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>我的第一个网页</title>
</head>
<body>
    <h1>欢迎来到我的网站</h1>
    <p>这是我用 HTML 写的第一段话。</p>
</body>
</html>
```

**代码解读：**

| 行 | 代码 | 含义 |
|:---|:---|:---|
| 1 | `<!DOCTYPE html>` | 声明文档类型为 HTML5，告诉浏览器"请按 HTML5 标准解析我" |
| 2 | `<html lang="zh-CN">` | 整个 HTML 文档的根元素，`lang="zh-CN"` 表示页面语言是简体中文 |
| 3 | `<head>` | 头部区域，存放页面的"元信息"（给浏览器和搜索引擎看的，不直接显示） |
| 4 | `<meta charset="UTF-8">` | 设置字符编码为 UTF-8，确保中文不会乱码 |
| 5 | `<title>` | 浏览器标签页上显示的标题 |
| 6 | `</head>` | 头部区域结束 |
| 7 | `<body>` | 主体区域，所有在页面上**可见的内容**都放在这里 |
| 8 | `<h1>` | 一级标题（Heading 1），通常用于页面主标题 |
| 9 | `<p>` | 段落（Paragraph） |
| 10-11 | `</body></html>` | 关闭主体和文档 |

!!! tip "动手试一试"

    将上面的代码复制到 VS Code 中，保存为 `index.html`，然后用浏览器打开这个文件。你会看到一个最简单的网页——这就是你前端之旅的第一步！

**渲染效果：** 浏览器打开后，你会看到：
- 标签页标题显示"我的第一个网页"
- 页面中央显示大号加粗的"欢迎来到我的网站"
- 下方显示普通大小的"这是我用 HTML 写的第一段话。"
- 整个页面背景为白色，文字为黑色（浏览器默认样式）

---

## 1.2 HTML 标签的核心概念

### 1.2.1 标签、元素与属性

在深入之前，我们需要先理清三个容易混淆的概念：

**标签（Tag）**：用尖括号 `<>` 包裹的关键词，如 `<p>`、`<h1>`、`<img>`。

**元素（Element）**：从开始标签到结束标签的完整结构，包括其中的内容。例如：

```html
<p>这是一段文字。</p>
```

上面这整行就是一个"段落元素"，它由开始标签 `<p>`、内容"这是一段文字。"和结束标签 `</p>` 组成。

**属性（Attribute）**：写在开始标签内部的额外信息，用于配置元素的行为或样式。格式为 `属性名="属性值"`：

```html
<a href="https://www.example.com">点击跳转</a>
<img src="photo.jpg" alt="一张照片">
```

**代码解读：**

- `href` 是 `<a>` 标签的属性，指定链接目标地址。
- `src` 是 `<img>` 标签的属性，指定图片文件路径。
- `alt` 是 `<img>` 标签的属性，当图片无法显示时，显示这段替代文字。

### 1.2.2 双标签与单标签

HTML 标签分为两种类型：

| 类型 | 格式 | 示例 | 说明 |
|:---|:---|:---|:---|
| **双标签（容器标签）** | `<标签>内容</标签>` | `<p>文字</p>`、`<div>...</div>` | 有开始和结束，中间包裹内容 |
| **单标签（空标签）** | `<标签>` 或 `<标签 />` | `<br>`、`<img src="...">`、`<hr>` | 没有结束标签，自身就是完整的 |

!!! note "常见单标签速查"

    - `<br>` —— 换行（Break）
    - `<hr>` —— 水平分割线（Horizontal Rule）
    - `<img>` —— 图片（Image）
    - `<input>` —— 输入框
    - `<meta>` —— 元数据（只在 `<head>` 中使用）
    - `<link>` —— 引入外部资源（CSS 文件等）

### 1.2.3 标签的嵌套规则

HTML 标签可以像俄罗斯套娃一样嵌套，但必须遵循**"先开后关，后开先关"**的原则：

```html
<!-- ✅ 正确：p 标签完全包裹在 div 内部 -->
<div>
    <p>这是一段文字。</p>
</div>

<!-- ❌ 错误：标签交叉嵌套 -->
<div>
    <p>这是一段文字。
</div>
</p>
```

**代码解读：** 可以把嵌套想象成括号匹配——每个开始标签都必须有一个对应的结束标签，且嵌套顺序不能交叉。浏览器的解析器虽然有一定的容错能力，但错误的嵌套可能导致页面渲染异常。

---

## 1.3 HTML5 语义化标签体系

### 1.3.1 什么是"语义化"？

**语义化（Semantic）** 就是"让标签具有含义"。在 HTML5 之前，开发者大量使用 `<div>` 和 `<span>` 来搭建页面结构，但这些标签本身没有任何含义——`<div>` 只是一个"块级容器"，你不知道它里面装的是导航栏还是文章正文。

HTML5 引入了一系列**语义化标签**，每个标签的名字本身就说明了它的用途：

```html
<!-- ❌ HTML4 时代：全是 div，含义不明 -->
<div class="header">...</div>
<div class="nav">...</div>
<div class="article">...</div>
<div class="footer">...</div>

<!-- ✅ HTML5 时代：标签即文档 -->
<header>...</header>
<nav>...</nav>
<article>...</article>
<footer>...</footer>
```

!!! info "语义化的三大好处"

    1. **对开发者友好**：看到 `<nav>` 就知道这是导航栏，看到 `<article>` 就知道这是文章正文，代码可读性大幅提升。
    2. **对搜索引擎友好（SEO）**：搜索引擎能更好地理解页面结构，从而更准确地索引你的内容。
    3. **对辅助设备友好（无障碍访问）**：屏幕阅读器能根据语义标签，为视障用户提供更好的导航体验。

### 1.3.2 核心语义化标签详解

#### 页面结构标签

```html
<body>
    <header>
        <!-- 页眉：通常包含网站 Logo、标题、导航栏 -->
    </header>

    <nav>
        <!-- 导航栏：包含主要导航链接 -->
    </nav>

    <main>
        <!-- 页面主体内容，每个页面只能有一个 <main> -->
        <article>
            <!-- 独立的文章内容，可以独立分发和复用 -->
        </article>

        <aside>
            <!-- 侧边栏：与主体内容相关的补充信息 -->
        </aside>
    </main>

    <footer>
        <!-- 页脚：版权信息、联系方式、友情链接等 -->
    </footer>
</body>
```

**代码解读：**

| 标签 | 含义 | 使用场景 |
|:---|:---|:---|
| `<header>` | 页眉/头部 | 网站顶部区域，通常包含 Logo、标题、导航 |
| `<nav>` | 导航 | 主要导航链接的集合（注意：不是所有链接组都用 nav） |
| `<main>` | 主体内容 | 页面的核心内容区域，**每个页面只能有一个** |
| `<article>` | 独立文章 | 博客文章、新闻报道、论坛帖子等可独立分发的内容 |
| `<section>` | 章节 | 对内容进行分组，通常带有一个标题 |
| `<aside>` | 侧边栏/附加内容 | 与主体内容相关的补充信息，如相关文章、广告等 |
| `<footer>` | 页脚 | 网站底部区域，版权、联系方式等 |

**渲染效果：** 在浏览器中，这些语义标签默认的视觉效果与 `<div>` 几乎一样——它们都是块级元素，各占一行。语义标签的真正价值不在于"长什么样"，而在于"表达了什么含义"。搜索引擎、屏幕阅读器和开发者工具都会利用这些语义信息来理解页面结构。

#### 文本内容标签

```html
<h1>一级标题（通常一个页面只有一个）</h1>
<h2>二级标题</h2>
<h3>三级标题</h3>
<!-- h4、h5、h6 依次递减 -->

<p>这是一个段落。段落之间会自动换行并保持间距。</p>

<ul>
    <li>无序列表项 1</li>
    <li>无序列表项 2</li>
</ul>

<ol>
    <li>有序列表项 1</li>
    <li>有序列表项 2</li>
</ol>

<strong>加粗且语义重要</strong>
<em>斜体且语义强调</em>
<code>行内代码片段</code>
<blockquote>这是一段引用文字。</blockquote>
```

!!! warning "`<b>` vs `<strong>`，`<i>` vs `<em>`"

    很多初学者会困惑：`<b>` 和 `<strong>` 都是加粗，`<i>` 和 `<em>` 都是斜体，有什么区别？
    
    - `<b>` 和 `<i>` 是**纯视觉**标签，只改变外观，没有语义含义。
    - `<strong>` 表示**内容很重要**（语义强调），浏览器默认将其渲染为加粗。
    - `<em>` 表示**内容需要重读**（语义强调），浏览器默认将其渲染为斜体。
    
    **建议**：优先使用 `<strong>` 和 `<em>`，它们不仅改变外观，还传达了语义。

### 1.3.3 多媒体标签

HTML5 原生支持音频和视频，不再需要 Flash 插件：

```html
<!-- 图片 -->
<img src="photo.jpg" alt="一张风景照片" width="400" height="300">

<!-- 视频 -->
<video controls width="640">
    <source src="movie.mp4" type="video/mp4">
    <source src="movie.webm" type="video/webm">
    你的浏览器不支持视频播放。
</video>

<!-- 音频 -->
<audio controls>
    <source src="music.mp3" type="audio/mpeg">
    你的浏览器不支持音频播放。
</audio>
```

**代码解读：**

- `<img>` 的 `alt` 属性非常重要：当图片加载失败时显示替代文字，同时也是无障碍访问的关键。
- `<video>` 和 `<audio>` 的 `controls` 属性会显示播放控制条（播放/暂停/音量等）。
- 多个 `<source>` 提供不同格式的备选方案，浏览器会选择第一个支持的格式。

---

## 1.4 链接与路径

### 1.4.1 超链接 `<a>`

超链接是 Web 的基石——它让不同的页面相互连接，形成"网"：

```html
<!-- 跳转到外部网站（在新标签页打开） -->
<a href="https://www.example.com" target="_blank" rel="noopener noreferrer">
    访问 Example 网站
</a>

<!-- 跳转到本站其他页面（相对路径） -->
<a href="about.html">关于我们</a>

<!-- 跳转到页面内的某个位置（锚点） -->
<a href="#section2">跳转到第二节</a>

<!-- 下载文件 -->
<a href="document.pdf" download>下载 PDF 文档</a>

<!-- 发送邮件 -->
<a href="mailto:hello@example.com">发送邮件</a>
```

**代码解读：**

| 属性 | 含义 | 常用值 |
|:---|:---|:---|
| `href` | 链接目标地址 | URL 或页面内锚点 `#id` |
| `target` | 打开方式 | `_blank`（新标签页）、`_self`（当前页，默认） |
| `rel` | 链接关系 | `noopener noreferrer`（安全最佳实践，配合 `target="_blank"` 使用） |
| `download` | 提示浏览器下载而非打开 | 可指定下载后的文件名 |

!!! danger "安全警示：`target="_blank"` 的安全风险"

    当你使用 `target="_blank"` 时，新打开的页面可以通过 `window.opener` 对象访问原页面的部分信息。为防止这种安全风险，**务必同时添加 `rel="noopener noreferrer"`**。

### 1.4.2 路径的三种写法

理解路径是阅读前端代码的基本功：

```html
<!-- 1. 绝对路径：完整的 URL -->
<img src="https://www.example.com/images/photo.jpg" alt="">

<!-- 2. 相对路径（相对于当前文件的位置） -->
<img src="images/photo.jpg" alt="">           <!-- 同级目录下的 images 文件夹 -->
<img src="./images/photo.jpg" alt="">          <!-- 同上，./ 表示当前目录 -->
<img src="../images/photo.jpg" alt="">         <!-- 上一级目录下的 images 文件夹 -->

<!-- 3. 根相对路径（相对于网站根目录） -->
<img src="/images/photo.jpg" alt="">           <!-- 网站根目录下的 images 文件夹 -->
```

**代码解读：**

- `./` 表示当前目录（通常可以省略）。
- `../` 表示上一级目录，可以连续使用如 `../../` 表示上两级。
- 以 `/` 开头的路径表示从网站根目录开始查找。

---

## 1.5 表单基础

表单是用户与网页交互的主要方式——登录、搜索、评论、购物，都离不开表单：

```html
<form action="/submit" method="POST">
    <!-- 文本输入 -->
    <label for="username">用户名：</label>
    <input type="text" id="username" name="username" placeholder="请输入用户名" required>

    <!-- 密码输入 -->
    <label for="password">密码：</label>
    <input type="password" id="password" name="password" placeholder="请输入密码" required>

    <!-- 电子邮件 -->
    <label for="email">邮箱：</label>
    <input type="email" id="email" name="email" placeholder="example@mail.com">

    <!-- 单选按钮 -->
    <fieldset>
        <legend>性别：</legend>
        <input type="radio" id="male" name="gender" value="male">
        <label for="male">男</label>
        <input type="radio" id="female" name="gender" value="female">
        <label for="female">女</label>
    </fieldset>

    <!-- 复选框 -->
    <input type="checkbox" id="agree" name="agree" required>
    <label for="agree">我同意服务条款</label>

    <!-- 下拉选择 -->
    <label for="city">城市：</label>
    <select id="city" name="city">
        <option value="">请选择</option>
        <option value="beijing">北京</option>
        <option value="shanghai">上海</option>
    </select>

    <!-- 文本域 -->
    <label for="message">留言：</label>
    <textarea id="message" name="message" rows="4" placeholder="请输入留言内容"></textarea>

    <!-- 提交按钮 -->
    <button type="submit">提交</button>
    <button type="reset">重置</button>
</form>
```

**代码解读：**

| 元素/属性 | 含义 |
|:---|:---|
| `<form>` | 表单容器，`action` 指定提交地址，`method` 指定提交方式（GET/POST） |
| `<label>` | 标签文字，`for` 属性关联对应输入框的 `id`，点击标签可聚焦输入框 |
| `<input>` | 万能输入控件，`type` 决定其形态（text/password/email/radio/checkbox 等） |
| `placeholder` | 输入框内的提示文字，用户开始输入后消失 |
| `required` | 必填验证，表单提交前浏览器会自动检查 |
| `<fieldset>` + `<legend>` | 将相关表单控件分组，`<legend>` 是分组标题 |
| `<select>` + `<option>` | 下拉选择框 |
| `<textarea>` | 多行文本输入框 |

**渲染效果：** 浏览器会渲染出一个完整的表单界面——文本框带圆角边框、单选按钮是圆形、复选框是方形、下拉框点击后展开选项列表。`placeholder` 文字显示为灰色，用户开始输入后自动消失。带有 `required` 属性的字段如果为空就提交，浏览器会弹出提示并高亮该字段。

---

## 1.6 HTML 实体字符

有些字符在 HTML 中有特殊含义（如 `<` 和 `>` 用于标签），如果你想在页面上显示这些字符本身，需要使用**实体字符（HTML Entities）**：

| 显示效果 | 实体写法 | 说明 |
|:---|:---|:---|
| `<` | `&lt;` | 小于号（Less Than） |
| `>` | `&gt;` | 大于号（Greater Than） |
| `&` | `&amp;` | 与符号（Ampersand） |
| `"` | `&quot;` | 双引号（Quotation） |
| `'` | `&apos;` | 单引号（Apostrophe） |
| ` ` | `&nbsp;` | 不换行空格（Non-Breaking Space） |
| © | `&copy;` | 版权符号 |

```html
<!-- 如果你想在页面上显示 "<p>这是一段文字</p>" 这段代码本身 -->
<p>HTML 段落标签的写法是：&lt;p&gt;这是一段文字&lt;/p&gt;</p>
```

---

## 1.7 实践任务：阅读并分析博客文章页面

现在，让我们把学到的知识整合起来。下面是一个结构完整的博客文章页面，你的任务是**逐行阅读并理解每个标签的作用**，而不是自己从零写。

### 任务要求

阅读以下 HTML 代码，回答这些问题：

- 页面的 `<head>` 区域包含了哪些元信息？
- 页面使用了哪些语义化标签？每个标签代表页面的哪个区域？
- 表单中包含哪些类型的输入控件？每个控件的 `name` 属性是什么？
- 如果你要修改作者名字，应该改哪个标签的内容？
- 如果你要添加一个新的导航链接，应该在哪个标签内部添加？

### 参考代码

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML5 入门指南 - 我的技术博客</title>
</head>
<body>
    <!-- 页眉 -->
    <header>
        <h1>📝 我的技术博客</h1>
        <nav>
            <a href="index.html">首页</a>
            <a href="about.html">关于</a>
            <a href="archive.html">归档</a>
        </nav>
    </header>

    <!-- 主体内容 -->
    <main>
        <!-- 文章 -->
        <article>
            <header>
                <h2>HTML5 入门指南：从零搭建你的第一个网页</h2>
                <p>
                    <strong>作者：</strong>张三
                    <strong>发布时间：</strong><time datetime="2026-05-08">2026年5月8日</time>
                </p>
            </header>

            <section>
                <h3>什么是 HTML？</h3>
                <p>HTML（超文本标记语言）是构建网页的基础语言。它使用标签来描述网页的结构和内容。</p>
                <p>每个 HTML 文档都由嵌套的<strong>元素</strong>组成，每个元素由<strong>标签</strong>定义。</p>
            </section>

            <section>
                <h3>第一个 HTML 页面</h3>
                <p>下面是一个最简单的 HTML 页面结构：</p>
                <pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="zh-CN"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;我的第一个网页&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;Hello World!&lt;/h1&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
            </section>

            <section>
                <h3>小结</h3>
                <p>通过本章的学习，你已经掌握了 HTML5 的核心概念和常用标签。接下来，我们将学习如何用 CSS3 为网页添加样式。</p>
            </section>
        </article>

        <!-- 评论区 -->
        <section>
            <h3>评论</h3>
            <form action="/comment" method="POST">
                <label for="name">昵称：</label>
                <input type="text" id="name" name="name" required>

                <label for="comment">评论内容：</label>
                <textarea id="comment" name="comment" rows="4" required></textarea>

                <button type="submit">发表评论</button>
            </form>
        </section>
    </main>

    <!-- 侧边栏 -->
    <aside>
        <section>
            <h3>关于作者</h3>
            <p>张三，前端开发工程师，热爱技术分享。</p>
        </section>
        <section>
            <h3>相关文章</h3>
            <ul>
                <li><a href="#">CSS3 入门指南</a></li>
                <li><a href="#">JavaScript 基础教程</a></li>
            </ul>
        </section>
    </aside>

    <!-- 页脚 -->
    <footer>
        <p>&copy; 2026 我的技术博客. All rights reserved.</p>
    </footer>
</body>
</html>
```

### 验证步骤

1. 将代码保存为 `blog-post.html`，用浏览器打开，观察页面渲染效果。
2. 按 F12 打开开发者工具，在 Elements 面板中查看 DOM 树结构——你能找到每个语义标签对应的位置吗？
3. 在 Elements 面板中，尝试双击修改标题文字和作者名字，页面会实时更新。
4. 右键点击任意元素 → "Edit as HTML"，尝试修改一段文字，观察页面变化。

---

## 📋 本章要点总结

- [ ] 理解 HTML 是"标记语言"而非"编程语言"，它描述内容的结构和含义
- [ ] 掌握 HTML5 文档的基本结构：`<!DOCTYPE html>` → `<html>` → `<head>` + `<body>`
- [ ] 能区分双标签（`<p>内容</p>`）和单标签（`<img>`、`<br>`）
- [ ] 理解标签嵌套的"先开后关"原则
- [ ] 掌握至少 10 个 HTML5 语义化标签：`<header>`、`<nav>`、`<main>`、`<article>`、`<section>`、`<aside>`、`<footer>`、`<h1>-<h6>`、`<p>`、`<ul>/<ol>/<li>`
- [ ] 理解 `<strong>` 和 `<b>`、`<em>` 和 `<i>` 的语义区别
- [ ] 能正确使用 `<a>` 标签创建链接，理解绝对路径和相对路径
- [ ] 掌握表单的基本结构：`<form>` + `<input>` + `<label>` + `<button>`
- [ ] 了解 HTML 实体字符的用途（`&lt;`、`&gt;`、`&amp;`、`&copy;`）

---

## 📚 课后练习

### 基础练习

1. 创建一个"个人简介"页面，包含你的姓名（`<h1>`）、一段自我介绍（`<p>`）、你的技能列表（`<ul>`）和联系方式（`<a>` 链接）。
2. 创建一个"食谱"页面，使用有序列表（`<ol>`）列出制作步骤，使用无序列表（`<ul>`）列出所需食材。

### 进阶挑战

3. 使用所有学过的语义化标签（`<header>`、`<nav>`、`<main>`、`<article>`、`<section>`、`<aside>`、`<footer>`），搭建一个完整的"新闻门户"首页结构。
4. 创建一个"用户注册"表单，包含用户名、密码、邮箱、性别（单选）、爱好（多选）、城市（下拉选择）和个人简介（文本域），并为每个输入框添加 `<label>`。

---

👉 [进入第 2 章：CSS3 样式与视觉美化 →](02-css3-styling.md)
