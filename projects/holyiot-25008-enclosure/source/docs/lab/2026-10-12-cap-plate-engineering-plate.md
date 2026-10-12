# Lab Note: Cap Plates Move to the Engineering Plate

- **Date**: 2026-10-12
- **Author**: Hen-Tag Engineering
- **Status**: Generator switched and verified by slicer (CLI) and the test suite. Engineering Plate test plate not printed yet.

---

## Purpose & Objective

The farm prints on the Bambu Engineering Plate from now on (operator,
2026-10-12). Slice the cap plates for it, test it on one eggshell cap, and
have the rest of the eggshell caps ready on one plate for when that passes.
The four 2026-10-04 test caps count as done (operator), so every other hen
of `2026-09-29-eggshell-01` gets exactly one cap.

---

## Verified Evidence

### The 2026-10-04 test plate

| Observation | Source |
|---|---|
| `2026-10-04-eggshell-test` (39, 190, 370, 265) printed on the Textured PEI Plate and accepted | operator, 2026-10-12 |
| The four caps fitted to bodies; they turned past nominal to the channel end walls | photos of 2026-10-09, commit `d2c5d34` |

No measurements or face photos of this print are recorded here.

### Engineering Plate requirements

| Item | Value | Source |
|---|---|---|
| Glue | required before printing any material on the plate | [Bambu Engineering Plate](https://us.store.bambulab.com/products/bambu-engineering-plate), read 2026-10-12 |
| PETG | bed 60-80 °C, glue stick or liquid glue | same page |
| `eng_plate_temp` / `_initial_layer`, PETG Basic | 70 / 70 °C, the same as `textured_plate_temp` | `cad/bambu/project_settings.json` |

### The sliced test plate (Bambu Studio 02.08.02.60 CLI)

`plate_2026-10-12-eggshell-eng-test_P1S.gcode.3mf` (serial 455: `dots` centre
pattern and `dots` band, all three colours plus the clear window) against the
2026-10-04 one:

| G-code | 2026-10-04 | 2026-10-12 |
|---|---|---|
| `curr_bed_type` | Textured PEI Plate | Engineering Plate |
| `M140` / `M190` | S70 | S70 |
| `G29.1 Z-0.04 ; for Textured PEI Plate` | present | absent |
| `initial_layer_print_height` / `initial_layer_flow_ratio` | 0.2 / 1.05 | 0.2 / 1.05 |
| Slice check | PASS, 4 caps, 1 h 25 m | PASS, 1 cap, 52 m 16 s, slots used 1-4, AMS loads 1-4 |

`test_bambu_project.py`: 23 passed.

### The full plate

`2026-10-12-eggshell-02`: the other 31 caps of the `2026-09-29-eggshell-01`
manifest (all 36 less 39, 190, 265, 370 and the test cap 455). Test cap,
plate and the four done caps cover the 36 serials exactly once. The original batch JSON
was not kept; every design was recovered from its manifest design hash by
trying every icon or centre pattern, band and zone colour combination of the
catalogue: each hash matched exactly one valid design, and the four test
caps reproduced the 2026-10-04 batch file exactly.

Slice check: PASS, 31 objects, 5 h 24 m 54 s, slots used 1-4, AMS loads 1-4,
Engineering Plate at 70 °C; filament 41.94 / 9.92 / 12.13 / 11.21 g in
slots 1-4.

## Technical Interpretation

- The P1S start G-code lowers the nozzle 0.04 mm only on the Textured PEI
  Plate. On the Engineering Plate the 0.2 mm first layer prints at its
  nominal height; the 1.05 first-layer flow stays, since it only undoes
  PETG Basic's 0.95.
- The design face prints against the glue, so the glue film, not a texture,
  now sets the face finish.

## Key Decisions

1. `bambu_project.PRINT_SETTINGS["curr_bed_type"]` is `Engineering Plate`;
   the plate temperature comes from PETG Basic's `eng_plate_temp`.
2. The published `out/hen_tag_revC_P1S.3mf` and the part checks in
   `slice_check.py` stay on the Textured PEI Plate: it is the public
   download, and an Engineering Plate needs glue.

## Open Questions & Verification Items

1. Print `2026-10-12-eggshell-eng-test` from its `.gcode.3mf` on a glued
   Engineering Plate and compare with the Textured PEI caps: face fill,
   the `dots` centre and band, the edge chamfer, release from the plate.
2. Record which glue was used (stick or liquid); Bambu notes liquid glue
   gives a more even first layer.
3. Print `2026-10-12-eggshell-02` only after item 1 passes.
