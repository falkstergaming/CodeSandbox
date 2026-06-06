"""
Jukebox-Modus – integrierter MP3-Player mit Moodboard.

Features:
  - MP3-Ordner von beliebigem Pfad (nicht im CodeSandbox-Verzeichnis nötig)
  - Ordner-Picker via tkinter (stdlib, keine Abhängigkeit)
  - Ordnerpfad wird in settings.ini gespeichert
  - Play / Pause / Zurück / Weiter / Zufall
  - Scrollbare Track-Liste
  - Moodboard: Schieberegler + Kippschalter → Top-8-Playlist + .m3u-Export
  - AudioManager wird beim Betreten gestoppt und beim Verlassen freigegeben

Farbkonzept: GOLD dominant · GRAU Hintergrund
"""

import json
import os
import random
import pygame

from core.utils.global_constants import FONT_FAMILY, GRAU, GOLD, SILBER
from core.utils.colors import TEXT_LIGHT, TEXT_HIGHLIGHT
from interfaces.renderer.pygame.components.room_panel import draw_room_panel

_ACCENT   = GOLD["midtone"]
_ROW_H    = 22
_CTRL_H   = 52
_FBAR_H   = 28
_TAB_H    = 30

_DB_PATH  = "jukebox_tags.json"
_MB_PATH  = "jukebox_moodboard.json"
_PL_PATH  = "jukebox_playlist.m3u"


def _pick_folder_dialog() -> str:
    """Öffnet einen Ordner-Auswahl-Dialog via tkinter. Gibt '' zurück bei Abbruch."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        folder = filedialog.askdirectory(title="Jukebox — MP3-Ordner wählen")
        root.destroy()
        return folder or ""
    except Exception:
        return ""


class _Slider:
    __slots__ = ("key", "label", "lo_label", "hi_label", "value", "rect", "_dragging")

    def __init__(self, key: str, label: str, lo_label: str = "0", hi_label: str = "100"):
        self.key       = key
        self.label     = label
        self.lo_label  = lo_label
        self.hi_label  = hi_label
        self.value     = 50
        self.rect      = pygame.Rect(0, 0, 1, 1)
        self._dragging = False


class _Toggle:
    __slots__ = ("key", "label", "state", "rects")

    def __init__(self, key: str, label: str):
        self.key   = key
        self.label = label
        self.state = None       # None = Egal, True = Ja, False = Nein
        self.rects: dict = {}   # "egal"/"ja"/"nein" → Rect


class Jukebox:
    """Jukebox-Raum – MP3-Player mit Moodboard-Playlisten-Generator."""

    def __init__(self, screen, screen_width: int, screen_height: int, **kwargs):
        self.screen        = screen
        self.screen_width  = screen_width
        self.screen_height = screen_height
        self._set_mode_fn  = None
        self._audio_mgr    = None
        self._settings     = kwargs.get("settings", None)

        # Fonts
        self._f_small  = pygame.font.SysFont(FONT_FAMILY, 12)
        self._f_normal = pygame.font.SysFont(FONT_FAMILY, 13)
        self._f_bold   = pygame.font.SysFont(FONT_FAMILY, 13, bold=True)
        self._f_ctrl   = pygame.font.SysFont(FONT_FAMILY, 14, bold=True)
        self._f_tab    = pygame.font.SysFont(FONT_FAMILY, 13, bold=True)

        # Playback
        self._tracks:  list = []
        self._current: int  = -1
        self._playing: bool = False
        self._shuffle: bool = False

        # UI-Zustand Tracks-Tab
        self._scroll:     int         = 0
        self._hover:      object      = None
        self._folder_btn: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self._ctrl_btns:  dict        = {}
        self._list_rect:  pygame.Rect = pygame.Rect(0, 0, 0, 0)

        # Tab-Zustand
        self._view      = "tracks"   # "tracks" | "moodboard"
        self._tab_rects: dict = {}

        # Moodboard
        self._sliders: list[_Slider] = [
            _Slider("tempo",     "Tempo",     "langsam",  "schnell"),
            _Slider("energy",    "Energy",    "ruhig",    "intensiv"),
            _Slider("mood",      "Mood",      "dunkel",   "hell"),
            _Slider("density",   "Dichte",    "minimal",  "voll"),
            _Slider("roughness", "Roughness", "glatt",    "rau"),
        ]
        self._toggles: list[_Toggle] = [
            _Toggle("instrumental", "Instrumental"),
            _Toggle("loop_ready",   "Loop-Ready"),
            _Toggle("beat_driven",  "Beat-Driven"),
        ]
        self._playlist:    list = []   # [(score, name, album, path), ...]
        self._gen_btn:     pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self._reset_btn:   pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self._drag_slider: _Slider | None = None

        # Datenbank und gespeicherte Moodboard-Settings laden
        self._db: dict = self._load_db()
        self._load_moodboard()

        # Letzten bekannten Ordner laden
        folder = self._settings.jukebox_folder if self._settings else ""
        if folder:
            self._scan(folder)

    # ── Callbacks ─────────────────────────────────────────────────────────

    def set_app_callbacks(self, set_mode_fn, audio_manager=None):
        self._set_mode_fn = set_mode_fn
        self._audio_mgr   = audio_manager

    # ── Lifecycle ─────────────────────────────────────────────────────────

    def on_enter(self):
        if self._audio_mgr:
            self._audio_mgr.stop()

    def on_leave(self):
        pygame.mixer.music.stop()
        self._playing = False

    # ── Datenbank ─────────────────────────────────────────────────────────

    def _load_db(self) -> dict:
        if os.path.exists(_DB_PATH):
            try:
                with open(_DB_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Jukebox] DB-Ladefehler: {e}")
        return {}

    def _load_moodboard(self):
        if os.path.exists(_MB_PATH):
            try:
                with open(_MB_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                sliders = data.get("sliders", {})
                for s in self._sliders:
                    if s.key in sliders:
                        s.value = max(0, min(100, int(sliders[s.key])))
                toggles = data.get("toggles", {})
                for t in self._toggles:
                    if t.key in toggles:
                        raw = toggles[t.key]
                        t.state = None if raw is None else bool(raw)
            except Exception as e:
                print(f"[Jukebox] Moodboard-Ladefehler: {e}")

    def _save_moodboard(self):
        data = {
            "sliders": {s.key: s.value for s in self._sliders},
            "toggles": {t.key: t.state for t in self._toggles},
        }
        try:
            with open(_MB_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Jukebox] Moodboard-Speicherfehler: {e}")

    # ── Scoring + Playlist ────────────────────────────────────────────────

    def _score_track(self, entry: dict) -> float:
        tags   = entry.get("tags", {})
        scores = []
        for s in self._sliders:
            tv = tags.get(s.key)
            if tv is not None:
                scores.append((100 - abs(s.value - int(tv))) / 100.0)
        for t in self._toggles:
            if t.state is None:
                continue
            tv = tags.get(t.key)
            if tv is None:
                scores.append(0.5)
            elif bool(tv) == t.state:
                scores.append(1.0)
            else:
                scores.append(0.0)
        return sum(scores) / len(scores) if scores else 0.0

    def _generate_playlist(self):
        ranked = sorted(
            [
                (self._score_track(entry), entry.get("name", "?"),
                 entry.get("album", "?"), path)
                for path, entry in self._db.items()
            ],
            key=lambda x: x[0],
            reverse=True,
        )
        self._playlist = ranked[:8]
        self._export_m3u(self._playlist)
        self._save_moodboard()

    def _export_m3u(self, playlist: list):
        try:
            with open(_PL_PATH, "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                for score, name, album, path in playlist:
                    f.write(f"#EXTINF:0,{name} [{album}]  ({score:.0%})\n")
                    f.write(path.replace("/", "\\") + "\n")
        except Exception as e:
            print(f"[Jukebox] M3U-Exportfehler: {e}")

    def _reset_moodboard(self):
        for s in self._sliders:
            s.value = 50
        for t in self._toggles:
            t.state = None
        self._playlist = []

    # ── Track-Verwaltung ──────────────────────────────────────────────────

    def _scan(self, folder: str):
        self._tracks = []
        if folder and os.path.isdir(folder):
            for f in sorted(os.listdir(folder), key=str.lower):
                if f.lower().endswith(".mp3"):
                    name = os.path.splitext(f)[0]
                    self._tracks.append((name, os.path.join(folder, f)))
        self._current = 0 if self._tracks else -1
        self._scroll  = 0

    def _pick_folder(self):
        folder = _pick_folder_dialog()
        if folder:
            self._scan(folder)
            if self._settings:
                self._settings.jukebox_folder = folder

    def _play(self, index: int):
        if 0 <= index < len(self._tracks):
            _, path = self._tracks[index]
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                if self._settings:
                    pygame.mixer.music.set_volume(self._settings.music_volume / 100.0)
                self._current = index
                self._playing = True
                self._scroll_to_current()
            except Exception as e:
                print(f"[Jukebox] Fehler beim Laden: {e}")

    def _toggle(self):
        if not self._tracks:
            return
        if self._current < 0:
            self._current = 0
        if self._playing:
            pygame.mixer.music.pause()
            self._playing = False
        else:
            if pygame.mixer.music.get_pos() > 0:
                pygame.mixer.music.unpause()
            else:
                self._play(self._current)
                return
            self._playing = True

    def _next(self):
        if not self._tracks:
            return
        if self._shuffle:
            idx = random.randint(0, len(self._tracks) - 1)
        else:
            idx = (max(0, self._current) + 1) % len(self._tracks)
        self._play(idx)

    def _prev(self):
        if not self._tracks:
            return
        idx = (max(0, self._current) - 1) % len(self._tracks)
        self._play(idx)

    def _scroll_to_current(self):
        if self._current < 0:
            return
        rows = self._list_rect.height // _ROW_H if self._list_rect.height else 10
        if self._current < self._scroll:
            self._scroll = self._current
        elif self._current >= self._scroll + rows:
            self._scroll = self._current - rows + 1

    def _scroll_list(self, delta: int):
        if not self._tracks:
            return
        rows   = self._list_rect.height // _ROW_H if self._list_rect.height else 1
        max_sc = max(0, len(self._tracks) - rows)
        self._scroll = max(0, min(max_sc, self._scroll + delta))

    # ── Event-Handling ────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self._hover = self._hittest(event.pos)
            if self._drag_slider:
                self._update_slider_drag(self._drag_slider, event.pos[0])
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._click(event.pos)
            elif event.button == 4:
                if self._view == "tracks":
                    self._scroll_list(-1)
            elif event.button == 5:
                if self._view == "tracks":
                    self._scroll_list(1)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self._drag_slider = None
        elif event.type == pygame.MOUSEWHEEL:
            if self._view == "tracks" and self._list_rect.collidepoint(pygame.mouse.get_pos()):
                self._scroll_list(-event.y)

    def _hittest(self, pos) -> object:
        # Tab-Buttons immer prüfen
        for key, rect in self._tab_rects.items():
            if rect.collidepoint(pos):
                return ("tab", key)

        if self._view == "tracks":
            if self._folder_btn.collidepoint(pos):
                return "folder"
            for key, rect in self._ctrl_btns.items():
                if rect.collidepoint(pos):
                    return key
            if self._list_rect.collidepoint(pos):
                row = (pos[1] - self._list_rect.y) // _ROW_H
                idx = self._scroll + row
                if 0 <= idx < len(self._tracks):
                    return ("track", idx)
        elif self._view == "moodboard":
            for s in self._sliders:
                if s.rect.collidepoint(pos):
                    return ("slider", s)
            for t in self._toggles:
                for st, rect in t.rects.items():
                    if rect.collidepoint(pos):
                        return ("toggle", t, st)
            if self._gen_btn.collidepoint(pos):
                return "generate"
            if self._reset_btn.collidepoint(pos):
                return "reset"
        return None

    def _click(self, pos):
        hit = self._hittest(pos)
        if isinstance(hit, tuple) and hit[0] == "tab":
            self._view = hit[1]
            return

        if self._view == "tracks":
            if hit == "folder":
                self._pick_folder()
            elif hit == "play":
                self._toggle()
            elif hit == "next":
                self._next()
            elif hit == "prev":
                self._prev()
            elif hit == "shuffle":
                self._shuffle = not self._shuffle
            elif isinstance(hit, tuple) and hit[0] == "track":
                self._play(hit[1])
        elif self._view == "moodboard":
            if isinstance(hit, tuple) and hit[0] == "slider":
                self._drag_slider = hit[1]
                self._update_slider_drag(hit[1], pos[0])
            elif isinstance(hit, tuple) and hit[0] == "toggle":
                t, st = hit[1], hit[2]
                t.state = {"egal": None, "ja": True, "nein": False}[st]
            elif hit == "generate":
                self._generate_playlist()
            elif hit == "reset":
                self._reset_moodboard()

    def _update_slider_drag(self, slider: _Slider, mx: int):
        r = slider.rect
        rel   = mx - r.x
        val   = int(rel / r.width * 100)
        slider.value = max(0, min(100, val))

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, dt: float):
        if self._playing and not pygame.mixer.music.get_busy():
            self._next()

    # ── Rendering ─────────────────────────────────────────────────────────

    def render_content(self):
        ix, iy, iw, ih = draw_room_panel(
            self.screen, self.screen_width, self.screen_height,
            title="♪  JUKEBOX",
            subtitle="MP3-Player  ·  Moodboards  ·  Playlisten",
            accent_color=_ACCENT,
        )
        self._draw(ix, iy, iw, ih)

    def _draw(self, ix, iy, iw, ih):
        surf = self.screen

        # ── Tab-Leiste ────────────────────────────────────────────────────
        self._draw_tabs(surf, ix, iy, iw)
        content_y = iy + _TAB_H + 4

        if self._view == "tracks":
            self._draw_tracks_view(surf, ix, content_y, iw, ih - _TAB_H - 4)
        else:
            self._draw_moodboard_view(surf, ix, content_y, iw, ih - _TAB_H - 4)

    def _draw_tabs(self, surf, ix, iy, iw):
        tabs = [("tracks", "♪  Tracks"), ("moodboard", "⊞  Moodboard")]
        tab_w = iw // len(tabs)
        self._tab_rects = {}
        for i, (key, label) in enumerate(tabs):
            rect = pygame.Rect(ix + i * tab_w, iy, tab_w - 2, _TAB_H)
            self._tab_rects[key] = rect
            active = self._view == key
            hov    = self._hover == ("tab", key)
            bg = GOLD["overtone"] if active else (GRAU["hightone"] if hov else GRAU["midtone"])
            pygame.draw.rect(surf, bg, rect, border_radius=3)
            border = _ACCENT if active else GRAU["halftone"]
            pygame.draw.rect(surf, border, rect, 1, border_radius=3)
            col = TEXT_HIGHLIGHT if active else (TEXT_LIGHT if hov else GRAU["lowtone"])
            txt = self._f_tab.render(label, True, col)
            surf.blit(txt, txt.get_rect(center=rect.center))

    # ── Tracks-Tab ────────────────────────────────────────────────────────

    def _draw_tracks_view(self, surf, ix, iy, iw, ih):
        self._draw_folder_bar(surf, ix, iy, iw)
        sep1_y = iy + _FBAR_H + 2
        pygame.draw.line(surf, GRAU["midtone"], (ix, sep1_y), (ix + iw, sep1_y), 1)

        ctrl_top = iy + ih - _CTRL_H
        sep2_y   = ctrl_top - 4
        list_y   = sep1_y + 4
        list_h   = sep2_y - list_y - 2
        self._list_rect = pygame.Rect(ix, list_y, iw, list_h)
        self._draw_track_list(surf, ix, list_y, iw, list_h)

        pygame.draw.line(surf, GRAU["midtone"], (ix, sep2_y), (ix + iw, sep2_y), 1)
        self._draw_controls(surf, ix, ctrl_top, iw)

    def _draw_folder_bar(self, surf, ix, iy, iw):
        btn_w  = 120
        folder = self._settings.jukebox_folder if self._settings else ""

        display = folder if folder else "Kein Ordner ausgewählt"
        col     = GRAU["lowtone"] if folder else GRAU["halftone"]
        max_w   = iw - btn_w - 20
        txt     = self._f_normal.render(display, True, col)
        if txt.get_width() > max_w:
            while txt.get_width() > max_w and len(display) > 4:
                display = "…" + display[-(len(display) - 2):]
                txt = self._f_normal.render(display, True, col)
        cy = iy + (_FBAR_H - txt.get_height()) // 2
        surf.blit(txt, (ix, cy))

        btn_x    = ix + iw - btn_w
        btn_rect = pygame.Rect(btn_x, iy + 2, btn_w, _FBAR_H - 4)
        self._folder_btn = btn_rect
        hov = self._hover == "folder"
        pygame.draw.rect(surf, GOLD["hightone"] if hov else GRAU["hightone"], btn_rect, border_radius=3)
        pygame.draw.rect(surf, _ACCENT, btn_rect, 1, border_radius=3)
        lbl = self._f_bold.render("Ordner wählen", True, TEXT_HIGHLIGHT if hov else GRAU["lowtone"])
        surf.blit(lbl, lbl.get_rect(center=btn_rect.center))

    def _draw_track_list(self, surf, ix, iy, iw, ih):
        if not self._tracks:
            msg = self._f_normal.render(
                "Kein Ordner ausgewählt  —  'Ordner wählen' oben rechts",
                True, GRAU["halftone"],
            )
            surf.blit(msg, msg.get_rect(centerx=ix + iw // 2, centery=iy + ih // 2))
            return

        rows  = ih // _ROW_H
        start = self._scroll
        end   = min(start + rows, len(self._tracks))

        for i, idx in enumerate(range(start, end)):
            name, _ = self._tracks[idx]
            ry     = iy + i * _ROW_H
            is_cur = idx == self._current
            is_hov = self._hover == ("track", idx)

            if is_cur:
                pygame.draw.rect(surf, GOLD["overtone"], (ix, ry, iw, _ROW_H))
                col  = TEXT_HIGHLIGHT
                font = self._f_bold
                icon = "▶ " if self._playing else "‖ "
            elif is_hov:
                pygame.draw.rect(surf, GRAU["midtone"], (ix, ry, iw, _ROW_H))
                col  = TEXT_LIGHT
                font = self._f_normal
                icon = "  "
            else:
                col  = GRAU["lowtone"]
                font = self._f_normal
                icon = "  "

            label = f"{icon}{idx + 1:3d}.  {name}"
            txt   = font.render(label, True, col)
            surf.blit(txt, (ix + 6, ry + (_ROW_H - txt.get_height()) // 2))

        if len(self._tracks) > rows:
            bx = ix + iw - 5
            bh = max(20, ih * rows // len(self._tracks))
            by = iy + self._scroll * (ih - bh) // max(1, len(self._tracks) - rows)
            pygame.draw.rect(surf, GRAU["midtone"], (bx, iy, 4, ih),  border_radius=2)
            pygame.draw.rect(surf, GOLD["midtone"], (bx, by, 4, bh),  border_radius=2)

    def _draw_controls(self, surf, ix, iy, iw):
        definitions = [
            ("prev",    "⏮  Zurück"),
            ("play",    "⏸  Pause" if self._playing else "▶  Play"),
            ("next",    "⏭  Weiter"),
            ("shuffle", "⇄  Zufall"),
        ]
        btn_w = 88
        btn_h = 32
        gap   = 10
        total = len(definitions) * btn_w + (len(definitions) - 1) * gap
        bx    = ix + (iw - total) // 2
        by    = iy + 4

        self._ctrl_btns = {}
        for key, label in definitions:
            hov    = self._hover == key
            active = (key == "shuffle" and self._shuffle) or (key == "play" and self._playing)
            bg     = GOLD["hightone"]  if hov    else (GOLD["overtone"] if active else GRAU["hightone"])
            border = _ACCENT           if active else (GOLD["halftone"] if hov else GRAU["halftone"])
            rect   = pygame.Rect(bx, by, btn_w, btn_h)
            pygame.draw.rect(surf, bg,     rect, border_radius=4)
            pygame.draw.rect(surf, border, rect, 1, border_radius=4)
            lbl = self._f_ctrl.render(label, True, TEXT_HIGHLIGHT if (hov or active) else GRAU["lowtone"])
            surf.blit(lbl, lbl.get_rect(center=rect.center))
            self._ctrl_btns[key] = rect
            bx += btn_w + gap

        if 0 <= self._current < len(self._tracks):
            name, _ = self._tracks[self._current]
            state   = "▶" if self._playing else "‖"
            np      = self._f_small.render(f"{state}  {name}", True, GOLD["halftone"])
            surf.blit(np, np.get_rect(centerx=ix + iw // 2, y=iy + btn_h + 10))

    # ── Moodboard-Tab ─────────────────────────────────────────────────────

    def _draw_moodboard_view(self, surf, ix, iy, iw, ih):
        SECT_H   = 16
        SLIDER_H = 30
        TOGGLE_H = 26
        PAD      = 8

        left_w  = int(iw * 0.55)
        right_w = iw - left_w - PAD

        left_x  = ix
        right_x = ix + left_w + PAD

        cy = iy + 4

        # ── Linke Spalte: Schieberegler ───────────────────────────────────
        header = self._f_bold.render("Filter — Schieberegler", True, GOLD["halftone"])
        surf.blit(header, (left_x, cy))
        cy += SECT_H + 2

        for s in self._sliders:
            self._draw_slider(surf, s, left_x, cy, left_w, SLIDER_H)
            cy += SLIDER_H + 4

        # ── Rechte Spalte: Kippschalter + Buttons ─────────────────────────
        ry = iy + 4
        header2 = self._f_bold.render("Eigenschaften", True, GOLD["halftone"])
        surf.blit(header2, (right_x, ry))
        ry += SECT_H + 2

        for t in self._toggles:
            self._draw_toggle(surf, t, right_x, ry, right_w, TOGGLE_H)
            ry += TOGGLE_H + 6

        ry += 4
        btn_h = 28
        btn_w = (right_w - 6) // 2

        # Reset-Button
        self._reset_btn = pygame.Rect(right_x, ry, btn_w, btn_h)
        hov_reset = self._hover == "reset"
        pygame.draw.rect(surf, GRAU["hightone"] if hov_reset else GRAU["midtone"], self._reset_btn, border_radius=3)
        pygame.draw.rect(surf, GRAU["halftone"], self._reset_btn, 1, border_radius=3)
        lbl = self._f_bold.render("↺ Zurücksetzen", True, TEXT_LIGHT if hov_reset else GRAU["lowtone"])
        surf.blit(lbl, lbl.get_rect(center=self._reset_btn.center))

        # Generate-Button
        self._gen_btn = pygame.Rect(right_x + btn_w + 6, ry, btn_w, btn_h)
        hov_gen = self._hover == "generate"
        pygame.draw.rect(surf, GOLD["hightone"] if hov_gen else GOLD["overtone"], self._gen_btn, border_radius=3)
        pygame.draw.rect(surf, _ACCENT, self._gen_btn, 1, border_radius=3)
        lbl2 = self._f_bold.render("▶ Generieren", True, TEXT_HIGHLIGHT)
        surf.blit(lbl2, lbl2.get_rect(center=self._gen_btn.center))

        # ── Ergebnis-Liste ─────────────────────────────────────────────────
        sep_y = iy + max(
            cy - iy + 4,
            ry + btn_h + 8 - iy,
        )
        pygame.draw.line(surf, GRAU["midtone"], (ix, sep_y), (ix + iw, sep_y), 1)

        res_y = sep_y + 4
        res_h = (iy + ih) - res_y

        if not self._playlist:
            hint = self._f_small.render(
                "Schieberegler einstellen und '▶ Generieren' drücken",
                True, GRAU["halftone"],
            )
            surf.blit(hint, hint.get_rect(centerx=ix + iw // 2, centery=res_y + res_h // 2))
        else:
            header3 = self._f_bold.render("Top 8 Playlist", True, GOLD["midtone"])
            surf.blit(header3, (ix, res_y))
            res_y += 16

            for rank, (score, name, album, path) in enumerate(self._playlist):
                ry2    = res_y + rank * 18
                if ry2 + 18 > iy + ih:
                    break
                score_col = GOLD["midtone"] if score > 0.75 else (GOLD["halftone"] if score > 0.5 else GRAU["lowtone"])
                score_txt = self._f_small.render(f"{score:.0%}", True, score_col)
                name_txt  = self._f_small.render(f"{rank+1}. {name}", True, TEXT_LIGHT)
                album_txt = self._f_small.render(f"[{album}]", True, GRAU["halftone"])
                surf.blit(score_txt, (ix, ry2 + 2))
                surf.blit(name_txt,  (ix + 42, ry2 + 2))
                # album rechts
                surf.blit(album_txt, album_txt.get_rect(right=ix + iw, y=ry2 + 2))

        # Hinweis auf Export
        if self._playlist:
            hint2 = self._f_small.render(f"Exportiert nach {_PL_PATH}", True, GRAU["halftone"])
            surf.blit(hint2, (ix, iy + ih - 14))

    def _draw_slider(self, surf, slider: _Slider, x, y, w, h):
        TRACK_H = 6
        KNOB_R  = 7

        # Label + Wert
        lbl = self._f_small.render(slider.label, True, GRAU["lowtone"])
        val = self._f_bold.render(str(slider.value), True, TEXT_LIGHT)
        surf.blit(lbl, (x, y))
        surf.blit(val, (x + w - val.get_width(), y))

        # Track
        track_y  = y + 14 + (h - 14 - TRACK_H) // 2
        track_x0 = x + KNOB_R
        track_x1 = x + w - KNOB_R
        track_w  = track_x1 - track_x0
        pygame.draw.rect(surf, GRAU["midtone"], (track_x0, track_y, track_w, TRACK_H), border_radius=3)

        fill_w = int(slider.value / 100 * track_w)
        if fill_w > 0:
            pygame.draw.rect(surf, _ACCENT, (track_x0, track_y, fill_w, TRACK_H), border_radius=3)

        # Lo/Hi Labels
        lo_txt = self._f_small.render(slider.lo_label, True, GRAU["halftone"])
        hi_txt = self._f_small.render(slider.hi_label, True, GRAU["halftone"])
        surf.blit(lo_txt, (track_x0, track_y + TRACK_H + 1))
        surf.blit(hi_txt, hi_txt.get_rect(right=track_x1, y=track_y + TRACK_H + 1))

        # Knob
        knob_x = track_x0 + int(slider.value / 100 * track_w)
        knob_y = track_y + TRACK_H // 2
        pygame.draw.circle(surf, _ACCENT,          (knob_x, knob_y), KNOB_R)
        pygame.draw.circle(surf, GOLD["hightone"], (knob_x, knob_y), KNOB_R - 2)

        # Interaktionsbereich speichern
        slider.rect = pygame.Rect(track_x0, y, track_w, h)

    def _draw_toggle(self, surf, toggle: _Toggle, x, y, w, h):
        lbl = self._f_small.render(toggle.label, True, GRAU["lowtone"])
        surf.blit(lbl, (x, y + (h - lbl.get_height()) // 2))

        seg_w  = 42
        seg_h  = h
        states = [("egal", "Egal", None), ("ja", "Ja", True), ("nein", "Nein", False)]
        bx     = x + w - len(states) * (seg_w + 2)

        toggle.rects = {}
        for key, label, val in states:
            rect   = pygame.Rect(bx, y, seg_w, seg_h)
            active = toggle.state == val
            hov    = self._hover == ("toggle", toggle, key)
            bg     = (GOLD["overtone"] if active else (GRAU["hightone"] if hov else GRAU["midtone"]))
            border = (_ACCENT         if active else GRAU["halftone"])
            col    = (TEXT_HIGHLIGHT  if active else (TEXT_LIGHT if hov else GRAU["lowtone"]))
            pygame.draw.rect(surf, bg,     rect, border_radius=3)
            pygame.draw.rect(surf, border, rect, 1, border_radius=3)
            txt = self._f_small.render(label, True, col)
            surf.blit(txt, txt.get_rect(center=rect.center))
            toggle.rects[key] = rect
            bx += seg_w + 2

    # ── Boilerplate ───────────────────────────────────────────────────────

    def init(self):
        pass
