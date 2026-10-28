// FIN2DAY interactive charts. Renders .chart.ic[data-spec] from JSON; the original SVG inside stays as the no-JS fallback.
(function () {
  var NS = 'http://www.w3.org/2000/svg';
  var els = document.querySelectorAll('.chart.ic[data-spec]');
  if (!els.length) return;
  var h = function (tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  var s = function (tag, attrs) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); return e; };
  var sign = function (t) { return t.replace(/^-/, '−'); };

  // ---- number helpers (read values out of the label text, so figures always match what the chart shows)
  function num(t) { var m = String(t).replace(/[\u2212\u2013]/g, '-').match(/-?\d[\d,]*\.?\d*/); return m ? parseFloat(m[0].replace(/,/g, '')) : NaN; }
  function decs(t) { var m = String(t).match(/\d\.(\d+)/); return m ? m[1].length : 0; }
  function timey(ls) {
    var re = /\b(19|20)\d\d\b|\bFY\d|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b|\bQ[1-4]\b|\b(Mon|Tue|Wed|Thu|Fri)\b/;
    return ls.length > 1 && ls.filter(function (l) { return re.test(l); }).length >= ls.length * 0.8;
  }
  // change chip: percentage points when both values are percentages, otherwise percent change
  function delta(a, b, ta, tb) {
    var x = num(ta), y = num(tb); if (isNaN(x) || isNaN(y) || x === y) return null;
    var up = y > x, pct = /%/.test(ta) && /%/.test(tb), txt;
    if (pct) txt = Math.abs(y - x).toFixed(Math.max(decs(ta), decs(tb), 1)) + ' pts';
    else { if (x === 0) return null; var c = Math.abs((y - x) / Math.abs(x) * 100); txt = (c >= 100 ? c.toFixed(0) : c.toFixed(1)) + '%'; }
    return {up: up, t: txt};
  }
  function titleOf(a, k) {
    var kick = 'Chart', t = String(a || '');
    if (/^Illustration/i.test(t)) { kick = 'Illustration'; t = t.replace(/^Illustration[:,]?\s*/i, ''); }
    var i = t.search(/:\s|\.\s/);
    if (i > 10) t = t.slice(0, i);
    else if (t.length > 58) { var c = t.search(/,\s/); t = c > 22 && c < 70 ? t.slice(0, c) : t.slice(0, 56).replace(/\s+\S*$/, '') + '\u2026'; }
    if (t.length > 90) t = t.slice(0, 88).replace(/\s+\S*$/, '') + '\u2026';
    return {kick: kick, title: t.charAt(0).toUpperCase() + t.slice(1)};
  }
  function frame(sp, box) {
    var T = titleOf(sp.a, sp.k), head = h('div', 'ic-head'), big = h('div', 'ic-big');
    var kick = h('div', 'ic-kick'); kick.appendChild(h('i')); kick.appendChild(document.createTextNode(T.kick));
    head.appendChild(kick); head.appendChild(h('h4', 'ic-title', T.title));
    if (sp.note) head.appendChild(h('div', 'ic-sub', sp.note));
    var bv = h('b', '', ''), chip = h('span', 'ic-chip'), sm = h('small', '', '');
    big.appendChild(bv); big.appendChild(chip); big.appendChild(sm); head.appendChild(big);
    var foot = h('div', 'ic-foot'), br = h('span', 'ic-brand'); br.appendChild(h('i')); br.appendChild(document.createTextNode('FIN2DAY'));
    foot.appendChild(br); foot.appendChild(h('span', 'ic-hint', 'Hover or tap to explore'));
    var api = {
      set: function (v, label, d, extra) {
        bv.textContent = v; sm.textContent = label || '';
        chip.className = 'ic-chip'; chip.textContent = '';
        if (d) { chip.classList.add(d.up ? 'up' : 'dn'); chip.appendChild(h('i', '', d.up ? '\u25B2' : '\u25BC')); chip.appendChild(document.createTextNode(d.t)); if (extra) chip.appendChild(h('em', '', extra)); }
        else if (extra) { chip.classList.add('nu'); chip.textContent = extra; }
        else chip.classList.add('none');
      }
    };
    box.appendChild(head); box._foot = foot;
    return api;
  }

  // numbers count up when a chart scrolls into view
  function countUp(el) {
    var t = el.getAttribute('data-final') || el.textContent, v = num(t);
    if (isNaN(v) || !document.documentElement.classList.contains('moving')) return;
    var m = t.match(/\d[\d,]*\.?\d*/); if (!m) return;
    var d = decs(m[0]), indian = /\d{1,2},\d{2},\d{3}/.test(m[0]), loc = indian ? 'en-IN' : 'en-US';
    var fmt = function (n) { return n.toLocaleString(loc, {minimumFractionDigits: d, maximumFractionDigits: d}); };
    var pre = t.slice(0, t.indexOf(m[0])), post = t.slice(t.indexOf(m[0]) + m[0].length), mag = Math.abs(v);
    if (fmt(mag) !== m[0]) return;
    var t0 = performance.now(), dur = 900;
    (function tick(now) {
      var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = p >= 1 ? t : pre + fmt(mag * e) + post;
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  }

  // readable text on any bar colour: dark text on light bars, white on dark
  function onColor(el) {
    var m = getComputedStyle(el).backgroundColor.match(/[\d.]+/g) || [0, 0, 0];
    var l = (0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]) / 255;
    return l > 0.62 ? '#171717' : '#fff';
  }

  function hbars(sp, box) {
    var pos = 0, neg = 0;
    sp.rows.forEach(function (r) { if (r.n) neg = Math.max(neg, r.w); else pos = Math.max(pos, r.w); });
    var tot = (pos + neg) || 1, z = neg / tot * 100;
    var wrap = h('div', 'hb'); wrap.setAttribute('role', 'list');
    sp.rows.forEach(function (r, i) {
      var w = r.w / tot * 100, row = h('div', 'hb-row'); row.setAttribute('role', 'listitem'); row.tabIndex = 0;
      row.style.setProperty('--d', (i * 55) + 'ms');
      row.setAttribute('aria-label', r.l + ': ' + sign(r.t));
      row._i = i;
      var lab = h('div', 'hb-l', r.l), track = h('div', 'hb-t');
      if (neg) { var zl = h('i', 'hb-z'); zl.style.left = z + '%'; track.appendChild(zl); }
      var bar = h('div', 'hb-b'); bar.style.backgroundColor = r.c; bar.dataset.c = r.c;
      bar.style.left = (r.n ? z - w : z) + '%'; bar.style.width = Math.max(w, 0.6) + '%';
      bar.style.transformOrigin = r.n ? 'right center' : 'left center';
      var inside = w > 24, v = h('span', 'hb-v', sign(r.t));
      if (inside) { bar.classList.add('in'); bar.appendChild(v); }
      else { v.style.color = r.c; v.style.position = 'absolute'; v.style[r.n ? 'right' : 'left'] = 'calc(100% + 8px)'; bar.appendChild(v); bar.classList.add('out'); }
      track.appendChild(bar); row.appendChild(lab); row.appendChild(track); wrap.appendChild(row);
    });
    // header: biggest bar by default, follows the row under the pointer
    var top = 0; sp.rows.forEach(function (r, i) { if (r.w > sp.rows[top].w) top = i; });
    var api = frame(sp, box), tv = num(sp.rows[top].t);
    var head = function (i) {
      var r = sp.rows[i], x = num(r.t), share = (!isNaN(tv) && tv && !isNaN(x) && i !== top) ? Math.round(Math.abs(x) / Math.abs(tv) * 100) + '% of the top' : null;
      api.set(sign(r.t), (i === top ? 'Largest \u00B7 ' : '') + r.l, null, share);
    };
    head(top);
    wrap.addEventListener('pointerover', function (e) { var rw = e.target.closest && e.target.closest('.hb-row'); if (rw && rw._i != null) head(rw._i); });
    wrap.addEventListener('focusin', function (e) { var rw = e.target.closest && e.target.closest('.hb-row'); if (rw && rw._i != null) head(rw._i); });
    wrap.addEventListener('pointerleave', function () { head(top); });
    box.appendChild(wrap);
    if (sp.note) box.appendChild(h('div', 'ic-note', sp.note));
    box.appendChild(box._foot);
    wrap._count = function () { wrap.querySelectorAll('.hb-v').forEach(countUp); };
    wrap._fit = function () {
      wrap.querySelectorAll('.hb-b').forEach(function (bar) {
        var v = bar.querySelector('.hb-v'); if (!v) return;
        var neg = bar.style.transformOrigin.indexOf('right') === 0;
        bar.classList.remove('in', 'out'); v.style.position = ''; v.style.left = v.style.right = ''; v.style.color = '';
        var fits = bar.clientWidth >= v.offsetWidth + 18;
        if (fits) { bar.classList.add('in'); v.style.color = onColor(bar); }
        else { bar.classList.add('out'); v.style.position = 'absolute'; v.style[neg ? 'right' : 'left'] = 'calc(100% + 8px)'; v.style.color = bar.dataset.c; }
      });
    };
  }

  function vbars(sp, box) {
    var pos = 0, neg = 0;
    sp.rows.forEach(function (r) { if (r.n) neg = Math.max(neg, r.h); else pos = Math.max(pos, r.h); });
    var tot = (pos + neg) || 1, H = 230, padT = 26, padB = 46, area = H - padT - padB;
    var wrap = h('div', 'vb' + (sp.rows.length > 6 ? ' dense' : '')); wrap.style.height = H + 'px';
    var zy = padT + pos / tot * area;
    for (var gi = 1; gi <= 3; gi++) { var gl = h('i', 'vb-g'); gl.style.top = (padT + area * gi / 4 * (pos / tot)) + 'px'; wrap.appendChild(gl); }
    var tip = h('div', 'ln-tip vb-tip'), tm = timey(sp.rows.map(function (r) { return r.l; })), api = frame(sp, box);
    var n0 = sp.rows.length - 1, first = sp.rows[0], last = sp.rows[n0], hi = 0;
    sp.rows.forEach(function (r, i) { if (num(r.t) > num(sp.rows[hi].t) || isNaN(num(sp.rows[hi].t))) hi = i; });
    var head = function (i) {
      var r = sp.rows[i];
      if (tm) api.set(sign(r.t), r.l, i ? delta(0, 0, first.t, r.t) : null, i ? 'since ' + first.l : null);
      else api.set(sign(r.t), (i === hi ? 'Highest \u00B7 ' : '') + r.l, null, null);
    };
    var rest = tm ? n0 : hi; head(rest);
    var base = h('i', 'vb-z'); base.style.top = zy + 'px'; wrap.appendChild(base);
    sp.rows.forEach(function (r, i) {
      var col = h('div', 'vb-c'); col.tabIndex = 0; col.style.setProperty('--d', (i * 60) + 'ms');
      col.setAttribute('aria-label', r.l + ': ' + sign(r.t));
      col._i = i;
      var bh = r.h / tot * area, bar = h('div', 'vb-b'); bar.style.backgroundColor = r.c; bar.style.height = Math.max(bh, 2) + 'px';
      bar.style.top = (r.n ? zy : zy - bh) + 'px'; bar.style.transformOrigin = r.n ? 'center top' : 'center bottom';
      var v = h('span', 'vb-v', sign(r.t)); v.style.color = r.c;
      v.style.top = (r.n ? zy + bh + 4 : zy - bh - 20) + 'px';
      var x = h('span', 'vb-x', r.l); x.style.top = (H - 20) + 'px';
      col.appendChild(bar); col.appendChild(v); col.appendChild(x); wrap.appendChild(col);
      var on = function () {
        head(i); var p = i ? sp.rows[i - 1] : null, d = (tm && p) ? delta(0, 0, p.t, r.t) : null;
        tip.innerHTML = ''; tip.appendChild(h('span', '', r.l)); tip.appendChild(h('b', '', sign(r.t)));
        if (d) tip.appendChild(h('em', d.up ? 'up' : 'dn', (d.up ? '\u25B2 ' : '\u25BC ') + d.t));
        tip.classList.add('on');
        var cr = col.getBoundingClientRect(), wr = wrap.getBoundingClientRect(), tw = tip.offsetWidth;
        tip.style.left = Math.max(0, Math.min(wr.width - tw, cr.left - wr.left + cr.width / 2 - tw / 2)) + 'px';
        tip.style.top = Math.max(0, (r.n ? zy : zy - bh) - 40) + 'px';
      };
      col.addEventListener('pointerenter', on); col.addEventListener('focus', on); col.addEventListener('pointerdown', on);
    });
    wrap.appendChild(tip);
    wrap.addEventListener('pointerleave', function () { tip.classList.remove('on'); head(rest); });
    wrap.addEventListener('focusout', function () { tip.classList.remove('on'); head(rest); });
    box.appendChild(wrap);
    if (sp.note) box.appendChild(h('div', 'ic-note', sp.note));
    box.appendChild(box._foot);
    wrap._count = function () { wrap.querySelectorAll('.vb-v').forEach(countUp); };
  }

  function line(sp, box) {
    var W = sp.W, H = sp.H, wrap = h('div', 'ln'), tip = h('div', 'ln-tip'), api = frame(sp, box);
    var svg = s('svg', {viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': sp.a});
    var xs = sp.xl.map(function (t) { return t[0]; }), L = 46, R = W - 8, T = 14, B = sp.yt.length ? Math.max.apply(null, sp.yt.map(function (t) { return t[0]; })) : H - 30;
    (sp.bands || []).forEach(function (b) { svg.appendChild(s('rect', {x: b[0], y: b[1], width: b[2], height: b[3], fill: b[4], opacity: .09, class: 'ln-band'})); });
    sp.yt.forEach(function (t) {
      svg.appendChild(s('line', {x1: L - 4, x2: W - 6, y1: t[0], y2: t[0], class: 'ln-g'}));
      var tx = s('text', {x: 2, y: t[0] + 4, class: 'ln-y'}); tx.textContent = t[1]; svg.appendChild(tx);
    });
    svg.appendChild(s('line', {x1: L - 4, x2: W - 6, y1: B + 0.5, y2: B + 0.5, class: 'ln-base'}));
    sp.xl.forEach(function (t) { svg.appendChild(s('line', {x1: t[0], x2: t[0], y1: T, y2: B, class: 'ln-vg'})); });
    (sp.refs || []).forEach(function (r) { svg.appendChild(s('line', {x1: L - 4, x2: W - 6, y1: r[0], y2: r[0], stroke: r[1], 'stroke-dasharray': '5 4', 'stroke-width': 1.4, class: 'ln-ref'})); });
    sp.xl.forEach(function (t) { svg.appendChild(s('line', {x1: t[0], x2: t[0], y1: B, y2: B + 5, class: 'ln-tick'})); var tx = s('text', {x: t[0], y: H - 6, class: 'ln-x', 'text-anchor': 'middle'}); tx.textContent = t[1]; svg.appendChild(tx); });
    var base = sp.series[0], hov = [], endp;
    sp.series.forEach(function (se, si) {
      if (si === 0 && sp.series.length >= 1) {
        var id = 'ica' + Math.random().toString(36).slice(2, 7), gr = s('linearGradient', {id: id, x1: 0, x2: 0, y1: 0, y2: 1});
        gr.appendChild(s('stop', {offset: '0%', 'stop-color': se.c, 'stop-opacity': '.3'})); gr.appendChild(s('stop', {offset: '100%', 'stop-color': se.c, 'stop-opacity': '0'}));
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
    // header: last value by default; follows the pointer; change is measured from the first point
    var firstT, lastT, firstL = sp.xl.length ? sp.xl[0][1] : '', lastL = sp.xl.length ? sp.xl[sp.xl.length - 1][1] : '';
    if (base.p) { firstT = base.p[0][2]; lastT = base.p[base.p.length - 1][2]; } else { firstT = base.r[0][3]; lastT = base.r[base.r.length - 1][3]; }
    var rest = function () { api.set(sign(lastT), lastL, delta(0, 0, firstT, lastT), firstL ? 'since ' + firstL : null); };
    rest();
    wrap.appendChild(svg); wrap.appendChild(tip); box.appendChild(wrap); if (sp.note) box.appendChild(h('div', 'ic-note', sp.note)); box.appendChild(box._foot);
    var show = function (ev) {
      var r = svg.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width * W, hx, hy, label = '', t;
      if (base.p) { var best = hov[0]; hov.forEach(function (p) { if (Math.abs(p.x - x) < Math.abs(best.x - x)) best = p; }); hx = best.x; hy = best.y; t = best.t; var i = hov.indexOf(best); label = sp.xl[i] ? sp.xl[i][1] : ''; }
      else { var run = base.r[0]; base.r.forEach(function (q) { if (q[0] <= x + 0.01) run = q; }); hx = Math.max(run[0], Math.min(run[1], x)); hy = run[2]; t = run[3]; }
      cross.setAttribute('x1', hx); cross.setAttribute('x2', hx); cross.style.opacity = 1;
      dot.setAttribute('cx', hx); dot.setAttribute('cy', hy); dot.setAttribute('fill', base.c); dot.style.opacity = 1;
      tip.innerHTML = ''; if (label) tip.appendChild(h('span', '', label)); tip.appendChild(h('b', '', t));
      api.set(sign(t), label, delta(0, 0, firstT, t), firstL ? 'since ' + firstL : null);
      tip.classList.add('on');
      var px = hx / W * r.width, tw = tip.offsetWidth;
      tip.style.left = Math.max(0, Math.min(r.width - tw, px - tw / 2)) + 'px'; tip.style.top = Math.max(0, hy / H * r.height - 48) + 'px';
    };
    var hide = function () { cross.style.opacity = 0; dot.style.opacity = 0; tip.classList.remove('on'); rest(); };
    svg.addEventListener('pointermove', show); svg.addEventListener('pointerdown', show); svg.addEventListener('pointerleave', hide);
  }

  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('play'); io.unobserve(e.target); var w = e.target.querySelector('.hb,.vb'); if (w && w._count) setTimeout(w._count, 250); } });
  }, {threshold: 0.2}) : null;

  els.forEach(function (el) {
    try {
      var sp = JSON.parse(el.getAttribute('data-spec')), fb = el.querySelector('.ic-fallback'), box = h('div', 'ic-body');
      if (sp.k === 'h') hbars(sp, box); else if (sp.k === 'v') vbars(sp, box); else if (sp.k === 'l') line(sp, box); else return;
      el.insertBefore(box, fb); fb.hidden = true; el.classList.add('ready', 'ic-' + sp.k);
      var hb = box.querySelector('.hb'); if (hb && hb._fit) { hb._fit(); window.addEventListener('resize', hb._fit); if (document.fonts && document.fonts.ready) document.fonts.ready.then(hb._fit); }
      if (io) io.observe(el); else el.classList.add('play');
    } catch (e) { /* keep the static SVG */ }
  });
})();
