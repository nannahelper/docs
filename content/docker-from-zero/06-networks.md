# 第 6 章：网络管理 —— 让容器之间"对话"

> **场景：** 你的 Web 应用容器需要连接 MySQL 数据库容器。两个容器怎么找到对方？怎么通信？Docker 提供了灵活的网络模型——从简单的端口映射到自定义网络中的服务发现，本章一一讲解。

---

## 6.1 Docker 网络模型概览

!!! example "核心比喻：Docker 网络就像港口里的通信系统"
    港口里有很多集装箱（容器），它们需要互相通信。Docker 网络就是港口里的通信系统：
    
    - **bridge（桥接网络）**：港口内部的电话系统——同一个港口的集装箱可以互相打电话
    - **host（主机网络）**：集装箱直接使用港口办公室的电话——没有隔离，性能最好
    - **none（无网络）**：集装箱没有电话——完全隔离
    - **overlay（覆盖网络）**：跨港口的卫星电话——不同港口的集装箱也能通信

| 网络驱动 | 用途 | 隔离性 |
|:---|:---|:---|
| `bridge` | 默认网络，单机容器通信 | 中等 |
| `host` | 直接使用宿主机网络 | 无 |
| `none` | 完全禁用网络 | 完全 |
| `overlay` | 跨主机容器通信（Swarm） | 高 |

---

## 6.2 默认网络行为

```bash
# 查看所有网络
docker network ls

# 输出示例：
# NETWORK ID     NAME      DRIVER    SCOPE
# abc123def456   bridge    bridge    local
# def456abc789   host      host      local
# ghi789jkl012   none      null      local
```

### 默认 bridge 网络

```bash
# 运行两个容器（默认连接到 bridge 网络）
docker run -d --name container-a alpine sleep 3600
docker run -d --name container-b alpine sleep 3600

# 查看 container-a 的 IP 地址
docker inspect container-a | grep IPAddress

# 进入 container-a，ping container-b（只能用 IP）
docker exec container-a ping 172.17.0.3
```

!!! warning "默认 bridge 网络的限制"
    - 容器之间只能用 **IP 地址** 通信，不能用容器名
    - 没有自动 DNS 解析
    - 不推荐用于生产环境

---

## 6.3 自定义 Bridge 网络 —— 推荐方式

```bash
# 创建自定义网络
docker network create my-network

# 查看网络详情
docker network inspect my-network

# 在自定义网络中运行容器
docker run -d --name web --network my-network nginx
docker run -d --name db --network my-network \
  -e MYSQL_ROOT_PASSWORD=secret mysql:8

# 验证：容器之间可以用容器名互相访问！
docker exec web ping db
# PING db (172.18.0.3): 56 data bytes
# 64 bytes from 172.18.0.3: seq=0 ttl=64 time=0.123 ms
```

!!! tip "自定义网络的优势"
    -  **自动 DNS 解析** ：容器之间可以用容器名互相访问
    -  **更好的隔离** ：只有同一网络的容器才能通信
    -  **动态管理** ：可以随时将容器加入或移出网络

---

## 6.4 网络操作命令

```bash
# 创建网络
docker network create --driver bridge my-net

# 创建带子网指定的网络
docker network create \
  --driver bridge \
  --subnet=192.168.100.0/24 \
  --gateway=192.168.100.1 \
  my-net

# 将运行中的容器连接到网络
docker network connect my-net web

# 将容器从网络中断开
docker network disconnect my-net web

# 查看网络详情（包含连接的容器）
docker network inspect my-net

# 删除网络（必须没有容器在使用）
docker network rm my-net

# 清理所有未使用的网络
docker network prune
```

---

## 6.5 实战：Web 应用 + 数据库通信

```bash
# 1. 创建自定义网络
docker network create app-network

# 2. 启动 MySQL 容器
docker run -d \
  --name mysql-db \
  --network app-network \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=myapp \
  mysql:8

# 3. 启动 Web 应用容器
docker run -d \
  --name web-app \
  --network app-network \
  -p 5000:5000 \
  -e DB_HOST=mysql-db \
  -e DB_USER=root \
  -e DB_PASSWORD=secret \
  -e DB_NAME=myapp \
  my-flask-app:v1

# 4. 验证通信
docker exec web-app ping mysql-db
# 成功！容器名自动解析为 IP 地址

# 5. 查看网络拓扑
docker network inspect app-network
```

**网络拓扑图：**

```
┌─────────────────────────────────────────────┐
│              app-network (自定义网络)          │
│                                              │
│  ┌──────────────┐    ┌──────────────┐        │
│  │   web-app    │───▶│   mysql-db   │        │
│  │  (Flask)     │    │   (MySQL)    │        │
│  │  172.18.0.2  │    │  172.18.0.3  │        │
│  └──────┬───────┘    └──────────────┘        │
│         │ 5000                                │
└─────────┼────────────────────────────────────┘
          │
    ┌─────▼──────┐
    │  宿主机     │
    │ localhost  │
    │   :5000    │
    └────────────┘
```

---

## 6.6 Host 网络和 None 网络

```bash
# Host 网络：容器直接使用宿主机网络（无隔离）
docker run --rm --network host nginx
# 容器直接监听宿主机的 80 端口

# None 网络：完全禁用网络
docker run --rm --network none alpine ip addr
# 只有 lo 回环接口，无法访问外部网络
```

---

## 6.7 端口映射详解

```bash
# 基本格式：宿主机端口:容器端口
docker run -d -p 8080:80 nginx

# 指定宿主机 IP
docker run -d -p 127.0.0.1:8080:80 nginx

# 随机宿主机端口
docker run -d -P nginx

# 映射 UDP 端口
docker run -d -p 8080:80/udp nginx

# 映射端口范围
docker run -d -p 8080-8090:80 nginx

# 查看端口映射
docker port web
# 80/tcp -> 0.0.0.0:8080
```

---

## 要点总结

- [x] Docker 默认 bridge 网络只能用 IP 通信
- [x] 自定义 bridge 网络支持容器名 DNS 解析
- [x] `docker network create` 创建网络
- [x] `--network` 指定容器加入的网络
- [x] `docker network connect/disconnect` 动态管理网络连接
- [x] Host 网络无隔离，None 网络完全禁用
- [x] `-p 宿主机:容器` 进行端口映射

---

## 课后练习

1.  **网络实验** ：创建自定义网络，运行两个 Alpine 容器，验证它们可以用容器名互相 ping 通。

2.  **Web + DB** ：在自定义网络中运行一个 Web 应用容器和一个 MySQL 容器，验证 Web 应用能通过容器名连接数据库。

3.  **网络隔离** ：在两个不同的自定义网络中运行容器，验证跨网络无法通信。

---

**下一章预告：** 手动创建网络、逐个启动容器太麻烦了。有没有办法一条命令启动整个应用栈？第 7 章将学习 Docker Compose——多容器应用的"一键部署"。

[继续第 7 章：Docker Compose →](07-docker-compose.md)