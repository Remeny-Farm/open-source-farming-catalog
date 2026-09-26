#!/usr/bin/env node
// Prints project.json "files" entries for the given paths.
// Usage: node scripts/hash.mjs <project-id> <role> <path relative to projects/<id>/>...
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { fileRoles } from '../schema/project.ts';

const [id, role, ...paths] = process.argv.slice(2);
if (!id || !fileRoles.includes(role) || paths.length === 0) {
  console.error(`usage: node scripts/hash.mjs <project-id> <${fileRoles.join('|')}> <path>...`);
  process.exit(2);
}
const base = join(fileURLToPath(new URL('..', import.meta.url)), 'projects', id);
const entries = [];
for (const path of paths) {
  const sha256 = createHash('sha256').update(await readFile(join(base, path))).digest('hex');
  entries.push({ path, sha256, role });
}
console.log(JSON.stringify(entries, null, 2));
