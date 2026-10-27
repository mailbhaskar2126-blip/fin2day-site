"""Extra FIN2DAY pages: Tools (calculators), Glossary, Learn paths, home snapshot + tools teaser.
Called from build.py. Calculators are educational and use no live data."""
import html, os
from glossary import GLOSSARY

E = html.escape

LEARN = [
    ("Money basics", "Start here: the ideas behind almost every headline.",
     ["what-is-the-repo-rate", "how-sensex-nifty-work", "pe-ratio-explained", "sip-compounding-explained", "bond-prices-and-yields"]),
    ("How IPOs work", "From the offer document to listing day, with real Indian examples.",
     ["how-an-ipo-works", "lic-ipo-2022", "hyundai-india-ipo-2024", "jio-platforms-ipo-explained", "jio-ipo-subscription-who-bid"]),
    ("The RBI and interest rates", "What the repo rate is and how rate cycles play out.",
     ["what-is-the-repo-rate", "rbi-hiking-cycle-2022-23", "rbi-cutting-cycle-2025", "rbi-rate-hike-oct-2026", "fed-hike-rupee-fpi-2026"]),
    ("Trade wars and the world economy", "Tariffs, oil and why far-away decisions reach your wallet.",
     ["smoot-hawley-tariff-1930", "us-china-trade-war-2018-19", "us-tariffs-on-india-2025-26", "china-trade-surplus-india-2026", "oil-100-india-import-bill"]),
]

# slug, title, blurb, fields [(id,label,default,min,max,step,unit)], formula note
TOOLS = [
    ("sip-calculator", "SIP calculator", "See what a monthly investment could grow to at an assumed rate of return.",
     [("amt", "Monthly investment", 5000, 500, 200000, 500, "₹"), ("rate", "Expected return (p.a.)", 12, 1, 30, 0.5, "%"), ("yrs", "Time period", 10, 1, 40, 1, "years")],
     "Future value = P × [((1 + i)<sup>n</sup> − 1) ÷ i] × (1 + i), where P is the monthly amount, i is the monthly rate (annual rate ÷ 12) and n is the number of months. Instalments are assumed to be paid at the start of each month."),
    ("emi-calculator", "EMI calculator", "Work out the monthly instalment, total interest and total cost of a loan.",
     [("amt", "Loan amount", 1000000, 50000, 50000000, 50000, "₹"), ("rate", "Interest rate (p.a.)", 9, 1, 30, 0.05, "%"), ("yrs", "Loan tenure", 20, 1, 30, 1, "years")],
     "EMI = P × r × (1 + r)<sup>n</sup> ÷ [(1 + r)<sup>n</sup> − 1], where P is the loan, r is the monthly rate (annual rate ÷ 12) and n is the number of months. It ignores processing fees and floating-rate changes."),
    ("fd-calculator", "FD and lump-sum calculator", "How much a one-time deposit or investment grows with compounding.",
     [("amt", "Amount invested", 100000, 1000, 50000000, 1000, "₹"), ("rate", "Interest rate (p.a.)", 7, 1, 30, 0.1, "%"), ("yrs", "Time period", 5, 1, 30, 1, "years")],
     "Maturity = P × (1 + r ÷ (100 × k))<sup>k × t</sup>, where k is the number of compounding periods a year (4 for quarterly, the common bank FD practice) and t is the number of years. Interest is shown before tax."),
    ("inflation-calculator", "Inflation calculator", "What something costing you today could cost in the future, or what today's money is worth then.",
     [("amt", "Cost today", 100000, 1000, 100000000, 1000, "₹"), ("rate", "Inflation (p.a.)", 6, 1, 20, 0.1, "%"), ("yrs", "Years ahead", 10, 1, 40, 1, "years")],
     "Future cost = today's cost × (1 + i)<sup>n</sup>, where i is the yearly inflation rate and n is the number of years. Purchasing power of today's amount = today's amount ÷ (1 + i)<sup>n</sup>."),
]
SELECT = {"fd-calculator": ("freq", "Compounding", [("4", "Quarterly"), ("12", "Monthly"), ("2", "Half-yearly"), ("1", "Yearly")])}


def _tool_card(t):
    return (f'<a class="tool-card rv" href="/tools/{t[0]}.html"><h3>{E(t[1])}</h3><p>{E(t[2])}</p>'
            f'<span class="go">Open calculator →</span></a>')


def snapshot(ticker):
    want = ["Nifty 50", "Sensex", "Brent crude", "Rupee", "RBI repo", "CPI inflation"]
    d = {k: (v, c) for k, v, c in ticker}
    asof = next((v for k, v, c in ticker if k == "Closing data as of"), "")
    tiles = "".join(
        f'<div class="snap"><span class="k">{E(k)}</span><span class="v mono {d[k][1]}">{E(d[k][0])}</span></div>'
        for k in want if k in d)
    return (f'<section class="wrap snapshot rv" aria-label="Markets snapshot"><div class="snap-head"><div class="label">Markets snapshot</div>'
            f'<span class="asof">Closing data as of {E(asof)}</span></div><div class="snaps">{tiles}</div></section>')


def tools_teaser():
    cards = "".join(_tool_card(t) for t in TOOLS)
    return (f'<section class="block" id="tools"><div class="wrap"><div class="shead rv"><div><div class="label">Free tools</div>'
            f'<h2>Run your own numbers.</h2></div><a class="btn ghost" href="/tools/">All tools →</a></div>'
            f'<div class="tools-grid">{cards}</div></div></section>')


def _field(f):
    i, label, d, lo, hi, step, unit = f
    pre = '<span class="u">₹</span>' if unit == "₹" else ""
    post = f'<span class="u">{unit}</span>' if unit != "₹" else ""
    return (f'<div class="fld"><label for="{i}">{E(label)}</label><div class="inp">{pre}'
            f'<input id="{i}" type="number" inputmode="decimal" value="{d}" min="{lo}" max="{hi}" step="{step}">{post}</div>'
            f'<input class="rng" id="{i}-r" type="range" value="{d}" min="{lo}" max="{hi}" step="{step}" aria-label="{E(label)} slider"></div>')


def build(page, write, explainers, ticker, site):
    by_slug = {e["slug"]: e for e in explainers}
    for t in TOOLS:
        pass
    os.makedirs("tools", exist_ok=True)
    os.makedirs("learn", exist_ok=True)

    # Tools hub
    cards = "".join(_tool_card(t) for t in TOOLS)
    write("tools/index.html", page("tools/index.html", "Money tools",
        "Free calculators for SIP, EMI, fixed deposits and inflation, with the formulas shown.",
        f'<div class="page-head"><div class="wrap"><div class="label">Tools</div><h1>Run your own numbers.</h1>'
        f'<p>Simple calculators with the maths shown. They run in your browser and nothing you enter is stored or sent anywhere.</p></div></div>'
        f'<section class="block" style="padding-top:12px"><div class="wrap"><div class="tools-grid">{cards}</div>'
        f'<p class="note-sm">These are educational estimates based on the rates you enter. Real returns and loan terms vary. Nothing here is investment advice.</p></div></section>',
        "/tools/"))

    # Calculators
    for slug, title, blurb, fields, note in TOOLS:
        flds = "".join(_field(f) for f in fields)
        if slug in SELECT:
            sid, sl, opts = SELECT[slug]
            flds += (f'<div class="fld"><label for="{sid}">{sl}</label><div class="inp"><select id="{sid}">' +
                     "".join(f'<option value="{v}">{n}</option>' for v, n in opts) + '</select></div></div>')
        others = "".join(f'<a href="/tools/{o[0]}.html">{E(o[1])}</a>' for o in TOOLS if o[0] != slug)
        body = (f'<div class="page-head"><div class="wrap"><div class="label"><a href="/tools/" style="text-decoration:none">Tools</a></div><h1>{E(title)}</h1><p>{E(blurb)}</p></div></div>'
                f'<section class="block" style="padding-top:12px"><div class="wrap"><div class="calc" data-calc="{slug}">'
                f'<div class="calc-in">{flds}</div><div class="calc-out" aria-live="polite"></div></div>'
                f'<div class="calc-note"><h3>How it is worked out</h3><p>{note}</p>'
                f'<p class="note-sm">Educational estimate only. It assumes a constant rate for the whole period; real returns and rates change. Nothing here is investment advice.</p></div>'
                f'<div class="calc-more"><span>More tools</span>{others}</div></div></section>'
                f'<script src="/assets/tools.js" defer></script>')
        write(f"tools/{slug}.html", page(f"tools/{slug}.html", title, blurb, body, "/tools/"))

    # Glossary
    letters = sorted({g[0][0].upper() for g in GLOSSARY})
    az = "".join(f'<a href="#g-{l}">{l}</a>' for l in letters)
    items = []
    for term, d, slugs in sorted(GLOSSARY, key=lambda g: g[0].lower()):
        for s in slugs:
            assert s in by_slug, f"glossary slug missing: {s}"
        links = "".join(f' <a class="rd" href="/explainers/{s}.html">Read: {E(by_slug[s]["title"])} →</a>' for s in slugs[:1])
        items.append((term[0].upper(), f'<div class="gl" data-t="{E(term.lower())} {E(d.lower())}"><dt>{E(term)}</dt><dd>{E(d)}{links}</dd></div>'))
    groups = ""
    for l in letters:
        groups += f'<div class="gl-group" id="g-{l}"><h2>{l}</h2><dl>' + "".join(h for ll, h in items if ll == l) + '</dl></div>'
    write("glossary.html", page("glossary.html", "Finance glossary",
        "Plain-English definitions of the finance terms you meet in the news: repo rate, SIP, P/E, FPI and more.",
        f'<div class="page-head"><div class="wrap"><div class="label">Glossary</div><h1>Finance, in plain words.</h1>'
        f'<p>{len(GLOSSARY)} terms you meet in the news, explained without jargon.</p></div></div>'
        f'<section class="block" style="padding-top:12px"><div class="wrap narrow-wide">'
        f'<input class="search" id="gl-search" type="search" placeholder="Search terms…" aria-label="Search glossary">'
        f'<nav class="az" aria-label="Jump to letter">{az}</nav>{groups}'
        f'<p class="empty" id="gl-empty" hidden>No term matches that search.</p></div></section>', "/glossary.html"))

    # Learn hub
    paths = ""
    for i, (name, blurb, slugs) in enumerate(LEARN, 1):
        for s in slugs:
            assert s in by_slug, f"learn slug missing: {s}"
        steps = "".join(f'<li><a href="/explainers/{s}.html"><span class="n">{j}</span><span class="tt">{E(by_slug[s]["title"])}</span>'
                        f'<span class="mm">{by_slug[s]["mins"]} min</span></a></li>' for j, s in enumerate(slugs, 1))
        paths += f'<div class="path rv"><div class="label">Path {i}</div><h2>{E(name)}</h2><p>{E(blurb)}</p><ol>{steps}</ol></div>'
    write("learn/index.html", page("learn/index.html", "Learn",
        "Guided reading paths through FIN2DAY explainers: money basics, IPOs, the RBI and trade wars.",
        f'<div class="page-head"><div class="wrap"><div class="label">Learn</div><h1>Start here, in order.</h1>'
        f'<p>Reading paths that take you from the basics to the big stories, one explainer at a time. Stuck on a word? Try the <a href="/glossary.html">glossary</a>.</p></div></div>'
        f'<section class="block" style="padding-top:12px"><div class="wrap"><div class="paths">{paths}</div></div></section>', "/learn/"))

    return ["/tools/", "/glossary.html", "/learn/"] + [f"/tools/{t[0]}.html" for t in TOOLS]
