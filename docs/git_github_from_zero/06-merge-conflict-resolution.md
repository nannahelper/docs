# 第 6 章：遇到冲突怎么办？(Merge Conflicts)
## ⚔️ 冲突不是坏事——学会优雅地解决它

在这一章，你会学到什么是 Merge Conflict，以及如何像专业人士一样解决它。冲突看起来吓人，但实际上很好解决。

---

## 你会学到

- ✅ **什么是 Merge Conflict**：为什么会发生冲突
- ✅ **冲突标记**：理解 Git 显示冲突的方式
- ✅ **解决策略**：用 VSCode 快速解决
- ✅ **Python 特定冲突**：imports、requirements.txt 等

---

## 6.1 什么是 Merge Conflict？

### 场景：两个人改了同一行代码

```
main 分支：
  app.py 第 10 行是：API_URL = "https://prod.com"

你的分支 (feature/auth)：
  改成了：API_URL = "https://prod-auth.com"

Alice 的分支 (feature/payment)：
  改成了：API_URL = "https://prod-payment.com"

现在要合并：
  哪个 URL 才是对的？Git 傻眼了！`❌ CONFLICT
```

!!! info "名词解释：Merge Conflict"
    
    **Merge Conflict**（合并冲突）= 当合并两个分支时，Git 发现同一个文件的同一行有**不同的改动**，无法自动决定保留哪一个。

---

### 为什么冲突并不可怕？

- ✅ **冲突是安全的**：Git 不会自动选择一个版本，而是让你手动决定
- ✅ **冲突容易发现**：不会悄悄产生 Bug
- ✅ **冲突容易解决**：一旦理解了标记，就很直观
- ✅ **冲突是正常的**：大型项目中，冲突是家常便饭

---

## 6.2 冲突是如何产生的？

### 触发冲突的常见操作

1. **合并分支时（Merge Conflict）**
   ```bash
   git merge feature/auth    # 两个分支改了同一行 → 冲突
   ```

2. **拉取远程代码时（Pull Conflict）**
   ```bash
   git pull origin main      # 队友改了你也改的地方 → 冲突
   ```

3. **变基时（Rebase Conflict）**（高级操作，初学者通常不用）

---

## 6.3 识别冲突标记

当冲突发生时，Git 会在冲突的文件里插入特殊的标记。让我们看一个例子：

有一个 `config.py` 文件在冲突状态下看起来像这样：

```python
# config.py

DATABASE_URL = "postgresql://localhost"

<<<<<< HEAD
API_KEY = "sk-prod-12345"      # ← 这是你在 main 分支上的版本（HEAD）
======
API_KEY = "sk-dev-67890"       # ← 这是 feature/auth 分支要合并进来的版本
>>>>>> feature/auth

DEBUG = False
```

让我们理解每一部分：

| 部分 | 含义 |
|------|------|
| `<<<<< HEAD` | "下面这个是当前分支的改动" |
| 中间的代码 | 当前分支的版本 |
| `======` | "分隔符" |
| 下面的代码 | 另一个分支的版本 |
| `>>>>> feature/auth` | "上面这个是 feature/auth 分支的改动" |

---

## 6.4 解决冲突（CLI 方式）

如果你是命令行爱好者，手动编辑也不复杂。

### 步骤 1：打开冲突文件

```bash
# Git 会告诉你哪个文件有冲突
# 或者用这个命令查看
git status
```

### 步骤 2：手动编辑文件

打开 `config.py`，你会看到冲突标记。现在决定：

**选项 A：保留当前分支的改动**

删除冲突标记和对方的代码，只保留自己的：

```python
# 删除这些：
# <<<<<< HEAD
# ======
# >>>>>> feature/auth

API_KEY = "sk-prod-12345"      # ← 保留这一行
```

**选项 B：保留对方分支的改动**

```python
API_KEY = "sk-dev-67890"       # ← 保留这一行（来自 feature/auth）
```

**选项 C：两个都要**

```python
# 保留两个版本，可能用不同的变量名
PROD_API_KEY = "sk-prod-12345"
DEV_API_KEY = "sk-dev-67890"

# 然后根据环境选择使用哪一个
import os
API_KEY = PROD_API_KEY if os.getenv("ENV") == "prod" else DEV_API_KEY
```

### 步骤 3：完成编辑

编辑完毕后，文件应该不再包含 `<<<<`、`====`、`>>>>` 标记。

### 步骤 4：标记为已解决

```bash
# 告诉 Git 你已经解决了冲突
git add config.py

# 完成合并
git commit -m "resolve: 合并冲突，选择 prod API key"
```

现在冲突被解决了！

---

## 6.5 解决冲突（VSCode 方式 - 推荐）

VSCode 提供了超级友好的冲突解决界面。这是推荐的方式。

### 步骤 1：识别冲突

当冲突发生时，VSwCode 会在有冲突的文件旁边显示 **红色叉号**。

### 步骤 2：打开冲突文件

点击有冲突的文件，VSCode 会高亮显示冲突区域：

```python
┌────────────────────────────────────────────────────────┐
│ Current Change (HEAD)  │  Incoming Change (feature/auth) │  Both │ Accept Both │
├────────────────────────────────────────────────────────┤
│ API_KEY = "sk-prod-12345"                                │
│ ======                                                   │
│ API_KEY = "sk-dev-67890"                                 │
└────────────────────────────────────────────────────────┘
```

### 步骤 3：选择解决方式

VSCode 为你提供了 4 个按钮：

| 按钮 | 作用 |
|------|------|
| **Accept Current** | 保留当前分支的改动 |
| **Accept Incoming** | 保留来自另一分支的改动 |
| **Accept Both** | 两个都保留 |
| **Compare** | 并排查看两个版本 |

**例子**：假设你想保留当前分支的值，点击 **"Accept Current"** 按钮。

VSCode 会自动：
- ✅ 删除冲突标记
- ✅ 删除对方的代码
- ✅ 保留你选择的版本

### 步骤 4：验证并提交

当所有冲突都被解决后（所有冲突标记都消失了），提交改动：

```bash
git add .
git commit -m "resolve: 合并冲突"
```

或者用 VSCode 的 Source Control 面板完成提交。

---

## 6.6 Python 特定冲突：imports

### 场景：两个开发者都添加了新的 imports

```
main 分支的 app.py:
  from flask import Flask, render_template
  from datetime import datetime

你的分支（feature/auth）:
  from flask import Flask, render_template
  from datetime import datetime
  from jwt import encode, decode    # ← 你加的

Alice 的分支（feature/cache）:
  from flask import Flask, render_template
  from datetime import datetime
  from redis import Redis           # ← Alice 加的
```

合并时会产生冲突吗？**通常不会**，因为 import 在不同的行。但如果你们都改了同一行呢？

```
你改了：
  from flask import Flask, render_template, session

Alice 改了：
  from flask import Flask, render_template, request

冲突！
```

### 解决方法

1. **用 VSCode 的冲突解决**，或者
2. **手动编辑**为一个完整的 import：

```python
from flask import Flask, render_template, session, request
```

**最佳实践**：

```python
# 推荐这样组织 imports（各占一行，便于解决冲突）
from flask import (
    Flask,
    render_template,
    session,
    request,
)
```

这样即使冲突，也只是添加新行，不会产生同行冲突。

---

## 6.7 Python 特定冲突：`requirements.txt`

### 场景：两个开发者都升级了某个库

```
main 分支：
  Flask==2.3.0
  requests==2.31.0

你的分支：
  Flask==2.3.0
  requests==2.31.0
  PyJWT==2.8.0     # 你加的

Alice 的分支：
  Flask==2.4.0     # Alice 升级的
  requests==2.31.0
```

合并时可能产生冲突（如果冲突解决器不够聪明）。

### 解决方法

```
<<<<<< HEAD
Flask==2.3.0
PyJWT==2.8.0
======
Flask==2.4.0
>>>>>> feature/payment
```

**最终的正确答案**：

```
Flask==2.4.0       # 最新版本
PyJWT==2.8.0       # 保留两个分支都需要的库
requests==2.31.0
```

**关键点**：
- 合并 requirements.txt 时，**同时保留双方添加的库**
- **使用最高的版本号**（如果版本冲突的话）
- 提交后运行 `pip install -r requirements.txt` 测试

---

## 6.8 冲突解决的完整流程

假设你正在合并 Alice 的分支，产生了冲突。完整的解决流程是：

```bash
# 1. 尝试合并（产生冲突）
git merge feature/alice-changes

# 2. 查看冲突状态
git status

# 3. 打开 VSCode，用图形界面解决冲突
# （或者用编辑器手动编辑）

# 4. 确认所有文件都被编辑好了
git status

# 5. 把已解决的文件标记为已解决
git add .

# 6. 完成合并
git commit -m "resolve: 合并 feature/alice-changes, 保留双方的改动"

# 7. 查看日志，确认合并成功
git log --oneline

# 8. 如果在本地代码仓库中工作，推送到远程
git push origin main
```

---

## 6.9 避免冲突的最佳实践

虽然冲突不可避免，但你可以最小化冲突的发生：

### 1️⃣ 经常 Pull 主分支

```bash
# 每天开始时
git fetch origin main
git merge origin/main

# 在功能开发中途也要经常同步
```

### 2️⃣ 保持分支小而精

- ❌ 不好：一个 `feature/huge-refactor` 包含 100 行改动
- ✅ 好：多个小分支，各自解决一个问题

### 3️⃣ 通信和协调

- 告诉队友你要改哪些文件
- 避免多个人同时改同一个文件的同一部分

### 4️⃣ 使用编辑器的自动格式化

某些情况下（如调整空格），自动格式化会产生噪音冲突。使用一致的 formatter（如 `black` for Python）**在 commit 前**自动格式化。

---

## 🚀 下一步

完成本章后，你已经能够：
- ✅ 理解冲突的原因
- ✅ 用 VSCode 快速解决冲突
- ✅ 处理 Python 特定的库冲突
- ✅ 知道如何避免冲突

**下一章**：处理其他常见问题和高级技巧。
