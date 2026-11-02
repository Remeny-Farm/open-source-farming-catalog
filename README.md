# Open Source Farming catalogue

Magyarul: [README.hu.md](README.hu.md)

The reviewed catalogue behind [opensource.remeny.farm](https://opensource.remeny.farm) (Hungarian) and [opensource.mootopia.wtf](https://opensource.mootopia.wtf) (English): open agricultural tool designs with their documentation, bill of materials, files and photos. Every design states its stage (`concept`, `prototype`, `built`, `field-tested`), its licence and its limitations. Nothing is embellished.

The website builds from a pinned commit of this repository (a git submodule) that an automated pull request in the website's repository moves forward; a change merged here goes live only after that pull request is merged. Its API (`/api/v1/projects.json`, `/api/v1/project.schema.json`) is derived from the same files.

## Layout

```
schema/project.ts            project contract (Zod), schema version 2
schema/build.ts              "I built this" report contract
schema/README.md             schema public API and import rules (the website re-exports project.ts)
projects/<id>/
  project.json               metadata: title, description, stage, topics, licences, files, links, photo, limitations
  README.hu.md, README.en.md what it is, its state, how to build it (required from stage "built")
  bom.csv                    ref,qty,item_hu,item_en,source,notes
  CHANGELOG.md               version history
  source/                    the project's own tree: editable CAD, code, documentation, evidence
  export/                    derived files (STL, STEP, PDF, gerber) for projects without a source tree
  photos/                    <name>-1200.webp, <name>-600.webp and a provenance sidecar for each
  builds/                    <yyyy-mm-dd>-<slug>.json reports from people who built it
scripts/validate.mjs         runs the catalogue checks (exit 1 on any problem)
scripts/lib/validate-catalog.ts  the checks: layout, hashes, photos and sidecars, README, BOM, build reports
scripts/hash.mjs             prints "files" entries with sha256 for project.json
scripts/photo.mjs            derives the photo pair from an original (needs sharp)
scripts/release-check.mjs    checks a "<project-id>/<version>" tag against project.json (release workflow)
tests/                       validator unit tests; Holyiot editor data parity
```

The website serves the files listed in `project.json` `files` at `/projects/<id>/<path>`, each with its sha256, and also everything in `photos/` except the git-ignored `photos/originals/`. Large binaries stay under 20 MB per file; anything bigger lives on a mirror linked in `links`.

## Contributing

- Read [CONTRIBUTING.md](CONTRIBUTING.md) (people) or [SUBMITTING.md](SUBMITTING.md) (exact contract, for agents and scripts).
- Agents maintaining this repository: start at [AGENTS.md](AGENTS.md).
- New design without writing JSON: open a [new design issue](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=new-design.yml).
- New design or fix as a pull request: fork, add or edit `projects/<id>/`, run `npm ci && npm test && npm run validate`, open the PR.
- Built one? File a [build report](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=build-report.yml).

A GitHub account is required; there is no e-mail or web-form intake. Every entry is reviewed by the maintainer before it is merged and published.

## Checks

```sh
npm ci
npm test          # validator unit tests and the Holyiot editor data parity check
npm run validate  # the whole catalogue
```

Node 22.18 or newer (the scripts import TypeScript directly).

## Releases

The maintainer pushes a tag `<project-id>/<version>` (the `version` in that project's `project.json`). `.github/workflows/release.yml` validates the catalogue and publishes an immutable zip of `projects/<id>/` as a GitHub Release. Contributors and agents do not push tags.

## Licences

- Catalogue metadata, documentation and photos: [CC BY-SA 4.0](LICENSE).
- Scripts and schema in this repository: [MIT](LICENSE-MIT).
- Each project's files carry the licences stated in its `project.json` `licenses`; a licence with a `path` covers that file or directory, one without covers the whole project.

Maintained by [Remény Farm](https://github.com/Remeny-Farm).
