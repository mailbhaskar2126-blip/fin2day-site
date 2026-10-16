# FIN2DAY website: how to publish a story

This folder is not published (Netlify returns 404 for `/_src/*`, see `/_redirects`).
Netlify deploys the repo root automatically on every push to `main`. There is no build
step on Netlify: run the build locally and commit the generated HTML.

## Files
- `content/<slug>.json` — story metadata (see fields below)
- `content/<slug>.html` — story body (HTML fragment, charts inline as SVG)
- `content/<slug>.hero.svg` — optional homepage chart (otherwise the first chart in the body is used)
- `content/ticker.json` — homepage ticker: list of `[label, value, "up" | "dn" | ""]`
- `charts.py` — SVG chart helpers (`hbars`, `vbars`, `steps`, `line`, `flow`, `chart`, `save`)
  Charts animate and show hover/tap readouts automatically (`assets/motion.js`). Bar readouts use the bar's own
  label and value. `line()` points carry their exact value in `data-tip` (pass `tipfmt=` to control the format).
- `example_stories.py` — reference examples of real stories (do not run)
- `build.py` — generates every page into the repo root. Run: `python3 _src/build.py`

## Story JSON fields
`slug` (kebab-case, unique), `date` (YYYY-MM-DD, IST date of publication), `order` (int; higher = shown first
among stories with the same date), `topic` (space-separated from: `concepts ipo rbi global trade markets`),
`tag` (short label: Basics, IPO, RBI, Global, Trade, Markets, Inflation, World markets), `tag_class` (`"red"` for RBI/inflation, else `""`),
`title`, `short` (card/hero headline, under ~70 chars), `dek` (1–2 sentence summary), `card` (1 sentence teaser),
`hero_src` (optional, e.g. "Data: NSE, BSE"), `sources` (list of `[name, url]`).
Read time and display dates are computed automatically by build.py. Never type them by hand.
The newest story (by date, then order) becomes the homepage lead story.

## Weekly schedule (all times IST)
| Day | Beat story (morning) | Topic tag |
|---|---|---|
| Mon | Money basics (a concept: inflation, GDP, SIP, compounding, CRR, G-secs, fiscal deficit…) | `concepts` |
| Tue | IPO watch (upcoming/recent IPO: what the company does, pricing, subscription, OFS vs fresh; or a past landmark IPO) | `ipo` |
| Wed | RBI & rates (latest RBI action, bank rates, liquidity, or a past cycle) | `rbi` |
| Thu | Global economy (Fed, China, oil, dollar, and how it ripples into India) | `global` |
| Fri | Trade wars (one historical OR one current tariff/trade fight) | `trade` |
| Mon–Fri, after 15:30 close | Indian markets update: Nifty/Sensex closes, % moves, sectors, top movers, why, flows, what's next | `markets` |
| Sat, Sun | World markets: NYSE/Nasdaq/S&P 500, Shanghai/Hang Seng, Nikkei, Europe — what moved and what it means for India | `markets global` |
If big news breaks, it can replace that day's beat story. Skip the Indian markets update on NSE trading holidays.
Do not repeat a topic already covered: check existing slugs and titles in `content/` first.

## Editorial rules (non-negotiable)
1. Every number must come from a source fetched during research (official data, exchanges, RBI/MoSPI/PIB,
   established news outlets). No numbers from memory for anything current. If a figure can't be verified, leave it out.
2. List every source used in `sources`. Label own calculations "FIN2DAY calculation" and illustrations "Illustration".
3. Website stories go deeper than the Instagram post: up to 1,000 words, 2–4 charts of their own, sections with `<h2>`.
4. Neutral and factual. No buy/sell advice; end with "Educational content only" where relevant.
5. Plain English, short sentences, Indian number formats (₹ lakh, crore). Link related explainers with
   `<a href="/explainers/<slug>.html">`.
6. Allowed body elements: `<p> <h2> <strong> <em> <ul class="points"><li><b>Label</b><span>text</span></li></ul>`,
   `<div class="callout"><b>Title</b><p>…</p></div>`, charts via `chart(svg, caption)`.
7. Markets updates: also refresh `content/ticker.json`. The first item is always `["Closing data as of", "<D Mon YYYY>", ""]`.
   Then Nifty 50, Sensex, Brent crude, Rupee and other macro items. Always exact verified figures with units
   (e.g. `$105.69 / bbl`, `₹95.36 / $`), never approximations like "above $100". The ticker is not live; it
   shows the latest closing figures, refreshed by the daily markets update.

## Publish checklist
1. Write the story with a small script using `charts.py` (see `example_stories.py`), save to `content/`.
2. `python3 _src/build.py`
3. Check: chart labels don't overlap or clip (screenshot the page with Playwright at 1280px and 390px),
   no horizontal overflow on phone, all internal links exist, word count ≤ 1,000.
4. `git add -A && git commit -m "..." && git push`. Netlify publishes within ~1 minute.
5. Verify the live page at https://fin2day.netlify.app/explainers/<slug>.html
