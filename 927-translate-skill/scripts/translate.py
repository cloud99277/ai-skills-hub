#!/usr/bin/env python3
"""
translate: 通用翻译工具
支持：文件翻译、URL 翻译、长文分块
纯 Python 实现，无外部依赖
"""
import os
import sys
import re
import argparse
import textwrap
import urllib.request
import json

import subprocess
import tempfile

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AI_SKILLS_DIR = os.path.join(os.path.expanduser('~'), '.ai-skills')
GLOSSARY_FILE = os.path.join(SKILL_DIR, 'references', 'glossary-en-zh.md')

# baoyu skill paths
X_TO_MD_SCRIPT = os.path.join(AI_SKILLS_DIR, 'baoyu-danger-x-to-markdown', 'scripts', 'main.ts')
URL_TO_MD_SCRIPT = os.path.join(AI_SKILLS_DIR, 'baoyu-url-to-markdown', 'scripts', 'main.ts')

# Load X auth from ~/.baoyu-skills/.env
def load_env_file():
    """Load environment variables from ~/.baoyu-skills/.env"""
    env_file = os.path.join(os.path.expanduser('~'), '.baoyu-skills', '.env')
    env = {}
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    env[key.strip()] = val.strip()
    return env


def is_x_url(url):
    """Check if URL is an X/Twitter URL"""
    return bool(re.match(r'https?://(x\.com|twitter\.com)/', url))


def resolve_bun():
    """Resolve bun runtime: bun or npx -y bun"""
    try:
        subprocess.run(['bun', '--version'], capture_output=True, check=True)
        return ['bun']
    except (FileNotFoundError, subprocess.CalledProcessError):
        return ['npx', '-y', 'bun']


def fetch_x_tweet(url, output_path):
    """Fetch X tweet using baoyu-danger-x-to-markdown"""
    if not os.path.exists(X_TO_MD_SCRIPT):
        print(f'❌ baoyu-danger-x-to-markdown not found: {X_TO_MD_SCRIPT}')
        print('   请先安装: cp -r baoyu-skills/skills/baoyu-danger-x-to-markdown ~/.ai-skills/')
        sys.exit(1)

    env = {**os.environ, **load_env_file()}
    bun = resolve_bun()
    cmd = bun + [X_TO_MD_SCRIPT, url, '-o', output_path]

    print(f'📥 获取 X 推文: {url}')
    result = subprocess.run(cmd, env=env, input='y\n', capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f'❌ 获取失败: {result.stderr}')
        sys.exit(1)
    print(f'✅ 已保存到: {output_path}')
    return output_path


def fetch_web_url(url, output_path):
    """Fetch web URL using baoyu-url-to-markdown"""
    if not os.path.exists(URL_TO_MD_SCRIPT):
        print(f'❌ baoyu-url-to-markdown not found: {URL_TO_MD_SCRIPT}')
        print('   请先安装: cp -r baoyu-skills/skills/baoyu-url-to-markdown ~/.ai-skills/')
        sys.exit(1)

    bun = resolve_bun()
    cmd = bun + [URL_TO_MD_SCRIPT, url, '-o', output_path]

    print(f'📥 获取网页: {url}')
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f'❌ 获取失败: {result.stderr}')
        sys.exit(1)
    print(f'✅ 已保存到: {output_path}')
    return output_path

STYLES = {
    'storytelling': '叙事流畅，引人入胜，过渡自然，措辞生动',
    'formal': '正式、专业、中性语气，无口语化表达',
    'technical': '精确、简洁、术语密集，文档风格',
    'conversational': '口语化、亲切，像和朋友聊天',
    'academic': '学术、严谨，正式措辞',
    'humorous': '幽默、诙谐，保留并适配原文趣味',
    'literal': '尽量贴近原文结构，最小化重组',
    'elegant': '文学性强，节奏优美，措辞考究',
    'business': '简洁、结果导向，商务友好',
}

AUDIENCES = {
    'general': '普通读者，术语需要解释',
    'developer': '开发者/工程师，常见技术术语不需解释',
    'academic': '学术研究者，正式术语',
    'business': '商务人士，技术概念需通俗解释',
}


def fetch_url(url):
    """抓取 URL 内容"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; translate-skill/1.0)'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f'❌ 无法获取 URL: {e}', file=sys.stderr)
        sys.exit(1)


def load_glossary(glossary_file=None):
    """加载术语表"""
    terms = {}
    files = []
    if os.path.exists(GLOSSARY_FILE):
        files.append(GLOSSARY_FILE)
    if glossary_file and os.path.exists(glossary_file):
        files.append(glossary_file)

    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            for line in fh:
                line = line.strip()
                # 支持 | term | translation | 格式
                if '|' in line:
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 2 and parts[0] != 'English' and parts[0] != '---':
                        terms[parts[0]] = parts[1]
    return terms


def count_words(text):
    """Count words, treating CJK characters individually."""
    import re
    cjk = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]', text))
    latin = len(re.findall(r'[a-zA-Z0-9]+', text))
    return cjk + latin


def parse_md_blocks(text):
    """Parse markdown into structural blocks (heading sections, paragraphs, lists, etc.)."""
    import re
    lines = text.split('\n')
    blocks = []
    current_block = []
    in_frontmatter = False
    frontmatter = None

    i = 0
    # Handle YAML frontmatter
    if lines and lines[0].strip() == '---':
        fm_lines = ['---']
        for j in range(1, len(lines)):
            fm_lines.append(lines[j])
            if lines[j].strip() == '---':
                frontmatter = '\n'.join(fm_lines)
                i = j + 1
                break

    while i < len(lines):
        line = lines[i]

        # Heading → start new block
        if re.match(r'^#{1,6}\s', line):
            if current_block:
                blocks.append('\n'.join(current_block))
                current_block = []
            current_block.append(line)
        # Empty line → potential block boundary
        elif line.strip() == '':
            if current_block:
                current_block.append(line)
        # Content line
        else:
            # If previous block ended with empty lines and this is new content
            # check if we should split
            if current_block and all(l.strip() == '' for l in current_block[-2:] if current_block):
                # Double empty line = definite block boundary
                text_part = '\n'.join(current_block).rstrip()
                if text_part:
                    blocks.append(text_part)
                current_block = [line]
            else:
                current_block.append(line)
        i += 1

    if current_block:
        text_part = '\n'.join(current_block).rstrip()
        if text_part:
            blocks.append(text_part)

    return frontmatter, blocks


def chunk_text(text, max_words=4000):
    """Split text into chunks at Markdown structural boundaries.
    
    Priority: heading boundaries > paragraph boundaries > line-level fallback.
    """
    frontmatter, blocks = parse_md_blocks(text)

    # Group blocks into chunks respecting max_words
    chunks = []
    current_blocks = []
    current_words = 0

    for block in blocks:
        block_words = count_words(block)

        # If single block exceeds max, split it by paragraphs/lines
        if block_words > max_words:
            # Flush current
            if current_blocks:
                chunks.append('\n\n'.join(current_blocks))
                current_blocks = []
                current_words = 0

            # Split oversized block by double-newline (paragraphs)
            sub_parts = block.split('\n\n')
            sub_current = []
            sub_words = 0
            for part in sub_parts:
                pw = count_words(part)
                if sub_words + pw > max_words and sub_current:
                    chunks.append('\n\n'.join(sub_current))
                    sub_current = [part]
                    sub_words = pw
                else:
                    sub_current.append(part)
                    sub_words += pw
            if sub_current:
                chunks.append('\n\n'.join(sub_current))
            continue

        # Normal case: add block to current chunk
        if current_words + block_words > max_words and current_blocks:
            chunks.append('\n\n'.join(current_blocks))
            current_blocks = [block]
            current_words = block_words
        else:
            current_blocks.append(block)
            current_words += block_words

    if current_blocks:
        chunks.append('\n\n'.join(current_blocks))

    # Prepend frontmatter to first chunk if exists
    if frontmatter and chunks:
        chunks[0] = frontmatter + '\n\n' + chunks[0]
    elif frontmatter:
        chunks = [frontmatter]

    return chunks


def build_prompt(text, args, glossary, mode='normal'):
    """构建翻译 prompt"""
    style_desc = STYLES.get(args.style, args.style)
    audience_desc = AUDIENCES.get(args.audience, args.audience)

    glossary_section = ''
    if glossary:
        glossary_lines = [f'  - {k} → {v}' for k, v in list(glossary.items())[:50]]
        glossary_section = '\n术语表（请遵循）：\n' + '\n'.join(glossary_lines)

    if mode == 'quick':
        prompt = textwrap.dedent(f"""
请将以下内容翻译为 {args.to}。

翻译要求：
- 风格：{style_desc}
- 目标受众：{audience_desc}
- 准确翻译，意译优于直译
- 保留所有 Markdown 格式
- 术语首次出现时括号标注原文
- 比喻和习语按含义翻译{glossary_section}

原文：
{text}
""").strip()

    elif mode == 'analysis':
        prompt = textwrap.dedent(f"""
请分析以下文章，输出分析报告（用 Markdown 格式）：

1. **领域**：文章所属领域
2. **语气和风格**：原文写作风格
3. **核心术语**：提取关键术语并建议翻译
4. **翻译难点**：可能的翻译挑战
5. **比喻和习语**：原文中的比喻表达及建议处理方式

原文：
{text}
""").strip()

    elif mode == 'translate_with_analysis':
        prompt = textwrap.dedent(f"""
基于之前的分析，请将以下内容翻译为 {args.to}。

翻译要求：
- 风格：{style_desc}
- 目标受众：{audience_desc}
- 准确翻译，意译优于直译
- 保留所有 Markdown 格式
- 术语首次出现时括号标注原文
- 比喻和习语按含义翻译
- 对目标读者可能不理解的概念，添加简短译者注{glossary_section}

原文：
{text}
""").strip()

    elif mode == 'review':
        prompt = textwrap.dedent(f"""
请审校以下翻译，指出问题：

1. **准确性**：是否有翻译错误或遗漏
2. **欧化表达**：是否有不自然的翻译腔
3. **术语一致性**：术语翻译是否统一
4. **流畅度**：是否通顺易读

翻译稿：
{text}
""").strip()

    elif mode == 'polish':
        prompt = textwrap.dedent(f"""
基于审校意见，请润色以下翻译至出版级质量：

- 修复所有指出的问题
- 消除翻译腔，使用地道的目标语言表达
- 保持原文信息完整
- 保留 Markdown 格式

翻译稿：
{text}
""").strip()

    else:
        prompt = ''

    return prompt


def main():
    parser = argparse.ArgumentParser(description='通用翻译工具')
    parser.add_argument('source', nargs='?', help='源文件路径')
    parser.add_argument('--fetch', help='自动获取 URL 内容（X 推文或网页）并翻译')
    parser.add_argument('--to', default='zh-CN', help='目标语言 (默认: zh-CN)')
    parser.add_argument('--from', dest='from_lang', help='源语言 (自动检测)')
    parser.add_argument('--mode', default='normal',
                        choices=['quick', 'normal', 'refined'],
                        help='翻译模式 (默认: normal)')
    parser.add_argument('--style', default='storytelling',
                        help=f'翻译风格: {", ".join(STYLES.keys())}')
    parser.add_argument('--audience', default='general',
                        help=f'目标受众: {", ".join(AUDIENCES.keys())}')
    parser.add_argument('--glossary', help='额外术语表文件')
    parser.add_argument('--stdout', action='store_true',
                        help='输出 prompt 到 stdout（供 Agent 直接使用）')
    parser.add_argument('--output-dir', help='自定义输出目录')
    parser.add_argument('--chunk-threshold', type=int, default=4000,
                        help='分块阈值 (默认: 4000 词)')

    args = parser.parse_args()

    # Handle --fetch: auto-fetch content from URL
    if args.fetch:
        url = args.fetch
        fetch_dir = os.path.join(os.getcwd(), 'translate-fetch')
        os.makedirs(fetch_dir, exist_ok=True)

        if is_x_url(url):
            # X tweet/article
            slug = re.sub(r'[^\w]', '-', url.split('/')[-1])[:30]
            output_path = os.path.join(fetch_dir, f'x-{slug}.md')
            fetch_x_tweet(url, output_path)
        else:
            # Regular web URL
            slug = re.sub(r'[^\w]', '-', url.split('/')[-1])[:30]
            output_path = os.path.join(fetch_dir, f'web-{slug}.md')
            fetch_web_url(url, output_path)

        args.source = output_path
        print()

    if not args.source:
        parser.error('请指定源文件路径，或使用 --fetch <url> 获取内容')

    # 读取源内容
    if args.source.startswith('http://') or args.source.startswith('https://'):
        print(f'🌐 获取 URL: {args.source}')
        text = fetch_url(args.source)
        source_name = 'url-content'
        source_dir = os.getcwd()
    elif os.path.isfile(args.source):
        with open(args.source, 'r', encoding='utf-8') as f:
            text = f.read()
        source_name = os.path.splitext(os.path.basename(args.source))[0]
        source_dir = os.path.dirname(os.path.abspath(args.source))
    else:
        print(f'❌ 文件不存在: {args.source}')
        sys.exit(1)

    # 加载术语表
    glossary = load_glossary(args.glossary)

    # 创建输出目录
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = os.path.join(source_dir, f'{source_name}-{args.to}')
    os.makedirs(output_dir, exist_ok=True)

    word_count = len(text.split())
    print(f'📄 源文件: {args.source}')
    print(f'📊 字数: ~{word_count} 词')
    print(f'🎯 目标: {args.to} | 模式: {args.mode} | 风格: {args.style}')
    print(f'📁 输出: {output_dir}/')
    print()

    # 检查分块
    needs_chunking = word_count >= args.chunk_threshold and args.mode != 'quick'
    if needs_chunking:
        chunks = chunk_text(text, args.chunk_threshold)
        print(f'📦 长文拆分为 {len(chunks)} 个块')
    else:
        chunks = [text]

    # 生成翻译 prompt
    if args.mode == 'quick':
        # Quick: 直接翻译
        for i, chunk in enumerate(chunks):
            prompt = build_prompt(chunk, args, glossary, 'quick')
            if args.stdout:
                print(prompt)
            else:
                prompt_file = os.path.join(output_dir, f'prompt-{i+1:02d}.md' if len(chunks) > 1 else 'prompt.md')
                with open(prompt_file, 'w', encoding='utf-8') as f:
                    f.write(prompt)

        if not args.stdout:
            print('✅ 翻译 prompt 已生成', file=sys.stderr)
            print(file=sys.stderr)
            print('📝 请将以下文件的内容发送给 AI 进行翻译：', file=sys.stderr)
            for i in range(len(chunks)):
                name = f'prompt-{i+1:02d}.md' if len(chunks) > 1 else 'prompt.md'
                print(f'   {output_dir}/{name}', file=sys.stderr)
            print(f'\n💾 将翻译结果保存到: {output_dir}/translation.md', file=sys.stderr)

    elif args.mode == 'normal':
        # Normal: 分析 → 翻译
        # Step 1: 分析 prompt
        analysis_prompt = build_prompt(text[:3000], args, glossary, 'analysis')
        with open(os.path.join(output_dir, '01-analysis-prompt.md'), 'w', encoding='utf-8') as f:
            f.write(analysis_prompt)

        # Step 2: 翻译 prompt
        for i, chunk in enumerate(chunks):
            prompt = build_prompt(chunk, args, glossary, 'translate_with_analysis')
            name = f'02-translate-prompt-{i+1:02d}.md' if len(chunks) > 1 else '02-translate-prompt.md'
            with open(os.path.join(output_dir, name), 'w', encoding='utf-8') as f:
                f.write(prompt)

        print('✅ 翻译 prompt 已生成')
        print()
        print('📝 请按顺序发送给 AI：')
        print(f'   1. {output_dir}/01-analysis-prompt.md （分析原文）')
        print(f'   2. {output_dir}/02-translate-prompt*.md （翻译）')
        print(f'\n💾 将翻译结果保存到: {output_dir}/translation.md')

    elif args.mode == 'refined':
        # Refined: 分析 → 翻译 → 审校 → 润色
        analysis_prompt = build_prompt(text[:3000], args, glossary, 'analysis')
        with open(os.path.join(output_dir, '01-analysis-prompt.md'), 'w', encoding='utf-8') as f:
            f.write(analysis_prompt)

        for i, chunk in enumerate(chunks):
            prompt = build_prompt(chunk, args, glossary, 'translate_with_analysis')
            name = f'02-translate-prompt-{i+1:02d}.md' if len(chunks) > 1 else '02-translate-prompt.md'
            with open(os.path.join(output_dir, name), 'w', encoding='utf-8') as f:
                f.write(prompt)

        # 审校和润色 prompt 模板
        review_prompt = build_prompt('[翻译结果放这里]', args, glossary, 'review')
        with open(os.path.join(output_dir, '03-review-prompt.md'), 'w', encoding='utf-8') as f:
            f.write(review_prompt)

        polish_prompt = build_prompt('[审校后的翻译放这里]', args, glossary, 'polish')
        with open(os.path.join(output_dir, '04-polish-prompt.md'), 'w', encoding='utf-8') as f:
            f.write(polish_prompt)

        print('✅ 翻译 prompt 已生成')
        print()
        print('📝 请按顺序发送给 AI：')
        print(f'   1. {output_dir}/01-analysis-prompt.md （分析原文）')
        print(f'   2. {output_dir}/02-translate-prompt*.md （翻译初稿）')
        print(f'   3. {output_dir}/03-review-prompt.md （审校）')
        print(f'   4. {output_dir}/04-polish-prompt.md （润色）')
        print(f'\n💾 将最终翻译保存到: {output_dir}/translation.md')

    print()
    print(f'📚 术语表: {len(glossary)} 条')
    if glossary:
        for k, v in list(glossary.items())[:5]:
            print(f'   {k} → {v}')
        if len(glossary) > 5:
            print(f'   ... (还有 {len(glossary) - 5} 条)')


if __name__ == '__main__':
    main()
