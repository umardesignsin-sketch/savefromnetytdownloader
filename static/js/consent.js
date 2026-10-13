// Cookie consent for Google Analytics. UK, EU and EEA visitors see a choice and
// the tag loads only after they accept. Elsewhere it loads unless the visitor has
// rejected it through Cookie settings. Essential cookies are not affected.
(() => {
  const GA_ID = 'G-L1G52YY7TJ';
  const CHOICE_KEY = 'sfn-cookie-consent-v1';
  const REGION_KEY = 'sfn-consent-required';
  const TEXT = {
    en: {
      label: 'Cookie consent',
      body: 'We would like to use Google Analytics cookies to understand how people use SaveFromNet. They stay off unless you accept. Cookies that make downloads work are always on.',
      accept: 'Accept analytics', reject: 'Reject', privacy: 'Privacy policy', settings: 'Cookie settings',
    },
    es: {
      label: 'Consentimiento de cookies',
      body: 'Queremos usar cookies de Google Analytics para entender cómo se usa SaveFromNet. Están desactivadas salvo que las aceptes. Las cookies necesarias para las descargas siempre están activas.',
      accept: 'Aceptar analítica', reject: 'Rechazar', privacy: 'Política de privacidad', settings: 'Configuración de cookies',
    },
    fr: {
      label: 'Consentement aux cookies',
      body: 'Nous aimerions utiliser les cookies de Google Analytics pour comprendre comment SaveFromNet est utilisé. Ils restent désactivés sauf si vous les acceptez. Les cookies nécessaires aux téléchargements sont toujours actifs.',
      accept: "Accepter l'analyse", reject: 'Refuser', privacy: 'Politique de confidentialité', settings: 'Paramètres des cookies',
    },
  };
  const text = TEXT[(document.documentElement.lang || 'en').slice(0, 2)] || TEXT.en;

  const storage = (area) => ({
    get(key) { try { return window[area].getItem(key); } catch { return null; } },
    set(key, value) { try { window[area].setItem(key, value); } catch { /* private mode: ask again next time */ } },
  });
  const local = storage('localStorage');
  const session = storage('sessionStorage');

  let analyticsLoaded = false;
  function loadAnalytics() {
    if (analyticsLoaded) return;
    analyticsLoaded = true;
    window[`ga-disable-${GA_ID}`] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function gtag() { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
    document.head.append(script);
  }

  function removeAnalyticsCookies() {
    window[`ga-disable-${GA_ID}`] = true;
    const host = location.hostname;
    const domains = ['', host, `.${host}`, `.${host.split('.').slice(-2).join('.')}`];
    for (const part of document.cookie.split(';')) {
      const name = part.split('=')[0].trim();
      if (!/^(_ga(_.*)?|_gid|_gat.*)$/.test(name)) continue;
      for (const domain of domains) {
        document.cookie = `${name}=; Max-Age=0; path=/${domain ? `; domain=${domain}` : ''}`;
      }
    }
  }

  function addStyles() {
    if (document.getElementById('cookie-banner-style')) return;
    const style = document.createElement('style');
    style.id = 'cookie-banner-style';
    style.textContent = '.cookie-banner{position:fixed;left:16px;right:16px;bottom:16px;z-index:1000;max-width:720px;margin:0 auto;padding:18px 20px;border:1px solid #d6e2da;border-radius:16px;background:#fff;color:#1d2a24;box-shadow:0 18px 50px rgba(16,43,31,.22);font:inherit}'
      + '.cookie-banner p{margin:0 0 14px;line-height:1.5;font-size:.95rem}'
      + '.cookie-banner a{color:#215e36;font-weight:700}'
      + '.cookie-actions{display:flex;flex-wrap:wrap;gap:10px}'
      + '.cookie-actions button{flex:1 1 160px;min-height:44px;border:0;border-radius:10px;font:inherit;font-weight:750;cursor:pointer;color:#fff}'
      + '.cookie-actions .cookie-accept{background:#23854b}.cookie-actions .cookie-reject{background:#24302b}'
      + '.cookie-actions button:focus-visible,.cookie-banner a:focus-visible{outline:3px solid #78bc8b;outline-offset:2px}'
      + '.cookie-settings-link{background:none;border:0;padding:0;font:inherit;color:inherit;text-decoration:underline;cursor:pointer}';
    document.head.append(style);
  }

  function hideBanner() {
    document.getElementById('cookie-banner')?.remove();
  }

  function decide(choice) {
    local.set(CHOICE_KEY, choice);
    hideBanner();
    if (choice === 'granted') loadAnalytics();
    else removeAnalyticsCookies();
  }

  function showBanner() {
    if (document.getElementById('cookie-banner')) return;
    addStyles();
    const banner = document.createElement('section');
    banner.id = 'cookie-banner';
    banner.className = 'cookie-banner';
    banner.setAttribute('aria-label', text.label);
    const body = document.createElement('p');
    body.append(`${text.body} `);
    const link = document.createElement('a');
    link.href = '/privacy-policy';
    link.textContent = text.privacy;
    body.append(link);
    const actions = document.createElement('div');
    actions.className = 'cookie-actions';
    for (const [choice, label, className] of [['granted', text.accept, 'cookie-accept'], ['denied', text.reject, 'cookie-reject']]) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = className;
      button.textContent = label;
      button.addEventListener('click', () => decide(choice));
      actions.append(button);
    }
    banner.append(body, actions);
    document.body.append(banner);
  }

  async function consentRequired() {
    const cached = session.get(REGION_KEY);
    if (cached === '1' || cached === '0') return cached === '1';
    try {
      const response = await fetch('/api/consent-region', { cache: 'no-store', credentials: 'same-origin' });
      if (!response.ok) throw new Error(String(response.status));
      const required = (await response.json()).required !== false;
      session.set(REGION_KEY, required ? '1' : '0');
      return required;
    } catch {
      return true; // when the region is unknown, ask rather than assume
    }
  }

  function bindSettingsLinks() {
    addStyles();
    for (const button of document.querySelectorAll('[data-cookie-settings]')) {
      button.textContent = text.settings;
      button.addEventListener('click', showBanner);
    }
  }

  async function start() {
    bindSettingsLinks();
    const choice = local.get(CHOICE_KEY);
    if (choice === 'granted') return loadAnalytics();
    if (choice === 'denied') return removeAnalyticsCookies();
    if (await consentRequired()) showBanner();
    else loadAnalytics();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
