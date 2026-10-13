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
  // Netlify strips data-netlify from the served HTML, so match our forms by class.
  var SUCCESS = {
    newsletter: 'You\u2019re on the list! We\u2019ll email you when the daily brief starts.',
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
      fetch('/', {method: 'POST', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, body: encode(form)})
        .then(function (r) {
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
