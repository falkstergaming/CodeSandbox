# CodeSandbox

Ein modularer **Entwicklungs-Hub** – aufgebaut wie ein großes Hotel.  
Lobby, Museum, Labor, Werkräume und weitere Anbauten wachsen unabhängig voneinander.

> Basis: Design-Sprache und UI-Infrastruktur von [Assault on Grayskull](https://github.com/falkstergaming/Assault)  
> Stack: **Python · Pygame**  
> Status: **Alpha v0.2**

---

## Zielbild

```
                ╔══════════════════════════════════════════════════════╗
                ║                  CODESANDBOX                        ║
   [VORHOF]     ║  [LOBBY]  [MUSEUM]  [LABOR]  [GALERIE]  [JUKEBOX]  ║
   Außen ──────►║                                                     ║
                ║  [SPRENGSTOFF]  [RAUM 1]  [RAUM 2]  [RAUM 8]  …   ║
                ╚══════════════════════════════════════════════════════╝
```

---

## Räume nach Reifegrad (Gold / Silber / Bronze)

Die Räume des Hotels folgen einer Reife-Skala. Farben sind **semantisch**, nicht dekorativ:

| Farbe | Bedeutung | Räume |
|-------|-----------|-------|
| **Gold** | Poliert · Fertig · Stabil | Museum, Jukebox, Vorhof |
| **Silber** (Petrol) | In Arbeit · Schliff | Labor, Raum 1, Raum 2 |
| **Bronze** | Rohbau · Riskant · Unfertig | Galerie, Sprengstoff, Raum 8 |

---

## Button-Belegung

### Linke Spalte (Buttons 0–4)

| Button | Symbol | Farbe | Modus |
|--------|--------|-------|-------|
| 0 (oben) | ⏳ | Gold | Lobby |
| 1 | 🔒 | Gold | Museum |
| 2 | ? | Silber | Raum 2 (reserviert) |
| 3 | ⛰ | Bronze | Galerie |
| 4 (unten) | ♪ | Gold | Jukebox |

### Rechte Spalte (Buttons 5–9)

| Button | Symbol | Farbe | Modus |
|--------|--------|-------|-------|
| 5 (oben) | ⚙ | Gold | Settings-Menü |
| 6 | ⚗ | Silber | Labor |
| 7 | 💣 | Bronze | Sprengstoff |
| 8 | ? | Bronze | Raum 8 (reserviert) |
| 9 (unten) | 🧭 | Gold | Vorhof |

### Tastatur-Shortcuts

| Taste | Modus |
|-------|-------|
| `G` | Lobby / Sandbox |
| `S` | Museum |
| `D` | Lab (alt, Stub) |
| `P` | Prototype (alt, Stub) |
| `ESC` | Beenden |

---

## Farbkonzept

### Palette (`core/utils/colors.py`)

Vier Farbfamilien, je **5 Tonstufen**:

| Familie | Charakter | overtone | hightone | midtone | halftone | lowtone |
|---------|-----------|----------|----------|---------|----------|---------|
| `GRAU` | Kühl, neutral | `(31,33,41)` | `(44,50,64)` | `(75,83,100)` | `(150,162,180)` | `(220,225,234)` |
| `SILBER` | Petrol/Teal | `(17,46,63)` | `(34,96,112)` | `(54,153,168)` | `(146,205,214)` | `(224,241,244)` |
| `GOLD` | Warmes Amber | `(40,28,0)` | `(90,61,0)` | `(163,120,0)` | `(222,192,104)` | `(248,240,214)` |
| `BRONZE` | Warmes Kupfer | `(40,22,0)` | `(92,50,0)` | `(158,96,32)` | `(212,160,104)` | `(244,226,206)` |

Zugriff: `GRAU["midtone"]`, `GOLD["halftone"]`, `PALETTE["silber"]["lowtone"]`

### Button-Farbregeln

- **Gold-Buttons**: Räume mit klarer, stabiler Identität (Museum 🔒, Jukebox ♪, Vorhof 🧭, Settings ⚙)
- **Silber-Buttons**: Arbeits- und Entwicklungsräume (Labor ⚗, Raum 1 ?, Raum 2 ?)
- **Bronze-Buttons**: Rohbau, Risiko, Unfertig (Galerie ⛰, Sprengstoff 💣, Raum 8 ?)

---

## UI-Infrastruktur (zentral, persistent)

### AppHeader (`interfaces/renderer/pygame/components/header.py`)

- Obere **12% des Bildschirms**
- Links: „CODE SANDBOX" mit `◆ TITEL ◆`-Muster und Gold-Linien
- Rechts: Name + Kurzbeschreibung des aktiven Modus
- Unterstützte Modi: alle 10 Räume + Lobby

### Console (`interfaces/renderer/pygame/components/console.py`)

- Persistente Log-Konsole im unteren Bildbereich
- `console.log("Text", symbol_type="info")` — Typen: `info · warning · success · error · highlight · phase`

### Settings-Menü (`interfaces/renderer/pygame/components/settings_menu.py`)

- Button 5 (⚙, Gold) togglet das Overlay
- Sprachauswahl (DE/EN), Musik- und Effekt-Lautstärke
- GRAU-Theme mit Gold-Akzenten

### Dekor-Ketten (`main.py → _render_diamond_chains`)

Zwei vertikale Gold-Bänder durch beide Button-Spalten, von y=0 bis y=Bildschirmhöhe.  
Header und Console überdecken die Enden — Kette wirkt „unendlich".

---

## Architektur

### Modularitätsprinzip

Jeder Raum ist ein eigenständiges Python-Modul unter `modes/`.  
`main.py` koppelt über eine schmale Schnittstelle: `render_content`, `update`, `handle_event`, `on_enter`, `set_app_callbacks`.

### Exception-Isolation

**Fehler in einem Modus stürzen die App nicht ab.**

`main.py` kapselt alle Modus-Aufrufe in `try/except`. Ein Fehler zeigt ein rotes Overlay im betroffenen Bereich — alle anderen Modi laufen weiter.

---

## Aktueller Stand

### Fertig
- [x] App-Gerüst (Fenster, Modus-Wechsel, Startup-Fade)
- [x] 10 Hex-Buttons (5 links + 5 rechts) mit Farb-Semantik Gold/Silber/Bronze
- [x] Exception-Isolation
- [x] AudioManager mit Fade-In/Out
- [x] Hintergrundbild-Loader
- [x] **Farbkonzept** (GRAU / SILBER / GOLD / BRONZE, je 5 Tonstufen)
- [x] **AppHeader** — persistente Kopfzeile
- [x] **Console** — persistente Log-Konsole
- [x] **Settings-Menü** (⚙, Gold, Button 5)
- [x] **Dekor-Ketten** — Band + Diamanten durch Button-Spalten
- [x] **Museum** (🔒, Gold, Button 0) — Petrol-Theme, Nav-Hexagone, Exponat 4000
- [x] **Jukebox** (♪, Gold, Button 4) — Stub, Gold-Tint
- [x] **Galerie** (⛰, Bronze, Button 3) — Stub, Bronze-Tint
- [x] **Vorhof** (🧭, Gold, Button 9) — Stub, kein Tint
- [x] **Labor** (⚗, Silber, Button 6) — Stub, Silber-Tint
- [x] **Sprengstoff** (💣, Bronze, Button 7) — Stub, Bronze-Tint
- [x] **Raum 1** (?, Silber, Button 1) — Stub, Silber-Tint
- [x] **Raum 2** (?, Silber, Button 2) — Stub, Silber-Tint
- [x] **Raum 8** (?, Bronze, Button 8) — Stub, Bronze-Tint
- [x] **Lobby / Sandbox** (G-Taste) — bewusst leer, nur Infrastruktur

---

## ToDo

### Vorhof (nächste Priorität)
- [ ] Gebäude-Grundriss / Karte aller Räume
- [ ] Klickbare Raumkarte → Direktnavigation
- [ ] Raumzustände anzeigen (aktiv / in Entwicklung / gesperrt)
- [ ] Versions- und Projekt-Infos

### Jukebox
- [ ] MP3-Ordner einlesen und auflisten
- [ ] Play / Pause / Skip / Shuffle
- [ ] Moodboard-Editor: Playlisten erstellen, benennen, speichern
- [ ] Unabhängig von den globalen Settings

### Galerie
- [ ] Bilddateien (PNG, JPG) aus Ordner einlesen
- [ ] Vollbild-Viewer mit Prev/Next
- [ ] Alben / Sammlungen
- [ ] Slideshow-Modus

### Museum
- [ ] Mehr Exponate (4001, 4002, …)
- [ ] Scrollbare Exponat-Übersicht
- [ ] Farbpaletten-Schaukasten als eigenes Exponat

### Labor & Sprengstoff
- [ ] Labor: Silber-Theme ausbauen, interaktive Panels
- [ ] Sprengstoff: Bronze-Theme, freies Canvas für Hochrisiko-Tests

### Reservierte Räume
- [ ] Raum 1, 2, 8 — Zweckbestimmung festlegen und Symbol/Namen vergeben

### Infrastruktur
- [ ] `core/utils/room_themes.py` — semantische Farbschlüssel pro Raum
- [ ] Hot-Reload: Modul zur Laufzeit neu laden
- [ ] Modul-Gesundheitsanzeige am Button (Punkt bei bekanntem Fehler)
- [ ] Persistente Modus-Zustände

---

## Projektstruktur

```
CodeSandbox/
├── main.py                              # App-Einstiegspunkt, 10 Buttons, Modus-Routing
├── settings.ini
├── requirements.txt
│
├── modes/
│   ├── sandbox.py                       # Lobby (leer – nur Infrastruktur sichtbar)
│   ├── museum.py                        # Museum: Nav-Hexagone + Exponate (Petrol-Theme)
│   ├── jukebox.py                       # Jukebox: MP3-Player (Stub, Gold-Theme)
│   ├── gallery.py                       # Galerie: Bildbetrachter (Stub, Bronze-Theme)
│   ├── vorhof.py                        # Vorhof: Gebäude-Übersicht / Wegweiser (Stub)
│   ├── labor.py                         # Labor: Werkstatt (Stub, Silber-Theme)
│   ├── sprengstoff.py                   # Sprengstoff: Hochrisiko (Stub, Bronze-Theme)
│   ├── raum_1.py                        # Raum 1: reserviert (Stub, Silber-Theme)
│   ├── raum_2.py                        # Raum 2: reserviert (Stub, Silber-Theme)
│   ├── raum_8.py                        # Raum 8: reserviert (Stub, Bronze-Theme)
│   ├── lab.py                           # (alt – D-Taste)
│   └── prototype.py                     # (alt – P-Taste)
│
├── core/utils/
│   ├── colors.py                        # Farbpalette: GRAU/SILBER/GOLD/BRONZE
│   ├── global_constants.py              # Konstanten, Fonts, Palette-Importe
│   ├── settings.py                      # INI-basierte Einstellungen
│   └── translations.py                  # DE/EN-Übersetzungen
│
├── interfaces/renderer/pygame/
│   ├── audio.py                         # AudioManager
│   ├── screen.py                        # Hintergrundbild-Management
│   └── components/
│       ├── button.py                    # HexButton + draw_raised_effects
│       ├── header.py                    # AppHeader (persistente Kopfzeile)
│       ├── console.py                   # Console (persistente Log-Konsole)
│       └── settings_menu.py             # Settings-Overlay (GRAU-Theme)
│
├── media/                               # Musik, Hintergrundbilder
└── artwork/                             # Weitere Grafiken
```

---

## Namenskonventionen

- Alles heißt **App**, nicht Game (`AppHeader`, `app_callbacks` — nie `game_*`)
- Modi sind **Räume**, nicht Spielzustände
- Buttons sind **Eingänge**, nicht Actions

---

## Installation & Start

```bash
pip install -r requirements.txt
python main.py
```
