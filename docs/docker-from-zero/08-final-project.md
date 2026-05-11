# 第 8 章：综合实战 —— 部署一个完整的 Web 应用

> **场景：** 你已经掌握了 Docker 的所有核心技能。现在，让我们把它们全部用上——从零开始，用 Docker 部署一个完整的 **任务管理 API** 应用。这个项目涵盖镜像构建、数据持久化、网络配置、服务编排和反向代理，是你 Docker 学习之旅的"毕业设计"。

---

## 8.1 项目概览

!!! example "核心比喻：从零搭建一个自动化物流中心"
    你要建一个物流中心：Nginx 是前台接待（接收请求、分发任务），Flask 是仓库管理员（处理业务逻辑），MySQL 是货架系统（存储数据）。Docker Compose 是总控系统，一键启动整个物流中心。

### 架构图

```
┌──────────────────────────────────────────────────┐
│                    用户浏览器                       │
│                 http://localhost                   │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│              Nginx (反向代理 :80)                   │
│         静态文件 / → 前端页面                       │
│         API /api/ → 转发到 Flask                   │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│            Flask API (后端 :5000)                   │
│    ┌──────────────────────────────────────┐       │
│    │  GET    /api/tasks    获取所有任务     │       │
│    │  POST   /api/tasks    创建新任务       │       │
│    │  PUT    /api/tasks/:id 更新任务        │       │
│    │  DELETE /api/tasks/:id 删除任务        │       │
│    └──────────────────────────────────────┘       │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│            MySQL 8 (数据库 :3306)                   │
│           数据库: taskdb                           │
│           表: tasks                                │
└──────────────────────────────────────────────────┘
```

---

## 8.2 项目结构

```
task-manager/
├── docker-compose.yml
├── .env
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── init.sql
├── frontend/
│   └── index.html
└── nginx/
    └── nginx.conf
```

---

## 8.3 后端：Flask API

### backend/app.py

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
import time

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'secret'),
    'database': os.environ.get('DB_NAME', 'taskdb'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    retries = 10
    while retries > 0:
        try:
            conn = pymysql.connect(**DB_CONFIG)
            return conn
        except pymysql.Error:
            retries -= 1
            time.sleep(3)
    raise Exception("无法连接到数据库")

def init_db():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                status ENUM('pending', 'in_progress', 'done') DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()

@app.route('/api/health')
def health():
    try:
        conn = get_db()
        conn.close()
        return {'status': 'ok', 'database': 'connected'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'title is required'}), 400

    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO tasks (title, description, status) VALUES (%s, %s, %s)",
            (data['title'], data.get('description', ''), data.get('status', 'pending'))
        )
        conn.commit()
        task_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': task_id, 'message': 'Task created'}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    conn = get_db()
    with conn.cursor() as cursor:
        updates = []
        params = []
        if 'title' in data:
            updates.append("title = %s")
            params.append(data['title'])
        if 'description' in data:
            updates.append("description = %s")
            params.append(data['description'])
        if 'status' in data:
            updates.append("status = %s")
            params.append(data['status'])

        if not updates:
            return jsonify({'error': 'no fields to update'}), 400

        params.append(task_id)
        sql = f"UPDATE tasks SET {', '.join(updates)} WHERE id = %s"
        cursor.execute(sql, params)
        conn.commit()
        affected = cursor.rowcount
    conn.close()

    if affected == 0:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task updated'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        affected = cursor.rowcount
    conn.close()

    if affected == 0:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### backend/requirements.txt

```
flask==3.0.0
flask-cors==4.0.0
pymysql==1.1.0
```

### backend/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')" || exit 1

CMD ["python", "app.py"]
```

---

## 8.4 前端：静态页面

### frontend/index.html

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>任务管理器 - Docker Demo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0f2f5; color: #333; }
        .container { max-width: 800px; margin: 40px auto; padding: 20px; }
        h1 { text-align: center; margin-bottom: 30px; color: #1a73e8; }
        .add-form { display: flex; gap: 10px; margin-bottom: 20px; }
        .add-form input { flex: 1; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; }
        .add-form input:focus { border-color: #1a73e8; outline: none; }
        .add-form button { padding: 12px 24px; background: #1a73e8; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; }
        .add-form button:hover { background: #1557b0; }
        .task-list { list-style: none; }
        .task-item { background: white; padding: 16px; margin-bottom: 10px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .task-info { flex: 1; }
        .task-title { font-size: 18px; font-weight: 600; }
        .task-desc { color: #666; margin-top: 4px; }
        .task-status { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; margin-top: 6px; }
        .status-pending { background: #fff3cd; color: #856404; }
        .status-in_progress { background: #cce5ff; color: #004085; }
        .status-done { background: #d4edda; color: #155724; }
        .task-actions { display: flex; gap: 8px; }
        .task-actions button { padding: 6px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; }
        .btn-done { background: #28a745; color: white; }
        .btn-progress { background: #007bff; color: white; }
        .btn-delete { background: #dc3545; color: white; }
        .loading { text-align: center; padding: 40px; color: #999; }
        .empty { text-align: center; padding: 40px; color: #999; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 任务管理器</h1>
        <div class="add-form">
            <input type="text" id="taskInput" placeholder="输入新任务..." />
            <button onclick="addTask()">添加</button>
        </div>
        <ul class="task-list" id="taskList">
            <li class="loading">加载中...</li>
        </ul>
    </div>

    <script>
        const API = '/api/tasks';

        async function loadTasks() {
            try {
                const res = await fetch(API);
                const tasks = await res.json();
                const list = document.getElementById('taskList');
                if (tasks.length === 0) {
                    list.innerHTML = '<li class="empty">暂无任务，添加一个吧！</li>';
                    return;
                }
                list.innerHTML = tasks.map(t => `
                    <li class="task-item">
                        <div class="task-info">
                            <div class="task-title">${escapeHtml(t.title)}</div>
                            ${t.description ? `<div class="task-desc">${escapeHtml(t.description)}</div>` : ''}
                            <span class="task-status status-${t.status}">${statusLabel(t.status)}</span>
                        </div>
                        <div class="task-actions">
                            ${t.status !== 'done' ? `<button class="btn-done" onclick="updateTask(${t.id}, 'done')">完成</button>` : ''}
                            ${t.status === 'pending' ? `<button class="btn-progress" onclick="updateTask(${t.id}, 'in_progress')">进行中</button>` : ''}
                            <button class="btn-delete" onclick="deleteTask(${t.id})">删除</button>
                        </div>
                    </li>
                `).join('');
            } catch (e) {
                document.getElementById('taskList').innerHTML = '<li class="loading">加载失败，请检查后端服务</li>';
            }
        }

        async function addTask() {
            const input = document.getElementById('taskInput');
            const title = input.value.trim();
            if (!title) return;
            await fetch(API, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title})
            });
            input.value = '';
            loadTasks();
        }

        async function updateTask(id, status) {
            await fetch(`${API}/${id}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({status})
            });
            loadTasks();
        }

        async function deleteTask(id) {
            if (!confirm('确定删除这个任务吗？')) return;
            await fetch(`${API}/${id}`, {method: 'DELETE'});
            loadTasks();
        }

        function statusLabel(s) {
            return {pending: '待处理', in_progress: '进行中', done: '已完成'}[s] || s;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        loadTasks();
    </script>
</body>
</html>
```

---

## 8.5 Nginx 反向代理

### nginx/nginx.conf

```nginx
server {
    listen 80;
    server_name localhost;

    # 前端静态页面
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API 反向代理到 Flask
    location /api/ {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 8.6 Docker Compose 编排

### docker-compose.yml

```yaml
version: "3.8"

services:
  backend:
    build: ./backend
    container_name: task-backend
    environment:
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=${MYSQL_PASSWORD}
      - DB_NAME=taskdb
    networks:
      - app-network
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: mysql:8
    container_name: task-db
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_DATABASE: taskdb
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
    container_name: task-nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./frontend:/usr/share/nginx/html:ro
    networks:
      - app-network
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  mysql-data:

networks:
  app-network:
    driver: bridge
```

### .env

```
MYSQL_PASSWORD=task-manager-secret-2024
```

---

## 8.7 部署步骤

```bash
# 1. 进入项目目录
cd task-manager

# 2. 一键启动整个应用栈
docker compose up -d

# 3. 查看启动状态
docker compose ps

# 4. 查看日志（确认后端已连接数据库）
docker compose logs backend

# 5. 验证健康检查
curl http://localhost/api/health

# 6. 打开浏览器访问 http://localhost
```

**预期输出：**

```
[+] Running 4/4
 ✔ Network task-manager_app-network  Created
 ✔ Volume "task-manager_mysql-data"  Created
 ✔ Container task-db                 Healthy
 ✔ Container task-backend            Started
 ✔ Container task-nginx              Started
```

---

## 8.8 验证与测试

```bash
# 创建任务
curl -X POST http://localhost/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "学习 Docker", "description": "完成 Docker 新手指南全部章节"}'

# 获取所有任务
curl http://localhost/api/tasks

# 更新任务状态
curl -X PUT http://localhost/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'

# 删除任务
curl -X DELETE http://localhost/api/tasks/1
```

---

## 8.9 常用运维操作

```bash
# 查看所有容器状态
docker compose ps

# 查看实时日志
docker compose logs -f

# 只查看后端日志
docker compose logs -f backend

# 进入后端容器调试
docker compose exec backend bash

# 进入数据库
docker compose exec db mysql -p${MYSQL_PASSWORD} taskdb

# 重启单个服务
docker compose restart backend

# 更新代码后重新构建并启动
docker compose up -d --build

# 停止整个应用
docker compose down

# 停止并删除数据卷（⚠️ 数据会丢失！）
docker compose down -v
```

---

## 8.10 项目总结

通过这个综合项目，你实践了 Docker 的全部核心技能：

| 技能 | 在本项目中的应用 |
|:---|:---|
| **Dockerfile** | 为 Flask 后端编写 Dockerfile，定义构建流程 |
| **镜像构建** | `docker compose up --build` 自动构建后端镜像 |
| **容器管理** | Compose 管理 3 个容器的生命周期 |
| **数据持久化** | MySQL 数据存储在命名卷 `mysql-data` 中 |
| **网络配置** | 自定义 `app-network`，服务间用服务名通信 |
| **端口映射** | Nginx 的 80 端口映射到宿主机 |
| **环境变量** | `.env` 文件管理数据库密码 |
| **健康检查** | MySQL 健康检查确保后端启动时数据库已就绪 |
| **反向代理** | Nginx 将 `/api/` 请求转发到 Flask 后端 |
| **服务编排** | `docker compose up -d` 一键启动全部服务 |

---

## 要点总结

- [x] 完整项目包含 3 个服务：Nginx + Flask + MySQL
- [x] Docker Compose 编排所有服务，一键启动
- [x] 自定义网络实现服务间通信
- [x] 命名卷实现 MySQL 数据持久化
- [x] 健康检查确保服务启动顺序正确
- [x] `.env` 文件管理敏感配置
- [x] Nginx 反向代理统一入口

---

## 课后练习

1.  **部署验证** ：按照本章步骤，在你的机器上完整部署这个任务管理器。

2.  **功能扩展** ：为任务添加"优先级"字段，修改数据库表、后端 API 和前端页面。

3.  **添加 Redis** ：在 Compose 中加入 Redis 服务，用于缓存任务列表。

4.  **生产优化** ：尝试使用多阶段构建优化后端镜像大小，添加非 root 用户运行容器。

---

🎉 **恭喜你完成了 Docker 新手指南的全部学习！**

你已经掌握了：
- Docker 核心概念（镜像、容器、仓库）
- 常用命令（run、ps、logs、exec、cp）
- Dockerfile 编写与镜像构建
- 数据卷与持久化
- 网络配置与服务通信
- Docker Compose 多容器编排
- 完整的 Web 应用容器化部署

**下一步建议：**
- 学习 Docker Swarm 或 Kubernetes 进行集群编排
- 学习 CI/CD 中 Docker 的应用（GitHub Actions、Jenkins）
- 学习 Docker 安全最佳实践（非 root 用户、镜像扫描）
- 将你自己的项目容器化！

[返回首页 →](index.md)