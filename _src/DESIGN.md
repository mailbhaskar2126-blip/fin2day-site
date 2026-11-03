# FIN2DAY design system (v2)

The @fin2day Instagram carousels, carried to the web: a clean white front page in the spirit of Finshots, with every chart set as a self-contained, sourced card in the spirit of Statista.

## Colour

| Token | Hex | Use |
|---|---|---|
| `--white` | #FFFFFF | Page ground, cards |
| `--mist` | #F2F5FA | Secondary bands, market strip, calculator inputs |
| `--navy` | #0E1A2E | Text, rules, footer |
| `--ink-2` | #38455A | Body copy |
| `--mute` | #5E6B80 | Meta, captions, axis labels |
| `--rule` | #D7DEE9 | Hairlines and card borders |
| `--blue` | #1D46C8 | The only accent: links, buttons, the "2", chart tab, primary series, newsletter band |
| `--blue-deep` | #142F8C | Button hover |
| `--blue-soft` | #E9EEFB | Beat tags, callouts |
| `--up` / `--down` / `--warn` | #0B7A47 / #C4332B / #A86A06 | Market moves only, never decoration |

Old token names (`--ink`, `--brass`, `--green`, `--red`, `--panel`, `--card` and so on) are kept as aliases, so pages built for v1 render in v2 without template changes.

## Type

- **Libre Caslon Text** 700: headlines, card titles, big figures, wordmark. Echoes the serif on the carousels.
- **Schibsted Grotesk** 400–700: body, UI, meta and all chart text (tabular figures). A grotesk drawn for a news publisher.
- Scale: 13 / 14 / 15.5 / 17 (body) / 19–22 (card titles) / 30–44 (section heads) / 36–58 (front-page headline).
- No uppercase eyebrows. Meta items sit side by side with spacing, not dot separators.

## Structure

- 1200px measure, `--gut` side padding (16–40px).
- Sections separated by 1px rules or a mist band; lists and tables start with a 2px navy rule.
- Corners 4–6px. One shadow only, under today's chart card.

## Chart card (signature)

`.cc` anatomy, top to bottom:
1. `.cc-h` – 4px blue tab beside the serif title (`h2` for the lead chart, `h3` in galleries).
2. `.cc-s` – one line saying exactly what is measured and in what unit.
3. `.chart.ic[data-spec]` – rendered by `assets/charts.js`.
4. `.cc-f` (source and wordmark) or `.cc-foot` (beat tag, date and wordmark).

`charts.js` reads the same `data-spec` JSON as v1 (`h` horizontal bars, `v` vertical bars, `l` line) and maps v1 colours onto v2 series tokens while keeping their meaning (ink → blue, green → up, red → down, amber → warn). Bars print their values; lines get an end-value pill and hover/tap readouts; chart text stays at a readable px size on any width.

## Motion

One moment only: charts draw in once when they scroll into view (bars grow, lines trace). Nothing else animates. All of it is off under `prefers-reduced-motion`.

## Status

Every page of fin2day.pages.dev (as of 3 Nov 2026) is mirrored in this folder with the changes below already applied. Line-chart annotations that sit on a data point render as value pills; reference-line labels (targets, limits) render as plain coloured text.

## Adopting it in the generator

1. Replace `assets/style.css` and `assets/charts.js` with the v2 files.
2. In every page template, swap the Google Fonts link for `family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Schibsted+Grotesk:wght@400;500;600;700`.
3. Remove the `lenis.min.js` and `motion.js` script tags.
4. Set `theme-color` to `#FFFFFF`.
5. Use `index.html` from this folder as the homepage template. Its chart cards are the pattern for explainer listings.
