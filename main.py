"""
Einstiegspunkt für Code Sandbox.
Hauptanwendung mit Modus-Wechsel zwischen Sandbox, Museum, Labor und Prototyp.
Basiert auf Sturm auf Grayskull – game-spezifische Logik entfernt.

10 Hex-Buttons: 5 links (0-4) + 5 rechts (5-9), vertikal um Bildmitte zentriert.
  Rechts   5 y=256  → Prototyp-Modus
           6 y=316  → Sandbox-Modus (Start)
           7 y=376  → Settings-Menü toggle
           8 y=436  → Museum-Modus
           9 y=496  → Labor-Modus
  Links    0-4      → zukünftige Bereiche (Stubs)

Tastenkürzel: G=Sandbox  S=Museum  D=Labor  P=Prototyp  ESC=Beenden
"""
import pygame
from pygame.locals import *
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.utils.global_constants import (
    COLORS,
    UI_BUTTON_PRIMARY,
    UI_BUTTON_TEXT,
    UI_BUTTON_HIGHLIGHT,
    UI_BUTTON_HIGHLIGHT_TEXT,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GOLD,
    GRAU,
    BRONZE,
    SILBER,
    TEXT_LIGHT,
    TEXT_HIGHLIGHT,
)
from core.utils.settings import Settings
from interfaces.renderer.pygame.screen import Screen
from interfaces.renderer.pygame.audio import AudioManager


class App:
    """
    Hauptanwendung – verwaltet Modus-Wechsel und zentrale UI.

    Architektur:
    - Single Pygame-Instanz
    - Screen-Klasse für Hintergrundbild-Management
    - Modus-Wechsel ohne Neu-Initialisierung
    - 5 Hex-Buttons am rechten Rand (identisch mit Sturm auf Grayskull)
    - 4 Modi: sandbox, museum, lab, proto
    """

    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH  = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.MARGIN_LEFT   = 25
        self.MARGIN_RIGHT  = 25

        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Code Sandbox")

        # Screen-Manager für Hintergrundbild
        self.screen_manager = Screen(
            width=self.SCREEN_WIDTH,
            height=self.SCREEN_HEIGHT,
            screen=self.screen,
            resizable=True
        )

        # Einstellungen + Audio
        self.settings      = Settings()
        self.audio_manager = AudioManager(settings=self.settings)

        # Aktiver Modus
        self.mode = "sandbox"

        # Zentrale UI-Elemente (bleiben beim Modus-Wechsel erhalten)
        self._init_central_ui()

        # Startup-Fade: schwarzes Overlay blendet in 1 Sekunde aus
        self._fade_alpha:    int   = 255
        self._fade_elapsed:  float = 0.0
        self._fade_duration: float = 1.0

        # Isoliert Fehler pro Modus – App läuft bei Modus-Exception weiter
        self._mode_errors: dict = {}

        # Modi initialisieren
        self._init_modi()

    # ------------------------------------------------------------------
    # Initialisierung
    # ------------------------------------------------------------------

    def _init_central_ui(self):
        from interfaces.renderer.pygame.components.settings_menu import SettingsMenu
        from interfaces.renderer.pygame.components.button import HexButton
        from interfaces.renderer.pygame.components.header import AppHeader
        from interfaces.renderer.pygame.components.console import Console

        # Header (obere 12% des Bildschirms)
        self.header = AppHeader(
            width=self.SCREEN_WIDTH,
            height=self.SCREEN_HEIGHT,
            settings=self.settings,
        )

        # Console (unterer Bereich, persistent)
        _cx = self.MARGIN_LEFT + 48 + 10   # nach den linken Buttons
        _cw = self.SCREEN_WIDTH - _cx - 48 - 10 - self.MARGIN_RIGHT
        _ch = 160
        _cy = self.SCREEN_HEIGHT - _ch - 10
        self.console = Console(x=_cx, y=_cy, width=_cw, height=_ch)
        self.console.log("Code Sandbox gestartet.", symbol_type="success")

        # Settings-Menü (Overlay – unter dem Header, rechtsbündig)
        self.settings_menu = SettingsMenu(
            x=self.SCREEN_WIDTH - 25 - 300,
            y=130,
            settings=self.settings
        )

        # ===================================================================
        # 10 Hex-Buttons — Das Markenzeichen von CodeSandbox
        # 5 links (0–4) + 5 rechts (5–9), vertikal um Bildmitte zentriert
        # Positionen: y_c = Offset von Bildmitte (400), size=48, angle_offset=30
        # Linker Rand: x = MARGIN_LEFT (25)
        # Rechter Rand: x = SCREEN_WIDTH − MARGIN_RIGHT − 48 = 1207
        # Abstand zwischen Buttons: 60 px (size=48 + 12 px Lücke)
        # ===================================================================

        def _make_btn(x, y, text, y_c, callback=None, is_bold=True):
            btn = HexButton(
                x=x, y=y, size=48,
                color=UI_BUTTON_PRIMARY,
                text=text,
                callback=callback,
                highlight_color=UI_BUTTON_HIGHLIGHT,
                highlight_text_color=UI_BUTTON_HIGHLIGHT_TEXT,
                text_color=UI_BUTTON_TEXT,
                font_size=24,
                bold=is_bold,
                angle_offset=30,
                alpha=220,
            )
            btn.y_c = y_c
            return btn

        x_l = self.MARGIN_LEFT                              # linker Rand: 25
        x_r = self.SCREEN_WIDTH - self.MARGIN_RIGHT - 48   # rechter Rand: 1207

        # --- LINKS: Buttons 0–4 (oben → unten) ---
        # Button 0: Lobby – Sanduhr-Symbol, Gold
        self.button_0 = HexButton(
            x=x_l, y=256, size=48,
            color=GOLD["hightone"],
            text="⏳",
            callback=lambda: self.set_mode("sandbox"),
            highlight_color=GOLD["midtone"],
            highlight_text_color=GRAU["lowtone"],
            text_color=GRAU["lowtone"],
            font_size=18,
            bold=True,
            angle_offset=30,
            alpha=220,
        )
        self.button_0.y_c = -120

        # Button 1: Museum – Schloss-Symbol, Gold (von Button 0 hierher verschoben)
        self.button_1 = HexButton(
            x=x_l, y=316, size=48,
            color=GOLD["hightone"],
            text="🔒",
            callback=lambda: self.set_mode("museum"),
            highlight_color=GOLD["midtone"],
            highlight_text_color=GRAU["lowtone"],
            text_color=GRAU["lowtone"],
            font_size=18,
            bold=True,
            angle_offset=30,
            alpha=220,
        )
        self.button_1.y_c = -60

        # Button 2: Raum 2 – Silber
        self.button_2 = HexButton(
            x=x_l, y=376, size=48,
            color=SILBER["hightone"],
            text="?",
            callback=lambda: self.set_mode("raum2"),
            highlight_color=SILBER["midtone"],
            highlight_text_color=GRAU["lowtone"],
            text_color=GRAU["lowtone"],
            font_size=24,
            bold=True,
            angle_offset=30,
            alpha=220,
        )
        self.button_2.y_c = 0
        # Button 3: Galerie – Landschafts-Symbol, Bronze
        self.button_3 = HexButton(
            x=x_l, y=436, size=48,
            color=BRONZE["hightone"],
            text="⛰",
            callback=lambda: self.set_mode("gallery"),
            highlight_color=BRONZE["midtone"],
            highlight_text_color=GRAU["lowtone"],
            text_color=GRAU["lowtone"],
            font_size=20,
            bold=True,
            angle_offset=30,
            alpha=220,
        )
        self.button_3.y_c = 60

        # Button 4: Jukebox – Noten-Symbol, Gold
        self.button_4 = HexButton(
            x=x_l, y=496, size=48,
            color=GOLD["hightone"],
            text="♪",
            callback=lambda: self.set_mode("jukebox"),
            highlight_color=GOLD["midtone"],
            highlight_text_color=GRAU["lowtone"],
            text_color=GRAU["lowtone"],
            font_size=22,
            bold=True,
            angle_offset=30,
            alpha=220,
        )
        self.button_4.y_c = 120

        # Speichere alle linken Buttons als Liste für einfache Iteration
        self._left_buttons = [
            self.button_0, self.button_1, self.button_2,
            self.button_3, self.button_4,
        ]

        # --- RECHTS: Buttons 5–9 (oben → unten) ---
        # Aliase behalten Assault-kompatible Namen für _update_mode_buttons

        # Button 5: Settings-Toggle ⚙  (Gold)
        self.settings_button = HexButton(
            x=x_r, y=256, size=48,
            color=GOLD["hightone"],
            text="⚙",
            callback=lambda: self.settings_menu.toggle(),
            highlight_color=GOLD["midtone"],
            highlight_text_color=GRAU["lowtone"],
            text_color=GRAU["lowtone"],
            font_size=22,
            bold=True,
            angle_offset=30,
            alpha=220,
        )
        self.settings_button.y_c = -120
        self.settings_button.x_r = x_r

        # Button 6: Labor – Reagenzglas-Symbol, Silber
        self.lobby_button = HexButton(
            x=x_r, y=316, size=48,
            color=SILBER["hightone"],
            text="⚗",
            callback=lambda: self.set_mode("labor"),
            highlight_color=SILBER["midtone"],
            highlight_text_color=GRAU["lowtone"],
            text_color=GRAU["lowtone"],
            font_size=20,
            bold=True,
            angle_offset=30,
            alpha=220,
        )
        self.lobby_button.y_c = -60

        # Button 7: Sprengstoff – Bomben-Symbol, Bronze
        self.match_status_button = HexButton(
            x=x_r, y=376, size=48,
            color=BRONZE["hightone"],
            text="💣",
            callback=lambda: self.set_mode("sprengstoff"),
            highlight_color=BRONZE["midtone"],
            highlight_text_color=GRAU["lowtone"],
            text_color=GRAU["lowtone"],
            font_size=18,
            bold=True,
            angle_offset=30,
            alpha=220,
        )
        self.match_status_button.y_c = 0
        # Button 8: Raum 8 – Bronze
        self.simulator_button = HexButton(
            x=x_r, y=436, size=48,
            color=BRONZE["hightone"],
            text="?",
            callback=lambda: self.set_mode("raum8"),
            highlight_color=BRONZE["midtone"],
            highlight_text_color=GRAU["lowtone"],
            text_color=GRAU["lowtone"],
            font_size=24,
            bold=True,
            angle_offset=30,
            alpha=220,
        )
        self.simulator_button.y_c = 60
        # Button 9 (unten rechts): Vorhof – Kompass-Symbol, Gold
        self.debugger_button = HexButton(
            x=x_r, y=496, size=48,
            color=GOLD["hightone"],
            text="🧭",
            callback=lambda: self.set_mode("vorhof"),
            highlight_color=GOLD["midtone"],
            highlight_text_color=GRAU["lowtone"],
            text_color=GRAU["lowtone"],
            font_size=18,
            bold=True,
            angle_offset=30,
            alpha=220,
        )
        self.debugger_button.y_c = 120

        # Rechter-Rand-Merkmal für _reposition_ui
        for btn in (self.settings_button, self.lobby_button, self.match_status_button,
                    self.simulator_button, self.debugger_button):
            btn.x_r = x_r

        self.button_0.is_selected = True   # Lobby ist Start-Modus

    def _init_modi(self):
        from modes.sandbox   import Sandbox
        from modes.museum    import Museum
        from modes.lab       import Lab
        from modes.prototype import Prototype
        from modes.jukebox   import Jukebox
        from modes.gallery   import Gallery
        from modes.vorhof      import Vorhof
        from modes.labor       import Labor as LaborNeu
        from modes.sprengstoff import Sprengstoff
        from modes.raum_1      import Raum1
        from modes.raum_2      import Raum2
        from modes.raum_8      import Raum8

        self.sandbox = Sandbox(
            screen=self.screen,
            screen_width=self.SCREEN_WIDTH,
            screen_height=self.SCREEN_HEIGHT,
        )
        self.sandbox.set_app_callbacks(self.set_mode)

        self.museum = Museum(
            screen=self.screen,
            screen_width=self.SCREEN_WIDTH,
            screen_height=self.SCREEN_HEIGHT,
        )
        self.museum.set_app_callbacks(self.set_mode)

        self.lab = Lab(
            screen=self.screen,
            screen_width=self.SCREEN_WIDTH,
            screen_height=self.SCREEN_HEIGHT,
        )

        self.proto = Prototype(
            screen=self.screen,
            screen_width=self.SCREEN_WIDTH,
            screen_height=self.SCREEN_HEIGHT,
        )

        self.jukebox = Jukebox(
            screen=self.screen,
            screen_width=self.SCREEN_WIDTH,
            screen_height=self.SCREEN_HEIGHT,
        )
        self.jukebox.set_app_callbacks(self.set_mode)

        self.gallery = Gallery(
            screen=self.screen,
            screen_width=self.SCREEN_WIDTH,
            screen_height=self.SCREEN_HEIGHT,
        )
        self.gallery.set_app_callbacks(self.set_mode)

        self.vorhof = Vorhof(
            screen=self.screen,
            screen_width=self.SCREEN_WIDTH,
            screen_height=self.SCREEN_HEIGHT,
        )
        self.vorhof.set_app_callbacks(self.set_mode)

        self.labor_neu = LaborNeu(
            screen=self.screen,
            screen_width=self.SCREEN_WIDTH,
            screen_height=self.SCREEN_HEIGHT,
        )
        self.labor_neu.set_app_callbacks(self.set_mode)

        self.sprengstoff = Sprengstoff(
            screen=self.screen,
            screen_width=self.SCREEN_WIDTH,
            screen_height=self.SCREEN_HEIGHT,
        )
        self.sprengstoff.set_app_callbacks(self.set_mode)

        self.raum1 = Raum1(screen=self.screen, screen_width=self.SCREEN_WIDTH, screen_height=self.SCREEN_HEIGHT)
        self.raum1.set_app_callbacks(self.set_mode)
        self.raum2 = Raum2(screen=self.screen, screen_width=self.SCREEN_WIDTH, screen_height=self.SCREEN_HEIGHT)
        self.raum2.set_app_callbacks(self.set_mode)
        self.raum8 = Raum8(screen=self.screen, screen_width=self.SCREEN_WIDTH, screen_height=self.SCREEN_HEIGHT)
        self.raum8.set_app_callbacks(self.set_mode)

        self.museum.init()
        self.lab.init()
        self.proto.init()
        self.jukebox.init()
        self.gallery.init()
        self.vorhof.init()
        self.labor_neu.init()
        self.sprengstoff.init()
        self.raum1.init()
        self.raum2.init()
        self.raum8.init()

    # ------------------------------------------------------------------
    # Modus-Verwaltung
    # ------------------------------------------------------------------

    def _update_mode_buttons(self):
        if hasattr(self, 'button_0'):
            self.button_0.is_selected = (self.mode == "sandbox")
        if hasattr(self, 'button_1'):
            self.button_1.is_selected = (self.mode == "museum")
        if hasattr(self, 'button_2'):
            self.button_2.is_selected = (self.mode == "raum2")
        if hasattr(self, 'button_3'):
            self.button_3.is_selected = (self.mode == "gallery")
        if hasattr(self, 'button_4'):
            self.button_4.is_selected = (self.mode == "jukebox")
        if hasattr(self, 'lobby_button'):
            self.lobby_button.is_selected = (self.mode == "labor")
        if hasattr(self, 'simulator_button'):
            self.simulator_button.is_selected = (self.mode == "raum8")
        if hasattr(self, 'debugger_button'):
            self.debugger_button.is_selected = (self.mode == "vorhof")
        if hasattr(self, 'match_status_button'):
            self.match_status_button.is_selected = (self.mode == "sprengstoff")
        if hasattr(self, 'settings_button') and hasattr(self, 'settings_menu'):
            self.settings_button.is_selected = self.settings_menu.is_active

    def set_mode(self, new_mode: str):
        valid_modes = ["sandbox", "museum", "lab", "proto", "jukebox", "gallery", "vorhof", "labor", "sprengstoff", "raum1", "raum2", "raum8"]
        if new_mode not in valid_modes or new_mode == self.mode:
            return

        old_mode  = self.mode
        self.mode = new_mode
        self._update_mode_buttons()
        if hasattr(self, 'header'):
            self.header.set_mode(new_mode)

        if new_mode == "museum" and hasattr(self, "museum"):
            self.museum.on_enter()
        if new_mode == "jukebox" and hasattr(self, "jukebox"):
            self.jukebox.on_enter()
        if new_mode == "gallery" and hasattr(self, "gallery"):
            self.gallery.on_enter()
        if new_mode == "vorhof" and hasattr(self, "vorhof"):
            self.vorhof.on_enter()
        if new_mode == "labor" and hasattr(self, "labor_neu"):
            self.labor_neu.on_enter()
        if new_mode == "sprengstoff" and hasattr(self, "sprengstoff"):
            self.sprengstoff.on_enter()
        if new_mode == "raum1" and hasattr(self, "raum1"):
            self.raum1.on_enter()
        if new_mode == "raum2" and hasattr(self, "raum2"):
            self.raum2.on_enter()
        if new_mode == "raum8" and hasattr(self, "raum8"):
            self.raum8.on_enter()

        if new_mode in ("museum", "lab", "proto") and old_mode == "sandbox":
            self.audio_manager.play_neutral()
        elif new_mode == "sandbox" and old_mode != "sandbox":
            self.audio_manager.play_welcome()

    # ------------------------------------------------------------------
    # Hauptschleife
    # ------------------------------------------------------------------

    def update(self, dt: float) -> None:
        # Startup-Fade
        if self._fade_alpha > 0:
            self._fade_elapsed += dt
            progress = min(1.0, self._fade_elapsed / self._fade_duration)
            self._fade_alpha = int(255 * (1.0 - progress))

        self.audio_manager.update(dt)

        try:
            if self.mode == "sandbox":
                self.sandbox.update(dt)
            elif self.mode == "museum":
                self.museum.update(dt)
            elif self.mode == "lab":
                self.lab.update(dt)
            elif self.mode == "proto":
                self.proto.update(dt)
            elif self.mode == "jukebox":
                self.jukebox.update(dt)
            elif self.mode == "gallery":
                self.gallery.update(dt)
            elif self.mode == "vorhof":
                self.vorhof.update(dt)
            elif self.mode == "labor":
                self.labor_neu.update(dt)
            elif self.mode == "sprengstoff":
                self.sprengstoff.update(dt)
            elif self.mode == "raum1":
                self.raum1.update(dt)
            elif self.mode == "raum2":
                self.raum2.update(dt)
            elif self.mode == "raum8":
                self.raum8.update(dt)
            self._mode_errors.pop(self.mode, None)
        except Exception as e:
            self._mode_errors[self.mode] = e

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            elif event.type == VIDEORESIZE:
                self.SCREEN_WIDTH, self.SCREEN_HEIGHT = event.size
                self.screen = pygame.display.set_mode(
                    (self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
                    pygame.RESIZABLE
                )
                self.screen_manager.set_screen_size(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                self._reposition_ui()
                continue

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_g:
                    self.set_mode("sandbox"); continue
                elif event.key == K_s:
                    self.set_mode("museum");  continue
                elif event.key == K_d:
                    self.set_mode("lab");     continue
                elif event.key == K_p:
                    self.set_mode("proto");   continue

            # Settings-Menü hat Vorrang
            if self.settings_menu.handle_event(event):
                continue

            # Rechte Buttons (5-9): Modus-Wechsel (6,8,9,7) + Settings-Toggle (5)
            _mode_btn_clicked = False
            for btn_name in ('lobby_button', 'simulator_button', 'debugger_button', 'match_status_button'):
                btn = getattr(self, btn_name, None)
                if btn and btn.handle_event(event):
                    _mode_btn_clicked = True
            # Settings-Button togglet Menü (kein Modus-Wechsel)
            if hasattr(self, 'settings_button'):
                if self.settings_button.handle_event(event):
                    self._update_mode_buttons()   # selected-state sofort aktualisieren
            # Linke Buttons (0-4): Button 0 hat Callback → setzt _mode_btn_clicked
            for btn in getattr(self, '_left_buttons', []):
                if btn.handle_event(event) and btn.callback:
                    _mode_btn_clicked = True
            if _mode_btn_clicked:
                continue

            # Event an aktiven Modus weiterleiten (isoliert)
            try:
                if self.mode == "sandbox":
                    self.sandbox.handle_event(event)
                elif self.mode == "museum":
                    self.museum.handle_event(event)
                elif self.mode == "lab":
                    self.lab.handle_event(event)
                elif self.mode == "proto":
                    self.proto.handle_event(event)
                elif self.mode == "jukebox":
                    self.jukebox.handle_event(event)
                elif self.mode == "gallery":
                    self.gallery.handle_event(event)
                elif self.mode == "vorhof":
                    self.vorhof.handle_event(event)
                elif self.mode == "labor":
                    self.labor_neu.handle_event(event)
                elif self.mode == "sprengstoff":
                    self.sprengstoff.handle_event(event)
                elif self.mode == "raum1":
                    self.raum1.handle_event(event)
                elif self.mode == "raum2":
                    self.raum2.handle_event(event)
                elif self.mode == "raum8":
                    self.raum8.handle_event(event)
            except Exception as e:
                self._mode_errors[self.mode] = e

        return True

    def _reposition_ui(self):
        """Positioniert alle 10 Buttons nach Fenstergrößenänderung neu."""
        self.MARGIN_RIGHT = 25
        # Rechte Buttons (5-9): x folgt dem rechten Rand
        _right_buttons = (
            'match_status_button', 'settings_button',
            'lobby_button', 'simulator_button', 'debugger_button',
        )
        for btn_name in _right_buttons:
            btn = getattr(self, btn_name, None)
            if btn is None:
                continue
            btn.x        = self.SCREEN_WIDTH - self.MARGIN_RIGHT - btn.size
            btn.y        = self.SCREEN_HEIGHT // 2 + btn.y_c - btn.size // 2
            btn.center_x = btn.x + btn.size / 2
            btn.center_y = btn.y + btn.size / 2
            btn.points   = btn._calculate_hex_points()
        # Linke Buttons (0-4): x = MARGIN_LEFT (konstant), y folgt der Bildmitte
        for btn in getattr(self, '_left_buttons', []):
            btn.x        = self.MARGIN_LEFT
            btn.y        = self.SCREEN_HEIGHT // 2 + btn.y_c - btn.size // 2
            btn.center_x = btn.x + btn.size / 2
            btn.center_y = btn.y + btn.size / 2
            btn.points   = btn._calculate_hex_points()
        self.settings_menu.x = self.SCREEN_WIDTH - 25 - 300
        if hasattr(self, 'header'):
            self.header.resize(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        if hasattr(self, 'console'):
            _cx = self.MARGIN_LEFT + 48 + 10
            _cw = self.SCREEN_WIDTH - _cx - 48 - 10 - self.MARGIN_RIGHT
            _ch = 160
            _cy = self.SCREEN_HEIGHT - _ch - 10
            self.console.resize(_cx, _cy, _cw, _ch)

    def render(self):
        # Hintergrund
        self.screen_manager.render_background()

        # Modus-Inhalt (isoliert — Fehler im Modus crashen nicht die App)
        try:
            if self.mode == "sandbox":
                self.sandbox.render_content()
            elif self.mode == "museum":
                self.museum.render_content()
            elif self.mode == "lab":
                self.lab.render_content()
            elif self.mode == "proto":
                self.proto.render_content()
            elif self.mode == "jukebox":
                self.jukebox.render_content()
            elif self.mode == "gallery":
                self.gallery.render_content()
            elif self.mode == "vorhof":
                self.vorhof.render_content()
            elif self.mode == "labor":
                self.labor_neu.render_content()
            elif self.mode == "sprengstoff":
                self.sprengstoff.render_content()
            elif self.mode == "raum1":
                self.raum1.render_content()
            elif self.mode == "raum2":
                self.raum2.render_content()
            elif self.mode == "raum8":
                self.raum8.render_content()
            self._mode_errors.pop(self.mode, None)
        except Exception as e:
            self._mode_errors[self.mode] = e
            self._render_mode_error(self.mode, e)

        # Settings-Menü (Overlay)
        self.settings_menu.render(self.screen)

        # Diamant-Ketten (linker + rechter Rand, je 5 Diamanten)
        self._render_diamond_chains()

        # Erhaben-Effekte + alle 10 Buttons
        from interfaces.renderer.pygame.components.button import draw_raised_effects
        _app_buttons = [
            b for b in [
                getattr(self, 'lobby_button',          None),
                getattr(self, 'simulator_button',     None),
                getattr(self, 'debugger_button',      None),
                getattr(self, 'settings_button',      None),
                getattr(self, 'match_status_button',  None),
                *getattr(self, '_left_buttons', []),
            ] if b is not None
        ]
        draw_raised_effects(self.screen, _app_buttons)
        for btn in _app_buttons:
            btn.render(self.screen)

        # Header (obere 12%)
        if hasattr(self, 'header'):
            self.header.render(self.screen)

        # Console (unterer Bereich)
        if hasattr(self, 'console'):
            self.console.render(self.screen)

        # Startup-Fade
        if self._fade_alpha > 0:
            _fade_surf = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            _fade_surf.fill((0, 0, 0))
            _fade_surf.set_alpha(self._fade_alpha)
            self.screen.blit(_fade_surf, (0, 0))

        pygame.display.flip()

    def _render_diamond_chains(self):
        """
        Zwei vertikale Dekor-Ketten durch die Button-Spalten.

        Aufbau (von oben nach unten):
          Band ─────────────────── geht von y=0 bis y=H (unendlich)
          ◆ ◆ ◆ ◆ ◆               5 kleine Diamanten Richtung Header
          [Hex-Button]  [Hex-Button]  [...]   ← 5 dicke "Diamanten" (die Buttons selbst)
          ◆ ◆ ◆ ◆ ◆               5 kleine Diamanten Richtung Console
          Band ─────────────────── (wird von Header + Console überdeckt)
        """
        font_d        = pygame.font.SysFont("Segoe UI Symbol", 12)
        color_diamond = (165, 118, 45)   # warmes Bernstein-Gold
        color_dark    = ( 80,  55, 18)   # dunkler Bandrand

        btn_size = 48
        # Band läuft durch Button-Mittelpunkte (Buttons zeichnen sich danach obendrüber)
        x_left  = self.MARGIN_LEFT + btn_size // 2
        x_right = self.SCREEN_WIDTH - self.MARGIN_RIGHT - btn_size // 2

        mid         = self.SCREEN_HEIGHT // 2
        btn_spacing = 60
        centers_y   = [mid + y_c for y_c in (-120, -60, 0, 60, 120)]
        top_anchor  = centers_y[0]    # oberster Button-Mittelpunkt
        bot_anchor  = centers_y[-1]   # unterster Button-Mittelpunkt

        # 5 kleine Diamanten oberhalb + unterhalb der Button-Gruppe
        upper = [top_anchor - (i + 1) * btn_spacing for i in range(5)]
        lower = [bot_anchor + (i + 1) * btn_spacing for i in range(5)]

        d_surf = font_d.render("◆", True, color_diamond)
        half_h = d_surf.get_height() // 2

        for cx in (x_left, x_right):
            # ── 1. Dekorband — von oben nach unten (wird von Header + Console überdeckt) ──
            pygame.draw.line(self.screen, color_dark,    (cx - 1, 0), (cx - 1, self.SCREEN_HEIGHT), 1)
            pygame.draw.line(self.screen, color_diamond, (cx,     0), (cx,     self.SCREEN_HEIGHT), 1)
            pygame.draw.line(self.screen, color_dark,    (cx + 1, 0), (cx + 1, self.SCREEN_HEIGHT), 1)

            # ── 2. Verbindungslinien zwischen kleinen Diamanten (auf dem Band) ──
            small_all = list(reversed(upper)) + lower   # alle 10, sortiert nach y
            for seq in (list(reversed(upper)), lower):  # erst oben, dann unten separat
                for i in range(len(seq) - 1):
                    y_a = seq[i]     + half_h + 2
                    y_b = seq[i + 1] - half_h - 2
                    if y_b > y_a:
                        pygame.draw.line(self.screen, color_diamond, (cx, y_a), (cx, y_b), 1)

            # ── 3. Kleine Diamanten oben + unten ──
            for cy in upper + lower:
                rect = d_surf.get_rect(center=(cx, cy))
                self.screen.blit(d_surf, rect)

    def _render_mode_error(self, mode: str, error: Exception):
        """Zeigt Fehler-Overlay für einen Modus an – App und andere Modi laufen weiter."""
        from core.utils.global_constants import FONT_FAMILY
        font_big   = pygame.font.SysFont(FONT_FAMILY, 22, bold=True)
        font_small = pygame.font.SysFont(FONT_FAMILY, 14)

        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 10, 10, 200))
        self.screen.blit(overlay, (0, 0))

        title = font_big.render(f"FEHLER IN {mode.upper()}", True, (255, 100, 80))
        self.screen.blit(title, (30, 90))

        msg = font_small.render(str(error)[:140], True, (230, 200, 200))
        self.screen.blit(msg, (30, 125))

        hint = font_small.render(
            "Fehler beheben und Modus wechseln  (G / S / D / P)  –  andere Modi bleiben aktiv.",
            True, (180, 160, 140)
        )
        self.screen.blit(hint, (30, 148))

    def run(self):
        clock = pygame.time.Clock()
        running = True

        self.sandbox.on_enter()
        self.audio_manager.play_welcome()

        try:
            while running:
                dt      = clock.get_rawtime() / 1000.0
                running = self.handle_events()
                self.update(dt)
                self.render()
                clock.tick(60)
        finally:
            pygame.quit()


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
