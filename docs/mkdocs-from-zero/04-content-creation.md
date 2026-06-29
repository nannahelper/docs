# 第 4 章：内容创作

> **让文档活起来** —— 掌握 MkDocs Material 专属的 Markdown 写作技巧，写出专业美观的技术文档。

---

## 4.1 创建第一个子页面

在 `docs/` 目录下创建子文件夹和页面：

```bash
mkdir docs\guide          # Windows
# 或
mkdir docs/guide           # macOS / Linux
```

然后在 `docs/guide/` 中创建 `quickstart.md`：

```markdown
# 快速开始

欢迎阅读快速开始指南！这里将帮助你 **在 5 分钟内** 上手本项目。

## 安装

​```bash
pip install my-package
​```

## 基本用法

​```python
from my_package import hello

hello("World")
​```
```

!!! note "文件路径与 nav 配置的对应关系"

    如果你在 `nav` 中配置了 `- 快速开始: guide/quickstart.md`，MkDocs 会在 `docs/guide/quickstart.md` 查找文件。路径是相对于 `docs/` 目录的。

---

## 4.2 弹窗组件（Admonitions）

Material 主题支持丰富的弹窗组件，用于突出显示不同类型的信息：

```markdown
!!! note "这是一个提示"
    这是普通提示信息，用于补充说明。

!!! info "信息框"
    用于提供额外的背景信息或上下文。

!!! tip "小技巧"
    用于分享最佳实践和实用建议。

!!! warning "警告"
    用于提醒用户注意潜在问题。

!!! danger "危险"
    用于警告可能导致严重后果的操作。

!!! example "示例"
    用于展示代码示例或使用场景。

!!! quote "引用"
    用于引用外部内容或名言。
```

**渲染效果：** 每种弹窗都有不同的颜色和图标——`note` 是蓝色信息图标，`tip` 是绿色灯泡，`warning` 是橙色三角，`danger` 是红色闪电。这让读者能快速识别信息的类型和重要程度。

### 可折叠弹窗

在类型后添加 `+` 或 `-` 可以控制默认展开/折叠状态：

```markdown
???+ note "默认展开的弹窗"
    点击标题可以折叠内容。

??? warning "默认折叠的弹窗"
    需要点击才能展开查看内容。
```

### 内联弹窗

使用 `inline` 修饰符让弹窗在文本流中显示：

```markdown
!!! note inline "内联提示"
    这个弹窗会和后面的文字在同一行显示。
```

---

## 4.3 代码块

### 语法高亮

在代码块开头指定语言即可启用语法高亮：

````markdown
​```python
def greet(name: str) -> str:
    """向指定用户打招呼"""
    return f"Hello, {name}!"

print(greet("World"))
​```
````

**渲染效果：** Python 关键字（`def`、`return`）、字符串、函数名和注释会分别以不同颜色显示，让代码结构一目了然。

### 代码块标题

使用 `title` 属性给代码块添加标题：

````markdown
​```python title="greet.py"
def greet(name):
    return f"Hello, {name}!"
​```
````

### 行号

使用 `linenums` 属性显示行号：

````markdown
​```python linenums="1"
def greet(name):
    return f"Hello, {name}!"

def main():
    print(greet("World"))
​```
````

### 高亮特定行

````markdown
​```python hl_lines="2 4"
def greet(name):          # 第 1 行
    return f"Hello!"      # 第 2 行（高亮）
                           # 第 3 行
def main():               # 第 4 行（高亮）
    print(greet("World"))
​```
````

---

## 4.4 内容标签页（Content Tabs）

标签页非常适合展示"不同操作系统下的不同命令"或"不同语言的同一功能"：

````markdown
=== "Windows"

    ​```powershell
    mkdir my-project
    cd my-project
    ​```

=== "macOS / Linux"

    ​```bash
    mkdir my-project
    cd my-project
    ​```
````

**渲染效果：** 页面上会显示"Windows"和"macOS / Linux"两个标签页，用户点击切换查看对应内容。这比分别写两个章节更加紧凑和直观。

!!! tip "标签页的最佳使用场景"

    - 不同操作系统的安装命令
    - 不同编程语言的同一算法实现
    - 不同版本的 API 用法对比
    - 同一功能的多种实现方式

---

## 4.5 表格

MkDocs Material 会自动美化表格样式：

```markdown
| 功能 | 说明 | 状态 |
|:---|:---|:---:|
| 全文搜索 | 支持中英文搜索 | ✅ |
| 暗色模式 | 自动/手动切换 | ✅ |
| 代码复制 | 一键复制代码块 | ✅ |
| 响应式 | 适配手机/平板/桌面 | ✅ |
```

**渲染效果：** 表格会自动应用斑马纹（交替行背景色），表头加粗居中。`:---` 表示左对齐，`:---:` 表示居中对齐，`---:` 表示右对齐。

---

## 4.6 图片与图表

### 插入图片

```markdown
![图片描述](../assets/screenshot.png)

<!-- 带标题的图片 -->
<figure markdown="span">
  ![图片描述](../assets/screenshot.png)
  <figcaption>图 1：网站首页截图</figcaption>
</figure>
```

### Mermaid 流程图

Material 主题内置了 Mermaid 图表支持：

````markdown
​```mermaid
flowchart TD
    A[开始] --> B{是否已安装 Python？}
    B -->|是| C[安装 MkDocs]
    B -->|否| D[安装 Python]
    D --> C
    C --> E[创建项目]
    E --> F[编写文档]
    F --> G[部署上线]
    G --> H[完成]
​```
````

**渲染效果：** Mermaid 代码会被渲染为可交互的矢量流程图，支持缩放和平移。这比截图更加清晰，且可以随主题切换颜色。

---

## 4.7 格式化文本

```markdown
**粗体文字**          → 渲染为 **粗体文字**

*斜体文字*            → 渲染为 *斜体文字*

`行内代码`            → 渲染为 `行内代码`

~~删除线~~            → 渲染为 ~~删除线~~

==高亮文字==          → 渲染为 ==高亮文字==

^上标^ 和 ~下标~      → 渲染为上标和下标

H~2~O 和 X^2^         → H₂O 和 X²
```

!!! warning "粗体标记前后必须加空格"

    为确保 MkDocs 正确渲染粗体文字，`**` 标记前后必须各留一个空格：
    
    - ✅ `这是 **粗体文字** 示例`
    - ❌ `这是 **粗体文字** 示例`

---

## 4.8 任务列表

```markdown
- [x] 已完成的任务
- [x] 另一个已完成的任务
- [ ] 待完成的任务
- [ ] 另一个待完成的任务
```

**渲染效果：** 已完成的项显示为勾选的复选框，未完成的显示为空复选框。这在教程的"本章要点总结"中非常实用。

---

## 本章要点总结

- [ ] 能在 `docs/` 下创建子目录和 Markdown 文件
- [ ] 掌握 7 种弹窗组件的用法
- [ ] 能使用代码块语法高亮、行号、高亮行
- [ ] 能使用标签页展示多版本内容
- [ ] 能插入表格、图片和 Mermaid 流程图
- [ ] 了解粗体标记的空格规范

---

👉 [进入第 5 章：主题定制 →](05-theme-customization.md)