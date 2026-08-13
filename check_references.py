#!/usr/bin/env python3
"""
检查项目的引用完整性 —— 确保 mkdocs.yml 中引用的所有文件都存在。

检查项：
  1. mkdocs.yml nav 中引用的所有 .md/.js 文件是否存在
  2. content/ 目录下是否有未被 mkdocs.yml 引用的孤立文件

用法：
  python check_references.py           # 检查所有
  python check_references.py --files   # 仅检查文件存在性
  python check_references.py --dangling # 仅检查孤立文件
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, 'content')

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
    """检查所有引用的文件是否存在于 content/ 目录"""
    missing = []
    for ref in sorted(refs):
        full = os.path.join(CONTENT, ref)
        if not os.path.exists(full):
            missing.append(ref)
    return missing

# ── 3. 检查孤立文件 ──

def find_dangling_files(refs):
    """检查 content/ 下是否有未被 mkdocs.yml 引用的 .md 文件"""
    dangling = []
    for dirpath, _, filenames in os.walk(CONTENT):
        for f in filenames:
            if not f.endswith('.md'):
                continue
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, CONTENT).replace('\\', '/')
            if rel not in refs:
                dangling.append(rel)
    return dangling

# ── Main ──

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    errors = 0

    refs = extract_mkdocs_refs()
    print(f"[INFO] 从 mkdocs.yml 提取了 {len(refs)} 个文件引用\n")

    if mode in ('all', '--files'):
        print("=" * 60)
        print("1. 检查 mkdocs.yml 引用的文件是否存在")
        print("=" * 60)
        missing = check_files_exist(refs)
        if missing:
            print(f"\n  FAIL  发现 {len(missing)} 个缺失文件：")
            for m in missing:
                print(f"         MISSING: content/{m}")
            errors += len(missing)
        else:
            print("\n  PASS  所有引用的文件都存在")

        # 额外检查：extra_javascript 中的本地文件
        with open(os.path.join(ROOT, 'mkdocs.yml'), 'r', encoding='utf-8') as f:
            content = f.read()
        js_match = re.search(r'extra_javascript:(.*?)(?:^\w|\Z)', content, re.DOTALL | re.MULTILINE)
        if js_match:
            js_section = js_match.group(1)
            local_js = re.findall(r'^\s*-\s*([\w/]+\.js)', js_section, re.MULTILINE)
            for js_file in local_js:
                if js_file.startswith('http'):
                    continue
                full = os.path.join(CONTENT, js_file)
                if not os.path.exists(full):
                    print(f"         MISSING JS: content/{js_file}")
                    errors += 1
        print()

    if mode in ('all', '--dangling'):
        print("=" * 60)
        print("2. 检查孤立文件（在 content/ 但未被 mkdocs.yml 引用）")
        print("=" * 60)
        dangling = find_dangling_files(refs)
        # 过滤常见排除项
        excluded = []
        active = []
        for d in dangling:
            if d.startswith('assets/'):
                excluded.append(d)
            else:
                active.append(d)
        for d in active:
            print(f"         DANGLING: content/{d}")
        for e in excluded:
            print(f"         SKIPPED (assets): content/{e}")
        if not active:
            print("\n  PASS  无活跃孤立文件")
        else:
            print(f"\n  WARN  发现 {len(active)} 个孤立文件（可能在 nav 中缺失）")
        print()

    print("=" * 60)
    if errors > 0:
        print(f"\n  FAIL  发现 {errors} 个问题，请修复后重新提交。")
        sys.exit(1)
    else:
        print("\n  PASS  所有检查通过！")
        sys.exit(0)

if __name__ == '__main__':
    main()
