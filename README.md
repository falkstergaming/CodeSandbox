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
- **Lobby / Vorplatz** – Empfang, Navigation, Startpunkt  
- **Museum** – Ausstellungsraum für fertige Objekte und Design-Referenzen  
- **Labor** – Werkstatt für aktive Entwicklung, Prototypen, Experimente  
- **Testgelände (Prototyp)** – Sandbox für neue Ideen ohne Stabilitätspflicht  
- **[Weitere Flügel]** – kommen nach Bedarf hinzu (Galerie, Demo-Raum, Archiv, …)

---

## Architektur & Live-Entwicklungs-Stabilität

> ⚠️ **Hohe Priorität:** Das System ist explizit für parallele Live-Entwicklung ausgelegt.

### Modularitätsprinzip

Jeder Flügel ist ein eigenständiges Python-Modul unter `modes/`.  
Die Hauptanwendung (`main.py`) koppelt diese Module nur über eine schmale Schnittstelle:

```
modes/
  sandbox.py    → Lobby-Inhalt
  museum.py     → Museum + Exponate
  lab.py        → Labor
  prototype.py  → Testgelände
```

### Exception-Isolation

**Fehler in einem Modus stürzen die App nicht ab.**

`main.py` kapselt alle Aufrufe (`render_content`, `update`, `handle_event`) in `try/except`-Blöcken.  
Wirft ein Modus eine Exception, zeigt die App ein rotes Fehler-Overlay im betroffenen Bereich –  
alle anderen Modi bleiben vollständig funktionsfähig.

```
Szenario: Du entwickelst lab.py und baust einen SyntaxError / RuntimeError ein.
  → Du sitzt in der Lobby (G) und siehst nichts davon.
  → Du wechselst in den Labor-Modus (D): roter Fehlerscreen.
  → Fehler beheben, Modus wechseln, fertig.
  → Die App hat die ganze Zeit ohne Absturz weitergelaufen.
```

### Was diese Isolation NICHT abdeckt

- Fehler in `main.py` selbst (Vorplatz) betreffen die ganze App  
- Fehler beim **Import** eines Moduls beim Start (→ App startet nicht)  
- Fehler in geteilter Infrastruktur (`core/`, `interfaces/`) betreffen alle Modi

---

## Navigation

| Taste | Modus      | Button |
|-------|-----------|--------|
| `G`   | Sandbox / Lobby | G |
| `S`   | Museum    | S |
| `D`   | Labor     | D |
| `P`   | Prototyp  | ⚙ |
| `⏳`  | Settings-Menü öffnen/schließen | ⏳ |
| `ESC` | Beenden   | — |

---

## Aktueller Stand

### Fertig
- [x] App-Gerüst (Fenster, Modus-Wechsel, Startup-Fade)
- [x] 5 Hex-Buttons rechts (1:1 aus Assault on Grayskull)
- [x] Settings-Menü (Sprache DE/EN, Musik-Lautstärke, Effekt-Lautstärke)
- [x] AudioManager mit Fade-In/Fade-Out
- [x] Hintergrundbild-Loader (SVG, JPG, PNG – Suche in `media/`, `artwork/`)
- [x] Lobby / Sandbox-Modus mit 3 Navigations-Hexagonen
- [x] Museum-Modus mit Galerie-Ansicht
- [x] **Button 4000** – erstes Museum-Exponat (HexButton Design-Referenz)
  - Schaukasten: alle 4 Fraktionen × 4 Zustände (Normal, Hover, Selektiert, Deaktiviert)
  - Interaktiver Demo-Bereich
- [x] Labor-Modus (Stub)
- [x] Prototyp-Modus (Stub)
- [x] Exception-Isolation: Modusfehler → Fehlerscreen, App läuft weiter

---

## ToDo

### Infrastruktur
- [ ] Hot-Reload: Modul zur Laufzeit neu laden ohne App-Neustart (`importlib.reload`)
- [ ] Modul-Gesundheitsanzeige: roter Punkt am Button bei bekanntem Fehler
- [ ] Logging-Konsole (wie Assault's Console-Komponente) für Entwickler-Output
- [ ] Persistente Modus-Zustände (zuletzt geöffnetes Exponat etc.)

### Museum
- [ ] Mehr Exponate hinzufügen (Button 4001, 4002, …)
- [ ] Exponat-Übersicht als scrollbare Galerie
- [ ] Exponat-Metadaten (Beschreibung, Erstellungsdatum, Kategorie)

### Labor
- [ ] Echter Labor-Inhalt: interaktive Code-Experimente
- [ ] Variablen-Inspector / Live-Editor-Panel

### Prototyp / Testgelände
- [ ] Freies Canvas für Ad-hoc-Tests
- [ ] Import-Mechanismus für externe Test-Skripte

### Lobby
- [ ] Willkommens-Animation beim Start
- [ ] Neuigkeiten / Changelog-Panel
- [ ] Uhr / Live-Systeminformationen

### Design
- [ ] Eigene Hintergrundbilder (media/, artwork/)
- [ ] Eigene Soundscapes (media/*.mp3)
- [ ] Farbthema konfigurierbar (nicht mehr Assault-gebunden)

---

## Technische Basis (von Assault on Grayskull übernommen)

| Komponente | Herkunft | Pfad |
|-----------|----------|------|
| `HexButton` | 1:1 | `interfaces/renderer/pygame/components/button.py` |
| Farb-System (Fraktionen, Zustände) | 1:1 | `core/utils/colors.py` |
| `AudioManager` (Fade-In/Out) | 1:1, media_dir angepasst | `interfaces/renderer/pygame/audio.py` |
| `Screen` (Hintergrundbild-Loader) | 1:1, Titel angepasst | `interfaces/renderer/pygame/screen.py` |
| `Settings` (INI-Datei) | 1:1 | `core/utils/settings.py` |
| `SettingsMenu` (Overlay) | 1:1 | `interfaces/renderer/pygame/components/settings_menu.py` |
| Übersetzungen (DE/EN) | angepasst | `core/utils/translations.py` |
| `global_constants` | angepasst (game-Logik entfernt) | `core/utils/global_constants.py` |

---

## Installation & Start

```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Starten
python main.py
```

**Optional:** Hintergrundbilder (JPG/PNG/SVG mit Namen `background*`) in `media/` oder `artwork/` legen.  
**Optional:** Musik-Dateien (MP3) aus Assault in `media/` kopieren.

---

## Projektstruktur

```
CodeSandbox/
├── main.py                          # App-Einstiegspunkt, 5 Buttons, Modus-Verwaltung
├── settings.ini                     # Auto-generiert beim ersten Start
├── requirements.txt
│
├── modes/                           # ← Hier wächst das Gebäude
│   ├── sandbox.py                   # Lobby / Vorplatz
│   ├── museum.py                    # Ausstellungsraum + Exponate
│   ├── lab.py                       # Labor (Werkstatt)
│   └── prototype.py                 # Testgelände
│
├── core/utils/
│   ├── colors.py                    # Farbpalette (Assault)
│   ├── global_constants.py          # Konstanten (Fonts, Größen, …)
│   ├── settings.py                  # INI-basierte Einstellungen
│   └── translations.py             # DE/EN-Übersetzungen
│
├── interfaces/renderer/pygame/
│   ├── audio.py                     # AudioManager
│   ├── screen.py                    # Hintergrundbild-Management
│   └── components/
│       ├── button.py                # HexButton + draw_raised_effects
│       └── settings_menu.py        # Settings-Overlay
│
├── media/                           # Musik, Hintergrundbilder
└── artwork/                         # Weitere Grafiken
```
