---
name: history-reader
description: Retrieve and summarize Claude local chat history when the user asks to 查看 Claude 之前的对话, 最近 N 条 Claude 记录, 回顾上次聊了什么, or continue a past Claude session. Prefer `history-chat` for Codex history.
---

# 历史对话查看

## 功能

读取 ~/.claude/history.jsonl 文件，显示最近的对话记录。

## 使用方式

1. 读取历史对话文件 `~/.claude/history.jsonl`
2. 解析每行的 display 字段
3. 按时间倒序显示最近 N 条对话

## 脚本位置

脚本位于: `~/.claude/skills/history-reader/scripts/history.sh`

## 调用方式

可以直接执行脚本，或通过已配置的 skill 触发：
- `/history` 或 `history` - 查看最近10条
- `/h` 或 `h` - 查看最近10条
- 支持传入数量: `/history 5` 查看最近5条
