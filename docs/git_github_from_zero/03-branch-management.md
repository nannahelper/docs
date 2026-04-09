# 第 3 章：分支管理——创造平行宇宙 (Branching)
## 🌌 平行宇宙和时间线——安全地探索新功能

在这一章，你会学到 Git 最强大的特性之一：**分支（Branch）**。分支让你可以在不影响成熟代码的前提下，安全地尝试新功能。

---

## 你会学到

- ✅ **什么是分支**：理解"平行宇宙"模型，知道为什么分支如此安全
- ✅ **为什么需要分支**：多人开发、实验新功能、修复Bug时为什么必须用分支
- ✅ **创建和切换分支**：学会在不同"平行宇宙"之间切换
- ✅ **合并分支**：将成熟的功能合并回主线，而不损坏已有的代码
- ✅ **分支命名规范**：用专业的方式命名分支

---

## 3.1 什么是分支？

### 问题：多人同时开发同一个项目

想象你和队友 Alice、Bob 一起开发一个 Python Flask API：

- 🚀 **主线（main 分支）** 正在运行生产环境，用户正在使用
- 👤 **你**：想添加一个新数据库查询功能
- 👤 **Alice**：想优化 API 响应速度
- 👤 **Bob**：想修复一个登录 Bug

如果你们都直接改 `main` 分支的代码：

```
你: app.py 第 45 行改了 X
Alice: app.py 第 45 行改了 Y
Bob: app.py 第 45 行改了 Z

现在谁的改动生效？代码冲突！💥
```

最糟糕的是，如果 Alice 的改动有 Bug，一旦正式上线并触发，整个生产环境都会挂掉。

### 解决方案：分支（Branch）

!!! info "名词解释：Branch"
    **分支** = 一条独立的代码开发线。每条分支都是完整的项目副本，互不影响。
    
    想象你在看一个树——`main` 分支是树干，其他分支是从树干长出来的树枝。
    
    每条树枝上都有完整的项目代码，你可以在树枝上随便修改，不影响树干。

### 分支的超能力

使用分支，上面的场景变成了：

```
main 分支（生产环境）：稳定，用户正在使用 ✅

feature/database（你的分支）
  ├─ 代码随便改
  ├─ 可以删除、重构、试验
  └─ 玩坏了也没关系

feature/performance（Alice 的分支）
  ├─ 优化代码
  └─ 完全独立，不影响任何人

bugfix/login（Bob 的分支）
  ├─ 修复 Bug
  └─ 修好了再合并回 main
```

每个人都在自己的分支上工作，互不干扰。等功能稳定后再合并回 `main` 分支。

### 为什么分支如此安全？

- ✅ **隔离**：每条分支完全独立，一个分支的Bug不会影响其他分支或main分支
- ✅ **并行开发**：多人可以同时在不同分支上工作
- ✅ **试验性**：可以大胆尝试新功能，玩坏了删掉重来
- ✅ **Code Review**：合并前可以让队友审查代码（通过 Pull Request）
- ✅ **历史保留**：分支被删除后，提交记录永远保存在 main 分支里

!!! example "举个例子 / 类比理解"
    
    分支就像一个**平行宇宙小说**：
    
    - 🌍 **主世界（main）**：现实中正在发生的事
    - 🌌 **平行世界 1（feature/dragon）**：假如世界上出现了龙会怎样？
    - 🌌 **平行世界 2（feature/magic）**：假如人类有魔法会怎样？
    
    在平行世界里你可以随便尝试，看看效果。如果你喜欢某个平行世界的情节，就把它合并回现实。否则，那个平行世界就永远关闭了，现实世界不受影响。

---

## 3.2 创建与切换分支

现在我们开始实操。

### 分支命名规范

在创建分支前，要知道怎样给分支起名。专业的分支名字让代码审查更容易。

**推荐的命名模式**：

```
feature/功能名         新功能分支（用 feature/ 前缀）
  feature/user-auth
  feature/database-query
  feature/api-caching

bugfix/Bug名           修复 Bug 分支（用 bugfix/ 前缀）
  bugfix/login-error
  bugfix/api-timeout

refactor/说明          重构分支（用 refactor/ 前缀）
  refactor/database-layer
  refactor/error-handling

docs/说明              文档更新分支
  docs/api-documentation
```

**分支名命名要点**：
- 使用英文（Git 历史记录主要是英文）（编者注：德日法西都可以，你自己看的明白就行）
- 用连字符 `-` 分隔单词（不要用下划线或空格）
- 名字要有意义（`feature/fix` 是模糊的，`bugfix/login-validation` 更清楚）
- 长度合理（一或两个单词就够）

---

### 步骤 1：创建一个新分支

你要开发一个新功能：添加用户认证。

**方法 A：命令行**

```bash
# 创建一个新分支，并立即切换到这个分支
# 分支名：feature/user-auth
git switch -c feature/user-auth

# 你会看到输出：
# Switched to a new branch 'feature/user-auth'
```

或者用更传统的语法也行（效果一样）：

```bash
git checkout -b feature/user-auth
```

**方法 B：VSCode**

1. 打开 **Source Control** 面板
2. 找到面板顶部显示当前分支名的地方（例如 `main`）
3. 点击那个分支名
4. 在弹出的菜单里选择 **"Create new branch"**
5. 输入新分支名 `feature/user-auth`
6. 按 Enter

---

### 步骤 2：确认你在正确的分支上

很重要：在提交代码前，确认你在正确的分支上。

**方法 A：命令行**

```bash
# 这个命令显示所有分支，当前分支会被标记为 *
git branch

# 输出类似：
#   main
# * feature/user-auth
```

星号 `*` 表示你正在 `feature/user-auth` 分支上。

**方法 B：VSCode**

看左下角的状态栏。分支名会显示在那里（例如 `feature/user-auth`）。点击它可以快速切换分支。

---

### 步骤 3：在分支上进行开发

现在你可以安全地修改代码，不用担心影响 `main` 分支。

创建一个新文件 `auth.py`：

```python
# auth.py - 用户认证功能

def verify_login(username, password):
    """
    验证用户登录信息。
    这是一个演示函数，实际项目中会连接数据库。
    """
    # 这里应该连接数据库检查 username 和 password
    print(f"验证用户: {username}")
    return True

def generate_token(user_id):
    """生成一个会话 token（简化版）"""
    return f"token-{user_id}"
```

### 步骤 4：提交改动

就像之前一样提交代码：

```bash
git add auth.py
git commit -m "feat: 添加用户认证模块"
```

或者用 VSCode 完成同样的操作。

!!! tip "重要"
    你现在的所有改动都在 `feature/user-auth` 分支上。`main` 分支完全不受影响。
    
    如果你想看看 `main` 分支现在什么样，切换到 `main`，你会发现 `auth.py` 文件不存在。这就是分支的隔离性。

---

### 步骤 5：切换分支

想象现在 Bob 说："嘿，我发现了一个登录 Bug，需要立即修复。" 你需要暂停当前工作，帮他修 Bug。

**方法 A：命令行**

```bash
# 切换回 main 分支
git switch main

# 或者用跨平台的旧语法
git checkout main

# 输出：
# Switched to branch 'main'
```

现在你在 `main` 分支上，`auth.py` 文件消失了（因为它只存在于 `feature/user-auth` 分支）。

**方法 B：VSCode**

点击左下角的分支名 `feature/user-auth` → 选择 `main` → 完成。

!!! warning "重要警告"
    
    切换分支前，**必须提交或存储**所有改动。否则 Git 会拒绝切换：
    
    ```
    error: Your local changes to the following files would be overwritten by checkout:
      some_file.py
    Please commit your changes or stash them before you switch branches.
    ```
    
    解决方法：
    - ✅ 提交改动：`git commit -am "message"`
    - ✅ 或者暂存：`git stash`（第 7 章详细讲）

---

## 3.3 合并分支（Merge）

现在 `feature/user-auth` 分支的代码已经完成并测试通过了。你需要把这些改动合并回 `main` 分支。

### 合并的原理

```
feature/user-auth 分支：
  commit A
  commit B
  commit C（auth.py 功能完成）

｜
｜（合并）
v

main 分支：
  commit 1
  commit 2
  commit C（auth.py 被添加到 main）
```

合并后，`main` 分支拥有了 `feature/user-auth` 的所有改动。

### 步骤 1：切换回 main 分支

```bash
git switch main
```

### 步骤 2：执行合并

**方法 A：命令行**

```bash
# 将 feature/user-auth 分支合并到当前分支（main）
git merge feature/user-auth

# 输出应该像这样：
# Updating abc123..def456
# Fast-forward
#  auth.py | 15 ++++++++++++++
#  1 file changed, 15 insertions(+)
```

**方法 B：VSCode**

1. 确保你已经切换到 `main` 分支
2. 打开命令面板：Ctrl+Shift+P（Windows）或 Cmd+Shift+P（macOS）
3. 输入 "Git: Merge Branch"
4. 选择要合并的分支 `feature/user-auth`
5. 完成！

### 步骤 3：验证合并成功

```bash
# 现在 main 分支拥有了 auth.py
git log --oneline

# 输出：
# def456 feat: 添加用户认证模块
# abc123 feat: 初始化项目
# ...
```

或者直接看文件系统，`auth.py` 应该已经出现在 `main` 分支的工作目录里。

---

### 步骤 4：删除已合并的分支（可选）

合并完成后，`feature/user-auth` 分支可以删除了。保留它会导致分支列表臃肿。

```bash
# 删除本地分支
git branch -d feature/user-auth

# 如果删除失败（比如分支没有完全合并），用强制删除
git branch -D feature/user-auth
```

或者用 VSCode：
1. 右键点击分支名
2. 选择 "Delete Branch"

!!! note "提醒"
    删除本地分支后，提交历史仍然保留在 `main` 分支里。你可以随时查看 `git log` 看到曾经是谁提交的改动。
    
    分支本身只是一个"指针"，删除分支不会删除提交。

---

### 冲突解决简介

有时候合并分支时，Git 会说："两个分支修改了同一个文件的同一行，我不知道应该用哪个。" 这叫 **merge conflict**（合并冲突）。

**冲突示例**：

```python
# main 分支的 app.py 第 10 行：
<<<<<< HEAD
API_BASE_URL = "https://prod.api.com"
======
API_BASE_URL = "https://dev.api.com"
>>>>>> feature/user-auth
```

这说明主分支和功能分支在这一行有不同的改动。

**解决方法**（简化版）：

1. 打开有冲突的文件
2. VSCode 会高亮显示冲突区域
3. 点击 **"Accept Current"**（用主分支的）、**"Accept Incoming"**（用功能分支的）或 **"Accept Both"**（两个都要）
4. 手动编辑到满意为止
5. `git add` 和 `git commit` 完成合并

（第 6 章会详细讲冲突解决）

---

## 3.4 分支最佳实践

### 1️⃣ 规则：每个功能用一个分支

- ❌ 错误：所有改动都在 `main` 分支上
- ✅ 正确：给每个功能创建一个分支（`feature/auth`、`feature/payment` 等）

### 2️⃣ 规则：分支要保持小而精

- ❌ 错误：`feature/huge-refactor` 包含 50 个文件的改动
- ✅ 正确：每个分支只完成一个明确的功能或修复

### 3️⃣ 规则：经常同步主分支

在开发途中，经常从 `main` 拉取最新代码，保持同步：

```bash
git fetch origin main
git merge origin/main
```

这样可以早发现冲突，而不是积累到最后。

### 4️⃣ 规则：不要在主分支上直接提交

- ❌ 错误：在 `main` 分支上随便改代码
- ✅ 正确：创建 feature 分支，开发完成后通过 Pull Request 审查，再合并

---

## 3.5 常见问题排查

### 问题 1：分支创建后，旧代码还在

**症状**：我创建了 `feature/new-feature` 分支，但 `main` 分支的所有文件都复制过来了。

**原因**：这是对的！分支是完整的项目副本。如果不是这样，分支就没有意义了。

**验证**：
```bash
git log --all --oneline --graph
```

这会显示分支图表，你会看到 `feature/new-feature` 和 `main` 分别有自己的提交线。

### 问题 2：我忘了在正确的分支上

**症状**：我改好了代码，才发现我在 `main` 分支上改的，不是 `feature/` 分支上。

**解决**：
```bash
# 先 commit 你的改动
git commit -m "feat: 我本应在 feature 分支上的改动"

# 创建一个新分支指向这个 commit
git branch feature/intended-feature

# 然后把 main 分支回退（第 7 章详细讲）
git reset --soft HEAD~1
```

### 问题 3：我想查看另一个分支的代码

**不需要切换分支**。用差异查看：

```bash
# 查看两个分支的差异
git diff main feature/new-feature

# 查看特定文件的差异
git diff main feature/new-feature -- auth.py
```

---

## 📚 关键概念总结

| 命令 | 作用 |
|------|------|
| `git branch` | 列出所有分支 |
| `git switch -c <分支名>` | 创建新分支并切换 |
| `git switch <分支名>` | 切换到既有分支 |
| `git merge <分支名>` | 合并分支到当前分支 |
| `git branch -d <分支名>` | 删除分支 |
| `git log --graph` | 查看分支图表 |

---

## 🚀 下一步

完成本章后，你已经能够：
- ✅ 理解为什么需要分支
- ✅ 创建和管理多个开发分支
- ✅ 安全地并行开发
- ✅ 合并功能完整的代码回主线

**下一章**：走向云端。你会学到如何把本地的分支 "推送" 到 GitHub，与队友共享代码。
