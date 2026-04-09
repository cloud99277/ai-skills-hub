---
name: personal-dossier-builder
description: Build and maintain a living personal dossier from existing notes through gap analysis, interview-style follow-up, and structured writeback. Use when the user asks to 建个人档案, 补个人档案, 继续补档, 盘点还缺什么, 整理确认版摘要, or maintain a personal profile / operating manual over time. Prefer this over generic summarization when the goal is stable self-definition rather than a one-off recap.
io:
  input:
    - type: text
      description: 用户请求，可选包含目标个人目录、模式（init/gap-check/interview/update）与当前聚焦主题
  output:
    - type: markdown_file
      description: 更新后的个人档案文件，如 personal-master-dossier.md、personal-summary-confirmed.md，或新增的 open-items / decision-checklist
---

# personal-dossier-builder

这个 skill 用来维护一套可持续更新的个人档案系统，不是一次性的“人设包装”。

把它理解成：

- `structured interviewer`
- `dossier maintainer`
- `stable self-definition builder`

而不是：

- `persona generator`
- `personal branding generator`
- `resume generator`

## 什么时候用

- 用户说“帮我建立个人档案”
- 用户说“继续补档”
- 用户说“看看我还缺什么”
- 用户说“整理确认版摘要”
- 用户说“把关于我的信息沉淀成稳定档案”
- 用户想长期维护自我认知、职业路线、生活结构、决策规则

## 不要在这些场景用

- 只是要保存当前这次对话
  - 用 `conversation-distiller`
- 只是要写一版对外介绍、自我介绍、个人品牌文案
  - 用写作或内容类 skill
- 只是要做一份简历或岗位定制
  - 用职业/简历相关 skill
- 用户想做人格测试、贴标签、下心理诊断
  - 这个 skill 不做此类判断

## 默认目标

优先维护“双层结构”：

- `personal-master-dossier.md`
  - 详细档案，保留上下文、推理、待补项、冲突项
- `personal-summary-confirmed.md`
  - 确认摘要，只保留当前稳定成立的结论

可选联动文件：

- `profile.md`
- `preferences.md`
- `personal-operating-manual.md`
- `public-bio.md`

不要假设这些文件一定在固定位置。先发现目录结构，再决定文件角色。

## 核心工作流

1. 发现个人目录里的关键文件
2. 识别稳定结论、未定项、冲突项和过期项
3. 找出当前最值得追问的一个高价值主题
4. 用访谈式问题补齐该主题
5. 回写详细档案与确认摘要，并做一致性检查

## 四种模式

- `init`
  - 建立第一版档案骨架
- `gap-check`
  - 盘点缺口、冲突和下一轮优先级
- `interview`
  - 聚焦一个主题做访谈式补档
- `update`
  - 将新信息分类回写并同步摘要

如果用户没有指定模式：

- 已有主档案时，优先 `gap-check`
- 已知当前就在补某个主题时，优先 `interview`
- 没有主档案时，优先 `init`

## 参考导航

只在需要时读取这些参考文件，不要默认全部加载：

- 文件发现、目录判断、模式选择：
  - [references/discovery-and-modes.md](references/discovery-and-modes.md)
- 主题优先级、提问方式、访谈节奏：
  - [references/interview-playbook.md](references/interview-playbook.md)
- 状态模型、回写边界、一致性检查：
  - [references/state-writeback-and-checks.md](references/state-writeback-and-checks.md)

如果只是要先做一次轻量初扫，优先运行：

```bash
python3 ~/.ai-skills/personal-dossier-builder/scripts/scan_personal_dossier.py \
  --root /path/to/personal --json
```

如果要直接拿到一份可读的 `gap-check` 报告，运行：

```bash
python3 ~/.ai-skills/personal-dossier-builder/scripts/gap_check_report.py \
  --root /path/to/personal
```

## 主规则

- 一次只推进一个高价值主题
- 抽象词必须落地成可执行定义
- 优先使用用户自己的语言，不抢定义权
- `confirmed` 才能进入确认摘要主干
- `tentative` / `open` / `conflict` 不要混进 confirmed 主体
- 每轮结束时都要清楚说明：
  - 本轮确认了什么
  - 还有什么没定
  - 更新了哪些文件
  - 下一步最值得补什么

## 风格要求

- 语气要合作式，不要审问式
- 用户是在定义自己，不是在被归类
- 优先帮助用户看清取舍，不是替用户贴标签
- 保留主体性与尊重感

## 推荐搭配

需要检索已有知识时：

- `knowledge-search`

需要保存一次对话过程时：

- `conversation-distiller`

需要把稳定短结论写入共享记忆时：

- `l2-capture`

### 行为挖掘增强

interview 模式已集成 `tacit-mining` 的行为挖掘方法（关键事件/对比逼近/Laddering/反事实）。
当常规问卷式提问遇到「说不清」「差不多」时，自动切换到行为挖掘模式——
不问「你的标准是什么」，问「你做了什么」。详见 `references/interview-playbook.md`。

## 第一版边界

V1 先只做：

- 档案扫描
- 缺口识别
- 访谈补档
- 双层回写
- 一致性检查

V1 不做：

- 自动生成完整个人品牌内容包
- 自动发布到平台
- 复杂人格分类体系
- 投资、心理、医疗等高风险判断

## 可复用触发语

以下类型的请求都应该触发这个 skill：

- “继续补我的个人档案”
- “基于已有资料看看我还缺什么”
- “把这些新信息写进 confirmed summary”
- “帮我把个人资料整理成双层档案”
- “检查 master dossier 和 confirmed summary 是否一致”
