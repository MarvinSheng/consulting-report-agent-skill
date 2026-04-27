# Consulting Report Agent Skill

这是一个平台无关的 Agent Skill，用于生成交互式中文咨询报告。它适合能读取技能文件夹或自定义指令的 Agent，例如 Codex、Claude、Gemini，以及其他支持长指令/文件上下文的 AI 助手。

## 能力

- 生成中文咨询报告、行业白皮书、市场分析、战略报告、竞争格局报告、尽调报告。
- 正式生成前先完成字体检查、客户 brief 访谈、章节确认和数据来源确认。
- 根据客户 brief 动态生成章节，不预设固定模板。
- 默认产出客户面向的咨询白皮书式 PDF：自然段落、专业小标题、图表解读和克制的咨询报告语气。
- 支持展品图表、来源标注、脚注、质量检查和 PDF 生成脚本；重要图表需包含 1-2 条客户可读解读。
- 内置版式护栏：正文使用稳定左对齐主轴，按实际渲染宽度换行；目录使用真实页码，图表解读与来源安全换行，长表格自动改为卡片/拆页/横向方案，章节导入页按阅读节奏使用。
- 中文字体优先使用本机 `STKaitiSC-Regular/Bold/Black`；不内置任何字体文件。

## 输出标准

最终 PDF 应面向客户阅读，而不是展示内部分析过程。正文应使用白底段落、蓝色小标题、细分隔线和自然叙事；正文段落、小标题和图表解读默认左对齐在稳定主轴上；避免浅灰白板框、三栏推理框和大面积空白。

最终 PDF 不应出现以下内部标签：`证据：`、`含义：`、`逻辑链条`、`事实基础`、`对客户启示`、`本章逻辑`、`竞品`。可使用更客户化的表达，例如“市场表现”“战略打法”“行业启示”“章节导读”“重点企业”“主要参与者”“竞争参与者”。

交付前应渲染抽查目录页、章节导读页、图表页、企业/表格页和策略建议页，确认没有正文主轴漂移、右侧裁切、标签重叠、标题孤字换行或页脚遮挡。

## 文件结构

```text
consulting-report-skill/
├─ consulting-report/
│  ├─ SKILL.md
│  ├─ agents/openai.yaml
│  ├─ references/
│  └─ scripts/
├─ adapters/
│  ├─ gemini/gem-instructions.md
│  └─ generic-agent-instructions.md
└─ consulting-report.skill
```

也可以直接下载本仓库中的 `consulting-report-agent-skill.zip` 或 `consulting-report.skill`。

## 安装方式

### Codex / OpenAI-style folder skills

把 `consulting-report/` 文件夹复制到你的 skills 目录，例如：

```bash
mkdir -p ~/.codex/skills
cp -R consulting-report ~/.codex/skills/
```

### Claude-style skills

把 `consulting-report/` 作为一个完整 Skill 文件夹导入或放到 Claude/Claude Code 支持的技能位置。保留 `SKILL.md`、`references/` 和 `scripts/`。

### Gemini Gems

Gemini Gems 更接近“自定义专家指令”。打开 Gemini 的 Gems 创建界面，把 `adapters/gemini/gem-instructions.md` 的内容复制进去；如果环境不能运行 Python 脚本，就把字体检查和 PDF 生成作为外部步骤处理。

### 通用 Agent

如果你的 Agent 只支持普通系统提示词或项目说明，把 `adapters/generic-agent-instructions.md` 作为主指令，并把 `consulting-report/references/` 中的文件作为参考资料提供给 Agent。

## 版权与字体

本仓库不包含麦肯锡 PDF、麦肯锡 Logo、McKinseySans、Bower 或其他专有资产。麦肯锡品牌字体只做近似替代。中文字体通过用户本机字体检查获得，不打包分发。

## 官方参考

- Claude Skills: https://platform.claude.com/docs/en/managed-agents/skills
- Gemini Gems: https://gemini.google/overview/gems/
- Gemini Gems Help: https://support.google.com/gemini/answer/15235603
