// FIN2DAY charts v2. Renders .chart.ic[data-spec] (same JSON as v1); the static SVG inside stays as the no-JS fallback.
(function () {
  var NS = 'http://www.w3.org/2000/svg';
  var els = document.querySelectorAll('.chart.ic[data-spec]');
  if (!els.length) return;
  var h = function (tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  var s = function (tag, attrs) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); return e; };
  var sign = function (t) { return String(t).replace(/^-/, '−'); };

  // specs name v1 colours; map them onto the v2 series palette, keeping their meaning
  var MAP = {'var(--ink)': 'var(--s1)', 'var(--green)': 'var(--s-up)', 'var(--red)': 'var(--s-down)', 'var(--amber)': 'var(--s-warn)', 'var(--brass)': 'var(--s1)', 'var(--hot)': 'var(--s1)', 'var(--blue)': 'var(--s1)'};
  var col = function (c) { return MAP[c] || c; };

  // white text on dark bars, navy on light ones
  function onColor(el) {
    var m = getComputedStyle(el).backgroundColor.match(/[\d.]+/g) || [0, 0, 0];
    return (0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]) / 255 > 0.6 ? '#0E1A2E' : '#fff';
  }

  function hbars(sp, box) {
    var pos = 0, neg = 0;
    sp.rows.forEach(function (r) { if (r.n) neg = Math.max(neg, r.w); else pos = Math.max(pos, r.w); });
    var tot = (pos + neg) * 1.12 || 1, z = neg / tot * 100;
    var wrap = h('div', 'hb'); wrap.setAttribute('role', 'list');
    sp.rows.forEach(function (r, i) {
      var w = r.w / tot * 100, c = col(r.c), row = h('div', 'hb-row');
      row.setAttribute('role', 'listitem'); row.tabIndex = 0;
      row.style.setProperty('--d', (i * 70) + 'ms');
      row.setAttribute('aria-label', r.l + ': ' + sign(r.t));
      var track = h('div', 'hb-t');
      if (neg) { var zl = h('i', 'hb-z'); zl.style.left = z + '%'; track.appendChild(zl); }
      var bar = h('div', 'hb-b'); bar.style.background = c;
      bar.style.left = (r.n ? z - w : z) + '%'; bar.style.width = Math.max(w, 0.6) + '%';
      bar.style.transformOrigin = r.n ? 'right center' : 'left center';
      if (r.n) bar.style.borderRadius = '3px 0 0 3px';
      bar.appendChild(h('span', 'hb-v', sign(r.t)));
      track.appendChild(bar); row.appendChild(h('div', 'hb-l', r.l)); row.appendChild(track); wrap.appendChild(row);
    });
    box.appendChild(wrap);
    if (sp.note) box.appendChild(h('div', 'ic-note', sp.note));
    // value sits inside the bar when it fits, otherwise just past its end in the bar's colour
    return function () {
      wrap.querySelectorAll('.hb-b').forEach(function (bar) {
        var v = bar.querySelector('.hb-v'), left = bar.style.transformOrigin.indexOf('right') === 0;
        bar.classList.remove('in', 'out'); v.style.position = v.style.left = v.style.right = v.style.color = '';
        if (bar.clientWidth >= v.offsetWidth + 18) { bar.classList.add('in'); v.style.color = onColor(bar); }
        else {
          // a negative bar with no room on its left puts its value on the right of the zero line instead
          var side = left && bar.offsetLeft < v.offsetWidth + 10 ? 'left' : (left ? 'right' : 'left');
          bar.classList.add('out'); v.style.position = 'absolute'; v.style[side] = 'calc(100% + 7px)'; v.style.color = bar.style.background;
        }
      });
    };
  }

  function vbars(sp, box) {
    var pos = 0, neg = 0;
    sp.rows.forEach(function (r) { if (r.n) neg = Math.max(neg, r.h); else pos = Math.max(pos, r.h); });
    var tot = (pos + neg) || 1, H = 250, padT = 28, padB = 64, area = H - padT - padB;
    var wrap = h('div', 'vb' + (sp.rows.length > 6 ? ' dense' : '')); wrap.style.height = H + 'px'; wrap.setAttribute('role', 'list');
    var zy = padT + pos / tot * area;
    [0.5, 1].forEach(function (f) { if (pos) { var g = h('i', 'vb-g'); g.style.top = (zy - pos / tot * area * f) + 'px'; wrap.appendChild(g); } });
    var base = h('i', 'vb-z'); base.style.top = zy + 'px'; wrap.appendChild(base);
    sp.rows.forEach(function (r, i) {
      var c = col(r.c), cl = h('div', 'vb-c'); cl.tabIndex = 0; cl.setAttribute('role', 'listitem');
      cl.style.setProperty('--d', (i * 70) + 'ms'); cl.setAttribute('aria-label', r.l + ': ' + sign(r.t));
      var bh = r.h / tot * area, bar = h('div', 'vb-b' + (r.n ? ' neg' : '')); bar.style.background = c; bar.style.height = Math.max(bh, 2) + 'px';
      bar.style.top = (r.n ? zy : zy - bh) + 'px'; bar.style.transformOrigin = r.n ? 'center top' : 'center bottom';
      var v = h('span', 'vb-v', sign(r.t)); v.style.color = c; v.style.top = (r.n ? zy + bh + 5 : zy - bh - 22) + 'px';
      var x = h('span', 'vb-x', r.l); x.style.top = (H - padB + (neg ? 28 : 10)) + 'px';
      cl.appendChild(bar); cl.appendChild(v); cl.appendChild(x); wrap.appendChild(cl);
    });
    box.appendChild(wrap);
    if (sp.note) box.appendChild(h('div', 'ic-note', sp.note));
  }

  function line(sp, box) {
    var W = sp.W, H = sp.H, wrap = h('div', 'ln'), tip = h('div', 'ln-tip');
    var svg = s('svg', {viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': sp.a});
    var L = 46, T = 14, B = sp.yt.length ? Math.max.apply(null, sp.yt.map(function (t) { return t[0]; })) : H - 30;
    var text = function (x, y, str, cls, anchor) { var t = s('text', {x: x, y: y, class: cls}); if (anchor) t.setAttribute('text-anchor', anchor); t.textContent = str; svg.appendChild(t); return t; };
    (sp.bands || []).forEach(function (b) { svg.appendChild(s('rect', {x: b[0], y: b[1], width: b[2], height: b[3], fill: col(b[4]), opacity: .08})); });
    sp.yt.forEach(function (t) { svg.appendChild(s('line', {x1: L - 4, x2: W - 4, y1: t[0], y2: t[0], class: 'ln-g'})); text(2, t[0] + 4, t[1], 'ln-y'); });
    svg.appendChild(s('line', {x1: L - 4, x2: W - 4, y1: B + 0.5, y2: B + 0.5, class: 'ln-base'}));
    (sp.refs || []).forEach(function (r) { svg.appendChild(s('line', {x1: L - 4, x2: W - 4, y1: r[0], y2: r[0], stroke: col(r[1]), 'stroke-dasharray': '5 4', 'stroke-width': 1.3})); });
    sp.xl.forEach(function (t) { svg.appendChild(s('line', {x1: t[0], x2: t[0], y1: B, y2: B + 5, class: 'ln-tick'})); text(t[0], H - 6, t[1], 'ln-x', 'middle'); });
    var base = sp.series[0], bc = col(base.c), hov = [];
    var id = 'g' + Math.random().toString(36).slice(2, 7), gr = s('linearGradient', {id: id, x1: 0, x2: 0, y1: 0, y2: 1});
    gr.appendChild(s('stop', {offset: '0%', 'stop-color': bc, 'stop-opacity': '.20'})); gr.appendChild(s('stop', {offset: '100%', 'stop-color': bc, 'stop-opacity': '0'}));
    var defs = s('defs', {}); defs.appendChild(gr); svg.appendChild(defs);
    var lastx, lasty;
    if (base.p) { base.p.forEach(function (p) { hov.push({x: p[0], y: p[1], t: p[2]}); }); lastx = base.p[base.p.length - 1][0]; lasty = base.p[base.p.length - 1][1]; }
    else { var rr = base.r[base.r.length - 1]; lastx = rr[1]; lasty = rr[2]; }
    var fx = Number(base.d.match(/-?[\d.]+/)[0]);
    svg.appendChild(s('path', {d: base.d + 'L' + lastx + ' ' + B + 'L' + fx + ' ' + B + 'Z', fill: 'url(#' + id + ')', class: 'ln-area'}));
    sp.series.forEach(function (se) {
      svg.appendChild(s('path', {d: se.d, fill: 'none', stroke: col(se.c), 'stroke-width': Math.max(se.w || 0, 2.6), 'stroke-linejoin': 'round', 'stroke-linecap': 'round', class: 'ln-p', pathLength: 1}));
    });
    hov.forEach(function (p) { svg.appendChild(s('circle', {cx: p.x, cy: p.y, r: 3.2, stroke: bc, class: 'ln-pt'})); });
    // labels sitting on a data point become value pills; the rest (reference lines, bands) stay plain text
    var onPoint = function (a) { return hov.some(function (p) { return Math.abs(p.x - a[0]) < 26 && Math.abs(p.y - a[1]) < 26; }) || (Math.abs(lastx - a[0]) < 26 && Math.abs(lasty - a[1]) < 26); };
    var pills = [], notes = [];
    (sp.ann || []).forEach(function (a) {
      var c = col(a[4]);
      if (onPoint(a)) {
        var g = s('g', {class: 'ln-pill'}), r = s('rect', {fill: c, rx: 4}), t = s('text', {'text-anchor': 'middle'}); t.textContent = a[2];
        g.appendChild(r); g.appendChild(t); svg.appendChild(g);
        pills.push({a: a, r: r, t: t});
      } else {
        var n = s('text', {x: a[0], y: a[1], 'text-anchor': a[3] || 'start', class: 'ln-a', fill: c}); n.textContent = a[2]; svg.appendChild(n);
        notes.push(n);
      }
    });
    var cross = s('line', {y1: T, y2: B, class: 'ln-c'}), dot = s('circle', {r: 5.5, class: 'ln-hd', fill: bc});
    svg.appendChild(cross); svg.appendChild(dot);
    wrap.appendChild(svg); wrap.appendChild(tip); box.appendChild(wrap);

    // keep chart text at a readable px size whatever width the svg renders at
    var fit = function () {
      var w = svg.getBoundingClientRect().width; if (!w) return;
      var k = W / w, fs = 11.5 * k;
      svg.querySelectorAll('.ln-y,.ln-x').forEach(function (t) { t.style.fontSize = fs + 'px'; });
      notes.forEach(function (n) { n.style.fontSize = 12 * k + 'px'; n.style.strokeWidth = 4 * k + 'px'; });
      pills.forEach(function (p) {
        var px = 12 * k, padX = 7 * k, ph = 20 * k;
        p.t.style.fontSize = px + 'px';
        var tw = p.t.getComputedTextLength(), pw = tw + padX * 2;
        var x = p.a[3] === 'end' ? Math.min(W - 2, p.a[0] + pw * 0.15) - pw : p.a[3] === 'middle' ? p.a[0] - pw / 2 : p.a[0];
        x = Math.max(0, Math.min(W - pw, x));
        var y = Math.max(0, p.a[1] - 4 * k - ph / 2);
        p.r.setAttribute('x', x); p.r.setAttribute('y', y); p.r.setAttribute('width', pw); p.r.setAttribute('height', ph); p.r.setAttribute('rx', 4 * k);
        p.t.setAttribute('x', x + pw / 2); p.t.setAttribute('y', y + ph / 2 + px * 0.36);
      });
    };
    var show = function (ev) {
      var r = svg.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width * W, hx, hy, label = '', t;
      if (base.p) { var best = hov[0]; hov.forEach(function (p) { if (Math.abs(p.x - x) < Math.abs(best.x - x)) best = p; }); hx = best.x; hy = best.y; t = best.t; var i = hov.indexOf(best); label = sp.xl[i] ? sp.xl[i][1] : ''; }
      else { var run = base.r[0]; base.r.forEach(function (q) { if (q[0] <= x + 0.01) run = q; }); hx = Math.max(run[0], Math.min(run[1], x)); hy = run[2]; t = run[3]; }
      cross.setAttribute('x1', hx); cross.setAttribute('x2', hx); cross.style.opacity = 1;
      dot.setAttribute('cx', hx); dot.setAttribute('cy', hy); dot.style.opacity = 1;
      tip.innerHTML = ''; if (label) tip.appendChild(h('span', '', label)); tip.appendChild(h('b', '', t));
      tip.classList.add('on');
      var px = hx / W * r.width, tw = tip.offsetWidth;
      tip.style.left = Math.max(0, Math.min(r.width - tw, px - tw / 2)) + 'px'; tip.style.top = Math.max(0, hy / H * r.height - 46) + 'px';
    };
    var hide = function () { cross.style.opacity = 0; dot.style.opacity = 0; tip.classList.remove('on'); };
    svg.addEventListener('pointermove', show); svg.addEventListener('pointerdown', show); svg.addEventListener('pointerleave', hide);
    return fit;
  }

  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.remove('wait'); io.unobserve(e.target); } });
  }, {threshold: 0.25}) : null;
  var fits = [];

  els.forEach(function (el) {
    try {
      var sp = JSON.parse(el.getAttribute('data-spec')), fb = el.querySelector('.ic-fallback'), box = h('div', 'ic-body'), fit;
      if (sp.k === 'h') fit = hbars(sp, box); else if (sp.k === 'v') vbars(sp, box); else if (sp.k === 'l') fit = line(sp, box); else return;
      el.insertBefore(box, fb); if (fb) fb.hidden = true;
      el.classList.add('ready', 'ic-' + sp.k);
      if (fit) { fit(); fits.push(fit); }
      if (io) { el.classList.add('wait'); io.observe(el); }
    } catch (e) { /* keep the static SVG */ }
  });
  var refit = function () { fits.forEach(function (f) { f(); }); };
  window.addEventListener('resize', refit);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(refit);
})();
