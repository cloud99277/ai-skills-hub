---
name: translate
description: 通用翻译工具，支持所有 AI Agent（Claude Code、Codex CLI、Gemini CLI），可翻译文件、URL、X 推文。支持 quick/normal/refined 三种模式，含欧化语言检测、比喻映射、出版级审校。
io:
  input:
    - type: markdown_file
      description: 需要翻译的 Markdown 文件
    - type: url
      description: 需要获取并翻译的 URL（网页或 X 推文）
      required: false
  output:
    - type: markdown_file
      description: 翻译后的 Markdown 文件
      path_pattern: "{source-name}-{target-lang}/translation.md"
---

# translate

通用翻译 Skill，支持所有 AI 编程助手。

## 快速开始

### Agent 直接翻译（推荐）
AI Agent 读取本 SKILL.md 后，按照下方翻译原则直接翻译，无需运行脚本。

### 脚本辅助翻译
脚本负责**内容获取**和**智能分块**，翻译由 Agent 完成：
```bash
# 翻译本地文件
python3 ~/.ai-skills/translate/scripts/translate.py article.md --to zh-CN

# 自动获取并翻译 X 推文
python3 ~/.ai-skills/translate/scripts/translate.py --fetch https://x.com/user/status/123 --to zh-CN

# 自动获取并翻译网页
python3 ~/.ai-skills/translate/scripts/translate.py --fetch https://example.com/article --to zh-CN

# 输出 prompt 到 stdout（Agent 直接消费）
python3 ~/.ai-skills/translate/scripts/translate.py article.md --stdout
```

## 翻译原则（核心）

Agent 翻译时**必须遵循**以下原则。这些原则适用于所有模式。

### 准确性
1. 事实、数据、逻辑必须与原文完全一致
2. 不增不减，不改变原文立场

### 表达
3. **意译优于直译**：翻译作者的意思，而非逐字翻译。当直译不自然或无法传达意图时，自由重组句式
4. **消除翻译腔**：句式应符合目标语言思维，不保留源语言语序
5. **情感保真**：保留原文措辞的情感色彩，不能把有情绪的词翻译成中性的

### 比喻与习语
6. **按含义翻译**：不逐字翻译比喻和习语，而是传达其"想要表达的意思"
7. 处理策略三选一：
   - **意译（Interpret）**：丢弃源语言意象，用目标语言直接表达含义
   - **替换（Substitute）**：用目标语言中传达同样含义的习语/比喻替换
   - **保留（Retain）**：当原始意象在目标语言中同样有效时保留

### 术语
8. 专业术语首次出现时 **中文（English）** 括号标注，后续只用中文
9. 参考术语表（`references/glossary-en-zh.md`），可通过 `--glossary` 追加
10. 对目标读者可能不熟的概念，添加简短的括号解释

### 格式
11. 保持所有 Markdown 格式（标题、列表、引用、链接、图片）
12. 保留 YAML frontmatter
13. 代码块内容不翻译

### 欧化语言检测（中日韩目标语言特有）
翻译为 CJK 语言时，**必须**避免以下问题：
- **多余连接词**：过度使用 因此/然而/此外/另外，上下文已暗示关系时省略
- **被动语态滥用**：能用主动语态时不用 被/由/受到
- **名词堆砌**：长修饰语链应拆分为多个短句
- **过度代词化**：中文中 他/她/它/我们/你 能省则省
- **过度名词化**：优先用动词（"讨论了" 而非 "进行了讨论"）

## 翻译模式

| 模式 | 步骤 | 适用场景 |
|------|------|----------|
| `quick` | 直接翻译 | 短文、推文、快速了解 |
| `normal` | 分析 → 翻译 | 一般文章（**默认**） |
| `refined` | 分析 → 初稿 → 审校 → 润色 | 重要文档、出版级 |

### normal 模式工作流
1. **分析** → `01-analysis.md`
2. **翻译** → `translation.md`

完成后提示用户：`翻译完成。如需进一步润色，回复"继续润色"或"refine"。`

### refined 模式工作流
详细步骤见 [references/refined-workflow.md](references/refined-workflow.md)

1. **分析** → `01-analysis.md`（领域、语气、术语、比喻映射、读者理解难点）
2. **初稿** → `03-draft.md`
3. **审校** → `04-critique.md`（仅诊断，不修改）
4. **修订** → `05-revision.md`（应用审校发现）
5. **润色** → `translation.md`（出版级最终稿）

## 内容分析模板（normal/refined 共用）

`01-analysis.md` 应包含：

```markdown
## 概要
[3-5 句核心摘要]

## 内容分析
- 核心论点：[一句话]
- 关键概念：[列表]
- 结构：[大纲]

## 背景
- 作者：[背景、立场]
- 写作语境：[回应什么现象/趋势]

## 术语提取
| 原文 | 翻译 | 说明 |
|------|------|------|

## 语气 & 风格
[评估]

## 比喻/习语映射
| 原文 | 含义 | 策略 | 建议译法 |
|------|------|------|----------|

## 读者理解难点
| 术语/段落 | 为何困难 | 建议注释 |
|-----------|---------|----------|
```

## 翻译风格

| 风格 | 说明 |
|------|------|
| `storytelling` | 叙事流畅，引人入胜（**默认**） |
| `formal` | 正式、专业 |
| `technical` | 精确、文档风格 |
| `conversational` | 口语化、亲切 |
| `academic` | 学术、严谨 |
| `elegant` | 文学、精雕细琢 |
| `humorous` | 保留并改编幽默 |
| `literal` | 贴近原文结构（仅特殊需求） |
| `business` | 简洁、结果导向 |

也支持自定义描述，如 `--style "诗意而抒情"`

## 目标受众

| 受众 | 效果 |
|------|------|
| `general` | 通俗语言，术语加注释（**默认**） |
| `developer` | 技术人员，少注释常见术语 |
| `academic` | 学术读者，正式措辞 |
| `business` | 商务人士，简洁结果导向 |

也支持自定义描述，如 `--audience "对 AI 感兴趣的普通读者"`

## 脚本参数

```bash
python3 ~/.ai-skills/translate/scripts/translate.py [source] [options]

# 位置参数
source              源文件路径

# 选项
--fetch <url>       自动获取 URL 内容（X 推文或网页）
--to <lang>         目标语言（默认: zh-CN）
--mode <mode>       翻译模式: quick|normal|refined（默认: normal）
--style <style>     翻译风格（默认: storytelling）
--audience <aud>    目标受众（默认: general）
--glossary <file>   额外术语表文件
--stdout            将 prompt 输出到 stdout 而非文件
--output-dir <dir>  自定义输出目录
--chunk-threshold   分块阈值，单位词数（默认: 4000）
```

## 输出结构

```
{source-name}-{target-lang}/
├── translation.md       # 最终翻译
├── 01-analysis.md       # 内容分析（normal/refined）
├── 03-draft.md          # 初稿（refined）
├── 04-critique.md       # 审校发现（refined）
├── 05-revision.md       # 修订稿（refined）
└── chunks/              # 长文分块（如有）
```

## 智能分块

脚本按 Markdown 结构分块（标题、段落、列表边界），不会把段落从中间切断：
- 优先在标题处分割
- 段落级别次之
- 超大段落按行回退分割
- 保留 YAML frontmatter

## 内容获取

### X 推文/Article
依赖 `baoyu-danger-x-to-markdown`（`~/.ai-skills/baoyu-danger-x-to-markdown/`）
- 需要 `X_AUTH_TOKEN` 和 `X_CT0`（在 `~/.baoyu-skills/.env`）

### 网页 URL
依赖 `baoyu-url-to-markdown`（`~/.ai-skills/baoyu-url-to-markdown/`）

## 术语表

内置 EN→ZH 术语表：`references/glossary-en-zh.md`
- 按领域分类：AI/Tech、Business、Philosophy、Creator Economy
- 仅收录易错/非显而易见的翻译
- 可通过 `--glossary` 追加项目级术语表
