# Exhibit System

An exhibit is a sourced visual argument, not just a chart.

## Exhibit Object

Every exhibit should specify:

- Figure number
- Claim-style title
- Subtitle or scope note
- Unit
- Data table
- Chart type
- Direct labels
- Notes/footnotes
- Source line
- Interpretation points

## Chart Selection

| Analytical need | Preferred exhibit |
|---|---|
| Size or ranking | Horizontal bar, vertical bar, indexed bar |
| Trend over time | Line, area, slope chart |
| Composition | Stacked bar, 100% stacked bar |
| Relationship | Scatter, bubble scatter, quadrant |
| Scenario comparison | Matrix, sensitivity table |
| Multi-part argument | Small multiples or two-panel exhibit |
| Evidence detail | Table with inline bars |

Avoid pie charts unless the user explicitly requests them.

## Labeling Rules

- Put key values directly on bars, points, or lines.
- Include units in the subtitle or axis label.
- Use legends only when direct labeling would clutter the chart.
- Add notes for methodology, definitions, sample size, and caveats.
- Add source lines for every chart.
- Add 1-2 client-readable interpretation points below every important exhibit. These should summarize what the chart means for the audience, not describe how the analysis was performed.
- Keep interpretation points concise and decision-oriented. They should answer "what should the client take from this?" rather than restating the chart.
- Wrap title, subtitle, notes, source lines, and interpretation points within the exhibit text column. Do not use long unwrapped strings or bullets that can run off the right page boundary.
- Do not invent precision: round numbers consistently.

## Tables and Matrices

- Use a table only when the information remains readable within the available content width.
- For portrait reports, convert long multi-column comparison tables into card grids or split them across pages.
- For heatmaps and matrices, wrap or rotate axis labels so they remain legible after PDF rendering.
- Re-render any exhibit page with dense labels before delivery and inspect it visually.

## Source Rules

Every final chart needs one of:

- User-provided file reference
- Public URL or publication name/date
- Client-approved estimate labeled as an estimate
- Explicit assumption labeled as an assumption

If the source is not confirmed, mark the chart as draft and do not present it as final.
