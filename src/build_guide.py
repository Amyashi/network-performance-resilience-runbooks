"""Build the Windows 11 Pro and Home network runbooks."""

from __future__ import annotations

import math
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfdoc import PDFString
from reportlab.pdfbase.pdfmetrics import Font
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]

PAGE_W, PAGE_H = landscape(letter)
TOTAL_PAGES = 32
VERSION = "1.0.1"
RELEASE_DATE_LONG = "30 July 2026"
RELEASE_DATE_SHORT = "30 Jul 2026"

NAVY = HexColor("#102A43")
NAVY_2 = HexColor("#173F5F")
INK = HexColor("#243B53")
SLATE = HexColor("#52667A")
MUTED = HexColor("#718096")
TEAL = HexColor("#0F9D8A")
TEAL_DARK = HexColor("#08786A")
TEAL_PALE = HexColor("#E8F7F4")
BLUE = HexColor("#2F6FED")
BLUE_PALE = HexColor("#ECF3FF")
GREEN = HexColor("#177C62")
GREEN_PALE = HexColor("#E9F7F1")
AMBER = HexColor("#B66A00")
AMBER_PALE = HexColor("#FFF5DF")
RED = HexColor("#B42318")
RED_PALE = HexColor("#FDECEA")
PURPLE = HexColor("#6F4AA8")
PURPLE_PALE = HexColor("#F2ECFA")
PAPER = HexColor("#F7F9FC")
LINE = HexColor("#D9E2EC")
CODE_BG = HexColor("#102B3F")
CODE_INK = HexColor("#D9F4F0")
WHITE = white


LABELS = {
    "PROVEN BASELINE": (TEAL_DARK, TEAL_PALE),
    "FIELD VERIFIED": (GREEN, GREEN_PALE),
    "CONDITIONAL CHANGE": (AMBER, AMBER_PALE),
    "CONTROLLED EXPERIMENT": (PURPLE, PURPLE_PALE),
    "AVOID": (RED, RED_PALE),
    "AMY-UNTESTED": (PURPLE, PURPLE_PALE),
}


def normalize_pdf_text(value: str) -> str:
    """Keep punctuation portable, extractable, and searchable across PDF readers."""
    return (
        value
        .replace(" — ", " - ")
        .replace("—", " - ")
        .replace(" – ", " - ")
        .replace("–", "-")
        .replace("‐", "-")
        .replace("‑", "-")
        .replace("‒", "-")
        .replace("−", "-")
        .replace("→", "->")
        .replace("≈", "~")
        .replace("≥", ">=")
    )


def register_fonts() -> None:
    """Register portable aliases backed by the standard PDF Base 14 fonts."""
    fonts = {
        "Segoe": "Helvetica",
        "Segoe-Bold": "Helvetica-Bold",
        "Segoe-Italic": "Helvetica-Oblique",
        "Segoe-Light": "Helvetica",
        "Consolas": "Courier",
        "Consolas-Bold": "Courier-Bold",
    }
    for name, face_name in fonts.items():
        try:
            pdfmetrics.getFont(name)
        except KeyError:
            pdfmetrics.registerFont(Font(name, face_name, "WinAnsiEncoding"))


def rr(c: canvas.Canvas, x: float, y: float, w: float, h: float, r: float,
       fill: Color, stroke: Color | None = None, sw: float = 0.8) -> None:
    c.setFillColor(fill)
    if stroke is None:
        c.setStrokeColor(fill)
    else:
        c.setStrokeColor(stroke)
    c.setLineWidth(sw)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1)


def text_width(text: str, font: str, size: float) -> float:
    return pdfmetrics.stringWidth(text, font, size)


def wrap(text: str, width: float, font: str, size: float) -> list[str]:
    if text == "":
        return [""]
    lines: list[str] = []
    for raw in text.splitlines() or [""]:
        if raw == "":
            lines.append("")
            continue
        words = raw.split()
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if text_width(candidate, font, size) <= width:
                current = candidate
            elif current:
                lines.append(current)
                current = word
            else:
                # Long commands/URLs get character-wrapped without shrinking the page.
                part = ""
                for ch in word:
                    if text_width(part + ch, font, size) <= width:
                        part += ch
                    else:
                        if part:
                            lines.append(part)
                        part = ch
                current = part
        if current:
            lines.append(current)
    return lines


class Guide:
    def __init__(
        self,
        path: Path,
        *,
        edition: str = "Pro",
        title: str | None = None,
        footer_title: str | None = None,
        subject: str | None = None,
        keywords: str | None = None,
        total_pages: int = TOTAL_PAGES,
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(
            str(path),
            pagesize=(PAGE_W, PAGE_H),
            pageCompression=1,
            invariant=1,
        )
        for method_name in ("drawString", "drawCentredString", "drawRightString"):
            original = getattr(self.c, method_name)

            def normalized_draw(x, y, text, *args, _original=original, **kwargs):
                return _original(x, y, normalize_pdf_text(str(text)), *args, **kwargs)

            setattr(self.c, method_name, normalized_draw)
        self.edition = edition
        self.title = title or f"Windows 11 {edition} Wired Network Performance & Resilience Runbook"
        self.footer_title = footer_title or self.title
        self.total_pages = total_pages
        self.c.setTitle(self.title)
        self.c.setAuthor("Amyashi")
        self.c.setCreator("Amyashi network-performance-resilience-runbooks build system")
        self.c.setSubject(subject or (
            "Implementation-first Windows wired-network baseline, multi-gigabit validation, "
            "latency testing, and failover runbook"
        ))
        self.c.setKeywords(keywords or (
            "Windows 11, Ethernet, iPerf3, PsPing, 2 Gbps, 5 Gbps, 10 Gbps, "
            "Intel Ethernet, eero SQM, failover"
        ))
        self.c._doc.Catalog.Lang = PDFString("en-US")
        self.page_no = 0
        self.overflows: list[str] = []

    def add_bookmark(self, title: str) -> None:
        key = f"page-{self.page_no}"
        self.c.bookmarkPage(key)
        self.c.addOutlineEntry(normalize_pdf_text(title), key, level=0, closed=False)

    def begin(self, title: str, section: str, label: str | None = None,
              subtitle: str | None = None, appendix: bool = False) -> None:
        self.page_no += 1
        c = self.c
        self.add_bookmark(f"{section}: {title}")
        c.setFillColor(PURPLE_PALE if appendix else PAPER)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        c.setFillColor(PURPLE if appendix else TEAL)
        c.rect(0, PAGE_H - 7, PAGE_W, 7, fill=1, stroke=0)
        c.setFont("Segoe-Bold", 7.2)
        c.setFillColor(PURPLE if appendix else TEAL_DARK)
        c.drawString(40, PAGE_H - 29, section.upper())
        c.setFont("Segoe-Bold", 20)
        c.setFillColor(NAVY)
        c.drawString(40, PAGE_H - 55, title)
        if subtitle:
            c.setFont("Segoe", 8.5)
            c.setFillColor(SLATE)
            c.drawString(40, PAGE_H - 71, subtitle)
        if label:
            self.badge(label, PAGE_W - 40, PAGE_H - 43, align="right")
        if appendix:
            c.setFont("Segoe-Bold", 7.2)
            c.setFillColor(PURPLE)
            c.drawRightString(PAGE_W - 40, PAGE_H - 69, "DOCUMENTATION-BACKED / NOT FIELD-TESTED BY AMY")
        self.footer()

    def footer(self) -> None:
        c = self.c
        c.setStrokeColor(LINE)
        c.setLineWidth(0.7)
        c.line(40, 28, PAGE_W - 40, 28)
        c.setFont("Segoe", 6.8)
        c.setFillColor(MUTED)
        c.drawString(40, 16, f"{self.footer_title}  |  v{VERSION}  |  {RELEASE_DATE_SHORT}")
        c.drawRightString(PAGE_W - 40, 16, f"{self.page_no} / {self.total_pages}")

    def badge(self, label: str, x: float, y: float, align: str = "left",
              font_size: float = 6.7) -> tuple[float, float]:
        fg, bg = LABELS.get(label, (NAVY, BLUE_PALE))
        w = text_width(label, "Segoe-Bold", font_size) + 18
        h = 17
        bx = x - w if align == "right" else x
        rr(self.c, bx, y - h / 2, w, h, 8.5, bg, fg, 0.55)
        self.c.setFont("Segoe-Bold", font_size)
        self.c.setFillColor(fg)
        self.c.drawCentredString(bx + w / 2, y - 2.4, label)
        return bx, w

    def paragraph(self, text: str, x: float, top: float, width: float,
                  font: str = "Segoe", size: float = 8.2, leading: float | None = None,
                  color: Color = INK) -> float:
        leading = leading or size * 1.3
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        y = top
        for line in wrap(text, width, font, size):
            self.c.drawString(x, y - size, line)
            y -= leading
        return y

    def blocks(self, blocks: list[dict], x: float, top: float, width: float,
               bottom: float, page_tag: str) -> float:
        y = top
        for b in blocks:
            kind = b.get("type", "p")
            if kind == "gap":
                y -= b.get("h", 5)
                continue
            if kind == "rule":
                y -= 3
                self.c.setStrokeColor(LINE)
                self.c.line(x, y, x + width, y)
                y -= 7
                continue
            if kind == "label":
                self.c.setFont("Segoe-Bold", b.get("size", 7.2))
                self.c.setFillColor(b.get("color", TEAL_DARK))
                self.c.drawString(x, y - b.get("size", 7.2), b["text"].upper())
                y -= b.get("leading", 13)
                continue
            if kind == "p":
                y = self.paragraph(
                    b["text"], x, y, width, b.get("font", "Segoe"),
                    b.get("size", 8.0), b.get("leading", None), b.get("color", INK)
                )
                y -= b.get("after", 4)
                continue
            if kind in {"bullet", "step"}:
                size = b.get("size", 7.9)
                leading = b.get("leading", 10.4)
                bullet_w = 14 if kind == "bullet" else 20
                marker = "•" if kind == "bullet" else str(b.get("n", "")) + "."
                lines = wrap(b["text"], width - bullet_w, "Segoe", size)
                self.c.setFillColor(b.get("marker_color", TEAL_DARK))
                self.c.setFont("Segoe-Bold", size)
                self.c.drawString(x, y - size, marker)
                self.c.setFillColor(b.get("color", INK))
                self.c.setFont("Segoe", size)
                for i, line in enumerate(lines):
                    self.c.drawString(x + bullet_w, y - size - i * leading, line)
                y -= len(lines) * leading + b.get("after", 3)
                continue
            if kind == "code":
                size = b.get("size", 6.9)
                leading = b.get("leading", 9.0)
                pad = 8
                all_lines: list[str] = []
                for raw in b["text"].splitlines():
                    all_lines.extend(wrap(raw, width - pad * 2, "Consolas", size))
                h = max(24, len(all_lines) * leading + 11)
                rr(self.c, x, y - h, width, h, 5, b.get("fill", CODE_BG), None)
                self.c.setFillColor(b.get("color", CODE_INK))
                self.c.setFont("Consolas", size)
                ty = y - 9
                for line in all_lines:
                    self.c.drawString(x + pad, ty - size, line)
                    ty -= leading
                y -= h + b.get("after", 6)
                continue
            if kind == "check":
                size = b.get("size", 7.8)
                lines = wrap(b["text"], width - 20, "Segoe", size)
                self.c.setStrokeColor(b.get("color", TEAL_DARK))
                self.c.rect(x, y - 11, 8, 8, fill=0, stroke=1)
                self.c.setFont("Segoe", size)
                self.c.setFillColor(INK)
                for i, line in enumerate(lines):
                    self.c.drawString(x + 17, y - size - i * 10.2, line)
                y -= len(lines) * 10.2 + 3
                continue
            raise ValueError(f"Unknown block type: {kind}")
        if y < bottom:
            self.overflows.append(f"{page_tag}: content bottom {y:.1f} < {bottom:.1f}")
        return y

    def card(self, x: float, top: float, w: float, h: float, title: str,
             blocks: list[dict], label: str | None = None, fill: Color = WHITE,
             stroke: Color = LINE, title_color: Color = NAVY,
             page_tag: str = "") -> None:
        bottom = top - h
        rr(self.c, x, bottom, w, h, 10, fill, stroke, 0.7)
        self.c.setFont("Segoe-Bold", 10.0)
        self.c.setFillColor(title_color)
        self.c.drawString(x + 14, top - 20, title)
        if label:
            self.badge(label, x + w - 12, top - 16, align="right", font_size=5.9)
        self.blocks(blocks, x + 14, top - 35, w - 28, bottom + 10, page_tag or title)

    def metric(self, x: float, y: float, w: float, h: float, number: str,
               caption: str, fill: Color = TEAL_PALE, color: Color = TEAL_DARK) -> None:
        rr(self.c, x, y, w, h, 9, fill, None)
        self.c.setFillColor(color)
        self.c.setFont("Segoe-Bold", 21)
        self.c.drawString(x + 13, y + h - 28, number)
        self.c.setFont("Segoe", 7.6)
        self.c.setFillColor(INK)
        for i, line in enumerate(wrap(caption, w - 26, "Segoe", 7.6)):
            self.c.drawString(x + 13, y + h - 44 - i * 9.4, line)

    def action_strip(self, items: list[tuple[str, str, str]], y: float = 42,
                     appendix: bool = False) -> None:
        x = 40
        total_w = PAGE_W - 80
        gap = 7
        w = (total_w - gap * (len(items) - 1)) / len(items)
        accent = PURPLE if appendix else TEAL_DARK
        for i, (head, text, status) in enumerate(items):
            bx = x + i * (w + gap)
            fill = {
                "pass": GREEN_PALE,
                "warn": AMBER_PALE,
                "fail": RED_PALE,
                "info": BLUE_PALE,
                "purple": PURPLE_PALE,
            }.get(status, WHITE)
            rr(self.c, bx, y, w, 56, 8, fill, LINE, 0.6)
            self.c.setFillColor(accent)
            self.c.setFont("Segoe-Bold", 6.3)
            self.c.drawString(bx + 9, y + 41, head.upper())
            self.paragraph(text, bx + 9, y + 34, w - 18, size=6.5, leading=8.1)

    def next(self) -> None:
        self.c.showPage()

    def finish(self) -> None:
        if self.page_no != self.total_pages:
            raise RuntimeError(f"Expected {self.total_pages} pages, built {self.page_no}")
        if self.overflows:
            raise RuntimeError("Layout overflow:\n" + "\n".join(self.overflows))
        self.c.save()


def b(text: str, **kwargs) -> dict:
    return {"type": "bullet", "text": text, **kwargs}


def p(text: str, **kwargs) -> dict:
    return {"type": "p", "text": text, **kwargs}


def s(n: int, text: str, **kwargs) -> dict:
    return {"type": "step", "n": n, "text": text, **kwargs}


def code(text: str, **kwargs) -> dict:
    return {"type": "code", "text": text, **kwargs}


def label(text: str, **kwargs) -> dict:
    return {"type": "label", "text": text, **kwargs}


def check(text: str, **kwargs) -> dict:
    return {"type": "check", "text": text, **kwargs}


def cover(g: Guide) -> None:
    g.page_no += 1
    c = g.c
    g.add_bookmark("Cover")
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, 0, 13, PAGE_H, fill=1, stroke=0)
    rr(c, 40, 56, PAGE_W - 80, PAGE_H - 96, 22, NAVY, NAVY)
    c.setFillColor(HexColor("#174466"))
    c.circle(PAGE_W - 128, PAGE_H - 145, 76, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.circle(PAGE_W - 128, PAGE_H - 145, 49, fill=1, stroke=0)
    c.setFont("Segoe-Light", 43)
    c.setFillColor(WHITE)
    c.drawCentredString(PAGE_W - 128, PAGE_H - 160, "10")
    c.setFont("Segoe-Bold", 7.5)
    c.drawCentredString(PAGE_W - 128, PAGE_H - 180, "GbE SCALE")
    c.setFont("Segoe-Bold", 8)
    c.setFillColor(TEAL)
    c.drawString(74, PAGE_H - 105, f"IMPLEMENTATION-FIRST WINDOWS 11 {g.edition.upper()} GUIDE")
    c.setFont("Segoe-Bold", 29)
    c.setFillColor(WHITE)
    c.drawString(74, PAGE_H - 157, "Windows Wired Network")
    c.drawString(74, PAGE_H - 194, "Performance & Resilience")
    c.drawString(74, PAGE_H - 231, "Runbook")
    c.setFont("Segoe", 11)
    c.setFillColor(HexColor("#D5E6F3"))
    c.drawString(76, PAGE_H - 264, "Driver baseline  •  low-latency configuration  •  symmetric")
    c.drawString(76, PAGE_H - 282, "multi-gigabit validation  •  deterministic host failover")
    rr(c, 74, 155, 456, 78, 12, HexColor("#163D5C"), HexColor("#2B5978"), 0.8)
    c.setFont("Segoe-Bold", 8.2)
    c.setFillColor(TEAL)
    c.drawString(91, 211, "EVIDENCE BOUNDARY")
    c.setFont("Segoe", 9.2)
    c.setFillColor(WHITE)
    c.drawString(91, 190, "Field-tested at 2 Gbps up / 2 Gbps down")
    c.drawString(91, 173, "Scaling method to 5/5 and 10/10 is documentation-backed and Amy-untested")
    g.badge("FIELD VERIFIED", 74, 122)
    c.setFont("Segoe-Bold", 7.1)
    c.setFillColor(WHITE)
    c.drawString(188, 119, "AMY'S 2/2 GBPS RECORD")
    g.badge("AMY-UNTESTED", 346, 122)
    c.setFont("Segoe-Bold", 7.1)
    c.setFillColor(WHITE)
    c.drawString(452, 119, "5/5 + 10/10 APPENDIX")
    c.setFont("Segoe", 7.2)
    c.setFillColor(MUTED)
    c.drawString(40, 28, f"v{VERSION}  |  {RELEASE_DATE_LONG}  |  Built for repeatable measurement and safe rollback")
    c.drawRightString(PAGE_W - 40, 28, f"1 / {g.total_pages}")
    g.next()


def page_2(g: Guide) -> None:
    g.begin("Choose the correct path", "Start here", "PROVEN BASELINE",
            "Do not tune a healthy link before establishing what is actually failing.")
    x, top, gap = 40, 520, 12
    w = (PAGE_W - 80 - gap * 3) / 4
    cards = [
        ("1  VALIDATE", TEAL_PALE, [
            p("Use when the link feels slow but no configuration change is justified yet.", size=7.6),
            b("Capture the baseline package."),
            b("Pass the local gate."),
            b("Measure idle, one direction, then both."),
            b("Stop if the evidence already meets the target."),
        ]),
        ("2  REPAIR", BLUE_PALE, [
            p("Use for link drops, wrong negotiation, driver regression, or counter errors.", size=7.6),
            b("Restore a known-good driver."),
            b("Return advanced properties to defaults."),
            b("Replace one physical component at a time."),
            b("Revalidate locally before WAN testing."),
        ]),
        ("3  EXPERIMENT", PURPLE_PALE, [
            p("Use only for a named symptom and an A/B measurement.", size=7.6),
            b("Change one property."),
            b("Repeat the same workload three times."),
            b("Keep only a repeatable improvement."),
            b("Roll back neutral or worse results."),
        ]),
        ("4  FAILOVER", AMBER_PALE, [
            p("Use to prefer a primary path and test recovery to a secondary path.", size=7.6),
            b("Define failure domains."),
            b("Set interface metrics."),
            b("Expect existing TCP sessions to reset."),
            b("Do not call one shared ISP redundant."),
        ]),
    ]
    for i, (title, fill, blocks) in enumerate(cards):
        g.card(x + i * (w + gap), top, w, 214, title, blocks, fill=fill, page_tag=f"p2-{i}")
    g.card(40, 291, 435, 155, "Evidence labels used throughout", [
        p("PROVEN BASELINE — authoritative documentation and safe default behavior.", size=7.5),
        p("FIELD VERIFIED — observed in Amy's recorded 2/2 Gbps environment.", size=7.5),
        p("CONDITIONAL CHANGE — justified only by a named symptom or deployment need.", size=7.5),
        p("CONTROLLED EXPERIMENT — one-change A/B test; retain only after measured improvement.", size=7.5),
        p("AVOID — unsafe bulk changes, unmeasured folklore, or evidence-conflicting advice.", size=7.5),
    ], fill=WHITE, page_tag="p2-labels")
    g.card(487, 291, 265, 155, "Release integrity", [
        p("Use a PDF from the official tagged release and match it to the same-version Markdown companion.", size=7.7),
        p("Verify the file against outputs/SHA256SUMS.txt before relying on a downloaded copy.", size=7.7),
        p("Modified, unversioned, or checksum-mismatched copies are outside the supported release.", size=7.7),
    ], fill=BLUE_PALE, page_tag="p2-repo")
    g.action_strip([
        ("Start", "Run pages 4–5 before any change.", "info"),
        ("Restart", "None for reading or baseline capture.", "pass"),
        ("Pass", "The chosen path matches the observed symptom.", "pass"),
        ("Fail", "The path assumes a cause without evidence.", "fail"),
        ("Rollback", "Return to VALIDATE and capture evidence.", "warn"),
    ])
    g.next()


def page_3(g: Guide) -> None:
    g.begin("What Amy's 2/2 Gbps evidence proves", "Field record", "FIELD VERIFIED",
            "A bounded result, not a promise about every server, route, adapter, or future date.")
    g.metric(40, 379, 160, 111, "1.9", "Gbps upload and approximately 1.9 Gbps download in one simultaneous run.")
    g.metric(212, 379, 160, 111, "3.8", "Gbps simultaneous aggregate application throughput in that run.")
    g.metric(384, 379, 160, 111, "3.9", "Gbps best observed aggregate: about 2.0 up plus 1.9 down.")
    g.metric(556, 379, 196, 111, "0", "Adapter error/discard deltas in two documented counter checks.", GREEN_PALE, GREEN)
    g.card(40, 361, 348, 219, "Observed environment and test record", [
        b("Windows 11 wired client using an Intel Ethernet Controller I225-V."),
        b("eero edge and a Metronet symmetric 2 Gbps service path."),
        b("Separate upload and reverse-download iPerf3 sessions ran concurrently."),
        b("A documented receive run moved 33.5 GB in 150 seconds at about 1.92 Gbps average."),
        b("Gateway and Internet PsPing windows were used to separate local from WAN queuing."),
        b("Public endpoint performance varied; the strongest repeatable runs were retained as evidence."),
    ], fill=WHITE, page_tag="p3-record")
    g.card(404, 361, 348, 219, "The correct conclusion — and its limit", [
        label("Supported conclusion"),
        p("The observed path did not impose a 2 Gbps combined cap. It delivered near-line-rate traffic in both directions at the same time, consistent with full-duplex operation.", size=7.8),
        label("Not established"),
        b("Every public iPerf server can sustain the service rate."),
        b("Every retransmission came from Amy's LAN or adapter."),
        b("The same settings are optimal for another controller."),
        b("The host, router, media, or ISP can sustain 5/5 or 10/10."),
    ], fill=GREEN_PALE, page_tag="p3-limit")
    g.action_strip([
        ("Prerequisite", "Use the same evidence boundary when comparing future results.", "info"),
        ("Restart", "None.", "pass"),
        ("Pass", "Claims stay within the measured 2/2 path.", "pass"),
        ("Fail", "A result is generalized to untested hardware or speed.", "fail"),
        ("Recovery", "Relabel the claim and run the appendix protocol.", "warn"),
    ])
    g.next()


def page_4(g: Guide) -> None:
    g.begin("Safety package before any change", "Preparation", "PROVEN BASELINE",
            "Preserve access, capture state, and change only one variable at a time.")
    g.card(40, 520, 343, 270, "Before you touch a driver or adapter property", [
        check("Use a local administrator account; keep a second working sign-in if this PC is remote-managed."),
        check("Schedule a short outage window. An adapter restart ends active calls, transfers, VPNs, and remote sessions."),
        check("Download the intended OEM driver and confirm the exact device/OS match before removing anything."),
        check("Keep a second connection or local console available when changing the primary adapter."),
        check("Record the adapter name, hardware ID, driver version/date/provider, link speed, and every advanced property."),
        check("Capture idle gateway and Internet latency plus adapter counter values."),
        check("Name the symptom and the pass threshold before changing a setting."),
    ], fill=WHITE, page_tag="p4-before")
    g.card(397, 520, 355, 270, "The one-change protocol", [
        s(1, "Capture the before state and save the exact command/output."),
        s(2, "Apply one bounded change. Do not combine a driver, cable, MTU, and offload change."),
        s(3, "Allow the adapter to reset. Reboot Windows only when the procedure or installer requires it."),
        s(4, "Repeat the identical validation at least three times where throughput or latency varies."),
        s(5, "Keep the change only when the predeclared pass criterion is repeatable."),
        s(6, "If it fails, roll back first; collect new evidence only after basic connectivity returns."),
        {"type": "rule"},
        p("A restore point can help with system configuration, but it is not a reliable substitute for an exported driver, written settings, or a second access path.", size=7.4, color=SLATE),
    ], fill=BLUE_PALE, page_tag="p4-protocol")
    stop_blocks = [
        p("Stop immediately if the negotiated speed falls, the default gateway is unreachable, adapter errors/discards begin increasing, the PC becomes unreachable, or the correct rollback package is unavailable. Restore basic link state before continuing with performance tests.", size=8.4),
        p("Do not continue a stress test through overheating, driver resets, Event Viewer hardware errors, or sustained endpoint CPU saturation.", size=8.4, color=RED),
    ]
    if g.edition == "Home":
        stop_blocks.append(
            p("Home in S mode blocks ordinary non-Store iPerf3, PsPing, and vendor installers. Verify S mode before this runbook; leaving S mode is a one-way Windows change, so stop for an explicit owner decision.", size=6.8, color=RED)
        )
    g.card(40, 236, 712, 109, "Stop conditions", stop_blocks,
           fill=RED_PALE, stroke=HexColor("#F2B8B5"), page_tag="p4-stop")
    g.action_strip([
        ("Prerequisite", "Admin access, outage window, driver package, second path.", "info"),
        ("Restart", "Only when the specific change requires it.", "pass"),
        ("Pass", "One change is traceable to one result.", "pass"),
        ("Fail", "Access or baseline evidence is missing.", "fail"),
        ("Rollback", "Stop and restore connectivity before testing.", "warn"),
    ])
    g.next()


def page_5(g: Guide) -> None:
    g.begin("Capture a reusable Windows baseline", "Baseline", "PROVEN BASELINE",
            "Run in PowerShell. The first block is non-destructive; the output folder is in Documents.")
    g.card(40, 520, 456, 260, "1  Create the capture folder and record the adapter", [
        code(
            '$stamp = Get-Date -Format "yyyyMMdd-HHmmss"\n'
            '$dir = "$env:USERPROFILE\\Documents\\Network-Baseline-$stamp"\n'
            'New-Item -ItemType Directory -Path $dir | Out-Null\n'
            'Get-NetAdapter | Format-Table Name,InterfaceDescription,Status,LinkSpeed,MacAddress -Auto |\n'
            '  Out-File "$dir\\adapters.txt"\n'
            'Get-NetAdapterAdvancedProperty -Name "*" |\n'
            '  Format-Table Name,DisplayName,DisplayValue,RegistryKeyword,RegistryValue -Auto |\n'
            '  Out-File "$dir\\advanced-properties.txt"\n'
            'Get-NetAdapterStatistics -Name "*" | Format-List * |\n'
            '  Out-File "$dir\\adapter-statistics.txt"',
            size=6.35,
        ),
        p("If the adapter alias is not Ethernet, substitute the exact value returned by Get-NetAdapter on later pages.", size=7.2, color=SLATE),
    ], fill=WHITE, page_tag="p5-capture1")
    g.card(510, 520, 242, 260, "Record before each test set", [
        check("Date, time, and test location"),
        check("Windows build and power plan"),
        check("Adapter alias and link speed"),
        check("Driver provider/version/date"),
        check("Router/SQM state"),
        check("Server name/IP and route"),
        check("iPerf3 version and command"),
        check("Idle gateway + Internet latency"),
        check("Endpoint CPU and temperature"),
        check("Counter deltas after the run"),
    ], fill=TEAL_PALE, page_tag="p5-record")
    g.card(40, 252, 712, 147, "2  Capture routes, TCP state, RSS, IP configuration, and driver identity", [
        code(
            'Get-NetIPConfiguration | Format-List * | Out-File "$dir\\ip-configuration.txt"\n'
            'Get-NetIPInterface | Sort-Object AddressFamily,InterfaceMetric |\n'
            '  Format-Table ifIndex,InterfaceAlias,AddressFamily,AutomaticMetric,InterfaceMetric,NlMtu -Auto |\n'
            '  Out-File "$dir\\interface-metrics.txt"\n'
            'Get-NetAdapterRss -Name "*" | Format-List * | Out-File "$dir\\rss.txt"\n'
            'netsh interface tcp show global | Out-File "$dir\\tcp-global.txt"\n'
            'route print | Out-File "$dir\\routes.txt"\n'
            'Get-CimInstance Win32_PnPSignedDriver | Where-Object {$_.DeviceClass -eq "NET"} |\n'
            '  Select-Object DeviceName,DriverProviderName,DriverVersion,DriverDate,InfName |\n'
            '  Format-Table -Auto | Out-File "$dir\\network-drivers.txt"',
            size=5.95,
            leading=7.4,
        ),
    ], fill=BLUE_PALE, page_tag="p5-capture2")
    g.action_strip([
        ("Prerequisite", "PowerShell; administrator only for later mutations.", "info"),
        ("Restart", "None.", "pass"),
        ("Validate", "Open every output file; confirm it is not empty.", "info"),
        ("Pass", "Baseline can identify the exact adapter and restore values.", "pass"),
        ("If it fails", "Fix the alias/path; do not begin configuration work.", "fail"),
    ])
    g.next()


def page_6(g: Guide) -> None:
    g.begin("Driver selection, install, and rollback", "Windows driver", "PROVEN BASELINE",
            "Use the motherboard/system OEM package first; generic Intel packages are a fallback, not an automatic upgrade.")
    g.card(40, 520, 310, 288, "Select and stage the package", [
        s(1, "Identify the exact controller and current INF from the baseline."),
        s(2, "Check the computer or motherboard support page for the matching Windows release."),
        s(3, "Compare the contained driver version, provider, compatible hardware IDs, and INF. A later download-page or package date is not proof of a newer device driver."),
        s(4, "Read the release notes. Install only for a relevant fix, support need, or measured regression."),
        s(5, "Use Intel's generic Windows package only when the OEM package is unavailable/inadequate and the Intel OS matrix includes the exact retail adapter."),
        s(6, "Do not use third-party driver-updater utilities."),
        label("Optional export"),
        code('pnputil /enum-drivers /class Net\npnputil /export-driver oem##.inf "$dir\\DriverBackup"', size=6.7),
        p("Replace oem##.inf with the published name shown for the active package.", size=7.0, color=SLATE),
    ], fill=WHITE, page_tag="p6-select")
    g.card(364, 520, 388, 288, "Install without forcing an unnecessary reboot", [
        label("Vendor installer"),
        s(1, "Close network-dependent work and run the signed OEM installer as administrator."),
        s(2, "Allow the adapter to reset. Do not interrupt a firmware component if the package explicitly includes one."),
        s(3, "Restart Windows only if the installer requests it, the device remains in a pending state, or link behavior is inconsistent after the adapter reset."),
        label("INF package alternative"),
        code('pnputil /add-driver ".\\DriverFolder\\*.inf" /subdirs /install', size=6.7),
        p("PnPUtil selects the highest-ranked matching package; a numerically newer file is not automatically preferred.", size=7.2),
        label("Do not"),
        p("Do not delete the old package or add /reboot until the replacement has been validated and local access is assured.", size=7.2, color=RED),
    ], fill=BLUE_PALE, page_tag="p6-install")
    g.action_strip([
        ("Restart", "Only if prompted, pending, or the adapter cannot recover.", "warn"),
        ("Validate", "Driver identity, expected link speed, gateway, DNS, counters.", "info"),
        ("Pass", "Correct package; stable link; no new error/discard deltas.", "pass"),
        ("Fail", "Wrong speed, resets, errors, or loss of connectivity.", "fail"),
        ("Rollback", "Device Manager > Driver > Roll Back, or reinstall exported/OEM INF.", "warn"),
    ])
    g.next()


def page_pcie_install(g: Guide) -> None:
    g.begin("Install or replace a PCIe Ethernet adapter safely", "Adapter hardware", "CONDITIONAL CHANGE",
            "Use for 2.5, 5, or 10 GbE. Enumeration comes before driver or firmware work.")
    g.card(40, 520, 342, 396, "Preflight before the shutdown", [
        label("Identify the exact hardware"),
        s(1, "Verify the complete retail/OEM adapter, supported Windows release, supplied bracket, and return path. A controller name on a marketplace listing is not proof of a supported retail card."),
        s(2, "Read the exact system or motherboard revision manual. Confirm the slot's electrical width, generation, lane sharing, clearance, and airflow - not only connector length."),
        s(3, "Stage the signed OEM/retail driver and rollback package. Keep the working onboard/old adapter enabled and its driver intact; leave the production cable there until the new card enumerates."),
        s(4, "Check BitLocker or Device Encryption and retrieve the 48-digit recovery key from a second device or approved store before opening the case."),
        code("manage-bde -status C:", size=6.6),
        p("For a planned firmware, UEFI, option-ROM, or other measured-boot change, follow Microsoft/OEM suspend guidance and plan immediate resume. Do not disable TPM or Secure Boot as a shortcut.", size=6.9, color=SLATE),
        s(5, "Close work, perform a full shutdown, switch the PSU off, unplug AC power, and use ESD precautions. Do not hot-plug unless both the platform and adapter explicitly support it."),
    ], fill=WHITE, page_tag="pcie-preflight")
    g.card(396, 520, 356, 396, "Install, enumerate, then validate", [
        label("Physical and enumeration gates"),
        s(1, "Use the correct bracket. Seat the card straight and evenly; no exposed contacts, PCB flex, case contact, modified metal, or force. Secure it snugly."),
        s(2, "Leave the production cable on the known-good adapter. Power on and establish a normal firmware/Windows boot first."),
        s(3, "In Device Manager and PowerShell, confirm a new PCIe/PnP network device exists before installing a driver or running a firmware updater."),
        code("Get-PnpDevice -Class Net | Sort-Object Status,FriendlyName\nGet-NetAdapter | Format-Table Name,Status,LinkSpeed,InterfaceDescription -Auto", size=5.8),
        s(4, "If absent, shut down and remove AC power. Inspect and reseat once, then try only a slot supported by the exact manual. If still absent, test/return the card; do not force firmware or arbitrary BIOS settings."),
        s(5, "After enumeration, install the matching signed driver. Let the adapter reset. Restart Windows only if prompted, left pending, or the adapter does not recover cleanly."),
        s(6, "Move the cable. Verify device/driver identity, negotiated speed, gateway, DNS, clean counters, a local throughput gate, one restart, and one cold start before retiring the old path."),
        s(7, "Resume BitLocker protection if it was suspended and verify Protection On. Stop and use Microsoft/OEM recovery if entering the known key does not restore a normal boot."),
        label("Amy's bounded field result"),
        p("A later I226-based card install negotiated 2.5 Gbps and reached approximately 2 Gbps in Speedtest. Amy's later I226-T1 record showed device driver 2.1.5.7 dated 2025-09-03 inside Intel package 31.2.2; those are different version identities. The adapter reset and reconnected without a Windows reboot. These are bounded system/path records.", size=6.35, color=TEAL_DARK),
    ], fill=BLUE_PALE, page_tag="pcie-install")
    g.action_strip([
        ("Prerequisite", "Exact manual, signed driver, recovery key, old path.", "info"),
        ("Power", "Full shutdown and AC removal for hardware work.", "warn"),
        ("Pass", "Enumerated, correct link/driver, clean counters and boots.", "pass"),
        ("Fail", "No PnP device, POST/power fault, recovery loop, or card flex.", "fail"),
        ("Rollback", "Power off; remove card; restore old path; resume encryption.", "warn"),
    ])
    g.next()


def page_7(g: Guide) -> None:
    g.begin("Evidence-backed Ethernet adapter baseline", "Adapter properties", "PROVEN BASELINE",
            "Property names vary by driver. Record the displayed value before changing anything.")
    g.card(40, 520, 435, 341, "Recommended starting state", [
        p("Speed & Duplex — Auto Negotiation. A forced speed can break negotiation and does not create bandwidth.", size=7.45),
        p("Receive Side Scaling (RSS) — Enabled. It distributes receive processing across available processors.", size=7.45),
        p("TCP/UDP checksum offloads — Enabled. Preserve hardware offload unless a documented defect is isolated.", size=7.45),
        p("Large Send Offload v2 — Enabled/default. Do not disable it merely because a tuning list says so.", size=7.45),
        p("Jumbo Packet / MTU — Standard Ethernet default. Every hop and endpoint must agree before an isolated-LAN experiment.", size=7.45),
        p("Interrupt Moderation — Driver default/adaptive. Lower latency can cost interrupt and CPU load.", size=7.45),
        p("Flow Control — Driver/OEM default. Do not force a state without a switch and workload reason.", size=7.45),
        p("Receive/Transmit buffers — Default. Increase only to test a CPU/burst/drop symptom.", size=7.45),
        p("Energy Efficient Ethernet — Default. Disable only for repeatable idle/resume or link-flap evidence.", size=7.45),
        p("Priority & VLAN — Disabled unless the network explicitly uses 802.1p/VLAN tagging.", size=7.45),
    ], fill=WHITE, page_tag="p7-state")
    g.card(489, 520, 263, 341, "Exact change path", [
        s(1, "Open Device Manager."),
        s(2, "Expand Network adapters."),
        s(3, "Open the exact wired adapter."),
        s(4, "Select Advanced."),
        s(5, "Capture a screenshot or baseline export."),
        s(6, "Change one property and select OK."),
        s(7, "Allow the adapter to disconnect/reconnect."),
        s(8, "Run the local validation block."),
        {"type": "rule"},
        code('Get-NetAdapter -Name "Ethernet"\nGet-NetAdapterRss -Name "Ethernet"\nGet-NetAdapterStatistics -Name "Ethernet"', size=6.5),
        p("Use PowerShell mutation only after you have recorded the exact vendor-specific property/value names.", size=7.1, color=SLATE),
    ], fill=TEAL_PALE, page_tag="p7-path")
    g.action_strip([
        ("Restart", "Adapter reset is normal; Windows reboot usually unnecessary.", "pass"),
        ("Validate", "Expected link speed, RSS enabled, gateway ping, counter deltas.", "info"),
        ("Pass", "Stable link and equal/better repeated result.", "pass"),
        ("Fail", "Negotiation falls, CPU spikes, drops/errors increase.", "fail"),
        ("Rollback", "Restore the captured display value and reset the adapter.", "warn"),
    ])
    g.next()


def page_8(g: Guide) -> None:
    g.begin("Latency and stability experiments", "Adapter properties", "CONTROLLED EXPERIMENT",
            "Each change needs a symptom, an A/B test, and a rollback. Neutral results return to baseline.")
    g.card(40, 520, 346, 316, "Conditionally test — one at a time", [
        label("Energy Efficient Ethernet: Off"),
        p("Only for repeatable idle/resume disconnects, renegotiation, or latency spikes that disappear when disabled.", size=7.35),
        label("Interrupt Moderation: Low / Off"),
        p("Only when low-latency packet handling matters and endpoint CPU/interrupt load remains acceptable.", size=7.35),
        label("Receive / Transmit buffers: Higher"),
        p("Only when counters or traces show drops under bursts and CPU/memory headroom exists.", size=7.35),
        label("RSS queues / processors: Higher"),
        p("Only when receive CPU is concentrated and the driver/CPU topology supports more queues.", size=7.35),
        label("Flow Control: Alternate state"),
        p("Only with a known switch configuration and a specific loss/pausing hypothesis.", size=7.35),
    ], fill=PURPLE_PALE, page_tag="p8-test")
    g.card(400, 520, 352, 316, "Avoid cargo-cult tuning", [
        b("Disabling every checksum/segmentation offload."),
        b("Forcing Speed & Duplex for ordinary production use."),
        b("Enabling jumbo frames on an Internet path or on only one device."),
        b("Applying registry TCP 'gaming' packs or undocumented timer changes."),
        b("Maxing buffers, RSS queues, or interrupt rates without measuring CPU and counters."),
        b("Changing five properties and treating one speed test as proof."),
        b("Keeping a change because a synthetic benchmark improved while latency, stability, or normal workloads regressed."),
        {"type": "rule"},
        p("A lower single ping is not sufficient. Compare the latency distribution, throughput, CPU load, adapter counters, and the real workload.", size=7.6, color=RED),
    ], fill=RED_PALE, stroke=HexColor("#F2B8B5"), page_tag="p8-avoid")
    g.card(40, 192, 712, 82, "Historical Amy configuration - field record, not a baseline", [
        p("Before the successful Pro failover observation, Amy's recorded adapter state included Auto Negotiation and standard MTU; EEE off; Interrupt Moderation on with Low rate when Adaptive was unavailable; Flow Control off; ARP/NS, LSOv2, and TCP/UDP checksum offloads off; Priority/VLAN and unused wake features off; and Idle Power Down Restriction on when exposed. The bundle was not isolated or causally validated. Do not reproduce it wholesale; keep the defaults-first baseline and test only one justified change at a time.", size=6.55, leading=8.1, color=SLATE),
    ], fill=AMBER_PALE, page_tag="p8-history")
    g.action_strip([
        ("Prerequisite", "Named symptom + saved baseline + identical workload.", "info"),
        ("Restart", "Adapter reset usually enough; note the short outage.", "warn"),
        ("Pass", "Three-run result improves without a new regression.", "pass"),
        ("Fail", "Neutral, inconsistent, hotter, higher CPU, or less stable.", "fail"),
        ("Rollback", "Restore the one changed property immediately.", "warn"),
    ])
    g.next()


def page_9(g: Guide) -> None:
    g.begin("Windows network stack and update behavior", "Windows 11", "CONDITIONAL CHANGE",
            "Inspect first. Resets and update controls are recovery/maintenance tools, not speed tweaks.")
    g.card(40, 520, 350, 292, "TCP state — preserve normal behavior", [
        label("Inspect"),
        code('netsh interface tcp show global\nGet-NetTCPSetting | Format-Table SettingName,AutoTuningLevelLocal,ScalingHeuristics', size=6.5),
        p("Receive Window Auto-Tuning should normally remain Normal. Do not disable it to 'lower ping'; high-bandwidth, higher-latency paths need window growth.", size=7.4),
        label("Conditional restore"),
        code('netsh interface tcp set global autotuninglevel=normal', size=6.7),
        p("Use only if the inspection shows a non-normal state you did not intentionally set. Re-run the same test; no reboot is normally required.", size=7.25),
        label("Recovery only"),
        code('netsh winsock reset\nnetsh int ip reset "$dir\\ip-reset.log"', size=6.7),
        p("These resets can remove custom networking state. They require a Windows restart and do not belong in routine performance tuning.", size=7.25, color=RED),
    ], fill=WHITE, page_tag="p9-tcp")
    if g.edition == "Home":
        update_blocks = [
            label("Home-safe default"),
            p("Leave Windows driver delivery enabled and keep normal security/cumulative servicing active. Prefer the PC or motherboard maker's signed package when a documented problem or support matrix calls for it.", size=7.35),
            label("If a network driver regresses"),
            s(1, "Stage the known-good signed OEM package before making another change."),
            s(2, "Use Device Manager > adapter > Properties > Driver > Roll Back Driver when available."),
            s(3, "Pause updates only long enough to prevent immediate reinstallation; document the bad version, then resume servicing."),
            label("Edition boundary"),
            p("Windows 11 Home has no supported Local Group Policy path for “Do not include drivers with Windows Updates.” Do not install fake gpedit packages or undocumented registry packs to imitate it.", size=7.2, color=RED),
        ]
    else:
        update_blocks = [
            p("Leave Windows driver delivery enabled; install required Windows security/cumulative updates. Prefer the OEM network driver when a specific problem or support matrix calls for it.", size=7.4),
            label("Pro / Education / Enterprise - conditional"),
            s(1, "Stage a known-good OEM package, test rollback, and assign review of future driver/security releases.", size=7.05),
            s(2, "Open gpedit.msc > Computer Configuration > Administrative Templates > Windows Components > Windows Update > Manage updates offered from Windows Update.", size=7.0),
            s(3, "Open “Do not include drivers with Windows Updates,” select Enabled, then Apply > OK.", size=7.0),
            code(
                'gpupdate /force\n'
                'gpresult /scope computer /h "$env:USERPROFILE\\Documents\\network-policy.html"',
                size=5.95,
            ),
            p("Validate the report lists the enabled policy. No reboot is normally required. Rollback: set it Not Configured, Apply > OK, run gpupdate /force, and restore normal driver servicing.", size=6.8),
            label("After a bad update"),
            p("Roll back the driver first; pause only long enough to prevent immediate reinstallation, document the version, then resume normal servicing.", size=7.1),
        ]
    g.card(404, 520, 348, 292, "Driver updates — choose one maintenance model",
           update_blocks, fill=AMBER_PALE, page_tag="p9-update")
    g.action_strip([
        ("Restart", "TCP reset: yes. Autotuning/policy inspection: no.", "warn"),
        ("Validate", "TCP state, link, DNS, gateway, test repeatability.", "info"),
        ("Pass", "Known state; updates still have an intentional owner/path.", "pass"),
        ("Fail", "Reset removes required configuration or driver reappears.", "fail"),
        ("Rollback", "Restore default servicing; reinstall known-good OEM driver.", "warn"),
    ])
    g.next()


def page_10(g: Guide) -> None:
    g.begin("Deterministic primary and secondary interfaces", "Host path preference", "CONDITIONAL CHANGE",
            "Interface metrics select new routes; they do not migrate an established TCP session.")
    g.card(40, 520, 382, 295, "Set an explicit preference", [
        label("Inspect both address families"),
        code('Get-NetIPInterface | Sort-Object AddressFamily,InterfaceMetric |\n  Format-Table ifIndex,InterfaceAlias,AddressFamily,AutomaticMetric,InterfaceMetric,ConnectionState -Auto', size=6.3),
        s(1, "Choose the real primary and secondary adapter aliases."),
        s(2, "Set the primary to a lower metric and the secondary to a higher metric."),
        code(
            'Set-NetIPInterface -InterfaceAlias "Ethernet" -AddressFamily IPv4 -AutomaticMetric Disabled -InterfaceMetric 10\n'
            'Set-NetIPInterface -InterfaceAlias "Secondary" -AddressFamily IPv4 -AutomaticMetric Disabled -InterfaceMetric 50\n'
            'Set-NetIPInterface -InterfaceAlias "Ethernet" -AddressFamily IPv6 -AutomaticMetric Disabled -InterfaceMetric 10\n'
            'Set-NetIPInterface -InterfaceAlias "Secondary" -AddressFamily IPv6 -AutomaticMetric Disabled -InterfaceMetric 50',
            size=5.8,
        ),
        p("Use values that preserve the ordering; the exact numbers have no inherent performance benefit.", size=7.2, color=SLATE),
    ], fill=WHITE, page_tag="p10-set")
    g.card(436, 520, 316, 295, "Validate route choice", [
        code('Test-NetConnection 1.1.1.1 -DiagnoseRouting -InformationLevel Detailed\nroute print', size=6.25),
        b("The selected outbound interface and source address are the primary."),
        b("IPv4 and IPv6 behave as intended; otherwise one family may bypass the preference."),
        b("DNS resolution works over each path when tested independently."),
        b("No unintended default route has a lower combined route + interface metric."),
        label("Restore automatic metrics"),
        code(
            'Set-NetIPInterface -InterfaceAlias "Ethernet" -AddressFamily IPv4 -AutomaticMetric Enabled\n'
            'Set-NetIPInterface -InterfaceAlias "Secondary" -AddressFamily IPv4 -AutomaticMetric Enabled',
            size=5.95,
        ),
        p("Repeat for IPv6 if it was changed.", size=7.1),
        p(
            "On Home, metrics can prefer Ethernet but cannot enforce Wi-Fi disconnection; the next page preserves automatic fallback and states that limit."
            if g.edition == "Home"
            else "On Pro, metrics establish route preference; the next page adds the supported Connection Manager policy that holds Wi-Fi back while Ethernet exists.",
            size=6.9, color=SLATE,
        ),
    ], fill=BLUE_PALE, page_tag="p10-validate")
    g.action_strip([
        ("Prerequisite", "Both adapters already work independently.", "info"),
        ("Restart", "None.", "pass"),
        ("Pass", "New connections select the intended primary path.", "pass"),
        ("Fail", "Wrong family/route, DNS failure, or asymmetric reachability.", "fail"),
        ("Rollback", "Re-enable AutomaticMetric on every changed family.", "warn"),
    ])
    g.next()


def page_11(g: Guide) -> None:
    g.begin("Failover validation — and its real boundary", "Host resilience", "CONDITIONAL CHANGE",
            "Test planned recovery of new connections. A second adapter on the same upstream is not ISP redundancy.")
    g.card(40, 520, 346, 335, "Controlled failover test", [
        s(1, "Confirm each interface works alone, Wi-Fi is allowed to connect automatically, and the metrics on page 11 are correct."),
        s(2, "Start continuous gateway and Internet pings. Open a simple TCP test on the primary."),
        s(3, "Disconnect the primary cable or disable only the primary adapter."),
        code('Disable-NetAdapter -Name "Ethernet" -Confirm:$false', size=6.6),
        s(4, "Record loss duration, new source/interface, DNS behavior, and whether new connections succeed."),
        s(5, "Restore the primary; verify the route returns only after the link is stable."),
        code('Enable-NetAdapter -Name "Ethernet" -Confirm:$false', size=6.6),
        p("Repeat the outage/failback cycle three times. Any failed cycle fails the validation.", size=7.0),
        p("Run locally if possible. Disabling the adapter ends a remote session that depends on it.", size=7.2, color=RED),
    ], fill=WHITE, page_tag="p11-test")
    if g.edition == "Home":
        policy_title = "Home: prefer Ethernet and preserve fallback"
        policy_blocks = [
            label("Supported Home behavior"),
            s(1, "Keep the intended T-Mobile Wi-Fi profile saved and allowed to connect automatically."),
            s(2, "Use page 11 metrics so new routes prefer Ethernet whenever it is healthy."),
            s(3, "Test cable/adapter loss, then verify new connections use Wi-Fi and the T-Mobile path."),
            p("Home has no supported Local Group Policy equivalent of Connection Manager option 3 or configurable soft disconnect. Wi-Fi may remain associated while Ethernet is active; route preference is not radio disassociation.", size=7.0),
            p("Do not manually turn off Wi-Fi if automatic host failover is required. Strict Wi-Fi absence while Ethernet is up requires manual control or a supported managed/edition path, and manual control sacrifices automatic recovery.", size=6.95, color=RED),
        ]
    else:
        policy_title = "Pro-only: Ethernet preferred, Wi-Fi held back"
        policy_blocks = [
            label("Windows 11 Pro / Education / Enterprise"),
            s(1, "Run gpedit.msc as administrator."),
            s(2, "Go to Computer Configuration > Administrative Templates > Network > Windows Connection Manager."),
            s(3, "Open “Minimize the number of simultaneous connections to the Internet or a Windows Domain.”"),
            s(4, "Set Enabled, then choose 3 = Prevent Wi-Fi when on Ethernet. Select OK."),
            s(5, "Leave “Enable Windows to soft-disconnect...” Enabled or Not Configured so active traffic can settle."),
            code("gpupdate /force", size=6.6),
            p("The Wi-Fi radio can remain on. The policy prevents a WLAN connection while Ethernet exists; soft disconnect may preserve existing TCP traffic temporarily.", size=6.85, color=SLATE),
        ]
    g.card(400, 520, 352, 218, policy_title, policy_blocks,
           fill=AMBER_PALE, page_tag="p11-policy")
    if g.edition == "Home":
        field_title = "What Amy's Pro field record does not prove on Home"
        field_blocks = [
            label("Edition boundary"),
            p("Amy's strict disconnect/failback observation used Windows 11 Pro, metrics 10/50, and WCM option 3. It is not evidence that Home can hold Wi-Fi disconnected while Ethernet is present.", size=6.65),
            b("Home metrics can prefer a route; they do not disassociate the Wi-Fi radio.", size=6.55, leading=8.3),
            b("Keep the T-Mobile profile usable and validate three cable-loss/failback cycles on the actual PC.", size=6.55, leading=8.3),
            p("Existing TCP/VPN sessions may reset. Both direct-host and eero-wide recovery share the same T-Mobile backup failure domain.", size=6.6, color=SLATE),
        ]
    else:
        field_title = "Amy's Windows 11 Pro failover field record"
        field_blocks = [
            label("Two PCs; one bounded observation"),
            p("Ethernet metric 10, Wi-Fi metric 50, WCM option 3, and a saved T-Mobile profile allowed to Auto-Connect.", size=6.65),
            b("Cable removal moved both PCs to T-Mobile: one observed lost ping on I225-V/AX210; none observed on I226-V/Realtek 8851BE.", size=6.55, leading=8.3),
            b("Cable return restored Ethernet and left Wi-Fi disconnected; eero SQM behavior remained normal.", size=6.55, leading=8.3),
            p("This is not an SLA or carrier-diverse enterprise failover. Existing sessions may reset, and both recovery layers share T-Mobile.", size=6.6, color=SLATE),
        ]
    g.card(400, 290, 352, 185, field_title, field_blocks,
           fill=PURPLE_PALE, page_tag="p11-field")
    g.action_strip([
        ("Restart", "None; adapter disable/enable creates the intended outage.", "pass"),
        ("Pass", "New connections use secondary within the declared objective.", "pass"),
        ("Expected", "Existing TCP/VPN sessions may reset.", "warn"),
        ("Fail", "No route/DNS, shared failure, or primary never returns cleanly.", "fail"),
        (
            "Rollback",
            "Restore automatic metrics and the prior Wi-Fi profile behavior."
            if g.edition == "Home"
            else "Set policy Not Configured; gpupdate /force; restore metrics.",
            "warn",
        ),
    ])
    g.next()


def page_12(g: Guide) -> None:
    g.begin("Install and verify the measurement toolkit", "Throughput testing", "PROVEN BASELINE",
            "Use a trusted iPerf3 build and Microsoft Sysinternals PsPing. Do not expose a test listener to the Internet.")
    g.card(40, 520, 350, 303, "iPerf3 — throughput", [
        s(1, "Acquire iPerf3 from a trusted project/distribution source; preserve the version and hash used."),
        s(2, "Extract it to a dedicated test folder and open PowerShell in that folder."),
        code('.\\iperf3.exe --version', size=6.8),
        s(3, "On a controlled server, listen only on the intended interface/firewall scope."),
        code('iperf3 -s -p 5201', size=6.8),
        s(4, "Allow the test port only on the required private/test network. Never create a broad Internet port-forward."),
        p("Public servers were used in Amy's historical evidence, but a dedicated endpoint is the reproducible default. Follow every public server's rules and stop if it is busy.", size=7.3),
    ], fill=WHITE, page_tag="p12-iperf")
    g.card(404, 520, 348, 303, "PsPing — latency distribution", [
        s(1, "Download PsPing/PsTools from Microsoft Sysinternals."),
        s(2, "Run once to accept the license, or use the documented non-interactive switch."),
        code('.\\psping64.exe -accepteula\n.\\psping64.exe -4 -n 10 -q 1.1.1.1', size=6.8),
        s(3, "Keep separate terminals for gateway latency, Internet latency, upload, and download."),
        label("Core options"),
        p("-4 IPv4  |  -n sample count  |  -i interval  |  -q quiet  |  -h histogram  |  -R iPerf reverse  |  -P streams  |  -O omit warmup  |  -t duration", size=7.15),
        p("Confirm system time, server identity, commands, and router/SQM state in the test record.", size=7.3),
    ], fill=TEAL_PALE, page_tag="p12-psping")
    g.action_strip([
        ("Prerequisite", "Trusted binaries; controlled server; scoped firewall.", "info"),
        ("Restart", "None.", "pass"),
        ("Validate", "Version output, 10-ping smoke test, local listener.", "info"),
        ("Pass", "Tools run and the test endpoint is attributable.", "pass"),
        ("Rollback", "Remove the scoped firewall rule/listener after testing.", "warn"),
    ])
    g.next()


def page_12_failover(g: Guide) -> None:
    evidence_label = "FIELD VERIFIED" if g.edition == "Pro" else "PROVEN BASELINE"
    evidence_boundary = (
        "Host-direct recovery and eero Internet Backup are complementary; both depend on the same backup service."
        if g.edition == "Pro"
        else "Amy field-verified the eero-wide path and Windows 11 Pro/macOS host paths; validate Home fallback locally."
    )
    g.begin("Two tested failover layers, one T-Mobile backup", "Field resilience", evidence_label,
            evidence_boundary)
    g.card(40, 520, 352, 328, "Amy's field topology and edition boundary", [
        label("Primary path"),
        p("Metronet symmetric 2/2 Gbps Internet → eero gateway/network → wired and Wi-Fi clients.", size=7.45),
        label("Full-network backup — successful field test"),
        p("eero Plus Internet Backup is configured to use the T-Mobile Home Backup Internet Wi-Fi source. A whole-eero-network switch to that backup completed successfully.", size=7.45),
        label("Direct host backup"),
        p("The Windows 11 Pro PCs and M1 Pro MacBook Pro also have a direct T-Mobile backup path configured for host-level failover when their eero/Ethernet path is unavailable.", size=7.45),
        label("Critical boundary"),
        p("These are two control layers but only one backup carrier/gateway. A T-Mobile outage, allowance exhaustion, poor signal, or gateway power loss defeats both. This is not carrier-diverse backup.", size=7.45, color=RED),
        p(
            "When Ethernet remains linked and only the primary WAN fails, eero Internet Backup owns recovery. Home's metric-based host preference is best matched to loss of the Ethernet path itself."
            if g.edition == "Home"
            else "When Ethernet remains linked and only the primary WAN fails, eero Internet Backup owns recovery. The Pro WCM policy is best matched to loss of the Ethernet path itself.",
            size=7.25, color=SLATE,
        ),
    ], fill=WHITE, page_tag="p12f-topology")
    g.card(406, 520, 346, 328, "Reproduce network-wide failover safely", [
        s(1, "Confirm eero Plus is active, the eero network is not in bridge mode, and the T-Mobile gateway is powered, in range, and has usable allowance."),
        s(2, "In the eero app, open Security & privacy > eero Plus > eero Internet Backup. Add/select the T-Mobile backup network."),
        s(3, "Start gateway/Internet pings and a lightweight new-connection check on at least one wired and one Wi-Fi eero client."),
        s(4, "Disconnect only the primary WAN feed from the eero gateway. Do not power off the eero or T-Mobile gateway."),
        s(5, "Record detection/recovery time, eero backup status, DNS, local-LAN access, public reachability, and representative workload behavior."),
        s(6, "Restore the primary WAN and verify automatic failback after the path is stable."),
        s(7, "Repeat the outage/failback cycle three times; one failed cycle fails validation."),
        label("Score the backup for its job"),
        p("Existing sessions may reset and brief downtime is expected. Validate the minimum backup workload; do not run a multi-gigabit stress campaign against a metered/time-limited cellular backup.", size=7.05),
    ], fill=GREEN_PALE, page_tag="p12f-test")
    g.action_strip([
        ("Restart", "No reboot. Keep both gateways powered during the test.", "pass"),
        ("Pass", "eero clients recover on T-Mobile and automatically fail back.", "pass"),
        (
            "Host path",
            "Validate Home locally; Amy field-tested Windows 11 Pro and M1 Pro host paths."
            if g.edition == "Home"
            else "Direct T-Mobile fallback is tested separately per PC/Mac.",
            "info",
        ),
        ("Fail", "Bridge mode, no signal/allowance, shared power, or no DNS.", "fail"),
        ("Rollback", "Restore primary WAN; disable/remove backup network if needed.", "warn"),
    ])
    g.next()


def page_13(g: Guide) -> None:
    g.begin("Pass the local gate before testing the ISP", "Throughput testing", "PROVEN BASELINE",
            "The WAN cannot be interpreted until the client, server, NICs, slots, switch, and media work locally.")
    g.card(40, 520, 363, 307, "Topology and local test sequence", [
        check("Draw every hop and record the negotiated rate at both ends of every link."),
        check("Use a controlled server whose NIC, CPU, PCIe path, and switch port exceed the client/service target."),
        check("Close VPNs, cloud sync, game downloads, backup jobs, and browser speed tests."),
        code('Get-NetAdapter | Format-Table Name,Status,LinkSpeed,InterfaceDescription -Auto', size=6.4),
        s(1, "Run one TCP stream to reveal a per-flow/CPU/window limit."),
        code('.\\iperf3.exe -c <LAN-SERVER-IP> -P 1 -t 30 -O 5', size=6.35),
        s(2, "Run four streams, then eight only if throughput is still rising."),
        code('.\\iperf3.exe -c <LAN-SERVER-IP> -P 4 -t 30 -O 5\n.\\iperf3.exe -c <LAN-SERVER-IP> -R -P 4 -t 30 -O 5', size=6.1),
        s(3, "Repeat three times and compare counter deltas and endpoint CPU."),
    ], fill=WHITE, page_tag="p13-sequence")
    g.card(417, 520, 335, 307, "Local acceptance gate", [
        label("Pass"),
        b("Median application throughput is at least 90% of the slower negotiated link rate, or meets a documented platform-specific ceiling."),
        b("No run is below 85% without an explained transient."),
        b("Adapter error/discard deltas remain zero; link speed does not renegotiate."),
        b("No endpoint core is saturated and no driver reset/thermal event occurs."),
        label("Fail — stay local"),
        b("Wrong link speed: inspect cable, port, negotiation, driver, and power state."),
        b("One direction only is slow: swap endpoints/ports and inspect receive CPU/RSS."),
        b("More streams plateau early: inspect CPU, PCIe width, server capacity, and switch path."),
        p("A LAN failure invalidates a WAN conclusion. Repair locally, then repeat the gate.", size=7.4, color=RED),
    ], fill=BLUE_PALE, page_tag="p13-gate")
    g.action_strip([
        ("Restart", "None unless a driver/firmware correction explicitly needs it.", "pass"),
        ("Pass", "Three-run local gate clears target with clean counters.", "pass"),
        ("Fail", "Do not call the ISP or tune TCP yet.", "fail"),
        ("Rollback", "Return the last local change; swap one component.", "warn"),
        ("Next", "Proceed to single-direction WAN validation.", "info"),
    ])
    g.next()


def page_14(g: Guide) -> None:
    g.begin("Validate 2 Gbps one direction at a time", "2/2 Gbps field method", "FIELD VERIFIED",
            "Use a dedicated WAN endpoint when possible. Public servers are variable and may not permit sustained high-rate tests.")
    g.card(40, 520, 348, 313, "Baseline latency first", [
        label("Gateway — substitute the actual default gateway"),
        code('.\\psping64.exe -4 -n 600 -i 0.1 -q -h 20 <GATEWAY-IP>', size=6.3),
        label("Internet reference"),
        code('.\\psping64.exe -4 -n 600 -i 0.1 -q -h 50 1.1.1.1', size=6.3),
        p("Record average, median/histogram shape, high-percentile behavior, loss, and isolated maxima. The distribution matters more than one outlier.", size=7.4),
        label("Before each throughput set"),
        b("Save adapter counters."),
        b("Confirm SQM state and that no other heavy workload is running."),
        b("Record server, route, iPerf version, and endpoint CPU."),
    ], fill=TEAL_PALE, page_tag="p14-latency")
    g.card(402, 520, 350, 313, "Upload, reverse-download, repeat", [
        label("Upload"),
        code('.\\iperf3.exe -4 -c <SERVER> -p 5201 -P 8 -t 120 -O 10 --get-server-output', size=6.05),
        label("Download"),
        code('.\\iperf3.exe -4 -c <SERVER> -p 5201 -R -P 8 -t 120 -O 10', size=6.05),
        s(1, "Run upload and download separately, at least three times each."),
        s(2, "Use one stream, then four, before eight when characterizing a new endpoint."),
        s(3, "Retest with a second controlled endpoint/time window if the result is inconsistent."),
        label("2 Gbps method gate"),
        p("Pass: median at least 1.8 Gbps (90%), no run below 1.7 Gbps without explanation, clean local counters, stable plateau, and no endpoint CPU saturation.", size=7.35),
    ], fill=WHITE, page_tag="p14-throughput")
    g.action_strip([
        ("Restart", "None.", "pass"),
        ("Pass", "Each direction independently clears the method gate.", "pass"),
        ("Conditional", "Remote endpoint/path varies; local gate remains clean.", "warn"),
        ("Fail", "Repeatable deficit across controlled servers or local errors.", "fail"),
        ("Next", "Only then run simultaneous bidirectional load.", "info"),
    ])
    g.next()


def page_15(g: Guide) -> None:
    g.begin("Prove simultaneous bidirectional capacity", "2/2 Gbps field method", "FIELD VERIFIED",
            "Two independent sessions reduce the chance that one process, port, or remote server masks full-duplex capacity.")
    g.card(40, 520, 457, 325, "Four-window run order", [
        s(1, "Start gateway and Internet PsPing. Wait about 10 seconds."),
        code(
            '.\\psping64.exe -4 -n 1400 -i 0.1 -q -h 20 <GATEWAY-IP>\n'
            '.\\psping64.exe -4 -n 1400 -i 0.1 -q -h 50 1.1.1.1',
            size=6.15,
        ),
        s(2, "Start the upload and reverse-download sessions as close together as practical."),
        code(
            '# Window A — upload\n'
            '.\\iperf3.exe -4 -c <UPLOAD-SERVER> -p 5201 -P 8 -t 150 -O 15 --get-server-output\n'
            '# Window B — reverse download\n'
            '.\\iperf3.exe -4 -c <DOWNLOAD-SERVER> -p 5201 -R -P 8 -t 150 -O 15',
            size=5.8,
        ),
        s(3, "Let every process finish. Record sender/receiver rates, retransmissions, CPU, latency, and adapter-counter deltas."),
        s(4, "Repeat three times. A 16-stream escalation is acceptable only if the endpoint permits it and 8 streams have not reached a stable plateau."),
    ], fill=WHITE, page_tag="p15-run")
    g.card(511, 520, 241, 325, "2/2 simultaneous gate", [
        label("Target"),
        p("At least 1.8 Gbps in each direction and at least 3.6 Gbps aggregate application throughput.", size=7.8),
        label("Also required"),
        b("Local errors/discards: zero delta."),
        b("No link renegotiation or driver reset."),
        b("Endpoint CPU not saturated."),
        b("Gateway latency remains consistent with the chosen SQM/queueing state."),
        label("Do not misread"),
        p("Remote sender retransmissions indicate loss/congestion somewhere between that sender and the receiver. Clean local adapter counters argue against, but do not mathematically eliminate, a local cause.", size=7.3),
        p("A public server miss is not a service failure until controlled endpoints and the local gate agree.", size=7.3, color=SLATE),
    ], fill=GREEN_PALE, page_tag="p15-gate")
    g.action_strip([
        ("Restart", "None.", "pass"),
        ("Pass", "Each direction ≥1.8; aggregate ≥3.6; counters clean.", "pass"),
        ("Fail", "Same bounded deficit across controlled endpoints.", "fail"),
        ("Rollback", "Stop load; restore SQM/adapter state used for baseline.", "warn"),
        ("Record", "Keep commands, interval output, latency, counters.", "info"),
    ])
    g.next()


def page_16(g: Guide) -> None:
    g.begin("Amy's approximately 3.8–3.9 Gbps validation", "Evidence record", "FIELD VERIFIED",
            "The strongest simultaneous runs demonstrate the expected full-duplex aggregate for a symmetric 2/2 service.")
    g.metric(40, 387, 220, 108, "≈ 3.8", "Gbps aggregate: approximately 1.9 Gbps upload + 1.9 Gbps download.")
    g.metric(275, 387, 220, 108, "≈ 3.9", "Gbps best aggregate: approximately 2.0 Gbps upload + 1.9 Gbps download.")
    g.metric(510, 387, 242, 108, "33.5 GB", "Transferred in one 150-second receive run at approximately 1.92 Gbps.")
    g.card(40, 365, 345, 225, "Corroborating observations", [
        b("Two captured post-test adapter checks showed zero received discards, received errors, outbound discards, and outbound errors."),
        b("The successful simultaneous totals were far above a hypothetical 2 Gbps combined ceiling."),
        b("The measured direction rates were close to the provisioned rate at the same time."),
        b("Variation across public tests tracked endpoint/path limitations more than a persistent local ceiling."),
        b("Heavy retransmissions on weak public runs were not accompanied by local adapter-error deltas."),
    ], fill=GREEN_PALE, page_tag="p16-corroborate")
    g.card(399, 365, 353, 225, "How to cite this result safely", [
        label("Say"),
        p("Amy's recorded Windows/I225-V/eero/Metronet path sustained approximately 3.8–3.9 Gbps aggregate application throughput during concurrent upload and download testing.", size=7.75),
        label("Do not say"),
        b("The Ethernet link moved 4.0 Gbps of payload exactly."),
        b("Every public test endpoint can reproduce the result."),
        b("Zero adapter counters prove the entire path had zero loss."),
        b("The result validates 5/5 or 10/10 equipment."),
        p("Application goodput, protocol overhead, sample timing, and rounded display values explain why this is an approximate record.", size=7.25, color=SLATE),
    ], fill=WHITE, page_tag="p16-cite")
    g.action_strip([
        ("Restart", "None.", "pass"),
        ("Pass", "A future run stays within the same evidence boundary.", "pass"),
        ("Fail", "Rounded totals or public servers are treated as guarantees.", "fail"),
        ("Reproduce", "Use pages 14–17 with a controlled endpoint.", "info"),
        ("Escalate", "Use the appendix only after hardware/path prerequisites.", "purple"),
    ])
    g.next()


def page_17(g: Guide) -> None:
    g.begin("eero SQM A/B test for loaded latency", "Latency under load", "CONTROLLED EXPERIMENT",
            "SQM can reduce latency while reducing peak throughput. Test both states; bridge mode does not provide SQM.")
    g.card(40, 520, 366, 323, "Exact A/B sequence", [
        s(1, "Open the eero app and tap Settings."),
        s(2, "Tap Advanced networking."),
        s(3, "Under Network services, tap SQM."),
        s(4, "Record the current toggle state. No eero reboot is normally required; allow a few minutes after changing it."),
        s(5, "Run three cycles in state A: idle, download-only, upload-only, then simultaneous bidirectional load."),
        s(6, "Toggle SQM and repeat the identical server, commands, order, and time window for state B."),
        s(7, "Compare throughput, gateway and Internet latency distributions, loss, counters, and application behavior."),
        p("eero documents that SQM is unavailable in bridge mode and may lower bandwidth for some devices while improving latency-sensitive work.", size=7.2, color=SLATE),
    ], fill=PURPLE_PALE, page_tag="p17-sequence")
    g.card(420, 520, 332, 323, "Decision rule", [
        label("Calculate"),
        p("Added latency = loaded latency − idle latency. Compare medians and high-percentile behavior; do not optimize around one maximum.", size=7.7),
        label("Practical interpretation — not a standard"),
        p("0–5 ms exceptional  |  5–15 very good  |  15–30 good  |  30–60 moderate  |  60–100 significant  |  >100 severe", size=7.15),
        label("Keep SQM when"),
        b("Loaded latency improves materially and repeatedly."),
        b("Throughput remains above the workload/service floor."),
        b("The real application behaves better."),
        label("Roll back when"),
        b("The improvement is neutral/inconsistent or throughput cost is unacceptable."),
        p("Gateway stays low while Internet rises: likely WAN/upstream/remote queue. Both rise: investigate client/router/local queue.", size=7.25, color=SLATE),
    ], fill=WHITE, page_tag="p17-rule")
    g.action_strip([
        ("Restart", "No reboot; allow the eero state to settle.", "pass"),
        ("Pass", "Repeatable loaded-latency gain above throughput floor.", "pass"),
        ("Fail", "No gain, unstable result, or unacceptable throughput loss.", "fail"),
        ("Rollback", "Return the toggle to its captured original state.", "warn"),
        ("Record", "Keep both states and all four workload results.", "info"),
    ])
    g.next()


def page_wifi_evidence(g: Guide) -> None:
    g.begin("Amy's eero radio record: healthy, no change", "Wi-Fi optimization", "FIELD VERIFIED",
            "Two wired eero Pro 7 nodes already had excellent 5/6 GHz conditions and no symptom that justified tuning.")
    g.card(40, 520, 350, 324, "2.4 GHz — busy air, quiet network", [
        label("Representative Node A snapshot"),
        p("Total busyness 48% = 4% activity on this radio + 44% other-device interference. 24-hour average 36%; P99 47%; maximum 59%; noise floor −111 dBm; channel 6 at 20 MHz.", size=7.35),
        label("Later observations across both nodes"),
        p("Averages were roughly 28–30%, current readings roughly 26–36%, and noise floor roughly −95 to −107 dBm. Node B sometimes heard more RF energy than Node A.", size=7.35),
        label("Decision"),
        p("The eero network itself occupied little airtime; neighboring/other transmitters explained most of the busy time. With stable latency, no loss/disconnect symptom, and clean higher bands, no change was warranted.", size=7.45, color=GREEN),
        p("Official eero definitions: total busyness is own-radio activity plus other-device interference; P99 describes the worst 1% more usefully than one maximum spike.", size=7.15, color=SLATE),
    ], fill=WHITE, page_tag="wifi-record-24")
    g.card(404, 520, 348, 324, "5 and 6 GHz — exceptionally clean", [
        label("5 GHz"),
        p("Current busyness 4% = 1% own + 3% other; 24-hour average 5%; P99 9%; one transient maximum 69%; noise floor −105 dBm; channel 130 at 240 MHz.", size=7.4),
        label("6 GHz"),
        p("Across the wired Pro 7 nodes, average busyness was about 2%, P99 3%, maximum 4–5%, and noise floor about −107 dBm.", size=7.4),
        label("Context"),
        p("eero documents 240 MHz channel support on Wi-Fi 7 5/6 GHz radios. DFS operation and an isolated maximum are not failures by themselves; correlate a channel event with a real client symptom.", size=7.35),
        label("Evidence boundary"),
        p("These values describe Amy's two-node, Ethernet-backhauled home at the observed times. They do not define universal pass thresholds, predict every client, or prove Wi-Fi can carry the wired 2/2 service rate.", size=7.35, color=SLATE),
    ], fill=GREEN_PALE, page_tag="wifi-record-56")
    g.action_strip([
        ("Prerequisite", "Compare 24-hour data and actual client symptoms.", "info"),
        ("Restart", "None; no setting changed.", "pass"),
        ("Pass", "Healthy clients + low sustained own activity + stable tests.", "pass"),
        ("Fail", "A single maximum or neighbor traffic is treated as a fault.", "fail"),
        ("Decision", "Preserve the working topology and automatic control.", "warn"),
    ])
    g.next()


def page_wifi_protocol(g: Guide) -> None:
    g.begin("Optimize Wi-Fi only after a client fails a test", "Wi-Fi optimization", "CONDITIONAL CHANGE",
            "Observe → localize → change one physical or feature variable → retest → roll back if it does not help.")
    iperf_client = "iperf3" if g.edition == "macOS" else ".\\iperf3.exe"
    g.card(40, 520, 355, 334, "Measurement sequence", [
        s(1, "Name the affected device, room, application, time window, and symptom. Keep a wired client as the control."),
        s(2, "In the eero app: Home > select an eero > Wifi radio analytics. Choose 24 hours and record each node/band: average, P99, maximum, total, own activity, other interference, noise floor, channel, width, and channel-change times."),
        s(3, "Run Settings > Troubleshooting > Device coverage scan. Treat an eero result of zero poor connections as healthy; follow placement guidance for a poor device."),
        s(4, "From the same client position, ping the gateway and test both directions to a wired local server before testing the Internet."),
        code(
            f'{iperf_client} -c <WIRED-LAN-SERVER> -t 60 -O 5\n'
            f'{iperf_client} -c <WIRED-LAN-SERVER> -R -t 60 -O 5',
            size=6.3,
        ),
        s(5, "Repeat three times on the same client, position, power state, band, and server. If aggregate capacity is the question, repeat separately with -P 4; do not hide the one-stream result."),
        p("Runbook consistency gate: no loss/abort, and each direction's slowest run is at least 85% of its three-run median. Choose a client-specific throughput target before testing.", size=6.95, color=TEAL_DARK),
        p("Wi-Fi is shared, half-duplex airtime. Do not apply the wired 2/2, 5/5, or 10/10 gates to a wireless client; its radio, channel width, signal, contention, and power state may be the ceiling.", size=7.1, color=SLATE),
    ], fill=WHITE, page_tag="wifi-method")
    g.card(409, 520, 343, 334, "Symptom-driven changes and stop rules", [
        label("If own-radio activity is sustained and the client is slow"),
        p("Identify local talkers, backups, cameras, or downloads; pause/reschedule one source and repeat the identical test.", size=7.1),
        label("If Coverage scan reports a poor connection"),
        p("Move the affected eero/client away from obstructions and retest. Add a node only when measured coverage remains poor and the app's guidance supports it; validate that contention and roaming do not worsen.", size=7.1),
        label("If other interference is high but clients are healthy"),
        p("Observe. eero chooses channels automatically and does not expose ordinary manual channel/width selection. Keep Ethernet backhaul and Client Steering defaults unless a documented compatibility symptom requires an A/B test.", size=7.1),
        label("Operator heuristics — not eero specifications"),
        p("A high-performance client around −65 dBm or better, sustained busyness around 70–80%+, or noise approaching −90 dBm can justify closer investigation only when a repeatable symptom agrees. They are not automatic change thresholds.", size=7.0, color=PURPLE),
        p("Avoid repeated reboots to chase a channel: eero says long-term channel optimization takes roughly 2 days to 1 week, and resets restart that learning.", size=7.05, color=RED),
    ], fill=AMBER_PALE, page_tag="wifi-decisions")
    g.action_strip([
        ("Restart", "Normally none; allow automatic optimization to settle.", "pass"),
        ("Pass", "No loss; ≥85% consistency; declared client target met.", "pass"),
        ("Fail", "No repeatable gain, new poor devices, or worse latency.", "fail"),
        ("Rollback", "Restore prior placement/toggle; leave ACS automatic.", "warn"),
        ("Escalate", "Capture graphs, scan, client details, and exact times.", "info"),
    ])
    g.next()


def page_18(g: Guide) -> None:
    g.begin("Interpret the evidence without guessing", "Result analysis", "PROVEN BASELINE",
            "A useful conclusion names the measurement point, direction, endpoint, and competing bottlenecks.")
    g.card(40, 520, 350, 330, "Signal → likely interpretation", [
        p("Gateway latency rises under load — queueing is local to the client/router/LAN path or the router is saturated.", size=7.45),
        p("Gateway stays flat; Internet latency rises — WAN access, upstream, transit, or remote path queueing.", size=7.45),
        p("Only one remote server is slow — remote endpoint/route is the first suspect; retest elsewhere.", size=7.45),
        p("Download slow; upload normal — inspect reverse path, receive CPU/RSS, server sender, and service shaping by direction.", size=7.45),
        p("More streams help until a plateau — a single-flow window/CPU/path limit existed; plateau identifies the next ceiling.", size=7.45),
        p("Local adapter errors/discards increase — investigate physical link, driver, buffers, or hardware before blaming WAN.", size=7.45),
        p("Retransmissions rise but local counters stay clean — loss/congestion may be remote or in transit; still correlate timing and direction.", size=7.45),
        p("One endpoint core is pinned — the benchmark is CPU-limited even if total CPU appears low.", size=7.45),
    ], fill=WHITE, page_tag="p18-signals")
    g.card(404, 520, 348, 330, "Pass / conditional / fail language", [
        label("Pass"),
        p("Three-run median clears the predeclared gate; no unexplained low run; clean counters; stable negotiation; endpoints have headroom.", size=7.55),
        label("Conditional pass"),
        p("Local gate passes and a second controlled endpoint passes, while one public endpoint/path does not. Record the exception; do not tune the client around it.", size=7.55),
        label("Fail"),
        p("The same deficit repeats locally or across controlled WAN endpoints; errors/discards increase; negotiation falls; or endpoint/slot/CPU limits are demonstrated.", size=7.55),
        label("Insufficient evidence"),
        p("One browser speed test, one public server, mixed Wi-Fi/wired tests, simultaneous unrelated traffic, unknown router state, or missing counter/CPU data.", size=7.55),
        {"type": "rule"},
        p("Fast.com and browser speed tests can be useful corroboration, but their connection behavior and remote selection make them weak isolation tools.", size=7.3, color=SLATE),
    ], fill=BLUE_PALE, page_tag="p18-language")
    g.action_strip([
        ("Restart", "None.", "pass"),
        ("Pass", "Conclusion follows the same measurement in ≥3 runs.", "pass"),
        ("Fail", "Cause is assigned from correlation alone.", "fail"),
        ("Recovery", "Change server, localize the path, then repeat.", "warn"),
        ("Evidence", "Keep raw commands/results; summarize only after.", "info"),
    ])
    g.next()


def page_19(g: Guide) -> None:
    g.begin("Failure decision tree", "Troubleshooting", "PROVEN BASELINE",
            "Localize the first failing boundary; do not skip ahead to tuning.")
    c = g.c
    nodes = [
        (40, 430, 160, 68, "1  LINK", "Expected negotiation?", TEAL_PALE, TEAL_DARK),
        (224, 430, 160, 68, "2  LOCAL", "LAN ≥90% and clean?", BLUE_PALE, BLUE),
        (408, 430, 160, 68, "3  SINGLE", "Each WAN direction?", GREEN_PALE, GREEN),
        (592, 430, 160, 68, "4  BOTH", "Simultaneous gate?", PURPLE_PALE, PURPLE),
    ]
    for x, y, w, h, head, body, fill, color in nodes:
        rr(c, x, y, w, h, 10, fill, color, 0.8)
        c.setFont("Segoe-Bold", 8)
        c.setFillColor(color)
        c.drawString(x + 12, y + 43, head)
        c.setFont("Segoe", 8)
        c.setFillColor(INK)
        c.drawString(x + 12, y + 23, body)
    for x in (204, 388, 572):
        c.setStrokeColor(SLATE)
        c.setLineWidth(1.3)
        c.line(x, 464, x + 14, 464)
        c.line(x + 10, 468, x + 14, 464)
        c.line(x + 10, 460, x + 14, 464)
    g.card(40, 409, 344, 240, "If the first NO is at LINK or LOCAL", [
        label("Wrong negotiation / link flap"),
        b("Try a known-good cable and port; verify both ends support the rate."),
        b("Restore Auto Negotiation and documented driver defaults."),
        b("Check driver identity, power/EEE symptoms, and event logs."),
        label("Local throughput / counters"),
        b("Swap endpoints and direction; inspect per-core CPU and RSS."),
        b("Verify PCIe lane width, switch path, and server capacity."),
        b("Change only one physical or driver variable, then repeat three runs."),
        p("Do not proceed to ISP tests until the local gate passes.", size=7.3, color=RED),
    ], fill=WHITE, page_tag="p19-local")
    g.card(400, 409, 352, 240, "If the first NO is at SINGLE or BOTH", [
        label("Single direction"),
        b("Use a second controlled endpoint and compare route/time."),
        b("Confirm provisioning, router capacity, endpoint CPU, and SQM state."),
        label("Simultaneous only"),
        b("Use separate servers/ports; check router full-duplex NAT/firewall/SQM capacity."),
        b("Correlate gateway vs Internet latency and counter deltas."),
        b("If each direction passes alone but both fail repeatedly, test router/handoff capacity before host tuning."),
        p("Escalate to the ISP with timestamps, local-gate proof, multiple controlled endpoints, commands, and direction-specific results.", size=7.25, color=SLATE),
    ], fill=AMBER_PALE, page_tag="p19-wan")
    g.action_strip([
        ("Restart", "Only after a driver/firmware correction requires it.", "warn"),
        ("Pass", "The earliest failed boundary is identified.", "pass"),
        ("Fail", "Multiple variables change before localization.", "fail"),
        ("Rollback", "Return last variable and retest the same boundary.", "warn"),
        ("Escalate", "Send evidence, not a browser screenshot alone.", "info"),
    ])
    g.next()


def page_20(g: Guide) -> None:
    g.begin("Rollback matrix and recovery order", "Recovery", "PROVEN BASELINE",
            "Restore basic connectivity first. Performance evidence is irrelevant while the path is unstable.")
    g.card(40, 520, 712, 318, "Change → immediate rollback → reboot decision → validation", [
        p("Driver — Device Manager > adapter > Properties > Driver > Roll Back Driver, or reinstall the staged OEM/exported INF. Reboot only if prompted/pending. Validate driver identity, link, gateway, DNS, and counters.", size=7.35),
        p("Advanced property — restore the captured DisplayValue in Device Manager. Let the adapter reset; Windows reboot is rarely needed. Validate negotiation, RSS/offload state, gateway, and local gate.", size=7.35),
        p("Interface metric — re-enable AutomaticMetric for every changed address family. No reboot. Validate route selection and DNS over both paths.", size=7.35),
        p("SQM — return the eero toggle to its captured state and allow it to settle. No reboot. Repeat idle and one loaded-latency run.", size=7.35),
        p("TCP autotuning — restore the recorded state (normally Normal). No reboot unless a reset was also performed. Repeat the same one-stream and multi-stream test.", size=7.35),
        p("Winsock/IP reset — restore any required custom IP, DNS, proxy, VPN, binding, and route configuration from the baseline. Windows restart is required. Validate every business-critical path.", size=7.35),
        p("Failover test — re-enable the primary adapter, reconnect its cable, and confirm intended metrics/routes. No reboot. Expect applications to reconnect.", size=7.35),
        p("Jumbo/VLAN experiment — return every endpoint/switch hop to the prior consistent MTU/tagging state. Adapter/switch-port reset may be needed; validate standard ping and local throughput.", size=7.35),
    ], fill=WHITE, page_tag="p20-matrix")
    g.card(40, 185, 712, 85, "Emergency recovery order", [
        p("1  Stop the load  →  2  Re-enable/reconnect the known primary  →  3  restore automatic addressing/metrics if route choice is unclear  →  4  undo the last change  →  5  reboot only if the driver or network reset requires it  →  6  validate gateway, DNS, and local link  →  7  capture the failure before retrying.", size=8.15),
    ], fill=RED_PALE, stroke=HexColor("#F2B8B5"), page_tag="p20-order")
    g.action_strip([
        ("Pass", "Known-good connectivity and baseline state return.", "pass"),
        ("Fail", "Link/DNS still broken after the last change is undone.", "fail"),
        ("Next", "Use local console/second path; reinstall known-good OEM driver.", "info"),
        ("Restart", "Only where the matrix says it is required.", "warn"),
        ("Preserve", "Do not delete the failed package/logs until analyzed.", "info"),
    ])
    g.next()


def page_21(g: Guide) -> None:
    g.begin("Final acceptance record", "Closeout", "PROVEN BASELINE",
            "A result is complete only when the before state, command, pass gate, and rollback are reproducible.")
    g.card(40, 520, 345, 321, "Environment and change record", [
        check("Date/time/time zone: __________________________________"),
        check("Windows edition/build: ________________________________"),
        check("Adapter/controller: ___________________________________"),
        check("Driver provider/version/date: _________________________"),
        check("Negotiated link / service target: _____________________"),
        check("Router / firmware / SQM state: ________________________"),
        check("Primary + secondary path: _____________________________"),
        check("Change made (one only): _______________________________"),
        check("Reason / named symptom: _______________________________"),
        check("Rollback tested:  YES / NO / NOT APPLICABLE"),
        check("Windows reboot actually required:  YES / NO"),
    ], fill=WHITE, page_tag="p21-record")
    g.card(399, 520, 353, 321, "Measurement and decision", [
        check("Local median / lowest run: _____________________________"),
        check("WAN upload median / lowest: ____________________________"),
        check("WAN download median / lowest: __________________________"),
        check("Bidirectional upload + download: _______________________"),
        check("Aggregate application throughput: ______________________"),
        check("Idle / loaded gateway latency: _________________________"),
        check("Idle / loaded Internet latency: ________________________"),
        check("Error/discard deltas: __________________________________"),
        check("Endpoint max core / temperature: _______________________"),
        check("Outcome: PASS / CONDITIONAL PASS / FAIL / ROLLED BACK"),
        check("Evidence folder / notes: ______________________________"),
    ], fill=TEAL_PALE, page_tag="p21-decision")
    g.action_strip([
        ("Accept", "Every required gate passes and rollback is known.", "pass"),
        ("Conditional", "Exception is bounded to server/path and recorded.", "warn"),
        ("Reject", "Missing baseline, clean counters, or repeatability.", "fail"),
        ("Integrity", "Record the release version and verify its checksum.", "purple"),
        ("Privacy", "Keep raw diagnostics and identifying evidence private.", "info"),
    ])
    g.next()


def page_22(g: Guide) -> None:
    g.page_no += 1
    c = g.c
    g.add_bookmark("Scaling appendix: 5/5 and 10/10 Gbps stress-test method")
    c.setFillColor(PURPLE_PALE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(PURPLE)
    c.rect(0, 0, 13, PAGE_H, fill=1, stroke=0)
    rr(c, 40, 56, PAGE_W - 80, PAGE_H - 96, 22, NAVY, NAVY)
    c.setFont("Segoe-Bold", 8)
    c.setFillColor(HexColor("#BDA9DC"))
    c.drawString(74, PAGE_H - 107, "SEPARATE SCALING APPENDIX")
    c.setFont("Segoe-Bold", 31)
    c.setFillColor(WHITE)
    c.drawString(74, PAGE_H - 168, "5/5 and 10/10 Gbps")
    c.drawString(74, PAGE_H - 207, "Stress-Test Method")
    c.setFont("Segoe", 11)
    c.setFillColor(HexColor("#D5E6F3"))
    c.drawString(76, PAGE_H - 246, "Authoritative-documentation baseline")
    c.drawString(76, PAGE_H - 264, "Not field-tested by Amy; not a product endorsement or line-rate guarantee")
    rr(c, 74, 164, 628, 98, 12, HexColor("#163D5C"), HexColor("#2B5978"), 0.8)
    c.setFont("Segoe-Bold", 8)
    c.setFillColor(HexColor("#BDA9DC"))
    c.drawString(92, 236, "DO NOT SCALE THE 2/2 SETTINGS BY MULTIPLICATION")
    c.setFont("Segoe", 9)
    c.setFillColor(WHITE)
    c.drawString(92, 214, "At 5 and 10 Gbps, endpoint CPU topology, PCIe lanes, switch fabric, router full-duplex")
    c.drawString(92, 197, "capacity, media, driver support, thermals, and the test server become first-class limits.")
    c.drawString(92, 180, "Clear each boundary locally before interpreting an Internet result.")
    g.badge("AMY-UNTESTED", 74, 123)
    c.setFont("Segoe-Bold", 7.1)
    c.setFillColor(WHITE)
    c.drawString(178, 120, "DOCUMENTATION-BACKED / CONTROLLED EXPERIMENT")
    c.setFont("Segoe", 7.2)
    c.setFillColor(MUTED)
    c.drawString(40, 28, "Appendix boundary  |  Re-verify hardware support and vendor matrices before purchase or publication")
    c.drawRightString(PAGE_W - 40, 28, f"{g.page_no} / {g.total_pages}")
    g.next()


def page_23(g: Guide) -> None:
    g.begin("Architecture prerequisites for 5 and 10 Gbps", "Scaling appendix", "AMY-UNTESTED",
            "The slowest hop and the busiest shared resource set the result.", appendix=True)
    g.card(40, 520, 352, 335, "Every boundary must exceed the target", [
        check("ISP handoff/ONT exposes the required per-direction rate and Ethernet mode."),
        check("Router/firewall/NAT/SQM can sustain the simultaneous aggregate, not only one-way marketing throughput."),
        check("Every switch port and internal fabric supports the rate without oversubscription on the tested path."),
        check("Both endpoint NICs, drivers, OS releases, and negotiated modes match."),
        check("PCIe slot is electrically wide/fast enough and not lane-shared into a lower mode."),
        check("CPU has per-core and aggregate headroom; RSS is enabled and actually distributing flows."),
        check("Media, connectors, modules/DAC, and length are supported at both ends."),
        check("The test server has ≥ target-rate headroom and is not a public shared endpoint."),
        check("Cooling/airflow keeps the NIC, PHY, chipset, and SFP+ modules within limits."),
        check("No VPN, storage, browser, or security inspection bottleneck contaminates the path."),
    ], fill=WHITE, page_tag="p23-boundaries")
    g.card(406, 520, 346, 335, "Preflight commands and stop gates", [
        code(
            'Get-NetAdapter | Format-Table Name,Status,LinkSpeed,InterfaceDescription -Auto\n'
            'Get-NetAdapterRss -Name "Ethernet" | Format-List Enabled,NumberOfReceiveQueues,MaxProcessors,Profile\n'
            'Get-NetAdapterStatistics -Name "Ethernet" | Format-List *',
            size=6.05,
        ),
        label("Hardware checks outside Windows"),
        b("Motherboard manual/block diagram: physical slot versus electrical lane width; GPU/M.2 sharing."),
        b("Switch/router datasheet: port combinations, fabric/NAT/SQM performance, and thermal requirements."),
        b("Vendor OS matrix: exact retail card/controller, driver branch, Windows release, and supported link modes."),
        label("Stop"),
        p("Do not start a WAN stress test if any hop negotiates below target, the local server lacks headroom, counters already increase, or the NIC/module is overheating.", size=7.3, color=RED),
        p("A 10 Gb-capable motherboard label does not prove the onboard controller, driver, chipset path, router, or ISP handoff can sustain 10/10.", size=7.3, color=SLATE),
    ], fill=PURPLE_PALE, page_tag="p23-preflight")
    g.action_strip([
        ("Restart", "Only after driver/firmware/slot changes require it.", "warn"),
        ("Pass", "Every hop negotiates at target with clean idle counters.", "pass"),
        ("Fail", "Any shared resource or endpoint is below target.", "fail"),
        ("Rollback", "Restore prior card/driver/slot and standard MTU.", "warn"),
        ("Next", "Clear the phased local throughput gates.", "purple"),
    ], appendix=True)
    g.next()


def page_24(g: Guide) -> None:
    g.begin("Phased 5/5 and 10/10 throughput gates", "Scaling appendix", "AMY-UNTESTED",
            "A publication method: median ≥90% of negotiated rate, no unexplained run <85%, three runs, clean counters.", appendix=True)
    g.card(40, 520, 348, 326, "Stream progression and run order", [
        s(1, "Local test for 30 seconds; WAN test for 120 seconds after the local gate passes."),
        s(2, "Begin with one TCP stream, then four, then eight. Stop adding streams when throughput plateaus."),
        code(
            '.\\iperf3.exe -c <SERVER> -P 1 -t 30 -O 5\n'
            '.\\iperf3.exe -c <SERVER> -P 4 -t 30 -O 5\n'
            '.\\iperf3.exe -c <SERVER> -P 8 -t 30 -O 5\n'
            '.\\iperf3.exe -c <SERVER> -R -P 4 -t 30 -O 5',
            size=6.25,
        ),
        s(3, "Repeat the selected stream count three times in each direction."),
        s(4, "Run simultaneous upload/reverse-download with two sessions or a controlled --bidir endpoint."),
        s(5, "Record per-core CPU, negotiated speed, interval stability, retransmissions, and counter deltas."),
        p("iPerf3 3.16+ uses a separate thread per stream, but the endpoint, OS, and path can still bottleneck. Record the exact version.", size=7.2, color=SLATE),
    ], fill=WHITE, page_tag="p24-order")
    g.card(402, 520, 350, 326, "Application-throughput method gates", [
        label("5 Gbps negotiated path"),
        p("Single direction median ≥4.5 Gbps. Simultaneous: each direction ≥4.5 Gbps; aggregate ≥9.0 Gbps.", size=7.7),
        label("10 Gbps negotiated path"),
        p("Single direction median ≥9.0 Gbps. Simultaneous: each direction ≥9.0 Gbps; aggregate ≥18.0 Gbps.", size=7.7),
        label("Also required"),
        b("No unexplained run below 85% of negotiated rate."),
        b("Zero local error/discard deltas and no link renegotiation."),
        b("No saturated endpoint core, PCIe bottleneck, thermal throttle, or driver reset."),
        label("Interpret carefully"),
        p("These are runbook acceptance gates, not universal service standards. Protocol overhead and implementation ceilings mean payload never equals the nominal PHY rate.", size=7.35),
        p("If four streams plateau but one does not, record both; do not hide a single-flow limitation behind stream count.", size=7.25, color=SLATE),
    ], fill=PURPLE_PALE, page_tag="p24-gates")
    g.action_strip([
        ("Restart", "None for testing.", "pass"),
        ("Pass", "Median ≥90%; all runs ≥85%; counters/CPU/thermals clean.", "pass"),
        ("Fail", "Same deficit locally or across controlled endpoints.", "fail"),
        ("Rollback", "Stop load; restore last driver/property/MTU change.", "warn"),
        ("Escalate", "Add streams only to characterize, never to conceal.", "purple"),
    ], appendix=True)
    g.next()


def page_25(g: Guide) -> None:
    g.begin("Intel 10 GbE PCIe cards and onboard controllers", "Scaling appendix", "AMY-UNTESTED",
            "Examples illustrate selection logic; verify the live Intel/OEM matrix before buying.", appendix=True)
    g.card(40, 520, 350, 330, "Documented Intel reference points", [
        label("X710-T2L — copper reference"),
        p("Intel lists 10/5/2.5/1 GbE and 100 Mb per port, PCIe 3.0 x8, RJ45 media, and current Windows 11 client support in its retail-adapter matrix.", size=7.35),
        p("Use when the exact slot, cooling, OS/driver branch, and port-speed requirements match. The x8 requirement must be electrical, not merely a long connector.", size=7.35),
        label("X550-T2 — cautionary reference"),
        p("Intel lists dual 10 GbE, PCIe 3.0 x4, and current Windows 11 client support, but its product page states NBASE-T support is Linux-only. Do not infer Windows 2.5/5 Gb support from the controller's headline rates.", size=7.35),
        label("X710-DA2 — SFP+ reference"),
        p("Intel lists dual 10/1 GbE SFP+, PCIe 3.0 x8, and direct-attach twinax support up to 10 m. Module/cable/platform compatibility still must be verified.", size=7.35),
        p("These are capability references, not blanket purchase recommendations.", size=7.2, color=PURPLE),
    ], fill=WHITE, page_tag="p25-intel")
    g.card(404, 520, 348, 330, "Motherboard and card selection checklist", [
        check("Exact controller model/revision — not '2.5/5/10G LAN' marketing alone."),
        check("Windows release and driver branch in the current OEM/Intel support matrix."),
        check("Required link modes on Windows, including 2.5/5 Gb NBASE-T where needed."),
        check("Physical and electrical slot width, generation, lane sharing, and GPU/M.2 impact."),
        check("Full-height/low-profile bracket, port count, airflow, and heatsink clearance."),
        check("OEM driver/firmware/BIOS dependencies for an onboard controller."),
        check("Router/switch/handoff media and autonegotiation compatibility."),
        check("Retail provenance and hardware revision; avoid unsupported/counterfeit server pulls."),
        check("Return path and staged fallback NIC before changing the production adapter."),
        p("For onboard 10 GbE, read the motherboard block diagram: a chipset-attached port can share uplink bandwidth even when its PHY negotiates at 10 Gb.", size=7.25, color=SLATE),
    ], fill=PURPLE_PALE, page_tag="p25-checklist")
    g.action_strip([
        ("Restart", "Card install/BIOS/driver package may require Windows restart.", "warn"),
        ("Validate", "Device identity, lane width, driver, modes, thermals, local gate.", "info"),
        ("Pass", "Exact OS/mode/slot/media combination is documented.", "pass"),
        ("Fail", "Support is inferred from controller name or connector length.", "fail"),
        ("Rollback", "Reinstall prior NIC/slot/driver and standard MTU.", "warn"),
    ], appendix=True)
    g.next()


def page_26(g: Guide) -> None:
    g.begin("RJ45, SFP+, thermals, and experimental knobs", "Scaling appendix", "AMY-UNTESTED",
            "Choose one supported media system end to end; adapter defaults remain the baseline.", appendix=True)
    g.card(40, 520, 346, 331, "Copper / RJ45 path", [
        b("For a new 10GBASE-T run, Cat6A is the conservative 100 m choice. Intel lists X550-T2 Cat6 to 55 m and Cat6A to 100 m."),
        b("Intel lists X710-T2L RJ45 Category 5e/6/6A up to 100 m, but installation quality and alien crosstalk still matter."),
        b("Use certified terminations and patch cords; avoid damaged, tightly bent, flat, or unknown-category cable."),
        b("Verify both ends advertise the intended NBASE-T/10GBASE-T mode and link at the same rate."),
        b("10GBASE-T PHYs run warm. Provide chassis airflow and watch for renegotiation under a long full-duplex load."),
        label("Baseline"),
        p("Auto Negotiation, standard MTU, RSS/offloads enabled, driver-default interrupt moderation/buffers.", size=7.4),
    ], fill=WHITE, page_tag="p26-rj45")
    g.card(400, 520, 352, 331, "SFP+ / DAC / fiber path", [
        b("Verify NIC, switch, module/DAC, firmware, and vendor compatibility matrix together."),
        b("For DAC, verify passive/active type and supported length at both ends. Intel documents X710-DA2 twinax up to 10 m."),
        b("For optics, match wavelength, fiber type, connector polish, reach, and transmit/receive pairing."),
        b("Treat an SFP+ RJ45 module as a distinct thermal/compatibility case; many are distance- and platform-limited."),
        b("Capture digital optical monitoring values when the platform exposes them; do not diagnose fiber from link-up alone."),
        label("Controlled experiments only"),
        p("Jumbo frames, RSS-queue changes, interrupt moderation changes, buffer increases, and zero-copy/UDP tuning. Test one at a time on an isolated path and restore defaults if the declared metric does not improve.", size=7.3),
        label("Never infer"),
        p("A clean TCP test does not validate high-rate UDP; packet size, CPU, buffers, pacing, and MTU change that workload materially.", size=7.3, color=RED),
    ], fill=PURPLE_PALE, page_tag="p26-sfp")
    g.action_strip([
        ("Restart", "Link/module reset first; reboot only for driver/firmware need.", "warn"),
        ("Pass", "Long full-duplex load holds rate, link, counters, and temperature.", "pass"),
        ("Fail", "Renegotiation, errors, unsupported module, or thermal drift.", "fail"),
        ("Rollback", "Known-good media; standard MTU; driver defaults.", "warn"),
        ("Record", "Exact cable/module/length/port/firmware combination.", "purple"),
    ], appendix=True)
    g.next()


CORE_REFS = [
    ("ESnet — Invoking iPerf3", "https://software.es.net/iperf/invoking.html"),
    ("Microsoft Sysinternals — PsPing", "https://learn.microsoft.com/en-us/sysinternals/downloads/psping"),
    ("Microsoft Learn — Get-NetAdapterStatistics", "https://learn.microsoft.com/en-us/powershell/module/netadapter/get-netadapterstatistics"),
    ("Microsoft Learn — Get-NetIPInterface", "https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-netipinterface"),
    ("Microsoft Learn — Test-NetConnection", "https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection"),
    ("Microsoft Learn — Windows Update client policies", "https://learn.microsoft.com/en-us/windows/deployment/update/waas-manage-updates-wufb"),
    ("Microsoft Learn — Windows Connection Manager policy (WCM)", "https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wcm"),
    ("Microsoft Learn — BitLocker recovery overview", "https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/recovery-overview"),
    ("Microsoft Learn — How Windows selects a driver package", "https://learn.microsoft.com/en-us/windows-hardware/drivers/install/how-windows-selects-a-driver-for-a-device"),
    ("Microsoft Support — Update drivers through Device Manager", "https://support.microsoft.com/en-us/windows/update-drivers-through-device-manager-in-windows-ec62f46c-ff14-c91d-eead-d7126dc1f7b6"),
    ("Microsoft Learn — PnPUtil command syntax", "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/pnputil-command-syntax"),
    ("Microsoft Learn — Network adapter performance tuning", "https://learn.microsoft.com/en-us/windows-server/networking/technologies/network-subsystem/net-sub-performance-tuning-nics"),
    ("Intel — Advanced settings for Intel Ethernet adapters", "https://www.intel.com/content/www/us/en/support/articles/000005593/ethernet-products.html"),
    ("Intel — Receive Side Scaling", "https://www.intel.com/content/www/us/en/support/articles/000006703/ethernet-products.html"),
    ("Intel — Interrupt Moderation Rate", "https://edc.intel.com/content/www/us/en/design/products/ethernet/adapters-and-devices-user-guide/30.1/interrupt-moderation-rate/"),
    ("Intel — Windows 11 network adapter driver", "https://www.intel.com/content/www/us/en/download/727998/intel-network-adapter-driver-for-microsoft-windows-11.html"),
    ("eero — Smart Queue Management", "https://eero.com/support/articles/360000709886-What-is-Smart-Queue-Management-SQM"),
    ("eero — Internet Backup with eero Plus", "https://support.eero.com/hc/en-us/articles/8947860842523-What-is-eero-Internet-Backup"),
    ("eero — Wifi Radio Analytics", "https://support.eero.com/hc/en-us/articles/15282384606107-Wifi-Radio-Analytics"),
    ("eero — Coverage scan", "https://support.eero.com/hc/en-us/articles/34604365204635-What-is-Coverage-scan"),
    ("eero — How network optimization works", "https://support.eero.com/hc/en-us/articles/360057257311-How-Does-eero-Optimize-My-Network"),
    ("eero — Client Steering and DFS", "https://support.eero.com/hc/en-us/articles/207613326-What-advanced-features-does-eero-support"),
    ("eero — Ethernet backhaul", "https://support.eero.com/hc/en-us/articles/207852743-Can-I-connect-my-eeros-with-Ethernet"),
    ("eero — Wi-Fi channel width", "https://support.eero.com/hc/en-us/articles/4888558892955-Channel-Size-and-Why-it-Matters"),
    ("T-Mobile — Home Internet Backup plan", "https://www.t-mobile.com/home-internet/plans/5g-backup-internet-options"),
    ("Flent — Introduction and RRUL", "https://flent.org/intro.html"),
]

APPENDIX_REFS = [
    ("ESnet — Network performance expectations", "https://fasterdata.es.net/performance-testing/troubleshooting/network-performance-expectations/"),
    ("ESnet — Test/measurement host tuning", "https://fasterdata.es.net/host-tuning/linux/test-measurement-host-tuning/"),
    ("ESnet — UDP tuning", "https://fasterdata.es.net/host-tuning/linux/udp-tuning/"),
    ("Intel — X710-T2L specifications", "https://www.intel.com/content/www/us/en/products/sku/189463/intel-ethernet-network-adapter-x710t2l/specifications.html"),
    ("Intel — Supported OS matrix for retail Ethernet adapters", "https://www.intel.com/content/www/us/en/support/articles/000025890/ethernet-products.html"),
    ("Intel — X550-T2 specifications", "https://www.intel.com/content/www/us/en/products/sku/88209/intel-ethernet-converged-network-adapter-x550t2/specifications.html"),
    ("Intel — X710-DA2 specifications", "https://www.intel.com/content/www/us/en/products/sku/83964/intel-ethernet-converged-network-adapter-x710da2/specifications.html"),
    ("Intel — Ethernet adapter installation guide", "https://edc.intel.com/content/www/us/en/design/products/ethernet/adapters-and-devices-user-guide/installation/"),
    ("Cisco — 10GBASE SFP+ modules data sheet", "https://www.cisco.com/c/en/us/products/collateral/interfaces-modules/transceiver-modules/data_sheet_c78-455693.html"),
    ("Cisco — Catalyst 9200 hardware guide (10GBASE-T media)", "https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9200/hardware/install/b-c9200-hig/product_overview.pdf"),
]


def draw_refs(g: Guide, refs: list[tuple[str, str]], top: float, appendix: bool = False) -> None:
    c = g.c
    accent = PURPLE if appendix else TEAL_DARK
    y = top
    for idx, (title, url) in enumerate(refs, 1):
        rr(c, 40, y - 36, 712, 32, 6, WHITE, LINE, 0.55)
        c.setFont("Segoe-Bold", 7.5)
        c.setFillColor(accent)
        c.drawString(51, y - 16, f"{idx:02d}")
        c.setFont("Segoe-Bold", 7.6)
        c.setFillColor(NAVY)
        c.drawString(78, y - 15, title)
        shown = url.replace("https://", "")
        c.setFont("Segoe", 6.5)
        c.setFillColor(BLUE)
        c.drawString(78, y - 27, shown)
        c.linkURL(url, (76, y - 31, 742, y - 6), relative=0)
        y -= 39


def draw_ref_columns(g: Guide, refs: list[tuple[str, str]], top: float,
                     appendix: bool = False) -> None:
    c = g.c
    accent = PURPLE if appendix else TEAL_DARK
    midpoint = math.ceil(len(refs) / 2)
    columns = [(refs[:midpoint], 40, 0), (refs[midpoint:], 404, midpoint)]
    for items, x, offset in columns:
        y = top
        for local_idx, (title, url) in enumerate(items, 1):
            rr(c, x, y - 29, 348, 27, 5, WHITE, LINE, 0.5)
            c.setFont("Segoe-Bold", 5.9)
            c.setFillColor(accent)
            c.drawString(x + 9, y - 12, f"{offset + local_idx:02d}")
            c.setFont("Segoe-Bold", 6.15)
            c.setFillColor(NAVY)
            for line_idx, line in enumerate(wrap(title, 298, "Segoe-Bold", 6.15)[:2]):
                c.drawString(x + 31, y - 11 - line_idx * 6.8, line)
            shown = url.replace("https://", "")
            if len(shown) > 82:
                shown = shown[:79] + "…"
            c.setFont("Segoe", 4.45)
            c.setFillColor(BLUE)
            c.drawString(x + 31, y - 24, shown)
            c.linkURL(url, (x + 29, y - 27, x + 339, y - 2), relative=0)
            y -= 33


def page_27(g: Guide) -> None:
    g.begin("Authoritative references — core runbook", "References", "PROVEN BASELINE",
            "Reviewed 30 July 2026. Links are live; re-check vendor matrices and UI paths before use.")
    draw_ref_columns(g, CORE_REFS, 526)
    rr(g.c, 40, 43, 712, 46, 7, NAVY, NAVY)
    g.c.setFont("Segoe-Bold", 7.0)
    g.c.setFillColor(TEAL)
    g.c.drawString(52, 71, "SOURCE-USE BOUNDARY")
    g.c.setFont("Segoe", 6.95)
    g.c.setFillColor(WHITE)
    g.c.drawString(52, 56, "Vendor defaults remain the baseline; server-focused material supplies architecture context, not a Windows 11 client mandate.")
    g.next()


def page_28(g: Guide) -> None:
    g.begin("Authoritative references — adapter, SQM, and scale", "References", "AMY-UNTESTED",
            "Current product examples are capabilities, not endorsements. The appendix remains outside Amy's field evidence.", appendix=True)
    refs = APPENDIX_REFS
    # Fit compact rows in two balanced columns.
    midpoint = math.ceil(len(refs) / 2)
    left = refs[:midpoint]
    right = refs[midpoint:]
    c = g.c
    def col(items, x, width):
        y = 526
        for idx, (title, url) in enumerate(items, 1):
            rr(c, x, y - 39, width, 35, 6, WHITE, LINE, 0.55)
            c.setFont("Segoe-Bold", 6.4)
            c.setFillColor(PURPLE)
            c.drawString(x + 10, y - 15, f"{idx:02d}")
            c.setFont("Segoe-Bold", 6.6)
            c.setFillColor(NAVY)
            title_lines = wrap(title, width - 47, "Segoe-Bold", 6.6)
            for i, line in enumerate(title_lines[:2]):
                c.drawString(x + 34, y - 14 - i * 7.8, line)
            shown = url.replace("https://", "")
            shown_lines = wrap(shown, width - 47, "Segoe", 5.0)
            c.setFont("Segoe", 5.0)
            c.setFillColor(BLUE)
            c.drawString(x + 34, y - 31, shown_lines[0])
            c.linkURL(url, (x + 32, y - 35, x + width - 9, y - 5), relative=0)
            y -= 43
    col(left, 40, 348)
    col(right, 404, 348)
    rr(c, 40, 43, 712, 46, 7, NAVY, NAVY)
    c.setFont("Segoe-Bold", 7.0)
    c.setFillColor(HexColor("#BDA9DC"))
    c.drawString(52, 71, "PUBLICATION CHECKPOINT")
    c.setFont("Segoe", 7.2)
    c.setFillColor(WHITE)
    c.drawString(52, 56, "Verify this PDF against outputs/SHA256SUMS.txt and use the same-version accessible Markdown companion.")
    g.next()


def build(edition: str) -> Path:
    if edition not in {"Pro", "Home"}:
        raise ValueError(f"Unsupported Windows edition: {edition}")
    output = ROOT / "outputs" / (
        f"Windows_11_{edition}_Wired_Network_Performance_Resilience_Runbook_v{VERSION}.pdf"
    )
    register_fonts()
    g = Guide(output, edition=edition, total_pages=TOTAL_PAGES)
    cover(g)
    page_2(g)
    page_3(g)
    page_4(g)
    page_5(g)
    page_6(g)
    page_pcie_install(g)
    page_7(g)
    page_8(g)
    page_9(g)
    page_10(g)
    page_11(g)
    page_12_failover(g)
    page_12(g)
    page_13(g)
    page_14(g)
    page_15(g)
    page_16(g)
    page_17(g)
    page_wifi_evidence(g)
    page_wifi_protocol(g)
    page_18(g)
    page_19(g)
    page_20(g)
    page_21(g)
    page_22(g)
    page_23(g)
    page_24(g)
    page_25(g)
    page_26(g)
    page_27(g)
    page_28(g)
    g.finish()
    return output


if __name__ == "__main__":
    for selected_edition in ("Pro", "Home"):
        print(build(selected_edition))
