---
name: baoyu-html-deck
description: Lightweight single-file HTML presentation generator for Markdown, outlines, articles, or talk notes, with theme switching and basic navigation. Use when the user wants a quick browser-native deck without complex motion. Prefer `frontend-slides` for design-heavy presentations and `baoyu-slide-deck` for image-rendered slides.
---

# baoyu-html-deck

生成 HTML 演示文稿的技能，输出单文件 HTML，支持主题切换、键盘导航、全屏演示。

## 何时使用

- 需要快速生成单文件网页 PPT 或 HTML 幻灯片
- 内容已经基本成型，重点是快速排版与分享，不追求复杂动画
- 适合轻量浏览器演示、录屏讲解、内部分发

## 何时不要使用

- 需要强设计感、复杂动画或重度视觉探索：优先 `frontend-slides`
- 需要图片式幻灯片、逐页渲染或导出 PPTX/PDF：优先 `baoyu-slide-deck`

## 使用命令

- `/baoyu-html-deck <content>` - 直接输入内容
- `/baoyu-html-deck <file.md>` - 从文件读取内容
- `/baoyu-html-deck <file.md> --theme dark` - 指定主题
- `/baoyu-html-deck --theme blueprint` - 指定默认主题

## 输入格式

```markdown
---
title: 项目名称
subtitle: 副标题（可选）
theme: blueprint
---

# 封面标题
副标题内容

# 第一页标题
内容段落...

## 第二页标题（卡片布局）
- 卡片1标题
  卡片1内容
- 卡片2标题
  卡片2内容

## 第三页标题（列表布局）
- 列表项1
- 列表项2
```

## 布局类型

| 布局 | 说明 | 语法 |
|------|------|------|
| 封面 | 特殊封面样式 | 第一页自动识别 |
| 默认 | 标题 + 内容 | `# 标题` + 内容 |
| 卡片 | 网格卡片 | `## 标题` + 无序列表 |
| 列表 | 居中列表 | `## 标题` + 无序列表 |
| 步骤 | 步骤流程 | 数字列表 |

## 主题

- `blueprint` - 科技蓝主题（默认）
- `dark` - 暗黑主题
- `light` - 浅色主题

## 功能特性

- 自动布局识别
- 主题切换
- 全屏演示（隐藏按钮）
- 键盘导航（←/→/空格翻页，Esc 退出）
- 响应式设计
- 大字体优化（移动端/录屏）
