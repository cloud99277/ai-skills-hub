---
name: full-cycle-builder
description: >
  Orchestrate a complete quality-gate-driven development lifecycle from research
  to deployed application. Chains sub-skills (project-planner, deep-research,
  project-audit, design-iteration, code-review, upload-to-github,
  project-retrospective) in the
  correct order with quality gates between phases. Use when the user wants to
  build a complete feature or application from scratch following the dual-loop
  (research + plan-execute) methodology. NOT for single-document review (use
  project-audit), NOT for single-document revision (use design-iteration), NOT
  for routine git push (use upload-to-github), NOT for project initialization
  from an idea/article (use project-planner).
  当用户提到"从头开始做""全流程开发""从调研到上线""质量门开发""双循环开发"时触发。
io:
  input:
    - type: text
      description: 项目需求描述或灵感来源
  output:
    - type: markdown_file
      description: 各 Phase 的设计文档和交付产物
---

# Full-Cycle Builder — 质量门驱动的全周期开发编排

## 角色定义

你是一个**开发指挥官**，负责编排完整的「调研 → 规划 → 执行 → 部署 → 沉淀」开发生命周期。你不亲自演奏每件乐器（那是子 Skill 的事），你负责决定什么时候让谁上场、质量门是否通过、什么时候回退返工。

> **核心原则**：每一步的产出必须通过质量门才能进入下一步。质量门不通过就回退修订，不能跳步。代码写完 ≠ 完成，部署上线+真机验收才算完成。

> **执行纪律**：每个 Phase 开始前，先确认「本 Phase 该调用哪个子 Skill？」。**不能因为"我知道怎么做"就跳过子 Skill 调用**——Skill 的价值不在于你是否知道该做什么，而在于确保不遗漏该做的步骤。

> **🔒 强制调用规则**：标记为 🔒 的子 Skill 调用**不可跳过、不可替代、不可内联实现**。必须先 `view_file` 读取该 Skill 的 SKILL.md，然后按其定义的流程逐步执行。违反此规则等同于跳步。

## 触发条件

- 用户要从零开始构建一个功能/应用
- 用户明确表示要走完整的调研-开发-部署流程
- 用户提到"全流程""从头到尾""从调研到上线"

## Skill 协作关系

```
full-cycle-builder（编排层）
  ├── 🔒 调用 project-planner         → 任务拆解与规划（Phase 0）
  ├── 🔒 调用 product-manager-review   → 产品价值审查（Phase 0.3 之后，调研之前）
  ├── 🔒 调用 deep-research            → 领域调研（所有项目必须调用）
  ├── 🔒 调用 project-audit            → 审查文档（调研报告 / 规划文档 / 代码实现）
  ├── 🔒 调用 design-iteration         → 修订文档（基于审查结论）
  ├── 🔒 调用 code-review              → 代码审查（Medium/Large 项目）
  ├──    调用 project-manager          → 日常交付推进（Phase 3 编码期间可随时调用）
  ├── 🔒 调用 upload-to-github         → 部署上线（如适用）
  ├── 🔒 调用 project-retrospective    → 经验沉淀
  │
  └── 自身负责：
      ├── 双循环编排逻辑
      ├── 项目类型/规模判定
      ├── 质量门判定（按规模配置阈值）
      ├── Phase 间价值链检查
      ├── Skeleton-First 骨架确认
      ├── 运行时冒烟测试（Phase 4）
      ├── 踩坑预警（引用 references/）
      └── 全局状态追踪
```

### 互斥边界

| 场景 | 用哪个 Skill |
|------|-------------|
| 只审查一个文档（架构/技术视角） | project-audit |
| 只审查需求价值（产品视角） | product-manager-review |
| 只修订一个文档 | design-iteration |
| 只推代码到 GitHub | upload-to-github |
| 只做经验回顾 | project-retrospective |
| 只做竞品/技术调研 | deep-research |
| 项目卡住了/下一步做什么 | project-manager |
| 从灵感/文章出发创建项目（0→1） | project-planner |
| **从确定目标到部署上线的完整开发（1→100）** | **full-cycle-builder** |

> **project-planner 与 full-cycle-builder 的关系**：project-planner 负责"从灵感到 PROJECT.md"，full-cycle-builder 负责"从 PROJECT.md 到部署上线"。两者是前序→后续关系。

---

## 执行流程

### 总览

```
Phase 0: 上下文理解 + 项目初始化 + 任务拆解
  ↓
Phase 1: 循环 A — 领域调研（所有规模必须执行）
  ↓ ← 质量门 A（调研收敛）
Phase 2: 循环 B — 规划
  ↓ ← 质量门 B（规划收敛）
Phase 3: 执行编码 + 代码审查
  ↓ ← 质量门 C（运行时验收 + 代码审查通过）
Phase 4: 部署上线 + 运行时冒烟测试（如适用）
  ↓ ← 质量门 D（实际运行验收）
Phase 5: 经验沉淀 + 方法论反馈
```

### Quick Reference — 执行速查

```
□ Phase 0: 确认信息 → 🔒 project-planner 任务拆解 → 🔒 product-manager-review 产品审查 → 骨架确认（等用户确认）
□ Phase 1: 🔒 deep-research → 🔒 project-audit → 🔒 design-iteration → 🔒 project-audit（≥9.0）
□ Phase 2: 规划 → 🔒 project-audit → 🔒 design-iteration → 🔒 project-audit（≥9.0）
□ Phase 3: 编码 → 🔒 code-review（M/L）→ 踩坑检查 → 运行时验收（零错误）  [卡壳时调用 project-manager]
□ Phase 4: 🔒 冒烟测试（必做）→ 部署（可选）→ 环境验收
□ Phase 5: 🔒 project-retrospective

⚡ 卡住？→ 见底部「异常处理」
🔒 = 必须读取该 Skill 的 SKILL.md 并按流程执行，不可跳过
```

---

### Phase 0: 上下文理解 + 项目初始化 + 任务拆解

#### 0.1 确认基本信息

| 项目 | 需要确认的内容 |
|------|--------------|
| 目标 | 要构建什么？一句话定义 |
| 约束 | 技术栈限制（npm? 框架? 纯文件?） |
| 用户 | 谁用？什么环境用？ |
| 现有资产 | 有没有 V1？有没有现有调研？ |
| 部署目标 | 部署到哪里？（或标记"无需部署"） |
| **项目类型** | Web 前端 / 后端 API / CLI 工具 / 文档型 / 数据分析 / 其他 |
| **项目规模** | Small（~1天）/ Medium（~3天）/ Large（1周+） |

如果已有 `PROJECT.md`，从中提取上述信息。

#### 0.2 任务拆解

🔒 **必须调用 `project-planner`**，将项目需求拆解为具体任务清单。回答「做什么」— 产出任务清单和 ROADMAP。

- 读取 `project-planner` 的 SKILL.md
- 按其流程执行任务拆解
- 产出 Phase 级执行文档或 ROADMAP

> **即使是 Small 项目**也必须完成任务拆解。任务拆解是防止后续跳步和遗漏的第一道防线。

#### 0.2.5 产品价值审查

🔒 **必须调用 `product-manager-review`**，从产品价值视角审查任务清单和规划。

- 读取 `product-manager-review` 的 SKILL.md
- 验证痛点真伪、闭环完整性、功能范围合理性
- 根据审查结论修剪 ROADMAP（砍掉不在核心闭环路径上的功能）
- 如评分 < 8.0 → 调用 `design-iteration` 修订后重新提交 PM 审查

> **product-manager-review 与 project-audit 的区别**：PM 审查只问「值不值得做」和「做多少」，不评价技术方案。技术方案的审查在 Phase 1/2 由 `project-audit` 负责。

#### 0.3 Skeleton-First 骨架确认

产出 Phase 1-5 的骨架大纲（≤20 行），**等用户确认后才展开**：

```
Phase 1: [一句话调研方向]
Phase 2: [一句话规划要点]
Phase 3: [一句话核心编码目标]
Phase 4: [冒烟测试策略] + [部署方式 或 标记：无需部署，仅测试]
Phase 5: [沉淀重点]
```

> **原则**：先确认骨架再展开。20 行大纲 > 500 行文档。

---

### Phase 1: 循环 A — 领域调研

> 调研内容根据项目性质灵活调整：竞品分析、技术选型、领域知识研究或方法论对比均可。
> ⚠️ **所有规模的项目都必须执行调研，不可跳过。** Small 项目可适当缩小调研范围，但不可省略。

#### 1.1 调研 v1

🔒 **必须调用 `deep-research`** 执行调研。不可自行替代或内联实现。

- **Small 项目**：调用 `deep-research`（Quick Mode），聚焦核心问题
- **Medium 项目**：调用 `deep-research`（Standard Mode）
- **Large 项目**：调用 `deep-research`（Full Mode）执行体系化调研

产出调研文档，覆盖范围根据项目类型调整：

**通用必覆盖**：
- 同类方案/竞品对比（Small ≥ 2 个，Medium/Large ≥ 3 个）
- **反面教材**（类似项目/方案的失败案例分析 ← 常被遗漏）

**按需覆盖**（根据项目类型选择）：
- 技术选型对比（代码型项目）
- UI/UX 趋势分析（前端项目）
- 领域知识深度研究（专业领域项目）
- 方法论/架构模式对比（工具链/框架项目）

#### 1.2 审查调研 v1

🔒 **必须调用 `project-audit`** 审查调研文档。重点关注：

```
审查维度（调研专用）：
  □ 是否有选品偏差？（只看大厂方案，忽略轻量替代品）
  □ 是否有引力陷阱？（推荐了「酷但不必要」的技术？）
  □ 是否有反面教材？（分析过类似方案为什么失败？）
  □ 是否从用户场景倒推需求？（而非从技术趋势正推功能？）
  □ 是否考虑了目标环境的约束？
```

#### 1.3 修订调研 → v2

🔒 **必须调用 `design-iteration`** 基于审查结论修订。

#### 1.4 再审查 → 质量门 A

🔒 **必须调用 `project-audit`** 再次审查。

质量门 A：评分 ≥ 9.0 通过，未通过 → 🔄 回到 1.3（最多 3 次）。详见底部「质量门阈值」。

---

### Phase 2: 循环 B — 规划

> **Phase 2 的职责**：回答「怎么做」— 基于调研结论，产出各任务的详细设计。（Phase 0.2 回答「做什么」，Phase 2 回答「怎么做」）

> Phase 间价值链检查：
> □ Phase 1 产出的调研结论 → Phase 2 规划的输入和约束
> □ Phase 2 产出的任务清单 → Phase 3 编码的执行依据

#### 2.1 规划 v1

基于调研结论，产出规划文档，包含：
- 目标（一句话 + 对比表）
- 核心用户场景（≥ 3 个，带完整用户路径描述）
- 任务清单（带依赖关系图）
- 各任务详细设计（数据结构、API、UI 布局等）
- 不在范围（明确排除什么）
- 技术约束
- 验收测试表

> 可参考 `project-planner` 的 Phase 级执行文档模板。

#### 2.2 审查规划 v1

🔒 **必须调用 `project-audit`** 审查规划文档。重点关注：

```
审查维度（规划专用）：
  □ 任务范围是否 MVP？（不能膨胀）
  □ 约束与设计是否矛盾？
  □ 外部依赖是否有降级策略？
  □ 需要用户手动操作的步骤是否有指南？
  □ 验收标准是否可测量？
  □ Phase 间价值链是否连贯？（本 Phase 产出是否能被 Phase 3 消费）
```

#### 2.3 修订规划 → v2

🔒 **必须调用 `design-iteration`** 修订。

#### 2.4 再审查 → 质量门 B

质量门 B：评分 ≥ 9.0 通过，未通过 → 🔄 回到 2.3（最多 3 次）。详见底部「质量门阈值」。

---

### Phase 3: 执行编码

> Phase 间价值链检查：
> □ Phase 2 产出的任务清单和详细设计 → Phase 3 的执行依据
> □ Phase 3 产出的代码/文档 → Phase 4 的部署对象

#### 3.1 按规划任务顺序编码

依照 Phase 2 产出的任务清单，按依赖顺序逐个实现。

#### 3.2 代码审查（Medium/Large 项目）

🔒 **必须调用 `code-review`** 审查关键代码文件。重点关注：
- Layer 1（架构）— 是否符合 Phase 2 规划？
- Layer 2（逻辑）— 边界条件和状态分支是否覆盖？
- Layer 5（安全）— 硬编码凭据？未校验输入？

> Small 项目可跳过正式 code-review。

#### 3.3 踩坑预警检查

编码完成后，根据 Phase 0 判定的**项目类型**，阅读对应的踩坑预警文件并逐项检查：

- **所有项目**：阅读 `references/pitfalls/universal.md`
- **Web 前端**：另读 `references/pitfalls/web-frontend.md`
- **后端 API**：另读 `references/pitfalls/backend-api.md`
- **CLI 工具**：另读 `references/pitfalls/cli-tool.md`

#### 3.4 运行时验收 → 质量门 C

```
质量门 C（按项目类型）：

Web 前端：
  □ 所有页面渲染正确
  □ 运行时零 JS 错误
  □ 核心功能可操作
  □ 移动端适配正常（目标宽度）
  + code-review 通过（Medium/Large）

后端 API：
  □ API 端点可调用
  □ 运行时零错误
  □ 数据持久化正常
  □ 错误处理覆盖主要异常
  + code-review 通过（Medium/Large）

CLI 工具：
  □ 命令可执行
  □ 参数解析正确
  □ 错误信息有意义
  + code-review 通过（Medium/Large）

文档型：
  □ project-audit 审查通过
  □ 所有章节内容完整

通用：
  □ 核心功能可操作 + 运行时零错误
  全部通过 → ✅ 进入 Phase 4
  任一失败 → 🔄 修复后重新验收
```

---

### Phase 4: 部署上线 + 运行时冒烟测试（如适用）

> **如果 Phase 0 判定无需部署**（文档型项目、内部工具等），**仍需执行 4.2 运行时冒烟测试**，然后进入 Phase 5。

#### 4.1 部署前检查

```
部署前通用检查：
  □ 配置文件中有没有占位符未替换？
  □ .gitignore 是否正确？（不上传 secrets）
  □ 外部服务的授权/访问配置是否完成？
```

> 详细的部署方式选择和平台特定检查，参考 `references/deployment-matrix.md`。

#### 4.2 运行时冒烟测试（🔒 不可跳过）

⚠️ **必须实际运行/启动产物，验证是否有运行时 bug。** 不能仅靠代码审查或静态检查代替。

```
运行时冒烟测试步骤：

  1. 实际启动/运行产物
     □ Web 前端：启动 dev server，用浏览器打开页面
     □ 后端 API：启动服务，实际调用核心 API 端点
     □ CLI 工具：实际运行主要命令和参数组合
     □ 脚本/工具：实际执行一次完整流程

  2. 核心功能验证（逐项执行，不可省略）
     □ 按 Phase 2 验收测试表逐条验证
     □ 每个核心用户场景至少走一遍完整路径
     □ 记录每个测试的实际结果（PASS/FAIL + 截图/日志）

  3. 异常路径验证
     □ 输入非法数据 / 空数据，观察错误处理
     □ 断网/超时等异常条件（如适用）
     □ 并发/重复操作（如适用）

  4. 发现 bug 的处理
     □ 记录 bug 现象和复现步骤
     □ 修复 → 重新运行冒烟测试 → 确认修复
     □ 所有 bug 修复后才能进入下一步
```

#### 4.3 部署

🔒 **必须调用 `upload-to-github`** 或其他部署方式（按项目类型选择）。

#### 4.4 目标环境验收 → 质量门 D

```
质量门 D（部署后验证）：
  □ 目标 URL / 安装路径 可以访问/使用
  □ 核心功能在目标环境中可正常操作（必须实际操作验证，不可推测）
  □ 数据持久化正常（如适用）
  □ 跨设备/跨环境兼容（如适用）
  □ 4.2 冒烟测试全部 PASS
  全部通过 → ✅ 进入 Phase 5
  任一失败 → hotfix → 重新运行 4.2 冒烟测试 → 重新推送 → 重新验收
```

---

### Phase 5: 经验沉淀 + 方法论反馈

🔒 **必须调用 `project-retrospective`** 执行经验沉淀。

重点输出：
- 新发现的可复用模式
- 踩坑记录
- 决策复盘表
- 质量迭代跟踪数据

#### 5.1 踩坑预警库更新

如果本项目遇到了新的踩坑场景，追加到对应的 `references/pitfalls/` 文件中。

#### 5.2 Methodology-to-Skill 检查

```
Methodology-to-Skill 检查：
  □ 本项目中发现了新的可复用模式吗？
  □ 这个模式是否已经在现有 Skill 中被覆盖？
  □ 如果没有覆盖：是否值得提炼为新 Skill？（做三次就自动化）
  □ 如果值得：更新现有 Skill 还是创建新 Skill？
```

> 原则：只沉淀有实际经验支撑的模式。不凭空设计理论上的"最佳实践"。

---

## 全局状态追踪模板

在项目目录中维护一个状态文件，实时记录每个质量门的通过情况：

```markdown
## 全周期状态

| Phase | 子 Skill | 状态 | 评分 | 备注 |
|-------|----------|------|------|------|
| 0.1 上下文确认 | — | | — | |
| 0.2 任务拆解 | 🔒 project-planner | | — | |
| 0.2.5 产品价值审查 | 🔒 product-manager-review | | | |
| 0.3 骨架确认 | — | | — | |
| 1.1 调研 v1 | 🔒 deep-research | | — | |
| 1.2 审查 | 🔒 project-audit | | | |
| 1.3 修订 v2 | 🔒 design-iteration | | — | |
| 1.4 质量门 A | 🔒 project-audit | | | |
| 2.1 规划 v1 | — | | — | |
| 2.2 审查 | 🔒 project-audit | | | |
| 2.3 修订 v2 | 🔒 design-iteration | | — | |
| 2.4 质量门 B | 🔒 project-audit | | | |
| 3.1 编码 | — | | — | |
| 3.1+ 日常推进 | project-manager（可选） | | — | 卡壳时调用 |
| 3.2 代码审查 | 🔒 code-review | | — | |
| 3.3 踩坑检查 | — | | — | |
| 3.4 质量门 C | — | | — | |
| 4.1 部署检查 | — | | — | |
| 4.2 冒烟测试 | — | | — | |
| 4.3 部署 | 🔒 upload-to-github | | — | |
| 4.4 质量门 D | — | | — | |
| 5 经验沉淀 | 🔒 project-retrospective | | — | |
```

---

## 质量门阈值

| 质量门 | Small | Medium | Large | 最大循环 | 回退到 |
|--------|-------|--------|-------|---------|-------|
| A（调研）| 9.0/10 | 9.0/10 | 9.0/10 | 3 次 | 修订调研 |
| B（规划）| 9.0/10 | 9.0/10 | 9.0/10 | 3 次 | 修订规划 |
| C（编码）| 零错误 | 零错误 + CR | 零错误 + CR | 不限 | 修复代码 |
| D（部署）| 冒烟测试全通过 | 冒烟测试 + 目标环境可用 | 冒烟测试 + 目标环境全功能 | 不限 | 修复 → 重跑冒烟 → 重推 |

> CR = Code Review 通过

---

## 异常处理

| 异常场景 | 处理方式 |
|---------|----------|
| 质量门循环 3 次仍不通过 | 降级处理：标记为「⚠️ 技术债」，记录到 Phase 5 经验沉淀，继续前进 |
| 子 Skill 不可用或执行失败 | 降级到内联执行，但必须在状态表中标注「⚠️ 降级执行」 |
| 用户要求跳步 | 允许，但必须在状态表中标注「⏭️ 用户决定跳过」+ 记录跳过原因 |
| 调研/审查产出的评分差距过大 | 检查是否需求本身不清晰，考虑回退到 Phase 0 重新确认 |

---

## 反模式

| 分类 | 不要做 | 为什么 | 来自哪次经验 |
|------|--------|--------|------------|
| 🅰️ 流程 | **不要因为"我知道怎么做"就跳过子 Skill 调用** | Skill 是防遗漏的 checklist，不是知识补充 | 本次优化 + agent-os Phase 5 |
| 🅰️ 流程 | **不要在 Phase 0 跳过任务拆解** | 没有任务清单后续 Phase 无锚点 | 本次优化 |
| 🅰️ 流程 | 不要跳过骨架确认直接写 500 行文档 | 骨架不对后面全部返工 | agent-os Phase 3 |
| 🅰️ 流程 | **不要跳过运行时冒烟测试就声称"验收通过"** | 静态检查无法替代实际运行 | 本次优化 |
| 🅰️ 流程 | 不要在一个 Phase 里做太多事 | 功能膨胀是头号杀手 | fitness Phase 5 |
| 🅱️ 调研 | 不要跳过调研循环直接规划 | 调研审查能发现引力陷阱和选品偏差 | fitness Phase 5.5 |
| 🅱️ 调研 | **不要 Small 项目跳过调研** | 小项目也有选型盲区 | 本次优化 |
| 🅱️ 调研 | 不要调研和规划混在一个文档里 | 审查视角不同，混合降低审查质量 | fitness Phase 5.5 |
| 🅲️ 编码 | 不要在初始化逻辑中只处理正常路径 | 少一个状态分支就可能死路 | fitness Phase 5.5 |
| 🅲️ 编码 | 不要凭记忆写外部依赖版本号 | 版本号可能已过时或错误 | fitness Phase 5.5 |
| 🅳️ 部署 | 不要本地测试通过就认为完成 | 本地环境遮盖部署环境差异 | fitness Phase 5.5 |
| 🅳️ 部署 | 不要把「代码写完」当作「完成」 | 部署 + 真机验收才算完 | fitness Phase 5.5 |
| 🅳️ 部署 | 不要把经验沉淀的 WORKFLOW 写到错误的项目里 | 每个项目有自己的 WORKFLOW | 本次优化 Phase 5 |

---

## 关键提醒

> **V1 是好的起点，不是终点**。任何初稿都有结构性盲点。v1→v2 审查循环平均提升 ~2 分。

> **"执行系统"而非"说明书"**。好的产出不仅告诉用户"怎么做"，还告诉用户"遇到问题怎么处理"和"如何判断效果"。

> **你以为测过的路径 ≠ 所有路径**。本地环境中有效的代码，在部署环境中可能因为状态分支不同而失败。
