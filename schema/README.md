# schema/

The project and build-report contracts, in Zod 4. Project schema version 2 (`schemaVersion`), build reports version 1.

- `project.ts`: the `project.json` contract, its derived JSON Schema and `validateProjects`.
- `build.ts`: the "I built this" report contract (`projects/<id>/builds/*.json`).

## Consumers

- Here: `scripts/hash.mjs` (`fileRoles`), `scripts/lib/validate-catalog.ts` (`projectSchema`, `maxFileBytes`, `Project`, `Photo`, `buildSchema`, `buildFilePattern`), and `tests/` through it.
- The private platform Remeny-Farm/opensource.remeny.farm mounts this repo as its `content/` submodule and re-exports `project.ts` unchanged (`src/lib/projects.ts`: `export * from '../../content/schema/project.ts'`). It uses `stages`, `validateProjects`, `schemaVersion`, `projectJsonSchema` (served as `/api/v1/project.schema.json`), and in its tests `projectSchema`, `topics`, `requirements` and `linkKinds`. Its build is an Astro server bundle for Cloudflare Workers, and it resolves `zod` from its own dependencies.

A green `validate` check here does not prove the platform still builds: a break shows up only on the platform's content bump PR.

## Public API: keep

From `project.ts`: `schemaVersion`, `stages`, `categories`, `topics`, `requirements`, `linkKinds`, `fileRoles`, `maxFileBytes`, `projectSchema`, `projectJsonSchema`, `validateProjects`, `Project`, `Photo`. From `build.ts`: `buildSchema`, `buildFilePattern`. An export with no consumer in this repo is not dead: the platform may use it.

## Imports

- `schema/` MAY import `zod` and `./*.ts`. It MUST NOT import `node:*` modules, `scripts/`, `tests/` or any other package.
- `scripts/` and `tests/` MAY import `schema/` and `scripts/lib/`.
- Erasable TypeScript only (no `enum`, `namespace` or parameter properties): Node runs these files with type stripping, and there is no build step.

## Changing the contract

- A new `topics`, `requirements` or `linkKinds` value needs HU and EN labels in the platform; its foundation test fails on the bump PR otherwise. The same test lists the project ids, so a new project also needs a platform change.
- Removing or renaming a key or an export, adding a required key, or narrowing an enum breaks the platform and API clients: open the platform PR first. Whether such a change bumps `schemaVersion` is the owner's call.
- Run `npm test && npm run validate`, then update [SUBMITTING.md](../SUBMITTING.md#contract) to match.
