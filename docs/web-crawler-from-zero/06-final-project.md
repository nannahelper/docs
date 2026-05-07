# 第 6 章：完整实战：抓取豆瓣 Top 250 全榜单 (Final Project)

## 📺 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 整合前 5 章全部知识，独立完成一个工程化的全榜单爬虫项目 |
| **核心比喻** | **自动化情报流水线 (Automated Intelligence Pipeline)** |
| **预计时长** | 90 分钟 |
| **关键技术** | 翻页逻辑分析, 模块化架构, 断点续抓, 数据校验, 日志系统 |
| **最终产出** | 一份包含 250 部电影完整信息的 CSV/JSON 文件 + 可复用的爬虫框架 |

---

这是本教程的终章。我们将不再满足于"能跑就行"的脚本，而是构建一个具备工程化思维的完整爬虫项目。你将学到的不仅是代码，更是一套可复用的方法论。

---

## 6.1 翻页逻辑分析：破解分页规律

豆瓣电影 Top 250 共有 10 页，每页 25 部电影。我们需要找出 URL 的翻页规律。

### 🔍 观察 URL 模式

| 页码 | URL |
|:---|:---|
| 第 1 页 | `https://movie.douban.com/top250` |
| 第 2 页 | `https://movie.douban.com/top250?start=25` |
| 第 3 页 | `https://movie.douban.com/top250?start=50` |
| 第 10 页 | `https://movie.douban.com/top250?start=225` |

**规律发现：** `start` 参数的值 = `(页码 - 1) × 25`

```python
# 生成所有 10 页的 URL
base_url = "https://movie.douban.com/top250"
all_urls = []

for page in range(10):
    start = page * 25
    if start == 0:
        url = base_url  # 第一页不需要 start 参数
    else:
        url = f"{base_url}?start={start}"
    all_urls.append(url)
    print(f"第 {page + 1} 页: {url}")
```

---

## 6.2 项目架构设计

在动手写代码之前，先设计好项目结构。良好的架构是工程化的基石。

### 📁 推荐项目结构

```
douban_crawler/
├── main.py                 # 入口文件，编排整个抓取流程
├── crawler.py              # 爬虫核心类（请求 + 解析）
├── storage.py              # 数据存储模块（CSV + JSON）
├── config.py               # 配置文件（URL、请求头、延时参数）
├── utils.py                # 工具函数（日志、延时、重试）
├── requirements.txt        # 依赖清单
├── output/                 # 输出目录
│   ├── douban_top250.csv
│   └── douban_top250.json
└── logs/                   # 日志目录
    └── crawler.log
```

### 🏗️ 架构设计原则

1. **单一职责**：每个模块只做一件事。
2. **配置分离**：URL、请求头等可变参数集中在 `config.py`。
3. **容错设计**：单页失败不影响整体流程。
4. **可观测性**：日志记录每一步的状态。

---

## 6.3 模块实现

### config.py —— 配置中心

```python
"""
爬虫配置文件
将所有可变参数集中管理，方便维护和调整
"""

# 目标 URL 模板
BASE_URL = "https://movie.douban.com/top250"

# 请求头 —— 伪装成 Chrome 浏览器
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

# 延时配置（秒）
MIN_DELAY = 1.0      # 最小请求间隔
MAX_DELAY = 3.0      # 最大请求间隔
REQUEST_TIMEOUT = 15  # 单次请求超时时间

# 重试配置
MAX_RETRIES = 3      # 最大重试次数

# 输出配置
OUTPUT_DIR = "output"
CSV_FILENAME = "douban_top250.csv"
JSON_FILENAME = "douban_top250.json"

# 日志配置
LOG_DIR = "logs"
LOG_FILENAME = "crawler.log"
```

### utils.py —— 工具函数

```python
"""
工具函数模块
提供日志、延时、重试等通用功能
"""
import os
import time
import random
import logging
from datetime import datetime


def setup_logger(log_dir="logs", log_file="crawler.log"):
    """配置日志系统 —— 同时输出到文件和控制台"""
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("DoubanCrawler")
    logger.setLevel(logging.INFO)

    # 文件处理器 —— 记录详细日志到文件
    file_handler = logging.FileHandler(
        os.path.join(log_dir, log_file),
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)

    # 控制台处理器 —— 简洁输出到屏幕
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def human_delay(min_sec=1.0, max_sec=3.0):
    """随机延时，模拟人类浏览行为"""
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)
    return delay


def ensure_dir(directory):
    """确保目录存在，不存在则创建"""
    os.makedirs(directory, exist_ok=True)
```

### crawler.py —— 爬虫核心

```python
"""
爬虫核心模块
负责发送请求、解析 HTML、提取结构化数据
"""
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import config
import utils


class DoubanCrawler:
    """豆瓣电影 Top 250 爬虫"""

    def __init__(self, logger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)

    def fetch_page(self, url, page_num):
        """抓取单页数据，带重试机制"""
        for attempt in range(config.MAX_RETRIES):
            try:
                self.logger.info(f"正在抓取第 {page_num} 页: {url}")

                response = self.session.get(url, timeout=config.REQUEST_TIMEOUT)

                if response.status_code == 200:
                    self.logger.debug(f"第 {page_num} 页请求成功 (状态码 200)")
                    return response

                if response.status_code in (429, 503):
                    wait = 2 ** attempt
                    self.logger.warning(f"第 {page_num} 页触发频率限制，等待 {wait} 秒后重试...")
                    utils.human_delay(wait, wait + 1)
                    continue

                if response.status_code == 403:
                    self.logger.error(f"第 {page_num} 页访问被拒绝 (403)")
                    return None

                response.raise_for_status()

            except RequestException as e:
                self.logger.error(f"第 {page_num} 页请求异常 (尝试 {attempt + 1}/{config.MAX_RETRIES}): {e}")
                if attempt < config.MAX_RETRIES - 1:
                    utils.human_delay(2, 5)

        self.logger.error(f"第 {page_num} 页抓取最终失败")
        return None

    def parse_page(self, html, page_num):
        """解析单页 HTML，提取电影数据"""
        soup = BeautifulSoup(html, "lxml")
        movie_items = soup.find_all("div", class_="item")

        if not movie_items:
            self.logger.warning(f"第 {page_num} 页未找到电影条目，可能页面结构已变化")
            return []

        movies = []
        for item in movie_items:
            try:
                movie = self._parse_movie_item(item)
                movies.append(movie)
            except Exception as e:
                self.logger.error(f"解析电影条目失败: {e}")
                continue

        self.logger.info(f"第 {page_num} 页解析完成，提取 {len(movies)} 部电影")
        return movies

    def _parse_movie_item(self, item):
        """解析单个电影条目"""
        # 排名
        rank = item.find("em").get_text()

        # 标题
        title_spans = item.find_all("span", class_="title")
        chinese_title = title_spans[0].get_text()
        english_title = title_spans[1].get_text().replace("\xa0/\xa0", "").strip() if len(title_spans) > 1 else ""

        # 其他译名
        other_tag = item.find("span", class_="other")
        other_title = other_tag.get_text().replace("\xa0/\xa0", "").strip() if other_tag else ""

        # 评分
        rating_tag = item.find("span", class_="rating_num")
        rating = float(rating_tag.get_text()) if rating_tag else 0.0

        # 评价人数
        star_div = item.find("div", class_="star")
        rating_people = "0"
        if star_div:
            people_text = star_div.find_all("span")[-1].get_text()
            rating_people = people_text.replace("人评价", "")

        # 短评
        quote_tag = item.find("span", class_="inq")
        quote = quote_tag.get_text() if quote_tag else ""

        # 导演与主演信息
        info_p = item.find("p", class_="")
        info_text = info_p.get_text().strip().replace("\xa0", " ") if info_p else ""

        # 提取导演和主演
        director = ""
        actors = ""
        if "导演:" in info_text:
            parts = info_text.split("主演:")
            director_part = parts[0].replace("导演:", "").strip()
            director = director_part
            if len(parts) > 1:
                actors = parts[1].strip()

        # 提取年份和国家
        import re
        year = ""
        country = ""
        year_match = re.search(r"(\d{4})", info_text)
        if year_match:
            year = year_match.group(1)

        # 链接
        link_tag = item.find("a")
        link = link_tag["href"] if link_tag else ""

        # 海报图片
        img_tag = item.find("img")
        poster_url = img_tag["src"] if img_tag else ""

        return {
            "排名": int(rank),
            "中文名": chinese_title,
            "英文名": english_title,
            "其他译名": other_title,
            "评分": rating,
            "评价人数": rating_people,
            "短评": quote,
            "导演": director,
            "主演": actors,
            "上映年份": year,
            "详情": info_text,
            "链接": link,
            "海报": poster_url,
        }

    def crawl_all(self):
        """抓取全部 10 页数据"""
        all_movies = []

        for page in range(10):
            start = page * 25
            url = config.BASE_URL if start == 0 else f"{config.BASE_URL}?start={start}"
            page_num = page + 1

            # 抓取页面
            response = self.fetch_page(url, page_num)
            if response is None:
                self.logger.warning(f"跳过第 {page_num} 页（抓取失败）")
                continue

            # 解析数据
            movies = self.parse_page(response.text, page_num)
            all_movies.extend(movies)

            # 人类行为延时（最后一页不需要延时）
            if page < 9:
                delay = utils.human_delay(config.MIN_DELAY, config.MAX_DELAY)
                self.logger.debug(f"延时 {delay:.1f} 秒")

        return all_movies
```

### storage.py —— 数据存储

```python
"""
数据存储模块
负责将电影数据导出为 CSV 和 JSON 格式
"""
import csv
import json
import os
import config


class DataStorage:
    """数据持久化管理器"""

    def __init__(self, logger):
        self.logger = logger
        utils_module = __import__("utils")
        utils_module.ensure_dir(config.OUTPUT_DIR)

    def save_csv(self, movies, filename=None):
        """保存为 CSV 文件"""
        if not movies:
            self.logger.warning("无数据可保存 (CSV)")
            return

        filepath = os.path.join(config.OUTPUT_DIR, filename or config.CSV_FILENAME)

        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            fieldnames = movies[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(movies)

        self.logger.info(f"CSV 已保存: {filepath} ({len(movies)} 条记录)")

    def save_json(self, movies, filename=None):
        """保存为 JSON 文件"""
        if not movies:
            self.logger.warning("无数据可保存 (JSON)")
            return

        filepath = os.path.join(config.OUTPUT_DIR, filename or config.JSON_FILENAME)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(movies, f, ensure_ascii=False, indent=2)

        self.logger.info(f"JSON 已保存: {filepath} ({len(movies)} 条记录)")
```

### main.py —— 入口文件

```python
"""
豆瓣电影 Top 250 爬虫 —— 主入口
整合所有模块，编排完整的抓取流程
"""
import time
import config
from utils import setup_logger
from crawler import DoubanCrawler
from storage import DataStorage


def print_banner():
    """打印启动横幅"""
    banner = """
    ╔══════════════════════════════════════════╗
    ║     豆瓣电影 Top 250 数据抓取系统        ║
    ║     Douban Movie Top 250 Crawler         ║
    ╚══════════════════════════════════════════╝
    """
    print(banner)


def print_summary(movies, elapsed_time):
    """打印抓取结果摘要"""
    if not movies:
        print("\n❌ 未抓取到任何数据")
        return

    ratings = [m["评分"] for m in movies if m["评分"] > 0]

    print("\n" + "=" * 50)
    print("📊 抓取结果摘要")
    print("=" * 50)
    print(f"  总电影数: {len(movies)} 部")
    print(f"  总耗时: {elapsed_time:.1f} 秒")
    if ratings:
        print(f"  最高评分: {max(ratings)}")
        print(f"  最低评分: {min(ratings)}")
        print(f"  平均评分: {sum(ratings) / len(ratings):.2f}")
    print(f"  输出目录: {config.OUTPUT_DIR}/")
    print("=" * 50)


def main():
    """主函数 —— 编排整个抓取流程"""
    print_banner()

    # 初始化日志系统
    logger = setup_logger(config.LOG_DIR, config.LOG_FILENAME)
    logger.info("爬虫系统启动")

    start_time = time.time()

    try:
        # 创建爬虫实例
        crawler = DoubanCrawler(logger)

        # 执行全量抓取
        logger.info("开始抓取豆瓣电影 Top 250 全榜单...")
        movies = crawler.crawl_all()

        # 数据校验
        logger.info(f"抓取完成，共获取 {len(movies)} 部电影数据")

        if len(movies) < 250:
            logger.warning(f"数据不完整！预期 250 部，实际获取 {len(movies)} 部")

        # 保存数据
        storage = DataStorage(logger)
        storage.save_csv(movies)
        storage.save_json(movies)

        # 打印摘要
        elapsed = time.time() - start_time
        print_summary(movies, elapsed)

        logger.info(f"爬虫任务完成，总耗时 {elapsed:.1f} 秒")

    except KeyboardInterrupt:
        logger.warning("用户中断爬虫运行")
        print("\n⚠️ 爬虫已被用户中断")
    except Exception as e:
        logger.error(f"爬虫运行异常: {e}", exc_info=True)
        print(f"\n❌ 爬虫运行出错: {e}")


if __name__ == "__main__":
    main()
```

---

## 6.4 运行与验证

### 安装依赖

```bash
pip install requests beautifulsoup4 lxml
```

### 启动爬虫

```bash
python main.py
```

### 预期输出

```
    ╔══════════════════════════════════════════╗
    ║     豆瓣电影 Top 250 数据抓取系统        ║
    ║     Douban Movie Top 250 Crawler         ║
    ╚══════════════════════════════════════════╝

2026-05-07 20:00:01 [INFO] 爬虫系统启动
2026-05-07 20:00:01 [INFO] 开始抓取豆瓣电影 Top 250 全榜单...
2026-05-07 20:00:01 [INFO] 正在抓取第 1 页: https://movie.douban.com/top250
2026-05-07 20:00:03 [INFO] 第 1 页解析完成，提取 25 部电影
2026-05-07 20:00:05 [INFO] 正在抓取第 2 页: https://movie.douban.com/top250?start=25
...
2026-05-07 20:01:30 [INFO] 第 10 页解析完成，提取 25 部电影
2026-05-07 20:01:30 [INFO] 抓取完成，共获取 250 部电影数据
2026-05-07 20:01:30 [INFO] CSV 已保存: output/douban_top250.csv (250 条记录)
2026-05-07 20:01:30 [INFO] JSON 已保存: output/douban_top250.json (250 条记录)

==================================================
📊 抓取结果摘要
==================================================
  总电影数: 250 部
  总耗时: 89.3 秒
  最高评分: 9.7
  最低评分: 8.9
  平均评分: 9.12
  输出目录: output/
==================================================
```

---

## 6.5 进阶优化方向

完成基础项目后，你可以从以下方向继续深化：

| 方向 | 技术方案 | 价值 |
|:---|:---|:---|
| **异步并发** | `aiohttp` + `asyncio` | 将抓取速度提升 5-10 倍 |
| **分布式抓取** | `Scrapy` + `Redis` | 支持亿级数据量 |
| **数据可视化** | `matplotlib` / `pyecharts` | 生成评分分布图、年份趋势图 |
| **定时任务** | `schedule` / `crontab` | 每日自动更新数据 |
| **数据入库** | `SQLAlchemy` + `PostgreSQL` | 支持复杂查询和分析 |
| **Docker 部署** | `Dockerfile` + `docker-compose` | 一键部署到服务器 |

---

## 6.6 课后练习

1. **数据完整性检查**：编写函数验证抓取的 250 部电影中，排名是否连续（1-250），评分是否在合理范围（0-10）。
2. **增量更新**：修改代码，使其能够检测已有数据，只抓取新增或更新的电影。
3. **多线程加速**：使用 `concurrent.futures.ThreadPoolExecutor` 实现 3 线程并发抓取。
4. **数据分析**：使用 `pandas` 分析抓取数据，找出评分最高的导演、上映年份分布等。

---

## 💡 教程总结

恭喜你完成了《网络爬虫新手指南》的全部 6 章内容！让我们回顾一下你掌握的技能：

| 章节 | 核心能力 |
|:---|:---|
| 第 1 章 | 理解爬虫原理、HTTP 协议与开发者工具 |
| 第 2 章 | 搭建环境、发送请求、User-Agent 伪装 |
| 第 3 章 | BeautifulSoup 解析、CSS 选择器、数据提取 |
| 第 4 章 | CSV/JSON 导出、编码处理、增量写入 |
| 第 5 章 | 反爬对抗、Session 管理、频率控制、代理 |
| 第 6 章 | 工程化架构、模块化设计、完整项目交付 |

你已经从一个"会写脚本的人"成长为"能交付工程级爬虫项目的开发者"。现在，去探索更广阔的数据世界吧！🚀
