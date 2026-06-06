"""
Raum 8 – Reservierter Bronze-Raum (ohne Zweckbestimmung).
Farbkonzept: GRAU Hintergrund · BRONZE Akzent
"""

import pygame
from core.utils.global_constants import BRONZE
from interfaces.renderer.pygame.components.room_panel import draw_room_panel

_ACCENT = BRONZE["halftone"]


class Raum8:
    """Raum 8 – reserviert, ohne Zweckbestimmung."""

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
            title="RAUM 8",
            subtitle="Reserviert  ·  Ohne Zweckbestimmung",
            accent_color=_ACCENT,
        )

    def init(self):
        pass

    def on_enter(self):
        pass
