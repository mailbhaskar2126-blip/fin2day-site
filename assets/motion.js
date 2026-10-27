/* FIN2DAY motion layer: smooth scroll, split-text reveals, chart draw-in + hover readouts,
   counters, hero parallax, card tilt, scroll-linked panels, nav hover pill, hide-on-scroll header.
   Everything is skipped for visitors with "reduce motion" switched on. Content is never changed. */
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;
  var root = document.documentElement;

  /* ---------- Chart readouts (work even with reduced motion) ---------- */
  var tip = document.createElement('div');
  tip.className = 'tip'; tip.setAttribute('role', 'status'); tip.setAttribute('aria-live', 'polite');
  document.body.appendChild(tip);
  function showTip(label, value, x, y) {
    tip.innerHTML = '';
    if (label) { var a = document.createElement('span'); a.textContent = label; tip.appendChild(a); }
    if (value) { var b = document.createElement('b'); b.textContent = value; tip.appendChild(b); }
    tip.classList.add('on');
    var w = tip.offsetWidth, h = tip.offsetHeight;
    var left = Math.min(Math.max(8, x - w / 2), innerWidth - w - 8);
    var top = y - h - 14; if (top < 8) top = y + 18;
    tip.style.transform = 'translate(' + left + 'px,' + top + 'px)';
  }
  function hideTip() { tip.classList.remove('on'); }

  function num(el, attr) { return parseFloat(el.getAttribute(attr)) || 0; }
  function texts(svg) {
    return Array.prototype.map.call(svg.querySelectorAll('text'), function (t) {
      return { el: t, x: num(t, 'x'), y: num(t, 'y'), s: t.textContent.trim(),
        mono: /Mono/.test(t.getAttribute('font-family') || ''), bold: t.getAttribute('font-weight') === '700',
        end: t.getAttribute('text-anchor') === 'end', mid: t.getAttribute('text-anchor') === 'middle' };
    });
  }

  // Work out what each chart is from the shapes inside it.
  function analyse(svg) {
    var vb = (svg.getAttribute('viewBox') || '0 0 460 230').split(/[\s,]+/).map(Number);
    var rects = Array.prototype.slice.call(svg.querySelectorAll('rect'));
    var circles = Array.prototype.slice.call(svg.querySelectorAll('circle'));
    var tx = texts(svg);
    var info = { svg: svg, w: vb[2], h: vb[3], kind: 'other', items: [] };
    var nameLabels = tx.filter(function (t) { return t.end && !t.mono; });
    var isFlow = rects.length && rects.every(function (r) { return r.getAttribute('stroke-width') === '1.3'; });
    if (isFlow) { info.kind = 'flow'; info.items = rects; return info; }
    if (rects.length && nameLabels.length && rects.every(function (r) { return num(r, 'height') === 18; })) {
      info.kind = 'hbars';
      var vline = svg.querySelector('line');
      var zero = vline && vline.getAttribute('x1') === vline.getAttribute('x2') ? num(vline, 'x1') : Math.min.apply(null, rects.map(function (r) { return num(r, 'x'); }));
      info.items = rects.map(function (r) {
        var y = num(r, 'y'), x = num(r, 'x');
        var name = nameLabels.filter(function (t) { return Math.abs(t.y - (y + 13)) < 5; })[0];
        var val = tx.filter(function (t) { return t.mono && t.bold && Math.abs(t.y - (y + 14)) < 5; })[0];
        return { el: r, origin: x + 1 < zero ? 'right' : 'left', key: y + 9, label: name && name.s, value: val && val.s, valEl: val && val.el,
          tip: r.getAttribute('data-tip') };
      });
      return info;
    }
    var hline = Array.prototype.filter.call(svg.querySelectorAll('line'), function (l) { return l.getAttribute('y1') === l.getAttribute('y2') && l.getAttribute('stroke') === 'var(--ink)'; })[0];
    var barRects = rects.filter(function (r) { return !r.getAttribute('opacity') && !/rule|paper|soft/.test(r.getAttribute('fill') || '') && num(r, 'width') <= 60; });
    if (hline && barRects.length >= 2 && !svg.querySelector('polyline')) {
      info.kind = 'vbars';
      var zy = num(hline, 'y1');
      info.items = barRects.map(function (r) {
        var cx = num(r, 'x') + num(r, 'width') / 2, y = num(r, 'y');
        var val = tx.filter(function (t) { return t.mono && t.bold && Math.abs(t.x - cx) < 3; })[0];
        var xl = tx.filter(function (t) { return t.mono && !t.bold && Math.abs(t.x - cx) < 3; })[0];
        return { el: r, origin: y + 1 < zy ? 'bottom' : 'top', key: cx, label: xl && xl.s, value: val && val.s, valEl: val && val.el,
          tip: r.getAttribute('data-tip') };
      });
      return info;
    }
    if (circles.length >= 2) {
      info.kind = 'line';
      var xlabels = tx.filter(function (t) { return t.mono && t.mid; });
      var annots = tx.filter(function (t) { return t.bold; });
      info.items = circles.map(function (c) {
        var cx = num(c, 'cx'), cy = num(c, 'cy');
        var xl = xlabels.filter(function (t) { return Math.abs(t.x - cx) < 6; })[0];
        var an = annots.filter(function (t) { return Math.abs(t.x - cx) < 34 && Math.abs(t.y - cy) < 22; })
          .sort(function (a, b) { return (Math.abs(a.x - cx) + Math.abs(a.y - cy)) - (Math.abs(b.x - cx) + Math.abs(b.y - cy)); })[0];
        var dt = c.getAttribute('data-tip');
        return { el: c, key: cx, cy: cy, label: xl && xl.s, value: dt || (an && an.s), tip: null };
      });
      return info;
    }
    if (svg.querySelector('path[stroke-width="2.4"]')) info.kind = 'steps';
    return info;
  }

  function attachReadout(info) {
    var svg = info.svg, items = info.items.filter(function (it) { return it.label || it.value || it.tip; });
    if (!items.length || !/bars|line/.test(info.kind)) return;
    svg.classList.add('interactive');
    var guide;
    if (info.kind === 'line') {
      guide = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      guide.setAttribute('class', 'guide'); guide.setAttribute('y1', 14); guide.setAttribute('y2', info.h - 26);
      svg.insertBefore(guide, svg.firstChild.nextSibling || null);
    }
    var current = null;
    function pick(e) {
      var pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
      var m = svg.getScreenCTM(); if (!m) return null; var p = pt.matrixTransform(m.inverse());
      var axis = info.kind === 'hbars' ? p.y : p.x, best = null, d = 1e9;
      items.forEach(function (it) { var dd = Math.abs(it.key - axis); if (dd < d) { d = dd; best = it; } });
      return best;
    }
    function on(e) {
      var it = pick(e); if (!it) return;
      if (it !== current) {
        if (current) { current.el.classList.remove('hot'); if (current.valEl) current.valEl.classList.remove('hot'); }
        current = it; it.el.classList.add('hot'); if (it.valEl) it.valEl.classList.add('hot'); svg.classList.add('focus');
        if (guide) { guide.setAttribute('x1', it.key); guide.setAttribute('x2', it.key); }
      }
      var r = it.el.getBoundingClientRect();
      var label = it.tip ? '' : it.label, value = it.tip || it.value;
      if (info.kind === 'line' && !value) value = '';
      showTip(label, value, r.left + r.width / 2, r.top - (info.kind === 'line' ? 22 : 0));
    }
    function off() { if (current) { current.el.classList.remove('hot'); if (current.valEl) current.valEl.classList.remove('hot'); } current = null; svg.classList.remove('focus'); hideTip(); }
    svg.addEventListener('pointermove', on);
    svg.addEventListener('pointerdown', on);
    svg.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') off(); });
    document.addEventListener('pointerdown', function (e) { if (current && !svg.contains(e.target)) off(); });
    window.addEventListener('scroll', function () { if (current) off(); }, { passive: true });
  }

  var charts = Array.prototype.map.call(document.querySelectorAll('.chart:not(.ready) svg'), analyse);
  charts.forEach(attachReadout);
  // Chart cards that sit inside a link: let the link work on click, readouts on hover only.

  if (reduce) { root.classList.add('still'); return; }
  root.classList.add('moving');

  /* ---------- Smooth scroll ---------- */
  var lenis = null;
  if (window.Lenis && fine) {
    lenis = new Lenis({ duration: 1.15, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); }, smoothWheel: true });
    var raf = function (t) { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href*="#"]');
      if (!a) return;
      var url = new URL(a.href, location.href);
      if (url.pathname !== location.pathname || !url.hash || url.hash.length < 2) return;
      var t = document.getElementById(url.hash.slice(1)); if (!t) return;
      e.preventDefault(); lenis.scrollTo(t, { offset: -90 });
      if (history.pushState) history.pushState(null, '', url.hash);
    });
    if (location.hash && document.getElementById(location.hash.slice(1))) {
      setTimeout(function () { lenis.scrollTo(document.getElementById(location.hash.slice(1)), { offset: -90, immediate: true }); }, 60);
    }
  }

  /* ---------- Split headings into words that rise in ---------- */
  function split(el) {
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), nodes = [], n;
    while ((n = walker.nextNode())) nodes.push(n);
    var i = 0;
    nodes.forEach(function (node) {
      var parts = node.textContent.split(/(\s+)/), frag = document.createDocumentFragment();
      parts.forEach(function (p) {
        if (!p) return;
        if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
        var o = document.createElement('span'); o.className = 'wo';
        var w = document.createElement('span'); w.className = 'wi'; w.style.transitionDelay = (i++ * 45) + 'ms';
        w.textContent = p; o.appendChild(w); frag.appendChild(o);
      });
      node.parentNode.replaceChild(frag, node);
    });
    el.classList.add('words');
  }
  var heads = document.querySelectorAll('.hero h1, .shead h2, .center h2, .how h2, .ctap h2, .page-head h1, .article-head h1');
  heads.forEach(function (h) { h.classList.remove('reveal', 'd1', 'd2', 'd3'); split(h); });

  /* ---------- Chart draw-in ---------- */
  function prep(info) {
    var svg = info.svg;
    svg.classList.add('anim');
    Array.prototype.forEach.call(svg.querySelectorAll('polyline, path'), function (p) {
      if (p.getAttribute('fill') && p.getAttribute('fill') !== 'none') return;
      try { var L = p.getTotalLength(); p.style.strokeDasharray = L + ' ' + L; p.style.strokeDashoffset = L; p.classList.add('draw'); } catch (e) {}
    });
    if (info.kind === 'hbars' || info.kind === 'vbars') {
      info.items.forEach(function (it, i) {
        it.el.classList.add('grow', 'o-' + it.origin); it.el.style.transitionDelay = (120 + i * 70) + 'ms';
        if (it.valEl) { it.valEl.classList.add('late'); it.valEl.style.transitionDelay = (520 + i * 70) + 'ms'; }
      });
    } else if (info.kind === 'line') {
      info.items.forEach(function (it, i) { it.el.classList.add('pop'); it.el.style.transitionDelay = (300 + i * 90) + 'ms'; });
    } else if (info.kind === 'flow') {
      info.items.forEach(function (r, i) { r.classList.add('late'); r.style.transitionDelay = (i * 120) + 'ms'; });
    }
    Array.prototype.forEach.call(svg.querySelectorAll('text'), function (t) { if (!t.classList.contains('late')) t.classList.add('soft'); });
  }
  charts.forEach(prep);

  /* ---------- Count-up numbers ---------- */
  function countUp(el) {
    var txt = el.textContent, m = txt.match(/[\d,]+(\.\d+)?/);
    if (!m) return;
    var target = parseFloat(m[0].replace(/,/g, '')), dec = m[1] ? m[1].length - 1 : 0, commas = m[0].indexOf(',') > -1;
    if (!target) return;
    var start = performance.now(), dur = 1400, from = target * (target > 50 ? 0.82 : 0);
    function fmt(v) {
      var s = v.toFixed(dec);
      if (commas) { var p = s.split('.'); p[0] = Number(p[0]).toLocaleString('en-IN'); s = p.join('.'); }
      return s;
    }
    var first = el.firstChild;
    if (!first || first.nodeType !== 3) return;
    var lead = first.textContent;
    (function step(now) {
      var k = Math.min(1, (now - start) / dur), e = 1 - Math.pow(1 - k, 4);
      first.textContent = lead.replace(m[0], k < 1 ? fmt(from + (target - from) * e) : m[0]);
      if (k < 1) requestAnimationFrame(step);
    })(start);
  }

  /* ---------- One observer for everything that plays on arrival ---------- */
  var watch = document.querySelectorAll('.words, .chart svg.anim, .stat .n, .float strong, .u');
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) {
      if (!en.isIntersecting) return;
      var t = en.target; t.classList.add('play'); io.unobserve(t);
      if (t.matches('.stat .n, .float strong')) countUp(t);
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.2 });
  watch.forEach(function (el) { io.observe(el); });

  /* ---------- Hero: pointer parallax ---------- */
  var collage = document.querySelector('.collage');
  if (collage && fine) {
    var main = collage.querySelector('.main'), fl = collage.querySelectorAll('.float');
    collage.addEventListener('pointermove', function (e) {
      var r = collage.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      main.style.transform = 'perspective(1000px) rotateY(' + (x * 6) + 'deg) rotateX(' + (-y * 6) + 'deg)';
      fl.forEach(function (f, i) { f.style.translate = (x * (i ? -26 : 22)) + 'px ' + (y * (i ? -18 : 16)) + 'px'; });
    });
    collage.addEventListener('pointerleave', function () { main.style.transform = ''; fl.forEach(function (f) { f.style.translate = ''; }); });
  }

  /* ---------- Card tilt ---------- */
  if (fine) {
    document.querySelectorAll('.story, .bx, .mini, .stat').forEach(function (c) {
      c.addEventListener('pointermove', function (e) {
        var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        c.style.setProperty('--rx', (-y * 3) + 'deg'); c.style.setProperty('--ry', (x * 3) + 'deg');
        c.style.setProperty('--mx', ((x + .5) * 100) + '%'); c.style.setProperty('--my', ((y + .5) * 100) + '%');
        c.classList.add('tilting');
      });
      c.addEventListener('pointerleave', function () { c.classList.remove('tilting'); c.style.removeProperty('--rx'); c.style.removeProperty('--ry'); });
    });
  }

  /* ---------- Nav hover pill ---------- */
  var nav = document.querySelector('.nav');
  if (nav && fine) {
    var blob = document.createElement('span'); blob.className = 'blob'; nav.appendChild(blob);
    var links = nav.querySelectorAll('a:not(.btn)');
    function moveTo(a) {
      if (!a) { blob.style.opacity = 0; return; }
      blob.style.opacity = 1; blob.style.width = a.offsetWidth + 'px'; blob.style.transform = 'translateX(' + a.offsetLeft + 'px)';
    }
    var cur = nav.querySelector('a[aria-current="page"]');
    links.forEach(function (a) { a.addEventListener('pointerenter', function () { moveTo(a); }); });
    nav.addEventListener('pointerleave', function () { moveTo(cur); });
    nav.classList.add('has-blob');
    requestAnimationFrame(function () { blob.style.transition = 'none'; moveTo(cur); requestAnimationFrame(function () { blob.style.transition = ''; }); });
  }

  /* ---------- Scroll-linked: header, beat panels, tiles ---------- */
  var mast = document.querySelector('.mast'), lastY = 0;
  var par = Array.prototype.slice.call(document.querySelectorAll('.svc .vis, .tile, .ctap .vis .mail'));
  var ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (mast) {
      mast.classList.toggle('scrolled', y > 10);
      if (y > 400 && y > lastY + 4 && !(nav && nav.classList.contains('open'))) mast.classList.add('away');
      else if (y < lastY - 4 || y < 400) mast.classList.remove('away');
    }
    lastY = y;
    par.forEach(function (el, i) {
      var r = el.getBoundingClientRect(); if (r.bottom < -200 || r.top > innerHeight + 200) return;
      var c = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
      var amt = el.classList.contains('tile') ? (i % 2 ? 60 : -40) : el.classList.contains('mail') ? 30 : 36;
      el.style.translate = '0 ' + (c * amt).toFixed(1) + 'px';
    });
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
})();
