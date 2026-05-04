# 第5章：用户与权限 —— 房间的"钥匙和锁"

## 🔐 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 理解Linux用户系统，掌握权限管理，学会安全使用sudo |
| **核心比喻** | **钥匙和锁** |
| **预计时长** | 55分钟 |
| **核心命令** | `whoami`, `id`, `chmod`, `chown`, `sudo` |
| **实践任务** | 创建只读文件，给自己开放写入权限 |

---

## 5.1 Linux用户：你是这个房间的主人

**比喻理解：**  
想象一栋公寓大楼：
- **root用户** = 房东 — 拥有整栋楼的万能钥匙，可以进入任何房间，做任何事
- **普通用户** = 房客 — 只能进入自己的房间，使用自己的东西
- **系统用户** = 物业工作人员 — 负责特定服务（如邮件、数据库），不住在楼里

### 👤 查看当前用户

**命令：** `whoami`
```bash
$ whoami
yourname
```
显示你当前登录的用户名。

**命令：** `id`
```bash
$ id
uid=1000(yourname) gid=1000(yourname) groups=1000(yourname),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),120(lpadmin),131(lxd),132(sambashare)
```
显示详细的用户信息：
- `uid` — 用户ID（你的身份证号）
- `gid` — 主组ID（你所属的主要家庭）
- `groups` — 你所属的所有组（你能进的房间）

### 🏠 用户的家目录

每个用户都有自己的"家"（home directory）：
- 普通用户：`/home/用户名` — 如 `/home/yourname`
- root用户：`/root` — 房东的私人办公室

**查看家目录：**
```bash
$ echo $HOME
/home/yourname

$ cd ~
$ pwd
/home/yourname
```

### 👥 用户类型详解

| 用户类型 | UID范围 | 用途 | 比喻 |
|:---|:---|:---|:---|
| **root** | 0 | 系统管理员 | 房东 |
| **系统用户** | 1-999 | 运行系统服务 | 物业工作人员 |
| **普通用户** | 1000+ | 日常使用 | 房客 |

**为什么普通用户从1000开始？**  
因为0-999预留给系统和特殊服务，避免冲突。

---

## 5.2 权限系统：读（R）、写（W）、执行（X）就像钥匙权限

**比喻理解：**  
每个文件/目录都有三把锁：
- **读锁（R）** — 能看房间里的东西
- **写锁（W）** — 能往房间里放东西或拿走东西
- **执行锁（X）** — 能进房间（对目录）或运行程序（对文件）

### 🔍 查看文件权限

**命令：** `ls -l`
```bash
$ ls -la
总用量 48
drwxr-xr-x 2 yourname yourname 4096 5月   3 11:30 Desktop
-rw-r--r-- 1 yourname yourname  220 5月   3 11:30 .bash_logout
-rw-r--r-- 1 yourname yourname 3771 5月   3 11:30 .bashrc
```

**权限字符串解析：**
```
-rw-r--r--
│└┬┘└┬┘└┬┘
│ │  │  │
│ │  │  └── 其他用户的权限
│ │  └───── 所属组的权限
│ └──────── 文件所有者的权限
└────────── 文件类型（-表示普通文件，d表示目录）
```

**权限字符含义：**

| 字符 | 含义 | 数字值 | 比喻 |
|:---|:---|:---:|:---|
| `r` | 读（Read） | 4 | 能看房间里的东西 |
| `w` | 写（Write） | 2 | 能放东西或拿走东西 |
| `x` | 执行（eXecute） | 1 | 能进房间/运行程序 |
| `-` | 无权限 | 0 | 锁着，进不去 |

### 📊 权限组合示例

| 权限字符串 | 数字表示 | 含义 |
|:---|:---:|:---|
| `rwxrwxrwx` | 777 | 所有人都有读写执行权限（危险！） |
| `rw-r--r--` | 644 | 所有者可读写，其他人只读 |
| `rwxr-xr-x` | 755 | 目录：所有者可读写执行，其他人可读执行 |
| `rwx------` | 700 | 只有所有者能访问（私密文件） |
| `r--r--r--` | 444 | 所有人只读（系统配置文件） |

**数字权限计算方法：**
```
所有者权限 + 组权限 + 其他用户权限

rwx = 4+2+1 = 7
rw- = 4+2+0 = 6
r-- = 4+0+0 = 4
r-x = 4+0+1 = 5

所以 755 = rwxr-xr-x
```

---

## 5.3 权限修改命令：给文件加锁/解锁

### 🔧 1. `chmod` — 修改权限（换锁）

**全称：** Change Mode（改变模式）  
**作用：** 修改文件或目录的权限  
**比喻：** 给文件换一把新锁，或者调整锁的权限

**语法：**
```bash
chmod [选项] 权限 文件名
```

**数字方式设置权限：**
```bash
# 设置文件为所有者可读写，其他人只读（644）
$ chmod 644 myfile.txt

# 设置目录为所有者可读写执行，其他人可读执行（755）
$ chmod 755 mydirectory/

# 设置文件为只有所有者可访问（700）
$ chmod 700 secret.txt
```

**符号方式设置权限：**

| 符号 | 含义 |
|:---|:---|
| `u` | 用户（所有者） |
| `g` | 组 |
| `o` | 其他用户 |
| `a` | 所有人（all） |
| `+` | 添加权限 |
| `-` | 移除权限 |
| `=` | 设置权限 |

**示例：**
```bash
# 给所有者添加执行权限
$ chmod u+x script.sh

# 移除组的写权限
$ chmod g-w myfile.txt

# 设置其他用户只有读权限
$ chmod o=r myfile.txt

# 给所有人添加读权限
$ chmod a+r myfile.txt

# 递归修改目录及其内容的权限
$ chmod -R 755 mydirectory/
```

### 🏷️ 2. `chown` — 修改所有者（换房主）

**全称：** Change Owner（改变所有者）  
**作用：** 修改文件或目录的所有者  
**比喻：** 把房间的房契转给别人

**语法：**
```bash
chown [选项] 新所有者:新组 文件名
```

**示例：**
```bash
# 将文件所有者改为root（需要sudo）
$ sudo chown root myfile.txt

# 将文件所有者和组都改为root
$ sudo chown root:root myfile.txt

# 只修改组
$ sudo chown :users myfile.txt

# 递归修改目录及其内容
$ sudo chown -R yourname:yourname mydirectory/
```

**注意：** 修改所有者通常需要root权限，所以要用 `sudo`。

---

## 5.4 sudo：临时借房东的万能钥匙

**全称：** Superuser Do（以超级用户身份执行）  
**作用：** 临时获得root权限执行命令  
**比喻：** 房客向房东借万能钥匙，做完事立即归还

### 🗝️ 为什么需要sudo？

**场景：** 你想在系统目录（如 `/usr/bin`）安装软件，但普通用户没有权限。

**错误尝试：**
```bash
$ apt install vim
E: Could not open lock file /var/lib/dpkg/lock-frontend - open (13: Permission denied)
E: Unable to acquire the dpkg frontend lock
```

**正确做法：**
```bash
$ sudo apt install vim
[sudo] password for yourname:  # 输入你的密码
# 成功安装！
```

### ⚠️ sudo使用安全原则

1. **只在必要时使用sudo**  
   就像只在必要时才借房东的钥匙

2. **输入密码时注意隐私**  
   输入密码时不会显示任何字符（连*都没有），这是正常的

3. **sudo有超时机制**  
   输入密码后，15分钟内再次使用sudo不需要重复输入密码

4. **不要滥用sudo**  
   特别是 `sudo rm -rf /` 这样的危险命令

### 🚫 危险命令警告

**绝对不要运行的命令：**
```bash
sudo rm -rf /          # 删除整个系统！
sudo rm -rf /*         # 同上！
sudo rm -rf ~          # 删除你的家目录！
sudo chmod -R 777 /      # 给所有文件777权限（系统崩溃）
sudo chown -R yourname /  # 把所有文件所有者改成你（系统崩溃）
```

**为什么危险？**
- Linux假设你知道自己在做什么
- 没有"确认删除"对话框
- 删除后很难恢复

---

## 🛠️ 实践任务：创建只读文件，然后给自己开放写入权限

### 任务目标

理解权限的工作机制，练习 `chmod` 命令。

### 步骤1：创建测试文件

```bash
$ cd ~
$ mkdir PermissionTest
$ cd PermissionTest
$ echo "This is a secret message." > secret.txt
$ ls -l secret.txt
-rw-r--r-- 1 yourname yourname 27 5月   3 14:30 secret.txt
```

当前权限：`rw-r--r--`（644）
- 所有者可读写
- 组只读
- 其他人只读

### 步骤2：移除所有写权限（变成只读）

```bash
$ chmod 444 secret.txt
$ ls -l secret.txt
-r--r--r-- 1 yourname yourname 27 5月   3 14:30 secret.txt
```

现在所有人都是只读权限。

### 步骤3：尝试写入（会失败）

```bash
$ echo "New content" >> secret.txt
bash: secret.txt: Permission denied
```

**失败原因：** 文件现在是只读的，即使是所有者也不能写入。

### 步骤4：给自己恢复写权限

```bash
$ chmod u+w secret.txt
$ ls -l secret.txt
-rw-r--r-- 1 yourname yourname 27 5月   3 14:30 secret.txt
```

现在所有者又有了写权限。

### 步骤5：验证写入成功

```bash
$ echo "New content" >> secret.txt
$ cat secret.txt
This is a secret message.
New content
```

**成功！**

### 步骤6：设置更安全的权限

```bash
# 设置只有自己能读写，其他人只读（适合个人文档）
$ chmod 644 secret.txt

# 设置只有自己能访问（适合私密文件）
$ chmod 600 very_secret.txt

# 验证
$ ls -l
-rw-r--r-- 1 yourname yourname  27 5月   3 14:30 secret.txt
-rw------- 1 yourname yourname   0 5月   3 14:35 very_secret.txt
```

### 步骤7：清理

```bash
$ cd ~
$ rm -rf PermissionTest
```

---

## 💡 第五章要点总结

✅ **用户类型**：
  - root = 房东（万能钥匙）
  - 普通用户 = 房客（自己的房间钥匙）
  - 系统用户 = 物业工作人员（服务专用）

✅ **权限三要素**：
  - `r`（读）= 4 — 能看
  - `w`（写）= 2 — 能改
  - `x`（执行）= 1 — 能运行/进入

✅ **权限表示**：
  - 字符串：`rwxr-xr-x`
  - 数字：`755`
  - 三组：所有者、组、其他用户

✅ **修改权限**：
  - `chmod` — 换锁（修改权限）
  - `chown` — 换房主（修改所有者）

✅ **sudo使用**：
  - 临时借用root权限
  - 谨慎使用，只在必要时
  - 绝对不要运行危险命令

✅ **安全原则**：
  - 最小权限原则：只给必要的权限
  - 重要文件设为600（只有自己能访问）
  - 脚本文件设为755（可执行但受控）

---

## 📝 小练习

1. **权限计算练习**  
   计算以下权限的数字表示：
   ```
   rwxr-xr-x = ?
   rw-r--r-- = ?
   rwx------ = ?
   r--r--r-- = ?
   ```

2. **权限设置练习**  
   创建文件并设置不同权限：
   ```bash
   touch test1.txt test2.txt test3.txt
   chmod 755 test1.txt
   chmod 644 test2.txt
   chmod 700 test3.txt
   ls -l test*.txt
   ```
   观察权限字符串的变化。

3. **sudo体验**  
   ```bash
   # 查看当前用户
   whoami
   
   # 查看root用户的家目录（需要sudo）
   sudo ls -la /root
   
   # 输入你的密码
   ```

4. **思考题**  
   为什么 `chmod 777` 是危险的？在什么情况下你会使用 `sudo`？

---

## 🚪 下一章预告

在第六章，我们将学习**实用技巧和进阶工具**。现在你已经掌握了Linux的基础，是时候学习如何更高效地使用它了。

**核心比喻：智能管家**  
- Tab补全 = 智能输入提示  
- 命令历史 = 对话记录本  
- 管道 `|` = 流水线传送带  
- 脚本 = 管家任务清单

👉 [进入第6章：实用技巧与下一步](chapter6.md)