"""
Screen - Hintergrundbild und Fensterverwaltung.
Basiert auf Sturm auf Grayskull (1:1, Titel angepasst).
"""

import pygame
import os
import glob
from typing import Optional
from core.utils.global_constants import COLORS


class Screen:
    """
    Verwaltet Hintergrundbild und Fenstergröße.
    Unterstützt SVG (via cairosvg oder pygame direkt) und Rasterformate (JPG, PNG).
    Sucht in media/, artwork/ und interfaces/renderer/pygame/media/ nach Hintergrundbildern.
    """

    def __init__(self, width: int = 1280, height: int = 800,
                 screen: Optional[pygame.Surface] = None,
                 resizable: bool = True):
        self.width = width
        self.height = height
        self.resizable = resizable

        if screen is None:
            self.screen = pygame.display.set_mode(
                (width, height), pygame.RESIZABLE if resizable else 0
            )
            pygame.display.set_caption("Code Sandbox")
        else:
            self.screen = screen

        self.background_img = None
        self._load_background()

    def _search_candidates(self) -> list:
        """Gibt priorisierte Liste möglicher Hintergrundbild-Pfade zurück."""
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
        media_dirs = [
            os.path.join(project_root, "interfaces", "renderer", "pygame", "media"),
            os.path.join(project_root, "media"),
            os.path.join(project_root, "artwork"),
            os.path.join(project_root, "interfaces", "media"),
            os.path.join(project_root, "interfaces", "artwork"),
        ]
        candidates = []
        for d in media_dirs:
            if not os.path.isdir(d):
                continue
            candidates += sorted(glob.glob(os.path.join(d, "background*.svg")))
            candidates += sorted(glob.glob(os.path.join(d, "background*.jpg")))
            candidates += sorted(glob.glob(os.path.join(d, "background*.png")))
        return candidates

    def _load_svg(self, path: str) -> Optional[pygame.Surface]:
        """Lädt eine SVG-Datei über cairosvg + Pillow."""
        try:
            import cairosvg, io
            from PIL import Image as PILImage

            png_bytes = cairosvg.svg2png(
                url=path,
                output_width=self.width,
                output_height=self.height
            )
            pil_img = PILImage.open(io.BytesIO(png_bytes)).convert("RGB")
            raw = pil_img.tobytes()
            surf = pygame.image.fromstring(raw, pil_img.size, "RGB")
            print(f"SVG geladen via cairosvg+Pillow: {path}")
            return surf.convert()
        except ImportError as e:
            print(f"Abhängigkeit fehlt ({e}) – versuche pygame direkt.")
        except Exception as e:
            print(f"cairosvg/Pillow Fehler bei {path}: {e}")

        try:
            surf = pygame.image.load(path).convert()
            print(f"SVG geladen via pygame direkt: {path}")
            return surf
        except Exception as e:
            print(f"pygame SVG-Direktladen fehlgeschlagen ({path}): {e}")

        return None

    def _load_background(self) -> None:
        for path in self._search_candidates():
            try:
                if path.lower().endswith(".svg"):
                    surface = self._load_svg(path)
                else:
                    surface = pygame.image.load(path).convert()

                if surface:
                    self.background_img = surface
                    print(f"Hintergrundbild geladen: {path}")
                    return
            except Exception as e:
                print(f"Fehler beim Laden von {path}: {e}")

        print("Kein Hintergrundbild gefunden – Fallback auf Farbe.")
        self.background_img = None

    def set_screen_size(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        if self.resizable:
            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def render_background(self) -> None:
        if self.background_img:
            scaled = pygame.transform.scale(self.background_img, (self.width, self.height))
            self.screen.blit(scaled, (0, 0))
        else:
            self.screen.fill(COLORS["background"])

    def get_surface(self) -> pygame.Surface:
        return self.screen
