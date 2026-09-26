<!-- One project per pull request. Delete lines that do not apply. / Egy projekt PR-onként. -->

## Project / Projekt

`projects/<id>/` — new design | fix | build report

## What changed / Mi változott

<!-- Two or three sentences. Where do the files live (here or on a mirror)? / Két-három mondat. Hol élnek a fájlok? -->

## Checklist / Ellenőrzőlista

- [ ] I hold the rights to the files, text and photos, or they are already under a licence that allows this publication. / A jogok az enyémek, vagy már megengedő licenc alatt állnak.
- [ ] `licenses` in `project.json` is explicit per file group and matches the files. / A `licenses` fájlcsoportonként explicit, és a fájlokhoz illik.
- [ ] Title, description, limitations and photo alt text say the same thing in `hu` and `en`. / A cím, leírás, korlátok és alt-szöveg ugyanazt mondja magyarul és angolul.
- [ ] `limitations` is honest and includes safety notes. / A `limitations` őszinte, és tartalmazza a biztonsági tudnivalókat.
- [ ] `stage` is supported by evidence (photo, lab note, build report). / Az állapotot bizonyíték támasztja alá.
- [ ] The photo is a real photograph of the real object, generated with `npm run photo`, with its provenance sidecar. / A fotó valódi, `npm run photo`-val készült, sidecarral.
- [ ] Every served file is listed in `files` with its sha256 (`npm run hash`) and is under 20 MB. / Minden kiszolgált fájl a `files`-ban van sha256-tal, 20 MB alatt.
- [ ] `npm run validate` passes locally. / Az `npm run validate` helyben zöld.

## For the reviewer / A lektornak

<!-- Anything you are unsure about, or a language you could not write. / Amiben bizonytalan vagy, vagy amelyik nyelvet nem tudtad megírni. -->
