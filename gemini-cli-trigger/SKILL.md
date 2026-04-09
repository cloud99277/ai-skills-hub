---
name: gemini-cli-trigger
description: Routes requests that explicitly ask to delegate a task to Gemini CLI to the full-access `geminix` runner. Use when the user clearly wants Gemini CLI. Not for generic requests to use an AI model, assistant, or provider.
---

# Gemini CLI Trigger

## 触发条件

当用户请求使用以下关键词执行任务时自动触发：
- Gemini CLI、geminix、gx
- Gemini（明确指 CLI/命令行执行时）

关键词组合：调用、使用、启动、运行、让 Gemini CLI 帮忙、交给 Gemini CLI 来做

仅提到 Google、Google AI 或泛指 AI 模型时不触发。

## 执行方式

使用完全授权模式 `geminix` 执行任务：

```bash
# 交互模式
geminix

# 执行具体任务
geminix <任务描述>
gx <任务描述>
```

## 使用示例

- "调用 Gemini 帮我写个文案" → `geminix 帮我写个文案`
- "用 Gemini 分析这个图片" → `geminix 分析这个图片`
- "启动 geminix 来总结这个文章" → `geminix 总结这个文章`

## 注意事项

- 直接将用户的自然语言请求作为 geminix 的参数传递
- 不需要额外解释，直接执行 CLI 命令
