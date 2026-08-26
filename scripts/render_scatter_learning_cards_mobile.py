from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageFilter

import render_scatter_learning_cards as base


LABEL_BOOST = 1.08
DESCRIPTION_BOOST = 1.06
DEFAULT_WIDTH = 2880


_draw_stage_badge = base.draw_stage_badge
_draw_label = base.draw_label
_draw_description = base.draw_description


def larger_stage_badge(layer, card, scale):
    return _draw_stage_badge(layer, card, scale * LABEL_BOOST)


def larger_label(layer, item, scale):
    return _draw_label(layer, item, scale * LABEL_BOOST)


def larger_description(layer, card, scale):
    return _draw_description(layer, card, scale * DESCRIPTION_BOOST)


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
    if "--width" not in sys.argv:
        sys.argv.extend(["--width", str(DEFAULT_WIDTH)])
    base.draw_stage_badge = larger_stage_badge
    base.draw_label = larger_label
    base.draw_description = larger_description
    base.main()
    output = argument_value("--output-dir")
    if output:
        finalize_pngs(Path(output))


if __name__ == "__main__":
    main()
