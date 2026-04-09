#!/usr/bin/env python3
"""
X Article HTML 预览生成器（零依赖）
用法: python3 to-x-html.py <input.md> [output.html]

将纯文本发布包转换为带富文本格式的 HTML 预览。
在浏览器中打开 → 全选复制 → 粘贴到 X Article 编辑器 → 格式自动保留。

格式规则：
- emoji 开头的行 → <h2> 段落标题
- 〔...〕行 → 跳过（操作指示）
- [...] 行 → 跳过（元信息）
- 全角空格缩进的行 → <p> 段落
- · 开头的行 → <li> 列表项
- 1./2./3. 开头 → <li> 有序列表项
"""
import re
import sys
import os

SECTION_EMOJIS = set('🔧🧪🏆📊🤔📝💡🎯🔍⚡🚀✅❌⚠️')

def is_meta(line):
    s = line.strip()
    return s.startswith('[') and s.endswith(']')

def is_instruction(line):
    s = line.strip()
    return s.startswith('〔') and s.endswith('〕')

def is_section_title(line):
    s = line.strip()
    return s and s[0] in SECTION_EMOJIS

def convert(lines):
    html_parts = []
    html_parts.append("""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>X Article 预览 — 全选复制后粘贴到 X Article 编辑器</title>
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    max-width: 720px;
    margin: 40px auto;
    padding: 0 20px;
    line-height: 1.8;
    color: #e7e9ea;
    background: #15202b;
  }
  .instructions {
    background: #1d3a5c;
    border: 1px solid #2d5a8c;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 32px;
    color: #8ecdf7;
    font-size: 14px;
  }
  .instructions strong { color: #fff; }
  .content { /* 这部分是要复制的 */ }
  h2 { font-size: 18px; font-weight: 700; margin: 24px 0 8px; color: #f7f9f9; }
  p { margin: 8px 0; text-indent: 2em; }
  p.no-indent { text-indent: 0; }
  p.hook { font-weight: 700; text-indent: 0; font-size: 17px; }
  blockquote {
    border-left: 3px solid #536471;
    padding-left: 12px;
    color: #8b98a5;
    font-style: italic;
    margin: 8px 0;
  }
  ul, ol { padding-left: 24px; margin: 8px 0; }
  li { margin: 4px 0; }
  .golden { font-style: italic; color: #d4a574; }
  hr { border: none; border-top: 1px solid #38444d; margin: 16px 0; }
</style>
</head>
<body>
<div class="instructions">
  <strong>操作步骤：</strong><br>
  1. 选中下方「内容区域」的所有文字（Ctrl+A 或手动选中）<br>
  2. 复制（Ctrl+C）<br>
  3. 粘贴到 X Article 编辑器（Ctrl+V）<br>
  4. 富文本格式（加粗标题、列表）会自动保留
</div>
<div class="content" id="content">
""")

    in_list = False
    is_first_body_line = True

    for line in lines:
        s = line.strip()

        # 跳过元信息
        if not s or is_meta(s):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            continue

        # 图片上传指示 → 嵌入 <img>
        if is_instruction(s):
            img_match = re.search(r'imgs/([^\s〕]+)', s)
            if img_match:
                img_file = img_match.group(1)
                html_parts.append(f'<img src="imgs/{img_file}" alt="{img_file}" style="max-width:100%;margin:12px 0;border-radius:8px;">')
            continue

        # 段落标题（emoji 开头）
        if is_section_title(s):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append(f'<h2>{s}</h2>')
            is_first_body_line = False
            continue

        # 无序列表
        if s.startswith('·'):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            html_parts.append(f'<li>{s[1:].strip()}</li>')
            continue

        # 有序列表
        m = re.match(r'^(\d+)\.\s*(.*)', s)
        if m:
            if not in_list:
                html_parts.append('<ol>')
                in_list = True
            html_parts.append(f'<li>{m.group(2)}</li>')
            continue

        if in_list:
            list_tag = 'ol' if html_parts[-1].startswith('<li>') and '<ol>' in ''.join(html_parts[-5:]) else 'ul'
            html_parts.append(f'</{list_tag}>')
            in_list = False

        # Hook（第一行正文，加粗无缩进）
        if is_first_body_line:
            html_parts.append(f'<p class="hook">{s}</p>')
            is_first_body_line = False
            continue

        # 普通段落
        text = s.lstrip('\u3000')  # 去掉全角空格，HTML 用 text-indent
        html_parts.append(f'<p>{text}</p>')

    if in_list:
        html_parts.append('</ul>')

    html_parts.append('</div>\n</body>\n</html>')
    return '\n'.join(html_parts)

def main():
    if len(sys.argv) < 2:
        print("用法: python3 to-x-html.py <input.md> [output.html]")
        sys.exit(1)

    infile = sys.argv[1]
    outfile = sys.argv[2] if len(sys.argv) > 2 else infile.rsplit('.', 1)[0] + '.html'

    with open(infile, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    html = convert(lines)

    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ 生成预览: {outfile}")
    print(f"   在浏览器中打开 → 全选复制 → 粘贴到 X Article 编辑器")

if __name__ == '__main__':
    main()
