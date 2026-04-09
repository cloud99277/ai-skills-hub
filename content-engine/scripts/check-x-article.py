#!/usr/bin/env python3
"""
X Article 格式自动检查脚本（零依赖）
用法: python3 check-x-article.py <file>

检查 X Article 发布包中的 Markdown 残留和格式问题。
只检查正文区域（跳过元信息标记行）。
"""
import re
import sys
import os

MARKDOWN_PATTERNS = [
    (r'\*\*[^*]+\*\*', '** 加粗标记', 'X Article 编辑器中用 Ctrl+B 加粗'),
    (r'(?<!\*)\*[^*]+\*(?!\*)', '* 斜体标记', 'X Article 编辑器中用 Ctrl+I 斜体'),
    (r'^#{1,6}\s', '# 标题符号', '用 emoji 开头代替'),
    (r'!\[.*?\]\(.*?\)', '![]() 图片语法', '用〔此处上传 imgs/xxx.png〕代替'),
    (r'(?<!!)\[.*?\]\(.*?\)', '[]() 链接语法', '放到文末「相关链接」区域'),
    (r'^>\s', '> 引用语法', '去掉 > 符号'),
    (r'^- \s*\S', '- 列表符号', '用 · 代替'),
    (r'`[^`]+`', '`` 代码标记', '去掉反引号'),
    (r'\|.*\|.*\|', '| 表格语法', '转为文字描述'),
    (r'^---$', '--- 分隔线', 'X Article 不需要分隔线，用空行或段落标题分隔'),
]

META_LINE_PATTERNS = [
    r'^\[.*\]$',       # [发布包元信息] 等
    r'^〔.*〕$',       # 〔此处上传...〕
]

def is_meta_line(line):
    """判断是否为元信息/操作指示行（不检查这些行）"""
    stripped = line.strip()
    return any(re.match(p, stripped) for p in META_LINE_PATTERNS)

def check_file(filepath):
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filepath}")
        return 1

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    issues = []
    for i, line in enumerate(lines, 1):
        if is_meta_line(line):
            continue
        for pattern, name, fix in MARKDOWN_PATTERNS:
            matches = re.findall(pattern, line.rstrip(), re.MULTILINE)
            if matches:
                for match in matches:
                    issues.append((i, name, match.strip()[:50], fix))

    # 检查首行缩进
    indent_missing = []
    in_body = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped == '[正文 — 粘贴到 X Article 正文区域]':
            in_body = True
            continue
        if not in_body or is_meta_line(line):
            continue
        if stripped == '' or stripped == '---':
            continue
        # 段落标题行（emoji 开头）不需要缩进
        if stripped and stripped[0] in '🔧🧪🏆📊🤔📝💡·0123456789':
            continue
        # 正文段落应该有全角空格缩进
        if stripped and not line.startswith('\u3000\u3000'):
            indent_missing.append(i)

    # 检查连续空行（段落间只需换 1 行）
    double_blanks = []
    prev_blank = False
    for i, line in enumerate(lines, 1):
        is_blank = line.strip() == ''
        if is_blank and prev_blank:
            double_blanks.append(i)
        prev_blank = is_blank

    # 输出结果
    print(f"═══ X Article 格式检查: {os.path.basename(filepath)} ═══\n")

    if not issues and not indent_missing and not double_blanks:
        print("✅ 全部通过，无 Markdown 残留\n")
        return 0

    if issues:
        print(f"❌ 发现 {len(issues)} 处 Markdown 残留:\n")
        for line_no, name, content, fix in issues:
            print(f"  行 {line_no}: {name}")
            print(f"    内容: {content}")
            print(f"    修复: {fix}\n")

    if double_blanks:
        print(f"⚠️ {len(double_blanks)} 处连续空行（只需换 1 行）:")
        print(f"  行号: {', '.join(str(n) for n in double_blanks[:15])}")
        if len(double_blanks) > 15:
            print(f"  ...等共 {len(double_blanks)} 处")
        print()

    if indent_missing:
        print(f"⚠️ {len(indent_missing)} 行缺少首行缩进（全角空格）:")
        print(f"  行号: {', '.join(str(n) for n in indent_missing[:10])}")
        if len(indent_missing) > 10:
            print(f"  ...等共 {len(indent_missing)} 行\n")

    total = len(issues) + len(double_blanks) + len(indent_missing)
    print(f"\n总计: {total} 个问题")
    return 1 if issues else 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python3 check-x-article.py <file>")
        sys.exit(1)
    sys.exit(check_file(sys.argv[1]))
