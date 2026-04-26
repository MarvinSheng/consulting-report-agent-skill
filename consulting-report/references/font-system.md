# Font System

## Reference Font Findings

The McKinsey reference PDF uses these embedded fonts:

- Chinese: `STKaitiSC-Regular`, `STKaitiSC-Bold`, `STKaitiSC-Black`
- Occasional Traditional Chinese fallback: `STKaitiTC-Regular`, `STKaitiTC-Black`
- Latin/brand: `McKinseySans-Light`, `McKinseySans-Regular`, `McKinseySans-Medium`, `Bower-Bold`

The production skill must match the Chinese font family whenever available. McKinsey brand fonts are proprietary and must not be extracted from a PDF or bundled without an explicit legal font file supplied by the user.

## Required Chinese Font

Preferred local font collection:

```text
/Users/marvinsheng/Library/Fonts/STKaiti-Kaiti.ttc
```

Required PostScript names inside the collection:

- `STKaitiSC-Regular`
- `STKaitiSC-Bold`
- `STKaitiSC-Black`

The generator registers these as ReportLab fonts with the same names. The default subfont indices in the known macOS collection are:

- Regular: 0
- Bold: 3
- Black: 5

## Fallback Policy

1. If `STKaitiSC` is available, use it for all Chinese body, titles, chart labels, notes, and page numbers.
2. If Regular is available but Bold/Black are missing, continue only after telling the user that emphasis weights will be visually weaker.
3. If no `STKaitiSC` is available, ask the user whether to provide the font file or accept a fallback such as system Kaiti, Songti, or Noto/Source Han.
4. Latin text and numbers may use an available system font such as Georgia, Helvetica, Arial, or Verdana if McKinsey brand fonts are unavailable.

## Preflight Command

```bash
python scripts/font_preflight.py
```

Optional:

```bash
python scripts/font_preflight.py --font-path /path/to/STKaiti-Kaiti.ttc --json
```
