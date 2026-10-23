import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const root = new URL('..', import.meta.url);
const project = 'projects/holyiot-25008-enclosure/source';
const editorData = `${project}/editor/src/cap-editor/data`;
const fix = "run 'pnpm sync:data' in projects/holyiot-25008-enclosure/source/editor";

test('editor data copies are byte-identical to the generator sources', () => {
  const pairs = [
    [`${editorData}/catalog.json`, `${project}/cad/catalog.json`],
    [`${editorData}/layout.json`, `${project}/cad/out/layout.json`],
  ] as const;
  for (const [copy, source] of pairs) {
    const editorBytes = readFileSync(new URL(copy, root));
    const sourceBytes = readFileSync(new URL(source, root));
    assert.ok(editorBytes.equals(sourceBytes), `${copy} differs from ${source}; ${fix}`);
  }
});

test('every catalog icon has a non-empty path in the editor layout', () => {
  const catalog = JSON.parse(readFileSync(new URL(`${project}/cad/catalog.json`, root), 'utf8'));
  const layout = JSON.parse(readFileSync(new URL(`${editorData}/layout.json`, root), 'utf8'));
  const missing = catalog.icons
    .filter((icon: { id: string }) => typeof layout.icons[icon.id] !== 'string' || layout.icons[icon.id].length === 0)
    .map((icon: { id: string }) => icon.id);
  assert.equal(missing.length, 0, `icons without a non-empty path in ${editorData}/layout.json: ${missing.join(', ')}; ${fix}`);
});
