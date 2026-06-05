"""
Labor-Modus – Werkstatt für aktive Entwicklung und Experimente.

Farbkonzept: GRAU Hintergrund · SILBER/Petrol dominant · GOLD Highlight (sparsam)
"""

import pygame
from core.utils.global_constants import FONT_FAMILY, GRAU, SILBER, GOLD


class Labor:
    """Leerer Labor-Raum – Platzhalter für die Werkstatt."""

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

        _ov = pygame.Surface((w, h), pygame.SRCALPHA)
        _ov.fill((*SILBER["overtone"], 40))
        self.screen.blit(_ov, (0, 0))

        label = self._font_title.render("⚗  LABOR", True, SILBER["halftone"])
        sub   = self._font_sub.render(
            "Werkstatt  ·  Experimente  ·  Aktive Entwicklung  ·  Coming soon",
            True, GRAU["halftone"]
        )
        cx = w // 2
        cy = h // 2
        self.screen.blit(label, label.get_rect(centerx=cx, centery=cy - 20))
        self.screen.blit(sub,   sub.get_rect(centerx=cx,   centery=cy + 18))

    def init(self):
        pass

    def on_enter(self):
        pass
