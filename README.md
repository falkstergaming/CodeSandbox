# CodeSandbox

Ein modularer **Entwicklungs-Hub** – aufgebaut wie ein großes Hotel.  
Lobby, Museum, Labor, Testgelände und weitere Anbauten wachsen unabhängig voneinander.

> Basis: Design-Sprache und UI-Infrastruktur von [Assault on Grayskull](https://github.com/falkstergaming/Assault)  
> Stack: **Python · Pygame**  
> Status: **Alpha v0.1**

---

## Zielbild

```
                ╔══════════════════════════════════════╗
                ║           CODESANDBOX                ║
                ║                                      ║
  ┌─────────┐   ║   ┌──────┐  ┌──────┐  ┌──────────┐  ║
  │ LOBBY   │◄──╬───│Muse- │  │Labor │  │Prototyp  │  ║
  │ Vorplatz│   ║   │  um  │  │      │  │Testgelände│  ║
  └─────────┘   ║   └──────┘  └──────┘  └──────────┘  ║
                ║                                      ║
                ║   [zukünftige Anbauten...]           ║
                ╚══════════════════════════════════════╝
```

CodeSandbox ist ein wachsendes Programm-Gebäude:
- **Lobby / Vorplatz** – Empfang, Ausgangspunkt; zeigt keinen eigenen Inhalt (nur Infrastruktur)
- **Museum** – Navigationspunkt + Ausstellungsraum für fertige Objekte und Design-Referenzen
- **Labor** – Werkstatt für aktive Entwicklung, Prototypen, Experimente
- **Testgelände (Prototyp)** – Sandbox für neue Ideen ohne Stabilitätspflicht
- **[Weitere Flügel]** – kommen nach Bedarf hinzu (Galerie, Demo-Raum, Archiv, …)

### Räume nach Reifegrad (Gold / Silber / Bronze)

Die Räume des Hotels folgen einer Reife-Skala. Die Farben sind nicht dekorativ, sondern semantisch:

| Farbe | Bedeutung | Räume |
|-------|-----------|-------|
| **Gold** | Poliert · Fertig · Stabil | Museum, Exponate, Archiv |
| **Silber** (Petrol) | In Arbeit · Schliff · Simulationen | Labor, Balancing, Tuning |
| **Bronze** | Rohbau · Ideen ohne Pflicht | Prototyp, Testgelände |

---

## Architektur & Live-Entwicklungs-Stabilität

> ⚠️ **Hohe Priorität:** Das System ist explizit für parallele Live-Entwicklung ausgelegt.

### Modularitätsprinzip

Jeder Flügel ist ein eigenständiges Python-Modul unter `modes/`.  
Die Hauptanwendung (`main.py`) koppelt diese Module nur über eine schmale Schnittstelle:

```
modes/
  sandbox.py    → Lobby / Vorplatz (kein eigener Inhalt)
  museum.py     → Museum: Nav-Hexagone + Exponate (Petrol-Theme)
  lab.py        → Labor (Werkstatt)
  prototype.py  → Testgelände
```

### Exception-Isolation

**Fehler in einem Modus stürzen die App nicht ab.**

`main.py` kapselt alle Aufrufe (`render_content`, `update`, `handle_event`) in `try/except`-Blöcken.  
Wirft ein Modus eine Exception, zeigt die App ein rotes Fehler-Overlay im betroffenen Bereich –  
alle anderen Modi bleiben vollständig funktionsfähig.

```
Szenario: Du entwickelst lab.py und baust einen SyntaxError / RuntimeError ein.
  → Du sitzt in der Lobby und siehst nichts davon.
  → Du wechselst ins Labor: roter Fehlerscreen.
  → Fehler beheben, Modus wechseln, fertig.
  → Die App hat die ganze Zeit ohne Absturz weitergelaufen.
```

**Was diese Isolation NICHT abdeckt:**
- Fehler in `main.py` selbst betreffen die ganze App
- Fehler beim **Import** eines Moduls beim Start → App startet nicht
- Fehler in geteilter Infrastruktur (`core/`, `interfaces/`) betreffen alle Modi

---

## Navigation

### Tastatur

| Taste | Modus |
|-------|-------|
| `G`   | Lobby / Sandbox |
| `S`   | Museum |
| `D`   | Labor |
| `P`   | Prototyp |
| `ESC` | Beenden |

### Buttons (10 Hex-Buttons, 5 links + 5 rechts)

| Position | Symbol | Farbe | Funktion |
|----------|--------|-------|----------|
| Links 0 (oben) | 🔒 | Gold | Museum |
| Links 1–4 | 1–4 | Neutral | frei |
| Rechts 5 (oben) | ⚙ | Gold | Settings-Menü öffnen/schließen |
| Rechts 6 | 6 | Neutral | Lobby / Sandbox |
| Rechts 7 | 7 | Neutral | Prototyp |
| Rechts 8 | 8 | Neutral | Museum |
| Rechts 9 | 9 | Neutral | Labor |

---

## Farbkonzept

### Palette (`core/utils/colors.py`)

Vier Farbfamilien, je **5 Tonstufen** (benannt statt nummeriert):

| Familie | Charakter | overtone | hightone | midtone | halftone | lowtone |
|---------|-----------|----------|----------|---------|----------|---------|
| `GRAU` | Kühl, neutral | `(31,33,41)` | `(44,50,64)` | `(75,83,100)` | `(150,162,180)` | `(220,225,234)` |
| `SILBER` | Petrol/Teal | `(17,46,63)` | `(34,96,112)` | `(54,153,168)` | `(146,205,214)` | `(224,241,244)` |
| `GOLD` | Warmes Amber | `(40,28,0)` | `(90,61,0)` | `(163,120,0)` | `(222,192,104)` | `(248,240,214)` |
| `BRONZE` | Warmes Kupfer | `(40,22,0)` | `(92,50,0)` | `(158,96,32)` | `(212,160,104)` | `(244,226,206)` |

Zugriff: `GRAU["midtone"]`, `GOLD["halftone"]`, `PALETTE["silber"]["lowtone"]`

### Tonhierarchie pro Raum

Jeder Raum kombiniert die Palette nach fester Hierarchie:

```
Museum (Gold · Petrol · Grau):
  GRAU     → dominant   (~70% Fläche: Hintergrund, Großflächen)
  SILBER   → Akzent     (~25%: Buttons, Rahmen, Labels, Trennlinien)
  GOLD     → Highlight  (~5%: Ausgewählte Elemente, Akzent-Diamanten)
```

> **Merkrege:** SILBER ist der Schmuck, GOLD ist der Edelstein darin.

**Geplant:** `core/utils/room_themes.py` — einheitliche semantische Farbschlüssel  
(`bg_tint`, `border`, `text`, `accent`, `btn_fill`, …) pro Raum, abgeleitet aus der Palette.

---

## UI-Infrastruktur (zentral, persistent)

Diese Elemente liegen in `main.py` und bleiben bei jedem Modus-Wechsel sichtbar.  
Sie werden nach dem Modus-Inhalt gerendert und überdecken ihn am Rand.

### AppHeader (`interfaces/renderer/pygame/components/header.py`)

- Belegt obere **12% des Bildschirms** (y=25, Höhe ≈96px)
- **Linker Block:** Titel „CODE SANDBOX" mit `◆ TITEL ◆`-Muster und Gold-Linien
- **Rechter Block:** Name des aktiven Modus (LOBBY · MUSEUM · LABOR · PROTOTYP) + Kurzbeschreibung
- Visuelle Sprache 1:1 aus Assault on Grayskull: weißer Außenrahmen, Gold-Innenrahmen (3px), L-förmige Ecken mit Diamant, Separator-Linien mit Diamant-Endmarken

### Console (`interfaces/renderer/pygame/components/console.py`)

- Persistente **Log-Konsole** im unteren Bildbereich
- `console.log("Text", symbol_type="info")` — Typen: `info · warning · success · error · highlight · phase`
- Gleiche Dekorationssprache wie Header (Rahmen, Ecken, transparenter Hintergrund)
- Aus `main.py` heraus zugreifbar via `app.console.log(...)`

### Settings-Menü (`interfaces/renderer/pygame/components/settings_menu.py`)

- Wird durch **Button 5 (⚙)** getriggert (Gold-Button, rechte Spalte oben)
- Farbkonzept: **GRAU-Theme** — dunkler Hintergrund, Gold-Akzente, Petrol-Trennlinien
- Enthält: Sprachauswahl (DE/EN), Musik-Lautstärke, Effekt-Lautstärke
- Separator-Linien mit Diamant-Endmarken (konsistent mit Header/Console)
- Erscheint unterhalb des Headers (y=130), rechtsbündig

### Dekor-Ketten (`main.py → _render_diamond_chains`)

Zwei vertikale Gold-Bänder (links + rechts) ziehen sich durch die Button-Spalten:

```
  ◆  ◆  ◆  ◆  ◆     ← 5 kleine Diamanten Richtung Header
  [Button]            ← 5 Hex-Buttons = "dicke Diamanten" der Kette
  ◆  ◆  ◆  ◆  ◆     ← 5 kleine Diamanten Richtung Console
```

- Das Band (3px: dunkel/gold/dunkel) läuft von y=0 bis y=Bildschirmhöhe
- Header und Console überdecken die Enden → Kette wirkt „unendlich"
- Buttons rendern sich obendrüber und decken das Band in ihrem Bereich ab

---

## Aktueller Stand

### Fertig
- [x] App-Gerüst (Fenster, Modus-Wechsel, Startup-Fade)
- [x] 10 Hex-Buttons (5 links + 5 rechts), mit Reposition bei Fenstergrößenänderung
- [x] Exception-Isolation: Modusfehler → Fehlerscreen, App läuft weiter
- [x] AudioManager mit Fade-In/Fade-Out
- [x] Hintergrundbild-Loader (SVG, JPG, PNG – Suche in `media/`, `artwork/`)
- [x] **Farbkonzept CodeSandbox** (GRAU / SILBER / GOLD / BRONZE, je 5 Tonstufen)
- [x] **AppHeader** — persistente Kopfzeile mit Titel + aktivem Modus
- [x] **Console** — persistente Log-Konsole (unten), mit Symbol-Typen
- [x] **Settings-Menü** (GRAU-Theme, Gold-Akzente) + **Button 5 (⚙, Gold)**
- [x] **Dekor-Ketten** — Band durch Button-Spalten, 5+5 Diamanten, Header/Console-Clipping
- [x] **Button 0 (🔒, Gold)** — navigiert ins Museum
- [x] **Museum-Modus** mit Petrol-Theme (GRAU + SILBER + GOLD)
  - 3 Navigations-Hexagone: Labor · Prototyp · Exponate
  - Exponat-Kachel 4000 (HexButton Design-Referenz)
  - Petrol-Tint-Overlay über Content-Bereich
- [x] **Exponat 4000** — HexButton Design-Referenz
  - Schaukasten: alle 4 Fraktionen × 4 Zustände (Normal, Hover, Selektiert, Deaktiviert)
  - Interaktiver Demo-Bereich
- [x] **Lobby** — bewusst leer (nur Infrastruktur sichtbar)
- [x] Labor-Modus (Stub)
- [x] Prototyp-Modus (Stub)

---

## ToDo

### Infrastruktur
- [ ] `core/utils/room_themes.py` — semantische Farbschlüssel pro Raum (`bg_tint`, `border`, `text`, `accent`, …)
- [ ] Hot-Reload: Modul zur Laufzeit neu laden ohne App-Neustart (`importlib.reload`)
- [ ] Modul-Gesundheitsanzeige: farbiger Punkt am Button bei bekanntem Fehler
- [ ] Persistente Modus-Zustände (zuletzt geöffnetes Exponat etc.)

### Navigation & Buttons
- [ ] Buttons 1–4 (links) belegen: Labor, Prototyp, weitere Räume
- [ ] Buttons 7–9 (rechts) sauber benennen / umwidmen wenn Räume wachsen
- [ ] Keyboard-Shortcuts aktualisieren sobald Belegung feststeht

### Museum
- [ ] Mehr Exponate hinzufügen (Button 4001, 4002, …)
- [ ] Exponat-Übersicht als scrollbare Galerie
- [ ] Exponat-Metadaten (Beschreibung, Erstellungsdatum, Kategorie)
- [ ] Eigenes Gold-Exponat: Farbpaletten-Schaukasten (GRAU / SILBER / GOLD / BRONZE)

### Labor
- [ ] Echter Labor-Inhalt: interaktive Code-Experimente
- [ ] Variablen-Inspector / Live-Editor-Panel
- [ ] Silber-Theme (GRAU + SILBER, kein Gold)

### Prototyp / Testgelände
- [ ] Bronze-Theme (GRAU + BRONZE)
- [ ] Freies Canvas für Ad-hoc-Tests
- [ ] Import-Mechanismus für externe Test-Skripte

### Lobby / Vorplatz
- [ ] Willkommens-Animation beim Start
- [ ] Neuigkeiten / Changelog-Panel

### Design
- [ ] `room_themes.py` anlegen und Museum-Theme migrieren
- [ ] Eigene Hintergrundbilder (`media/`, `artwork/`)
- [ ] Eigene Soundscapes (`media/*.mp3`)

---

## Namenskonventionen

- Alles in CodeSandbox heißt **App**, nicht Game.  
  (`app.py`, `AppHeader`, `app_callbacks` — niemals `game_*`)
- Modi sind Räume, nicht Spielzustände
- Buttons sind Eingänge, nicht Actions

---

## Technische Basis

| Komponente | Herkunft | Pfad |
|-----------|----------|------|
| `HexButton` | 1:1 aus Assault | `interfaces/renderer/pygame/components/button.py` |
| `AudioManager` | 1:1, media_dir angepasst | `interfaces/renderer/pygame/audio.py` |
| `Screen` (Hintergrundbild-Loader) | 1:1, Titel angepasst | `interfaces/renderer/pygame/screen.py` |
| `Settings` (INI-Datei) | 1:1 | `core/utils/settings.py` |
| Übersetzungen (DE/EN) | angepasst | `core/utils/translations.py` |
| `AppHeader` | neu (aus GameStatusDisplay adaptiert) | `interfaces/renderer/pygame/components/header.py` |
| `Console` | adaptiert aus Assault | `interfaces/renderer/pygame/components/console.py` |
| `SettingsMenu` | neu (GRAU-Theme) | `interfaces/renderer/pygame/components/settings_menu.py` |
| Farbpalette CodeSandbox | neu | `core/utils/colors.py` (GRAU/SILBER/GOLD/BRONZE) |
| `global_constants` | angepasst | `core/utils/global_constants.py` |

---

## Installation & Start

```bash
pip install -r requirements.txt
python main.py
```

**Optional:** Hintergrundbilder (`background*` als JPG/PNG/SVG) in `media/` oder `artwork/`.  
**Optional:** Musik-Dateien (MP3) in `media/`.

---

## Projektstruktur

```
CodeSandbox/
├── main.py                              # App-Einstiegspunkt, 10 Buttons, Modus-Verwaltung
├── settings.ini                         # Auto-generiert beim ersten Start
├── requirements.txt
│
├── modes/                               # ← Hier wächst das Gebäude
│   ├── sandbox.py                       # Lobby / Vorplatz (leer – nur Infrastruktur)
│   ├── museum.py                        # Museum: Nav-Hexagone + Exponate (Petrol-Theme)
│   ├── lab.py                           # Labor (Werkstatt, Stub)
│   └── prototype.py                     # Testgelände (Stub)
│
├── core/utils/
│   ├── colors.py                        # Farbpalette: GRAU/SILBER/GOLD/BRONZE + Assault-Farben
│   ├── global_constants.py              # Konstanten (Fonts, Größen, Palette-Importe, Symbole)
│   ├── settings.py                      # INI-basierte Einstellungen
│   └── translations.py                  # DE/EN-Übersetzungen
│
├── interfaces/renderer/pygame/
│   ├── audio.py                         # AudioManager (Fade-In/Out)
│   ├── screen.py                        # Hintergrundbild-Management
│   └── components/
│       ├── button.py                    # HexButton + draw_raised_effects
│       ├── header.py                    # AppHeader (persistente Kopfzeile)
│       ├── console.py                   # Console (persistente Log-Konsole)
│       └── settings_menu.py             # Settings-Overlay (GRAU-Theme)
│
├── core/utils/
│   └── Farbkonzept_CodeSandbox.png      # Design-Referenz für die Farbpalette
│
├── media/                               # Musik, Hintergrundbilder
└── artwork/                             # Weitere Grafiken
```
