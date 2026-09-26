# Submitting a project: the exact contract

For scripts, agents and people who prefer precision. Human-oriented guidance is in [CONTRIBUTING.md](CONTRIBUTING.md) / [CONTRIBUTING.hu.md](CONTRIBUTING.hu.md).

## Channels

1. **Pull request** (preferred): add or edit `projects/<id>/` and open a PR against `main`. CI runs `npm run validate`; the maintainer reviews and merges.
2. **Issue with a JSON block**: open a [new design issue](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=new-design.yml) and paste a complete `project.json` in the "Machine-readable entry" field. The maintainer turns it into a PR.

Both require a GitHub account. Nothing else is accepted.

## Contract

- Schema source: [`schema/project.ts`](schema/project.ts) (Zod). The same schema is served as JSON Schema at `https://opensource.mootopia.wtf/api/v1/project.schema.json`.
- Current `schemaVersion`: **2**. Unknown keys are rejected.
- `id`: lowercase kebab-case, equal to the directory name `projects/<id>/`.
- `title`, `description`, `limitations`, `photo.alt`: objects with non-empty `hu` and `en`.
- `category`: `mechanical | electronics | firmware | mixed`.
- `stage`: `concept | prototype | built | field-tested`. From `built` upwards `README.hu.md` and `README.en.md` are required.
- `topics` (at least one): `poultry | livestock | water | fencing | soil | tools | sensors | energy | storage`.
- `requires` (at least one): `3d-printer | soldering | welding | woodworking | microcontroller-flashing | none`.
- `licenses` (at least one): `{ "identifier": "<SPDX id>", "path"?: "<file or directory>" }`. No `path` means the whole project.
- `files` (optional, at least one if present): `{ "path", "sha256", "role" }` with `role` in `source | export | documentation | bom | evidence`. Paths are relative to `projects/<id>/`, must exist, must hash to `sha256`, and must be at most 20 971 520 bytes. Only listed files are served by the website.
- `links` (optional): `{ "kind": "printables | repository | discussion | mirror | video", "url": "https://..." }`.
- Either `files` or `links` is required.
- `photo` (optional but required in practice for `built` and `field-tested`): `{ "src": "photos/<name>-1200.webp", "width": 1200, "height": 900, "alt": {hu,en} }`. A `photos/<name>-600.webp` at exactly half size must exist next to it. Generate both with `npm run photo -- <id> <original> --by "<Name>"`.
- `gallery` (optional): array of the same photo objects.
- `derivedFrom` (optional): `[{ "id"?: "<catalogue id>", "url"?: "https://...", "note"?: {hu,en} }]`, each with `id` or `url`.
- `maintainers` (at least one) and `contributors` (optional): `{ "name", "url"? , "role"? }`.

## Directory layout

```
projects/<id>/
  project.json         required
  README.hu.md         required from stage "built"
  README.en.md         required from stage "built"
  bom.csv              optional; header exactly: ref,qty,item_hu,item_en,source,notes
  CHANGELOG.md         optional
  source/              the project's own tree (any layout); list served files in project.json
  export/              derived files for projects without a source tree
  photos/              <name>-1200.webp, <name>-600.webp, plus <file>.json provenance sidecars
  builds/              <yyyy-mm-dd>-<slug>.json build reports (schema/build.ts)
```

## Minimal example (files hosted here)

```json
{
  "schemaVersion": 2,
  "id": "example-nest-box-latch",
  "title": { "hu": "Példa fészekajtó-retesz", "en": "Example nest box latch" },
  "description": { "hu": "Nyomtatott retesz fészekajtóhoz.", "en": "Printed latch for a nest box door." },
  "category": "mechanical",
  "stage": "prototype",
  "version": "0.1.0",
  "topics": ["poultry"],
  "requires": ["3d-printer"],
  "maintainers": [{ "name": "Your Name", "url": "https://github.com/your-handle" }],
  "licenses": [{ "identifier": "CC-BY-SA-4.0" }],
  "files": [{ "path": "export/latch.stl", "sha256": "<64 hex chars>", "role": "export" }],
  "photo": { "src": "photos/example-nest-box-latch-1200.webp", "width": 1200, "height": 900,
             "alt": { "hu": "A retesz a fészekajtón.", "en": "The latch on the nest box door." } },
  "limitations": { "hu": "Egyszer nyomtatva, terhelés nem mérve.", "en": "Printed once, load not measured." }
}
```

Get the `files` entries with `npm run hash -- example-nest-box-latch export export/latch.stl`.

## Minimal example (files hosted elsewhere)

Replace `files` with `"links": [{ "kind": "printables", "url": "https://www.printables.com/model/..." }]`. A `photo` is still expected for `built` and `field-tested`.

## Validate before you submit

```sh
npm ci
npm run validate
```

The same command runs in CI on every pull request, without secrets.

## Build reports

`projects/<id>/builds/<yyyy-mm-dd>-<slug>.json`:

```json
{
  "schemaVersion": 1,
  "date": "2026-10-01",
  "builder": { "name": "Your Name", "url": "https://github.com/your-handle" },
  "projectVersion": "rev-c",
  "notes": { "en": "Printed in PETG on a Prusa MK4; the cap needed 0.1 mm more clearance." },
  "photo": { "src": "photos/2026-10-01-your-handle-1200.webp", "width": 1200, "height": 900,
             "alt": { "hu": "...", "en": "..." } }
}
```

## Review criteria

Rights and licence explicit; HU and EN equivalent; limitations honest and safety-relevant; stage supported by evidence; photo real with provenance; validation green. The maintainer may edit wording and translations before merging and will say so in the PR.
