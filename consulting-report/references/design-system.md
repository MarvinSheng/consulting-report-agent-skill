# Design System

This design system borrows the discipline of a top-tier consulting whitepaper without copying proprietary logos, brand fonts, cover art, or source content.

## Page Setup

- Default format: portrait professional report
- Default size: US Letter (`612 x 792 pt`) to match the reference PDF metadata
- Alternative size: A4 portrait when the client requests it
- Default margins: wide left/right whitespace with a centered content column
- Footer: page number, report title or short footer label, and optional source notes

## Typography

- Chinese primary: `STKaitiSC-Regular`
- Chinese emphasis: `STKaitiSC-Bold`
- Chinese headline: `STKaitiSC-Black`
- Latin fallback: available system serif/sans fonts; do not require proprietary McKinsey fonts

Suggested type scale:

| Element | Font | Size |
|---|---|---:|
| Cover title | STKaitiSC-Black | 34-48 pt |
| Chapter title | STKaitiSC-Black | 36-54 pt |
| Page headline | STKaitiSC-Black | 18-26 pt |
| Body text | STKaitiSC-Regular | 10-12 pt |
| Exhibit title | STKaitiSC-Bold | 13-16 pt |
| Exhibit labels | STKaitiSC-Regular | 8-10 pt |
| Notes/source | STKaitiSC-Regular | 6.5-8 pt |

## Color Palette

Use a restrained blue, black, gray, and cyan palette:

| Name | Hex | Usage |
|---|---|---|
| Deep Blue | `#174A9C` | Headline emphasis, chapter accents |
| Navy | `#111B3F` | Body and primary chart series |
| Cyan | `#26B6E8` | Secondary chart series and callouts |
| Steel Gray | `#6F7782` | Notes, axes, captions |
| Light Gray | `#E7E9ED` | Rules, fills, comparison bars |
| Black | `#111111` | Core body text |

## Page Components

Use components according to the confirmed storyline; do not force all components into every report.

- Cover page: report title, subtitle, date, optional client/author line, original non-proprietary visual if needed.
- Contents page: generated from the confirmed outline with actual page numbers after the report structure is finalized.
- Chapter intro page: large chapter title plus a short `章节导读` paragraph that explains the client question answered in the chapter; use selectively for major turns in the storyline.
- Whitepaper narrative page: body text organized around a single claim, with blue subheads, thin gray separators, and natural paragraphs.
- Exhibit page: one or more charts with figure number, title, subtitle, notes, and source.
- Mixed page: chart plus supporting interpretation.
- Callout page: a major quote, key implication, or transition claim.
- Appendix page: assumptions, methodology, detailed source tables.

## Layout Principles

- One page should have one dominant message.
- Body pages may be text-led; exhibit pages must be visual-led.
- Client-facing paragraphs should be left-aligned on a stable main text axis. Page headline, subheads, paragraph text, exhibit interpretation, and footnotes should not drift across unrelated x positions.
- Contents pages must use real page numbers and fit all chapters above the footer.
- Preserve generous whitespace. Do not fill every page with dense bullets.
- Use footnotes and source lines instead of hiding evidence.
- Avoid decorative borders, heavy shadows, and arbitrary color variety.
- Avoid whiteboard-style gray boxes, three-column reasoning frames, and visible analysis scaffolding in client deliverables.
- Do not expose internal labels such as `证据：`, `含义：`, `逻辑链条`, `事实基础`, `对客户启示`, `本章逻辑`, or `竞品` in the final PDF.
- For client-facing body pages, prefer white backgrounds with restrained blue subheads, thin horizontal rules, and 2-4 well-developed paragraphs. Do not shift the entire body block to the right of the headline; use the same left boundary for the headline, subheads, and paragraphs unless a card or callout layout is intentional.
- Wrap Chinese and mixed Chinese/English text by rendered width, not by a fixed character count. Avoid premature line breaks at punctuation, line-start punctuation, and one- or two-character orphan lines.
- Chapter intro pages should not be empty title pages; include a short guide to the chapter's business question and how the evidence will be used. Avoid using a full blue intro page for every chapter when it creates a stop-start reading rhythm; smaller chapters may begin with a chapter-labeled whitepaper page or exhibit page.
- Avoid awkward title wraps, especially one-character final lines. Adjust wrap width, shorten the title, or use a chapter label in the headline.
- Long text tables are risky in portrait layouts. Use two-column card grids, split the table across pages, or switch to landscape; never let tables extend beyond the right page boundary.
- Exhibit interpretation, footnotes, source lines, and table cells must all have conservative wrap widths. Render the page and check that no text is clipped on the right edge.
