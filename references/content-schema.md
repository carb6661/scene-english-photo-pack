# Six-card `content.json` schema

Use UTF-8 JSON. Coordinates and widths are normalized from `0` to `1`. The renderer accepts exactly six cards numbered 1-6.

```json
{
  "topic_en": "Pharmacy and everyday healthcare",
  "topic_zh": "药店与日常健康护理",
  "scene_description": "A bright community pharmacy with medicine shelves.",
  "cards": [
    {
      "number": 1,
      "title": "场景核心词汇",
      "title_en": "Scene vocabulary",
      "labels": [
        {
          "en": "pharmacy",
          "zh": "药店",
          "x": 0.05,
          "y": 0.08,
          "max_width": 0.40,
          "font_size": 28,
          "kind": "core"
        }
      ]
    },
    {
      "number": 2,
      "title": "核心词汇与发音",
      "title_en": "Vocabulary & pronunciation",
      "labels": [
        {
          "en": "pharmacy",
          "zh": "药店",
          "ipa": "/ˈfɑːməsi/",
          "x": 0.05,
          "y": 0.08,
          "max_width": 0.44,
          "font_size": 27,
          "kind": "core"
        }
      ]
    },
    {
      "number": 6,
      "title": "看图输出示范",
      "title_en": "Model description",
      "description": {
        "en": "This photo shows ...",
        "zh": "这张照片展示了……",
        "anchor": "bottom",
        "font_size": 23,
        "max_height": 0.36
      }
    }
  ]
}
```

## Cards 1-5

Each card requires `number`, `title`, `title_en`, and `labels`. Each label requires:

- `en`: English term, phrase, or sentence;
- `zh`: concise Chinese translation;
- `x`, `y`: normalized top-left coordinates.

Optional label fields:

- `ipa`: British IPA, required for every Card 2 item;
- `max_width`: maximum label width, default `0.48`;
- `font_size`: design-space size, default `27`;
- `kind`: `core`, `object`, `collocation`, `cet`, `speaking`, or `writing`; metadata only.

Cards 1 and 2 should contain matching vocabulary. Cards 3-5 may contain longer expressions but must keep every item as a separate patch.

## Card 6

Card 6 requires `description.en`, `description.zh`, and `description.anchor`. Anchor must be `top` or `bottom`. Keep the English description to 4-6 sentences and `max_height` at or below `0.36`.

Shorten content or move coordinates before shrinking text below a readable size. The renderer rejects out-of-bounds and overlapping labels.
