# 第 2 章：环境搭建与第一个请求——开启你的爬虫之旅 (Environment & First Request)

## 📺 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 搭建专业爬虫开发环境，掌握 requests 库核心 API，成功发送并验证第一个 HTTP 请求 |
| **核心比喻** | **装配侦察兵装备 (Equipping the Scout)** |
| **预计时长** | 75 分钟 |
| **关键库/概念** | `requests`, `pip`, 虚拟环境, `Response` 对象, `User-Agent` 伪装 |
| **实践任务** | 编写脚本获取豆瓣电影 Top 250 首页 HTML，并验证响应状态与内容完整性 |

---

在第 1 章中，我们通过 F12 开发者工具"观察"了浏览器如何与豆瓣服务器通信。现在，我们将亲手用 Python 代码复现这一过程。

---

## 2.1 武器库准备：虚拟环境与依赖管理

在开始编码之前，我们必须建立专业的工程习惯。直接使用系统全局 Python 环境安装依赖，会导致不同项目之间的库版本冲突。

!!! info "名词解释：虚拟环境 (Virtual Environment)"
    **虚拟环境** 是 Python 的一个隔离运行环境。每个项目拥有自己独立的 `site-packages` 目录，互不干扰。
    **类比理解**：就像一栋大楼里的不同房间。你在 301 房间（项目 A）里放了一张桌子（安装了 requests v2.28），这不会影响 302 房间（项目 B）里放的沙发（requests v2.31）。

### 🛠️ 创建虚拟环境

=== "Windows"

    1. 打开 **命令提示符** 或 **PowerShell**（按 `Win + R`，输入 `cmd`）。
    2. 进入你的项目目录：
       ```powershell
       cd D:\Projects\web-crawler-tutorial
       ```
    3. 创建虚拟环境：
       ```powershell
       python -m venv venv
       ```
    4. 激活虚拟环境：
       ```powershell
       venv\Scripts\activate
       ```
    5. 激活成功后，命令行前会出现 `(venv)` 标识。

=== "macOS"

    1. 打开 **终端 (Terminal)**。
    2. 进入你的项目目录：
       ```bash
       cd ~/Projects/web-crawler-tutorial
       ```
    3. 创建虚拟环境：
       ```bash
       python3 -m venv venv
       ```
    4. 激活虚拟环境：
       ```bash
       source venv/bin/activate
       ```
    5. 激活成功后，命令行前会出现 `(venv)` 标识。

**验证安装成功：** 命令行前缀出现 `(venv)` 字样，说明虚拟环境已激活 ✅

---

## 2.2 安装核心依赖：requests 库

`requests` 是 Python 生态中最优雅、最人性化的 HTTP 库。它封装了 `urllib3` 的复杂性，提供了直观的 API。

!!! info "名词解释：requests 库"
    **requests** = Python 的 HTTP 客户端库。它让你能够用极简的代码发送 HTTP/1.1 请求，无需手动构造查询字符串或编码 POST 数据。

```bash
pip install requests
```

**验证安装成功：**

```python
# 在终端输入 python 进入交互模式，然后执行：
>>> import requests
>>> print(requests.__version__)
2.31.0  # 输出版本号即表示安装成功
```

!!! tip "作者经验：锁定依赖版本"
    建议在项目根目录创建 `requirements.txt` 文件，记录精确的依赖版本：
    ```
    requests==2.31.0
    beautifulsoup4==4.12.2
    lxml==4.9.3
    pandas==2.1.0
    ```
    这样你的队友可以通过 `pip install -r requirements.txt` 一键复现你的开发环境。

---

## 2.3 发送第一个 GET 请求：获取豆瓣首页 HTML

现在，让我们用 Python 代码模拟浏览器发送请求。

### 📝 基础代码

```python
import requests  # 导入 requests 库，这是我们的"侦察兵"核心装备

# 定义目标 URL —— 豆瓣电影 Top 250 首页
url = "https://movie.douban.com/top250"

# 发送 GET 请求 —— 相当于在浏览器地址栏输入网址并回车
# requests.get() 会返回一个 Response 对象，包含服务器返回的所有信息
response = requests.get(url)

# 打印状态码 —— 200 表示成功，403 表示被拒绝，404 表示页面不存在
print(f"状态码: {response.status_code}")

# 打印响应内容的类型 —— 通常是 text/html
print(f"内容类型: {response.headers['Content-Type']}")

# 打印前 500 个字符，预览 HTML 内容
print(f"响应内容预览:\n{response.text[:500]}")
```

### 🔍 运行结果分析

如果你直接运行上述代码，你很可能会看到：

```
状态码: 418
```

或者：

```
状态码: 200
响应内容预览:
（一片空白或极简的提示信息）
```

**问题出在哪里？** 豆瓣服务器检测到了你的请求来自 Python 脚本，而非真实浏览器。它要么拒绝服务，要么返回了一个"简化版"页面。

---

## 2.4 深入理解 Response 对象

在解决上述问题之前，让我们先彻底理解 `requests.get()` 返回的 `Response` 对象。

| 属性/方法 | 类型 | 说明 | 使用场景 |
|:---|:---|:---|:---|
| `response.status_code` | `int` | HTTP 状态码 | 判断请求是否成功 |
| `response.text` | `str` | 响应体的文本内容（自动解码） | 获取 HTML 源码 |
| `response.content` | `bytes` | 响应体的二进制内容 | 下载图片、PDF 等文件 |
| `response.headers` | `dict` | 响应头字典 | 查看服务器类型、编码等 |
| `response.encoding` | `str` | 响应体的编码方式 | 处理中文乱码问题 |
| `response.json()` | `dict` | 将 JSON 响应解析为 Python 字典 | 处理 API 返回的 JSON 数据 |
| `response.url` | `str` | 最终请求的 URL（可能经过重定向） | 确认是否被重定向 |
| `response.elapsed` | `timedelta` | 请求耗时 | 性能监控 |

!!! tip "作者经验：总是先检查状态码"
    在编写爬虫时，养成习惯：**先检查 `status_code`，再处理 `text`**。如果状态码不是 200，处理响应内容毫无意义。

---

## 2.5 伪装身份：User-Agent 的艺术

### 问题根源

每个 HTTP 请求都会携带一个 `User-Agent` 头。Python 的 `requests` 库默认的 UA 类似于：

```
python-requests/2.31.0
```

这等于直接告诉服务器："我是爬虫，请拒绝我。"

### 解决方案：伪装成浏览器

```python
import requests

url = "https://movie.douban.com/top250"

# 构造请求头 —— 伪装成 Chrome 浏览器
# 这些字段告诉服务器："我是一个正常的 macOS 用户，正在用 Chrome 浏览网页"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 将 headers 参数传入 get 方法
response = requests.get(url, headers=headers)

print(f"状态码: {response.status_code}")

# 检查是否成功获取到包含电影信息的 HTML
if response.status_code == 200 and "肖申克的救赎" in response.text:
    print("✅ 成功获取豆瓣电影 Top 250 页面！")
else:
    print(f"❌ 获取失败，状态码: {response.status_code}")
```

### 📊 常见 User-Agent 对照表

| 平台 | User-Agent 示例 |
|:---|:---|
| **Windows Chrome** | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ... Chrome/120.0.0.0` |
| **macOS Chrome** | `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ... Chrome/120.0.0.0` |
| **iPhone Safari** | `Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 ...` |
| **Android Chrome** | `Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 ... Chrome/120.0.0.0` |

---

## 2.6 健壮性设计：异常处理与超时设置

专业的爬虫代码必须具备容错能力。网络波动、服务器宕机、DNS 解析失败等情况随时可能发生。

```python
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    # timeout=10 表示最多等待 10 秒，超时则抛出 Timeout 异常
    response = requests.get(url, headers=headers, timeout=10)

    # raise_for_status() 会在状态码为 4xx 或 5xx 时自动抛出 HTTPError
    response.raise_for_status()

    # 手动设置编码，防止中文乱码
    response.encoding = response.apparent_encoding

    print(f"✅ 请求成功！状态码: {response.status_code}")
    print(f"页面标题: {response.text.split('<title>')[1].split('</title>')[0]}")

except Timeout:
    print("❌ 请求超时！请检查网络连接或增加超时时间。")
except ConnectionError:
    print("❌ 连接错误！请检查 URL 是否正确，或目标服务器是否在线。")
except RequestException as e:
    print(f"❌ 请求异常: {e}")
```

!!! warning "重要警告：不要使用无限超时"
    永远不要省略 `timeout` 参数。如果不设置超时，你的程序可能会因为等待一个无响应的服务器而永久挂起。

---

## 2.7 实战练习：编写你的第一个爬虫脚本

将本章所学整合为一个完整的脚本 `first_crawler.py`：

```python
"""
第一个爬虫脚本：获取豆瓣电影 Top 250 首页
学习目标：掌握 requests 的基本用法、请求头伪装和异常处理
"""
import requests
from requests.exceptions import RequestException, Timeout


def fetch_douban_top250():
    """获取豆瓣电影 Top 250 首页的 HTML 内容"""
    url = "https://movie.douban.com/top250"

    # 伪装成浏览器 —— 这是爬虫的"身份证"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    try:
        print("正在发送请求...")
        # 发送 GET 请求，设置 10 秒超时
        response = requests.get(url, headers=headers, timeout=10)

        # 检查 HTTP 状态码
        response.raise_for_status()

        # 自动检测编码
        response.encoding = response.apparent_encoding

        print(f"✅ 请求成功！")
        print(f"  状态码: {response.status_code}")
        print(f"  内容长度: {len(response.text)} 字符")
        print(f"  请求耗时: {response.elapsed.total_seconds():.2f} 秒")

        return response.text

    except Timeout:
        print("❌ 请求超时，请检查网络连接。")
    except RequestException as e:
        print(f"❌ 请求失败: {e}")

    return None


if __name__ == "__main__":
    html_content = fetch_douban_top250()

    if html_content:
        # 将 HTML 保存到本地文件，方便后续分析
        with open("douban_top250_page1.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("📁 HTML 已保存到 douban_top250_page1.html")
```

---

## 💡 本章小结

- **虚拟环境** 是项目隔离的最佳实践，每个项目独立管理依赖。
- **requests.get()** 是发送 HTTP 请求的核心方法，返回的 `Response` 对象包含丰富的信息。
- **User-Agent 伪装** 是突破基础反爬的第一道防线。
- **异常处理** 和 **超时设置** 是专业爬虫的必备要素。

**下一章预告：** 我们已经拿到了 HTML 源码，但它还是一堆"乱码"。在第 3 章中，我们将学习如何使用 BeautifulSoup 像外科医生一样精准地从中提取电影名称、评分和导演信息！
