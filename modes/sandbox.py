"""
Sandbox-Modus – Hauptlobby / Hotel-Vorhof.
"""

import pygame
from core.utils.global_constants import (
    COLORS, FONT_FAMILY, TEXT_LIGHT, TEXT_HIGHLIGHT, TEXT_DARK,
    PERGAMENT, LEDER, FACTION_ADAM, FACTION_SKELETOR, FACTION_ZODAK,
    SCREEN_WIDTH, SCREEN_HEIGHT,
)
from interfaces.renderer.pygame.components.button import HexButton, draw_raised_effects


class Sandbox:
    """Hauptlobby des CodeSandbox-Hubs."""

    def __init__(self, screen, screen_width: int, screen_height: int, **kwargs):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self._font_title  = pygame.font.SysFont(FONT_FAMILY, 52, bold=True)
        self._font_sub    = pygame.font.SysFont(FONT_FAMILY, 18)
        self._font_label  = pygame.font.SysFont(FONT_FAMILY, 15)
        self._font_footer = pygame.font.SysFont(FONT_FAMILY, 12)

        # Drei große Navigations-Hexagone (steuern den App-Modus)
        # Callbacks werden nach dem App-Init gesetzt (via on_enter)
        self._nav_callbacks = {}
        self._build_nav_buttons()

    def _build_nav_buttons(self):
        size = 130
        nav_y = 270
        entries = [
            (240,  FACTION_ADAM["primary"],     "Adam",     "Museum",   "museum",    "Ausstellungsraum"),
            (640,  FACTION_SKELETOR["primary"], "Skeletor", "Labor",    "lab",       "Werkstatt"),
            (1040, FACTION_ZODAK["primary"],    "Zodak",    "Prototyp", "proto",     "Testgelände"),
        ]
        self._nav_buttons = []
        self._nav_labels  = []
        self._nav_modes   = []
        for cx, color, faction, text, mode, label in entries:
            btn = HexButton(
                x=cx - size // 2,
                y=nav_y,
                size=size,
                color=color,
                text=text,
                faction=faction,
                callback=lambda m=mode: self._on_nav(m),
                text_color=TEXT_LIGHT,
                font_size=20,
            )
            self._nav_buttons.append(btn)
            self._nav_labels.append((cx, nav_y + size + 14, label))
            self._nav_modes.append(mode)

    def _on_nav(self, mode: str):
        if self._nav_callbacks.get("set_mode"):
            self._nav_callbacks["set_mode"](mode)

    def set_app_callbacks(self, set_mode_fn):
        """Wird vom App nach der Initialisierung aufgerufen."""
        self._nav_callbacks["set_mode"] = set_mode_fn

    def handle_event(self, event: pygame.event.Event):
        for btn in self._nav_buttons:
            btn.handle_event(event)

    def update(self, dt: float):
        pass

    def render_content(self):
        w = self.screen_width

        # Header-Balken
        pygame.draw.rect(self.screen, (22, 16, 10), (0, 0, w, 78))
        pygame.draw.line(self.screen, (80, 58, 36), (0, 78), (w, 78), 1)

        # Titel
        title = self._font_title.render("CODESANDBOX", True, TEXT_HIGHLIGHT)
        title_rect = title.get_rect(centerx=w // 2, y=14)
        self.screen.blit(title, title_rect)

        # Trennlinie
        pygame.draw.line(self.screen, (60, 45, 28), (80, 110), (w - 80, 110), 1)

        # Navigations-Hexagone
        draw_raised_effects(self.screen, self._nav_buttons)
        for btn in self._nav_buttons:
            btn.render(self.screen)

        # Labels unter den Buttons
        for cx, ly, label in self._nav_labels:
            lbl = self._font_label.render(label, True, TEXT_LIGHT)
            lbl_rect = lbl.get_rect(centerx=cx, y=ly)
            self.screen.blit(lbl, lbl_rect)

        # Footer
        footer = self._font_footer.render("CodeSandbox  v0.1  —  Alpha", True, (70, 55, 36))
        footer_rect = footer.get_rect(centerx=w // 2, bottom=self.screen_height - 10)
        self.screen.blit(footer, footer_rect)

    def on_enter(self):
        pass
