import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdtemp, rm, mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { validateCatalog, webpDimensions, parseCsvLine, bomHeader } from '../scripts/lib/validate-catalog.ts';

function makeVp8(w: number, h: number): Buffer {
  const b = Buffer.alloc(34);
  b.write('RIFF', 0); b.writeUInt32LE(26, 4); b.write('WEBP', 8); b.write('VP8 ', 12);
  b.set([0, 0, 0, 0x9d, 0x01, 0x2a], 20);
  b.writeUInt16LE(w, 26); b.writeUInt16LE(h, 28);
  return b;
}

function makeVp8l(w: number, h: number): Buffer {
  const b = Buffer.alloc(32);
  b.write('RIFF', 0); b.write('WEBP', 8); b.write('VP8L', 12);
  b[20] = 0x2f;
  b.writeUInt32LE((w - 1) | ((h - 1) << 14), 21);
  return b;
}

function makeVp8x(w: number, h: number): Buffer {
  const b = Buffer.alloc(32);
  b.write('RIFF', 0); b.write('WEBP', 8); b.write('VP8X', 12);
  b.writeUIntLE(w - 1, 24, 3);
  b.writeUIntLE(h - 1, 27, 3);
  return b;
}

const latchBytes = Buffer.from('solid latch\nendsolid latch\n');
const latchSha = createHash('sha256').update(latchBytes).digest('hex');

function baseProject(overrides: Record<string, unknown> = {}) {
  return {
    schemaVersion: 2,
    id: 'sample-latch',
    title: { hu: 'Példa retesz', en: 'Sample latch' },
    description: { hu: 'Leírás.', en: 'Description.' },
    category: 'mechanical',
    stage: 'prototype',
    version: '0.1.0',
    topics: ['poultry'],
    requires: ['3d-printer'],
    maintainers: [{ name: 'Tester' }],
    licenses: [{ identifier: 'CC-BY-SA-4.0' }],
    files: [{ path: 'export/latch.stl', sha256: latchSha, role: 'export' }],
    limitations: { hu: 'Csak teszt.', en: 'Test only.' },
    ...overrides,
  };
}

async function withCatalog(fn: (root: string) => Promise<void>) {
  const root = await mkdtemp(join(tmpdir(), 'catalog-'));
  await mkdir(join(root, 'projects'), { recursive: true });
  try {
    await fn(root);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
}

async function setupProject(root: string, id = 'sample-latch', json: unknown = baseProject()) {
  const dir = join(root, 'projects', id);
  await mkdir(join(dir, 'export'), { recursive: true });
  await writeFile(join(dir, 'export', 'latch.stl'), latchBytes);
  if (json !== null) await writeFile(join(dir, 'project.json'), typeof json === 'string' ? json : JSON.stringify(json));
  return dir;
}

test('webpDimensions parses lossy VP8 buffer', () => {
  assert.deepEqual(webpDimensions(makeVp8(1200, 900)), { width: 1200, height: 900 });
});

test('webpDimensions parses lossless VP8L buffer', () => {
  assert.deepEqual(webpDimensions(makeVp8l(800, 600)), { width: 800, height: 600 });
});

test('webpDimensions parses extended VP8X buffer', () => {
  assert.deepEqual(webpDimensions(makeVp8x(1920, 1080)), { width: 1920, height: 1080 });
});

test('webpDimensions returns undefined for invalid buffers', () => {
  assert.equal(webpDimensions(Buffer.alloc(20)), undefined);
  assert.equal(webpDimensions(Buffer.from('RIFF1234NOTWVP8 ')), undefined);
  const badSig = makeVp8(100, 100); badSig[23] = 0x00;
  assert.equal(webpDimensions(badSig), undefined);
  const badVp8l = makeVp8l(100, 100); badVp8l[20] = 0x00;
  assert.equal(webpDimensions(badVp8l), undefined);
});

test('parseCsvLine splits CSV lines handling quotes and escaped quotes', () => {
  assert.deepEqual(parseCsvLine('a,b,c'), ['a', 'b', 'c']);
  assert.deepEqual(parseCsvLine('r1,1,"item, with comma","has ""quote"""'), ['r1', '1', 'item, with comma', 'has "quote"']);
});

test('validateCatalog succeeds on a valid project', () => withCatalog(async root => {
  await setupProject(root);
  const { projects, errors } = await validateCatalog(root);
  assert.equal(errors.length, 0);
  assert.equal(projects.length, 1);
  assert.equal(projects[0].id, 'sample-latch');
}));

test('validateCatalog detects unreadable project.json', () => withCatalog(async root => {
  await setupProject(root, 'sample-latch', '{ invalid json ');
  const { errors } = await validateCatalog(root);
  assert.ok(errors.some(e => e.includes('project.json unreadable')));
}));

test('validateCatalog detects schema violations in project.json', () => withCatalog(async root => {
  await setupProject(root, 'sample-latch', baseProject({ category: 'invalid-category' }));
  const { errors } = await validateCatalog(root);
  assert.ok(errors.some(e => e.includes('project.json category:')));
}));

test('validateCatalog checks id equals directory name', () => withCatalog(async root => {
  await setupProject(root, 'sample-latch', baseProject({ id: 'wrong-id' }));
  const { errors } = await validateCatalog(root);
  assert.ok(errors.some(e => e.includes('must equal the directory name')));
}));

test('validateCatalog checks files[] existence and sha256 mismatch', () => withCatalog(async root => {
  await setupProject(root, 'sample-latch', baseProject({
    files: [
      { path: 'export/missing.stl', sha256: latchSha, role: 'export' },
      { path: 'export/latch.stl', sha256: '0'.repeat(64), role: 'export' },
    ],
  }));
  const { errors } = await validateCatalog(root);
  assert.ok(errors.some(e => e.includes('export/missing.stl is missing')));
  assert.ok(errors.some(e => e.includes('export/latch.stl sha256 is')));
}));

test('validateCatalog checks photo suffix, missing file, and dimensions', () => withCatalog(async root => {
  const dir = await setupProject(root, 'sample-latch', baseProject({
    photo: { src: 'photos/latch.webp', width: 1200, height: 900, alt: { hu: 'A', en: 'A' } },
  }));
  let res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('src must end with')));

  await writeFile(join(dir, 'project.json'), JSON.stringify(baseProject({
    photo: { src: 'photos/latch-1200.webp', width: 1200, height: 900, alt: { hu: 'A', en: 'A' } },
  })));
  res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('is missing or not a WebP file')));

  await mkdir(join(dir, 'photos'), { recursive: true });
  await writeFile(join(dir, 'photos', 'latch-1200.webp'), makeVp8(1000, 900));
  res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('project.json says')));
}));

test('validateCatalog checks thumbnail sibling existence and half dimensions', () => withCatalog(async root => {
  const dir = await setupProject(root, 'sample-latch', baseProject({
    photo: { src: 'photos/latch-1200.webp', width: 1200, height: 900, alt: { hu: 'A', en: 'A' } },
  }));
  await mkdir(join(dir, 'photos'), { recursive: true });
  await writeFile(join(dir, 'photos', 'latch-1200.webp'), makeVp8(1200, 900));
  let res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('photos/latch-600.webp is missing')));

  await writeFile(join(dir, 'photos', 'latch-600.webp'), makeVp8(500, 450));
  res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('expected half of')));

  await writeFile(join(dir, 'photos', 'latch-600.webp'), makeVp8(600, 450));
  res = await validateCatalog(root);
  assert.equal(res.errors.length, 0);
}));

test('validateCatalog requires hu and en READMEs for built stage', () => withCatalog(async root => {
  const dir = await setupProject(root, 'sample-latch', baseProject({ stage: 'built' }));
  let res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('README.hu.md is required for stage built')));
  assert.ok(res.errors.some(e => e.includes('README.en.md is required for stage built')));

  await writeFile(join(dir, 'README.hu.md'), 'Leírás');
  await writeFile(join(dir, 'README.en.md'), '   ');
  res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('README.en.md is required for stage built')));
  assert.ok(!res.errors.some(e => e.includes('README.hu.md')));

  await writeFile(join(dir, 'README.en.md'), 'Description');
  res = await validateCatalog(root);
  assert.equal(res.errors.length, 0);
}));

test('validateCatalog validates bom.csv header, columns, and required fields', () => withCatalog(async root => {
  const dir = await setupProject(root);
  await writeFile(join(dir, 'bom.csv'), 'bad,header\n');
  let res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('header must be')));

  await writeFile(join(dir, 'bom.csv'), `${bomHeader}\nr1,1,hu,en,src\n`);
  res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('columns, expected 6')));

  await writeFile(join(dir, 'bom.csv'), `${bomHeader}\n,1,hu,en,src,note\n`);
  res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('ref, qty, item_hu and item_en are required')));

  await writeFile(join(dir, 'bom.csv'), `${bomHeader}\nr1,1,hu,en,src,note\n`);
  res = await validateCatalog(root);
  assert.equal(res.errors.length, 0);
}));

test('validateCatalog validates build reports filename, schema, and date match', () => withCatalog(async root => {
  const dir = await setupProject(root);
  const buildsDir = join(dir, 'builds');
  await mkdir(buildsDir, { recursive: true });

  await writeFile(join(buildsDir, 'badname.json'), '{}');
  let res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('file name must be')));
  await rm(join(buildsDir, 'badname.json'));

  const validBuild = { schemaVersion: 1, date: '2026-05-01', builder: { name: 'Builder' }, notes: { en: 'Built fine' } };
  await writeFile(join(buildsDir, '2026-05-01-build.json'), JSON.stringify({ ...validBuild, schemaVersion: 2 }));
  res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('builds/2026-05-01-build.json schemaVersion:')));

  await writeFile(join(buildsDir, '2026-05-01-build.json'), JSON.stringify({ ...validBuild, date: '2026-05-02' }));
  res = await validateCatalog(root);
  assert.ok(res.errors.some(e => e.includes('does not match the file name')));

  await writeFile(join(buildsDir, '2026-05-01-build.json'), JSON.stringify(validBuild));
  res = await validateCatalog(root);
  assert.equal(res.errors.length, 0);
}));
