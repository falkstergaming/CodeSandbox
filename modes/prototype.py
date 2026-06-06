"""
Prototyp-Modus – Testgelände für neue Ideen (P-Taste).
Wird gerade aufgebaut.

Farbkonzept: GRAU Hintergrund · GRAU/Neutral Akzent
"""

import pygame
from core.utils.global_constants import GRAU
from interfaces.renderer.pygame.components.room_panel import draw_room_panel

_ACCENT = GRAU["halftone"]


class Prototype:
    """Prototyp-Raum – Testgelände (P-Taste)."""

    def __init__(self, screen, screen_width: int, screen_height: int, **kwargs):
        self.screen        = screen
        self.screen_width  = screen_width
        self.screen_height = screen_height

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, dt: float):
        pass

    def render_content(self):
        draw_room_panel(
            self.screen, self.screen_width, self.screen_height,
            title="PROTOTYP",
            subtitle="Testgelände  ·  Keine Stabilitätspflicht  ·  P-Taste",
            accent_color=_ACCENT,
        )

    def init(self):
        pass

    def on_enter(self):
        pass
