"""Mod scanner. Reads modinfo.json[c] under the configured mod roots and
returns enriched dicts the JS bridge can consume directly."""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field, asdict

from . import files as files_module
from . import paths as paths_module

# Maps the app's UI-language keys to the language keys modinfo.json uses
# (Portugese / Chinese / Taiwanese — yes, with those exact spellings).
_MODINFO_LANG_MAP = {
    'english': 'English',
    'german': 'German',
    'french': 'French',
    'spanish': 'Spanish',
    'italian': 'Italian',
    'polish': 'Polish',
    'russian': 'Russian',
    'brazilian': 'Portugese',
    'japanese': 'Japanese',
    'korean': 'Korean',
    'simplified_chinese': 'Chinese',
    'traditional_chinese': 'Taiwanese',
}


@dataclass
class Mod:
    id: str
    name: str
    category: str
    version: str
    description: str
    creator: str
    path: str
    parent_path: str = ''
    active: bool = False
    has_options: bool = False
    difficulty: str = 'Normal'
    deps_require: list[str] = field(default_factory=list)
    deps_incompatible: list[str] = field(default_factory=list)
    folder: str = ''            # basename of `path` for convenience on the JS side
    size_bytes: int = 0
    banner: str = ''            # filename of the local banner if found, else ''


def _strip_jsonc_comments(text: str) -> str:
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'(?<!:)//.*', '', text)
    return text


def _localized(value, lang_key: str, default: str = '') -> str:
    if isinstance(value, dict):
        return value.get(lang_key) or value.get('English') or default
    if isinstance(value, str):
        return value
    return default


def _scan_one(path: str, lang_key: str, parent_path: str = '') -> Mod | None:
    if os.path.basename(path).startswith('-'):
        return None
    info_json = os.path.join(path, 'modinfo.json')
    info_jsonc = os.path.join(path, 'modinfo.jsonc')
    target = info_json if os.path.exists(info_json) else (info_jsonc if os.path.exists(info_jsonc) else None)
    if not target:
        return None
    try:
        with open(target, 'r', encoding='utf-8') as f:
            raw = f.read()
        if target.endswith('.jsonc'):
            raw = _strip_jsonc_comments(raw)
        data = json.loads(raw)
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    mid = data.get('ModID')
    if not mid:
        return None
    deps_raw = data.get('Dependencies')
    deps = deps_raw if isinstance(deps_raw, dict) else {}
    return Mod(
        id=str(mid),
        name=_localized(data.get('ModName'), lang_key, default=str(mid)),
        category=_localized(data.get('Category'), lang_key, default=''),
        version=str(data.get('Version', '1.0.0')),
        description=_localized(data.get('Description'), lang_key, default=''),
        creator=str(data.get('CreatorName', '')),
        path=path,
        parent_path=parent_path,
        has_options=bool(data.get('Options')),
        difficulty=str(data.get('Difficulty', 'Normal')),
        deps_require=list(deps.get('Require', []) or []),
        deps_incompatible=list(deps.get('Incompatible', []) or []),
    )


def list_mods(game_exe_path: str = '', custom_docs: str = '', lang: str = 'english') -> list[dict]:
    """Scan the configured mod roots and return a flat list of enriched mod
    dicts. Each top-level mod folder is parsed once; nested sub-mods become
    entries with a populated ``parent_path``. Folder names starting with '-'
    are treated as disabled (ignored) — same convention the Tk version uses."""
    lang_key = _MODINFO_LANG_MAP.get(lang, 'English')
    roots: list[str] = []
    for r in (paths_module.documents_mods_root(custom_docs),
              paths_module.game_mods_root(game_exe_path)):
        if r and os.path.isdir(r) and r not in roots:
            roots.append(r)

    seen_folders: set[str] = set()
    out: list[Mod] = []
    for base in roots:
        try:
            for entry in os.scandir(base):
                if not entry.is_dir() or entry.name.startswith('.') or entry.name.startswith('-'):
                    continue
                if entry.name in seen_folders:
                    continue
                seen_folders.add(entry.name)
                mod = _scan_one(entry.path, lang_key)
                if mod:
                    out.append(mod)
                # Descend into sub-mods (one level)
                try:
                    for sub in os.scandir(entry.path):
                        if sub.is_dir():
                            child = _scan_one(sub.path, lang_key, parent_path=entry.path)
                            if child:
                                out.append(child)
                except OSError:
                    pass
        except OSError:
            continue

    # Enrich with folder name, size and banner before serialising
    for m in out:
        m.folder = os.path.basename(m.path)
        m.size_bytes = files_module.dir_size_bytes(m.path)
        m.banner = files_module.find_banner(m.path)
    return [asdict(m) for m in out]
