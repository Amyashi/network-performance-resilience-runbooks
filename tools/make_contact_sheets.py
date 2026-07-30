"""Create compact contact sheets from Poppler-rendered PDF pages."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


thumb_w, thumb_h = 396, 306
cols, rows = 2, 4
per_sheet = cols * rows

def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--render-root",
        type=Path,
        default=project_root / "work" / "final_render",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=project_root / "work" / "final_contact_sheets",
    )
    args = parser.parse_args()

    for edition in ("pro", "home", "mac"):
        pages = sorted((args.render_root / edition).glob("page-*.png"))
        if not pages:
            raise FileNotFoundError(f"No rendered pages found for {edition}")
        out = args.output_root / edition
        out.mkdir(parents=True, exist_ok=True)
        for sheet_index in range((len(pages) + per_sheet - 1) // per_sheet):
            selected = pages[sheet_index * per_sheet:(sheet_index + 1) * per_sheet]
            sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + 18)), "white")
            draw = ImageDraw.Draw(sheet)
            for idx, path in enumerate(selected):
                with Image.open(path) as source:
                    image = source.convert("RGB")
                image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                x = (idx % cols) * thumb_w
                y = (idx // cols) * (thumb_h + 18)
                sheet.paste(image, (x, y))
                draw.text((x + 5, y + thumb_h + 2), path.stem, fill="#243B53")
            sheet.save(out / f"sheet-{sheet_index + 1:02d}.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
