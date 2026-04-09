---
name: content-engine
description: Review and optimize platform-native content against formatting rules, quality gates, and platform-specific best practices. Use after content-for-x or other content creation skills to audit hooks, formatting, CTA quality, and cross-platform consistency. 当用户说 内容审查, 质量检查, 发布前检查, or /content-review 时触发。
---

# Content Engine

Review content drafts against platform-specific rules and quality gates. Typically used after `content-for-x` (or similar creation skills) to ensure content is platform-native, hooks are strong, and formatting is correct before publishing.

## When to Activate

- reviewing X posts, threads, or articles before publishing
- checking formatting compliance for a specific platform
- auditing content quality (hooks, CTA, hype language)
- cross-platform consistency check when repurposing content

## First Questions

Clarify:
- platform: X, LinkedIn, TikTok, YouTube, newsletter, or multi-platform
- content type: tweet, thread, article, video script, etc.
- source: file path or inline content to review

## Platform Review Checklists

### X

#### Posts & Threads Review
- [ ] Hook 够强（亮结果/数字，不是"记录一下"）
- [ ] 每条只讲一个 idea
- [ ] 链接不在正文中间（放最后一条）
- [ ] 无 hashtag 堆砌
- [ ] 字数 ≤ 280（普通）或 ≤ 25,000（Premium）

#### X Article Review Checklist

**标题审查**（最重要）：

*原则*：X Article 标题是唯一决定用户是否点开的东西。在 feed 中只显示标题 + 封面图。

- [ ] **长度**：6-15 个词 / 50-71 个字符（feed 中完整显示的安全范围）
- [ ] **具体数字**：包含数字且用阿拉伯数字（"4 个" 而非 "四个"），放在标题前半部分
- [ ] **好奇心缺口**：暗示了结果但没完全揭示（读者必须点进来才知道答案）
- [ ] **价值承诺**：读者能在 2 秒内判断"看了有什么用"
- [ ] **无 hype**：不用"震惊""颠覆""必看""你不知道的"
- [ ] **关键词前置**：核心关键词在前半句（提高搜索可见度）
- [ ] **争议性/立场**：包含一个能引发讨论的观点或暗示（让人想评论反驳或表示认同）
- [ ] **与正文呼应**：标题承诺 = 正文第一段兑现

*好标题公式*：
· **[数字] + [动作] + [意外结果]** — "4 个 AI 审查同一份代码，发现了完全不同的 bug"
· **[反常识立场]** — "只用 1 个 AI 验收代码，你会漏掉一半以上的问题"
· **[争议性观点]** — "没有哪个 AI 能单独完成代码审查——包括你最信任的那个"
· **How-to + [具体收益]** — "如何用多 Agent 交叉验收找到单 Agent 漏掉的 bug"

**格式审查**：
- [ ] 段落标题用 emoji 开头（🔧、🧪、🏆 等），不用 `###` 也不用 `**`
- [ ] 正文为纯文本，无任何 Markdown 符号（`**`、`*`、`#`、`` ` ``、`|`、`- `、`![]()`、`[]()`、`> `、`---`）
- [ ] 加粗/斜体在 X Article 编辑器中用 Ctrl+B / Ctrl+I 手动应用，发布包中不标记
- [ ] 每段首行有两个全角空格缩进（`　　`，U+3000）
- [ ] 链接集中在文末「相关链接」区域，正文无内联链接
- [ ] 列表用 `·` 而非 `-`
- [ ] 段落间只换 1 行，不换 2 行（X Article 不需要 Markdown 的双换行）

**封面图审查**：
- [ ] 比例 5:2（1500×600）
- [ ] 封面包含文章标题文字
- [ ] 关键内容在垂直中间 40%（安全区），裁剪后无内容被切断
- [ ] 提示词使用了裁剪安全模板（布局约束在前，内容描述在后）
- [ ] 图片文件存在于 `imgs/cover.png`

**正文配图审查**：
- [ ] 2-4 张内嵌插图
- [ ] 插入位置合理（概念解释后 / 对比后 / 结论后）
- [ ] 每张有描述性 alt text
- [ ] 图片文件存在于 `imgs/`

**内容质量审查**：
- [ ] 开头 Hook：具体、有数字，第一句就给读者继续看的理由
- [ ] 每段一个 idea，不堆砌
- [ ] 无 hype 用语（"革命性""颠覆""game-changer""震惊"）
- [ ] 结尾 CTA：有互动提问，与内容匹配
- [ ] 内容读起来像平台原生帖子，不像文档/报告
- [ ] 段落间用 `---` 分隔，结构清晰

**审查结果格式**：
```
═══ X Article Quality Review ═══

格式：✅ 7/7 通过
封面：✅ 通过
配图：✅ 3/3 通过
质量：⚠️ 5/6 通过（⚠️ Hook 可以更具体）

总评：⚠️ 需小幅修订后通过
修改建议：
1. Hook 改为更具体的版本
```

### LinkedIn
- [ ] 第一行够强
- [ ] 短段落
- [ ] 明确的 lessons / results / takeaways

### TikTok / Short Video
- [ ] 前 3 秒打断注意力
- [ ] 脚本围绕视觉，不只是旁白
- [ ] 一个演示、一个观点、一个 CTA

### YouTube
- [ ] 结果前置
- [ ] 按章节结构化
- [ ] 每 20-30 秒刷新视觉

### Newsletter
- [ ] 一个清晰视角，不是无关内容堆砌
- [ ] 段落标题可扫读
- [ ] 开头段落做实事

## Review Flow

当审查内容时：
1. 确认平台类型（X Article / Thread / Tweet / 其他）
2. **先跑自动检查脚本**（X Article 用 `check-x-article.py`）
3. 脚本通过后，按 Review Checklist 人工审查标题、配图、内容质量
4. 产出审查结果（✅ 通过 / ⚠️ 需修订 / ❌ 不通过）
5. 给出具体修改建议（精确到哪一段、怎么改）
6. 修改后再次审查，直到全部 ✅
7. **审查通过后**，自动生成 HTML 预览：`python3 to-x-html.py <file>`

### 自动化检查

X Article 格式检查（零依赖）：
```bash
python3 ~/.ai-skills/content-engine/scripts/check-x-article.py <file>
```
检测项：`**` `*` `#` `![]()` `[]()` `>` `-` `` ` `` `|` `---`、连续空行、首行缩进

X Article HTML 预览生成（零依赖）：
```bash
python3 ~/.ai-skills/content-engine/scripts/to-x-html.py <input.md> [output.html]
```
将纯文本发布包转为带格式 HTML。浏览器打开 → 全选复制 → 粘贴到 X Article 编辑器，富文本格式（加粗标题、列表）自动保留。图片需在编辑器中手动上传。

## Quality Gate

审查通过的标准：
- 自动检查脚本 0 个 ❌
- 格式检查项全部 ✅
- 封面图和配图全部到位
- 内容质量无 ❌（允许 ⚠️ 但需标注原因）
- 读起来像平台原生帖子，不像文档

## 踩坑记录

| 错误 | 原因 | 教训 |
|------|------|------|
| 用 `**加粗**` 标记段落标题 | 误以为 X Article 支持 Markdown 加粗 | X Article 是富文本编辑器，`**` 会显示为字面星号。加粗用 Ctrl+B |
| 用 `![alt](path)` 嵌入图片 | 发布包是 .md 文件，习惯性用了 Markdown 图片语法 | X Article 图片必须在编辑器中手动上传，用〔〕标注上传位置 |
| 审查给了 30/30 全通过但实际有残留 | Agent 目测审查不可靠 | 格式检查必须先跑自动化脚本，不能只靠人工/Agent 判断 |
| 封面图裁切后内容不完整 | 提示词没有足够强调留白 | 5:2 裁切必须用裁切安全模板，明确声明上下 30% 纯背景 |

