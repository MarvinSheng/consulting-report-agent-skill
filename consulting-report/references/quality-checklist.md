# Quality Checklist

Run this before final delivery.

## Interaction Gates

- Font preflight was run and reported.
- Client brief was collected or inferred from provided materials.
- Chapter outline was confirmed by the user.
- Data source plan was confirmed by the user.
- Any assumptions are documented.

## Logic

- The report answers the client's decision question.
- Chapters follow the confirmed outline, not a generic template.
- Each key claim has evidence, a source, or a labeled assumption.
- Storyline moves from context to evidence to implication internally, then appears in the final PDF as polished client-facing prose.
- Recommendations are specific to the client brief.

## Typography and Layout

- Chinese text uses `STKaitiSC` when available.
- No page has overlapping text, clipped labels, or unreadable footnotes.
- Headline hierarchy is consistent.
- Footer and page numbers are consistent.
- White space is deliberate.
- Body pages use whitepaper-style paragraphs, blue subheads, and thin separators rather than whiteboard-style gray boxes.
- Chapter intro pages include client-readable guidance and are not empty title-only pages.
- Run `pdftotext` or equivalent text extraction and confirm the final PDF does not contain `证据：`, `含义：`, `逻辑链条`, `事实基础`, `对客户启示`, `本章逻辑`, or `竞品`.

## Exhibits

- Every chart has a figure number, title, subtitle/unit, notes, and source.
- Every important chart has 1-2 interpretation points written for the target audience.
- Key values are directly labeled.
- Colors are limited and meaningful.
- Axes and labels are readable after PDF rendering.
- Draft or estimated data is clearly marked.

## Delivery

- Final PDF is under the active workspace output folder: prefer `03-outputs/consulting-report/<run-name>/final/report.pdf` when available, otherwise `outputs/consulting-report/<run-name>/final/report.pdf`.
- Intermediate artifacts are under the same run folder.
- Render and inspect at least four representative pages before delivery: a core insight page, a market/structure page, a company or participant analysis page, and a recommendation page.
- Final response cites relative output paths.
