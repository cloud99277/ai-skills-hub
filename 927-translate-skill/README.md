[English](README.md) | [简体中文](README_CN.md)

<div align="center">

# 🌐 927 Translate Skill

**A universal AI-powered translation skill for all agents**

[![Author](https://img.shields.io/badge/Author-Cloud927-blue?style=flat-square)](https://github.com/cloud99277)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](../../LICENSE)
[![Part of](https://img.shields.io/badge/Part%20of-AI%20Skills%20Hub-orange?style=flat-square)](https://github.com/cloud99277/ai-skills-hub)

</div>

## ✨ Features

- 🤖 **Cross-Agent Compatible** — Works with Claude Code, Codex CLI, Gemini CLI, and any skill-aware AI agent
- 📰 **One-Click Fetch & Translate** — Directly fetch **web articles** and **X (Twitter) posts/articles**, auto-convert to Markdown, then translate
- 💬 **Meaning-First Translation** — Translates the author's intent, not word-by-word; eliminates "translationese"
- 📋 **Three Translation Modes** — quick / normal / refined (publication-quality)
- 🔍 **CJK Europeanization Detection** — Automatically detects and eliminates passive voice abuse, excessive connectives, noun piling, and other translationese issues in CJK targets
- 📦 **Smart Chunking** — Splits long documents at Markdown structural boundaries (headings > paragraphs > lines) without breaking paragraphs
- 📚 **Multi-Domain Glossary** — Built-in EN→ZH glossary covering AI/Tech, Business, Philosophy, and Creator Economy

## 🚀 Quick Start

### Option 1: Agent Direct Translation (Recommended)

The AI agent reads `SKILL.md` and translates directly following the translation principles. No script required. Best for short texts and tweets.

### Option 2: Script-Assisted Translation

The script handles **content fetching** and **smart chunking**; the agent does the translation:

```bash
# Translate a local file
python3 scripts/translate.py article.md --to zh-CN

# Fetch and translate an X tweet
python3 scripts/translate.py --fetch https://x.com/user/status/123 --to zh-CN

# Fetch and translate a web article
python3 scripts/translate.py --fetch https://example.com/article --to zh-CN

# Output prompt to stdout (for agent direct consumption)
python3 scripts/translate.py article.md --stdout
```

## 📖 Translation Modes

| Mode | Steps | Use Case |
|------|-------|----------|
| `quick` | Direct translation | Short texts, tweets, quick understanding |
| `normal` | Analyze → Translate | General articles (**default**) |
| `refined` | Analyze → Draft → Review → Polish | Important documents, publication-quality |

### Normal Mode
1. **Analyze** → `01-analysis.md`
2. **Translate** → `translation.md`

### Refined Mode (Publication-Quality)
1. **Analyze** → `01-analysis.md` (domain, tone, terminology, metaphor mapping)
2. **Draft** → `03-draft.md`
3. **Review** → `04-critique.md` (diagnosis only, no edits)
4. **Revise** → `05-revision.md`
5. **Polish** → `translation.md` (final publication-quality output)

See [references/refined-workflow.md](references/refined-workflow.md) for detailed steps.

## 🎨 Translation Styles & Audiences

### Styles

| Style | Description |
|-------|-------------|
| `storytelling` | Smooth narrative, engaging (**default**) |
| `formal` | Professional, neutral |
| `technical` | Precise, documentation-style |
| `conversational` | Casual, friendly |
| `academic` | Scholarly, rigorous |
| `elegant` | Literary, polished |
| `humorous` | Preserves and adapts humor |
| `business` | Concise, results-oriented |

Custom descriptions also supported: `--style "poetic and lyrical"`

### Target Audiences

| Audience | Effect |
|----------|--------|
| `general` | Plain language, annotated terms (**default**) |
| `developer` | Technical audience, fewer annotations |
| `academic` | Formal terminology |
| `business` | Concise, results-oriented |

Custom descriptions also supported: `--audience "general readers interested in AI"`

## ⚙️ Options

```bash
python3 scripts/translate.py [source] [options]

# Positional
source              Source file path

# Options
--fetch <url>       Fetch URL content (X tweets or web pages)
--to <lang>         Target language (default: zh-CN)
--mode <mode>       Translation mode: quick|normal|refined (default: normal)
--style <style>     Translation style (default: storytelling)
--audience <aud>    Target audience (default: general)
--glossary <file>   Additional glossary file
--stdout            Output prompt to stdout instead of file
--output-dir <dir>  Custom output directory
--chunk-threshold   Chunking threshold in words (default: 4000)
```

## 📁 Output Structure

```
{source-name}-{target-lang}/
├── translation.md       # Final translation
├── 01-analysis.md       # Content analysis (normal/refined)
├── 03-draft.md          # Draft (refined)
├── 04-critique.md       # Review findings (refined)
├── 05-revision.md       # Revised draft (refined)
└── chunks/              # Long document chunks (if any)
```

## 📚 Glossary

Built-in EN→ZH glossary organized by domain:

- **AI & Tech** — AI Agent, Vibe Coding, Context Engineering, Hallucination, etc.
- **Business & Strategy** — Moat, Flywheel, Product-Market Fit, etc.
- **Philosophy & Psychology** — Agency, Sensemaking, Meaning Crisis, etc.
- **Creator Economy** — Creator Economy, Attention Economy, Skill Stack, etc.

Only includes non-obvious or easily mistranslated terms. Use `--glossary` to add project-level glossaries.

## 🙏 Acknowledgments

This project was inspired by the translation skill in [baoyu-skills](https://github.com/JimLiu/baoyu-skills) by [JimLiu (宝玉)](https://github.com/JimLiu). Thanks for the pioneering work in AI agent-assisted translation.

---

<div align="center">

**Made with ❤️ by [Cloud927](https://github.com/cloud99277)**

*Part of the [AI Skills Hub](https://github.com/cloud99277/ai-skills-hub) ecosystem*

</div>
