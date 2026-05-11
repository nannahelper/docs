# 第 5 章：数据管理 —— 让数据"活"在容器之外

> **场景：** 你用 Docker 跑了一个 MySQL 容器，存了几百条用户数据。某天你升级镜像，删掉了旧容器——数据全没了！容器是无状态的，删除即消失。要让数据持久化，你需要把数据"搬"到容器外面——这就是数据卷的作用。

---

## 5.1 为什么需要数据持久化？

!!! example "核心比喻：容器就像酒店房间，数据卷就像你家仓库"
    住酒店时，房间里的东西（牙刷、毛巾）退房后就没了。但如果你把贵重物品存进酒店的保险柜（数据卷），退房后东西还在，下次入住还能取出来。
    
    容器 = 酒店房间（临时的，删了就没了）
    数据卷 = 保险柜 / 你家仓库（持久的，独立于容器的生命周期）

```bash
# 演示数据丢失问题
docker run -d --name temp-mysql -e MYSQL_ROOT_PASSWORD=secret mysql:8
docker exec temp-mysql mysql -psecret -e "CREATE DATABASE mydb;"
docker rm -f temp-mysql

# 重新运行一个新容器——数据库没了！
docker run -d --name new-mysql -e MYSQL_ROOT_PASSWORD=secret mysql:8
docker exec new-mysql mysql -psecret -e "SHOW DATABASES;"
# mydb 不存在了！
```

---

## 5.2 三种数据存储方式

| 方式 | 管理方 | 位置 | 适用场景 |
|:---|:---|:---|:---|
| **Volume** | Docker 管理 | `/var/lib/docker/volumes/` | 生产环境数据库、持久化存储 |
| **Bind Mount** | 用户管理 | 宿主机任意路径 | 开发环境、配置文件热更新 |
| **tmpfs** | 内存 | 内存中 | 临时敏感数据、缓存 |

---

## 5.3 Volume（数据卷）—— 推荐方式

### 创建和管理 Volume

```bash
# 创建数据卷
docker volume create mysql-data

# 查看所有数据卷
docker volume ls

# 查看数据卷详细信息（包括挂载点）
docker volume inspect mysql-data

# 删除数据卷
docker volume rm mysql-data

# 清理所有未使用的数据卷
docker volume prune
```

### 使用 Volume 运行容器

```bash
# 将数据卷挂载到 MySQL 的数据目录
docker run -d \
  --name mysql \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  mysql:8

# 验证数据持久化
docker exec mysql mysql -psecret -e "CREATE DATABASE mydb;"
docker rm -f mysql

# 重新运行容器，使用同一个数据卷
docker run -d \
  --name mysql \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  mysql:8

# 数据还在！
docker exec mysql mysql -psecret -e "SHOW DATABASES;"
```

### 多个容器共享 Volume

```bash
# 容器 A 写入数据
docker run -d --name writer \
  -v shared-data:/data \
  alpine sh -c "echo 'Hello from writer' > /data/message.txt && sleep 3600"

# 容器 B 读取数据
docker run --rm \
  -v shared-data:/data \
  alpine cat /data/message.txt
# 输出：Hello from writer
```

---

## 5.4 Bind Mount（绑定挂载）—— 开发利器

!!! example "核心比喻：Bind Mount 就像把仓库直接建在你家后院"
    Volume 是 Docker 帮你管理的仓库（你不知道具体在哪）。Bind Mount 是你自己指定仓库位置——比如你家后院 `/home/user/my-data`。你可以随时走过去看看里面有什么，非常方便开发调试。

```bash
# 将宿主机目录挂载到容器
docker run -d \
  --name nginx-dev \
  -v /home/user/my-web:/usr/share/nginx/html:ro \
  -p 8080:80 \
  nginx

# Windows 路径示例（PowerShell）
docker run -d --name nginx-dev `
  -v C:\Users\me\my-web:/usr/share/nginx/html:ro `
  -p 8080:80 nginx
```

!!! tip "挂载选项"
    - `:ro` — 只读挂载（容器不能修改）
    - `:rw` — 读写挂载（默认）
    - `:z` — SELinux 标签（共享）
    - `:Z` — SELinux 标签（私有）

### 开发场景：代码热更新

```bash
# 将本地代码目录挂载到容器，修改代码立即生效
docker run -d \
  --name flask-dev \
  -v $(pwd):/app \
  -p 5000:5000 \
  -e FLASK_ENV=development \
  my-flask-app:v1
```

---

## 5.5 实战：MySQL 数据持久化

```bash
# 1. 创建数据卷
docker volume create mysql-data

# 2. 运行 MySQL 容器
docker run -d \
  --name mysql-db \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  -e MYSQL_DATABASE=myapp \
  -p 3306:3306 \
  mysql:8

# 3. 创建测试数据
docker exec mysql-db mysql -pmy-secret-pw myapp \
  -e "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100));"
docker exec mysql-db mysql -pmy-secret-pw myapp \
  -e "INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie');"

# 4. 验证数据
docker exec mysql-db mysql -pmy-secret-pw myapp \
  -e "SELECT * FROM users;"

# 5. 删除容器（数据卷保留）
docker rm -f mysql-db

# 6. 重新运行容器，挂载同一个数据卷
docker run -d \
  --name mysql-db-new \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  -p 3306:3306 \
  mysql:8

# 7. 数据完好无损！
docker exec mysql-db-new mysql -pmy-secret-pw myapp \
  -e "SELECT * FROM users;"
```

---

## 5.6 备份和恢复 Volume

```bash
# 备份数据卷
docker run --rm \
  -v mysql-data:/source \
  -v $(pwd):/backup \
  alpine tar czf /backup/mysql-backup.tar.gz -C /source .

# 恢复数据卷
docker run --rm \
  -v mysql-data:/target \
  -v $(pwd):/backup \
  alpine tar xzf /backup/mysql-backup.tar.gz -C /target
```

---

## 要点总结

- [x] 容器删除后数据丢失，需要数据卷实现持久化
- [x] Volume 由 Docker 管理，适合生产环境
- [x] Bind Mount 由用户指定路径，适合开发环境
- [x] `-v 卷名:容器路径` 挂载数据卷
- [x] 多个容器可以共享同一个 Volume
- [x] 备份 Volume：用临时容器打包数据

---

## 课后练习

1.  **Volume 实验** ：运行一个 MySQL 容器，创建数据、删除容器、重新运行——验证数据是否保留。

2.  **Bind Mount 开发** ：将本地一个 HTML 文件目录挂载到 Nginx 容器，修改文件后刷新浏览器验证热更新。

3.  **备份练习** ：备份 MySQL 数据卷，然后删除数据卷，再用备份恢复。

---

**下一章预告：** 数据持久化搞定了。但你的 Web 应用需要连接数据库——容器之间怎么通信？第 6 章将学习 Docker 网络管理。

[继续第 6 章：网络管理 →](06-networks.md)