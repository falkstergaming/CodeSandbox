"""
Vorhof – Außenperspektive auf das CodeSandbox-Gebäude.

Ein Schritt nach draußen: kein Arbeitsraum, sondern ein Wegweiser.
Zeigt alle 10 Buttons mit ihrer aktuellen Belegung und die Gebäude-Vision.

Farbkonzept: GRAU Hintergrund · GOLD Akzente · kein Raumtint (man steht draußen)
"""

import pygame
from core.utils.global_constants import (
    FONT_FAMILY, TEXT_LIGHT, TEXT_HIGHLIGHT,
    GRAU, GOLD, SILBER, BRONZE,
)

# Farb-Zuordnung pro Button-Typ (Beschriftungsfarbe in der Tabelle)
_COL = {
    "Gold":   GOLD["halftone"],
    "Silber": SILBER["halftone"],
    "Bronze": BRONZE["halftone"],
    "–":      GRAU["halftone"],
}

_LEFT_BUTTONS = [
    (0, "⏳", "Gold",   "Lobby"),
    (1, "🔒", "Gold",   "Museum"),
    (2, "?",  "Silber", "Raum 2   —  reserviert"),
    (3, "⛰", "Bronze", "Galerie"),
    (4, "♪",  "Gold",   "Jukebox"),
]
_RIGHT_BUTTONS = [
    (5, "⚙",  "Gold",   "Settings"),
    (6, "⚗",  "Silber", "Labor"),
    (7, "💣", "Bronze", "Sprengstoff"),
    (8, "?",  "Bronze", "Raum 8   —  reserviert"),
    (9, "🧭", "Gold",   "Vorhof"),
]

_VISION_LINES = [
    ("Ein Hotel für Code.", True),
    ("Jeder Raum ein Werkzeug. Jede Etage ein Reifegrad.", False),
    ("", False),
    ("Modular  ·  Persistent  ·  Erweiterbar  ·  Experimentell  ·  Dokumentiert", False),
]

_TICK = 8
_IM   = 3


class Vorhof:
    """Außenperspektive – Wegweiser und Gebäude-Übersicht."""

    def __init__(self, screen, screen_width: int, screen_height: int, **kwargs):
        self.screen        = screen
        self.screen_width  = screen_width
        self.screen_height = screen_height
        self._set_mode_fn  = None

        self._font_title  = pygame.font.SysFont(FONT_FAMILY, 18, bold=True)
        self._font_head   = pygame.font.SysFont(FONT_FAMILY, 13, bold=True)
        self._font_row    = pygame.font.SysFont(FONT_FAMILY, 13)
        self._font_vision = pygame.font.SysFont(FONT_FAMILY, 13)

    def set_app_callbacks(self, set_mode_fn):
        self._set_mode_fn = set_mode_fn

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, dt: float):
        pass

    def render_content(self):
        w, h = self.screen_width, self.screen_height

        # ── Panel-Dimensionen ────────────────────────────────────────────────
        btn_col_w = 25 + 48 + 14        # MARGIN_LEFT + button_size + gap
        header_h  = int(h * 0.12) + 25  # Header-Unterkante (y + status_height)
        console_h = 160 + 10            # Console-Höhe + Abstand

        px = btn_col_w + 12
        py = header_h + 14
        pw = w - 2 * px
        ph = h - py - console_h - 10

        self._draw_panel(px, py, pw, ph)

    def _draw_panel(self, px, py, pw, ph):
        surf = self.screen
        P    = 14    # inneres Padding

        # ── 1. Hintergrund ────────────────────────────────────────────────────
        bg = pygame.Surface((pw, ph), pygame.SRCALPHA)
        bg.fill((*GRAU["hightone"], 210))
        surf.blit(bg, (px, py))

        # ── 2. Rahmen: weiß außen, Gold innen + Eck-Akzente ─────────────────
        x1, y1 = px, py
        x2, y2 = px + pw - 1, py + ph - 1
        pygame.draw.rect(surf, TEXT_LIGHT, (x1, y1, pw, ph), 1)
        pygame.draw.rect(surf, TEXT_HIGHLIGHT,
                         (x1 + _IM, y1 + _IM, pw - 2*_IM, ph - 2*_IM), 1)
        for cx, cy in ((x1, y1), (x2, y1), (x1, y2), (x2, y2)):
            dx = _TICK if cx == x1 else -_TICK
            dy = _TICK if cy == y1 else -_TICK
            pygame.draw.line(surf, TEXT_HIGHLIGHT, (cx, cy), (cx + dx, cy), 2)
            pygame.draw.line(surf, TEXT_HIGHLIGHT, (cx, cy), (cx, cy + dy), 2)
            ox = 3 if cx == x1 else -3
            oy = 3 if cy == y1 else -3
            dcx, dcy = cx + ox, cy + oy
            pygame.draw.polygon(surf, TEXT_HIGHLIGHT, [
                (dcx, dcy - 3), (dcx + 3, dcy), (dcx, dcy + 3), (dcx - 3, dcy),
            ])

        inner_x = px + _IM + P
        inner_y = py + _IM + P
        inner_w = pw - 2 * (_IM + P)

        # ── 3. Titel ──────────────────────────────────────────────────────────
        title = self._font_title.render("◆  VORHOF  —  WEGWEISER  ◆", True, TEXT_HIGHLIGHT)
        surf.blit(title, title.get_rect(centerx=px + pw // 2, y=inner_y))
        title_bottom = inner_y + title.get_height() + 6

        self._draw_sep(surf, inner_x, inner_x + inner_w, title_bottom)
        table_top = title_bottom + 10

        # ── 4. Tabelle: zwei Spalten ──────────────────────────────────────────
        col_w     = inner_w // 2 - 8
        col_r_x   = inner_x + inner_w // 2 + 8
        row_h     = self._font_row.get_height() + 5

        # Spaltenköpfe
        lh = self._font_head.render("  #    sym   Farbe      Raum", True, GRAU["lowtone"])
        rh = self._font_head.render("  #    sym   Farbe      Raum", True, GRAU["lowtone"])
        surf.blit(lh, (inner_x,  table_top))
        surf.blit(rh, (col_r_x,  table_top))
        hd_bottom = table_top + lh.get_height() + 3
        self._draw_sep(surf, inner_x, inner_x + col_w,      hd_bottom)
        self._draw_sep(surf, col_r_x, col_r_x  + col_w,     hd_bottom)

        row_y = hd_bottom + 5
        for (num, sym, farbe, name), (num2, sym2, farbe2, name2) in zip(_LEFT_BUTTONS, _RIGHT_BUTTONS):
            self._draw_row(surf, inner_x, row_y, col_w, num, sym, farbe, name)
            self._draw_row(surf, col_r_x, row_y, col_w, num2, sym2, farbe2, name2)
            row_y += row_h

        # Vertikaler Trenner
        mid_x = inner_x + inner_w // 2
        pygame.draw.line(surf, GRAU["midtone"],
                         (mid_x, table_top), (mid_x, row_y), 1)

        # ── 5. Separator + Vision ─────────────────────────────────────────────
        vis_sep_y = row_y + 8
        self._draw_sep(surf, inner_x, inner_x + inner_w, vis_sep_y)
        vis_y = vis_sep_y + 10

        for text, bold in _VISION_LINES:
            if not text:
                vis_y += 6
                continue
            fnt   = pygame.font.SysFont(FONT_FAMILY, 13, bold=bold)
            color = TEXT_HIGHLIGHT if bold else GRAU["lowtone"]
            s     = fnt.render(text, True, color)
            surf.blit(s, s.get_rect(centerx=px + pw // 2, y=vis_y))
            vis_y += s.get_height() + 4

    def _draw_row(self, surf, x, y, col_w, num, sym, farbe, name):
        col = _COL.get(farbe, GRAU["halftone"])
        # Nummer
        ns = self._font_row.render(f" {num} ", True, col)
        surf.blit(ns, (x, y))
        # Symbol
        ss = self._font_row.render(f"  {sym}", True, col)
        surf.blit(ss, (x + 28, y))
        # Farbe
        fs = self._font_row.render(farbe, True, col)
        surf.blit(fs, (x + 64, y))
        # Raumname
        rs = self._font_row.render(name, True, GRAU["lowtone"])
        surf.blit(rs, (x + 120, y))

    def _draw_sep(self, surf, x1, x2, sy):
        pygame.draw.line(surf, GRAU["midtone"], (x1, sy), (x2, sy), 1)
        mid = (x1 + x2) // 2
        for px in (x1 + 4, x2 - 4, mid):
            sz = 3 if px == mid else 2
            pygame.draw.polygon(surf, TEXT_HIGHLIGHT, [
                (px, sy - sz), (px + sz, sy), (px, sy + sz), (px - sz, sy),
            ])

    def init(self):
        pass

    def on_enter(self):
        pass
