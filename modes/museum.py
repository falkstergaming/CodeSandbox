"""
Museum-Modus – Ausstellungsraum.
Enthält Galerie-Übersicht und einzelne Exponate.
Erstes Exponat: Button 4000 (HexButton Design-Referenz).
"""

import pygame
from core.utils.global_constants import (
    FONT_FAMILY, TEXT_LIGHT, TEXT_HIGHLIGHT, TEXT_DARK,
    PERGAMENT, LEDER,
    FACTION_ADAM, FACTION_SKELETOR, FACTION_HORDAK, FACTION_ZODAK,
)
from interfaces.renderer.pygame.components.button import HexButton, draw_raised_effects


class Museum:
    """
    Ausstellungsraum mit Galerie und Exponaten.

    Sub-Views:
      gallery       – Übersicht aller Exponate
      exhibit_4000  – Button 4000 Detail-Ansicht
    """

    def __init__(self, screen, screen_width: int, screen_height: int, **kwargs):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._view = "gallery"

        self._font_title  = pygame.font.SysFont(FONT_FAMILY, 36, bold=True)
        self._font_header = pygame.font.SysFont(FONT_FAMILY, 22, bold=True)
        self._font_label  = pygame.font.SysFont(FONT_FAMILY, 15)
        self._font_small  = pygame.font.SysFont(FONT_FAMILY, 13)

        self._init_gallery()
        self._init_exhibit_4000()

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------

    def _init_gallery(self):
        self._tile_4000 = HexButton(
            x=540, y=295,
            size=100,
            color=PERGAMENT["field"],
            text="4000",
            highlight_color=PERGAMENT["highlight"],
            text_color=TEXT_DARK,
            callback=self._open_exhibit_4000,
            font_size=28,
        )

    def _init_exhibit_4000(self):
        factions = ["Adam", "Skeletor", "Hordak", "Zodak"]
        colors = [
            FACTION_ADAM["primary"],
            FACTION_SKELETOR["primary"],
            FACTION_HORDAK["primary"],
            FACTION_ZODAK["primary"],
        ]

        # Zurück-Button (oben links im Header)
        self._back_button = HexButton(
            x=15, y=15, size=48,
            color=LEDER["field"],
            text="←",
            callback=self._close_exhibit,
            text_color=TEXT_LIGHT,
            font_size=22,
            angle_offset=30,
            alpha=220,
        )

        # Schaukasten-Grid: 4 Fraktionen × 4 Zustände
        # Spalten-Zentren: 440, 540, 640, 740  → top-left (size=80): 400, 500, 600, 700
        col_x  = [400, 500, 600, 700]
        row_y  = [108, 208, 308, 408]
        states = [
            (False, False, False),   # Normal
            (True,  False, False),   # Hover  (statisch – kein handle_event)
            (False, True,  False),   # Selektiert
            (False, False, True),    # Deaktiviert
        ]

        self._showcase_buttons = []
        for row_idx, (is_hl, is_sel, is_dis) in enumerate(states):
            for col_idx, faction in enumerate(factions):
                btn = HexButton(
                    x=col_x[col_idx],
                    y=row_y[row_idx],
                    size=80,
                    color=colors[col_idx],
                    faction=faction,
                    text_color=TEXT_LIGHT,
                    font_size=16,
                )
                btn.is_highlighted = is_hl
                btn.is_selected    = is_sel
                btn.is_disabled    = is_dis
                self._showcase_buttons.append(btn)

        # Interaktive Reihe (size=60, gleiche Spalten-Zentren)
        col_x_inter = [410, 510, 610, 710]   # center_x - 30 für size=60
        self._interactive_buttons = []
        for i, (faction, color) in enumerate(zip(factions, colors)):
            btn = HexButton(
                x=col_x_inter[i],
                y=530,
                size=60,
                color=color,
                faction=faction,
                text_color=TEXT_LIGHT,
                font_size=14,
            )
            self._interactive_buttons.append(btn)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _open_exhibit_4000(self):
        self._view = "exhibit_4000"

    def _close_exhibit(self):
        self._view = "gallery"

    # ------------------------------------------------------------------
    # Public interface (wird von App aufgerufen)
    # ------------------------------------------------------------------

    def handle_event(self, event: pygame.event.Event):
        if self._view == "gallery":
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

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render_gallery(self):
        w = self.screen_width

        # Header-Balken
        pygame.draw.rect(self.screen, (22, 16, 10), (0, 0, w, 78))
        pygame.draw.line(self.screen, (80, 58, 36), (0, 78), (w, 78), 1)

        title = self._font_title.render("MUSEUM", True, TEXT_HIGHLIGHT)
        self.screen.blit(title, (30, 20))

        sub = self._font_small.render("Ausstellungsraum", True, TEXT_LIGHT)
        self.screen.blit(sub, (30, 54))

        pygame.draw.line(self.screen, (60, 45, 28), (20, 108), (w - 80, 108), 1)

        # Exponat-Kachel
        draw_raised_effects(self.screen, [self._tile_4000])
        self._tile_4000.render(self.screen)

        # Label unter der Kachel
        lbl = self._font_label.render("HexButton  —  Design-Referenz", True, TEXT_HIGHLIGHT)
        lbl_rect = lbl.get_rect(centerx=590, y=408)
        self.screen.blit(lbl, lbl_rect)

        hint = self._font_small.render("Klicken zum Erkunden", True, TEXT_LIGHT)
        hint_rect = hint.get_rect(centerx=590, y=430)
        self.screen.blit(hint, hint_rect)

    def _render_exhibit_4000(self):
        w = self.screen_width

        # Header-Balken
        pygame.draw.rect(self.screen, (22, 16, 10), (0, 0, w, 78))
        pygame.draw.line(self.screen, (80, 58, 36), (0, 78), (w, 78), 1)

        # Zurück-Button
        draw_raised_effects(self.screen, [self._back_button])
        self._back_button.render(self.screen)

        # ID-Badge + Titel
        badge = self._font_header.render("4000", True, TEXT_HIGHLIGHT)
        self.screen.blit(badge, (75, 22))

        title = self._font_header.render("HexButton  —  Design-Referenz", True, TEXT_LIGHT)
        self.screen.blit(title, (130, 22))

        # Fraktions-Spaltenköpfe
        factions    = ["Adam", "Skeletor", "Hordak", "Zodak"]
        col_centers = [440, 540, 640, 740]
        for i, faction in enumerate(factions):
            lbl = self._font_label.render(faction, True, TEXT_LIGHT)
            lbl_rect = lbl.get_rect(centerx=col_centers[i], y=83)
            self.screen.blit(lbl, lbl_rect)

        # Zustand-Zeilenbeschriftung
        state_names   = ["Normal", "Hover", "Selektiert", "Deaktiviert"]
        row_centers_y = [148, 248, 348, 448]
        for i, name in enumerate(state_names):
            lbl = self._font_label.render(name, True, TEXT_LIGHT)
            lbl_rect = lbl.get_rect(right=390, centery=row_centers_y[i])
            self.screen.blit(lbl, lbl_rect)

        # Schaukasten-Grid (statisch)
        draw_raised_effects(self.screen, self._showcase_buttons)
        for btn in self._showcase_buttons:
            btn.render(self.screen)

        # Trennlinie + Interaktiv-Label
        sep_y = 508
        pygame.draw.line(self.screen, (60, 45, 30), (20, sep_y), (1180, sep_y), 1)
        sep_lbl = self._font_label.render("Interaktiv  —  Hover & Klick", True, TEXT_HIGHLIGHT)
        self.screen.blit(sep_lbl, (20, sep_y + 8))

        # Interaktive Reihe
        draw_raised_effects(self.screen, self._interactive_buttons)
        for btn in self._interactive_buttons:
            btn.render(self.screen)
