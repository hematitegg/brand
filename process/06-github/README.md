# Round 6: GitHub

11 November 2026. Branding for the hematitegg GitHub organisation.

- `01-avatars-and-readme.png`: avatar options G1–G6 (the plain emblem on GitHub dark, night, iron, steel, white) and a first org README with the big two-tone logo.
- `02-github-ideas.png`: GitHub-styled ideas: the emblem as contribution squares (P1 green, P2 steel, P3 steel on light), a contribution-graph banner, and a contribution strip under the logo.
- `03-readme-headers.png`: the README header as a green contribution grid behind the normal logo, three densities: H1 even, H2 halo, H3 edges.

**Picked: P1 as the org avatar and H3 as the README header**, both in GitHub's own greens. The final files are in `github/`, made by `generator/github.py`.

**Fix, 12 November 2026:** the first P1 export sat one cell left of centre (the lit emblem was 11 cells wide in an 18-cell grid, and the odd remainder was rounded down). `github.py` now nudges the sampling grid until the lit width and height have the same parity and centres on the lit cells: 4 empty columns each side, 2 rows top and bottom. Before and after: `04-avatar-centring-fix.png`.

**Fix, 13 November 2026:** the org README's header was blank in the GitHub mobile apps. They render the README through the REST API, which leaves relative image paths unresolved. `hematitegg/.github` now links the headers by absolute `raw.githubusercontent.com` URL, with the dark header as the `<img>` fallback. Keep it that way when the headers change: copy the new SVGs into `.github/profile/assets/` under the same names.
