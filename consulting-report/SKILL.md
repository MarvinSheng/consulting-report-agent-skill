---
name: consulting-report
description: Platform-neutral Agent Skill for interactive Chinese consulting report production across agents such as Codex, Claude, Gemini, and other AI assistants that can follow bundled instructions. Use when the user asks to create, improve, or generate a polished Chinese consulting report, strategy report, industry whitepaper, market analysis, competitive landscape, due diligence report, or executive decision report with custom chapters, client-confirmed brief, data source confirmation, exhibit-quality charts, STKaitiSC Chinese typography, and final quality checks. This skill must ask before proceeding through report gates instead of jumping directly to final generation.
---

# Consulting Report

This is a platform-neutral Agent Skill. Agents that support folder-based skills can load this folder directly. Agents that only support custom instructions should use the workflow in this file plus the platform adapter notes in `references/agent-compatibility.md`.

## Core Rule

Do not generate the final report immediately. Run the report through four gates:

1. Font preflight
2. Client brief interview
3. Chapter outline confirmation
4. Data source confirmation

Only after the user confirms the chapter outline and data source plan should you draft the storyline, exhibits, body pages, and PDF.

Final PDFs must read like client-facing consulting whitepapers, not internal reasoning boards. Build the evidence chain internally, then rewrite it into polished prose with natural paragraphs, client-safe section headings, and exhibit interpretation.

## Workflow

### 1. Font Preflight

Run `scripts/font_preflight.py` before report production. The preferred Chinese font is `STKaitiSC` with Regular, Bold, and Black weights.

- If all weights are available, report that Chinese typography can match the reference style.
- If any required weight is missing, explain the missing weight, available fallback, and likely visual impact.
- McKinsey brand fonts such as McKinseySans and Bower must not be copied from reference PDFs. Use a visually similar available font for Latin text and numbers.

Read `references/font-system.md` when font details or troubleshooting matter.

### 2. Client Brief Interview

Before proposing chapters, collect the missing brief fields in one structured round:

- Report topic and decision question
- Target readers and use scenario
- Intended outcome or decision the report should support
- Desired depth, length, and output format
- Existing materials and whether they are confidential
- Required or forbidden data sources
- Language, tone, and brand preference
- Deadline or constraints

Ask only for information that cannot be inferred from the user or provided files.

### 3. Chapter Confirmation Gate

Generate a custom outline from the brief. Do not use a fixed chapter template.

For each proposed chapter, include:

- Why the chapter exists
- The decision question it answers
- The likely evidence or data needed
- Expected exhibit types, if any

Stop and ask the user to confirm or revise the outline. Do not collect data, write body text, or generate slides/pages until the user confirms the chapter structure.

### 4. Data Source Confirmation Gate

After the outline is confirmed, create a chapter-by-chapter data plan.

For every important claim or exhibit, mark whether it should come from:

- User-provided files
- Public research
- Paid/proprietary sources supplied by the user
- Explicitly labeled estimates or assumptions

Ask the user whether they have the required sources or want public research. Confirm acceptable source types before web research.

### 5. Storyline, Exhibits, and PDF

After both gates are confirmed:

1. Build a storyline/storyboard before writing full pages.
2. Build an internal evidence chain for each important claim.
3. Rewrite the evidence chain into client-facing whitepaper prose: natural paragraphs, concise blue subheads, thin separators, and no exposed analysis-process labels.
4. Create exhibit-quality charts using `scripts/generate_report.py`, including wrapped notes, wrapped source lines, and interpretation points under every important exhibit.
5. Use actual page numbers in the contents page; do not use placeholder or formula-generated page numbers.
6. Keep chapter-intro pacing intentional: use full-page chapter intros for major turns in the storyline, and let smaller chapters start on a whitepaper body or exhibit page when that improves rhythm.
7. For long tables in portrait PDFs, use card grids, split pages, or a landscape page; never allow a table or interpretation text to exceed the right page boundary.
8. Store outputs under the active workspace output folder. Prefer `03-outputs/consulting-report/<run-name>/` when that folder exists; otherwise use `outputs/consulting-report/<run-name>/`.
9. Run the quality checklist in `references/quality-checklist.md` before delivery.

The final PDF must not contain internal drafting labels such as `证据：`, `含义：`, `逻辑链条`, `事实基础`, `对客户启示`, `本章逻辑`, or `竞品`. Use client-facing wording such as "市场表现", "战略打法", "行业启示", "章节导读", "重点企业", "主要参与者", and "竞争参与者".

## References

- `references/report-workflow.md` - detailed gate-by-gate workflow and user prompts.
- `references/font-system.md` - STKaitiSC font requirements, fallback policy, and preflight behavior.
- `references/design-system.md` - page components and report layout standards.
- `references/exhibit-system.md` - chart/exhibit structure, labeling, and source rules.
- `references/quality-checklist.md` - final acceptance checklist.
- `references/agent-compatibility.md` - platform-neutral usage notes for Codex, Claude, Gemini, and plain agents.

## Scripts

- `scripts/font_preflight.py` - checks whether required STKaitiSC weights are available.
- `scripts/generate_report.py` - reusable PDF/report engine and demo report generator.
