# Hen Tag Enclosure — Design Specification

## Purpose & Status

Parametric two-part enclosure for the Holyiot 25008 tag, generated from code in
`cad/hen_tag_enclosure.py`.

- **Status**: Revision C. Geometry generated, machine-verified, exported.
  **The coupon pair has been printed once (dimensions good). Four per-hen
  caps printed on 2026-10-04 run on to the channel end walls at 55° and stay
  on when pulled (lab note 2026-10-09), and a body with the lugs turned 25°
  puts the number at 6 o'clock (2026-10-12). The O-ring seal, water
  resistance and the tabs under load are untested.**
- **Revision A was printed and fitted** on a Bambu Lab P1S — dimensions good,
  and its thread mated on that one pair. See
  `docs/lab/2026-08-28-enclosure-print-trial.md`. Later caps tore along the
  thread, whose ridges compute to less than one extrusion wide; the thread
  was replaced by a bayonet on 2026-09-10. See
  `docs/lab/2026-09-10-thread-print-failure.md` and decision 9. The board
  outline, thickness and parts come from the manufacturer STEP (2026-09-23,
  `cad/board_holyiot_25008.py`).
- **Blocking caveat**: the holder (Ø21 × 4.0 mm) and the total stack height
  are still operator caliper readings with an unresolved ambiguity; the
  ceiling tolerates a holder of 3.79–4.19 mm. See
  `docs/lab/2026-08-28-enclosure-board-measurements.md`.

---

## Summary

| | |
|---|---|
| Assembled envelope | **40.14 × 31.94 × 8.70 mm** (Ø31.94 body, tabs to 40.14) |
| Printed mass (PETG) | **5.01 g** (body 2.71 + cap 2.30) |
| Assembled mass | **9.92 g** — within the 10 g target (board from the manufacturer STEP; about 1.2 g, the board parts, holder and O-ring, still estimated) |
| Orientation | Holder **down** toward the harness, PCB **up**, LED outward |
| Sealing | Radial NBR O-ring, **ID 26.74 × CS 1.50 mm** |
| Closure | Bayonet: 3 lugs × 20°, 0.80 mm proud, 55° clockwise to the channel end walls over self-locking helical ramps |
| Material | Transparent PETG. Conductive/CF filament remains prohibited. |

```
                              Ø31.94
              ┌──────────────────────────────┐   cap top 1.10
              │ ▁▁▁  clear LED ring  ▁▁▁     │   foam recess 0.30
         ═════╪══════════════════════════════╪═════  ceiling z=6.60
              │      ░░░   S1   ░░░          │   foam RING OD16/ID12 x 2.0
              │ ▓▓▓▓▓ PCB Ø25 ▓▓▓▓▓ z=4.81/6.41│   ← LED faces the cap
         ○────┤ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ z=4.0 ├────○  O-ring, z=3.71…5.74
              │███┌──────────────────┐███████│   seals on band r=13.70
              │███│ CR2032 + holder  │███████│   ███ = fill, holds the holder
    ▓▓▓▓▓▓▓▓▓▓╪███│ Ø21, offset 2.0  │███████╪▓▓▓▓▓▓▓▓  3 lugs z=1.80…3.10
    ┌─────┐   │▁▁▁└──────────────────┘▁▁▁▁▁▁▁│   ┌─────┐  floor 1.00
    │  ▄  │═══╡        cell rests on the floor  ╞═══│  ▄  │  ← in-plane tabs
    └─────┘   └──────────────────────────────┘   └─────┘     slot 8.8 x 1.8
                    FLAT UNDERSIDE                           bar 1.5
```

---

## Design Decisions

### 1. Radial seal, not the axial face seal

`docs/requirements.md` originally specified an axial face seal on an NBR 30 × 2 mm ring.
A face seal must sit **outboard of the cap skirt**, which forces a flange out to
Ø36 around a Ø25 board. Modelled and weighed, the three options were:

| Variant | OD | Plastic | Assembled |
|---|---|---|---|
| Face seal, NBR 30×2 (original spec) | 36.0 mm | 6.01 g | 11.88 g |
| Face seal, NBR 24×2 | 31.1 mm | 4.40 g | 10.26 g |
| **Radial seal (adopted)** | **31.9 mm** | **4.32 g** | **10.19 g** |

The flange was ~1.7 g of pure overhead. The radial seal needs none.

> Those masses compare the three sealing strategies on identical revision A
> bodies. Revision B is heavier (5.05 g) because of the cell fill and the tabs;
> the comparison between strategies is unaffected.

Second advantage, specific to FDM: a radial seal's compression is set by the bore
diameter, not by how hard the cap is tightened. The face seal needed a stop
flange precisely to stop the operator from shearing the ring — a failure mode the
radial arrangement does not have.

### 2. Closure low, seal high

The first layout put the seal below the thread and **could not be assembled**.
The cap's internal thread crests sat at r 14.00; sliding them down past a
sealing band at r 14.30 is a collision. Caught by `verify.py`, not by eye.

Inverting it fixes the assembly path and adds a second benefit: **the O-ring
never travels across the closure**, which would shred it. The rule survived
the change from thread to bayonet (decision 9) unchanged: the lugs sit at
z 1.80–3.10, the groove starts at z 3.91, and the checks that enforce it are
`cap bore clears the seal band` and `O-ring never crosses the lugs` in
`verify.py`.

### 3. Holder down, PCB up

The LED sits on the PCB face. With the board the other way up it pointed at the
bird and was unreadable. Inverted, the PCB looks into the transparent cap and
the LED can be read on a closed tag.

This also removes an old awkwardness. Because the holder is internally tangent
to the PCB, **no rotationally symmetric ring lands on bare PCB all the way
round** when the holder faces up — at the tangent point the holder reaches the
board edge exactly. With the holder underneath, the PCB presents a full Ø25 disc
to the cap, so a plain annular clamp works.

### 4. Fill around the cell

The crescent of cavity the offset holder does not occupy is filled solid from
the floor to just under the PCB face. That fill is what holds the holder: 100 %
of the holder's circumference is backed either by fill or, at the tangent point,
by the cavity wall itself.

The fill deliberately stops 0.20 mm **short** of the PCB rather than seating it.
The board still rests on its own holder, and the fill never touches whatever
components sit on that face (the STEP's generic clip model does not show them
reliably). It costs about 0.7 g.

### 5. Tolerance lives in a foam ring, not a pad

A 2.0 mm closed-cell foam **ring**, OD 16 × ID 12, against the cap ceiling.
It bears on the board's r 6–8 zone: on the parts there (0.5–1.1 mm, Q1 at
worst, 66 % local squeeze) and just on bare board (11 %). Holder heights from
3.79 mm (foam leaves bare board) to 4.19 mm (the ceiling reaches S1) assemble,
so a wrong holder reading is fixed by changing foam, not by reprinting.

**Geometry from the manufacturer STEP (2026-09-23).** The rev A ring was OD 25 ×
ID 16 × 1.0 over a 2.0 mm "board", both from a caliper. The Holyiot STEP
(`cad/board_holyiot_25008.py`) showed the board is **0.81 mm** with parts up
to **1.60 mm** (the tactile switch S1, dead centre), so the old ring hung
1.1 mm above the board face and held nothing, and its r 8–12.5 band sat
**right on the LED** (r 8.78–10.91). The ring moved inboard, under the opaque
core, and doubled in thickness. The ceiling did not move: z 6.60 closed over a
real board on revision A, and leaves **0.19 mm over S1**.

Ring rather than disc: the switch sits inside the ID. A cap pressing S1 is the
failure to watch for if the holder turns out taller than 4.0 mm.

### 6. Battery retention comes free

At the tangent point the cell edge is flush with the PCB edge, so the cavity wall
sits directly against the cell and blocks the direction it would slide out. With
the holder now facing down, the cavity floor also backs the cell face, pressing
it into its clip. No retention feature was added because none is needed.

### 7. In-plane side tabs for the harness

Two flat tabs in the plane of the base, each with a transverse slot and a bar at
the tip that the elastic wraps. The tag's **underside is completely flat** —
verified at 0.000 mm³ of material below the floor plane.

This replaced under-floor bridges, which stood 2.8 mm proud of the base. Losing
them took the assembled height from 11.50 mm to **8.70 mm**; the tabs widen the
tag to 40.14 mm across.

The tab root is only as thick as the base flange (1.2 mm), because above that
and inside the cap radius the space belongs to the rotating cap skirt. That root
carries harness load in tension, not bending, across 13 mm of width — so the
thin section is not the weak point it looks like. **Untested under load.**

### 8. Customer cap: base shell, clear LED ring, zone colours

`cad/cap_marking.py <number>` generates the per-hen cap from the patron's
design. It writes the vendor-neutral `out/cap_<n>.3mf` and, with Bambu Studio
installed, the pre-registered project `out/cap_<n>_P1S.3mf`. The cap is cut
into up to four bodies, one per AMS slot:

| Body | Slot | What it is |
|---|---|---|
| `cap_<n>` | 1, scheme base | the shell: closure, seal and envelope untouched |
| `window_<n>` | 2, Prusament PETG Clear | the LED ring r 8.5–11.5 through the whole top plate, plus any zone set to clear |
| `a_<n>` | 3, scheme colour a | the zones and inlays set to `a` |
| `b_<n>` | 4, scheme colour b | the zones and inlays set to `b` |

The zones are `ring`, `number`, `disc`, `centre` and `band`
(`cad/catalog.json`), and `--colours` gives each one `base`, `a`, `b` or
`clear`. The number (4.5 pt, 1–5 digits) bends along the bottom arc between
r 11.60 and 15.40. The staff-only `--top` message (3.6 pt, ALL CAPS) runs
along the top arc, out to r 15.60. Font sizes are fixed: input that does not
fit is refused with the measured numbers. The generator is deterministic
(byte-identical output for identical input) and is tested by
`test_cap_marking.py` (92 checks passed on 2026-10-04).

Earlier layouts did not last. The first print trial (opaque shell, clear LED
ring, a 2.9 mm lettering band) proved the multi-colour registration, but its
lettering was unreadable. A whole-clear shell followed. The customisation
design of 2026-09-14 (decision 10) went back to the clear ring, with the
number in 4.5 pt outside it.

Because the cap prints top-plate-down, all bodies meet in the first layers
against the plate: the outer face is one smooth plane, the number reads
correctly from outside, and the window is flush on both faces. The inlays
stop 0.46 mm short of the cavity; the window and any zone in a, b or clear
run through the whole plate.

**Why a ring.** The LED centre sits at r 9.84 (manufacturer STEP; the caliper
said 10.0), at −60° in the body frame. Its *angle* relative to the cap is not controlled —
the board can turn a few degrees in its pocket, and the cap's stop angle
carried print tolerance at 360° per millimetre of thread pitch (the bayonet
ramp brings that down to about 4° per 0.05 mm, decision 9) — so a local window
would need bench-proven angular registration. A ring at the LED radius lights
wherever the LED is and needs no alignment at all. Its width only has to
cover the radial tolerance chain, which is small and known:

| Term | ± mm | Source |
|---|---|---|
| board radial play in the cavity | 0.30 | `fit_board` |
| cap concentricity, set by the seal bore | 0.10 | `fit_seal_r` |
| LED emitting-area half-size | ~0.8 | 0606–2020 package, UNVERIFIED |
| **half-width needed** | **1.2** | → 2.4 mm minimum ring |

The ring is fixed at **3.0 mm** (r 8.5–11.5, `cap_marking.LED_RING`): 0.3 mm
margin each side and ~7 extrusion widths, so the colour boundary prints crisp.
There is no CLI override, and no inlay may cover more than 0.1 % of it.

**Coin-style lettering.** The number does not sit in the centre: it bends
along the band outside the clear ring (r 11.60–15.40), like the lettering on a
coin, with glyph tops toward the centre. The optional staff-only message
(`--top "Szeretlek Bözsi!"`) runs along the top arc with tops outward, out to
r 15.60. Both read left to right, the gaps falling on the tab axis. The centre
inside the ring carries an icon or a centre pattern (`--icon none` leaves it
empty). Font sizes are fixed (4.5 pt number, 3.6 pt message), and glyphs are
dilated so hairline strokes print; a feature under 0.58 mm is refused. A
message longer than 200° of arc is refused rather than shrunk into
illegibility.

**What the ring costs.** The shell's central disc is joined to the rest of the
shell only through the clear ring — fine for printing (same PETG, different
pigment, fused in place) but worth knowing. The foam ring cannot stay at the
rim, which is exactly the LED radius: it moves inboard to **OD 16 / ID 12**,
where it bears on the board's r 6–8 zone. The manufacturer STEP shows what
sits in that zone (decision 5); the tactile switch near the centre is inside
the ID.

### 10. Per-hen customisation: patterns, catalog, batch plates

Patrons choose a colour scheme (a base filament plus two free colours, a and
b, beside the clear LED ring), an icon *or* a centre pattern, a top-band
pattern and a colour per zone; the serial number is always on the cap.
Everything a patron may choose is in `cad/catalog.json`, mirrored in the app.
Locked designs are batched one scheme per plate, 6 × 6 on the P1S, by
`cad/cap_batch.py`; a 36-cap plate slices to 36 objects in an estimated
6 h 17 m with 20 filament changes
(`docs/lab/2026-09-29-cap-plate-filament-slots.md`). The first production
plate printed and failed, and its causes were fixed in the generator (lab
notes 2026-09-30, 2026-10-04); the 2026-10-04 four-cap test plate was
accepted on 2026-10-12. Design, constraints and the chirp-side requirements:
`docs/superpowers/specs/2026-09-14-hen-cap-customisation-design.md`.

### 9. Bayonet, not a thread

Revisions A/B closed with a Tr28.6 × 1.0 trapezoidal thread. One pair printed
and mated on 2026-08-28; the caps printed since tore along the thread and the
operator reported the flanks as "too steep". Computed from the revision B
`Params`, the thread was never inside what a 0.4 mm nozzle can lay down:

| Feature | Rev B thread | Why it tears |
|---|---|---|
| flank angle from horizontal | 15° | a 75° overhang; each ridge is a 0.55 mm shelf ~3 layers tall |
| male crest width | 0.35 mm | below one 0.40 mm extrusion |
| cap (female) crest width | **0.05 mm** | (1.0 − 0.647) − 2 × 0.15: a knife edge, hanging downward once the cap is flipped for printing |
| cap ridge root width | 0.35 mm | the whole ridge is thinner than one extrusion at its base |

The replacement is a three-lug bayonet, sized so that on **both** parts, in
their print orientations, nothing needs support. (Revision D, 2026-09-24:
the bearing faces were a 0.50 mm flat plus a 50° chamfer, and the flat under
each cap lip -- plus the 1.07 mm flat lower flank of the O-ring groove -- drew
slicer support. Both are now pure 50° cones; with support enabled Bambu
Studio generates none, on any of the four parts.)

| | Body | Cap |
|---|---|---|
| Feature | 3 lugs on the seal band, 20° × 0.80 mm proud, z 1.80–3.10 | 3 L-channels: 28° entry slot at the skirt's open end, then a 51° leg under a ceiling at z 3.40 |
| Bearing face | underside: a 50° cone from the bore radius to the crest (0.10 mm flat against the band) | lip top: the same 50° cone, bore to channel root |
| Overhang when printed | 50°, self-supporting (body prints upright) | 50°, self-supporting (cap prints top-plate-down, the lips hang from the skirt) |
| Load path | lug sheared at its root, 3 × 4.8 × 0.8 mm | lip in bending, 1.4–2.0 mm thick; 10.4 mm² projected cone-on-cone contact |

Both bearing faces are **helical at the same pitch** (12 µm per degree of cap
rotation, 2.7° helix angle), so they meet face to face rather than edge on
face. Turning the cap clockwise runs the lugs up the lips; after 30° the
flats meet and every further degree wedges the cap 12 µm harder onto the
base flange — the same hand-tight-to-the-stop feel the thread gave, and
self-locking (2.7° is far below PETG's ~11° friction angle). The ramp keeps
rising to 55° of travel, so a part that prints 0.36 mm tight or 0.30 mm loose
still locks, just at a different angle. Angular repeatability of the locked
cap improves from 18° per 0.05 mm of stop-face error (1.0 mm pitch) to about
4° per 0.05 mm.

**Rest angle (2026-10-09).** The four eggshell test caps all ran on past
nominal contact to the channel end walls and stopped there, which left the
number 35° off 6 o'clock. The end wall is now the rest pose. The body's lugs
sit `lug_phase` = `cam_travel` − `cam_lock` = 25° further round (25/145/265°)
and the cap is unchanged. Three lugs on a body that is symmetric under a 180°
flip put the number on a 60° lattice; with the phase it lands at 6 or 12
o'clock either way round. A printed body with the turned lugs puts a test
cap's number at 6 o'clock (operator, 2026-10-12). See lab note
`docs/lab/2026-10-09-cap-rest-angle.md`.

What did not change: the radial seal and its groove, the cap OD (31.94 mm),
the grip scallops, the tabs, the lettering and LED ring, and the assembly
rule of decision 2. `cap_marking.py` and the accessory-platform proposal
inherit the new skirt untouched. The thread code is gone from the source
(and with it the `bd_warehouse` dependency); commit `e3cf940` has it.

**Fit partly verified.** The coupon pair has been printed once — dimensions
good, lock-up angle not yet reported (lab note 2026-09-10, print trial 1).
The 2026-10-04 caps on revision D bodies turn on to the end wall (lab note
2026-10-09).
The coupon pair (`coupon_body`, `coupon_cap`) carries the lugs, the channels and the
groove at the real parts' z stations; the print trial's two questions are
whether the cap drops on at the entry slots and at what angle it locks up.
That angle re-tunes `cam_lock` for caps not yet printed; for printed caps,
re-tune the body's `lug_phase` instead.

---

## Bill of Materials — non-printed

| Item | Spec | Status |
|---|---|---|
| O-ring | NBR, **ID 26.74 × CS 1.50 mm**, closest stock size | to source |
| Foam ring | closed-cell PE/EVA, adhesive backed, **2.0 mm, OD 16 × ID 12** — a rim ring would sit on the LED | to source or punch |
| Clear PETG | Prusament PETG Clear in AMS slot 2 on every cap plate: the LED ring and any zone set to clear | per print |
| Elastic | 8 mm figure-eight harness | cross-section UNVERIFIED |
| Conformal coating | acrylic, per `docs/requirements.md` masking rules | unchanged |

> The previously specified 30 × 2 mm ring **does not fit this geometry**. Sourcing
> it would be wasted money.

---

## Print Settings

| Setting | Value | Why |
|---|---|---|
| Material | Transparent PETG | UV/impact per README; LEDs stay readable |
| Nozzle | 0.40 mm | thinnest wall in the design is 0.80 mm = 2 perimeters |
| Layer | 0.16 mm | the lip ramps and the O-ring groove need the resolution |
| Perimeters | 3 | the bayonet lips make the skirt 5 lines thick in places; 3 walls + gap fill |
| Wall generator | **Arachne** | variable-width walls absorb the lips as walls, not as infill islands |
| Avoid crossing walls | **on** | routes travels over the print instead of across the open bore — see *Stringing* below |
| Infill | 30 %+ | parts are nearly all perimeter anyway |
| Supports | **none** | verified by slicing; see below |
| Orientation | **already baked into the STLs** | drop them on the plate as-is |

`cad/out/hen_tag_revC_P1S.3mf` (from `slice_check.py --project`) carries all
four printables and these settings as a Bambu Studio project.

**Variable layer height: not used for the cap face** (decided 2026-10-04).
The face's look is set in XY (line width, flow, squish, plate texture). A
thinner first layer caused the 2026-09-29 plate failure. Thinner layers
through the 1.1 mm multi-colour top plate would roughly double the filament
changes (about 24 → 45 on the test plate) and push the 0.64 mm inlay
boundary onto a mid-layer. Thicker layers in the skirt above 1.1 mm remain a
candidate for saving print time. <!-- INFERRED: verify (from the owner session of 2026-10-04) -->

The exported STLs lie in their print orientation: the body floor-down, the cap
and the female coupon flipped top-plate-down. Do not re-orient them. Left as
modelled, the cap lands opening-down and its top plate becomes a ~28 mm bridge
over the cavity. The STEP files keep the design coordinate system, so the model
stays readable in CAD.

Revision B was sliced with Bambu Studio 02.08.02.60 at default settings: all
four parts returned `Success.` with **zero warnings** and
`max_cantilever_dist = 0` for the body. Revision C slices clean in the same
version, no warnings on any part; `cad/slice_check.py` repeats that check
from the command line and also reads the G-code back for the item below.

**Stringing is a toolpath property, not a geometry one.** In every layer of
the lip zone the skirt is a thin wall carrying three thicker arcs separated
by the entry slots, so the slicer prints three islands per layer and travels
between them. Left to the stock profile it flies straight across the open
bore and PETG leaves a hair on every pass; the first printed coupon showed
exactly that (lab note 2026-09-10, print trial 1). Measured on the G-code —
travels longer than 3 mm passing within 12 mm of the axis over open air:

| Part | stock Bambu profile | 3 walls + Arachne + avoid crossing walls |
|---|---|---|
| `coupon_cap` | 58 | **3** |
| `cap` | 107 | **19** (layer changes) |
| `coupon_body` | 96 | **0** |
| `body`, across the cell pocket | 102 | 68 |

The revision B threaded cap measured 106 on the stock profile, so this is
not a cost of the bayonet; it was always there, hidden inside a closed cap.

The coupons (`coupon_body.stl` 1.70 g, `coupon_cap.stl` 1.16 g) carry the
bayonet pair and the groove and nothing else, at the real parts' z stations.
The coupon pair has printed once and four caps rest on the end wall (lab
notes 2026-09-10, 2026-10-09); on a new printer, print the pair first. The
cap should turn 55° to the end wall, where it rests (2026-10-09). If
it locks up well before that the parts are tight. Report the angle and change
`lug_phase` on the body (`cam_lock` moves the cap's channels, so it is for caps
not yet printed), or `fit_lug_r` if the lugs bind radially, then regenerate;
do not file the parts.

---

## Assembly

1. Conformal-coat the PCB per `docs/requirements.md`, masking SWD pads, battery contacts and
   the antenna area.
2. Seat the CR2032 in the holder, sliding it in at the tangent edge.
3. Drop the board into the body cavity **holder first, PCB facing up**. The
   holder should drop into its pocket with about 0.25 mm of play, and the PCB
   face should end up about 1.8 mm below the cap ceiling (0.19 mm over the
   centre switch).
   - Check the LED is facing you. If the PCB is against the floor, the board is
     upside down and the LED will be pointed at the bird.
4. Stick the OD 16 × ID 12 × 2.0 mm foam ring centred on the cap ceiling,
   under the core disc; the centre switch stays inside its hole.
5. Fit the O-ring into the cap's internal groove.
6. Turn the cap about 55° anticlockwise from its final position so the entry
   slots sit over the three lugs, press it straight down over the seal band
   until the skirt meets the base flange, then turn it clockwise to the stop,
   about 55°. Of the three ways the slots fit over the lugs, pick the one
   that ends with the number at 6 o'clock. Hand-tight is enough; the stop is
   the channel end wall, and the radial seal does not need more.
7. Thread the elastic through each side tab's slot and back around the bar.

---

## Verification Performed

`cad/verify.py`, 40 machine checks (49 with `--board-step`), all passing. Notable ones:

- body/cap collision: **0.000 mm³** at the assembled position
- board vs. enclosure interference: **0.0000 mm³**
- holder circumference backed by plastic: **100 %**
- fill clears the PCB face: 0.20 mm
- clearance at the tangent point: **0.30 mm**
- cap drops on at the entry angle and the lugs run free for 0–28°: **0.000 mm³**
  overlap at every step
- ramp wedges past the lock angle: **0.498 mm³** interference at +4°, the cap tightens
- cap rests on the end walls: clear 1° short of the rest pose, **0.026 mm³**
  in the wall 2° past it (the old 0° lug phase gives 0.000 mm³)
- locked cap retained: **6.08 mm³** lug/lip overlap when lifted 0.6 mm; at the
  entry angle it lifts off clean
- cap bore clears the seal band: +0.10 mm (the rule that caught decision 2)
- O-ring never crosses the lugs: groove starts z 3.91, channels end z 3.40
- slicer support with support enabled: **none** on body, cap and both coupons (Bambu Studio CLI)
- O-ring squeeze: **22 %** (static radial target is 15–30 %)
- thinnest wall: **0.80 mm** between the cap and the tab slot (0.85 mm under
  the grip scallops)
- 8.0 mm elastic threads the tab slot: **0.000 mm³** obstructing
- tab bar cross-section: **4.80 mm²**
- underside flat: **0.000 mm³** below the floor plane
- assembled envelope: 40.14 × 31.94 × 8.70 mm
- worst unsupported overhang band: **0.59 mm²** at z 1.8 on the body; none
  above the bed on the cap. The limit is 1.0 mm² per 0.1 mm band on both parts
  (`CLUSTER_LIMIT` in `verify.py`). Since 2026-09-24 the lug
  undersides, lip tops and the O-ring groove flank are 50° cones, so only the
  0.10 mm lug flat against the seal band remains.
- meshes watertight: 0 non-manifold edges, 0 loose vertices, positive volume
- **sliced clean in Bambu Studio** (revision C, 2026-09-10): all four parts,
  zero warnings; open-air travels with the recommended settings: cap 19,
  coupon 3, body 0 above the fill (`cad/slice_check.py`)

### The floating-cantilever defect

The rim's lead-in chamfer was cut with a cone tapering the wrong way. Instead of
narrowing toward the rim it widened, which thinned the wall to a **0.10 mm knife
edge** low down and left a downward-facing annular shelf above it — a genuine
undercut, and unprintable.

Confirmed by slicing both versions:

| | `max_cantilever_dist` | Slicer verdict |
|---|---|---|
| Inverted chamfer | 1.37 × 10⁶ | *"floating cantilever… enable support generation"* |
| Corrected | **0** | `Success.`, no warnings |

A second, smaller floating feature was found in the same pass: the thread began
0.2 mm above the base flange, leaving its first ridge unsupported. The thread now
starts flush on the flange, which took the body's worst overhang band from
18.95 mm² down to 9.36 mm² (revision B; the bayonet and the 2026-09-24 cones
removed the rest).

`verify.py` now measures unsupported overhang area per part, per 0.1 mm
height band, against a 1.0 mm² limit, so this class of defect cannot return
unnoticed.

Mesh volume matches the solid model to within 0.3 mm³, so STL tessellation is
not distorting the geometry.

**What revision A proved**: printed on a Bambu Lab P1S, dimensions and thread
fit both confirmed good on physical parts.

**What none of this proves**: the seal. The coupon pair and four per-hen
caps are printed and fitted (lab notes 2026-09-10, 2026-10-09); no O-ring has
been compressed, no water has touched it, no elastic has loaded a tab, and no
hen has worn it.

---

## Verified Evidence vs. Working Hypotheses

### Verified

- **Revision A printed and fitted on a Bambu Lab P1S: dimensions good; the
  thread mated on that one pair.** Later caps tore along it (lab note
  2026-09-10), so the thread and its clearances are history. What carries over
  as empirical is the cavity, the seal band and the skirt.
- The geometry is internally consistent, manifold, and assembles without
  interference **given the assumed inputs**.
- The internal tangency of PCB and holder follows from the two reported
  diameters and matches the operator's description.
- The mass comparison between sealing strategies is computed from real solids,
  not estimated.
- **Board and parts from the manufacturer STEP** (`HOLYIOT-25008-V1.0.step`,
  2026-09-23): Ø25.00 × 0.81 board, S1 1.60 tall at the centre, LED at r 9.84 /
  −60°, nothing beyond r 11.77. `verify.py --board-step PATH` re-extracts
  the numbers and collides the real board with body and cap (0.0000 mm³).
  The STEP's battery clip is a generic model (it leaves 2.39 mm for a 3.2 mm
  cell) and is ignored.

### Assumed (UNVERIFIED)

- Holder Ø21 × 4.0 mm (caliper). Board stack 6.41 mm follows from it; the
  ceiling tolerates a holder of 3.79–4.19 mm.
- Board part mass 0.18 g (volume at an assumed 2.5 g/cm³); holder mass 0.6 g and O-ring mass 0.4 g, both estimates that the 10 g budget
  argument depends on.
- Elastic cross-section fitting an 8.6 × 2.0 mm channel.
- The bayonet fit: `fit_lug_r` 0.15, `fit_lug_z` 0.30, ramp contact at 30°. The
  caps rest on the end wall at 55° (four caps, 2026-10-09); the axial play
  there is unmeasured.

### Unknown

- Antenna location. Probably a printed antenna: the matching network
  (L3/L4/C8–C13) sits beside the radio at 115–136°, and the rim from 141° to
  290° carries no parts. The STEP has no copper, so this stays unconfirmed; the
  enclosure puts no metal anywhere near the board.

---

## Open Questions & Next Steps

1. **Check the assembled tag**: that the LED is actually visible through the
   clear LED ring (r 8.5–11.5), and that a tab survives being loaded with an
   elastic. The revision B body has already accepted the board, and a body with the
   turned lugs puts a test cap's number at 6 o'clock (lab note 2026-10-09).
2. **Measure the total stack height** in one caliper span and the assembly mass
   on a scale. Both feed straight back into `Params`.
3. **Source the O-ring** at ID 26.74 × CS 1.50 mm, or report the nearest stock
   size available so the groove can be re-cut to it.
4. **Mass**: the current model lands at 9.92 g (`hen_tag_enclosure.py` mass
   summary), 0.08 g under the 10 g target. About 1.2 g of the total (board parts,
   holder, O-ring) is still estimated rather than weighed. If the weighed
   figures overrun, the cheapest reductions are lightening the fill in its thick sector, the cap
   top plate, and the base flange — but a decision on whether 10 g is a hard
   welfare limit or a design aspiration should come first.
5. **No ingress rating is claimed.** IP54 remains an intent, not a test result.
