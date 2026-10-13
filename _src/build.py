"""Generates the FIN2DAY static site. Run: python3 build.py"""
import os, html

SITE = "https://fin2day.netlify.app"
IG = "https://www.instagram.com/fin2day/"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap">')
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23141414'/%3E"
           "%3Ctext x='32' y='47' font-family='Georgia,serif' font-size='44' fill='%237C9DFF' text-anchor='middle'%3E2%3C/text%3E%3C/svg%3E")

NAV = [("/", "Home"), ("/explainers/", "Explainers"), ("/about.html", "About"), ("/#newsletter", "Newsletter"), ("/contact.html", "Contact")]


def page(path, title, desc, body, active=None, og_type="website"):
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
<meta name="theme-color" content="#F6F2EA">
<link rel="icon" href="{FAVICON}">
{FONTS}
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="mast">
  <div class="wrap">
    <a class="logo" href="/" aria-label="FIN2DAY home">FIN<b>2</b>DAY</a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">
      {nav}
      <a class="btn sm" href="{IG}" target="_blank" rel="noopener">Follow @fin2day</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="wrap">
    <div class="fgrid">
      <div class="fbig">FIN<b>2</b>DAY</div>
      <div class="fcols">
        <div class="flinks"><span>Read</span><a href="/explainers/">All explainers</a><a href="/explainers/#rbi">RBI</a><a href="/explainers/#ipo">IPOs</a><a href="/explainers/#global">Global economy</a></div>
        <div class="flinks"><span>FIN2DAY</span><a href="/about.html">About</a><a href="/contact.html">Contact</a><a href="/#newsletter">Newsletter</a><a href="{IG}" target="_blank" rel="noopener">Instagram ↗</a></div>
        <div class="flinks"><span>Legal</span><a href="/disclaimer.html">Disclaimer</a><a href="/disclaimer.html#privacy">Privacy</a></div>
      </div>
    </div>
    <p class="disc">FIN2DAY publishes educational content only. Nothing here is investment, legal or tax advice. Do your own research or speak to a SEBI-registered adviser before making financial decisions. © 2026 FIN2DAY.</p>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def newsletter_form(fid="newsletter"):
    return f"""<form class="form" name="newsletter" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-success="You're on the list! The first brief lands soon." novalidate>
      <input type="hidden" name="form-name" value="newsletter">
      <p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <label for="{fid}-email">Your email</label>
      <div class="field">
        <input id="{fid}-email" name="email" type="email" placeholder="you@example.com" autocomplete="email" required>
        <button class="btn" type="submit">Join the list</button>
      </div>
      <div class="msg" role="status" aria-live="polite"></div>
      <p class="fine">One email on weekday mornings. No spam, and you can unsubscribe any time. See our <a href="/disclaimer.html#privacy">privacy note</a>.</p>
    </form>"""


# ----------------------------------------------------------------------------
# Explainers
# ----------------------------------------------------------------------------
EXPLAINERS = [
    dict(
        slug="september-2026-inflation-onions", topic="rbi concepts", tag=("Inflation", "red"), date="14 Oct 2026", mins=4,
        title="Onions are up 108%. Why India's inflation just jumped to 5.54%",
        short="Onions are up 108%. Why inflation just jumped to 5.54%",
        dek="Five charts that take September's 5.54% apart: where it really comes from, how one vegetable punched far above its weight, and why villages feel it more than cities.",
        card="Retail inflation jumped from 4.83% to 5.54% in September. Food inflation hit 7.74%, led by onions.",
        hero_src="Data: CPI, Sep 2026",
    ),
    dict(
        slug="us-russia-diesel-deal", topic="global trade", tag=("Global", ""), date="13 Oct 2026", mins=3,
        title="America punished India for buying Russian oil. Then it bought Russian diesel.",
        short="America punished India for Russian oil. Then it bought Russian diesel.",
        dek="Trump's diesel deal with Putin, the sanctions it paused, and why India is watching closely.",
        card="The US doubled tariffs on India over Russian oil. On 9 October, Trump agreed to buy Russian diesel.",
    ),
    dict(
        slug="rbi-rate-hike-oct-2026", topic="rbi concepts", tag=("RBI", "red"), date="12 Oct 2026", mins=2,
        title="Why the RBI raised rates after a year of cutting",
        short="Why the RBI raised rates after a year of cutting",
        dek="The repo rate went from 5.25% to 5.50%, the first hike since 2023. Here's what changed and what it means for your EMI.",
        card="The repo rate went from 5.25% to 5.50%, the first hike since 2023. Ten months ago the RBI was still cutting.",
    ),
    dict(
        slug="how-an-ipo-works", topic="ipo concepts", tag=("IPO", ""), date="Oct 2026", mins=2,
        title="Big IPO coming? How an IPO actually works",
        short="Big IPO coming? How an IPO actually works",
        dek="With mega listings like Reliance's Jio Platforms in the news, here's what happens when a company goes public, and what to check before you apply.",
        card="What happens when a company goes public, and the three things to read before you bid.",
    ),
]

RBI_CHART = """<svg viewBox="0 0 460 198" role="img" aria-label="Repo rate: 6.50% through 2024, cut to 6.25% Feb 2025, 6.00% Apr 2025, 5.50% Jun 2025, 5.25% Dec 2025, then hiked to 5.50% in Oct 2026">
  <g font-family="JetBrains Mono, monospace" font-size="10" fill="var(--mute)">
    <g stroke="var(--rule)" stroke-dasharray="2 3"><line x1="44" x2="450" y1="20" y2="20"/><line x1="44" x2="450" y1="80" y2="80"/><line x1="44" x2="450" y1="140" y2="140"/></g>
    <text x="4" y="24">6.50%</text><text x="4" y="84">6.00%</text><text x="4" y="144">5.50%</text>
    <text x="44" y="192">2024</text><text x="180" y="192">2025</text><text x="316" y="192">2026</text>
  </g>
  <path d="M44 20 H191 V50 H213 V80 H236 V140 H304 V170 H417 V140 H450" fill="none" stroke="var(--ink)" stroke-width="2.4"/>
  <path d="M417 170 V140 H450" fill="none" stroke="var(--red)" stroke-width="3.2"/>
  <circle cx="417" cy="140" r="5" fill="var(--red)"/>
  <text x="448" y="128" text-anchor="end" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="var(--red)">Oct 2026: 5.50%</text>
  <text x="310" y="163" font-family="Inter, sans-serif" font-size="10" fill="var(--mute)">5.25%</text>
</svg>"""

TARIFF_CHART = """<svg viewBox="0 0 460 230" role="img" aria-label="US tariffs on Indian goods: 25% from 7 Aug 2025, 50% from 27 Aug 2025, 18% after the Feb 2026 deal, and up to 100% threatened under the Sep 2026 law">
  <g font-family="Inter, sans-serif">
    <line x1="20" x2="450" y1="180" y2="180" stroke="var(--ink)" stroke-width="1.5"/>
    <rect x="30" y="140" width="80" height="40" fill="var(--mute)"/>
    <rect x="135" y="100" width="80" height="80" fill="var(--red)"/>
    <rect x="240" y="151" width="80" height="29" fill="var(--blue)"/>
    <rect x="345" y="20" width="80" height="160" fill="none" stroke="var(--red)" stroke-width="2" stroke-dasharray="6 4"/>
    <g font-weight="700" font-size="16" text-anchor="middle" fill="var(--ink)">
      <text x="70" y="132">25%</text><text x="175" y="92" fill="var(--red)">50%</text><text x="280" y="143" fill="var(--blue)">18%</text><text x="385" y="104" fill="var(--red)">up to 100%</text>
    </g>
    <g font-family="JetBrains Mono, monospace" font-size="10" text-anchor="middle" fill="var(--mute)">
      <text x="70" y="198">AUG 7 2025</text><text x="175" y="198">AUG 27 2025</text><text x="280" y="198">FEB 2026</text><text x="385" y="198">SEP 2026 LAW</text>
    </g>
    <g font-size="10" text-anchor="middle" fill="var(--mute)">
      <text x="70" y="214">reciprocal</text><text x="175" y="214">+25% oil penalty</text><text x="280" y="214">trade deal</text><text x="385" y="214">top 5 buyers</text>
    </g>
  </g>
</svg>"""

DIESEL_CHART = """<svg viewBox="0 0 460 170" role="img" aria-label="Russian diesel promised to the US: 300,000 tons immediately, 500,000 tons in November, 1,000,000 tons soon after">
  <g font-family="Inter, sans-serif" font-size="13">
    <text x="0" y="34" fill="var(--ink)" font-weight="600">Immediately</text>
    <rect x="120" y="20" width="96" height="20" fill="var(--ink)"/><text x="224" y="35" fill="var(--ink)" font-family="JetBrains Mono, monospace" font-size="12">300,000 t</text>
    <text x="0" y="84" fill="var(--ink)" font-weight="600">November</text>
    <rect x="120" y="70" width="160" height="20" fill="var(--ink)"/><text x="288" y="85" fill="var(--ink)" font-family="JetBrains Mono, monospace" font-size="12">500,000 t</text>
    <text x="0" y="134" fill="var(--ink)" font-weight="600">Soon after</text>
    <rect x="120" y="120" width="320" height="20" fill="var(--amber)"/><text x="436" y="160" text-anchor="end" fill="var(--ink)" font-family="JetBrains Mono, monospace" font-size="12">1,000,000 t</text>
  </g>
</svg>"""

IPO_CHART = """<svg viewBox="0 0 460 150" role="img" aria-label="Illustration: in an IPO part of the ownership moves from existing owners to new public shareholders">
  <g font-family="Inter, sans-serif" font-size="12" fill="var(--ink)">
    <rect x="10" y="22" width="440" height="34" fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1.2"/>
    <rect x="10" y="22" width="300" height="34" fill="var(--ink)"/>
    <rect x="310" y="22" width="80" height="34" fill="var(--rule)"/>
    <rect x="390" y="22" width="60" height="34" fill="var(--blue)"/>
    <text x="18" y="44" fill="var(--paper)" font-weight="600">Promoters / parent company</text>
    <text x="316" y="44" font-size="11">Early investors</text>
    <text x="10" y="84" font-weight="700">Before listing</text>
    <text x="10" y="102" fill="var(--mute)" font-size="11">Shares are held privately.</text>
    <text x="450" y="84" text-anchor="end" font-weight="700" fill="var(--blue)">New public shareholders</text>
    <text x="450" y="102" text-anchor="end" fill="var(--mute)" font-size="11">Anyone with a demat account can bid.</text>
    <text x="10" y="138" fill="var(--mute)" font-size="10" font-family="JetBrains Mono, monospace">Shares shown for illustration, not an actual offer size</text>
  </g>
</svg>"""


CPI_BARS = """<svg viewBox="0 0 460 250" role="img" aria-label="August vs September 2026 inflation: food 5.97% to 7.74%, rural 5.24% to 6.08%, overall 4.83% to 5.54%, urban 4.31% to 4.88%">
  <g font-family="Inter, sans-serif" font-size="12">
    <rect x="0" y="0" width="12" height="12" fill="var(--rule)"/><text x="18" y="10" fill="var(--mute)">August</text>
    <rect x="80" y="0" width="12" height="12" fill="var(--ink)"/><text x="98" y="10" fill="var(--mute)">September</text>
""" + "".join(
    f'<text x="0" y="{44+i*54}" font-weight="700" fill="var(--ink)">{n}</text>'
    f'<rect x="70" y="{30+i*54}" width="{a/8*300:.0f}" height="14" fill="var(--rule)"/>'
    f'<text x="{76+a/8*300:.0f}" y="{41+i*54}" font-family="JetBrains Mono, monospace" font-size="11" fill="var(--mute)">{a:.2f}%</text>'
    f'<rect x="70" y="{47+i*54}" width="{b/8*300:.0f}" height="18" fill="{c}"/>'
    f'<text x="{76+b/8*300:.0f}" y="{61+i*54}" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" fill="{c}">{b:.2f}%</text>'
    for i,(n,a,b,c) in enumerate([("Food",5.97,7.74,"var(--red)"),("Rural",5.24,6.08,"var(--ink)"),("Overall",4.83,5.54,"var(--ink)"),("Urban",4.31,4.88,"var(--ink)")])
) + "</g></svg>"

CPI_ITEMS = """<svg viewBox="0 0 460 300" role="img" aria-label="Year-on-year price change, September 2026: onion +108.1%, silver jewellery +87.8%, ginger +62.9%, garlic +54.6%, lemon +36.4%, coconut -4.0%, tomato -8.6%, potato -11.5%">
  <line x1="150" x2="150" y1="0" y2="300" stroke="var(--ink)" stroke-width="1.5"/>
  <g font-family="Inter, sans-serif" font-size="12">
""" + "".join(
    f'<text x="{142 if v>=0 else 142-abs(v)*2.2:.0f}" y="{20+i*35+(10 if v<0 else 0)}" text-anchor="end" font-weight="600" fill="var(--ink)">{n}</text>'
    f'<rect x="{150 if v>=0 else 150-abs(v)*2.2:.0f}" y="{8+i*35+(10 if v<0 else 0)}" width="{max(abs(v)*2.2,2):.0f}" height="18" fill="{"var(--red)" if v>=0 else "var(--green)"}"/>'
    f'<text x="{156+abs(v)*2.2 if v>=0 else 156:.0f}" y="{21+i*35+(10 if v<0 else 0)}" font-family="JetBrains Mono, monospace" font-size="11" fill="{"var(--red)" if v>=0 else "var(--green)"}">{"+" if v>=0 else "−"}{abs(v):.1f}%</text>'
    for i,(n,v) in enumerate([("Onion",108.09),("Silver jewellery",87.80),("Ginger",62.85),("Garlic",54.62),("Lemon",36.41),("Coconut",-3.99),("Tomato",-8.62),("Potato",-11.50)])
) + "</g></svg>"


_M=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep"]
_V=[2.74,3.21,3.40,3.48,3.93,4.38,4.45,4.83,5.54]
def _y(v): return 200-(v-2)*36
TREND_CHART = ('<svg viewBox="0 0 460 236" role="img" aria-label="CPI inflation in 2026, new series: Jan 2.74%, Feb 3.21%, Mar 3.40%, Apr 3.48%, May 3.93%, Jun 4.38%, Jul 4.45%, Aug 4.83%, Sep 5.54%. RBI target 4%, upper limit 6%">'
  '<g font-family="Inter, sans-serif" font-size="11">'
  f'<rect x="44" y="20" width="406" height="{_y(6)-20:.0f}" fill="var(--red)" opacity="0.08"/>'
  f'<line x1="44" x2="450" y1="{_y(6):.0f}" y2="{_y(6):.0f}" stroke="var(--red)" stroke-dasharray="4 4"/>'
  f'<text x="50" y="{_y(6)-6:.0f}" fill="var(--red)" font-weight="700">6% upper limit</text>'
  f'<line x1="44" x2="450" y1="{_y(4):.0f}" y2="{_y(4):.0f}" stroke="var(--blue)" stroke-dasharray="4 4"/>'
  f'<text x="448" y="{_y(4)+16:.0f}" text-anchor="end" fill="var(--blue)" font-weight="700">4% target</text>'
  '<g font-family="JetBrains Mono, monospace" font-size="10" fill="var(--mute)">'
  + "".join(f'<text x="4" y="{_y(v)+4:.0f}">{v}%</text>' for v in (2,3,5,7))
  + "".join(f'<text x="{60+i*48}" y="226" text-anchor="middle">{m}</text>' for i,m in enumerate(_M))
  + '</g>'
  f'<polyline points="{" ".join(f"{60+i*48},{_y(v):.1f}" for i,v in enumerate(_V))}" fill="none" stroke="var(--ink)" stroke-width="2.4"/>'
  + "".join(f'<circle cx="{60+i*48}" cy="{_y(v):.1f}" r="{5 if i==8 else 3}" fill="{"var(--red)" if i==8 else "var(--ink)"}"/>' for i,v in enumerate(_V))
  + f'<text x="60" y="{_y(2.74)+18:.0f}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="var(--ink)">2.74%</text>'
  f'<text x="432" y="{_y(5.54)-5:.0f}" text-anchor="end" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" fill="var(--red)">5.54%</text>'
  '</g></svg>')

_C=[("Food & beverages",2.71,"var(--red)"),("Personal care & misc.",0.69,"var(--amber)"),("Housing & fuel",0.48,"var(--ink)"),("Transport",0.44,"var(--ink)"),("Restaurants & hotels",0.31,"var(--ink)"),("Clothing & footwear",0.25,"var(--ink)"),("Other six groups",0.62,"var(--mute)")]
CONTRIB_CHART = ('<svg viewBox="0 0 460 250" role="img" aria-label="Approximate contribution to 5.54% inflation in September 2026, percentage points: food and beverages 2.71, personal care and miscellaneous 0.69, housing and fuel 0.48, transport 0.44, restaurants and hotels 0.31, clothing and footwear 0.25, other six groups 0.62">'
  '<g font-family="Inter, sans-serif" font-size="12">'
  + "".join(f'<text x="150" y="{24+i*33}" text-anchor="end" font-weight="600" fill="var(--ink)">{n}</text>'
            f'<rect x="160" y="{11+i*33}" width="{v/2.71*230:.0f}" height="18" fill="{c}"/>'
            f'<text x="{166+v/2.71*230:.0f}" y="{25+i*33}" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="{c}">{v:.2f}</text>' for i,(n,v,c) in enumerate(_C))
  + '<text x="160" y="246" font-family="JetBrains Mono, monospace" font-size="10" fill="var(--mute)">percentage points of the 5.54% headline</text>'
  '</g></svg>')

PUNCH_CHART = ('<svg viewBox="0 0 460 196" role="img" aria-label="Onion is 0.70% of the CPI basket but about 13.7% of September inflation. Silver jewellery is 0.31% of the basket but about 5% of inflation">'
  '<g font-family="Inter, sans-serif" font-size="12">'
  '<rect x="0" y="0" width="12" height="12" fill="var(--rule)"/><text x="18" y="10" fill="var(--mute)">Share of the basket</text>'
  '<rect x="160" y="0" width="12" height="12" fill="var(--red)"/><text x="178" y="10" fill="var(--mute)">Share of September inflation (est.)</text>'
  + "".join(f'<text x="0" y="{58+i*76}" font-weight="700" fill="var(--ink)">{n}</text>'
            f'<rect x="120" y="{38+i*76}" width="{max(a/16*300,3):.0f}" height="16" fill="var(--rule)"/>'
            f'<text x="{126+max(a/16*300,3):.0f}" y="{51+i*76}" font-family="JetBrains Mono, monospace" font-size="11" fill="var(--mute)">{a:.2f}%</text>'
            f'<rect x="120" y="{57+i*76}" width="{b/16*300:.0f}" height="20" fill="var(--red)"/>'
            f'<text x="{126+b/16*300:.0f}" y="{72+i*76}" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" fill="var(--red)">~{b:.1f}%</text>' for i,(n,a,b) in enumerate([("Onion",0.70,13.7),("Silver jewellery",0.31,5.0)]))
  + '</g></svg>')

BASKET_CHART = ('<svg viewBox="0 0 460 236" role="img" aria-label="Share of the CPI basket, rural vs urban: food and beverages 42.0% vs 30.3%, housing and fuel 11.8% vs 25.0%, transport 8.6% vs 9.0%, education 2.4% vs 4.5%">'
  '<g font-family="Inter, sans-serif" font-size="12">'
  '<rect x="0" y="0" width="12" height="12" fill="var(--red)"/><text x="18" y="10" fill="var(--mute)">Rural</text>'
  '<rect x="70" y="0" width="12" height="12" fill="var(--blue)"/><text x="88" y="10" fill="var(--mute)">Urban</text>'
  + "".join(f'<text x="0" y="{44+i*50}" font-weight="700" fill="var(--ink)">{n}</text>'
            f'<rect x="120" y="{30+i*50}" width="{r/45*290:.0f}" height="15" fill="var(--red)"/>'
            f'<text x="{126+r/45*290:.0f}" y="{42+i*50}" font-family="JetBrains Mono, monospace" font-size="11" fill="var(--red)">{r:.1f}%</text>'
            f'<rect x="120" y="{47+i*50}" width="{u/45*290:.0f}" height="15" fill="var(--blue)"/>'
            f'<text x="{126+u/45*290:.0f}" y="{59+i*50}" font-family="JetBrains Mono, monospace" font-size="11" fill="var(--blue)">{u:.1f}%</text>' for i,(n,r,u) in enumerate([("Food",41.98,30.25),("Housing & fuel",11.76,25.00),("Transport",8.64,8.99),("Education",2.38,4.52)]))
  + '</g></svg>')

_S=[("Tamil Nadu",6.81),("Odisha",6.70),("Madhya Pradesh",6.68),("Telangana",6.64),("All India",5.54),("Maharashtra",5.18),("Gujarat",5.11),("Delhi",3.40)]
def _sx(v): return 140+(v-3)/4.5*300
STATES_CHART = ('<svg viewBox="0 0 460 262" role="img" aria-label="CPI inflation by state, September 2026: Tamil Nadu 6.81%, Odisha 6.70%, Madhya Pradesh 6.68%, Telangana 6.64%, All India 5.54%, Maharashtra 5.18%, Gujarat 5.11%, Delhi 3.40%">'
  '<g font-family="Inter, sans-serif" font-size="12">'
  f'<line x1="{_sx(6):.0f}" x2="{_sx(6):.0f}" y1="4" y2="240" stroke="var(--red)" stroke-dasharray="4 4"/>'
  f'<text x="{_sx(6)+4:.0f}" y="256" fill="var(--red)" font-size="10" font-family="JetBrains Mono, monospace">6% limit</text>'
  + "".join(f'<text x="130" y="{22+i*29}" text-anchor="end" font-weight="{700 if n=="All India" else 500}" fill="var(--ink)">{n}</text>'
            f'<line x1="140" x2="{_sx(v):.0f}" y1="{18+i*29}" y2="{18+i*29}" stroke="var(--rule)" stroke-width="2"/>'
            f'<circle cx="{_sx(v):.0f}" cy="{18+i*29}" r="6" fill="{"var(--red)" if v>6 else ("var(--blue)" if n=="All India" else "var(--ink)")}"/>'
            f'<text x="{_sx(v)+12:.0f}" y="{22+i*29}" font-family="JetBrains Mono, monospace" font-size="11" fill="var(--ink)">{v:.2f}%</text>' for i,(n,v) in enumerate(_S))
  + '</g></svg>')

HERO_CHART = {"september-2026-inflation-onions": TREND_CHART}


def share_bar():
    return """<div class="share" aria-label="Share this explainer">
  <button class="btn sm" data-share="whatsapp">Share on WhatsApp</button>
  <button class="btn sm ghost" data-share="x">Share on X</button>
  <button class="btn sm ghost" data-share="copy">Copy link</button>
  <button class="btn sm ghost" data-share="native">More…</button>
  <span class="msg" role="status" aria-live="polite"></span>
</div>"""


ARTICLE_BODIES = {
"september-2026-inflation-onions": f"""
<p>The headline says inflation is 5.54%. Underneath that number, one vegetable that makes up less than 1% of what Indians buy did about a seventh of the work. Here's what the September data shows when you take it apart.</p>
<h2>Nine months of climbing</h2>
<p>This didn't happen overnight. Under the new CPI series, inflation has risen every single month of 2026, from 2.74% in January to 5.54% in September. September was the fourth month in a row above the RBI's 4% target, and it came in above the 5.4% that economists polled by Reuters had expected.</p>
<div class="chart">{TREND_CHART}<div class="cap">CPI inflation, year on year, 2026 (base 2024=100). September is provisional.</div></div>
<h2>Where the 5.54% actually comes from</h2>
<p>Each spending group's contribution to inflation is roughly its weight in the basket multiplied by its own inflation rate. Run that maths on September's official numbers and the pieces add up to about 5.51%, very close to the published 5.54%.</p>
<div class="chart">{CONTRIB_CHART}<div class="cap">Approximate contribution by spending group, September 2026. FIN2DAY calculation from official MoSPI weights and group inflation rates.</div></div>
<p>Food and beverages make up 36.75% of the basket but delivered about 2.7 points, nearly half of all inflation. The surprise is in second place: personal care and miscellaneous goods, up 13.75%, mostly because of jewellery. "Other personal effects" rose 38.69%. Eating out is getting pricier too, with restaurant and hotel inflation at 9.36%.</p>
<p>Meanwhile housing and fuel, the second-biggest group at 17.67% of the basket, rose just 2.74%. That's what is holding the headline number down.</p>
<h2>Small weight, big punch</h2>
<p>In the new series, onion has a weight of just 0.70%. But when the price of something doubles, even a small weight matters. At 108% inflation, onions alone contributed roughly 0.75 of a percentage point, about 14% of all inflation in September.</p>
<div class="chart">{PUNCH_CHART}<div class="cap">FIN2DAY estimate using official item weights (onion 0.7006, silver jewellery 0.3127). Approximate.</div></div>
<p>The jump from August is even more striking. Onion inflation went from 48.78% to 108.09%, which on its own adds about 0.4 points. Headline inflation rose 0.71 points in the month, so onions explain more than half of the increase.</p>
<p>Silver jewellery, at just 0.31% of the basket, rose 87.8% and added roughly another quarter of a point.</p>
<h2>Why villages are hit harder</h2>
<p>Rural and urban households don't buy the same things, and the CPI weights show it.</p>
<div class="chart">{BASKET_CHART}<div class="cap">Share of the CPI basket by group, rural vs urban. Source: MoSPI, CPI base 2024.</div></div>
<p>Food is 42% of the rural basket but only 30% of the urban one. Housing, where prices barely moved, is a quarter of the urban basket. So when food spikes and rents don't, villages take the hit while cities get a cushion. Rural food inflation hit 8.06% in September, against 7.18% in cities.</p>
<p>That's also why Delhi, at 3.40%, looks so different from Tamil Nadu at 6.81%. Four large states are already above the RBI's 6% limit.</p>
<div class="chart">{STATES_CHART}<div class="cap">CPI inflation by state, September 2026 (provisional).</div></div>
<h2>What's behind it, beyond onions</h2>
<ul class="points">
  <li><b>Weather</b><span>Analysts point to below-normal rainfall this monsoon and an El Niño that Emkay Global's Madhavi Arora says may persist into 2027.</span></li>
  <li><b>Oil</b><span>Higher crude prices tied to the Iran war. DBS Bank's Radhika Rao expects fuel costs to push up non-food prices with a lag.</span></li>
  <li><b>Base effect</b><span>Inflation a year ago was unusually low. In September 2025 it was 1.54% on the old series, a 99-month low, so this year's comparison looks steeper.</span></li>
  <li><b>Core</b><span>ICRA estimates core inflation, which excludes food and fuel, at about 4.6%. Price pressure is spreading, but not yet runaway.</span></li>
</ul>
<h2>What forecasters now expect</h2>
<ul class="points">
  <li><b>HDFC Bank</b><span>Next print near 6%, full-year inflation 5.4%, a 25 bps hike in December. (Sakshi Gupta)</span></li>
  <li><b>Kotak</b><span>Inflation above 6% over the next few months, another 50 bps of hikes. (Upasna Bhardwaj)</span></li>
  <li><b>Emkay</b><span>October–December inflation averaging about 6.1%, hikes in December and February. (Madhavi Arora)</span></li>
  <li><b>IDFC First</b><span>Repo rate peaking at 6.0–6.25%, up from 5.50% today. (Gaura Sengupta)</span></li>
</ul>
<div class="callout"><b>What that could mean for your EMI</b><p>Take a ₹50 lakh, 20-year home loan at 8.5%. If two more 25 bps hikes are passed on in full, the rate becomes 9.0% and the EMI rises from about ₹43,391 to ₹44,986, roughly ₹1,600 more a month. That's an illustration; your bank's reset terms decide the actual change.</p></div>
<h2>Dates to watch</h2>
<ul class="points">
  <li><b>12 Nov</b><span>October inflation. If forecasters are right, it could touch 6%.</span></li>
  <li><b>2–4 Dec</b><span>RBI policy meeting. Most economists quoted above expect another hike.</span></li>
</ul>
<p><em>September figures are provisional. Contribution figures are FIN2DAY approximations from official weights, not official statistics.</em></p>
""",
"us-russia-diesel-deal": f"""
<p>For a year, Washington told New Delhi one thing: stop buying Russian oil. On 9 October 2026, President Trump announced the US would buy Russian <strong>diesel</strong> instead.</p>
<h2>How India got squeezed</h2>
<p>In August 2025 the US put a 25% reciprocal tariff on Indian goods, then added another 25% as a penalty for buying Russian crude. That took the total to 50%. In February 2026, India agreed to stop buying Russian crude, and the US said it would cut the tariff to 18%.</p>
<div class="chart">{TARIFF_CHART}<div class="cap">US tariffs on Indian goods. The Sep 2026 law allows tariffs of up to 100% on the five biggest buyers of Russian oil and gas; final rates are still to be set.</div></div>
<p>Then on 18 September 2026, Trump signed a new sanctions law. It directs tariffs of up to 100% on the top five importers of Russian oil or gas, which puts India back in the line of fire.</p>
<h2>The phone call</h2>
<p>Three weeks later, after a call with Vladimir Putin, Trump said Russia would supply:</p>
<div class="chart">{DIESEL_CHART}<div class="cap">Diesel volumes as stated by President Trump on 9 Oct 2026. He said 3 million more tons would follow "within a short period of time".</div></div>
<p>The US Treasury issued a licence so that sanctions won't apply until <strong>April 2027</strong> to Russian diesel loaded onto tankers as of that day. It's the first diesel licence longer than the usual 30 days since the Ukraine war began in 2022.</p>
<h2>Why Trump did it</h2>
<ul class="points">
  <li><b>$6.52</b><span>Record US national average for diesel per AAA, on 22 September 2026. It was $6.28 on 9 October.</span></li>
  <li><b>Midterms</b><span>Trump said lower fuel prices for truckers, farmers and ranchers were his top priority, with midterm elections weeks away.</span></li>
  <li><b>Russia</b><span>Moscow had restricted diesel exports in July after Ukrainian attacks on its refineries. It said it would lift those limits early.</span></li>
</ul>
<h2>The reaction</h2>
<p>Ukraine's President Zelenskyy called it "a weak decision by strong partners." US Democrats including Chuck Schumer and Elizabeth Warren called it a betrayal of Ukraine. Analysts disagreed on whether it would bring prices down much at all.</p>
<div class="callout"><b>What it means for India</b><p>The same law that threatens India with up to 100% tariffs is still on the books. Watch for which five countries the US Trade Representative names, and whether India's February deal protects it.</p></div>
""",
"rbi-rate-hike-oct-2026": f"""
<p>On 7 October 2026, the RBI raised the repo rate from 5.25% to 5.50%. All six members of the Monetary Policy Committee voted yes. It was the first hike since 2023, and it came just ten months after the RBI's last cut.</p>
<div class="chart">{RBI_CHART}<div class="cap">RBI policy repo rate, Jan 2024 to Oct 2026.</div></div>
<h2>What changed</h2>
<p>Through 2025 the RBI cut rates four times, from 6.50% to 5.25%, to support growth. Then three things turned at once:</p>
<ul class="points">
  <li><b>Oil</b><span>Crude crossed $100 a barrel again. India imports most of its oil, so this feeds straight into prices.</span></li>
  <li><b>Rupee</b><span>The rupee slid close to its record low against the dollar, which makes imports costlier still.</span></li>
  <li><b>Inflation</b><span>The RBI expects inflation to touch about 6% in October to December, the top of its 2–6% comfort band.</span></li>
</ul>
<h2>What the RBI signalled</h2>
<p>The Governor's message was that the next move is another hike or a pause. Rate cuts are off the table for now.</p>
<div class="callout"><b>What it means for you</b><p>EMIs on floating-rate home and car loans linked to the repo rate can rise slightly at the next reset. New fixed deposits should start paying a little more.</p></div>
<h2>Repo rate, explained</h2>
<p>The repo rate is the interest rate at which the RBI lends money to banks overnight. When it goes up, borrowing gets costlier for banks, and they pass that on to loans. It's the RBI's main tool to cool inflation.</p>
""",
"how-an-ipo-works": f"""
<p>An IPO, or initial public offering, is the first time a company sells its shares to the public. Part of the ownership moves from the founders and early investors to anyone who bids through a broker.</p>
<div class="chart">{IPO_CHART}<div class="cap">How ownership changes when a company lists.</div></div>
<h2>Why companies do it</h2>
<ul class="points">
  <li><b>Fresh issue</b><span>New shares are created and the money goes to the company, often for expansion or paying down debt.</span></li>
  <li><b>Offer for sale</b><span>Existing owners sell some of their shares. That money goes to them, not the company.</span></li>
  <li><b>A price tag</b><span>Listing gives the business a public market value that changes every trading day.</span></li>
</ul>
<h2>Three things to read before you bid</h2>
<p><strong>1. The price band and valuation.</strong> Compare the valuation it implies with listed rivals.<br>
<strong>2. Fresh issue vs offer for sale.</strong> A big offer for sale means owners are cashing out.<br>
<strong>3. The risk factors.</strong> Every IPO files a draft red herring prospectus (DRHP) with SEBI. Read the debt, litigation and risk sections.</p>
<div class="callout"><b>How to apply</b><p>You bid through your broker app using UPI. Big IPOs are often oversubscribed, so shares are allotted by lottery for retail investors and allotment isn't guaranteed.</p></div>
""",
}

SOURCES = {
"september-2026-inflation-onions": [
    ("MoSPI / PIB: CPI (base 2024=100) group and item weights", "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc2026212787501.pdf"),
    ("MoSPI / PIB: CPI press release, June 2026 (monthly series)", "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2284125&reg=48&lang=1"),
    ("Reuters via Investing.com: India inflation jumps to 5.54% in September", "https://www.investing.com/news/economy-news/india-inflation-jumps-to-554-in-september-strengthening-case-for-further-rate-hikes-4943948"),
    ("Finnovate: India CPI inflation September 2026 (group, item and state data)", "https://www.finnovate.in/learn/blog/india-cpi-inflation-september-2026"),
    ("Trading Economics: India inflation rate", "https://tradingeconomics.com/india/inflation-cpi"),
    ("Business Today: CPI base revision, what's changed", "https://www.businesstoday.in/amp/latest/economy/story/cpi-inflation-base-revision-whats-changed-why-it-matters-515940-2026-02-12"),
    ("Business Standard: Retail inflation at 1.54% in September 2025", "https://www.business-standard.com/amp/economy/news/india-s-retail-inflation-slips-to-99-month-low-of-1-54-in-september-125101301472_1.html"),
],
"us-russia-diesel-deal": [
    ("AP: Trump says US to get diesel from Russia (9 Oct 2026)", "https://www.kttc.com/2026/10/09/trump-says-us-get-diesel-russia-relaxing-pressure-moscow-ease-prices-before-midterms/"),
    ("Business Today: India faces fresh US tariff threat over Russian oil", "https://www.businesstoday.in/latest/economy/story/india-faces-fresh-us-tariff-threat-over-russian-oil-what-happens-next-gtri-explains-556634-2026-09-19"),
    ("Breakwave Advisors: India drops Russian crude, secures US tariff relief", "https://www.breakwaveadvisors.com/insights/2026/2/4/energy-realignment-india-drops-russian-crude-secures-us-tariff-relief"),
    ("Fox Business: US diesel hits record high", "https://www.foxbusiness.com/economy/national-average-price-diesel-hits-new-record-high-amid-iran-conflict"),
],
"rbi-rate-hike-oct-2026": [
    ("Reserve Bank of India: Monetary Policy Statements", "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx"),
],
"how-an-ipo-works": [
    ("SEBI: Investor education on IPOs", "https://investor.sebi.gov.in/"),
],
}


def story_card(e, link_prefix="/explainers/"):
    t, cls = e["tag"]
    return f"""<article class="story" data-topic="{e['topic']}">
  <div class="meta"><span class="tag {cls}">{t}</span><span>{e['date']}</span><span>{e['mins']} min</span></div>
  <h3><a href="{link_prefix}{e['slug']}.html">{e['short']}</a></h3>
  <p>{e['card']}</p>
  <a class="read" href="{link_prefix}{e['slug']}.html">Read the explainer →</a>
</article>"""


def build():
    os.makedirs("explainers", exist_ok=True)
    cards = "\n".join(story_card(e) for e in EXPLAINERS)
    home_cards = "\n".join(story_card(e) for e in EXPLAINERS[:3])

    # ---------------- Home ----------------
    home = f"""
<div class="dateline"><div class="wrap"><span id="today">Tuesday, 13 October 2026</span><span>Finance, Explained</span></div></div>
<div class="ticker" aria-label="Topics we cover"><div class="track">
  {''.join(['<div class="tk"><span>CPI inflation</span><span class="mono dn">5.54% ▲ Sep</span></div><div class="tk"><span>Onion prices</span><span class="mono dn">+108% y/y</span></div><div class="tk"><span>RBI repo</span><span class="mono dn">5.50% ▲ 25 bps</span></div><div class="tk"><span>US diesel</span><span class="mono dn">record $6.52/gal</span></div><div class="tk"><span>Russian diesel</span><span class="mono">1M tons to US</span></div><div class="tk"><span>Brent crude</span><span class="mono dn">above $100</span></div><div class="tk"><span>Rupee</span><span class="mono dn">near record low</span></div><div class="tk"><span>Your EMI</span><span class="mono dn">floating rates up</span></div><div class="tk"><span>Fixed deposits</span><span class="mono up">new rates better</span></div>']*2)}
</div></div>

<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <div class="label reveal">Finance, Explained</div>
      <h1 class="reveal d1">Today's money news, explained in <em>2&nbsp;minutes.</em></h1>
      <p class="lede reveal d2">One story a day on markets, IPOs, the RBI and the global economy. Plain words, real charts, and what it means for your wallet.</p>
      <div class="cta-row reveal d3">
        <a class="btn" href="#newsletter">Get the daily brief →</a>
        <a class="btn ghost" href="/explainers/{EXPLAINERS[0]['slug']}.html">Read today's story</a>
      </div>
    </div>
    <a class="postcard reveal d2" href="/explainers/{EXPLAINERS[0]['slug']}.html" style="text-decoration:none" aria-label="Today's story: {html.escape(EXPLAINERS[0]['short'])}">
      <div class="bar"><b>FIN<i>2</i>DAY</b><span class="stamp">FACT-CHECKED</span></div>
      <div class="label" style="margin-top:16px">Today's story · {EXPLAINERS[0]['tag'][0]}</div>
      <h3>{EXPLAINERS[0]['short']}</h3>
      <div class="chart" style="margin:14px 0 0;padding:12px 10px 6px">{HERO_CHART.get(EXPLAINERS[0]['slug'], DIESEL_CHART)}</div>
      <div class="meta"><span>{EXPLAINERS[0]['date']}</span><span>{EXPLAINERS[0]['mins']} min read</span><span>{EXPLAINERS[0].get('hero_src','Sources: AP, AAA')}</span></div>
    </a>
  </div>
</section>

<div class="wrap">
  <div class="stats">
    <div class="stat"><div class="n">1</div><h4>Story a day</h4><p>The one that matters most, not a feed of twenty.</p></div>
    <div class="stat"><div class="n">2<small> min</small></div><h4>Reading time</h4><p>Finished before your chai goes cold.</p></div>
    <div class="stat"><div class="n">0</div><h4>Stock tips</h4><p>We explain. We never tell you what to buy.</p></div>
    <div class="stat"><div class="n">100<small>%</small></div><h4>Real data</h4><p>Every chart comes from a cited source.</p></div>
  </div>
</div>

<section class="block" id="latest">
  <div class="wrap">
    <div class="shead">
      <div><div class="label">Latest explainers</div><h2>The stories moving your money.</h2></div>
      <a class="btn ghost" href="/explainers/">All explainers →</a>
    </div>
    <div class="stories">{home_cards}</div>
  </div>
</section>

<section class="block" id="topics" style="padding-top:0">
  <div class="wrap">
    <div class="shead">
      <div><div class="label">What we explain</div><h2>Six beats. One story a day.</h2></div>
      <p>We pick the story that matters most each morning, and swap the plan when big news breaks.</p>
    </div>
    <div class="topics">
      <a class="topic" href="/explainers/#concepts"><div class="sym">CONCEPTS</div><h3>Money basics</h3><p>Repo rate, inflation, bonds, P/E. The ideas behind the headlines.</p><span class="go">Browse →</span></a>
      <a class="topic" href="/explainers/#ipo"><div class="sym">IPO</div><h3>IPO watch</h3><p>What the company does, how it's priced, and what to read before you bid.</p><span class="go">Browse →</span></a>
      <a class="topic" href="/explainers/#rbi"><div class="sym">RBI · REPO</div><h3>RBI &amp; rates</h3><p>Every policy move, and what it does to your EMI and FD.</p><span class="go">Browse →</span></a>
      <a class="topic" href="/explainers/#global"><div class="sym">USD · OIL · CNY</div><h3>Global economy</h3><p>The Fed, China, oil and the dollar, and how they ripple into India.</p><span class="go">Browse →</span></a>
      <a class="topic" href="/explainers/#trade"><div class="sym">TARIFFS</div><h3>Trade wars</h3><p>Who taxes whose goods, why, and who pays in the end.</p><span class="go">Browse →</span></a>
      <a class="topic" href="/explainers/#markets"><div class="sym">NIFTY · SENSEX</div><h3>Markets</h3><p>Why the market moved, and which sectors are booming or bust.</p><span class="go">Browse →</span></a>
    </div>
  </div>
</section>

<section class="block band">
  <div class="wrap">
    <div class="label">How it works</div>
    <h2>From headline to "oh, I get it" in three steps.</h2>
    <div class="steps" style="margin-top:40px">
      <div class="step" style="border-color:var(--paper)"><div class="k" style="color:var(--blue)">01</div><h3>News breaks</h3><p style="color:inherit;opacity:.75">We pick the one story each day that actually affects your money.</p></div>
      <div class="step" style="border-color:var(--paper)"><div class="k" style="color:var(--blue)">02</div><h3>We break it down</h3><p style="color:inherit;opacity:.75">Plain words, a real chart, and every number checked against its source.</p></div>
      <div class="step" style="border-color:var(--paper)"><div class="k" style="color:var(--blue)">03</div><h3>You get it in 2 minutes</h3><p style="color:inherit;opacity:.75">As an Instagram carousel, a reel, and a full explainer right here.</p></div>
    </div>
  </div>
</section>

<section class="block" id="faq">
  <div class="wrap narrow">
    <div class="label">Questions</div>
    <h2 style="font-size:clamp(34px,5vw,56px);line-height:1.02;margin:10px 0 30px">Good to know.</h2>
    <div class="faq">
      <details><summary>Is this investment advice?</summary><p>No. FIN2DAY explains what happened and why. We never recommend buying or selling anything. For decisions about your money, talk to a SEBI-registered adviser.</p></details>
      <details><summary>How often do you post?</summary><p>One story every weekday on Instagram, with longer explainers here on the site. When big news breaks, we cover it the same day.</p></details>
      <details><summary>Is it free?</summary><p>Yes. The Instagram page, the site and the newsletter are all free.</p></details>
      <details><summary>Where do the numbers come from?</summary><p>From primary sources like the RBI, SEBI, government releases, and established news agencies. Every explainer lists its sources at the bottom.</p></details>
      <details><summary>Can I suggest a topic?</summary><p>Please do. Use the <a href="/contact.html">contact form</a> or DM us on <a href="{IG}" target="_blank" rel="noopener">Instagram</a>.</p></details>
    </div>
  </div>
</section>

<section class="block" id="newsletter" style="padding-top:0">
  <div class="wrap letter">
    <div>
      <div class="label">The daily brief</div>
      <h2>Get the story before your first meeting.</h2>
      <p>One email every weekday morning: today's story, one chart, and what it means for you. Free, and you can leave any time.</p>
    </div>
    {newsletter_form("home")}
  </div>
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
<section class="block" style="padding-top:36px"><div class="wrap">
  <div class="filters" role="group" aria-label="Filter by topic">{chips}</div>
  <div class="stories">{cards}</div>
  <p class="empty" id="empty" hidden>No explainers on this topic yet. <a href="/#newsletter">Join the newsletter</a> to get the first one, or <a href="/explainers/">see all explainers</a>.</p>
</div></section>
"""
    open("explainers/index.html", "w").write(page("explainers/index.html", "Explainers",
        "All FIN2DAY explainers: RBI, IPOs, markets, global economy and trade wars, explained in plain words.", lst, "/explainers/"))

    # ---------------- Articles ----------------
    for i, e in enumerate(EXPLAINERS):
        t, cls = e["tag"]
        nxt = EXPLAINERS[(i + 1) % len(EXPLAINERS)]
        srcs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(n)}</a></li>' for n, u in SOURCES[e["slug"]])
        body = f"""
<div class="wrap narrow">
  <p class="crumbs"><a href="/">Home</a> / <a href="/explainers/">Explainers</a> / {t}</p>
  <header class="article-head">
    <div class="byline"><span class="tag {cls}">{t}</span><span>{e['date']}</span><span>{e['mins']} min read</span></div>
    <h1>{e['title']}</h1>
    <p class="dek">{e['dek']}</p>
  </header>
  <div class="prose">{ARTICLE_BODIES[e['slug']]}</div>
  {share_bar()}
  <div class="sources"><b>Sources</b><ol>{srcs}</ol>
  <p>Educational content only. Not investment advice. Spotted an error? <a href="/contact.html">Tell us</a>.</p></div>
  <div class="next"><div class="label">Read next</div>
    <h2 style="font-size:clamp(26px,3vw,34px);margin-top:10px"><a href="/explainers/{nxt['slug']}.html" style="text-decoration:none">{nxt['short']} →</a></h2>
  </div>
</div>
<section class="block"><div class="wrap letter">
  <div><div class="label">The daily brief</div><h2>Liked this? Get one every morning.</h2><p>Today's story, one chart, and what it means for you.</p></div>
  {newsletter_form("art")}
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
<section class="block" style="padding-top:40px"><div class="wrap narrow prose">
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
</div></section>
"""
    open("about.html", "w").write(page("about.html", "About", "What FIN2DAY is: daily finance news explained in plain words, with real charts and no stock tips.", about, "/about.html"))

    # ---------------- Contact ----------------
    contact = f"""
<div class="page-head"><div class="wrap">
  <div class="label">Contact</div>
  <h1>Say hello.</h1>
  <p>Suggest a topic, point out a mistake, or ask about working together. We read everything.</p>
</div></div>
<section class="block" style="padding-top:40px"><div class="wrap letter" style="align-items:start">
  <div>
    <h2 style="font-size:clamp(28px,3.4vw,40px)">Other ways to reach us</h2>
    <p>The quickest way is a DM on <a href="{IG}" target="_blank" rel="noopener">Instagram @fin2day</a>.</p>
    <p>Found an error in an explainer? Tell us which one and what's wrong, and we'll fix it and note the correction.</p>
  </div>
  <form class="form" name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-success="Thanks! Your message is in. We'll get back to you soon." novalidate>
    <input type="hidden" name="form-name" value="contact">
    <p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
    <div class="row"><label for="c-name">Name (required)</label><input id="c-name" name="name" autocomplete="name" required></div>
    <div class="row"><label for="c-email">Email (required)</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
    <div class="row"><label for="c-type">What's it about?</label>
      <select id="c-type" name="type"><option>Topic suggestion</option><option>Correction</option><option>Collaboration</option><option>Something else</option></select></div>
    <div class="row"><label for="c-msg">Message (required)</label><textarea id="c-msg" name="message" required></textarea></div>
    <button class="btn" type="submit">Send message</button>
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
<section class="block" style="padding-top:40px"><div class="wrap narrow prose">
  <h2 id="disclaimer">Not investment advice</h2>
  <p>FIN2DAY publishes educational content about finance and the economy. Nothing on this site, our Instagram page or our newsletter is investment, legal or tax advice, or a recommendation to buy or sell any security. We are not SEBI-registered investment advisers. Please do your own research and consult a registered professional before making financial decisions.</p>
  <p>We work hard to get every number right and we cite our sources, but information can change after publication. If you spot an error, <a href="/contact.html">tell us</a> and we'll correct it.</p>
  <h2 id="privacy">Privacy</h2>
  <ul>
    <li><strong>What we collect:</strong> your email if you join the newsletter, and your name, email and message if you use the contact form.</li>
    <li><strong>Why:</strong> to send the newsletter you asked for and to reply to you. Nothing else.</li>
    <li><strong>Where it's stored:</strong> with our hosting provider, Netlify, and later with our email newsletter service.</li>
    <li><strong>What we don't do:</strong> we don't sell or share your details, and we don't use tracking cookies or ads on this site.</li>
    <li><strong>Your choice:</strong> every newsletter has an unsubscribe link. To have your details deleted, use the <a href="/contact.html">contact form</a>.</li>
  </ul>
  <h2>Third-party links</h2>
  <p>We link to news sources and official websites. We're not responsible for their content or privacy practices.</p>
</div></section>
"""
    open("disclaimer.html", "w").write(page("disclaimer.html", "Disclaimer & privacy", "FIN2DAY is educational content, not investment advice. How we handle your email and contact details.", legal))

    # ---------------- 404 ----------------
    nf = """
<div class="page-head" style="border-bottom:0"><div class="wrap">
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
