import test from 'node:test';
import assert from 'node:assert/strict';
import redirect from '../src/www-redirect.mjs';

test('www redirects permanently to HTTPS apex while preserving path and query', () => {
  const response = redirect.fetch(new Request('http://www.savefromnet.fun/youtube-to-mp3?source=share'));
  assert.equal(response.status, 301);
  assert.equal(response.headers.get('location'), 'https://savefromnet.fun/youtube-to-mp3?source=share');
});

test('plain HTTP apex redirects permanently to HTTPS while preserving path and query', () => {
  const response = redirect.fetch(new Request('http://savefromnet.fun/youtube-to-mp3?source=share'));
  assert.equal(response.status, 301);
  assert.equal(response.headers.get('location'), 'https://savefromnet.fun/youtube-to-mp3?source=share');
});

test('HTTPS apex is not redirected by the redirect Worker', () => {
  const response = redirect.fetch(new Request('https://savefromnet.fun/youtube-to-mp3'));
  assert.equal(response.status, 404);
});

test('redirect worker does not redirect unrelated hosts', () => {
  const response = redirect.fetch(new Request('https://other.example/youtube-to-mp3'));
  assert.equal(response.status, 404);
});
