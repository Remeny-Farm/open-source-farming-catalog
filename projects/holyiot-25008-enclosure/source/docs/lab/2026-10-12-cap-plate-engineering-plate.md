# Lab Note: Cap Plates Move to the Engineering Plate

- **Date**: 2026-10-12
- **Author**: Hen-Tag Engineering
- **Status**: Generator switched; the face's first layer now gets one wall. 455 printed rope-like round its dots with three walls; 420, which has no holes, printed a fused disc on the same plate. A one-wall 455 plate is sliced and waits for printing. Do not print `2026-10-12-eggshell-02`: it was sliced with three walls.

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
slots 1-4. Sliced with three walls on the first layer.

### The 455 test print (operator photos, 2026-10-12)

Printed from `plate_2026-10-12-eggshell-eng-test_P1S.gcode.3mf` on the
Engineering Plate with a glue stick, bed levelling on, dried filament
(operator).

| Observation | Where |
|---|---|
| Beige lines round, apart and rope-like, with gaps between them | disc and upper band, around the brown dots |
| Straighter, smoother lines, gaps still visible | the lower band, which has no dots |
| Solid, smooth glyphs | the white number |
| Glittery, bubbly surface | inside the brown dots |

First layer from the G-code, against the accepted 2026-10-04 plate. Lengths
include the walls' arc (G2/G3) moves; a first version of this table counted
straight G1 moves only.

| | 2026-10-04 (Textured PEI) | 455 (Engineering Plate) |
|---|---|---|
| Layer, line width, flow | 0.2 mm, 0.5 mm, 1.05 | the same |
| Deposited section, all features | 0.086-0.102 mm3/mm | 0.076-0.102 mm3/mm |
| Inner-wall paths of the busiest filament | brown, 147 for four caps, 7.9 mm mean | beige, 118 for one cap, 5.1 mm mean |
| Retractions of that filament on layer 1 | 251 for four caps | 159 for one cap |

The 0.2 x 0.5 mm line at this flow deposits 0.091 mm3/mm, exactly one
0.2 mm layer at 0.457 mm spacing: no margin for a gap larger than 0.2 mm.

### The A/B print (operator photos, 2026-10-12)

`plate_2026-10-12-eggshell-eng-ab_P1S.gcode.3mf` (455 at 1A, 420 at 2A,
three walls) printed unchanged, glue stick again. Photos of 420 only.

| Observation on 420 | Where |
|---|---|
| Continuous surface, lines fused | beige disc |
| A band of hairline gaps between straight lines | across the middle of the disc |
| Beige blob over the clear window; cause not found in the G-code | disc edge toward the number |
| Solid glyphs | brown number |

First layer of each cap from the same G-code (exclude-object labels 100 and
101), beige only:

| | 455 | 420 |
|---|---|---|
| Bottom surface | 131 mm | 350 mm in 1 path |
| Inner wall | 596 mm in 118 paths, 5.1 mm mean | 95 mm in 2 paths |
| Outer wall | 421 mm in 42 paths | 52 mm in 1 path |
| Retractions | 151 | 3 |
| Face covered with every line drawn at its width | 99.3 % | 99.6 % |

### One wall on the first layer

Bambu Studio's `only_one_wall_first_layer` (default 0) set to 1, 455 sliced
alone (`plate_2026-10-12-eggshell-eng-onewall_P1S.gcode.3mf`):

| Beige, layer 1 | three walls | one wall |
|---|---|---|
| Bottom surface | 131 mm in 12 paths | 757 mm in 24 paths, 31.5 mm mean |
| Inner wall | 596 mm in 118 paths | none |
| Outer wall | 421 mm in 42 paths | the same |
| Volume | 108 mm3 | 108 mm3 |
| Retractions | 159 | 69 |
| Face covered | 99.3 % | 99.3 % |

Slice check: PASS, 52 m 9 s, Engineering Plate, `M190 S70`, no
`G29.1 Z-0.04`, `wall_loops` 3 from layer 2. `test_bambu_project.py`: 24
passed; `test_cap_batch.py`: 20 passed.

## Technical Interpretation

- The P1S start G-code lowers the nozzle 0.04 mm only on the Textured PEI
  Plate. On the Engineering Plate the 0.2 mm first layer prints at its
  nominal height; the 1.05 first-layer flow stays, since it only undoes
  PETG Basic's 0.95.
- The design face prints against the glue, so the glue film, not a texture,
  now sets the face finish.
- The A/B plate separates the two causes left open after 455. Same plate,
  glue, flow and filament: 420's hole-free beige, one long straight path,
  fused; 455's beige, short wall loops round 31 dot holes, did not. The
  slicer covers both faces alike, so the gaps come from printing short
  variable-width loops, each after a retraction, at nominal height.
- The 2026-10-04 plate had the same kind of structure (brown, 147 short
  inner-wall paths) and was accepted on the Textured PEI Plate. Its 0.04 mm
  lowering prints the 0.2 mm layer about 0.16 mm high, so each line spreads
  about a quarter wider and closes such gaps. The Engineering Plate lost
  that cover.
- With one wall the beige between the dots becomes straight bottom-surface
  lines, the structure that fused on 420. The hairline gaps across 420's
  middle show that even straight lines have little margin at nominal
  height; left alone here, one change at a time.

## Key Decisions

1. `bambu_project.PRINT_SETTINGS["curr_bed_type"]` is `Engineering Plate`;
   the plate temperature comes from PETG Basic's `eng_plate_temp`.
2. The published `out/hen_tag_revC_P1S.3mf` and the part checks in
   `slice_check.py` stay on the Textured PEI Plate: it is the public
   download, and an Engineering Plate needs glue.
3. `only_one_wall_first_layer` is 1: the face gets one wall; the body keeps
   three walls from layer 2.

## Open Questions & Verification Items

1. Print `2026-10-12-eggshell-eng-onewall` (455 alone, 52 m), glue stick,
   otherwise unchanged. Fused beige round the dots confirms the fix; then
   regenerate `2026-10-12-eggshell-02` with it, less 455.
2. Accept or reject 420 (hairline gaps, blob); accepted, it leaves
   `2026-10-12-eggshell-02`.
3. If straight lines still show hairline gaps on the one-wall 455, the next
   single change is the first-layer flow or liquid glue, which Bambu says
   gives a more even first layer. All three prints so far used a glue stick.
4. Watch whether the beige blob at the disc edge comes back.
5. Print `2026-10-12-eggshell-02` only after item 1 passes.
