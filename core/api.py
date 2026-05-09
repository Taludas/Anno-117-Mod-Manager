"""Python API exposed to JavaScript via pywebview.

Methods on this class are callable from the frontend as
``window.pywebview.api.method_name(...)`` and return Promises in JS.

This is a thin JSON-friendly façade over the pure functions in
``core.{mods, profile, files, launcher, paths}``. The legacy Tk app
(anno117-modmanager.py) calls into the same modules — so logic only lives
once and a fix benefits both UIs.
"""
from __future__ import annotations

import base64
import json
import mimetypes
import os
import platform
import tempfile
from typing import Any

from . import files as files_module
from . import i18n as i18n_module
from . import installer as installer_module
from . import launcher as launcher_module
from . import modio as modio_module
from . import mods as mods_module
from . import news as news_module
from . import options as options_module
from . import paths as paths_module
from . import profile as profile_module

IS_WINDOWS = platform.system() == 'Windows'


def _appdata_dir() -> str:
    if IS_WINDOWS:
        root = os.getenv('APPDATA') or os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')
    else:
        root = os.getenv('XDG_CONFIG_HOME') or os.path.join(os.path.expanduser('~'), '.config')
    return os.path.join(root, 'Anno 117 Mod Manager')


class Api:
    def __init__(self) -> None:
        self.appdata = _appdata_dir()
        self.settings_file = os.path.join(self.appdata, 'settings.json')
        self.presets_dir = os.path.join(self.appdata, 'presets')
        self.settings: dict[str, Any] = self._load_settings()
        # Set by app.py once the window exists; needed for create_file_dialog.
        self.window: Any = None
        # In-memory news cache so repeated tab opens don't re-fetch.
        self._news_cache: dict[str, Any] = {'items': [], 'fetched_at': 0.0, 'key': None}

    # ── settings ──────────────────────────────────────────────────────────────
    def _load_settings(self) -> dict[str, Any]:
        if not os.path.exists(self.settings_file):
            return {}
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}

    def get_settings(self) -> dict[str, Any]:
        return self.settings

    def _save_settings(self) -> tuple[bool, str]:
        """Persist self.settings to disk. Returns (ok, error)."""
        try:
            os.makedirs(self.appdata, exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            return True, ''
        except OSError as e:
            return False, str(e)

    def update_setting(self, key: str, value: Any) -> dict:
        """Update a single key in settings.json (used for small toggles like
        selected_language). For more complex updates use the dedicated
        endpoints (toggle_mod, save_preset, etc.)."""
        # Whitelist what JS can write so a stray bridge call can't pollute
        # arbitrary keys (game_path stays managed by browse_game_path etc.).
        # Only what the new pywebview UI actually writes — the legacy Tk
        # whitelist had a handful of settings (jump_to_activation,
        # show_tooltips, use_mod_browser, modio_declined, last_seen_news_ts)
        # that nothing in frontend/ ever calls update_setting() with.
        allowed = {
            'selected_language', 'show_reddit_news', 'enable_new_mods',
            'mod_location_mode', 'modio_api_key', 'active_profile_name',
            'browser_subscribed_only', 'browser_followed_only',
            'text_scale',
        }
        if key not in allowed:
            return {'ok': False, 'error': f'setting not writable from UI: {key}'}
        self.settings[key] = value
        ok, err = self._save_settings()
        return {'ok': ok, 'error': err}

    # ── settings (paths) ──────────────────────────────────────────────────────
    def pick_folder(self, title: str = '') -> str:
        """Open the OS native folder picker. Returns the chosen path or ''
        if cancelled. The pywebview window must be set first (app.py wires it)."""
        if not self.window:
            return ''
        try:
            import webview
            result = self.window.create_file_dialog(
                webview.FOLDER_DIALOG,
                directory=os.path.expanduser('~'),
                allow_multiple=False,
            )
        except Exception:
            return ''
        if not result:
            return ''
        return result[0] if isinstance(result, (list, tuple)) else str(result)

    def pick_file(self, title: str = '', file_types: list[str] | None = None) -> str:
        """Open the OS native file picker. ``file_types`` is a list of
        pywebview filter strings like 'Anno executable (*.exe)'."""
        if not self.window:
            return ''
        try:
            import webview
            result = self.window.create_file_dialog(
                webview.OPEN_DIALOG,
                directory=os.path.expanduser('~'),
                allow_multiple=False,
                file_types=tuple(file_types or ()),
            )
        except Exception:
            return ''
        if not result:
            return ''
        return result[0] if isinstance(result, (list, tuple)) else str(result)

    def set_game_path(self, path: str) -> dict:
        """Validate that the path points at Anno117.exe (or a folder containing
        it) and persist it to settings.json. Returns {ok, path, error}."""
        if not path:
            return {'ok': False, 'error': 'empty path'}
        candidate = os.path.realpath(path)
        # If it's a directory, look for the exe inside it
        if os.path.isdir(candidate):
            for sub in (
                os.path.join(candidate, 'Bin', 'Win64', 'Anno117.exe'),
                os.path.join(candidate, 'Anno 117 - Pax Romana', 'Bin', 'Win64', 'Anno117.exe'),
                os.path.join(candidate, 'Anno117.exe'),
            ):
                if os.path.isfile(sub):
                    candidate = sub
                    break
            else:
                return {'ok': False, 'error': 'no Anno117.exe found inside that folder'}
        if not os.path.isfile(candidate) or not candidate.lower().endswith('anno117.exe'):
            return {'ok': False, 'error': 'not a valid Anno117.exe path'}
        self.settings['game_path'] = candidate
        ok, err = self._save_settings()
        return {'ok': ok, 'path': candidate, 'error': err}

    def detect_game_path(self) -> dict:
        """Run the cross-platform find_anno_exe and persist the result."""
        found = paths_module.find_anno_exe()
        if not found:
            return {'ok': False, 'error': 'Anno117.exe not found on this machine'}
        return self.set_game_path(found)

    def set_custom_docs_path(self, path: str) -> dict:
        """Persist (or clear if empty) the override for the Anno 117 documents
        folder. The override should point at the directory that *contains*
        ``Anno 117 - Pax Romana``."""
        if not path:
            self.settings['custom_docs_path'] = ''
            ok, err = self._save_settings()
            return {'ok': ok, 'path': '', 'error': err}
        path = os.path.realpath(path)
        if not os.path.isdir(path):
            return {'ok': False, 'error': 'path is not a directory'}
        self.settings['custom_docs_path'] = path
        ok, err = self._save_settings()
        return {'ok': ok, 'path': path, 'error': err}

    def get_paths_info(self) -> dict:
        """Return everything the Settings tab needs to display: configured
        paths, whether they exist, the resolved mods + active-profile paths."""
        game = self.settings.get('game_path', '')
        docs = self.settings.get('custom_docs_path', '')
        return {
            'game_path': game,
            'game_path_exists': bool(game) and os.path.isfile(game),
            'custom_docs_path': docs,
            'custom_docs_path_exists': bool(docs) and os.path.isdir(docs),
            'documents_mods_root': paths_module.documents_mods_root(docs),
            'game_mods_root': paths_module.game_mods_root(game),
            'active_profile_path': self._active_profile_path(),
            'appdata_dir': self.appdata,
            'presets_dir': self.presets_dir,
        }

    # ── i18n ──────────────────────────────────────────────────────────────────
    def get_languages(self) -> list[dict]:
        """Return all supported languages with their key, native name, flag."""
        return [
            {'key': l.key, 'name': l.name, 'flag': l.flag, 'flag_code': l.flag_code}
            for l in i18n_module.LANGUAGES
        ]

    def detect_language(self) -> str:
        """Best-effort guess at the system language. Returns a key."""
        return i18n_module.detect_system_lang()

    def get_language(self) -> str:
        """Return the currently selected language key (or detected one if
        nothing is saved yet)."""
        saved = self.settings.get('selected_language')
        if saved and i18n_module.is_known(saved):
            return saved
        return i18n_module.detect_system_lang()

    def set_language(self, key: str) -> dict:
        """Persist the user's language choice to settings.json."""
        if not i18n_module.is_known(key):
            return {'ok': False, 'error': f'unknown language: {key}'}
        return self.update_setting('selected_language', key)

    # ── mods ──────────────────────────────────────────────────────────────────
    def list_mods(self) -> list[dict]:
        """Scan mod folders and return enriched mod dicts (active flag included)."""
        game_path = self.settings.get('game_path', '')
        custom_docs = self.settings.get('custom_docs_path', '')
        lang = self.settings.get('selected_language', 'english')
        mods = mods_module.list_mods(game_exe_path=game_path, custom_docs=custom_docs, lang=lang)

        profile_path = self._active_profile_path()
        enabled_ids = profile_module.parse_enabled_ids(profile_path)
        enable_new = profile_module.is_enable_new_mods(profile_path)
        for mod in mods:
            mid = mod['id']
            if mid in enabled_ids:
                mod['active'] = True
            elif enable_new and not profile_module.mod_id_appears(profile_path, mid):
                mod['active'] = True
            else:
                mod['active'] = False
        return mods

    def toggle_mod(self, mod_id: str, should_be_active: bool) -> dict:
        """Comment / uncomment ``mod_id`` in active-profile.txt."""
        ok, err = profile_module.toggle_mod(self._active_profile_path(), mod_id, should_be_active)
        return {'ok': ok, 'active': should_be_active, 'error': err}

    def set_all_active(self, active: bool) -> dict:
        """Bulk activate or deactivate every installed top-level mod."""
        # Sub-mods are handled by the loader via the parent — only list ids of
        # top-level mods.
        ids = [m['id'] for m in self.list_mods() if not m.get('parent_path')]
        ok, err = profile_module.write_set_all(self._active_profile_path(), ids, active)
        return {'ok': ok, 'error': err}

    def uninstall_mod(self, folder: str) -> dict:
        """Delete a mod folder. ``folder`` must be a basename (no slashes)
        and we restrict the rmtree to the configured mod roots so a malicious
        JS payload can't delete anything outside them."""
        if not folder or '/' in folder or '\\' in folder or folder.startswith('.'):
            return {'ok': False, 'error': 'invalid folder name'}
        roots = self._mod_roots()
        # Find the actual location and delegate to safe_rmtree
        for root in roots:
            candidate = os.path.join(root, folder)
            if os.path.isdir(candidate):
                ok, err = files_module.safe_rmtree(candidate, roots)
                return {'ok': ok, 'error': err}
        return {'ok': False, 'error': f'folder not found: {folder}'}

    def open_path(self, path: str) -> dict:
        """Open a file, folder or URL. URLs go through Python's webbrowser
        module (more reliable than xdg-open for https://) so news cards
        always land in the user's default browser; local paths still use
        the xdg-open / startfile / open chain."""
        if not path:
            return {'ok': False, 'error': 'path missing'}
        if path.startswith(('http://', 'https://')):
            try:
                import webbrowser
                webbrowser.open_new_tab(path)
                return {'ok': True}
            except Exception as e:
                return {'ok': False, 'error': str(e)}
        ok, err = files_module.open_path(path)
        return {'ok': ok, 'error': err}

    def open_mods_folder(self) -> dict:
        """Open the primary mods folder (Documents-side first, fall back to
        the game install dir)."""
        for root in self._mod_roots():
            return self.open_path(root)
        return {'ok': False, 'error': 'no mods folder configured'}

    def get_mod_banner(self, mod_id: str) -> dict:
        """Return the mod's local banner (banner.png / thumbnail.jpg) as a
        base64 data URL. Capped at ~5 MB to keep the bridge call light."""
        for m in self.list_mods():
            if m['id'] != mod_id:
                continue
            banner_name = m.get('banner') or ''
            if not banner_name:
                return {'ok': True, 'data_url': ''}
            full = os.path.join(m['path'], banner_name)
            if not os.path.isfile(full):
                return {'ok': True, 'data_url': ''}
            try:
                if os.path.getsize(full) > 5 * 1024 * 1024:
                    return {'ok': False, 'error': 'banner too large'}
                with open(full, 'rb') as f:
                    raw = f.read()
                mime, _ = mimetypes.guess_type(full)
                mime = mime or 'image/png'
                return {'ok': True, 'data_url': f'data:{mime};base64,{base64.b64encode(raw).decode()}'}
            except OSError as e:
                return {'ok': False, 'error': str(e)}
        return {'ok': False, 'error': 'mod not found'}

    # ── mod.io OAuth ──────────────────────────────────────────────────────────
    def modio_status(self) -> dict:
        """Return what the UI needs to render the connection state: whether
        an API key is set, whether we hold a non-expired bearer token, and
        the human-readable expiry date."""
        import datetime as _dt
        api_key = bool(self.settings.get('modio_api_key'))
        token = self.settings.get('modio_token', '')
        expires = int(self.settings.get('modio_token_expires') or 0)
        valid = bool(token) and modio_module.is_token_valid(expires)
        expiry_text = ''
        if expires:
            try:
                expiry_text = _dt.datetime.fromtimestamp(expires).strftime('%Y-%m-%d %H:%M')
            except Exception:
                pass
        return {
            'api_key_set': api_key,
            'has_token': bool(token),
            'token_valid': valid,
            'expires_ts': expires,
            'expires_text': expiry_text,
            'terms_agreed': bool(self.settings.get('modio_terms_agreed', False)),
        }

    def modio_email_request(self, email: str) -> dict:
        """Step 1 of OAuth: ask mod.io to send a security code by email."""
        api_key = self.settings.get('modio_api_key', '')
        return modio_module.email_request(api_key, email)

    def modio_email_exchange(self, code: str, terms_agreed: bool) -> dict:
        """Step 2: trade the security code for a bearer token, then persist."""
        api_key = self.settings.get('modio_api_key', '')
        res = modio_module.email_exchange(api_key, code, bool(terms_agreed))
        if not res.get('ok'):
            # 11074 means terms updated server-side; reset our local flag so
            # the UI re-collects agreement on the next attempt.
            if res.get('error_ref') == modio_module.ERR_TERMS_UPDATED:
                self.settings['modio_terms_agreed'] = False
                self._save_settings()
            return res
        self.settings['modio_token'] = res['access_token']
        self.settings['modio_token_expires'] = res['date_expires']
        self.settings['modio_terms_agreed'] = bool(terms_agreed)
        self._save_settings()
        # Drop the news cache so the next refresh picks up the mod.io feeds
        # that previously needed a token to work.
        self._news_cache = {'items': [], 'fetched_at': 0.0, 'key': None}
        return {'ok': True, 'expires_ts': res['date_expires']}

    def modio_disconnect(self) -> dict:
        """Forget the bearer token (keeps the API key around — disconnect ≠
        clearing the user's mod.io account binding)."""
        self.settings['modio_token'] = ''
        self.settings['modio_token_expires'] = 0
        ok, err = self._save_settings()
        return {'ok': ok, 'error': err}

    # ── mod.io browsing ───────────────────────────────────────────────────────
    def _modio_token(self) -> str:
        """Return a still-valid bearer token, or '' if the user must re-auth.
        Browsing endpoints uniformly return {ok: False, error: 'not authenticated'}
        when this is empty, so the UI can prompt for a reconnect."""
        token = self.settings.get('modio_token', '')
        expires = int(self.settings.get('modio_token_expires') or 0)
        return token if token and modio_module.is_token_valid(expires) else ''

    def modio_browse(self, search: str = '', tags: list[str] | None = None,
                     limit: int = 30, offset: int = 0,
                     sort: str = '-date_updated',
                     submitted_by: int = 0,
                     collections: bool = False) -> dict:
        """Paginated mod or collection search. Frontend passes the search
        string + optional tag list + optional author; we forward to mod.io
        and return the raw page envelope. ``collections`` flips the URL
        to mod.io's dedicated /collections endpoint."""
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        return modio_module.list_mods(token, search=search, tags=tags or None,
                                      submitted_by=int(submitted_by or 0),
                                      collections=bool(collections),
                                      limit=int(limit), offset=int(offset), sort=sort)

    def modio_get(self, mod_id: int, collection: bool = False) -> dict:
        """Full mod or collection record (description_plaintext, modfile,
        media, etc.). ``collection=True`` flips the URL to /collections."""
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        return modio_module.get_mod(token, int(mod_id), collection=bool(collection))

    def modio_dependencies(self, mod_id: int, collection: bool = False) -> dict:
        """Mods bundled by ``mod_id`` (its dependencies). The Browser uses
        this to render the "Mods inclus" list on a collection's detail page."""
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        return modio_module.list_dependencies(token, int(mod_id),
                                              collection=bool(collection))

    # ── collection follow ─────────────────────────────────────────────────
    def modio_follow_collection(self, name_id: str) -> dict:
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        return modio_module.follow_collection(token, str(name_id or ''))

    def modio_unfollow_collection(self, name_id: str) -> dict:
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        return modio_module.unfollow_collection(token, str(name_id or ''))

    def modio_followed_collections(self, search: str = '',
                                   limit: int = 100, offset: int = 0,
                                   sort: str = '') -> dict:
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        return modio_module.list_followed_collections(
            token, search=search, limit=int(limit),
            offset=int(offset), sort=sort)

    def modio_check_updates(self, ids: list[int]) -> dict:
        """Return the current modfile_id for each mod_id passed. The
        Activation tab calls this once on boot to decide which rows
        can offer an Update icon (compared against the local
        _modio_install.json marker)."""
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        return modio_module.check_updates(token, [int(i) for i in (ids or [])])

    def modio_subscribed(self, search: str = '',
                         limit: int = 100, offset: int = 0,
                         sort: str = '') -> dict:
        """List of subscribed mods (Anno-117-scoped). Default args (no
        search, _limit=100) match the original "membership cache" use the
        Browser does on cold start to flag rows in its main listing.
        With explicit args it doubles as the data source for the
        "My Subscriptions" filter — same response shape as modio_browse
        so the frontend can swap endpoints transparently."""
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        return modio_module.list_subscribed(token, search=search,
                                            limit=int(limit),
                                            offset=int(offset),
                                            sort=sort)

    def modio_tags(self) -> dict:
        """List of tag groups defined for Anno 117 — feeds the Browser's
        filter-by-tag dropdown so the choices match what the game actually
        exposes (no hard-coded list to drift out of sync)."""
        api_key = self.settings.get('modio_api_key', '')
        return modio_module.list_game_tags(api_key)

    def modio_my_ratings(self) -> dict:
        """Per-mod rating cast by this user — what the Browser uses to
        light up the heart on mods already endorsed (the mod summary
        doesn't include user_rating, only /me/ratings does)."""
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        return modio_module.list_my_ratings(token)

    def modio_installed_ids(self) -> dict:
        """Walk every installed mod folder and read its ``_modio_install.json``
        marker (written by ``modio_install_mod``) to build the live set of
        mod.io IDs currently on disk. Self-healing: a manual rm -rf of the
        folder takes the marker with it, so the Browser instantly stops
        showing "Installed" for that mod — no stale settings to clean up.

        Also returns a ``meta`` dict {mod_id: {modfile_id, version}} the
        Browser uses to compare the installed modfile against the latest
        available on mod.io, so the CTA only flips to "Update" when there
        actually IS a newer modfile (otherwise it stays "Installed")."""
        ids: list[int] = []
        meta_map: dict[int, dict] = {}
        try:
            for m in self.list_mods():
                folder = m.get('path') or ''
                if not folder:
                    continue
                meta_path = os.path.join(folder, '_modio_install.json')
                if not os.path.isfile(meta_path):
                    continue
                try:
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        meta = json.load(f) or {}
                except (OSError, ValueError):
                    continue
                mid = meta.get('mod_id')
                if isinstance(mid, int) and mid > 0:
                    ids.append(mid)
                    meta_map[mid] = {
                        'modfile_id': int(meta.get('modfile_id') or 0),
                        'version': str(meta.get('version') or ''),
                        # basename of the mod folder so the Browser's Uninstall
                        # button can call uninstall_mod(folder) without an
                        # extra round-trip to look it up.
                        'folder': os.path.basename(folder),
                    }
        except Exception as e:
            return {'ok': False, 'error': str(e), 'ids': [], 'meta': {}}
        return {'ok': True, 'ids': ids, 'meta': meta_map}

    def modio_subscribe(self, mod_id: int) -> dict:
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        return modio_module.subscribe(token, int(mod_id))

    def modio_unsubscribe(self, mod_id: int) -> dict:
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        return modio_module.unsubscribe(token, int(mod_id))

    def modio_endorse(self, mod_id: int, positive: bool) -> dict:
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        return modio_module.endorse(token, int(mod_id), bool(positive))

    def modio_uninstall_collection(self, collection_id: int,
                                   also_remove_mods: bool = False) -> dict:
        """Reverse modio_install_collection. Always deletes the preset
        named after the collection. When ``also_remove_mods`` is True,
        also wipes every mod folder that was bundled in the collection
        (resolved live via the /collections/{id}/mods endpoint, then
        matched against the local install via the mod.io ID stored in
        each mod folder's _modio_install.json marker).

        Returns:
          {ok, profile_name, profile_removed, mods_removed: [folders]}"""
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}

        # 1. Resolve the collection name to find which preset to drop.
        coll_res = modio_module.get_mod(token, int(collection_id), collection=True)
        if not coll_res.get('ok'):
            return coll_res
        coll = coll_res.get('mod') or {}
        collection_name = (coll.get('name') or '').strip() or f'Collection {collection_id}'
        safe_name = modio_module.collection_preset_name(collection_name, int(collection_id))

        # 2. Optionally fetch the bundled mod IDs to know what to wipe.
        mods_to_wipe: list[int] = []
        if also_remove_mods:
            deps = modio_module.list_dependencies(token, int(collection_id),
                                                  collection=True)
            if deps.get('ok'):
                for m in (deps.get('data') or []):
                    mid = int(m.get('id') or 0)
                    if mid:
                        mods_to_wipe.append(mid)

        # 3. Wipe each mod folder whose _modio_install.json marker matches
        #    a wanted ID. The folder + marker disappear together.
        removed_folders: list[str] = []
        if mods_to_wipe:
            wipe_set = set(mods_to_wipe)
            for m in self.list_mods():
                folder = m.get('path') or ''
                if not folder or not os.path.isdir(folder):
                    continue
                meta_path = os.path.join(folder, '_modio_install.json')
                if not os.path.isfile(meta_path):
                    continue
                try:
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        meta = json.load(f) or {}
                except (OSError, ValueError):
                    continue
                mid = meta.get('mod_id')
                if not isinstance(mid, int) or mid not in wipe_set:
                    continue
                # Build the allowed-roots list the same way uninstall_mod does
                roots: list[str] = []
                custom_docs = self.settings.get('custom_docs_path', '')
                game_path = self.settings.get('game_path', '')
                gmr = paths_module.game_mods_root(game_path) if game_path else ''
                dmr = paths_module.documents_mods_root(custom_docs)
                if gmr: roots.append(gmr)
                if dmr: roots.append(dmr)
                ok, _err = files_module.safe_rmtree(folder, roots)
                if ok:
                    removed_folders.append(os.path.basename(folder))

        # 4. Drop the preset file (no error if it doesn't exist anymore —
        #    user may have already deleted it from Activation).
        preset_path = os.path.join(self.presets_dir, f'{safe_name}.txt')
        profile_removed = False
        if os.path.isfile(preset_path):
            try:
                os.remove(preset_path)
                profile_removed = True
            except OSError:
                pass

        # 5. If the active profile was this preset, switch back to Default
        #    so the Activation tab doesn't reference a now-missing file.
        # (Reading active-profile.txt is overkill — the dropdown will just
        # re-render from list_presets which no longer includes it.)

        return {
            'ok': True,
            'profile_name': safe_name,
            'profile_removed': profile_removed,
            'mods_removed': removed_folders,
        }

    def modio_install_collection(self, collection_id: int) -> dict:
        """Install every mod a collection bundles, then create + activate a
        new preset named after the collection that has only those mods on.

        Returns:
          {ok, profile_name, total, installed, failed: [{name, error}]}

        ``Default`` and ``Vanilla`` are reserved preset names — if a
        collection is called either, we fall back to ``Collection_<id>``."""
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}

        # 1. Resolve the collection record (we need its name, even if it
        #    fails on a couple of bundled mods we still want a sensible
        #    preset to land in).
        coll_res = modio_module.get_mod(token, int(collection_id), collection=True)
        if not coll_res.get('ok'):
            return coll_res
        coll = coll_res.get('mod') or {}
        collection_name = (coll.get('name') or '').strip() or f'Collection {collection_id}'

        # 2. List the bundled mods.
        deps_res = modio_module.list_dependencies(token, int(collection_id), collection=True)
        if not deps_res.get('ok'):
            return deps_res
        bundled = deps_res.get('data') or []
        if not bundled:
            return {'ok': False, 'error': 'collection lists no bundled mods'}

        # 3. Install each one. Collect the *local* ModID parsed from
        #    modinfo.json — that's what active-profile.txt references,
        #    not the mod.io numeric ID.
        installed_local_ids: list[str] = []
        failed: list[dict] = []
        for m in bundled:
            mid = int(m.get('id') or 0)
            if not mid:
                continue
            res = self.modio_install_mod(mid)
            if res.get('ok'):
                local_id = str(res.get('mod_id') or '').strip()
                if local_id and local_id not in installed_local_ids:
                    installed_local_ids.append(local_id)
            else:
                failed.append({
                    'name': m.get('name', f'mod {mid}'),
                    'error': str(res.get('error') or 'unknown'),
                })

        # 4. Sanitise the preset name (matches what is_valid_preset_name
        #    accepts and what the JS frontend mirrors in
        #    _collectionPresetName so the "already installed" badge stays
        #    in sync).
        safe_name = modio_module.collection_preset_name(collection_name, int(collection_id))

        # 5. Write the preset file directly (one mod_id per line + the
        #    EnableNewMods sentinel) — no need to round-trip through
        #    save_preset which only copies the active profile.
        try:
            os.makedirs(self.presets_dir, exist_ok=True)
            preset_path = os.path.join(self.presets_dir, f'{safe_name}.txt')
            with open(preset_path, 'w', encoding='utf-8') as f:
                for mid in installed_local_ids:
                    f.write(f'{mid}\n')
                # Don't auto-enable mods that aren't in the collection
                f.write('EnableNewMods false\n')
        except OSError as e:
            return {
                'ok': False,
                'error': f'cannot write preset: {e}',
                'profile_name': safe_name,
                'installed': len(installed_local_ids),
                'total': len(bundled),
                'failed': failed,
            }

        # 6. Apply the preset to the active profile so the user lands
        #    straight on the collection.
        profile_path = self._active_profile_path()
        all_ids = [m['id'] for m in self.list_mods()]
        profile_module.load_preset(self.presets_dir, profile_path,
                                   safe_name, all_ids)

        return {
            'ok': True,
            'profile_name': safe_name,
            'total': len(bundled),
            'installed': len(installed_local_ids),
            'failed': failed,
        }

    def modio_link_mod(self, folder: str, mod_id: int) -> dict:
        """Manually associate an existing local mod folder with a mod.io
        record by writing the same _modio_install.json marker that an
        install through the manager would have produced. Used by the
        Activation tab's link picker for mods the user dropped in by
        hand: from there on they get version-aware Update / Uninstall /
        auto-subscribe like any managed mod. Doesn't touch the mod's own
        files — only adds the marker. Auto-subscribes too so the
        association mirrors an in-app install."""
        if not folder or '/' in folder or '\\' in folder or folder.startswith('.'):
            return {'ok': False, 'error': 'invalid folder name'}
        if not mod_id:
            return {'ok': False, 'error': 'mod_id required'}
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        roots = self._mod_roots()
        target_path = None
        for root in roots:
            candidate = os.path.join(root, folder)
            if os.path.isdir(candidate):
                target_path = candidate
                break
        if not target_path:
            return {'ok': False, 'error': f'folder not found: {folder}'}
        res = modio_module.get_mod(token, int(mod_id))
        if not res.get('ok'):
            return res
        mod = res.get('mod') or {}
        modfile = mod.get('modfile') or {}
        meta = {
            'mod_id': int(mod_id),
            'name_id': (mod.get('name_id') or ''),
            'name': (mod.get('name') or ''),
            'modfile_id': int(modfile.get('id') or 0),
            'version': str(modfile.get('version') or ''),
            'installed_at': int(__import__('time').time()),
            # Distinguishes a marker written by a manual link from one
            # written by an actual install — purely informational, the
            # rest of the app treats them identically.
            'linked': True,
        }
        meta_path = os.path.join(target_path, '_modio_install.json')
        try:
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
        except OSError as e:
            return {'ok': False, 'error': str(e)}
        try:
            modio_module.subscribe(token, int(mod_id))
        except Exception:
            pass
        return {'ok': True, 'name': mod.get('name') or ''}

    def modio_auto_link_unmarked(self) -> dict:
        """Walk every local mod folder that has no _modio_install.json
        marker, read modinfo.json's ModID, batch-look up matching mod.io
        records by name_id, and write a marker for each STRICT match
        (mod.io.name_id == modinfo.ModID, case-insensitive). Mods whose
        author-chosen ModID slug doesn't match the mod.io slug are left
        untouched — the user can still link them manually via the 🔗
        button. Auto-subscribes each linked mod, like a regular install.

        Returns {ok, linked: int, candidates: int} so the frontend can
        flash a "X mods reliés" toast and refresh installedMeta."""
        token = self._modio_token()
        if not token:
            return {'ok': True, 'linked': 0, 'candidates': 0}
        candidates: list[tuple[str, str]] = []
        for m in self.list_mods():
            folder = m.get('path') or ''
            if not folder:
                continue
            if os.path.isfile(os.path.join(folder, '_modio_install.json')):
                continue
            modinfo_path = os.path.join(folder, 'modinfo.json')
            if not os.path.isfile(modinfo_path):
                continue
            try:
                with open(modinfo_path, 'r', encoding='utf-8') as f:
                    modinfo = json.load(f) or {}
            except (OSError, ValueError):
                continue
            slug = (modinfo.get('ModID') or '').strip().lower()
            if slug:
                candidates.append((folder, slug))
        if not candidates:
            return {'ok': True, 'linked': 0, 'candidates': 0}
        slugs_csv = ','.join(slug for _, slug in candidates)
        res = modio_module.list_mods_by_name_ids(token, slugs_csv)
        if not res.get('ok'):
            return {'ok': False,
                    'error': res.get('error', 'mod.io fetch failed'),
                    'linked': 0, 'candidates': len(candidates)}
        by_name_id = {(r.get('name_id') or '').lower(): r for r in (res.get('data') or [])}
        linked = 0
        for folder, slug in candidates:
            match = by_name_id.get(slug)
            if not match:
                continue
            modfile = match.get('modfile') or {}
            meta = {
                'mod_id': int(match.get('id') or 0),
                'name_id': match.get('name_id') or '',
                'name': match.get('name') or '',
                'modfile_id': int(modfile.get('id') or 0),
                'version': str(modfile.get('version') or ''),
                'installed_at': int(__import__('time').time()),
                'linked': True,
            }
            try:
                with open(os.path.join(folder, '_modio_install.json'),
                          'w', encoding='utf-8') as f:
                    json.dump(meta, f, indent=2, ensure_ascii=False)
                linked += 1
                try:
                    modio_module.subscribe(token, int(match['id']))
                except Exception:
                    pass
            except OSError:
                continue
        return {'ok': True, 'linked': linked, 'candidates': len(candidates)}

    def modio_install_by_name_id(self, name_id: str) -> dict:
        """Resolve a mod.io name_id (slug) to a numeric mod_id, then install it.
        Used by the dependency dialog to install a missing dep in one click."""
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        name_id = (name_id or '').strip().lower()
        if not name_id:
            return {'ok': False, 'error': 'name_id required'}
        res = modio_module.list_mods_by_name_ids(token, name_id)
        if not res.get('ok'):
            return res
        mods = res.get('data') or []
        match = next((m for m in mods if (m.get('name_id') or '').lower() == name_id), None)
        if not match:
            return {'ok': False, 'error': f'mod not found on mod.io: {name_id}'}
        return self.modio_install_mod(int(match['id']))

    def modio_install_mod(self, mod_id: int) -> dict:
        """Download the latest modfile of ``mod_id`` and install it. Always
        allow_overwrite=True so updates from mod.io replace the previous
        version cleanly."""
        token = self._modio_token()
        if not token:
            return {'ok': False, 'error': 'not authenticated'}
        target = self._mod_install_target()
        if not target:
            return {'ok': False, 'error': 'no mods folder configured'}
        # 1. Resolve the mod → modfile.binary_url
        meta = modio_module.get_mod(token, int(mod_id))
        if not meta.get('ok'):
            return meta
        mod = meta.get('mod') or {}
        modfile = mod.get('modfile') or {}
        download = modfile.get('download') or {}
        url = download.get('binary_url') or modfile.get('binary_url') or ''
        if not url:
            return {'ok': False, 'error': 'no downloadable modfile (mod has no published file?)'}
        # 2. Stream the binary into a temp .zip, then run the regular installer
        try:
            with tempfile.NamedTemporaryFile(prefix='_modio_', suffix='.zip',
                                             delete=False) as tf:
                tmp_path = tf.name
        except OSError as e:
            return {'ok': False, 'error': f'cannot create temp file: {e}'}
        try:
            dl = modio_module.download_modfile(url, tmp_path)
            if not dl.get('ok'):
                return dl
            res = installer_module.install_zip(tmp_path, target, allow_overwrite=True)
            # Drop a small marker file inside the mod folder so we can prove
            # later — even after the user manually deletes the folder — which
            # mod.io record this install came from. Self-cleaning: deleting
            # the folder removes the marker too, so the Browser tab notices
            # the install is gone on the next refresh.
            if res.get('ok') and res.get('folder'):
                meta = {
                    'mod_id': int(mod_id),
                    'name_id': (mod.get('name_id') or ''),
                    'name': (mod.get('name') or ''),
                    'modfile_id': int(modfile.get('id') or 0),
                    'version': str(modfile.get('version') or ''),
                    'installed_at': int(__import__('time').time()),
                }
                meta_path = os.path.join(target, res['folder'], '_modio_install.json')
                try:
                    with open(meta_path, 'w', encoding='utf-8') as f:
                        json.dump(meta, f, indent=2, ensure_ascii=False)
                except OSError:
                    pass  # not fatal — the install succeeded
                # Auto-subscribe so the user shows up in the mod's subscribers
                # and the "My Subscriptions" filter mirrors what's actually
                # installed. mod.io returns 201 if already subscribed, so
                # this is idempotent and safe to call unconditionally. We
                # ignore failures — install succeeded, which is what matters.
                try:
                    modio_module.subscribe(token, int(mod_id))
                except Exception:
                    pass
            return res
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    # ── release check ─────────────────────────────────────────────────────────
    def check_latest_release(self) -> dict:
        """Hit the GitHub releases API and compare its latest tag against
        the bundled version. Returns:
          {ok, current, latest, up_to_date, url, error?}
        Never blocks / raises into the JS bridge — failures are reported
        as ok=False with an error string.
        """
        import _version
        try:
            import requests
            r = requests.get(
                'https://api.github.com/repos/taludas/anno-117-mod-manager/releases/latest',
                headers={'Accept': 'application/vnd.github+json',
                         'User-Agent': 'Anno117ModManager'},
                timeout=8,
            )
            if r.status_code != 200:
                return {'ok': False,
                        'error': f'GitHub HTTP {r.status_code}',
                        'current': _version.__VERSION__}
            data = r.json() or {}
        except Exception as e:
            return {'ok': False, 'error': str(e),
                    'current': _version.__VERSION__}
        tag = (data.get('tag_name') or '').lstrip('vV').strip()
        # Tolerant version compare: split on dots, compare as ints when
        # possible, fall back to string equality otherwise.
        def _parse(v: str) -> tuple:
            parts = []
            for p in (v or '').split('.'):
                try: parts.append(int(p))
                except ValueError: parts.append(p)
            return tuple(parts)
        current = _version.__VERSION__
        try:
            up_to_date = _parse(tag) <= _parse(current)
        except TypeError:
            up_to_date = (tag == current)
        return {
            'ok': True,
            'current': current,
            'latest': tag or current,
            'up_to_date': up_to_date,
            'url': data.get('html_url') or 'https://github.com/taludas/anno-117-mod-manager/releases',
        }

    # ── news ──────────────────────────────────────────────────────────────────
    def fetch_news(self, force_refresh: bool = False) -> dict:
        """Return the merged news feed. Cached for 10 minutes per
        (reddit-on/off, modio-on/off) combination — pass
        ``force_refresh=True`` to bypass the cache."""
        import time
        include_reddit = bool(self.settings.get('show_reddit_news', False))
        modio_token = self._modio_token()  # '' when not connected → no modio cards
        cache = self._news_cache
        ttl_ok = (time.time() - cache.get('fetched_at', 0.0)) < 600
        cache_key = (include_reddit, bool(modio_token))
        if (not force_refresh
                and ttl_ok
                and cache.get('key') == cache_key
                and cache.get('items')):
            return {'ok': True, 'items': cache['items'], 'cached': True}
        items = news_module.fetch_all(include_reddit=include_reddit,
                                      parallel=True,
                                      modio_token=modio_token)
        self._news_cache = {
            'items': items,
            'fetched_at': time.time(),
            'key': cache_key,
        }
        return {'ok': True, 'items': items, 'cached': False}

    def fetch_anno_union_post(self, post_id: int) -> dict:
        """Lazy fetch of a single Anno Union post's full HTML — the News
        list only carries excerpts to keep the cold load fast, full content
        is pulled on demand when the user clicks a card."""
        return news_module.fetch_anno_union_post(int(post_id or 0))

    # ── tweaking (mod options) ────────────────────────────────────────────────
    def list_tweakable_mods(self) -> list[dict]:
        """Return only the installed mods that expose an Options block —
        what the Tweaking tab should populate its left list with."""
        out = []
        for m in self.list_mods():
            schema = options_module.get_options_schema(m['path'])
            if schema:
                out.append({
                    'id': m['id'],
                    'name': m['name'],
                    'category': m['category'],
                    'folder': m.get('folder', ''),
                    'option_count': len(schema),
                })
        return out

    def get_mod_options(self, mod_id: str) -> dict:
        """Return the schema + the user's saved values for a mod. Caller
        renders the form from this; the schema is the source of truth for
        types/labels/defaults, the values dict carries the current selection."""
        for m in self.list_mods():
            if m['id'] != mod_id:
                continue
            schema = options_module.get_options_schema(m['path'])
            active_all = options_module.load_active_options(self._options_path())
            mod_active = active_all.get(mod_id, {}) if isinstance(active_all.get(mod_id), dict) else {}
            return {
                'ok': True,
                'mod_id': mod_id,
                'name': m['name'],
                'schema': schema,
                'values': options_module.merged_values(schema, mod_active),
            }
        return {'ok': False, 'error': 'mod not found'}

    def set_mod_option(self, mod_id: str, key: str, value) -> dict:
        ok, err = options_module.set_option(self._options_path(), mod_id, key, value)
        return {'ok': ok, 'error': err}

    def reset_mod_options(self, mod_id: str) -> dict:
        ok, err = options_module.reset_mod(self._options_path(), mod_id)
        return {'ok': ok, 'error': err}

    def reset_all_options(self) -> dict:
        ok, err = options_module.reset_all(self._options_path())
        return {'ok': ok, 'error': err}

    def _options_path(self) -> str:
        custom_docs = self.settings.get('custom_docs_path', '')
        docs_mods = paths_module.documents_mods_root(custom_docs)
        return os.path.join(docs_mods, 'active-options.jsonc') if docs_mods else ''

    # ── manual install ────────────────────────────────────────────────────────
    def install_zip_from_path(self, zip_path: str, allow_overwrite: bool = False) -> dict:
        """Install a mod from a ZIP file already on disk (e.g. picked via the
        native file dialog). Returns the installer's result dict augmented
        with target info."""
        target = self._mod_install_target()
        if not target:
            return {'ok': False, 'error': 'no mods folder configured'}
        return installer_module.install_zip(zip_path, target, allow_overwrite=allow_overwrite)

    def install_zip_from_b64(self, filename: str, b64: str, allow_overwrite: bool = False) -> dict:
        """Install a mod from an in-memory ZIP (used for HTML5 drag-drop:
        the JS reads the dropped File as base64 and posts it here). The
        payload is decoded into a temp file then the regular install path is
        re-used. Capped at 200 MB."""
        if not b64:
            return {'ok': False, 'error': 'empty payload'}
        try:
            raw = base64.b64decode(b64, validate=True)
        except Exception as e:
            return {'ok': False, 'error': f'bad base64: {e}'}
        if len(raw) > 200 * 1024 * 1024:
            return {'ok': False, 'error': 'archive too large (>200 MB)'}
        target = self._mod_install_target()
        if not target:
            return {'ok': False, 'error': 'no mods folder configured'}
        # Sanitise the filename — only used for the temp file's extension
        safe_name = (filename or 'upload.zip').replace('/', '_').replace('\\', '_')
        if not safe_name.lower().endswith('.zip'):
            safe_name += '.zip'
        try:
            with tempfile.NamedTemporaryFile(prefix='_modupload_', suffix='_' + safe_name,
                                             delete=False) as tf:
                tf.write(raw)
                tmp_path = tf.name
        except OSError as e:
            return {'ok': False, 'error': f'cannot stash upload: {e}'}
        try:
            return installer_module.install_zip(tmp_path, target, allow_overwrite=allow_overwrite)
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    def _mod_install_target(self) -> str:
        """Where new mods land (Documents folder takes precedence over the
        game-side folder, mirroring the Tk version's mod_loc_mode default)."""
        custom_docs = self.settings.get('custom_docs_path', '')
        mode = self.settings.get('mod_location_mode', 'Documents')
        if mode == 'GameDirectory':
            return paths_module.game_mods_root(self.settings.get('game_path', '')) \
                or paths_module.documents_mods_root(custom_docs)
        return paths_module.documents_mods_root(custom_docs) \
            or paths_module.game_mods_root(self.settings.get('game_path', ''))

    # ── modloader log ─────────────────────────────────────────────────────────
    def read_modloader_log(self) -> dict:
        """Read mod-loader.log from the documents mods folder. Returns
        ``{ok, content, path, exists}``. Capped at ~2 MB so a runaway log
        can't make the bridge call hang."""
        custom_docs = self.settings.get('custom_docs_path', '')
        docs_mods = paths_module.documents_mods_root(custom_docs)
        path = os.path.join(docs_mods, 'mod-loader.log') if docs_mods else ''
        if not path:
            return {'ok': False, 'path': '', 'exists': False, 'error': 'no documents folder'}
        if not os.path.exists(path):
            return {'ok': True, 'path': path, 'exists': False, 'content': ''}
        try:
            size = os.path.getsize(path)
            cap = 2 * 1024 * 1024
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                if size > cap:
                    f.seek(size - cap)
                    f.readline()  # discard the partial first line
                content = f.read()
            return {'ok': True, 'path': path, 'exists': True, 'content': content,
                    'truncated': size > cap}
        except OSError as e:
            return {'ok': False, 'path': path, 'exists': True, 'error': str(e)}

    # ── load order ────────────────────────────────────────────────────────────
    def get_profile_order(self) -> list[str]:
        """Return the list of mod IDs in the order they currently appear in
        active-profile.txt (active or commented). Drives the Load Order view."""
        return profile_module.parse_profile_order(self._active_profile_path())

    def reorder_mods(self, ordered_ids: list[str]) -> dict:
        """Rewrite active-profile.txt with the given order. Active/disabled
        state per mod is preserved from the existing file."""
        if not isinstance(ordered_ids, list):
            return {'ok': False, 'error': 'expected a list of ids'}
        ok, err = profile_module.reorder_profile(self._active_profile_path(), ordered_ids)
        return {'ok': ok, 'error': err}

    # ── presets ───────────────────────────────────────────────────────────────
    def list_presets(self) -> list[str]:
        """Return user-saved preset names (without file extension)."""
        return profile_module.list_presets(self.presets_dir)

    def save_preset(self, name: str) -> dict:
        """Snapshot the current active-profile.txt as ``presets/<name>.txt``."""
        ok, err = profile_module.save_preset(self.presets_dir, self._active_profile_path(), name)
        return {'ok': ok, 'error': err}

    def delete_preset(self, name: str) -> dict:
        """Permanently remove ``presets/<name>.txt``."""
        ok, err = profile_module.delete_preset(self.presets_dir, name)
        return {'ok': ok, 'error': err}

    def load_preset(self, name: str) -> dict:
        """Apply a preset (or the reserved 'Default' / 'Vanilla') to the
        active profile. The preset's mod ids are expanded against the current
        installed-mods list so EnableNewMods can never silently re-enable a
        mod the preset wanted disabled."""
        ids = [m['id'] for m in self.list_mods() if not m.get('parent_path')]
        ok, err = profile_module.load_preset(self.presets_dir, self._active_profile_path(), name, ids)
        return {'ok': ok, 'error': err}

    # ── launch ────────────────────────────────────────────────────────────────
    def launch_game(self) -> dict:
        ok, err = launcher_module.launch(self.settings.get('game_path', ''))
        return {'ok': ok, 'error': err}

    # ── meta ──────────────────────────────────────────────────────────────────
    def app_info(self) -> dict[str, Any]:
        import _version
        return {
            'version': _version.__VERSION__,
            'platform': platform.system(),
            'has_game_path': bool(self.settings.get('game_path')),
        }

    # ── internals ─────────────────────────────────────────────────────────────
    def _active_profile_path(self) -> str:
        return paths_module.active_profile_path(self.settings.get('custom_docs_path', ''))

    def _mod_roots(self) -> list[str]:
        custom_docs = self.settings.get('custom_docs_path', '')
        game_path = self.settings.get('game_path', '')
        out: list[str] = []
        for r in (paths_module.documents_mods_root(custom_docs),
                  paths_module.game_mods_root(game_path)):
            if r and os.path.isdir(r):
                out.append(r)
        return out
