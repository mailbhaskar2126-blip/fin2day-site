"""Small SVG chart helpers matching the FIN2DAY site (uses CSS vars)."""
import json, os, re

MONO = 'font-family="JetBrains Mono, monospace"'
SANS = 'font-family="Inter, sans-serif"'


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def hbars(rows, label, fmt="{:g}", maxv=None, lw=150, w=460, unit_note=None):
    """rows: [(name, value, color)] ; horizontal bars, supports mixed negatives."""
    vals = [v for _, v, _ in rows]
    posmax = max([v for v in vals if v > 0] + [0])
    negmax = max([-v for v in vals if v < 0] + [0])
    if maxv and not negmax:
        posmax = maxv
    span = w - lw - 70
    tot = (posmax + negmax) or 1
    negw = span * negmax / tot + (40 if negmax and posmax else 0)
    zero = lw + negw
    scale = (span - (40 if negmax and posmax else 0)) / tot
    h = 16 + len(rows) * 32 + (18 if unit_note else 0)
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}"><g {SANS} font-size="12">']
    if negmax:
        out.append(f'<line x1="{zero:.0f}" x2="{zero:.0f}" y1="4" y2="{h-(22 if unit_note else 4)}" stroke="var(--ink)" stroke-width="1.2"/>')
    for i, (n, v, c) in enumerate(rows):
        y = 10 + i * 32
        bw = max(abs(v) * scale, 2)
        x = zero if v >= 0 else zero - bw
        out.append(f'<text x="{lw-10}" y="{y+14}" text-anchor="end" font-weight="600" fill="var(--ink)">{esc(n)}</text>')
        out.append(f'<rect x="{x:.0f}" y="{y+1}" width="{bw:.0f}" height="18" fill="{c}"/>')
        if v >= 0:
            out.append(f'<text x="{zero+bw+6:.0f}" y="{y+15}" {MONO} font-size="11" font-weight="700" fill="{c}">{esc(fmt.format(v))}</text>')
        else:
            out.append(f'<text x="{zero+6:.0f}" y="{y+15}" {MONO} font-size="11" font-weight="700" fill="{c}">{esc(fmt.format(v))}</text>')
    if unit_note:
        out.append(f'<text x="{lw}" y="{h-4}" {MONO} font-size="10" fill="var(--mute)">{esc(unit_note)}</text>')
    out.append("</g></svg>")
    return "".join(out)


def vbars(rows, label, fmt="{:g}", w=460, h=230, maxv=None, note=None):
    """rows: [(xlabel, value, color)] vertical bars (supports negatives)."""
    vals = [v for _, v, _ in rows]
    top = maxv or max(max(vals), 0)
    bot = min(min(vals), 0)
    plot_t, plot_b = 26, h - (46 if note else 34)
    sc = (plot_b - plot_t) / ((top - bot) or 1)
    zy = plot_t + top * sc
    n = len(rows)
    slot = (w - 20) / n
    bw = min(56, slot * 0.6)
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}"><g {SANS} font-size="12">',
           f'<line x1="10" x2="{w-10}" y1="{zy:.0f}" y2="{zy:.0f}" stroke="var(--ink)" stroke-width="1.2"/>']
    for i, (xl, v, c) in enumerate(rows):
        cx = 10 + slot * i + slot / 2
        bh = abs(v) * sc
        y = zy - bh if v >= 0 else zy
        out.append(f'<rect x="{cx-bw/2:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{max(bh,2):.0f}" fill="{c}"/>')
        if v >= 0:
            out.append(f'<text x="{cx:.0f}" y="{y-6:.0f}" text-anchor="middle" {MONO} font-size="11" font-weight="700" fill="{c}">{esc(fmt.format(v))}</text>')
        else:
            out.append(f'<text x="{cx:.0f}" y="{y+bh-8:.0f}" text-anchor="middle" {MONO} font-size="11" font-weight="700" fill="var(--paper)">{esc(fmt.format(v))}</text>')
        out.append(f'<text x="{cx:.0f}" y="{(zy-8) if v < 0 else zy+16:.0f}" text-anchor="middle" {MONO} font-size="10" fill="var(--mute)">{esc(xl)}</text>')
    if note:
        out.append(f'<text x="10" y="{h-4}" {MONO} font-size="10" fill="var(--mute)">{esc(note)}</text>')
    out.append("</g></svg>")
    return "".join(out)


def steps(points, label, ymin, ymax, yticks, xlabels, w=460, h=230, fmt="{:.2f}%", hl_from=None, color="var(--ink)", hl="var(--red)", annotate=()):
    """points: [(x 0..1, y)] step chart. xlabels: [(x 0..1, text)]."""
    L, R, T, B = 46, w - 12, 18, h - 30
    X = lambda x: L + x * (R - L)
    Y = lambda y: B - (y - ymin) / (ymax - ymin) * (B - T)
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}"><g {SANS} font-size="11">']
    for t in yticks:
        out.append(f'<line x1="{L}" x2="{R}" y1="{Y(t):.0f}" y2="{Y(t):.0f}" stroke="var(--rule)" stroke-dasharray="2 3"/>')
        out.append(f'<text x="4" y="{Y(t)+4:.0f}" {MONO} font-size="10" fill="var(--mute)">{fmt.format(t)}</text>')
    for x, t in xlabels:
        out.append(f'<text x="{X(x):.0f}" y="{h-8}" text-anchor="middle" {MONO} font-size="10" fill="var(--mute)">{esc(t)}</text>')
    d = f"M{X(points[0][0]):.1f} {Y(points[0][1]):.1f}"
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        d += f" H{X(x1):.1f} V{Y(y1):.1f}"
    d += f" H{R}"
    out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.4"/>')
    if hl_from is not None:
        seg = [p for p in points if p[0] >= hl_from]
        if seg:
            d2 = f"M{X(seg[0][0]):.1f} {Y(seg[0][1]):.1f}"
            for (x0, y0), (x1, y1) in zip(seg, seg[1:]):
                d2 += f" H{X(x1):.1f} V{Y(y1):.1f}"
            d2 += f" H{R}"
            out.append(f'<path d="{d2}" fill="none" stroke="{hl}" stroke-width="3"/>')
    for x, y, t, anchor, dy, c in annotate:
        out.append(f'<text x="{X(x):.0f}" y="{Y(y)+dy:.0f}" text-anchor="{anchor}" font-weight="700" font-size="11" fill="{c}">{esc(t)}</text>')
    out.append("</g></svg>")
    return "".join(out)


def _tip(fmt, y):
    """Exact value for the hover readout, keeping the axis format's prefix/suffix (e.g. %, $)."""
    s = fmt.format(y)
    try:
        if abs(float(re.sub(r"[^0-9.\-]", "", s)) - y) < 1e-9:
            return s
    except ValueError:
        pass
    pre, suf = fmt.split("{", 1)[0], fmt.rsplit("}", 1)[-1]
    raw = f"{y:,.2f}".rstrip("0").rstrip(".")
    return pre + raw + suf


def line(series, label, ymin, ymax, yticks, xlabels, w=460, h=230, fmt="{:g}", annotate=(), tipfmt=None):
    """series: [(color, [(x 0..1, y)], name)]. Each point carries its exact value for the hover readout
    (tipfmt, else the axis fmt with full precision)."""
    L, R, T, B = 46, w - 12, 18, h - 30
    X = lambda x: L + x * (R - L)
    Y = lambda y: B - (y - ymin) / (ymax - ymin) * (B - T)
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}"><g {SANS} font-size="11">']
    for t in yticks:
        out.append(f'<line x1="{L}" x2="{R}" y1="{Y(t):.0f}" y2="{Y(t):.0f}" stroke="var(--rule)" stroke-dasharray="2 3"/>')
        out.append(f'<text x="4" y="{Y(t)+4:.0f}" {MONO} font-size="10" fill="var(--mute)">{fmt.format(t)}</text>')
    for x, t in xlabels:
        out.append(f'<text x="{X(x):.0f}" y="{h-8}" text-anchor="middle" {MONO} font-size="10" fill="var(--mute)">{esc(t)}</text>')
    for c, pts, _ in series:
        out.append(f'<polyline points="{" ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in pts)}" fill="none" stroke="{c}" stroke-width="2.4"/>')
        out.extend(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="3.5" fill="{c}" data-tip="{esc(tipfmt.format(y) if tipfmt else _tip(fmt, y))}"/>' for x, y in pts)
    for x, y, t, anchor, dy, c in annotate:
        out.append(f'<text x="{X(x):.0f}" y="{Y(y)+dy:.0f}" text-anchor="{anchor}" font-weight="700" font-size="11" fill="{c}">{esc(t)}</text>')
    out.append("</g></svg>")
    return "".join(out)


def flow(boxes, label, w=460):
    """Vertical chain of boxes with arrows: [(title, sub)]"""
    bh, gap = 48, 22
    h = len(boxes) * (bh + gap) - gap + 8
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}"><g {SANS}>']
    for i, (t, s) in enumerate(boxes):
        y = 4 + i * (bh + gap)
        fill = "var(--ink)" if i == 0 else "var(--paper)"
        tc = "var(--paper)" if i == 0 else "var(--ink)"
        out.append(f'<rect x="20" y="{y}" width="{w-40}" height="{bh}" fill="{fill}" stroke="var(--ink)" stroke-width="1.3"/>')
        out.append(f'<text x="36" y="{y+20}" font-size="13" font-weight="700" fill="{tc}">{esc(t)}</text>')
        out.append(f'<text x="36" y="{y+38}" font-size="11" fill="{tc}" opacity=".8">{esc(s)}</text>')
        if i < len(boxes) - 1:
            ay = y + bh
            out.append(f'<path d="M{w/2} {ay+3} V{ay+gap-4}" stroke="var(--red)" stroke-width="2"/><path d="M{w/2-5} {ay+gap-9} L{w/2} {ay+gap-3} L{w/2+5} {ay+gap-9}" fill="none" stroke="var(--red)" stroke-width="2"/>')
    out.append("</g></svg>")
    return "".join(out)


def chart(svg, cap):
    return f'<div class="chart">{svg}<div class="cap">{cap}</div></div>'


def save(meta, body, outdir):
    os.makedirs(outdir, exist_ok=True)
    json.dump(meta, open(os.path.join(outdir, meta["slug"] + ".json"), "w"), indent=1, ensure_ascii=False)
    open(os.path.join(outdir, meta["slug"] + ".html"), "w").write(body.strip() + "\n")
