from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
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

    def test_mobile_renderer_writes_six_300_dpi_pngs(self) -> None:
        terms = [
            ("espresso machine", "意式咖啡机", "/eˈspresəʊ məˌʃiːn/"),
            ("coffee grinder", "磨豆机", "/ˈkɒfi ˌɡraɪndə/"),
            ("pendant light", "吊灯", "/ˈpendənt laɪt/"),
        ]

        def labels(with_ipa: bool = False, kinds: bool = False) -> list[dict]:
            result = []
            for index, (en, zh, ipa) in enumerate(terms):
                item = self.label(en, zh, x=0.15, y=0.20)
                if with_ipa:
                    item["ipa"] = ipa
                if kinds:
                    item["kind"] = "speaking" if index == 0 else "writing"
                result.append(item)
            return result

        cards = [
            {"number": 1, "title": "中文回忆", "title_en": "RECALL", "labels": labels()},
            {"number": 2, "title": "英文与发音", "title_en": "REVEAL", "labels": labels(with_ipa=True)},
            {"number": 3, "title": "情景搭配", "title_en": "COLLOCATIONS", "labels": labels()},
            {"number": 4, "title": "四六级表达", "title_en": "CET", "labels": labels()},
            {"number": 5, "title": "雅思表达", "title_en": "IELTS", "labels": labels(kinds=True)},
            {
                "number": 6,
                "title": "看图输出",
                "title_en": "MODEL",
                "description": {
                    "en": "This compact coffee bar contains specialist equipment. The counter is arranged for preparing espresso and pour-over coffee. Pendant lights give the room a warm atmosphere. The scene shows how design and function can work together.",
                    "zh": "这间紧凑的咖啡吧配有专业设备。操作台为制作意式咖啡和手冲咖啡而布置。吊灯营造出温暖的氛围。这个场景展示了设计与功能如何结合。",
                    "anchor": "bottom",
                    "font_size": 24,
                    "max_height": 0.36,
                },
            },
        ]

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            photo = root / "photo.png"
            content = root / "content.json"
            output = root / "output"
            Image.new("RGB", (900, 1200), (215, 207, 192)).save(photo)
            content.write_text(json.dumps({"cards": cards}, ensure_ascii=False), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "render_scatter_learning_cards_mobile.py"),
                    "--photo",
                    str(photo),
                    "--content",
                    str(content),
                    "--output-dir",
                    str(output),
                    "--width",
                    "1080",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            paths = sorted(output.glob("card-*.png"))
            self.assertEqual(len(paths), 6)
            for path in paths:
                with Image.open(path) as image:
                    self.assertEqual(image.width, 1080)
                    dpi = image.info.get("dpi", (0, 0))
                    self.assertAlmostEqual(dpi[0], 300, delta=1)
                    self.assertAlmostEqual(dpi[1], 300, delta=1)


if __name__ == "__main__":
    unittest.main()
