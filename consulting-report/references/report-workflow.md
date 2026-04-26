# Report Workflow

This Agent Skill is interactive and platform-neutral. The agent must not proceed to formal report generation until the client confirms the chapter outline and the data source plan.

## Gate 1: Font Preflight

Run:

```bash
python scripts/font_preflight.py
```

If the required Chinese weights are available, continue to the brief interview. If not, tell the user:

- Which weights are missing
- Which fallback fonts are available
- How the report will visually differ

## Gate 2: Brief Interview

Use this concise interview when the user has not already provided enough detail:

```text
为了先把报告方向定准，我需要确认以下信息：
1. 报告主题与核心决策问题是什么？
2. 目标读者是谁？他们会用这份报告做什么决定？
3. 期望报告深度/页数大概是多少？
4. 你已经有哪些材料或数据？哪些内容需要保密？
5. 数据来源希望使用你提供的资料、公开资料，还是两者结合？
6. 是否有必须引用或禁止引用的来源？
7. 输出格式是否只要 PDF，还是还需要中间稿/图表数据？
```

Ask fewer questions when the answer is already present in the user request or files.

## Gate 3: Chapter Confirmation

After the brief, propose a custom outline. Do not use a fixed industry-report template. Use this structure:

```text
基于当前 brief，我建议报告采用以下章节：

1. <章节名>
   - 作用：<为什么需要这一章>
   - 决策问题：<本章回答什么问题>
   - 所需证据：<需要哪些数据/访谈/材料>
   - 可能展品：<图表或框架类型>

请确认这个章节结构是否可以继续；也可以告诉我需要删除、合并或调整的章节。
```

Stop here. Wait for explicit user confirmation or revision before moving on.

## Gate 4: Data Source Confirmation

Once the outline is confirmed, produce a data plan:

```text
下面是数据来源确认表：

| 章节 | 关键问题/结论 | 所需数据 | 建议来源 | 需要你确认 |
|---|---|---|---|---|
| ... | ... | ... | 用户资料/公开资料/估算 | 是否有资料或允许公开检索 |
```

Ask whether the user has these sources or wants public research. If public research is needed, confirm acceptable source types such as official statistics, company filings, industry associations, consulting reports, academic papers, and reputable financial media.

## Production Sequence After Confirmation

1. Create storyline/storyboard.
2. Draft page claims and evidence.
3. Generate exhibits with direct labels, notes, and sources.
4. Generate PDF under the active workspace output folder. Prefer `03-outputs/consulting-report/<run-name>/final/report.pdf` when that folder exists; otherwise use `outputs/consulting-report/<run-name>/final/report.pdf`.
5. Render selected pages for visual QA.
6. Report final paths and any remaining assumptions.
