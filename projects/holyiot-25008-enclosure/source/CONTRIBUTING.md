# Contributing

> **Scope (since 2026-09-26).** This tree was the `Remeny-Farm/hen-tag-enclosure`
> repository, now archived. It lives in the catalogue at
> `projects/holyiot-25008-enclosure/source/`, and "this repository" below
> means this source tree. Open pull requests against
> `Remeny-Farm/open-source-farming-catalog`; the catalogue's root
> [`AGENTS.md`](../../../AGENTS.md) covers landing, and its
> [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) and
> [`SUBMITTING.md`](../../../SUBMITTING.md) apply too: the rules below add to
> them for this tree. Its CI runs only the
> catalogue checks (`npm test`, `npm run validate`), not `verify.py` or the
> cad suites. Files listed in `../project.json` `files` are hash-pinned: see
> [Hash-pinned files in the catalogue](#hash-pinned-files-in-the-catalogue).

This is the mechanical CAD tree of the Holyiot 25008 enclosure in the Open
Source Farming catalogue, with a machine-verified, physically
tested culture: geometry changes are checked by code before they are checked
by a printer, and claims about what has actually been built are kept
separate from claims about what the model says. Contributions are expected
to follow the same discipline.

## Environment

- [`uv`](https://docs.astral.sh/uv/) for running the scripts. Every script in
  `cad/` carries its dependencies as [PEP 723](https://peps.python.org/pep-0723/)
  inline metadata, so `uv run --python 3.12 <script>.py` resolves and caches
  everything itself — no virtualenv to set up, nothing installed into the
  repository.
- Python **3.11–3.12** (the scripts pin `requires-python = ">=3.11,<3.13"`).
- [build123d](https://build123d.readthedocs.io/) is the modelling library.
  Changes should stay in real B-rep solids — fillets, sweeps, boolean ops —
  not hand-authored meshes.

## Before opening a PR

Run, from `cad/`, and make sure all of these pass:

```sh
uv run --python 3.12 hen_tag_enclosure.py   # rebuild + re-export
uv run --python 3.12 verify.py              # 40 machine checks (49 with --board-step); must exit 0
uv run --python 3.12 test_cap_marking.py    # cap-generator test suite; must exit 0
uv run --python 3.12 slice_check.py         # real-slicer check; skips if Bambu Studio is absent
```

A change to `cap_batch.py`, `bambu_project.py` or `cap_motifs.py` also runs
`uv run --python 3.12 test_cap_batch.py`, `uv run --python 3.12
test_bambu_project.py` and `uv run --python 3.12 check_motifs.py`; each exits
1 on a failure.

`verify.py` is the geometry gate: it checks interference, wall thickness,
seal and harness fit by assembling the parts virtually and measuring them,
not by eyeballing a render. The catalogue's CI (`validate`) does not run
`verify.py` or any other script in this tree, so this rule holds only in
review: run the checks yourself and paste their summary lines into the PR. A
change that regenerates geometry without a clean `verify.py` run will not be
merged. Step 1 rewrites the export time in every STEP file, so it changes
hash-pinned files even when the geometry is unchanged (see below).

## Geometry changes need physical evidence

`verify.py` passing means the model is internally consistent — not that it
prints or fits. For any change to the enclosure's fit-critical geometry
(bayonet lugs and channels, seal groove, cavity dimensions, harness tabs), either:

- print the relevant fit coupon (`out/coupon_*.stl`, or add a new one) and
  report the result, or
- state explicitly in the PR why a coupon isn't warranted for this change
  (e.g. a change confined to the cap's decorative lettering, which does not
  touch the closure, seal or envelope).

Do not claim a fit is confirmed without a printed part behind it.

## Recording physical evidence

Anything learned from a real print, measurement, or bench test goes in a
dated note under `docs/lab/`, following the existing notes' structure:

- Filename: `YYYY-MM-DD-<short-slug>.md`.
- Header block: `Date`, `Author`, `Status` (e.g. *Completed / Fit confirmed*,
  *Partial / awaiting confirmation*).
- Sections, as applicable: **Purpose & Objective**, **Verified Evidence** /
  **Reported / Measured** (keep operator-reported readings clearly separate
  from independently confirmed measurements), **Technical Interpretation**,
  **Key Decisions**, **Open Questions & Verification Items**.
- Link the note from `DESIGN.md` (and `docs/requirements.md` if it changes a
  requirement) wherever it changes a decision or resolves an open question.
- List the new note in `../project.json` `files` with the role `evidence`,
  like the existing notes (see
  [Hash-pinned files in the catalogue](#hash-pinned-files-in-the-catalogue)).

See any file in `docs/lab/` for the pattern in practice.

## Accessory proposals

Anything added under `platform/` is a proposal until it has been printed and
bench-tested. New accessory designs must satisfy the hard safety envelope in
[`platform/accessories.md`](platform/accessories.md) — summarized here, full
detail there:

1. One rigid piece (or permanently bonded) — nothing a peck can separate.
2. No magnets; no zinc-plated or galvanized metal; preferably no metal at all.
3. No dangling, swinging or flexible protruding elements.
4. All edges ≥1 mm radius; no points.
5. Mass ≤5 g (T1), weighed, not estimated.
6. Height above the crown deck ≤6 mm (T1).
7. The optical keep-out over the clear LED ring stays open, or is bridged
   only by clear PETG.
8. Flock wear is matte, muted colours only.
9. Survives a 3 % bleach soak; no paint or coatings that flake.
10. Passes the pull-off (≥30 N) and torque (3× cap break-loose) bench tests.

The current shipping design (`DESIGN.md`, `cad/hen_tag_enclosure.py`) must
never be modified to accommodate an accessory — the platform is designed
specifically so accessories mount without touching the shipping cap or body
geometry.

## Style

- English only, in code, comments, commit messages and docs. Sample strings
  that demonstrate Hungarian-diacritic support in the cap generator (e.g.
  `--top "Bözsi!"`) are the one intentional exception — that charset support
  is a feature being demonstrated, not prose.
- Be explicit about **verified vs. UNVERIFIED**. If a dimension, mass or fit
  claim has not been physically confirmed, say so in the same sentence,
  matching the convention already used throughout `DESIGN.md` and
  `docs/requirements.md`. Do not upgrade an assumption to a fact because the
  model is internally consistent.
- Keep edits minimal and scoped. Don't rewrite a document's structure or tone
  to make an unrelated change.

## Generated files in PRs

`cad/out/` mixes committed and gitignored outputs — see `cad/out/.gitignore`
for exactly which. As a rule:

- The stable printables (`body.stl`/`.step`, `cap.stl`/`.step`, the fit
  coupons) are committed, so a maker can print without setting up the CAD
  toolchain. Regenerate and commit them when a change to
  `hen_tag_enclosure.py` actually changes the exported geometry; otherwise
  restore them after a run (see below).
- Per-tag caps, half-sections and other debugging or on-demand output are
  gitignored and should not be added to a PR, except the one reference
  sample pair already tracked as an example of the cap generator's output.
- Don't hand-edit anything in `out/` — it is generated, and hand edits will
  be silently overwritten and diverge from the source next time someone runs
  the generator.

## Hash-pinned files in the catalogue

This tree lives at `projects/holyiot-25008-enclosure/source/` in
`Remeny-Farm/open-source-farming-catalog`. `../project.json` pins the sha256
of the exports in `cad/out/` (STL, STEP, `hen_tag_revC_P1S.3mf`), of
`hen_tag_enclosure.py`, `cap_marking.py` and `verify.py`, of this tree's
`README.md`, `DESIGN.md`, `docs/requirements.md` and `cad/README.md`, and of
the lab notes. Read its `files` list before you edit anything here. The
required check `validate` fails when one of these files changes and its entry
does not.

- `hen_tag_enclosure.py` writes the export time into every STEP file. After
  a run, restore the exports you did not mean to change
  (`git checkout -- cad/out/<file>`, or all of `cad/out` when the geometry
  did not change).
- For every pinned file you did change, run
  `npm run hash -- holyiot-25008-enclosure <role> source/<path>` from the
  repository root (role `export`, `source`, `documentation` or `evidence`, as
  in `project.json`) and paste the printed sha256 into its entry in the same
  commit.
