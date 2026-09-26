// Project contract, schema version 2. Single source of truth for the catalogue and the
// platform (which re-exports it); /api/v1/project.schema.json is derived from it.
// Erasable TypeScript only (Node runs this file with type stripping).
import { z } from 'zod';

export const schemaVersion = 2;
export const stages = ['concept', 'prototype', 'built', 'field-tested'] as const;
export const categories = ['mechanical', 'electronics', 'firmware', 'mixed'] as const;
// Problem areas. Extend with a pull request; every value needs HU and EN labels on the platform.
export const topics = ['poultry', 'livestock', 'water', 'fencing', 'soil', 'tools', 'sensors', 'energy', 'storage'] as const;
// What a builder needs. 'none' means hand tools only.
export const requirements = ['3d-printer', 'soldering', 'welding', 'woodworking', 'microcontroller-flashing', 'none'] as const;
export const linkKinds = ['printables', 'repository', 'discussion', 'mirror', 'video'] as const;
export const fileRoles = ['source', 'export', 'documentation', 'bom', 'evidence'] as const;
// Served files must fit Cloudflare Workers static assets (25 MiB) with margin.
export const maxFileBytes = 20 * 1024 * 1024;

export const idPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
export const localized = z.object({ hu: z.string().min(1), en: z.string().min(1) }).strict();
// Relative to projects/<id>/; no leading slash, no parent traversal.
export const relativePath = z.string().regex(/^(?!\/)(?!.*(?:^|\/)\.\.(?:\/|$))[a-zA-Z0-9_.\/-]+$/);
export const httpsUrl = z.url({ protocol: /^https$/ });
export const photoSchema = z.object({
  src: relativePath,
  width: z.number().int().positive(),
  height: z.number().int().positive(),
  alt: localized,
}).strict();
export const personSchema = z.object({ name: z.string().min(1), url: httpsUrl.optional() }).strict();
const contributorSchema = z.object({ name: z.string().min(1), url: httpsUrl.optional(), role: z.string().min(1).optional() }).strict();

export const projectSchema = z.object({
  schemaVersion: z.literal(schemaVersion),
  id: z.string().regex(idPattern),
  title: localized,
  description: localized,
  category: z.enum(categories),
  stage: z.enum(stages),
  version: z.string().min(1),
  topics: z.array(z.enum(topics)).min(1),
  requires: z.array(z.enum(requirements)).min(1),
  maintainers: z.array(personSchema).min(1),
  contributors: z.array(contributorSchema).min(1).optional(),
  // A licence without a path covers the whole project, including linked files.
  // A licence with a path covers that file or directory (relative to projects/<id>/).
  licenses: z.array(z.object({ path: relativePath.optional(), identifier: z.string().min(1) }).strict()).min(1),
  // Files the platform serves at /projects/<id>/<path>. Paths are relative to projects/<id>/.
  files: z.array(z.object({ path: relativePath, sha256: z.string().regex(/^[a-f0-9]{64}$/), role: z.enum(fileRoles) }).strict()).min(1).optional(),
  // External locations: mirrors such as Printables, upstream repositories, discussion threads.
  links: z.array(z.object({ kind: z.enum(linkKinds), url: httpsUrl }).strict()).min(1).optional(),
  photo: photoSchema.optional(),
  gallery: z.array(photoSchema).min(1).optional(),
  derivedFrom: z.array(z.object({ id: z.string().regex(idPattern).optional(), url: httpsUrl.optional(), note: localized.optional() }).strict()
    .refine(d => d.id || d.url, 'derivedFrom needs an id or a url')).min(1).optional(),
  limitations: localized,
}).strict().refine(p => p.files || p.links, 'A project needs served files or download links');

export type Project = z.infer<typeof projectSchema>;
export type Photo = z.infer<typeof photoSchema>;
export const projectJsonSchema = z.toJSONSchema(projectSchema);

export function validateProjects(input: unknown): Project[] {
  const values = z.array(projectSchema).parse(input);
  if (new Set(values.map(p => p.id)).size !== values.length) throw new Error('Duplicate project ID');
  return values;
}
