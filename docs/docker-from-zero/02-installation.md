# 第 2 章：环境搭建 —— 安装 Docker 并运行第一个容器

> **场景：** 你已经理解了 Docker 的价值。现在要做的第一件事就是把 Docker 装到你的电脑上，然后运行那个经典的 `hello-world` 容器——这是每个 Docker 新手的"入门仪式"。

---

## 2.1 安装 Docker

!!! example "核心比喻：安装 Docker 就像在港口安装一台吊车"
    你要开始装卸集装箱了，首先得在港口安装一台吊车（Docker Engine）。不同操作系统就像不同的港口地形——Windows 港口、Mac 港口、Linux 港口——安装方式略有不同，但吊车的操作方式完全一样。

### Windows 安装

=== "Windows 10/11（推荐 WSL2）"

    1. **启用 WSL2**（Windows Subsystem for Linux）：
    
        以管理员身份打开 PowerShell，运行：
    
        ```powershell
        wsl --install
        ```
    
        安装完成后 **重启电脑**。
    
    2. **下载 Docker Desktop**：
    
        访问 [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)，下载 Windows 版本。
    
    3. **安装 Docker Desktop**：
    
        双击安装包，按照向导完成安装。确保勾选 **"Use WSL 2 instead of Hyper-V"**。
    
    4. **启动 Docker Desktop**：
    
        安装完成后，从开始菜单启动 Docker Desktop。首次启动可能需要几分钟。
    
    5. **验证安装**：
    
        打开 PowerShell 或命令提示符，输入：
    
        ```cmd
        docker --version
        docker run hello-world
        ```

=== "Windows（旧版，使用 Hyper-V）"

    1. 下载 Docker Desktop 安装包
    2. 安装时选择 Hyper-V 后端
    3. 在 BIOS 中启用虚拟化支持（Intel VT-x 或 AMD-V）

!!! warning "Windows 注意事项"
    - Docker Desktop 需要 Windows 10 专业版/企业版/教育版（或 Windows 11）
    - 如果使用 Windows 10 家庭版，需要升级或使用 WSL2 方案
    - 安装后如果 Docker 无法启动，检查是否启用了虚拟化

### macOS 安装

=== "Apple Silicon（M1/M2/M3）"

    1. 访问 [Docker Desktop 下载页](https://www.docker.com/products/docker-desktop)
    2. 下载 **Apple Chip** 版本
    3. 双击 `.dmg` 文件，将 Docker 拖入 Applications
    4. 启动 Docker Desktop，等待鲸鱼图标稳定

=== "Intel Mac"

    1. 访问 [Docker Desktop 下载页](https://www.docker.com/products/docker-desktop)
    2. 下载 **Intel Chip** 版本
    3. 双击 `.dmg` 文件，将 Docker 拖入 Applications
    4. 启动 Docker Desktop

```bash
# 验证安装
docker --version
docker run hello-world
```

### Linux 安装

=== "Ubuntu / Debian"

    ```bash
    # 卸载旧版本（如果有）
    sudo apt-get remove docker docker-engine docker.io containerd runc
    
    # 安装依赖
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    
    # 添加 Docker 官方 GPG 密钥
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    
    # 添加 Docker 仓库
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # 安装 Docker
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # 将当前用户加入 docker 组（避免每次用 sudo）
    sudo usermod -aG docker $USER
    
    # 重新登录后验证
    docker --version
    docker run hello-world
    ```

=== "CentOS / RHEL / Fedora"

    ```bash
    # 卸载旧版本
    sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine
    
    # 安装依赖
    sudo yum install -y yum-utils
    
    # 添加 Docker 仓库
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    
    # 安装 Docker
    sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # 启动 Docker
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # 将当前用户加入 docker 组
    sudo usermod -aG docker $USER
    
    # 重新登录后验证
    docker --version
    docker run hello-world
    ```

---

## 2.2 验证安装：Hello World

安装完成后，运行 Docker 的"入门仪式"：

```bash
docker run hello-world
```

**预期输出：**

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
c1ec31eb5944: Pull complete
Digest: sha256:...
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.
```

!!! tip "这条命令背后发生了什么？"
    1. Docker 客户端（你敲的命令）联系 Docker 守护进程
    2. 守护进程检查本地有没有 `hello-world` 镜像 → 没有
    3. 从 Docker Hub 拉取 `hello-world` 镜像
    4. 基于镜像创建一个新容器并运行
    5. 容器输出"Hello from Docker!"，然后自动退出

---

## 2.3 运行第一个实用容器

`hello-world` 只是验证安装。让我们运行一个真正有用的容器——Nginx Web 服务器：

```bash
# 以后台模式运行 Nginx，将容器的 80 端口映射到本机的 8080 端口
docker run -d -p 8080:80 --name my-nginx nginx
```

**命令解析：**

| 参数 | 含义 |
|:---|:---|
| `docker run` | 创建并启动一个新容器 |
| `-d` | 后台运行（detached mode） |
| `-p 8080:80` | 端口映射：本机 8080 → 容器 80 |
| `--name my-nginx` | 给容器起个名字 |
| `nginx` | 使用的镜像名称 |

**验证：**

1. 打开浏览器，访问 `http://localhost:8080`
2. 你应该看到 Nginx 的欢迎页面！

```bash
# 查看运行中的容器
docker ps

# 预期输出：
# CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                  NAMES
# abc123def456   nginx     "/docker-entrypoint.…"   2 minutes ago   Up 2 minutes   0.0.0.0:8080->80/tcp   my-nginx
```

---

## 2.4 Docker 的基本架构

```
┌──────────────────────────────────────────────┐
│                  Docker 客户端                 │
│              (docker 命令)                     │
└──────────────────┬───────────────────────────┘
                   │ REST API
                   ▼
┌──────────────────────────────────────────────┐
│              Docker 守护进程 (dockerd)         │
│    ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│    │ 容器管理  │  │ 镜像管理  │  │ 网络管理  │     │
│    └─────────┘  └─────────┘  └─────────┘     │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│              containerd (容器运行时)           │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│              runc (OCI 运行时)                 │
│         ┌──────┐  ┌──────┐  ┌──────┐         │
│         │容器 A │  │容器 B │  │容器 C │         │
│         └──────┘  └──────┘  └──────┘         │
└──────────────────────────────────────────────┘
```

!!! info "Docker Desktop vs Docker Engine"
    - **Docker Desktop**（Windows/Mac）：包含 Docker Engine + GUI 管理界面 + Kubernetes 支持
    - **Docker Engine**（Linux）：纯命令行版本，生产环境的标准选择
    - 本教程的命令在两种环境下完全通用

---

## 2.5 常用验证命令

```bash
# 查看 Docker 版本信息
docker version

# 查看 Docker 系统信息（镜像数、容器数、存储驱动等）
docker info

# 查看已下载的镜像
docker images

# 查看所有容器（包括已停止的）
docker ps -a

# 停止并删除测试容器
docker stop my-nginx
docker rm my-nginx
```

---

## 要点总结

- [x] Docker Desktop 是 Windows/Mac 的一站式安装方案
- [x] Linux 通过包管理器安装 Docker Engine
- [x] `docker run hello-world` 验证安装是否成功
- [x] `docker run -d -p 8080:80 nginx` 运行第一个实用容器
- [x] `docker ps` 查看运行中的容器
- [x] Docker 采用客户端-守护进程架构

---

## 课后练习

1.  **安装验证** ：在你的电脑上安装 Docker，运行 `hello-world` 和 Nginx 容器。

2.  **端口探索** ：尝试将 Nginx 映射到不同的本机端口（如 9090），验证端口映射的工作原理。

3.  **容器生命周期** ：练习 `docker stop`、`docker start`、`docker rm` 命令，理解容器的停止、重启和删除。

---

**下一章预告：** 你已经成功运行了第一个容器。但镜像是怎么来的？容器和镜像到底是什么关系？第 3 章将深入镜像与容器的核心操作。

[继续第 3 章：镜像与容器 →](03-images-and-containers.md)