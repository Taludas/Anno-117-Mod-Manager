"""Mod-tweaking helpers — read the schema from each mod's modinfo.json, and
read/write the user's chosen values in active-options.jsonc.

Schema shape (per option key under modinfo.json's ``Options`` block):

    {
      "label":   "Human-readable name",
      "type":    "enum" | "slider" | "toggle" | "text",
      "default": "<stringy default>",
      "values":  [...],     # enum: list of allowed values
                            # slider: [min, max, step]
      "labels":  [...]      # optional human hints, paired with values
    }

Stored values live as ``{ mod_id: { opt_key: value } }`` in
active-options.jsonc, written next to active-profile.txt.
"""
from __future__ import annotations

import json
import os
import re


def _strip_jsonc(text: str) -> str:
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'(?<!:)//.*', '', text)
    return text


def get_options_schema(mod_path: str) -> dict:
    """Return the ``Options`` block from a mod's modinfo.json[c], or {} if
    missing or unreadable."""
    if not mod_path:
        return {}
    for name in ('modinfo.json', 'modinfo.jsonc'):
        target = os.path.join(mod_path, name)
        if not os.path.exists(target):
            continue
        try:
            with open(target, 'r', encoding='utf-8') as f:
                raw = f.read()
            if name.endswith('.jsonc'):
                raw = _strip_jsonc(raw)
            data = json.loads(raw)
            opts = data.get('Options')
            return opts if isinstance(opts, dict) else {}
        except (OSError, ValueError):
            return {}
    return {}


def load_active_options(options_path: str) -> dict:
    """Read the on-disk active-options.jsonc into a dict-of-dicts."""
    if not options_path or not os.path.exists(options_path):
        return {}
    try:
        with open(options_path, 'r', encoding='utf-8') as f:
            raw = f.read()
        return json.loads(_strip_jsonc(raw)) or {}
    except (OSError, ValueError):
        return {}


def save_active_options(options_path: str, data: dict) -> tuple[bool, str]:
    """Persist the dict to active-options.jsonc."""
    if not options_path:
        return False, 'no options path'
    try:
        os.makedirs(os.path.dirname(options_path), exist_ok=True)
        with open(options_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True, ''
    except OSError as e:
        return False, str(e)


def set_option(options_path: str, mod_id: str, key: str, value) -> tuple[bool, str]:
    """Update a single option for a single mod and persist the file."""
    if not mod_id or not key:
        return False, 'missing mod_id or key'
    data = load_active_options(options_path)
    if mod_id not in data or not isinstance(data.get(mod_id), dict):
        data[mod_id] = {}
    data[mod_id][key] = value
    return save_active_options(options_path, data)


def reset_mod(options_path: str, mod_id: str) -> tuple[bool, str]:
    """Drop the entry for a single mod from active-options.jsonc."""
    if not mod_id:
        return False, 'missing mod_id'
    data = load_active_options(options_path)
    if mod_id in data:
        del data[mod_id]
        return save_active_options(options_path, data)
    return True, ''


def reset_all(options_path: str) -> tuple[bool, str]:
    """Delete the file entirely so every mod falls back to its defaults."""
    if not options_path or not os.path.exists(options_path):
        return True, ''
    try:
        os.remove(options_path)
        return True, ''
    except OSError as e:
        return False, str(e)


def merged_values(schema: dict, active: dict) -> dict:
    """For each option in ``schema``, return ``{key: current_value}`` where
    current_value is the user's saved value, falling back to the schema
    default. Used to render the form with the right initial values."""
    out = {}
    for key, spec in schema.items():
        if not isinstance(spec, dict):
            continue
        if key in active:
            out[key] = active[key]
        else:
            out[key] = spec.get('default', '')
    return out
