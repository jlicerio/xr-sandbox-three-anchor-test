import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import test from 'node:test';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const comparisonPage = resolve(root, 'public/dev/three-anchor/index.html');
const page = readFileSync(comparisonPage, 'utf8');

 test('comparison page exposes separate MindAR and 8th Wall scanner modes', () => {
  assert.match(page, /engine=mindar/);
  assert.match(page, /engine=8thwall/);
});

test('both engines load the same three static target images', () => {
  for (let index = 1; index <= 3; index += 1) {
    const imagePath = resolve(root, `public/dev/three-anchor/targets/anchor-${index}.png`);
    assert.ok(existsSync(imagePath), `missing shared image target ${index}`);
  }
  assert.match(page, /targets\/anchor-\$\{target\.index \+ 1\}\.png/);
});

test('8th Wall target files and licensed engine assets exist locally', () => {
  for (let index = 1; index <= 3; index += 1) {
    assert.ok(existsSync(resolve(root, `public/dev/three-anchor/8thwall/anchor-${index}.json`)));
  }
  assert.ok(existsSync(resolve(root, 'public/dev/three-anchor/vendor/8thwall/xr.js')));
  assert.ok(existsSync(resolve(root, 'public/dev/three-anchor/vendor/8thwall/LICENSE')));
});
