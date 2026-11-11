# hematite brand guide

How the hematite brand looks and how to use it: the logo, colour, type, and which file to use where. The visual language behind it (surfaces, light, depth, motion) is in [DESIGN-LANGUAGE.md](DESIGN-LANGUAGE.md), and every value is in [tokens.css](tokens.css) and [tokens.json](tokens.json).

hematite.gg is a free screenshot uploader: capture, organise and share screenshots, with Discord embeds, custom domains and an API. The name is the mineral: steel-grey, metallic and faceted. The brand should feel the same way: dark, sharp and a little crystalline, never loud.

## The brand at a glance

- **Two tones per ground.** On dark, a steel `#C4D4E0` emblem with a white wordmark; on light, an iron `#2E3A46` emblem with a graphite `#18181B` wordmark. The i-dot always follows the emblem.
- **One night.** The product lives on near-black zinc, `#09090B`, and light comes into it as a soft steel glow.
- **One family of angles.** Everything follows the emblem's 22.5° grid: the emblem's edges, the 45° cuts in the wordmark, the shard i-dot.
- **One typeface.** Inter for all text. Inter Display exists only inside the drawn wordmark.
- **One finish.** Flat. No metal, no gradients on the logo.

## The logo

| Part          | What it is                                                                                         |
|---------------|----------------------------------------------------------------------------------------------------|
| **Emblem**    | Two crystal shards split by a cleft that bends from 45° to 67.5°. Every edge on the 22.5° grid (E2). |
| **Wordmark**  | "hematite", drawn from Inter Display SemiBold Italic, tracked −22 units.                          |
| **Cuts**      | 45° chamfers on the stem tops (h, t, t, i) and feet (h, m, a, i), all parallel (C2 light).        |
| **i-dot**     | A small shard grown on the 22.5° grid, 1.22× the font's dot (S6). The emblem's family, not a copy of it. |

The wordmark is lettering, not type. Never retype it in a font; always use the files. ".gg" is not part of the logo yet.

### Lockups

| Lockup     | Use                                                                | Files          |
|------------|--------------------------------------------------------------------|----------------|
| Horizontal | The default, almost everywhere                                     | `horizontal/`  |
| Stacked    | Square and tall formats: avatars with text, posters, title cards   | `stacked/`     |
| Wordmark   | Where the emblem already stands nearby, or space is very low       | `wordmark/`    |
| Emblem     | Small sizes, avatars, app icons, favicons, a signature mark        | `emblem/`, `favicon/`, `app-icon/` |

**Clear space:** half the emblem's height on every side.
**Minimum size:** horizontal with the emblem 20 px tall (6 mm in print); stacked with the emblem 32 px (10 mm). Smaller than that, use the emblem alone.
**Small-size cut:** at 48 px and below the emblem's cleft is widened (gap 11 instead of 7 units) so it doesn't close up. The favicons use it; use them rather than scaling down `emblem/`.

### Colourways

| Colourway    | Emblem + i-dot | Wordmark | Use on                                   |
|--------------|----------------|----------|------------------------------------------|
| `color-dark` | Steel          | White    | Night and dark backgrounds. The default  |
| `color`      | Iron           | Graphite | White and light backgrounds              |
| `steel`      | Steel          | Steel    | Dark, where one colour is needed         |
| `iron`       | Iron           | Iron     | Light, where one colour is needed        |
| `black`      | Black          | Black    | One colour, print                        |
| `white`      | White          | White    | Photos, iron and coloured grounds        |

In the two-tone colourways the i-dot ties the word back to the emblem: it always takes the emblem's colour. The emblem alone has no two-tone version; it comes in steel, iron, black and white.

## Colour

Most of what people see is the night, light text, and steel as light. Colour is never decoration on its own.

| Role        | Token         | Hex / value               | Use                                                     |
|-------------|---------------|---------------------------|---------------------------------------------------------|
| Steel       | `steel`       | `#C4D4E0`                 | The emblem on dark, one-colour logo on dark, accents, glows, icon tint |
| Iron        | `iron`        | `#2E3A46`                 | The emblem on light; one-colour logo on light; text on steel |
| Graphite    | `graphite`    | `#18181B` (zinc-900)      | The wordmark in the light two-tone logo (17.7:1 on white) |
| Haze        | `haze`        | `#8A9BAB`                 | Secondary marks, favicons, the second glow              |
| Night       | `night`       | `#09090B` (zinc-950)      | The ground of everything digital                        |
| Surface     | `surface`     | white at 2–4%             | Cards and panels on the night                           |
| Line        | `line`        | white at 6–8%             | Card borders, hairlines                                 |
| Line, hover | `line-strong` | white at 10–14%           | Borders under the pointer                               |
| Text        | `zinc-50`/`zinc-100` | `#FAFAFA` / `#F4F4F5` | Headings and what matters                             |
| Muted text  | `zinc-400`    | `#A1A1AA`                 | Body copy on the night                                  |
| Quiet text  | `zinc-500`    | `#71717A`                 | Descriptions, captions                                  |
| Primary action | `zinc-100` | `#F4F4F5` on `#09090B` text | Main buttons                                         |

Measured contrast: steel on night 13.1:1, haze on night 7.0:1, iron on white 11.6:1. Steel on white is only 1.5:1, which is why light grounds take iron.

## Type

Inter, everywhere, as the website sets it (`next/font`, weights 400–700).

| Style    | Size                                   | Leading | Tracking | Weight |
|----------|----------------------------------------|---------|----------|--------|
| Hero     | 36 px → 48 px (sm) → 60 px (md)        | 1.1     | tight (−0.025em) | 700 |
| Section  | 30 px → 36 px (sm)                     | 1.1–1.2 | tight    | 700    |
| Card title | 15 px                                | 1.4     | normal   | 600    |
| Lead     | 16 px → 18 px (sm)                     | 1.625   | normal   | 400    |
| Body     | 14 px                                  | 1.625   | normal   | 400    |
| Badge    | 11 px → 12 px (sm)                     | 1.4     | normal   | 500    |

In a headline, one word can carry the steel shimmer (steel → white → steel, see DESIGN-LANGUAGE.md), as "moments" does in the hero. One word per headline, at most.

## Applications

| Need                       | Use                                                              |
|----------------------------|------------------------------------------------------------------|
| Website favicon            | `favicon/` (snippet in the README)                               |
| Website header and footer  | `horizontal/svg/hematite-horizontal-color-dark.svg`              |
| App sidebar                | `emblem/svg/hematite-emblem-steel.svg` (32 px: use the favicon cut) |
| Open Graph / link preview  | Not made yet; steel lockup on night, see DESIGN-LANGUAGE.md      |
| GitHub org avatar          | `github/hematite-github-avatar-1024.png` (the emblem in contribution squares, GitHub green) |
| GitHub org README header   | `github/hematite-github-header-dark.svg` and `-light.svg`, switched with `<picture>` |
| Discord server icon        | `app-icon/hematite-app-icon-night-1024.png`                      |
| Profile pictures           | `app-icon/hematite-app-icon-night-1024.png` on dark platforms, `…-steel-1024.png` on light ones |
| Documents, email           | `horizontal/svg/hematite-horizontal-color.svg`                   |
| Print, merch               | Black or white SVG, one colour                                   |

## Don'ts

- Don't retype, re-space or redraw the wordmark, and don't swap its font.
- Don't put steel on white or light backgrounds; use iron.
- Don't make other two-tone pairs than `color` and `color-dark`, and don't give the i-dot its own colour.
- Don't add, remove or deepen the cuts in the letters.
- Don't add drop shadows, glows, outlines, bevels, gradients or 3D to the logo.
- Don't rotate, skew or stretch the logo.
- Don't type ".gg" next to the wordmark; a domain lockup will be drawn.
- Don't scale `emblem/` below 48 px; use the favicon's small-size cut.
- Don't use GitHub's green outside `github/`. On GitHub the contribution grid is the motif; everywhere else the brand stays steel.

## Files and sources

- Repo root — the logo files (see `README.md`).
- `brand/` — this guide, the design language, the tokens, the stylesheet page.
- `process/` — the exploration rounds and the generator (`process/generator/`). Regenerate rather than hand-edit.
- The website, `hematite/website`, is where the design language lives in code: `src/app/globals.css` (theme), `src/app/(landing)/_components/` (glows, buttons, cards), `src/lib/motion.ts` (springs, easing).
