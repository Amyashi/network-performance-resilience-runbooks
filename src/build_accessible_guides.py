"""Build synchronized, reflowable Markdown companions for all three runbooks."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterable

import build_guide as windows
import build_macos_guide as macos


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

WINDOWS_PRO = DOCS / "WINDOWS_11_PRO_ACCESSIBLE_GUIDE.md"
WINDOWS_HOME = DOCS / "WINDOWS_11_HOME_ACCESSIBLE_GUIDE.md"
MACOS = DOCS / "MACOS_APPLE_SILICON_ACCESSIBLE_GUIDE.md"


def clean(value: object) -> str:
    return windows.normalize_pdf_text(str(value)).strip()


class NullCanvas:
    """Accept direct drawing calls while preserving meaningful text."""

    def __init__(self, guide: "MarkdownGuide") -> None:
        self.guide = guide

    def drawString(self, _x: float, _y: float, text: object, *_args, **_kwargs) -> None:
        self.guide.capture_direct_text(text)

    drawCentredString = drawString
    drawRightString = drawString

    def __getattr__(self, _name: str):
        return lambda *_args, **_kwargs: None


class MarkdownGuide:
    """Record the canonical page functions as structured Markdown."""

    def __init__(
        self,
        *,
        edition: str,
        title: str,
        total_pages: int,
        destination: Path,
        evidence_boundary: Iterable[str],
    ) -> None:
        self.edition = edition
        self.title = title
        self.total_pages = total_pages
        self.destination = destination
        self.page_no = 0
        display_edition = (
            f"Windows 11 {edition}"
            if edition in {"Home", "Pro"}
            else "macOS on Apple silicon"
        )
        self.lines: list[str] = [
            f"# {title}",
            "",
            f"**Edition:** {display_edition}",
            f"**Version:** {windows.VERSION}",
            f"**Release date:** {windows.RELEASE_DATE_LONG}",
            "**Author:** Amyashi",
            "",
            "> This is the substantive, reflowable companion to the matching PDF. "
            "It preserves the implementation sequence, safety boundaries, commands, "
            "validation gates, rollback guidance, and references. The PDF remains the "
            "designed visual edition.",
            "",
            "## Evidence boundary",
            "",
        ]
        for item in evidence_boundary:
            self.lines.extend([f"- {clean(item)}"])
        self.lines.extend(
            [
                "",
                "Evidence labels are part of the instructions. Do not present an "
                "Amy-untested method or controlled experiment as Amy's field result.",
                "",
                "Guide materials are licensed as described in "
                "[LICENSE.md](../LICENSE.md). Modified or checksum-mismatched copies "
                "are outside the supported release.",
                "",
            ]
        )
        self.c = NullCanvas(self)
        self._metric_heading_page = 0
        self._direct_heading_page = 0

    def cover(self, summary: str) -> None:
        self.page_no += 1
        self.lines.extend(
            [
                f"## Page {self.page_no}: Cover and scope",
                "",
                clean(summary),
                "",
            ]
        )

    def add_bookmark(self, _title: str) -> None:
        return None

    def begin(
        self,
        title: str,
        section: str,
        label: str | None = None,
        subtitle: str | None = None,
        appendix: bool = False,
    ) -> None:
        self.page_no += 1
        self._metric_heading_page = 0
        self._direct_heading_page = 0
        self.lines.extend(
            [
                "---",
                "",
                f"## Page {self.page_no}: {clean(title)}",
                "",
                f"**Section:** {clean(section)}",
            ]
        )
        if label:
            self.lines.append(f"**Evidence state:** {clean(label)}")
        if appendix:
            self.lines.append(
                "**Appendix boundary:** Documentation-backed and not field-tested by Amy."
            )
        self.lines.append("")
        if subtitle:
            self.lines.extend([clean(subtitle), ""])

    def add_divider(
        self,
        *,
        title: str,
        label: str,
        summary: Iterable[str],
    ) -> None:
        self.page_no += 1
        self.lines.extend(
            [
                "---",
                "",
                f"## Page {self.page_no}: {clean(title)}",
                "",
                f"**Evidence state:** {clean(label)}",
                "",
            ]
        )
        for item in summary:
            self.lines.extend([clean(item), ""])

    def add_references(
        self,
        *,
        title: str,
        label: str,
        subtitle: str,
        references: Iterable[tuple[str, str]],
        boundary: str,
    ) -> None:
        self.begin(title, "References", label, subtitle, appendix=label == "AMY-UNTESTED")
        for name, url in references:
            self.lines.append(f"- [{clean(name)}]({url})")
        self.lines.extend(["", f"**Source-use boundary:** {clean(boundary)}", ""])

    def badge(self, *_args, **_kwargs):
        return (0.0, 0.0)

    def metric(
        self,
        _x: float,
        _y: float,
        _w: float,
        _h: float,
        number: str,
        caption: str,
        *_args,
        **_kwargs,
    ) -> None:
        if self._metric_heading_page != self.page_no:
            self.lines.extend(["### Key measurements", ""])
            self._metric_heading_page = self.page_no
        self.lines.append(f"- **{clean(number)}:** {clean(caption)}")
        self.lines.append("")

    def capture_direct_text(self, text: object) -> None:
        value = clean(text)
        if not value:
            return
        if self._direct_heading_page != self.page_no:
            self.lines.extend(["### Decision path", ""])
            self._direct_heading_page = self.page_no
        self.lines.append(f"- {value}")

    def card(
        self,
        _x: float,
        _top: float,
        _w: float,
        _h: float,
        title: str,
        blocks: list[dict],
        label: str | None = None,
        **_kwargs,
    ) -> None:
        self.lines.extend([f"### {clean(title)}", ""])
        if label:
            self.lines.extend([f"**Evidence state:** {clean(label)}", ""])
        self.render_blocks(blocks)

    def render_blocks(self, blocks: list[dict]) -> None:
        for block in blocks:
            kind = block.get("type", "p")
            if kind == "gap":
                continue
            if kind == "rule":
                self.lines.extend(["---", ""])
                continue
            text = clean(block.get("text", ""))
            if kind == "label":
                self.lines.extend([f"**{text.upper()}**", ""])
            elif kind == "p":
                self.lines.extend([text, ""])
            elif kind == "bullet":
                self.lines.extend([f"- {text}", ""])
            elif kind == "step":
                self.lines.extend([f"{block.get('n', '')}. {text}", ""])
            elif kind == "check":
                self.lines.extend([f"- [ ] {text}", ""])
            elif kind == "code":
                language = "powershell" if self.edition in {"Home", "Pro"} else "bash"
                self.lines.extend([f"```{language}", text, "```", ""])
            else:
                raise ValueError(f"Unknown block type: {kind}")

    def action_strip(
        self,
        items: list[tuple[str, str, str]],
        *_args,
        **_kwargs,
    ) -> None:
        self.lines.extend(["### Decision gate", ""])
        for heading, text, status in items:
            self.lines.extend(
                [f"- **{clean(heading)} [{clean(status).upper()}]:** {clean(text)}", ""]
            )

    def next(self) -> None:
        return None

    def finish(self) -> Path:
        if self.page_no != self.total_pages:
            raise RuntimeError(
                f"{self.edition}: expected {self.total_pages} pages, recorded {self.page_no}"
            )
        self.lines.extend(
            [
                "---",
                "",
                "End of accessible companion.",
                "",
            ]
        )
        self.destination.parent.mkdir(parents=True, exist_ok=True)
        self.destination.write_text("\n".join(self.lines), encoding="utf-8", newline="\n")
        return self.destination


def run_pages(guide: MarkdownGuide, pages: Iterable[Callable[[MarkdownGuide], None]]) -> None:
    for page in pages:
        page(guide)


def build_windows(edition: str) -> Path:
    if edition not in {"Pro", "Home"}:
        raise ValueError(f"Unsupported Windows edition: {edition}")
    destination = WINDOWS_PRO if edition == "Pro" else WINDOWS_HOME
    title = f"Windows 11 {edition} Wired Network Performance & Resilience Runbook"
    guide = MarkdownGuide(
        edition=edition,
        title=title,
        total_pages=windows.TOTAL_PAGES,
        destination=destination,
        evidence_boundary=[
            "Amy field-validated a 2 Gbps upload / 2 Gbps download Windows path and approximately 3.8-3.9 Gbps simultaneous aggregate application throughput in the recorded environment.",
            "Amy field-validated Windows 11 Pro direct-host failover and eero Internet Backup through the same T-Mobile Home Backup Internet service.",
            "The 5/5 and 10/10 Gbps appendix is documentation-backed and Amy-untested.",
            (
                "Windows 11 Pro uses supported Local Group Policy where specified."
                if edition == "Pro"
                else "Windows 11 Home does not gain Pro-only Local Group Policy behavior from unsupported workarounds."
            ),
        ],
    )
    guide.cover(
        "Implementation-first Windows wired-network baseline, multi-gigabit "
        "validation, latency testing, Wi-Fi context, and failover runbook."
    )
    run_pages(
        guide,
        [
            windows.page_2,
            windows.page_3,
            windows.page_4,
            windows.page_5,
            windows.page_6,
            windows.page_pcie_install,
            windows.page_7,
            windows.page_8,
            windows.page_9,
            windows.page_10,
            windows.page_11,
            windows.page_12_failover,
            windows.page_12,
            windows.page_13,
            windows.page_14,
            windows.page_15,
            windows.page_16,
            windows.page_17,
            windows.page_wifi_evidence,
            windows.page_wifi_protocol,
            windows.page_18,
            windows.page_19,
            windows.page_20,
            windows.page_21,
        ],
    )
    guide.add_divider(
        title="5/5 and 10/10 Gbps stress-test method",
        label="AMY-UNTESTED",
        summary=[
            "This separate scaling appendix is an authoritative-documentation baseline, not an Amy field result, product endorsement, or line-rate guarantee.",
            "Do not scale the 2/2 settings by multiplication. Clear endpoint CPU, PCIe, switch fabric, router full-duplex capacity, media, driver support, thermal, and controlled-server gates locally first.",
        ],
    )
    run_pages(
        guide,
        [
            windows.page_23,
            windows.page_24,
            windows.page_25,
            windows.page_26,
        ],
    )
    guide.add_references(
        title="Authoritative references - core runbook",
        label="PROVEN BASELINE",
        subtitle="Reviewed 30 July 2026. Re-check vendor matrices and UI paths before use.",
        references=windows.CORE_REFS,
        boundary="Vendor defaults remain the baseline; server-focused material supplies architecture context, not a Windows 11 client mandate.",
    )
    guide.add_references(
        title="Authoritative references - adapter, SQM, and scale",
        label="AMY-UNTESTED",
        subtitle="Product examples are capability references, not endorsements.",
        references=windows.APPENDIX_REFS,
        boundary="Verify the same-version PDF against outputs/SHA256SUMS.txt before use.",
    )
    return guide.finish()


def build_macos() -> Path:
    title = "macOS Apple Silicon Network Performance & Resilience Runbook"
    guide = MarkdownGuide(
        edition="macOS",
        title=title,
        total_pages=macos.TOTAL_PAGES,
        destination=MACOS,
        evidence_boundary=[
            "Amy field-validated direct M1 Pro host failover and eero Internet Backup through the same T-Mobile Home Backup Internet service.",
            "Those two recovery controls share a carrier, gateway, power, radio, and plan failure domain; they are not carrier-diverse redundancy.",
            "macOS throughput methods at 2/2, 5/5, and 10/10 Gbps are documentation-backed and Amy-untested.",
            "Service order ranks active network services; it does not reproduce the Windows Pro policy or preserve established sessions.",
        ],
    )
    guide.cover(
        "Implementation-first Apple-silicon network baseline, direct-host and "
        "eero-wide failover, Wi-Fi context, and multi-gigabit validation methods."
    )
    run_pages(
        guide,
        [
            macos.page_2,
            macos.page_3,
            macos.page_4,
            macos.page_5,
            macos.page_6,
            macos.page_7,
            macos.page_8,
            macos.page_9,
            macos.page_10,
            macos.page_11,
            macos.page_12,
            macos.page_13,
            macos.page_14,
            macos.page_15,
            macos.page_wifi_evidence,
            macos.page_wifi_protocol,
            macos.page_18,
            macos.page_19,
        ],
    )
    guide.add_divider(
        title="5/5 and 10/10 Gbps Apple-silicon stress-test method",
        label="AMY-UNTESTED",
        summary=[
            "This separate appendix is documentation-backed and was not field-tested by Amy on the M1 Pro MacBook Pro.",
            "A Thunderbolt label is not Ethernet throughput proof. The adapter, enclosure, driver, shared bus, switch, router, media, endpoint CPU, thermals, and test server all remain gates.",
        ],
    )
    run_pages(
        guide,
        [
            macos.page_21,
            macos.page_22,
            macos.page_23,
            macos.page_24,
        ],
    )
    guide.add_references(
        title="Authoritative references - macOS and core method",
        label="PROVEN BASELINE",
        subtitle="Reviewed 30 July 2026. Re-check macOS UI, managed-device policy, and vendor support.",
        references=macos.CORE_REFS,
        boundary="Apple and eero define documented behavior; Amy's field record retains its separate evidence status.",
    )
    guide.add_references(
        title="Authoritative references - scaling and hardware",
        label="AMY-UNTESTED",
        subtitle="Hardware examples are compatibility checkpoints, not purchase endorsements.",
        references=macos.SCALE_REFS,
        boundary="Verify the same-version PDF against outputs/SHA256SUMS.txt before use.",
    )
    return guide.finish()


def main() -> int:
    for edition in ("Pro", "Home"):
        print(build_windows(edition))
    print(build_macos())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
