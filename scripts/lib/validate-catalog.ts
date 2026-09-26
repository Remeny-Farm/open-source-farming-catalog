// Catalogue validation beyond the JSON contract: directory layout, served files and their
// hashes, photo files and dimensions, required READMEs, BOM shape and build reports.
// Erasable TypeScript only (Node runs this file with type stripping).
import { createHash } from 'node:crypto';
import { readdir, readFile, stat } from 'node:fs/promises';
import { join } from 'node:path';
import { projectSchema, maxFileBytes, type Photo, type Project } from '../../schema/project.ts';
import { buildSchema, buildFilePattern } from '../../schema/build.ts';

export const bomHeader = 'ref,qty,item_hu,item_en,source,notes';
export const heroSuffix = '-1200.webp';
export const thumbSuffix = '-600.webp';
const readmeStages = new Set(['built', 'field-tested']);

export interface CatalogResult { projects: Project[]; errors: string[] }
type Fail = (message: string) => void;

export async function validateCatalog(root: string): Promise<CatalogResult> {
  const errors: string[] = [];
  const projects: Project[] = [];
  const projectsDir = join(root, 'projects');
  const dirs = (await readdir(projectsDir, { withFileTypes: true })).filter(e => e.isDirectory()).map(e => e.name).sort();
  for (const dir of dirs) {
    const base = join(projectsDir, dir);
    const fail: Fail = message => errors.push(`${dir}: ${message}`);
    let raw: unknown;
    try { raw = JSON.parse(await readFile(join(base, 'project.json'), 'utf8')); }
    catch (error) { fail(`project.json unreadable: ${(error as Error).message}`); continue; }
    const parsed = projectSchema.safeParse(raw);
    if (!parsed.success) {
      for (const issue of parsed.error.issues) fail(`project.json ${issue.path.join('.') || '(root)'}: ${issue.message}`);
      continue;
    }
    const project = parsed.data;
    if (project.id !== dir) fail(`id "${project.id}" must equal the directory name`);
    for (const file of project.files ?? []) {
      const info = await fileInfo(join(base, file.path));
      if (!info) { fail(`files: ${file.path} is missing`); continue; }
      if (info.size > maxFileBytes) fail(`files: ${file.path} is ${info.size} bytes, above the ${maxFileBytes}-byte limit`);
      if (info.sha256 !== file.sha256) fail(`files: ${file.path} sha256 is ${info.sha256}, not ${file.sha256}`);
    }
    const photos: Array<[string, Photo]> = [];
    if (project.photo) photos.push(['photo', project.photo]);
    project.gallery?.forEach((photo, i) => photos.push([`gallery.${i}`, photo]));
    for (const [label, photo] of photos) await checkPhoto(base, label, photo, fail);
    if (readmeStages.has(project.stage)) {
      for (const lang of ['hu', 'en']) if (!(await nonEmpty(join(base, `README.${lang}.md`)))) fail(`README.${lang}.md is required for stage ${project.stage}`);
    }
    await checkBom(base, fail);
    await checkBuilds(base, fail);
    projects.push(project);
  }
  if (new Set(projects.map(p => p.id)).size !== projects.length) errors.push('duplicate project ids');
  return { projects, errors };
}

async function fileInfo(path: string): Promise<{ size: number; sha256: string } | undefined> {
  try {
    const info = await stat(path);
    if (!info.isFile()) return undefined;
    const sha256 = createHash('sha256').update(await readFile(path)).digest('hex');
    return { size: info.size, sha256 };
  } catch { return undefined; }
}

async function nonEmpty(path: string): Promise<boolean> {
  try { return (await readFile(path, 'utf8')).trim().length > 0; } catch { return false; }
}

async function checkPhoto(base: string, label: string, photo: Photo, fail: Fail): Promise<void> {
  if (!photo.src.endsWith(heroSuffix)) { fail(`${label}: src must end with ${heroSuffix} (the platform derives the ${thumbSuffix} variant name from it)`); return; }
  const hero = await readWebp(join(base, photo.src));
  if (!hero) { fail(`${label}: ${photo.src} is missing or not a WebP file`); return; }
  if (hero.width !== photo.width || hero.height !== photo.height) fail(`${label}: ${photo.src} is ${hero.width}x${hero.height}, project.json says ${photo.width}x${photo.height}`);
  const thumbSrc = photo.src.slice(0, -heroSuffix.length) + thumbSuffix;
  const thumb = await readWebp(join(base, thumbSrc));
  if (!thumb) fail(`${label}: ${thumbSrc} is missing`);
  else if (thumb.width * 2 !== hero.width || thumb.height * 2 !== hero.height) fail(`${label}: ${thumbSrc} is ${thumb.width}x${thumb.height}, expected half of ${hero.width}x${hero.height}`);
}

async function readWebp(path: string): Promise<{ width: number; height: number } | undefined> {
  try { return webpDimensions(await readFile(path)); } catch { return undefined; }
}

// RIFF/WEBP header parser for the three container variants; no image library needed.
export function webpDimensions(buf: Uint8Array): { width: number; height: number } | undefined {
  const view = Buffer.from(buf.buffer, buf.byteOffset, buf.byteLength);
  if (view.length < 30 || view.toString('ascii', 0, 4) !== 'RIFF' || view.toString('ascii', 8, 12) !== 'WEBP') return undefined;
  const chunk = view.toString('ascii', 12, 16);
  if (chunk === 'VP8 ') {
    if (view[23] !== 0x9d || view[24] !== 0x01 || view[25] !== 0x2a) return undefined;
    return { width: view.readUInt16LE(26) & 0x3fff, height: view.readUInt16LE(28) & 0x3fff };
  }
  if (chunk === 'VP8L') {
    if (view[20] !== 0x2f) return undefined;
    const b0 = view[21], b1 = view[22], b2 = view[23], b3 = view[24];
    return { width: 1 + (((b1 & 0x3f) << 8) | b0), height: 1 + (((b3 & 0x0f) << 10) | (b2 << 2) | ((b1 & 0xc0) >> 6)) };
  }
  if (chunk === 'VP8X') return { width: 1 + view.readUIntLE(24, 3), height: 1 + view.readUIntLE(27, 3) };
  return undefined;
}

export function parseCsvLine(line: string): string[] {
  const out: string[] = [];
  let cur = '';
  let quoted = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (quoted) {
      if (ch === '"') { if (line[i + 1] === '"') { cur += '"'; i++; } else quoted = false; }
      else cur += ch;
    } else if (ch === '"') quoted = true;
    else if (ch === ',') { out.push(cur); cur = ''; }
    else cur += ch;
  }
  out.push(cur);
  return out;
}

async function checkBom(base: string, fail: Fail): Promise<void> {
  let text: string;
  try { text = await readFile(join(base, 'bom.csv'), 'utf8'); } catch { return; }
  const lines = text.split(/\r?\n/).filter(line => line.trim());
  if (lines[0] !== bomHeader) { fail(`bom.csv: header must be "${bomHeader}"`); return; }
  const columns = bomHeader.split(',').length;
  lines.slice(1).forEach((line, i) => {
    const cells = parseCsvLine(line);
    if (cells.length !== columns) { fail(`bom.csv row ${i + 2}: ${cells.length} columns, expected ${columns}`); return; }
    const [ref, qty, itemHu, itemEn] = cells;
    if (!ref.trim() || !qty.trim() || !itemHu.trim() || !itemEn.trim()) fail(`bom.csv row ${i + 2}: ref, qty, item_hu and item_en are required`);
  });
}

async function checkBuilds(base: string, fail: Fail): Promise<void> {
  let names: string[];
  try { names = (await readdir(join(base, 'builds'))).filter(name => name.endsWith('.json')).sort(); } catch { return; }
  for (const name of names) {
    const match = buildFilePattern.exec(name);
    if (!match) { fail(`builds/${name}: file name must be <yyyy-mm-dd>-<slug>.json`); continue; }
    let raw: unknown;
    try { raw = JSON.parse(await readFile(join(base, 'builds', name), 'utf8')); }
    catch (error) { fail(`builds/${name}: unreadable: ${(error as Error).message}`); continue; }
    const parsed = buildSchema.safeParse(raw);
    if (!parsed.success) { for (const issue of parsed.error.issues) fail(`builds/${name} ${issue.path.join('.') || '(root)'}: ${issue.message}`); continue; }
    if (parsed.data.date !== match[1]) fail(`builds/${name}: date ${parsed.data.date} does not match the file name`);
    if (parsed.data.photo) await checkPhoto(base, `builds/${name} photo`, parsed.data.photo, fail);
  }
}
