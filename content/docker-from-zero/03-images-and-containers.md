# 第 3 章：镜像与容器 —— Docker 的核心"积木"

> **场景：** 你已经运行了 `hello-world` 和 Nginx 容器。但你可能会问：这些镜像是从哪来的？容器停止后数据还在吗？怎么进入容器内部看看？本章将深入镜像与容器的核心操作——这是 Docker 日常使用中最频繁的技能。

---

## 3.1 镜像（Image）—— 容器的"蓝图"

!!! example "核心比喻：镜像就像饼干模具，容器就像饼干"
    你有一个星星形状的饼干模具（镜像）。用这个模具在面团上按一下，就做出一块星星饼干（容器）。同一个模具可以做出无数块一模一样的饼干。模具本身不会被消耗——它只是模板。
    
    镜像 = 只读模板，容器 = 镜像的运行实例。

### 搜索和拉取镜像

```bash
# 在 Docker Hub 上搜索镜像
docker search mysql

# 拉取镜像（默认拉取 latest 标签）
docker pull nginx

# 拉取指定版本的镜像
docker pull nginx:1.25
docker pull python:3.11-slim
docker pull node:18-alpine
```

!!! info "镜像标签（Tag）"
    镜像标签用于区分不同版本。格式为 `镜像名:标签`。
    
    - `nginx:latest` — 最新稳定版
    - `nginx:1.25` — 指定大版本
    - `nginx:1.25.3` — 精确版本
    - `python:3.11-slim` — 精简版（体积更小）
    - `python:3.11-alpine` — 基于 Alpine Linux 的超精简版

### 查看和管理镜像

```bash
# 列出本地所有镜像
docker images

# 或者使用更详细的命令
docker image ls

# 查看镜像详细信息
docker image inspect nginx

# 查看镜像历史（每一层的构建信息）
docker image history nginx

# 删除镜像
docker rmi nginx:latest

# 强制删除（即使有容器在使用）
docker rmi -f nginx:latest

# 清理无用的镜像（悬空镜像）
docker image prune
```

**`docker images` 输出示例：**

```
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
nginx        latest    605c77e624dd   2 weeks ago   141MB
python       3.11-slim 1e6f2e3b3b3b   3 weeks ago   122MB
hello-world  latest    d2c94e258dcb   8 months ago  13.3kB
```

| 列 | 含义 |
|:---|:---|
| REPOSITORY | 镜像仓库名 |
| TAG | 标签（版本） |
| IMAGE ID | 镜像唯一标识 |
| CREATED | 创建时间 |
| SIZE | 镜像大小 |

---

## 3.2 容器（Container）—— 镜像的"实例"

### 创建和启动容器

```bash
# 基本运行（前台模式）
docker run nginx

# 后台运行
docker run -d nginx

# 后台运行 + 端口映射 + 命名
docker run -d -p 8080:80 --name web nginx

# 交互式运行（进入容器内部）
docker run -it ubuntu bash

# 运行后自动删除（用于临时任务）
docker run --rm ubuntu echo "Hello"
```

**`docker run` 常用参数速查：**

| 参数 | 全称 | 作用 |
|:---|:---|:---|
| `-d` | `--detach` | 后台运行 |
| `-p` | `--publish` | 端口映射 `本机:容器` |
| `--name` | | 给容器命名 |
| `-it` | `--interactive --tty` | 交互式终端 |
| `--rm` | | 容器退出后自动删除 |
| `-e` | `--env` | 设置环境变量 |
| `-v` | `--volume` | 挂载数据卷 |
| `--restart` | | 重启策略 |

### 查看容器

```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括已停止的）
docker ps -a

# 只显示容器 ID
docker ps -q

# 查看最新创建的容器
docker ps -l

# 查看容器资源使用情况
docker stats
```

**`docker ps` 输出示例：**

```
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                  NAMES
a1b2c3d4e5f6   nginx     "/docker-entrypoint.…"   5 minutes ago   Up 5 minutes   0.0.0.0:8080->80/tcp   web
```

### 容器生命周期管理

```bash
# 停止容器
docker stop web

# 启动已停止的容器
docker start web

# 重启容器
docker restart web

# 暂停容器（冻结进程）
docker pause web
docker unpause web

# 强制停止（相当于 kill -9）
docker kill web

# 删除已停止的容器
docker rm web

# 强制删除运行中的容器
docker rm -f web

# 删除所有已停止的容器
docker container prune
```

---

## 3.3 进入容器内部

```bash
# 方法 1：在运行中的容器里执行命令
docker exec -it web bash

# 方法 2：以 root 用户进入
docker exec -it -u root web bash

# 方法 3：执行单条命令（不进入交互模式）
docker exec web ls /usr/share/nginx/html
docker exec web cat /etc/nginx/nginx.conf
```

!!! example "核心比喻：docker exec 就像走进集装箱里检查货物"
    集装箱在码头上运行着（容器在运行），你想看看里面的货物是否完好。`docker exec` 就是打开集装箱的门，走进去看看——你可以查看文件、修改配置、安装工具，但注意：容器重启后这些修改会丢失（除非你把它写进镜像）。

---

## 3.4 查看日志和调试

```bash
# 查看容器日志
docker logs web

# 实时跟踪日志（类似 tail -f）
docker logs -f web

# 查看最近 50 行日志
docker logs --tail 50 web

# 查看带时间戳的日志
docker logs -t web

# 查看容器详细信息（IP 地址、挂载点、环境变量等）
docker inspect web

# 查看容器内进程
docker top web

# 查看容器资源使用统计
docker stats web
```

---

## 3.5 文件复制

```bash
# 从宿主机复制文件到容器
docker cp index.html web:/usr/share/nginx/html/

# 从容器复制文件到宿主机
docker cp web:/etc/nginx/nginx.conf ./nginx.conf

# 验证文件已复制
docker exec web ls /usr/share/nginx/html/
```

---

## 3.6 综合练习：操作一个 Nginx 容器

```bash
# 1. 拉取 Nginx 镜像
docker pull nginx:alpine

# 2. 创建并启动容器
docker run -d -p 8080:80 --name my-web nginx:alpine

# 3. 查看容器状态
docker ps

# 4. 查看日志
docker logs my-web

# 5. 进入容器查看默认页面
docker exec my-web cat /usr/share/nginx/html/index.html

# 6. 创建一个自定义页面
echo "<h1>Hello from Docker!</h1>" > index.html

# 7. 复制到容器中
docker cp index.html my-web:/usr/share/nginx/html/

# 8. 验证：浏览器访问 http://localhost:8080

# 9. 查看容器详细信息
docker inspect my-web | grep IPAddress

# 10. 停止并删除容器
docker stop my-web
docker rm my-web
```

---

## 要点总结

- [x] 镜像 = 只读模板，容器 = 镜像的运行实例
- [x] `docker pull` 拉取镜像，`docker images` 查看本地镜像
- [x] `docker run -d -p 8080:80 --name xxx nginx` 启动容器
- [x] `docker ps` 查看运行中的容器，`docker ps -a` 查看所有
- [x] `docker stop/start/restart/rm` 管理容器生命周期
- [x] `docker exec -it xxx bash` 进入容器内部
- [x] `docker logs` 查看日志，`docker cp` 复制文件
- [x] 标签（Tag）区分镜像版本，`latest` 是默认标签

---

## 课后练习

1.  **镜像探索** ：拉取 `python:3.11-slim` 和 `python:3.11-alpine`，对比它们的大小差异。

2.  **容器操作** ：运行一个 Ubuntu 容器，进入内部安装 `curl`，然后退出并删除容器。

3.  **日志调试** ：运行一个 Nginx 容器，访问几次页面，然后用 `docker logs` 查看访问日志。

---

**下一章预告：** 从 Docker Hub 拉取现成的镜像很方便，但真正的威力在于构建自己的镜像。第 4 章将学习 Dockerfile——镜像的"配方说明书"。

[继续第 4 章：Dockerfile →](04-dockerfile.md)