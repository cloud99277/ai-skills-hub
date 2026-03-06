---
name: with-scripts
description: Example skill that bundles a helper script for deterministic execution. Use when learning how to create skills with executable scripts, or as a template for script-driven workflows.
---

# With Scripts Example

This skill demonstrates how to bundle executable scripts alongside SKILL.md for tasks that need deterministic reliability.

## When to Use Scripts

Include scripts when:

- The same code would be rewritten repeatedly by the agent
- Deterministic, consistent execution is required
- The task benefits from parameterized command-line usage

## Available Scripts

### `scripts/example.py`

A simple helper that demonstrates the pattern. Run it directly:

```bash
python3 scripts/example.py --name "World"
```

Expected output: `Hello, World! This is an example skill script.`

## Workflow

1. Determine if the user's request matches this skill's scope
2. Run the helper script with appropriate arguments
3. Present the result to the user
