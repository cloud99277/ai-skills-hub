---
name: ppt-template-skill
description: Generate or refine an editable `.pptx` skeleton from a visual presentation style, especially when reverse-engineering a deck from screenshots, video analysis, or a known design language such as dark neon tech slides. Use when the user wants a reusable PPT master, slide taxonomy, spacing/color rules, or a source-inspired PowerPoint skeleton rather than a one-off image.
metadata:
  short-description: Generate editable PPT skeletons from a design spec
---

# PPT Template Skill

## Overview

Use this skill when the user wants a real, editable PowerPoint skeleton that follows a specific visual system. It is optimized for source-inspired decks reconstructed from screenshots or video analysis, and ships with a reusable dark-tech template generator.

## When To Use

- The user wants to imitate a PPT style seen in a video, screenshot set, or recorded demo.
- The deliverable must be an editable `.pptx`, not HTML slides or rendered images.
- The task needs explicit design rules: colors, spacing, typography, card styles, and page taxonomy.
- The user wants a reusable master deck that can be regenerated with small parameter changes.

## Workflow

1. Start from a source signal.
   Accept one of:
   - a video analysis report
   - a screenshot set
   - a written design brief

2. Read the design rules.
   Load [references/dark-tech-design-system.md](references/dark-tech-design-system.md) for the default visual system and page taxonomy.

3. Generate the `.pptx`.
   Use the bundled script:

```bash
python3 ~/.ai-skills/ppt-template-skill/scripts/generate_dark_tech_pptx.py \
  --output /absolute/path/output.pptx
```

4. If `python-pptx` is missing, use a local venv instead of touching the system Python:

```bash
python3 -m venv /tmp/pptx-venv
/tmp/pptx-venv/bin/pip install python-pptx
/tmp/pptx-venv/bin/python ~/.ai-skills/ppt-template-skill/scripts/generate_dark_tech_pptx.py \
  --output /absolute/path/output.pptx
```

5. Forward-check the result.
   Re-open the generated file with `python-pptx` and confirm slide count plus the first visible text items.

## Script

Primary generator:

```bash
python3 ~/.ai-skills/ppt-template-skill/scripts/generate_dark_tech_pptx.py --help
```

Supported options:

- `--output`: required output `.pptx` path
- `--deck-title`: cover title, default `Hunter Alpha`
- `--deck-subtitle`: cover subtitle, default `Mimo-V2-Omni source-inspired dark tech presentation skeleton`
- `--brand-label`: small label above the cover title, default `MIMO-V2-OMNI`
- `--repo-url`: CTA slide repository or link text

## Notes

- This skill generates editable shapes and text boxes, not flattened screenshots.
- It aims for high structural fidelity, not pixel-perfect cloning.
- If the user needs a new style family, add a new reference file and extend the script rather than overloading this one with many unrelated themes.
