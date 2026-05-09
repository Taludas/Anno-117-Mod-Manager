"""Anno 117 install / Documents / mods folder discovery, cross-platform.

Pulled out of the original Tk app's ``find_anno_exe`` and
``update_mod_path_from_mode`` so both UIs (Tk legacy and pywebview) share
the same lookup logic — and so PR #4's Linux fixes (no /proc traversal,
realpath resolution, Steam compatdata enumeration) live in one place."""
from __future__ import annotations

import glob
import os
import platform
import string

IS_WINDOWS = platform.system() == 'Windows'

if IS_WINDOWS:
    import ctypes  # noqa: F401  (Windows-only, used in get_drive_letters)
    import winreg


def get_drive_letters() -> list[str]:
    """Returns logical drive letters on Windows or sub-mount points on Linux.

    Linux deliberately omits ``/`` because globbing the root traverses /proc
    and /sys symlinks (e.g. /proc/<pid>/cwd) and produces phantom paths like
    //proc/123/cwd/... that KIO/xdg-open mis-parses as ``smb://`` URLs."""
    if not IS_WINDOWS:
        candidates: list[str] = []
        for entry in ('/home', '/mnt', '/media', '/run/media', '/opt'):
            if os.path.isdir(entry):
                try:
                    for sub in os.scandir(entry):
                        if sub.is_dir():
                            candidates.append(sub.path)
                except PermissionError:
                    pass
        return candidates

    drives: list[str] = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()  # type: ignore[attr-defined]
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f'{letter}:')
        bitmask >>= 1
    return drives


def find_anno_exe() -> str:
    """Locate Anno117.exe across Steam, Ubisoft Launcher, and known
    install dirs. Returns the absolute, symlink-resolved path or '' if not
    found. Symlinks are resolved (notably /proc/<pid>/cwd) so we never
    persist a path that depends on a running process."""
    possible_roots: list[str] = []

    if IS_WINDOWS:
        # Ubisoft assigns Anno 117 the launcher ID 921 (the "117" of the
        # original key path was a guess based on the game name and never
        # matched a real install). We also probe the dedicated per-game
        # key and the Uplay uninstall record — both confirmed by users
        # running the Ubisoft Connect edition. Steam's UninstallString
        # pattern stays in case the Steam edition publishes one.
        reg_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Ubisoft\Launcher\Installs\921'),
            (winreg.HKEY_CURRENT_USER,  r'SOFTWARE\Ubisoft\Launcher\Installs\921'),
            (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Ubisoft\Anno 117 - Pax Romana'),
            (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Uplay Install 921'),
            (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 3274580'),
        ]
        for hive, key_path in reg_paths:
            try:
                with winreg.OpenKey(hive, key_path) as key:
                    for val_name in ('InstallDir', 'InstallLocation'):
                        try:
                            path, _ = winreg.QueryValueEx(key, val_name)
                            if path:
                                possible_roots.append(path)
                        except FileNotFoundError:
                            continue
            except (FileNotFoundError, OSError):
                continue

        program_files = os.environ.get('ProgramFiles(x86)', r'C:\Program Files (x86)')
        # Ubisoft Connect installs straight into "...\games\Anno 117 - Pax Romana"
        # — the previous code added an extra "\Anno 117" subfolder that
        # doesn't exist on disk, so the fallback never resolved.
        possible_roots.append(os.path.join(program_files, 'Ubisoft', 'Ubisoft Game Launcher', 'games', 'Anno 117 - Pax Romana'))
        possible_roots.append(os.path.join(program_files, 'Steam', 'steamapps', 'common', 'Anno 117 - Pax Romana'))
    else:
        home = os.path.expanduser('~')
        for steam_root in (
            os.path.join(home, '.steam', 'steam'),
            os.path.join(home, '.local', 'share', 'Steam'),
            '/usr/share/steam',
        ):
            possible_roots.append(os.path.join(steam_root, 'steamapps', 'common', 'Anno 117 - Pax Romana', 'Anno 117'))
            compat = os.path.join(steam_root, 'steamapps', 'compatdata')
            if os.path.isdir(compat):
                try:
                    for appid in os.listdir(compat):
                        possible_roots.append(os.path.join(
                            compat, appid, 'pfx', 'drive_c', 'Program Files (x86)',
                            'Ubisoft', 'Ubisoft Game Launcher', 'games',
                            'Anno 117 - Pax Romana',
                        ))
                except OSError:
                    pass

    drives = get_drive_letters()
    # Glob for the exe at depths 0..5 below each drive root so we catch most
    # nested install layouts (Lutris/Bottles/manual prefixes).
    exe_patterns = [
        os.path.join('Anno 117 - Pax Romana', 'Bin', 'Win64', 'Anno117.exe'),
        *[
            os.path.join(*(['*'] * n), 'Anno 117 - Pax Romana', 'Bin', 'Win64', 'Anno117.exe')
            for n in range(1, 6)
        ],
    ]

    for drive in drives:
        # On Windows "C:" needs a trailing sep ("C:\\"); on Linux drives are
        # already absolute and adding os.sep would produce '//' which KIO
        # mis-parses as smb://.
        drive_root = (drive + os.sep) if (IS_WINDOWS and not drive.endswith(os.sep)) else drive
        for pattern in exe_patterns:
            full_pattern = os.path.join(drive_root, pattern)
            try:
                for match in glob.glob(full_pattern):
                    if os.path.isfile(match):
                        return os.path.realpath(match)
            except Exception:
                continue

    for root in dict.fromkeys(possible_roots):
        if not root or not os.path.exists(root):
            continue
        for target in (
            os.path.join(root, 'Bin', 'Win64', 'Anno117.exe'),
            os.path.join(root, 'Anno 117 - Pax Romana', 'Bin', 'Win64', 'Anno117.exe'),
            os.path.join(root, 'Anno117.exe'),
        ):
            if os.path.exists(target):
                return os.path.realpath(target)
    return ''


def proton_documents_root() -> str:
    """Find the Anno 117 Documents folder inside any Proton compatdata prefix."""
    home = os.path.expanduser('~')
    for compat in (
        os.path.join(home, '.steam', 'steam', 'steamapps', 'compatdata'),
        os.path.join(home, '.local', 'share', 'Steam', 'steamapps', 'compatdata'),
    ):
        if not os.path.isdir(compat):
            continue
        try:
            for appid in os.listdir(compat):
                docs = os.path.join(compat, appid, 'pfx', 'drive_c', 'users', 'steamuser', 'Documents')
                if os.path.isdir(os.path.join(docs, 'Anno 117 - Pax Romana')):
                    return docs
        except OSError:
            continue
    return ''


def documents_mods_root(custom_docs: str = '') -> str:
    """Returns the Anno 117 ``mods`` folder under the user's Documents."""
    if custom_docs:
        base = custom_docs
    elif IS_WINDOWS:
        base = os.path.expanduser('~/Documents')
    else:
        base = proton_documents_root() or os.path.join(os.path.expanduser('~'), 'Documents')
    return os.path.join(base, 'Anno 117 - Pax Romana', 'mods')


def game_mods_root(game_exe_path: str) -> str:
    """Returns the ``mods`` folder relative to the configured game install."""
    if not game_exe_path:
        return ''
    game_root = os.path.dirname(os.path.dirname(os.path.dirname(game_exe_path)))
    candidate = os.path.join(game_root, 'mods')
    return candidate if os.path.isdir(candidate) else ''


def active_profile_path(custom_docs: str = '') -> str:
    """Returns the path to active-profile.txt under the documents mods root."""
    base = documents_mods_root(custom_docs)
    return os.path.join(base, 'active-profile.txt') if base else ''
