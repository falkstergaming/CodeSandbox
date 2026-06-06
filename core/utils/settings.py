"""
Settings-Modul für CodeSandbox.
Verwaltet Spracheinstellungen und Audio-Einstellungen.
Übernommen aus Assault.
"""

import configparser
import os
from typing import Dict, Any

DEFAULT_SETTINGS = {
    "language": "en",
    "music_volume": 100,
    "effect_volume": 100,
    "music_enabled": True,
    "jukebox_folder": "",
}


class Settings:
    """
    Verwaltet die Anwendungs-Einstellungen.

    Einstellungen:
    - language: "de" oder "en"
    - music_volume: 0-100 (Integer)
    - effect_volume: 0-100 (Integer)
    - music_enabled: True/False
    """

    def __init__(self, settings_file: str = "settings.ini"):
        self.settings_file = settings_file
        self._settings: Dict[str, Any] = DEFAULT_SETTINGS.copy()
        self._load()

    def _load(self) -> None:
        config = configparser.ConfigParser()
        config["Language"] = {"lang": self._settings["language"]}
        config["Audio"] = {
            "music_volume": str(self._settings["music_volume"]),
            "effect_volume": str(self._settings["effect_volume"]),
            "music_enabled": str(self._settings["music_enabled"])
        }
        config["Jukebox"] = {"folder": self._settings["jukebox_folder"]}
        if os.path.exists(self.settings_file):
            try:
                config.read(self.settings_file, encoding='utf-8')
                if "Language" in config and "lang" in config["Language"]:
                    self._settings["language"] = config["Language"]["lang"]
                if "Audio" in config:
                    if "music_volume" in config["Audio"]:
                        self._settings["music_volume"] = int(config["Audio"]["music_volume"])
                    if "effect_volume" in config["Audio"]:
                        self._settings["effect_volume"] = int(config["Audio"]["effect_volume"])
                    if "music_enabled" in config["Audio"]:
                        self._settings["music_enabled"] = config["Audio"].getboolean("music_enabled")
                if "Jukebox" in config and "folder" in config["Jukebox"]:
                    self._settings["jukebox_folder"] = config["Jukebox"]["folder"]
            except Exception as e:
                print(f"[WARNING] Fehler beim Laden der Settings: {e}")
        else:
            self._save()

    def _save(self) -> None:
        config = configparser.ConfigParser()
        config["Language"] = {"lang": self._settings["language"]}
        config["Audio"] = {
            "music_volume": str(self._settings["music_volume"]),
            "effect_volume": str(self._settings["effect_volume"]),
            "music_enabled": str(self._settings["music_enabled"])
        }
        config["Jukebox"] = {"folder": self._settings["jukebox_folder"]}
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                config.write(f)
        except Exception as e:
            print(f"[WARNING] Fehler beim Speichern der Settings: {e}")

    def save(self) -> None:
        self._save()

    @property
    def language(self) -> str:
        return self._settings["language"]

    @language.setter
    def language(self, value: str) -> None:
        if value in ["de", "en"]:
            self._settings["language"] = value
            self._save()

    @property
    def music_volume(self) -> int:
        return self._settings["music_volume"]

    @music_volume.setter
    def music_volume(self, value: int) -> None:
        self._settings["music_volume"] = max(0, min(100, value))
        self._save()

    @property
    def effect_volume(self) -> int:
        return self._settings["effect_volume"]

    @effect_volume.setter
    def effect_volume(self, value: int) -> None:
        self._settings["effect_volume"] = max(0, min(100, value))
        self._save()

    @property
    def music_enabled(self) -> bool:
        return self._settings["music_enabled"]

    @music_enabled.setter
    def music_enabled(self, value: bool) -> None:
        self._settings["music_enabled"] = value
        self._save()

    @property
    def jukebox_folder(self) -> str:
        return self._settings["jukebox_folder"]

    @jukebox_folder.setter
    def jukebox_folder(self, value: str) -> None:
        self._settings["jukebox_folder"] = value or ""
        self._save()

    def get_all(self) -> Dict[str, Any]:
        return self._settings.copy()
