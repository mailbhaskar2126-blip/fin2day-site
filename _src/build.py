"""Generates the FIN2DAY static site. Run: python3 build.py"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extras, enhance, thumbs

SITE = "https://fin2day.pages.dev"
IG = "https://www.instagram.com/fin2day/"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Schibsted+Grotesk:wght@400;500;600;700&display=swap">')
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='10' fill='%231D46C8'/%3E"
           "%3Ctext x='32' y='47' font-family='Georgia,serif' font-weight='700' font-size='42' fill='%23fff' text-anchor='middle'%3E2%3C/text%3E%3C/svg%3E")
# Shared icons: arrow for links, check for lists. Use <svg aria-hidden="true"><use href="#i-go"/></svg>.
ICONS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-go" viewBox="0 0 16 16"><path d="M2.5 8h10M8.5 3.8 12.7 8l-4.2 4.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="i-check" viewBox="0 0 20 20"><circle cx="10" cy="10" r="8.6" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="m6.2 10.2 2.6 2.6 5-5.4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
</svg>"""
GO = '<svg aria-hidden="true"><use href="#i-go"/></svg>'

NAV = [("/", "Home"), ("/explainers/", "Explainers"), ("/learn/", "Learn"), ("/tools/", "Tools"), ("/glossary.html", "Glossary"), ("/about.html", "About"), ("/contact.html", "Contact")]


def page(path, title, desc, body, active=None, og_type="website", pre=""):
    url = SITE + ("/" if path == "index.html" else "/" + path.replace("index.html", ""))
    nav = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if active == h else ""}>{t}</a>' for h, t in NAV)
    full_title = title if title.startswith("FIN2DAY") else f"{title} | FIN2DAY"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="FIN2DAY">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="{FAVICON}">
{FONTS}
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<script>document.documentElement.classList.add('js')</script>
{ICONS}
<a class="skip" href="#main">Skip to content</a>
<header class="mast">
  <div class="wrap">
    <a class="logo" href="/" aria-label="FIN2DAY home"><span class="wm">FIN<b>2</b>DAY</span><span class="by">Finance, explained in 2 minutes</span></a>
    <nav class="nav" id="nav" aria-label="Main">
      {nav}
      <a class="btn" href="/#newsletter">Get the daily brief</a>
    </nav>
    <a class="btn sm mast-cta" href="/#newsletter">Get the daily brief</a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>
</header>
{pre}
<main id="main">
{body}
</main>
<footer>
  <div class="fbox">
    <div class="fgrid">
      <div><div class="fbig">FIN<b>2</b>DAY</div><p class="ftag">Today’s money news, explained in 2 minutes.</p></div>
      <div class="fcols">
        <div class="flinks"><span>Read</span><a href="/explainers/">All explainers</a><a href="/explainers/#rbi">RBI</a><a href="/explainers/#ipo">IPOs</a><a href="/explainers/#global">Global economy</a><a href="/explainers/#markets">Markets</a><a href="/learn/">Learn</a><a href="/tools/">Money tools</a><a href="/glossary.html">Glossary</a></div>
        <div class="flinks"><span>FIN2DAY</span><a href="/about.html">About</a><a href="/contact.html">Contact</a><a href="/#newsletter">Newsletter</a><a href="{IG}" target="_blank" rel="noopener">Instagram</a></div>
        <div class="flinks"><span>Legal</span><a href="/disclaimer.html">Disclaimer</a><a href="/disclaimer.html#privacy">Privacy</a></div>
      </div>
    </div>
    <p class="disc">FIN2DAY publishes educational content only. Nothing here is investment, legal or tax advice. Do your own research or speak to a SEBI-registered adviser before making financial decisions. © 2026 FIN2DAY.</p>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
<script src="/assets/charts.js" defer></script>
</body>
</html>
"""


def newsletter_form(fid="newsletter"):
    return f"""<form class="form" name="newsletter" method="POST" novalidate>
      <input type="hidden" name="form-name" value="newsletter">
      <p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <label for="{fid}-email">Your email</label>
      <div class="field">
        <input id="{fid}-email" name="email" type="email" placeholder="you@example.com" autocomplete="email" required>
        <button class="btn brass" type="submit">Join the list</button>
      </div>
      <div class="msg" role="status" aria-live="polite"></div>
      <p class="fine">One email on weekday mornings. No spam, and you can unsubscribe any time. See our <a href="/disclaimer.html#privacy">privacy note</a>.</p>
    </form>"""


def cta_panel(fid, label, heading, intro, e):
    chart = f'{e["hero_html"]}' if e.get("hero") else ""
    return f"""<div class="ctap rv">
    <div class="txt">
      <div class="label">{label}</div>
      <h2>{heading}</h2>
      <p class="intro">{intro}</p>
      <div style="margin-top:26px">{newsletter_form(fid)}</div>
    </div>
    <div class="vis" aria-hidden="true">
      <div class="mail">
        <div class="from"><b>FIN2DAY Daily Brief</b><span>{e['date_label']}</span></div>
        <h4>{e['short']}</h4>
        {chart}
      </div>
    </div>
  </div>"""


# ----------------------------------------------------------------------------
# Content: one story = _src/content/<slug>.json (meta) + <slug>.html (body)
# optional <slug>.hero.svg (homepage chart; else the first chart in the body).
# Read time and display dates are worked out from the content automatically.
# ----------------------------------------------------------------------------
import json, glob, re, math, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
ROOT = os.path.dirname(HERE)

def _words(body):
    t = re.sub(r"<svg.*?</svg>", " ", body, flags=re.S)
    t = re.sub(r'<div class="cap">.*?</div>', " ", t, flags=re.S)
    return len(html.unescape(re.sub(r"<[^>]+>", " ", t)).split())

# Stories whose charts use the interactive renderer (first batch; add slugs to roll out).
ENHANCED = None  # all stories now use the interactive renderer


def load_stories():
    out = []
    for jf in glob.glob(os.path.join(CONTENT, "*.json")):
        if jf.endswith(("ticker.json", "thumbs.json")):
            continue
        m = json.load(open(jf))
        base = jf[:-5]
        m["body"] = open(base + ".html").read()
        hero = base + ".hero.svg"
        if os.path.exists(hero):
            m["hero"] = open(hero).read()
        else:
            f = re.search(r"<svg.*?</svg>", m["body"], re.S)
            m["hero"] = f.group(0) if f else ""
        m["body_ic"] = enhance.enhance(m["body"])
        m["hero_html"] = enhance.enhance(f'<div class="chart">{m["hero"]}</div>') if m["hero"] else ""
        m["mins"] = max(2, math.ceil(_words(m["body"]) / 220))
        d = datetime.date.fromisoformat(m["date"])
        m["date_label"] = f"{d.day} {d.strftime('%b %Y')}"
        m.setdefault("tag_class", "")
        out.append(m)
    out.sort(key=lambda m: (m["date"], m.get("order", 0)), reverse=True)
    return out

EXPLAINERS = load_stories()
SOURCES = {e["slug"]: e["sources"] for e in EXPLAINERS}
ARTICLE_BODIES = {e["slug"]: e["body_ic"] for e in EXPLAINERS}
TICKER = json.load(open(os.path.join(CONTENT, "ticker.json")))


def share_bar():
    return """<div class="share" aria-label="Share this explainer">
  <button class="btn sm" data-share="whatsapp">Share on WhatsApp</button>
  <button class="btn sm ghost" data-share="x">Share on X</button>
  <button class="btn sm ghost" data-share="copy">Copy link</button>
  <button class="btn sm ghost" data-share="native">More…</button>
  <span class="msg" role="status" aria-live="polite"></span>
</div>"""


def story_card(e, link_prefix="/explainers/"):
    t, cls = e["tag"], e["tag_class"]
    href = f"{link_prefix}{e['slug']}.html"
    return f"""<article class="story" data-topic="{e['topic']}">
  {thumbs.thumb(e, href)}
  <div class="meta"><span class="tag {cls}">{t}</span><span>{e['date_label']}</span><span>{e['mins']} min</span></div>
  <h3><a href="{href}">{e['short']}</a></h3>
  <p>{e['card']}</p>
  <a class="read" href="{href}">Read the explainer {GO}</a>
</article>"""


def build():
    os.chdir(ROOT)
    os.makedirs("explainers", exist_ok=True)
    cards = "\n".join(story_card(e) for e in EXPLAINERS)
    home_cards = "\n".join(story_card(e) for e in EXPLAINERS[:3])

    # ---------------- Home ----------------
    lead = EXPLAINERS[0]
    tick = [t for t in TICKER if t[0] != "Closing data as of"]
    asof = next((t[1] for t in TICKER if t[0] == "Closing data as of"), "")
    close_items = "".join(
        f'<li><span class="k">{html.escape(k)}</span><span class="v{(" " + c) if c else ""}">{html.escape(v)}</span></li>' for k, v, c in tick)
    close_strip = f"""<section class="close" aria-labelledby="close-h">
  <div class="wrap">
    <h2 id="close-h">Markets at close <span>{html.escape(asof)}</span></h2>
    <ul>{close_items}</ul>
  </div>
</section>"""

    def chart_bits(e):
        """(title, measure line, source) for a story's lead chart, read from the caption under it in the body."""
        cap = ""
        i = e["body"].find(e["hero"]) if e["hero"] else -1
        if i >= 0:
            m = re.search(r'<div class="cap">(.*?)</div>', e["body"][i + len(e["hero"]):i + len(e["hero"]) + 1500], re.S)
            if m:
                cap = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
                cap = re.sub(r"\s+", " ", cap).replace(" .", ".").replace(" ,", ",").replace(" :", ":").strip()
        parts = re.split(r"\s*Sources?:\s*", cap, maxsplit=1)
        text = parts[0].strip().rstrip(".")
        src = ("Source: " + parts[1].strip().rstrip(".")) if len(parts) > 1 else (e.get("hero_src") or "Sources listed in the explainer")
        bits = [s.strip() for s in re.split(r"(?<=[a-z0-9)%])\.\s+", text) if s.strip()]
        title = bits[0] if bits else ""
        sub = ". ".join(bits[1:])
        return title, sub, src

    def gallery_card(e):
        title, sub, _ = chart_bits(e)
        measure = title + (f". {sub}" if sub else "")
        return f"""<article class="cc">
        <div class="cc-h"><h3><a href="/explainers/{e['slug']}.html">{e['short']}</a></h3></div>
        {f'<p class="cc-s">{measure}</p>' if measure else ''}
        <div class="cc-body">{e["hero_html"]}</div>
        <div class="cc-foot"><span class="meta"><span class="tag {e['tag_class']}">{e['tag']}</span><span>{e['date_label']}</span></span><span class="wm" style="font-size:14px">FIN<b>2</b>DAY</span></div>
      </article>"""

    gallery = "".join(gallery_card(e) for e in [e for e in EXPLAINERS[1:] if e["hero"]][:6])

    lt, ls, lsrc = chart_bits(lead)
    hero_card = f"""<figure class="cc" style="margin:0">
      <div class="cc-h"><h2>{lt or "Today’s story in one chart"}</h2></div>
      {f'<p class="cc-s">{ls}</p>' if ls else ''}
      <div class="cc-body">{lead["hero_html"]}</div>
      <figcaption class="cc-f"><span class="cc-src">{lsrc}</span><span class="wm">FIN<b>2</b>DAY</span></figcaption>
    </figure>""" if lead["hero"] else ""
    prev = EXPLAINERS[1] if len(EXPLAINERS) > 1 else None
    also = f"""<div class="also">
      <span>Previous story, {prev['date_label']}</span>
      <a href="/explainers/{prev['slug']}.html">{prev['short']}</a>
    </div>""" if prev else ""

    # The week as a planner: one card per beat day, the weekend shared, and the daily markets update as a bar under Mon-Fri.
    def latest(test):
        return next((e for e in EXPLAINERS if test(e)), None)
    def topics(e):
        return e["topic"].split()
    WEEK = [  # data-dow uses JavaScript's getDay(): 0 = Sunday
        ("1", "Mon", "Money basics", "Repo rate, inflation, bonds, P/E. The ideas behind the headlines.", "concepts", lambda e: "concepts" in topics(e)),
        ("2", "Tue", "IPO watch", "What the company does, how it’s priced, and what to read before you bid.", "ipo", lambda e: "ipo" in topics(e)),
        ("3", "Wed", "RBI &amp; rates", "Every policy move, and what it does to your EMI and FD.", "rbi", lambda e: "rbi" in topics(e)),
        ("4", "Thu", "Global economy", "The Fed, China, oil and the dollar, and how they ripple into India.", "global", lambda e: "global" in topics(e) and e["tag"] != "World markets"),
        ("5", "Fri", "Trade wars", "Who taxes whose goods, why, and who pays in the end.", "trade", lambda e: "trade" in topics(e)),
        ("6 0", "Sat &amp; Sun", "World markets", "How New York, London, Frankfurt, Hong Kong and Shanghai closed the week.", "global", lambda e: e["tag"] == "World markets"),
    ]
    def day_card(dow, day, name, desc, key, test):
        e = latest(test)
        last = (f'<a class="wk-latest" href="/explainers/{e["slug"]}.html"><span>Latest, {e["date_label"]}</span>{e["short"]}</a>' if e else "")
        weekend = " wk-weekend" if " " in dow else ""
        cover = f'<div class="wk-cover">{thumbs.cover(e)}</div>' if weekend and e else ""
        return (f'<div class="wk-day{weekend}" data-dow="{dow}"><span class="wk-d">{day}</span><h3>{name}</h3><p>{desc}</p>'
                f'{cover}{last}<a class="go" href="/explainers/#{key}">Browse {GO}</a></div>')
    mk = latest(lambda e: e["tag"] == "Markets")
    mk_last = f'<a class="wk-latest" href="/explainers/{mk["slug"]}.html"><span>Latest, {mk["date_label"]}</span>{mk["short"]}</a>' if mk else ""
    sched = (f'<div class="week">{"".join(day_card(*d) for d in WEEK)}'
             f'<div class="wk-markets"><div><span class="wk-d">Mon to Fri, after the 3:30 pm close</span><h3>Markets</h3>'
             f'<p>Why the market moved, and which sectors are booming or bust.</p></div>{mk_last}'
             f'<a class="go" href="/explainers/#markets">Browse {GO}</a></div></div>')

    CHECK = '<svg aria-hidden="true"><use href="#i-check"/></svg>'
    home = f"""
<section class="front" aria-labelledby="today-h">
  <div class="wrap front-grid">
    <div class="lead">
      <h1 id="today-h">{lead['short']}</h1>
      <p class="dek">{lead['dek']}</p>
      <div class="meta"><span class="tag {lead['tag_class']}">{lead['tag']}</span><span>Today’s story, {lead['date_label']}</span><span>{lead['mins']} min read</span></div>
      <div class="acts">
        <a class="btn" href="/explainers/{lead['slug']}.html">Read today’s story</a>
        <a class="go" href="#newsletter">Get it by email each morning {GO}</a>
      </div>
    </div>
    {also}
    {hero_card}
  </div>
</section>

<section class="sec" id="charts" aria-labelledby="charts-h">
  <div class="wrap">
    <div class="shead">
      <div><h2 id="charts-h">The week in charts</h2><p>Every explainer is built on one chart from a cited source. Hover or tap a bar or line for the exact figure.</p></div>
      <a class="go" href="/explainers/">All explainers {GO}</a>
    </div>
    <div class="gallery">{gallery}</div>
  </div>
</section>

<section class="sec band" id="topics" aria-labelledby="topics-h">
  <div class="wrap">
    <div class="shead"><div><h2 id="topics-h">What we explain, and when</h2><p>A new beat every weekday, a markets update after every trading day, and world markets at the weekend. When big news breaks, it jumps the queue.</p></div></div>
    {sched}
  </div>
</section>

{extras.tools_teaser()}

<section class="sec band" id="how" aria-labelledby="how-h">
  <div class="wrap">
    <div class="shead"><div><h2 id="how-h">From headline to “oh, I get it”</h2><p>The same three steps, every single day.</p></div></div>
    <ol class="flow">
      <li><div class="fl-art"><svg viewBox="0 0 240 132" aria-hidden="true"><rect x="34" y="12" width="172" height="22" rx="4" fill="#E6ECF5"/><rect x="44" y="20" width="96" height="6" rx="3" fill="#C3CEDF"/><rect x="24" y="42" width="192" height="30" rx="5" fill="#1D46C8"/><rect x="36" y="52" width="112" height="10" rx="3" fill="#fff"/><circle cx="196" cy="57" r="9" fill="#fff"/><path d="m191.5 57 3.2 3.2 5.3-6" stroke="#1D46C8" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/><rect x="34" y="80" width="172" height="22" rx="4" fill="#E6ECF5"/><rect x="44" y="88" width="120" height="6" rx="3" fill="#C3CEDF"/><rect x="34" y="108" width="172" height="20" rx="4" fill="#E6ECF5"/><rect x="44" y="115" width="80" height="6" rx="3" fill="#C3CEDF"/></svg></div>
        <span class="fl-n">Step 1</span><b>News breaks</b><span class="fl-t">We pick the one story each day that actually affects your money.</span></li>
      <li><div class="fl-art"><svg viewBox="0 0 240 132" aria-hidden="true"><rect x="40" y="8" width="160" height="116" rx="6" fill="#fff" stroke="#D7DEE9"/><rect x="54" y="22" width="4" height="14" rx="1" fill="#1D46C8"/><rect x="64" y="24" width="78" height="9" rx="3" fill="#0E1A2E"/><rect x="62" y="74" width="16" height="26" rx="2" fill="#8EA6E6"/><rect x="86" y="62" width="16" height="38" rx="2" fill="#8EA6E6"/><rect x="110" y="68" width="16" height="32" rx="2" fill="#8EA6E6"/><rect x="134" y="54" width="16" height="46" rx="2" fill="#8EA6E6"/><rect x="158" y="42" width="16" height="58" rx="2" fill="#1D46C8"/><line x1="54" x2="186" y1="100.5" y2="100.5" stroke="#0E1A2E" stroke-width="1.4"/><rect x="54" y="109" width="64" height="5" rx="2.5" fill="#C3CEDF"/><circle cx="190" cy="16" r="12" fill="#0B7A47"/><path d="m184.5 16 3.6 3.6 6.4-7" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <span class="fl-n">Step 2</span><b>We break it down</b><span class="fl-t">Plain words, a real chart, and every number checked against its source.</span></li>
      <li><div class="fl-art"><svg viewBox="0 0 240 132" aria-hidden="true"><rect x="50" y="22" width="44" height="80" rx="6" fill="#C3CEDF"/><rect x="146" y="22" width="44" height="80" rx="6" fill="#C3CEDF"/><rect x="84" y="4" width="72" height="124" rx="13" fill="#0E1A2E"/><rect x="90" y="14" width="60" height="94" rx="5" fill="#1D46C8"/><rect x="98" y="24" width="30" height="4" rx="2" fill="#fff" opacity=".7"/><text x="98" y="64" font-family="Libre Caslon Text,Georgia,serif" font-weight="700" font-size="24" fill="#fff">2</text><text x="98" y="82" font-family="Schibsted Grotesk,Arial,sans-serif" font-weight="600" font-size="11" fill="#fff">minutes</text><rect x="98" y="92" width="40" height="4" rx="2" fill="#fff" opacity=".5"/><circle cx="111" cy="118" r="2.5" fill="#fff"/><circle cx="120" cy="118" r="2.5" fill="#fff" opacity=".45"/><circle cx="129" cy="118" r="2.5" fill="#fff" opacity=".45"/></svg></div>
        <span class="fl-n">Step 3</span><b>You get it in 2 minutes</b><span class="fl-t">As an Instagram carousel, a reel, and a full explainer right here.</span></li>
    </ol>
    <ul class="promises-row">
      <li>{CHECK}<span><b>One story a day.</b> The one that matters most, not a feed of twenty.</span></li>
      <li>{CHECK}<span><b>Every number sourced.</b> RBI, SEBI, NSE, BSE, PIB, MoSPI, Reuters and more, listed in each explainer.</span></li>
      <li>{CHECK}<span><b>No stock tips.</b> We explain. We never tell you what to buy.</span></li>
    </ul>
  </div>
</section>

<section class="sec" id="faq" aria-labelledby="faq-h">
  <div class="wrap faq-grid">
    <div class="faq-side">
      <h2 id="faq-h">Good to know</h2>
      <div class="ask-card">
        <b>Still curious?</b>
        <p>Suggest a topic, point out a mistake, or just ask. We read everything.</p>
        <div class="ask-acts"><a class="btn sm" href="/contact.html">Contact us</a><a class="btn sm ghost" href="{IG}" target="_blank" rel="noopener">DM on Instagram</a></div>
      </div>
    </div>
    <div class="faq faq-cards">
      <details><summary>Is this investment advice?</summary><p>No. FIN2DAY explains what happened and why. We never recommend buying or selling anything. For decisions about your money, talk to a SEBI-registered adviser.</p></details>
      <details><summary>How often do you post?</summary><p>Every day. Monday is money basics, Tuesday IPOs, Wednesday the RBI and rates, Thursday the global economy and Friday trade wars. After every trading day there is a markets update, and on weekends we cover world markets like the NYSE and Shanghai. When big news breaks, we cover it the same day.</p></details>
      <details><summary>Is it free?</summary><p>Yes. The Instagram page, the site and the newsletter are all free.</p></details>
      <details><summary>Where do the numbers come from?</summary><p>From primary sources like the RBI, SEBI, government releases, and established news agencies. Every explainer lists its sources at the bottom.</p></details>
      <details><summary>Can I suggest a topic?</summary><p>Please do. Use the <a href="/contact.html">contact form</a> or DM us on <a href="{IG}" target="_blank" rel="noopener">Instagram</a>.</p></details>
    </div>
  </div>
</section>

<section class="brief" id="newsletter" aria-labelledby="brief-h">
  <div class="wrap">
    <div>
      <h2 id="brief-h">Get the story before your first meeting</h2>
      <p class="intro">One email every weekday morning: today’s story, one chart, and what it means for you. Free, and you can leave any time.</p>
    </div>
    {newsletter_form("home").replace('class="btn brass"', 'class="btn light"')}
  </div>
</section>
"""
    open("index.html", "w").write(page("index.html", "FIN2DAY | Finance, Explained",
        "Today's money news, explained in 2 minutes. Markets, IPOs, the RBI and the global economy in plain words, with real charts.", home, "/", pre=close_strip))

    # ---------------- Explainers list ----------------
    chips = "".join(f'<button class="chip" data-filter="{k}" aria-pressed="false">{v}</button>' for k, v in
                    [("all", "All"), ("rbi", "RBI"), ("ipo", "IPOs"), ("markets", "Markets"), ("global", "Global economy"), ("trade", "Trade wars"), ("concepts", "Concepts")])
    lst = f"""
<div class="page-head"><div class="wrap">
  <div class="label">Explainers</div>
  <h1>Every story, explained.</h1>
  <p>Filter by topic, or start with the latest. New explainers go up as the news breaks.</p>
</div></div>
<section class="block" style="padding-top:12px"><div class="wrap">
  <input class="search" id="ex-search" type="search" placeholder="Search explainers…" aria-label="Search explainers">
  <div class="filters" role="group" aria-label="Filter by topic">{chips}</div>
  <div class="stories">{cards}</div>
  <p class="empty" id="empty" hidden>No explainers on this topic yet. <a href="/#newsletter">Join the newsletter</a> to get the first one, or <a href="/explainers/">see all explainers</a>.</p>
</div></section>
"""
    open("explainers/index.html", "w").write(page("explainers/index.html", "Explainers",
        "All FIN2DAY explainers: RBI, IPOs, markets, global economy and trade wars, explained in plain words.", lst, "/explainers/"))

    extra_urls = extras.build(page, lambda p, c: open(p, "w").write(c), EXPLAINERS, TICKER, SITE)

    # ---------------- Articles ----------------
    for i, e in enumerate(EXPLAINERS):
        t, cls = e["tag"], e["tag_class"]
        nxt = EXPLAINERS[(i + 1) % len(EXPLAINERS)]
        srcs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(n)}</a></li>' for n, u in SOURCES[e["slug"]])
        body = f"""
<div class="wrap narrow">
  <p class="crumbs"><a href="/">Home</a> / <a href="/explainers/">Explainers</a> / {t}</p>
  <header class="article-head">
    <div class="byline"><span class="tag {cls}">{t}</span><span>{e['date_label']}</span><span>{e['mins']} min read</span></div>
    <h1>{e['title']}</h1>
    <p class="dek">{e['dek']}</p>
  </header>
  {thumbs.figure(e)}
  <div class="prose">{ARTICLE_BODIES[e['slug']]}</div>
  {share_bar()}
  <div class="sources"><b>Sources</b><ol>{srcs}</ol>
  <p>Educational content only. Not investment advice. Spotted an error? <a href="/contact.html">Tell us</a>.</p></div>
  <div class="next"><div class="label">Read next</div>
    <h2 style="font-size:clamp(24px,2.8vw,32px);margin-top:10px"><a href="/explainers/{nxt['slug']}.html">{nxt['short']} →</a></h2>
  </div>
</div>
<section class="block"><div class="wrap">
  {cta_panel("art", "The daily brief", "Liked this? Get one every morning.", "Today's story, one chart, and what it means for you.", EXPLAINERS[0])}
</div></section>
"""
        open(f"explainers/{e['slug']}.html", "w").write(page(f"explainers/{e['slug']}.html", e["short"], e["dek"], body, "/explainers/", "article"))

    # ---------------- About ----------------
    about = f"""
<div class="page-head"><div class="wrap">
  <div class="label">About</div>
  <h1>Finance news is written for people who already understand it.</h1>
  <p>FIN2DAY is for everyone else.</p>
</div></div>
<section class="block" style="padding-top:0"><div class="wrap"><div class="page-body prose" style="max-width:none"><div class="narrow">
  <p>Every day there's a headline about the repo rate, an IPO, a tariff or an oil shock. Most coverage assumes you already know what those words mean and why they matter. FIN2DAY starts from the other end: what happened, why, and what it means for your EMI, your savings and your job.</p>
  <h2>What we promise</h2>
  <ul class="points">
    <li><b>One story</b><span>The one that matters most each day, not a feed of twenty.</span></li>
    <li><b>Real numbers</b><span>Every figure comes from a primary source or an established news agency, and we list them.</span></li>
    <li><b>No tips</b><span>We explain. We never tell you what to buy or sell.</span></li>
    <li><b>Both sides</b><span>On contested topics, we lay out the facts and the main arguments, and let you decide.</span></li>
  </ul>
  <h2>Where to find us</h2>
  <p>Daily carousels and reels on <a href="{IG}" target="_blank" rel="noopener">Instagram @fin2day</a>, full explainers here, and a weekday-morning <a href="/#newsletter">newsletter</a>.</p>
  <div class="cta-row" style="margin-top:28px"><a class="btn" href="/explainers/">Read the explainers</a><a class="btn ghost" href="/contact.html">Get in touch</a></div>
</div></div></div></section>
"""
    open("about.html", "w").write(page("about.html", "About", "What FIN2DAY is: daily finance news explained in plain words, with real charts and no stock tips.", about, "/about.html"))

    # ---------------- Contact ----------------
    contact = f"""
<div class="page-head"><div class="wrap">
  <div class="label">Contact</div>
  <h1>Say hello.</h1>
  <p>Suggest a topic, point out a mistake, or ask about working together. We read everything.</p>
</div></div>
<section class="block" style="padding-top:0"><div class="wrap split">
  <div class="rv">
    <h2>Other ways to reach us</h2>
    <p>The quickest way is a DM on <a href="{IG}" target="_blank" rel="noopener">Instagram @fin2day</a>.</p>
    <p>Found an error in an explainer? Tell us which one and what's wrong, and we'll fix it and note the correction.</p>
  </div>
  <form class="form card-form rv" name="contact" method="POST" novalidate>
    <input type="hidden" name="form-name" value="contact">
    <p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
    <div class="row"><label for="c-name">Name (required)</label><input id="c-name" name="name" autocomplete="name" required></div>
    <div class="row"><label for="c-email">Email (required)</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
    <div class="row"><label for="c-type">What's it about?</label>
      <select id="c-type" name="type"><option>Topic suggestion</option><option>Correction</option><option>Collaboration</option><option>Something else</option></select></div>
    <div class="row"><label for="c-msg">Message (required)</label><textarea id="c-msg" name="message" required></textarea></div>
    <button class="btn brass" type="submit">Send message</button>
    <div class="msg" role="status" aria-live="polite"></div>
  </form>
</div></section>
"""
    open("contact.html", "w").write(page("contact.html", "Contact", "Contact FIN2DAY: suggest a topic, report a correction, or ask about working together.", contact, "/contact.html"))

    # ---------------- Disclaimer & privacy ----------------
    legal = f"""
<div class="page-head"><div class="wrap">
  <div class="label">Legal</div>
  <h1>Disclaimer &amp; privacy</h1>
  <p>Plain-English version. Last updated 13 October 2026.</p>
</div></div>
<section class="block" style="padding-top:0"><div class="wrap"><div class="page-body prose"><div class="narrow">
  <h2 id="disclaimer">Not investment advice</h2>
  <p>FIN2DAY publishes educational content about finance and the economy. Nothing on this site, our Instagram page or our newsletter is investment, legal or tax advice, or a recommendation to buy or sell any security. We are not SEBI-registered investment advisers. Please do your own research and consult a registered professional before making financial decisions.</p>
  <p>We work hard to get every number right and we cite our sources, but information can change after publication. If you spot an error, <a href="/contact.html">tell us</a> and we'll correct it.</p>
  <h2 id="privacy">Privacy</h2>
  <ul>
    <li><strong>What we collect:</strong> your email if you join the newsletter, and your name, email and message if you use the contact form.</li>
    <li><strong>Why:</strong> to send the newsletter you asked for and to reply to you. Nothing else.</li>
    <li><strong>Where it's stored:</strong> with our hosting provider, Netlify, and our email newsletter service, Brevo, which sends the daily brief.</li>
    <li><strong>What we don't do:</strong> we don't sell or share your details, and we don't use tracking cookies or ads on this site.</li>
    <li><strong>Your choice:</strong> every newsletter has an unsubscribe link. To have your details deleted, use the <a href="/contact.html">contact form</a>.</li>
  </ul>
  <h2>Third-party links</h2>
  <p>We link to news sources and official websites. We're not responsible for their content or privacy practices.</p>
</div></div></div></section>
"""
    open("disclaimer.html", "w").write(page("disclaimer.html", "Disclaimer & privacy", "FIN2DAY is educational content, not investment advice. How we handle your email and contact details.", legal))

    # ---------------- 404 ----------------
    nf = """
<div class="page-head" style="padding-bottom:clamp(60px,8vw,120px)"><div class="wrap">
  <div class="label">Error 404</div>
  <h1>This page went the way of the 2025 rate cuts.</h1>
  <p>It doesn't exist anymore, or never did. Try one of these instead.</p>
  <div class="cta-row" style="margin-top:28px"><a class="btn" href="/">Go home</a><a class="btn ghost" href="/explainers/">Read the explainers</a></div>
</div></div>
"""
    open("404.html", "w").write(page("404.html", "Page not found", "This page doesn't exist.", nf))

    # Netlify config: headers + pretty 404 is automatic for 404.html
    open("_headers", "w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = ["/", "/explainers/", "/about.html", "/contact.html", "/disclaimer.html"] + extra_urls + [f"/explainers/{e['slug']}.html" for e in EXPLAINERS]
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                                   "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")


if __name__ == "__main__":
    build()
    print("built")
