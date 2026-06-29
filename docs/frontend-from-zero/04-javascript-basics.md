# 第 4 章：JavaScript 基础语法——让网页"活"起来

## 📺 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 掌握 JavaScript 核心语法，理解变量、函数、数组和对象，能阅读和理解网页中的 JS 代码逻辑 |
| **核心比喻** | **家电控制系统（智能开关）** —— JavaScript 让网页"活"起来，响应用户操作 |
| **预计时长** | 120 分钟 |
| **关键概念** | 变量声明、数据类型、运算符、条件判断、循环、函数、数组方法、对象 |
| **实践任务** | 阅读并分析一个计算器的 JavaScript 代码，理解每行代码的执行逻辑 |

---

HTML 定义了网页的 **结构**，CSS 定义了网页的 **外观**，而 JavaScript 定义了网页的 **行为**。如果把网页比作一栋智能房子：HTML 是钢筋水泥，CSS 是室内装修，JavaScript 就是 **智能家居系统**——它让灯光自动开关、空调自动调温、门锁自动识别。没有 JavaScript，网页就只是一张静态的"图片"。

---

## 4.1 JavaScript 是什么？—— 认识网页的"大脑"

### 4.1.1 JavaScript 的定位

JavaScript（简称 JS）是一门 **真正的编程语言**。与 HTML 和 CSS 不同，JS 拥有完整的编程能力：

- **变量**：存储和操作数据
- **逻辑判断**：根据条件执行不同代码（if-else）
- **循环**：重复执行某段代码（for/while）
- **函数**：封装可复用的代码块
- **对象**：组织复杂的数据结构

!!! info "Java 和 JavaScript 的关系"

    很多人以为 JavaScript 是 Java 的"简化版"，这是一个经典的误解。Java 和 JavaScript 的关系就像"雷锋"和"雷峰塔"——**名字相似，但完全是两门不同的语言**。JavaScript 最初叫 LiveScript，后来为了蹭 Java 的热度才改名。

### 4.1.2 JavaScript 的三种引入方式

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>JavaScript 引入方式</title>

    <!-- 方式一：外部脚本文件（推荐） -->
    <script src="script.js" defer></script>

    <!-- 方式二：内部脚本 -->
    <script>
        console.log('Hello from internal script!');
    </script>
</head>
<body>
    <!-- 方式三：行内事件处理（不推荐） -->
    <button onclick="alert('Hello!')">点击我</button>
</body>
</html>
```

**代码解读：**

| 方式 | 写法 | 推荐度 | 说明 |
|:---|:---|:---:|:---|
| **外部文件** | `<script src="script.js" defer>` | ⭐⭐⭐⭐⭐ | 结构与行为分离，可缓存，`defer` 确保 DOM 加载完再执行 |
| **内部脚本** | `<script>...</script>` | ⭐⭐⭐ | 适合小型演示，但不利于维护 |
| **行内事件** | `onclick="..."` | ⭐ | 与 HTML 耦合，难以维护，不符合关注点分离原则 |

!!! tip "`defer` vs `async`"

    - `defer`：脚本在后台下载，**等 HTML 解析完成后** 按顺序执行（推荐）。
    - `async`：脚本在后台下载，**下载完立即执行**，不保证执行顺序。
    - 不加属性：脚本下载和执行都会 **阻塞 HTML 解析**（不推荐）。

---

## 4.2 变量与数据类型

### 4.2.1 声明变量

```javascript
// 现代写法（ES6+）：使用 let 和 const
let name = '张三';        // 可变变量
const PI = 3.14159;       // 常量，不可重新赋值
let age = 25;
age = 26;                 // ✅ let 可以修改
// PI = 3.14;             // ❌ const 不能修改，会报错

// 过时写法：var（有作用域问题，不推荐）
var oldWay = '不推荐使用';
```

**代码解读：**

| 关键字 | 可修改 | 作用域 | 推荐度 |
|:---|:---:|:---|:---:|
| `const` | ❌ | 块级 | ⭐⭐⭐⭐⭐ 默认首选 |
| `let` | ✅ | 块级 | ⭐⭐⭐⭐ 需要修改时使用 |
| `var` | ✅ | 函数级 | ⭐ 遗留代码中常见，新代码避免 |

!!! tip "默认使用 `const`，需要修改时改用 `let`"

    这是一个最佳实践：声明变量时优先使用 `const`，当你确定这个变量需要被重新赋值时，再改为 `let`。这样做可以减少意外的变量修改。

### 4.2.2 基本数据类型

JavaScript 有 7 种基本数据类型：

```javascript
// 1. 字符串（String）
const name = '张三';
const greeting = "你好，世界！";
const template = `欢迎你，${name}！`;  // 模板字符串（ES6），支持变量插值

// 2. 数字（Number）—— 不区分整数和浮点数
const age = 25;
const price = 19.99;
const infinity = Infinity;
const notANumber = NaN;  // Not a Number，如 0/0 的结果

// 3. 布尔值（Boolean）
const isLoggedIn = true;
const isExpired = false;

// 4. 未定义（Undefined）—— 变量已声明但未赋值
let something;
console.log(something);  // undefined

// 5. 空值（Null）—— 表示"空"或"不存在"
const empty = null;

// 6. 符号（Symbol，ES6）—— 创建唯一标识
const uniqueId = Symbol('id');

// 7. 大整数（BigInt，ES2020）—— 表示超大整数
const hugeNumber = 9007199254740991n;
```

### 4.2.3 类型检测

```javascript
console.log(typeof 'hello');     // "string"
console.log(typeof 42);          // "number"
console.log(typeof true);        // "boolean"
console.log(typeof undefined);   // "undefined"
console.log(typeof null);        // "object"（这是一个历史遗留 bug）
console.log(typeof Symbol());    // "symbol"
console.log(typeof function(){});// "function"
```

---

## 4.3 运算符

### 4.3.1 算术运算符

```javascript
const a = 10;
const b = 3;

console.log(a + b);   // 13  加法
console.log(a - b);   // 7   减法
console.log(a * b);   // 30  乘法
console.log(a / b);   // 3.333...  除法
console.log(a % b);   // 1   取余（模运算）
console.log(a ** b);  // 1000  指数（ES7）
```

### 4.3.2 比较运算符

```javascript
console.log(5 > 3);          // true
console.log(5 >= 5);         // true
console.log(5 < 3);          // false
console.log(5 === 5);        // true  严格相等（比较值和类型）
console.log(5 === '5');      // false 类型不同
console.log(5 == '5');       // true  宽松相等（会做类型转换，不推荐）
console.log(5 !== '5');      // true  严格不等
```

!!! warning "始终使用 `===` 而非 `==`"

    `==` 会进行隐式类型转换，导致意想不到的结果：
    ```javascript
    console.log(0 == '');       // true（诡异！）
    console.log(0 == false);    // true（诡异！）
    console.log(null == undefined); // true
    ```
    使用 `===`（严格相等）可以避免这些陷阱。

### 4.3.3 逻辑运算符

```javascript
// 与（AND）：两边都为 true 才返回 true
console.log(true && true);    // true
console.log(true && false);   // false

// 或（OR）：任意一边为 true 就返回 true
console.log(true || false);   // true
console.log(false || false);  // false

// 非（NOT）：取反
console.log(!true);           // false
console.log(!false);          // true

// 短路求值（常用技巧）
const displayName = userName || '匿名用户';  // 如果 userName 为空，使用默认值
const result = isLoggedIn && getUserData();  // 只有登录了才调用函数

// 空值合并运算符（ES2020）
const name = inputName ?? '默认名称';  // 只有 null/undefined 时才用默认值
```

---

## 4.4 条件判断——让代码做选择

### 4.4.1 if-else 语句

```javascript
const score = 85;

if (score >= 90) {
    console.log('优秀');
} else if (score >= 80) {
    console.log('良好');
} else if (score >= 60) {
    console.log('及格');
} else {
    console.log('不及格');
}
// 输出：良好
```

### 4.4.2 switch 语句

```javascript
const day = '星期一';

switch (day) {
    case '星期一':
        console.log('新的一周开始了！');
        break;
    case '星期五':
        console.log('马上周末了！');
        break;
    case '星期六':
    case '星期日':
        console.log('周末愉快！');
        break;
    default:
        console.log('工作日继续加油！');
}
```

### 4.4.3 三元运算符

```javascript
const age = 20;
const canVote = age >= 18 ? '可以投票' : '不能投票';
console.log(canVote);  // 可以投票

// 等价于：
// if (age >= 18) {
//     canVote = '可以投票';
// } else {
//     canVote = '不能投票';
// }
```

---

## 4.5 循环——让代码重复执行

### 4.5.1 for 循环

```javascript
// 经典 for 循环
for (let i = 0; i < 5; i++) {
    console.log(`第 ${i + 1} 次循环`);
}

// 遍历数组
const fruits = ['苹果', '香蕉', '橘子', '葡萄'];
for (let i = 0; i < fruits.length; i++) {
    console.log(fruits[i]);
}
```

### 4.5.2 for...of 循环（推荐遍历数组）

```javascript
const colors = ['红色', '绿色', '蓝色'];

for (const color of colors) {
    console.log(color);
}
// 输出：红色 绿色 蓝色
```

### 4.5.3 while 循环

```javascript
let count = 0;

while (count < 3) {
    console.log(`计数：${count}`);
    count++;
}
// 输出：计数：0  计数：1  计数：2
```

### 4.5.4 循环控制

```javascript
// break：立即退出循环
for (let i = 0; i < 10; i++) {
    if (i === 5) break;
    console.log(i);  // 输出 0 1 2 3 4
}

// continue：跳过当前迭代，继续下一次
for (let i = 0; i < 5; i++) {
    if (i === 2) continue;
    console.log(i);  // 输出 0 1 3 4
}
```

---

## 4.6 函数——封装可复用的代码

### 4.6.1 函数声明

```javascript
// 函数声明
function greet(name) {
    return `你好，${name}！`;
}

console.log(greet('张三'));  // 你好，张三！

// 函数表达式
const add = function(a, b) {
    return a + b;
};

console.log(add(3, 5));  // 8
```

### 4.6.2 箭头函数（ES6，推荐）

```javascript
// 完整写法
const multiply = (a, b) => {
    return a * b;
};

// 简写：只有一条 return 语句时，可省略 {} 和 return
const multiplyShort = (a, b) => a * b;

// 只有一个参数时，可省略 ()
const square = x => x * x;

// 没有参数时，必须保留 ()
const sayHello = () => console.log('Hello!');
```

### 4.6.3 参数默认值

```javascript
function createUser(name, role = '普通用户') {
    return { name, role };
}

console.log(createUser('张三'));           // { name: '张三', role: '普通用户' }
console.log(createUser('李四', '管理员'));  // { name: '李四', role: '管理员' }
```

---

## 4.7 数组——有序的数据集合

### 4.7.1 创建和访问数组

```javascript
// 创建数组
const fruits = ['苹果', '香蕉', '橘子'];
const numbers = [1, 2, 3, 4, 5];
const mixed = ['文字', 42, true, null];  // 数组可以包含不同类型

// 访问元素（索引从 0 开始）
console.log(fruits[0]);     // 苹果
console.log(fruits[1]);     // 香蕉
console.log(fruits.length); // 3

// 修改元素
fruits[1] = '葡萄';
console.log(fruits);  // ['苹果', '葡萄', '橘子']
```

### 4.7.2 常用数组方法

```javascript
const arr = [1, 2, 3, 4, 5];

// 末尾添加/删除
arr.push(6);        // [1, 2, 3, 4, 5, 6]
arr.pop();          // [1, 2, 3, 4, 5]  返回被删除的 6

// 开头添加/删除
arr.unshift(0);     // [0, 1, 2, 3, 4, 5]
arr.shift();        // [1, 2, 3, 4, 5]  返回被删除的 0

// 查找元素
console.log(arr.indexOf(3));     // 2（索引位置）
console.log(arr.includes(3));    // true（是否存在）

// 截取子数组（不修改原数组）
const sub = arr.slice(1, 3);     // [2, 3]

// 删除/插入元素（修改原数组）
arr.splice(2, 1);                // 从索引 2 开始删除 1 个元素 → [1, 2, 4, 5]
arr.splice(2, 0, 99);            // 在索引 2 处插入 99 → [1, 2, 99, 4, 5]
```

### 4.7.3 数组遍历方法（函数式编程）

```javascript
const numbers = [1, 2, 3, 4, 5];

// forEach：遍历每个元素
numbers.forEach((num, index) => {
    console.log(`索引 ${index}：${num}`);
});

// map：将每个元素映射为新值，返回新数组
const doubled = numbers.map(num => num * 2);
console.log(doubled);  // [2, 4, 6, 8, 10]

// filter：筛选符合条件的元素，返回新数组
const evens = numbers.filter(num => num % 2 === 0);
console.log(evens);  // [2, 4]

// find：查找第一个符合条件的元素
const found = numbers.find(num => num > 3);
console.log(found);  // 4

// reduce：将数组归约为单个值
const sum = numbers.reduce((total, num) => total + num, 0);
console.log(sum);  // 15
```

---

## 4.8 对象——无序的键值对集合

### 4.8.1 创建和访问对象

```javascript
// 创建对象
const user = {
    name: '张三',
    age: 25,
    email: 'zhangsan@example.com',
    isAdmin: false,
    hobbies: ['编程', '阅读', '跑步'],
    address: {
        city: '北京',
        district: '海淀区'
    }
};

// 访问属性
console.log(user.name);           // 张三（点号访问）
console.log(user['email']);       // zhangsan@example.com（方括号访问）
console.log(user.hobbies[0]);     // 编程
console.log(user.address.city);   // 北京（链式访问）

// 修改和添加属性
user.age = 26;
user.phone = '13800138000';       // 添加新属性

// 删除属性
delete user.isAdmin;
```

### 4.8.2 对象方法简写（ES6）

```javascript
const calculator = {
    // 方法简写
    add(a, b) {
        return a + b;
    },

    subtract(a, b) {
        return a - b;
    },

    // 属性值简写
    display(result) {
        console.log(`计算结果：${result}`);
    }
};

console.log(calculator.add(10, 5));  // 15
```

### 4.8.3 解构赋值（ES6）

```javascript
const user = { name: '张三', age: 25, email: 'zhangsan@example.com' };

// 对象解构
const { name, age, email } = user;
console.log(name, age);  // 张三 25

// 重命名
const { name: userName, age: userAge } = user;
console.log(userName);  // 张三

// 默认值
const { role = '普通用户' } = user;
console.log(role);  // 普通用户

// 数组解构
const colors = ['红色', '绿色', '蓝色'];
const [first, second, third] = colors;
console.log(first, second);  // 红色 绿色
```

---

## 4.9 实践任务：阅读并分析计算器代码

### 任务要求

下面是一个完整的网页计算器代码（HTML + CSS + JS）。你的任务是 **逐行阅读 JavaScript 部分，理解每行代码的执行逻辑**，回答以下问题：

- `parseFloat()` 函数的作用是什么？为什么不用 `parseInt()`？
- `isNaN()` 检查的是什么情况？如果用户不输入任何内容就点击按钮会发生什么？
- `switch` 语句中每个 `case` 分支做了什么？`break` 的作用是什么？
- 除法运算中，为什么需要单独检查 `num2 === 0`？
- `resultElement.textContent` 和 `resultElement.style.color` 分别修改了什么？

### 参考代码

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>简易计算器</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #f0f2f5;
            font-family: "Microsoft YaHei", sans-serif;
        }
        .calculator {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            width: 320px;
        }
        .calculator h2 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 20px;
        }
        .calculator input {
            width: 100%;
            padding: 10px;
            margin-bottom: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            box-sizing: border-box;
        }
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-bottom: 15px;
        }
        .buttons button {
            padding: 12px;
            border: none;
            border-radius: 6px;
            font-size: 18px;
            cursor: pointer;
            background: #4A90D9;
            color: white;
            transition: background 0.3s ease;
        }
        .buttons button:hover {
            background: #357ABD;
        }
        .result {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 6px;
            min-height: 30px;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <h2>简易计算器</h2>
        <input type="number" id="num1" placeholder="请输入第一个数字">
        <input type="number" id="num2" placeholder="请输入第二个数字">
        <div class="buttons">
            <button onclick="calculate('+')">+</button>
            <button onclick="calculate('-')">-</button>
            <button onclick="calculate('*')">×</button>
            <button onclick="calculate('/')">÷</button>
        </div>
        <div class="result" id="result">结果将显示在这里</div>
    </div>

    <script>
        function calculate(operator) {
            const num1 = parseFloat(document.getElementById('num1').value);
            const num2 = parseFloat(document.getElementById('num2').value);
            const resultElement = document.getElementById('result');

            if (isNaN(num1) || isNaN(num2)) {
                resultElement.textContent = '请输入有效的数字！';
                resultElement.style.color = '#e74c3c';
                return;
            }

            let result;
            switch (operator) {
                case '+':
                    result = num1 + num2;
                    break;
                case '-':
                    result = num1 - num2;
                    break;
                case '*':
                    result = num1 * num2;
                    break;
                case '/':
                    if (num2 === 0) {
                        resultElement.textContent = '错误：除数不能为 0！';
                        resultElement.style.color = '#e74c3c';
                        return;
                    }
                    result = num1 / num2;
                    break;
            }

            resultElement.textContent = `${num1} ${operator} ${num2} = ${result}`;
            resultElement.style.color = '#2c3e50';
        }
    </script>
</body>
</html>
```

### 验证步骤

1. 将代码保存为 `calculator.html`，用浏览器打开。
2. 输入两个数字，分别点击加减乘除按钮，验证结果是否正确——同时观察 `resultElement.textContent` 的变化。
3. 输入 0 作为第二个数字，点击除法，验证是否显示红色错误提示——注意 `resultElement.style.color` 的变化。
4. 不输入数字直接点击按钮，验证是否提示"请输入有效的数字"——理解 `isNaN()` 的检查逻辑。
5. 按 F12 打开 Console，手动输入 `calculate('+')` 测试函数调用。

---

## 📋 本章要点总结

- [ ] 理解 JavaScript 是真正的编程语言，负责网页的交互行为
- [ ] 掌握 `const` 和 `let` 声明变量，避免使用 `var`
- [ ] 熟悉 7 种基本数据类型：string、number、boolean、undefined、null、symbol、bigint
- [ ] 理解 `===`（严格相等）和 `==`（宽松相等）的区别，始终使用 `===`
- [ ] 掌握 if-else 条件判断和三元运算符
- [ ] 熟练使用 for 循环和 for...of 循环遍历数组
- [ ] 能声明和调用函数，理解参数和返回值
- [ ] 会使用箭头函数 `() => {}` 简化代码
- [ ] 掌握数组的常用方法：push、pop、map、filter、find、reduce
- [ ] 理解对象的概念，能创建和访问对象属性
- [ ] 会使用解构赋值简化代码

---

## 📚 课后练习

### 基础练习

1. 编写一个函数 `isEven(n)`，判断一个数字是否为偶数，返回布尔值。
2. 编写一个函数 `getMax(arr)`，接收一个数字数组，返回其中的最大值。
3. 创建一个对象 `book`，包含属性：title、author、year、pages，并编写一个方法 `getSummary()` 返回书籍简介。

### 进阶挑战

4. 编写一个函数 `fizzBuzz(n)`：遍历 1 到 n，能被 3 整除输出 "Fizz"，能被 5 整除输出 "Buzz"，能同时被 3 和 5 整除输出 "FizzBuzz"，否则输出数字本身。
5. 扩展计算器：添加"清空"按钮、支持小数运算、美化结果显示。

---

👉 [进入第 5 章：DOM 操作与事件处理 →](05-dom-events.md)
