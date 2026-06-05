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

        # Settings-Menü (Overlay)
        self.settings_menu = SettingsMenu(
            x=self.SCREEN_WIDTH - 25 - 300,
            y=53,
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

        # --- LINKS: Buttons 0–4 (oben → unten, center_y: 280, 340, 400, 460, 520) ---
        self.button_0 = _make_btn(x_l, 256, "0", -120)   # frei
        self.button_1 = _make_btn(x_l, 316, "1",  -60)   # frei
        self.button_2 = _make_btn(x_l, 376, "2",    0)   # frei
        self.button_3 = _make_btn(x_l, 436, "3",   60)   # frei
        self.button_4 = _make_btn(x_l, 496, "4",  120)   # frei

        # Speichere alle linken Buttons als Liste für einfache Iteration
        self._left_buttons = [
            self.button_0, self.button_1, self.button_2,
            self.button_3, self.button_4,
        ]

        # --- RECHTS: Buttons 5–9 (oben → unten) ---
        # Aliase behalten Assault-kompatible Namen für _update_mode_buttons

        # Button 5 (ehem. ⚙): Prototyp – center_y=280
        self.settings_button = _make_btn(x_r, 256, "5", -120,
                                         callback=lambda: self.set_mode("proto"))
        # Button 6 (ehem. G): Sandbox – center_y=340
        self.game_button = _make_btn(x_r, 316, "6", -60,
                                     callback=lambda: self.set_mode("sandbox"))
        # Button 7 (ehem. ⏳): Settings-Toggle – center_y=400
        self.match_status_button = _make_btn(x_r, 376, "7", 0,
                                             callback=lambda: self.settings_menu.toggle())
        # Button 8 (ehem. S): Museum – center_y=460
        self.simulator_button = _make_btn(x_r, 436, "8", 60,
                                          callback=lambda: self.set_mode("museum"))
        # Button 9 (ehem. D): Labor – center_y=520
        self.debugger_button = _make_btn(x_r, 496, "9", 120,
                                         callback=lambda: self.set_mode("lab"))

        # Rechter-Rand-Merkmal für _reposition_ui
        for btn in (self.settings_button, self.game_button, self.match_status_button,
                    self.simulator_button, self.debugger_button):
            btn.x_r = x_r

        self.game_button.is_selected = True   # Sandbox ist Start-Modus

    def _init_modi(self):
        from modes.sandbox   import Sandbox
        from modes.museum    import Museum
        from modes.lab       import Lab
        from modes.prototype import Prototype

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

        self.museum.init()
        self.lab.init()
        self.proto.init()

    # ------------------------------------------------------------------
    # Modus-Verwaltung
    # ------------------------------------------------------------------

    def _update_mode_buttons(self):
        if hasattr(self, 'game_button'):
            self.game_button.is_selected = (self.mode == "sandbox")
        if hasattr(self, 'simulator_button'):
            self.simulator_button.is_selected = (self.mode == "museum")
        if hasattr(self, 'debugger_button'):
            self.debugger_button.is_selected = (self.mode == "lab")
        if hasattr(self, 'settings_button'):
            self.settings_button.is_selected = (self.mode == "proto")

    def set_mode(self, new_mode: str):
        valid_modes = ["sandbox", "museum", "lab", "proto"]
        if new_mode not in valid_modes or new_mode == self.mode:
            return

        old_mode  = self.mode
        self.mode = new_mode
        self._update_mode_buttons()

        if new_mode == "museum" and hasattr(self, "museum"):
            self.museum.on_enter()

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

            # Rechte Buttons (5-9): Modus-Wechsel und Settings-Toggle
            _mode_btn_clicked = False
            for btn_name in ('game_button', 'simulator_button', 'debugger_button', 'settings_button'):
                btn = getattr(self, btn_name, None)
                if btn and btn.handle_event(event):
                    _mode_btn_clicked = True
            if hasattr(self, 'match_status_button'):
                self.match_status_button.handle_event(event)
            # Linke Buttons (0-4): noch ohne Callback, reagieren auf Hover
            for btn in getattr(self, '_left_buttons', []):
                btn.handle_event(event)
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
            except Exception as e:
                self._mode_errors[self.mode] = e

        return True

    def _reposition_ui(self):
        """Positioniert alle 10 Buttons nach Fenstergrößenänderung neu."""
        self.MARGIN_RIGHT = 25
        # Rechte Buttons (5-9): x folgt dem rechten Rand
        _right_buttons = (
            'match_status_button', 'settings_button',
            'game_button', 'simulator_button', 'debugger_button',
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
                getattr(self, 'game_button',          None),
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

        # Modus-Indikator (oben links)
        self._render_mode_indicator()

        # Startup-Fade
        if self._fade_alpha > 0:
            _fade_surf = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            _fade_surf.fill((0, 0, 0))
            _fade_surf.set_alpha(self._fade_alpha)
            self.screen.blit(_fade_surf, (0, 0))

        pygame.display.flip()

    def _render_diamond_chains(self):
        """
        Zeichnet zwei vertikale Diamant-Ketten (je 5 Diamanten) am linken und
        rechten Bildrand – flankierend zu den 10 Hex-Buttons.
        Verbindungslinien zwischen den Diamanten erzeugen den Perlenketten-Effekt.
        """
        font_d        = pygame.font.SysFont("Segoe UI Symbol", 12)
        color_diamond = (165, 118, 45)   # warmes Bernstein-Gold
        color_line    = (100,  72, 25)   # gedämpftes Braun

        # x-Mitte des jeweiligen Randstreifens (MARGIN = 25 px)
        x_left  = self.MARGIN_LEFT  // 2          # ≈ 12 px
        x_right = self.SCREEN_WIDTH - self.MARGIN_RIGHT // 2  # ≈ 1268 px

        # y-Mittelpunkte der 5 Buttons (center_y = Bildmitte + y_c)
        mid = self.SCREEN_HEIGHT // 2
        centers_y = [mid + y_c for y_c in (-120, -60, 0, 60, 120)]

        d_surf = font_d.render("◆", True, color_diamond)
        half_h = d_surf.get_height() // 2

        for cx in (x_left, x_right):
            # Verbindungslinien zwischen je zwei aufeinanderfolgenden Diamanten
            for i in range(len(centers_y) - 1):
                y_top = centers_y[i]     + half_h + 3
                y_bot = centers_y[i + 1] - half_h - 3
                if y_bot > y_top:
                    pygame.draw.line(self.screen, color_line, (cx, y_top), (cx, y_bot), 1)
            # Diamanten selbst
            for cy in centers_y:
                rect = d_surf.get_rect(center=(cx, cy))
                self.screen.blit(d_surf, rect)

    def _render_mode_indicator(self):
        from core.utils.global_constants import FONT_FAMILY
        font = pygame.font.SysFont(FONT_FAMILY, 20)
        mode_names = {
            "sandbox": "SANDBOX",
            "museum":  "MUSEUM",
            "lab":     "LABOR",
            "proto":   "PROTOTYP",
        }
        text_surface = font.render(mode_names.get(self.mode, self.mode.upper()), True, COLORS["text"])
        self.screen.blit(text_surface, (10, 10))

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
