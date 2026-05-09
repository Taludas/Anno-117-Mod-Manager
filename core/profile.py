"""Pure functions to read and modify Anno 117's active-profile.txt.

Format reminder (per the in-game modloader):
    # comment line                ← ignored
    EnableNewMods                 ← directive: new mods auto-enabled
    # EnableNewMods               ← directive disabled
    some-mod-id                   ← mod is active
    # some-mod-id                 ← mod is disabled
    some-mod-id  # inline comment ← active, comment preserved
"""
from __future__ import annotations

import os
import re
import shutil

# Reserved preset names that are computed from current state rather than
# loaded from disk (used by the UI to render virtual entries in the dropdown).
RESERVED_PRESETS = ('Default', 'Vanilla')

# Preset filenames must look like a regular identifier — no path traversal,
# no hidden files, plain alphanumerics + dash/underscore/space.
_VALID_PRESET = re.compile(r'^[A-Za-z0-9 _\-]{1,64}$')


def is_valid_preset_name(name: str) -> bool:
    return bool(name) and bool(_VALID_PRESET.match(name)) and name not in RESERVED_PRESETS


def _safe_existing_preset(presets_dir: str, name: str) -> str | None:
    """Resolve presets/<name>.txt safely (no path traversal) and return the
    absolute path only if the file exists. Used by load/delete so a preset
    with a name the strict validator rejects (legacy or imported file) is
    still operable — the only real constraint is that it stays inside
    ``presets_dir`` and isn't a reserved virtual name."""
    if not name or name in RESERVED_PRESETS or not presets_dir:
        return None
    if '/' in name or '\\' in name or name in ('.', '..') or name.startswith('.'):
        return None
    base = os.path.realpath(presets_dir)
    candidate = os.path.realpath(os.path.join(presets_dir, f'{name}.txt'))
    if not candidate.startswith(base + os.sep):
        return None
    return candidate if os.path.isfile(candidate) else None


def list_presets(presets_dir: str) -> list[str]:
    """Return the names (without .txt) of user-saved presets in lexical order."""
    if not presets_dir or not os.path.isdir(presets_dir):
        return []
    out: list[str] = []
    try:
        for name in os.listdir(presets_dir):
            if name.lower().endswith('.txt'):
                out.append(name[:-4])
    except OSError:
        pass
    out.sort(key=str.lower)
    return out


def save_preset(presets_dir: str, profile_path: str, name: str) -> tuple[bool, str]:
    """Copy active-profile.txt → presets/<name>.txt."""
    if not is_valid_preset_name(name):
        return False, 'invalid preset name'
    if not profile_path or not os.path.exists(profile_path):
        return False, 'no active profile to save'
    try:
        os.makedirs(presets_dir, exist_ok=True)
        shutil.copy2(profile_path, os.path.join(presets_dir, f'{name}.txt'))
        return True, ''
    except OSError as e:
        return False, str(e)


def delete_preset(presets_dir: str, name: str) -> tuple[bool, str]:
    """Remove presets/<name>.txt. Accepts any name that resolves to an
    existing preset file inside ``presets_dir`` — useful for cleaning up
    legacy presets whose names the current strict validator rejects."""
    target = _safe_existing_preset(presets_dir, name)
    if not target:
        return False, 'preset not found'
    try:
        os.remove(target)
        return True, ''
    except OSError as e:
        return False, str(e)


def load_preset(presets_dir: str, profile_path: str, name: str, all_mod_ids: list[str]) -> tuple[bool, str]:
    """Apply a preset to active-profile.txt. Two reserved names short-circuit:
    'Vanilla' rewrites the profile with everything disabled, 'Default' enables
    every installed mod. For user presets we copy the file over but expand it
    so every currently-installed top-level mod has an explicit line — this
    avoids surprise activations by EnableNewMods."""
    if name == 'Vanilla':
        return write_set_all(profile_path, all_mod_ids, active=False)
    if name == 'Default':
        return write_set_all(profile_path, all_mod_ids, active=True)
    src = _safe_existing_preset(presets_dir, name)
    if not src:
        return False, 'preset not found'
    try:
        with open(src, 'r', encoding='utf-8') as f:
            preset_content = f.read()
        # Build the set of mod ids the preset marks as active
        preset_active: set[str] = set()
        for line in preset_content.splitlines():
            clean = line.strip()
            if not clean or clean.startswith('#'):
                continue
            tok = clean.split('#', 1)[0].strip().split()
            if not tok or tok[0] == 'EnableNewMods':
                continue
            preset_active.add(tok[0])
        # Rewrite profile with explicit lines for every installed mod
        os.makedirs(os.path.dirname(profile_path), exist_ok=True)
        out = [f'# Anno 117 Profile: {name}\n', '# EnableNewMods\n']
        seen: set[str] = set()
        for mid in all_mod_ids:
            if mid in seen:
                continue
            seen.add(mid)
            prefix = '' if mid in preset_active else '# '
            out.append(f'{prefix}{mid}\n')
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.writelines(out)
        return True, ''
    except OSError as e:
        return False, str(e)


def parse_enabled_ids(profile_path: str) -> set[str]:
    """Return the set of mod IDs whose line is uncommented in the file."""
    if not profile_path or not os.path.exists(profile_path):
        return set()
    enabled: set[str] = set()
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            for line in f:
                clean = line.strip()
                if not clean or clean.startswith('#'):
                    continue
                token = clean.split('#', 1)[0].strip().split()
                if not token:
                    continue
                tok = token[0]
                if tok == 'EnableNewMods':
                    continue
                enabled.add(tok)
    except OSError:
        pass
    return enabled


def is_enable_new_mods(profile_path: str) -> bool:
    """Whether the EnableNewMods directive is present and uncommented. When
    True, mods absent from the file are active by default."""
    if not profile_path or not os.path.exists(profile_path):
        # Default behaviour when no profile exists: include new mods.
        return True
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            for line in f:
                clean = line.strip()
                if 'EnableNewMods' in clean:
                    return not clean.startswith('#')
    except OSError:
        pass
    return False


def mod_id_appears(profile_path: str, mod_id: str) -> bool:
    """Whether ``mod_id`` is mentioned in the file (commented or not).
    Used together with EnableNewMods to decide the default active state."""
    if not profile_path or not os.path.exists(profile_path):
        return False
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            for line in f:
                clean = line.strip().lstrip('#').strip()
                tokens = clean.split('#', 1)[0].strip().split()
                if tokens and tokens[0] == mod_id:
                    return True
    except OSError:
        pass
    return False


def toggle_mod(profile_path: str, mod_id: str, should_be_active: bool) -> tuple[bool, str]:
    """Comment / uncomment ``mod_id``'s line in active-profile.txt. Creates
    the file with a stub header if it doesn't exist. Returns (ok, error)."""
    if not profile_path:
        return False, 'no profile path'
    try:
        os.makedirs(os.path.dirname(profile_path), exist_ok=True)
        if not os.path.exists(profile_path):
            with open(profile_path, 'w', encoding='utf-8') as f:
                f.write('# Anno 117 Active Profile\n')

        with open(profile_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        updated: list[str] = []
        found = False
        for line in lines:
            clean = line.strip()
            # Preserve blank lines and "##"-style header comments verbatim
            if not clean or clean.startswith('##'):
                updated.append(line)
                continue
            current = clean.lstrip('#').split('#', 1)[0].strip().split()
            current_id = current[0] if current else ''
            if current_id == mod_id:
                found = True
                inline = ''
                hash_idx = clean.find('#', 1)
                if hash_idx != -1:
                    inline = ' ' + clean[hash_idx:].strip()
                prefix = '' if should_be_active else '# '
                updated.append(f'{prefix}{mod_id}{inline}\n')
            else:
                updated.append(line)

        if not found:
            prefix = '' if should_be_active else '# '
            updated.append(f'{prefix}{mod_id}\n')

        with open(profile_path, 'w', encoding='utf-8') as f:
            f.writelines(updated)
        return True, ''
    except OSError as e:
        return False, str(e)


def parse_profile_order(profile_path: str) -> list[str]:
    """Return the list of mod IDs in the order they appear in
    active-profile.txt (active or commented). Header comments and the
    EnableNewMods directive are skipped. Used by the Load Order view."""
    if not profile_path or not os.path.exists(profile_path):
        return []
    out: list[str] = []
    seen: set[str] = set()
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            for line in f:
                clean = line.strip().lstrip('#').strip()
                if not clean:
                    continue
                tokens = clean.split('#', 1)[0].strip().split()
                if not tokens:
                    continue
                mid = tokens[0]
                if mid == 'EnableNewMods' or mid.startswith('Anno'):
                    continue
                if mid in seen:
                    continue
                seen.add(mid)
                out.append(mid)
    except OSError:
        pass
    return out


def reorder_profile(profile_path: str, ordered_ids: list[str]) -> tuple[bool, str]:
    """Rewrite active-profile.txt with mods in ``ordered_ids`` order while
    preserving each one's active/disabled state from the existing file.
    Mods present in the file but missing from ``ordered_ids`` are appended at
    the end so we never lose any state."""
    if not profile_path:
        return False, 'no profile path'
    try:
        os.makedirs(os.path.dirname(profile_path), exist_ok=True)
        # Read existing state per mod id
        active_by_id: dict[str, bool] = {}
        inline_by_id: dict[str, str] = {}
        header_lines: list[str] = []
        new_mods_directive_line = ''
        if os.path.exists(profile_path):
            with open(profile_path, 'r', encoding='utf-8') as f:
                for line in f:
                    clean = line.strip()
                    if not clean:
                        continue
                    if clean.startswith('##'):
                        header_lines.append(line)
                        continue
                    raw_token = clean.lstrip('#').split('#', 1)[0].strip().split()
                    raw_id = raw_token[0] if raw_token else ''
                    if raw_id == 'EnableNewMods':
                        new_mods_directive_line = line if line.endswith('\n') else line + '\n'
                        continue
                    if not raw_id or raw_id.startswith('Anno'):
                        # Single-# header / banner-style line — keep at top
                        if clean.startswith('#') and raw_id and raw_id.startswith('Anno'):
                            header_lines.append(line)
                        continue
                    is_active = not clean.startswith('#')
                    inline = ''
                    h = clean.find('#', 1)
                    if h != -1:
                        inline = ' ' + clean[h:].strip()
                    active_by_id[raw_id] = is_active
                    inline_by_id[raw_id] = inline

        # Compose the new file
        out: list[str] = []
        out.extend(header_lines)
        if not header_lines:
            out.append('# Anno 117 Active Profile\n')
        out.append(new_mods_directive_line or '# EnableNewMods\n')

        seen: set[str] = set()
        for mid in ordered_ids:
            if mid in seen:
                continue
            seen.add(mid)
            active = active_by_id.get(mid, True)  # newcomers default to active
            inline = inline_by_id.get(mid, '')
            prefix = '' if active else '# '
            out.append(f'{prefix}{mid}{inline}\n')
        # Append any leftover mods not in ordered_ids so we don't drop state
        for mid, active in active_by_id.items():
            if mid in seen:
                continue
            seen.add(mid)
            inline = inline_by_id.get(mid, '')
            prefix = '' if active else '# '
            out.append(f'{prefix}{mid}{inline}\n')

        with open(profile_path, 'w', encoding='utf-8') as f:
            f.writelines(out)
        return True, ''
    except OSError as e:
        return False, str(e)


def write_set_all(profile_path: str, mod_ids: list[str], active: bool) -> tuple[bool, str]:
    """Rewrite the profile from scratch with one explicit line per mod id,
    either all active or all commented out. Sub-mods (parent_path) should be
    excluded by the caller — the loader handles them via the parent."""
    if not profile_path:
        return False, 'no profile path'
    try:
        os.makedirs(os.path.dirname(profile_path), exist_ok=True)
        header = '# Anno 117 Default Profile\n' if active else '# Anno 117 No Mods Active Profile\n'
        new_mods = 'EnableNewMods\n' if active else '# EnableNewMods\n'
        out = [header, new_mods]
        seen: set[str] = set()
        for mid in mod_ids:
            if mid in seen:
                continue
            seen.add(mid)
            prefix = '' if active else '# '
            out.append(f'{prefix}{mid}\n')
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.writelines(out)
        return True, ''
    except OSError as e:
        return False, str(e)


