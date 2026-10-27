// FIN2DAY interactive charts. Renders .chart.ic[data-spec] from JSON; the original SVG inside stays as the no-JS fallback.
(function () {
  var NS = 'http://www.w3.org/2000/svg';
  var els = document.querySelectorAll('.chart.ic[data-spec]');
  if (!els.length) return;
  var h = function (tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  var s = function (tag, attrs) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); return e; };
  var sign = function (t) { return t.replace(/^-/, '−'); };

  function hbars(sp, box) {
    var pos = 0, neg = 0;
    sp.rows.forEach(function (r) { if (r.n) neg = Math.max(neg, r.w); else pos = Math.max(pos, r.w); });
    var tot = (pos + neg) || 1, z = neg / tot * 100;
    var wrap = h('div', 'hb'); wrap.setAttribute('role', 'list');
    sp.rows.forEach(function (r, i) {
      var w = r.w / tot * 100, row = h('div', 'hb-row'); row.setAttribute('role', 'listitem'); row.tabIndex = 0;
      row.style.setProperty('--d', (i * 55) + 'ms');
      row.setAttribute('aria-label', r.l + ': ' + sign(r.t));
      var lab = h('div', 'hb-l', r.l), track = h('div', 'hb-t');
      if (neg) { var zl = h('i', 'hb-z'); zl.style.left = z + '%'; track.appendChild(zl); }
      var bar = h('div', 'hb-b'); bar.style.background = r.c;
      bar.style.left = (r.n ? z - w : z) + '%'; bar.style.width = Math.max(w, 0.6) + '%';
      bar.style.transformOrigin = r.n ? 'right center' : 'left center';
      var inside = w > 24, v = h('span', 'hb-v', sign(r.t));
      if (inside) { bar.classList.add('in'); bar.appendChild(v); v.style.color = '#fff'; }
      else { v.style.color = r.c; v.style.position = 'absolute'; v.style[r.n ? 'right' : 'left'] = 'calc(100% + 8px)'; bar.appendChild(v); bar.classList.add('out'); }
      track.appendChild(bar); row.appendChild(lab); row.appendChild(track); wrap.appendChild(row);
    });
    box.appendChild(wrap);
    if (sp.note) box.appendChild(h('div', 'ic-note', sp.note));
  }

  function vbars(sp, box) {
    var pos = 0, neg = 0;
    sp.rows.forEach(function (r) { if (r.n) neg = Math.max(neg, r.h); else pos = Math.max(pos, r.h); });
    var tot = (pos + neg) || 1, H = 230, padT = 26, padB = 46, area = H - padT - padB;
    var wrap = h('div', 'vb' + (sp.rows.length > 6 ? ' dense' : '')); wrap.style.height = H + 'px';
    var zy = padT + pos / tot * area;
    var base = h('i', 'vb-z'); base.style.top = zy + 'px'; wrap.appendChild(base);
    sp.rows.forEach(function (r, i) {
      var col = h('div', 'vb-c'); col.tabIndex = 0; col.style.setProperty('--d', (i * 60) + 'ms');
      col.setAttribute('aria-label', r.l + ': ' + sign(r.t));
      var bh = r.h / tot * area, bar = h('div', 'vb-b'); bar.style.background = r.c; bar.style.height = Math.max(bh, 2) + 'px';
      bar.style.top = (r.n ? zy : zy - bh) + 'px'; bar.style.transformOrigin = r.n ? 'center top' : 'center bottom';
      var v = h('span', 'vb-v', sign(r.t)); v.style.color = r.c;
      v.style.top = (r.n ? zy + bh + 4 : zy - bh - 20) + 'px';
      var x = h('span', 'vb-x', r.l); x.style.top = (H - 20) + 'px';
      col.appendChild(bar); col.appendChild(v); col.appendChild(x); wrap.appendChild(col);
    });
    box.appendChild(wrap);
    if (sp.note) box.appendChild(h('div', 'ic-note', sp.note));
  }

  function line(sp, box) {
    var W = sp.W, H = sp.H, wrap = h('div', 'ln'), tip = h('div', 'ln-tip');
    var svg = s('svg', {viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': sp.a});
    var xs = sp.xl.map(function (t) { return t[0]; }), L = 46, R = W - 8, T = 14, B = sp.yt.length ? Math.max.apply(null, sp.yt.map(function (t) { return t[0]; })) : H - 30;
    (sp.bands || []).forEach(function (b) { svg.appendChild(s('rect', {x: b[0], y: b[1], width: b[2], height: b[3], fill: b[4], opacity: .09, class: 'ln-band'})); });
    sp.yt.forEach(function (t) {
      svg.appendChild(s('line', {x1: L - 4, x2: W - 6, y1: t[0], y2: t[0], class: 'ln-g'}));
      var tx = s('text', {x: 2, y: t[0] + 4, class: 'ln-y'}); tx.textContent = t[1]; svg.appendChild(tx);
    });
    svg.appendChild(s('line', {x1: L - 4, x2: W - 6, y1: B + 0.5, y2: B + 0.5, class: 'ln-base'}));
    (sp.refs || []).forEach(function (r) { svg.appendChild(s('line', {x1: L - 4, x2: W - 6, y1: r[0], y2: r[0], stroke: r[1], 'stroke-dasharray': '5 4', 'stroke-width': 1.4, class: 'ln-ref'})); });
    sp.xl.forEach(function (t) { svg.appendChild(s('line', {x1: t[0], x2: t[0], y1: B, y2: B + 5, class: 'ln-tick'})); var tx = s('text', {x: t[0], y: H - 6, class: 'ln-x', 'text-anchor': 'middle'}); tx.textContent = t[1]; svg.appendChild(tx); });
    var base = sp.series[0], hov = [], endp;
    sp.series.forEach(function (se, si) {
      if (si === 0 && sp.series.length >= 1) {
        var id = 'ica' + Math.random().toString(36).slice(2, 7), gr = s('linearGradient', {id: id, x1: 0, x2: 0, y1: 0, y2: 1});
        gr.appendChild(s('stop', {offset: '0%', 'stop-color': se.c, 'stop-opacity': '.22'})); gr.appendChild(s('stop', {offset: '100%', 'stop-color': se.c, 'stop-opacity': '0'}));
        var defs = s('defs', {}); defs.appendChild(gr); svg.appendChild(defs);
        var nums = se.d.match(/-?[\d.]+/g).map(Number), fx = nums[0], lx, ly;
        if (se.p) { lx = se.p[se.p.length - 1][0]; ly = se.p[se.p.length - 1][1]; } else { var rr = se.r[se.r.length - 1]; lx = rr[1]; ly = rr[2]; }
        svg.appendChild(s('path', {d: se.d + 'L' + lx + ' ' + B + 'L' + fx + ' ' + B + 'Z', fill: 'url(#' + id + ')', stroke: 'none', class: 'ln-area'}));
      }
      svg.appendChild(s('path', {d: se.d, fill: 'none', stroke: se.c, 'stroke-width': Math.max(se.w, 2.8), 'stroke-linejoin': 'round', 'stroke-linecap': 'round', class: 'ln-p', pathLength: 1}));
    });
    var lastx, lasty, lastc = base.c;
    if (base.p) { base.p.forEach(function (p) { hov.push({x: p[0], y: p[1], t: p[2]}); }); var lp = base.p[base.p.length - 1]; lastx = lp[0]; lasty = lp[1]; }
    else { var rr2 = base.r[base.r.length - 1]; lastx = rr2[1]; lasty = rr2[2]; }
    sp.series.forEach(function (se) { if (se !== base) lastc = se.c; });
    svg.appendChild(s('circle', {cx: lastx, cy: lasty, r: 9, fill: lastc, class: 'ln-halo'}));
    svg.appendChild(s('circle', {cx: lastx, cy: lasty, r: 4.6, fill: lastc, class: 'ln-end'}));
    sp.ann.forEach(function (a) { var tx = s('text', {x: a[0], y: a[1], 'text-anchor': a[3], class: 'ln-a', 'font-size': Math.max(a[5], 12)}); tx.setAttribute('fill', a[4]); tx.textContent = a[2]; svg.appendChild(tx); });
    var cross = s('line', {y1: T, y2: B, class: 'ln-c'}), dot = s('circle', {r: 6, class: 'ln-hd'});
    svg.appendChild(cross); svg.appendChild(dot);
    wrap.appendChild(svg); wrap.appendChild(tip); box.appendChild(wrap);
    var show = function (ev) {
      var r = svg.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width * W, hx, hy, label = '', t;
      if (base.p) { var best = hov[0]; hov.forEach(function (p) { if (Math.abs(p.x - x) < Math.abs(best.x - x)) best = p; }); hx = best.x; hy = best.y; t = best.t; var i = hov.indexOf(best); label = sp.xl[i] ? sp.xl[i][1] : ''; }
      else { var run = base.r[0]; base.r.forEach(function (q) { if (q[0] <= x + 0.01) run = q; }); hx = Math.max(run[0], Math.min(run[1], x)); hy = run[2]; t = run[3]; }
      cross.setAttribute('x1', hx); cross.setAttribute('x2', hx); cross.style.opacity = 1;
      dot.setAttribute('cx', hx); dot.setAttribute('cy', hy); dot.setAttribute('fill', base.c); dot.style.opacity = 1;
      tip.innerHTML = ''; if (label) tip.appendChild(h('span', '', label)); tip.appendChild(h('b', '', t));
      tip.classList.add('on');
      var px = hx / W * r.width, tw = tip.offsetWidth;
      tip.style.left = Math.max(0, Math.min(r.width - tw, px - tw / 2)) + 'px'; tip.style.top = Math.max(0, hy / H * r.height - 48) + 'px';
    };
    var hide = function () { cross.style.opacity = 0; dot.style.opacity = 0; tip.classList.remove('on'); };
    svg.addEventListener('pointermove', show); svg.addEventListener('pointerdown', show); svg.addEventListener('pointerleave', hide);
  }

  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('play'); io.unobserve(e.target); } });
  }, {threshold: 0.2}) : null;

  els.forEach(function (el) {
    try {
      var sp = JSON.parse(el.getAttribute('data-spec')), fb = el.querySelector('.ic-fallback'), box = h('div', 'ic-body');
      if (sp.k === 'h') hbars(sp, box); else if (sp.k === 'v') vbars(sp, box); else if (sp.k === 'l') line(sp, box); else return;
      el.insertBefore(box, fb); fb.hidden = true; el.classList.add('ready', 'ic-' + sp.k);
      if (io) io.observe(el); else el.classList.add('play');
    } catch (e) { /* keep the static SVG */ }
  });
})();
