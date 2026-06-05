"""
Museum-Modus – Ausstellungsraum & Navigationspunkt.
Farbkonzept: GRAU dominant · SILBER/Petrol Akzent · GOLD Highlight

Galerie-Ansicht:
  - 3 große Navigations-Hexagone (Labor, Prototyp, Exponate)
  - Exponate-Kacheln (Button 4000, …)
"""

import pygame
from core.utils.global_constants import (
    FONT_FAMILY, TEXT_LIGHT, TEXT_HIGHLIGHT, TEXT_DARK,
    FACTION_ADAM, FACTION_SKELETOR, FACTION_HORDAK, FACTION_ZODAK,
    GRAU, SILBER, GOLD,
)
from interfaces.renderer.pygame.components.button import HexButton, draw_raised_effects

# ── Raum-Farbpalette (GRAU→SILBER→GOLD) ─────────────────────────────────────
_BG_TINT  = (*GRAU["overtone"],  60)   # sehr dezente Petrol-Tinte
_PANEL_BG = GRAU["hightone"]          # Hintergrundstreifen / Panels
_BORDER   = SILBER["midtone"]         # Rahmenfarbe (Petrol)
_ACCENT   = GOLD["midtone"]           # Gold-Highlight (wenig einsetzen)
_TEXT     = SILBER["lowtone"]         # heller Petrol-Text (fast weiß mit Stich)
_TEXT_DIM = SILBER["halftone"]        # gedämpfter Label-Text
_NAV_FILL = SILBER["hightone"]        # Füllfarbe der Nav-Hexagone
_NAV_HOV  = SILBER["midtone"]         # Hover-Farbe der Nav-Hexagone
_SEP      = SILBER["midtone"]         # Trennlinie


class Museum:
    """
    Ausstellungsraum mit Navigation + Exponaten.

    Sub-Views:
      gallery       – Übersicht (Nav-Hexagone + Exponate-Liste)
      exhibit_4000  – Button 4000 Detail-Ansicht
    """

    def __init__(self, screen, screen_width: int, screen_height: int, **kwargs):
        self.screen = screen
        self.screen_width  = screen_width
        self.screen_height = screen_height
        self._view = "gallery"
        self._set_mode_fn = None

        self._font_title  = pygame.font.SysFont(FONT_FAMILY, 28, bold=True)
        self._font_header = pygame.font.SysFont(FONT_FAMILY, 20, bold=True)
        self._font_label  = pygame.font.SysFont(FONT_FAMILY, 14)
        self._font_small  = pygame.font.SysFont(FONT_FAMILY, 12)

        self._init_nav()
        self._init_gallery()
        self._init_exhibit_4000()

    # ── Callbacks ─────────────────────────────────────────────────────────

    def set_app_callbacks(self, set_mode_fn):
        self._set_mode_fn = set_mode_fn

    def _go_mode(self, mode: str):
        if self._set_mode_fn:
            self._set_mode_fn(mode)

    # ── Init ──────────────────────────────────────────────────────────────

    def _init_nav(self):
        """3 große Navigations-Hexagone (analog Sandbox, aber mit SILBER-Farben)."""
        size  = 110
        nav_y = 165   # unter dem Header, der bis ~121 geht
        entries = [
            (280,  "Labor",    "lab"),
            (640,  "Prototyp", "proto"),
            (1000, "Exponate", None),    # intern: wechselt zu exhibit_4000
        ]
        self._nav_buttons = []
        self._nav_labels  = []
        for cx, label, mode in entries:
            cb = (lambda m=mode: self._go_mode(m)) if mode else self._open_exhibit_4000
            btn = HexButton(
                x=cx - size // 2, y=nav_y,
                size=size,
                color=_NAV_FILL,
                text=label,
                callback=cb,
                highlight_color=_NAV_HOV,
                highlight_text_color=TEXT_HIGHLIGHT,
                text_color=_TEXT,
                font_size=16,
            )
            self._nav_buttons.append(btn)
            self._nav_labels.append((cx, nav_y + size + 10, label))

    def _init_gallery(self):
        """Exponate-Kachel (Button 4000)."""
        self._tile_4000 = HexButton(
            x=590, y=350,
            size=80,
            color=SILBER["overtone"],
            text="4000",
            highlight_color=SILBER["hightone"],
            text_color=TEXT_HIGHLIGHT,
            callback=self._open_exhibit_4000,
            font_size=22,
        )

    def _init_exhibit_4000(self):
        factions = ["Adam", "Skeletor", "Hordak", "Zodak"]
        colors   = [
            FACTION_ADAM["primary"], FACTION_SKELETOR["primary"],
            FACTION_HORDAK["primary"], FACTION_ZODAK["primary"],
        ]

        self._back_button = HexButton(
            x=15, y=130, size=40,
            color=SILBER["hightone"],
            text="←",
            callback=self._close_exhibit,
            text_color=_TEXT,
            font_size=18,
            angle_offset=30,
            alpha=220,
        )

        col_x = [400, 500, 600, 700]
        row_y = [170, 270, 370, 470]
        states = [
            (False, False, False),
            (True,  False, False),
            (False, True,  False),
            (False, False, True),
        ]
        self._showcase_buttons = []
        for row_idx, (is_hl, is_sel, is_dis) in enumerate(states):
            for col_idx, faction in enumerate(factions):
                btn = HexButton(
                    x=col_x[col_idx], y=row_y[row_idx],
                    size=80, color=colors[col_idx], faction=faction,
                    text_color=TEXT_LIGHT, font_size=16,
                )
                btn.is_highlighted = is_hl
                btn.is_selected    = is_sel
                btn.is_disabled    = is_dis
                self._showcase_buttons.append(btn)

        col_x_inter = [410, 510, 610, 710]
        self._interactive_buttons = []
        for i, (faction, color) in enumerate(zip(factions, colors)):
            btn = HexButton(
                x=col_x_inter[i], y=590,
                size=60, color=color, faction=faction,
                text_color=TEXT_LIGHT, font_size=14,
            )
            self._interactive_buttons.append(btn)

    # ── Navigation intern ─────────────────────────────────────────────────

    def _open_exhibit_4000(self):
        self._view = "exhibit_4000"

    def _close_exhibit(self):
        self._view = "gallery"

    # ── Public interface ──────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event):
        if self._view == "gallery":
            for btn in self._nav_buttons:
                btn.handle_event(event)
            self._tile_4000.handle_event(event)
        elif self._view == "exhibit_4000":
            self._back_button.handle_event(event)
            for btn in self._interactive_buttons:
                btn.handle_event(event)

    def update(self, dt: float):
        pass

    def render_content(self):
        if self._view == "gallery":
            self._render_gallery()
        elif self._view == "exhibit_4000":
            self._render_exhibit_4000()

    def init(self):
        pass

    def on_enter(self):
        self._view = "gallery"

    # ── Rendering ─────────────────────────────────────────────────────────

    def _draw_sep(self, y: int, x1: int = None, x2: int = None):
        w  = self.screen_width
        x1 = x1 if x1 is not None else 73
        x2 = x2 if x2 is not None else w - 73
        pygame.draw.line(self.screen, _SEP, (x1, y), (x2, y), 1)
        mid = (x1 + x2) // 2
        for px in (x1 + 6, x2 - 6, mid):
            sz = 3 if px == mid else 2
            pygame.draw.polygon(self.screen, _ACCENT, [
                (px, y - sz), (px + sz, y), (px, y + sz), (px - sz, y)
            ])

    def _render_gallery(self):
        w = self.screen_width

        # ── Petrol-Tint-Overlay auf dem Content-Bereich ──────────────────
        _ov = pygame.Surface((w, self.screen_height), pygame.SRCALPHA)
        _ov.fill(_BG_TINT)
        self.screen.blit(_ov, (0, 0))

        # ── Separator unter Header ────────────────────────────────────────
        self._draw_sep(128)

        # ── 3 Navigations-Hexagone ────────────────────────────────────────
        draw_raised_effects(self.screen, self._nav_buttons)
        for btn in self._nav_buttons:
            btn.render(self.screen)
        for cx, ly, label in self._nav_labels:
            lbl = self._font_label.render(label, True, _TEXT_DIM)
            self.screen.blit(lbl, lbl.get_rect(centerx=cx, y=ly))

        # ── Separator vor Exponate ─────────────────────────────────────────
        sep_y = 308
        self._draw_sep(sep_y)
        exp_label = self._font_label.render("EXPONATE", True, _ACCENT)
        self.screen.blit(exp_label, (73, sep_y + 7))

        # ── Exponat-Kachel 4000 ───────────────────────────────────────────
        draw_raised_effects(self.screen, [self._tile_4000])
        self._tile_4000.render(self.screen)

        hint = self._font_small.render("HexButton  ·  Design-Referenz  ·  klicken", True, _TEXT_DIM)
        self.screen.blit(hint, hint.get_rect(centerx=630, y=445))

    def _render_exhibit_4000(self):
        w = self.screen_width

        # Petrol-Tint
        _ov = pygame.Surface((w, self.screen_height), pygame.SRCALPHA)
        _ov.fill(_BG_TINT)
        self.screen.blit(_ov, (0, 0))

        # Zurück-Button
        draw_raised_effects(self.screen, [self._back_button])
        self._back_button.render(self.screen)

        # ID + Titel
        badge = self._font_header.render("4000", True, _ACCENT)
        self.screen.blit(badge, (65, 133))
        title = self._font_header.render("HexButton  —  Design-Referenz", True, _TEXT)
        self.screen.blit(title, (120, 133))

        self._draw_sep(158)

        # Spaltenköpfe
        factions    = ["Adam", "Skeletor", "Hordak", "Zodak"]
        col_centers = [440, 540, 640, 740]
        for i, faction in enumerate(factions):
            lbl = self._font_label.render(faction, True, _TEXT_DIM)
            self.screen.blit(lbl, lbl.get_rect(centerx=col_centers[i], y=160))

        # Zeilenbeschriftung
        state_names   = ["Normal", "Hover", "Selektiert", "Deaktiviert"]
        row_centers_y = [210, 310, 410, 510]
        for i, name in enumerate(state_names):
            lbl = self._font_label.render(name, True, _TEXT_DIM)
            self.screen.blit(lbl, lbl.get_rect(right=392, centery=row_centers_y[i]))

        # Schaukasten-Grid
        draw_raised_effects(self.screen, self._showcase_buttons)
        for btn in self._showcase_buttons:
            btn.render(self.screen)

        # Separator + interaktive Reihe
        self._draw_sep(568)
        sep_lbl = self._font_label.render("Interaktiv  ·  Hover & Klick", True, _ACCENT)
        self.screen.blit(sep_lbl, (73, 573))

        draw_raised_effects(self.screen, self._interactive_buttons)
        for btn in self._interactive_buttons:
            btn.render(self.screen)
