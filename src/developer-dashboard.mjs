export const developerDashboardHtml = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Transcript API developer dashboard · SaveFromNet</title>
<link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
<style>
:root{font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:#162024;background:#f8f7f1}*{box-sizing:border-box}body{margin:0}a{color:#087f68}header{border-bottom:1px solid #e5e7e0;background:#fff}nav{max-width:1050px;margin:auto;padding:17px 24px;display:flex;align-items:center;justify-content:space-between;gap:20px}nav a:first-child{font-weight:850;color:#162024;text-decoration:none;font-size:20px;letter-spacing:-.05em}main{max-width:1050px;margin:auto;padding:60px 24px 100px}h1{font-size:clamp(34px,6vw,64px);line-height:1.04;letter-spacing:-.065em;margin:6px 0 18px}h2{letter-spacing:-.04em;margin-top:0}.lead{color:#657277;font-size:18px;line-height:1.6;max-width:680px}.tag{color:#008263;font-size:12px;letter-spacing:.16em;font-weight:800;text-transform:uppercase}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:34px}.card{background:#fff;border:1px solid #e0e6df;border-radius:20px;padding:28px;box-shadow:0 15px 40px #1c302c0b}.wide{grid-column:1/-1}.price{font-size:46px;font-weight:850;letter-spacing:-.06em}.muted{color:#667579;line-height:1.6}button{border:0;border-radius:10px;background:#f56249;color:#fff;padding:13px 18px;font:inherit;font-weight:750;cursor:pointer}button:hover{background:#db503a}button:disabled{opacity:.5;cursor:not-allowed}.secondary{background:#e9f5ef;color:#006c54}.secondary:hover{background:#d4eddf}input{width:100%;border:1px solid #c8d6ce;border-radius:10px;padding:13px 14px;font:inherit;min-width:0}form{display:flex;gap:10px}.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}code,pre{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#132426;color:#d1f7e8;border-radius:12px;padding:18px;line-height:1.5}output{display:block;overflow-wrap:anywhere;color:#00634d;background:#e9f5ef;padding:14px;border-radius:10px;margin-top:15px}#message{min-height:24px;color:#9a3f2d;margin-top:16px}#account{display:none}.meter{height:12px;background:#e5eee8;border-radius:99px;overflow:hidden}.meter span{display:block;height:100%;background:#1bab83;width:0}.number{font-size:28px;font-weight:800;margin:8px 0 14px}@media(max-width:700px){main{padding-top:35px}.grid{grid-template-columns:1fr}.wide{grid-column:auto}.card{padding:22px}form{flex-direction:column}form button{width:100%}}
</style></head><body><header><nav><a href="/">↓ savefromnet.fun</a><a href="/youtube-transcript-api">API documentation</a></nav></header>
<main><p class="tag">Developers</p><h1>YouTube Transcript API</h1><p class="lead">Retrieve available public YouTube captions as timed JSON. Connect with an API key and track your monthly usage here.</p>
<div class="grid"><section class="card"><h2>Developer plan</h2><div><span class="price">$5</span> / month</div><p class="muted">1,000 successful transcripts per billing period. Failed extraction does not use your allowance. Up to 4 requests per minute and 2 processing requests at once.</p><button id="checkout">Subscribe for $5/month</button><p class="muted" id="availability"></p></section>
<section class="card"><h2>Restore an account</h2><p class="muted">Use the recovery code you saved when you subscribed. Keep it private: it controls your API key.</p><form id="restore"><input id="recovery-input" autocomplete="off" placeholder="Paste recovery code" aria-label="Recovery code" required><button type="submit" class="secondary">Restore</button></form></section>
<section class="card wide" id="account"><p class="tag">Your account</p><h2 id="account-status">Loading</h2><p class="muted" id="period"></p><div class="number" id="usage"></div><div class="meter" aria-label="Monthly usage"><span id="usage-bar"></span></div><p class="muted">The API key is shown only when created or rotated. Rotating it immediately invalidates the old key.</p><div class="row"><button id="key" class="secondary">Create / rotate API key</button><button id="recovery" class="secondary">Show recovery code</button><button id="billing" class="secondary">Manage billing / cancel</button></div><output id="secret" hidden></output></section>
<section class="card wide"><h2>Make a request</h2><p class="muted">Send one public YouTube watch, Shorts, or youtu.be URL. Only available caption tracks can be returned; this API does not run speech recognition.</p><pre>curl -X POST https://savefromnet.fun/api/v2/youtube/transcript \\\n+  -H 'Authorization: Bearer YOUR_API_KEY' \\\n+  -H 'Content-Type: application/json' \\\n+  -d '{"url":"https://www.youtube.com/watch?v=VIDEO_ID","language":"en"}'</pre><p class="muted">A successful JSON response includes title, author, language, available languages, and timestamped segments. Invalid links, missing captions, and restricted videos return an error. <a href="/youtube-transcript-api">Read the API documentation</a>.</p></section></div><p id="message" role="status"></p></main>
<script>
'use strict';
const $ = id => document.getElementById(id);
const message = value => { $('message').textContent = value || ''; };
async function send(path, body) {
  const response = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify(body || {}) });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || 'Request failed. Please try again.');
  return data;
}
async function refresh() {
  const response = await fetch('/api/developer/status', { credentials: 'same-origin', cache: 'no-store' });
  const data = await response.json();
  $('checkout').disabled = !data.available || data.active;
  $('availability').textContent = data.available ? (data.active ? 'Your subscription is active.' : 'Checkout is ready.') : 'Checkout is being configured. The public caption preview remains available.';
  $('account').style.display = data.status === 'signed_out' ? 'none' : 'block';
  if (data.status !== 'signed_out') {
    $('account-status').textContent = data.active ? 'Subscription active' : data.status === 'pending' ? 'Awaiting payment confirmation' : 'Subscription ' + data.status;
    $('period').textContent = data.periodEnd ? 'Current period ends ' + new Date(data.periodEnd).toLocaleString() : 'Your billing period will appear after payment.';
    $('usage').textContent = (data.used || 0) + ' / ' + data.limit + ' successful transcripts';
    $('usage-bar').style.width = Math.min(100, (data.used || 0) / data.limit * 100) + '%';
    $('key').disabled = !data.active;
    $('key').textContent = data.hasKey ? 'Rotate API key' : 'Create API key';
    $('billing').disabled = data.status === 'pending';
  }
}
$('checkout').addEventListener('click', async () => { try { message('Starting secure checkout…'); const data = await send('/api/developer/checkout'); location.assign(data.checkoutUrl); } catch(error) { message(error.message); } });
$('restore').addEventListener('submit', async event => { event.preventDefault(); try { await send('/api/developer/redeem', { code: $('recovery-input').value.trim() }); $('recovery-input').value = ''; $('secret').hidden = true; message('Account restored.'); await refresh(); } catch(error) { message(error.message); } });
$('key').addEventListener('click', async () => { if ($('key').textContent.includes('Rotate') && !confirm('Rotate the API key? Your old key will stop working immediately.')) return; try { const data = await send('/api/developer/key'); $('secret').hidden = false; $('secret').textContent = 'Save this API key now. It will not be shown again: ' + data.apiKey; message('API key created.'); await refresh(); } catch(error) { message(error.message); } });
$('recovery').addEventListener('click', async () => { try { const data = await send('/api/developer/recovery'); $('secret').hidden = false; $('secret').textContent = 'Save this recovery code securely: ' + data.recoveryCode; } catch(error) { message(error.message); } });
$('billing').addEventListener('click', async () => { try { message('Opening billing portal…'); const data = await send('/api/developer/portal'); location.assign(data.portalUrl); } catch(error) { message(error.message); } });
if (new URL(location.href).searchParams.get('checkout') === 'returned') message('Checkout returned. Payment confirmation may take a few minutes.');
refresh().catch(() => message('Could not load account status. Try refreshing.'));
</script></body></html>`;
