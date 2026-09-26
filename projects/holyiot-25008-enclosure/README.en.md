# Holyiot 25008 enclosure (nRF54L15, CR2032)

Two-part transparent PETG enclosure for the Holyiot 25008 BLE module (Nordic nRF54L15, ST LIS2DH12) with a CR2032 coin cell. It is the mechanical housing of the Remény Farm hen tag, worn by free-range laying hens on a figure-eight elastic harness through the enclosure's side tabs. The electronics and firmware are not part of this project.

## State

- **Revision C.** Geometry generated from parametric [build123d](https://build123d.readthedocs.io/) source, machine-verified and exported as STEP and STL.
- The revision C fit coupons (body and cap) have been printed once; dimensions were good.
- The complete sealed assembly, the radial O-ring seal and water resistance are **untested**. Revision A was printed and fitted on a Bambu Lab P1S; its thread later tore in print and was replaced by the bayonet closure (see the 2026-09-10 lab note).
- Modelled assembled mass 9.92 g against a 10 g target; the cell, holder and O-ring masses are still estimates.
- **No conductive or carbon-fibre filament.** It detunes the 2.4 GHz antenna and can short the exposed coin-cell terminals.

## Key numbers

| Item | Value |
|---|---|
| Assembled envelope | 40.14 × 31.94 × 8.70 mm (Ø31.94 body, tabs to 40.14) |
| Printed mass (PETG) | 5.01 g (body 2.71 g, cap 2.30 g) |
| Seal | Radial NBR O-ring, ID 26.74 × CS 1.50 mm |
| Closure | Three-lug bayonet, 30° clockwise onto self-locking ramps |
| Material | Transparent PETG |

## Files

| Purpose | Path |
|---|---|
| Print the body and cap | `source/cad/out/body.stl`, `source/cad/out/cap.stl` |
| Solid CAD exports | `source/cad/out/body.step`, `source/cad/out/cap.step` |
| Print the fit coupons first | `source/cad/out/coupon_body.stl`, `source/cad/out/coupon_cap.stl` |
| Ready-to-slice Bambu Studio project (P1S) | `source/cad/out/hen_tag_revC_P1S.3mf` |
| Parametric source | `source/cad/hen_tag_enclosure.py` |
| Per-hen cap generator | `source/cad/cap_marking.py` |
| Machine checks | `source/cad/verify.py` |
| Bill of materials | `bom.csv` |

## Building it

1. Print the two coupons and check the fit on your printer before the full parts.
2. Print `body.stl` and `cap.stl` in transparent PETG. Print settings and orientation are documented in `source/DESIGN.md`.
3. Fit the O-ring, seat the Holyiot 25008 board with the holder facing down and the PCB (LED) facing the cap, close the bayonet.

To regenerate the geometry, run the scripts in `source/cad/` with `uv` (PEP 723 inline dependencies; see `source/cad/README.md`).

## Documentation

The full engineering record is in English under `source/`:

- `source/README.md`: project overview, hardware context, quickstart.
- `source/DESIGN.md`: design decisions, verification results, print settings, open questions.
- `source/docs/requirements.md`: material, sealing and form-factor requirements.
- `source/docs/lab/`: dated lab notes with measurements, print trials and failures.
- `source/platform/`: accessory platform proposal (keeper collar, bayonet interface), not yet built.
- `source/editor/`: browser prototype of the per-hen cap editor.
- `CHANGELOG.md`: revision history.

## Licence

`source/` is MIT (see `source/LICENSE`). This summary, the bill of materials and the photos are CC BY-SA 4.0.
