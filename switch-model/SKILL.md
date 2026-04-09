---
name: switch-model
description: 交互式切换 OpenClaw 的 AI 模型，显示模型能力和费用信息
allowed-tools: Bash(openclaw:*) AskUserQuestion
---

# OpenClaw 模型切换

交互式切换 OpenClaw 使用的 Google Gemini 模型，提供模型能力对比和费用信息。

## 触发条件

- 用户说"切换模型"、"换个模型"、"更换模型"
- 用户说"switch model"、"change model"
- 用户询问"有哪些模型"、"可以用什么模型"

## 可用模型

### Gemini 3.1 Flash Lite Preview（当前默认）
- **ID**: `google/gemini-3.1-flash-lite-preview`
- **特点**: 最快速、最经济的选择
- **适用**: 日常对话、快速响应、高频使用
- **性能**: 前沿性能，成本极低

### Gemini 3.1 Flash Image Preview
- **ID**: `google/gemini-3.1-flash-image-preview`
- **特点**: 支持图像处理和生成
- **适用**: 需要处理图片的场景
- **性能**: 多模态能力，图像理解

### Gemini 3.1 Pro Preview
- **ID**: `google/gemini-3.1-pro-preview`
- **特点**: 最强大的推理能力
- **适用**: 复杂问题、深度分析、代码生成
- **性能**: 高级智能，复杂任务处理

### Gemini 3 Flash Preview
- **ID**: `google/gemini-3-flash-preview`
- **特点**: 前沿性能，媲美大模型
- **适用**: 平衡性能和成本
- **性能**: 高性价比

### Gemini 3 Pro Image Preview
- **ID**: `google/gemini-3-pro-image-preview`
- **特点**: Pro 级图像处理能力
- **适用**: 专业图像分析和生成
- **性能**: 最强图像能力

## 实现步骤

### 1. 显示当前模型

```bash
CURRENT_MODEL=$(openclaw config get agents.defaults.model.primary)
echo "当前模型: $CURRENT_MODEL"
```

### 2. 使用 AskUserQuestion 展示选项

使用 AskUserQuestion 工具创建交互式选择界面，包含：
- 模型名称
- 能力描述
- 适用场景

### 3. 切换模型

```bash
# 用户选择后，设置新模型
openclaw config set agents.defaults.model.primary "<选择的模型ID>"
```

### 4. 重启 Gateway

```bash
# 在 tmux session 中重启 gateway
tmux send-keys -t openclaw_gateway C-c
sleep 3
tmux send-keys -t openclaw_gateway "openclaw gateway" Enter
```

### 5. 确认切换成功

```bash
# 等待几秒后确认
sleep 5
NEW_MODEL=$(openclaw config get agents.defaults.model.primary)
echo "✅ 模型已切换为: $NEW_MODEL"
echo "Gateway 正在重启，请稍等片刻后测试新模型"
```

## 完整实现示例

当用户请求切换模型时：

1. **查询当前模型**
2. **使用 AskUserQuestion 显示选项**：
   - 每个选项包含模型名称、特点、适用场景
   - 用户选择想要的模型
3. **执行切换**：
   - 使用 `openclaw config set` 更新配置
   - 在 tmux 中重启 gateway
4. **确认完成**：
   - 显示切换成功消息
   - 提示用户测试新模型

## 注意事项

- 切换模型需要重启 gateway，会短暂中断服务（约5-10秒）
- 确保 gateway 运行在 tmux session `openclaw_gateway` 中
- 切换后建议发送测试消息验证新模型是否正常工作
- 不同模型的响应速度和质量可能有差异

## 费用说明

- **Flash Lite**: 最低成本，适合高频使用
- **Flash**: 中等成本，性价比高
- **Pro**: 较高成本，但能力最强
- 具体定价请参考 Google AI 官方文档

## 故障排除

如果切换失败：
1. 检查 tmux session 是否存在：`tmux ls`
2. 手动重启 gateway：`openclaw gateway`
3. 验证配置：`openclaw config get agents.defaults.model.primary`
