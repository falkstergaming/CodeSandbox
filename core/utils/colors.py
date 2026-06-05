"""
Alle Farbkonstanten für CodeSandbox.
1:1 übernommen aus Sturm auf Grayskull.
"""

# =============================================================================
# UNIVERSELLE SCHRIFTFARBEN
# =============================================================================

TEXT_LIGHT = (243, 230, 193)
TEXT_HIGHLIGHT = (255, 227, 106)
TEXT_DARK = (59, 46, 30)
TEXT_DARK_SECONDARY = (88, 69, 45)

# =============================================================================
# NEUTRALE FARBEN (Header, Textkonsole, 60er Hexfelder rechts am Rand)
# =============================================================================

PERGAMENT = {
    "field": (230, 215, 184),
    "highlight": (241, 231, 205),
    "frame": (154, 128, 90),
    "text": (59, 46, 30)
}

LEDER = {
    "field": (90, 65, 46),
    "highlight": (120, 90, 65),
    "frame": (52, 36, 24),
    "text": (243, 230, 193)
}

# =============================================================================
# FACTION-FARBEN
# =============================================================================

FACTION_ADAM = {
    "overtone": (28, 56, 35),
    "primary": (47, 94, 58),
    "highlight": (68, 130, 78),
    "midtone": (110, 146, 110),
    "selected": (174, 199, 163),
    "disabled": (211, 223, 205)
}

FACTION_SKELETOR = {
    "overtone": (54, 37, 73),
    "primary": (90, 61, 122),
    "highlight": (129, 82, 171),
    "midtone": (142, 117, 165),
    "selected": (195, 174, 208),
    "disabled": (225, 217, 231)
}

FACTION_HORDAK = {
    "overtone": (83, 18, 21),
    "primary": (139, 30, 35),
    "highlight": (182, 48, 52),
    "midtone": (176, 97, 97),
    "selected": (214, 164, 160),
    "disabled": (231, 214, 211)
}

FACTION_ZODAK = {
    "overtone": (118, 64, 16),
    "primary": (196, 106, 26),
    "highlight": (233, 140, 39),
    "midtone": (210, 148, 87),
    "selected": (224, 191, 148),
    "disabled": (236, 226, 214)
}

FACTION_COLORS = {
    "Adam": FACTION_ADAM,
    "Skeletor": FACTION_SKELETOR,
    "Hordak": FACTION_HORDAK,
    "Zodak": FACTION_ZODAK
}

# =============================================================================
# BUTTON STATES
# =============================================================================

BUTTON_OCCUPIED = {
    "Adam":     {"field": (47, 94, 58),    "frame": (31, 62, 38),   "text": (243, 230, 193)},
    "Skeletor": {"field": (90, 61, 122),   "frame": (64, 42, 88),   "text": (243, 230, 193)},
    "Hordak":   {"field": (139, 30, 35),   "frame": (97, 18, 23),   "text": (243, 230, 193)},
    "Zodak":    {"field": (196, 106, 26),  "frame": (145, 74, 17),  "text": (243, 230, 193)},
}

BUTTON_HIGHLIGHTED = {
    "Adam":     {"field": (68, 130, 78),   "frame": (104, 176, 117), "text": (255, 227, 106)},
    "Skeletor": {"field": (129, 82, 171),  "frame": (165, 114, 206), "text": (255, 227, 106)},
    "Hordak":   {"field": (182, 48, 52),   "frame": (220, 88, 92),   "text": (255, 227, 106)},
    "Zodak":    {"field": (233, 140, 39),  "frame": (255, 184, 78),  "text": (255, 227, 106)},
}

BUTTON_SELECTED = {
    "Adam":     {"field": (174, 199, 163), "frame": (104, 136, 94),  "text": (255, 227, 106)},
    "Skeletor": {"field": (195, 174, 208), "frame": (136, 111, 150), "text": (255, 227, 106)},
    "Hordak":   {"field": (214, 164, 160), "frame": (155, 101, 98),  "text": (255, 227, 106)},
    "Zodak":    {"field": (224, 191, 148), "frame": (172, 135, 92),  "text": (255, 227, 106)},
}

BUTTON_DISABLED = {
    "Adam":     {"field": (211, 223, 205), "frame": (170, 184, 164), "text": (59, 46, 30)},
    "Skeletor": {"field": (225, 217, 231), "frame": (189, 180, 197), "text": (59, 46, 30)},
    "Hordak":   {"field": (231, 214, 211), "frame": (193, 175, 172), "text": (59, 46, 30)},
    "Zodak":    {"field": (236, 226, 214), "frame": (199, 189, 177), "text": (59, 46, 30)},
}

BUTTON_OVERTONE = {
    "Adam":     {"field": (28, 56, 35),   "frame": (16, 36, 20),  "text": (243, 230, 193)},
    "Skeletor": {"field": (54, 37, 73),   "frame": (32, 20, 46),  "text": (243, 230, 193)},
    "Hordak":   {"field": (83, 18, 21),   "frame": (52, 10, 12),  "text": (243, 230, 193)},
    "Zodak":    {"field": (118, 64, 16),  "frame": (76, 40, 8),   "text": (243, 230, 193)},
}

BUTTON_MIDTONE = {
    "Adam":     {"field": (110, 146, 110), "frame": (73, 98, 73),   "text": (59, 46, 30)},
    "Skeletor": {"field": (142, 117, 165), "frame": (95, 78, 110),  "text": (59, 46, 30)},
    "Hordak":   {"field": (176, 97, 97),   "frame": (118, 65, 65),  "text": (59, 46, 30)},
    "Zodak":    {"field": (210, 148, 87),  "frame": (141, 99, 58),  "text": (59, 46, 30)},
}

# =============================================================================
# VEREINHEITLICHTE FARBKONSTANTEN
# =============================================================================

COLORS = {
    "primary":        PERGAMENT["frame"],
    "secondary":      LEDER["field"],
    "background":     (15, 15, 15),
    "text":           TEXT_DARK,
    "highlight":      TEXT_HIGHLIGHT,
    "idle_player":    (0, 255, 0),
    "idle_opponent":  (255, 0, 0),
    "idle_neutral":   (200, 200, 0),
    "idle":           (255, 215, 0),
}

DARK_BACKGROUND_COLOR = (15, 15, 15)
EMPTY_HEX_COLOR       = LEDER["field"]
NEUTRAL_TEXT_COLOR    = TEXT_DARK

UI_BUTTON_PRIMARY        = LEDER["field"]
UI_BUTTON_TEXT           = TEXT_DARK
UI_BUTTON_HIGHLIGHT      = LEDER["highlight"]
UI_BUTTON_HIGHLIGHT_TEXT = TEXT_DARK

HEX_COLORS = {
    "player_area":      FACTION_ADAM["primary"],
    "opponent_area":    FACTION_SKELETOR["primary"],
    "idle_area":        PERGAMENT["field"],
    "preview_player":   PERGAMENT["field"],
    "preview_opponent": PERGAMENT["field"],
    "empty":            EMPTY_HEX_COLOR,
    "neutral":          PERGAMENT["field"],
}
