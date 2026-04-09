# Discovery and Modes

## 期望维护的文档层次

优先维护“双层结构”：

- `personal-master-dossier.md`
  - 详细档案，保留推理、上下文、待补项、开放问题
- `personal-summary-confirmed.md`
  - 确认摘要，只保留当前稳定成立的结论

可选 supporting docs：

- `profile.md`
- `preferences.md`
- `personal-operating-manual.md`
- `public-bio.md`
- 个人领域下的职业、项目、案例、访谈准备材料

## 默认发现策略

当用户给出一个个人知识目录时：

1. 先看目录结构和文件命名
2. 找出最可能的主档案与摘要档案
3. 再找 supporting docs
4. 最后才补读具体内容

优先按文件名检索这些候选：

- `personal-master-dossier.md`
- `personal-summary-confirmed.md`
- `profile.md`
- `preferences.md`
- `personal-operating-manual.md`
- `public-bio.md`

如果目录结构已经重组，不要假设这些文件一定在旧位置。先递归发现，再决定角色。

## 同名文件冲突处理

如果同名文件有多份：

- 优先选择离个人根目录最近的版本
- 优先选择文件名更明确的版本
- 如仍冲突，先向用户确认，或在详细档案标注歧义

## 模式说明

### `init`

当个人档案体系还不存在或非常零散时使用。

目标：

- 建立第一版档案骨架
- 识别现有资料来源
- 开始第一轮高价值访谈

### `gap-check`

当已有档案时，先做缺口盘点。

目标：

- 识别未定项、冲突项、过期项
- 按优先级列出下一轮最值得补的主题

### `interview`

当用户明确要继续补档时使用。

目标：

- 一次只推进一个主题块
- 通过少量高质量问题补足关键判断

### `update`

当用户已经给出新信息，需要回写档案时使用。

目标：

- 分类写回
- 更新详细档案
- 同步确认摘要
- 检查一致性

## 默认模式选择

如果用户没有指定模式：

- 已有主档案时，优先 `gap-check`
- 已知当前就在补某个主题时，优先 `interview`
- 没有主档案时，优先 `init`

## 最小发现顺序

每次都按这个顺序推进，减少无效读取：

1. 目录结构
2. 候选文件名
3. 主档案与摘要档案
4. supporting docs
5. 具体内容

## 轻量初扫脚本

如果只是要先建立一份启发式地图，先运行：

```bash
python3 ~/.ai-skills/personal-dossier-builder/scripts/scan_personal_dossier.py \
  --root /path/to/personal --json
```

脚本会返回三类初步结果：

- `confirmed_candidates`
- `open_items`
- `conflict_signals`

注意：

- 它只做启发式初扫，不负责判定真值
- 输出适合拿来决定“下一轮先问什么”
- 真正回写前仍然需要人工或 agent 二次判断

## Markdown gap-check 报告

如果想直接拿到一份更适合阅读的报告，运行：

```bash
python3 ~/.ai-skills/personal-dossier-builder/scripts/gap_check_report.py \
  --root /path/to/personal
```

这个报告会在初扫结果之上补三层信息：

- 文件发现总览
- open items 的主题归类
- 下一轮最值得推进的主题建议
