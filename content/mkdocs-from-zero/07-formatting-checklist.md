# 第 7 章：MkDocs 格式规范检查清单

> **写得对 ≠ 渲染对** —— 掌握 MkDocs Material 的格式规范，确保教程在网页上完美呈现。

---

## 7.1 为什么需要格式规范？

Markdown 看似简单，但 MkDocs 底层使用的 **Python-Markdown** 解析器对格式有严格的要求。中文内容尤其容易出现"源码看起来没问题，但网页渲染出错"的情况。

本章总结了一套系统化的格式规范，帮助你：
- **写前避免**：遵循规范，从源头消灭渲染问题
- **写后自查**：用检查清单快速定位问题
- **持续维护**：将规范融入日常工作流

---

## 7.2 核心规则：粗体标记与中文的间距

### 问题根因

Python-Markdown 使用 Python 3 的正则表达式 `\w`（word character）来判断 **粗体标记** `**` 是否位于"词边界"（word boundary）上。

- Python 3 中，**CJK 汉字属于 `\w` 字符**（Unicode Letter 类别）
- `**` 开标记要求前面不是 `\w` 字符
- `**` 闭标记要求后面不是 `\w` 字符

当汉字与 `**` 紧贴时（如 `的**技能**的`），解析器将整个序列 `的**技能**的` 视为连续的文字，无法识别其中的 `**` 为粗体分隔符，**粗体渲染失败**。

### 规则

| 模式 | 错误写法 | 正确写法 | 说明 |
|:---|:---|:---|:---|
| 汉字后接开标记 | `的**技能**` | `的 **技能**` | `的` 是 `\w`，会阻止 `**` 被识别为开标记 |
| 闭标记后接汉字 | `**技能**的` | `**技能** 的` | `的` 是 `\w`，会阻止 `**` 被识别为闭标记 |
| 两个粗体相邻 | `**A**、**B**` | `**A**、**B**` | `、` 不是 `\w`，中间有标点 → **无需修改** |

### 无需修改的安全模式

以下模式中 `**` 已经位于正确位置，**不需要修改**：

```
✅ 1. **列表项**：开头        （** 前有空格）
✅ - **列表项**：开头          （** 前有空格）
✅ | **表格** | 内容           （** 前有空格）
✅ 完成后，**重新开始**        （** 前有标点，不是 \w）
✅ **开头即粗体**：后续文字    （** 是行内第一个元素）
```

---

## 7.3 完整格式检查清单

### 粗体与中文 ✅

- [ ] 所有 `**` 开标记前如有汉字，汉字与 `**` 之间必须有空格
- [ ] 所有 `**` 闭标记后如有汉字，`**` 与汉字之间必须有空格
- [ ] 列表项、表格中的粗体无需修改（`- **` / `| **` 已有空格）

### 代码块 ✅

- [ ] 代码块前后各有一个空行
- [ ] 代码块正确标注语言：` ```python `、` ```bash `、` ```markdown ` 等
- [ ] 代码块内没有多余的前导/后随空格

### 列表 ✅

- [ ] 无序列表前有空行（从段落过渡到列表时）
- [ ] 有序列表前有空行
- [ ] 嵌套列表缩进为 4 个空格

### 链接 ✅

- [ ] 内部链接使用相对路径：`[标题](../other-tutorial/chapter.md)`
- [ ] 外部链接使用完整 URL：`[文字](https://example.com)`
- [ ] 链接文字不含多余的引号或括号

### 表格 ✅

- [ ] 表格分隔行正确：`|:---|:---|:---|`
- [ ] 表格每行列数一致
- [ ] 表格前有空行

### Admonition ✅

- [ ] `!!! note` / `!!! info` / `!!! warning` 后内容缩进 4 空格
- [ ] Admonition 前后各有一个空行

### 图片与图表 ✅

- [ ] 图片使用相对路径
- [ ] Mermaid 图表前后有空行
- [ ] 图表语法在本地 mkdocs serve 中验证通过

---

## 7.4 自动化检查工具

### 使用脚本检查粗体间距

将以下 Python 脚本保存为 `check_bold.py`，放在项目根目录：

```python
#!/usr/bin/env python3
"""检查 MkDocs 教程中粗体标记与 CJK 汉字的间距问题。

用法：
  python check_bold.py          # 检查 docs/ 目录
  python check_bold.py --fix    # 自动修复
"""

import re
import os
import sys

CJK = r'[一-鿿㐀-䶿豈-﫿]'
CJK_RE = re.compile(CJK)

def is_cjk(ch):
    return bool(CJK_RE.match(ch))

def fix_line(line):
    """修复一行中的粗体间距问题（状态机方式）。"""
    result = []
    i = 0
    in_bold = False
    n = len(line)
    while i < n:
        if i + 1 < n and line[i] == '*' and line[i + 1] == '*':
            if not in_bold:
                if i > 0 and is_cjk(line[i - 1]):
                    result.append(' ')
                result.append('**')
                in_bold = True
            else:
                result.append('**')
                if i + 2 < n and is_cjk(line[i + 2]):
                    result.append(' ')
                in_bold = False
            i += 2
        else:
            result.append(line[i])
            i += 1
    return ''.join(result)

def check_file(filepath):
    """返回文件中的问题行列表。"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    issues = []
    in_code = False
    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('```') or stripped.startswith('~~~'):
            in_code = not in_code
            continue
        if in_code:
            continue
        fixed = fix_line(line)
        if fixed != line:
            issues.append(lineno)
    return issues

def main():
    root = 'docs'
    fix_mode = '--fix' in sys.argv
    total = 0

    for dirpath, _, filenames in os.walk(root):
        for f in sorted(filenames):
            if not f.endswith('.md'):
                continue
            filepath = os.path.join(dirpath, f)
            issues = check_file(filepath)
            if issues:
                total += len(issues)
                print(f"  {len(issues):>3} issues: {filepath}")
                if fix_mode:
                    # Apply fix
                    with open(filepath, 'r', encoding='utf-8') as fp:
                        content = fp.read()
                    lines = content.split('\n')
                    in_code = False
                    new_lines = []
                    for line in lines:
                        s = line.strip()
                        if s.startswith('```') or s.startswith('~~~'):
                            in_code = not in_code
                            new_lines.append(line)
                            continue
                        if in_code:
                            new_lines.append(line)
                            continue
                        new_lines.append(fix_line(line))
                    with open(filepath, 'w', encoding='utf-8') as fp:
                        fp.write('\n'.join(new_lines))

    print(f"\nTotal: {total} issues found")
    if not fix_mode:
        print("Run with --fix to auto-fix all issues.")

if __name__ == '__main__':
    main()
```

### 使用 Git Hook 防止回归

在 `.git/hooks/pre-commit` 中添加：

```bash
#!/bin/bash
# 检查 Markdown 文件的粗体间距问题

python check_bold.py 2>&1 | grep -q "issues"
if [ $? -eq 0 ]; then
    echo ""
    echo "⚠️  发现粗体标记与汉字的间距问题！"
    echo "   请运行 'python check_bold.py --fix' 自动修复后重新提交。"
    echo ""
    exit 1
fi
```

---

## 7.5 写作工作流建议

### 阶段 1：写作时

1. 在 VS Code 中编写 Markdown，开启拼写检查
2. 每完成一个章节，运行 `mkdocs serve` 本地预览
3. **粗体规则记忆口诀**："汉字贴星号，渲染会糟糕；前后加空格，粗体就稳妥"

### 阶段 2：提交前

1. 运行 `python check_bold.py` 检查粗体间距
2. 运行 `mkdocs build --strict` 确保无构建错误
3. 浏览构建产物中新增/修改的页面

### 阶段 3：CI/CD（推荐）

在 GitHub Actions 中添加格式检查步骤：

```yaml
- name: Check Markdown formatting
  run: |
    python check_bold.py
    # 如果有问题，CI 失败，阻止合并
```

---

## 7.6 常见问题 FAQ

### Q：加了空格后，渲染出来的网页上会有多余的空格吗？

不会。中文网页排版中，`<strong>` 标签两侧的空格在视觉上几乎不可见。这是 MkDocs Material 的标准做法。

### Q：英文教程需要关注这个问题吗？

通常不需要。英文单词之间本身有空格，`**` 自然位于词边界上。只有 **CJK 字符**（中日韩统一表意文字）才需要额外注意。

### Q：有没有一劳永逸的解决方案？

最彻底的方案是在 CI 中加入检查步骤（见 7.5 阶段 3）。每次 PR 自动扫描，阻止新问题的引入。

### Q：`***` 斜粗体呢？

同理，`***` 斜粗体标记也需要与汉字保持间距。上述检查脚本同时适用于 `**` 和 `***`（`***` 以 `**` 开头，会被同样的逻辑处理）。

---

## 7.7 本章小结

- **根因**：Python 3 中 CJK 汉字属于 `\w` 字符，会阻止 `**` 被识别为词边界
- **规则**：汉字与 `**` 之间必须有空格
- **工具**：用 `check_bold.py` 自动检查和修复
- **流程**：写作 → 预览 → 检查 → 提交 → CI 验证
- **口诀**："汉字贴星号，渲染会糟糕；前后加空格，粗体就稳妥"

---

> **格式规范不是限制，而是一种保障** —— 让你写的内容在 MkDocs 网页上完美呈现。
