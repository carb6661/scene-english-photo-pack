from __future__ import annotations

import sys
import unittest
from pathlib import Path

from PIL import Image


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import render_scatter_learning_cards as renderer  # noqa: E402
import render_scatter_learning_cards_mobile as mobile  # noqa: E402


class ReadableLayoutTests(unittest.TestCase):
    def setUp(self) -> None:
        self.layer = Image.new("RGBA", (1080, 1440), (0, 0, 0, 0))
        renderer.AUTO_PLACE = True

    @staticmethod
    def label(en: str, zh: str, x: float = 0.16, y: float = 0.18, ipa: str = "") -> dict:
        return {
            "en": en,
            "zh": zh,
            "ipa": ipa,
            "x": x,
            "y": y,
            "font_size": 30,
            "max_width": 0.48,
        }

    def test_card_one_is_chinese_only(self) -> None:
        layout = renderer.build_label_layout(
            self.layer,
            self.label("espresso machine", "意式咖啡机"),
            scale=1.20,
            chinese_only=True,
        )
        self.assertEqual(layout["top_h"], 0)
        self.assertTrue(layout["chinese_only"])
        self.assertGreaterEqual(layout["zh_font"].size, 36)

    def test_card_two_ipa_uses_its_own_line(self) -> None:
        plain = renderer.build_label_layout(
            self.layer,
            self.label("coffee grinder", "磨豆机"),
            scale=1.20,
            chinese_only=False,
        )
        pronounced = renderer.build_label_layout(
            self.layer,
            self.label("coffee grinder", "磨豆机", ipa="/ˈkɒfi ˌɡraɪndə/"),
            scale=1.20,
            chinese_only=False,
        )
        self.assertGreater(pronounced["top_h"], plain["top_h"])
        self.assertGreater(pronounced["ipa_h"], 0)

    def test_automatic_placement_repairs_deliberate_overlap(self) -> None:
        scale = 1.20
        gap = round(12 * scale)
        occupied = [(42, 38, 330, 130)]
        labels = [
            self.label("espresso machine", "意式咖啡机"),
            self.label("coffee grinder", "磨豆机"),
            self.label("vintage refrigerator", "复古冷藏柜"),
            self.label("pour-over coffee set", "手冲咖啡器具"),
            self.label("framed artwork", "装饰画"),
        ]

        for item in labels:
            position = renderer.resolve_label_position(
                self.layer,
                item,
                scale=scale,
                occupied=occupied,
                chinese_only=False,
            )
            layout = renderer.build_label_layout(self.layer, item, scale, chinese_only=False)
            box = (
                position[0],
                position[1],
                position[0] + layout["box_w"],
                position[1] + layout["box_h"],
            )
            self.assertFalse(any(renderer.boxes_conflict(box, other, gap) for other in occupied))
            occupied.append(box)

    def test_mobile_defaults_are_large_and_high_resolution(self) -> None:
        self.assertEqual(mobile.DEFAULT_WIDTH, 2880)
        self.assertGreaterEqual(mobile.LABEL_SCALE, 1.20)
        self.assertGreaterEqual(mobile.BADGE_SCALE, 1.10)
        self.assertGreaterEqual(mobile.DESCRIPTION_SCALE, 1.14)


if __name__ == "__main__":
    unittest.main()
