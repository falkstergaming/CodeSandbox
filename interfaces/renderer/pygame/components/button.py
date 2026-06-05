"""
Button-Klasse für hexagonale Buttons.
1:1 übernommen aus Sturm auf Grayskull.

- Board-Hexfelder: Groß (size=80) für das Spielfeld.
- Action-Button: Mittel (size=60), rechts am Rand, mittig (für Modus-Wechsel).
- Settings-Button: Mittel (size=60), oben rechts im Eck.
- BoardButton: Vorbereitung für Hexfelder des Spielfelds (interaktiv).

FARBKONZEPT:
- normal: Primary-Farbe
- highlighted: Highlight-Farbe (Mouseover)
- selected: Selected-Farbe (ausgewählt)
- disabled: Disabled-Farbe (deaktiviert)
"""

from math import cos, sin, pi
from typing import List, Tuple, Optional, Callable, Iterable
import pygame

from core.utils.global_constants import (
    FONT_FAMILY,
    FONT_SYMBOL,
    COLORS
)
from core.utils.colors import (
    TEXT_LIGHT,
    TEXT_HIGHLIGHT,
    TEXT_DARK,
    FACTION_COLORS,
    BUTTON_OCCUPIED,
    BUTTON_HIGHLIGHTED,
    BUTTON_SELECTED,
    BUTTON_DISABLED,
    BUTTON_MIDTONE,
    BUTTON_OVERTONE,
)


def draw_raised_effects(
    surface: pygame.Surface,
    buttons: Iterable,
    shadow_shift: int = 2,
    bevel_outset: int = 2,
) -> None:
    """
    Zeichnet Schlagschatten und äußere Bevel-Linien für eine Menge HexButtons.

    Die Effekte liegen AUSSERHALB der Polygon-Grenzen der Buttons und sind
    kein Bestandteil der jeweiligen Hitboxen. Muss VOR dem eigentlichen
    Rendern der Buttons aufgerufen werden.
    """
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

    for button in buttons:
        pts = button.points
        n = len(pts)

        shadow_pts = [(int(p[0] + shadow_shift), int(p[1] + shadow_shift)) for p in pts]
        pygame.draw.polygon(overlay, (0, 0, 0, 55), shadow_pts)

        for i in range(n):
            p1 = pts[i]
            p2 = pts[(i + 1) % n]
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]

            length = (dx * dx + dy * dy) ** 0.5
            if length < 0.001:
                continue

            shift_x = dy / length * bevel_outset
            shift_y = -dx / length * bevel_outset

            op1 = (int(p1[0] + shift_x), int(p1[1] + shift_y))
            op2 = (int(p2[0] + shift_x), int(p2[1] + shift_y))

            ny_norm = -dx / length

            if ny_norm < 0:
                pygame.draw.line(overlay, (255, 255, 255, 100), op1, op2, 2)
            else:
                pygame.draw.line(overlay, (0, 0, 0, 80), op1, op2, 2)

    surface.blit(overlay, (0, 0))


class HexButton:
    """
    Basis-Klasse für ALLE hexagonalen Buttons.
    1:1 übernommen aus Sturm auf Grayskull.

    - Präzise Kollisionserkennung (Point-in-Polygon).
    - Highlighting bei Mausüberfahrt.
    - Text und Symbol-Unterstützung.
    - Callback-Funktion bei Klick.
    - Unterstützt 4 States: normal, highlighted, selected, disabled
    """

    STATE_NORMAL      = "normal"
    STATE_HIGHLIGHTED = "highlighted"
    STATE_OVERTONE    = "overtone"
    STATE_MIDTONE     = "midtone"
    STATE_SELECTED    = "selected"
    STATE_DISABLED    = "disabled"

    def __init__(
        self,
        x: int,
        y: int,
        size: int,
        color: tuple,
        text: str = "",
        hex_id: Optional[str] = None,
        callback: Optional[Callable] = None,
        highlight_color: Optional[tuple] = None,
        highlight_text_color: Optional[tuple] = None,
        symbol: Optional[pygame.Surface] = None,
        text_color: tuple = TEXT_DARK,
        font_size: int = 20,
        font_family: Optional[str] = None,
        use_symbol_font: bool = False,
        faction: Optional[str] = None,
        state: str = STATE_NORMAL,
        is_setter: bool = False,
        setter_delay_ms: int = 200,
        angle_offset: float = 0,
        bold: bool = False,
        alpha: int = 255,
    ):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.text = text
        self.hex_id = hex_id
        self.callback = callback
        self.symbol = symbol
        self.text_color = text_color
        self.highlight_color = highlight_color
        self.highlight_text_color = highlight_text_color
        self.faction = faction
        self.angle_offset = angle_offset
        self.alpha = alpha

        self.is_setter = is_setter
        self.setter_delay_ms = setter_delay_ms
        self._reset_at_ms: Optional[int] = None

        if use_symbol_font or (text and any(ord(c) > 127 for c in text)):
            _font_name = FONT_SYMBOL[0] if isinstance(FONT_SYMBOL, tuple) else FONT_SYMBOL
            self.font = pygame.font.SysFont(_font_name, font_size, bold=bold)
        else:
            self.font = pygame.font.SysFont(font_family or FONT_FAMILY, font_size, bold=bold)

        self._state = state
        self.is_highlighted = False
        self.is_selected = False
        self.is_disabled = (state == self.STATE_DISABLED)
        self.is_pressed = False
        self._visually_disabled = False
        self._visually_midtone = False
        self._visually_overtone = False

        self.center_x = x + size / 2
        self.center_y = y + size / 2
        self.points = self._calculate_hex_points()

    @property
    def state(self) -> str:
        return self._state

    @state.setter
    def state(self, value: str) -> None:
        self._state = value
        self.is_disabled = (value == self.STATE_DISABLED)
        self.is_selected = (value == self.STATE_SELECTED)
        self.is_highlighted = (value == self.STATE_HIGHLIGHTED)

    def _calculate_hex_points(self) -> List[Tuple[float, float]]:
        points = []
        for i in range(6):
            angle_deg = 60 * i + self.angle_offset
            angle_rad = pi / 180 * angle_deg
            point_x = self.center_x + self.size / 2 * cos(angle_rad)
            point_y = self.center_y + self.size / 2 * sin(angle_rad)
            points.append((point_x, point_y))
        return points

    def _lighten_color(self, color: tuple, factor: int = 30) -> tuple:
        r, g, b = color
        return (min(255, r + factor), min(255, g + factor), min(255, b + factor))

    def _darken_color(self, color: tuple, factor: int = 30) -> tuple:
        r, g, b = color
        return (max(0, r - factor), max(0, g - factor), max(0, b - factor))

    def get_color_for_state(self, state: Optional[str] = None) -> tuple:
        if state is None:
            state = self.state
        if self.faction and self.faction in FACTION_COLORS:
            faction_colors = FACTION_COLORS[self.faction]
            if state == self.STATE_NORMAL:
                return faction_colors.get("primary", self.color)
            elif state == self.STATE_HIGHLIGHTED:
                return faction_colors.get("highlight", self._lighten_color(self.color, 30))
            elif state == self.STATE_OVERTONE:
                return faction_colors.get("overtone", self._darken_color(self.color, 20))
            elif state == self.STATE_MIDTONE:
                return faction_colors.get("midtone", self._lighten_color(self.color, 50))
            elif state == self.STATE_SELECTED:
                return faction_colors.get("selected", self._lighten_color(self.color, 60))
            elif state == self.STATE_DISABLED:
                return faction_colors.get("disabled", self._lighten_color(self.color, 90))
        if state == self.STATE_NORMAL:
            return self.color
        elif state == self.STATE_HIGHLIGHTED:
            return self.highlight_color if self.highlight_color else self._lighten_color(self.color, 30)
        elif state == self.STATE_OVERTONE:
            return self._darken_color(self.color, 20)
        elif state == self.STATE_MIDTONE:
            return self._lighten_color(self.color, 50)
        elif state == self.STATE_SELECTED:
            return self._lighten_color(self.color, 40)
        elif state == self.STATE_DISABLED:
            return self._lighten_color(self.color, 90)
        return self.color

    def get_frame_color_for_state(self, state: Optional[str] = None) -> tuple:
        if state is None:
            state = self.state
        if self.faction:
            if state == self.STATE_NORMAL:
                if self.faction in BUTTON_OCCUPIED:
                    return BUTTON_OCCUPIED[self.faction].get("frame", COLORS["text"])
            elif state == self.STATE_HIGHLIGHTED:
                if self.faction in BUTTON_HIGHLIGHTED:
                    return BUTTON_HIGHLIGHTED[self.faction].get("frame", COLORS["highlight"])
            elif state == self.STATE_OVERTONE:
                if self.faction in BUTTON_OVERTONE:
                    return BUTTON_OVERTONE[self.faction].get("frame", COLORS["text"])
            elif state == self.STATE_MIDTONE:
                if self.faction in BUTTON_MIDTONE:
                    return BUTTON_MIDTONE[self.faction].get("frame", COLORS["text"])
            elif state == self.STATE_SELECTED:
                if self.faction in BUTTON_SELECTED:
                    return BUTTON_SELECTED[self.faction].get("frame", COLORS["highlight"])
            elif state == self.STATE_DISABLED:
                if self.faction in BUTTON_DISABLED:
                    return BUTTON_DISABLED[self.faction].get("frame", COLORS["text"])
        if state == self.STATE_DISABLED:
            return COLORS["text"]
        return COLORS["text"]

    def get_text_color_for_state(self, state: Optional[str] = None) -> tuple:
        if state is None:
            state = self.state
        if self.faction:
            if state == self.STATE_NORMAL:
                if self.faction in BUTTON_OCCUPIED:
                    return BUTTON_OCCUPIED[self.faction].get("text", TEXT_LIGHT)
            elif state == self.STATE_HIGHLIGHTED:
                if self.faction in BUTTON_HIGHLIGHTED:
                    return BUTTON_HIGHLIGHTED[self.faction].get("text", TEXT_HIGHLIGHT)
            elif state == self.STATE_OVERTONE:
                if self.faction in BUTTON_OVERTONE:
                    return BUTTON_OVERTONE[self.faction].get("text", TEXT_LIGHT)
            elif state == self.STATE_MIDTONE:
                if self.faction in BUTTON_MIDTONE:
                    return BUTTON_MIDTONE[self.faction].get("text", TEXT_DARK)
            elif state == self.STATE_SELECTED:
                if self.faction in BUTTON_SELECTED:
                    return BUTTON_SELECTED[self.faction].get("text", TEXT_HIGHLIGHT)
            elif state == self.STATE_DISABLED:
                if self.faction in BUTTON_DISABLED:
                    return BUTTON_DISABLED[self.faction].get("text", TEXT_DARK)
        if state == self.STATE_DISABLED:
            return TEXT_DARK
        elif state == self.STATE_HIGHLIGHTED:
            return self.highlight_text_color if self.highlight_text_color else TEXT_HIGHLIGHT
        elif state == self.STATE_SELECTED:
            return TEXT_HIGHLIGHT
        return self.text_color

    def point_in_polygon(self, point: Tuple[float, float]) -> bool:
        x, y = point
        inside = False
        j = len(self.points) - 1
        for i in range(len(self.points)):
            if ((self.points[i][1] > y) != (self.points[j][1] > y) and
                x < (self.points[j][0] - self.points[i][0]) * (y - self.points[i][1]) /
                    (self.points[j][1] - self.points[i][1]) + self.points[i][0]):
                inside = not inside
            j = i
        return inside

    def handle_event(self, event: pygame.event.Event) -> bool:
        if self.is_disabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_highlighted = self.point_in_polygon(event.pos)
            if self._reset_at_ms is None:
                if self.is_highlighted and not self.is_selected:
                    self._state = self.STATE_HIGHLIGHTED
                elif not self.is_highlighted and not self.is_selected:
                    self._state = self.STATE_NORMAL
            return False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.point_in_polygon(event.pos):
                self.is_pressed = True
                if self.is_setter:
                    self._state = self.STATE_SELECTED
                    self._reset_at_ms = None
                    if self.callback:
                        self.callback()
                else:
                    self.is_selected = not self.is_selected
                    if self.is_selected:
                        self._state = self.STATE_SELECTED
                    else:
                        self._state = self.STATE_HIGHLIGHTED
                    if self.callback:
                        self.callback()
                return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed:
                if self.is_setter:
                    self._reset_at_ms = pygame.time.get_ticks() + self.setter_delay_ms
                else:
                    self.is_pressed = False
                    if not self.is_selected:
                        self._state = self.STATE_HIGHLIGHTED if self.is_highlighted else self.STATE_NORMAL

        return False

    def render(self, surface: pygame.Surface):
        if self.is_setter and self._reset_at_ms is not None:
            if pygame.time.get_ticks() >= self._reset_at_ms:
                self.is_pressed = False
                self._reset_at_ms = None
                self._state = self.STATE_HIGHLIGHTED if self.is_highlighted else self.STATE_NORMAL

        if self.is_disabled:
            effective_state = self.STATE_DISABLED
        elif self.is_selected or (self.is_setter and self.is_pressed):
            effective_state = self.STATE_SELECTED
        elif self.is_highlighted:
            effective_state = self.STATE_HIGHLIGHTED
        elif self._visually_overtone:
            effective_state = self.STATE_OVERTONE
        elif self._visually_midtone:
            effective_state = self.STATE_MIDTONE
        elif self._visually_disabled:
            effective_state = self.STATE_DISABLED
        else:
            effective_state = self.STATE_NORMAL

        fill_color = self.get_color_for_state(effective_state)
        text_color_to_use = self.get_text_color_for_state(effective_state)
        bevel_dark  = self._darken_color(fill_color, 55)
        bevel_light = self._lighten_color(fill_color, 55)
        is_inset = self.is_pressed or effective_state == self.STATE_SELECTED

        margin = 3
        bx = int(self.center_x - self.size / 2) - margin
        by = int(self.center_y - self.size / 2) - margin
        surf = pygame.Surface((self.size + 2 * margin, self.size + 2 * margin), pygame.SRCALPHA)
        lp = [(int(p[0] - bx), int(p[1] - by)) for p in self.points]

        if not is_inset and effective_state != self.STATE_DISABLED:
            pygame.draw.polygon(surf, (0, 0, 0, 80), [(p[0] + 2, p[1] + 2) for p in lp])

        pygame.draw.polygon(surf, (*fill_color, self.alpha), lp)

        n = len(lp)
        for i in range(n):
            p1, p2 = lp[i], lp[(i + 1) % n]
            dx = self.points[(i + 1) % n][0] - self.points[i][0]
            if dx > 1:
                c = bevel_dark if is_inset else bevel_light
                pygame.draw.line(surf, (*c, 200), p1, p2, 2)
            elif dx < -1:
                c = bevel_light if is_inset else bevel_dark
                pygame.draw.line(surf, (*c, 180), p1, p2, 2)

        if effective_state == self.STATE_HIGHLIGHTED:
            pygame.draw.polygon(surf, (*TEXT_HIGHLIGHT, 255), lp, 2)
        elif is_inset:
            pygame.draw.polygon(surf, (*bevel_light, 200), lp, 2)
        elif effective_state == self.STATE_DISABLED:
            pygame.draw.polygon(surf, (*bevel_dark, 120), lp, 1)

        surface.blit(surf, (bx, by))

        if self.symbol:
            symbol_rect = self.symbol.get_rect(center=(self.center_x, self.center_y - 10))
            surface.blit(self.symbol, symbol_rect)

        if self.text:
            lines = self.text.split('\n')
            if len(lines) == 1:
                text_surface = self.font.render(self.text, True, text_color_to_use)
                text_rect = text_surface.get_rect(center=(self.center_x, self.center_y))
                surface.blit(text_surface, text_rect)
            else:
                y_offset = -6
                for line in lines:
                    text_surface = self.font.render(line, True, text_color_to_use)
                    text_rect = text_surface.get_rect(center=(self.center_x, self.center_y + y_offset))
                    surface.blit(text_surface, text_rect)
                    y_offset += 12

    def set_disabled(self, disabled: bool) -> None:
        self.is_disabled = disabled
        if disabled:
            self._state = self.STATE_DISABLED
            self.is_highlighted = False
            self.is_selected = False
        else:
            self._state = self.STATE_NORMAL

    def set_faction(self, faction: str) -> None:
        self.faction = faction
