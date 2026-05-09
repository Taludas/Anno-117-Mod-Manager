"""Cross-platform game-launch helpers.

On Windows we just exec the .exe. On Linux the same path is a Win32 binary
running inside a Steam Proton prefix, so we route through the Steam URI
(``steam://rungameid/<id>``) instead — that lets Steam set up Proton and chain
to Ubisoft Connect properly. Steam appids fit in 32 bits; non-Steam shortcuts
need the full 64-bit GameID format ``(appid << 32) | 0x02000000``."""
from __future__ import annotations

import os
import platform
import re
import subprocess

IS_WINDOWS = platform.system() == 'Windows'
IS_LINUX = platform.system() == 'Linux'

NON_STEAM_GAMEID_HIGH = 0x02000000


def _steam_root_for_path(path: str) -> str:
    """Returns the Steam library root containing the given path (the dir
    holding steamapps/), or '' if the path isn't inside a Steam layout."""
    marker = '/steamapps/'
    idx = path.find(marker)
    return path[:idx] if idx != -1 else ''


def launch(game_exe_path: str) -> tuple[bool, str]:
    """Launch the game given the absolute path to its .exe. Returns (ok, error)."""
    if not game_exe_path or not os.path.exists(game_exe_path):
        return False, 'game_path not set or file missing'
    try:
        if IS_WINDOWS:
            subprocess.Popen(
                [game_exe_path],
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0),
            )
            return True, ''
        if IS_LINUX:
            m = re.search(r'/steamapps/compatdata/(\d+)/pfx/', game_exe_path)
            if m:
                appid = int(m.group(1))
                steam_root = _steam_root_for_path(game_exe_path)
                manifest = (
                    os.path.join(steam_root, 'steamapps', f'appmanifest_{appid}.acf')
                    if steam_root else ''
                )
                # Real Steam apps publish an appmanifest_<appid>.acf and accept
                # the bare appid in rungameid. Non-Steam shortcuts need the
                # 64-bit GameID variant ((appid << 32) | 0x02000000) — passing
                # the bare appid for those returns "Unknown GameID type".
                if manifest and os.path.exists(manifest):
                    target = str(appid)
                else:
                    target = str((appid << 32) | NON_STEAM_GAMEID_HIGH)
                subprocess.Popen(['xdg-open', f'steam://rungameid/{target}'])
                return True, ''
        # Non-Steam Linux install (Lutris/Heroic/Bottles/raw Wine) → hand the
        # path to whatever launcher is registered for .exe.
        subprocess.Popen(['xdg-open' if IS_LINUX else 'open', game_exe_path])
        return True, ''
    except Exception as e:
        return False, str(e)
