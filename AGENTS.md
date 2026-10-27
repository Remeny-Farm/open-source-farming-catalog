# Agent guide

Start here for any change in this repository. English only, like [SUBMITTING.md](SUBMITTING.md): agents read it. `CLAUDE.md` is a symlink to this file.

## What this is

The public catalogue of open farm designs behind opensource.remeny.farm (HU) and opensource.mootopia.wtf (EN). The private platform repository (Remeny-Farm/opensource.remeny.farm) mounts this repo as its `content/` git submodule, pinned to a commit, and re-exports [schema/project.ts](schema/project.ts). A daily Dependabot gitsubmodule PR in the platform bumps the pin, and merging that PR deploys. A merge here is not live until then. The platform's tests run on that PR: they pin the list of project ids and need HU and EN labels for every `topics`, `requirements` and `linkKinds` value, so a new project or enum value fails there until the platform follows ([schema/README.md](schema/README.md)).

Below, `source/` means `projects/holyiot-25008-enclosure/source/`.

## Reading order

1. This file.
2. [SUBMITTING.md](SUBMITTING.md): the project contract.
3. The doc for your task in the table below.

## Task → read → proof before the PR

| Task | Read | Proof |
|---|---|---|
| Project metadata, READMEs, `bom.csv`, photos, build reports | [SUBMITTING.md](SUBMITTING.md) | `npm ci && npm test && npm run validate` |
| `schema/` | [schema/README.md](schema/README.md) (public API, import rules), [SUBMITTING.md#contract](SUBMITTING.md#contract) | `npm test && npm run validate`. Erasable TypeScript only (Node type stripping, no build step). A contract change changes the platform API (`/api/v1/project.schema.json`) at the next bump. |
| `scripts/`, `tests/` | [README.md#checks](README.md#checks) | `npm test && npm run validate` |
| Holyiot CAD (`source/cad/`) | [source/README.md](projects/holyiot-25008-enclosure/source/README.md) → [source/cad/README.md](projects/holyiot-25008-enclosure/source/cad/README.md) → [source/DESIGN.md](projects/holyiot-25008-enclosure/source/DESIGN.md); rules in [source/CONTRIBUTING.md](projects/holyiot-25008-enclosure/source/CONTRIBUTING.md) | From `source/cad/`: `uv run --python 3.12 verify.py` (must exit 0) and `uv run --python 3.12 test_cap_marking.py`; for batch or plate code also `test_cap_batch.py`, `test_bambu_project.py` and `check_motifs.py` the same way. CI runs none of these: paste the summary into the PR. |
| `source/cad/catalog.json`, `cap_design.py`, `out/layout.json` | [source/cad/README.md#batch-workflow](projects/holyiot-25008-enclosure/source/cad/README.md#batch-workflow) | `pnpm sync:data` in `source/editor/`, then `npm test` (runs `tests/editor-data-parity.test.ts`). Chirp holds the app copies: `packages/shared-types/src/i18n/hen-cap-catalog.json` and `packages/shared-types/src/hen-cap.ts`. |
| Cap editor (`source/editor/`) | [source/editor/README.md](projects/holyiot-25008-enclosure/source/editor/README.md) | Reference prototype only. Editor changes go to chirp `packages/real-chicken-ui/src/cap-editor/` (landed by Remeny-Farm/chirp#2409). The default `CHIRP_DIR` (`../../chirp`) and the `tsconfig.json` paths predate the import and resolve inside `projects/holyiot-25008-enclosure/`: point both at your chirp checkout. |
| Accessory proposal (`source/platform/`) | [source/platform/README.md](projects/holyiot-25008-enclosure/source/platform/README.md), [accessories.md](projects/holyiot-25008-enclosure/source/platform/accessories.md) | Proposal only, nothing printed. |
| New physical evidence | [source/CONTRIBUTING.md#recording-physical-evidence](projects/holyiot-25008-enclosure/source/CONTRIBUTING.md#recording-physical-evidence) | A new dated note in `source/docs/lab/`, listed in `project.json` `files` as `evidence` like the existing notes. |

## Hash-pinned files

Every path in a `project.json` `files` list carries its sha256, and `npm run validate` (the required `validate` check) fails on a mismatch. For Holyiot the list includes `source/README.md`, `source/DESIGN.md`, `source/docs/requirements.md`, `source/cad/README.md`, the lab notes, core `.py` files and the committed `cad/out/` exports. Read the list before you edit anything under `source/`. After an edit, run `npm run hash -- <project-id> <role> <path>...` (paths relative to `projects/<id>/`, the role of the existing entry) and paste the new sha256 into `project.json` in the same commit.

## Records and generated files

- Records, append only: `source/docs/lab/*.md`, the history lines of each `CHANGELOG.md`, `source/docs/superpowers/plans/` and `specs/`. A correction is a new dated note or a new CHANGELOG line. The one in-place addition allowed is a status callout at the top of a plan or spec (executed, superseded).
- Legal, owner only: `LICENSE`, `LICENSE-MIT`, `source/LICENSE`.
- Generated, never hand-edited: `source/cad/out/*` (rerun its generator, see [source/cad/README.md#files](projects/holyiot-25008-enclosure/source/cad/README.md#files)); `source/editor/src/cap-editor/data/*.json` (`pnpm sync:data`); `photos/*.webp` and their `.json` sidecars (`npm run photo`).

## Language

- `README.md` and `CONTRIBUTING.md` are English, with the Hungarian mirrors `README.hu.md` and `CONTRIBUTING.hu.md`. Change both files in the same PR, with the same structure and meaning.
- Each project's `README.en.md` and `README.hu.md` say the same; localized `project.json` fields carry both `hu` and `en`.
- English only: this file, `SUBMITTING.md`, `REVIEW.md`, `schema/`, `scripts/`, `tests/`, and everything under `source/` (its CONTRIBUTING.md, Style).
- Issue and PR templates are bilingual inline.
- No check enforces any of this: the reviewer does.

## Conflict rules

- Code beats prose: `schema/project.ts` over SUBMITTING.md; `scripts/lib/validate-catalog.ts` over README.md and SUBMITTING.md; `source/cad/*.py` over DESIGN.md and the READMEs on what the model does.
- A dated lab note beats DESIGN.md and the READMEs on what was printed or measured; the newest note on the same subject wins.
- Root docs: when an English file and its `*.hu.md` mirror disagree, the English file is the source; fix the mirror in the same PR.
- An open owner decision beats any doc wording: do not "fix" text that an open issue covers (revision label: issue #11).
- Inside `source/`, "this repository" means the archived Remeny-Farm/hen-tag-enclosure. Its rules ([source/CONTRIBUTING.md](projects/holyiot-25008-enclosure/source/CONTRIBUTING.md)) apply to `source/`; landing follows this file.

## Vocabulary

- catalogue: this repo. platform: the private Remeny-Farm/opensource.remeny.farm. sites: opensource.remeny.farm (HU), opensource.mootopia.wtf (EN).
- `holyiot-25008-enclosure` = "Hen Tag Enclosure" = the archived Remeny-Farm/hen-tag-enclosure, imported under `source/`. Holyiot 25008 is the BLE module inside it.
- Revision A/B/C/D: geometry revisions in DESIGN.md and the lab notes. `"version": "rev-c"` in `project.json` is the release label. Whether the current geometry is C or D is open ([issue #11](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/11)).
- chirp: the farm app monorepo (`@chirpcoop/*` packages). Tyutyu: its mobile app. patron: a person who sponsors a hen and designs its cap. Golden Grain: the app currency.
- stage: `concept | prototype | built | field-tested`. UNVERIFIED: not physically confirmed.

## Landing

- Work on a branch and open a PR against `main`. A ruleset requires a PR for `main`.
- Required check: `validate` (`npm ci`, `npm test`, `npm run validate`). It is strict, so the branch must be up to date with `main`. No approval and no `review-gate` check are required, and repo auto-merge is off.
- Review: a fresh reviewer reads the diff and [REVIEW.md](REVIEW.md). PRs carry the owner's lane labels (`risk:*`, `reviewed:<model>@<effort>`, `review-round:N`, `owner-ok`).
- Merge only with the owner's license (an owner-lane `/ship` or "merge <n>"), never with `gh pr merge --admin`.
- Release: the maintainer pushes a tag `<project-id>/<version>` equal to the project's `version`; [release.yml](.github/workflows/release.yml) publishes an immutable zip. Agents never push tags.

## Do not (hot list)

Ranked by cost.

### ❌ Push to `main`, merge with `gh pr merge --admin`, or push a tag
**Why:** a direct push or an admin merge skips the PR rule and the required `validate` check (82e4b45 and 1b9851b reached `main` without a PR on 2026-10-26). A `<id>/<version>` tag publishes an immutable release.
**Instead:** open a PR; the maintainer merges and cuts releases.

### ❌ Specify carbon-fibre, conductive or metal-filled filament for any part
**Why:** it detunes the 2.4 GHz antenna and can short the coin cell on a live hen ([source/docs/requirements.md](projects/holyiot-25008-enclosure/source/docs/requirements.md), section 1).
**Instead:** PETG only, as the design specifies.

### ❌ Change CAD geometry without a clean `verify.py` run
**Why:** CI does not run the CAD checks, and a live hen wears the part.
**Instead:** run `verify.py` and the cad suites from `source/cad/` and paste the summary into the PR. A fit-critical change also needs a printed coupon or a stated reason ([source/CONTRIBUTING.md#geometry-changes-need-physical-evidence](projects/holyiot-25008-enclosure/source/CONTRIBUTING.md#geometry-changes-need-physical-evidence)).

### ❌ Edit a file listed in `project.json` `files` and stop [gate: `validate`]
**Why:** the sha256 mismatch fails the required check.
**Instead:** run `npm run hash -- <id> <role> <path>` and update `project.json` in the same commit.

### ❌ Edit or delete a lab note, a CHANGELOG history line, or a plan or spec
**Why:** they are dated evidence, and a rehash hides the rewrite from `validate`.
**Instead:** add a new dated note or append a CHANGELOG line.

### ❌ Hand-edit `source/cad/out/*` or the editor data copies [gate: `npm test` parity test, for the copies]
**Why:** the next generator run overwrites them, and the committed exports are hash-pinned.
**Instead:** rerun the generator, or `pnpm sync:data`.

### ❌ Rename a revision or change `version`
**Why:** the C vs D label is an open owner decision.
**Instead:** cite [issue #11](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/11) and leave the wording.

### ❌ Upgrade an UNVERIFIED claim (fit, mass, seal, stage) to a fact
**Why:** `stage` and `limitations` are published safety claims about a device a live animal wears.
**Instead:** cite a lab note, a photo or a build report.

### ❌ Re-slice a cap plate `.3mf` in the Bambu Studio GUI, or re-orient the exported STLs
**Why:** the GUI gave a 0.12 mm first layer and two walls (lab note 2026-10-04); a re-oriented cap prints its top plate as a ~28 mm bridge.
**Instead:** print the `.gcode.3mf` as written, and drop the STLs on the plate as exported.

### ❌ Modify `hen_tag_enclosure.py` to fit an accessory
**Why:** the shipping cap and body must stay as printed ([source/CONTRIBUTING.md#accessory-proposals](projects/holyiot-25008-enclosure/source/CONTRIBUTING.md#accessory-proposals)).
**Instead:** extend `hen_tag_platform.py`, which imports the enclosure.

### ❌ Change `cad/catalog.json` or the design hash in this repo alone
**Why:** chirp ships its own copy and schema, and `cap_batch.py` refuses a batch whose generator version or design hash does not match.
**Instead:** bump `generator_version` in `catalog.json` in the same PR, make the matching chirp change and name it in the PR ([source/cad/README.md#files](projects/holyiot-25008-enclosure/source/cad/README.md#files)).

### ❌ Delete an "unused" export from `schema/`, or import anything there but `zod`
**Why:** the private platform re-exports `schema/project.ts`; this repo's CI stays green and the break shows up on the platform's content bump PR.
**Instead:** follow [schema/README.md](schema/README.md).

### ❌ Edit `README.md` or `CONTRIBUTING.md` without its `*.hu.md` mirror
**Why:** the Hungarian site and contributors read the mirror, and no check catches the drift.
**Instead:** change both files in the same PR (see Language above).

### ❌ File or sand printed parts to make them fit
**Why:** it hides a parameter error that every later print repeats.
**Instead:** change `Params` (`fit_lug_r`, `fit_lug_z`, `cam_lock`, `cam_rate`) and regenerate ([source/cad/README.md#bayonet-fit](projects/holyiot-25008-enclosure/source/cad/README.md#bayonet-fit)).

## Settled decisions

There is no ADR directory; this list is the decision index. Reopen a decision only on the owner's word.

- Content and platform split (2026-09-26): this public repo holds all content; the private platform pins it as `content/` and re-exports `schema/project.ts`; a Dependabot bump deploys.
- Intake is GitHub only, through issue forms or PRs ([CONTRIBUTING.md](CONTRIBUTING.md)).
- Contract: strict Zod schema v2 in [schema/project.ts](schema/project.ts); erasable TypeScript only, run by Node type stripping, no build step.
- Served files are at most 20 MiB, a margin under the Cloudflare Workers 25 MiB static-asset limit (`maxFileBytes`).
- Licences: CC BY-SA 4.0 for content, MIT for scripts and schema, per-path licences per project ([README.md#licences](README.md#licences)).
- Releases: a tag `<project-id>/<version>` → [release.yml](.github/workflows/release.yml) publishes an immutable zip; maintainer only.
- Fork PRs: [validate.yml](.github/workflows/validate.yml) runs on `pull_request`, never `pull_request_target`, with a read-only token and no secrets.
- Cap generator home (2026-09-30, [ADR-0244 "Generator home"](https://github.com/Remeny-Farm/chirp/blob/main/docs/decisions/0244-hen-cap-customisation.md#generator-home--2026-09-30) in the private chirp repo): canonical in `source/cad/` on `main`; the catalog flows generator → chirp as a verbatim copy with a `generator_version` bump, designs flow chirp → generator only as a `hen-cap-batch/1` file. Never generate a plate from the archived repo.
- Cap face: no variable layer height (2026-10-04, [source/DESIGN.md#print-settings](projects/holyiot-25008-enclosure/source/DESIGN.md#print-settings)).
- Holyiot source: imported with full history from the archived Remeny-Farm/hen-tag-enclosure on 2026-09-26. Its design decisions are [source/DESIGN.md#design-decisions](projects/holyiot-25008-enclosure/source/DESIGN.md#design-decisions) 1–10.
- Cap editor: the live editor is chirp `packages/real-chicken-ui/src/cap-editor/` (Remeny-Farm/chirp#2409); `source/editor/` is the reference prototype.
- Open, not settled: the revision label C vs D ([issue #11](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/11)); whether 10 g is a hard welfare limit or an aspiration ([source/DESIGN.md#open-questions--next-steps](projects/holyiot-25008-enclosure/source/DESIGN.md#open-questions--next-steps), item 4).
