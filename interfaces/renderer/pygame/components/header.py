"""
AppHeader - Kopfzeile für CodeSandbox.
Visuelles Design 1:1 aus Assault on Grayskull (GameStatusDisplay).

Layout (obere 12% des Bildschirms):
  [MARGIN] Info-Block: Titel "CODE SANDBOX" [GAP] Modus-Block: aktiver Modus [MARGIN]

Identische Dekorationssprache:
  - Semi-transparenter Hintergrund
  - Weißer Außenrahmen + Gold-Innenrahmen (3px Abstand)
  - L-förmige Ecken-Akzente mit kleinem Diamant
  - Separator-Linien mit Diamant-Endmarken und zentralem Diamant
  - ◆ TITEL ◆ Muster mit Goldlinien links/rechts
"""

import pygame
from typing import Optional, TYPE_CHECKING
from core.utils.global_constants import (
    COLORS, FONT_FAMILY, FONT_SYMBOL, TEXT_LIGHT, TEXT_HIGHLIGHT,
)

if TYPE_CHECKING:
    from core.utils.settings import Settings


class AppHeader:
    """Kopfzeile für CodeSandbox (obere 12% des Bildschirms)."""

    MARGIN = 25
    GAP    = 3
    TICK   = 10

    # Modus-Label + Kurzinfo für den rechten Block
    MODE_LABELS = {
        "sandbox": ("LOBBY",    "Empfang  ·  Navigation  ·  Startpunkt"),
        "museum":  ("MUSEUM",   "Ausstellung  ·  Exponate  ·  Design-Referenzen"),
        "lab":     ("LABOR",    "Werkstatt  ·  Experimente  ·  Aktive Entwicklung"),
        "proto":   ("PROTOTYP", "Testgelände  ·  Sandbox  ·  Keine Stabilitätspflicht"),
    }

    def __init__(self, width: int, height: int, settings: Optional['Settings'] = None):
        self.width         = width
        self.height        = height
        self.status_height = int(height * 0.12)
        self.y             = 25
        self.settings      = settings
        self._mode         = "sandbox"

        self.title_font      = pygame.font.SysFont(FONT_FAMILY, 36, bold=True)
        self.mode_font       = pygame.font.SysFont(FONT_FAMILY, 15, bold=True)
        self.stat_font       = pygame.font.SysFont(FONT_FAMILY, 14)
        self.title_deco_font = pygame.font.SysFont(FONT_SYMBOL[0], 22)

    def set_mode(self, mode: str) -> None:
        self._mode = mode

    def resize(self, width: int, height: int) -> None:
        self.width  = width
        self.height = height
        self.status_height = int(height * 0.12)

    # ─────────────────────────────────────────────────────────────────────────

    def render(self, surface: pygame.Surface) -> None:
        G      = self.GAP
        M      = self.MARGIN
        TICK   = self.TICK
        BG     = COLORS["background"]
        ACCENT = TEXT_HIGHLIGHT
        IM     = 3
        P      = 12

        # 38% Info-Block / 62% Modus-Block
        split_x = M + int((self.width - 2 * M) * 0.38)

        ly      = self.y + G
        inner_h = self.status_height - 2 * G
        title_h    = int(inner_h * 0.56)
        info_h     = inner_h - title_h
        title_sep_y = ly + title_h
        info_sub_h = info_h // 2

        # Info-Block (links)
        lx  = M
        lw  = split_x - M - G
        lrx = lx + lw - 1
        lby = ly + inner_h - 1

        # Modus-Block (rechts)
        fx  = split_x
        fw  = self.width - M - split_x
        frx = self.width - M - 1

        title_area_top = ly + IM + 1
        title_area_h   = title_h - IM - 1

        # ── Hilfsfunktionen (identisch mit GameStatusDisplay) ────────────────

        def fancy_corner(x1, y1, x2, y2):
            for cx, cy in ((x1, y1), (x2, y1), (x1, y2), (x2, y2)):
                dx = TICK if cx == x1 else -TICK
                dy = TICK if cy == y1 else -TICK
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

        def separator_line(x_left, x_right, sy):
            pygame.draw.line(surface, TEXT_LIGHT, (x_left + 2, sy), (x_right - 2, sy), 1)
            mid = (x_left + x_right) // 2
            for bx in (x_left + 5, x_right - 9):
                pygame.draw.polygon(surface, ACCENT, [
                    (bx + 2, sy    ),
                    (bx + 4, sy - 2),
                    (bx + 6, sy    ),
                    (bx + 4, sy + 2),
                ])
            pygame.draw.polygon(surface, ACCENT, [
                (mid,     sy - 4),
                (mid + 4, sy    ),
                (mid,     sy + 4),
                (mid - 4, sy    ),
            ])

        def blit_vcenter(surf, x, band_top, band_h):
            vy = band_top + (band_h - surf.get_height()) // 2
            surface.blit(surf, (x, vy))

        def draw_title_block(label: str, bx: int, bw: int, brx: int):
            """Zeichnet den ◆ LABEL ◆ Titelblock zentriert in einem Rechteck."""
            t_surf   = self.title_font.render(label, True, TEXT_LIGHT)
            t_shadow = self.title_font.render(label, True, (55, 40, 18))
            d_surf   = self.title_deco_font.render("◆", True, ACCENT)
            gap      = 12
            grp_w    = d_surf.get_width() + gap + t_surf.get_width() + gap + d_surf.get_width()
            grp_x    = bx + (bw - grp_w) // 2
            tx       = grp_x + d_surf.get_width() + gap
            ty       = title_area_top + (title_area_h - t_surf.get_height()) // 2
            dy       = ty + (t_surf.get_height() - d_surf.get_height()) // 2
            surface.blit(t_shadow, (tx + 1, ty + 1))
            surface.blit(t_surf,   (tx,     ty    ))
            surface.blit(d_surf, (grp_x,                             dy))
            surface.blit(d_surf, (grp_x + grp_w - d_surf.get_width(), dy))
            # Goldlinien links/rechts vom Titelblock
            line_y    = ty + t_surf.get_height() // 2
            gap_deco  = 10
            ll_x1, ll_x2 = bx + IM + P, grp_x - gap_deco
            rl_x1, rl_x2 = grp_x + grp_w + gap_deco, brx - IM - P
            for x1l, x2l in ((ll_x1, ll_x2), (rl_x1, rl_x2)):
                if x2l > x1l + 12:
                    pygame.draw.line(surface, ACCENT, (x1l, line_y), (x2l, line_y), 1)
                    pygame.draw.rect(surface, ACCENT, pygame.Rect(x1l,     line_y - 2, 4, 5))
                    pygame.draw.rect(surface, ACCENT, pygame.Rect(x2l - 3, line_y - 2, 4, 5))

        # ── 1. Semi-transparenter Hintergrund ─────────────────────────────────
        _ov = pygame.Surface((self.width, self.status_height), pygame.SRCALPHA)
        _ov.fill((*BG[:3], 128))
        surface.blit(_ov, (0, self.y))

        # ── 2. Info-Block links: "CODE SANDBOX" ──────────────────────────────
        pygame.draw.rect(surface, TEXT_LIGHT, pygame.Rect(lx, ly, lw, inner_h), 1)
        pygame.draw.rect(surface, ACCENT,
                         pygame.Rect(lx + IM, ly + IM, lw - 2*IM, inner_h - 2*IM), 1)
        fancy_corner(lx, ly, lrx, lby)
        separator_line(lx + IM, lrx - IM, title_sep_y)

        draw_title_block("CODE SANDBOX", lx, lw, lrx)

        sub1 = self.mode_font.render("[ ENTWICKLUNGS-HUB ]", True, ACCENT)
        sub2 = self.stat_font.render("Python  ·  Pygame  ·  Alpha v0.1", True, TEXT_LIGHT)
        blit_vcenter(sub1, lx + P, title_sep_y, info_sub_h)
        blit_vcenter(sub2, lx + P, title_sep_y + info_sub_h, info_sub_h)

        # ── 3. Modus-Block rechts: aktiver Modus ─────────────────────────────
        pygame.draw.rect(surface, TEXT_LIGHT, pygame.Rect(fx, ly, fw, inner_h), 1)
        pygame.draw.rect(surface, ACCENT,
                         pygame.Rect(fx + IM, ly + IM, fw - 2*IM, inner_h - 2*IM), 1)
        fancy_corner(fx, ly, frx, lby)
        separator_line(fx + IM, frx - IM, title_sep_y)

        mode_label, mode_desc = self.MODE_LABELS.get(
            self._mode, (self._mode.upper(), "")
        )
        draw_title_block(mode_label, fx, fw, frx)

        desc_surf = self.stat_font.render(mode_desc, True, TEXT_LIGHT)
        blit_vcenter(desc_surf, fx + P, title_sep_y, info_sub_h)
