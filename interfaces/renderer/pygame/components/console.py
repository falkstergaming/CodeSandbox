"""
Text-Konsole für CodeSandbox.
Zeigt Log-Meldungen an. Visuelles Design 1:1 aus Assault on Grayskull.
"""

import pygame
from core.utils.global_constants import (
    COLORS, TEXT_DARK, TEXT_LIGHT, TEXT_HIGHLIGHT,
    FONT_CONSOLE, CONSOLE_SYMBOLS, FONT_SYMBOL,
)


class Console:
    """
    Persistente Text-Konsole für Debug-Ausgaben und Statusmeldungen.

    log(text, symbol_type)  — Zeile anhängen
    clear()                 — Konsole leeren
    resize(x, y, w, h)     — Größe anpassen (z.B. bei VIDEORESIZE)
    render(surface)         — Zeichnen
    """

    def __init__(self, x: int, y: int, width: int, height: int, max_lines: int = 15):
        self.x = x
        self.y = y
        self.width  = width
        self.height = height
        self.lines  = []   # [(symbol, text, symbol_type), ...]
        self.font        = pygame.font.SysFont(*FONT_CONSOLE)
        self.symbol_font = pygame.font.SysFont(*FONT_SYMBOL)
        self.line_height      = self.font.get_height() + 2
        self.max_visible_lines = max(1, (self.height - 20) // self.line_height)
        self.max_lines = min(max_lines, self.max_visible_lines)

    def log(self, text: str, color: tuple = None, symbol_type: str = None):
        if symbol_type is None and color == TEXT_HIGHLIGHT:
            symbol_type = "highlight"
        symbol = CONSOLE_SYMBOLS.get(symbol_type, "") if symbol_type else ""
        self.lines.append((symbol, text, symbol_type))
        if len(self.lines) > self.max_lines:
            self.lines.pop(0)

    def clear(self):
        self.lines = []

    def resize(self, x: int, y: int, width: int, height: int):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.font        = pygame.font.SysFont(*FONT_CONSOLE)
        self.symbol_font = pygame.font.SysFont(*FONT_SYMBOL)
        self.line_height       = self.font.get_height() + 2
        self.max_visible_lines = max(1, (self.height - 20) // self.line_height)
        self.max_lines = min(self.max_lines, self.max_visible_lines)

    def render(self, surface: pygame.Surface):
        BG     = COLORS["background"]
        ACCENT = TEXT_HIGHLIGHT
        TICK   = 10
        IM     = 3

        _ov = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        _ov.fill((*BG[:3], 128))
        surface.blit(_ov, (self.x, self.y))

        x1, y1 = self.x, self.y
        x2, y2 = self.x + self.width - 1, self.y + self.height - 1

        pygame.draw.rect(surface, TEXT_LIGHT, (self.x, self.y, self.width, self.height), 1)
        pygame.draw.rect(surface, ACCENT,
                         (x1 + IM, y1 + IM, self.width - 2*IM, self.height - 2*IM), 1)

        for cx, cy in ((x1, y1), (x2, y1), (x1, y2), (x2, y2)):
            dx = TICK  if cx == x1 else -TICK
            dy = TICK  if cy == y1 else -TICK
            pygame.draw.line(surface, ACCENT, (cx, cy), (cx + dx, cy), 2)
            pygame.draw.line(surface, ACCENT, (cx, cy), (cx, cy + dy), 2)
            ox = 2 if cx == x1 else -2
            oy = 2 if cy == y1 else -2
            dcx, dcy = cx + ox, cy + oy
            pygame.draw.polygon(surface, ACCENT, [
                (dcx,     dcy - 3),
                (dcx + 3, dcy    ),
                (dcx,     dcy + 3),
                (dcx - 3, dcy    ),
            ])

        pad_x = IM + 7
        pad_y = IM + 4
        for i, (symbol, text, symbol_type) in enumerate(self.lines):
            y_pos = self.y + pad_y + i * self.line_height
            if y_pos + self.line_height > self.y + self.height - IM:
                break
            x_pos = self.x + pad_x
            if symbol:
                sym_surf = self.symbol_font.render(symbol, True, ACCENT)
                surface.blit(sym_surf, (x_pos, y_pos))
                x_pos += sym_surf.get_width() + 4
            text_surf = self.font.render(text, True, TEXT_LIGHT)
            surface.blit(text_surf, (x_pos, y_pos))
