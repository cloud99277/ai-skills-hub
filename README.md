[English](README.md) | [简体中文](README_CN.md)

<div align="center">

# 🧠 AI Skills Hub

**One repository. Every AI agent. Shared skills.**

[![Author](https://img.shields.io/badge/Author-Cloud927-blue?style=flat-square)](https://github.com/cloud99277)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-2+-brightgreen?style=flat-square)](#-built-in-skills)

</div>

## ✨ Features

- 🔗 **One Place, All Agents** — Claude, Codex, Gemini share skills through symlinks to a single repository
- 🛠️ **Complete Toolchain** — Create, validate, lint, and generate skills with built-in tools
- 📐 **Progressive Disclosure** — Metadata → Body → Resources, three-level loading to save context window
- 🔌 **Plug & Play** — New AI tool? One `ln -s` command and it's connected
- 📦 **Examples Included** — From hello-world to full skills with scripts, ready to learn from

## 🤔 Why?

If you use multiple AI coding assistants, you've probably noticed the problem: each tool has its own isolated skill/knowledge system. You end up duplicating skills, maintaining them separately, and dealing with inconsistencies.

AI Skills Hub solves this with a simple architecture:

```
~/.claude/skills  ──┐
~/.codex/skills   ──┤
~/.gemini/skills  ──┼──→  ~/.ai-skills  (this repository)
~/.agents/skills  ──┘
```

All agent entry points are symlinks to one centralized repository. **Update once, all agents benefit.**

## 🚀 Quick Start

### 1. Clone

```bash
git clone https://github.com/cloud99277/ai-skills-hub.git
cd ai-skills-hub
```

### 2. Setup

```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Link the repository to `~/.ai-skills`
- Create symlinks for Claude, Codex, Gemini, and generic agents
- Check that Python 3 and PyYAML are installed
- Run a self-test to verify everything works

### 3. Create Your First Skill

```bash
python3 ~/.ai-skills/.system/skill-creator/scripts/init_skill.py my-first-skill \
    --path ~/.ai-skills \
    --resources scripts
```

### 4. Validate

```bash
# Single skill check
python3 ~/.ai-skills/.system/skill-creator/scripts/quick_validate.py ~/.ai-skills/my-first-skill

# Repository-wide lint
python3 ~/.ai-skills/.system/skill-creator/scripts/lint_skills.py ~/.ai-skills
```

## 📖 What's a Skill?

A skill is a self-contained directory with a `SKILL.md` file that gives an AI agent specialized knowledge, workflows, or tools for a specific domain.

```
my-skill/
├── SKILL.md           ← Required: frontmatter + instructions
├── agents/            ← Recommended: UI metadata
│   └── openai.yaml
├── scripts/           ← Optional: executable helpers
├── references/        ← Optional: detailed docs for context
└── assets/            ← Optional: templates, images, fonts
```

### The Most Important Part: `description`

The YAML frontmatter `description` is the **primary routing mechanism** — it tells agents when to use the skill:

```yaml
---
name: my-skill
description: Converts PDF documents to clean Markdown text. Use when the user wants
  to extract text from PDFs, convert PDF to Markdown, or process PDF documents for
  text analysis. Not for image-heavy PDFs; prefer pdf-ocr for scanned documents.
---
```

A good description answers: **What does it do? When should it trigger? What should it NOT handle?**

## 📦 Built-in Skills

| Skill | Description |
|-------|-------------|
| [927-translate-skill](927-translate-skill/) | 🌐 Universal translation skill — web/tweet fetching, 3 modes, CJK europeanization detection |
| [skill-lint](skill-lint/) | 🔍 Repository-wide skill quality linting |

## 🏗️ Repository Structure

```
ai-skills-hub/
├── .system/                    ← Core infrastructure (skill creation toolchain)
│   └── skill-creator/
│       ├── SKILL.md            ← Design principles and creation guide
│       └── scripts/            ← init, validate, lint, generate tools
├── 927-translate-skill/        ← Universal translation skill (all agents)
├── skill-lint/                 ← Built-in repository linting skill
├── _examples/                  ← Example skills to learn from
│   ├── hello-world/            ← Minimal skill (just SKILL.md)
│   └── with-scripts/           ← Skill with bundled scripts
├── docs/
│   ├── ARCHITECTURE.md         ← System design and concepts
│   └── CONVENTIONS.md          ← Naming, frontmatter, routing standards
├── setup.sh                    ← One-click installation
└── uninstall.sh                ← Clean removal
```

## 🛠️ Toolchain

| Tool | Scope | Purpose |
|------|-------|---------|
| `init_skill.py` | New skill | Generate skill directory skeleton |
| `quick_validate.py` | Single skill | Structural validation (frontmatter, naming) |
| `lint_skills.py` | Full repo | Routing quality + consistency checks |
| `generate_openai_yaml.py` | Single skill | Generate UI metadata |
| `skill-lint` (skill) | Full repo | Same as lint_skills.py, as a reusable skill |

## 🔌 Adding a New Agent

If a new AI tool stores skills at `~/.newtool/skills/`, just add a symlink:

```bash
ln -s ~/.ai-skills ~/.newtool/skills
```

Done. The new tool instantly has access to all shared skills.

## 🏗️ Core Design

### Progressive Disclosure

Skills load in three levels to save context window space:

1. **Metadata** (always loaded) — `name` + `description` (~100 words)
2. **Body** (on trigger) — SKILL.md instructions (<5k words)
3. **Resources** (on demand) — scripts, references, assets (unlimited)

### Routing Priority

When multiple skills could match:

1. Platform-specific > generic
2. Tech-stack-specific > general
3. Output-specific > broad capability
4. Newer version > legacy
5. Generic only as fallback

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) — System design, progressive disclosure, validation pipeline
- [Conventions](docs/CONVENTIONS.md) — Naming, frontmatter, routing, lifecycle, governance

## 🗑️ Uninstall

```bash
chmod +x uninstall.sh
./uninstall.sh
```

This removes symlinks only. Your skills and the repository itself are not deleted.

## 📄 License

[MIT](LICENSE)

---

<div align="center">

**Made with ❤️ by [Cloud927](https://github.com/cloud99277)**

</div>
