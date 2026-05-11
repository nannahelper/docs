# 第 7 章：Docker Compose —— 一键启动多容器应用

> **场景：** 你的应用由 3 个服务组成：Nginx 前端代理、Flask 后端 API、MySQL 数据库。每次部署都要手动创建网络、启动三个容器、配置环境变量……太繁琐了。Docker Compose 让你用一个 YAML 文件定义整个应用栈，一条命令全部启动。

---

## 7.1 什么是 Docker Compose？

!!! example "核心比喻：Docker Compose 就像交响乐总谱"
    一场交响乐有几十种乐器（服务），每种乐器有自己的乐谱（配置）。指挥不需要逐个告诉乐手怎么演奏——他只需要看总谱（docker-compose.yml），一挥指挥棒，所有乐器同时奏响。
    
    Docker Compose = 多容器应用的总谱，`docker compose up` = 指挥棒一挥。

```yaml
# docker-compose.yml —— 整个应用栈的定义
services:
  web:
    build: .
    ports:
      - "5000:5000"
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: secret
```

一条命令启动全部：

```bash
docker compose up -d
```

---

## 7.2 docker-compose.yml 核心语法

### 完整示例

```yaml
version: "3.8"

services:
  # 服务 1：Web 应用
  web:
    build: .                              # 从当前目录的 Dockerfile 构建
    container_name: my-web-app            # 容器名称
    ports:
      - "5000:5000"                       # 端口映射
    environment:                          # 环境变量
      - FLASK_ENV=production
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=${MYSQL_PASSWORD}     # 使用 .env 文件中的变量
    depends_on:                           # 依赖关系
      db:
        condition: service_healthy        # 等待 db 健康检查通过
    volumes:                              # 数据卷
      - ./app:/app                        # Bind Mount（开发用）
    networks:
      - app-network
    restart: unless-stopped               # 重启策略

  # 服务 2：数据库
  db:
    image: mysql:8                        # 使用现成镜像
    container_name: my-mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_DATABASE: myapp
    volumes:
      - mysql-data:/var/lib/mysql         # 命名卷
    networks:
      - app-network
    healthcheck:                          # 健康检查
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # 服务 3：反向代理
  nginx:
    image: nginx:alpine
    container_name: my-nginx-proxy
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - app-network
    depends_on:
      - web

volumes:
  mysql-data:                             # 声明命名卷

networks:
  app-network:                            # 声明自定义网络
    driver: bridge
```

---

## 7.3 核心配置项详解

### build —— 构建镜像

```yaml
services:
  web:
    build: .                    # 当前目录的 Dockerfile

  api:
    build:
      context: ./api            # 构建上下文
      dockerfile: Dockerfile.prod  # 指定 Dockerfile
      args:                     # 构建参数
        - NODE_ENV=production
```

### ports —— 端口映射

```yaml
ports:
  - "80:80"                    # 宿主机:容器
  - "127.0.0.1:8080:80"       # 绑定特定 IP
  - "8080:80/udp"             # UDP 端口
```

### environment —— 环境变量

```yaml
# 方式 1：直接定义
environment:
  - NODE_ENV=production
  - DB_HOST=db

# 方式 2：键值对
environment:
  NODE_ENV: production
  DB_HOST: db

# 方式 3：从 .env 文件读取
environment:
  - DB_PASSWORD=${MYSQL_PASSWORD}
```

### volumes —— 数据卷

```yaml
volumes:
  - mysql-data:/var/lib/mysql           # 命名卷
  - ./data:/data                        # Bind Mount
  - /var/run/docker.sock:/var/run/docker.sock  # 挂载 Docker Socket
```

### depends_on —— 依赖关系

```yaml
depends_on:
  - db                    # 基本依赖（只保证启动顺序）

depends_on:
  db:
    condition: service_healthy  # 等待健康检查通过（Compose v2.1+）
```

### restart —— 重启策略

| 值 | 行为 |
|:---|:---|
| `no` | 不自动重启（默认） |
| `always` | 总是重启 |
| `on-failure` | 仅异常退出时重启 |
| `unless-stopped` | 除非手动停止，否则重启 |

---

## 7.4 Compose 常用命令

```bash
# 启动所有服务（后台）
docker compose up -d

# 启动并重新构建镜像
docker compose up -d --build

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs
docker compose logs -f web     # 跟踪特定服务的日志

# 停止所有服务
docker compose stop

# 停止并删除所有容器、网络
docker compose down

# 停止并删除容器、网络、数据卷
docker compose down -v

# 重启服务
docker compose restart

# 在运行中的服务里执行命令
docker compose exec web bash

# 拉取最新镜像
docker compose pull

# 查看服务使用的资源
docker compose top
```

---

## 7.5 实战：Flask + MySQL + Nginx 全栈

### 项目结构

```
my-fullstack-app/
├── docker-compose.yml
├── .env
├── web/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── nginx/
    └── nginx.conf
```

### docker-compose.yml

```yaml
version: "3.8"

services:
  web:
    build: ./web
    container_name: flask-app
    environment:
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=${MYSQL_PASSWORD}
      - DB_NAME=myapp
    networks:
      - app-network
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: mysql:8
    container_name: mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_DATABASE: myapp
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    networks:
      - app-network
    depends_on:
      - web
    restart: unless-stopped

volumes:
  mysql-data:

networks:
  app-network:
    driver: bridge
```

### .env

```
MYSQL_PASSWORD=my-secret-pw-2024
```

### nginx/nginx.conf

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://flask-app:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 启动

```bash
# 一键启动整个应用栈
docker compose up -d

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f

# 访问 http://localhost
```

---

## 7.6 多环境配置

```bash
# 开发环境
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# 生产环境
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

**docker-compose.dev.yml（覆盖开发配置）：**

```yaml
services:
  web:
    volumes:
      - ./web:/app              # 代码热更新
    environment:
      - FLASK_ENV=development
    ports:
      - "5000:5000"             # 暴露调试端口
```

---

## 要点总结

- [x] Docker Compose 用一个 YAML 文件定义多容器应用
- [x] `services` 定义各个服务，`volumes` 声明命名卷，`networks` 声明网络
- [x] `docker compose up -d` 一键启动所有服务
- [x] `docker compose down` 停止并清理
- [x] Compose 自动创建网络，服务间用服务名通信
- [x] `depends_on` 控制启动顺序，`healthcheck` 确保依赖就绪
- [x] `.env` 文件管理敏感配置

---

## 课后练习

1.  **第一个 Compose** ：将之前的 Flask + MySQL 手动部署改写为 docker-compose.yml。

2.  **添加 Nginx** ：在上面的 Compose 中加入 Nginx 反向代理。

3.  **环境切换** ：创建 `docker-compose.dev.yml` 覆盖文件，实现开发/生产环境切换。

---

**下一章预告：** 所有技能都学完了。第 8 章将带你完成一个综合实战项目——从零部署一个完整的 Web 应用，涵盖镜像构建、数据持久化、网络配置和服务编排。

[继续第 8 章：综合实战 →](08-final-project.md)