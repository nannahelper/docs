# 第 6 章：综合实战——打造个人主页

## 📺 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 通过阅读一个完整的响应式个人主页项目，综合理解 HTML、CSS、JavaScript 三者的协作方式 |
| **核心比喻** | **精装样板房** —— 将前面学到的所有知识整合成一个完整的、可交付的作品 |
| **预计时长** | 120 分钟 |
| **关键概念** | 项目结构、CSS 变量主题切换、打字机效果、Intersection Observer、表单验证、响应式导航 |
| **实践任务** | 逐段阅读个人主页的完整代码，理解每个模块的实现原理，尝试修改配色和内容 |

---

恭喜你来到了最后一章！前面五章我们分别学习了 HTML5 结构、CSS3 样式、响应式布局、JavaScript 语法和 DOM 操作。现在，是时候把这些知识 **融会贯通**，打造一个真正拿得出手的作品了。

本章我们将从零开始，一步步构建一个 **完整的个人主页**，包含以下功能模块：

- 🎨 导航栏（响应式，含移动端汉堡菜单）
- 🦸 英雄区（Hero Section，含打字机效果）
- 📋 关于我（个人简介 + 技能标签）
- 💼 项目展示（卡片网格布局）
- 📬 联系方式（表单 + 表单验证）
- 🌙 深色/浅色主题切换
- 📱 完全响应式（手机、平板、桌面）

---

## 6.1 项目概览

本章我们将 **逐段阅读** 一个完整的个人主页项目。这个项目整合了前五章的所有知识，是你理解"HTML + CSS + JS 如何协作"的最佳范例。

### 你将看到的效果

- **深色/浅色主题切换**：点击按钮，整个页面配色瞬间改变
- **打字机动画**：英雄区的职位描述像打字一样逐字出现
- **响应式布局**：手机、平板、桌面三种设备自动适配
- **滚动动画**：元素进入视口时优雅地淡入
- **表单验证**：实时检查用户输入，给出友好提示
- **平滑导航**：点击导航链接平滑滚动到对应区域

---

## 6.2 HTML 结构——搭建骨架

```html
<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>张三 - 前端开发工程师 | 个人主页</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="js/main.js" defer></script>
</head>
<body>
    <!-- ========== 导航栏 ========== -->
    <header class="header" id="header">
        <nav class="nav container">
            <a href="#" class="nav-logo">ZhangSan.dev</a>

            <ul class="nav-menu" id="nav-menu">
                <li><a href="#home" class="nav-link">首页</a></li>
                <li><a href="#about" class="nav-link">关于</a></li>
                <li><a href="#projects" class="nav-link">项目</a></li>
                <li><a href="#contact" class="nav-link">联系</a></li>
            </ul>

            <div class="nav-actions">
                <button class="theme-toggle" id="theme-toggle" aria-label="切换主题">
                    <span class="theme-icon">🌙</span>
                </button>
                <button class="hamburger" id="hamburger" aria-label="菜单">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </div>
        </nav>
    </header>

    <main>
        <!-- ========== 英雄区 ========== -->
        <section class="hero section" id="home">
            <div class="hero-container container">
                <div class="hero-content">
                    <p class="hero-greeting">你好，我是</p>
                    <h1 class="hero-name">张三</h1>
                    <p class="hero-title">
                        <span class="typed-text" id="typed-text"></span>
                        <span class="typed-cursor">|</span>
                    </p>
                    <p class="hero-description">
                        热爱前端开发，专注于构建优雅、高性能的 Web 应用。
                        相信代码可以改变世界，一行一行地。
                    </p>
                    <div class="hero-buttons">
                        <a href="#projects" class="btn btn-primary">查看作品</a>
                        <a href="#contact" class="btn btn-outline">联系我</a>
                    </div>
                </div>
                <div class="hero-image">
                    <div class="hero-avatar">
                        <img src="images/avatar.jpg" alt="张三的头像" onerror="this.style.display='none'; this.parentElement.innerHTML='<div style=\\'width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;color:white;font-size:48px;\\'>张</div>'">
                    </div>
                </div>
            </div>
            <a href="#about" class="scroll-down" aria-label="向下滚动">
                <span></span>
            </a>
        </section>

        <!-- ========== 关于我 ========== -->
        <section class="about section" id="about">
            <div class="container">
                <h2 class="section-title">关于我</h2>
                <p class="section-subtitle">一个热爱技术与生活的开发者</p>

                <div class="about-content">
                    <div class="about-text">
                        <p>
                            我是一名拥有 3 年经验的前端开发工程师，目前专注于 React 生态和现代 CSS 技术。
                            我相信好的用户体验来自于对细节的极致追求。
                        </p>
                        <p>
                            工作之余，我喜欢写技术博客、参与开源项目，也热衷于帮助新人入门前端开发。
                            这个个人主页就是我用纯 HTML、CSS 和 JavaScript 从零构建的。
                        </p>
                    </div>

                    <div class="skills">
                        <h3>技术栈</h3>
                        <div class="skill-tags">
                            <span class="skill-tag">HTML5</span>
                            <span class="skill-tag">CSS3</span>
                            <span class="skill-tag">JavaScript</span>
                            <span class="skill-tag">React</span>
                            <span class="skill-tag">Vue.js</span>
                            <span class="skill-tag">Node.js</span>
                            <span class="skill-tag">Git</span>
                            <span class="skill-tag">Webpack</span>
                            <span class="skill-tag">TypeScript</span>
                            <span class="skill-tag">Tailwind CSS</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ========== 项目展示 ========== -->
        <section class="projects section" id="projects">
            <div class="container">
                <h2 class="section-title">我的项目</h2>
                <p class="section-subtitle">一些我最近完成的作品</p>

                <div class="project-grid">
                    <article class="project-card">
                        <div class="project-image">
                            <div class="project-placeholder">📊</div>
                        </div>
                        <div class="project-info">
                            <h3>数据可视化仪表盘</h3>
                            <p>基于 ECharts 的实时数据监控面板，支持多种图表类型和自定义主题。</p>
                            <div class="project-tags">
                                <span>React</span>
                                <span>ECharts</span>
                                <span>WebSocket</span>
                            </div>
                            <div class="project-links">
                                <a href="#" class="btn btn-small">演示</a>
                                <a href="#" class="btn btn-small btn-outline">源码</a>
                            </div>
                        </div>
                    </article>

                    <article class="project-card">
                        <div class="project-image">
                            <div class="project-placeholder">🛒</div>
                        </div>
                        <div class="project-info">
                            <h3>电商小程序</h3>
                            <p>全栈电商应用，包含商品浏览、购物车、订单管理和支付集成。</p>
                            <div class="project-tags">
                                <span>Vue.js</span>
                                <span>Node.js</span>
                                <span>MongoDB</span>
                            </div>
                            <div class="project-links">
                                <a href="#" class="btn btn-small">演示</a>
                                <a href="#" class="btn btn-small btn-outline">源码</a>
                            </div>
                        </div>
                    </article>

                    <article class="project-card">
                        <div class="project-image">
                            <div class="project-placeholder">📝</div>
                        </div>
                        <div class="project-info">
                            <h3>Markdown 编辑器</h3>
                            <p>支持实时预览的 Markdown 编辑器，支持语法高亮和自定义主题。</p>
                            <div class="project-tags">
                                <span>TypeScript</span>
                                <span>CodeMirror</span>
                            </div>
                            <div class="project-links">
                                <a href="#" class="btn btn-small">演示</a>
                                <a href="#" class="btn btn-small btn-outline">源码</a>
                            </div>
                        </div>
                    </article>
                </div>
            </div>
        </section>

        <!-- ========== 联系方式 ========== -->
        <section class="contact section" id="contact">
            <div class="container">
                <h2 class="section-title">联系我</h2>
                <p class="section-subtitle">有任何问题或合作意向，欢迎随时联系</p>

                <form class="contact-form" id="contact-form">
                    <div class="form-group">
                        <label for="name">姓名</label>
                        <input type="text" id="name" name="name" placeholder="请输入你的姓名" required>
                        <span class="error-message"></span>
                    </div>

                    <div class="form-group">
                        <label for="email">邮箱</label>
                        <input type="email" id="email" name="email" placeholder="请输入你的邮箱" required>
                        <span class="error-message"></span>
                    </div>

                    <div class="form-group">
                        <label for="subject">主题</label>
                        <input type="text" id="subject" name="subject" placeholder="请输入主题">
                    </div>

                    <div class="form-group">
                        <label for="message">留言</label>
                        <textarea id="message" name="message" rows="5" placeholder="请输入你的留言内容" required></textarea>
                        <span class="error-message"></span>
                    </div>

                    <button type="submit" class="btn btn-primary btn-block">
                        <span class="btn-text">发送消息</span>
                        <span class="btn-loading" style="display:none;">发送中...</span>
                    </button>
                </form>
            </div>
        </section>
    </main>

    <!-- ========== 页脚 ========== -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <p class="footer-copy">&copy; 2026 张三. All rights reserved.</p>
                <div class="footer-social">
                    <a href="#" aria-label="GitHub" title="GitHub">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
                    </a>
                    <a href="#" aria-label="Email" title="Email">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 4L12 13 2 4"/></svg>
                    </a>
                </div>
            </div>
        </div>
    </footer>

    <!-- 返回顶部按钮 -->
    <button class="back-to-top" id="back-to-top" aria-label="返回顶部">↑</button>
</body>
</html>
```

---

## 6.3 CSS 样式——穿上漂亮的衣服

```css
/* ============================================
   CSS 变量 & 主题系统
   ============================================ */
:root {
    /* 颜色 */
    --primary: #667eea;
    --primary-dark: #5a6fd6;
    --secondary: #764ba2;
    --accent: #f093fb;

    /* 浅色主题 */
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --bg-card: #ffffff;
    --text-primary: #2c3e50;
    --text-secondary: #636e72;
    --text-muted: #b2bec3;
    --border: #e9ecef;
    --shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    --shadow-hover: 0 8px 30px rgba(0, 0, 0, 0.12);

    /* 尺寸 */
    --header-height: 70px;
    --max-width: 1100px;
    --radius: 12px;
    --radius-sm: 6px;
    --transition: 0.3s ease;
}

/* 深色主题 */
[data-theme="dark"] {
    --bg-primary: #1a1a2e;
    --bg-secondary: #16213e;
    --bg-card: #1f2b47;
    --text-primary: #e4e6eb;
    --text-secondary: #b0b3b8;
    --text-muted: #6c757d;
    --border: #2d3748;
    --shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    --shadow-hover: 0 8px 30px rgba(0, 0, 0, 0.4);
}

/* ============================================
   全局重置
   ============================================ */
*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    scroll-behavior: smooth;
    scroll-padding-top: var(--header-height);
}

body {
    font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", sans-serif;
    font-size: 16px;
    line-height: 1.7;
    color: var(--text-primary);
    background-color: var(--bg-primary);
    transition: background-color var(--transition), color var(--transition);
}

img {
    max-width: 100%;
    height: auto;
    display: block;
}

a {
    color: var(--primary);
    text-decoration: none;
    transition: color var(--transition);
}

.container {
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 0 24px;
}

.section {
    padding: 80px 0;
}

.section-title {
    font-size: 32px;
    text-align: center;
    margin-bottom: 12px;
    color: var(--text-primary);
}

.section-subtitle {
    text-align: center;
    color: var(--text-secondary);
    margin-bottom: 48px;
    font-size: 17px;
}

/* ============================================
   导航栏
   ============================================ */
.header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: var(--header-height);
    background: var(--bg-primary);
    box-shadow: 0 1px 10px rgba(0, 0, 0, 0.05);
    z-index: 1000;
    transition: background var(--transition), box-shadow var(--transition);
}

.header.scrolled {
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
}

.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
}

.nav-logo {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.5px;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 32px;
}

.nav-link {
    color: var(--text-secondary);
    font-size: 15px;
    font-weight: 500;
    position: relative;
    padding: 4px 0;
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--primary);
    transition: width var(--transition);
}

.nav-link:hover,
.nav-link.active {
    color: var(--primary);
}

.nav-link:hover::after,
.nav-link.active::after {
    width: 100%;
}

.nav-actions {
    display: flex;
    align-items: center;
    gap: 12px;
}

.theme-toggle {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    padding: 4px;
    border-radius: 50%;
    transition: transform var(--transition);
}

.theme-toggle:hover {
    transform: rotate(30deg);
}

/* 汉堡菜单（移动端） */
.hamburger {
    display: none;
    flex-direction: column;
    gap: 5px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
}

.hamburger span {
    display: block;
    width: 24px;
    height: 2px;
    background: var(--text-primary);
    border-radius: 2px;
    transition: all var(--transition);
}

.hamburger.active span:nth-child(1) {
    transform: rotate(45deg) translate(5px, 5px);
}

.hamburger.active span:nth-child(2) {
    opacity: 0;
}

.hamburger.active span:nth-child(3) {
    transform: rotate(-45deg) translate(5px, -5px);
}

/* ============================================
   英雄区
   ============================================ */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
    position: relative;
    overflow: hidden;
}

.hero-container {
    display: flex;
    align-items: center;
    gap: 60px;
    width: 100%;
}

.hero-content {
    flex: 1;
}

.hero-greeting {
    font-size: 18px;
    color: var(--primary);
    margin-bottom: 8px;
    font-weight: 500;
}

.hero-name {
    font-size: 52px;
    font-weight: 800;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
    line-height: 1.2;
}

.hero-title {
    font-size: 22px;
    color: var(--text-secondary);
    margin-bottom: 20px;
    min-height: 33px;
}

.typed-cursor {
    animation: blink 0.8s infinite;
    color: var(--primary);
    font-weight: 300;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

.hero-description {
    font-size: 17px;
    color: var(--text-secondary);
    line-height: 1.8;
    margin-bottom: 32px;
    max-width: 480px;
}

.hero-buttons {
    display: flex;
    gap: 16px;
}

.hero-image {
    flex-shrink: 0;
}

.hero-avatar {
    width: 280px;
    height: 280px;
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid var(--primary);
    box-shadow: 0 0 60px rgba(102, 126, 234, 0.3);
    animation: float 3s ease-in-out infinite;
}

.hero-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-15px); }
}

.scroll-down {
    position: absolute;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    width: 30px;
    height: 50px;
    border: 2px solid var(--text-muted);
    border-radius: 15px;
    display: flex;
    justify-content: center;
    padding-top: 8px;
}

.scroll-down span {
    width: 4px;
    height: 8px;
    background: var(--text-muted);
    border-radius: 2px;
    animation: scrollDown 1.5s infinite;
}

@keyframes scrollDown {
    0% { transform: translateY(0); opacity: 1; }
    100% { transform: translateY(12px); opacity: 0; }
}

/* ============================================
   按钮
   ============================================ */
.btn {
    display: inline-block;
    padding: 12px 28px;
    border-radius: var(--radius-sm);
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition);
    border: 2px solid transparent;
    text-align: center;
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-outline {
    border-color: var(--primary);
    color: var(--primary);
    background: transparent;
}

.btn-outline:hover {
    background: var(--primary);
    color: white;
}

.btn-small {
    padding: 6px 16px;
    font-size: 13px;
}

.btn-block {
    width: 100%;
}

/* ============================================
   关于我
   ============================================ */
.about {
    background: var(--bg-secondary);
}

.about-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: start;
}

.about-text p {
    margin-bottom: 16px;
    color: var(--text-secondary);
    font-size: 16px;
}

.skills h3 {
    font-size: 18px;
    margin-bottom: 16px;
    color: var(--text-primary);
}

.skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.skill-tag {
    padding: 6px 16px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    font-size: 14px;
    color: var(--text-secondary);
    transition: all var(--transition);
}

.skill-tag:hover {
    border-color: var(--primary);
    color: var(--primary);
    transform: translateY(-2px);
}

/* ============================================
   项目展示
   ============================================ */
.project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 30px;
}

.project-card {
    background: var(--bg-card);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: transform var(--transition), box-shadow var(--transition);
}

.project-card:hover {
    transform: translateY(-6px);
    box-shadow: var(--shadow-hover);
}

.project-image {
    height: 180px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    display: flex;
    align-items: center;
    justify-content: center;
}

.project-placeholder {
    font-size: 56px;
    opacity: 0.8;
}

.project-info {
    padding: 24px;
}

.project-info h3 {
    font-size: 18px;
    margin-bottom: 10px;
    color: var(--text-primary);
}

.project-info p {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 16px;
    line-height: 1.6;
}

.project-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
}

.project-tags span {
    padding: 3px 10px;
    background: var(--bg-secondary);
    border-radius: 4px;
    font-size: 12px;
    color: var(--text-muted);
}

.project-links {
    display: flex;
    gap: 10px;
}

/* ============================================
   联系表单
   ============================================ */
.contact {
    background: var(--bg-secondary);
}

.contact-form {
    max-width: 600px;
    margin: 0 auto;
    background: var(--bg-card);
    padding: 40px;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 6px;
    font-weight: 600;
    font-size: 14px;
    color: var(--text-primary);
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid var(--border);
    border-radius: var(--radius-sm);
    font-size: 15px;
    font-family: inherit;
    background: var(--bg-primary);
    color: var(--text-primary);
    transition: border-color var(--transition), box-shadow var(--transition);
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
}

.form-group input.error,
.form-group textarea.error {
    border-color: #e74c3c;
}

.error-message {
    display: block;
    color: #e74c3c;
    font-size: 13px;
    margin-top: 4px;
    min-height: 18px;
}

/* ============================================
   页脚
   ============================================ */
.footer {
    background: var(--bg-secondary);
    border-top: 1px solid var(--border);
    padding: 30px 0;
}

.footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.footer-copy {
    color: var(--text-muted);
    font-size: 14px;
}

.footer-social {
    display: flex;
    gap: 16px;
}

.footer-social a {
    color: var(--text-muted);
    transition: color var(--transition), transform var(--transition);
}

.footer-social a:hover {
    color: var(--primary);
    transform: translateY(-2px);
}

/* ============================================
   返回顶部按钮
   ============================================ */
.back-to-top {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: var(--primary);
    color: white;
    border: none;
    font-size: 20px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    opacity: 0;
    visibility: hidden;
    transform: translateY(20px);
    transition: all var(--transition);
    z-index: 999;
}

.back-to-top.visible {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

.back-to-top:hover {
    background: var(--primary-dark);
    transform: translateY(-3px);
}

/* ============================================
   响应式设计
   ============================================ */

/* 平板端（≤ 1024px） */
@media (max-width: 1024px) {
    .hero-container {
        flex-direction: column-reverse;
        text-align: center;
        gap: 40px;
    }

    .hero-description {
        max-width: 100%;
    }

    .hero-buttons {
        justify-content: center;
    }

    .hero-avatar {
        width: 200px;
        height: 200px;
    }

    .about-content {
        grid-template-columns: 1fr;
        gap: 32px;
    }
}

/* 手机端（≤ 768px） */
@media (max-width: 768px) {
    .section {
        padding: 60px 0;
    }

    .section-title {
        font-size: 26px;
    }

    .hero-name {
        font-size: 36px;
    }

    .hero-title {
        font-size: 18px;
    }

    .hamburger {
        display: flex;
    }

    .nav-menu {
        position: fixed;
        top: var(--header-height);
        left: 0;
        width: 100%;
        background: var(--bg-primary);
        flex-direction: column;
        align-items: center;
        gap: 0;
        padding: 20px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        transform: translateY(-120%);
        transition: transform var(--transition);
        z-index: 999;
    }

    .nav-menu.active {
        transform: translateY(0);
    }

    .nav-menu li {
        width: 100%;
        text-align: center;
    }

    .nav-link {
        display: block;
        padding: 14px 0;
        font-size: 16px;
    }

    .project-grid {
        grid-template-columns: 1fr;
    }

    .contact-form {
        padding: 24px;
    }

    .footer-content {
        flex-direction: column;
        gap: 16px;
        text-align: center;
    }

    .back-to-top {
        bottom: 20px;
        right: 20px;
        width: 40px;
        height: 40px;
        font-size: 18px;
    }
}
```

---

## 6.4 JavaScript 交互——让页面活起来

```javascript
// ============================================
// 1. 主题切换（深色/浅色模式）
// ============================================
const themeToggle = document.querySelector('#theme-toggle');
const themeIcon = themeToggle.querySelector('.theme-icon');
const html = document.documentElement;

// 从 localStorage 读取保存的主题
const savedTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', savedTheme);
themeIcon.textContent = savedTheme === 'dark' ? '☀️' : '🌙';

themeToggle.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    themeIcon.textContent = newTheme === 'dark' ? '☀️' : '🌙';
});

// ============================================
// 2. 打字机效果
// ============================================
const typedText = document.querySelector('#typed-text');
const titles = [
    '前端开发工程师',
    'React 爱好者',
    '开源贡献者',
    '终身学习者'
];

let titleIndex = 0;
let charIndex = 0;
let isDeleting = false;
let typeSpeed = 100;

function typeEffect() {
    const currentTitle = titles[titleIndex];

    if (isDeleting) {
        typedText.textContent = currentTitle.substring(0, charIndex - 1);
        charIndex--;
        typeSpeed = 50;
    } else {
        typedText.textContent = currentTitle.substring(0, charIndex + 1);
        charIndex++;
        typeSpeed = 120;
    }

    // 一个词打完，停顿后开始删除
    if (!isDeleting && charIndex === currentTitle.length) {
        typeSpeed = 2000;  // 停顿 2 秒
        isDeleting = true;
    }
    // 删除完毕，切换到下一个词
    else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        titleIndex = (titleIndex + 1) % titles.length;
        typeSpeed = 500;
    }

    setTimeout(typeEffect, typeSpeed);
}

// 启动打字机效果
setTimeout(typeEffect, 1000);

// ============================================
// 3. 移动端汉堡菜单
// ============================================
const hamburger = document.querySelector('#hamburger');
const navMenu = document.querySelector('#nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// 点击导航链接后关闭菜单
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// ============================================
// 4. 导航栏滚动效果
// ============================================
const header = document.querySelector('#header');
const backToTop = document.querySelector('#back-to-top');
const sections = document.querySelectorAll('.section');

// 滚动时：导航栏添加阴影 + 显示/隐藏返回顶部按钮
window.addEventListener('scroll', () => {
    // 导航栏阴影
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }

    // 返回顶部按钮
    if (window.scrollY > 500) {
        backToTop.classList.add('visible');
    } else {
        backToTop.classList.remove('visible');
    }

    // 高亮当前区域的导航链接
    let currentSection = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        if (window.scrollY >= sectionTop) {
            currentSection = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
});

// 返回顶部
backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ============================================
// 5. 表单验证
// ============================================
const contactForm = document.querySelector('#contact-form');

function showError(input, message) {
    const formGroup = input.closest('.form-group');
    const errorElement = formGroup.querySelector('.error-message');
    input.classList.add('error');
    errorElement.textContent = message;
}

function clearError(input) {
    const formGroup = input.closest('.form-group');
    const errorElement = formGroup.querySelector('.error-message');
    input.classList.remove('error');
    errorElement.textContent = '';
}

function validateEmail(email) {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(email);
}

// 实时验证
const nameInput = document.querySelector('#name');
const emailInput = document.querySelector('#email');
const messageInput = document.querySelector('#message');

nameInput.addEventListener('input', () => {
    if (nameInput.value.trim().length > 0) {
        clearError(nameInput);
    }
});

emailInput.addEventListener('input', () => {
    if (validateEmail(emailInput.value)) {
        clearError(emailInput);
    }
});

messageInput.addEventListener('input', () => {
    if (messageInput.value.trim().length > 0) {
        clearError(messageInput);
    }
});

// 表单提交
contactForm.addEventListener('submit', (event) => {
    event.preventDefault();

    let isValid = true;

    // 验证姓名
    if (nameInput.value.trim() === '') {
        showError(nameInput, '请输入你的姓名');
        isValid = false;
    } else {
        clearError(nameInput);
    }

    // 验证邮箱
    if (emailInput.value.trim() === '') {
        showError(emailInput, '请输入你的邮箱');
        isValid = false;
    } else if (!validateEmail(emailInput.value)) {
        showError(emailInput, '请输入有效的邮箱地址');
        isValid = false;
    } else {
        clearError(emailInput);
    }

    // 验证留言
    if (messageInput.value.trim() === '') {
        showError(messageInput, '请输入你的留言内容');
        isValid = false;
    } else {
        clearError(messageInput);
    }

    if (isValid) {
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoading = submitBtn.querySelector('.btn-loading');

        // 模拟发送
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
        submitBtn.disabled = true;

        setTimeout(() => {
            alert('消息已发送！感谢你的联系。（演示模式）');
            contactForm.reset();
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
            submitBtn.disabled = false;
        }, 1500);
    }
});

// ============================================
// 6. 滚动动画（元素进入视口时淡入）
// ============================================
const animateElements = document.querySelectorAll(
    '.project-card, .skill-tag, .about-text'
);

const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    },
    { threshold: 0.1 }
);

animateElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});
```

---

## 6.5 代码解读——理解每一行

### 6.5.1 主题切换原理

```javascript
// 核心思路：修改 <html> 的 data-theme 属性
html.setAttribute('data-theme', 'dark');

// CSS 中通过属性选择器切换变量值
[data-theme="dark"] {
    --bg-primary: #1a1a2e;
    --text-primary: #e4e6eb;
}
```

**代码解读：** 主题切换的本质是 **切换 CSS 变量的值**。我们只需要修改 `<html>` 上的 `data-theme` 属性，所有使用了 CSS 变量的元素都会自动更新颜色。这就是 CSS 变量的强大之处——**一处修改，全局生效**。

### 6.5.2 打字机效果原理

打字机效果的核心是一个 **递归的 `setTimeout`**：

1. **打字阶段**：逐字增加 `textContent`，`charIndex++`
2. **停顿阶段**：打完一个词后等待 2 秒
3. **删除阶段**：逐字减少 `textContent`，`charIndex--`
4. **切换阶段**：删除完毕后切换到下一个词

```javascript
// 状态机：打字 → 停顿 → 删除 → 切换 → 打字...
if (!isDeleting && charIndex === currentTitle.length) {
    isDeleting = true;   // 打完 → 开始删除
} else if (isDeleting && charIndex === 0) {
    isDeleting = false;  // 删完 → 切换下一个词
    titleIndex++;
}
```

### 6.5.3 Intersection Observer——滚动动画

```javascript
const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // 元素进入视口 → 播放动画
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    },
    { threshold: 0.1 }  // 元素 10% 可见时触发
);
```

**代码解读：** `IntersectionObserver` 是浏览器原生 API，用于监测元素是否进入视口。相比传统的 `scroll` 事件监听，它的性能好得多——浏览器会在空闲时批量处理回调。

---

## 6.6 部署到 GitHub Pages

完成代码后，你可以免费部署到 GitHub Pages：

1. 在 GitHub 上创建一个名为 `username.github.io` 的仓库。
2. 将 `index.html`、`css/`、`js/`、`images/` 推送到仓库。
3. 进入仓库 Settings → Pages，选择 `main` 分支，点击 Save。
4. 等待几分钟，访问 `https://username.github.io` 即可看到你的个人主页。

---

### 验证步骤

1. 将 HTML、CSS、JS 代码分别保存为 `index.html`、`css/style.css`、`js/main.js`。
2. 用浏览器打开 `index.html`，观察完整页面的渲染效果。
3. 点击右上角的主题切换按钮（🌙/☀️），观察整个页面配色的变化——理解 CSS 变量切换的原理。
4. 观察英雄区的打字机效果——注意文字逐字出现、停顿、删除、切换的完整循环。
5. 按 F12 → Toggle Device Toolbar，切换手机/平板/桌面视图，观察布局变化。
6. 滚动页面，观察导航栏阴影变化、返回顶部按钮的出现、以及元素淡入动画。
7. 在联系表单中提交空内容，观察验证错误提示；输入有效内容后提交，观察发送状态。

---

## 📋 本章要点总结

- [ ] 掌握完整前端项目的文件结构设计
- [ ] 理解 CSS 变量 + `data-theme` 实现主题切换的原理
- [ ] 会用 `setTimeout` 递归实现打字机效果
- [ ] 掌握移动端汉堡菜单的 HTML + CSS + JS 完整实现
- [ ] 理解 `IntersectionObserver` 实现滚动动画
- [ ] 能实现完整的表单验证（实时验证 + 提交验证）
- [ ] 会用 `localStorage` 持久化用户偏好（主题选择）
- [ ] 理解 `scroll-behavior: smooth` 和 `scroll-padding-top` 的配合
- [ ] 掌握 `window.scrollTo()` 实现平滑滚动
- [ ] 了解 GitHub Pages 的部署流程

---

## 📚 课后练习

### 基础练习

1. 将打字机效果的词库改为你自己的职业描述。
2. 修改配色方案（CSS 变量中的 `--primary` 和 `--secondary`），打造属于你自己的配色。
3. 添加真实的项目截图替换占位符。

### 进阶挑战

4. 添加"博客"板块，使用 JavaScript 动态渲染文章列表。
5. 实现多语言切换（中/英文），将所有文字提取为配置对象。
6. 使用 GitHub API 动态拉取你的真实项目列表并展示。

---

## 🎉 结语

恭喜你完成了全部 6 章的学习！从 HTML5 的文档结构，到 CSS3 的样式布局，再到 JavaScript 的交互逻辑，你已经掌握了前端开发的三大核心技术。

回顾一下你学到的内容：

| 章节 | 核心技能 |
|:---|:---|
| 第 1 章 | HTML5 语义化标签、文档结构、表单基础 |
| 第 2 章 | CSS3 选择器、盒模型、颜色字体、过渡动画 |
| 第 3 章 | Flexbox、Grid、媒体查询、响应式设计 |
| 第 4 章 | JavaScript 变量、函数、数组、对象、条件循环 |
| 第 5 章 | DOM 查询与修改、事件监听、事件委托、表单处理 |
| 第 6 章 | 综合实战：主题切换、打字机效果、滚动动画、完整项目 |

**前端的世界非常广阔**，本教程只是一个起点。接下来你可以：

- 📖 学习一个前端框架（React / Vue / Angular）
- 🎨 深入学习 CSS 动画和 SVG
- ⚡ 学习构建工具（Vite / Webpack）
- 🔧 学习 TypeScript 为代码添加类型安全
- 🚀 学习 Next.js / Nuxt.js 构建全栈应用

**记住：最好的学习方式就是动手做项目。** 现在就去创建你的 GitHub Pages 个人主页吧！

---

[返回教程首页 →](index.md)
