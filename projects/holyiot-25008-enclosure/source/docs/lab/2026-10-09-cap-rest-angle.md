# Lab Note: The Caps Rest on the End Wall, Number at Five O'Clock

- **Date**: 2026-10-09
- **Author**: Hen-Tag Engineering
- **Status**: Fixed in the body (lugs turned 25°) and confirmed on a printed body (2026-10-12). Caps unchanged.

---

## Purpose & Objective

The four eggshell test caps of 2026-10-04 (serials 39, 370, 190 and 265) were
screwed onto revision D bodies until they stopped. The generator draws the
number at 6 o'clock, between the strap tabs, but on every cap it ended up near
5 o'clock. Find where the cap actually stops, and correct it on the body
without reprinting the per-hen caps.

---

## Verified Evidence

Top-down photos of each assembled tag were measured against the cap's proof
SVG. Each angle is the number's position relative to the tab axis, minus its
design position. Positive is anticlockwise seen from above; the photos are
good to about ±3°.

| Serial | Number centroid | Whole lettering ring (cross-correlation) |
|---|---|---|
| 39 | +37.4° | +37° |
| 370 | +35.9° | +35° |
| 190 | +32.8° | +30° |
| 265 | +31.7° | +32° |

None of the caps comes off when pulled straight up in that pose.

Geometry, measured on the printed plate's 3MF and on the body STLs:

- body lugs at 0/120/240°, lug 0 on the tab axis
- cap entry slots at −30/90/210°
- the number at 270°

### Printed body with the turned lugs (2026-10-12)

One body from `plate_2026-10-12-body-test_P1S.gcode.3mf` (the fix, lugs at
25/145/265°), Prusament PETG Clear on the Textured PEI Plate. A 2026-10-04
test cap screwed on stopped with its number at 6 o'clock (operator,
2026-10-12: "perfect"). Which test caps were tried is not recorded, and the
angle was not measured from a photo.

---

## Analysis

- In the model, turning clockwise from the entry slots reaches nominal ramp
  contact after 30° (the cap's modelled pose) and the channel end wall after
  55°, which is 25° further.
- The tabs make the body look the same turned over, and there are three lugs.
  Together they put the number on a 60° lattice: 245° + δ + 60°·m, where δ
  is the lug phase. With δ = 0 the lattice points either side of 6 o'clock
  are −25° and +35°.
- All four caps sit at +35° ± 3°, so they ran past nominal contact to the end
  wall. The only other pose that gives +35° is the entry slot's side wall
  (+34°, after an anticlockwise turn), and there the cap lifts off. None did.
- In the model, the ramp at the end wall is 0.30 mm into the lug. Reaching it
  means the printed pair is at least that much looser axially. This is inside
  the window the ramp was sized for (−0.36..+0.30 mm).
- The end wall is printed in XY, so it is a hard and repeatable stop. The
  scatter across the four caps is within the photos' error.

---

## Decision

- **Body only.** The lugs move by `lug_phase` = `cam_travel` − `cam_lock` =
  25°, to 25/145/265°. The cap's modelled pose, with the number at 6 o'clock,
  is now the end-wall pose. The lattice becomes 270° + 60°·m, so the number
  lands at 6 or 12 o'clock with the body either way round.
- **The cap is untouched.** Channels, lips and marking do not move, and
  `cap.stl` is byte-identical. Printed caps go onto the new body as onto the
  old one: same drop-in, then the same 55° turn to the same stop.
- `cam_lock` is not re-tuned. It lays out the cap's channels, so changing it
  would leave every printed cap behind.
- `verify.py` has a new check, "cap rests on the end walls". It probes just
  outside the bore and above the lips, where only the end wall can meet a lug.
  It reads 0.000 mm³ 1° short of the rest pose and 0.026 mm³ 2° past it. On
  the old body (phase 0) the probe reads 0.000 mm³ past the modelled pose, so
  the check fails.
- The assembled-interference check now collides the cap at nominal contact,
  where it did before. At the rest pose the model's ramp overlap is real by
  design.

---

## Open

- Done 2026-10-12: a printed body with the turned lugs puts a test cap's
  number at 6 o'clock (above).
- The axial play at the stop has not been measured; the foam ring takes it up.
  If a cap rattles at the stop, report it before changing anything.
