# hematite.gg logo

The logo system for hematite.gg, the screenshot uploader. Flat only for now: no metal or liquid finishes.

What it is:

- **Emblem (E2).** Two crystal shards split by a cleft. Every edge sits on a 22.5° grid; the cleft runs at 45°, then 67.5°.
- **Wordmark.** "hematite", drawn from Inter Display SemiBold Italic, with 45° cuts on the stem tops and feet and a small shard as the i-dot.
- **Two-tone by default.** On dark: steel `#C4D4E0` emblem and i-dot, white wordmark. On light: iron `#2E3A46` emblem and i-dot, graphite `#18181B` wordmark. One-colour versions for everything else.

The full guide is [brand/BRAND.md](brand/BRAND.md); notes for agents are in [AGENTS.md](AGENTS.md).

## Colours

| Name  | Hex       | Use                                                    |
|-------|-----------|--------------------------------------------------------|
| Steel | `#C4D4E0` | The logo on dark backgrounds. The default              |
| Iron  | `#2E3A46` | The logo on white and light backgrounds (11.6:1)       |
| Graphite | `#18181B` | The wordmark in the light two-tone logo (zinc-900, 17.7:1 on white) |
| Haze  | `#8A9BAB` | Secondary; favicons, which must read on light and dark |
| Night | `#09090B` | The dark ground (the app's zinc-950)                   |

## Colourways

| Colourway    | Emblem + i-dot | Wordmark | Use on                                  |
|--------------|----------------|----------|-----------------------------------------|
| `color-dark` | Steel          | White    | Night and dark backgrounds. The default |
| `color`      | Iron           | Graphite | White and light backgrounds             |
| `steel`      | Steel          | Steel    | Dark, one colour                        |
| `iron`       | Iron           | Iron     | Light, one colour                       |
| `black`      | Black          | Black    | One colour, print                       |
| `white`      | White          | White    | Photos, iron and coloured grounds       |

In the two-tone colourways the i-dot always takes the emblem's colour, never the wordmark's. The emblem alone comes in the four one-colour versions.

## Folders

| Folder          | Contents                                                                                       |
|-----------------|------------------------------------------------------------------------------------------------|
| `horizontal/`   | Primary lockup, 6 colourways, SVG + PNG 1x–4x (1x = 160 px tall)                              |
| `stacked/`      | Emblem above the wordmark, 6 colourways, SVG + PNG 1x–4x (1x = 400 px)                        |
| `wordmark/`     | Wordmark only, 6 colourways, SVG + PNG 1x–4x (1x = 128 px)                                    |
| `emblem/`       | Emblem only, 4 colourways, SVG + PNG 1x–4x (1x = 512 px)                                      |
| `favicon/`      | `favicon.svg`, `favicon.ico` (16/32/48), PNGs 16–128, apple-touch 180, android-chrome 192/512 |
| `app-icon/`     | 1024 px: steel emblem on night, iron emblem on steel, square and rounded                       |
| `social/`       | X header 1500×500 (centre, right, logo; PNG 1x and 2x + SVG) and round avatars (night, iron, steel; 400 and 1000 px + SVG) |
| `github/`       | GitHub org avatar (the emblem as contribution squares, 1024 + 460 px) and the org README header (1280×400, dark and light, SVG + PNG @2x) |
| `brand/`        | Guide, design language, tokens, stylesheet page                                               |
| `process/`      | How the logo came about (rounds 1–4) and the generator that makes every file                  |

`hematite-overview.png` (and `overview.html`) shows the whole system on one page.

File names follow `hematite-<layout>-<colourway>[@<n>x].<ext>`, PNGs in `png/1x|2x|3x|4x/`.

## Favicon snippet

```html
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

`favicon.svg` switches itself: iron on light browser tabs, steel on dark ones. The `.ico` and PNG favicons are in haze, which reads on both.

## Clear space and minimum size

- **Clear space:** keep half the emblem's height free on every side.
- **Horizontal minimum:** emblem at least 20 px tall on screen, 6 mm in print.
- **Stacked minimum:** emblem at least 32 px tall on screen, 10 mm in print.
- **Smaller than that:** use the emblem alone. At 48 px and below it uses the small-size cut (a wider cleft), as the favicons do.

## Construction

- **Emblem:** today's hematite mark, cleaned up. The 3 px stroke is baked into the outline and every edge is snapped to 22.5° (E2).
- **Base typeface:** Inter Display SemiBold Italic (SIL Open Font License 1.1), tracking −22 units.
- **Cuts:** 45° chamfers on the stem tops (h, t, t, i) and the stem feet (h, m, a, i), parallel to each other, 45 units deep at 1000 units per em (C2 light).
- **i-dot:** a small shard grown on the same 22.5° grid, 1.22× the font's own dot (S6).
- **".gg":** not part of the logo yet. Domain lockups come later.
- **Usage:** the wordmark is lettering, not a font setting. Never retype it; always use these files.
