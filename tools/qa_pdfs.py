"""Run structural, textual, link, and bounds checks against release PDFs."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
SPECS = {
    "Windows_11_Pro_Wired_Network_Performance_Resilience_Runbook_v1.0.1.pdf": {
        "pages": 32,
        "required": [
            "Windows 11 Pro Wired Network Performance & Resilience Runbook",
            "Install or replace a PCIe Ethernet adapter safely",
            "Historical Amy configuration - field record, not a baseline",
            "Do not include drivers with Windows Updates",
            "Prevent Wi-Fi when on Ethernet",
            "Amy's Windows 11 Pro failover field record",
            "Two tested failover layers, one T-Mobile backup",
            "Amy's eero radio record: healthy, no change",
            "approximately 3.8-3.9 Gbps validation",
            "5/5 and 10/10 Gbps",
            "Release integrity",
        ],
        "forbidden": ["Home in S mode", "fake gpedit packages"],
    },
    "Windows_11_Home_Wired_Network_Performance_Resilience_Runbook_v1.0.1.pdf": {
        "pages": 32,
        "required": [
            "Windows 11 Home Wired Network Performance & Resilience Runbook",
            "Install or replace a PCIe Ethernet adapter safely",
            "Historical Amy configuration - field record, not a baseline",
            "Home in S mode",
            "no supported Local Group Policy equivalent",
            "What Amy's Pro field record does not prove on Home",
            "Two tested failover layers, one T-Mobile backup",
            "Amy's eero radio record: healthy, no change",
            "approximately 3.8-3.9 Gbps validation",
            "5/5 and 10/10 Gbps",
            "Release integrity",
        ],
        "forbidden": [
            "gpedit.msc",
            "Prevent Wi-Fi when on Ethernet",
            "gpupdate /force",
            "Do not include drivers with Windows Updates",
        ],
    },
    "macOS_Apple_Silicon_Network_Performance_Resilience_Runbook_v1.0.1.pdf": {
        "pages": 26,
        "required": [
            "macOS Network Performance & Resilience Runbook",
            "Amy's tested resilience topology",
            "Reproduce direct Mac failover and failback",
            "networkQuality",
            "Amy's eero radio record: healthy, no change",
            "macOS throughput methods at 2/2, 5/5, and 10/10: Amy-untested",
            "M1 Pro adapter and Intel-card reality check",
            "Release integrity",
        ],
        "forbidden": ["PsPing", "gpedit.msc", "Windows Connection Manager"],
    },
}

BAD_HYPHENS = {
    "\u2010": "HYPHEN",
    "\u2011": "NON-BREAKING HYPHEN",
    "\u2012": "FIGURE DASH",
    "\u2013": "EN DASH",
    "\u2014": "EM DASH",
    "\u2212": "MINUS SIGN",
}


def all_page_text(reader: PdfReader) -> tuple[list[str], str]:
    pages = [(page.extract_text() or "") for page in reader.pages]
    return pages, "\n".join(pages)


def link_urls(reader: PdfReader) -> list[str]:
    urls: list[str] = []
    for page in reader.pages:
        annotations = page.get("/Annots") or []
        for annotation_ref in annotations:
            annotation = annotation_ref.get_object()
            action = annotation.get("/A")
            if action and action.get("/URI"):
                urls.append(str(action["/URI"]))
    return urls


def check_one(path: Path, spec: dict) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    reader = PdfReader(str(path))
    pages, text = all_page_text(reader)
    expected_pages = spec["pages"]

    if len(reader.pages) != expected_pages:
        errors.append(f"page count {len(reader.pages)} != {expected_pages}")
    title = str((reader.metadata or {}).get("/Title", ""))
    if not title:
        errors.append("missing PDF title metadata")
    if str((reader.metadata or {}).get("/Author", "")) != "Amyashi":
        errors.append("PDF author metadata is not Amyashi")
    if str((reader.metadata or {}).get("/Creator", "")) != (
        "Amyashi network-performance-resilience-runbooks build system"
    ):
        errors.append("PDF creator metadata is not the canonical build system")
    if str(reader.trailer["/Root"].get("/Lang", "")) != "en-US":
        errors.append("PDF document language is not en-US")

    for index, page in enumerate(reader.pages, 1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        if abs(width - 792) > 0.5 or abs(height - 612) > 0.5:
            errors.append(f"page {index}: size {width}x{height}, expected 792x612")
        if not pages[index - 1].strip():
            errors.append(f"page {index}: no extractable text")
        marker = f"{index} / {expected_pages}"
        if marker not in pages[index - 1]:
            errors.append(f"page {index}: missing page marker {marker!r}")

    for phrase in spec["required"]:
        if phrase not in text:
            errors.append(f"required phrase missing: {phrase!r}")
    for phrase in spec["forbidden"]:
        if phrase in text:
            errors.append(f"forbidden phrase present: {phrase!r}")

    for char, name in BAD_HYPHENS.items():
        count = text.count(char)
        if count:
            errors.append(f"{name} U+{ord(char):04X}: {count}")

    forbidden_patterns = [
        (r"\bturn\d+(?:search|view|fetch)\d+\b", "internal source reference"),
        (r"chatgpt\.com/c/", "private chat URL"),
        (r"\bsource_thread_id\b", "private thread identifier"),
        (r"\bcodex-clipboard-[A-Za-z0-9-]+\b", "temporary clipboard asset"),
        (r"[A-Za-z]:\\Users\\[^\\\s]+", "personal Windows path"),
        (r"\brepresentative fireplace\b", "private room label"),
        (r"\boffice node\b", "private room label"),
        (r"\bwork M1 Pro MacBook Pro\b", "employment/device context"),
    ]
    for pattern, label in forbidden_patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"{label} present")

    urls = link_urls(reader)
    if not urls:
        errors.append("no link annotations")
    insecure = [url for url in urls if not url.startswith("https://")]
    if insecure:
        errors.append(f"non-HTTPS links: {insecure}")
    duplicate_count = len(urls) - len(set(urls))
    if duplicate_count:
        warnings.append(f"{duplicate_count} duplicate link annotations")

    with pdfplumber.open(path) as document:
        for index, page in enumerate(document.pages, 1):
            for char in page.chars:
                if char["x0"] < -0.5 or char["x1"] > page.width + 0.5:
                    errors.append(f"page {index}: horizontal glyph out of bounds")
                    break
                if char["top"] < -0.5 or char["bottom"] > page.height + 0.5:
                    errors.append(f"page {index}: vertical glyph out of bounds")
                    break

    if re.search(r"\b\d+\s*/\s*(?:25|27|28|29|30|31)\b", text):
        warnings.append("possible stale alternate page-count marker")

    return {
        "file": path.name,
        "size_bytes": path.stat().st_size,
        "pages": len(reader.pages),
        "metadata_title": title,
        "links": len(urls),
        "unique_links": len(set(urls)),
        "errors": errors,
        "warnings": warnings,
        "status": "PASS" if not errors else "FAIL",
    }


def main() -> int:
    results = []
    for filename, spec in SPECS.items():
        path = OUTPUTS / filename
        if not path.exists():
            results.append({"file": filename, "status": "FAIL", "errors": ["file missing"], "warnings": []})
            continue
        results.append(check_one(path, spec))
    report = {"results": results, "status": "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL"}
    report_path = ROOT / "work" / "final_qa.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
