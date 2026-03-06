[简体中文](README_CN.md) | [English](README.md)

<div align="center">

# 🌐 927 Translate Skill

**跨 AI Agent 的通用翻译技能 —— 一次配置，所有 Agent 共享**

[![Author](https://img.shields.io/badge/Author-Cloud927-blue?style=flat-square)](https://github.com/cloud99277)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](../../LICENSE)
[![Part of](https://img.shields.io/badge/Part%20of-AI%20Skills%20Hub-orange?style=flat-square)](https://github.com/cloud99277/ai-skills-hub)

</div>

## ✨ 特点

- 🤖 **跨 Agent 兼容** — 支持 Claude Code、Codex CLI、Gemini CLI 及任何支持 skill 的 AI Agent
- 📰 **一键抓取翻译** — 直接抓取**网页文章**和 **X (Twitter) 推文/Article**，自动转 Markdown 后翻译
- 💬 **意译优先** — 翻译作者的意思，而非逐字翻译，消除翻译腔
- 📋 **三种翻译模式** — quick（快速）/ normal（标准）/ refined（出版级）
- 🔍 **CJK 欧化语言检测** — 自动识别并消除被动语态滥用、多余连接词、名词堆砌等翻译腔问题
- 📦 **智能分块** — 长文按 Markdown 结构边界分块（标题 > 段落 > 行），不会切断段落
- 📚 **多领域术语表** — 内置 AI/Tech、Business、Philosophy、Creator Economy 四大领域术语

## 🚀 快速开始

### 方式一：Agent 直接翻译（推荐）

AI Agent 读取 `SKILL.md` 后，按翻译原则直接翻译，无需运行脚本。适合短文、推文等。

### 方式二：脚本辅助翻译

脚本负责**内容获取**和**智能分块**，翻译由 Agent 完成：

```bash
# 翻译本地文件
python3 scripts/translate.py article.md --to zh-CN

# 一键抓取并翻译 X 推文
python3 scripts/translate.py --fetch https://x.com/user/status/123 --to zh-CN

# 一键抓取并翻译网页文章
python3 scripts/translate.py --fetch https://example.com/article --to zh-CN

# 输出 prompt 到 stdout（Agent 直接消费）
python3 scripts/translate.py article.md --stdout
```

## 📖 翻译模式

| 模式 | 步骤 | 适用场景 |
|------|------|----------|
| `quick` | 直接翻译 | 短文、推文、快速了解 |
| `normal` | 分析 → 翻译 | 一般文章（**默认**） |
| `refined` | 分析 → 初稿 → 审校 → 润色 | 重要文档、出版级 |

### Normal 模式
1. **分析原文** → `01-analysis.md`
2. **翻译** → `translation.md`

### Refined 模式（出版级）
1. **分析** → `01-analysis.md`（领域、语气、术语、比喻映射）
2. **初稿** → `03-draft.md`
3. **审校** → `04-critique.md`（仅诊断，不修改）
4. **修订** → `05-revision.md`
5. **润色** → `translation.md`（出版级最终稿）

详细步骤见 [references/refined-workflow.md](references/refined-workflow.md)

## 🎨 翻译风格 & 目标受众

### 翻译风格

| 风格 | 说明 |
|------|------|
| `storytelling` | 叙事流畅，引人入胜（**默认**） |
| `formal` | 正式、专业 |
| `technical` | 精确、文档风格 |
| `conversational` | 口语化、亲切 |
| `academic` | 学术、严谨 |
| `elegant` | 文学、精雕细琢 |
| `humorous` | 保留并改编幽默 |
| `business` | 简洁、结果导向 |

也支持自定义描述：`--style "诗意而抒情"`

### 目标受众

| 受众 | 效果 |
|------|------|
| `general` | 通俗语言，术语加注释（**默认**） |
| `developer` | 技术人员，少注释常见术语 |
| `academic` | 学术读者，正式措辞 |
| `business` | 商务人士，简洁结果导向 |

也支持自定义：`--audience "对 AI 感兴趣的普通读者"`

## ⚙️ 配置选项

```bash
python3 scripts/translate.py [source] [options]

# 位置参数
source              源文件路径

# 选项
--fetch <url>       自动获取 URL 内容（X 推文或网页）
--to <lang>         目标语言（默认: zh-CN）
--mode <mode>       翻译模式: quick|normal|refined（默认: normal）
--style <style>     翻译风格（默认: storytelling）
--audience <aud>    目标受众（默认: general）
--glossary <file>   额外术语表文件
--stdout            将 prompt 输出到 stdout 而非文件
--output-dir <dir>  自定义输出目录
--chunk-threshold   分块阈值，单位词数（默认: 4000）
```

## 📁 输出结构

```
{source-name}-{target-lang}/
├── translation.md       # 最终翻译
├── 01-analysis.md       # 内容分析（normal/refined）
├── 03-draft.md          # 初稿（refined）
├── 04-critique.md       # 审校发现（refined）
├── 05-revision.md       # 修订稿（refined）
└── chunks/              # 长文分块（如有）
```

## 📚 术语表

内置 EN→ZH 术语表，按领域分类：

- **AI & Tech** — AI Agent、Vibe Coding、Context Engineering、Hallucination 等
- **Business & Strategy** — Moat、Flywheel、Product-Market Fit 等
- **Philosophy & Psychology** — Agency、Sensemaking、Meaning Crisis 等
- **Creator Economy** — Creator Economy、Attention Economy、Skill Stack 等

仅收录易错/非显而易见的翻译，可通过 `--glossary` 追加项目级术语表。

## 🙏 致谢

本项目受到 [宝玉 (JimLiu)](https://github.com/JimLiu) 的 [baoyu-skills](https://github.com/JimLiu/baoyu-skills) 翻译技能启发，感谢他在 AI Agent 辅助翻译领域的开创性工作。

---

<div align="center">

**Made with ❤️ by [Cloud927](https://github.com/cloud99277)**

*Part of the [AI Skills Hub](https://github.com/cloud99277/ai-skills-hub) ecosystem*

</div>
