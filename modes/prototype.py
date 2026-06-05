"""
Prototyp-Modus – Testgelände für neue Ideen.
"""

import pygame
from core.utils.global_constants import (
    FONT_FAMILY, TEXT_LIGHT, TEXT_HIGHLIGHT,
    SCREEN_WIDTH, SCREEN_HEIGHT,
)


class Prototype:
    """Testgelände-Modus – Coming Soon."""

    def __init__(self, screen, screen_width: int, screen_height: int, **kwargs):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._font_title = pygame.font.SysFont(FONT_FAMILY, 36, bold=True)
        self._font_body  = pygame.font.SysFont(FONT_FAMILY, 20)

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, dt: float):
        pass

    def render_content(self):
        w, h = self.screen_width, self.screen_height

        pygame.draw.rect(self.screen, (22, 16, 10), (0, 0, w, 78))
        pygame.draw.line(self.screen, (80, 58, 36), (0, 78), (w, 78), 1)

        title = self._font_title.render("PROTOTYP", True, TEXT_HIGHLIGHT)
        self.screen.blit(title, (30, 20))

        msg = self._font_body.render("Testgelände — kommt bald.", True, TEXT_LIGHT)
        msg_rect = msg.get_rect(center=(w // 2, h // 2))
        self.screen.blit(msg, msg_rect)

    def init(self):
        pass

    def on_enter(self):
        pass
