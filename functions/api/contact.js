// Cloudflare Pages Function: receives the contact form and emails it to the FIN2DAY inbox via Brevo.
// Needs two settings in Cloudflare (Settings > Variables and Secrets): BREVO_API_KEY (secret) and CONTACT_TO (the inbox).
export async function onRequestPost({ request, env }) {
  const json = (o, s) => new Response(JSON.stringify(o), { status: s, headers: { 'Content-Type': 'application/json' } });
  let d;
  try { d = await request.json(); } catch (e) { return json({ ok: false }, 400); }
  if (d['bot-field']) return json({ ok: true }, 200); // honeypot: pretend success
  const clean = (v, n) => String(v || '').replace(/[\r\n]+/g, ' ').trim().slice(0, n);
  const name = clean(d.name, 120), email = clean(d.email, 200), type = clean(d.type, 60), message = String(d.message || '').trim().slice(0, 5000);
  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || !message) return json({ ok: false, error: 'invalid' }, 400);
  if (!env.BREVO_API_KEY || !env.CONTACT_TO) return json({ ok: false, error: 'not-configured' }, 503);
  const esc = (s) => s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  const r = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: { 'api-key': env.BREVO_API_KEY, 'Content-Type': 'application/json', accept: 'application/json' },
    body: JSON.stringify({
      sender: { name: 'FIN2DAY website', email: env.CONTACT_FROM || env.CONTACT_TO },
      to: [{ email: env.CONTACT_TO }],
      replyTo: { email, name },
      subject: `FIN2DAY contact: ${type || 'Message'} from ${name}`,
      htmlContent: `<p><b>${esc(name)}</b> (${esc(email)}) wrote about <b>${esc(type)}</b>:</p><p>${esc(message).replace(/\n/g, '<br>')}</p>`
    })
  });
  return r.ok ? json({ ok: true }, 200) : json({ ok: false, error: 'send-failed' }, 502);
}
