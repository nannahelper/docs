# 第 3 章：精准解析网页——像外科医生一样提取数据 (HTML Parsing)

## 📺 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 掌握 BeautifulSoup 核心 API，熟练使用 CSS 选择器与 find 系列方法精准提取结构化数据 |
| **核心比喻** | **外科手术式数据剥离 (Surgical Data Extraction)** |
| **预计时长** | 90 分钟 |
| **关键库/概念** | `BeautifulSoup`, `lxml` 解析器, CSS Selector, `find()` / `find_all()`, 标签导航 |
| **实践任务** | 从豆瓣电影 Top 250 首页提取所有电影的标题、评分和短评金句 |

---

在第 2 章中，我们成功获取了豆瓣电影 Top 250 的 HTML 源码。但它看起来像这样：

```html
<div class="info">
    <div class="hd">
        <a href="https://movie.douban.com/subject/1292052/" class="">
            <span class="title">肖申克的救赎</span>
            <span class="title"> / The Shawshank Redemption</span>
            <span class="other"> / 月黑高飞(港)  / 刺激1995(台)</span>
        </a>
        <span class="playable">[可播放]</span>
    </div>
    <div class="bd">
        <p class="">导演: 弗兰克·德拉邦特&nbsp;&nbsp;主演: 蒂姆·罗宾斯 / 摩根·弗里曼...</p>
        <div class="star">
            <span class="rating_num">9.7</span>
            <span>1550880人评价</span>
        </div>
        <p class="quote">
            <span class="inq">希望让人自由。</span>
        </p>
    </div>
</div>
```

我们的任务是从这堆"乱码"中精准提取出： **电影名、评分、导演、短评** 。这就是本章的核心使命。

---

## 3.1 解析器选型：BeautifulSoup + lxml

### 为什么选择 BeautifulSoup？

Python 生态中有多种 HTML 解析方案：

| 方案 | 优点 | 缺点 | 适用场景 |
|:---|:---|:---|:---|
|  **正则表达式**  | 无需额外库 | 极其脆弱，HTML 结构一变就失效 | ❌ 不推荐用于 HTML 解析 |
|  **BeautifulSoup + lxml**  | API 优雅，容错性强 | 速度中等 | ✅  **本教程选择**  |
|  **lxml.etree (XPath)**  | 速度极快 | API 不够直观 | 大规模高性能场景 |
|  **PyQuery**  | jQuery 风格语法 | 社区较小 | 前端开发者友好 |

!!! info "名词解释：BeautifulSoup"
     **BeautifulSoup**  是一个可以从 HTML 或 XML 文件中提取数据的 Python 库。它能够自动修复破损的 HTML 标签，并提供多种导航、搜索和修改解析树的方式。

### 🛠️ 安装依赖

```bash
pip install beautifulsoup4 lxml
```

`lxml` 是底层 C 语言实现的解析器，速度比 Python 原生的 `html.parser` 快数倍。

---

## 3.2 BeautifulSoup 核心对象模型

### 创建 Soup 对象

```python
import requests
from bs4 import BeautifulSoup

url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers, timeout=10)
response.encoding = response.apparent_encoding

# 创建 BeautifulSoup 对象
# 第一个参数：HTML 字符串
# 第二个参数：指定解析器（推荐使用 lxml）
soup = BeautifulSoup(response.text, "lxml")
```

### 四大核心对象

| 对象 | 说明 | 示例 |
|:---|:---|:---|
| **Tag** | HTML 标签对象，可访问属性（如 `class`, `href`） | `soup.find("span")` |
| **NavigableString** | 标签内的文本内容 | `tag.string` 或 `tag.get_text()` |
| **BeautifulSoup** | 整个文档对象，本质是特殊的 Tag | `soup` 本身 |
| **Comment** | HTML 注释，是特殊的 NavigableString | 通常忽略 |

---

## 3.3 搜索方法详解：find() 与 find_all()

这是 BeautifulSoup 最核心的两个方法，你必须熟练掌握。

### find_all() —— 查找所有匹配的标签

```python
# 语法：find_all(name, attrs, recursive, string, limit, **kwargs)

# 1. 按标签名查找 —— 找到所有 <span> 标签
all_spans = soup.find_all("span")

# 2. 按 class 属性查找 —— 找到所有 class="title" 的标签
#    注意：class 是 Python 关键字，所以用 class_ 代替
titles = soup.find_all("span", class_="title")

# 3. 按多个属性查找 —— 精确匹配
specific = soup.find_all("span", attrs={"class": "rating_num"})

# 4. 限制返回数量 —— 只取前 5 个
first_five = soup.find_all("span", class_="title", limit=5)

# 5. 按文本内容查找 —— 找到包含"肖申克"的标签
matching = soup.find_all(string=lambda text: "肖申克" in str(text))
```

### find() —— 只返回第一个匹配项

```python
# find() 与 find_all(limit=1) 等价，但返回单个 Tag 而非列表
first_movie = soup.find("div", class_="item")
```

!!! tip "作者经验：find() vs find_all() 的选择"
    - 当你确定只有一个目标元素时，用 `find()`，它直接返回 Tag 对象。
    - 当可能有多个匹配时，用 `find_all()`，它返回列表。
    - 常见错误：对 `find_all()` 的结果直接调用 `.text`，忘记它是列表。

---

## 3.4 CSS 选择器：select() 方法

如果你熟悉前端开发，CSS 选择器是更优雅的定位方式。

```python
# select() 使用 CSS 选择器语法，返回列表
# select_one() 只返回第一个匹配项

# 1. 按标签选择
soup.select("span")

# 2. 按 class 选择（. 前缀）
soup.select(".title")           # class="title"
soup.select("span.title")       # <span class="title">

# 3. 按 id 选择（# 前缀）
soup.select("#content")

# 4. 层级选择（空格分隔）
soup.select("div.info div.hd a")     # div.info 下的 div.hd 下的 a 标签

# 5. 直接子元素选择（> 分隔）
soup.select("ol.grid_view > li")     # ol.grid_view 的直接子元素 li

# 6. 属性选择
soup.select("a[href]")               # 所有带 href 属性的 a 标签
soup.select('a[href*="subject"]')    # href 包含 "subject" 的 a 标签
```

### 📊 find 系列 vs CSS 选择器 对比

| 特性 | find / find_all | select / select_one |
|:---|:---|:---|
| **语法风格** | Python 函数调用 | CSS 选择器字符串 |
| **可读性** | 参数明确，适合简单查询 | 表达式紧凑，适合复杂层级 |
| **性能** | 略快 | 略慢（需解析 CSS 表达式） |
| **学习曲线** | 低 | 需要 CSS 基础知识 |
| **推荐场景** | 简单标签/属性匹配 | 深层嵌套、复杂条件组合 |

---

## 3.5 实战：提取豆瓣电影 Top 250 首页数据

现在，让我们将理论付诸实践。我们将从首页提取 25 部电影的完整信息。

### 步骤 1：定位电影列表容器

```python
import requests
from bs4 import BeautifulSoup

url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers, timeout=10)
response.encoding = response.apparent_encoding
soup = BeautifulSoup(response.text, "lxml")

# 每部电影都包裹在 class="item" 的 div 中
# 使用 find_all 获取所有电影条目
movie_items = soup.find_all("div", class_="item")
print(f"本页共找到 {len(movie_items)} 部电影")
```

**验证结果：** 输出应为 `本页共找到 25 部电影` ✅

### 步骤 2：逐部提取详细信息

```python
for item in movie_items:
    # --- 提取排名 ---
    # 排名在 <em class="">1</em> 中
    rank = item.find("em").get_text()

    # --- 提取电影标题 ---
    # 中文标题在第一个 <span class="title"> 中
    # 注意：每部电影有两个 title span（中文 + 英文/港台译名）
    title_spans = item.find_all("span", class_="title")
    chinese_title = title_spans[0].get_text()  # 第一个是中文名
    # 有些电影没有英文名，需要做安全处理
    english_title = title_spans[1].get_text().replace("\xa0/\xa0", "").strip() if len(title_spans) > 1 else "无"

    # --- 提取评分 ---
    # 评分在 <span class="rating_num"> 中
    rating = item.find("span", class_="rating_num").get_text()

    # --- 提取评价人数 ---
    # 评价人数在包含 "人评价" 的 span 中
    # 使用正则从文本中提取数字
    rating_people_text = item.find("div", class_="star").find_all("span")[-1].get_text()
    rating_people = rating_people_text.replace("人评价", "")

    # --- 提取短评金句 ---
    # 短评在 <span class="inq"> 中，部分电影可能没有
    quote_tag = item.find("span", class_="inq")
    quote = quote_tag.get_text() if quote_tag else "无短评"

    # --- 提取导演与主演 ---
    # 导演和主演在 <p class=""> 的第一个文本节点中
    info_p = item.find("p", class_="")
    # get_text() 获取所有文本，用 strip() 去除首尾空白
    director_info = info_p.get_text().strip().replace("\xa0", " ")

    # --- 提取电影链接 ---
    link = item.find("a")["href"]

    print(f"排名: {rank}")
    print(f"中文名: {chinese_title}")
    print(f"英文名: {english_title}")
    print(f"评分: {rating} (共 {rating_people} 人评价)")
    print(f"短评: {quote}")
    print(f"链接: {link}")
    print(f"详情: {director_info}")
    print("-" * 60)
```

### 步骤 3：结构化存储为字典列表

```python
movies_data = []  # 用于存储所有电影信息的列表

for item in movie_items:
    rank = item.find("em").get_text()

    title_spans = item.find_all("span", class_="title")
    chinese_title = title_spans[0].get_text()
    english_title = title_spans[1].get_text().replace("\xa0/\xa0", "").strip() if len(title_spans) > 1 else "无"

    rating = item.find("span", class_="rating_num").get_text()

    rating_people_text = item.find("div", class_="star").find_all("span")[-1].get_text()
    rating_people = rating_people_text.replace("人评价", "")

    quote_tag = item.find("span", class_="inq")
    quote = quote_tag.get_text() if quote_tag else "无短评"

    info_p = item.find("p", class_="")
    director_info = info_p.get_text().strip().replace("\xa0", " ")

    link = item.find("a")["href"]

    # 将每部电影的信息组织为字典
    movie = {
        "排名": int(rank),
        "中文名": chinese_title,
        "英文名": english_title,
        "评分": float(rating),
        "评价人数": rating_people,
        "短评": quote,
        "详情": director_info,
        "链接": link,
    }
    movies_data.append(movie)

print(f"✅ 成功提取 {len(movies_data)} 部电影的数据！")
print(f"第一部电影: {movies_data[0]['中文名']} - 评分 {movies_data[0]['评分']}")
```

---

## 3.6 常见陷阱与排错指南

### 陷阱 1：AttributeError: 'NoneType' object has no attribute 'get_text'

**原因：** `find()` 没有找到匹配的标签，返回了 `None`。

**解决方案：** 在调用方法前检查是否为 `None`：

```python
quote_tag = item.find("span", class_="inq")
quote = quote_tag.get_text() if quote_tag else "无短评"
```

### 陷阱 2：提取到多余的空格和换行符

**原因：** HTML 源码中通常包含大量空白字符。

**解决方案：** 使用 `.strip()` 和 `.replace()` 清理：

```python
text = tag.get_text().strip().replace("\n", "").replace(" ", "")
```

### 陷阱 3：class 属性包含多个值

**原因：** HTML 的 class 可以是多个值，如 `class="title other"`。

**解决方案：** BeautifulSoup 会匹配包含该值的所有标签：

```python
# class="title other" 也会被 class_="title" 匹配到
soup.find_all("span", class_="title")
```

---

## 3.7 实战练习：提取更多维度的数据

尝试扩展上述代码，额外提取以下信息：

1.  **电影海报图片 URL** ：在 `<img>` 标签的 `src` 属性中。
2.  **是否可播放** ：检查是否存在 `<span class="playable">[可播放]</span>`。
3.  **上映年份** ：从 `info_p` 文本中用正则提取四位数字年份。

```python
import re

# 提取上映年份的示例
info_text = "导演: 弗兰克·德拉邦特主演: 蒂姆·罗宾斯...1994 / 美国 / 犯罪 剧情"
year_match = re.search(r"(\d{4})", info_text)
year = year_match.group(1) if year_match else "未知"
print(f"上映年份: {year}")
```

---

## 💡 本章小结

- **BeautifulSoup** 是 Python 最优雅的 HTML 解析库，配合 `lxml` 解析器性能最佳。
- **find() / find_all()** 按标签名和属性搜索，适合简单场景。
- **select() / select_one()** 使用 CSS 选择器语法，适合复杂层级定位。
-  **防御性编程** ：始终检查 `find()` 的返回值是否为 `None`。
-  **数据清洗** ：使用 `.strip()`, `.replace()`, 正则表达式清理提取到的文本。

**下一章预告：** 我们已经成功提取了数据，但它们还"漂浮"在内存中。在第 4 章中，我们将学习如何将数据持久化到 CSV 和 JSON 文件中，让"战利品"永久保存！

👉 [进入第 4 章：数据持久化 →](04-storage.md)
