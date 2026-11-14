# Saját összeállítású RTK GNSS mérőrúd

Centiméteres pontosságra képes terepi mérőeszköz, amely nagyjából 250 euróból kijön. A szakdolgozatomhoz raktam össze, mert egy kész RTK-vevő ára ennek többszöröse, és diákként nem tudtam volna kifizetni. Az alapja egy kereskedelmi ArduSimple simpleRTK2B készlet (u-blox ZED-F9P vevő és kétsávos antenna). Ehhez jön egy farúd, egy vízálló villanyszerelési doboz és egy Android-telefon az SW Maps alkalmazással. A korrekciót az ingyenes Centipede hálózat adja interneten, NTRIP-en keresztül, így saját bázisállomás nem kell.

Drónos felmérés illesztőpontjainak (GCP) bemérésére használtam, de ugyanígy alkalmas kerítésnyomvonal, kút, vezeték vagy egy keyline-terv kulcspontjainak kitűzésére és rögzítésére is.

## Állapot

- **Terepen tesztelve**: 2026. szeptember 22-én öt illesztőpontot mértem vele egy kb. 3,5 ha-os legelőrészen, egy DJI Mini 4 Pro drónos felméréshez. A részleteket a `docs/2026-09-22-gcp-survey.md` jegyzet tartalmazza.
- A drónmodell kihagyásos ellenőrzése az öt ponton 0,194 m magassági RMSE-t adott. Ez a drónmodellről szól, nem a vevőről: az illesztő- és ellenőrzőpontok ugyanabból a mérésből származnak, ismert koordinátájú alapponton pedig nem ellenőriztem az eszközt.
- A magasságok ellipszoidi magasságok. Geoidfájlt nem használtam, így az értékek nem a Balti rendszerben vannak.
- A vevő firmware-ét Windows alatt, u-centerrel frissítettem. A pontos konfigurációt nem mentettem el.

## Alkatrészek

A teljes lista a `bom.csv` fájlban van. A lényeg:

| Elem | Szerep |
|---|---|
| simpleRTK2B Basic Starter Kit | ZED-F9P vevőpanel és ANN-MB-00 antenna 5 m kábellel |
| Vízálló ABS doboz | védi a vevőpanelt |
| Lapos szerelőlap (80 × 80 mm) | erre kerül az antenna a rúd tetején |
| Tépőzáras pántok | a doboz és a kábelek rögzítése |
| 2 m-es USB-kábel | a vevő és a telefon között |
| Mágneses dobozos vízmérték | a rúd függőlegesen tartásához |
| Egyenes farúd, kb. 2 m | a mérőrúd maga |
| Android-telefon, SW Maps | adatrögzítés és NTRIP-kliens (csak Android) |

A 250 eurós összeg a saját beszerzésemre vonatkozik (2026), a telefon nélkül.

## Összeállítás

1. Rögzítsd a szerelőlapot a farúd tetejére, és tedd rá az antennát úgy, hogy az ég felé nézzen, és semmi ne takarja.
2. Tedd a vevőpanelt a vízálló dobozba. Az antenna- és az USB-kábelt úgy vezesd ki, hogy a doboz zárható maradjon.
3. Pántold a dobozt a rúd alsó részére, kényelmes kézmagasságba. A felesleges antennakábelt tekerd fel és rögzítsd, hogy ne akadjon bele semmibe.
4. A vízmértéket és a telefont a doboz fölé rögzítsd, hogy mérés közben egyszerre lásd mindkettőt.
5. Mérd meg a talajtól az antenna talpáig tartó magasságot. A megépített rúdon ez 2,04 m volt, de a saját rudadon mindenképp mérd le.

## Beállítás és mérés

1. Ha a vevő firmware-e régi, frissítsd egy Windowsos gépen a u-blox u-center programmal. Én ezt tettem, utána külön beállítás nélkül működött.
2. Csatlakoztasd a vevőt USB-n a telefonhoz. Androiddal adapter nélkül, magától működik; iPhone-nal ez a megoldás nem használható.
3. Az SW Mapsben add hozzá a vevőt külső GNSS-eszközként, majd állítsd be az NTRIP-kapcsolatot: a kiszolgáló `crtk.net`, a port `2101`. Csatolási pontnak válaszd a legközelebbi Centipede bázist a lefedettségi térképről, vagy a `NEAR` pontot. Utóbbi csak akkor küld korrekciót, ha a kliens GGA-mondatot küld.
4. Add meg az antennamagasságot. Döntsd el előre, hogy kell-e geoidfájl: ha országos magassági rendszerben kellenek az adatok, azt külön kell beállítani.
5. Várd meg, amíg az SW Maps RTK Fix állapotot mutat. Tartsd a rudat a pont fölött, a vízmértékkel ellenőrizd, hogy függőleges-e, és pontonként átlagolj. Én 60 másodpercig átlagoltam.
6. A pontokat exportáld, és a feldolgozásnál ne vond le még egyszer az antennamagasságot, ha az SW Mapsben már megadtad.

## Mire figyelj

- A pontosság a bázisállomás távolságától, a mobilnet lefedettségétől és az égbolt szabad részétől függ. Fák alatt, épület mellett vagy völgyben a Fix elmaradhat, és csak Float megoldás jön létre.
- A Fix állapotot minden pontnál ellenőrizd. Az export nem rögzíti, hogy a teljes átlagolás alatt megvolt-e.
- A 2 m-es rúd felfelé vagy oldalra billentve légvezetékbe érhet. Légvezeték közelében és zivatarban ne mérj vele.

## Licenc

A teljes dokumentáció CC BY-SA 4.0. Az ArduSimple készlet, az SW Maps és a Centipede szolgáltatás a saját feltételeik szerint használható.
