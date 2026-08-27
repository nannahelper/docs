# 第 6 章：Git 与 Shell — 给项目装上存档和遥控器

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 8 分钟 |
| 核心概念 | Git、仓库、提交、Shell、重定向、管道 |
| 核心比喻 | Git 是可回溯存档，Shell 是组合命令的遥控器 |
| 实践任务 | 创建仓库并保存一次环境检查结果 |
| 难度等级 | ★★☆☆☆ |

## Git 是可回看的存档，不是云盘同步

Git 会在项目目录里记录一组有顺序的快照，让你知道哪些文件被改了、哪一次改动引入了问题，以及需要时怎样回到一个已知状态。远程仓库是协作和备份的一种方式，但“提交”与“推送”是两个动作：前者先留在本地，后者才把选定的提交发送到远程。

Shell 则提供了组合命令的方式。把“列出文件、筛选结果、查看状态”串起来，可以快速获取证据；但命令越长，越应该分段确认中间结果。先在安全的小目录里练习，理解每一段会读取、修改还是删除什么，再用于真实项目。

## 6.1 安装并验证 Git

=== "Windows"
    ```powershell
    winget install --id Git.Git -e
    git --version
    ```

=== "macOS"
    ```bash
    brew install git
    git --version
    ```

=== "Ubuntu / Debian"
    ```bash
    sudo apt update
    sudo apt install git
    git --version
    ```

## 6.2 创建第一个仓库

```bash
mkdir environment-check
cd environment-check
git init
git status
```

把环境信息保存到文件：

=== "Windows PowerShell"
    ```powershell
    python --version | Out-File versions.txt
    git --version | Out-File -Append versions.txt
    ```

=== "macOS / Linux"
    ```bash
    { python3 --version; git --version; } > versions.txt
    ```

```bash
git add versions.txt
git commit -m "docs: record local tool versions"
git log --oneline -1
```

## 6.3 认识 Shell 组合

管道 `|` 把前一个命令的输出交给后一个命令；重定向 `>` 把输出写入文件。组合命令前先确认输入和输出目标，避免覆盖重要文件。

## ✅ 验证步骤

`git status` 应显示干净工作区；`git log --oneline -1` 应显示刚才的提交；打开 `versions.txt`，确认其中没有 API Key 或个人隐私。

## 📝 本章总结

- Git 记录项目变化，Shell 组合命令处理信息。
- `add`、`commit` 和 `status` 是最小可用的 Git 循环。
- 重定向前必须确认目标文件。

## ✏️ 课后练习

1. 为仓库添加 `.gitignore`，排除 `.venv/` 和 `.env`。
2. 修改 `versions.txt` 后再提交一次，并查看两次提交的差异。

## 🔮 下一章预告

最后一章会把工具安装、版本记录和排错流程串起来，完成一次环境验收。
