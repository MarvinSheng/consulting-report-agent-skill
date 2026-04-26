# Agent Compatibility

This package is a platform-neutral Agent Skill. The core workflow lives in `SKILL.md`; scripts and references are optional resources that capable agents may load or execute.

## Core Contract

Any agent using this skill must follow these gates:

1. Run or simulate font preflight.
2. Interview for the client brief.
3. Propose a custom chapter outline and wait for confirmation.
4. Propose a data source plan and wait for confirmation.
5. Only then generate storyline, exhibits, and report files.

## Codex / OpenAI-Style Folder Skills

Install the `consulting-report/` folder into the agent's skills directory. The `agents/openai.yaml` file is optional UI metadata and is not required by non-OpenAI agents.

## Claude-Style Skills

Use the same `consulting-report/` folder as the skill folder. Preserve `SKILL.md`, `references/`, and `scripts/`. If the Claude environment cannot execute local scripts, treat scripts as implementation references and perform font/PDF checks through the host environment.

## Gemini Gems

Gemini Gems are instruction-oriented rather than local folder/script bundles. Use `adapters/gemini/gem-instructions.md` from the public repository as the Gem instruction text, and upload or paste relevant reference files when needed.

Limitations for Gemini Gems:

- They may not execute the bundled Python scripts directly.
- PDF generation may require a local runner, Colab notebook, or another agent environment.
- Font preflight should be treated as a checklist unless the environment can run Python.

## Generic Agents

If an agent supports only plain instructions, provide:

- `SKILL.md`
- `references/report-workflow.md`
- `references/font-system.md`
- `references/exhibit-system.md`
- `references/quality-checklist.md`

Then ask it to follow the gates exactly and to request user confirmation before moving from outline to data plan or from data plan to production.
