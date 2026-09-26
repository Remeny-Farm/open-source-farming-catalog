// "I built this" report, one file per build under projects/<id>/builds/<yyyy-mm-dd>-<slug>.json.
import { z } from 'zod';
import { personSchema, photoSchema } from './project.ts';

export const buildFilePattern = /^(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.json$/;

export const buildSchema = z.object({
  schemaVersion: z.literal(1),
  date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  builder: personSchema,
  // The project version that was built, as written in project.json at the time.
  projectVersion: z.string().min(1).optional(),
  // At least one language; the reviewer may add the other.
  notes: z.object({ hu: z.string().min(1).optional(), en: z.string().min(1).optional() }).strict()
    .refine(n => n.hu || n.en, 'notes need hu or en'),
  photo: photoSchema.optional(),
}).strict();

export type Build = z.infer<typeof buildSchema>;
