# Open Source Farming catalogue

Magyarul: [README.hu.md](README.hu.md)

The reviewed catalogue behind [opensource.remeny.farm](https://opensource.remeny.farm) (Hungarian) and [opensource.mootopia.wtf](https://opensource.mootopia.wtf) (English): open agricultural tool designs with their documentation, bill of materials, files and photos. Every design states its stage (`concept`, `prototype`, `built`, `field-tested`), its licence and its limitations. Nothing is embellished.

The website reads this repository directly. Its API (`/api/v1/projects.json`, `/api/v1/project.schema.json`) is derived from the same files.

## Layout

```
schema/project.ts            project contract (Zod), schema version 2
schema/build.ts              "I built this" report contract
projects/<id>/
  project.json               metadata: title, description, stage, topics, licences, files, links, photo, limitations
  README.hu.md, README.en.md what it is, its state, how to build it (required from stage "built")
  bom.csv                    ref,qty,item_hu,item_en,source,notes
  CHANGELOG.md               version history
  source/                    the project's own tree: editable CAD, code, documentation, evidence
  export/                    derived files (STL, STEP, PDF, gerber) for projects without a source tree
  photos/                    <name>-1200.webp, <name>-600.webp and a provenance sidecar for each
  builds/                    <yyyy-mm-dd>-<slug>.json reports from people who built it
scripts/validate.mjs         layout, hashes, photos, README, BOM and build-report checks
scripts/hash.mjs             prints "files" entries with sha256 for project.json
scripts/photo.mjs            derives the photo pair from an original (needs sharp)
```

Only files listed in `project.json` `files` are served by the website, at `/projects/<id>/<path>`, each with its sha256. Large binaries stay under 20 MB per file; anything bigger lives on a mirror linked in `links`.

## Contributing

- Read [CONTRIBUTING.md](CONTRIBUTING.md) (people) or [SUBMITTING.md](SUBMITTING.md) (exact contract, for agents and scripts).
- New design without writing JSON: open a [new design issue](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=new-design.yml).
- New design or fix as a pull request: fork, add or edit `projects/<id>/`, run `npm ci && npm run validate`, open the PR.
- Built one? File a [build report](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=build-report.yml).

A GitHub account is required; there is no e-mail or web-form intake. Every entry is reviewed by the maintainer before it is merged and published.

## Checks

```sh
npm ci
npm test          # unit tests for the validator
npm run validate  # the whole catalogue
```

Node 22.18 or newer (the scripts import TypeScript directly).

## Licences

- Catalogue metadata, documentation and photos: [CC BY-SA 4.0](LICENSE).
- Scripts and schema in this repository: [MIT](LICENSE-MIT).
- Each project's files carry the licences stated in its `project.json` `licenses`; a licence with a `path` covers that file or directory, one without covers the whole project.

Maintained by [Remény Farm](https://github.com/Remeny-Farm).
