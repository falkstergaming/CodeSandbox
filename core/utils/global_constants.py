"""
Globale Konstanten für CodeSandbox.
Basiert auf Assault – game-spezifische Konstanten entfernt.
"""

import os
import sys

from core.utils.colors import (
    TEXT_LIGHT,
    TEXT_HIGHLIGHT,
    TEXT_DARK,
    TEXT_DARK_SECONDARY,
    PERGAMENT,
    LEDER,
    FACTION_ADAM,
    FACTION_SKELETOR,
    FACTION_HORDAK,
    FACTION_ZODAK,
    FACTION_COLORS,
    BUTTON_OCCUPIED,
    BUTTON_HIGHLIGHTED,
    BUTTON_SELECTED,
    BUTTON_DISABLED,
    BUTTON_OVERTONE,
    BUTTON_MIDTONE,
    COLORS,
    DARK_BACKGROUND_COLOR,
    EMPTY_HEX_COLOR,
    NEUTRAL_TEXT_COLOR,
    UI_BUTTON_PRIMARY,
    UI_BUTTON_TEXT,
    UI_BUTTON_HIGHLIGHT,
    UI_BUTTON_HIGHLIGHT_TEXT,
    HEX_COLORS,
    # CodeSandbox Farbkonzept
    GRAU,
    SILBER,
    GOLD,
    BRONZE,
    PALETTE,
)

# =============================================================================
# WINDOW
# =============================================================================
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 800

# =============================================================================
# FONTS
# =============================================================================
FONT_FAMILY      = "Eurostile"
FONT_SYMBOL      = ("Segoe UI Symbol", 16)
FONT_TITLE       = (FONT_FAMILY, 24)
FONT_BODY        = (FONT_FAMILY, 16)
FONT_CONSOLE     = (FONT_FAMILY, 16)
FONT_DESCRIPTION = (FONT_FAMILY, 14)

# =============================================================================
# HEXFELD-GEOMETRIE
# =============================================================================
HEX_SIZE    = {"width": 80, "height": 80}
HEX_SPACING = 10

# =============================================================================
# CONSOLE SYMBOLE
# =============================================================================
CONSOLE_SYMBOLS = {
    "info":      "ℹ",   # Hinweis / allgemeine Info
    "warning":   "⚠",   # Warnung / nicht möglich
    "success":   "✓",   # Bestätigung / Erfolg
    "error":     "✗",   # Fehler
    "highlight": "⚡",  # Hervorhebung / Ereignis
    "phase":     "▶",   # Phasen- / Statusübergang
}

# =============================================================================
# FACTIONS
# =============================================================================
FACTIONS = ["Adam", "Skeletor", "Hordak", "Zodak"]

FACTION_SYMBOLS = {
    "Adam":     "🌹",
    "Skeletor": "☠️",
    "Hordak":   "🦇",
    "Zodak":    "⚖️",
}
