#!/usr/bin/env python3
"""Reusable PDF engine for interactive Chinese consulting reports."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_FONT_PATH = Path(os.environ.get("CONSULTING_REPORT_STKAITI_PATH", "/Users/marvinsheng/Library/Fonts/STKaiti-Kaiti.ttc"))


class Colors:
    DEEP_BLUE = HexColor("#174A9C")
    NAVY = HexColor("#111B3F")
    CYAN = HexColor("#26B6E8")
    GRAY = HexColor("#6F7782")
    LIGHT_GRAY = HexColor("#E7E9ED")
    TEXT = HexColor("#111111")
    WHITE = HexColor("#FFFFFF")


FONT_REGULAR = "STKaitiSC-Regular"
FONT_BOLD = "STKaitiSC-Bold"
FONT_BLACK = "STKaitiSC-Black"
LATIN_FALLBACK = "Helvetica"


def register_fonts(font_path: Path = DEFAULT_FONT_PATH) -> Path:
    """Register STKaitiSC fonts for ReportLab and Matplotlib."""
    if not font_path.exists():
        raise FileNotFoundError(f"Required Chinese font file not found: {font_path}")

    pdfmetrics.registerFont(TTFont(FONT_REGULAR, str(font_path), subfontIndex=0))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, str(font_path), subfontIndex=3))
    pdfmetrics.registerFont(TTFont(FONT_BLACK, str(font_path), subfontIndex=5))

    try:
        font_manager.fontManager.addfont(str(font_path))
        plt.rcParams["font.family"] = "Kaiti SC"
    except Exception:
        plt.rcParams["font.family"] = "serif"
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "white"
    plt.rcParams["text.color"] = "#111111"
    plt.rcParams["axes.edgecolor"] = "#B8B8B8"
    plt.rcParams["xtick.color"] = "#6F7782"
    plt.rcParams["ytick.color"] = "#6F7782"
    return font_path


def wrap_text(text: str, chars: int) -> List[str]:
    if not text:
        return []
    lines = []
    while len(text) > chars:
        split = chars
        for mark in ["，", "。", "；", "、", "：", " ", "）"]:
            pos = text.rfind(mark, 0, chars + 1)
            if pos > chars * 0.45:
                split = pos + 1
                break
        remaining = len(text) - split
        if 0 < remaining <= 2 and split > max(4, chars * 0.6):
            split = max(4, split - (3 - remaining))
        lines.append(text[:split].strip())
        text = text[split:].strip()
    if text:
        lines.append(text)
    return lines


NO_LINE_START = set("，。；：、？！,.!?;:)]}）】》」』")
NO_LINE_END = set("（【《「『([{")


def wrap_text_width(text: str, font_name: str, font_size: float, max_width: float) -> List[str]:
    """Wrap text by rendered width, keeping CJK punctuation in sensible places."""
    if not text:
        return []

    def width(value: str) -> float:
        return pdfmetrics.stringWidth(value, font_name, font_size)

    def tokens(value: str) -> List[str]:
        out: List[str] = []
        latin = ""
        for char in value.strip():
            if char.isspace():
                if latin:
                    out.append(latin)
                    latin = ""
                out.append(" ")
            elif ord(char) < 128 and (char.isalnum() or char in "/._%+-"):
                latin += char
            else:
                if latin:
                    out.append(latin)
                    latin = ""
                out.append(char)
        if latin:
            out.append(latin)
        return out

    lines: List[str] = []
    current = ""
    for token in tokens(text):
        candidate = (current + token).strip() if token == " " else current + token
        if width(candidate) <= max_width or not current:
            current = candidate
            continue

        line = current.rstrip()
        next_line = token.lstrip()
        if token in NO_LINE_START and line:
            line += token
            next_line = ""
        if line and line[-1] in NO_LINE_END and len(line) > 1:
            next_line = line[-1] + next_line
            line = line[:-1].rstrip()
        if line:
            lines.append(line)
        current = next_line

    if current.strip():
        lines.append(current.strip())

    if len(lines) >= 2 and len(lines[-1]) <= 2:
        tail = lines.pop()
        previous = lines.pop()
        move = min(4, max(1, len(previous) // 5))
        lines.append(previous[:-move].rstrip())
        lines.append((previous[-move:] + tail).strip())
    return [line for line in lines if line]


@dataclass
class Exhibit:
    number: str
    title: str
    subtitle: str
    source: str
    chart: BytesIO
    notes: str = ""
    interpretation: Optional[List[str]] = None


class ConsultingReport:
    """A small portrait report engine with STKaitiSC typography."""

    def __init__(
        self,
        output_path: Path,
        title: str,
        subtitle: str = "",
        footer_label: str = "",
        page_size: str = "letter",
        font_path: Path = DEFAULT_FONT_PATH,
    ):
        register_fonts(font_path)
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.title = title
        self.subtitle = subtitle
        self.footer_label = footer_label or title
        self.page_size = letter if page_size == "letter" else A4
        self.w, self.h = self.page_size
        self.margin_x = 72
        self.top = 84
        self.bottom = 54
        self.page = 0
        self.c = canvas.Canvas(str(self.output_path), pagesize=self.page_size)
        self.c.setTitle(title)

    @property
    def content_w(self) -> float:
        return self.w - self.margin_x * 2

    def _new_page(self) -> None:
        if self.page:
            self.c.showPage()
        self.page += 1

    def _footer(self) -> None:
        c = self.c
        c.setStrokeColor(Colors.TEXT)
        c.setLineWidth(0.4)
        c.line(self.margin_x, 42, self.w - self.margin_x, 42)
        c.setFillColor(Colors.TEXT)
        c.setFont(FONT_REGULAR, 7.5)
        c.drawString(self.margin_x, 27, self.footer_label[:28])
        c.drawRightString(self.w - self.margin_x, 27, str(self.page))

    def cover(self, date: str = "", note: str = "") -> None:
        self._new_page()
        c = self.c
        c.setFillColor(Colors.DEEP_BLUE)
        c.rect(0, 0, self.w, self.h, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(FONT_BLACK, 36)
        y = self.h - 210
        for line in wrap_text(self.title, 14):
            c.drawString(self.margin_x, y, line)
            y -= 48
        if self.subtitle:
            c.setFont(FONT_REGULAR, 15)
            y -= 18
            for line in wrap_text(self.subtitle, 22):
                c.drawString(self.margin_x, y, line)
                y -= 23
        if note:
            c.setFont(FONT_REGULAR, 10.5)
            y -= 28
            for line in wrap_text(note, 27):
                c.drawString(self.margin_x, y, line)
                y -= 17
        if date:
            c.setFont(FONT_REGULAR, 10)
            c.drawString(self.margin_x, 72, date)

    def contents(self, chapters: List[str], page_numbers: Optional[List[int]] = None) -> None:
        self._new_page()
        c = self.c
        c.setFillColor(Colors.TEXT)
        c.setFont(FONT_BLACK, 30)
        c.drawString(self.margin_x + 72, self.h - 130, "目录")
        y = self.h - 190
        row_gap = min(72, max(50, (self.h - 260) / max(len(chapters), 1)))
        for idx, chapter in enumerate(chapters, 1):
            c.setFillColor(Colors.DEEP_BLUE)
            c.setFont(FONT_BOLD, 11)
            c.drawString(self.margin_x + 72, y, f"第{idx}章")
            c.setFillColor(Colors.TEXT)
            c.setFont(FONT_BOLD, 12.5)
            c.drawString(self.margin_x + 72, y - 20, chapter)
            if page_numbers and idx <= len(page_numbers):
                c.setFont(FONT_REGULAR, 12)
                c.drawRightString(self.w - self.margin_x, y - 10, str(page_numbers[idx - 1]))
            y -= row_gap
        self._footer()

    def chapter_divider(self, chapter_label: str, chapter_title: str) -> None:
        self._new_page()
        c = self.c
        c.setFillColor(Colors.DEEP_BLUE)
        c.rect(0, 0, self.w, self.h, fill=1, stroke=0)
        c.setFillColor(Colors.CYAN)
        c.setFont(FONT_BOLD, 18)
        c.drawString(self.margin_x + 90, self.h - 180, chapter_label)
        c.setFillColor(white)
        c.setFont(FONT_BLACK, 46)
        y = self.h - 310
        for line in wrap_text(chapter_title, 10):
            c.drawString(self.margin_x + 90, y, line)
            y -= 58

    def chapter_intro(self, chapter_label: str, chapter_title: str, guide: Iterable[str]) -> None:
        self._new_page()
        c = self.c
        c.setFillColor(Colors.DEEP_BLUE)
        c.rect(0, 0, self.w, self.h, fill=1, stroke=0)
        x = self.margin_x
        max_w = self.content_w
        y = self.h - 165
        c.setFillColor(Colors.CYAN)
        c.setFont(FONT_BOLD, 17)
        c.drawString(x, y, chapter_label)
        y -= 80
        c.setFillColor(white)
        c.setFont(FONT_BLACK, 42)
        for line in wrap_text_width(chapter_title, FONT_BLACK, 42, max_w):
            c.drawString(x, y, line)
            y -= 52
        y -= 24
        c.setFillColor(Colors.CYAN)
        c.setFont(FONT_BOLD, 11.5)
        c.drawString(x, y, "章节导读")
        y -= 30
        c.setFillColor(white)
        c.setFont(FONT_REGULAR, 10.8)
        for paragraph in guide:
            for line in wrap_text_width(paragraph, FONT_REGULAR, 10.8, max_w):
                c.drawString(x, y, line)
                y -= 17
            y -= 8

    def narrative_page(self, headline: str, paragraphs: Iterable[str], footnote: str = "") -> None:
        self._new_page()
        c = self.c
        y = self.h - 118
        c.setFillColor(Colors.DEEP_BLUE)
        c.setFont(FONT_BLACK, 21)
        for line in wrap_text_width(headline, FONT_BLACK, 21, self.content_w):
            c.drawString(self.margin_x, y, line)
            y -= 30
        y -= 22
        c.setFillColor(Colors.TEXT)
        c.setFont(FONT_REGULAR, 10.8)
        for para in paragraphs:
            for line in wrap_text_width(para, FONT_REGULAR, 10.8, self.content_w):
                c.drawString(self.margin_x, y, line)
                y -= 17
            y -= 12
        if footnote:
            c.setFont(FONT_REGULAR, 7)
            c.setFillColor(Colors.GRAY)
            for line in wrap_text(footnote, 76):
                c.drawString(self.margin_x, 58, line)
        self._footer()

    def whitepaper_page(
        self,
        headline: str,
        sections: Iterable[tuple[str, Iterable[str]]],
        footnote: str = "",
    ) -> None:
        self._new_page()
        c = self.c
        y = self.h - 112
        c.setFillColor(Colors.DEEP_BLUE)
        c.setFont(FONT_BLACK, 21)
        for line in wrap_text_width(headline, FONT_BLACK, 21, self.content_w):
            c.drawString(self.margin_x, y, line)
            y -= 30
        y -= 14
        x = self.margin_x
        max_w = self.content_w
        for title, paragraphs in sections:
            c.setFillColor(Colors.DEEP_BLUE)
            c.setFont(FONT_BOLD, 11.5)
            for line in wrap_text_width(title, FONT_BOLD, 11.5, max_w):
                c.drawString(x, y, line)
                y -= 15
            y -= 16
            c.setStrokeColor(Colors.LIGHT_GRAY)
            c.setLineWidth(0.5)
            c.line(x, y + 5, self.w - self.margin_x, y + 5)
            y -= 10
            c.setFillColor(Colors.TEXT)
            c.setFont(FONT_REGULAR, 9.6)
            for paragraph in paragraphs:
                for line in wrap_text_width(paragraph, FONT_REGULAR, 9.6, max_w):
                    c.drawString(x, y, line)
                    y -= 15
                y -= 8
            y -= 14
        if footnote:
            c.setFont(FONT_REGULAR, 7)
            c.setFillColor(Colors.GRAY)
            for line in wrap_text(footnote, 76):
                c.drawString(self.margin_x, 58, line)
        self._footer()

    def exhibit_page(self, exhibit: Exhibit) -> None:
        self._new_page()
        c = self.c
        y = self.h - 102
        c.setFillColor(Colors.TEXT)
        c.setFont(FONT_REGULAR, 10)
        x = self.margin_x
        right_x = self.w - self.margin_x
        c.drawString(x, y, f"图{exhibit.number}")
        y -= 25
        c.setFont(FONT_BOLD, 15)
        for line in wrap_text_width(exhibit.title, FONT_BOLD, 15, right_x - x):
            c.drawString(x, y, line)
            y -= 22
        c.setFont(FONT_BOLD, 10)
        for line in wrap_text_width(exhibit.subtitle, FONT_BOLD, 10, right_x - x):
            c.drawString(x, y - 4, line)
            y -= 12
        chart_y = y - 320
        c.drawImage(ImageReader(exhibit.chart), x, chart_y, width=right_x - x, height=285, preserveAspectRatio=True)
        c.setFont(FONT_REGULAR, 7)
        c.setFillColor(Colors.GRAY)
        note_y = chart_y - 20
        if exhibit.notes:
            for line in wrap_text_width(exhibit.notes, FONT_REGULAR, 7, right_x - x):
                c.drawString(x, note_y, line)
                note_y -= 10
        for line in wrap_text_width(f"资料来源：{exhibit.source}", FONT_REGULAR, 7, right_x - x):
            c.drawString(x, note_y - 4, line)
            note_y -= 10
        if exhibit.interpretation:
            y2 = note_y - 62
            c.setFillColor(Colors.TEXT)
            c.setFont(FONT_REGULAR, 10.5)
            for point in exhibit.interpretation:
                for line in wrap_text_width("• " + point, FONT_REGULAR, 10.5, right_x - x):
                    c.drawString(x, y2, line)
                    y2 -= 17
                y2 -= 6
        self._footer()

    def save(self) -> Path:
        self.c.save()
        return self.output_path


def create_bar_exhibit(categories: List[str], values: List[float], unit: str = "%") -> BytesIO:
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    colors = ["#111B3F", "#174A9C", "#26B6E8", "#A6B1BD"][: len(categories)]
    bars = ax.bar(categories, values, color=colors, width=0.56)
    max_value = max(values) if values else 1
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + max_value * 0.03, f"{value:g}{unit}", ha="center", va="bottom", fontsize=10)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", left=False, labelleft=False)
    ax.tick_params(axis="x", labelsize=10)
    ax.set_ylim(0, max_value * 1.25)
    fig.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=220, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    plt.close(fig)
    return buf


def build_demo(output: Path, page_size: str = "letter") -> Path:
    report = ConsultingReport(
        output,
        title="区域银行客户体验升级机会评估",
        subtitle="示例报告：用于验证交互式 Agent Skill 的字体、版式与图表能力",
        footer_label="示例报告",
        page_size=page_size,
    )
    report.cover(date="2026年4月", note="本文件为测试样例，数据为演示口径，不代表真实市场结论。")
    chapters = ["客户问题与决策目标", "体验差距与价值机会", "行动优先级与落地路径"]
    report.contents(chapters, page_numbers=[3, 4, 5])
    report.chapter_intro(
        "第一章",
        "客户问题与决策目标",
        [
            "本章用于明确客户的决策场景、目标读者和报告边界。正式报告应先回答客户需要做出的业务判断，再安排章节、展品和建议顺序。",
            "章节结构来自客户 brief 和已确认的数据来源计划，而不是套用固定模板。",
        ],
    )
    report.whitepaper_page(
        "正式报告应围绕客户决策展开，而不是展示内部分析过程。",
        [
            (
                "客户问题",
                [
                    "咨询报告的章节结构必须来自客户 brief。目标读者、使用场景、已有数据和决策问题不同，报告的章节颗粒度和证据顺序也应不同。",
                    "页面正文应以自然段落呈现事实、解释和业务含义，让客户顺畅理解判断依据。",
                ],
            ),
            (
                "交付方式",
                [
                    "正式生成前，Agent Skill 会先要求确认章节大纲和数据来源计划。只有当前置门槛完成后，才进入 storyline、展品和 PDF 生成。",
                    "最终 PDF 应使用客户可读的小标题、段落和图表解读，避免暴露内部推理标签。",
                ],
            ),
        ],
        footnote="注：本页用于验证 STKaitiSC 中文排版、页脚和白皮书式正文行距。",
    )
    chart = create_bar_exhibit(["响应速度", "个性化", "跨渠道一致性", "人工触点"], [64, 52, 47, 39])
    report.exhibit_page(
        Exhibit(
            number="1",
            title="示例展品：客户体验差距需要用直接标注的数据支撑，而不是仅凭判断描述。",
            subtitle="受访客户认为最需要改善的体验维度（演示数据，%）",
            source="演示数据；实际报告需替换为客户资料或公开来源",
            chart=chart,
            notes="注：本图为测试用途，数值仅用于版式和图表可读性验证。",
            interpretation=["图表必须包含标题、单位、注释和来源。", "未确认来源的数据不能作为最终报告结论。"],
        )
    )
    return report.save()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate consulting report PDFs.")
    parser.add_argument("--demo", action="store_true", help="Generate a small demo report.")
    parser.add_argument("--output", default="outputs/consulting-report/demo/final/report.pdf")
    parser.add_argument("--page-size", choices=["letter", "a4"], default="letter")
    args = parser.parse_args()

    if args.demo:
        output = build_demo(Path(args.output), page_size=args.page_size)
        print(f"Report saved to: {output}")
        return 0

    print("Import this module from a project-specific report script, or run with --demo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
