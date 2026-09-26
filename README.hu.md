# Open Source Farming katalógus

In English: [README.md](README.md)

Az [opensource.remeny.farm](https://opensource.remeny.farm) (magyar) és az [opensource.mootopia.wtf](https://opensource.mootopia.wtf) (angol) mögötti lektorált katalógus: nyílt mezőgazdasági eszköztervek a dokumentációjukkal, anyagjegyzékükkel, fájljaikkal és fotóikkal. Minden terv feltünteti az állapotát (`concept`, `prototype`, `built`, `field-tested`), a licencét és a korlátait. Semmit nem szépítünk.

A weboldal közvetlenül ezt a repót olvassa. Az API (`/api/v1/projects.json`, `/api/v1/project.schema.json`) ugyanezekből a fájlokból származik.

## Szerkezet

```
schema/project.ts            projektszerződés (Zod), 2-es sémaverzió
schema/build.ts              „én is megépítettem” jelentés szerződése
projects/<id>/
  project.json               metaadat: cím, leírás, állapot, témák, licencek, fájlok, linkek, fotó, korlátok
  README.hu.md, README.en.md mi ez, milyen állapotban van, hogyan építhető meg („built” állapottól kötelező)
  bom.csv                    ref,qty,item_hu,item_en,source,notes
  CHANGELOG.md               verziótörténet
  source/                    a projekt saját fája: szerkeszthető CAD, kód, dokumentáció, bizonyítékok
  export/                    származtatott fájlok (STL, STEP, PDF, gerber) forrásfa nélküli projektekhez
  photos/                    <név>-1200.webp, <név>-600.webp és mindegyikhez egy eredetigazoló sidecar
  builds/                    <éééé-hh-nn>-<slug>.json jelentések azoktól, akik megépítették
scripts/validate.mjs         szerkezet, hash-ek, fotók, README, BOM és építési jelentések ellenőrzése
scripts/hash.mjs             „files” bejegyzéseket ír ki sha256-tal a project.json-hoz
scripts/photo.mjs            fotópárt készít egy eredetiből (sharp kell hozzá)
```

A weboldal csak a `project.json` `files` listájában szereplő fájlokat szolgálja ki, a `/projects/<id>/<útvonal>` címen, mindegyiket sha256-tal. A nagy binárisok fájlonként 20 MB alatt maradnak; ami nagyobb, az egy `links`-ben megadott tükrön él.

## Hozzájárulás

- Olvasd el a [CONTRIBUTING.hu.md](CONTRIBUTING.hu.md) fájlt (embereknek) vagy a [SUBMITTING.md](SUBMITTING.md) fájlt (pontos szerződés, ágenseknek és scripteknek).
- Új terv JSON-írás nélkül: nyiss egy [új terv issue-t](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=new-design.yml).
- Új terv vagy javítás pull requesttel: fork, `projects/<id>/` hozzáadása vagy szerkesztése, `npm ci && npm run validate`, majd PR.
- Megépítetted? Küldj [építési jelentést](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=build-report.yml).

GitHub-fiók szükséges; e-mailes vagy webes űrlapos beküldés nincs. Minden bejegyzést a karbantartó lektorál, mielőtt beolvad és megjelenik.

## Ellenőrzések

```sh
npm ci
npm test          # a validátor egységtesztjei
npm run validate  # a teljes katalógus
```

Node 22.18 vagy újabb kell (a scriptek közvetlenül TypeScriptet importálnak).

## Licencek

- Katalógus-metaadat, dokumentáció és fotók: [CC BY-SA 4.0](LICENSE).
- A repó scriptjei és sémája: [MIT](LICENSE-MIT).
- Az egyes projektek fájljai a saját `project.json` `licenses` mezőjükben megadott licenceket viselik; a `path`-szal ellátott licenc arra a fájlra vagy könyvtárra, a `path` nélküli az egész projektre vonatkozik.

Karbantartó: [Remény Farm](https://github.com/Remeny-Farm).
