"""
Galerie-Modus – Bildbetrachter und Bildverwaltung.

Geplante Features:
  - Ordner-basiertes Einlesen von Bildern (PNG, JPG, …)
  - Vollbild-Viewer mit Navigation (Prev / Next)
  - Alben / Sammlungen erstellen und benennen
  - Slideshow-Modus

Farbkonzept: GRAU dominant · BRONZE Akzent · GOLD Highlight
"""

import pygame
from core.utils.global_constants import FONT_FAMILY, GRAU, BRONZE, GOLD


_BG_TINT = (*BRONZE["overtone"], 35)   # sehr dezenter Bronze-Hauch über GRAU


class Gallery:
    """Leerer Galerie-Raum – Platzhalter für den integrierten Bildbetrachter."""

    def __init__(self, screen, screen_width: int, screen_height: int, **kwargs):
        self.screen        = screen
        self.screen_width  = screen_width
        self.screen_height = screen_height
        self._set_mode_fn  = None

        self._font_title = pygame.font.SysFont(FONT_FAMILY, 28, bold=True)
        self._font_sub   = pygame.font.SysFont(FONT_FAMILY, 14)

    def set_app_callbacks(self, set_mode_fn):
        self._set_mode_fn = set_mode_fn

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, dt: float):
        pass

    def render_content(self):
        w, h = self.screen_width, self.screen_height

        # Dezenter Bronze-Tint als Raumton
        _ov = pygame.Surface((w, h), pygame.SRCALPHA)
        _ov.fill(_BG_TINT)
        self.screen.blit(_ov, (0, 0))

        # Platzhalter-Text
        label = self._font_title.render("⛰  GALERIE", True, BRONZE["halftone"])
        sub   = self._font_sub.render("Bildbetrachter  ·  Alben  ·  Slideshow  ·  Coming soon", True, GRAU["halftone"])
        cx    = w // 2
        cy    = h // 2
        self.screen.blit(label, label.get_rect(centerx=cx, centery=cy - 20))
        self.screen.blit(sub,   sub.get_rect(centerx=cx,   centery=cy + 18))

    def init(self):
        pass

    def on_enter(self):
        pass
