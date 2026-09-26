# Hozzájárulás

In English: [CONTRIBUTING.md](CONTRIBUTING.md)

Ez a katalógus olyan nyílt mezőgazdasági eszközterveket tesz közzé, amelyeket valóban meg lehet építeni. A hozzájárulás kizárólag GitHubon megy: issue-űrlappal vagy pull requesttel. E-mailes vagy webes űrlapos beküldés nincs, és minden bejegyzést a karbantartó lektorál, mielőtt beolvad.

## Mivel járulhatsz hozzá

1. **Új tervvel**, amelyet te készítettél vagy tartasz karban: fájlok (vagy link oda, ahol élnek), leírás, fotó a valódi tárgyról, állapot és korlátok.
2. **Meglévő terv javításával**: jobb fordítás, pontosított korlát, állapotfrissítés bizonyítékkal, a fájlok új verziója, cserefotó.
3. **Építési jelentéssel**: megépítettél egy listázott tervet; írd meg, mikor, melyik verziót, mi történt, fotóval.

A platform kódja (a weboldal) nem ebben a repóban van.

## Három út

| Te | Ezt tedd |
|---|---|
| Megvannak a fájljaid és van GitHub-fiókod, de nem akarsz JSON-t írni | Nyiss egy [új terv issue-t](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=new-design.yml). Egy nyelv elég; a lektor hozzáteszi a másikat és elkészíti a pull requestet. |
| Otthon vagy a gitben | Fork, `projects/<id>/` hozzáadása a [SUBMITTING.md](SUBMITTING.md) szerint, `npm ci && npm run validate`, majd pull request. |
| Megépítettél egy listázott tervet | Küldj [építési jelentést](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=build-report.yml). |

Meglévő terv javításához nyiss [javítási issue-t](https://github.com/Remeny-Farm/open-source-farming-catalog/issues/new?template=fix-design.yml), vagy szerkeszd a projektkönyvtárat pull requestben.

## Mi kell egy tervhez

- **Jogok.** A fájlok, szövegek és fotók jogai a tieid, vagy már olyan licenc alatt állnak, amely megengedi ezt a közzétételt.
- **Licenc, fájlcsoportonként megadva.** Például a `source/` MIT alatt, minden más CC BY-SA 4.0 alatt. Egyszerű terveknél az alapértelmezés a CC BY-SA 4.0.
- **Mindkét nyelv** a címhez, leíráshoz, korlátokhoz és a fotó alt-szövegéhez. Ha csak az egyiket írod meg, jelezd az issue-ban, és a lektor lefordítja; pull requestben mindkettő kötelező.
- **Őszinte állapot.** `concept` (nem épült meg), `prototype` (egyszer megépült, nincs használatban), `built` (működik, a szerző használja), `field-tested` (valódi használatban, dokumentáltan). A `built` és a `field-tested` valódi fotót kíván a valódi tárgyról.
- **Olyan korlátok, amelyeket az építőnek tudnia kell**, a biztonságiakkal együtt: mi nincs tesztelve, miből nem szabad készíteni, mire nem alkalmas.
- **Valódi fotó** a tárgyról, tőled vagy engedéllyel. Stock vagy generált kép nem.
- **Fájlonként 20 MB alatt.** A nagyobb fájlok tükrön (Printables, saját repó) élnek, a `project.json`-ból linkelve.

## Lektorálás

A karbantartó minden pull requestet ez alapján néz át beolvasztás előtt:

- a jogok és a licenc explicitek, és a fájlokhoz illenek;
- a HU és az EN ugyanazt mondja;
- a korlátok őszinték, és tartalmazzák a biztonsági tudnivalókat;
- az állapotállítás alá van támasztva (fotó, laborjegyzet, építési jelentés);
- a fotó valódi, és van eredetigazoló sidecarja;
- az `npm run validate` zöld a CI-ban.

A beolvasztott bejegyzés a következő platform-telepítés után jelenik meg a weboldalon, általában egy napon belül.

## A hozzájárulásod licence

Beküldéssel elfogadod, hogy az általad hozzáadott katalógus-metaadat, dokumentáció és fotó [CC BY-SA 4.0](LICENSE) alatt jelenik meg, a tervfájljaid pedig a `project.json`-ban megadott licencek alatt. A repó scriptjei [MIT](LICENSE-MIT) alatt állnak.
