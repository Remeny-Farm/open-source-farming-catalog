# Holyiot 25008 tok (nRF54L15, CR2032)

Kétrészes, átlátszó PETG tok a Holyiot 25008 BLE modulhoz (Nordic nRF54L15, ST LIS2DH12) és egy CR2032 gombelemhez. Ez a Remény Farm tyúkjelölő (hen tag) mechanikai háza: a szabadtartású tojótyúkok gumis, nyolcas hámmal viselik, a hám a tok oldalsó füleiben fut. Az elektronika és a firmware nem része ennek a projektnek.

## Állapot

- **C revízió.** A geometria parametrikus [build123d](https://build123d.readthedocs.io/) forrásból készül, gépi ellenőrzéssel, STEP és STL exporttal.
- A C revízió illesztési próbadarabjait (ház és kupak) egyszer kinyomtattuk; a méretek jók.
- A teljes zárt összeállítás, a radiális O-gyűrűs tömítés és a vízállóság **nincs tesztelve**. Az A revíziót Bambu Lab P1S nyomtatón kinyomtattuk és összeillesztettük; a menete később nyomtatáskor elszakadt, ezért bajonettzárra cseréltük (lásd a 2026-09-10-i laborjegyzetet).
- Modellezett összeszerelt tömeg 9,92 g a 10 g-os célhoz képest; az elem, a tartó és az O-gyűrű tömege még becslés.
- **Vezető vagy szénszálas filament tilos.** Elhangolja a 2,4 GHz-es antennát, és rövidre zárhatja a gombelem szabad érintkezőit.

## Fő adatok

| Tétel | Érték |
|---|---|
| Összeszerelt befoglaló méret | 40,14 × 31,94 × 8,70 mm (Ø31,94 ház, fülekkel 40,14) |
| Nyomtatott tömeg (PETG) | 5,01 g (ház 2,71 g, kupak 2,30 g) |
| Tömítés | Radiális NBR O-gyűrű, belső átmérő 26,74 × keresztmetszet 1,50 mm |
| Zárás | Háromkörmös bajonett, 30° jobbra, önzáró rámpákra |
| Anyag | Átlátszó PETG |

## Fájlok

| Cél | Útvonal |
|---|---|
| Ház és kupak nyomtatása | `source/cad/out/body.stl`, `source/cad/out/cap.stl` |
| Testmodell (CAD) exportok | `source/cad/out/body.step`, `source/cad/out/cap.step` |
| Először az illesztési próbadarabok | `source/cad/out/coupon_body.stl`, `source/cad/out/coupon_cap.stl` |
| Szeletelésre kész Bambu Studio projekt (P1S) | `source/cad/out/hen_tag_revC_P1S.3mf` |
| Parametrikus forrás | `source/cad/hen_tag_enclosure.py` |
| Tyúkonkénti kupakgenerátor | `source/cad/cap_marking.py` |
| Gépi ellenőrzések | `source/cad/verify.py` |
| Anyagjegyzék | `bom.csv` |

## Megépítés

1. Nyomtasd ki a két próbadarabot, és ellenőrizd az illeszkedést a saját nyomtatódon, mielőtt a teljes alkatrészeket nyomtatod.
2. Nyomtasd ki a `body.stl` és `cap.stl` fájlt átlátszó PETG-ből. A nyomtatási beállítások és a tájolás a `source/DESIGN.md`-ben vannak leírva.
3. Helyezd be az O-gyűrűt, tedd be a Holyiot 25008 panelt elemtartóval lefelé, panellel (LED-del) a kupak felé, majd zárd a bajonettet.

A geometria újragenerálásához futtasd a `source/cad/` scriptjeit `uv`-val (PEP 723 beágyazott függőségek; lásd `source/cad/README.md`).

## Dokumentáció

A teljes mérnöki dokumentáció angolul, a `source/` alatt található:

- `source/README.md`: áttekintés, hardverkörnyezet, gyors indulás.
- `source/DESIGN.md`: tervezési döntések, ellenőrzési eredmények, nyomtatási beállítások, nyitott kérdések.
- `source/docs/requirements.md`: anyag-, tömítési és formakövetelmények.
- `source/docs/lab/`: dátumozott laborjegyzetek mérésekkel, nyomtatási próbákkal és hibákkal.
- `source/platform/`: kiegészítő-platform javaslat (rögzítőgyűrű, bajonett-interfész), még nem épült meg.
- `source/editor/`: a tyúkonkénti kupakszerkesztő böngészős prototípusa.
- `CHANGELOG.md`: revíziótörténet.

## Licenc

A `source/` MIT licencű (lásd `source/LICENSE`). Ez az összefoglaló, az anyagjegyzék és a fotók CC BY-SA 4.0 alatt érhetők el.
