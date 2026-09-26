#!/usr/bin/env node
// Derives the served photo pair from an original: <id>-1200.webp (1200x900) and <id>-600.webp (600x450),
// centre-cropped to 4:3, metadata stripped, plus a provenance sidecar next to each.
// Usage: node scripts/photo.mjs <project-id> <original image> --by "Name" [--name <basename>] [--date YYYY-MM-DD]
import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const args = process.argv.slice(2);
const [id, original] = args;
const option = name => { const i = args.indexOf(`--${name}`); return i >= 0 ? args[i + 1] : undefined; };
const by = option('by');
if (!id || !original || !by) {
  console.error('usage: node scripts/photo.mjs <project-id> <original image> --by "Name" [--name <basename>] [--date YYYY-MM-DD]');
  process.exit(2);
}
const basename = option('name') ?? id;
const date = option('date') ?? new Date().toISOString().slice(0, 10);
const dir = join(fileURLToPath(new URL('..', import.meta.url)), 'projects', id, 'photos');
await mkdir(dir, { recursive: true });
const provenance = `Photo supplied by ${by}, ${date}; cropped 4:3 and re-encoded, metadata stripped.`;
for (const width of [1200, 600]) {
  const target = join(dir, `${basename}-${width}.webp`);
  await sharp(original).rotate().resize(width, width * 3 / 4, { fit: 'cover', position: 'centre' }).webp({ quality: 82 }).toFile(target);
  await writeFile(`${target}.json`, JSON.stringify({ provenance, createdAt: new Date().toISOString() }, null, 2) + '\n');
  console.log(`wrote ${target}`);
}
console.log(`project.json photo: { "src": "photos/${basename}-1200.webp", "width": 1200, "height": 900, "alt": { "hu": "...", "en": "..." } }`);
