(() => {
  'use strict';
  const send = kind => {
    if (document.visibilityState !== 'visible') return;
    fetch('/api/visit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ kind }),
      keepalive: true,
      credentials: 'omit',
    }).catch(() => { /* Visitor counts are best-effort and never block the page. */ });
  };
  send('page');
  setInterval(() => send('heartbeat'), 60_000);
})();
