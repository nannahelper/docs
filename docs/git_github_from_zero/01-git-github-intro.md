# 第 1 章：认识版本控制与环境配置 (Introduction)
## 🎮 游戏存档与云端同步——掌握代码管理的秘密

在这一章中，你会学到为什么 Python 开发者必须懂 Git，以及如何一次性配置好本地环境。完成本章后，你将能够理解 Git 和 GitHub 的区别，并为接下来的深入学习做好准备。

---

## 你会学到

- ✅ **Git 是什么**：一个"游戏存档系统"，帮你记住代码的每一次改动，而不需要手动重新命名文件
- ✅ **GitHub 是什么**：云端的"联机存档服务器"，让你和队友能共享代码，而不是各自孤立工作
- ✅ **为什么 Python 开发者需要 Git**：不仅仅是备份代码，更是为了统一团队的 Python 环境和项目依赖
- ✅ **如何配置 Git + GitHub + VSCode**：一次性的环境准备工作，之后就能流畅地开发了

---

## 1.1 什么是 Git？什么是 GitHub？

### 问题：为什么不能靠手动重新命名文件管理代码版本？

你可能曾经见过这样的场景：

```
script_v1.py
script_v2.py
script_final.py
script_REAL_final.py
script_final_final_v3.py  😱
```

这样做有几个致命的问题：

- ❌ **找不到哪个是最新的**：名字越来越长，反而很难找到
- ❌ **不知道改了什么**：文件众多，但不清楚 v2 到 v3 改了什么细节
- ❌ **无法团队协作**：队友给你 `script_final_v2.py`，你给他 `script_FINAL_v3.py`，两个文件根本合并不了
- ❌ **占用巨大磁盘空间**：每个版本都是整个文件的完整副本

**Git 解决这些问题的办法是什么？** 使用一个"游戏存档系统"，每次提交代码时，Git 自动为你记录是什么改变了。

!!! info "名词解释：Git"
    **Git** = 你电脑里的"版本控制工具"。它像一个高级的游戏存档系统，每次你对代码做出重要改动时，你可以按一个快照按钮，Git 就会记住 "在某年某月某日某时，文件 A 的第 5 行从 X 改成了 Y"。如果你以后需要回到某个时间点，Git 可以帮你恢复。

---

### 解决方案 1：Git（本地版本控制）

想象你在玩一款 RPG 游戏：

- 💾 **存档点**：在关键时刻，你手动存档（`git commit`），这样如果之后发生了不好的事，你可以读档恢复
- 💾 **多个存档位置**：你甚至可以在不同的地方存档（不同的分支），尝试不同的故事线
- 💾 **回溯历史**：Git 能完整记录你的操作历史，你可以随时查看 "一个月前你改了什么"

> **Git 的核心作用**：让你的代码文件拥有"完整的改动历史"，不需要手动重新命名。

---

### 问题升级：团队协作怎么办？

现在假设你和 3 个队友一起开发同一个项目。问题来了：

- ❌ **如何分享代码**？不能让大家都把文件写到移动硬盘上
- ❌ **如何同步版本**？A 改了 `app.py`，B 也改了 `app.py`，谁的版本更新？
- ❌ **如何审查代码**？提交代码前怎样确保质量？
- ❌ **如何处理冲突**？两个人同时改了同一行代码怎么办？

这就需要 **GitHub**。

!!! info "名词解释：GitHub"
    **GitHub** = 云端的"存档服务器"。如果 Git 是你电脑里的存档系统，GitHub 就是一个中央的云端服务，所有队友的代码都存在这里。你可以上传（push）你的最新进度，也可以下载（pull）队友的最新进度，大家保持进度同步。

---

### 解决方案 2：GitHub（云端协作平台）

继续用游戏的比喻：

- 🌐 **联机存档**：不再是单机游戏，你和队友可以在联机服务器上共享存档
- 🌐 **多人同步**：每个队友都可以上传自己的最新进度
- 🌐 **代码审查**：提交代码时，队友可以先看一下（Code Review），确保没问题
- 🌐 **备份保障**：即使你的电脑硬盘坏了，代码还在云上，不会丢失

---

### Git vs GitHub：它们不是一回事！

这是初学者最常见的混淆点。让我们用表格清楚地区分：

| 特性 | Git | GitHub |
|------|-----|--------|
| **是什么？** | 本地版本控制工具 | 云端代码托管平台 |
| **在哪里运行？** | 你的电脑上 | 互联网上的服务器 |
| **需要账号吗？** | 不需要，只需配置用户名 | 需要（免费注册） |
| **主要功能** | 记录代码改动历史、创建分支、合并代码 | 存储代码、团队协作、代码审查、Pull Request |
| **离线能用吗？** | 可以（完全离线工作） | 不行（需要网络同步） |

**核心概念**：Git 和 GitHub 是两个独立的工具，但经常一起使用。你可以只用 Git，但配合 GitHub 会让团队协作变得极其强大。

!!! tip "类比理解"
    把 Git 想象成**邮局**，把 GitHub 想象成**邮寄服务**：
    
    - **邮局（Git）**：帮你组织和管理你的信件（代码改动）
    - **邮寄服务（GitHub）**：帮你把信寄给远方的人（共享代码给队友）
    
    邮局单独存在且很有用；邮寄服务让邮局的价值倍增。

---

## 1.2 为什么 Python 开发者必须懂 Git？

"我只是想学 Python，为什么一定要学 Git？" ← 这是很多初学者的疑问。

答案很简单：**因为现实世界的 Python 项目必须用 Git 来管理团队协作和依赖**。

### 理由 1：统一团队的 Python 环境

想象这个场景：

👤 **你**：开了个新的 Flask 项目，安装了 Flask 2.3.0

👤 **队友 Alice**：下载了你的代码，但她装的是 Flask 2.2.0（版本不一致！）

👤 **队友 Bob**：又装了 Flask 3.0（更新版本！）

现在三个人的代码环境完全不同，每个人跑代码的结果都不一样，这就是灾难。

**Git 如何解决？** 通过 `requirements.txt` 文件。所有队友都把这个文件加入 Git 仓库，确保大家用同一版本的依赖。不同操作系统、不同电脑，环境始终一致。

### 理由 2：避免误删和灾难

你的队友不小心运行了 `rm -rf`，删除了 project 文件夹中的代码？不用慌！Git 存了所有历史记录，随时可以恢复。

没有 Git，一旦文件被删了，就找不回来了。有 Git，你可以像时间旅行一样回到任何时间点。

### 理由 3：团队代码审查（Code Review）

假设你写完了一个新功能，但你不敢直接把它合并到主代码里，因为害怕有 Bug。

**Git 的解决方案**：通过 GitHub 的 Pull Request 功能，队友可以先查看你的改动，提出意见，确认没问题后才合并。这叫 Code Review，是专业团队必须的流程。

### 理由 4：追踪代码改动的历史

你的 API 突然出现了 Bug，但不知道是谁改的。Git 可以告诉你：

```
谁改的？Alice
什么时候改的？2024-03-15
为什么改的？修复用户登录流程
改了什么？app.py 的第 45-60 行
```

这对 Debug 和团队沟通都很重要。

---

## 1.3 环境搭建（一次性工作）

好消息：环境搭建只需要做一次。之后你就可以一直用 Git 开发 Python 项目，不需要重复配置。

### 步骤 1：安装 Git

**选择你正在使用的操作系统：**

=== "Windows"

    **方法 A：使用 Git for Windows（推荐）**
    
    1. 访问 [https://git-scm.com/download/win](https://git-scm.com/download/win)
    2. 点击下载最新版本（通常自动下载）
    3. 打开下载的 `.exe` 文件
    4. 一路点击 **Next**，保持默认设置不变（除非你知道什么是 "core.autocrlf"，否则别改）
    5. 点击 **Install** 完成安装
    
    **验证安装成功：**
    
    1. 按 **Win + R**，输入 `cmd` 并按 Enter，打开命令行
    2. 输入 `git --version`
    3. 应该看到输出：`git version 2.xx.x` 之类的版本号
    
    如果看到版本号，说明安装成功了！🎉

=== "macOS"

    **方法 A：使用 Homebrew（推荐）**
    
    1. 打开 **Terminal** 应用（在 Application → Utilities 中）
    2. 如果没装 Homebrew，先运行：
       ```bash
       /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
       ```
    3. 安装 Git：
       ```bash
       brew install git
       ```
    4. 等待安装完成（可能需要 2-5 分钟）
    
    **方法 B：从官方下载**
    
    1. 访问 [https://git-scm.com/download/mac](https://git-scm.com/download/mac)
    2. 下载 `.dmg` 文件
    3. 打开文件，按照安装向导操作
    
    **验证安装成功：**
    
    1. 打开 **Terminal**
    2. 键入 `git --version`
    3. 应该看到输出：`git version 2.xx.x` 之类的版本号
    
    如果看到版本号，说明安装成功了！🎉

---

### 步骤 2：配置 Git 身份

现在 Git 已经安装了，但 Git 还不知道你是谁。你需要告诉 Git 你的名字和邮箱，这样每次提交代码时，Git 就知道是 "谁" 提交的了。

💭 **为什么需要这个？** 团队协作时，队友看历史记录会知道 "Alice 改了这行"、"Bob 改了那行"，这对责任清晰和 Code Review 很重要。

**配置命令：**

打开你的命令行（Windows 的 cmd 或 PowerShell，macOS 的 Terminal），输入以下两行（注意把引号里的内容替换成你自己的）：

```bash
# 配置你的名字（建议用真名或常用的开发者名字）
git config --global user.name "Your Name"

# 配置你的邮箱（建议用常用的邮箱）
git config --global user.email "your.email@example.com"
```

**例如：**

```bash
git config --global user.name "Alice Chen"
git config --global user.email "alice@example.com"
```

**验证配置成功：**

输入以下命令查看你刚才配置的信息：

```bash
# 查看名字
git config --global user.name

# 查看邮箱
git config --global user.email
```

如果能看到你刚才输入的内容，就证明配置成功了！✅

!!! note "提醒"
    这个配置是 "全局" 设置（`--global` 表示对整个电脑有效）。以后你创建的每一个 Git 项目都会自动使用这个身份。

---

### 步骤 3（可选）：配置 Git 代理（特定网络环境下需要）

在某些网络环境（如公司内网、校园网、或某些地区）下，直接访问 GitHub 可能会很慢或无法连接。这时你需要为 Git 配置代理服务器。

#### 什么情况需要配置代理？

- 访问 GitHub 时提示 `Failed to connect` 或 `Connection timed out`
- `git clone` 或 `git push` 时速度极慢或卡住不动
- 你所在的网络需要使用代理才能访问外网

#### 如何配置 HTTP/HTTPS 代理

如果你有一个 HTTP 代理服务器（如 `http://127.0.0.1:7890`），运行以下命令：

```bash
# 设置 HTTP 代理
git config --global http.proxy http://127.0.0.1:7890

# 设置 HTTPS 代理（GitHub 默认使用 HTTPS）
git config --global https.proxy http://127.0.0.1:7890
```

!!! tip "如何找到代理地址"
    - 如果你使用 Clash/V2Ray 等工具，代理地址通常是 `http://127.0.0.1:7890` 或 `http://127.0.0.1:1080`
    - 如果你使用公司代理，请向 IT 部门询问代理服务器地址和端口
    - Windows 用户可以在「设置 → 网络和 Internet → 代理」中查看系统代理设置

#### 如何配置 SOCKS5 代理

如果你的代理使用 SOCKS5 协议（如 Shadowsocks），Git 不直接支持 SOCKS5，但可以通过以下方式转换：

**方法 1：使用 ncat/socat 转换（推荐）**

先安装 ncat（通常随 Git for Windows 安装），然后配置：

```bash
# 使用 socks5h 协议（注意 Git 2.11+ 支持 socks5h）
git config --global http.proxy socks5h://127.0.0.1:1080
git config --global https.proxy socks5h://127.0.0.1:1080
```

**方法 2：仅对 GitHub 配置代理**

如果你只想让 GitHub 走代理，其他网站不走：

```bash
# 只对 github.com 使用代理
git config --global http.https://github.com.proxy http://127.0.0.1:7890
git config --global https.https://github.com.proxy http://127.0.0.1:7890
```

#### 验证代理是否生效

```bash
# 查看所有配置
git config --global -l

# 你应该能看到类似这样的输出：
# http.proxy=http://127.0.0.1:7890
# https.proxy=http://127.0.0.1:7890
```

#### 取消代理设置

如果你需要取消代理（比如换了网络环境）：

```bash
# 取消 HTTP/HTTPS 代理
git config --global --unset http.proxy
git config --global --unset https.proxy

# 取消特定网站的代理
git config --global --unset http.https://github.com.proxy
git config --global --unset https.https://github.com.proxy
```

!!! warning "注意"
    代理配置是全局的，会影响你所有的 Git 仓库。如果你只在特定网络需要代理，离开该网络后记得取消代理设置，否则会导致 Git 无法连接。

---

## 1.4 安装与配置 VSCode（推荐但可选）

VSCode 是一个代码编辑器，并且内置了强大的 Git 支持。接下来的所有章节中，我们会提供 "两种方式"：命令行方式 和 VSCode 图形界面方式。

### 为什么推荐用 VSCode？

- 🖱️ **图形界面更直观**：可以直观地看到文件改动、历史记录
- 🖱️ **减少命令行恐惧**：不需要记住复杂的 Git 命令
- 🖱️ **集成度高**：Git、Python、终端都在一个窗口里
- 🖱️ **学习曲线平缓**：点一下按钮就能完成操作，降低学习难度

**可选性**：如果你已经有其他顺手的编辑器（如 PyCharm、Sublime），也可以跳过这一步。

### 安装 VSCode

1. 访问 [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. 点击大按钮下载（它会自动检测你的操作系统）
3. 打开下载的文件，按照安装向导完成
4. 打开 VSCode

### 找到源代码管理面板

在 VSCode 窗口左侧，你会看到一排竖向的图标。点击看起来像 **分叉树干** 的图标（第 3 个或第 4 个），那就是 **"源代码管理"** 面板。

!!! tip "如何找到源代码管理？"
    - 快捷键：按 **Ctrl+Shift+G**（Windows）或 **Cmd+Shift+G**（macOS）
    - 或者：在左侧图标栏找到分叉树干的图标 🌳

### 验证 VSCode 的 Git 支持是否正常

VSCode 内置了 Git 支持，不需要安装额外插件。让我们验证一下它是否正确识别了你安装的 Git：

1. 点击左侧面板的 **"源代码管理"** 图标（分叉树干图标）
2. 如果看到类似这样的界面，说明 Git 支持已正常工作：
   - 显示 "没有打开的文件夹" 或 "初始化仓库" 按钮
   - 顶部没有红色的错误提示

3. **检查 Git 是否被正确识别**：
   - 按 **Ctrl+Shift+P**（Windows）或 **Cmd+Shift+P**（macOS）打开命令面板
   - 输入 `Git: Show` 并选择 **"Git: 显示输出"**
   - 在底部面板中，你应该能看到 Git 的版本信息和日志输出

!!! success "如果看到 Git 版本号"
    这说明 VSCode 已经成功找到了你安装的 Git，可以正常使用所有 Git 功能了。

!!! warning "如果提示 'Git not found' 或 '未找到 Git'"

    这可能是因为：

    1. Git 没有正确安装 —— 返回步骤 1 重新安装 Git

    2. Git 没有添加到系统路径 —— 重启 VSCode 或电脑后再试

    3. 需要手动指定 Git 路径 —— 按 **Ctrl+Shift+P**，搜索 `settings`，打开设置，搜索 `git.path`，添加你的 Git 安装路径（如 `C:\Program Files\Git\bin\git.exe`）

---

现在你已经知道 Git 的两种界面了：
- **命令行界面**：输入命令的方式
- **VSCode 界面**：点击按钮的方式

接下来的章节中，我们会经常对比这两种方式。

---

## 1.5 现在你已经准备好了！👏

恭喜！你已经完成了环境搭建。现在你的电脑上已经有了：

✅ **Git** —— 版本控制工具  
✅ **Git 身份配置** —— Git 知道你是谁  
✅ **VSCode**（可选）—— 友好的界面  
✅ **Git 可视化插件**（可选）—— 更直观地理解代码历史  

### 接下来呢？

进入 **第 2 章**，我们将开始实操：如何在你的电脑上创建第一个 Git 项目，记录第一次代码改动，以及学习 Python 开发者必须知道的 `.gitignore` 文件。

在那一章里，你会亲手操作 Git，从 "纸上谈兵" 变成 "真刀实枪"。

---

## 📚 参考资源

- [Git 官方文档](https://git-scm.com/doc)
- [GitHub 新手指南](https://guides.github.com/activities/hello-world/)
- [Git 速查表](https://education.github.com/git-cheat-sheet-education.pdf)
