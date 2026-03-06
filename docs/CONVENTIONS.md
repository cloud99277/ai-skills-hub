# Conventions

This document defines the standards and conventions for creating, maintaining, and governing skills in the centralized skill repository.

## Directory Structure

Every standard skill follows this layout:

```
skill-name/
├── SKILL.md              (required — the only mandatory file)
├── agents/openai.yaml    (recommended — UI metadata)
├── scripts/              (optional — executable code)
├── references/           (optional — documentation for agent context)
└── assets/               (optional — templates, images, fonts used in output)
```

**Rules:**

- `SKILL.md` is the only required file
- Do NOT create `README.md`, `CHANGELOG.md`, or `QUICK_REFERENCE.md` inside a skill
- Detailed reference material goes into `references/`
- Deterministic, reusable logic goes into `scripts/`
- Output templates, images, and fonts go into `assets/`

## Naming

| Rule | Example |
|------|---------|
| All lowercase | `search-first` ✅, `Search-First` ❌ |
| Letters, digits, hyphens only | `api-design` ✅, `api_design` ❌ |
| Short, verb-led when possible | `upload-to-github` ✅ |
| Namespace by tool/platform when needed | `springboot-verification` ✅ |
| Max 64 characters | — |
| No leading/trailing hyphens or double hyphens | `my-skill` ✅, `-my-skill-` ❌ |

## Frontmatter

SKILL.md frontmatter should contain only `name` and `description`:

```yaml
---
name: skill-name
description: <What this skill does>. Use when <scenarios>. Prefer <scope>; use <other-skill> for <narrower-scope>.
---
```

### Description Requirements

A good `description` covers at least 4 of these 5 elements:

1. **What the skill does** — Core capability
2. **When to use it** — User scenarios and triggers
3. **How the user asks** — Natural language trigger phrases
4. **What it produces** — Expected output or result
5. **Boundaries** — What it does NOT do, and which related skill to prefer

### Description Templates

**English:**

```
<What this skill does>. Use when the user wants to <task 1>, <task 2>, or <task 3>.
Prefer this skill for <specific scope>, and prefer <other-skill> when the request is more specific.
```

**Chinese:**

```
<这个 skill 做什么>。当用户提到"<触发词1>""<触发词2>""<触发词3>"，
或需要 <任务场景1>、<任务场景2>、<任务场景3> 时使用。
若请求更偏 <更具体范围>，优先使用 `<other-skill>`。
```

**Mixed (for bilingual repositories):**

```
<What this skill does>. Use when the user asks to "<phrase 1>", "<phrase 2>", or needs <scenario>.
当用户提到"<中文触发词>"或需要 <中文场景> 时也应触发。
Prefer this skill for <scope>; use <other-skill> for <narrower scope>.
```

## Trigger Words

**Prefer:**

- Natural user expressions ("publish to WeChat", "run tests before PR")
- Task goals ("add a new API endpoint")
- Output names ("generate a slide deck")
- Platform names ("deploy to AWS")
- Common verbs ("create", "analyze", "convert")

**Avoid:**

- Internal jargon ("instinct-based learning")
- Implementation details ("subagent context problem")
- Architecture slogans ("A comprehensive verification system")
- Author-only abbreviations

## Routing Priority

When multiple skills could match a request, follow this priority order:

1. **Platform-specific** over generic (e.g., `springboot-verification` > `verification-loop`)
2. **Tech-stack-specific** over general engineering (e.g., `python-patterns` > `coding-standards`)
3. **Output-specific** over broad capability (e.g., `cover-image` > `image-gen`)
4. **Newer version** over legacy (e.g., `continuous-learning-v2` > `continuous-learning`)
5. **Generic skills** only as fallback

Write these priorities explicitly in each skill's `description` using `Prefer ... Not for ...` clauses.

## Lifecycle

Recommended workflow for creating or modifying a skill:

1. **Clarify** — understand how the user will ask for this capability
2. **Design** — plan the minimal directory structure needed
3. **Initialize** — use `init_skill.py` to create the skeleton
4. **Write description first** — frontmatter is the primary routing mechanism
5. **Write the body** — concise execution instructions
6. **Add resources** — `scripts/`, `references/`, `assets/` as needed
7. **Validate** — run `quick_validate.py` for the single skill
8. **Lint** — run `lint_skills.py` for repository-wide consistency
9. **Test** — trigger the skill in a real CLI workflow
10. **Iterate** — refine based on actual usage

## Governance Cadence

| Frequency | Action |
|-----------|--------|
| Every new skill | Review frontmatter before merging |
| Monthly | Run full repository lint |
| Quarterly | Clean up legacy, aliases, duplicates |
| On misfire | Adjust `description` boundaries immediately |
