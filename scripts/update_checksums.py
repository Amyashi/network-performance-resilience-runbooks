"""Write SHA-256 checksums for the three published PDF artifacts."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
PDFS = (
    "Windows_11_Pro_Wired_Network_Performance_Resilience_Runbook_v1.0.2.pdf",
    "Windows_11_Home_Wired_Network_Performance_Resilience_Runbook_v1.0.2.pdf",
    "macOS_Apple_Silicon_Network_Performance_Resilience_Runbook_v1.0.2.pdf",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    missing = [name for name in PDFS if not (OUTPUTS / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing release PDFs: {', '.join(missing)}")
    lines = [f"{sha256(OUTPUTS / name)}  {name}" for name in PDFS]
    destination = OUTPUTS / "SHA256SUMS.txt"
    destination.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
