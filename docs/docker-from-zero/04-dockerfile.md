# 第 4 章：Dockerfile —— 定制你的专属镜像

> **场景：** 你写了一个 Python Web 应用，想把它打包成 Docker 镜像。你需要告诉 Docker：基于什么基础镜像、安装哪些依赖、复制哪些文件、怎么启动应用。Dockerfile 就是这份"配方说明书"——Docker 按照它一步步构建出你的专属镜像。

---

## 4.1 什么是 Dockerfile？

!!! example "核心比喻：Dockerfile 就像乐高积木的搭建说明书"
    你买了一盒乐高，里面有一本搭建说明书：第一步拼底座，第二步装轮子，第三步装车身……每一步都在前一步的基础上添加新零件。
    
    Dockerfile 就是镜像的搭建说明书——每一行指令在基础镜像上添加一层新内容，最终构建出完整的应用镜像。

```dockerfile
# 一个最简单的 Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask
CMD ["python", "app.py"]
```

---

## 4.2 Dockerfile 核心指令

### FROM —— 指定基础镜像

```dockerfile
# 基于官方 Python 镜像
FROM python:3.11-slim

# 基于 Alpine（超小体积）
FROM python:3.11-alpine

# 基于特定 digest（精确锁定版本）
FROM python:3.11-slim@sha256:abc123...

# 从头开始（不基于任何镜像，用于构建极简镜像）
FROM scratch
```

!!! tip "选择基础镜像的原则"
    - **官方镜像优先**：`python`、`node`、`nginx`、`mysql` 等
    - **slim 版本**：去掉非必要工具，体积更小
    - **alpine 版本**：基于 Alpine Linux，体积最小（但可能缺少某些库）
    - **锁定版本**：不要用 `latest`，用具体版本号

### WORKDIR —— 设置工作目录

```dockerfile
WORKDIR /app
```

相当于在容器里执行了 `mkdir -p /app && cd /app`。后续的 `COPY`、`RUN` 等指令都在这个目录下执行。

### COPY —— 复制文件

```dockerfile
# 将宿主机当前目录的所有文件复制到容器的 /app 目录
COPY . /app

# 只复制特定文件
COPY requirements.txt /app/
COPY src/ /app/src/

# 使用 .dockerignore 排除不需要的文件
```

!!! warning "COPY vs ADD"
    - `COPY`：简单复制文件（推荐）
    - `ADD`：复制文件 + 自动解压 tar + 支持 URL（不推荐，行为不透明）
    - 除非需要自动解压功能，否则始终使用 `COPY`

### RUN —— 执行命令

```dockerfile
# 安装系统依赖
RUN apt-get update && apt-get install -y gcc

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 合并多条命令减少镜像层数
RUN apt-get update && \
    apt-get install -y gcc curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

!!! tip "RUN 最佳实践"
    - 多条命令用 `&&` 连接，减少镜像层数
    - 安装完清理缓存（`apt-get clean`、`rm -rf /var/lib/apt/lists/*`）
    - pip 安装用 `--no-cache-dir` 减小体积

### CMD vs ENTRYPOINT —— 容器启动命令

```dockerfile
# CMD：定义默认的启动命令（可被 docker run 后面的命令覆盖）
CMD ["python", "app.py"]

# ENTRYPOINT：定义容器的主命令（不会被覆盖，docker run 后面的参数作为追加参数）
ENTRYPOINT ["python", "app.py"]

# 组合使用：ENTRYPOINT 定义主程序，CMD 定义默认参数
ENTRYPOINT ["python"]
CMD ["app.py"]
```

| 对比 | CMD | ENTRYPOINT |
|:---|:---|:---|
| 可被覆盖 | ✅ `docker run image other_cmd` | ❌（参数追加而非覆盖） |
| 使用场景 | 默认行为，允许用户覆盖 | 容器就是为运行这个程序设计的 |
| 组合 | `ENTRYPOINT` + `CMD` = 主程序 + 默认参数 |

### EXPOSE —— 声明端口

```dockerfile
# 声明容器监听的端口（仅文档作用，实际端口映射仍需 -p 参数）
EXPOSE 5000
```

### ENV —— 设置环境变量

```dockerfile
# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
```

---

## 4.3 实战：构建一个 Python Web 应用镜像

### 项目结构

```
my-flask-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

### app.py

```python
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = os.uname().nodename
    return f'<h1>Hello from Docker!</h1><p>Container: {hostname}</p>'

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### requirements.txt

```
flask==3.0.0
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["python", "app.py"]
```

### .dockerignore

```
__pycache__
*.pyc
*.pyo
.env
.git
.gitignore
README.md
Dockerfile
```

### 构建镜像

```bash
# 构建镜像（-t 指定名称和标签）
docker build -t my-flask-app:v1 .

# 构建时指定 Dockerfile 路径
docker build -f Dockerfile.prod -t my-flask-app:prod .

# 不使用缓存构建（确保使用最新依赖）
docker build --no-cache -t my-flask-app:v1 .
```

**构建过程输出：**

```
[+] Building 15.2s (10/10) FINISHED
 => [1/5] FROM python:3.11-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY . .
 => exporting to image
 => => naming to docker.io/library/my-flask-app:v1
```

### 运行容器

```bash
# 启动容器
docker run -d -p 5000:5000 --name flask-app my-flask-app:v1

# 验证
curl http://localhost:5000
curl http://localhost:5000/health
```

---

## 4.4 镜像分层与缓存

!!! example "核心比喻：镜像分层就像千层蛋糕"
    每一层是蛋糕的一层薄片。如果你只改了最上面的奶油装饰，不需要重做整个蛋糕——只需要重做奶油层。Docker 的构建缓存也是这样：只有发生变化的层和它上面的层需要重新构建。

```dockerfile
# 优化前：每次代码改动都要重装依赖
FROM python:3.11-slim
WORKDIR /app
COPY . .                          # 代码经常变
RUN pip install -r requirements.txt  # 依赖不常变，但每次都要重装！

# 优化后：利用缓存，依赖不常变就不重装
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .           # 依赖文件不常变
RUN pip install -r requirements.txt  # 这层会被缓存
COPY . .                          # 代码经常变，只重建这层
```

---

## 4.5 多阶段构建

多阶段构建让你在一个 Dockerfile 中使用多个 `FROM`，最终只保留需要的文件：

```dockerfile
# 阶段 1：构建阶段
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp .

# 阶段 2：运行阶段（只复制编译好的二进制文件）
FROM alpine:3.19
WORKDIR /app
COPY --from=builder /app/myapp .
CMD ["./myapp"]
```

**效果：** 最终镜像只有几 MB（只包含二进制文件），而不是几百 MB（包含整个 Go 编译工具链）。

---

## 4.6 推送镜像到 Docker Hub

```bash
# 1. 登录 Docker Hub
docker login

# 2. 给镜像打标签（格式：用户名/镜像名:标签）
docker tag my-flask-app:v1 your-username/my-flask-app:v1

# 3. 推送到 Docker Hub
docker push your-username/my-flask-app:v1

# 4. 其他人可以拉取你的镜像
docker pull your-username/my-flask-app:v1
```

---

## 要点总结

- [x] Dockerfile 是镜像的"配方说明书"
- [x] `FROM` 指定基础镜像，`WORKDIR` 设置工作目录
- [x] `COPY` 复制文件，`RUN` 执行命令
- [x] `CMD` 定义默认启动命令，`ENTRYPOINT` 定义主命令
- [x] 利用缓存优化构建速度：先复制不常变的文件
- [x] 多阶段构建减小最终镜像体积
- [x] `.dockerignore` 排除不需要的文件
- [x] `docker build -t name:tag .` 构建镜像

---

## 课后练习

1.  **第一个 Dockerfile** ：为你自己的一个项目（或上面的 Flask 示例）编写 Dockerfile 并构建镜像。

2.  **缓存实验** ：修改 `app.py` 后重新构建，观察哪些层使用了缓存。

3.  **多阶段构建** ：尝试用多阶段构建一个静态网站（构建阶段用 Node.js 编译，运行阶段用 Nginx 托管）。

---

**下一章预告：** 容器删了，里面的数据就没了。数据库、用户上传的文件、日志——这些数据需要"活"在容器之外。第 5 章将学习数据卷和数据持久化。

[继续第 5 章：数据管理 →](05-volumes.md)