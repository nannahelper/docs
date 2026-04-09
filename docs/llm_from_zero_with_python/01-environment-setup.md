# 第一章：环境准备——搭建你的"武器库"

在写代码之前，我们需要先装好两样东西：**代码编辑器（VSCode）** 和 **Python 解释器**。

---

## 1. 为什么选 VSCode？

市面上有很多 AI 辅助编程工具，让我们先认识一下：

| 工具 | 特点 | 适合谁 |
|------|------|--------|
| **Cursor** | AI 原生编辑器，代码补全极强 | 有一定经验的开发者 |
| **GitHub Copilot** | VS Code 插件，微软出品 | 已会编程的用户 |
| **Trae CN** | 字节跳动出品，中文优化 | 国内用户 |
| **Claude Code** | Anthropic 出品，终端原生 | 高级开发者 |
| **VSCode** | 通用编辑器，生态最成熟 | ✅ **本课程选择** |

!!! info "为什么选择VSCode？"
    - VScode开源，很多AI辅助开发代码的IDE就是基于VSCode；
    - VSCode有着丰富的插件，可以按照自己的需求随心添加删除；
    - **本文作者常用VSCode。**

---


## 2. 下载与安装 VSCode

!!! tip "区分 VSCode 和 Visual Studio"
    **VSCode**（Visual Studio Code）是微软出品的**轻量级代码编辑器**，完全免费开源。
    
    **Visual Studio**（不带 Code）是微软的**企业级 IDE**，功能更强大但更笨重，主要用于 C#/.NET 开发。
    
    本课程使用的是 **VSCode**，需要从 `https://code.visualstudio.com` 下载。



=== "Windows"

    1. 打开浏览器，访问 [https://code.visualstudio.com](https://code.visualstudio.com)
    2. 点击蓝色大按钮 **"Download for Windows"**
    3. 下载完成后双击 `.exe` 安装包
    4. 安装过程中，**务必勾选以下两项**：
        - ☑️ `将"通过 Code 打开"操作添加到 Windows 资源管理器文件上下文菜单`
        - ☑️ `添加到 PATH（重启后生效）`
    5. 点击"安装"，等待进度条完成

    ![VSCode Windows 安装界面](assets/vscode-install-windows.png)

=== "macOS"

    1. 访问 [https://code.visualstudio.com](https://code.visualstudio.com)
    2. 点击 **"Download for Mac"**（会自动识别你的芯片：Intel 或 Apple Silicon）
    3. 下载后解压 `.zip`，将 `Visual Studio Code.app` 拖入 **应用程序** 文件夹
    4. 从启动台打开 VSCode
    5. 按 `Cmd+Shift+P`，搜索 `Shell Command: Install 'code' command in PATH`，回车

    ![VSCode macOS 安装界面](assets/vscode-install-macos.png)

**验证安装成功：** 打开 VSCode，看到欢迎界面说明安装完成 ✅

---

## 3. 安装 Python 插件

VSCode 本身只是一个文本编辑器，需要安装插件才能"理解" Python 代码。

插件就像手机 App——安装 Python 插件后，VSCode 就能：

- 🎨 **让代码变为彩色，可以进一步辨识不同代码内容**（语法高亮）
- 💡 **自动补全后续代码**（输入几个字母就提示剩余部分）
- 🔴 **即时报错提示**（写错字符会立刻下划线标红，“预判”错误）

**安装步骤：**

1. 点击左侧边栏的 **扩展图标**（四个方块的图标），或按 `Ctrl+Shift+X`
2. 在搜索框输入 `Python`
3. 找到 **Microsoft** 发布的 `Python` 插件（蓝色微软图标）
4. 点击 **安装**

![VSCode Python 插件安装](assets/vscode-python-extension.png)

!!! tip "关于汉化插件的建议"
    **作者不建议安装汉化插件。** 理由如下：
    
    - 🌐 VSCode 的英文界面是官方标准，部分汉化翻译存在歧义或滞后
    - 🔧 遇到问题时，英文界面更容易对标官方文档和社区答案
    - 💡 作为开发者，习惯英文界面有助于阅读代码和技术文档
    
    **个人观点：** 保持默认英文，既能避免翻译坑，又能提升英文技术阅读能力。

---

## 4. 安装 Python

### 安全下载（非常重要！）

!!! danger "安全警示"
    **只从官方网站下载 Python！**
    
    X度等部分搜索引擎搜索"Python 下载"排在前面的结果很多是第三方软件站，可能被植入木马、捆绑软件、垃圾软件甚至“付费安装Python”。
    
    ✅ **唯一正确地址：** `https://www.python.org/downloads/`、

    ✅ **其他软件也是一样，请从正规下载站或官方渠道下载，避免被植入恶意软件。**


### 安装步骤（Windows）

1. 打开 [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. 点击黄色按钮 **"Download Python 3.x.x"**（最新稳定版）
3. 双击下载的 `.exe` 文件
4. 在安装界面**必须勾选** ⚠️：

    ![Python 安装界面](assets/python-install-path.png)

    - ☑️ **`Add python.exe to PATH`**（让终端能直接运行 `python` 命令）

5. 点击 **"Install Now"**
6. 安装完成后，如果看到 **"Disable path length limit"** 按钮，**点击它** ⚠️

    ![Python 路径限制](assets/python-disable-path-limit.png)

    这会解除 Windows 的路径长度限制（Windows 默认只允许 260 个字符的路径，现代开发常常超过这个长度）。

!!! warning "没有勾选 PATH 怎么办？"
    如果已经安装但没勾选 PATH，最简单的办法是重新运行安装程序，选择 **"Modify"** → 重新勾选 PATH 选项。

### 验证安装

安装完成后，打开终端（Windows 按 `Win+R` 输入 `cmd`，macOS 打开"终端"），运行：

```bash
python --version
```

看到类似 `Python 3.1x.x` 的输出，就说明 Python 已经正确安装了 ✅

再验证 pip（Python 的包管理器）：

```bash
pip --version
```

输出类似 `pip 25.x from ... (python 3.1x)` 即为成功。

---

## 5. 虚拟环境（venv）

### 为什么需要虚拟环境？

!!! example "类比理解"
    想象你有两个项目：

    - 项目 A 需要 `pandas 1.5`（一个特定版本的模块，我们稍后会讲到。）
    - 项目 B 需要 `pandas 2.0`（这就是不同版本的同一模块。）
    
    如果直接安装在系统 Python 里，两个版本会互相冲突。虚拟环境就像给每个项目建立独立的Python环境——各自的依赖互不干扰。

### 使用 VSCode 创建虚拟环境

VSCode 的 Python 插件内置了虚拟环境管理功能：

1. 在 VSCode 中打开你的项目文件夹（`文件 → 打开文件夹`）
2. 按 `Ctrl+Shift+P` 打开命令面板
3. 输入 `Python: Create Environment`，回车
4. 选择 **Venv**
5. 选择你刚安装的 Python 解释器版本
6. 等待进度条完成

!!! tip "命令面板的使用技巧"
    在命令面板中输入命令时，**务必保留 `>` 符号开头**。例如：
    
    - ✅ 正确：`> Python: Create Environment`
    - ❌ 错误：`Python: Create Environment`（去掉 `>` 会搜不到）
    
    `>` 符号告诉 VSCode 这是一条命令而不是文件搜索。


![VSCode 创建虚拟环境](assets/vscode-create-venv.png)

创建完成后，项目根目录会出现一个 `.venv` 文件夹，VSCode 右下角状态栏会显示当前 Python 解释器路径。

### 激活虚拟环境

VSCode 会在打开项目时**自动激活**虚拟环境。你也可以在集成终端（或新建的终端窗口）中手动激活：

=== "Windows (PowerShell)"

    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```

=== "macOS / Linux"

    ```bash
    source .venv/bin/activate
    ```

激活成功后，终端提示符前会出现 `(.venv)` 前缀：

```
(.venv) PS D:\my-project>
```

---

## 6. pip 包管理入门

pip 是 Python 的包管理器，相当于"应用商店"——通过一条命令就能安装别人写好的功能。

!!! tip "模块、包、库的区别（仅了解）"
    - **模块**：单个 `.py` 文件
    - **包**：包含多个模块的文件夹
    - **库**：可复用的代码集合，通过 `pip install` 安装
    
    写出来的好多函数 → 组织成模块 → 多个模块组成包 → 发布出去就是库。
    
    当你 `pip install openai` 时，安装的就是一个**库**（或叫**包**），包含了许多函数和工具供你使用。


### 安装你的第一个库

让我们安装 `tqdm`（一个在终端显示进度条的工具）来练习：

```bash
pip install tqdm
```

安装完成后，测试一下：

```python
from tqdm import tqdm
import time

for i in tqdm(range(100)):
    time.sleep(0.02)  # 模拟耗时操作
```

运行后会看到一个进度条在终端中推进——这就是 pip 的魔力 ✨

### 常用库速览

笔者常用库如下，可供参考：

| 库名 | 用途 | 安装命令 |
|------|------|----------|
| `openai` | 调用 DeepSeek / OpenAI API | `pip install openai` |
| `python-dotenv` | 从 `.env` 文件加载环境变量 | `pip install python-dotenv` |
| `pandas` | 数据处理的"瑞士军刀"，读写 Excel/CSV | `pip install pandas` |
| `openpyxl` | pandas 导出 Excel 必需的后端 | `pip install openpyxl` |
| `streamlit` | 把 Python 脚本变成可视化网页 | `pip install streamlit` |
| `SQLAlchemy` | 优雅地与数据库"打交道" | `pip install sqlalchemy` |

本教程需要的库可以一次性安装：

```bash
pip install openai python-dotenv pandas openpyxl
```

---

## 本章小结

✅ VSCode 安装完成，Python 插件就位  
✅ Python 从官网下载，PATH 和路径限制已配置  
✅ 虚拟环境已创建并激活  
✅ 核心依赖库已安装  

**下一章：** [API 集成入门 →](02-api-integration.md) 我们将写出第一份调用大模型的代码！
