# AI Skills Hub

**一个仓库，所有 AI agent，共享技能。**

AI Skills Hub 是一套中心化的 skill 体系，让多个 AI agent（Claude、Codex、Gemini 等）通过同一个仓库共享技能。创建一次，所有关联的 agent 立即可用。

## 为什么需要这个？

如果你同时使用多个 AI 编程助手，你一定遇到过这个问题：每个工具都有自己独立的技能/知识系统。你不得不重复创建技能、分别维护、处理不一致。

AI Skills Hub 用一个简单的架构解决了这个问题：

```
~/.claude/skills  ──┐
~/.codex/skills   ──┤
~/.gemini/skills  ──┼──→  ~/.ai-skills  (本仓库)
~/.agents/skills  ──┘
```

所有 agent 入口都通过软链接指向同一个中心仓库。**更新一次，所有 agent 受益。**

## 快速上手

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
- 为 Claude、Codex、Gemini 和通用 agent 创建软链接
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

## 什么是 Skill？

Skill 是一个独立的目录，包含一个 `SKILL.md` 文件，为 AI agent 提供特定领域的专业知识、工作流或工具。

```
my-skill/
├── SKILL.md           ← 必需：frontmatter + 指令
├── agents/            ← 推荐：UI 元数据
│   └── openai.yaml
├── scripts/           ← 可选：可执行的辅助脚本
├── references/        ← 可选：详细文档，按需加载到上下文
└── assets/            ← 可选：模板、图片、字体
```

### 最重要的部分：`description`

YAML frontmatter 中的 `description` 是**主要的路由机制**——它告诉 agent 何时使用这个 skill：

```yaml
---
name: my-skill
description: 将 PDF 文档转换为干净的 Markdown 文本。Use when the user wants to
  extract text from PDFs, convert PDF to Markdown, or process PDF documents.
  当用户提到"PDF 转文字""提取 PDF 内容"时使用。Not for scanned documents.
---
```

好的 description 回答三个问题：**做什么？何时触发？什么不处理？**

## 仓库结构

```
ai-skills-hub/
├── .system/                    ← 核心基础设施（skill 创建工具链）
│   └── skill-creator/
│       ├── SKILL.md            ← 设计原则和创建指南
│       └── scripts/            ← 初始化、校验、巡检、生成工具
├── skill-lint/                 ← 内置的仓库巡检 skill
├── _examples/                  ← 示例 skill，供学习参考
│   ├── hello-world/            ← 最简 skill（仅 SKILL.md）
│   └── with-scripts/           ← 带脚本的 skill
├── docs/
│   ├── ARCHITECTURE.md         ← 系统设计和核心概念
│   └── CONVENTIONS.md          ← 命名、frontmatter、路由规范
├── setup.sh                    ← 一键安装
├── uninstall.sh                ← 干净卸载
└── 你的 skill 放这里/           ← 添加你自己的 skill！
```

## 工具链

| 工具 | 范围 | 用途 |
|------|------|------|
| `init_skill.py` | 新建 skill | 生成 skill 目录骨架 |
| `quick_validate.py` | 单个 skill | 结构性校验（frontmatter、命名） |
| `lint_skills.py` | 整个仓库 | 路由质量 + 一致性检查 |
| `generate_openai_yaml.py` | 单个 skill | 生成 UI 元数据 |
| `skill-lint`（skill） | 整个仓库 | 和 lint_skills.py 相同，作为可复用的 skill |

## 标准工作流

```
创建 → 编辑 SKILL.md → quick_validate.py → lint_skills.py → 真实触发测试
```

## 核心设计

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

## 文档

- [Architecture](docs/ARCHITECTURE.md) — 系统设计、渐进加载、验证管线
- [Conventions](docs/CONVENTIONS.md) — 命名、frontmatter、路由、生命周期、治理

## 卸载

```bash
chmod +x uninstall.sh
./uninstall.sh
```

只会移除软链接，不会删除你创建的 skill 和仓库本身。

## 许可证

[MIT](LICENSE)
