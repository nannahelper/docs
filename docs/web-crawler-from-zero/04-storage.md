# 第 4 章：数据持久化——将战利品存入仓库 (Data Persistence)

## 📺 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 掌握 CSV 与 JSON 格式的数据导出，理解不同存储方案的选型策略，建立数据持久化的工程规范 |
| **核心比喻** | **仓库管理系统 (Warehouse Management System)** |
| **预计时长** | 60 分钟 |
| **关键库/概念** | `csv` 模块, `json` 模块, `pandas`, 编码处理, 增量写入 |
| **实践任务** | 将第 3 章提取的 25 部电影数据分别导出为 CSV 和 JSON 文件 |

---

在第 3 章中，我们成功从 HTML 中提取了电影数据，并将它们组织为 Python 字典列表。但这些数据目前只存在于内存中——一旦程序结束，它们就会消失。本章的目标是建立一套可靠的"仓储系统"，让数据永久保存。

---

## 4.1 存储方案选型：CSV vs JSON vs 数据库

不同的应用场景需要不同的存储策略：

| 方案 | 格式 | 优点 | 缺点 | 适用场景 |
|:---|:---|:---|:---|:---|
| **CSV** | 纯文本表格 | 通用性强，Excel 可直接打开 | 不支持嵌套结构，类型信息丢失 | 表格数据、数据分析 |
| **JSON** | 键值对文本 | 支持嵌套，保留数据类型 | 文件体积大，不易人工阅读 | API 数据交换、配置存储 |
| **SQLite** | 二进制数据库 | 支持 SQL 查询，适合大数据量 | 需要额外学习 SQL | 大规模数据、频繁查询 |
| **MongoDB** | 文档数据库 | Schema-less，灵活 | 需要独立部署 | 非结构化数据、快速迭代 |

!!! info "名词解释：序列化 (Serialization)"
    **序列化** 是将内存中的数据结构（如 Python 字典）转换为可存储或传输的格式（如 JSON 字符串）的过程。反序列化则是其逆过程。

---

## 4.2 CSV 导出：Python 标准库方案

CSV（Comma-Separated Values）是最通用的表格数据格式。Python 内置的 `csv` 模块提供了完整的读写支持。

### 基础导出

```python
import csv

# 假设 movies_data 是第 3 章中提取的电影字典列表
movies_data = [
    {"排名": 1, "中文名": "肖申克的救赎", "评分": 9.7, "短评": "希望让人自由。"},
    {"排名": 2, "中文名": "霸王别姬", "评分": 9.6, "短评": "风华绝代。"},
    # ... 更多数据
]

# 指定 CSV 文件路径
csv_file = "douban_top250.csv"

# newline="" 参数防止 Windows 下出现多余空行
# encoding="utf-8-sig" 确保 Excel 能正确识别中文（BOM 头）
with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
    # 从第一条数据中提取表头（字典的键）
    fieldnames = movies_data[0].keys()

    # 创建 DictWriter 对象
    # DictWriter 会根据 fieldnames 自动将字典映射到 CSV 列
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 写入表头行
    writer.writeheader()

    # 逐行写入数据
    for movie in movies_data:
        writer.writerow(movie)

print(f"✅ 数据已导出到 {csv_file}")
```

### 处理包含逗号和换行的字段

CSV 的"分隔符"是逗号。如果数据本身包含逗号（如导演信息 `"弗兰克·德拉邦特, 蒂姆·罗宾斯"`），`csv` 模块会自动用双引号包裹该字段，无需手动处理。

```python
# csv 模块自动处理特殊字符
movie = {"导演": "弗兰克·德拉邦特, 蒂姆·罗宾斯"}  # 包含逗号
writer.writerow(movie)
# 输出: "弗兰克·德拉邦特, 蒂姆·罗宾斯"  ← 自动加引号
```

---

## 4.3 CSV 导出：Pandas 高级方案

对于数据分析场景，`pandas` 提供了更强大的导出能力。

```bash
pip install pandas
```

```python
import pandas as pd

# 将字典列表直接转换为 DataFrame
# DataFrame 是 pandas 的核心数据结构，类似 Excel 表格
df = pd.DataFrame(movies_data)

# 按评分降序排列
df_sorted = df.sort_values(by="评分", ascending=False)

# 导出为 CSV
# index=False 表示不导出行号
df_sorted.to_csv("douban_top250_sorted.csv", index=False, encoding="utf-8-sig")

# 查看数据概览
print(f"数据形状: {df.shape}")  # (25, 7) 表示 25 行 7 列
print(f"平均评分: {df['评分'].mean():.2f}")
print(f"最高评分: {df['评分'].max()}")
print(f"最低评分: {df['评分'].min()}")
```

!!! tip "作者经验：CSV 编码问题"
    - **utf-8**：通用编码，但 Excel 直接打开会乱码。
    - **utf-8-sig**：带 BOM 头的 UTF-8，Excel 能正确识别中文。**推荐用于 CSV 导出。**
    - **gbk**：Windows 中文系统默认编码，但跨平台兼容性差。

---

## 4.4 JSON 导出：保留数据结构的完整性

JSON（JavaScript Object Notation）是 Web 开发中最通用的数据交换格式。与 CSV 不同，JSON 天然支持嵌套结构。

### 基础导出

```python
import json

json_file = "douban_top250.json"

# ensure_ascii=False 确保中文不被转义为 \uXXXX
# indent=2 使输出格式化，便于人工阅读
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(movies_data, f, ensure_ascii=False, indent=2)

print(f"✅ 数据已导出到 {json_file}")
```

### JSON 导出效果预览

```json
[
  {
    "排名": 1,
    "中文名": "肖申克的救赎",
    "英文名": "The Shawshank Redemption",
    "评分": 9.7,
    "评价人数": "1550880",
    "短评": "希望让人自由。",
    "详情": "导演: 弗兰克·德拉邦特 主演: 蒂姆·罗宾斯 / 摩根·弗里曼... 1994 / 美国 / 犯罪 剧情",
    "链接": "https://movie.douban.com/subject/1292052/"
  },
  {
    "排名": 2,
    "中文名": "霸王别姬",
    "评分": 9.6,
    "短评": "风华绝代。"
  }
]
```

### JSON 参数详解

| 参数 | 作用 | 推荐值 |
|:---|:---|:---|
| `ensure_ascii` | `False` 时保留中文原文，`True` 时转义为 `\uXXXX` | `False` |
| `indent` | 缩进空格数，`None` 表示紧凑输出 | `2` 或 `4` |
| `sort_keys` | 是否按 key 排序 | `False`（保持原始顺序） |
| `default` | 处理不可序列化对象（如 datetime）的回调函数 | 按需使用 |

---

## 4.5 增量写入：追加而非覆盖

在实际爬虫项目中，你可能需要分批次抓取数据。如果每次都覆盖文件，之前的数据就会丢失。

### CSV 增量写入

```python
import csv
import os

csv_file = "douban_top250_all.csv"
file_exists = os.path.isfile(csv_file)

# 以追加模式打开文件
with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:
    fieldnames = ["排名", "中文名", "评分", "短评"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 只在文件不存在时写入表头（避免重复表头）
    if not file_exists:
        writer.writeheader()

    # 追加新数据
    for movie in new_batch_of_movies:
        writer.writerow(movie)
```

### JSON 增量写入

JSON 格式不支持直接追加。你需要先读取已有数据，合并后再写回：

```python
import json

json_file = "douban_top250_all.json"

# 尝试读取已有数据
try:
    with open(json_file, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    existing_data = []

# 合并新旧数据
existing_data.extend(new_batch_of_movies)

# 写回文件
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=2)
```

---

## 4.6 完整实战：整合抓取与存储

将第 3 章的解析代码与本章的存储代码整合为一个完整的模块：

```python
"""
电影数据抓取与存储模块
功能：抓取豆瓣电影 Top 250 首页数据，并导出为 CSV 和 JSON
"""
import requests
import csv
import json
from bs4 import BeautifulSoup


def fetch_movies():
    """抓取豆瓣电影 Top 250 首页数据"""
    url = "https://movie.douban.com/top250"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "lxml")

    movie_items = soup.find_all("div", class_="item")
    movies = []

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

        movies.append({
            "排名": int(rank),
            "中文名": chinese_title,
            "英文名": english_title,
            "评分": float(rating),
            "评价人数": rating_people,
            "短评": quote,
            "详情": director_info,
            "链接": link,
        })

    return movies


def save_to_csv(movies, filename="douban_top250.csv"):
    """将电影数据保存为 CSV 文件"""
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        fieldnames = movies[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(movies)
    print(f"✅ CSV 已保存: {filename} ({len(movies)} 条记录)")


def save_to_json(movies, filename="douban_top250.json"):
    """将电影数据保存为 JSON 文件"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON 已保存: {filename} ({len(movies)} 条记录)")


if __name__ == "__main__":
    print("正在抓取豆瓣电影 Top 250 首页...")
    movies = fetch_movies()

    if movies:
        save_to_csv(movies)
        save_to_json(movies)
        print(f"\n📊 数据概览:")
        print(f"   共抓取 {len(movies)} 部电影")
        print(f"   评分最高: {movies[0]['中文名']} ({movies[0]['评分']})")
        print(f"   评分最低: {movies[-1]['中文名']} ({movies[-1]['评分']})")
    else:
        print("❌ 未抓取到任何数据，请检查网络或请求头配置。")
```

---

## 💡 本章小结

- **CSV** 适合表格数据，通用性强，Excel 可直接打开。
- **JSON** 适合嵌套结构，保留数据类型，是 API 交互的标准格式。
- **utf-8-sig** 编码确保 Excel 正确显示中文。
- **增量写入** 是分批抓取场景的必备技巧。
- **模块化设计**：将抓取、解析、存储分离为独立函数，提高代码可维护性。

**下一章预告：** 我们已经能抓取首页数据了，但豆瓣的反爬系统随时可能将我们"拒之门外"。在第 5 章中，我们将学习如何应对反爬挑战，成为真正的"伪装大师"！

👉 [进入第 5 章：应对反爬挑战 →](05-anti-scraping.md)
