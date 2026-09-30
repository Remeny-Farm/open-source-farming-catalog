# Lab Note: Five Caps Below the Bed, Thirty-One in the Air

- **Date**: 2026-09-30
- **Author**: Hen-Tag Engineering
- **Status**: Fixed in the generator; batch suite reproduces the fault and passes. Not reprinted yet.

---

## Purpose & Objective

The first production plate (`2026-09-29-eggshell-01`, 36 caps) failed on
the P1S. The printer laid about 1 mm on five caps (serials 435, 305, 1878,
88, 276), then moved to the other caps and started their faces, and the
print failed. Find out why only five caps started on the bed.

---

## Verified Evidence

The G-code the printer ran (`Assembly_PETG_7h26m.gcode`, Bambu Studio
02.08.02.60, 57 layers, 7 h 26 m), extrusion attributed to the 36 cap
centres found from the outer-wall arcs:

| Layers | Z | Caps extruded |
|---|---|---|
| 1-10 | 0.12-1.09 mm | 5 (the serials above) |
| 11 onwards | from 1.25 mm | all 36 |

So 31 caps started their design face 1.1-1.25 mm above the bed, with
nothing under them.

The plate the generator wrote (`plate_2026-09-29-eggshell-01_P1S_colours.3mf`),
lowest vertex per part, identity component transforms:

| Caps | Shell | Window and inlays |
|---|---|---|
| 31 caps | 0.00-7.50 mm | 0.00-1.10 mm |
| 435, 276, 305, 1878, 88 | 0.00-6.40 mm | -1.10-0.00 mm |

The five designs are the only ones on the plate with no base colour on the
design face: the ring on `a` or `b`, and no zone that draws anything in
`base` (435 has `band: base` but no band pattern).

## Technical Interpretation

- `cap_batch.build_bodies` flipped each cap face-down and dropped it onto the
  bed by the **shell's** lowest point. When no face zone is base-coloured,
  the shell ends at the underside of the 1.1 mm top plate, so the offset put
  the shell on z 0 and the window and inlays 1.1 mm below it.
- The G-code holds the plate as one object named `Assembly`. Laid on the
  bed as one piece, its lowest points (the five sunken faces) went to z 0
  and every other cap was lifted 1.1 mm. The first ten layers were the five
  caps' faces alone; at 1.25 mm the other 31 faces started in the air.
- Sliced as generated (36 separate objects), the same plate is harmless:
  Bambu Studio drops each object onto the bed on its own. Slicing the
  generated plate with the CLI put all 36 caps on the first layer (47
  layers, 7.56 mm). The fault needs both the sunken caps and the plate
  becoming one object, which happened in Bambu Studio before this print;
  how it was merged is not known. A slicer first-layer check on the
  generated plate would therefore not have caught it.
- `cap_marking.py` placed the single-cap project the same way.
- The body cache (`out/cache/<fingerprint>/<design hash>`) holds the
  oriented meshes, but `cap_batch.py` was not in the fingerprint. After the
  fix, a rerun would still have served the sunken bodies from the cache.

## Key Decisions

1. Both generators drop the whole cap (every part's lowest point) onto the
   bed.
2. `cap_batch.py` joins the cache fingerprint, so any change to the batch
   generator discards cached bodies.
3. `write_plate` refuses a plate on which any cap's lowest point is not at
   z 0, so a sunken cap can no longer reach a plate file at all
   (`test_bambu_project.py` covers the refusal).
4. `test_cap_batch.py` checks that every cap on the plate starts at z 0,
   including a design with no base colour on its face. Before the fix that
   design's cap started at -1.1 mm.

## Other Differences in the G-code (observed, not the cause)

The printed G-code was sliced with different settings than the generated
plate: variable layer heights (0.12 mm first layer, then 0.08-0.16 mm
steps), 2 walls instead of 3, `reduce_crossing_wall` off. Variable layers
break the 0.64 mm inlay = 4 x 0.16 mm assumption. Slice the generated plate
as it is.

## Open Questions & Verification Items

1. Regenerate the eggshell-01 plate with the fixed generator, check in Bambu
   Studio that every cap sits on the bed, then print.
2. Print and check the five caps without a base colour on their face.
