---
name: codex-cli-trigger
description: Routes requests that explicitly ask to delegate a coding or terminal task to Codex CLI to the full-access `codexx` runner. Use when the user clearly wants Codex CLI. Not for generic requests to use an AI model or agent.
---

# Codex CLI Trigger

## 触发条件

当用户请求使用以下关键词执行任务时自动触发：
- Codex CLI、codexx、cx
- Codex（明确指 CLI/命令行执行时）

关键词组合：调用、使用、启动、运行、让 Codex CLI 帮忙、交给 Codex CLI 来做

仅提到 GPT、OpenAI 或泛指 AI 模型时不触发。

## 执行方式

使用完全授权模式 `codexx` 执行任务：

```bash
# 交互模式
codexx

# 执行具体任务
codexx <任务描述>
cx <任务描述>
```

## 使用示例

- "调用 Codex CLI 帮我写个 Python 脚本" → `codexx 帮我写个 Python 脚本`
- "用 Codex 修复这个 bug" → `codexx 修复这个 bug`
- "启动 codexx 来重构代码" → `codexx 重构这个代码`

## 注意事项

- 直接将用户的自然语言请求作为 codexx 的参数传递
- 不需要额外解释，直接执行 CLI 命令
