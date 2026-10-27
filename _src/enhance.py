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


def _fill_tips(svg, circ, yt, snap=False):
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
            q = round(est / 0.05) * 0.05
            if not snap or abs(q - est) > 0.012:
                return None
            out.append((cx, cy, c, pre + f"{q:.2f}" + suf)); continue
        out.append((cx, cy, c, pre + best[1] + suf))
    return out


def _at(tag):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))


def line(svg):
    """Line / step charts, with optional shaded bands and dashed reference lines."""
    if "<polyline" not in svg and not re.search(r'<path d="M[^"]*H', svg):
        return None
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    W, H = float(vb.group(1)), float(vb.group(2))
    texts = [(_at(m.group(1)), _u(m.group(2))) for m in re.finditer(r"<text ([^>]*)>(.*?)</text>", svg)]
    yt = [(float(a["y"]) - 4, t) for a, t in texts if a.get("x") == "4" and a.get("y")]
    xl = [(float(a["x"]), t) for a, t in texts if a.get("text-anchor") == "middle" and float(a["y"]) >= H - 14 and "font-weight" not in a]
    ann = [(float(a["x"]), float(a["y"]), t, a.get("text-anchor", "start"), a.get("fill", "var(--ink)"), float(a.get("font-size", 11))) for a, t in texts
           if a.get("font-weight") == "700" and float(a["y"]) < H - 14 and a.get("x") != "4"]
    bands = [(float(a["x"]), float(a["y"]), float(a["width"]), float(a["height"]), a["fill"]) for a in (_at(m) for m in re.findall(r"<rect ([^>]*)/>", svg)) if "opacity" in a]
    refs = [(float(a["y1"]), a["stroke"]) for a in (_at(m) for m in re.findall(r"<line ([^>]*)/>", svg)) if a.get("stroke-dasharray") and a.get("stroke") != "var(--rule)" and a["y1"] == a["y2"]]
    series, tipsrc = [], []
    for pts, c, w in re.findall(r'<polyline points="([^"]+)" fill="none" stroke="([^"]+)" stroke-width="([\d.]+)"', svg):
        P = [tuple(float(v) for v in q.split(",")) for q in pts.split()]
        series.append({"c": c, "w": float(w), "d": "M" + "L".join(f"{x:g} {y:g}" for x, y in P), "pts": P})
    if not series:
        for d, c, w in re.findall(r'<path d="(M[^"]*H[^"]*)" fill="none" stroke="([^"]+)" stroke-width="([\d.]+)"', svg):
            runs, x, y = [], None, None
            for cmd, v in re.findall(r"([MHV])\s*([\d.]+)(?:\s+([\d.]+))?", d) and [(m[0], m[1:]) for m in re.findall(r"([MHV])\s*([\d.]+)(?:\s+([\d.]+))?", d)]:
                if cmd == "M": x, y = float(v[0]), float(v[1])
                elif cmd == "H":
                    nx = float(v[0])
                    if nx > x: runs.append((x, nx, y))
                    x = nx
                else: y = float(v[0])
            series.append({"c": c, "w": float(w), "d": d, "runs": runs})
    if not series:
        return None
    # exact values: stored tips, else the figures in the accessible label, accepted only if they sit on the axis position
    base = series[0]
    cir = re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="[\d.]+" fill="([^"]+)"(?: data-tip="([^"]*)")?', svg)
    if "pts" in base:
        if len(cir) < len(base["pts"]):
            return None
        cir = [(str(x), str(y), "", t) for (x, y), (_, _, _, t) in zip(base["pts"], cir[:len(base["pts"])])]
        if any(not c[3] for c in cir):
            cir = _fill_tips(svg, cir, yt)
            if cir is None:
                return None
        base["p"] = [[round(float(c[0]), 1), round(float(c[1]), 1), c[3]] for c in cir]
    else:
        tp = _fill_tips(svg, [(str(a), str(y), "", "") for a, _, y in base["runs"]], yt, snap=True)
        if tp is None:
            return None
        base["r"] = [[a, b, y, t[3]] for (a, b, y), t in zip(base["runs"], tp)]
    out = []
    for i, se in enumerate(series):
        o = {"c": se["c"], "w": se["w"], "d": se["d"]}
        if i == 0:
            if "p" in se: o["p"] = se["p"]
            else: o["r"] = se["r"]
        out.append(o)
    return {"k": "l", "W": W, "H": H, "series": out, "yt": yt, "xl": xl, "ann": ann, "bands": bands, "refs": refs}


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
