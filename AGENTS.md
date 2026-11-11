# Notes for agents working with the hematite brand

Read this before you make, pick or change anything with the hematite logo or design. Then read what the task needs:

- [brand/BRAND.md](brand/BRAND.md): the logo, colour, type, which file for which job, the don'ts.
- [brand/DESIGN-LANGUAGE.md](brand/DESIGN-LANGUAGE.md): the website's dark surfaces, steel light, depth and motion, with exact values.
- [brand/tokens.css](brand/tokens.css) / [brand/tokens.json](brand/tokens.json): every value, for code.
- [README.md](README.md): the logo files.

## The repo

| Path            | What                                                              | May you change it?                      |
|-----------------|-------------------------------------------------------------------|-----------------------------------------|
| `emblem/`, `wordmark/`, `horizontal/`, `stacked/`, `favicon/`, `app-icon/` | The logo files | Only by regenerating, and only if asked |
| `brand/`        | Guide, design language, tokens, stylesheet page                   | Yes, when the brand changes             |
| `process/0*/`   | Exploration rounds 1–4                                            | Never rewrite; add new rounds           |
| `process/generator/` | The scripts that make every file                             | Yes, then regenerate                    |

- Add new files; don't replace existing ones unless the owner asks for exactly that.
- Commit or push only when asked.

## Rules that are easy to get wrong

1. **The wordmark is a drawing.** Never set "hematite" in a font, Inter Display included. Use the SVG/PNG files.
2. **Steel on dark, iron on light.** Steel `#C4D4E0` has only 1.5:1 contrast on white: never put it on light grounds.
3. **Two pairs only.** The two-tone logo is `color-dark` (steel emblem, white wordmark) or `color` (iron emblem, graphite wordmark); everything else is one colour. The i-dot always takes the emblem's colour. Don't invent other pairs or a red i-dot.
4. **The 22.5° grid.** Every new shape (patterns, icons, motion paths) takes its angles from 22.5°, 45° and 67.5°.
5. **Cuts are fixed.** Don't add, remove or deepen cuts on the letters; they are part of the drawing (C2 light).
6. **Small sizes use the small-size cut.** At 48 px and below, use the favicon emblem (wider cleft), not a scaled-down `emblem/` file.
7. **No added effects:** no drop shadows, glows, outlines, gradients, rotation or recolouring of the logo. The website's steel glows go behind things, never on the logo.
8. **GitHub green stays on GitHub.** The contribution-grid avatar and header in `github/` use GitHub's own greens; green appears nowhere else in the brand.
9. **No ".gg" yet.** Don't build a domain lockup by typing ".gg" next to the wordmark; it will be drawn later.
10. **Type is Inter.** The UI and all text use Inter; Inter Display exists only inside the drawn wordmark.

## Picking a file

| You need                                 | Take                                                   |
|------------------------------------------|--------------------------------------------------------|
| The logo on a dark UI, slide or image    | `horizontal/svg/hematite-horizontal-color-dark.svg`    |
| The logo on a white page, doc, email     | `horizontal/svg/hematite-horizontal-color.svg`         |
| One colour on dark / light               | `…-steel.svg` / `…-iron.svg`                           |
| One colour, print                        | `horizontal/svg/hematite-horizontal-black.svg`         |
| On a photo or a coloured surface         | `horizontal/svg/hematite-horizontal-white.svg`         |
| Square or tall formats                   | `stacked/svg/hematite-stacked-<colourway>.svg`         |
| Where the emblem already stands nearby   | `wordmark/svg/hematite-wordmark-<colourway>.svg`       |
| Avatars, small marks                     | `emblem/svg/hematite-emblem-<colourway>.svg`           |
| Favicon                                  | `favicon/`                                             |
| App or tool icon                         | `app-icon/hematite-app-icon-night-1024.png`            |
| GitHub org avatar                        | `github/hematite-github-avatar-1024.png`               |
| GitHub org README header                 | `github/hematite-github-header-dark.svg` / `-light.svg` |
| Colours, radii, easing in code           | `brand/tokens.css`                                     |

## Making or changing files

Every logo file comes from `process/generator/` (Python, no network). Don't hand-edit exports: change the generator and run `python3 export.py` (see `process/generator/README.md`).

- Two-tone colourways are `COL2` in `export.py`; the letters and the i-dot come separately from `final.wordmark_parts()`.
- The locked logo lives in `final.py`: emblem `grid`, Inter Display SemiBold Italic, track −22, cuts `ladder_c2(45)`, i-dot `S6` at 1.22×.
- Cuts are subtracted from the letter outlines there, so exports are plain paths with no masks. Keep it that way.
- Rounds 1–4 have their own scripts (`make_board.py`, `round2.py` … `round4.py`); they rebuild the boards in `process/`.

## Where the design language comes from

The website (`hematite/website`, Next.js). Its `src/app/globals.css`, `src/app/(landing)/_components/` and `src/lib/motion.ts` are the source of truth for surfaces, glows and motion. When they change, update `brand/` to match.
