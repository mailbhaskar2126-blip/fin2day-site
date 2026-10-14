# REFERENCE ONLY: examples of how the 14 Oct 2026 stories were written with charts.py.
# Copy the pattern into a new script for a new story. Do not re-run this file.
raise SystemExit("reference only")
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from charts import *
OUT = __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "content")
D = "2026-10-14"

# ---------------------------------------------------------------- Global: Fed & rupee
chain = flow([("The Fed raises rates", "16 Sep 2026: 3.75%–4%, first hike since 2023"),
              ("US bond yields climb", "10-year Treasuries above 5.2%"),
              ("Foreign funds sell India", "Safe US returns beat risky emerging markets"),
              ("They convert rupees to dollars", "More dollar demand, weaker rupee"),
              ("Imports cost more", "Oil, electronics, overseas fees and travel")],
             "How a Fed rate hike travels to India in five steps")
fpi = vbars([("Jul", 20200, "var(--green)"), ("Aug", 29631, "var(--green)"), ("Sep", -35861, "var(--red)"), ("Oct*", -44166, "var(--red)")],
            "Net FPI flows into Indian equities, 2026, in ₹ crore: July +20,200, August +29,631, September −35,861, October to the 11th −44,166",
            fmt="{:+,}", h=250, note="₹ crore, NSDL. *October up to 11 Oct")
yr = hbars([("All of 2025", 1.66, "var(--ink)"), ("2026 so far", 3.04, "var(--red)")], "Net FPI selling of Indian equities: ₹1.66 lakh crore in 2025, ₹3.04 lakh crore in 2026 up to 11 October",
           fmt="₹{:.2f} lakh cr", maxv=4.2, unit_note="net outflow (selling), ₹ lakh crore")
save(dict(slug="fed-hike-rupee-fpi-2026", date=D, order=98, topic="global", tag="Global", tag_class="",
          title="The Fed just raised rates. Here's how that pulls money out of India",
          short="The Fed raised rates. Here's how that pulls money out of India",
          dek="Foreign investors have sold more than ₹3 lakh crore of Indian shares this year, and the rupee is near 97. The trail leads back to Washington.",
          card="FPIs have pulled ₹3.04 lakh crore from Indian shares in 2026, nearly double 2025. The Fed is a big reason why.",
          hero_src="Data: NSDL, Federal Reserve",
          sources=[["Federal Reserve: FOMC statement, 16 September 2026", "https://www.federalreserve.gov/monetarypolicy/files/monetary20260916a1.pdf"],
                   ["Advisor Perspectives: Fed's interest rate decision, 16 September 2026", "https://www.advisorperspectives.com/dshort/updates/2026/09/16/feds-interest-rate-decision-september-16-2026"],
                   ["Business Standard: FPIs pull out ₹44,166 cr in October, 2026 outflows cross ₹3 trn", "https://www.business-standard.com/finance/news/fpis-pull-out-44-166-cr-from-equities-in-oct-2026-outflows-cross-3-trn-126101100210_1.html"],
                   ["Trading Economics: Indian rupee", "https://tradingeconomics.com/india/currency/news/520625"],
                   ["Navia: Weekly market roundup, 5–9 October 2026", "https://navia.co.in/blog/navia-weekly-roundup-oct-5-9-2026/"]]),
f"""
<p>On 16 September 2026, the US Federal Reserve raised its key interest rate by 0.25 percentage points to a range of <strong>3.75% to 4%</strong>. It was the Fed's first hike since 2023, and all 12 voting members backed it. "Inflation remains elevated," the Fed said.</p>
<p>That decision was made 13,000 km from Dalal Street. Here's why Indian investors are feeling it.</p>
<h2>The chain reaction</h2>
{chart(chain, "How a US rate decision reaches Indian markets and your wallet.")}
<p>When the Fed raises rates, US government bonds pay more. Global fund managers can now earn more than 5% a year on 10-year US Treasuries, which they treat as the safest asset in the world. Indian shares, by comparison, carry currency risk, political risk and, this year, losses. Geojit's VK Vijayakumar put it simply: "as long as the US bond yields remain elevated, FPIs will continue to sell."</p>
<h2>The selling, in numbers</h2>
<p>Foreign portfolio investors, or FPIs, had actually been buying Indian shares over the summer. That reversed in September, the month of the Fed hike.</p>
{chart(fpi, "Monthly net FPI flows into Indian equities, 2026.")}
<p>By 11 October, net FPI selling for 2026 had crossed <strong>₹3.04 lakh crore</strong>, compared with ₹1.66 lakh crore in the whole of 2025.</p>
{chart(yr, "Net foreign selling of Indian shares, 2025 vs 2026 so far.")}
<p>Analysts also cite high oil prices and an AI-driven rally in North Asian markets, which is drawing foreign money elsewhere in Asia. Indian domestic investors, through SIPs and mutual funds, have been buying much of what foreigners sell, which is why the market has fallen but not collapsed. Even so, the Nifty was down 13.87% for the year as of early October.</p>
<h2>The rupee</h2>
<p>Every foreign investor who sells Indian shares and leaves has to convert rupees into dollars. Add a strong dollar and a large oil import bill, and the rupee weakens. It closed at <strong>₹96.73 to the dollar</strong> on 9 October, close to its record low of about ₹96.96 set in May. The RBI has been selling dollars from its reserves to slow the slide.</p>
<h2>What it means for you</h2>
<ul class="points">
  <li><b>Prices</b><span>A weaker rupee makes imports dearer: fuel, phones, laptops, foreign travel and overseas tuition.</span></li>
  <li><b>Interest rates</b><span>A weak rupee and imported inflation were part of why the RBI raised rates on 7 October. See <a href="/explainers/rbi-rate-hike-oct-2026.html">our explainer</a>.</span></li>
  <li><b>Investments</b><span>Funds that hold US stocks gain in rupee terms when the rupee falls. Indian exporters, like IT companies, also earn more rupees per dollar.</span></li>
</ul>
<h2>What to watch</h2>
<p>The Fed's own projections now point to a year-end rate of 4.1% to 4.4%, and markets are pricing one more quarter-point hike in December. If that happens, the pressure on Indian markets and the rupee is unlikely to ease quickly. If US inflation cools and the Fed pauses, flows could turn around just as fast as they did in July. Educational content only, not investment advice.</p>
""", OUT)

# ---------------------------------------------------------------- Global: oil
bill = vbars([("Apr–Aug 2025", 50.4, "var(--ink)"), ("Apr–Aug 2026", 74.8, "var(--red)")],
             "India's crude import bill, April to August: $50.4 billion in 2025 vs $74.8 billion in 2026", fmt="${:g}bn", w=300, maxv=85)
vol = vbars([("Apr–Aug 2025", 101.1, "var(--ink)"), ("Apr–Aug 2026", 100.7, "var(--ink)")],
            "India's crude import volume, April to August: 101.1 million tonnes in 2025 vs 100.7 million tonnes in 2026", fmt="{:g} MT", w=300, maxv=120)
basket = vbars([("Aug 2025", 69.11, "var(--ink)"), ("Jul 2026", 82.04, "var(--amber)"), ("Aug 2026", 90.19, "var(--red)")],
               "Indian crude basket price per barrel: $69.11 in August 2025, $82.04 in July 2026, $90.19 in August 2026", fmt="${:.2f}", maxv=110, note="US$ per barrel, Indian basket (PPAC)")
hormuz = hbars([("LPG", 90, "var(--red)"), ("LNG", 60, "var(--amber)"), ("Crude oil", 40, "var(--ink)")],
               "Share of India's imports that come from the Middle East through the Strait of Hormuz: LPG about 90%, LNG about 60%, crude about 40%", fmt="~{:g}%", maxv=100, unit_note="share of imports via the Middle East")
save(dict(slug="oil-100-india-import-bill", date=D, order=1, topic="global", tag="Global", tag_class="",
          title="Same oil, $24 billion more: what $100 crude does to India",
          short="Same oil, $24 billion more: what $100 crude does to India",
          dek="India imported slightly less crude this year and paid 48% more for it. How oil prices flow into the rupee, inflation and your gas cylinder.",
          card="India bought slightly less crude in April–August 2026 than a year ago, and paid $74.8 billion instead of $50.4 billion.",
          sources=[["ThePrint: India's oil import bill jumps 48% to nearly $75 bn in April–August (PPAC data)", "https://theprint.in/economy/indias-oil-import-bill-jumps-48-to-nearly-75-bn-in-april-august-up-from-50-bn-last-year-govt-data/3046384/"],
                   ["OilPrice.com: India's crude oil import bill soars 60% as Iran war drives prices higher", "https://oilprice.com/Latest-Energy-News/World-News/Indias-Crude-Oil-Import-Bill-Soars-60-as-Iran-War-Drives-Prices-Higher.amp.html"],
                   ["Straits.live: Hormuz brief, 9 October 2026", "https://straits.live/briefs/2026-10-09"],
                   ["PPAC: Petroleum Planning and Analysis Cell", "https://ppac.gov.in/"]]),
f"""
<p>India imports about <strong>88%</strong> of the crude oil it uses. So when oil gets expensive, the whole country gets a bill.</p>
<p>This year, that bill has been enormous.</p>
<h2>Same oil, much bigger bill</h2>
<div class="chart" style="display:grid;grid-template-columns:1fr 1fr;gap:10px">{bill}{vol}<div class="cap" style="grid-column:1/-1">Left: what India paid for crude imports. Right: how much it bought, in million tonnes. Source: PPAC via ThePrint.</div></div>
<p>Between April and August 2026, India imported 100.7 million tonnes of crude, a little <em>less</em> than the 101.1 million tonnes a year earlier. It paid <strong>$74.8 billion</strong> for it, up 48% from $50.4 billion. The extra $24 billion is almost entirely price.</p>
{chart(basket, "The average price India pays per barrel of crude has risen sharply.")}
<p>Benchmark Brent crude crossed $100 a barrel in September and was at about $104 on 9 October, according to market data cited by Straits.live.</p>
<h2>Why: the Strait of Hormuz</h2>
<p>A large share of the oil and gas India buys comes from the Gulf through the Strait of Hormuz, a narrow channel between Iran and Oman. Conflict there in 2026 has made shipping dangerous: on 4 October, IMF PortWatch counted just 4 ship crossings, against about 85 a day before the crisis.</p>
{chart(hormuz, "How much of India's energy imports come from the Middle East via Hormuz, as reported by OilPrice.com.")}
<p>That's why the impact goes beyond petrol. India gets about 90% of its imported LPG, the gas in kitchen cylinders, from the region.</p>
<h2>How oil reaches your wallet</h2>
<ul class="points">
  <li><b>Inflation</b><span>Fuel feeds into transport and the cost of almost everything that's moved by truck. The RBI now expects inflation to average almost 5.8% over the next three quarters.</span></li>
  <li><b>The rupee</b><span>Oil is paid for in dollars. A bigger oil bill means more dollar demand, which weakens the rupee and makes all other imports dearer too. See <a href="/explainers/fed-hike-rupee-fpi-2026.html">how the Fed and FPI selling add to that</a>.</span></li>
  <li><b>Interest rates</b><span>Oil above $100 was one of the triggers for the RBI's rate hike on 7 October 2026.</span></li>
  <li><b>Government finances</b><span>If pump prices are held steady, oil companies or the government absorb the cost instead, leaving less for other spending.</span></li>
</ul>
<h2>What's softening the blow</h2>
<p>Indians have been using less of some fuels: LPG consumption fell 16.8% in April–August, and total petroleum product use was down 3.9%, according to PPAC data. Domestic natural gas production rose 20%. But with domestic crude output still falling, import dependence isn't going away soon.</p>
<div class="callout"><b>What to watch</b><p>Ship crossings through Hormuz, and the monthly PPAC import data. The quickest relief for India's bill, the rupee and inflation would be oil falling back below $90. Educational content only.</p></div>
""", OUT)

# ---------------------------------------------------------------- Trade: US-China 2018-19
cover = vbars([("Jul 2018", 34, "var(--ink)"), ("Aug 2018", 50, "var(--ink)"), ("Sep 2018", 250, "var(--amber)"), ("Sep 2019", 375, "var(--red)")],
              "Chinese imports hit by US tariffs, cumulative: $34bn in July 2018, $50bn in August 2018, $250bn in September 2018, more than $375bn by September 2019",
              fmt="${:g}bn", maxv=420, note="US$ of annual Chinese imports covered; Sep 2019 = $250bn + over $125bn")
who = hbars([("US imports, targeted", -32, "var(--red)"), ("US exports, retaliated", -11, "var(--red)")],
            "Effect of the 2018 trade war, per Fajgelbaum and others: US imports of targeted goods fell 32%, US exports hit by retaliation fell 11%", fmt="{:+g}%", maxv=40, lw=170, unit_note="change in affected trade, 2018 (NBER study)")
save(dict(slug="us-china-trade-war-2018-19", date=D, order=0, topic="trade", tag="Trade", tag_class="",
          title="The US–China trade war of 2018–19: who paid, and who won",
          short="The US–China trade war of 2018–19: who paid, and who won",
          dek="Tariffs on $375 billion of goods, a 'Phase One' deal that fell short, and research showing Americans paid the bill. The template for every trade war since.",
          card="Tariffs on over $375 billion of Chinese goods. The research says American buyers paid almost all of it.",
          sources=[["SCMP: US-China trade war timeline, key dates and events", "https://scmp.com/economy/global-economy/article/3177652/us-china-trade-war-timeline-key-dates-and-events-july-2018"],
                   ["NBER Digest: US consumers have borne the brunt of the current trade war", "https://www.nber.org/digest/may19/us-consumers-have-borne-brunt-current-trade-war"],
                   ["PIIE: Trump's Phase One trade deal with China", "https://www.piie.com/blogs/trade-and-investment-policy-watch/trumps-phase-one-trade-deal-china-and-us-election"]]),
f"""
<p>On 6 July 2018, the United States put a 25% tariff on about $34 billion of goods from China. China hit back the same day with 25% tariffs on $34 billion of American goods. The biggest trade war in modern times had begun.</p>
<h2>How it escalated</h2>
{chart(cover, "Value of annual Chinese imports covered by US tariffs, by stage.")}
<ul class="points">
  <li><b>Jul 2018</b><span>25% on $34bn. China matches it, targeting 545 US products including soybeans and cars.</span></li>
  <li><b>Aug 2018</b><span>25% on another $16bn. China matches again.</span></li>
  <li><b>Sep 2018</b><span>10% on $200bn more. China retaliates on $60bn of US goods.</span></li>
  <li><b>May 2019</b><span>The US raises that 10% to 25% after talks stall.</span></li>
  <li><b>Sep 2019</b><span>Tariffs on more than $125bn of further Chinese goods. By now, the two sides' tariffs cover over $450bn of trade between them.</span></li>
  <li><b>Jan 2020</b><span>The "Phase One" deal is signed. Tariffs stay mostly in place; China promises to buy more.</span></li>
</ul>
<h2>Who actually paid?</h2>
<p>The political promise was that China would pay. Economists checked.</p>
<p>A study by Mary Amiti, Stephen Redding and David Weinstein found the tariffs were "largely passed through" to US prices, meaning American companies and households paid them. They estimated the cost to US real incomes at about <strong>$1.4 billion a month</strong> by the end of 2018. A second study, by Pablo Fajgelbaum and colleagues, found the pass-through was complete.</p>
{chart(who, "How trade in the targeted goods changed in 2018.")}
<p>Trade didn't stop; it moved. The researchers estimated about $165 billion of trade was rerouted to avoid the tariffs, as buyers switched to suppliers in other countries.</p>
<h2>The deal that fell short</h2>
<p>Under Phase One, China committed to buy an extra $200 billion of US goods and services over 2020 and 2021, on top of 2017 levels. The Peterson Institute tracked it: by September 2020, China had bought only 53% of what it should have by then, and Chinese imports from the US were still 16% below 2017. Covid made targets harder, but the gap was large in almost every category, from aircraft to soybeans.</p>
<h2>So who won?</h2>
<p>By most measures, neither side got what it wanted. The US trade deficit with China narrowed for a while, but much of that trade moved to other countries rather than back to America. US farmers lost their biggest soybean customer and needed government support. Chinese exporters lost market share in the US and began moving some production abroad.</p>
<p>Supporters argue the tariffs succeeded in a different way: they forced the world to take China's trade practices seriously, and started the shift of supply chains away from China that India has been trying to capitalise on.</p>
<h2>Why it matters now</h2>
<p>The 2018 playbook, tariffs announced by presidential action, quick retaliation and purchase-commitment deals, is exactly what India has faced since 2025. Read <a href="/explainers/us-tariffs-on-india-2025-26.html">how US tariffs on India went from 50% to 18% to 10%</a>.</p>
""", OUT)

# ---------------------------------------------------------------- Trade: US tariffs on India 2025-26
pts = [(0.0, 10), (0.24, 25), (0.27, 50), (0.55, 18), (0.585, 10), (0.88, 10), (1.0, 10)]
tar = steps(pts, "Headline US tariff on most Indian goods: 10% baseline from April 2025, 25% from 7 August 2025, 50% from 27 August 2025, 18% after the 2 February 2026 deal, 10% Section 122 levy from 24 February 2026, replaced by a 10% Section 301 duty from late July 2026",
            0, 60, [0, 10, 25, 50], [(0, "Apr 25"), (0.24, "Aug 25"), (0.55, "Feb 26"), (0.88, "Jul 26")], fmt="{:g}%",
            hl_from=0.24, annotate=[(0.27, 50, "50%", "start", -8, "var(--red)"), (0.55, 18, "18%", "start", -8, "var(--ink)"), (0.88, 10, "10% (s.301)", "end", -8, "var(--ink)")])
save(dict(slug="us-tariffs-on-india-2025-26", date=D, order=-1, topic="trade global", tag="Trade", tag_class="",
          title="50%, then 18%, then 10%: the rollercoaster of US tariffs on India",
          short="50%, then 18%, then 10%: US tariffs on India, explained",
          dek="In 14 months, the US tariff on most Indian goods went from 25% to 50%, was cut to 18%, struck down by the US Supreme Court, and replaced with 10%. And a new threat is on the table.",
          card="From 50% in August 2025 to a 10% duty in July 2026, and now a threat of up to 100%. Every turn, explained.",
          sources=[["Multibagg: US tariffs on India, timeline explained (May 2026)", "https://www.multibagg.ai/market-pulse/articles/us-tariffs-india-timeline-2026-cmowpabmm00memn0jhvyf4z31"],
                   ["TIGI: From 50% to 18% to a fresh 10% (July 2026)", "https://tigi.global/articles/from-50-to-18-to-a-fresh-10-inside-indias-rollercoaster-year-of-us-tariff-diplom"],
                   ["Business Today: New US tariff on India after Supreme Court order, GTRI pegs average at 13.4%", "https://www.businesstoday.in/amp/latest/economy/story/what-is-the-new-us-tariff-on-india-after-sc-order-gtri-pegs-average-effective-rate-at-134-517390-2026-02-21"],
                   ["The Week: US retains 10% tariff on India under Section 301 (24 July 2026)", "https://www.theweek.in/news/biz-tech/2026/07/24/us-tariffs-section-301-india.html"],
                   ["AP: Trump says US to get diesel from Russia (9 Oct 2026)", "https://www.kttc.com/2026/10/09/trump-says-us-get-diesel-russia-relaxing-pressure-moscow-ease-prices-before-midterms/"]]),
f"""
<p>For Indian exporters, the last 14 months have been a lesson in how fast trade rules can change. Here's every turn, and where things stand now.</p>
{chart(tar, "Headline US tariff rate on most Indian goods. Some products were always exempt, and sector tariffs on steel, aluminium and auto parts run separately.")}
<h2>2025: from 10% to 50%</h2>
<ul class="points">
  <li><b>2 Apr 2025</b><span>The US announces a 26% tariff on India. Within a week the "reciprocal" part is paused and a 10% baseline applies.</span></li>
  <li><b>7 Aug 2025</b><span>A 25% tariff on Indian goods takes effect.</span></li>
  <li><b>27 Aug 2025</b><span>Another 25% is added as a penalty for India buying Russian oil. Total: <strong>50%</strong> on goods including gems and jewellery, garments, footwear, furniture, shrimp and chemicals.</span></li>
</ul>
<p>The hit was real. India's goods exports to the US were about $86.5 billion a year, and the Global Trade Research Initiative (GTRI) warned they could fall towards $50 billion. Surat's diamond units reported shutdowns, and the rupee fell past 89 to the dollar at the time.</p>
<p>Some of India's biggest exports were spared throughout: medicines, smartphones and petroleum products were exempt from the reciprocal tariffs.</p>
<h2>2026: deal, court, and a new legal route</h2>
<ul class="points">
  <li><b>2 Feb 2026</b><span>An interim trade deal. The US cuts the tariff to <strong>18%</strong> and drops the Russia-oil penalty. India commits to stop buying Russian crude, lower its own tariffs on US goods, and buy more American products.</span></li>
  <li><b>20 Feb 2026</b><span>The US Supreme Court strikes down tariffs imposed under the emergency powers law (IEEPA) that the reciprocal tariffs relied on.</span></li>
  <li><b>24 Feb 2026</b><span>The US replaces them with a temporary <strong>10%</strong> global levy under Section 122 of the Trade Act, which can last at most 150 days. GTRI estimated India's average effective tariff at about 13.4%, counting sector duties.</span></li>
  <li><b>Late Jul 2026</b><span>As Section 122 expires, the US imposes a <strong>10% Section 301 duty</strong> on 17 economies including India, following an investigation into forced-labour import rules. India's government estimates it covers about 55% of exports to the US.</span></li>
</ul>
<h2>Who's still hurting</h2>
<p>Labour-intensive sectors: textiles and garments, gems and jewellery, leather, engineering goods and chemicals now pay normal US duties plus 10%. Steel and aluminium still face 50% under separate national-security tariffs, and certain auto components 25%. In February the US also put a 126% duty on Indian solar imports.</p>
<h2>The next threat</h2>
<p>On 18 September 2026, President Trump signed a sanctions law directing tariffs of up to <strong>100%</strong> on the five biggest buyers of Russian oil and gas. India committed to stop buying Russian crude under the February deal; which five countries will be named is not yet known. Three weeks later, the US agreed to buy Russian diesel itself. Read <a href="/explainers/us-russia-diesel-deal.html">that story here</a>.</p>
<div class="callout"><b>Why it matters</b><p>Tariffs are paid by importers, but they decide whether an Indian product can compete on price. For workers in Surat, Tiruppur or Moradabad, each turn of this rollercoaster has meant more or fewer orders. The history suggests these fights rarely end cleanly; see <a href="/explainers/us-china-trade-war-2018-19.html">the US–China trade war of 2018–19</a>.</p></div>
""", OUT)

# ---------------------------------------------------------------- Markets: how indices work
ff = hbars([("Company A, total value", 100, "var(--rule)"), ("A, free float (60%)", 60, "var(--ink)"), ("Company B, total value", 100, "var(--rule)"), ("B, free float (20%)", 20, "var(--ink)")],
           "Illustration: two companies worth ₹100 each. A has 60% of shares available to trade, B only 20%, so A counts three times as much in a free-float index",
           fmt="₹{:g}", maxv=110, lw=170, unit_note="illustration, ₹ value counted in the index")
save(dict(slug="how-sensex-nifty-work", date=D, order=-2, topic="markets concepts", tag="Markets", tag_class="",
          title="How the Sensex and Nifty are actually calculated",
          short="How the Sensex and Nifty are actually calculated",
          dek="When the Nifty 'rises 1%', what exactly rose? The two numbers behind every market headline, from base year to free float.",
          card="What 'the market rose 1%' really means: base values, free float, and why a few big stocks move everything.",
          sources=[["NSE Indices (Nifty index provider)", "https://www.niftyindices.com/"],
                   ["Asia Index (Sensex index provider)", "https://www.asiaindex.co.in/"],
                   ["Business Standard: Stock market close, 13 October 2026", "https://www.business-standard.com/amp/markets/news/stock-market-live-october-13-bse-sensex-today-nifty50-gift-nifty-crude-oil-prices-q2-results-ipo-today-126101300081_1.html"]]),
f"""
<p>On 13 October 2026, the Sensex closed at <strong>73,033.78</strong> and the Nifty 50 at <strong>22,721.95</strong>. Both rose about 1.6% that day. But what is that number, and what does "rising 1.6%" mean?</p>
<h2>Two baskets of shares</h2>
<ul class="points">
  <li><b>Sensex</b><span>Tracks 30 large companies listed on the BSE. Its base is the year 1978–79, set at 100. Today's 73,000 means the basket is worth about 730 times what it was then.</span></li>
  <li><b>Nifty 50</b><span>Tracks 50 large companies on the NSE. Its base is 3 November 1995, set at 1,000.</span></li>
</ul>
<p>An index is just the combined value of its basket, scaled so that the base date equals the starting number. If the basket's total value rises 1.6%, the index rises 1.6%.</p>
<h2>Not every share counts: free float</h2>
<p>Both indices are weighted by <strong>free-float market capitalisation</strong>. Market capitalisation is a company's share price times its number of shares. Free float means only the shares that are actually available to trade, excluding big blocks held by promoters, governments or strategic owners.</p>
{chart(ff, "Two companies with the same total value can count very differently in the index.")}
<p>This is why a company that is 90% government-owned counts for much less in the index than its total size suggests, and why a widely held private bank can be one of the heaviest stocks in both indices.</p>
<h2>Why a few stocks move everything</h2>
<p>Because the biggest companies carry the biggest weights, a handful of heavyweight stocks, typically the largest private banks, Reliance and the big IT companies, can account for a large share of any day's move. On 13 October, for example, IT stocks led the rally after a strong start to the results season.</p>
<p>That also means the index can rise while most shares fall, or the other way round. That's why analysts watch "market breadth": how many stocks rose versus fell. Midcap and smallcap indices track the next tiers of companies.</p>
<h2>Who decides what's in?</h2>
<p>The Nifty is run by NSE Indices; the Sensex by Asia Index, a BSE company. Both review their baskets twice a year, adding companies that have grown and dropping those that have shrunk or become less traded. Being added to the Nifty matters: index funds that track it must then buy the stock.</p>
<h2>Points vs percent</h2>
<p>Headlines love points: "Sensex zooms 1,109 points." But a 1,000-point move meant much more when the Sensex was at 20,000 than at 73,000. Always look at the percentage. On 13 October, 1,109 points was a 1.54% move.</p>
<div class="callout"><b>Why it matters to you</b><p>If you own a Nifty index fund or ETF, you own a slice of these exact 50 companies, in these exact weights. If you own a large-cap mutual fund, the Nifty or Sensex is usually its benchmark. Our <a href="/explainers/#markets">daily markets updates</a> explain each day's move. Educational content only.</p></div>
""", OUT)

# ---------------------------------------------------------------- Markets: this week
sect = hbars([("Capital markets", 2, "var(--green)"), ("FMCG", 2, "var(--green)"), ("PSU banks", 2, "var(--green)"), ("Private banks", 2, "var(--green)"), ("IT", 1, "var(--green)"),
              ("Defence", -1.5, "var(--red)"), ("Auto", -2, "var(--red)"), ("Metal", -3, "var(--red)"), ("Realty", -3, "var(--red)")],
             "Nifty sector indices, week ended 9 October 2026: capital markets, FMCG, PSU banks and private banks about +2%, IT +1%, defence −1.5%, auto −2%, metal and realty −3%",
             fmt="{:+g}%", maxv=3.2, lw=130, unit_note="approximate weekly change, rounded (Navia)")
three = vbars([("Fri 9 Oct", 22520.45, "var(--ink)"), ("Mon 12 Oct", 22363.35, "var(--red)"), ("Tue 13 Oct", 22721.95, "var(--green)")],
              "Nifty 50 closing levels: 22,520.45 on Friday 9 October, 22,363.35 on Monday 12 October, 22,721.95 on Tuesday 13 October", fmt="{:,.0f}", maxv=24000, w=360)
save(dict(slug="markets-week-oct-12-2026", date=D, order=99, topic="markets", tag="Markets", tag_class="",
          title="Markets this week: the Nifty's longest losing streak in 25 years is over. Now what?",
          short="Markets: the Nifty's 8-week losing streak is over. Now what?",
          dek="Eight straight weeks of losses ended on Friday. On Tuesday the Nifty jumped 1.6%. What drove the turn, and what could stop it.",
          card="The Nifty ended its worst losing streak since 2001, then jumped 1.6% on Tuesday. What moved, and what's next.",
          hero_src="Data: NSE, BSE",
          sources=[["Navia: Weekly market roundup, 5–9 October 2026", "https://navia.co.in/blog/navia-weekly-roundup-oct-5-9-2026/"],
                   ["Business Standard: Stock market close, 13 October 2026", "https://www.business-standard.com/amp/markets/news/stock-market-live-october-13-bse-sensex-today-nifty50-gift-nifty-crude-oil-prices-q2-results-ipo-today-126101300081_1.html"],
                   ["Business Standard: FPIs pull out ₹44,166 cr in October", "https://www.business-standard.com/finance/news/fpis-pull-out-44-166-cr-from-equities-in-oct-2026-outflows-cross-3-trn-126101100210_1.html"],
                   ["Upstox: Market wrap, 9 October 2026", "https://upstox.com/news/market-news/stocks/market-wrap-oct-9-sensex-jumps-879-pts-nifty-50-ends-above-22-500-as-it-stocks-rally-apollo-hospitals-top-gainer/article-201607/"]]),
f"""
<p>For eight weeks in a row, Indian stocks fell. The streak, which shaved 8.7% off the Nifty and 8.4% off the Sensex, was the longest since 2001. It finally broke last Friday.</p>
<h2>Last week (5–9 October)</h2>
<ul class="points">
  <li><b>Nifty 50</b><span>22,520.45, up 0.43% for the week.</span></li>
  <li><b>Sensex</b><span>72,472.33, up 0.78%.</span></li>
  <li><b>Bank Nifty</b><span>55,256.65, up 0.25%.</span></li>
</ul>
<p>It was a week of whiplash. On Wednesday the RBI raised the repo rate to 5.50%, its first hike since 2023. On Thursday the Sensex fell 1,045 points to 71,593, wiping out about ₹10 lakh crore of market value. On Friday, strong results from TCS and a dip in crude oil sparked a 1.3% rally that turned the week positive.</p>
{chart(sect, "How sectors did last week.")}
<p>Banks and consumer companies led. Metals and real estate, which are most sensitive to interest rates and global demand, fell the most.</p>
<h2>This week so far</h2>
{chart(three, "Nifty 50 closing levels over the last three sessions.")}
<p><strong>Monday:</strong> the Nifty slipped about 0.7% to 22,363 ahead of September's inflation data, which came in at 5.54%, the highest of the new CPI series. Read <a href="/explainers/september-2026-inflation-onions.html">what drove it</a>.</p>
<p><strong>Tuesday:</strong> the Sensex jumped 1,109 points (1.54%) to 73,033.78 and the Nifty 1.6% to 22,721.95. IT was the top-performing sector. The trigger was Finance Minister Nirmala Sitharaman saying the government will listen to market participants on securities taxation, including long-term capital gains tax and securities transaction tax, as Budget 2027 preparations begin. No proposal has been announced.</p>
<p>Not everything rose. Cable and wire makers Polycab, KEI Industries and R R Kabel fell as much as 5% during the day on worries about competition, and are now about 24% below their highs of last month.</p>
<h2>Why one good week doesn't end a bad year</h2>
<ul class="points">
  <li><b>Down for the year</b><span>The Nifty was down 13.87% for 2026 as of last week.</span></li>
  <li><b>Foreign selling</b><span>FPIs sold ₹44,166 crore of Indian shares in the first part of October alone, taking 2026's total past ₹3 lakh crore. See <a href="/explainers/fed-hike-rupee-fpi-2026.html">why</a>.</span></li>
  <li><b>Rupee and oil</b><span>The rupee closed last week at 96.73 to the dollar, and Brent crude is above $100.</span></li>
</ul>
<h2>The week ahead</h2>
<ul class="points">
  <li><b>Wed 14 Oct</b><span>Wholesale inflation (WPI) for September.</span></li>
  <li><b>All week</b><span>Second-quarter results season continues, led by IT and banks.</span></li>
  <li><b>21 Oct</b><span>Jio Platforms' IPO, reported to be India's largest ever, is due to open.</span></li>
</ul>
<p>Our markets update now runs after every trading day. Educational content only. Nothing here is a recommendation to buy or sell.</p>
""", OUT)
print("part B done")
