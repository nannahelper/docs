# 第 5 章：DOM 操作与事件处理——用代码操控网页

## 📺 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 理解 DOM 树结构，掌握用 JavaScript 操控网页元素和响应用户事件的方法，能阅读和理解交互逻辑代码 |
| **核心比喻** | **遥控器操作家电** —— DOM 操作就是用代码"遥控"网页上的每一个元素 |
| **预计时长** | 120 分钟 |
| **关键概念** | DOM 树、节点查找、内容修改、样式操作、事件监听、事件冒泡、事件委托 |
| **实践任务** | 阅读并分析一个 Todo 待办事项应用的完整代码，理解 DOM 操作和事件委托的实现 |

---

第 4 章我们学习了 JavaScript 的基础语法，但那些代码都是在控制台里"自言自语"。这一章，我们将让 JavaScript 真正与网页互动——**操控 HTML 元素、响应用户操作**。这就是 DOM 操作和事件处理的威力。

---

## 5.1 什么是 DOM？

### 5.1.1 DOM 的本质

**DOM（Document Object Model，文档对象模型）** 是浏览器将 HTML 文档解析后生成的一个**树状结构对象**。通过 DOM，JavaScript 可以访问和修改页面上的任何元素。

```
HTML 文档                          DOM 树
─────────                         ────────
<html>                            document
  <head>                            └── html
    <title>...                          ├── head
  <body>                                │   └── title
    <h1>...                             └── body
    <p>...                                  ├── h1
    <ul>                                   ├── p
      <li>...                              └── ul
      <li>...                                  ├── li
                                                └── li
```

**代码解读：**

- `document` 是整个 DOM 树的根节点，代表整个网页。
- 每个 HTML 标签都对应 DOM 树中的一个**节点（Node）**。
- 标签之间的嵌套关系变成了 DOM 树中的**父子关系**。
- JavaScript 通过操作这些节点，就能改变网页的内容、结构和样式。

!!! info "DOM 不是 JavaScript 的一部分"

    DOM 是浏览器提供的 **Web API**，不是 JavaScript 语言本身的一部分。理论上，其他编程语言也可以操作 DOM（只要浏览器支持）。但在前端开发中，我们几乎总是用 JavaScript 来操作 DOM。

---

## 5.2 查找 DOM 元素

操作 DOM 的第一步是"找到目标元素"。JavaScript 提供了多种查找方法：

### 5.2.1 通过 ID 查找

```javascript
// 返回单个元素（ID 在页面中应该唯一）
const header = document.getElementById('main-header');
console.log(header.textContent);  // 获取元素的文本内容
```

### 5.2.2 通过 CSS 选择器查找（推荐）

```javascript
// querySelector：返回匹配的第一个元素
const firstParagraph = document.querySelector('p');
const intro = document.querySelector('.intro');
const mainTitle = document.querySelector('#main-title');
const navLink = document.querySelector('nav a');  // 复合选择器

// querySelectorAll：返回所有匹配的元素（NodeList，类数组）
const allParagraphs = document.querySelectorAll('p');
const allCards = document.querySelectorAll('.card');
const allNavLinks = document.querySelectorAll('nav a');

// 遍历 NodeList
allParagraphs.forEach(p => {
    console.log(p.textContent);
});
```

### 5.2.3 通过类名和标签名查找

```javascript
// 通过类名（返回 HTMLCollection，实时更新）
const highlights = document.getElementsByClassName('highlight');

// 通过标签名（返回 HTMLCollection）
const allDivs = document.getElementsByTagName('div');
```

!!! tip "`querySelector` vs `getElementBy*`"

    - `querySelector` / `querySelectorAll`：支持任意 CSS 选择器，返回静态 NodeList（推荐）。
    - `getElementById` / `getElementsByClassName` / `getElementsByTagName`：老式 API，返回实时 HTMLCollection，性能略好但灵活性差。
    - **建议**：日常开发统一使用 `querySelector` 和 `querySelectorAll`。

### 5.2.4 通过节点关系导航

```javascript
const element = document.querySelector('.card');

// 父节点
const parent = element.parentElement;

// 子节点
const children = element.children;           // HTMLCollection（只包含元素节点）
const firstChild = element.firstElementChild;
const lastChild = element.lastElementChild;

// 兄弟节点
const nextSibling = element.nextElementSibling;
const prevSibling = element.previousElementSibling;
```

---

## 5.3 修改 DOM 元素

### 5.3.1 修改内容

```javascript
const element = document.querySelector('.message');

// 修改文本内容（安全，自动转义 HTML）
element.textContent = '新的文本内容';

// 修改 HTML 内容（危险，可能被 XSS 攻击）
element.innerHTML = '<strong>加粗文本</strong>';

// 读取内容
console.log(element.textContent);  // 获取纯文本
console.log(element.innerHTML);    // 获取 HTML 内容
```

!!! danger "安全警示：`innerHTML` 的 XSS 风险"

    如果 `innerHTML` 的内容来自用户输入，攻击者可能注入恶意脚本：
    ```javascript
    // ❌ 危险：用户输入直接插入 innerHTML
    element.innerHTML = userInput;
    
    // ✅ 安全：使用 textContent
    element.textContent = userInput;
    ```
    **原则**：除非你完全信任内容来源，否则使用 `textContent`。

### 5.3.2 修改属性

```javascript
const link = document.querySelector('a');
const image = document.querySelector('img');
const input = document.querySelector('input');

// 修改标准属性
link.href = 'https://www.example.com';
image.src = 'new-photo.jpg';
image.alt = '新图片描述';
input.type = 'email';
input.placeholder = '请输入邮箱';
input.disabled = true;    // 禁用输入框

// 读取属性
console.log(link.href);
console.log(image.getAttribute('src'));

// 修改自定义属性（data-*）
element.setAttribute('data-id', '123');
console.log(element.getAttribute('data-id'));  // 123

// 更简洁的方式（推荐）
console.log(element.dataset.id);  // 123
element.dataset.status = 'active';
```

### 5.3.3 修改样式

```javascript
const box = document.querySelector('.box');

// 修改行内样式（逐个设置）
box.style.backgroundColor = '#4A90D9';
box.style.color = 'white';
box.style.padding = '20px';
box.style.borderRadius = '8px';

// 批量修改：通过 class 切换（推荐）
box.classList.add('active');       // 添加 class
box.classList.remove('hidden');    // 移除 class
box.classList.toggle('dark');      // 切换 class（有则删，无则加）
box.classList.contains('active');  // 检查是否有某个 class
box.classList.replace('old', 'new'); // 替换 class
```

!!! tip "用 class 控制样式，而非直接修改 style"

    直接修改 `element.style.*` 会导致样式散落在 JavaScript 中，难以维护。更好的做法是：
    1. 在 CSS 中定义好各种状态的 class（如 `.active`、`.hidden`、`.disabled`）。
    2. 在 JavaScript 中用 `classList` 切换 class。
    3. 这样样式逻辑留在 CSS 中，JavaScript 只负责状态切换。

### 5.3.4 创建和删除元素

```javascript
// 创建元素
const newParagraph = document.createElement('p');
newParagraph.textContent = '这是动态创建的段落。';
newParagraph.classList.add('dynamic-text');

// 插入元素
const container = document.querySelector('.container');

// 方式一：追加到末尾
container.appendChild(newParagraph);

// 方式二：插入到指定位置
const referenceElement = document.querySelector('.reference');
container.insertBefore(newParagraph, referenceElement);

// 方式三：更灵活的插入（现代 API）
container.append('文本节点', newParagraph);       // 末尾追加（支持多个）
container.prepend(newParagraph);                   // 开头插入
referenceElement.before(newParagraph);             // 插入到参考元素之前
referenceElement.after(newParagraph);              // 插入到参考元素之后

// 删除元素
newParagraph.remove();           // 现代写法（推荐）
// container.removeChild(newParagraph);  // 传统写法

// 克隆元素
const clone = newParagraph.cloneNode(true);  // true = 深克隆（包含子元素）
```

---

## 5.4 事件处理——响应用户操作

### 5.4.1 什么是事件？

**事件（Event）** 是用户在网页上执行的操作——点击按钮、按下键盘、移动鼠标、滚动页面、提交表单……JavaScript 可以"监听"这些事件，并在事件发生时执行相应的代码。

### 5.4.2 添加事件监听器

```javascript
const button = document.querySelector('.btn');

// 推荐方式：addEventListener
button.addEventListener('click', function(event) {
    console.log('按钮被点击了！');
    console.log('事件对象：', event);
});

// 箭头函数写法（更简洁）
button.addEventListener('click', (event) => {
    console.log('点击位置：', event.clientX, event.clientY);
});
```

### 5.4.3 常用事件类型

```javascript
// ========== 鼠标事件 ==========
element.addEventListener('click', handler);        // 单击
element.addEventListener('dblclick', handler);     // 双击
element.addEventListener('mousedown', handler);    // 鼠标按下
element.addEventListener('mouseup', handler);      // 鼠标松开
element.addEventListener('mousemove', handler);    // 鼠标移动
element.addEventListener('mouseenter', handler);   // 鼠标进入（不冒泡）
element.addEventListener('mouseleave', handler);   // 鼠标离开（不冒泡）
element.addEventListener('mouseover', handler);    // 鼠标进入（冒泡）
element.addEventListener('mouseout', handler);     // 鼠标离开（冒泡）

// ========== 键盘事件 ==========
document.addEventListener('keydown', (event) => {
    console.log('按下的键：', event.key);
    console.log('键码：', event.keyCode);

    if (event.key === 'Escape') {
        closeModal();
    }
});
document.addEventListener('keyup', handler);       // 键盘松开

// ========== 表单事件 ==========
input.addEventListener('input', handler);          // 输入内容变化（实时）
input.addEventListener('change', handler);         // 值改变且失去焦点
form.addEventListener('submit', handler);          // 表单提交
input.addEventListener('focus', handler);          // 获得焦点
input.addEventListener('blur', handler);           // 失去焦点

// ========== 文档/窗口事件 ==========
window.addEventListener('load', handler);          // 页面完全加载
document.addEventListener('DOMContentLoaded', handler); // DOM 加载完（更早触发）
window.addEventListener('resize', handler);        // 窗口大小变化
window.addEventListener('scroll', handler);        // 页面滚动
```

### 5.4.4 事件对象

每个事件处理函数都会收到一个**事件对象（Event Object）**，它包含了事件的详细信息：

```javascript
document.addEventListener('click', (event) => {
    console.log('事件类型：', event.type);          // "click"
    console.log('目标元素：', event.target);        // 实际被点击的元素
    console.log('当前监听元素：', event.currentTarget);
    console.log('鼠标坐标：', event.clientX, event.clientY);
    console.log('是否按了 Ctrl：', event.ctrlKey);
    console.log('是否按了 Shift：', event.shiftKey);
});
```

---

## 5.5 事件冒泡与事件委托

### 5.5.1 事件冒泡

当一个元素上的事件被触发时，该事件会**向上冒泡**到父元素：

```html
<div class="outer">
    <div class="inner">
        <button class="btn">点击</button>
    </div>
</div>
```

```javascript
// 点击按钮时，事件会依次触发：
// button → .inner → .outer → document → window

document.querySelector('.btn').addEventListener('click', () => {
    console.log('按钮被点击');
});

document.querySelector('.outer').addEventListener('click', () => {
    console.log('外层 div 也收到了点击事件（冒泡）');
});

// 阻止冒泡
document.querySelector('.btn').addEventListener('click', (event) => {
    event.stopPropagation();  // 事件不再向上冒泡
    console.log('按钮被点击（已阻止冒泡）');
});
```

### 5.5.2 事件委托——性能优化的利器

**事件委托**利用事件冒泡机制，将事件监听器绑定在**父元素**上，而不是每个子元素上：

```html
<ul class="todo-list">
    <li>任务 1 <button class="delete-btn">删除</button></li>
    <li>任务 2 <button class="delete-btn">删除</button></li>
    <li>任务 3 <button class="delete-btn">删除</button></li>
</ul>
```

```javascript
// ❌ 低效：为每个按钮单独绑定事件
document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', handleDelete);
});

// ✅ 高效：事件委托——只在父元素上绑定一个事件
document.querySelector('.todo-list').addEventListener('click', (event) => {
    // 判断点击的是否是删除按钮
    if (event.target.classList.contains('delete-btn')) {
        const listItem = event.target.closest('li');  // 找到最近的 <li>
        listItem.remove();
        console.log('任务已删除');
    }
});
```

**代码解读：**

- `event.target` 是实际被点击的元素（可能是按钮）。
- `event.target.closest('li')` 向上查找最近的 `<li>` 祖先元素。
- 事件委托的三大好处：
  1. **性能更好**：只需绑定一个事件，而非 N 个。
  2. **动态元素支持**：后续通过 JavaScript 添加的新元素自动拥有事件响应。
  3. **代码更简洁**：不需要在创建元素时手动绑定事件。

---

## 5.6 表单处理

### 5.6.1 获取表单数据

```html
<form id="login-form">
    <input type="text" name="username" placeholder="用户名">
    <input type="password" name="password" placeholder="密码">
    <button type="submit">登录</button>
</form>
```

```javascript
const form = document.querySelector('#login-form');

form.addEventListener('submit', (event) => {
    event.preventDefault();  // 阻止表单默认提交（页面刷新）

    // 方式一：通过 name 属性获取
    const formData = new FormData(form);
    const username = formData.get('username');
    const password = formData.get('password');

    console.log('用户名：', username);
    console.log('密码：', password);

    // 方式二：直接通过元素获取
    const usernameInput = form.querySelector('[name="username"]');
    console.log(usernameInput.value);
});
```

### 5.6.2 实时表单验证

```javascript
const emailInput = document.querySelector('#email');
const errorMessage = document.querySelector('.error-message');

emailInput.addEventListener('input', () => {
    const email = emailInput.value;
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email)) {
        emailInput.style.borderColor = '#e74c3c';
        errorMessage.textContent = '请输入有效的邮箱地址';
        errorMessage.style.display = 'block';
    } else {
        emailInput.style.borderColor = '#27ae60';
        errorMessage.style.display = 'none';
    }
});
```

---

## 5.7 实践任务：阅读并分析 Todo 应用

### 任务要求

下面是一个完整的 Todo 待办事项应用代码。你的任务是**逐段阅读 JavaScript 部分，理解 DOM 操作和事件委托的实现**，回答以下问题：

- `addTodo()` 函数中，`createElement('li')` 和 `appendChild(li)` 分别做了什么？
- 为什么使用事件委托（在 `todoList` 上监听）而不是给每个按钮单独绑定事件？
- `event.target.closest('.todo-item')` 这行代码的作用是什么？
- `classList.toggle('completed')` 是如何实现完成/撤销切换的？
- `escapeHtml()` 函数的作用是什么？为什么需要它？
- 删除操作中，为什么先设置 `opacity` 和 `transform`，然后用 `setTimeout` 延迟 300ms 再 `remove()`？

### 参考代码

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo 待办事项</title>
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea, #764ba2);
            font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
        }

        .todo-app {
            background: white;
            border-radius: 16px;
            padding: 30px;
            width: 420px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }

        .todo-app h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 24px;
        }

        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .input-group input {
            flex: 1;
            padding: 12px 15px;
            border: 2px solid #ecf0f1;
            border-radius: 8px;
            font-size: 15px;
            transition: border-color 0.3s ease;
        }

        .input-group input:focus {
            outline: none;
            border-color: #667eea;
        }

        .input-group button {
            padding: 12px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        .input-group button:hover {
            background: #5a6fd6;
        }

        .stats {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            margin-bottom: 15px;
            border-bottom: 1px solid #ecf0f1;
            color: #7f8c8d;
            font-size: 14px;
        }

        .todo-list {
            list-style: none;
        }

        .todo-item {
            display: flex;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #f5f6fa;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .todo-item.completed .todo-text {
            text-decoration: line-through;
            color: #bdc3c7;
        }

        .todo-text {
            flex: 1;
            font-size: 15px;
            color: #2c3e50;
        }

        .todo-item button {
            padding: 6px 12px;
            border: none;
            border-radius: 4px;
            font-size: 13px;
            cursor: pointer;
            margin-left: 8px;
            transition: all 0.3s ease;
        }

        .btn-complete {
            background: #27ae60;
            color: white;
        }

        .btn-complete:hover {
            background: #219a52;
        }

        .btn-delete {
            background: #e74c3c;
            color: white;
        }

        .btn-delete:hover {
            background: #c0392b;
        }

        .empty-message {
            text-align: center;
            color: #bdc3c7;
            padding: 30px 0;
            font-size: 15px;
        }
    </style>
</head>
<body>
    <div class="todo-app">
        <h1>📝 待办事项</h1>

        <div class="input-group">
            <input type="text" id="todo-input" placeholder="添加新的待办事项..." autocomplete="off">
            <button id="add-btn">添加</button>
        </div>

        <div class="stats">
            <span id="pending-count">待完成：0</span>
            <span id="total-count">总计：0</span>
        </div>

        <ul class="todo-list" id="todo-list">
            <li class="empty-message">还没有待办事项，添加一个吧！</li>
        </ul>
    </div>

    <script>
        // ========== DOM 元素引用 ==========
        const todoInput = document.querySelector('#todo-input');
        const addBtn = document.querySelector('#add-btn');
        const todoList = document.querySelector('#todo-list');
        const pendingCount = document.querySelector('#pending-count');
        const totalCount = document.querySelector('#total-count');
        const emptyMessage = document.querySelector('.empty-message');

        // ========== 添加待办事项 ==========
        function addTodo() {
            const text = todoInput.value.trim();

            if (text === '') {
                todoInput.focus();
                return;
            }

            // 隐藏空状态提示
            if (emptyMessage) {
                emptyMessage.style.display = 'none';
            }

            // 创建列表项
            const li = document.createElement('li');
            li.className = 'todo-item';
            li.innerHTML = `
                <span class="todo-text">${escapeHtml(text)}</span>
                <button class="btn-complete">完成</button>
                <button class="btn-delete">删除</button>
            `;

            todoList.appendChild(li);
            todoInput.value = '';
            todoInput.focus();

            updateStats();
        }

        // ========== 事件委托：处理完成和删除 ==========
        todoList.addEventListener('click', (event) => {
            const target = event.target;
            const todoItem = target.closest('.todo-item');

            if (!todoItem) return;

            // 完成按钮
            if (target.classList.contains('btn-complete')) {
                todoItem.classList.toggle('completed');
                const btn = todoItem.querySelector('.btn-complete');
                btn.textContent = todoItem.classList.contains('completed') ? '撤销' : '完成';
                updateStats();
            }

            // 删除按钮
            if (target.classList.contains('btn-delete')) {
                todoItem.style.opacity = '0';
                todoItem.style.transform = 'translateX(30px)';
                todoItem.style.transition = 'all 0.3s ease';

                setTimeout(() => {
                    todoItem.remove();
                    updateStats();

                    // 如果列表为空，显示空状态
                    if (todoList.children.length === 0) {
                        const empty = document.createElement('li');
                        empty.className = 'empty-message';
                        empty.textContent = '还没有待办事项，添加一个吧！';
                        todoList.appendChild(empty);
                    }
                }, 300);
            }
        });

        // ========== 更新统计 ==========
        function updateStats() {
            const total = todoList.querySelectorAll('.todo-item').length;
            const completed = todoList.querySelectorAll('.todo-item.completed').length;
            const pending = total - completed;

            pendingCount.textContent = `待完成：${pending}`;
            totalCount.textContent = `总计：${total}`;
        }

        // ========== 防止 XSS：转义 HTML 特殊字符 ==========
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // ========== 事件绑定 ==========
        addBtn.addEventListener('click', addTodo);

        todoInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                addTodo();
            }
        });
    </script>
</body>
</html>
```

### 验证步骤

1. 将代码保存为 `todo.html`，用浏览器打开。
2. 输入文字点击"添加"（或按 Enter），验证待办事项是否出现在列表中——观察 `createElement` 和 `appendChild` 的效果。
3. 点击"完成"按钮，验证文字是否添加删除线，按钮是否变为"撤销"——理解 `classList.toggle` 的切换逻辑。
4. 再次点击"撤销"，验证是否恢复未完成状态。
5. 点击"删除"按钮，观察删除动画（淡出 + 右移），理解 `setTimeout` + `remove()` 的延迟删除设计。
6. 观察顶部的统计数据是否实时更新——理解 `updateStats()` 的调用时机。
7. 删除所有事项，验证是否显示空状态提示。

---

## 📋 本章要点总结

- [ ] 理解 DOM 是浏览器将 HTML 解析后生成的树状结构对象
- [ ] 熟练使用 `querySelector` 和 `querySelectorAll` 查找元素
- [ ] 掌握修改元素内容：`textContent`（安全）vs `innerHTML`（注意 XSS）
- [ ] 能修改元素属性（`href`、`src`、`disabled` 等）和 `data-*` 属性
- [ ] 会用 `classList`（`add`、`remove`、`toggle`、`contains`）管理样式
- [ ] 掌握创建元素（`createElement`）、插入元素（`appendChild`、`append`）、删除元素（`remove`）
- [ ] 理解事件驱动模型，会用 `addEventListener` 绑定事件
- [ ] 熟悉常用事件类型：click、keydown、input、submit、DOMContentLoaded
- [ ] 理解事件冒泡机制，掌握事件委托（`event.target`）
- [ ] 会用 `event.preventDefault()` 阻止默认行为
- [ ] 掌握表单数据获取（`FormData`）和实时验证

---

## 📚 课后练习

### 基础练习

1. 创建一个"点击计数器"：页面上有一个按钮和一个数字，每次点击按钮数字 +1。
2. 创建一个"实时字符统计"：一个文本框，下方实时显示已输入字符数。

### 进阶挑战

3. 为 Todo 应用添加"编辑"功能：双击待办事项文字可以进入编辑模式。
4. 为 Todo 应用添加 `localStorage` 持久化：刷新页面后待办事项不丢失。

---

👉 [进入第 6 章：综合实战——打造个人主页 →](06-final-project.md)
