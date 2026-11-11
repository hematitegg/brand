# Generator

Python, no network needed. Builds the exploration boards and every logo file from font outlines and the emblem's geometry.

Needs Python 3 with `fonttools` and `Pillow`, and `rsvg-convert` (librsvg) for PNGs. The boards render with any browser (open the `board.html` files); the PNG boards were made with Playwright.

## The logo files

```bash
cd process/generator
python3 export.py     # emblem/, wordmark/, horizontal/, stacked/, favicon/, app-icon/
python3 overview.py   # overview.html in the repo root
python3 github.py     # github/: org avatar and README headers
```

| File           | Does                                                                                          |
|----------------|-----------------------------------------------------------------------------------------------|
| `final.py`     | The locked logo as polygons: emblem `grid` (E2), Inter Display SemiBold Italic, track −22, cuts `ladder_c2(45)`, i-dot S6 at 1.22×. Glyph outlines are flattened and the cuts subtracted (`subtract`), so exports carry no masks. |
| `export.py`    | Writes every logo file in steel, iron, black and white (SVG + PNG 1x–4x), the favicons (small-size cut, gap 11, up to 48 px) and the app icons. |
| `round5.py`    | Round 5's two-tone board. Uses `final.wordmark_parts()`, which returns the letters and the i-dot separately. |
| `github.py`    | `github/`: the P1 avatar (emblem with a widened cleft, sampled into contribution cells) and the H3 README headers, dark and light. Seeded, so reruns are identical. |
| `overview.py`  | `overview.html`, built from the exported files.                                              |

## Shared pieces

| File          | Does                                                                                           |
|---------------|------------------------------------------------------------------------------------------------|
| `emblem.py`   | Today's emblem as edge lines. `build('current'|'clean'|'grid', gap)` gives E0, E1, E2; the 3 px stroke is baked in by offsetting each edge by 1.5. |
| `wordmark.py` | Lays out text from a font's outlines (normalised to 1000 units per em), swaps the i-dot, round-1 stem cuts. |
| `facets.py`   | Cuts as facets: a plane at an angle shaves a set depth off a letter's extreme point in that direction. Each letter is cut on its own, so cuts never reach a neighbour. |
| `dots.py`     | The sixteen i-dots of rounds 2 and 3 (D1–D16).                                                 |
| `shards.py`   | The shard i-dots of round 4 (S1–S12), grown as intersections of half-planes on the 22.5° grid. |

## The rounds

```bash
OUT=../01-options python3 make_board.py
OUT=../02-e2-b2-cuts-and-dots python3 round2.py
OUT=../03-c2-depth-and-dots python3 round3.py
OUT=../04-shard-dots python3 round4.py
OUT=../05-two-tone python3 round5.py      # two-tone variants, from final.py's real outlines
```

Each writes `svg/` and `board.html` into its folder. In rounds 1–4 the cuts are SVG masks; only `final.py` subtracts them for real.

## Fonts

`fonts/` holds the typefaces the boards and the logo are drawn from, all under the SIL Open Font License 1.1 (`fonts/OFL.txt`): Inter Display (the wordmark's base), DM Serif Text, Geist and Geist Mono (round 1 only). Geist, Geist Mono and DM Serif Text came from the website's build cache; the Geist files are static instances of the variable fonts.
