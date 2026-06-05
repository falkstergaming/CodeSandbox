"""
Alle Farbkonstanten für CodeSandbox.
1:1 übernommen aus Sturm auf Grayskull.
Ergänzt: CodeSandbox Farbkonzept (GRAU / SILBER / GOLD / BRONZE).
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

# =============================================================================
# CODESANDBOX FARBKONZEPT  (Quelle: Farbkonzept_CodeSandbox.PNG)
# Dunkles Arbeitsumfeld – vier Farbfamilien, je 5 Tonstufen
#
#   overtone  — tiefste Stufe  (Schatten, tiefer Hintergrund)
#   hightone  — dunkle Stufe  (dunkle Fläche, Kontur)
#   midtone   — Hauptton      (primärer Akzent / Füllfläche)
#   halftone  — helle Stufe   (Sekundärfläche, hover)
#   lowtone   — hellste Stufe (Highlight, Text auf Dunkel, heller BG)
# =============================================================================

GRAU = {
    "overtone": ( 31,  33,  41),   # #1F2129  tiefster Hintergrund
    "hightone": ( 44,  50,  64),   # #2C3240  dunkle Fläche
    "midtone":  ( 75,  83, 100),   # #4B5364  mittlerer Grauton
    "halftone": (150, 162, 180),   # #96A2B4  heller Sekundärton
    "lowtone":  (220, 225, 234),   # #DCE1EA  heller Hintergrund
}

SILBER = {
    "overtone": ( 17,  46,  63),   # #112E3F  tiefster Petrol
    "hightone": ( 34,  96, 112),   # #226070  dunkler Akzent
    "midtone":  ( 54, 153, 168),   # #3699A8  Hauptakzent Petrol
    "halftone": (146, 205, 214),   # #92CDD6  heller Petrol
    "lowtone":  (224, 241, 244),   # #E0F1F4  sehr heller Petrol
}

GOLD = {
    "overtone": ( 40,  28,   0),   # #281C00  tiefstes Gold
    "hightone": ( 90,  61,   0),   # #5A3D00  dunkles Gold
    "midtone":  (163, 120,   0),   # #A37800  Hauptgold
    "halftone": (222, 192, 104),   # #DEC068  helles Gold
    "lowtone":  (248, 240, 214),   # #F8F0D6  sehr helles Gold / Crème
}

BRONZE = {
    "overtone": ( 40,  22,   0),   # #281600  tiefstes Bronze
    "hightone": ( 92,  50,   0),   # #5C3200  dunkles Bronze
    "midtone":  (158,  96,  32),   # #9E6020  Hauptbronze
    "halftone": (212, 160, 104),   # #D4A068  helles Bronze
    "lowtone":  (244, 226, 206),   # #F4E2CE  sehr helles Bronze / Crème
}

PALETTE = {
    "grau":   GRAU,
    "silber": SILBER,
    "gold":   GOLD,
    "bronze": BRONZE,
}
