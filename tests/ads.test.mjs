import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const template = readFileSync(new URL('../templates/sponsor_section.html', import.meta.url), 'utf8');
const bannerScript = template.match(/<div class="sponsor-banner-slot">\s*<script>([\s\S]*?)<\/script>/)?.[1];

test('responsive banner selects one supplied size without loading a hidden ad', () => {
  assert.ok(bannerScript);
  const cases = [
    [1280, 'c8d671ad1f224dacbc2bd67e33e09aad', 728, 90],
    [700, 'a91b0d1b09ac06b7865ce5291520f233', 468, 60],
    [390, 'f310906e903f96b502db30668f3d2381', 320, 50],
    [320, null, 0, 0],
  ];
  for (const [viewport, key, width, height] of cases) {
    const banner = { hidden: false };
    const slot = { style: {}, parentElement: banner };
    const writes = [];
    const context = {
      window: { innerWidth: viewport },
      document: { documentElement: { clientWidth: viewport }, currentScript: { parentElement: slot }, write: (value) => writes.push(value) },
    };
    vm.runInNewContext(bannerScript, context);
    if (key === null) {
      assert.equal(banner.hidden, true);
      assert.equal(writes.length, 0);
    } else {
      assert.equal(context.atOptions.key, key);
      assert.equal(context.atOptions.width, width);
      assert.equal(context.atOptions.height, height);
      assert.equal(writes.length, 1);
      assert.match(writes[0], new RegExp(`https://bellnewyork.org/22/${key}`));
      assert.match(writes[0], /<\/script>$/);
    }
  }
});
