"""
Sprengstoff-Modus – Hochriskante Experimente ohne Stabilitätspflicht.

Der wilde Bruder des Labors. Hier explodiert alles, was noch nicht fertig ist.
Kein Test, kein Netz, keine Garantien.

Farbkonzept: GRAU Hintergrund · BRONZE dominant · kein Gold
"""

import pygame
from core.utils.global_constants import BRONZE
from interfaces.renderer.pygame.components.room_panel import draw_room_panel

_ACCENT = BRONZE["midtone"]


class Sprengstoff:
    """Sprengstoff-Raum – Hochriskante Experimente."""

    def __init__(self, screen, screen_width: int, screen_height: int, **kwargs):
        self.screen        = screen
        self.screen_width  = screen_width
        self.screen_height = screen_height
        self._set_mode_fn  = None

    def set_app_callbacks(self, set_mode_fn):
        self._set_mode_fn = set_mode_fn

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, dt: float):
        pass

    def render_content(self):
        draw_room_panel(
            self.screen, self.screen_width, self.screen_height,
            title="💣  SPRENGSTOFF",
            subtitle="Hochrisiko  ·  Explosiv  ·  Keine Stabilitätspflicht",
            accent_color=_ACCENT,
        )

    def init(self):
        pass

    def on_enter(self):
        pass
