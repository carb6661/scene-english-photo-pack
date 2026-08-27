# Mobile readability and PNG output

Apply these requirements to every six-image pack.

## Label scale

The mobile renderer applies these defaults relative to the base design:

- floating labels: `1.20` scale;
- page badge: `1.10` scale;
- Card 6 description: `1.14` scale.

Card 1 Chinese prompts use the full requested font size rather than a reduced translation size. Card 2 places IPA on its own line so vocabulary can remain large without creating an excessively wide strip.

Recommended design-space sizes:

- short Chinese or vocabulary labels: 27-34;
- situational and CET phrases: 23-28;
- IELTS sentence patches: 19-23;
- model description: 22-25.

Preview every result at 360-430 px wide. If text is hard to read, shorten the wording or remove the least useful item before reducing font size.

## Collision safety

- Keep at least a 12 px-derived safety gap around labels and the page badge.
- Any touching or intersection counts as a collision.
- Automatic placement searches near the requested anchor first.
- Inspect moved labels for semantic proximity to their objects; automatic geometry cannot determine the best referent.

## High-resolution PNG

- Default export width is 2880 px; preserve source aspect ratio.
- Save as RGB PNG with 300 DPI metadata and lossless compression.
- Apply restrained sharpening only; avoid halos, artificial HDR contrast, and text-edge artifacts.
- Inspect both the phone preview and full-resolution PNG.
