#!/usr/bin/env node
// Checks a release tag "<project-id>/<version>" against projects/<id>/project.json and
// prints ID=... and VERSION=... lines for the release workflow to append to $GITHUB_ENV.
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const tag = process.argv[2];
const slash = tag?.indexOf('/') ?? -1;
if (!tag || slash <= 0 || slash === tag.length - 1) {
  console.error('usage: node scripts/release-check.mjs <project-id>/<version>');
  process.exit(2);
}
const id = tag.slice(0, slash);
const version = tag.slice(slash + 1);
const root = fileURLToPath(new URL('..', import.meta.url));
const project = JSON.parse(await readFile(join(root, 'projects', id, 'project.json'), 'utf8'));
if (project.version !== version) {
  console.error(`project.json version "${project.version}" does not match tag version "${version}"`);
  process.exit(1);
}
console.log(`ID=${id}\nVERSION=${version}`);
