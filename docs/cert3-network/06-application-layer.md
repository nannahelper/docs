# 第 6 章：应用层 —— 互联网的"门面"

> **场景：** 你在浏览器输入 `https://www.example.com`，页面瞬间出现。这背后涉及 DNS 域名解析、HTTP 请求响应、可能的 FTP 文件下载、SMTP 邮件发送……应用层是我们每天直接使用的网络服务。

---

## 6.1 DNS —— 互联网的"电话簿"

!!! example "核心比喻：DNS 就是 114 查号台"
    你记得"肯德基"这个名字，但不知道它的电话号码。你打 114："帮我查一下肯德基的电话。"114 回复："010-12345678。"
    
    DNS 做同样的事——你把域名 `www.baidu.com` 告诉 DNS 服务器，它返回 IP 地址 `110.242.68.66`。

### 域名结构

```
                        根域 (.)
                         │
        ┌────────────────┼────────────────┐
       com              cn               org
        │                │
    ┌───┴───┐        ┌───┴───┐
  baidu   google   edu    gov
    │                │
  www              tsinghua
                     │
                   www
```

完整域名：`www.tsinghua.edu.cn.`（最后的点代表根域，通常省略）

### DNS 解析过程

```
用户输入 www.example.com
        │
        ▼
┌──────────────┐
│  本地 DNS 缓存  │ ← 先查浏览器缓存、系统 hosts 文件
└──────┬───────┘
       │ 未命中
       ▼
┌──────────────┐
│  本地 DNS 服务器 │ ← 由 ISP 提供（如 114.114.114.114）
└──────┬───────┘
       │ 递归查询
       ▼
┌──────────────┐
│   根域名服务器  │ → 返回 .com 顶级域名服务器地址
└──────┬───────┘
       ▼
┌──────────────┐
│ .com 顶级域服务器│ → 返回 example.com 权威服务器地址
└──────┬───────┘
       ▼
┌──────────────┐
│ 权威域名服务器  │ → 返回 www.example.com 的 IP 地址
└──────────────┘
```

| 查询方式 | 说明 |
|:---|:---|
| 递归查询 | 客户端要求 DNS 服务器给出最终结果（查不到就报错） |
| 迭代查询 | DNS 服务器返回"我不知道，但你可以去问 XXX" |

### 常见 DNS 记录类型

| 类型 | 全称 | 作用 | 示例 |
|:---|:---|:---|:---|
| **A** | Address | 域名 → IPv4 地址 | `example.com → 93.184.216.34` |
| **AAAA** | IPv6 Address | 域名 → IPv6 地址 | `example.com → 2606:2800:220:1:248:1893:25c8:1946` |
| **CNAME** | Canonical Name | 别名 → 规范域名 | `www.example.com → example.com` |
| **MX** | Mail Exchange | 邮件服务器地址 | `example.com → mail.example.com` |
| **NS** | Name Server | 该域的权威 DNS 服务器 | `example.com → ns1.example.com` |

---

## 6.2 HTTP —— 网页传输协议

!!! example "核心比喻：HTTP 就像餐厅的点餐流程"
    你（浏览器）走进餐厅，服务员（Web 服务器）递上菜单。你说"我要一份牛排"（HTTP 请求），服务员去厨房取来牛排（HTTP 响应）。
    
    HTTP 是无状态的——服务员不会记住你上次点了什么，每次点餐都是全新的对话。

### HTTP 请求报文

```
GET /index.html HTTP/1.1          ← 请求行：方法 + URL + 版本
Host: www.example.com             ← 请求头
User-Agent: Mozilla/5.0
Accept: text/html
Accept-Language: zh-CN
Connection: keep-alive
                                  ← 空行（头部结束标志）
（请求体，GET 请求通常为空）
```

### HTTP 响应报文

```
HTTP/1.1 200 OK                   ← 状态行：版本 + 状态码 + 描述
Date: Mon, 11 May 2026 08:00:00 GMT
Content-Type: text/html
Content-Length: 1234
Server: nginx/1.18.0
                                  ← 空行
<!DOCTYPE html>                   ← 响应体
<html>...</html>
```

### HTTP 请求方法

| 方法 | 含义 | 幂等性 | 安全性 |
|:---|:---|:---:|:---:|
| **GET** | 获取资源 | ✅ | ✅ |
| **POST** | 提交数据（创建资源） | ❌ | ❌ |
| **PUT** | 更新资源（完整替换） | ✅ | ❌ |
| **PATCH** | 更新资源（部分修改） | ❌ | ❌ |
| **DELETE** | 删除资源 | ✅ | ❌ |
| **HEAD** | 获取响应头（不含体） | ✅ | ✅ |

### HTTP 状态码

| 范围 | 类别 | 常见状态码 |
|:---|:---|:---|
| **1xx** | 信息 | `100 Continue` |
| **2xx** | 成功 | `200 OK`、`201 Created`、`204 No Content` |
| **3xx** | 重定向 | `301 永久重定向`、`302 临时重定向`、`304 Not Modified` |
| **4xx** | 客户端错误 | `400 Bad Request`、`401 Unauthorized`、`403 Forbidden`、`404 Not Found` |
| **5xx** | 服务器错误 | `500 Internal Server Error`、`502 Bad Gateway`、`503 Service Unavailable` |

---

## 6.3 HTTPS —— HTTP 的安全版

HTTPS = HTTP + SSL/TLS 加密层

| 对比维度 | HTTP | HTTPS |
|:---|:---|:---|
| 加密 | 明文传输 | TLS 加密 |
| 端口 | 80 | 443 |
| 证书 | 不需要 | 需要 CA 签发的 SSL 证书 |
| URL 前缀 | `http://` | `https://` |
| 安全性 | 可被窃听、篡改 | 防窃听、防篡改、身份认证 |

---

## 6.4 FTP —— 文件传输协议

| 特征 | 说明 |
|:---|:---|
| 端口 | 控制连接 21，数据连接 20 |
| 模式 | 主动模式（PORT）和被动模式（PASV） |
| 认证 | 支持匿名登录和用户名/密码认证 |
| 传输模式 | ASCII 模式和二进制模式 |

---

## 6.5 电子邮件协议

| 协议 | 全称 | 端口 | 作用 |
|:---|:---|:---|:---|
| **SMTP** | Simple Mail Transfer Protocol | 25/587 | 发送邮件（客户端→服务器，服务器→服务器） |
| **POP3** | Post Office Protocol v3 | 110/995 | 从服务器下载邮件到本地 |
| **IMAP** | Internet Message Access Protocol | 143/993 | 在服务器上管理邮件（多设备同步） |

---

## 6.6 常见题型

**例题 1：** DNS 服务器中，将域名映射为 IPv4 地址的记录类型是（ ）。

A. CNAME　　B. MX　　C. A　　D. NS

??? answer "查看答案"
    **答案：C**
    
    A（Address）记录将域名映射到 IPv4 地址。CNAME 是别名记录，MX 是邮件交换记录，NS 是域名服务器记录。

**例题 2：** HTTP 状态码 404 表示（ ）。

A. 服务器内部错误　　B. 请求的资源未找到　　C. 请求未授权　　D. 请求成功

??? answer "查看答案"
    **答案：B**
    
    404 Not Found 表示服务器找不到请求的资源。500 是服务器内部错误，401 是未授权，200 是请求成功。

**例题 3：** 以下协议中，用于发送电子邮件的是（ ）。

A. POP3　　B. IMAP　　C. SMTP　　D. FTP

??? answer "查看答案"
    **答案：C**
    
    SMTP（Simple Mail Transfer Protocol）用于发送邮件。POP3 和 IMAP 用于接收邮件，FTP 用于文件传输。

---

## 要点总结

- [x] DNS 将域名解析为 IP 地址，常用记录类型：A、AAAA、CNAME、MX、NS
- [x] HTTP 是无状态的应用层协议，基于请求-响应模型
- [x] HTTP 状态码：2xx 成功、3xx 重定向、4xx 客户端错误、5xx 服务器错误
- [x] HTTPS = HTTP + TLS 加密，端口 443
- [x] 电子邮件：SMTP 发邮件，POP3/IMAP 收邮件

---

## 课后练习

1.  **DNS 分析** ：描述从输入 `www.baidu.com` 到浏览器显示页面的完整 DNS 解析过程。

2.  **状态码判断** ：以下场景分别返回什么 HTTP 状态码？
    - 用户访问一个不存在的页面
    - 网站永久迁移到新域名
    - 用户未登录访问需要登录的页面

3.  **思考题** ：HTTP 协议的默认端口号是（ ），HTTPS 的默认端口号是（ ）。

---

**下一章预告：** 应用层之上，我们还需要了解局域网技术（以太网、VLAN、Wi-Fi）——这些是我们日常接触最多的网络形态。第 7 章见。

[继续第 7 章：局域网与无线网络 →](07-lan-and-wireless.md)