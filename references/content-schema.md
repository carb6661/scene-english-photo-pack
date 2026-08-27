# Six-card `content.json` schema

Use UTF-8 JSON. Coordinates and widths are normalized from `0` to `1`. The renderer accepts exactly six cards numbered 1-6.

```json
{
  "topic_en": "Independent coffee shop",
  "topic_zh": "独立咖啡店",
  "scene_description": "A compact coffee bar with brewing equipment.",
  "cards": [
    {
      "number": 1,
      "title": "中文场景提示",
      "title_en": "Chinese recall prompts",
      "labels": [
        {
          "en": "coffee grinder",
          "zh": "磨豆机",
          "x": 0.62,
          "y": 0.42,
          "max_width": 0.34,
          "font_size": 31,
          "kind": "object"
        }
      ]
    },
    {
      "number": 2,
      "title": "核心词汇与发音",
      "title_en": "Vocabulary & pronunciation",
      "labels": [
        {
          "en": "coffee grinder",
          "zh": "磨豆机",
          "ipa": "/ˈkɒfi ˌɡraɪndə/",
          "x": 0.62,
          "y": 0.42,
          "max_width": 0.42,
          "font_size": 29,
          "kind": "object"
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
        "font_size": 24,
        "max_height": 0.36
      }
    }
  ]
}
```

## Cards 1-5

Every card requires `number`, `title`, `title_en`, and `labels`. Every label requires:

- `en`: English source term or expression;
- `zh`: concise Chinese translation;
- `x`, `y`: preferred normalized top-left anchor.

Optional fields:

- `ipa`: required for every Card 2 item;
- `max_width`: preferred maximum width, normally `0.34-0.62`;
- `font_size`: design-space size;
- `kind`: `core`, `object`, `collocation`, `cet`, `speaking`, or `writing`.

Card 1 still requires `en`, but the renderer intentionally hides it and displays only `zh`. Card 2 must contain the same English terms in the same order and reveal English, IPA, and Chinese.

Recommended design-space font sizes before mobile scaling:

- Card 1 Chinese prompts: 29-34;
- Card 2 vocabulary: 27-31;
- Cards 3-4 phrases: 23-28;
- Card 5 expressions: 19-23;
- Card 6 description: 22-25.

Coordinates are preferred anchors, not guaranteed final positions. The default renderer automatically moves a label to the nearest safe position when its box or safety gap conflicts with the badge or another label. Use `--strict-layout` only to debug the supplied coordinates.

## Card 6

Card 6 requires `description.en`, `description.zh`, and `description.anchor`. Anchor must be `top` or `bottom`. Keep the panel at or below `0.36` of image height.

Shorten content, move anchors, or reduce item count before shrinking text below a readable size.
