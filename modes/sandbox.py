"""
Sandbox-Modus – Vorplatz / leere Bühne.
Zeigt keinen eigenen Inhalt: Header, Console und Buttons werden
von main.py zentral gerendert. Der Sandbox-Modus ist bewusst leer –
er ist der neutrale Ausgangspunkt, von dem aus alle Räume erreichbar sind.
"""

import pygame


class Sandbox:
    """Vorplatz des CodeSandbox-Hubs – kein eigener Inhalt."""

    def __init__(self, screen, screen_width: int, screen_height: int, **kwargs):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._set_mode_fn = None

    def set_app_callbacks(self, set_mode_fn):
        self._set_mode_fn = set_mode_fn

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, dt: float):
        pass

    def render_content(self):
        pass   # Alles liegt hinter Header + Console – kein eigener Content

    def on_enter(self):
        pass
