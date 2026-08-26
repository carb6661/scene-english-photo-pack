from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont


FONT_EN_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_EN = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_ZH = Path(r"C:\Windows\Fonts\msyh.ttc")
PAPER = (252, 251, 247, 255)
INK = (11, 13, 13, 255)
WHITE = (255, 255, 255, 255)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render six scattered bilingual learning cards.")
    parser.add_argument("--photo", type=Path, required=True, help="Clean photo with all UI already removed")
    parser.add_argument("--content", type=Path, required=True, help="UTF-8 six-card JSON")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--width", type=int, default=2160)
    return parser.parse_args()


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.exists():
        raise SystemExit(f"Required font not found: {path}")
    return ImageFont.truetype(str(path), max(12, size))


def text_box(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int, int, int]:
    return draw.textbbox((0, 0), text, font=font)


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    box = text_box(draw, text, font)
    return box[2] - box[0]


def overlap_ratio(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    if x2 <= x1 or y2 <= y1:
        return 0.0
    intersection = (x2 - x1) * (y2 - y1)
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    return intersection / min(area_a, area_b)


def draw_stage_badge(layer: Image.Image, card: dict, scale: float) -> tuple[int, int, int, int]:
    draw = ImageDraw.Draw(layer)
    number = int(card["number"])
    title_en = str(card.get("title_en", "")).strip()
    title_zh = str(card.get("title", "")).strip()
    top = f"{number:02d}/06  {title_en}"
    bottom = f"图{number} · {title_zh}"
    en_font = load_font(FONT_EN_BOLD, round(22 * scale))
    zh_font = load_font(FONT_ZH, round(20 * scale))
    pad_x, pad_y = round(12 * scale), round(7 * scale)
    x, y = round(40 * scale), round(36 * scale)
    top_box = text_box(draw, top, en_font)
    bottom_box = text_box(draw, bottom, zh_font)
    box_w = max(top_box[2] - top_box[0], bottom_box[2] - bottom_box[0]) + pad_x * 2
    top_h = top_box[3] - top_box[1] + pad_y * 2
    bottom_h = bottom_box[3] - bottom_box[1] + pad_y * 2
    shadow = max(2, round(3 * scale))
    draw.rectangle((x + shadow, y + shadow, x + box_w + shadow, y + top_h + bottom_h + shadow), fill=(0, 0, 0, 70))
    draw.rectangle((x, y, x + box_w, y + top_h), fill=PAPER)
    draw.rectangle((x, y + top_h, x + box_w, y + top_h + bottom_h), fill=INK)
    draw.text((x + pad_x, y + pad_y - top_box[1]), top, font=en_font, fill=INK)
    draw.text((x + pad_x, y + top_h + pad_y - bottom_box[1]), bottom, font=zh_font, fill=WHITE)
    return x, y, x + box_w, y + top_h + bottom_h


def draw_label(layer: Image.Image, item: dict, scale: float) -> tuple[int, int, int, int]:
    draw = ImageDraw.Draw(layer)
    canvas_w, canvas_h = layer.size
    x = round(float(item["x"]) * canvas_w)
    y = round(float(item["y"]) * canvas_h)
    en = str(item["en"]).strip()
    zh = str(item["zh"]).strip()
    ipa = str(item.get("ipa", "")).strip()
    max_w = round(float(item.get("max_width", 0.48)) * canvas_w)
    current = max(18, int(item.get("font_size", 27)))
    pad_x = round(12 * scale)
    pad_y = round(7 * scale)
    gap = round(9 * scale) if ipa else 0

    while True:
        en_font = load_font(FONT_EN_BOLD, round(current * scale))
        ipa_font = load_font(FONT_EN, round(max(17, current - 5) * scale))
        zh_font = load_font(FONT_ZH, round(max(19, current - 3) * scale))
        en_w = text_width(draw, en, en_font)
        ipa_w = text_width(draw, ipa, ipa_font) if ipa else 0
        zh_w = text_width(draw, zh, zh_font)
        box_w = max(en_w + gap + ipa_w, zh_w) + pad_x * 2
        if box_w <= max_w or current <= 18:
            break
        current -= 1

    en_box = text_box(draw, en, en_font)
    ipa_box = text_box(draw, ipa, ipa_font) if ipa else (0, 0, 0, 0)
    zh_box = text_box(draw, zh, zh_font)
    top_h = max(en_box[3] - en_box[1], ipa_box[3] - ipa_box[1]) + pad_y * 2
    bottom_h = zh_box[3] - zh_box[1] + pad_y * 2
    box_h = top_h + bottom_h
    if x < 0 or y < 0 or x + box_w > canvas_w or y + box_h > canvas_h:
        raise SystemExit(f"Label outside canvas: {en!r} at ({item['x']}, {item['y']})")

    shadow = max(2, round(4 * scale))
    draw.rectangle((x + shadow, y + shadow, x + box_w + shadow, y + box_h + shadow), fill=(0, 0, 0, 70))
    draw.rectangle((x, y, x + box_w, y + top_h), fill=PAPER)
    draw.rectangle((x, y + top_h, x + box_w, y + box_h), fill=INK)
    draw.text((x + pad_x, y + pad_y - en_box[1]), en, font=en_font, fill=INK)
    if ipa:
        draw.text((x + pad_x + en_w + gap, y + pad_y - ipa_box[1]), ipa, font=ipa_font, fill=(67, 72, 70, 255))
    draw.text((x + pad_x, y + top_h + pad_y - zh_box[1]), zh, font=zh_font, fill=WHITE)
    return x, y, x + box_w, y + box_h


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    line = words[0]
    for word in words[1:]:
        candidate = f"{line} {word}"
        if text_width(draw, candidate, font) <= max_width:
            line = candidate
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def wrap_chinese(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    line = ""
    for char in text:
        candidate = line + char
        if line and text_width(draw, candidate, font) > max_width:
            lines.append(line)
            line = char
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def draw_description(layer: Image.Image, card: dict, scale: float) -> tuple[int, int, int, int]:
    draw = ImageDraw.Draw(layer)
    canvas_w, canvas_h = layer.size
    desc = card.get("description") or {}
    en = str(desc.get("en", "")).strip()
    zh = str(desc.get("zh", "")).strip()
    if not en or not zh:
        raise SystemExit("Card 6 requires description.en and description.zh")
    anchor = str(desc.get("anchor", "bottom")).lower()
    if anchor not in {"top", "bottom"}:
        raise SystemExit("Card 6 description anchor must be 'top' or 'bottom'")

    margin = round(40 * scale)
    pad_x = round(20 * scale)
    pad_y = round(16 * scale)
    max_w = canvas_w - margin * 2
    text_w = max_w - pad_x * 2
    en_size = int(desc.get("font_size", 23))
    zh_size = max(19, en_size - 2)
    max_height = round(float(desc.get("max_height", 0.36)) * canvas_h)

    while True:
        en_font = load_font(FONT_EN, round(en_size * scale))
        zh_font = load_font(FONT_ZH, round(zh_size * scale))
        en_lines = wrap_text(draw, en, en_font, text_w)
        zh_lines = wrap_chinese(draw, zh, zh_font, text_w)
        en_line_h = math.ceil(en_font.size * 1.34)
        zh_line_h = math.ceil(zh_font.size * 1.45)
        top_h = len(en_lines) * en_line_h + pad_y * 2
        bottom_h = len(zh_lines) * zh_line_h + pad_y * 2
        panel_h = top_h + bottom_h
        if panel_h <= max_height or en_size <= 17:
            break
        en_size -= 1
        zh_size = max(17, en_size - 2)

    if panel_h > max_height:
        raise SystemExit("Card 6 description is too long for the permitted edge panel")
    y = margin if anchor == "top" else canvas_h - margin - panel_h
    x = margin
    shadow = max(2, round(5 * scale))
    draw.rectangle((x + shadow, y + shadow, x + max_w + shadow, y + panel_h + shadow), fill=(0, 0, 0, 68))
    draw.rectangle((x, y, x + max_w, y + top_h), fill=(252, 251, 247, 232))
    draw.rectangle((x, y + top_h, x + max_w, y + panel_h), fill=(10, 12, 12, 222))
    cursor_y = y + pad_y
    for line in en_lines:
        box = text_box(draw, line, en_font)
        draw.text((x + pad_x, cursor_y - box[1]), line, font=en_font, fill=INK)
        cursor_y += en_line_h
    cursor_y = y + top_h + pad_y
    for line in zh_lines:
        box = text_box(draw, line, zh_font)
        draw.text((x + pad_x, cursor_y - box[1]), line, font=zh_font, fill=WHITE)
        cursor_y += zh_line_h
    return x, y, x + max_w, y + panel_h


def render_card(base: Image.Image, card: dict, output: Path) -> None:
    scale = base.width / 1080
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    reserved = [draw_stage_badge(layer, card, scale)]
    number = int(card["number"])
    if number == 6:
        description_box = draw_description(layer, card, scale)
        if overlap_ratio(reserved[0], description_box) > 0.05:
            raise SystemExit("Card 6 badge overlaps the description panel; use bottom anchor or shorten the title")
    else:
        labels = card.get("labels", [])
        if not 3 <= len(labels) <= 18:
            raise SystemExit(f"Card {number} must contain 3-18 scattered labels")
        boxes = list(reserved)
        for item in labels:
            box = draw_label(layer, item, scale)
            if any(overlap_ratio(box, other) > 0.05 for other in boxes):
                raise SystemExit(f"Card {number} label overlaps another element: {item['en']!r}")
            boxes.append(box)
    result = Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")
    result.save(output, quality=96, subsampling=0)


def main() -> None:
    args = parse_args()
    data = json.loads(args.content.read_text(encoding="utf-8"))
    cards = data.get("cards", [])
    if len(cards) != 6 or [int(card.get("number", 0)) for card in cards] != [1, 2, 3, 4, 5, 6]:
        raise SystemExit("content.json must contain cards numbered 1 through 6")
    source = Image.open(args.photo).convert("RGB")
    target_w = max(1080, args.width)
    target_h = round(source.height * target_w / source.width)
    base = source.resize((target_w, target_h), Image.Resampling.LANCZOS)
    base = ImageEnhance.Contrast(base).enhance(1.02)
    base = ImageEnhance.Color(base).enhance(0.97)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for card in cards:
        output = args.output_dir / f"card-{int(card['number']):02d}.png"
        render_card(base, card, output)
        print(output.resolve())


if __name__ == "__main__":
    main()
