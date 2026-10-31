# Enclosure CAD

Parametric source for the hen tag enclosure. Solid B-rep modelling via
[build123d](https://build123d.readthedocs.io/) on the OCCT kernel, so the output
is real CAD geometry with true fillets and helical sweeps, exported as **STEP as well
as STL** — the model stays editable in FreeCAD or any other CAD tool rather than
being a dead triangle mesh.

## Running

The scripts carry PEP 723 inline dependencies, so `uv` resolves everything on
first run. No virtualenv, and nothing is installed into the repository.

```sh
uv run --python 3.12 hen_tag_enclosure.py   # build + export to out/
uv run --python 3.12 verify.py              # 40 machine checks + half sections (+9 with --board-step)
uv run --python 3.12 slice_check.py         # real-slicer check, needs Bambu Studio
```

First run downloads the OCCT wheel (~60 MB) and a CPython 3.12 toolchain; after
that it is cached. `verify.py` exits non-zero when a check fails, so it works as
a pre-commit or CI gate.

**STLs are exported already lying in their print orientation** — the cap and the
female coupon are flipped top-plate-down on export. Drop them on the plate as
they are; re-orienting the cap makes its top plate a ~28 mm bridge. The STEP
files keep the design coordinate system so the model stays readable in CAD.

`slice_check.py` re-checks printability against the real slicer: it runs the
Bambu Studio CLI on the four printables with the P1S 0.4 mm machine, the
0.16 mm process, PETG Basic, and the three settings `../DESIGN.md` asks for
(3 walls, Arachne, avoid crossing walls), then reads the G-code back and
counts travel moves that fly across open air — the bore of the cap, the cavity
and cell pocket of the body — where PETG leaves a string. It fails on a slicer
warning or when a count exceeds a limit set just above the 2026-09-10 numbers.
`--stock` slices with the untouched Bambu profile for comparison, `--keep`
leaves the G-code in `out/slice/`. Skips with exit 0 when Bambu Studio is not
installed.

## Per-tag cap markings — the deterministic tag generator

```sh
uv run --python 3.12 cap_marking.py 67 --top "Bözsi!" --icon heart
uv run --python 3.12 cap_marking.py 12345 --icon star
uv run --python 3.12 cap_marking.py 133 --icon flower --font tahoma
uv run --python 3.12 test_cap_marking.py            # test suite; --bambu for the full path
```

This is the back end for the customer design UI. The inputs are exactly the
customer-facing choices, everything else is fixed:

| Input | Envelope |
|---|---|
| number | **required**, 1–5 digits, bottom arc, 4.5 pt |
| `--top` message | staff-only; ALL CAPS coin lettering at 3.6 pt; letters incl. Hungarian (ő/ű), digits, space, `.:!?'"+-`; over-length is rejected with the measured span and the guaranteed-safe length |
| `--icon` / `--centre` / `--band` | ids from `catalog.json`: 34 icons or `none` (default `heart`), 3 centre patterns, 13 band patterns; `--icon` and `--centre` exclude each other |
| `--colours` / `--scheme` | each zone (`ring`, `number`, `disc`, `centre`, `band`) gets `base`, `a`, `b` or `clear`; the scheme (default `pasture`) sets the filaments |
| `--font` | curated list: verdana (default), tahoma, arial, futura, din, rounded |

**Layout: a shell in the scheme's base colour with a clear LED ring.** A clear
annulus (r 8.5–11.5) runs through the whole top plate, so the LED shows
wherever it lands and nothing has to be aligned. The patron's zone colours cut
the rest of the top plate into up to four bodies. A zone (outer ring, inner
disc) runs through the whole plate; the number, centre element and band
pattern are 0.64 mm flush inlays (`--depth`).

| Slot | Body | Filament |
|---|---|---|
| 1 | `cap_<n>` | the shell, scheme base colour |
| 2 | `window_<n>` | Prusament PETG Clear: the LED ring plus any zone set to `clear` |
| 3 | `a_<n>` | scheme colour a (zones and inlays) |
| 4 | `b_<n>` | scheme colour b (zones and inlays) |

Deterministic by design: **font sizes are fixed**, misfits are rejected with
measured numbers, and identical input produces **byte-identical** output
(canonically ordered welded meshes, deterministic STL writer, fixed zip
timestamps) — a regenerated tag can be diffed against a shipped one.

Envelope rules the test suite forced: the message is uppercased (a lowercase
descender plus an accented capital outgrows any printable band height, while
accented capitals alone fit), and comma/semicolon/parentheses are excluded
from the charset for the same below-the-baseline reason.

The deliverable for the P1S is **`out/cap_<n>_P1S.3mf`** — a Bambu Studio
project with the bodies as parts of ONE object (`--assemble` via the
Bambu CLI, so nothing can be arranged apart or dragged out of register) and
the filament slots pre-assigned. Open it, load the project settings, load the
scheme's base filament in AMS slot 1, Prusament PETG Clear in 2, colour a in 3
and colour b in 4, slice. Each
part's `extruder` is patched into `Metadata/model_settings.config`, the
assembler's per-part recentring is undone with measured translations, and the
result is verified numerically against the source solids plus round-tripped
through the CLI. Needs `/Applications/BambuStudio.app`; without it only the
vendor-neutral `cap_<n>.3mf` + per-part STLs are written (assign filaments by
hand in other slicers).

Because the cap prints top-plate-down, all bodies meet in the first
layers against the plate; the outer face comes out as one smooth plane. There
is no clear layer over or under the inlays — the first layer is already the
final colour. A washed-out colour means the coloured PETG itself is
translucent at 0.64 mm: deepen with `--depth` (up to 0.80) at the cost of
thinner cover above.

The 3MF is written by the script itself: one mesh object per body (libraries
explode the glyphs into a dozen objects), tessellation **welded** (OCCT
duplicates vertices per face; 3MF importers trust the index buffer and the
cracks sliced into "floating region" warnings) and refused if any non-manifold
edge remains. Lettering defaults to **Verdana** with the full Hungarian glyph
set; hairline strokes are lifted by dilation and any printable feature under
0.58 mm is refused. Icons are parametric geometry, no emoji fonts. The cap's
closure, seal and envelope are untouched — `build_cap()` is imported, not
copied.

## Files

| File | Role |
|---|---|
| `hen_tag_enclosure.py` | All geometry. `Params` at the top holds every dimension. |
| `board_holyiot_25008.py` | Board constants taken from the manufacturer's STEP model (not committed); `verify.py --board-step PATH` re-extracts them and fails on drift. |
| `hen_tag_platform.py`, `collar_full.py` | Accessory-platform proposal parts (`../platform/`), nothing printed. They import `hen_tag_enclosure.py` and never change it. |
| `catalog.json` | Source of truth for the schemes, icons, centre/band patterns, zones and fees a patron may choose. `test_cap_marking.py` checks its ids against the generator's `ICONS`, `PATTERNS_CENTRE` and `PATTERNS_BAND`. The editor prototype's copy (`../editor/src/cap-editor/data/catalog.json`, refreshed with `pnpm sync:data`) is kept byte-identical by the catalogue's `tests/editor-data-parity.test.ts` (root `npm test`, in CI). The app ships a verbatim copy, chirp `packages/shared-types/src/i18n/hen-cap-catalog.json` (chirp ADR-0244, "Generator home"): a change here bumps `generator_version` in the same PR and is followed by a chirp PR with the copy. Nothing here checks chirp; `cap_batch.py` only refuses a batch whose `generator_version` differs, at print time. |
| `cap_design.py` | Catalog loader, `design_hash` (v2, with zone colours), `validate_design` (zone rules incl. no translucent filament on an opaque zone; retired schemes stay valid), `lock_price`; no build123d, shared by the batch CLI and the tests. |
| `cap_motifs.py` | Every icon and pattern as a parametric sketch (34 icons, 3 centre, 13 band patterns; the barcode band is seeded by the serial). |
| `check_motifs.py` | Printability of the whole motif library (erosion/dilation, extents, the 1.0 mm face rule with its `FACE_PENDING` list) plus a contact sheet (`--svg`). |
| `cap_svg.py` | Sketch → SVG: `out/layout.json` for the app preview, proof SVGs for the batch. |
| `bambu_project.py` | Pure-Python Bambu Studio plate writer (6 × 6 grid, part extruders, the farm's `PRINT_SETTINGS`, purge volumes and first-layer colour order from the scheme). |
| `bambu_template.py` | Regenerates `bambu/project_settings.json` from Bambu Studio's own P1S / 0.16mm Optimal / PETG Basic × 4 profiles. Rerun after a Bambu Studio update. |
| `cap_batch.py` | Batch JSON → plate, manifest, proofs; caches bodies per design hash; runs `slice_check.py` on the plate, which writes the print-ready `.gcode.3mf`. |
| `fixtures/batch_sample.json` | The shape of a `hen-cap-batch/1` file. |
| `test_bambu_project.py`, `test_cap_batch.py` | Writer and batch suites (structure, determinism, refusals, a real slice). |
| `verify.py` | Interference, fit, bayonet, wall thickness, seal and harness checks. |
| `slice_check.py` | Real-slicer check: warnings and open-air travel counts per part; `--project` writes the ready-to-print Bambu project. Needs Bambu Studio. |
| `out/hen_tag_revC_P1S.3mf` | Bambu Studio project: body, cap and both coupons on one P1S plate, print settings baked in. |
| `cap_marking.py` | Deterministic per-tag cap generator (number, message, icon or centre pattern, band pattern, zone colours, font). |
| `test_cap_marking.py` | Generator test suite: envelope, rejections, determinism. |
| `out/body.stl` / `.step` | Main housing. |
| `out/cap.stl` / `.step` | Bayonet cap. |
| `overhang.py` | Mesh check for exported STLs (standard library only): reports downward faces steeper than 45° above the bed. Every printable must print support-free in its exported orientation; run it on new or changed parts before handing STLs over. |
| `out/coupon_*.stl` | Bayonet + groove fit coupons. Print these first on a new printer: the pair has printed once (dimensions good, `../docs/lab/2026-09-10-thread-print-failure.md`), and per-hen caps rest on the end wall (`../docs/lab/2026-10-09-cap-rest-angle.md`). |
| `out/section_*.stl` | Half sections, for looking at the internals only. |

Import rule: `cap_design.py` imports no build123d (the batch CLI and the tests
load it fast); the platform modules import the enclosure, never the reverse.

## Changing dimensions

Every dimension lives in the `Params` dataclass. Derived values — groove depth,
lug and lip stations, cap diameter, Z stations — are computed properties, so changing
one input propagates correctly instead of leaving stale constants behind.

The values most likely to need correcting, all currently UNVERIFIED:

```python
holder_h   = 4.0    # holder + seated cell, off the PCB face (board itself: STEP)
oring_cs   = 1.50   # measure the ring you actually have
strap_w    = 8.80   # slot length; measure the elastic you actually have
strap_t    = 1.80   # slot width, along the spine
foam_t     = 2.0    # foam ring over a 1.79 mm gap to the board face
```

Board orientation is **holder down, PCB up** — the LED has to look out through
the cap, not at the bird. `cell_fill()` builds the crescent that retains the
holder; `strap_tabs()` builds the in-plane side tabs; `body_lugs()` and
`cap_channels()` build the two halves of the bayonet, both from one helical
sweep helper so their bearing faces share a pitch.

### Batch workflow

1. The app's admin page downloads a `hen-cap-batch/1` JSON: `batch_id`, one
   scheme, `generator_version`, and up to 36 locked caps (serial, icon *or*
   centre pattern, band pattern, zone `colours`, design hash, hen name).
   `fixtures/batch_sample.json` is the shape.
2. `uv run --python 3.12 cap_batch.py <batch.json>` refuses the whole batch on
   any problem (schema, `generator_version` ≠ `catalog.json`, unknown ids,
   icon + centre together, a zone colour rule, a translucent filament on the
   ring or number, duplicate serial, bad hash, > 36 caps; a retired scheme is
   accepted) and lists
   every offending cap; otherwise it writes `out/plates/plate_<id>_P1S.3mf`,
   `plate_<id>_manifest.csv` (`position,serial,hen_name,design_hash`,
   positions `1A`…`6F`) and `proof/<design_hash>.svg`, then slices the plate
   through Bambu Studio and reports objects, warnings, the time estimate,
   which filament slots extruded and which the AMS loads; it fails unless
   every assigned slot did both. A passing plate gets its sliced project next
   to it, `plate_<id>_P1S.gcode.3mf`.
3. Print `plate_<id>_P1S.gcode.3mf` as it is: open it in Bambu Studio (it
   opens in the preview) and send it, or copy it to the printer. Do not
   re-slice the `.3mf` in the GUI: the 2026-09-29 plate went through the GUI
   and came out with a 0.12 mm first layer, two walls and variable layer
   heights (`../docs/lab/2026-10-04-cap-face-first-layer.md`). The slots
   show the scheme colours: AMS 1 = the scheme's base filament,
   2 = Prusament PETG Clear, 3 = colour a, 4 = colour b (`catalog.json` names
   them; the batch CLI prints the mapping). The patrons' zone choices are in
   the geometry, so load those four spools and print; no per-cap setting
   exists. The plate carries the `Bambu PETG Basic @BBL X1C` preset in all
   four slots whatever the scheme (Prusament, Bambu PETG Basic, or Bambu
   PETG Translucent in `lavender`'s slot 4): temperatures and flow come from
   that preset, the AMS mapping on the printer decides which spool feeds
   each slot. Whether PETG Translucent prints well on the Basic preset is
   UNVERIFIED. The design face prints against the bed: compare a cap with its
   proof in the bottom view.
4. Upload the proofs to the app (file name = design hash).

The generator lives only in this tree on `main`: never generate a plate from
the archived Remeny-Farm/hen-tag-enclosure (chirp ADR-0244, "Generator home").
The `design_hash` v2 test vectors in `test_cap_marking.py` are repeated in
chirp `packages/shared-types/src/hen-cap.test.ts`: change both or neither.
Cap plates keep 0.16 mm layers on a 0.2 mm first layer; variable layer height
was decided against for the face on 2026-10-04 (`../DESIGN.md`, Print
Settings). No body-plate generator is committed: the 36-body plate of
2026-10-09 came from a one-off script.

Patterns must survive a 0.4 mm erosion (feature ≥ 0.8 mm) and a 0.4 mm
dilation without islands merging (gap ≥ 0.8 mm). On top of that every motif
is an inlay on the design face, the first layer, printed in 0.5 mm lines on
the textured plate, so `check_motifs.py` also asks for islands and gaps of
1.0 mm; the twelve motifs drawn to the older rule are listed in
`cap_motifs.FACE_PENDING` until they are redrawn. Every inlay together must
leave ≥ 99.9 % of the LED ring (r 8.5–11.5) clear; `cap_marking.py` checks all
three and refuses the design otherwise. Band patterns live in a fixed window
(−10°…190°) that clears a 5-digit serial by more than 40° each side.

After any change, re-run `verify.py` before printing. It is what caught the
assembly-path defect described in `../DESIGN.md`.

## Bayonet fit

Print the coupons and note where the cap stops turning. Ramp contact is 30°
clockwise from the entry slots and the end wall 55°. The caps rest on the end
wall (2026-10-09), so that is where the body's lugs put the number at 6
o'clock (`lug_phase`). A cap that stops much earlier means tight parts. Then
adjust and regenerate — do not file the parts:

```python
cam_lock   = 30.0   # deg of rotation to nominal contact; moves the cap's channels: new caps only
fit_lug_r  = 0.15   # radial clearance, lug crest to channel root: raise if the lugs bind
fit_lug_z  = 0.30   # axial clearance, lug top to channel ceiling
cam_rate   = 0.012  # ramp rise per degree; lower for a longer, softer tightening
```

Note for anyone extending this: the cap is modelled in its **resting** pose, on
the channel end walls, so the cap solid is already the assembled one. `verify.py` turns it back toward
the entry angle (`pose(phi)`) to prove the drop-on, the free run and the wedge.
Lugs and lips are swept along helices of the same pitch; change `cam_rate` and
both follow.
