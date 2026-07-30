"""Validate the curated repository and its public release artifacts."""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
REPOSITORY = "Amyashi/network-performance-resilience-runbooks"

PDF_SPECS = {
    "Windows_11_Pro_Wired_Network_Performance_Resilience_Runbook_v1.0.1.pdf": 32,
    "Windows_11_Home_Wired_Network_Performance_Resilience_Runbook_v1.0.1.pdf": 32,
    "macOS_Apple_Silicon_Network_Performance_Resilience_Runbook_v1.0.1.pdf": 26,
}

ACCESSIBLE_SPECS = {
    "docs/WINDOWS_11_PRO_ACCESSIBLE_GUIDE.md": (
        32,
        (
            "approximately 3.8-3.9 Gbps",
            "Prevent Wi-Fi when on Ethernet",
            "5/5 and 10/10 Gbps",
        ),
        ("Home in S mode", "fake gpedit packages"),
    ),
    "docs/WINDOWS_11_HOME_ACCESSIBLE_GUIDE.md": (
        32,
        (
            "approximately 3.8-3.9 Gbps",
            "no supported Local Group Policy equivalent",
            "5/5 and 10/10 Gbps",
        ),
        (
            "gpedit.msc",
            "Prevent Wi-Fi when on Ethernet",
            "gpupdate /force",
        ),
    ),
    "docs/MACOS_APPLE_SILICON_ACCESSIBLE_GUIDE.md": (
        26,
        (
            "direct M1 Pro host failover",
            "networkQuality",
            "5/5 and 10/10 Gbps",
        ),
        ("PsPing", "gpedit.msc", "Windows Connection Manager"),
    ),
}

REQUIRED_FILES = {
    ".gitattributes",
    ".gitignore",
    ".github/CODEOWNERS",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/guide_problem.yml",
    ".github/ISSUE_TEMPLATE/improvement.yml",
    ".github/dependabot.yml",
    ".github/pull_request_template.md",
    ".github/workflows/validate.yml",
    "ACCESSIBILITY.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "LICENSE.md",
    "README.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "docs/EVIDENCE_AND_SOURCES.md",
    "licenses/REPORTLAB.txt",
    "requirements.txt",
    "scripts/update_checksums.py",
    "scripts/validate_public_release.py",
    "src/build_accessible_guides.py",
    "src/build_guide.py",
    "src/build_macos_guide.py",
    "tools/make_contact_sheets.py",
    "tools/qa_pdfs.py",
    "outputs/SHA256SUMS.txt",
    *ACCESSIBLE_SPECS,
    *(f"outputs/{name}" for name in PDF_SPECS),
}

TEXT_SUFFIXES = {
    ".cff",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}

PRIVATE_PATTERNS = (
    (re.compile(r"chatgpt\.com/c/", re.I), "private ChatGPT URL"),
    (re.compile(r"\bsource_thread_id\b", re.I), "private thread identifier"),
    (re.compile(r"\bcodex-clipboard-[A-Za-z0-9-]+\b", re.I), "clipboard filename"),
    (re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+", re.I), "personal Windows path"),
    (re.compile(r"/" + r"Users/[^/\s]+", re.I), "personal macOS path"),
    (re.compile(r"\bturn\d+(?:search|view|fetch)\d+\b", re.I), "internal source token"),
    (re.compile(r"\brepresentative fireplace\b", re.I), "private room label"),
    (re.compile(r"\boffice node\b", re.I), "private room label"),
    (re.compile(r"\bwork M1 Pro MacBook Pro\b", re.I), "employment/device context"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tracked_files() -> set[str]:
    command = [
        "git",
        "-c",
        f"safe.directory={ROOT.as_posix()}",
        "ls-files",
    ]
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return {line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()}


def outline_count(items: object) -> int:
    if not isinstance(items, list):
        return 0
    return sum(outline_count(item) if isinstance(item, list) else 1 for item in items)


def check_pdf(path: Path, expected_pages: int, errors: list[str]) -> None:
    reader = PdfReader(path)
    if len(reader.pages) != expected_pages:
        errors.append(f"{path}: {len(reader.pages)} pages; expected {expected_pages}")
    metadata = reader.metadata or {}
    if metadata.get("/Author") != "Amyashi":
        errors.append(f"{path}: PDF author must be Amyashi")
    if not metadata.get("/Title"):
        errors.append(f"{path}: missing PDF title")
    root = reader.trailer["/Root"]
    if str(root.get("/Lang", "")) != "en-US":
        errors.append(f"{path}: document language is not en-US")
    try:
        if outline_count(reader.outline) < expected_pages - 2:
            errors.append(f"{path}: insufficient section bookmarks")
    except Exception as exc:  # pragma: no cover - defensive parsing guard
        errors.append(f"{path}: could not read bookmarks: {exc}")

    for key in ("/OpenAction", "/AA"):
        if root.get(key):
            errors.append(f"{path}: active catalog entry {key} is not allowed")
    names = root.get("/Names")
    if names:
        names = names.get_object()
        for key in ("/EmbeddedFiles", "/JavaScript"):
            if names.get(key):
                errors.append(f"{path}: catalog name tree {key} is not allowed")

    for index, page in enumerate(reader.pages, 1):
        if page.get("/AA"):
            errors.append(f"{path}: page {index} has additional actions")
        for reference in page.get("/Annots") or []:
            annotation = reference.get_object()
            subtype = str(annotation.get("/Subtype", ""))
            if subtype != "/Link":
                errors.append(f"{path}: page {index} has unexpected annotation {subtype}")
            action = annotation.get("/A")
            if action and str(action.get("/S", "")) not in {"/URI", "/GoTo"}:
                errors.append(
                    f"{path}: page {index} has disallowed action {action.get('/S')}"
                )

    metadata_text = "\n".join(str(value) for value in metadata.values())
    for pattern, label in PRIVATE_PATTERNS:
        if pattern.search(metadata_text):
            errors.append(f"{path}: {label} in PDF metadata")


def check_checksums(errors: list[str]) -> None:
    path = OUTPUTS / "SHA256SUMS.txt"
    if not path.is_file():
        errors.append("outputs/SHA256SUMS.txt is missing")
        return
    found: dict[str, str] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\s]+)", line)
        if not match:
            errors.append(f"outputs/SHA256SUMS.txt: malformed line {line!r}")
            continue
        found[match.group(2)] = match.group(1)
    if set(found) != set(PDF_SPECS):
        errors.append("outputs/SHA256SUMS.txt does not cover exactly the three release PDFs")
        return
    for name, expected in found.items():
        actual = sha256(OUTPUTS / name)
        if actual != expected:
            errors.append(f"outputs/{name}: checksum mismatch")


def check_accessible_guides(errors: list[str]) -> None:
    for relative, (expected_pages, phrases, forbidden) in ACCESSIBLE_SPECS.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"{relative}: missing accessible companion")
            continue
        text = path.read_text(encoding="utf-8")
        pages = len(re.findall(r"^## Page \d+:", text, flags=re.MULTILINE))
        if pages != expected_pages:
            errors.append(f"{relative}: {pages} page sections; expected {expected_pages}")
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{relative}: missing phrase {phrase!r}")
        for phrase in forbidden:
            if phrase in text:
                errors.append(f"{relative}: forbidden phrase present {phrase!r}")
        if "End of accessible companion." not in text:
            errors.append(f"{relative}: incomplete ending")


def check_relative_links(errors: list[str]) -> None:
    for relative in ("README.md", "ACCESSIBILITY.md", "CONTRIBUTING.md", "LICENSE.md"):
        text = (ROOT / relative).read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            target = target.strip("<>")
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            file_part = target.split("#", 1)[0]
            if file_part and not (ROOT / file_part).exists():
                errors.append(f"{relative}: broken relative link {target}")


def main() -> int:
    errors: list[str] = []
    try:
        tracked = tracked_files()
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: could not enumerate tracked files: {exc}", file=sys.stderr)
        return 1

    missing = sorted(REQUIRED_FILES - tracked)
    if missing:
        errors.append("required tracked files missing: " + ", ".join(missing))
    if "RELEASE_CHECKLIST.md" in tracked:
        errors.append("RELEASE_CHECKLIST.md contains pre-publication decisions and must not be published")
    for relative in tracked:
        lowered = relative.lower()
        if lowered.startswith(("work/", "private/", "evidence/raw/", "evidence/private/")):
            errors.append(f"{relative}: private or generated path is tracked")
        if Path(relative).suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".zip", ".7z"}:
            errors.append(f"{relative}: screenshot/archive artifact is tracked")

    tracked_pdfs = {Path(path).name for path in tracked if path.lower().endswith(".pdf")}
    if tracked_pdfs != set(PDF_SPECS):
        errors.append("tracked PDF set must contain exactly the three versioned release PDFs")

    for relative in sorted(tracked):
        path = ROOT / relative
        if path.suffix.lower() not in TEXT_SUFFIXES or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern, label in PRIVATE_PATTERNS:
            if pattern.search(text):
                errors.append(f"{relative}: {label}")

    license_text = (ROOT / "LICENSE.md").read_text(encoding="utf-8") if (ROOT / "LICENSE.md").exists() else ""
    normalized_license = " ".join(license_text.split())
    for phrase in (
        "Creative Commons Attribution-NonCommercial-NoDerivatives 4.0",
        "Code and automation",
        "Contribution-only permission",
        REPOSITORY,
    ):
        if phrase not in normalized_license:
            errors.append(f"LICENSE.md: missing {phrase!r}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    if "No public license has been selected" in readme:
        errors.append("README.md still says that no public license is selected")
    if REPOSITORY not in readme:
        errors.append("README.md does not identify the canonical repository")

    source_text = "\n".join(
        (ROOT / relative).read_text(encoding="utf-8")
        for relative in ("src/build_guide.py", "src/build_macos_guide.py")
    )
    if "C:\\Windows\\Fonts" in source_text or "TTFont" in source_text:
        errors.append("builders still depend on proprietary operating-system font files")
    for alias in ("Helvetica", "Courier"):
        if alias not in source_text:
            errors.append(f"builders do not declare Base 14 {alias}")

    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    for line in requirements.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not re.fullmatch(r"[A-Za-z0-9_.-]+==[A-Za-z0-9_.+-]+", line):
            errors.append(f"requirements.txt: dependency is not directly pinned: {line!r}")

    for name, pages in PDF_SPECS.items():
        path = OUTPUTS / name
        if not path.is_file():
            errors.append(f"outputs/{name}: missing release PDF")
        else:
            check_pdf(path, pages, errors)

    check_checksums(errors)
    check_accessible_guides(errors)
    if all((ROOT / name).exists() for name in ("README.md", "ACCESSIBILITY.md", "CONTRIBUTING.md", "LICENSE.md")):
        check_relative_links(errors)

    if errors:
        print("Public release validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Public release validation: PASS")
    print(f"- tracked files: {len(tracked)}")
    print(f"- release PDFs: {len(PDF_SPECS)}")
    print(f"- accessible companions: {len(ACCESSIBLE_SPECS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
