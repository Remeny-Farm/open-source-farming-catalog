# DIY RTK GNSS survey pole

A field survey tool capable of centimetre-level positioning for roughly €250. I put it together for my thesis because a ready-made RTK receiver costs several times as much, which was out of reach on a student budget. It is built around a commercial ArduSimple simpleRTK2B kit (u-blox ZED-F9P receiver and dual-band antenna), plus a wooden pole, a waterproof electrical box and an Android phone running SW Maps. Corrections come from the free Centipede network over the internet via NTRIP, so no base station of your own is needed.

I used it to survey ground control points (GCPs) for a drone survey. The same setup works for staking out and recording fence lines, wells, pipes or the key points of a keyline design.

## State

- **Field-tested**: on 22 September 2026 I measured five ground control points with it on about 3.5 ha of pasture for a DJI Mini 4 Pro drone survey. Details are in `docs/2026-09-22-gcp-survey.md`.
- A leave-one-out check of the drone model at the five points gave a vertical RMSE of 0.194 m. That describes the drone model, not the receiver: control and check points come from the same session, and the pole has not been checked against a benchmark with known coordinates.
- Heights are ellipsoidal. No geoid file was used, so the values are not in the Hungarian national (Baltic) height system.
- The receiver firmware was updated with u-center on Windows. The exact configuration was not saved.

## Parts

The full list is in `bom.csv`. In short:

| Item | Role |
|---|---|
| simpleRTK2B Basic Starter Kit | ZED-F9P receiver board and ANN-MB-00 antenna with 5 m cable |
| Waterproof ABS box | protects the receiver board |
| Flat mounting plate (80 × 80 mm) | carries the antenna at the top of the pole |
| Hook-and-loop straps | hold the box and the cables |
| 2 m USB cable | between the receiver and the phone |
| Magnetic box spirit level | keeps the pole vertical |
| Straight wooden pole, about 2 m | the survey pole itself |
| Android phone, SW Maps | data logging and NTRIP client (Android only) |

The €250 figure is what I paid in 2026, excluding the phone.

## Building it

1. Fix the mounting plate to the top of the pole and place the antenna on it, facing the sky with nothing covering it.
2. Put the receiver board in the waterproof box. Route the antenna and USB cables so the box still closes.
3. Strap the box to the lower part of the pole at a comfortable hand height. Coil and secure the spare antenna cable so it cannot snag.
4. Mount the spirit level and the phone above the box so you can see both while measuring.
5. Measure the height from the ground to the base of the antenna. It was 2.04 m on the built pole; measure your own.

## Setup and measuring

1. If the receiver firmware is old, update it on a Windows PC with u-blox u-center. I did, and afterwards it worked without further setup.
2. Connect the receiver to the phone over USB. With Android it works on its own, without an adapter; this setup does not work with an iPhone.
3. In SW Maps, add the receiver as an external GNSS device, then set up NTRIP: caster `crtk.net`, port `2101`. As mountpoint, pick the nearest Centipede base from the coverage map, or `NEAR`. The latter only sends corrections once the client sends GGA sentences.
4. Enter the antenna height. Decide in advance whether you need a geoid file: national height system values need a separate setting.
5. Wait until SW Maps shows RTK Fix. Hold the pole over the point, check it is vertical with the level, and average each point. I averaged for 60 seconds.
6. Export the points. If you entered the antenna height in SW Maps, do not subtract it again during processing.

## Watch out for

- Accuracy depends on the distance to the base station, mobile coverage and how much open sky the antenna sees. Under trees, next to buildings or in a valley you may get only a Float solution instead of a Fix.
- Check the Fix at every point. The export does not record whether it held for the whole averaging period.
- A 2 m pole tipped up or sideways can reach an overhead power line. Do not use it near power lines or in a thunderstorm.

## Licence

CC BY-SA 4.0 for all documentation. The ArduSimple kit, SW Maps and the Centipede service are used under their own terms.
