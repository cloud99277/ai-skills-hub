# Architecture

This document explains the design and architecture of the centralized AI skills system.

## Overview

The centralized skill system solves a common problem: **multiple AI agents (Claude, Codex, Gemini, etc.) each maintain their own isolated skill directories**, leading to duplication, inconsistency, and maintenance overhead.

The solution is a **single shared repository** that all agents access through symlinks:

```
~/.claude/skills  ──┐
~/.codex/skills   ──┤
~/.gemini/skills  ──┼──→  ~/.ai-skills  (centralized repository)
~/.agents/skills  ──┘
```

**Update once, all agents benefit.**

## Core Design Principles

### 1. One Repository, Many Entry Points

The repository lives at `~/.ai-skills/`. Each AI tool's skill directory is a symlink pointing to it. When you add or modify a skill in the central repository, every linked agent sees the change immediately.

### 2. Progressive Disclosure

Skills use a three-level loading system to manage context window efficiently:

```
┌─────────────────────────────────────────────────────────┐
│ Level 1: Metadata (always loaded)                       │
│   name + description (~100 words)                       │
│   → Used for routing: "should I use this skill?"        │
├─────────────────────────────────────────────────────────┤
│ Level 2: SKILL.md body (loaded on trigger)              │
│   Instructions and workflow (<5k words)                 │
│   → Loaded only when the skill is activated             │
├─────────────────────────────────────────────────────────┤
│ Level 3: Bundled resources (loaded on demand)           │
│   scripts/, references/, assets/ (unlimited)            │
│   → Loaded only when specific resources are needed      │
│   → Scripts can execute without reading into context    │
└─────────────────────────────────────────────────────────┘
```

This design ensures that the agent's context window is not wasted on skills that aren't being used.

### 3. Description-Driven Routing

The `description` field in SKILL.md frontmatter is the **primary routing mechanism**. It determines when a skill gets activated. This is why the description must:

- State what the skill does (capability)
- State when to use it (trigger scenarios)
- State boundaries (what it does NOT do)

The body of SKILL.md is only loaded AFTER triggering, so "when to use" information must live in the frontmatter description, not in the body.

### 4. Skill as Directory

Each skill is a self-contained directory. This makes skills:

- **Portable** — copy a directory to share a skill
- **Versionable** — track changes with git
- **Composable** — add or remove skills without affecting others
- **Inspectable** — browse the filesystem to see all available skills

## Repository Structure

```
~/.ai-skills/
├── .system/                    ← System-level infrastructure (do not modify casually)
│   └── skill-creator/          ← Skill creation toolchain
│       ├── SKILL.md            ← Design principles and creation guide
│       ├── scripts/            ← Core scripts
│       │   ├── init_skill.py           ← Skill skeleton generator
│       │   ├── quick_validate.py       ← Single-skill structural validator
│       │   ├── lint_skills.py          ← Repository-wide linter
│       │   └── generate_openai_yaml.py ← UI metadata generator
│       ├── references/         ← openai.yaml field reference
│       └── agents/             ← UI metadata for skill-creator itself
├── skill-lint/                 ← Built-in repository lint skill
│   ├── SKILL.md
│   ├── scripts/run_lint.py     ← Wrapper that delegates to lint_skills.py
│   └── agents/openai.yaml
├── _examples/                  ← Example skills for learning
│   ├── hello-world/
│   └── with-scripts/
├── your-skill-1/               ← Your custom skills go here
├── your-skill-2/
└── ...
```

## Validation Toolchain

The system provides a three-tier validation pipeline:

```
                    ┌──────────────────────┐
 Create a skill ──→ │  quick_validate.py   │  Single skill, structural checks
                    │  (fast, focused)      │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
 Batch refactor ──→ │  lint_skills.py      │  Repository-wide, structural + semantic
                    │  (thorough)           │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
 Agent-driven   ──→ │  skill-lint (skill)  │  Same checks, exposed as a shared skill
                    │  (reusable)           │
                    └──────────────────────┘
```

### quick_validate.py

- **Scope**: Single skill directory
- **Checks**: YAML frontmatter format, required fields (`name`, `description`), naming rules, description length
- **Use when**: Creating or editing a single skill

### lint_skills.py

- **Scope**: Entire repository or subtree
- **Checks**: Everything in quick_validate + description routing quality (`Use when`, old phrases, capability-first pattern) + body consistency (legacy commands, outdated trigger wording)
- **Modes**: `--strict` (name + description only) or compatibility (allows metadata, license, etc.)
- **Output**: `text` or `json`
- **Use when**: After batch edits, before commits, or during governance reviews

### skill-lint (shared skill)

- **Scope**: Same as lint_skills.py
- **Purpose**: Exposes the linter as a reusable skill that agents can invoke
- **Use when**: You want an agent to perform repository-wide linting as part of a workflow

## Integration with AI Tools

### Claude Code (claude)

- Skills directory: `~/.claude/skills/`
- Skills are loaded based on frontmatter metadata matching

### Codex CLI (codex)

- Skills directory: `~/.codex/skills/`
- Supports `agents/openai.yaml` for UI metadata
- Supports `$skill-name` explicit invocation

### Gemini CLI (gemini)

- Skills directory: `~/.gemini/skills/`
- Skills with SKILL.md and YAML frontmatter are auto-discovered

### Generic Agents

- Skills directory: `~/.agents/skills/`
- Any agent that follows the SKILL.md convention can read skills from here

## Adding a New Agent Entry Point

If a new AI tool stores skills in `~/.newtool/skills/`, simply add a symlink:

```bash
ln -s ~/.ai-skills ~/.newtool/skills
```

The new tool will immediately have access to all shared skills.
