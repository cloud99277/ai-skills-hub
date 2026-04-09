[简体中文](README_CN.md) | [English](README.md)

<div align="center">

# 🧠 AI Skills Hub

**为所有 AI Agent 精选的共享技能集，按需挑选。**

[![Author](https://img.shields.io/badge/Author-Cloud927-blue?style=flat-square)](https://github.com/cloud99277)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Skills](https://img.shields.io/badge/技能-62-brightgreen?style=flat-square)](#-内置技能)

</div>

本仓库包含 **62 个精选 skill**，均已通过 KitClaw skill-admission 质量关口。所有 skill 适配 Claude Code、Codex CLI、Gemini CLI 以及任何使用 `SKILL.md` 契约的 Agent。

这是 [KitClaw](https://github.com/cloud99277/KitClaw) 的配套仓库。KitClaw 提供 16 个平台核心 skill（记忆、治理、编排），本仓库提供更丰富的领域 skill。

## ✨ 特点

- 🔗 **一处维护，全局共享** — 所有 AI Agent（Claude、Codex、Gemini）通过软链接共享同一套技能
- ✅ **质量保证** — 每个 skill 都通过收编检查（lint、安全、自包含、Agent 无关）
- 📦 **按需安装** — 可整体克隆，也可只复制需要的单个 skill
- 🔌 **即插即用** — 新的 AI 工具？一条 `ln -s` 命令就能接入

## 🚀 快速开始

### 1. 克隆 & 安装

```bash
git clone https://github.com/cloud99277/ai-skills-hub.git
cd ai-skills-hub
chmod +x setup.sh
./setup.sh
```

安装脚本会：
- 将仓库链接到 `~/.ai-skills`
- 为 Claude、Codex、Gemini 创建软链接

### 2. 或者：按需安装

如果只需要某些 skill，单独复制：

```bash
# 示例：只安装 code-review 和 python-patterns
cp -r ai-skills-hub/code-review ~/.ai-skills/
cp -r ai-skills-hub/python-patterns ~/.ai-skills/
```

## 📖 什么是 Skill？

Skill 是一个独立目录，包含 `SKILL.md` 文件，为 AI Agent 提供特定领域的专业知识、工作流或工具。

```
my-skill/
├── SKILL.md           ← 必需：frontmatter + 指令
├── scripts/           ← 可选：可执行的辅助脚本
├── references/        ← 可选：详细文档，按需加载
└── assets/            ← 可选：模板、图片、字体
```

## 📦 内置技能（62 个）

### 编码与开发

| Skill | 说明 |
|---|---|
| code-review | 代码变更审查，关注质量、可读性、架构 |
| python-patterns | Python 惯用写法、PEP 8、类型标注、可维护代码 |
| golang-patterns | Go 惯用模式、最佳实践、约定 |
| coding-standards | TypeScript / Python / Go 通用编码规范 |
| tdd-workflow | 测试驱动开发工作流 |
| e2e-testing | Playwright E2E 测试模式，Page Object Model |
| security-scan | 配置安全漏洞扫描 |
| security-review | 应用变更安全风险审查 |
| database-migrations | 数据库迁移最佳实践 |
| postgres-patterns | PostgreSQL schema 设计、查询优化 |
| api-design | REST API 生产级设计模式 |
| golang-testing | Go 测试模式：表驱动、子测试、基准测试 |
| python-testing | Python pytest、fixture、mock 测试模式 |

### 前端与设计

| Skill | 说明 |
|---|---|
| frontend-patterns | React 和 Next.js 前端开发模式 |
| frontend-slides | 设计级浏览器原生 HTML/CSS/JS 演示文稿 |
| popular-web-designs | 54 套真实生产级设计系统 |

### 研究与分析

| Skill | 说明 |
|---|---|
| deep-research | 系统性技术研究——对比开源工具 |
| market-research | 市场研究、竞品分析、投资者数据 |
| eval-harness | 构建可复现的评测和回归基准 |
| project-audit | 项目文档架构审查 |
| product-manager-review | 严格的 PM 项目计划审查 |
| project-retrospective | 提取执行经验，提炼新模式 |

### 写作与发布

| Skill | 说明 |
|---|---|
| article-writing | 撰写或优化长文 |
| baoyu-html-deck | 轻量单文件 HTML 演示文稿生成器 |
| baoyu-slide-deck | 图片优先的幻灯片工作空间 |
| baoyu-infographic | 出版级信息图 |
| baoyu-cover-image | 文章封面/头图 |
| baoyu-article-illustrator | 文章章节配图 |
| baoyu-comic | 多页教育漫画 |
| baoyu-xhs-images | 小红书/RedNote 多图卡片系列 |
| baoyu-format-markdown | Markdown 清理与结构化 |
| baoyu-markdown-to-html | Markdown → HTML（微信公众号等） |
| baoyu-compress-image | 图片/目录压缩 |
| china-content-compliance | 中国大陆内容合规过滤与改写 |

### 翻译与语言

| Skill | 说明 |
|---|---|
| translate | 通用翻译工具（所有 Agent） |
| 927-translate-skill | 通用翻译——网页/推文抓取、三种模式、欧化检测 |

### 自动化与 DevOps

| Skill | 说明 |
|---|---|
| coding-agent | 将编码任务委派给 Codex、Claude Code、Pi |
| claude-code | 将编码任务委派给 Claude Code CLI |
| codex | 将编码任务委派给 OpenAI Codex CLI |
| full-cycle-builder | 质量门驱动的开发生命周期 |
| deployment-patterns | 部署工作流、CI/CD、容器化 |
| docker-patterns | Docker 和 Compose 本地开发模式 |
| continuous-learning-v2 | 从重复模式学习可复用行为 |
| cost-aware-llm-pipeline | LLM API 使用成本优化模式 |

### 内容与社交媒体

| Skill | 说明 |
|---|---|
| content-engine | 平台原生内容审查与优化 |
| content-for-x | 准备 X (Twitter) 发布内容包 |
| baoyu-url-to-markdown | 通过 Chrome CDP 抓取 URL 转 Markdown |
| baoyu-danger-x-to-markdown | X 推文和文章转 Markdown |
| baoyu-danger-gemini-web | Gemini Web 文本/图片生成 |
| xhs-tunnel | Cloudflare Tunnel 移动端预览测试 |

### 项目管理

| Skill | 说明 |
|---|---|
| project-planner | 从外部灵感规划和构建新项目 |
| project-guidelines-example | 项目级 skill/约定/团队规范模板 |
| design-iteration | 基于审计结果驱动文档迭代 |
| product-manager-review | 严格的 PM 项目计划审查 |

### 工具与实用

| Skill | 说明 |
|---|---|
| find-skills | 跨仓库搜索 skill |
| regex-vs-llm-structured-text | 决策框架：正则 vs LLM 处理结构化文本 |
| strategic-compact | 在任务边界建议手动上下文压缩 |
| ppt-template-skill | 生成或优化可编辑 .pptx 骨架 |
| brain-link | 安装 brain-inject shell 集成 |
| history-reader | 检索和总结 Claude 本地对话历史 |
| history-chat | 检索和总结 Codex 本地对话历史 |
| iterative-retrieval | 大型代码库渐进式上下文检索 |
| search-first | 调研现有工具、库、MCP 服务器、skill |

### Agent 集成

| Skill | 说明 |
|---|---|
| add-provider | 从 base URL 添加或更新 Codex provider |
| codex-cli-trigger | 将编码请求路由到 Codex |
| codex-provider-bootstrap | 完整引导 Codex 本地 provider |
| gemini-cli-trigger | 将任务路由到 Gemini |
| agent-reach | 让你的 Agent 看到整个互联网 |
| switch-model | 交互式切换 OpenClaw AI 模型 |
| tacit-mining | 从用户交互中挖掘隐性知识 |
| personal-dossier-builder | 从现有数据构建动态个人档案 |

## 🏗️ 仓库结构

```
ai-skills-hub/
├── .system/                    ← 核心基础设施（skill 创建工具链）
│   └── skill-creator/
│       ├── SKILL.md            ← 设计原则和创建指南
│       └── scripts/            ← 初始化、校验、巡检、生成工具
├── (62 个 skill 目录)           ← 全部通过 skill-admission 质量关口
├── _examples/                  ← 示例 skill，供学习参考
│   ├── hello-world/            ← 最简 skill（仅 SKILL.md）
│   └── with-scripts/           ← 带脚本的 skill
├── docs/
│   ├── ARCHITECTURE.md         ← 系统设计和核心概念
│   └── CONVENTIONS.md          ← 命名、frontmatter、路由规范
├── setup.sh                    ← 一键安装
└── uninstall.sh                ← 干净卸载
```

## Skill 质量

本仓库每个 skill 都通过 KitClaw 的 **skill-admission** 质量关口：

| 检查项 | 验证内容 |
|---|---|
| Lint | frontmatter 包含 `name` + `description`，命名规范，路由质量 |
| 安全 | 无硬编码密钥、无危险命令、无 API key 模式 |
| 无个人依赖 | 无硬编码用户路径（`/home/xxx`、`/Users/xxx`） |
| Agent 无关 | 适配 Claude、Codex、Gemini——无 Agent 专属语法 |
| 自包含 | 所有引用文件（scripts、references）在 skill 内部存在 |
| 结构干净 | 无 README.md、banner 图片等非标准文件 |

## 🔌 添加新的 AI 工具

如果新的 AI 工具将 skill 存储在 `~/.newtool/skills/`，只需：

```bash
ln -s ~/.ai-skills ~/.newtool/skills
```

完成。新工具立即拥有所有共享技能。

## 与 KitClaw 的关系

| | KitClaw | AI Skills Hub |
|---|---|---|
| **定位** | 平台运行时 | Skill 集合 |
| **包含** | 16 个核心 skill + 记忆 + 治理 | 62 个领域 skill |
| **必须安装？** | 是——提供运行时基础设施 | 否——按需挑选 |
| **skill 范围** | 记忆、lint、可观测、收编 | 编码、研究、发布、自动化 |

先安装 KitClaw 获得运行时，再从 AI Skills Hub 按需挑选领域 skill。

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
