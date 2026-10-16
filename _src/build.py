"""Generates the FIN2DAY static site. Run: python3 build.py"""
import os, html

SITE = "https://fin2day.netlify.app"
IG = "https://www.instagram.com/fin2day/"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap">')
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23202020'/%3E"
           "%3Ctext x='32' y='46' font-family='Arial,sans-serif' font-size='40' fill='%23C9A95C' text-anchor='middle'%3E2%3C/text%3E%3C/svg%3E")

NAV = [("/", "Home"), ("/explainers/", "Explainers"), ("/about.html", "About"), ("/#newsletter", "Newsletter"), ("/contact.html", "Contact")]


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
<meta name="theme-color" content="#F5F5F5">
<link rel="icon" href="{FAVICON}">
{FONTS}
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<script>document.documentElement.classList.add('js')</script>
<a class="skip" href="#main">Skip to content</a>
{pre}
<header class="mast">
  <div class="wrap">
    <a class="logo" href="/" aria-label="FIN2DAY home"><span class="wm">FIN<b>2</b>DAY</span><span class="by">Finance, Explained</span></a>
    <nav class="nav" id="nav" aria-label="Main">
      {nav}
      <a class="btn" href="{IG}" target="_blank" rel="noopener">Follow @fin2day</a>
    </nav>
    <a class="btn sm mast-cta" href="{IG}" target="_blank" rel="noopener">Follow @fin2day</a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="fbox">
    <div class="fgrid">
      <div class="fbig">FIN<b>2</b>DAY</div>
      <div></div>
      <div class="fcols">
        <div class="flinks"><span>Read</span><a href="/explainers/">All explainers</a><a href="/explainers/#rbi">RBI</a><a href="/explainers/#ipo">IPOs</a><a href="/explainers/#global">Global economy</a><a href="/explainers/#markets">Markets</a></div>
        <div class="flinks"><span>FIN2DAY</span><a href="/about.html">About</a><a href="/contact.html">Contact</a><a href="/#newsletter">Newsletter</a><a href="{IG}" target="_blank" rel="noopener">Instagram ↗</a></div>
        <div class="flinks"><span>Legal</span><a href="/disclaimer.html">Disclaimer</a><a href="/disclaimer.html#privacy">Privacy</a></div>
      </div>
    </div>
    <p class="disc">FIN2DAY publishes educational content only. Nothing here is investment, legal or tax advice. Do your own research or speak to a SEBI-registered adviser before making financial decisions. © 2026 FIN2DAY.</p>
    <svg class="fcurve" viewBox="0 0 300 420" aria-hidden="true"><path d="M300 0v420H150c0-40 18-70 54-90 34-19 46-52 46-100V0z" fill="currentColor"/></svg>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
<script src="/assets/lenis.min.js" defer></script>
<script src="/assets/motion.js" defer></script>
</body>
</html>
"""


def newsletter_form(fid="newsletter"):
    return f"""<form class="form" name="newsletter" method="POST" data-netlify="true" netlify-honeypot="bot-field" novalidate>
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
    chart = f'<div class="chart">{e["hero"]}</div>' if e.get("hero") else ""
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

def load_stories():
    out = []
    for jf in glob.glob(os.path.join(CONTENT, "*.json")):
        if jf.endswith("ticker.json"):
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
        m["mins"] = max(2, math.ceil(_words(m["body"]) / 220))
        d = datetime.date.fromisoformat(m["date"])
        m["date_label"] = f"{d.day} {d.strftime('%b %Y')}"
        m.setdefault("tag_class", "")
        out.append(m)
    out.sort(key=lambda m: (m["date"], m.get("order", 0)), reverse=True)
    return out

EXPLAINERS = load_stories()
SOURCES = {e["slug"]: e["sources"] for e in EXPLAINERS}
ARTICLE_BODIES = {e["slug"]: e["body"] for e in EXPLAINERS}
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
    return f"""<article class="story" data-topic="{e['topic']}">
  <div class="meta"><span class="tag {cls}">{t}</span><span>{e['date_label']}</span><span>{e['mins']} min</span></div>
  <h3><a href="{link_prefix}{e['slug']}.html">{e['short']}</a></h3>
  <p>{e['card']}</p>
  <a class="read" href="{link_prefix}{e['slug']}.html">Read the explainer →</a>
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
    def tval(name):
        for k, v, c in TICKER:
            if k.lower().startswith(name.lower()):
                parts = v.split(" ", 1)
                return k, parts[0], (parts[1] if len(parts) > 1 else ""), c
        return None
    floats = ""
    for cls, name in (("a", "Nifty"), ("b", "Sensex")):
        tv = tval(name)
        if tv:
            k, num, chg, c = tv
            floats += f'<div class="float {cls}" aria-hidden="true"><small>{html.escape(k)}</small><strong>{html.escape(num)}</strong><span class="{c}">{html.escape(chg)}</span></div>'
    ticker_items = ''.join(''.join(f'<div class="tk"><span>{html.escape(k)}</span><span class="mono{(" " + c) if c else ""}">{html.escape(v)}</span></div>' for k, v, c in tick) for _ in range(2))

    BEATS = [("concepts", "CONCEPTS", "Money basics", "Repo rate, inflation, bonds, P/E. The ideas behind the headlines."),
             ("ipo", "IPO", "IPO watch", "What the company does, how it's priced, and what to read before you bid."),
             ("rbi", "RBI · REPO", "RBI &amp; rates", "Every policy move, and what it does to your EMI and FD."),
             ("global", "USD · OIL · CNY", "Global economy", "The Fed, China, oil and the dollar, and how they ripple into India."),
             ("trade", "TARIFFS", "Trade wars", "Who taxes whose goods, why, and who pays in the end."),
             ("markets", "NIFTY · SENSEX", "Markets", "Why the market moved, and which sectors are booming or bust.")]
    SQ = ["var(--ink)", "var(--brass)", "var(--hot)"]
    beats = ""
    used = set()
    for i, (key, sym, name, desc) in enumerate(BEATS):
        pool = [e for e in EXPLAINERS if key in e["topic"].split()]
        latest = next((e for e in pool if e["slug"] not in used), pool[0] if pool else None)
        if latest:
            used.add(latest["slug"])
        vis = ""
        if latest:
            vis = f"""<div class="vis rv"><a class="mini" href="/explainers/{latest['slug']}.html">
        <div class="mt"><span class="tag {latest['tag_class']}">{latest['tag']}</span><span>{latest['date_label']}</span><span>{latest['mins']} min</span></div>
        <h4>{latest['short']}</h4>
        <div class="chart">{latest['hero']}</div></a></div>"""
        beats += f"""
    <div class="svc" style="--sq:{SQ[i % 3]}">
      <div class="txt rv"><h3>{name}</h3><span class="sub">{sym}</span><p>{desc}</p><a class="more" href="/explainers/#{key}">Browse</a></div>
      {vis}
    </div>"""

    def bento(e, big=False):
        chart = f'<div class="chart">{e["hero"]}</div>' if big and e["hero"] else ""
        return f"""<article class="bx{' big' if big else ''} rv">
      <div class="meta"><span class="tag {e['tag_class']}">{e['tag']}</span><span>{e['date_label']}</span><span>{e['mins']} min</span></div>
      <h3><a href="/explainers/{e['slug']}.html">{e['short']}</a></h3>
      {chart}<p>{e['card']}</p>
      <a class="read" href="/explainers/{e['slug']}.html">Read the explainer →</a>
    </article>"""
    bentos = "".join(bento(e, i == 0) for i, e in enumerate(EXPLAINERS[:3]))

    SRC_TILES = ["RBI", "SEBI", "NSE", "BSE", "PIB", "MoSPI", "Reuters", "NBER"]
    tiles = "".join(f'<div class="tile t{i+1}">{t}</div>' for i, t in enumerate(SRC_TILES))


    home_cta = cta_panel("home", "The daily brief", 'Get the story before your <em class="u">first meeting</em>.', "One email every weekday morning: today's story, one chart, and what it means for you. Free, and you can leave any time.", lead)
    home = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <div class="label reveal">Finance, Explained</div>
      <h1 class="reveal d1">Today's money news, explained in <em class="u">2&nbsp;minutes</em>.</h1>
      <p class="lede reveal d2">One story a day on markets, IPOs, the RBI and the global economy. Plain words, real charts, and what it means for your wallet.</p>
      <div class="cta-row reveal d3">
        <a class="btn" href="#newsletter">Get the daily brief →</a>
        <a class="btn ghost" href="/explainers/{lead['slug']}.html">Read today's story</a>
      </div>
    </div>
    <div class="collage reveal d2">
      <a class="main" href="/explainers/{lead['slug']}.html" aria-label="Today's story: {html.escape(lead['short'])}">
        <div class="top"><b>FIN<i>2</i>DAY</b><span class="pill">FACT-CHECKED</span></div>
        <div class="label" style="margin-top:14px">Today's story · {lead['tag']}</div>
        <h3>{lead['short']}</h3>
        <div class="chart">{lead['hero']}</div>
        <div class="foot"><span>{lead['date_label']}</span><span>{lead['mins']} min read</span><span>{lead.get('hero_src') or 'Sources listed'}</span></div>
      </a>
      {floats}
    </div>
  </div>
  <div class="wrap tband">
    <div class="k"><span id="today">{datetime.date.fromisoformat(lead['date']).strftime('%A %-d %B %Y')}</span> · Closing data as of <b>{asof}</b></div>
    <div class="ticker" aria-label="Latest closing figures"><div class="track">{ticker_items}</div></div>
  </div>
</section>

<section class="svc-wrap" id="topics">
  <div class="svc-head rv">
    <div class="label">What we explain</div>
    <div class="shead" style="margin:0"><h2>Six beats. One story a day.</h2>
    <p>A new beat every weekday, a markets update after every trading day, and world markets at the weekend. When big news breaks, it jumps the queue.</p></div>
  </div>
  {beats}
</section>

<section class="block" id="latest">
  <div class="wrap">
    <div class="shead rv">
      <div><div class="label">Latest explainers</div><h2>The stories moving your money.</h2></div>
      <a class="btn ghost" href="/explainers/">All explainers →</a>
    </div>
    <div class="bento">{bentos}</div>
    <div class="stats">
      <div class="stat rv"><div class="n">1</div><h4>Story a day</h4><p>The one that matters most, not a feed of twenty.</p></div>
      <div class="stat rv"><div class="n">2<small>min</small></div><h4>Reading time</h4><p>Finished before your chai goes cold.</p></div>
      <div class="stat rv"><div class="n">0</div><h4>Stock tips</h4><p>We explain. We never tell you what to buy.</p></div>
      <div class="stat rv"><div class="n">100<small>%</small></div><h4>Real data</h4><p>Every chart comes from a cited source.</p></div>
    </div>
  </div>
</section>

<section class="how wrap" id="how">
  <div class="tiles" aria-hidden="true">{tiles}</div>
  <div class="inner rv">
    <div class="label">How it works</div>
    <h2 style="margin-top:14px">From headline to "oh, I get it" in three steps.</h2>
    <ul class="checks" style="margin-top:34px">
      <li><div><b>01 · News breaks</b><span>We pick the one story each day that actually affects your money.</span></div></li>
      <li><div><b>02 · We break it down</b><span>Plain words, a real chart, and every number checked against its source.</span></div></li>
      <li><div><b>03 · You get it in 2 minutes</b><span>As an Instagram carousel, a reel, and a full explainer right here.</span></div></li>
    </ul>
    <a class="btn" href="/explainers/{lead['slug']}.html">Read today's story</a>
  </div>
</section>

<section class="block" id="faq" style="padding-top:0">
  <div class="wrap">
    <div class="center rv"><div class="label">Questions</div><h2>Good to know.</h2></div>
    <div class="faq rv">
      <details><summary>Is this investment advice?</summary><p>No. FIN2DAY explains what happened and why. We never recommend buying or selling anything. For decisions about your money, talk to a SEBI-registered adviser.</p></details>
      <details><summary>How often do you post?</summary><p>Every day. Monday is money basics, Tuesday IPOs, Wednesday the RBI and rates, Thursday the global economy and Friday trade wars. After every trading day there is a markets update, and on weekends we cover world markets like the NYSE and Shanghai. When big news breaks, we cover it the same day.</p></details>
      <details><summary>Is it free?</summary><p>Yes. The Instagram page, the site and the newsletter are all free.</p></details>
      <details><summary>Where do the numbers come from?</summary><p>From primary sources like the RBI, SEBI, government releases, and established news agencies. Every explainer lists its sources at the bottom.</p></details>
      <details><summary>Can I suggest a topic?</summary><p>Please do. Use the <a href="/contact.html">contact form</a> or DM us on <a href="{IG}" target="_blank" rel="noopener">Instagram</a>.</p></details>
    </div>
  </div>
</section>

<section class="block" id="newsletter" style="padding-top:0">
  <div class="wrap">{home_cta}</div>
</section>
"""
    open("index.html", "w").write(page("index.html", "FIN2DAY | Finance, Explained",
        "Today's money news, explained in 2 minutes. Markets, IPOs, the RBI and the global economy in plain words, with real charts.", home, "/"))

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
  <div class="filters" role="group" aria-label="Filter by topic">{chips}</div>
  <div class="stories">{cards}</div>
  <p class="empty" id="empty" hidden>No explainers on this topic yet. <a href="/#newsletter">Join the newsletter</a> to get the first one, or <a href="/explainers/">see all explainers</a>.</p>
</div></section>
"""
    open("explainers/index.html", "w").write(page("explainers/index.html", "Explainers",
        "All FIN2DAY explainers: RBI, IPOs, markets, global economy and trade wars, explained in plain words.", lst, "/explainers/"))

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
  <form class="form card-form rv" name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" novalidate>
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
    urls = ["/", "/explainers/", "/about.html", "/contact.html", "/disclaimer.html"] + [f"/explainers/{e['slug']}.html" for e in EXPLAINERS]
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                                   "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")


if __name__ == "__main__":
    build()
    print("built")
