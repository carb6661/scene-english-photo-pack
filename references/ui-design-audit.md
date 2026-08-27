# UI audit for six scattered photo cards

This adapts the installed UI design system to photographic learning cards. The user's square-corner requirement overrides generic rounded-card examples.

## Design DNA

- Product: six progressive mobile-first English learning images.
- Focal surface: the user's clean photograph.
- Visual language: larger square bilingual patches floating beside objects and through genuine whitespace.
- Card 1 mode: black Chinese-only recall prompts.
- Card 2 mode: English, British IPA on its own line, then Chinese.
- Palette: warm white, near-black, white, muted IPA grey, and restrained neutral shadow.
- Grid: 8 px-derived internal padding with a 12 px-derived external safety gap.
- Type hierarchy: page badge, primary term or sentence, IPA/support, and translation; no more than three perceived levels within a label.

## Six-page consistency

- Keep the same photo crop, dimensions, font family, contrast, and shadow treatment.
- Increase text presence without turning patches into large cards.
- Page badges remain small outer-corner markers.
- Cards 1-5 use no large panels. Card 6 alone may use an edge-docked description panel up to 36% of height.
- Automatic collision repair may move anchors, but the final visual audit must confirm labels remain near the right objects.

## Audit gate

- Text is comfortably readable in a 360-430 px preview.
- No two labels touch, overlap, or violate the safety gap.
- The photograph stays recognisable and at least half unobstructed.
- Labels remain scattered rather than grid-aligned.
- Object labels sit beside plausible referents.
- Long Card 5 expressions stay separate and use ASCII `[Speaking]` / `[Writing]` markers.
- Card 6 panel stays top- or bottom-docked and outside the central focal region.
- Essential text meets WCAG AA contrast through near-black on warm white and white on black.
- No clipping, tofu glyphs, phone UI, app chrome, watermark, social element, or pre-existing study label remains.
