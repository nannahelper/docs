# 第 3 章：Python 与包管理器 — 给项目准备隔离工具箱

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 35 分钟 |
| 核心概念 | Python、venv、pip、npm、包版本 |
| 核心比喻 | 虚拟环境是项目专属工具箱，避免工具互相污染 |
| 实践任务 | 创建虚拟环境并安装一个依赖 |
| 难度等级 | ★★☆☆☆ |

## 3.1 验证 Python

```bash
python --version
python -m pip --version
```

Windows 如果 `python` 指向 Microsoft Store，可以尝试 `py --version`；不要在多个解释器都存在时只凭文件夹名称猜版本。

## 3.2 创建 Python 虚拟环境

```bash
python -m venv .venv
```

=== "Windows PowerShell"
    ```powershell
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    ```

=== "macOS / Linux"
    ```bash
    source .venv/bin/activate
    python -m pip install --upgrade pip
    ```

安装一个练习依赖并导出清单：

```bash
python -m pip install rich
python -m pip freeze > requirements.txt
```

!!! warning "不要把系统 Python 当项目环境"
    使用 `python -m pip` 可以确保 pip 属于当前调用的 Python。不要在不清楚解释器位置时直接运行全局 `pip install`。

## 3.3 认识其他包管理器

| 工具 | 主要职责 | 常见验证 |
|:---|:---|:---|
| `pip` | Python 包 | `python -m pip --version` |
| `npm` | Node.js 包和脚本 | `node --version; npm --version` |
| `cargo` | Rust 包和构建 | `cargo --version` |
| `apt` / `brew` | 系统级软件包 | `apt --version` / `brew --version` |

## ✅ 验证步骤

在项目目录中确认 Python 解释器路径包含 `.venv`，执行 `python -c "import rich; print(rich.__version__)"` 能成功；退出虚拟环境后，说明项目依赖为什么不应该依赖全局安装。

## 📝 本章总结

- 包管理器负责安装和更新依赖，不等于编译器。
- 虚拟环境把项目依赖和系统环境隔离。
- 依赖清单让别人可以复现你的环境。

## ✏️ 课后练习

1. 创建一个只安装 `requests` 的新虚拟环境。
2. 删除虚拟环境后，用依赖清单重新创建它。

## 🔮 下一章预告

下一章会安装 Git 和常用 Shell 工具，用版本库保存环境配置成果。
