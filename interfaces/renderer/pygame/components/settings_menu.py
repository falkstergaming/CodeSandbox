"""
Settings-Menü für CodeSandbox.
Farbkonzept: GRAU (neutral, dunkel) mit Gold-Akzenten.
Gleiche Dekorationssprache wie Header und Console.
"""

import pygame
from pygame.locals import *
from typing import Optional
from core.utils.global_constants import (
    FONT_FAMILY, FONT_SYMBOL,
    TEXT_LIGHT, TEXT_HIGHLIGHT, TEXT_DARK,
    GRAU, GOLD,
)
from core.utils.translations import TRANSLATIONS
from core.utils.settings import Settings

_BG      = GRAU["overtone"]    # (31, 33, 41)  — sehr dunkler Hintergrund
_TRACK   = GRAU["hightone"]    # (44, 50, 64)  — Slider-Spur
_FILL    = GOLD["midtone"]     # (163,120, 0)  — Slider-Füllung
_LABEL   = GRAU["lowtone"]     # (220,225,234) — heller Label-Text
_ACCENT  = TEXT_HIGHLIGHT      # (255,227,106) — Gold-Akzent
_FRAME   = TEXT_LIGHT          # (243,230,193) — äußerer Rahmen
_TICK    = 8


class SettingsMenu:
    """
    Kontextmenü für Einstellungen.
    Enthält: Sprachauswahl · Musik-Lautstärke · Effekt-Lautstärke
    """

    def __init__(self, x: int, y: int, width: int = 300, settings: Optional[Settings] = None):
        self.x       = x
        self.y       = y
        self.width   = width
        self.height  = 255
        self.settings = settings if settings else Settings()
        self.is_active   = False
        self.active_slider = None

        self.font       = pygame.font.SysFont(FONT_FAMILY, 14)
        self.font_title = pygame.font.SysFont(FONT_FAMILY, 15, bold=True)
        self.font_sym   = pygame.font.SysFont(FONT_SYMBOL[0], 14)

        self.padding      = 14
        self.line_height  = 28
        self.slider_width = 160
        self.slider_height = 8

    # ── Public API ─────────────────────────────────────────────────────────

    def toggle(self) -> None:
        self.is_active = not self.is_active

    # ── Event Handling ──────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.is_active:
            return False

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if self._lang_rect().collidepoint(pos):
                self.settings.language = "de" if self.settings.language == "en" else "en"
                return True
            if self._slider_rect("music").collidepoint(pos):
                self.active_slider = "music"
                self._set_slider(pos, "music")
                return True
            if self._slider_rect("effect").collidepoint(pos):
                self.active_slider = "effect"
                self._set_slider(pos, "effect")
                return True
            if not pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(pos):
                self.is_active = False
            return True

        elif event.type == MOUSEBUTTONUP and event.button == 1:
            self.active_slider = None
            return False

        elif event.type == MOUSEMOTION:
            if self.active_slider and pygame.mouse.get_pressed()[0]:
                self._set_slider(pygame.mouse.get_pos(), self.active_slider)
                return True
            return False

        return False

    def _lang_rect(self) -> pygame.Rect:
        P = self.padding
        return pygame.Rect(self.x + P, self.y + P + self.line_height,
                           self.width - 2 * P, self.line_height)

    def _slider_rect(self, kind: str) -> pygame.Rect:
        P  = self.padding
        LH = self.line_height
        if kind == "music":
            sy = self.y + P + LH * 3 + 6
        else:
            sy = self.y + P + LH * 5 + 8
        return pygame.Rect(self.x + P, sy - 6, self.slider_width, self.slider_height + 12)

    def _set_slider(self, pos, kind: str) -> None:
        rel = max(0, min(self.slider_width, pos[0] - self.x - self.padding))
        val = int(rel / self.slider_width * 100)
        if kind == "music":
            self.settings.music_volume = val
        else:
            self.settings.effect_volume = val

    # ── Render ─────────────────────────────────────────────────────────────

    def render(self, surface: pygame.Surface) -> None:
        if not self.is_active:
            return

        lang = getattr(self.settings, 'language', 'en')
        t    = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
        P    = self.padding
        LH   = self.line_height
        IM   = 3
        x, y, w, h = self.x, self.y, self.width, self.height

        # ── 1. Semi-transparenter Hintergrund ──────────────────────────────
        _ov = pygame.Surface((w, h), pygame.SRCALPHA)
        _ov.fill((*_BG, 230))
        surface.blit(_ov, (x, y))

        x1, y1, x2, y2 = x, y, x + w - 1, y + h - 1

        # Äußerer weißer Rahmen
        pygame.draw.rect(surface, _FRAME, (x, y, w, h), 1)
        # Innerer Gold-Rahmen
        pygame.draw.rect(surface, _ACCENT,
                         (x1 + IM, y1 + IM, w - 2*IM, h - 2*IM), 1)

        # Ecken-Akzente (L-Form + Diamant)
        for cx, cy in ((x1, y1), (x2, y1), (x1, y2), (x2, y2)):
            dx = _TICK if cx == x1 else -_TICK
            dy = _TICK if cy == y1 else -_TICK
            pygame.draw.line(surface, _ACCENT, (cx, cy), (cx + dx, cy), 2)
            pygame.draw.line(surface, _ACCENT, (cx, cy), (cx, cy + dy), 2)
            ox = 2 if cx == x1 else -2
            oy = 2 if cy == y1 else -2
            dcx, dcy = cx + ox, cy + oy
            pygame.draw.polygon(surface, _ACCENT, [
                (dcx,     dcy - 3),
                (dcx + 3, dcy    ),
                (dcx,     dcy + 3),
                (dcx - 3, dcy    ),
            ])

        # ── 2. Titel ────────────────────────────────────────────────────────
        title_surf = self.font_title.render(t["settings"].upper(), True, _ACCENT)
        ty = y + P - 2
        surface.blit(title_surf, (x + (w - title_surf.get_width()) // 2, ty))

        # Separator unter Titel
        sep_y = ty + title_surf.get_height() + 4
        self._draw_sep(surface, x + IM + 4, x + w - IM - 4, sep_y)

        # ── 3. Sprache ──────────────────────────────────────────────────────
        row_y = sep_y + 6
        label_surf = self.font.render(f"{t['language']}:", True, _LABEL)
        surface.blit(label_surf, (x + P, row_y))

        lang_name = t["german"] if lang == "de" else t["english"]
        val_surf  = self.font.render(f"[ {lang_name.upper()} ]", True, _ACCENT)
        surface.blit(val_surf, (x + w - P - val_surf.get_width(), row_y))

        # ── 4. Separator ────────────────────────────────────────────────────
        sep2_y = row_y + LH
        self._draw_sep(surface, x + IM + 4, x + w - IM - 4, sep2_y)

        # ── 5. Musik-Lautstärke ─────────────────────────────────────────────
        mu_y = sep2_y + 8
        mu_label = self.font.render(f"{t['music_volume']}:", True, _LABEL)
        surface.blit(mu_label, (x + P, mu_y))

        sl_mu_y = mu_y + LH - 6
        self._draw_slider(surface, x + P, sl_mu_y, self.settings.music_volume)

        pct_mu = self.font.render(f"{self.settings.music_volume}%", True, _LABEL)
        surface.blit(pct_mu, (x + P + self.slider_width + 10, sl_mu_y - 3))

        # ── 6. Separator ────────────────────────────────────────────────────
        sep3_y = sl_mu_y + self.slider_height + 14
        self._draw_sep(surface, x + IM + 4, x + w - IM - 4, sep3_y)

        # ── 7. Effekt-Lautstärke ─────────────────────────────────────────────
        ef_y = sep3_y + 8
        ef_label = self.font.render(f"{t['effect_volume']}:", True, _LABEL)
        surface.blit(ef_label, (x + P, ef_y))

        sl_ef_y = ef_y + LH - 6
        self._draw_slider(surface, x + P, sl_ef_y, self.settings.effect_volume)

        pct_ef = self.font.render(f"{self.settings.effect_volume}%", True, _LABEL)
        surface.blit(pct_ef, (x + P + self.slider_width + 10, sl_ef_y - 3))

    def _draw_sep(self, surface, x1, x2, sy):
        pygame.draw.line(surface, _LABEL, (x1, sy), (x2, sy), 1)
        mid = (x1 + x2) // 2
        for px in (x1 + 4, x2 - 4, mid):
            sz = 3 if px == mid else 2
            pygame.draw.polygon(surface, _ACCENT, [
                (px,      sy - sz),
                (px + sz, sy     ),
                (px,      sy + sz),
                (px - sz, sy     ),
            ])

    def _draw_slider(self, surface, x, y, value):
        # Spur
        pygame.draw.rect(surface, _TRACK, (x, y, self.slider_width, self.slider_height), 0, 4)
        # Füllung
        fill_w = int(value / 100 * self.slider_width)
        if fill_w > 0:
            pygame.draw.rect(surface, _FILL, (x, y, fill_w, self.slider_height), 0, 4)
        # Knob
        knob_x = x + max(self.slider_height // 2, fill_w)
        pygame.draw.circle(surface, _ACCENT, (knob_x, y + self.slider_height // 2), 7)
        pygame.draw.circle(surface, _BG,     (knob_x, y + self.slider_height // 2), 4)
