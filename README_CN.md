[简体中文](README_CN.md) | [English](README.md)

<div align="center">

# 🧠 AI Skills Hub

**一个仓库，所有 AI Agent，共享技能**

[![Author](https://img.shields.io/badge/Author-Cloud927-blue?style=flat-square)](https://github.com/cloud99277)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-2+-brightgreen?style=flat-square)](#-内置技能)

</div>

## ✨ 特点

- 🔗 **一处维护，全局共享** — 所有 AI Agent（Claude、Codex、Gemini）通过软链接共享同一套技能
- 🛠️ **完整工具链** — 创建、校验、巡检、生成一条龙，skill 质量有保障
- 📐 **渐进加载** — 元数据 → 正文 → 资源三级加载，节省上下文窗口
- 🔌 **即插即用** — 新的 AI 工具？一条 `ln -s` 命令就能接入
- 📦 **自带示例** — 从 hello-world 到带脚本的完整 skill，开箱即学

## 🤔 为什么需要？

如果你同时使用多个 AI 编程助手，一定遇到过这个问题：每个工具都有独立的技能系统，技能重复创建、分别维护、互不相通。

AI Skills Hub 用一个简单的架构解决了这个问题：

```
~/.claude/skills  ──┐
~/.codex/skills   ──┤
~/.gemini/skills  ──┼──→  ~/.ai-skills  (本仓库)
~/.agents/skills  ──┘
```

所有 Agent 入口都通过软链接指向同一个中心仓库。**更新一次，所有 Agent 受益。**

## 🚀 快速开始

### 1. 克隆

```bash
git clone https://github.com/cloud99277/ai-skills-hub.git
cd ai-skills-hub
```

### 2. 安装

```bash
chmod +x setup.sh
./setup.sh
```

安装脚本会：
- 将仓库链接到 `~/.ai-skills`
- 为 Claude、Codex、Gemini 和通用 Agent 创建软链接
- 检查 Python 3 和 PyYAML 是否已安装
- 运行自检确认一切正常

### 3. 创建你的第一个 Skill

```bash
python3 ~/.ai-skills/.system/skill-creator/scripts/init_skill.py my-first-skill \
    --path ~/.ai-skills \
    --resources scripts
```

### 4. 验证

```bash
# 单个 skill 校验
python3 ~/.ai-skills/.system/skill-creator/scripts/quick_validate.py ~/.ai-skills/my-first-skill

# 仓库级巡检
python3 ~/.ai-skills/.system/skill-creator/scripts/lint_skills.py ~/.ai-skills
```

## 📖 什么是 Skill？

Skill 是一个独立的目录，包含一个 `SKILL.md` 文件，为 AI Agent 提供特定领域的专业知识、工作流或工具。

```
my-skill/
├── SKILL.md           ← 必需：frontmatter + 指令
├── agents/            ← 推荐：UI 元数据
│   └── openai.yaml
├── scripts/           ← 可选：可执行的辅助脚本
├── references/        ← 可选：详细文档，按需加载
└── assets/            ← 可选：模板、图片、字体
```

### 最重要的部分：`description`

YAML frontmatter 中的 `description` 是**主要的路由机制**——它告诉 Agent 何时使用这个 skill：

```yaml
---
name: my-skill
description: 将 PDF 文档转换为干净的 Markdown 文本。当用户提到
  "PDF 转文字""提取 PDF 内容"时使用。不适用于扫描件。
---
```

好的 description 回答三个问题：**做什么？何时触发？什么不处理？**

## 📦 内置技能

| 技能 | 说明 |
|------|------|
| [927-translate-skill](927-translate-skill/) | 🌐 跨 Agent 通用翻译技能，支持网页/推文抓取、三种翻译模式、欧化检测 |
| [skill-lint](skill-lint/) | 🔍 仓库级 skill 质量巡检 |

## 🏗️ 仓库结构

```
ai-skills-hub/
├── .system/                    ← 核心基础设施（skill 创建工具链）
│   └── skill-creator/
│       ├── SKILL.md            ← 设计原则和创建指南
│       └── scripts/            ← 初始化、校验、巡检、生成工具
├── 927-translate-skill/        ← 通用翻译技能（支持所有 Agent）
├── skill-lint/                 ← 内置的仓库巡检 skill
├── _examples/                  ← 示例 skill，供学习参考
│   ├── hello-world/            ← 最简 skill（仅 SKILL.md）
│   └── with-scripts/           ← 带脚本的 skill
├── docs/
│   ├── ARCHITECTURE.md         ← 系统设计和核心概念
│   └── CONVENTIONS.md          ← 命名、frontmatter、路由规范
├── setup.sh                    ← 一键安装
└── uninstall.sh                ← 干净卸载
```

## 🛠️ 工具链

| 工具 | 范围 | 用途 |
|------|------|------|
| `init_skill.py` | 新建 skill | 生成 skill 目录骨架 |
| `quick_validate.py` | 单个 skill | 结构性校验（frontmatter、命名） |
| `lint_skills.py` | 整个仓库 | 路由质量 + 一致性检查 |
| `generate_openai_yaml.py` | 单个 skill | 生成 UI 元数据 |
| `skill-lint`（skill） | 整个仓库 | 和 lint_skills.py 相同，作为可复用的 skill |

## 🔌 添加新的 AI 工具

如果新的 AI 工具将 skill 存储在 `~/.newtool/skills/`，只需：

```bash
ln -s ~/.ai-skills ~/.newtool/skills
```

完成。新工具立即拥有所有共享技能。

## 🏗️ 核心设计

### 渐进加载

Skill 分三级加载，节省上下文窗口：

1. **元数据**（始终加载）— `name` + `description`（~100 词）
2. **正文**（触发时加载）— SKILL.md 指令（<5k 词）
3. **资源**（按需加载）— scripts、references、assets（无限制）

### 路由优先级

当多个 skill 可能匹配时：

1. 平台专项 > 通用能力
2. 技术栈专项 > 通用工程能力
3. 输出物明确 > 泛能力
4. 新版 > 旧版
5. 通用 skill 只做兜底

## 📚 文档

- [Architecture](docs/ARCHITECTURE.md) — 系统设计、渐进加载、验证管线
- [Conventions](docs/CONVENTIONS.md) — 命名、frontmatter、路由、生命周期

## 🗑️ 卸载

```bash
chmod +x uninstall.sh
./uninstall.sh
```

只会移除软链接，不会删除你创建的 skill 和仓库本身。

## 📄 许可证

[MIT](LICENSE)

---

<div align="center">

**Made with ❤️ by [Cloud927](https://github.com/cloud99277)**

</div>
