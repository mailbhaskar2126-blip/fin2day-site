// FIN2DAY calculators: SIP, EMI, FD/lump sum, inflation. Runs locally; nothing is sent anywhere.
(function () {
  var root = document.querySelector('.calc[data-calc]');
  if (!root) return;
  var kind = root.dataset.calc;
  var out = root.querySelector('.calc-out');
  var fmt = new Intl.NumberFormat('en-IN', {maximumFractionDigits: 0});
  var inr = function (n) { return '₹' + fmt.format(Math.round(n)); };
  var el = function (id) { return document.getElementById(id); };
  var num = function (id) { var v = parseFloat(el(id).value); return isFinite(v) ? v : 0; };

  function bar(a, b, la, lb) {
    var t = a + b || 1, pa = Math.max(0, Math.min(100, a / t * 100));
    return '<div class="sbar" role="img" aria-label="' + la + ' ' + pa.toFixed(0) + '%, ' + lb + ' ' + (100 - pa).toFixed(0) + '%"><i style="width:' + pa + '%"></i></div>' +
      '<div class="sleg"><span><b class="d1"></b>' + la + ' ' + pa.toFixed(0) + '%</span><span><b class="d2"></b>' + lb + ' ' + (100 - pa).toFixed(0) + '%</span></div>';
  }
  function stat(k, v, big) { return '<div class="res' + (big ? ' big' : '') + '"><span class="k">' + k + '</span><span class="v mono">' + v + '</span></div>'; }

  function calc() {
    var P = num('amt'), R = num('rate'), Y = num('yrs'), h = '';
    if (kind === 'sip-calculator') {
      var i = R / 1200, m = Math.round(Y * 12);
      var fv = i === 0 ? P * m : P * ((Math.pow(1 + i, m) - 1) / i) * (1 + i), inv = P * m;
      h = stat('Estimated value', inr(fv), true) + stat('Total invested', inr(inv)) + stat('Estimated gain', inr(fv - inv)) + bar(inv, fv - inv, 'Invested', 'Gain');
    } else if (kind === 'emi-calculator') {
      var r = R / 1200, n = Math.round(Y * 12);
      var emi = r === 0 ? P / n : P * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1), tot = emi * n;
      h = stat('Monthly EMI', inr(emi), true) + stat('Total interest', inr(tot - P)) + stat('Total payment', inr(tot)) + bar(P, tot - P, 'Principal', 'Interest');
    } else if (kind === 'fd-calculator') {
      var k = parseFloat(el('freq').value) || 4;
      var mat = P * Math.pow(1 + R / (100 * k), k * Y);
      h = stat('Maturity value', inr(mat), true) + stat('Amount invested', inr(P)) + stat('Interest earned', inr(mat - P)) + bar(P, mat - P, 'Invested', 'Interest');
    } else if (kind === 'inflation-calculator') {
      var f = Math.pow(1 + R / 100, Y);
      h = stat('Same thing costs in ' + Y + ' yrs', inr(P * f), true) + stat('Price rise', '× ' + f.toFixed(2)) + stat('Today’s money buys only', inr(P / f) + ' worth');
    }
    out.innerHTML = h;
  }

  root.querySelectorAll('input[type=number]').forEach(function (n) {
    var rg = el(n.id + '-r');
    n.addEventListener('input', function () { if (rg) rg.value = n.value; calc(); });
    if (rg) rg.addEventListener('input', function () { n.value = rg.value; calc(); });
  });
  var sel = root.querySelector('select');
  if (sel) sel.addEventListener('change', calc);
  calc();
})();
