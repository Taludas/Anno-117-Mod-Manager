"""Cross-platform file/folder utilities shared by both UIs."""
from __future__ import annotations

import os
import platform
import shutil
import subprocess

IS_WINDOWS = platform.system() == 'Windows'
IS_LINUX = platform.system() == 'Linux'

# Order matters: the first banner candidate that exists wins.
BANNER_NAMES = ('banner.png', 'banner.jpg', 'thumbnail.png', 'thumbnail.jpg')


def dir_size_bytes(path: str) -> int:
    """Recursively sum file sizes inside ``path``. Symlinks are not followed
    so a misconfigured prefix can't blow up the count."""
    total = 0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += dir_size_bytes(entry.path)
            except OSError:
                pass
    except OSError:
        pass
    return total


def find_banner(mod_path: str) -> str:
    """Return the filename of the first banner candidate that exists inside
    ``mod_path`` (banner.png / .jpg / thumbnail.png / .jpg), else ''."""
    for name in BANNER_NAMES:
        if os.path.isfile(os.path.join(mod_path, name)):
            return name
    return ''


def open_path(path: str) -> tuple[bool, str]:
    """Open ``path`` in the OS default file manager / handler. Returns
    (ok, error_message)."""
    if not path or not os.path.exists(path):
        return False, 'path missing'
    try:
        if IS_WINDOWS:
            os.startfile(path)  # type: ignore[attr-defined]
        elif IS_LINUX:
            subprocess.Popen(['xdg-open', path])
        else:
            subprocess.Popen(['open', path])
        return True, ''
    except Exception as e:
        return False, str(e)


def safe_rmtree(path: str, allowed_roots: list[str]) -> tuple[bool, str]:
    """Recursively delete ``path`` ONLY if it lives inside one of
    ``allowed_roots``. Used to make uninstall safe against any caller-provided
    folder name that might try to escape the configured mod roots."""
    if not path or not os.path.isdir(path):
        return False, 'not a directory'
    abs_target = os.path.realpath(path)
    if not any(
        abs_target == os.path.realpath(r) or
        abs_target.startswith(os.path.realpath(r) + os.sep)
        for r in allowed_roots if r
    ):
        return False, 'path outside allowed roots'
    try:
        shutil.rmtree(abs_target)
        return True, ''
    except OSError as e:
        return False, str(e)
