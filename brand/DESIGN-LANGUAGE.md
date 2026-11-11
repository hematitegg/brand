# hematite design language

The visual language of hematite's website and app: the night, the steel light that comes into it, the surfaces on it, and how things move. It was worked out on the website (`hematite/website`) and is written down here so slides, social images and other surfaces can speak it too. Logo usage is in [BRAND.md](BRAND.md); values are in [tokens.css](tokens.css) and [tokens.json](tokens.json).

## Principles

1. **Night first.** Everything stands on zinc-950, `#09090B`. The app is dark only.
2. **Light, not paint.** Colour arrives as a soft steel glow behind things, never as filled areas. The only filled light surface is the primary button.
3. **Glass, not cards.** Surfaces are white at a few percent with a hairline border; they let the night show through.
4. **Quiet until touched.** Surfaces rest. Light gathers where the pointer is (spotlight cards, glowing buttons).
5. **Things come into focus.** Entrances slide a little, fade in and un-blur. Nothing teleports.
6. **The 22.5° grid.** New shapes take their angles from the emblem: 22.5°, 45°, 67.5°.

## The night and its surfaces

| Layer        | Value                         | What lies there                                  |
|--------------|-------------------------------|--------------------------------------------------|
| Night        | `#09090B` (zinc-950)          | The page itself                                  |
| Surface      | white at 2%                   | Feature cards at rest                            |
| Surface, raised | white at 3–4%              | Badges, ghost buttons, icon tiles, cards under the pointer |
| Line         | white at 6%                   | Card and badge borders                           |
| Line, ghost  | white at 8%                   | Ghost button borders                             |
| Line, hover  | white at 10–14%               | Borders under the pointer                        |

- **Corners:** 12 px (`rounded-xl`) for buttons and icon tiles, 16 px (`rounded-2xl`) for cards, full pills for badges. The app's base radius is 10 px (`--radius: 0.625rem`).
- **Glass:** ghost buttons and badges carry `backdrop-filter: blur(4px)` (`backdrop-blur-sm`).
- **Text:** `zinc-50` for headings, `zinc-400` for body, `zinc-500` for descriptions.

## Light

### The steel glow

Soft round light behind the hero and section heads, in steel and haze:

- **Core:** `radial-gradient(circle, rgba(196,212,224,0.08) 0%, transparent 70%)`, about 900 px wide, centred, pulsing slowly.
- **Drifting:** two smaller glows (350–400 px) in haze `rgba(138,155,171,0.06)` and steel at 5%, blurred (24–40 px), floating slowly; the second 3 s behind the first.
- **On images** (the Open Graph card): steel at 18% from the top-left corner, haze at 14% from the bottom-right, on a dark diagonal (`#0A0A0A → #18181B → #0A0A0A`).

### The grid

A 64 px grid of steel hairlines at 3% (`rgba(196,212,224,0.03)`), faded to the night towards the edges (`radial-gradient(ellipse at center, transparent 30%, #09090B 70%)`). It fades out as the page scrolls: 40% at the top, 15% through the middle, gone at the end.

### The pointer's light

On feature cards, a spotlight follows the pointer: steel at 10% in a 400 px circle over the card, and steel at 15% in a 300 px circle on its 1 px border only. It appears over 300 ms when pointed at.

### Glows on actions

- **Primary button:** on hover, `box-shadow: 0 0 30px rgba(196,212,224,0.25)` and a white sheen that sweeps across in 700 ms.
- **Glow button:** a conic steel ring (30% and 20%) that turns once every 3 s, shown only on hover.
- **Status dot:** steel, 6 px, `box-shadow: 0 0 6px rgba(196,212,224,0.6)`.

### The shimmer

One word in a headline can run a steel shimmer: `linear-gradient(to right, #C4D4E0, #FFFFFF, #C4D4E0)` clipped to the text and moved slowly across. One word per headline, at most.

## Actions

| Action   | Look                                                                                         |
|----------|----------------------------------------------------------------------------------------------|
| Primary  | `zinc-100` fill, `zinc-950` text, 14 px semibold, 12 px corners, 24 × 12 px padding; hover: white + steel glow; press: scale 0.97 |
| Ghost    | white 3% fill, white 8% border, `zinc-300` text, 14 px medium, glass blur; hover: white 6% fill, 14% border, `zinc-100` text |
| Glow     | Primary face with the turning steel ring on hover                                            |

## Motion

The app's motion rules live in `src/lib/motion.ts`. Don't add new curves, springs or stagger values without updating it.

| Name              | Value                                   | For                                       |
|-------------------|-----------------------------------------|-------------------------------------------|
| Ease out expo     | `cubic-bezier(0.22, 1, 0.36, 1)`        | Landing entrances (0.5–0.7 s)             |
| Ease out quad     | `cubic-bezier(0.25, 0.46, 0.45, 0.94)`  | Small fades in the app                    |
| Spring, gentle    | stiffness 280, damping 26               | Rows, empty states: slight overshoot, settles |
| Spring, snappy    | stiffness 420, damping 30               | Hover and tap                             |
| Spring, overlay   | stiffness 340, damping 34               | Drawers, sliding panels                   |
| Stagger           | 0.06 s per item, 0.12 s delay (app); 0.08 s (landing) | Lists and hero lines        |

- **Entrances come into focus:** rows slide in from 28 px left, scale from 0.94 and un-blur from 4 px; landing blocks rise 16–24 px and fade in.
- **Press:** everything you can press scales to 0.97.
- **Glows** pulse and drift slowly; nothing else loops.

## Known gaps

- The hero and CTA use `landing-grain`, `animate-landing-pulse-glow`, `animate-landing-float` and `animate-landing-shimmer`, but no stylesheet in the website defines them yet, so the grain, pulse, float and shimmer don't currently show. The same goes for the glow button's `glow-spin` animation and its `--glow-angle` property: the ring doesn't turn. Their intended values belong here once they are written.
- The website still uses the old logo (DM Serif Text italic "hematite" + Inter ".gg", and the stroked emblem). Swap in `horizontal/` and `favicon/` when ready.
