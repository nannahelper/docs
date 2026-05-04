# 第4章：文件操作 —— 整理你的“数字抽屉”

## 🗄️ 本章概览

| 项目 | 内容 |
|:---|:---|
| **学习目标** | 掌握文件的创建、删除、复制、移动、查看等基本操作 |
| **核心比喻** | **房间和抽屉** |
| **预计时长** | 65分钟 |
| **核心命令** | `mkdir`, `touch`, `rm`, `cp`, `mv`, `cat`, `less` |
| **实践任务** | 创建个人资料抽屉并整理文件 |

---

## 4.1 文件系统树：房间→抽屉→文件夹→文件

**比喻理解：**  
想象一个巨大的图书馆：
- **根目录 `/`** = 图书馆的地基和主结构
- **`/home`** = 读者区，每个读者有自己的书架
- **`/home/yourname`** = 你的专属书架（家目录）
- **`Documents`** = 书架上专门放文档的抽屉
- **`report.txt`** = 抽屉里的一份具体文件

### 🌳 Linux文件系统层次结构

```
/ (根目录，图书馆地基)
├── bin (基本工具，像图书馆的公共设施)
├── etc (配置文件，图书馆的管理规则)
├── home (读者区)
│   ├── alice (Alice的书架)
│   ├── bob (Bob的书架)
│   └── yourname (你的书架)
│       ├── Documents (文档抽屉)
│       ├── Pictures (图片抽屉)
│       ├── Music (音乐抽屉)
│       └── Downloads (下载临时区)
├── tmp (临时区，公共休息区)
└── var (变化数据，图书馆的借阅记录)
```

### 📍 重要目录再认识

让我们在家目录里看看实际结构：
```bash
$ cd ~
$ ls -l
```
你可能看到：
```
drwxr-xr-x 2 yourname yourname 4096 4月  30 10:23 Desktop
drwxr-xr-x 2 yourname yourname 4096 4月  30 10:23 Documents
drwxr-xr-x 2 yourname yourname 4096 4月  30 10:23 Downloads
drwxr-xr-x 2 yourname yourname 4096 4月  30 10:23 Music
drwxr-xr-x 2 yourname yourname 4096 4月  30 10:23 Pictures
drwxr-xr-x 2 yourname yourname 4096 4月  30 10:23 Public
drwxr-xr-x 2 yourname yourname 4096 4月  30 10:23 Templates
drwxr-xr-x 2 yourname yourname 4096 4月  30 10:23 Videos
```

**注意开头的 `d`**：  
- `d` = 目录（directory）— 就像一个抽屉
- `-` = 普通文件 — 就像抽屉里的一张纸

---

## 4.2 创建与删除：买抽屉和扔废纸

### 📁 1. `mkdir` — 买个新抽屉

**全称：** Make Directory（创建目录）  
**作用：** 创建一个新的目录（文件夹）  
**比喻：** 在书架上增加一个新的抽屉

**基本用法：**
```bash
$ mkdir 目录名
```

**示例：创建个人资料抽屉**
```bash
$ cd ~
$ mkdir MyPersonalFiles
$ ls
```
你会看到新增了 `MyPersonalFiles` 目录。

**创建多级目录：**
```bash
$ mkdir -p Projects/2026/LinuxTutorial/notes
```
`-p` 选项表示创建多级目录（parent），如果中间目录不存在会自动创建。

**检查创建结果：**
```bash
$ ls -la MyPersonalFiles/
总用量 8
drwxr-xr-x 2 yourname yourname 4096 5月   3 11:30 .
drwxr-xr-x 19 yourname yourname 4096 5月   3 11:30 ..
```
- `.` = 当前目录（MyPersonalFiles）
- `..` = 上级目录（你的家目录）

### 📄 2. `touch` — 放一张空白纸

**作用：** 创建一个空文件，或者更新文件的访问时间  
**比喻：** 在抽屉里放一张空白的纸，准备写东西

**基本用法：**
```bash
$ touch 文件名
```

**示例：创建几个文件**
```bash
$ cd MyPersonalFiles
$ touch todo.txt
$ touch notes.md
$ touch ideas.txt
$ ls -l
```
你会看到三个大小为0的空文件。

**为什么叫"touch"？**  
想象你用手指轻轻触碰一下文件，更新它的“最后修改时间”。

### 🗑️ 3. `rm` — 扔掉废纸 ⚠️小心使用！

**全称：** Remove（删除）  
**作用：** 删除文件或目录  
**比喻：** 把废纸扔进垃圾桶  
**警告：** Linux没有回收站！删除后很难恢复！

**删除文件：**
```bash
$ rm 文件名
```

**示例：删除不需要的文件**
```bash
$ ls
todo.txt  notes.md  ideas.txt
$ rm ideas.txt
$ ls
todo.txt  notes.md
```

**安全删除（推荐给新手）：**
```bash
$ rm -i todo.txt
```
`-i` 选项会询问确认：`rm：是否删除普通文件 'todo.txt'?`  
输入 `y` 确认删除，`n` 取消。

**删除目录：**
```bash
$ rm -r 目录名
```
`-r` 表示递归删除（删除目录及其所有内容）

**⚠️ 危险命令（不要尝试！）**
```bash
rm -rf /      # 删除整个系统！绝对不要运行！
rm -rf ~      # 删除你的所有家目录文件！
```

**安全建议：**
1. 删除前先用 `ls` 确认文件名
2. 尽量使用 `-i` 选项让系统询问
3. 重要文件先备份再删除
4. 新手不要在root用户下使用rm

---

## 4.3 复制与移动：复印文件和搬动文件

### 🖨️ 1. `cp` — 复印一份文件

**全称：** Copy（复制）  
**作用：** 复制文件或目录  
**比喻：** 用复印机复印一份文件

**复制文件：**
```bash
$ cp 源文件 目标文件
```

**示例：备份todo列表**
```bash
$ cp todo.txt todo_backup.txt
$ ls
todo.txt  todo_backup.txt  notes.md
```

**复制目录（需要加 `-r`）：**
```bash
$ cp -r MyPersonalFiles MyPersonalFiles_backup
```
`-r` 表示递归复制（复制整个目录树）

**常用选项：**

| 选项 | 作用 | 示例 |
|:---|:---|:---|
| `cp -i` | 覆盖前询问 | `cp -i file1 file2` |
| `cp -v` | 显示详细过程 | `cp -v source dest` |
| `cp -u` | 只更新较新的文件 | `cp -u old new` |

### 🚚 2. `mv` — 把文件搬到另一个抽屉（或重命名）

**全称：** Move（移动）  
**作用：** 移动文件/目录 或 重命名文件/目录  
**比喻：** 把文件从一个抽屉搬到另一个抽屉，或者给文件贴新标签

**移动文件：**
```bash
$ mv 源文件 目标目录/
```

**示例：整理文件到不同目录**
```bash
$ mkdir Documents
$ mv todo.txt Documents/
$ mv notes.md Documents/
$ ls
Documents  todo_backup.txt
$ ls Documents/
todo.txt  notes.md
```

**重命名文件：**
```bash
$ mv 旧文件名 新文件名
```

**示例：给备份文件改名**
```bash
$ mv todo_backup.txt old_todo.txt
$ ls
Documents  old_todo.txt
```

**注意：** `mv` 既是移动也是重命名，取决于第二个参数：
- 如果第二个参数是已存在的目录 → 移动
- 如果第二个参数是不存在的路径 → 重命名

---

## 4.4 查看文件内容：快速一瞥或慢慢阅读

### 👀 1. `cat` — 快速看一眼文件内容

**全称：** Concatenate（连接）  
**作用：** 连接并显示文件内容（适合短文件）  
**比喻：** 快速瞥一眼纸条上的内容

**查看短文件：**
```bash
$ cat 文件名
```

**示例：查看todo列表**
```bash
$ cd Documents
$ cat todo.txt
Learn Linux commands
Practice file operations
Backup important files
```

**连接多个文件：**
```bash
$ cat file1.txt file2.txt > combined.txt
```

**显示行号：**
```bash
$ cat -n todo.txt
1 Learn Linux commands
2 Practice file operations
3 Backup important files
```

### 📖 2. `less` — 慢慢翻页看长文件

**作用：** 分页查看文件内容（适合长文件）  
**比喻：** 用书签慢慢读一本厚书

**查看长文件：**
```bash
$ less 文件名
```

**`less` 的导航键：**

| 按键 | 作用 |
|:---|:---|
| **空格** 或 **f** | 向下翻一页 |
| **b** | 向上翻一页 |
| **回车** 或 **↓** | 向下翻一行 |
| **↑** | 向上翻一行 |
| **/** | 搜索（输入关键词后按回车） |
| **n** | 跳转到下一个搜索结果 |
| **N** | 跳转到上一个搜索结果 |
| **q** | 退出less |

**示例：查看系统日志**
```bash
$ less /var/log/syslog
```

### 📄 3. `head` 和 `tail` — 看文件的头尾

**作用：**
- `head`：显示文件开头几行
- `tail`：显示文件末尾几行

**查看文件前5行：**
```bash
$ head -5 文件名
```

**查看文件后10行：**
```bash
$ tail -10 文件名
```

**实时查看日志文件（常用）：**
```bash
$ tail -f /var/log/syslog
```
`-f` 表示跟随（follow），文件有新内容时会自动显示。

---

## 🛠️ 实践任务：创建你的“个人资料抽屉”并整理文件

### 任务目标：模拟真实文件整理场景

**场景设定：**  
你刚安装了Linux，需要整理个人文件。你要创建合理的目录结构，将不同类型的文件归类存放。

**步骤1：创建目录结构**
```bash
$ cd ~
$ mkdir -p Personal/{Documents,Photos,Music,Projects}
$ ls Personal/
Documents  Music  Photos  Projects
```

**步骤2：创建一些示例文件**
```bash
$ cd Personal/Documents
$ touch todo.txt lecture_notes.txt shopping_list.txt
$ echo "1. Learn Linux" > todo.txt
$ echo "2. Backup files" >> todo.txt  # >> 表示追加内容
$ echo "3. Install software" >> todo.txt
```

**步骤3：整理文件**
```bash
# 创建子目录
$ mkdir Work Study Personal

# 移动文件到对应目录
$ mv todo.txt Work/
$ mv lecture_notes.txt Study/
$ mv shopping_list.txt Personal/

# 检查结果
$ ls Work/
todo.txt
$ cat Work/todo.txt
```

**步骤4：备份重要文件**
```bash
$ cp -r Personal Personal_backup_$(date +%Y%m%d)
$ ls
Personal  Personal_backup_20260503
```

**步骤5：清理临时文件**
```bash
# 创建一个临时文件
$ touch temp_file.txt
$ ls
Personal  Personal_backup_20260503  temp_file.txt

# 安全删除
$ rm -i temp_file.txt
rm：是否删除普通文件 'temp_file.txt'? y
```

---

## 💡 第四章要点总结

✅ **文件系统是树形结构** — 像图书馆的书架和抽屉  
✅ **创建操作**：
  - `mkdir` — 创建目录（新抽屉）
  - `touch` — 创建空文件（空白纸）
✅ **删除操作**：
  - `rm` — 删除文件（⚠️小心使用！）
  - `rm -i` — 安全删除（询问确认）
✅ **复制移动**：
  - `cp` — 复制文件（复印）
  - `mv` — 移动/重命名文件（搬动/贴新标签）
✅ **查看内容**：
  - `cat` — 快速查看（瞥一眼）
  - `less` — 分页查看（慢慢读）
  - `head`/`tail` — 查看头尾
✅ **你已经能**：在Linux里整理自己的数字文件

---

## 📝 小练习

1. **文件整理挑战**  
   完成以下任务：
   ```
   1. 在家目录创建 Archives/2026/May 目录结构
   2. 在May目录创建3个文本文件：week1.txt, week2.txt, week3.txt
   3. 在每个文件里写一行内容（如 echo "Week 1 notes" > week1.txt）
   4. 复制整个May目录到Backups目录
   5. 重命名week1.txt为first_week.txt
   6. 查看first_week.txt的内容
   7. 安全删除week2.txt（用-i选项）
   ```

2. **命令记忆卡（新增）**  
   扩充你的命令表格：

   | 命令 | 作用 | 生活比喻 |
   |:---|:---|:---|
   | `mkdir` | 创建目录 | 买个新抽屉 |
   | `touch` | 创建空文件 | 放一张空白纸 |
   | `rm` | 删除文件 | 扔掉废纸 ⚠️ |
   | `cp` | 复制文件 | 复印一份 |
   | `mv` | 移动/重命名 | 搬动文件/贴新标签 |
   | `cat` | 查看文件内容 | 快速瞥一眼 |
   | `less` | 分页查看 | 慢慢翻书 |

3. **安全习惯养成**  
   记住这三个安全习惯：
   ```
   1. 删除前先ls确认文件名
   2. 尽量用 rm -i 而不是 rm
   3. 重要文件先备份再操作
   ```

---

## 🚪 下一章预告

在第五章，我们将学习**用户与权限管理**。现在你会整理文件了，但Linux里还有“钥匙和锁”的概念——不同用户对文件有不同的访问权限。

**核心比喻：钥匙和锁**  
- 用户 = 钥匙持有人  
- 权限 = 锁的类型  
- root用户 = 房东（万能钥匙）  
- sudo = 临时借用万能钥匙

👉 [进入第5章：用户与权限](chapter5.md)