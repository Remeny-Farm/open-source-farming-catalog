#!/usr/bin/env node
// Validates every projects/<id>/ directory. Exit code 1 on any problem.
import { fileURLToPath } from 'node:url';
import { validateCatalog } from './lib/validate-catalog.ts';

const root = fileURLToPath(new URL('..', import.meta.url));
const { projects, errors } = await validateCatalog(root);
for (const error of errors) console.error(`x ${error}`);
if (errors.length) {
  console.error(`${errors.length} problem(s) in ${projects.length} parsed project(s)`);
  process.exit(1);
}
console.log(`ok ${projects.length} project(s): ${projects.map(p => `${p.id} (${p.stage}, ${p.version})`).join(', ')}`);
