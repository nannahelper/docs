# 第 2 章：打造项目主页

> **场景：** 你在 GitHub 上创建了一个开源项目，现在需要写一份专业的 README 来吸引贡献者和用户。一个好的 README 需要清晰的目录结构、代码示例、截图展示和导航链接。

---

## 2.1 从项目简介开始

打开 `README.md`，先搭建基本框架：

```markdown
# 智能课程表

> 一个基于 Python 的课程表管理工具，支持自动导入教务系统数据。

## 功能特性

- 自动从教务系统导入课程
- 支持手动添加和编辑课程
- 生成周视图和学期视图
- 课程冲突检测与提醒

## 快速开始

​```bash
git clone https://github.com/user/smart-schedule.git
cd smart-schedule
pip install -r requirements.txt
python main.py
​```
```

**渲染效果：**

> # 智能课程表
> > 一个基于 Python 的课程表管理工具，支持自动导入教务系统数据。
>
> ## 功能特性
> - 自动从教务系统导入课程
> - 支持手动添加和编辑课程
> - 生成周视图和学期视图
> - 课程冲突检测与提醒
>
> ## 快速开始
> ```bash
> git clone https://github.com/user/smart-schedule.git
> cd smart-schedule
> pip install -r requirements.txt
> python main.py
> ```

你已经用到了列表和代码块。让我们深入学习这两个强大的工具。

---

## 2.2 列表：组织信息的利器

### 无序列表

用 `-`、`*` 或 `+` 开头，缩进两个空格创建子列表：

```markdown
- 前端技术
  - HTML5
  - CSS3
  - JavaScript
- 后端技术
  - Python
  - Node.js
- 数据库
  - MySQL
  - MongoDB
```

**渲染效果：**

> - 前端技术
>   - HTML5
>   - CSS3
>   - JavaScript
> - 后端技术
>   - Python
>   - Node.js
> - 数据库
>   - MySQL
>   - MongoDB

### 有序列表

数字 + 点号 + 空格，子列表缩进三个空格：

```markdown
1. 安装 Python
   1. 下载安装包
   2. 运行安装程序
   3. 验证安装：`python --version`
2. 安装依赖
   1. `pip install numpy`
   2. `pip install pandas`
3. 运行项目
```

**渲染效果：**

> 1. 安装 Python
>    1. 下载安装包
>    2. 运行安装程序
>    3. 验证安装：`python --version`
> 2. 安装依赖
>    1. `pip install numpy`
>    2. `pip install pandas`
> 3. 运行项目

!!! tip "列表技巧"
    - 有序列表的数字不需要连续——Markdown 会自动递增，全部写 `1.` 也可以
    - 列表中可以嵌套代码块、引用等其他元素

---

## 2.3 代码：展示你的技术实力

### 行内代码

用单个反引号包裹：

```markdown
使用 `print()` 函数输出内容。

配置文件 `config.yaml` 位于项目根目录。
```

**渲染效果：** `print()` 和 `config.yaml` 使用等宽字体和浅灰色背景，与正文明显区分。

### 代码块

用三个反引号包裹，并指定语言获得语法高亮：

````markdown
​```python
def calculate_average(scores):
    """计算平均分，自动排除无效成绩"""
    valid = [s for s in scores if 0 <= s <= 100]
    if not valid:
        return 0
    return sum(valid) / len(valid)

scores = [85, 92, -1, 78, 105, 88]
avg = calculate_average(scores)
print(f"有效成绩平均分：{avg:.1f}")
​```
````

**渲染效果：**

```python
def calculate_average(scores):
    """计算平均分，自动排除无效成绩"""
    valid = [s for s in scores if 0 <= s <= 100]
    if not valid:
        return 0
    return sum(valid) / len(valid)

scores = [85, 92, -1, 78, 105, 88]
avg = calculate_average(scores)
print(f"有效成绩平均分：{avg:.1f}")
```

代码块有独立的背景区域，关键字、字符串、函数名显示不同颜色，右上角通常有复制按钮。

!!! tip "常用语言标识"
    `python`、`javascript`、`bash`、`json`、`yaml`、`html`、`css`、`sql`、`java`、`cpp`

---

## 2.4 链接：连接你的知识网络

```markdown
[链接文字](https://example.com)

[带提示的链接](https://example.com "鼠标悬停时显示这段文字")

<https://example.com>  <!-- 自动链接，直接写 URL -->
```

**渲染效果：** [链接文字](https://example.com) 显示为蓝色带下划线，点击跳转。带提示的链接在鼠标悬停时显示提示文字。

### 文档内跳转

```markdown
[跳转到安装步骤](#快速开始)

## 快速开始
```

**渲染效果：** 点击后页面平滑滚动到"快速开始"标题位置。锚点 ID 由标题自动生成（空格变 `-`，英文转小写）。

---

## 2.5 图片：一图胜千言

```markdown
![替代文字](screenshot.png)

![带标题的截图](screenshot.png "应用主界面")

[![点击图片跳转](logo.png)](https://example.com)  <!-- 图片链接 -->
```

**渲染效果：** 图片直接嵌入显示在文档中。如果图片加载失败，则显示替代文字。图片链接点击后会跳转到目标网址。

!!! warning "图片路径"
    推荐使用相对路径引用图片，如 `images/screenshot.png`。这样项目移动位置后图片仍然能正常显示。

---

## 2.6 完善你的项目 README

现在把学到的技能整合起来，完成一份专业的 README：

```markdown
# 智能课程表

> 一个基于 Python 的课程表管理工具，支持自动导入教务系统数据。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)

## 功能特性

- **自动导入**：一键从教务系统导入课程数据
- **冲突检测**：自动检测时间冲突并提醒
- **多视图**：支持周视图、学期视图和列表视图
- **导出分享**：导出为 ICS 日历格式，同步到手机

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装

​```bash
git clone https://github.com/user/smart-schedule.git
cd smart-schedule
pip install -r requirements.txt
​```

### 运行

​```bash
python main.py
​```

## 使用截图

![主界面](images/main.png)
![课程编辑](images/edit.png)

## 项目结构

​```
smart-schedule/
├── main.py          # 程序入口
├── config.yaml      # 配置文件
├── src/
│   ├── parser.py    # 教务系统解析
│   ├── scheduler.py # 课程调度
│   └── export.py    # 导出功能
└── tests/           # 测试文件
​```

## 贡献指南

欢迎提交 Issue 和 Pull Request！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

本项目采用 [MIT License](LICENSE)。
```

**渲染效果：** 顶部显示项目名称和描述，徽章展示项目状态；功能特性用列表清晰呈现；安装步骤用有序列表引导；代码块有语法高亮；项目结构用代码块展示目录树。

---

## 本章回顾

你的项目主页已经初具规模！回顾一下新掌握的技能：

- [x] 用 `-` 和 `1.` 创建无序和有序列表，支持嵌套
- [x] 用 `` ` `` 创建行内代码，用 ` ```语言 ` 创建语法高亮代码块
- [x] 用 `[文字](URL)` 创建链接，支持文档内跳转
- [x] 用 `![替代](URL)` 插入图片，支持图片链接

---

👉 [进入第 3 章：团队协作文档 →](03-tips.md)