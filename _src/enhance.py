"""Turns the static SVG charts in story bodies into data specs for assets/charts.js (interactive renderer).
Anything it cannot read exactly is left as the original static SVG. The original SVG is kept inside as a no-JS fallback."""
import re, json, html

CH = re.compile(r'<div class="chart">(<svg.*?</svg>)(.*?)</div>', re.S)
HB = re.compile(r'<text[^>]*text-anchor="end"[^>]*>(.*?)</text><rect x="([\d.]+)" y="[\d.]+" width="([\d.]+)" height="18" fill="([^"]+)"/><text [^>]*>(.*?)</text>')
VB = re.compile(r'<rect x="([\d.]+)" y="([\d.]+)" width="[\d.]+" height="([\d.]+)" fill="([^"]+)"/><text [^>]*>(.*?)</text><text [^>]*>(.*?)</text>')
ZERO = re.compile(r'<line x1="([\d.]+)" x2="([\d.]+)" y1="([\d.]+)" y2="([\d.]+)" stroke="var\(--ink\)"')
NOTE = re.compile(r'<text [^>]*font-size="10" fill="var\(--mute\)">([^<]*)</text></g></svg>$')
LABEL = re.compile(r'aria-label="([^"]*)"')


def _u(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def hbars(svg):
    rows = HB.findall(svg)
    if not rows or len(rows) != svg.count("<rect"):
        return None
    z = ZERO.search(svg)
    zx = float(z.group(1)) if z else None
    out = []
    for lab, x, w, c, val in rows:
        x, w = float(x), float(w)
        neg = zx is not None and x < zx - 0.5
        out.append({"l": _u(lab), "t": _u(val), "w": w, "n": neg, "c": c})
    n = NOTE.search(svg)
    return {"k": "h", "rows": out, "note": _u(n.group(1)) if n else ""}


def vbars(svg):
    rows = VB.findall(svg)
    if not rows or len(rows) != svg.count("<rect"):
        return None
    z = ZERO.search(svg)
    if not z:
        return None
    zy = float(z.group(3))
    out = []
    for x, y, h, c, val, xl in rows:
        y, h = float(y), float(h)
        out.append({"l": _u(xl), "t": _u(val), "h": h, "n": y >= zy - 0.5 and h > 0 and abs(y - zy) < 0.5, "c": c})
    n = NOTE.search(svg)
    return {"k": "v", "rows": out, "note": _u(n.group(1)) if n else ""}


def _num(t):
    m = re.search(r"-?[\d][\d,]*(?:\.\d+)?", t.replace("\u2212", "-"))
    return float(m.group(0).replace(",", "")) if m else None


def _fill_tips(svg, circ, yt):
    """Points without a stored value get the exact figure from the chart's accessible label, accepted only if it matches the axis position."""
    ticks = [(y, _num(t), t) for y, t in yt if _num(t) is not None]
    if len(ticks) < 2:
        return None
    (y1, v1, t1), (y2, v2, t2) = ticks[0], ticks[-1]
    per_px = (v2 - v1) / (y2 - y1)
    label = html.unescape(LABEL.search(svg).group(1)).replace("\u2212", "-")
    toks = re.findall(r"-?\d[\d,]*(?:\.\d+)?", label)
    nums = [(float(t.replace(",", "")), t) for t in toks]
    pre = re.match(r"^[^\d\-]*", t1.replace("\u2212", "-")).group(0)
    suf = re.search(r"[^\d.,]*$", t1).group(0)
    out = []
    for cx, cy, c, tip in circ:
        if tip:
            out.append((cx, cy, c, tip)); continue
        est = v1 + (float(cy) - y1) * per_px
        best = min(nums, key=lambda n: abs(n[0] - est), default=None)
        if best is None or abs(best[0] - est) > abs(per_px) * 2.5:
            return None
        out.append((cx, cy, c, pre + best[1] + suf))
    return out


def line(svg):
    if "<polyline" not in svg:
        return None
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    W, H = float(vb.group(1)), float(vb.group(2))
    pls = re.findall(r'<polyline points="([^"]+)" fill="none" stroke="([^"]+)"', svg)
    circ = re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="[\d.]+" fill="([^"]+)"(?: data-tip="([^"]*)")?', svg)
    if not pls or not circ or len(circ) != sum(len(p[0].split()) for p in pls):
        return None
    yt = [(float(y), _u(t)) for y, t in re.findall(r'<line x1="[\d.]+" x2="[\d.]+" y1="[\d.]+" y2="([\d.]+)" stroke="var\(--rule\)"[^>]*/><text x="4"[^>]*>(.*?)</text>', svg)]
    if any(not c[3] for c in circ):
        circ = _fill_tips(svg, circ, yt)
        if circ is None:
            return None
    xl = [(float(x), _u(t)) for x, t in re.findall(r'<text x="([\d.]+)" y="%d" text-anchor="middle"[^>]*>(.*?)</text>' % (H - 8), svg)]
    ann = [(float(x), float(y), _u(t), a, c) for x, y, a, c, t in re.findall(r'<text x="([\d.]+)" y="([\d.\-]+)" text-anchor="(\w+)" font-weight="700" font-size="11" fill="([^"]+)">(.*?)</text>', svg)]
    series, i = [], 0
    for pts, c in pls:
        n = len(pts.split())
        series.append({"c": c, "p": [[round(float(a), 1), round(float(b), 1), _u(circ[i + j][3])] for j, (a, b) in enumerate(p.split(",") for p in pts.split())]})
        i += n
    return {"k": "l", "W": W, "H": H, "series": series, "yt": yt, "xl": xl, "ann": ann}


def enhance(body):
    def sub(m):
        svg, cap = m.group(1), m.group(2)
        spec = hbars(svg) or vbars(svg) or line(svg)
        if not spec:
            return m.group(0)
        al = LABEL.search(svg)
        spec["a"] = html.unescape(al.group(1)) if al else ""
        return (f'<div class="chart ic" data-spec="{html.escape(json.dumps(spec, ensure_ascii=False, separators=(",", ":")), quote=True)}">'
                f'<div class="ic-fallback">{svg}</div>{cap}</div>')
    return CH.sub(sub, body)
