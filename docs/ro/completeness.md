---
title: Completitudinea
nav_order: 8
lang: "ro"
source: completeness.md
source_hash: "9bbf47120a80"
nav_exclude: true
search_exclude: true
---
# Completitudinea {#completeness}

Nimic dintr-un replay nu se aruncă. Ce citește convertorul intră în
tabel și în documentul meciului; fiecare alt element este păstrat întreg în fișierul auxiliar
`<match>.messages.parquet`; iar `selfCheck.completeness` din documentul meciului
numără ce s-a întâmplat cu fiecare fel de element. Aceasta este regula pe care o împart toate
convertoarele 3DHeat:
[Convertoarele păstrează tot](https://holdi601.github.io/3DHeat/converters.html).

![Autoverificarea unui replay sintetic: fiecare element văzut, citit, păstrat sau pierdut](../assets/img/completeness.svg)

## Numărătoarea {#the-count}

Pentru fiecare fel de element, `selfCheck.completeness.types` dă:

| Numărătoare | Înseamnă |
|---|---|
| `seen` | câte conține replay-ul |
| `decoded` | citite întregi |
| `partial` | citite parțial, și păstrate întregi în fișierul auxiliar |
| `raw` | doar păstrate întregi în fișierul auxiliar, necitite |
| `lost` | pierdute: mereu `0` |

Felurile sunt ale replay-ului însuși: `block 0` (antetul), `block 1` (rezultatele), `container sizes` și `deflate tail` (octeții proprii ai containerului),
`packet <type>`, iar pentru apelurile către entități `method <entity type>.<number>`
și `property <entity type>.<number>`. Tipurile de entități sunt numerele pe care le dau pachetele
de creare; `selfCheck.entities.roles` spune care este avatarul jucătorului care înregistrează și care sunt vehiculele. Un fel pe care nimeni nu îl cunoștea
apare cu numărătoarea sa.

## Fișierul auxiliar {#the-sidecar}

| Coloană | Ce este |
|---|---|
| `time` | ceasul replay-ului, ca în tabel |
| `type`, `name` | felul elementului; cum îl numește convertorul, acolo unde îl citește |
| `entity` | vehiculul sau avatarul căruia îi aparține, ca `entity` din tabel |
| `decoded` | ce s-a citit din el, ca JSON |
| `payload`, `text` | octeții săi, întregi; blocurile JSON, întregi |
| `entityType`, `packet`, `method` | numerele |

Rândurile sunt sortate după pachet, metodă, entitate și timp.

## Ce se citește, și cum a fost verificat {#what-is-read-and-how-it-was-checked}

- **Înclinarea și rularea** fiecărei poziții: înclinarea este minus panta traseului propriu al tancului cât timp merge înainte; două tancuri în același loc cu un cap au aceeași rulare, cu capete opuse au rulări opuse.
- **Entitățile** (`entities`): când a intrat fiecare în vederea clientului și când a ieșit. Niciun tanc nu are o poziție între ieșire și revenire.
- **Versiunea din flux** (`streamVersion`): aceeași cu cea din antet.
- **Ținta jucătorului care înregistrează** (pachetul 38): o direcție, în `decoded` din fișierul auxiliar (`forward`); la loviturile jucătorului este la o fracțiune de grad de locul unde a zburat obuzul.

Orice altceva citit (viața, loviturile, proiectilele, traseele de trasor, exploziile, unghiurile tunului,
actualizările arenei, chatul, modurile camerei, evenimentele clientului, pozițiile) este `partial`:
în tabel sau în documentul meciului, și păstrat întreg în fișierul auxiliar.

**Păstrat, dar necitit** (`raw`), cele mai mari feluri: actualizările de poziție care nu sunt în
tabel (ale avatarului, după moartea unui tanc, entitățile care nu sunt în listă), pachetele 26, 28, 29, 31, 36, 50, 54 și 57, unele proprietăți frecvente ale vehiculelor și avatarurilor, fiecare metodă și proprietate fără cititor (printre ele avarierea modulelor, echipajul și consumabilele), și proprietățile creărilor de entități.

## Ce nu este disponibil {#not-available}

- Ce nu a trimis niciodată serverul clientului care înregistrează: ținta, camera și comenzile altor jucători, inamicii nemarcați. Un replay este ce i s-a spus unui singur client.
- Numele tipurilor de entități, metodelor și proprietăților: sunt în fișierele de definiție ale jocului, nu în replay. Numerele sunt păstrate.
- Înălțimea în grade a tunului și orice altceva care are nevoie de datele proprii ale tancurilor din fișierele jocului.

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
