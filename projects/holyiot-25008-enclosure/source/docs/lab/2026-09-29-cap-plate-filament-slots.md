# Lab Note: Cap Plate Loaded One Filament

- **Date**: 2026-09-29
- **Author**: Hen-Tag Engineering
- **Status**: Fixed in the generator; verified by slicer (CLI). Not printed yet.

---

## Purpose & Objective

The first production batch plate (36 caps, one scheme) opened in Bambu
Studio with every part of every cap on filament 1. The operator could not
tell which cap needed which colour. Find out why the per-part filament
assignment was lost and make the generator produce a plate that opens with
the four slots already in place.

---

## Verified Evidence

Bambu Studio 02.08.02.60, P1S 0.4, the 36-cap `eggshell` plate:

| | Before | After |
|---|---|---|
| Per-part extruder in `model_settings.config` | 1 / 2 / 3 / 4 | 1 / 2 / 3 / 4 (unchanged) |
| `filament_colour` / `filament_type` entries | 1 (`#00AE42`, `PLA`) | 4 (scheme colours, `PETG`) |
| Filaments the CLI extruded (`result.json`) | 1 | 4 (48.1 / 6.6 / 11.9 / 7.0 g) |
| Filament changes | 0 | 20 |
| Bed type | Cool Plate | Textured PEI Plate |
| Layer height | 0.20 mm (37 layers) | 0.16 mm (47 layers) |
| Estimated time (CLI) | 3 h 59 m | 6 h 17 m |
| Slicer `[error]` lines | 1 (Arachne wall reversal) | 0 |

The GUI showed the same collapse as the CLI: all 36 caps rendered in the
slot 1 colour.

## Technical Interpretation

- Bambu Studio counts a project's filaments from the per-filament arrays in
  `project_settings.config`, not from `filament_settings_id`. The template
  held four `filament_settings_id` entries but one `filament_colour`, one
  `filament_type` and one of each other per-filament array, so the project
  loaded one filament and every part fell back to slot 1. The per-part
  extruders in `model_settings.config` were right all along.
- The 2026-09-14 bisect ("widening `filament_colour` breaks the CLI export")
  widened arrays one at a time. Widening every per-filament array together,
  from the stock `Bambu PETG Basic @BBL X1C` profile, slices cleanly.
- Once the filaments are PETG the CLI refuses the template's Cool Plate
  ("Cool Plate does not support filament 1"); the farm prints on the
  Textured PEI plate.
- The template's process is "0.16mm Optimal" but its `layer_height` was 0.2;
  the GUI showed 0.16 while the CLI sliced at 0.2. The inlays are
  0.64 mm deep, four 0.16 mm layers, so the template now says 0.16.
- The single-cap reference `out/cap_67_P1S.3mf` carries the same
  one-filament arrays; the 09-14 note's "no tool changes for any project" was
  this bug, not a CLI limit.

## Key Decisions

1. `bambu/project_settings.json` carries every per-filament array four
   entries wide; `write_plate` refuses a template that does not, and patches
   the scheme colours into slots 1-4 (base, clear, a, b).
2. `test_bambu_project.py` and `slice_check.py` read the slicer's
   `result.json` and fail unless every assigned slot extrudes. A collapsed
   plate slices without a warning, so this is the only guard.

## Operator Note

The patron's zone choices are already in the geometry: each cap is cut into
up to four parts by role, and each part is assigned to its slot. The operator
loads the scheme's four filaments (AMS 1 base, 2 Prusament Clear, 3 `a`,
4 `b`) once per plate and never needs the individual designs. The design face
prints against the bed, so check a cap against its proof SVG in the bottom
view.

## Open Questions & Verification Items

1. Print the first plate and confirm in the GUI and on the printer that the
   four slots map as above.
2. Regenerate `out/cap_67_P1S.3mf` from the fixed template when the single-cap
   project is next touched.
