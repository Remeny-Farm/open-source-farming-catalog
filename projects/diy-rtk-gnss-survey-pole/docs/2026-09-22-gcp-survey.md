# 2026-09-22: ground control point survey with the pole

Field record for the `field-tested` stage. Source: the maintainer's BSc thesis (SZTE, 2026), its SW Maps export and its processing logs. Point coordinates are deliberately left out; the site is a private pasture in northern Hungary.

## Setup on the day

- Receiver: simpleRTK2B Budget board (u-blox ZED-F9P) from the ArduSimple Basic Starter Kit, in a waterproof ABS electrical box strapped to the pole.
- Antenna: u-blox ANN-MB-00 on a flat plate at the top of a straight wooden pole.
- Logger: Android phone running SW Maps, connected to the receiver by USB.
- Corrections: Centipede network over NTRIP, Domoszló base (the nearest one to the site). The baseline length was not recorded; from the village centre it is roughly 30 km.
- Antenna height entered in SW Maps: 2.04 m.
- Pole held over the point, verticality checked with a box spirit level, position averaged for 60 s per point with the SW Maps Averaging function. The 60 s is the maintainer's account of the session; the export does not store it.
- No geoid file, "Record GNSS Orthometric Height" off. The export's `_ORTHO_HT` is 0.0 for every point, so all heights are ellipsoidal.

## What was measured

Five ground control points (cardboard targets) for a DJI Mini 4 Pro photogrammetry survey of about 3.5 ha (convex hull of the points), recorded between 07:54 and 08:18 local time. A phone photo taken during the first point shows "RTK Fix" with H/V accuracy "N/A"; that is one moment, not proof of a fix for the whole session.

## Downstream check

The imagery (1,044 photos) was processed in WebODM with all five points. Five leave-one-out reconstructions, each withholding one point, compared the terrain model with the withheld point's height:

| Statistic | Value |
|---|---|
| n | 5 |
| Mean signed difference | +0.012 m |
| Mean absolute difference | 0.175 m |
| RMSE | 0.194 m |
| Largest absolute difference | 0.242 m |

This tests the drone model at five places, not the receiver. Control and check coordinates come from the same RTK session, so an error shared by all five points would not show up here. No measurement against an independently known benchmark was made.
