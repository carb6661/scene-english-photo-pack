# Mobile readability and PNG output

Apply these requirements to every six-image pack.

## Label scale

- The default renderer enlarges ordinary floating labels by 8% and the Card 6 description typography by 6% relative to the original scattered-label design.
- Preserve compact patches, but prioritize comfortable reading on a 360-430 px-wide phone screen.
- Short vocabulary labels should normally use `font_size` 25-30. Situational and CET phrases should normally use 21-25. IELTS sentence patches should normally use 18-22 and be shortened before shrinking further.
- Use slightly more visual presence than the original compact design without merging separate labels.
- If enlarged labels overlap or exceed the canvas, move them into another whitespace region, shorten the wording, or reduce item count. Do not disable the renderer's overlap and bounds checks.

## High-resolution PNG

- Default export width is 2880 px; preserve the source aspect ratio.
- Save final images as RGB PNG with 300 DPI metadata and lossless compression.
- Apply only restrained sharpening. Do not introduce halos, artificial HDR contrast, or text-edge artifacts.
- Inspect a downscaled 360-430 px-wide preview as well as the full-resolution output. Text must remain legible on the phone preview, and the photograph must remain clear at full size.
