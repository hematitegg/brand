# hematite brand

Everything about how hematite looks, written down for people and for agents.

| File                                     | For                                                                                      |
|------------------------------------------|------------------------------------------------------------------------------------------|
| [BRAND.md](BRAND.md)                     | The brand guide: the logo, colour, type, which file to use where, don'ts                 |
| [DESIGN-LANGUAGE.md](DESIGN-LANGUAGE.md) | The visual language of the website: dark surfaces, steel light, depth, motion, with exact values |
| [tokens.css](tokens.css)                 | Every colour, radius, glow, type size, easing and spring as CSS custom properties        |
| [tokens.json](tokens.json)               | The same values for code and tools (W3C design tokens style), plus the logo colourways   |
| [stylesheet.html](stylesheet.html)       | The stylesheet as a page: logos, colours, type, surfaces and buttons, live. Open it from this folder |
| [stylesheet.png](stylesheet.png)         | A picture of that page, for sharing                                                      |
| [../AGENTS.md](../AGENTS.md)             | Rules and file picking for agents (and anyone in a hurry)                                |

The logo files themselves are in the repo root folders; the generator that makes them is in `process/generator/`.

The design language comes from the website (`hematite/website`): `src/app/globals.css`, the landing components and `src/lib/motion.ts`. This folder mirrors them as of 11 November 2026.
