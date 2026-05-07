# 第 5 章：应对反爬挑战——成为"伪装大师" (Anti-Scraping Countermeasures)

## 📺 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 识别常见反爬机制，掌握请求头伪装、Cookie 管理、频率控制与 IP 代理等核心对抗策略 |
| **核心比喻** | **伪装大师 (Master of Disguise)** |
| **预计时长** | 75 分钟 |
| **关键概念** | 请求头伪装, Session 维持, 随机延时, IP 代理池, 验证码识别 |
| **实践任务** | 为爬虫添加完整的反反爬策略，确保稳定抓取豆瓣电影数据 |

---

在前几章中，我们通过简单的 `User-Agent` 伪装成功获取了数据。但在真实的生产环境中，网站的反爬系统远比这复杂。本章将带你深入理解反爬虫的攻防博弈。

---

## 5.1 反爬虫的"武器库"：网站如何识别爬虫？

在制定对抗策略之前，我们必须先理解"敌人"的检测手段：

| 检测维度 | 检测方式 | 触发条件示例 |
|:---|:---|:---|
| **请求头检测** | 检查 `User-Agent`, `Referer`, `Accept-Language` | 缺失或异常的 UA 直接拒绝 |
| **频率检测** | 统计单位时间内的请求次数 | 1 秒内请求超过 5 次 |
| **行为检测** | 分析鼠标轨迹、页面停留时间 | 0 秒停留 + 无鼠标移动 |
| **IP 检测** | 统计单 IP 的请求总量 | 同一 IP 24 小时内请求超过 1000 次 |
| **Cookie/Session 检测** | 验证登录态和会话连续性 | 未登录访问需登录页面 |
| **验证码** | 图形验证码、滑块验证 | 触发频率阈值后弹出 |

!!! info "名词解释：反爬虫 (Anti-Scraping)"
    **反爬虫** 是网站为了保护自身数据不被批量抓取而采取的一系列技术手段。它不是一个单一的开关，而是一套多层次的防御体系。

---

## 5.2 请求头伪装：不止是 User-Agent

在第 2 章中，我们只伪装了 `User-Agent`。但在专业场景中，你需要构造一个完整的"浏览器身份"。

### 完整的请求头构造

```python
import requests

url = "https://movie.douban.com/top250"

# 构造一个"完整"的浏览器请求头
# 每一个字段都在向服务器传递"我是真人"的信号
headers = {
    # 浏览器身份标识
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    # 告诉服务器我能接受什么类型的内容
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",

    # 我能接受的语言（中文优先）
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",

    # 我能接受的编码方式
    "Accept-Encoding": "gzip, deflate, br",

    # 保持连接（HTTP/1.1 特性）
    "Connection": "keep-alive",

    # 告诉服务器我从哪里来（模拟从搜索引擎跳转）
    "Referer": "https://www.google.com/",

    # 缓存控制
    "Cache-Control": "max-age=0",

    # 升级不安全请求
    "Upgrade-Insecure-Requests": "1",
}

response = requests.get(url, headers=headers, timeout=10)
print(f"状态码: {response.status_code}")
```

### Referer 的妙用

`Referer` 告诉服务器"我是从哪个页面点进来的"。某些网站会检查这个字段，拒绝直接访问（防盗链）。

```python
# 场景：抓取图片时，模拟从豆瓣电影页面点击进入
headers = {
    "User-Agent": "...",
    "Referer": "https://movie.douban.com/top250",  # 假装从电影列表页跳转
}
```

---

## 5.3 Session 维持与 Cookie 管理

HTTP 是无状态协议。当你需要抓取"登录后可见"的内容时，必须维持会话状态。

### 使用 requests.Session()

```python
import requests

# 创建 Session 对象 —— 它像一个"浏览器实例"
# Session 会自动保存和携带 Cookie，维持登录状态
session = requests.Session()

# 设置默认请求头（Session 内的所有请求都会携带）
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

# 第一步：访问首页，获取初始 Cookie
response1 = session.get("https://movie.douban.com/top250", timeout=10)
print(f"首页状态码: {response1.status_code}")
print(f"当前 Cookie: {session.cookies.get_dict()}")

# 第二步：使用同一个 Session 访问其他页面
# Cookie 会自动携带，无需手动管理
response2 = session.get("https://movie.douban.com/top250?start=25", timeout=10)
print(f"第二页状态码: {response2.status_code}")
```

!!! tip "作者经验：Cookie 的时效性"
    Cookie 通常有过期时间。如果你的爬虫需要长时间运行，建议：
    1. 定期检查响应中是否包含新的 `Set-Cookie` 头。
    2. 如果遇到 403 或重定向到登录页，说明 Cookie 已失效，需要重新获取。

---

## 5.4 频率控制：让你的爬虫更像"人"

人类浏览网页的速度是有限的。如果你的爬虫在 0.1 秒内请求了 10 个页面，任何反爬系统都会立刻识别。

### 随机延时策略

```python
import time
import random

def human_like_delay():
    """模拟人类的浏览间隔：1 到 3 秒之间的随机延时"""
    delay = random.uniform(1.0, 3.0)
    print(f"⏳ 等待 {delay:.1f} 秒...")
    time.sleep(delay)

# 在每次请求之间调用
for page in range(0, 250, 25):
    url = f"https://movie.douban.com/top250?start={page}"
    response = session.get(url, headers=headers, timeout=10)
    # ... 处理数据 ...
    human_like_delay()  # 模拟人类浏览节奏
```

### 指数退避策略（遇到限制时）

当服务器返回 429（Too Many Requests）或 503（Service Unavailable）时，说明你的请求频率过高。此时应该"退避"：

```python
import time

def fetch_with_backoff(url, session, headers, max_retries=5):
    """带指数退避的请求函数"""
    for attempt in range(max_retries):
        response = session.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response

        if response.status_code in (429, 503):
            # 指数退避：2^attempt 秒
            wait_time = 2 ** attempt
            print(f"⚠️ 状态码 {response.status_code}，第 {attempt + 1} 次重试，等待 {wait_time} 秒...")
            time.sleep(wait_time)
        else:
            response.raise_for_status()

    raise Exception(f"请求失败，已重试 {max_retries} 次: {url}")
```

---

## 5.5 IP 代理：隐藏你的真实身份

当你的爬虫需要大规模抓取时，单一 IP 很容易被封锁。代理服务器可以帮你"换脸"。

### 代理的基本使用

```python
import requests

# 代理格式：{"协议": "协议://IP:端口"}
proxies = {
    "http": "http://127.0.0.1:7890",   # HTTP 代理
    "https": "http://127.0.0.1:7890",  # HTTPS 代理
}

response = requests.get(
    "https://movie.douban.com/top250",
    headers=headers,
    proxies=proxies,
    timeout=10
)
```

### 代理池轮换策略

```python
import random

# 代理池 —— 在实际项目中，这些代理应从专业代理服务商获取
proxy_pool = [
    {"http": "http://proxy1.example.com:8080", "https": "http://proxy1.example.com:8080"},
    {"http": "http://proxy2.example.com:8080", "https": "http://proxy2.example.com:8080"},
    {"http": "http://proxy3.example.com:8080", "https": "http://proxy3.example.com:8080"},
]

def get_random_proxy():
    """从代理池中随机选择一个代理"""
    return random.choice(proxy_pool)

# 每次请求使用不同的代理
for page in range(0, 250, 25):
    url = f"https://movie.douban.com/top250?start={page}"
    proxy = get_random_proxy()
    try:
        response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
        # ... 处理数据 ...
    except requests.exceptions.ProxyError:
        print(f"❌ 代理 {proxy} 连接失败，切换到下一个代理")
        continue
```

!!! warning "重要警告：代理的合法使用"
    使用代理抓取数据时，请确保：
    1. 代理来源合法（不使用盗用或未授权的代理）。
    2. 抓取频率仍然受控（代理不是"无限加速"的许可证）。
    3. 遵守目标网站的 `robots.txt` 和服务条款。

---

## 5.6 验证码处理策略

当你的爬虫触发了验证码，说明反爬系统已经高度警觉。

### 处理策略层级

| 策略 | 说明 | 适用场景 |
|:---|:---|:---|
| **降低频率** | 增加延时，减少并发 | 轻度触发 |
| **更换 IP** | 切换到新的代理 IP | 中度触发 |
| **手动打码** | 人工输入验证码 | 偶尔触发 |
| **打码平台** | 调用第三方 API 自动识别 | 大规模触发（需付费） |
| **放弃该请求** | 跳过当前页面，继续下一个 | 非关键数据 |

```python
def handle_captcha(response):
    """检测并处理验证码"""
    # 常见的验证码特征
    captcha_indicators = ["captcha", "验证码", "verify", "challenge"]

    if any(indicator in response.text.lower() for indicator in captcha_indicators):
        print("⚠️ 检测到验证码！建议：")
        print("   1. 增加请求间隔（当前延时 × 2）")
        print("   2. 更换代理 IP")
        print("   3. 暂停抓取 5-10 分钟后重试")
        return True
    return False
```

---

## 5.7 综合实战：构建"反反爬"爬虫类

将本章所有策略整合为一个健壮的爬虫类：

```python
"""
带反反爬策略的爬虫基类
集成了请求头伪装、Session 维持、随机延时、指数退避和代理轮换
"""
import time
import random
import requests
from requests.exceptions import RequestException


class AntiScrapingCrawler:
    """具备反反爬能力的爬虫基类"""

    def __init__(self, proxy_pool=None):
        # 创建持久化 Session
        self.session = requests.Session()

        # 设置完整的浏览器伪装头
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
        })

        # 代理池
        self.proxy_pool = proxy_pool or []

        # 基础延时范围（秒）
        self.min_delay = 1.0
        self.max_delay = 3.0

    def _get_proxy(self):
        """获取随机代理"""
        if self.proxy_pool:
            return random.choice(self.proxy_pool)
        return None

    def _human_delay(self):
        """模拟人类浏览间隔"""
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)

    def _backoff_delay(self, attempt):
        """指数退避延时"""
        wait = 2 ** attempt
        time.sleep(wait)

    def fetch(self, url, max_retries=3):
        """带完整反反爬策略的请求方法"""
        for attempt in range(max_retries):
            try:
                proxy = self._get_proxy()
                response = self.session.get(
                    url,
                    proxies=proxy,
                    timeout=15
                )

                # 成功 —— 返回响应
                if response.status_code == 200:
                    self._human_delay()  # 成功后也要延时
                    return response

                # 频率限制 —— 指数退避
                if response.status_code in (429, 503):
                    print(f"⚠️ 触发频率限制 (状态码 {response.status_code})，退避重试...")
                    self._backoff_delay(attempt)
                    continue

                # 禁止访问 —— 可能需要更换代理
                if response.status_code == 403:
                    print(f"⚠️ 访问被拒绝 (403)，尝试更换代理...")
                    continue

                # 其他错误
                response.raise_for_status()

            except RequestException as e:
                print(f"❌ 请求异常 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    self._backoff_delay(attempt)

        raise Exception(f"请求最终失败: {url}")


# 使用示例
if __name__ == "__main__":
    crawler = AntiScrapingCrawler()
    try:
        response = crawler.fetch("https://movie.douban.com/top250")
        print(f"✅ 请求成功！状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ {e}")
```

---

## 💡 本章小结

- **请求头伪装** 是基础，需要构造完整的浏览器身份（UA + Accept + Referer + Cookie）。
- **Session** 自动管理 Cookie，是维持登录态的必备工具。
- **随机延时** 和 **指数退避** 是频率控制的核心策略。
- **代理池** 用于大规模抓取时的 IP 轮换。
- **验证码** 是反爬的最后一道防线，优先通过降低频率和更换 IP 来避免触发。

**下一章预告：** 在最后一章中，我们将整合前 5 章的所有知识，编写一个完整的爬虫项目——自动抓取豆瓣电影 Top 250 的全部 250 部电影数据！
