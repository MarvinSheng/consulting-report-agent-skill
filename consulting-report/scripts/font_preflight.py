#!/usr/bin/env python3
"""Check whether the consulting-report skill can use STKaitiSC fonts."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List

from fontTools.ttLib import TTCollection, TTFont


ENV_FONT_PATH = os.environ.get("CONSULTING_REPORT_STKAITI_PATH")
DEFAULT_CANDIDATES = [
    *([Path(ENV_FONT_PATH)] if ENV_FONT_PATH else []),
    Path("/Users/marvinsheng/Library/Fonts/STKaiti-Kaiti.ttc"),
    Path.home() / "Library/Fonts/STKaiti-Kaiti.ttc",
    Path("/System/Library/Fonts/Supplemental/Kaiti.ttc"),
]

REQUIRED = ["STKaitiSC-Regular", "STKaitiSC-Bold", "STKaitiSC-Black"]


def _font_names(font: TTFont) -> List[str]:
    names = []
    for record in font["name"].names:
        if record.nameID in {1, 2, 4, 6}:
            try:
                names.append(record.toUnicode())
            except Exception:
                pass
    return sorted(set(names))


def scan_font_file(path: Path) -> Dict[str, object]:
    result = {"path": str(path), "exists": path.exists(), "fonts": [], "found": {}}
    if not path.exists():
        return result
    if path.is_dir():
        result["error"] = "path is a directory"
        return result

    if path.suffix.lower() == ".ttc":
        collection = TTCollection(str(path))
        fonts = collection.fonts
    else:
        fonts = [TTFont(str(path))]

    found = {}
    font_rows = []
    for index, font in enumerate(fonts):
        names = _font_names(font)
        font_rows.append({"index": index, "names": names})
        for required in REQUIRED:
            if required in names:
                found[required] = index

    result["fonts"] = font_rows
    result["found"] = found
    return result


def choose_candidate(explicit_path: str | None) -> Dict[str, object]:
    candidates = [Path(explicit_path)] if explicit_path else [p for p in DEFAULT_CANDIDATES if str(p)]
    scans = [scan_font_file(path) for path in candidates]
    for scan in scans:
        if all(name in scan["found"] for name in REQUIRED):
            scan["all_required"] = True
            scan["scans"] = scans
            return scan
    best = scans[0] if scans else {"path": "", "exists": False, "fonts": [], "found": {}}
    best["all_required"] = False
    best["scans"] = scans
    return best


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight STKaitiSC font availability.")
    parser.add_argument("--font-path", help="Path to STKaiti/Kaiti TTC or TTF file.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    result = choose_candidate(args.font_path)
    missing = [name for name in REQUIRED if name not in result["found"]]
    result["required"] = REQUIRED
    result["missing"] = missing

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Consulting report font preflight")
        print(f"Selected font file: {result['path']}")
        print(f"Exists: {result['exists']}")
        if result["found"]:
            print("Found required weights:")
            for name in REQUIRED:
                if name in result["found"]:
                    print(f"  [OK] {name} (subfont index {result['found'][name]})")
        if missing:
            print("Missing required weights:")
            for name in missing:
                print(f"  [MISSING] {name}")
            print("Chinese typography cannot fully match the McKinsey reference until these weights are available.")
        else:
            print("[OK] STKaitiSC Regular/Bold/Black are available.")

    return 0 if not missing else 2


if __name__ == "__main__":
    raise SystemExit(main())
