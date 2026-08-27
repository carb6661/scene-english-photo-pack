from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageFilter

import render_scatter_learning_cards as base


DEFAULT_WIDTH = 2880
LABEL_SCALE = 1.20
BADGE_SCALE = 1.10
DESCRIPTION_SCALE = 1.14


def ensure_argument(flag: str, value: str) -> None:
    if flag not in sys.argv:
        sys.argv.extend([flag, value])


def argument_value(flag: str) -> str | None:
    try:
        return sys.argv[sys.argv.index(flag) + 1]
    except (ValueError, IndexError):
        return None


def finalize_pngs(output_dir: Path) -> None:
    for path in sorted(output_dir.glob("card-*.png")):
        image = Image.open(path).convert("RGB")
        image = image.filter(ImageFilter.UnsharpMask(radius=0.7, percent=35, threshold=2))
        image.save(path, format="PNG", compress_level=3, dpi=(300, 300))


def main() -> None:
    ensure_argument("--width", str(DEFAULT_WIDTH))
    ensure_argument("--label-scale", str(LABEL_SCALE))
    ensure_argument("--badge-scale", str(BADGE_SCALE))
    ensure_argument("--description-scale", str(DESCRIPTION_SCALE))
    base.main()
    output = argument_value("--output-dir")
    if output:
        finalize_pngs(Path(output))


if __name__ == "__main__":
    main()
