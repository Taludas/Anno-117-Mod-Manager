"""ZIP-based mod installer.

Extracts an Anno 117 mod archive into the configured mods folder. The
archive must contain a ``modinfo.json`` (or ``.jsonc``) — anywhere inside,
not necessarily at the root — which we use to determine the destination
folder name and the parsed mod id.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import zipfile


def _strip_jsonc(text: str) -> str:
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'(?<!:)//.*', '', text)
    return text


def install_zip(zip_path: str, target_base_dir: str, allow_overwrite: bool = False) -> dict:
    """Extract ``zip_path`` into ``target_base_dir``. Returns:

    {ok, mod_id, folder, exists_already, error}

    - ``exists_already`` is True without action when the mod folder already
      exists in the target dir AND ``allow_overwrite`` is False — the caller
      should ask for confirmation and re-call with allow_overwrite=True.
    - On success, ``folder`` is the mod folder name (basename) and
      ``mod_id`` is the ModID parsed from modinfo.json[c] (may be empty if
      the file lacks one).
    """
    if not zip_path or not os.path.isfile(zip_path):
        return {'ok': False, 'error': 'zip not found'}
    if not target_base_dir:
        return {'ok': False, 'error': 'no target mods folder configured'}
    try:
        os.makedirs(target_base_dir, exist_ok=True)
    except OSError as e:
        return {'ok': False, 'error': f'cannot create mods folder: {e}'}

    try:
        with zipfile.ZipFile(zip_path, 'r') as zref:
            # Locate modinfo.json[c] anywhere in the archive
            mod_internal_path = None
            for fi in zref.infolist():
                low = fi.filename.lower()
                if low.endswith('modinfo.json') or low.endswith('modinfo.jsonc'):
                    mod_internal_path = os.path.dirname(fi.filename)
                    break
            if mod_internal_path is None:
                return {'ok': False, 'error': 'archive does not contain modinfo.json[c]'}

            folder_name = os.path.basename(mod_internal_path) \
                or os.path.basename(zip_path).rsplit('.', 1)[0]
            final_destination = os.path.join(target_base_dir, folder_name)

            if os.path.exists(final_destination) and not allow_overwrite:
                return {'ok': False, 'exists_already': True, 'folder': folder_name,
                        'error': 'mod already installed'}

            if os.path.exists(final_destination) and allow_overwrite:
                shutil.rmtree(final_destination)

            # Extract to a temp dir under the target so the cross-device move
            # is fast (rename), then promote the actual mod subfolder up.
            with tempfile.TemporaryDirectory(prefix='_modinstall_', dir=target_base_dir) as tmp:
                zref.extractall(tmp)
                src = os.path.join(tmp, mod_internal_path) if mod_internal_path else tmp
                if not os.path.isdir(src):
                    return {'ok': False, 'error': f'expected mod folder missing in archive: {mod_internal_path}'}
                shutil.move(src, final_destination)

            # Read the mod id back out of the freshly-installed file
            mod_id = ''
            for name in ('modinfo.json', 'modinfo.jsonc'):
                p = os.path.join(final_destination, name)
                if os.path.exists(p):
                    try:
                        with open(p, 'r', encoding='utf-8') as f:
                            raw = f.read()
                        if name.endswith('.jsonc'):
                            raw = _strip_jsonc(raw)
                        mod_id = str(json.loads(raw).get('ModID', ''))
                    except (OSError, ValueError):
                        pass
                    break

            return {'ok': True, 'mod_id': mod_id, 'folder': folder_name,
                    'exists_already': False}
    except zipfile.BadZipFile:
        return {'ok': False, 'error': 'not a valid ZIP archive'}
    except Exception as e:
        return {'ok': False, 'error': str(e)}
