"""
Zentrale Übersetzungen für CodeSandbox.
Basiert auf Sturm auf Grayskull – angepasst für CodeSandbox.
"""

from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        # Titel
        "app_title":      "Code Sandbox",
        "game_title":     "Code Sandbox",
        "stats_title":    "Prototype",

        # Modi
        "mode":           "Mode",
        "mode_sandbox":   "Sandbox",
        "mode_museum":    "Museum",
        "mode_lab":       "Lab",
        "mode_proto":     "Prototype",

        # Allgemein
        "back":           "Back",
        "close":          "Close",
        "coming_soon":    "Coming Soon",

        # Buttons
        "action":         "Action",
        "settings":       "Settings",

        # Settings-Menü
        "language":       "Language",
        "music_volume":   "Music Volume",
        "effect_volume":  "Effect Volume",
        "german":         "German",
        "english":        "English",
    },
    "de": {
        # Titel
        "app_title":      "Sandkasten",
        "game_title":     "Sandkasten",
        "stats_title":    "Prototyp",

        # Modi
        "mode":           "Modus",
        "mode_sandbox":   "Sandbox",
        "mode_museum":    "Museum",
        "mode_lab":       "Labor",
        "mode_proto":     "Prototyp",

        # Allgemein
        "back":           "Zurück",
        "close":          "Schließen",
        "coming_soon":    "Kommt bald",

        # Buttons
        "action":         "Aktion",
        "settings":       "Einstellungen",

        # Settings-Menü
        "language":       "Sprache",
        "music_volume":   "Musik-Lautstärke",
        "effect_volume":  "Effekt-Lautstärke",
        "german":         "Deutsch",
        "english":        "Englisch",
    }
}


def get_translation(key: str, lang: str = "en") -> str:
    """Gibt die Übersetzung für einen Schlüssel zurück."""
    return TRANSLATIONS.get(lang, {}).get(key, key)
