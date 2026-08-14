# 第 5 章：Node.js、npm 与前端工具链 — 管理 JavaScript 项目

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 35 分钟 |
| 核心概念 | Node.js、npm、npx、package.json、lockfile |
| 核心比喻 | `package.json` 是购物清单，`package-lock.json` 是实际小票 |
| 实践任务 | 创建项目、安装依赖、运行一次本地工具 |
| 难度等级 | ★★☆☆☆ |

## JavaScript 工具链为什么会有多个命令

Node.js 是让 JavaScript 在浏览器之外运行的环境，npm 通常随 Node.js 一起提供，负责读取项目清单、安装依赖和运行脚本。`npx` 更像一次性调用项目工具的入口，pnpm、Bun 则是不同的包管理或运行工具。它们名字相近，但职责和项目兼容性不完全相同。

新手最容易遇到的问题，是在错误目录运行命令，或者把全局安装和项目本地依赖混在一起。项目中的 `package.json` 和锁文件描述了“这个项目需要什么”，不要只看终端最后一行成功就结束，还要确认生成的文件、脚本和版本记录是否符合预期。

## 5.1 Node.js 和 npm 是什么

Node.js 让 JavaScript 可以在浏览器外运行；npm 随 Node.js 一起提供包管理和脚本运行能力。它们不是同一个东西：前者是运行时，后者是项目工具。

```bash
node --version
npm --version
```

如果命令不存在，回到第 4 章使用 `winget`、Scoop、Homebrew 或 APT 安装，不要从搜索结果中下载来路不明的安装包。

## 5.2 创建第一个项目

```bash
mkdir hello-node
cd hello-node
npm init -y
```

打开生成的 `package.json`，它描述项目名称、版本、脚本和依赖。添加一个开发依赖：

```bash
npm install --save-dev prettier
```

此时应出现 `node_modules/`、`package.json` 和 `package-lock.json`。`node_modules/` 通常不提交；`package-lock.json` 用来固定实际依赖版本，应该提交。

## 5.3 npm、npx、pnpm 和 Bun

| 工具 | 作用 | 适合什么时候用 |
|:---|:---|:---|
| `npm` | 安装依赖、运行脚本 | 默认起点，资料最多 |
| `npx` / `npm exec` | 临时运行项目工具 | 不想把工具全局安装时 |
| `pnpm` | 节省磁盘空间的包管理器 | 多项目或 monorepo |
| `bun` | 集运行时、包管理和工具于一体 | 明确接受其兼容性取舍时 |

用 `npx` 临时运行 Prettier：

```bash
npx prettier --check .
```

也可以使用更明确的等价写法：

```bash
npm exec -- prettier --check .
```

不要在同一个项目里随意混用 npm、pnpm 和 Bun。先看项目已有的 lockfile：`package-lock.json` 对应 npm，`pnpm-lock.yaml` 对应 pnpm，`bun.lock` 对应 Bun。

## 5.4 写一个可重复运行的脚本

在 `package.json` 的 `scripts` 中加入：

```json
{
  "scripts": {
    "format:check": "prettier --check ."
  }
}
```

然后运行：

```bash
npm run format:check
```

脚本的价值是让自己和队友使用同一条命令；它不是把错误藏起来的快捷方式。

## ✅ 验证步骤

删除 `node_modules/` 后执行 `npm install`，再运行 `npm run format:check`。如果结果与第一次一致，说明项目可以依据清单恢复依赖。

## 📝 本章总结

- Node.js 是运行时，npm 是包管理器和脚本入口。
- `package.json` 描述需求，lockfile 记录实际安装结果。
- `npx` 适合临时调用工具；项目应固定自己的依赖和命令。

## ✏️ 课后练习

1. 给项目增加 `check` 脚本，依次输出 Node 和 npm 版本。
2. 观察删除 `node_modules/` 后重新安装的过程，说明为什么不应提交它。

## 🔮 下一章预告

下一章会安装 Git、认识 Shell 的组合命令，并把这次环境配置结果保存成可追踪的版本。
