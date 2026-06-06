"""
Standard Room Panel für CodeSandbox.

Einheitliches Content-Fenster für alle Räume:
  - 15 px Abstand zu Header (oben) und Console (unten)
  - Genug Abstand zu den Button-Spalten links/rechts
  - Weißer Außen- + farbiger Innenrahmen mit Eck-Akzenten
  - Optionaler Titel + Separator am Panel-Kopf

Nutzung:
    from interfaces.renderer.pygame.components.room_panel import draw_room_panel

    inner_rect = draw_room_panel(
        screen, screen_width, screen_height,
        title="⚗  LABOR",
        subtitle="Werkstatt  ·  Experimente",
        accent_color=SILBER["halftone"],
    )
    ix, iy, iw, ih = inner_rect   # freier Innenbereich für Raum-Inhalt
"""

import pygame
from core.utils.global_constants import FONT_FAMILY, GRAU
from core.utils.colors import TEXT_LIGHT, TEXT_HIGHLIGHT

# Layout-Konstanten (müssen mit main.py übereinstimmen)
_MARGIN_L  = 25     # main.py: MARGIN_LEFT
_BTN_SIZE  = 48     # main.py: button size
_BTN_GAP   = 10     # Spalt zwischen Button und Panel-Rand
_HDR_Y     = 25     # header.py: self.y
_HDR_FRAC  = 0.12   # header.py: status_height = int(h * _HDR_FRAC)
_CON_H     = 160    # main.py: console height
_CON_GAP   = 10     # main.py: margin console to bottom edge
_PANEL_GAP = 15     # Luft zu Header und Console

_IM   = 3    # Abstand Außen- zu Innenrahmen
_TICK = 8    # Länge der Eck-Akzentlinien
_PAD  = 14   # inneres Content-Padding

_font_cache: dict = {}


def _font(size: int, bold: bool = False) -> pygame.font.Font:
    key = (size, bold)
    if key not in _font_cache:
        _font_cache[key] = pygame.font.SysFont(FONT_FAMILY, size, bold=bold)
    return _font_cache[key]


def draw_room_panel(
    screen: pygame.Surface,
    screen_width: int,
    screen_height: int,
    title: str = "",
    subtitle: str = "",
    accent_color: tuple = None,
) -> tuple:
    """
    Zeichnet das Standard-Raum-Panel.

    Args:
        title:        Raumtitel zentriert am Panel-Kopf (leer = kein Titel)
        subtitle:     Kurzbeschreibung unterhalb des Titels
        accent_color: Rahmen- und Titelfarbe; Standard = TEXT_HIGHLIGHT (Gold)

    Returns:
        (inner_x, inner_y, inner_w, inner_h) — freier Innenbereich für Raum-Inhalt
    """
    w, h = screen_width, screen_height
    col  = accent_color or TEXT_HIGHLIGHT

    btn_col_w   = _MARGIN_L + _BTN_SIZE + _BTN_GAP     # linke Grenze der Button-Spalte
    header_bot  = _HDR_Y + int(h * _HDR_FRAC)          # untere Kante des Headers
    console_top = h - _CON_H - _CON_GAP                # obere Kante der Console

    px = btn_col_w + _PANEL_GAP
    py = header_bot + _PANEL_GAP
    pw = w - 2 * px
    ph = console_top - py - _PANEL_GAP

    # ── 1. Hintergrund ───────────────────────────────────────────────────────
    bg = pygame.Surface((pw, ph), pygame.SRCALPHA)
    bg.fill((*GRAU["hightone"], 210))
    screen.blit(bg, (px, py))

    # ── 2. Rahmen: weiß außen · accent innen + Eck-Akzente ──────────────────
    x1, y1 = px, py
    x2, y2 = px + pw - 1, py + ph - 1
    pygame.draw.rect(screen, TEXT_LIGHT, (x1,       y1,       pw,          ph         ), 1)
    pygame.draw.rect(screen, col,        (x1 + _IM, y1 + _IM, pw - 2*_IM,  ph - 2*_IM), 1)
    for cx, cy in ((x1, y1), (x2, y1), (x1, y2), (x2, y2)):
        dx = _TICK if cx == x1 else -_TICK
        dy = _TICK if cy == y1 else -_TICK
        pygame.draw.line(screen, col, (cx, cy), (cx + dx, cy), 2)
        pygame.draw.line(screen, col, (cx, cy), (cx, cy + dy), 2)
        ox = 3 if cx == x1 else -3
        oy = 3 if cy == y1 else -3
        dcx, dcy = cx + ox, cy + oy
        pygame.draw.polygon(screen, col, [
            (dcx, dcy - 3), (dcx + 3, dcy), (dcx, dcy + 3), (dcx - 3, dcy),
        ])

    # ── 3. Titel + Trennlinie ────────────────────────────────────────────────
    inner_x   = px + _IM + _PAD
    inner_y   = py + _IM + _PAD
    inner_w   = pw - 2 * (_IM + _PAD)
    content_y = inner_y

    if title:
        t_surf = _font(18, bold=True).render(title, True, col)
        screen.blit(t_surf, t_surf.get_rect(centerx=px + pw // 2, y=inner_y))
        sep_y = inner_y + t_surf.get_height() + 6
        _draw_sep(screen, inner_x, inner_x + inner_w, sep_y, col)
        content_y = sep_y + 10

    if subtitle:
        s_surf = _font(13).render(subtitle, True, GRAU["lowtone"])
        screen.blit(s_surf, s_surf.get_rect(centerx=px + pw // 2, y=content_y))
        content_y += s_surf.get_height() + 8

    inner_h = (py + ph - _IM - _PAD) - content_y
    return (inner_x, content_y, inner_w, inner_h)


def _draw_sep(screen, x1, x2, sy, col):
    pygame.draw.line(screen, GRAU["midtone"], (x1, sy), (x2, sy), 1)
    mid = (x1 + x2) // 2
    for bx in (x1 + 4, x2 - 4, mid):
        sz = 3 if bx == mid else 2
        pygame.draw.polygon(screen, col, [
            (bx, sy - sz), (bx + sz, sy), (bx, sy + sz), (bx - sz, sy),
        ])
