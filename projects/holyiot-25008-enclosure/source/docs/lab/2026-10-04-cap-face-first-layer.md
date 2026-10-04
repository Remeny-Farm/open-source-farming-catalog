# Lab Note: Cap Faces Under-Extruded on the First Production Plate

- **Date**: 2026-10-04
- **Author**: Hen-Tag Engineering
- **Status**: Fixed in the generator; verified by slicer (CLI) and the test suites. Test plate not printed yet.

---

## Purpose & Objective

The `2026-09-29-eggshell-01` plate printed through on the P1S, but the design
faces came out rough and short of material. Find out what the printed faces
were sliced with, and make the generator produce a plate that prints the face
well without anyone setting anything by hand.

---

## Verified Evidence

### The printed caps (photos of serials 39 and 190, operator)

| Observation | Where |
|---|---|
| Separate, rounded lines with gaps between them | brown ring and white moon of 39 |
| Glossy pebbled surface | whole face of 190: the Textured PEI imprint plus the gaps |
| Frothy, bubbly clear ring | LED window of 39 |
| Band dots printed as hollow rings | `dots` band of 190 (1.2 mm dots) |
| Band pattern unreadable | `pixel` band of 39 (0.9 mm squares) |
| Brown streak on the white heart, a spot on the number | 190 |
| Strings; a clear flap off the rim | both |

The design of every cap on the plate was recovered from its design hash in
the manifest (36 of 36).

### What the plate was sliced with

The G-code of the photographed print was not kept. `Assembly_PETG_7h26m.gcode`
is the operator's GUI slice of the same plate on 2026-09-29 (lab note of
2026-09-30); its header against the plate the generator wrote:

| Setting | Generated plate | Printed G-code |
|---|---|---|
| `initial_layer_print_height` | 0.2 | **0.12** |
| `initial_layer_line_width` | 0.4 | 0.4 |
| `initial_layer_infill_speed` | 105 | 105 |
| `filament_flow_ratio` | 0.95 | 0.95 |
| `bottom_surface_pattern` | zig-zag | monotonic |
| `elefant_foot_compensation` | 0 | 0.15 |
| `enable_prime_tower` | 0 | 1 |
| `flush_volumes_matrix` | 280 everywhere | GUI auto-calculated, 123-563 |
| `wall_loops` | 3 | 2 |

### The settings template was not a P1S export

Every project this repository wrote carried the libslic3r defaults in place of
the P1S printer and partly in place of the process and filament:

| Setting | Template until today | Bambu's P1S / 0.16mm Optimal / PETG Basic |
|---|---|---|
| `machine_start_gcode` | `G28 ; home all axes` / `G1 Z5` | the P1S start sequence |
| `change_filament_gcode` | empty | `M620 S[next_extruder]A` ... |
| `single_extruder_multi_material` | 0 | 1 |
| `printable_height` | 100 | 250 |
| `filament_start_gcode` | blank | the PETG Basic block |
| `initial_layer_line_width` | 0.4 | 0.5 |
| `top_surface_pattern` / `bottom_surface_pattern` | zig-zag | monotonic line / monotonic |

Cause, reproduced: handed a system profile file (`--load-settings
"<...>/machine/Bambu Lab P1S 0.4 nozzle.json"`), the Bambu Studio CLI resolves
neither its `inherits` chain nor its `include` list (the P1S G-code lives in
the included templates) and falls back to libslic3r's defaults for whatever is
missing; the filament came out as `PLA`. Slicing the old template with the CLI
produces no `M620` (no AMS filament change) at all. A print sent from it would
have started with a bare `G28`.

### Bambu Studio's purge volumes

`libslic3r/FlushVolCalc.cpp` (v02.08.02.61) computes a purge from the two
colours: hue and saturation distance, the luminance step (towards light costs
far more than towards dark), combined as the third side of a 120 deg triangle,
at least 60, plus a floor. `Plater.cpp get_min_flush_volumes` sets the floor to
the nozzle volume less the filament the cutter retraction already removed:
107 - 18 mm x 2.405 mm2 = 63 mm3 for PETG Basic, 107 for Generic PETG (no
cutter retraction). Ported to `bambu_project.flush_volume`, it reproduces every
pair the GUI recalculated in the printed G-code exactly (10 of 10; the other two
pairs were the template's 280, never recalculated).

### After the fix (Bambu Studio 02.08.02.60 CLI)

| Check | Result |
|---|---|
| `test_bambu_project.py` | 23 passed: P1S machine, face settings, purge matrix vs the GUI's, first-layer order 2-1-4-3 in the G-code, tower x 236.6-252.4 |
| `test_cap_batch.py` | 20 passed, including the `.gcode.3mf` written by the slice check and removed when a new plate is written |
| `test_cap_marking.py` | 92 passed |
| `verify.py` | all checks passed; the cap has no unsupported overhang with the face chamfer |
| `slice_check.py` (parts, now on the resolved profiles) | travel counts unchanged (cap 16, coupon cap 6, body 66, coupon body 0) |
| `check_motifs.py` | all printable; 12 of 50 motifs below the face rule, listed |
| 4-cap test plate, serials 39 / 190 / 370 / 265 | PASS, 1 h 25 m, 24 filament loads, first layer 0.2 mm loading clear, white, beige, brown |

## Technical Interpretation

- The rough faces are the first layer being too thin for the textured plate:
  a 0.12 mm layer in 0.4 mm lines at 0.95 flow cannot fill the texture's
  valleys, so the lines stay round and apart, and small islands (the band
  dots) come out as a loop with nothing inside. None of those values came
  from the generator: the plate was re-sliced in the GUI on the operator's
  presets. The generated plate had the same 0.4 mm line and 0.95 flow,
  because its template was libslic3r's default and not Bambu's profile.
- Re-slicing in the GUI is also what merged the 2026-09-30 plate into one
  object. A plate that is printed exactly as the slice check sliced it
  removes both.
- Streaks and spots on the light zones are ooze and strings dragged across,
  not under-purging: a purge too small tints a whole island. The prime tower
  and drier filament address them; the purge matrix was nevertheless wrong
  (flat 280, brown to white needs 563).
- The `pixel` band's 0.9 mm squares are below two first-layer lines; the face
  rule names it and 11 more. The `dots` band (1.2 mm) meets the rule, yet
  printed hollow on the 0.12 mm layer; the test plate shows whether 0.2 mm,
  0.5 mm lines and 1.05 first-layer flow are enough.

## Key Decisions

1. `bambu/project_settings.json` is now Bambu's own export, regenerated by
   `bambu_template.py` (resolved profiles, per-filament arrays normalised to
   four Standard-nozzle entries, the shape the GUI loads). Every deviation
   lives in `bambu_project.PRINT_SETTINGS`.
2. The face settings: first layer 0.2 mm, 0.5 mm lines, first-layer flow
   1.05 (PETG Basic's 0.95 back to 1.0), 30/35 mm/s, monotonic, elephant foot
   0.15, no brim. Bambu values the face depends on are pinned.
3. A prime tower, 14 mm wide with a 1 mm brim at x 237.5, in the 22 mm strip
   right of the 6 x 6 grid; about seven layers tall, since colour changes stop
   at the top of the 1.1 mm top plate (window and zones run its full depth).
4. Purge volumes from the scheme's colours with Bambu's own formula, and the
   first layer loads the clear window first, then light to dark.
5. The slice check writes `plate_<id>_P1S.gcode.3mf` when, and only when, the
   plate passes (every assigned slot extrudes and is loaded by `M620`); a new
   plate deletes the old sliced file. That file is what gets printed.
6. `slice_check.py` loads the resolved profiles for the part checks and the
   published `out/hen_tag_revC_P1S.3mf`, which now carries the P1S start
   G-code; `out/cap_67_P1S.3mf` was regenerated from the new template.
7. A 0.30 mm chamfer at 50 deg on the design face's edge (`face_chamfer`):
   inside the outline where the first layer squashes outward; it starts at
   r 15.67, outboard of every marking (r <= 15.60).
8. Face rule in `check_motifs.py`: islands and gaps of 1.0 mm. The 12 motifs
   below it stay in the catalogue, listed in `cap_motifs.FACE_PENDING`; a
   listed motif that passes fails the check until it leaves the list.

## Open Questions & Verification Items

1. Print the test plate (`2026-10-04-eggshell-test`: 39 moon/pixel, 190
   heart/dots, 370 moon/stripes, 265 egg) from its `.gcode.3mf` and compare
   with the photos of 39 and 190. Tune `initial_layer_flow_ratio` from it.
2. Redraw or retire the 12 `FACE_PENDING` motifs (`pixel` and `stripes` are
   among the most chosen bands: 2 and 8 of 36 on the eggshell plate).
3. Calibrate flow for Prusament PETG Clear in slot 2; it runs on the PETG
   Basic preset (flow 0.95).
4. Open a generated `.3mf` in the Bambu Studio GUI once and confirm it loads
   four filaments with the new template (the CLI does; the GUI was not
   checked).
5. The sliced file carries the writer's 1 x 1 placeholder as its thumbnail;
   the printer shows no picture.
