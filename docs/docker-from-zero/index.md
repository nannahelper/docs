# Docker 新手指南

> **从"在我机器上能跑"到"到处都能跑"** —— 掌握 Docker 容器技术，用集装箱思维解决环境一致性难题，开启现代化部署之旅。

---

## 教程简介

Docker 是当今最流行的容器化平台，它将应用及其依赖打包成一个标准化的"集装箱"，确保在任何环境中都能一致运行。从本地开发到云端部署，Docker 已成为现代软件工程的必备技能。

!!! info "为什么学 Docker？"

    -  **环境一致性** ：彻底告别"在我机器上能跑啊"的尴尬，开发、测试、生产环境完全一致
    -  **快速部署** ：秒级启动，比虚拟机快数十倍，资源占用极低
    -  **微服务基石** ：每个服务独立打包、独立部署、独立扩缩容
    -  **生态丰富** ：Docker Hub 上有数百万现成的镜像，拿来即用

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 掌握 Docker 核心概念与常用命令，能独立完成多容器应用的部署 |
| **预计时长** | 8~10 小时 |
| **前置要求** | 基本的命令行操作能力，了解 Web 应用的基本概念 |
| **关键概念** | 镜像、容器、Dockerfile、数据卷、网络、Docker Compose |
| **实践任务** | 部署一个完整的 Web 应用：Nginx + 后端 + 数据库 |

---

## 学习路径

本教程采用 **场景驱动** 的方式，每个章节围绕一个真实运维任务展开：

| 章节 | 场景 | 你将学会 |
|:---|:---|:---|
| [第 1 章：认识 Docker](01-introduction.md) | 理解容器 vs 虚拟机的区别 | Docker 是什么、为什么用、核心概念 |
| [第 2 章：环境搭建](02-installation.md) | 安装 Docker 并运行第一个容器 | Docker Desktop 安装、Hello World 验证 |
| [第 3 章：镜像与容器](03-images-and-containers.md) | 拉取镜像、运行和管理容器 | pull、run、stop、rm、logs、exec |
| [第 4 章：Dockerfile](04-dockerfile.md) | 定制自己的应用镜像 | FROM、RUN、COPY、CMD、构建与推送 |
| [第 5 章：数据管理](05-volumes.md) | 让数据"活"在容器之外 | Volume、Bind Mount、数据持久化 |
| [第 6 章：网络管理](06-networks.md) | 让容器之间互相通信 | Bridge、自定义网络、容器互联 |
| [第 7 章：Docker Compose](07-docker-compose.md) | 一键启动多容器应用 | compose 文件编写、服务编排 |
| [第 8 章：综合实战](08-final-project.md) | 部署完整 Web 应用 | Nginx + Flask + MySQL 全栈部署 |

---

## 快速预览

```bash
# 运行你的第一个容器
docker run hello-world

# 在容器中运行一个交互式 Ubuntu
docker run -it ubuntu bash

# 以后台模式启动 Nginx
docker run -d -p 8080:80 --name my-nginx nginx

# 查看运行中的容器
docker ps

# 访问 http://localhost:8080 就能看到 Nginx 欢迎页！
```

---

👉 [开始学习：第 1 章 · 认识 Docker →](01-introduction.md)