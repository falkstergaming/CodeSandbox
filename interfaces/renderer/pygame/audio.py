"""
AudioManager - Faction-Soundscapes mit 3-Sekunden-Überblende und Titelmusik.
Übernommen aus Assault.

Übergänge:
- Faction gewählt (keine Musik aktiv): 3 s Wartezeit, dann 1.5 s Fade-In
- Faction gewechselt (Musik aktiv):    1.5 s Fade-Out → 1.5 s Fade-In
- Match beendet:                       1.5 s Fade-Out → 1.5 s Fade-In (Titelmusik)

Hinweis: MP3-Dateien müssen manuell in den media/-Ordner kopiert werden.
"""

import random
import pygame
from pathlib import Path
from typing import Optional


FACTION_TO_SOUNDSCAPE = {
    "Adam":     "good",
    "Skeletor": "evil",
    "Hordak":   "horde",
    "Zodak":    "neutral",
}

SOUNDSCAPE_FILES = {
    "good":    "Soundscape good - Assault OST - DeutscherSchmutz.mp3",
    "evil":    "Soundscape evil - Assault OST - DeutscherSchmutz.mp3",
    "horde":   "Soundscape horde - Assault OST - DeutscherSchmutz.mp3",
    "neutral": "Soundscape neutral - Assault OST - DeutscherSchmutz.mp3",
}

TITLE_MUSIC_FILE = "Assault Opening Theme - Assault OST - DeutscherSchmutz.mp3"


class AudioManager:
    """
    Verwaltet Faction-Soundscapes und Titelmusik mit Fade-In/Fade-Out-Überblenden.

    Zustände:
      IDLE       – keine Musik aktiv
      PENDING    – Faction gewählt, 3 s Wartezeit vor Fade-In
      FADING_IN  – Lautstärke blendet über 1.5 s auf Ziel-Volume ein
      PLAYING    – Musik läuft in Dauerschleife
      FADING_OUT – Musik blendet über 1.5 s aus; pending_path wartet
    """

    INITIAL_DELAY    = 3.0
    FADE_IN_DURATION = 1.5
    FADE_OUT_MS      = 1500

    _STATE_IDLE       = "idle"
    _STATE_PENDING    = "pending"
    _STATE_FADING_IN  = "fading_in"
    _STATE_PLAYING    = "playing"
    _STATE_FADING_OUT = "fading_out"

    def __init__(
        self,
        media_dir: str = "media",
        settings=None,
    ) -> None:
        self._media_dir    = Path(media_dir)
        self._settings     = settings

        self._state              = self._STATE_IDLE
        self._current_path: Optional[Path] = None
        self._pending_path: Optional[Path] = None
        self._timer              = 0.0
        self._target_volume      = 0.5

        self._neutral_key: str = random.choice(list(SOUNDSCAPE_FILES.keys()))

        if not pygame.mixer.get_init():
            pygame.mixer.init()

    def set_faction(self, faction_name: Optional[str]) -> None:
        if not faction_name:
            return
        key  = FACTION_TO_SOUNDSCAPE.get(faction_name)
        path = self._media_dir / SOUNDSCAPE_FILES.get(key or "", "")
        if not path.exists():
            return
        self._request_track(path, initial_delay=(self._state == self._STATE_IDLE))

    def play_neutral(self) -> None:
        path = self._media_dir / SOUNDSCAPE_FILES[self._neutral_key]
        if not path.exists():
            return
        self._request_track(path, initial_delay=(self._state == self._STATE_IDLE))

    def play_title(self) -> None:
        path = self._media_dir / TITLE_MUSIC_FILE
        if not path.exists():
            return
        self._request_track(path, initial_delay=False)

    def play_welcome(self) -> None:
        path = self._media_dir / TITLE_MUSIC_FILE
        if not path.exists():
            return
        self._request_track(path, initial_delay=True)

    def update(self, dt: float) -> None:
        if self._state == self._STATE_IDLE:
            return

        elif self._state == self._STATE_PENDING:
            self._timer -= dt
            if self._timer <= 0.0:
                self._begin_fade_in(self._pending_path)

        elif self._state == self._STATE_FADING_IN:
            self._timer -= dt
            elapsed = self.FADE_IN_DURATION - max(0.0, self._timer)
            progress = elapsed / self.FADE_IN_DURATION
            pygame.mixer.music.set_volume(progress * self._target_volume)
            if self._timer <= 0.0:
                pygame.mixer.music.set_volume(self._target_volume)
                self._state = self._STATE_PLAYING

        elif self._state == self._STATE_FADING_OUT:
            if not pygame.mixer.music.get_busy():
                if self._pending_path:
                    self._begin_fade_in(self._pending_path)
                else:
                    self._state        = self._STATE_IDLE
                    self._current_path = None

        elif self._state == self._STATE_PLAYING:
            new_vol = self._get_volume()
            if abs(new_vol - self._target_volume) > 0.005:
                self._target_volume = new_vol
                pygame.mixer.music.set_volume(new_vol)

    def stop(self) -> None:
        pygame.mixer.music.stop()
        self._state        = self._STATE_IDLE
        self._current_path = None
        self._pending_path = None

    def _request_track(self, path: Path, initial_delay: bool = False) -> None:
        if self._state == self._STATE_IDLE:
            self._pending_path = path
            if initial_delay:
                self._timer = self.INITIAL_DELAY
                self._state = self._STATE_PENDING
            else:
                self._begin_fade_in(path)

        elif self._state == self._STATE_PENDING:
            self._pending_path = path
            if initial_delay:
                self._timer = self.INITIAL_DELAY

        elif self._state in (self._STATE_FADING_IN, self._STATE_PLAYING):
            if path != self._current_path:
                self._pending_path = path
                pygame.mixer.music.fadeout(self.FADE_OUT_MS)
                self._state = self._STATE_FADING_OUT

        elif self._state == self._STATE_FADING_OUT:
            self._pending_path = path

    def _begin_fade_in(self, path: Path) -> None:
        self._target_volume = self._get_volume()
        self._current_path  = path
        self._pending_path  = None
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(0.0)
            pygame.mixer.music.play(loops=-1)
            self._timer = self.FADE_IN_DURATION
            self._state = self._STATE_FADING_IN
        except Exception as e:
            print(f"[AudioManager] Fehler beim Laden von {path.name}: {e}")
            self._state = self._STATE_IDLE

    def _get_volume(self) -> float:
        if self._settings is None:
            return 0.5
        if not self._settings.music_enabled:
            return 0.0
        return self._settings.music_volume / 100.0
