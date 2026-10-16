// FIN2DAY site behaviour: menu, live date, Netlify forms, topic filters, share.
(function () {
  // Mobile menu
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? 'Close' : 'Menu';
    });
  }

  // Scroll reveals
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, {rootMargin: '0px 0px -8% 0px', threshold: 0.08});
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }

  // Today's-story banner (dismissible for this visit)
  var news = document.getElementById('news');
  if (news) {
    try { if (sessionStorage.getItem('f2d-news') === news.querySelector('a').getAttribute('href')) news.hidden = true; } catch (e) {}
    news.querySelector('.x').addEventListener('click', function () {
      news.hidden = true;
      try { sessionStorage.setItem('f2d-news', news.querySelector('a').getAttribute('href')); } catch (e) {}
    });
  }

  // Live dateline
  var d = document.getElementById('today');
  if (d) {
    try {
      d.textContent = new Date().toLocaleDateString('en-IN', {weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'});
    } catch (e) {}
  }

  // Netlify forms (newsletter + contact)
  function encode(form) {
    return new URLSearchParams(new FormData(form)).toString();
  }
  // Newsletter signups also go to the FIN2DAY Daily Brief list in Brevo.
  var BREVO_URL = 'https://fd4d0761.sibforms.com/serve/MUIFACI9VykHTjuQVZ4hdoTJZGvPjqOURDK3uERQwFvWqMvhHTJHbZ6s_uxPkBk3xVT2Q0IgLzJ7WUut-DoqavaOhNJ13uoKyTI_KnXwq1NQk1LVkwUso04cIRfThRVtqRY2k8nLYdQavfCYyBV76FcHHDw_PYJtKn6zkKPMKMZyBh3Gb_idabbfBzs5evZ33uFPUVCcEEi8EEd-7A==';
  function toBrevo(form) {
    var bot = form.querySelector('[name="bot-field"]');
    if (bot && bot.value) return Promise.resolve();
    var body = new URLSearchParams({EMAIL: form.querySelector('input[type="email"]').value.trim(), email_address_check: '', locale: 'en', html_type: 'simple'}).toString();
    return fetch(BREVO_URL, {method: 'POST', mode: 'no-cors', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, body: body})
      .catch(function () {});
  }

  // Netlify strips data-netlify from the served HTML, so match our forms by class.
  var SUCCESS = {
    newsletter: 'You\u2019re on the list! Check your inbox (and spam folder) for a welcome email.',
    contact: 'Thanks! Your message is in. We\u2019ll get back to you soon.'
  };
  document.querySelectorAll('form.form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = form.querySelector('.msg');
      var submit = form.querySelector('[type="submit"]');
      var email = form.querySelector('input[type="email"]');
      var required = form.querySelectorAll('[required]');
      if (required.length > 1) {
        for (var i = 0; i < required.length; i++) {
          if (!required[i].value.trim()) {
            msg.className = 'msg err';
            msg.textContent = 'Please fill in every field marked required.';
            required[i].focus();
            return;
          }
        }
      }
      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value.trim())) {
        msg.className = 'msg err';
        msg.textContent = 'Enter a full email address, like name@gmail.com.';
        email.focus();
        return;
      }
      submit.disabled = true;
      var old = submit.textContent;
      submit.textContent = 'Sending…';
      var sends = [fetch('/', {method: 'POST', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, body: encode(form)})];
      if (form.getAttribute('name') === 'newsletter') sends.push(toBrevo(form));
      Promise.all(sends)
        .then(function (res) {
          var r = res[0];
          if (!r.ok) throw new Error(r.status);
          form.reset();
          msg.className = 'msg ok';
          msg.textContent = SUCCESS[form.getAttribute('name')] || 'Thanks! We got it.';
        })
        .catch(function () {
          msg.className = 'msg err';
          msg.textContent = 'That didn’t go through. Check your connection and try again.';
        })
        .finally(function () {
          submit.disabled = false;
          submit.textContent = old;
        });
    });
  });

  // Topic filters on the explainers page
  var chips = document.querySelectorAll('.chip[data-filter]');
  if (chips.length) {
    var stories = document.querySelectorAll('.story[data-topic]');
    var empty = document.getElementById('empty');
    var apply = function (topic) {
      var shown = 0;
      chips.forEach(function (c) { c.setAttribute('aria-pressed', c.dataset.filter === topic ? 'true' : 'false'); });
      stories.forEach(function (s) {
        var match = topic === 'all' || s.dataset.topic.split(' ').indexOf(topic) > -1;
        s.hidden = !match;
        if (match) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    };
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        apply(c.dataset.filter);
        if (history.replaceState) history.replaceState(null, '', c.dataset.filter === 'all' ? location.pathname : '#' + c.dataset.filter);
      });
    });
    var start = (location.hash || '').replace('#', '');
    var valid = Array.prototype.some.call(chips, function (c) { return c.dataset.filter === start; });
    apply(valid ? start : 'all');
  }

  // Share buttons
  document.querySelectorAll('[data-share]').forEach(function (b) {
    b.addEventListener('click', function () {
      var url = location.href.split('#')[0];
      var title = document.title;
      var out = b.parentNode.querySelector('.msg');
      if (b.dataset.share === 'native' && navigator.share) {
        navigator.share({title: title, url: url}).catch(function () {});
        return;
      }
      if (b.dataset.share === 'whatsapp') {
        window.open('https://wa.me/?text=' + encodeURIComponent(title + ' ' + url), '_blank', 'noopener');
        return;
      }
      if (b.dataset.share === 'x') {
        window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(title) + '&url=' + encodeURIComponent(url), '_blank', 'noopener');
        return;
      }
      var done = function () { if (out) { out.className = 'msg ok'; out.textContent = 'Link copied.'; } };
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function () { prompt('Copy this link:', url); });
      else prompt('Copy this link:', url);
    });
  });
  if (!navigator.share) document.querySelectorAll('[data-share="native"]').forEach(function (b) { b.hidden = true; });
})();
