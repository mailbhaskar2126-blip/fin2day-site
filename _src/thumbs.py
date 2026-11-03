"""Story thumbnails: a credited photo when content/thumbs.json lists one, otherwise a vector cover drawn from the
story's own lead chart (the chart spec that enhance.py made). Photos get a blue duotone in CSS so both kinds match."""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = json.load(open(os.path.join(HERE, "content", "thumbs.json"), encoding="utf-8"))

W, H = 400, 225
L, R, T, B = 30, 370, 112, 190  # chart band; the key figure sits above it
# field colour and mark colour per topic: every cover stays inside the site's blues
FIELDS = {"markets": ("#1D46C8", "#FFFFFF"), "global": ("#0E1A2E", "#8EA6E6"), "ipo": ("#142F8C", "#FFFFFF"),
          "rbi": ("#0E1A2E", "#FFFFFF"), "trade": ("#1D46C8", "#FFFFFF"), "concepts": ("#E9EEFB", "#1D46C8")}


def _spec(e):
    m = re.search(r'data-spec="([^"]+)"', e.get("hero_html") or "")
    return json.loads(html.unescape(m.group(1))) if m else None


def _field(e):
    topics = e["topic"].split()
    key = "global" if "global" in topics else topics[0]
    return FIELDS.get(key, FIELDS["markets"])


def _hbars(sp, mark):
    rows = sp["rows"][:7]
    pos = max([r["w"] for r in rows if not r["n"]] or [0]); neg = max([r["w"] for r in rows if r["n"]] or [0])
    tot = (pos + neg) or 1
    zx = L + neg / tot * (R - L)
    step = (B - T) / len(rows); bh = min(22, step * 0.62)
    out = []
    for i, r in enumerate(rows):
        w = r["w"] / tot * (R - L); y = T + i * step + (step - bh) / 2
        x = zx - w if r["n"] else zx
        op = 1 if r["w"] == (neg if r["n"] else pos) else (0.38 if r["n"] else 0.6)
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 2):.1f}" height="{bh:.1f}" rx="2" fill="{mark}" opacity="{op}"/>')
    if neg:
        out.append(f'<line x1="{zx:.1f}" x2="{zx:.1f}" y1="{T - 6}" y2="{B + 6}" stroke="{mark}" stroke-width="1.5" opacity=".7"/>')
    return "".join(out)


def _vbars(sp, mark):
    rows = sp["rows"][:10]
    pos = max([r["h"] for r in rows if not r["n"]] or [0]); neg = max([r["h"] for r in rows if r["n"]] or [0])
    tot = (pos + neg) or 1
    zy = T + pos / tot * (B - T)
    step = (R - L) / len(rows); bw = min(40, step * 0.6)
    out = [f'<line x1="{L}" x2="{R}" y1="{zy:.1f}" y2="{zy:.1f}" stroke="{mark}" stroke-width="1.5" opacity=".7"/>']
    for i, r in enumerate(rows):
        h = r["h"] / tot * (B - T); x = L + i * step + (step - bw) / 2
        y = zy if r["n"] else zy - h
        op = 1 if r["h"] == (neg if r["n"] else pos) else (0.38 if r["n"] else 0.6)
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(h, 2):.1f}" rx="2" fill="{mark}" opacity="{op}"/>')
    return "".join(out)


def _line(sp, mark, field):
    base = sp["series"][0]
    if "p" in base:
        pts = [(p[0], p[1]) for p in base["p"]]
    else:
        pts = [q for a, b, y, _ in base["r"] for q in ((a, y), (b, y))]
    if len(pts) < 2:
        return ""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    span = (y1 - y0) or 1
    P = [(L + (x - x0) / ((x1 - x0) or 1) * (R - L), T + 6 + (y - y0) / span * (B - T - 20)) for x, y in pts]
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in P)
    ex, ey = P[-1]
    return (f'<path d="{d}L{ex:.1f} {B}L{P[0][0]:.1f} {B}Z" fill="{mark}" opacity=".16"/>'
            f'<path d="{d}" fill="none" stroke="{mark}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="7" fill="{mark}" stroke="{field}" stroke-width="3"/>')


def _key(sp):
    """(label, value) to set large on the cover, taken from the chart itself: the biggest bar, or the line's last point."""
    if sp["k"] in ("h", "v"):
        size = "w" if sp["k"] == "h" else "h"
        r = max(sp["rows"], key=lambda r: r[size])
        # a bare number means nothing out of context; show it only with its unit
        return (r["l"], r["t"]) if re.search(r"[^\d\s,.+\-−~]", r["t"]) else None
    base = sp["series"][0]
    if "p" in base and base["p"] and base["p"][-1][2]:
        label = sp["xl"][-1][1] if sp.get("xl") else ""
        return label, base["p"][-1][2]
    return None


def _figure(sp, mark):
    k = _key(sp)
    if not k:
        return ""
    label, value = (html.escape(re.sub(r"^-", "−", s.strip())) for s in k)
    size = 44 if len(value) <= 9 else 34
    return (f'<text x="{L}" y="46" font-family="Schibsted Grotesk,Arial,sans-serif" font-weight="600" font-size="14" fill="{mark}" opacity=".82">{label}</text>'
            f'<text x="{L - 2}" y="{46 + size + 4}" font-family="Libre Caslon Text,Georgia,serif" font-weight="700" font-size="{size}" fill="{mark}">{value}</text>')


def _pattern(e, mark):
    """Fallback for stories with no readable chart: the story's tag set large, over a dot grid."""
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{mark}" opacity=".22"/>' for x in range(30, 380, 20) for y in range(30, 200, 20))
    return (dots + f'<text x="{R}" y="{B + 4}" text-anchor="end" font-family="Libre Caslon Text,Georgia,serif" font-weight="700" '
            f'font-size="64" fill="{mark}" opacity=".9">{html.escape(e["tag"])}</text>')


def cover(e):
    field, mark = _field(e)
    sp = _spec(e)
    grid = "".join(f'<line x1="{L}" x2="{R}" y1="{y}" y2="{y}" stroke="{mark}" opacity=".12"/>' for y in (T, (T + B) / 2, B))
    if sp and sp["k"] == "h":
        art = grid + _hbars(sp, mark) + _figure(sp, mark)
    elif sp and sp["k"] == "v":
        art = grid + _vbars(sp, mark) + _figure(sp, mark)
    elif sp and sp["k"] == "l":
        art = grid + _line(sp, mark, field) + _figure(sp, mark)
    else:
        art = _pattern(e, mark)
    two = "#8EA6E6" if field != "#E9EEFB" else "#0E1A2E"
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            f'<rect width="{W}" height="{H}" fill="{field}"/>{art}'
            f'<text x="{R}" y="46" text-anchor="end" font-family="Libre Caslon Text,Georgia,serif" font-weight="700" font-size="13" fill="{mark}">'
            f'FIN<tspan fill="{two}">2</tspan>DAY</text></svg>')


def thumb(e, href):
    """Card thumbnail, linked to the story. Decorative for screen readers: the card title is the link they use."""
    p = PHOTOS.get(e["slug"])
    if p:
        pos = f' style="object-position:{p["pos"]}"' if p.get("pos") else ""
        return (f'<a class="thumb photo" href="{href}" tabindex="-1" aria-hidden="true">'
                f'<img src="{p["file"]}" alt="" loading="lazy" width="960" height="540"{pos}>'
                f'<span class="credit">{html.escape(p["credit"])}</span></a>')
    return f'<a class="thumb" href="{href}" tabindex="-1" aria-hidden="true">{cover(e)}</a>'


def figure(e):
    """Lead photo for the article page, with a linked credit. Empty for stories without a photo."""
    p = PHOTOS.get(e["slug"])
    if not p:
        return ""
    pos = f' style="object-position:{p["pos"]}"' if p.get("pos") else ""
    return (f'<figure class="lead-photo"><div class="duo"><img src="{p["file"]}" alt="{html.escape(p["alt"])}" width="960" height="540"{pos}></div>'
            f'<figcaption><a href="{p["link"]}" target="_blank" rel="noopener">{html.escape(p["credit"])}</a></figcaption></figure>')
