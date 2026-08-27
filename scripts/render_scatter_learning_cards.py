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
MUTED = (67, 72, 70, 255)
WHITE = (255, 255, 255, 255)

LABEL_SCALE = 1.0
BADGE_SCALE = 1.0
DESCRIPTION_SCALE = 1.0
AUTO_PLACE = True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render six scattered bilingual learning cards.")
    parser.add_argument("--photo", type=Path, required=True, help="Clean photo with all UI already removed")
    parser.add_argument("--content", type=Path, required=True, help="UTF-8 six-card JSON")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--width", type=int, default=2160)
    parser.add_argument("--label-scale", type=float, default=1.0)
    parser.add_argument("--badge-scale", type=float, default=1.0)
    parser.add_argument("--description-scale", type=float, default=1.0)
    parser.add_argument(
        "--strict-layout",
        action="store_true",
        help="Disable automatic collision repair and fail on the requested coordinates",
    )
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


def box_size(box: tuple[int, int, int, int]) -> tuple[int, int]:
    return box[2] - box[0], box[3] - box[1]


def boxes_conflict(
    a: tuple[int, int, int, int],
    b: tuple[int, int, int, int],
    gap: int = 0,
) -> bool:
    return not (
        a[2] + gap <= b[0]
        or b[2] + gap <= a[0]
        or a[3] + gap <= b[1]
        or b[3] + gap <= a[1]
    )


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
    box_w = max(box_size(top_box)[0], box_size(bottom_box)[0]) + pad_x * 2
    top_h = box_size(top_box)[1] + pad_y * 2
    bottom_h = box_size(bottom_box)[1] + pad_y * 2
    shadow = max(2, round(3 * scale))
    draw.rectangle((x + shadow, y + shadow, x + box_w + shadow, y + top_h + bottom_h + shadow), fill=(0, 0, 0, 70))
    draw.rectangle((x, y, x + box_w, y + top_h), fill=PAPER)
    draw.rectangle((x, y + top_h, x + box_w, y + top_h + bottom_h), fill=INK)
    draw.text((x + pad_x, y + pad_y - top_box[1]), top, font=en_font, fill=INK)
    draw.text((x + pad_x, y + top_h + pad_y - bottom_box[1]), bottom, font=zh_font, fill=WHITE)
    return x, y, x + box_w, y + top_h + bottom_h


def build_label_layout(layer: Image.Image, item: dict, scale: float, chinese_only: bool) -> dict:
    draw = ImageDraw.Draw(layer)
    canvas_w, _ = layer.size
    en = str(item.get("en", "")).strip()
    zh = str(item.get("zh", "")).strip()
    ipa = str(item.get("ipa", "")).strip()
    if not zh:
        raise SystemExit("Every label requires Chinese text")
    if not chinese_only and not en:
        raise SystemExit("Cards 2-5 require English text")

    max_w = round(float(item.get("max_width", 0.48)) * canvas_w)
    current = max(18, int(item.get("font_size", 28)))
    pad_x = round(13 * scale)
    pad_y = round(8 * scale)
    ipa_gap = round(4 * scale)

    while True:
        en_font = load_font(FONT_EN_BOLD, round(current * scale))
        ipa_font = load_font(FONT_EN, round(max(18, current - 4) * scale))
        zh_size = current if chinese_only else max(20, current - 2)
        zh_font = load_font(FONT_ZH, round(zh_size * scale))
        en_box = text_box(draw, en, en_font) if en else (0, 0, 0, 0)
        ipa_box = text_box(draw, ipa, ipa_font) if ipa else (0, 0, 0, 0)
        zh_box = text_box(draw, zh, zh_font)
        en_w, en_h = box_size(en_box)
        ipa_w, ipa_h = box_size(ipa_box)
        zh_w, zh_h = box_size(zh_box)

        if chinese_only:
            box_w = zh_w + pad_x * 2
            top_h = 0
            bottom_h = zh_h + pad_y * 2
        else:
            box_w = max(en_w, ipa_w, zh_w) + pad_x * 2
            top_h = en_h + pad_y * 2
            if ipa:
                top_h += ipa_gap + ipa_h
            bottom_h = zh_h + pad_y * 2

        if box_w <= max_w or current <= 18:
            break
        current -= 1

    return {
        "en": en,
        "zh": zh,
        "ipa": ipa,
        "en_font": en_font,
        "ipa_font": ipa_font,
        "zh_font": zh_font,
        "en_box": en_box,
        "ipa_box": ipa_box,
        "zh_box": zh_box,
        "en_h": en_h,
        "ipa_h": ipa_h,
        "zh_h": zh_h,
        "pad_x": pad_x,
        "pad_y": pad_y,
        "ipa_gap": ipa_gap,
        "box_w": box_w,
        "top_h": top_h,
        "bottom_h": bottom_h,
        "box_h": top_h + bottom_h,
        "chinese_only": chinese_only,
    }


def requested_position(layer: Image.Image, item: dict) -> tuple[int, int]:
    canvas_w, canvas_h = layer.size
    return round(float(item["x"]) * canvas_w), round(float(item["y"]) * canvas_h)


def draw_label(
    layer: Image.Image,
    item: dict,
    scale: float,
    chinese_only: bool = False,
    position: tuple[int, int] | None = None,
) -> tuple[int, int, int, int]:
    draw = ImageDraw.Draw(layer)
    canvas_w, canvas_h = layer.size
    x, y = position if position is not None else requested_position(layer, item)
    layout = build_label_layout(layer, item, scale, chinese_only)
    box_w, box_h = layout["box_w"], layout["box_h"]
    if x < 0 or y < 0 or x + box_w > canvas_w or y + box_h > canvas_h:
        label_name = layout["en"] or layout["zh"]
        raise SystemExit(f"Label outside canvas after layout: {label_name!r}")

    shadow = max(2, round(4 * scale))
    draw.rectangle((x + shadow, y + shadow, x + box_w + shadow, y + box_h + shadow), fill=(0, 0, 0, 70))

    if chinese_only:
        draw.rectangle((x, y, x + box_w, y + box_h), fill=INK)
        zh_box = layout["zh_box"]
        draw.text(
            (x + layout["pad_x"], y + layout["pad_y"] - zh_box[1]),
            layout["zh"],
            font=layout["zh_font"],
            fill=WHITE,
        )
        return x, y, x + box_w, y + box_h

    top_h = layout["top_h"]
    draw.rectangle((x, y, x + box_w, y + top_h), fill=PAPER)
    draw.rectangle((x, y + top_h, x + box_w, y + box_h), fill=INK)
    en_box = layout["en_box"]
    cursor_y = y + layout["pad_y"]
    draw.text(
        (x + layout["pad_x"], cursor_y - en_box[1]),
        layout["en"],
        font=layout["en_font"],
        fill=INK,
    )
    if layout["ipa"]:
        cursor_y += layout["en_h"] + layout["ipa_gap"]
        ipa_box = layout["ipa_box"]
        draw.text(
            (x + layout["pad_x"], cursor_y - ipa_box[1]),
            layout["ipa"],
            font=layout["ipa_font"],
            fill=MUTED,
        )
    zh_box = layout["zh_box"]
    draw.text(
        (x + layout["pad_x"], y + top_h + layout["pad_y"] - zh_box[1]),
        layout["zh"],
        font=layout["zh_font"],
        fill=WHITE,
    )
    return x, y, x + box_w, y + box_h


def candidate_offsets(max_ring: int = 12):
    yield 0, 0
    for ring in range(1, max_ring + 1):
        half = max(1, ring // 2)
        for dx, dy in (
            (0, -ring),
            (0, ring),
            (-ring, 0),
            (ring, 0),
            (-ring, -ring),
            (ring, -ring),
            (-ring, ring),
            (ring, ring),
            (-half, -ring),
            (half, -ring),
            (-half, ring),
            (half, ring),
        ):
            yield dx, dy


def resolve_label_position(
    layer: Image.Image,
    item: dict,
    scale: float,
    occupied: list[tuple[int, int, int, int]],
    chinese_only: bool,
) -> tuple[int, int]:
    canvas_w, canvas_h = layer.size
    layout = build_label_layout(layer, item, scale, chinese_only)
    box_w, box_h = layout["box_w"], layout["box_h"]
    margin = max(4, round(8 * scale))
    safe_gap = max(6, round(12 * scale))
    origin_x, origin_y = requested_position(layer, item)
    origin_x = min(max(margin, origin_x), max(margin, canvas_w - margin - box_w))
    origin_y = min(max(margin, origin_y), max(margin, canvas_h - margin - box_h))

    if not AUTO_PLACE:
        box = (origin_x, origin_y, origin_x + box_w, origin_y + box_h)
        if any(boxes_conflict(box, other, safe_gap) for other in occupied):
            raise SystemExit(f"Strict layout collision: {layout['en'] or layout['zh']!r}")
        return origin_x, origin_y

    step = max(round(16 * scale), round(min(canvas_w, canvas_h) * 0.025))
    seen: set[tuple[int, int]] = set()
    for dx, dy in candidate_offsets():
        x, y = origin_x + dx * step, origin_y + dy * step
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if x < margin or y < margin or x + box_w > canvas_w - margin or y + box_h > canvas_h - margin:
            continue
        box = (x, y, x + box_w, y + box_h)
        if not any(boxes_conflict(box, other, safe_gap) for other in occupied):
            return x, y

    grid_step = max(step, box_h + safe_gap)
    candidates: list[tuple[int, int, int]] = []
    for y in range(margin, max(margin + 1, canvas_h - margin - box_h + 1), grid_step):
        for x in range(margin, max(margin + 1, canvas_w - margin - box_w + 1), step):
            distance = abs(x - origin_x) + abs(y - origin_y)
            candidates.append((distance, x, y))
    for _, x, y in sorted(candidates):
        box = (x, y, x + box_w, y + box_h)
        if not any(boxes_conflict(box, other, safe_gap) for other in occupied):
            return x, y

    raise SystemExit(f"No non-overlapping position found for {layout['en'] or layout['zh']!r}; shorten text or reduce labels")


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
        if panel_h <= max_height or en_size <= 18:
            break
        en_size -= 1
        zh_size = max(18, en_size - 2)

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


def validate_cards(cards: list[dict]) -> None:
    if len(cards) != 6 or [int(card.get("number", 0)) for card in cards] != [1, 2, 3, 4, 5, 6]:
        raise SystemExit("content.json must contain cards numbered 1 through 6")
    for card in cards[:5]:
        labels = card.get("labels", [])
        if not 3 <= len(labels) <= 18:
            raise SystemExit(f"Card {card['number']} must contain 3-18 scattered labels")
    card1_terms = [str(item.get("en", "")).strip().casefold() for item in cards[0]["labels"]]
    card2_terms = [str(item.get("en", "")).strip().casefold() for item in cards[1]["labels"]]
    if card1_terms != card2_terms:
        raise SystemExit("Cards 1 and 2 must contain the same English terms in the same order")
    if any(not str(item.get("ipa", "")).strip() for item in cards[1]["labels"]):
        raise SystemExit("Every Card 2 label requires British IPA")
    card5_kinds = {str(item.get("kind", "")).strip().lower() for item in cards[4]["labels"]}
    if not {"speaking", "writing"}.issubset(card5_kinds):
        raise SystemExit("Card 5 must include both speaking and writing expressions")
    description = cards[5].get("description") or {}
    if not str(description.get("en", "")).strip() or not str(description.get("zh", "")).strip():
        raise SystemExit("Card 6 requires complete English and Chinese descriptions")


def render_card(base: Image.Image, card: dict, output: Path) -> None:
    scale = base.width / 1080
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    badge_box = draw_stage_badge(layer, card, scale * BADGE_SCALE)
    occupied = [badge_box]
    number = int(card["number"])
    if number == 6:
        description_box = draw_description(layer, card, scale * DESCRIPTION_SCALE)
        gap = max(6, round(12 * scale))
        if boxes_conflict(badge_box, description_box, gap):
            raise SystemExit("Card 6 badge overlaps the description panel; use bottom anchor or shorten the panel")
    else:
        chinese_only = number == 1
        label_scale = scale * LABEL_SCALE
        gap = max(6, round(12 * label_scale))
        for item in card.get("labels", []):
            position = resolve_label_position(layer, item, label_scale, occupied, chinese_only)
            box = draw_label(layer, item, label_scale, chinese_only=chinese_only, position=position)
            if any(boxes_conflict(box, other, gap) for other in occupied):
                raise SystemExit(f"Internal layout error: unresolved collision for {item.get('en')!r}")
            occupied.append(box)
    result = Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")
    result.save(output, quality=96, subsampling=0)


def main() -> None:
    global LABEL_SCALE, BADGE_SCALE, DESCRIPTION_SCALE, AUTO_PLACE
    args = parse_args()
    LABEL_SCALE = max(0.8, args.label_scale)
    BADGE_SCALE = max(0.8, args.badge_scale)
    DESCRIPTION_SCALE = max(0.8, args.description_scale)
    AUTO_PLACE = not args.strict_layout
    data = json.loads(args.content.read_text(encoding="utf-8"))
    cards = data.get("cards", [])
    validate_cards(cards)
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
