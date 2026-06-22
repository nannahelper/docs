# 第 4 章：Dog-Frontier 前端设计实战

> **让 AI 帮你设计前端** —— 用 Dog-Frontier 生成高质量的前端设计方案与代码。

---

## 4.1 Dog-Frontier 简介

Dog-Frontier 是 Dog-Skills 中的前端设计综合技能系统。它整合了 18 个专业前端技能的精华，通过多轮对话精确理解需求，输出高质量、高结构化的前端设计方案与代码。

### 覆盖范围

| 覆盖领域 | 具体内容 |
|:---|:---|
| **UI/UX 设计系统** | 设计令牌、配色方案、字体搭配、品牌设计 |
| **组件库** | Tailwind CSS、shadcn/ui 组件 |
| **技术栈** | Vue、React 组件开发 |
| **页面类型** | 落地页、Dashboard 仪表盘、响应式布局 |
| **高级技巧** | CSS 动画、HTML 视频、设计令牌三大层级 |

---

## 4.2 实战：设计一个博客落地页

### 第一步：触发技能

在 AI 助手中输入触发词：

```
请帮我设计一个技术博客的落地页，风格简洁现代，支持暗色模式。
```

### 第二步：需求理解

Dog-Frontier 会通过多轮对话精确理解你的需求：

- 目标用户是谁？
- 需要的核心功能是什么？
- 配色偏好？
- 响应式要求？

```
# 示例回复
"目标用户是开发者，需要展示最新文章、分类标签、搜索功能。
配色偏好蓝色系，类似 GitHub 风格。需要适配手机和桌面。"
```

### 第三步：设计方案输出

AI 会输出结构化的设计方案：

1. **设计令牌（Design Tokens）**
   - 色彩系统（主色、辅助色、中性色）
   - 字体系统（标题、正文、代码）
   - 间距系统（xs/sm/md/lg/xl）

2. **布局设计**
   - 页面结构（Header、Hero、Features、Footer）
   - 组件树（导航栏、文章卡片、搜索框）

3. **代码实现**
   - HTML 结构
   - CSS/Tailwind 样式
   - 交互逻辑（JavaScript）

---

## 4.3 设计令牌系统

Dog-Frontier 使用三层设计令牌体系：

### 第一层：基础令牌（Primitive Tokens）

最底层的原始值，定义基础颜色、字体、间距：

```css
:root {
  /* 基础颜色 */
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  
  /* 基础间距 */
  --space-4: 1rem;
  --space-8: 2rem;
}
```

### 第二层：语义令牌（Semantic Tokens）

赋予基础令牌语义含义：

```css
:root {
  /* 语义颜色 */
  --color-primary: var(--color-blue-500);
  --color-primary-hover: var(--color-blue-600);
  
  /* 语义间距 */
  --section-padding: var(--space-8);
  --card-padding: var(--space-4);
}
```

### 第三层：组件令牌（Component Tokens）

针对具体组件的令牌：

```css
:root {
  /* 按钮组件 */
  --btn-primary-bg: var(--color-primary);
  --btn-primary-text: #ffffff;
  
  /* 卡片组件 */
  --card-bg: #ffffff;
  --card-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

---

## 4.4 常用组件模式

### 落地页布局

```
┌─────────────────────────────────────┐
│              Header / Nav            │
├─────────────────────────────────────┤
│              Hero Section            │
│     (标题 + 副标题 + CTA 按钮)        │
├─────────────────────────────────────┤
│           Features Section           │
│   (3 列网格: 功能1, 功能2, 功能3)     │
├─────────────────────────────────────┤
│           Content Section            │
│     (文章列表 / 卡片网格)             │
├─────────────────────────────────────┤
│              Footer                  │
└─────────────────────────────────────┘
```

### Dashboard 布局

```
┌──────────┬──────────────────────────┐
│          │      Stats Cards          │
│          ├──────────────────────────┤
│ Sidebar  │      Chart Area           │
│          ├──────────────────────────┤
│          │      Data Table           │
└──────────┴──────────────────────────┘
```

---

## 4.5 响应式设计

Dog-Frontier 生成的代码默认支持响应式设计，采用 Mobile First 策略：

| 断点 | 宽度 | 布局变化 |
|:---|:---|:---|
| **sm** | ≥ 640px | 小屏手机横屏 |
| **md** | ≥ 768px | 平板竖屏 |
| **lg** | ≥ 1024px | 平板横屏 / 小桌面 |
| **xl** | ≥ 1280px | 标准桌面 |

```html
<!-- Tailwind 响应式示例 -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="card">卡片 1</div>
  <div class="card">卡片 2</div>
  <div class="card">卡片 3</div>
</div>
```

---

## 4.6 暗色模式支持

Dog-Frontier 支持 Tailwind 的暗色模式：

```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
  <h1 class="text-2xl font-bold">标题</h1>
  <p class="text-gray-600 dark:text-gray-400">描述文字</p>
</div>
```

---

## 4.7 本章小结

- Dog-Frontier 整合 18 个前端技能，覆盖前端设计全链路
- 通过多轮对话精确理解需求，输出结构化设计方案
- 内置设计令牌三层体系，确保设计一致性
- 默认支持响应式设计和暗色模式

---

## 实践任务

1. 用 Dog-Frontier 设计一个个人作品集页面
2. 尝试修改配色方案和字体
3. 在不同屏幕尺寸下测试响应式效果

---