---
name: brain-link
description: Install brain-inject shell integration to automatically link projects to Claude Code Brain. Use when user wants to connect current project to brain, enable auto-linking for new projects, or set up brain integration.
---

# Brain Link

Installs the brain-inject shell integration that automatically links projects to Claude Code Brain.

## Usage

Run the install script:
```bash
~/.claude/brain/bin/install.sh
```

This will:
1. Detect your shell type (bash/zsh)
2. Add brain-inject integration to your shell config
3. Enable automatic linking when entering project directories

## After Installation

Restart your terminal or run:
- `source ~/.zshrc` (Zsh)
- `source ~/.bashrc` (Bash)

Then when you enter any project directory, it will automatically link to the brain.
