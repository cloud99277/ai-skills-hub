[English](README.md) | [简体中文](README_CN.md)

<div align="center">

# 🧠 AI Skills Hub

**Curated skills for every AI agent. Pick what you need.**

[![Author](https://img.shields.io/badge/Author-Cloud927-blue?style=flat-square)](https://github.com/cloud99277)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-62-brightgreen?style=flat-square)](#-built-in-skills)

</div>

This repository contains **62 curated skills** that have passed the KitClaw skill-admission quality gate. All skills work across Claude Code, Codex CLI, Gemini CLI, and any agent using the `SKILL.md` contract.

This is the companion repository to [KitClaw](https://github.com/cloud99277/KitClaw), which ships the 16 core platform skills (memory, governance, orchestration).

## ✨ Features

- 🔗 **One Place, All Agents** — Claude, Codex, Gemini share skills through symlinks to a single repository
- ✅ **Quality Guaranteed** — Every skill passes admission checks (lint, security, self-contained, agent-agnostic)
- 📦 **Selective Install** — Clone the whole repo or cherry-pick individual skills
- 🔌 **Plug & Play** — New AI tool? One `ln -s` command and it's connected

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/cloud99277/ai-skills-hub.git
cd ai-skills-hub
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Link the repository to `~/.ai-skills`
- Create symlinks for Claude, Codex, Gemini, and generic agents

### 2. Or: Install Selectively

If you only want specific skills, copy them individually:

```bash
# Example: install just code-review and python-patterns
cp -r ai-skills-hub/code-review ~/.ai-skills/
cp -r ai-skills-hub/python-patterns ~/.ai-skills/
```

## 📖 What's a Skill?

A skill is a self-contained directory with a `SKILL.md` file that gives an AI agent specialized knowledge, workflows, or tools for a specific domain.

```
my-skill/
├── SKILL.md           ← Required: frontmatter + instructions
├── scripts/           ← Optional: executable helpers
├── references/        ← Optional: detailed docs for context
└── assets/            ← Optional: templates, images, fonts
```

## 📦 Built-in Skills (62)

### Coding & Development

| Skill | Description |
|---|---|
| code-review | Review code changes for quality, readability, architecture |
| python-patterns | Pythonic idioms, PEP 8 guidance, typing, maintainable code |
| golang-patterns | Idiomatic Go patterns, best practices, and conventions |
| coding-standards | Universal coding standards for TypeScript, Python, Go |
| tdd-workflow | Test-driven development workflow |
| e2e-testing | Playwright E2E testing patterns, Page Object Model |
| security-scan | Scan configurations for security vulnerabilities |
| security-review | Review application changes for security risks |
| database-migrations | Database migration best practices for schema changes |
| postgres-patterns | PostgreSQL schema design, query optimization |
| api-design | REST API design patterns for production services |
| golang-testing | Go testing patterns: table-driven, subtests, benchmarks |
| python-testing | Python testing with pytest, fixtures, mocking |

### Frontend & Design

| Skill | Description |
|---|---|
| frontend-patterns | Frontend development patterns for React and Next.js |
| frontend-slides | Design-forward, browser-native HTML/CSS/JS presentations |
| popular-web-designs | 54 production-quality design systems extracted from real sites |

### Research & Analysis

| Skill | Description |
|---|---|
| deep-research | Systematic technical research — compare open-source tools |
| market-research | Market research, competitive analysis, investor data |
| eval-harness | Build repeatable evaluations and regression benchmarks |
| project-audit | Architectural reviews of project documents |
| product-manager-review | Rigorous PM review of project plans |
| project-retrospective | Capture execution experience, distill new patterns |

### Writing & Publishing

| Skill | Description |
|---|---|
| article-writing | Write or refine polished long-form content |
| baoyu-html-deck | Lightweight single-file HTML presentation generator |
| baoyu-slide-deck | Image-first slide deck workspace from content |
| baoyu-infographic | Publication-ready infographic image from content |
| baoyu-cover-image | Cover or hero image for articles |
| baoyu-article-illustrator | Visual illustrations for article sections |
| baoyu-comic | Multi-page educational comic with storyboards |
| baoyu-xhs-images | Xiaohongshu/RedNote multi-image card series |
| baoyu-format-markdown | Markdown cleanup and structuring workflow |
| baoyu-markdown-to-html | Markdown-to-HTML rendering for WeChat and similar |
| baoyu-compress-image | Compress images or image directories |
| china-content-compliance | Content filtering and rewriting for China mainland |

### Translation & Language

| Skill | Description |
|---|---|
| translate | Universal translation tool (all agents) |
| 927-translate-skill | Universal translation — web/tweet fetching, 3 modes, CJK detection |

### Automation & DevOps

| Skill | Description |
|---|---|
| coding-agent | Delegate coding tasks to Codex, Claude Code, or Pi agents |
| claude-code | Delegate coding tasks to Claude Code CLI |
| codex | Delegate coding tasks to OpenAI Codex CLI |
| full-cycle-builder | Quality-gate-driven development lifecycle |
| deployment-patterns | Deployment workflows, CI/CD, containerization |
| docker-patterns | Docker and Compose patterns for local development |
| continuous-learning-v2 | Learn reusable behaviors from repeated patterns |
| cost-aware-llm-pipeline | Cost optimization patterns for LLM API usage |

### Content & Social Media

| Skill | Description |
|---|---|
| content-engine | Review and optimize platform-native content |
| content-for-x | Prepare X (Twitter) content packages |
| baoyu-url-to-markdown | Fetch URLs and convert to markdown via Chrome CDP |
| baoyu-danger-x-to-markdown | Convert X tweets and articles to markdown |
| baoyu-danger-gemini-web | Gemini Web access for text/image generation |
| xhs-tunnel | Cloudflare Tunnel for mobile preview and testing |

### ML & MLOps

| Skill | Description |
|---|---|
| eval-harness | Evaluation benchmarks and experiment tracking |
| content-hash-cache-pattern | Cache file-processing results using SHA-256 |

### Project Management

| Skill | Description |
|---|---|
| project-planner | Plan and structure new projects from inspiration |
| project-guidelines-example | Template for project-specific skills and conventions |
| design-iteration | Drive document revision based on audit findings |
| product-manager-review | Rigorous PM review of project plans |

### Utilities & Tools

| Skill | Description |
|---|---|
| find-skills | Search for skills across repositories |
| regex-vs-llm-structured-text | Decision framework: regex vs LLM for text processing |
| strategic-compact | Suggest manual context compaction at task boundaries |
| ppt-template-skill | Generate or refine editable .pptx skeletons |
| brain-link | Install brain-inject shell integration |
| history-reader | Retrieve and summarize Claude local chat history |
| history-chat | Retrieve and summarize Codex local chat history |
| iterative-retrieval | Progressive codebase context retrieval for large repos |
| search-first | Research existing tools, libraries, MCP servers, skills |

### Agent Integration

| Skill | Description |
|---|---|
| add-provider | Add or update Codex provider from base URL |
| codex-cli-trigger | Route requests to delegate coding to Codex |
| codex-provider-bootstrap | Bootstrap a Codex local provider |
| gemini-cli-trigger | Route requests to delegate tasks to Gemini |
| agent-reach | Give your agent eyes to see the entire internet |
| switch-model | Interactively switch OpenClaw AI model |
| tacit-mining | Extract tacit knowledge from user interactions |
| personal-dossier-builder | Build a living personal dossier from existing data |

## 🏗️ Repository Structure

```
ai-skills-hub/
├── .system/                    ← Core infrastructure (skill creation toolchain)
│   └── skill-creator/
│       ├── SKILL.md            ← Design principles and creation guide
│       └── scripts/            ← init, validate, lint, generate tools
├── (62 skill directories)      ← All pass skill-admission quality gate
├── _examples/                  ← Example skills to learn from
│   ├── hello-world/            ← Minimal skill (just SKILL.md)
│   └── with-scripts/           ← Skill with bundled scripts
├── docs/
│   ├── ARCHITECTURE.md         ← System design and concepts
│   └── CONVENTIONS.md          ← Naming, frontmatter, routing standards
├── setup.sh                    ← One-click installation
└── uninstall.sh                ← Clean removal
```

## Skill Quality

Every skill in this repository passes the **skill-admission** quality gate from KitClaw:

| Check | What it validates |
|---|---|
| Lint | Frontmatter has `name` + `description`, naming conventions, routing quality |
| Security | No hardcoded secrets, no dangerous commands, no API key patterns |
| No personal deps | No hardcoded user paths (`/home/xxx`, `/Users/xxx`) |
| Agent-agnostic | Works across Claude, Codex, Gemini — no agent-specific syntax |
| Self-contained | All referenced files (scripts, references) exist within the skill |
| Clean structure | No README.md, banner images, or other non-standard files |

## 🔌 Adding a New Agent

If a new AI tool stores skills at `~/.newtool/skills/`, just add a symlink:

```bash
ln -s ~/.ai-skills ~/.newtool/skills
```

Done. The new tool instantly has access to all shared skills.

## Relationship to KitClaw

| | KitClaw | AI Skills Hub |
|---|---|---|
| **Purpose** | Platform runtime | Skill collection |
| **Contains** | 16 core skills + memory + governance | 62 curated ecosystem skills |
| **Required?** | Yes — provides the infrastructure | No — pick what you need |
| **Skill scope** | Memory, lint, observability, admission | Coding, research, publishing, automation |

Install KitClaw first for the runtime, then browse AI Skills Hub for domain-specific skills.

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
