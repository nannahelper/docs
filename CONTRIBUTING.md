# 教程更新工作流

> **改一处，查三处** —— 本项目的核心文件引用分布在 `mkdocs.yml`、`README.md`、`docs/categories/*.md` 三个位置，
> 任何教程的新增、修改、重命名都必须同步更新这三处，否则会导致引用断裂。

---

## 快速参考：三处同步更新清单

当你对教程做任何变更时，必须在以下 **3 个位置** 同步修改：

| # | 文件 | 作用 | 变更时必查 |
|---|------|------|-----------|
| 1 | `mkdocs.yml` | 网站导航配置 | 新增/删除/重命名章节文件 |
| 2 | `README.md` | 项目首页教程目录 | 新增/删除/重命名章节 **或章节名/内容变化** |
| 3 | `docs/categories/*.md` | 分类概览页的教程表格 | 新增/删除/重命名章节 **或章节名/内容变化** |

---

## 场景一：新增一个完整教程

### 步骤

```bash
# 1. 创建教程目录和文件
mkdir docs/my-tutorial-from-zero/
# 创建 index.md + 各章节 .md 文件

# 2. 更新 mkdocs.yml — 在对应分类下添加 nav 条目
# 编辑 mkdocs.yml，在合适的分类下添加：
#   - 我的新教程:
#     - 首页: my-tutorial-from-zero/index.md
#     - 第 1 章：xxx: my-tutorial-from-zero/01-xxx.md
#     ...

# 3. 更新 README.md — 在对应分类下添加教程表格
# 在 README.md 的对应章节区域添加教程表格（参考已有教程的格式）

# 4. 更新分类概览页 — 在 docs/categories/xxx.md 添加教程表格
# 基础技能 → docs/categories/basic-skills.md
# 编程语言 → docs/categories/programming-languages.md
# 技术领域 → docs/categories/technical-domains.md
# 工程实践 → docs/categories/engineering-practice.md

# 5. 运行验证
python check_references.py          # 验证所有引用正确
python check_bold.py                # 验证粗体格式
mkdocs build --strict               # 验证构建通过

# 6. 本地预览
mkdocs serve
# 浏览器访问 http://127.0.0.1:8000 逐页检查
```

### 检查清单

- [ ] `mkdocs.yml` 中 nav 路径指向的文件在磁盘上真实存在
- [ ] 新教程目录名使用小写字母 + 连字符（如 `my-tutorial-from-zero`）
- [ ] 新教程包含 `index.md` 作为首页
- [ ] README.md 中已添加对应的教程章节表格
- [ ] `docs/categories/xxx.md` 中已添加对应的教程章节表格
- [ ] README.md 和 category 页中的章节名与 mkdocs.yml 保持一致
- [ ] `mkdocs build --strict` 无错误
- [ ] 所有章节页面的"下一篇"导航链接指向正确

---

## 场景二：修改现有教程的章节文件名

> ⚠️ **这是最容易出错的场景！** PR #2 的 bug 正是由此引起。

### 危险操作示例

```bash
# 千万不要只做这一件事！
mv docs/office-word-from-zero/01-document-structure.md docs/office-word-from-zero/01-document-basics.md
# 如果只 rename 文件而不更新 mkdocs.yml → 网站导航断裂！
```

### 正确步骤

当重命名章节文件或修改章节标题时，必须逐一检查并更新以下所有位置：

```bash
# 1. 重命名文件
mv old-name.md new-name.md

# 2. 搜索所有引用旧文件名的地方
grep -r "old-name.md" docs/ mkdocs.yml README.md

# 3. 逐一更新找到的引用：
#    a. mkdocs.yml — 更新 nav 路径
#    b. 同教程内的 "下一篇"/"上一章" 导航链接
#    c. 其他教程的交叉引用链接

# 4. 如果章节名/标题也变了，更新：
#    a. README.md 中的教程表格
#    b. docs/categories/xxx.md 中的教程表格

# 5. 运行验证
python check_references.py
mkdocs build --strict
```

### 修改后的全局搜索命令

```bash
# 搜索旧文件名在整个仓库中所有出现的位置
git grep -n "old-name.md"

# 搜索旧章节标题
git grep -n "旧章节标题"
```

---

## 场景三：修改章节内容（不影响文件名）

如果只是修改章节的正文内容（不改文件名和章节标题），则只需要：

- [ ] 遵循排版格式规范（粗体与中文间距、代码块格式等）
- [ ] `python check_bold.py` 检查粗体格式
- [ ] `mkdocs build --strict` 验证构建通过
- [ ] 本地 `mkdocs serve` 预览修改的页面

---

## 场景四：删除教程或章节

```bash
# 1. 删除文件
rm docs/some-tutorial/obsolete-chapter.md

# 2. 从 mkdocs.yml 移除对应的 nav 条目

# 3. 从 README.md 移除对应的教程/章节行

# 4. 从 docs/categories/xxx.md 移除对应的教程/章节行

# 5. 搜索其他教程中是否有指向被删页面的链接
grep -r "obsolete-chapter.md" docs/

# 6. 验证
python check_references.py
mkdocs build --strict
```

---

## 自动化验证脚本

### check_references.py — 引用完整性检查

在项目根目录创建 `check_references.py`：

```python
#!/usr/bin/env python3
"""
检查项目的引用完整性 —— 确保 mkdocs.yml 中引用的所有文件都存在。

检查项：
  1. mkdocs.yml nav 中引用的所有 .md/.js 文件是否存在
  2. README.md 和 categories/*.md 中的教程章节表是否与 mkdocs.yml 一致
  3. docs/ 目录下是否有未被 mkdocs.yml 引用的孤立文件

用法：
  python check_references.py           # 检查所有
  python check_references.py --files   # 仅检查文件存在性
  python check_references.py --dangling # 仅检查孤立文件
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, 'docs')

# ── 1. 提取 mkdocs.yml 中所有文件引用 ──

def extract_mkdocs_refs():
    """从 mkdocs.yml 提取所有本地文件引用，返回 {相对路径} 集合"""
    with open(os.path.join(ROOT, 'mkdocs.yml'), 'r', encoding='utf-8') as f:
        content = f.read()
    # 匹配所有 .md 和 .js 路径（排除完整 URL）
    refs = set()
    for m in re.finditer(r'(?:^|\s)([\w][\w/-]*\.(?:md|js))', content, re.MULTILINE):
        path = m.group(1)
        if not path.startswith('http'):
            refs.add(path)
    return refs

# ── 2. 检查文件存在性 ──

def check_files_exist(refs):
    """检查所有引用的文件是否存在于 docs/ 目录"""
    missing = []
    for ref in sorted(refs):
        full = os.path.join(DOCS, ref)
        if not os.path.exists(full):
            missing.append(ref)
    return missing

# ── 3. 检查孤立文件 ──

def find_dangling_files(refs):
    """检查 docs/ 下是否有未被 mkdocs.yml 引用的 .md 文件"""
    dangling = []
    for dirpath, _, filenames in os.walk(DOCS):
        for f in filenames:
            if not f.endswith('.md'):
                continue
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, DOCS).replace('\\', '/')
            if rel not in refs:
                dangling.append(rel)
    return dangling

# ── 4. 提取 README/category 中的教程章节表 ──

def extract_table_rows(filepath):
    """提取 Markdown 表格中的数据行（跳过表头和分隔行）"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    rows = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and not stripped.startswith('|:'):
            # 跳过分隔行
            if re.match(r'^\|[\s:|-]+\|$', stripped):
                continue
            # 跳过只有 --- 的行
            if re.match(r'^\|[-\s|]+\|$', stripped):
                continue
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            rows.append(cells)
    return rows

# ── Main ──

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    errors = 0

    refs = extract_mkdocs_refs()
    print(f"✓ 从 mkdocs.yml 提取了 {len(refs)} 个文件引用\n")

    if mode in ('all', '--files'):
        print("=" * 60)
        print("1. 检查 mkdocs.yml 引用的文件是否存在")
        print("=" * 60)
        missing = check_files_exist(refs)
        if missing:
            print(f"❌ 发现 {len(missing)} 个缺失文件：")
            for m in missing:
                print(f"   MISSING: docs/{m}")
            errors += len(missing)
        else:
            print("✅ 所有引用的文件都存在")

        # 额外检查：extra_javascript 中的本地文件
        with open(os.path.join(ROOT, 'mkdocs.yml'), 'r', encoding='utf-8') as f:
            content = f.read()
        js_match = re.search(r'extra_javascript:.*?^\w', content, re.DOTALL)
        if js_match:
            js_section = js_match.group(0)
            local_js = re.findall(r'^\s*-\s*([\w/]+\.js)', js_section, re.MULTILINE)
            for js_file in local_js:
                full = os.path.join(DOCS, js_file)
                if not os.path.exists(full):
                    print(f"   MISSING JS: docs/{js_file}")
                    errors += 1
        print()

    if mode in ('all', '--dangling'):
        print("=" * 60)
        print("2. 检查孤立文件（在 docs/ 但未被 mkdocs.yml 引用）")
        print("=" * 60)
        dangling = find_dangling_files(refs)
        # 过滤常见排除项
        excluded = []
        for d in dangling:
            # 排除 assets/ 目录下的非教程文件
            if d.startswith('assets/'):
                excluded.append(d)
                continue
            print(f"   ⚠ DANGLING: docs/{d}")
        for e in excluded:
            print(f"   ℹ SKIPPED (assets): docs/{e}")
        active_dangling = [d for d in dangling if d not in excluded]
        if not active_dangling:
            print("   ✅ 无活跃孤立文件")
        print()

    print("=" * 60)
    if errors > 0:
        print(f"❌ 发现 {errors} 个问题，请修复后重新提交。")
        sys.exit(1)
    else:
        print("✅ 所有检查通过！")
        sys.exit(0)

if __name__ == '__main__':
    main()
```

### 在 CI 中集成检查

编辑 `.github/workflows/main.yml`，在 `Build documentation` 步骤前添加：

```yaml
- name: Check references
  run: python check_references.py --files
```

---

## 预提交检查清单（Pre-Commit Checklist）

每次提交涉及教程变更的 PR 前，确认以下项目全部通过：

### 文件引用

- [ ] `python check_references.py` 全部通过
- [ ] 所有新增/重命名的文件在 `mkdocs.yml` 中有对应的 nav 条目
- [ ] 所有 `mkdocs.yml` 中的 nav 路径指向真实存在的文件

### 三处同步

- [ ] `mkdocs.yml` 中的章节标题变化已同步到 `README.md`
- [ ] `mkdocs.yml` 中的章节标题变化已同步到 `docs/categories/*.md`
- [ ] 教程数量变化（新增/删除教程）已在三处全部更新

### 内容质量

- [ ] `python check_bold.py` 无粗体间距问题
- [ ] 任何重命名的旧文件名已用 `git grep` 全局搜索并更新
- [ ] 教程内"下一篇"/"上一章"链接指向正确

### 构建验证

- [ ] `mkdocs build --strict` 无错误、无警告
- [ ] `mkdocs serve` 本地预览所有修改页面正常渲染

---

## 常见错误与预防

### ❌ 错误 1：只改 mkdocs.yml，忘记同步 README/categories

**症状**：PR 合并后网站导航正确，但 README 和分类页显示的是旧信息。

**预防**：提交前用 diff 工具对比 mkdocs.yml 的章节标题与 README/categories 中的表格内容。

### ❌ 错误 2：重命名文件后未全局搜索旧引用

**症状**：教程内"下一篇"链接 404，或引用该章节的其他教程链接断裂。

**预防**：`git grep -n "old-filename.md"` 确保无残留引用。

### ❌ 错误 3：教程目录名与 mkdocs.yml 中路径不一致

**症状**：`mkdocs build` 报 `WARNING - Doc file 'xxx.md' does not exist`。

**预防**：使用 `python check_references.py` 自动检查。

### ❌ 错误 4：新增教程后忘记在分类概览页添加介绍

**症状**：新教程在导航栏可见，但在分类总览页找不到入口。

**预防**：检查对应分类页（`docs/categories/xxx.md`）是否已更新。

---

## 参考链接

- [MkDocs 格式规范检查清单](docs/mkdocs-from-zero/07-formatting-checklist.md)
- [AI 写作辅助 Prompt](prompt.md)
- [项目 README](README.md)
