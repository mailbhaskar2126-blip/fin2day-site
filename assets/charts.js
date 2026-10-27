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
    var wrap = h('div', 'vb'); wrap.style.height = H + 'px';
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
    var L = 46, R = W - 12, T = 18, B = H - 30;
    sp.yt.forEach(function (t) {
      svg.appendChild(s('line', {x1: L, x2: R, y1: t[0], y2: t[0], class: 'ln-g'}));
      var tx = s('text', {x: 2, y: t[0] + 4, class: 'ln-y'}); tx.textContent = t[1]; svg.appendChild(tx);
    });
    sp.xl.forEach(function (t) { var tx = s('text', {x: t[0], y: H - 8, class: 'ln-x', 'text-anchor': 'middle'}); tx.textContent = t[1]; svg.appendChild(tx); });
    var pts = [];
    sp.series.forEach(function (se, si) {
      var d = se.p.map(function (p, i) { return (i ? 'L' : 'M') + p[0] + ' ' + p[1]; }).join('');
      var id = 'ica' + Math.random().toString(36).slice(2, 7);
      var gr = s('linearGradient', {id: id, x1: 0, x2: 0, y1: 0, y2: 1});
      gr.appendChild(s('stop', {offset: '0%', 'stop-color': se.c, 'stop-opacity': '.20'}));
      gr.appendChild(s('stop', {offset: '100%', 'stop-color': se.c, 'stop-opacity': '0'}));
      var defs = s('defs', {}); defs.appendChild(gr); svg.appendChild(defs);
      if (sp.series.length === 1) svg.appendChild(s('path', {d: d + 'L' + se.p[se.p.length - 1][0] + ' ' + B + 'L' + se.p[0][0] + ' ' + B + 'Z', fill: 'url(#' + id + ')', class: 'ln-area'}));
      var path = s('path', {d: d, fill: 'none', stroke: se.c, 'stroke-width': 2.6, 'stroke-linejoin': 'round', 'stroke-linecap': 'round', class: 'ln-p', pathLength: 1});
      svg.appendChild(path);
      var last = se.p[se.p.length - 1];
      svg.appendChild(s('circle', {cx: last[0], cy: last[1], r: 8, fill: se.c, opacity: '.18', class: 'ln-halo'}));
      svg.appendChild(s('circle', {cx: last[0], cy: last[1], r: 4.2, fill: se.c, class: 'ln-end'}));
      se.p.forEach(function (p) { pts.push({x: p[0], y: p[1], t: p[2], c: se.c, i: pts.length, l: sp.xl[pts.length] ? sp.xl[pts.length][1] : ''}); });
    });
    sp.ann.forEach(function (a) { var tx = s('text', {x: a[0], y: a[1], 'text-anchor': a[3], class: 'ln-a'}); tx.setAttribute('fill', a[4]); tx.textContent = a[2]; svg.appendChild(tx); });
    var cross = s('line', {y1: T, y2: B, class: 'ln-c', opacity: 0}), dot = s('circle', {r: 5.5, class: 'ln-hd', opacity: 0});
    svg.appendChild(cross); svg.appendChild(dot);
    wrap.appendChild(svg); wrap.appendChild(tip); box.appendChild(wrap);
    var show = function (ev) {
      var r = svg.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width * W, best = pts[0];
      pts.forEach(function (p) { if (Math.abs(p.x - x) < Math.abs(best.x - x)) best = p; });
      cross.setAttribute('x1', best.x); cross.setAttribute('x2', best.x); cross.setAttribute('opacity', 1);
      dot.setAttribute('cx', best.x); dot.setAttribute('cy', best.y); dot.setAttribute('fill', best.c); dot.setAttribute('opacity', 1);
      tip.innerHTML = ''; if (best.l) tip.appendChild(h('span', '', best.l)); tip.appendChild(h('b', '', best.t));
      tip.classList.add('on');
      var px = best.x / W * r.width, tw = tip.offsetWidth;
      tip.style.left = Math.max(0, Math.min(r.width - tw, px - tw / 2)) + 'px'; tip.style.top = Math.max(0, best.y / H * r.height - 46) + 'px';
    };
    var hide = function () { cross.setAttribute('opacity', 0); dot.setAttribute('opacity', 0); tip.classList.remove('on'); };
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
