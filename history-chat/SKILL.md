---
name: history-chat
description: Retrieve and summarize Codex local chat history when the user asks to 查看 Codex 之前的对话, 最近 N 条 Codex 记录, 按时间定位某次 Codex 会话, or continue a past Codex session. Prefer `history-reader` for Claude history.
---

Use this skill to retrieve records from `~/.codex/history.jsonl`.

## Quick commands

- Recent 20 records:
```bash
python3 scripts/query_history.py recent --limit 20
```

- Locate by exact timestamp and show context:
```bash
python3 scripts/query_history.py around --timestamp "2026-03-03 15:12:09Z" --before 4 --after 6
```

## Rules

1. Always mask API keys in output (`sk-***`).
2. Default to concise one-line preview per record.
3. If user asks to continue a previous conversation, run `around` first, summarize the target context in 3-6 lines, then continue the task.
4. Use UTC timestamp format `YYYY-MM-DD HH:MM:SSZ` for stable matching.

## Output format

- `[index] [timestamp] [session_id] text`
- Truncate long text to keep readability.
