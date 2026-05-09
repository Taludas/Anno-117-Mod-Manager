"""mod.io API client wrapper for Anno 117.

Pure functions: each call returns a dict {ok, ...payload, error} so the JS
bridge can dispatch without ever raising into pywebview's event loop.

Endpoints we cover at this stage:
- /oauth/emailrequest + /oauth/emailexchange — the two-step email OAuth used
  by every mod.io desktop client
- /games/<gid>/mods    — paginated mod listing for the Mod Browser tab
- /games/<gid>/mods/<mid> — single mod (description, screenshots, etc.)
- /me/subscribed       — what the logged-in user has subscribed to
- /me/ratings          — endorsement state per mod
- POST /me/subscribed  — subscribe / unsubscribe
- POST /games/<gid>/mods/<mid>/ratings — endorse / unendorse

The download flow itself (modfile binary) is handled by core.installer once
we have a download URL from get_mod.
"""
from __future__ import annotations

import time
from typing import Any

import requests

GAME_ID = '11358'
GAME_NAME_ID = 'anno-117-pax-romana'   # slug used by the user-facing API
BASE_URL = f'https://g-{GAME_ID}.modapi.io/v1'
# The collection follow/subscribe endpoints (and /me/following/collections)
# only live on the user-facing host, addressed by @slug — captured from the
# mod.io web frontend's HAR. Same Bearer token works.
USER_API_URL = 'https://mod.io/v1'

# Reuse one HTTP session per process so back-to-back mod.io calls don't
# pay the TLS handshake every time. requests.Session is thread-safe for
# this read-mostly usage.
_SESSION = requests.Session()


def collection_preset_name(name: str, collection_id: int) -> str:
    """Strip a collection name down to characters the preset filename
    validator accepts ([A-Za-z0-9 _-]). Empty / reserved results fall
    back to ``Collection_<id>``. The JS frontend mirrors this same
    algorithm in app.js (_collectionPresetName) — keep them in lockstep
    or the "already installed" badge will lie."""
    import re as _re
    safe = _re.sub(r'[^A-Za-z0-9 _\-]', '_', name or '').strip()[:50]
    if not safe or safe in ('Default', 'Vanilla'):
        safe = f'Collection_{int(collection_id)}'
    return safe

# Distinct error refs we care about (full list at https://docs.mod.io)
ERR_TERMS_UPDATED = 11074


# ── helpers ──────────────────────────────────────────────────────────────────

def _bearer_headers(token: str) -> dict:
    return {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'X-Modio-Platform': 'Linux',
    }


def _bearer_headers_form(token: str) -> dict:
    """For POST/DELETE requests with no body — mod.io still demands a
    Content-Type header and rejects the call otherwise (error 13013:
    "Content-Type header is missing"). Use this on subscribe/unsubscribe
    where requests would otherwise omit the header."""
    h = _bearer_headers(token)
    h['Content-Type'] = 'application/x-www-form-urlencoded'
    return h


def _decode_error(response: requests.Response) -> tuple[int, str]:
    """Pull a usable {error_ref, message} out of a mod.io HTTP error body."""
    try:
        body = response.json() or {}
    except ValueError:
        return 0, response.text or f'HTTP {response.status_code}'
    err = body.get('error') or {}
    return int(err.get('error_ref') or 0), str(err.get('message') or 'unknown error')


# ── OAuth (email-based) ──────────────────────────────────────────────────────

def email_request(api_key: str, email: str, timeout: float = 10.0) -> dict:
    """Step 1: ask mod.io to email the user a 5-character security code."""
    if not api_key:
        return {'ok': False, 'error': 'no API key'}
    if not email:
        return {'ok': False, 'error': 'email required'}
    try:
        res = _SESSION.post(
            f'{BASE_URL}/oauth/emailrequest',
            data={'api_key': api_key, 'email': email},
            headers={'Accept': 'application/json'},
            timeout=timeout,
        )
        if res.status_code == 200:
            return {'ok': True}
        ref, msg = _decode_error(res)
        return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def email_exchange(api_key: str, code: str, terms_agreed: bool,
                   timeout: float = 10.0) -> dict:
    """Step 2: trade the security code for an access token + expiry."""
    if not api_key or not code:
        return {'ok': False, 'error': 'api key + code required'}
    try:
        res = _SESSION.post(
            f'{BASE_URL}/oauth/emailexchange',
            data={
                'api_key': api_key,
                'security_code': code,
                'terms_agreed': 'true' if terms_agreed else 'false',
            },
            headers={'Accept': 'application/json'},
            timeout=timeout,
        )
        if res.status_code == 200:
            data = res.json() or {}
            return {
                'ok': True,
                'access_token': data.get('access_token', ''),
                'date_expires': int(data.get('date_expires') or 0),
            }
        ref, msg = _decode_error(res)
        # 403 + error_ref 11074 means the user must re-accept the terms
        return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def is_token_valid(expires_ts: int) -> bool:
    """A token expiring in the next 60s is considered already gone — gives
    the UI a chance to re-auth before a request races the clock."""
    return bool(expires_ts) and (expires_ts - 60) > time.time()


# ── browsing ─────────────────────────────────────────────────────────────────

def list_mods(token: str, *, search: str = '', tags: list[str] | None = None,
              submitted_by: int = 0, collections: bool = False,
              limit: int = 30, offset: int = 0,
              sort: str = '-date_updated', timeout: float = 15.0) -> dict:
    """Paginated mod / collection search. ``sort`` follows mod.io's syntax:
    prefix with - for descending. Default '-date_updated' surfaces recent
    activity first.

    ``submitted_by`` (int) restricts the listing to one author — used by the
    "show me everything by this user" link on each card.

    ``collections`` switches the URL to the dedicated /collections endpoint
    (separate from /mods on mod.io). The response shape is identical to
    /mods so the same UI consumes both."""
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    params: dict[str, Any] = {
        '_limit': max(1, min(100, int(limit))),
        '_offset': max(0, int(offset)),
        '_sort': sort,
    }
    if search:
        params['_q'] = search
    if tags:
        params['tags-in'] = ','.join(tags)
    if submitted_by:
        params['submitted_by'] = int(submitted_by)
    endpoint = 'collections' if collections else 'mods'
    try:
        res = _SESSION.get(
            f'{BASE_URL}/games/{GAME_ID}/{endpoint}',
            headers=_bearer_headers(token),
            params=params,
            timeout=timeout,
        )
        if res.status_code != 200:
            ref, msg = _decode_error(res)
            return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
        body = res.json() or {}
        return {
            'ok': True,
            'data': body.get('data', []) or [],
            'result_count': int(body.get('result_count') or 0),
            'result_total': int(body.get('result_total') or 0),
            'result_offset': int(body.get('result_offset') or 0),
            'result_limit': int(body.get('result_limit') or 0),
        }
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def list_dependencies(token: str, mod_id: int, *, collection: bool = False,
                      timeout: float = 15.0) -> dict:
    """For a regular mod, returns its dependencies (other mods it requires).
    For a collection, returns the mods it bundles — these live under a
    different URL on mod.io: ``/games/{gid}/collections/{cid}/mods``
    (verified empirically; ``/mods/{cid}/dependencies`` returns 404 for
    collection IDs since those IDs aren't valid mod IDs).

    Same response envelope on both URLs (data: [mod, ...])."""
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    url = (f'{BASE_URL}/games/{GAME_ID}/collections/{int(mod_id)}/mods'
           if collection
           else f'{BASE_URL}/games/{GAME_ID}/mods/{int(mod_id)}/dependencies')
    try:
        res = _SESSION.get(
            url,
            headers=_bearer_headers(token),
            params={'_limit': 100},
            timeout=timeout,
        )
        if res.status_code != 200:
            ref, msg = _decode_error(res)
            return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
        return {'ok': True, 'data': (res.json() or {}).get('data', []) or []}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def get_mod(token: str, mod_id: int, *, collection: bool = False,
            timeout: float = 10.0) -> dict:
    """Full record for one mod or collection. mod.io routes per-record
    fetches to different URLs: ``/games/{gid}/mods/{id}`` for regular mods
    and ``/games/{gid}/collections/{id}`` for collections (verified empirically;
    asking /mods for a collection ID returns 404)."""
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    segment = 'collections' if collection else 'mods'
    try:
        res = _SESSION.get(
            f'{BASE_URL}/games/{GAME_ID}/{segment}/{int(mod_id)}',
            headers=_bearer_headers(token),
            timeout=timeout,
        )
        if res.status_code != 200:
            ref, msg = _decode_error(res)
            return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
        return {'ok': True, 'mod': res.json() or {}}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def list_game_tags(api_key: str, timeout: float = 15.0) -> dict:
    """Return the tag taxonomy mod.io exposes for Anno 117. Used to populate
    the Browser's "filter by tag" dropdown without hard-coding the list.
    Public endpoint — only needs the API key, no bearer token. Each entry
    is {name, type ('checkboxes'|'dropdown'), tags: [...], hidden}."""
    if not api_key:
        return {'ok': False, 'error': 'no API key'}
    try:
        res = _SESSION.get(
            f'{BASE_URL}/games/{GAME_ID}/tags',
            params={'api_key': api_key, '_limit': 100},
            headers={'Accept': 'application/json'},
            timeout=timeout,
        )
        if res.status_code != 200:
            ref, msg = _decode_error(res)
            return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
        return {'ok': True, 'data': (res.json() or {}).get('data', []) or []}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def list_my_ratings(token: str, timeout: float = 15.0) -> dict:
    """Return the list of ratings the user has cast. Each entry is
    {mod_id, rating, ...} — rating == 1 means a positive endorsement.
    Used by the UI to render the heart in its "already endorsed" state
    on a fresh page load (the mod summary doesn't carry user_rating)."""
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    try:
        res = _SESSION.get(
            f'{BASE_URL}/me/ratings',
            headers=_bearer_headers(token),
            params={'game_id': GAME_ID, '_limit': 100},
            timeout=timeout,
        )
        if res.status_code != 200:
            ref, msg = _decode_error(res)
            return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
        return {'ok': True, 'data': (res.json() or {}).get('data', []) or []}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def list_mods_by_name_ids(token: str, slugs: str, timeout: float = 15.0) -> dict:
    """Batch fetch of mods whose name_id matches any of the comma-separated
    slugs in ``slugs``. Used by the Activation tab's auto-link to wire
    hand-installed mods to their mod.io record when modinfo.ModID happens
    to match the mod.io slug."""
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    if not slugs:
        return {'ok': True, 'data': []}
    try:
        res = _SESSION.get(
            f'{BASE_URL}/games/{GAME_ID}/mods',
            headers=_bearer_headers(token),
            params={'name_id-in': slugs, '_limit': 100},
            timeout=timeout,
        )
        if res.status_code != 200:
            ref, msg = _decode_error(res)
            return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
        body = res.json() or {}
        return {'ok': True, 'data': body.get('data', []) or []}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def check_updates(token: str, ids: list[int], timeout: float = 15.0) -> dict:
    """Batch lookup of the current modfile_id for a set of mod ids — used
    by the Activation tab to decide which rows can offer an Update button.
    Compares against the locally recorded modfile_id (in _modio_install.json)
    and lights up the button only when they differ. One API call covers
    up to 100 mods, which is well above the typical user library size."""
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    cleaned = [int(i) for i in (ids or []) if int(i) > 0]
    if not cleaned:
        return {'ok': True, 'updates': {}}
    try:
        res = _SESSION.get(
            f'{BASE_URL}/games/{GAME_ID}/mods',
            headers=_bearer_headers(token),
            params={'id-in': ','.join(str(i) for i in cleaned), '_limit': 100},
            timeout=timeout,
        )
        if res.status_code != 200:
            ref, msg = _decode_error(res)
            return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
        body = res.json() or {}
        updates: dict[int, dict] = {}
        for m in (body.get('data') or []):
            mid = int(m.get('id') or 0)
            modfile = m.get('modfile') or {}
            mfid = int(modfile.get('id') or 0)
            mver = str(modfile.get('version') or '')
            if mid:
                updates[mid] = {'modfile_id': mfid, 'version': mver}
        return {'ok': True, 'updates': updates}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def list_subscribed(token: str, *, search: str = '',
                    limit: int = 100, offset: int = 0,
                    sort: str = '', timeout: float = 15.0) -> dict:
    """Return the list of mods the user is subscribed to (filtered to
    Anno 117 via the ``game_id`` query param). Same response shape as
    list_mods so the browser UI can swap endpoints transparently when the
    "My Subscriptions" filter is on."""
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    params: dict[str, Any] = {
        'game_id': GAME_ID,
        '_limit': max(1, min(100, int(limit))),
        '_offset': max(0, int(offset)),
    }
    if sort:
        params['_sort'] = sort
    if search:
        params['_q'] = search
    try:
        res = _SESSION.get(
            f'{BASE_URL}/me/subscribed',
            headers=_bearer_headers(token),
            params=params,
            timeout=timeout,
        )
        if res.status_code != 200:
            ref, msg = _decode_error(res)
            return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
        body = res.json() or {}
        return {
            'ok': True,
            'data': body.get('data', []) or [],
            'result_count': int(body.get('result_count') or 0),
            'result_total': int(body.get('result_total') or 0),
            'result_offset': int(body.get('result_offset') or 0),
            'result_limit': int(body.get('result_limit') or 0),
        }
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


# ── actions ──────────────────────────────────────────────────────────────────

def subscribe(token: str, mod_id: int, timeout: float = 10.0) -> dict:
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    try:
        res = _SESSION.post(
            f'{BASE_URL}/games/{GAME_ID}/mods/{int(mod_id)}/subscribe',
            headers=_bearer_headers_form(token),
            timeout=timeout,
        )
        # 200 = newly subscribed, 201 = already subscribed (mod.io quirk)
        if res.status_code in (200, 201):
            return {'ok': True}
        ref, msg = _decode_error(res)
        return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def unsubscribe(token: str, mod_id: int, timeout: float = 10.0) -> dict:
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    try:
        res = _SESSION.delete(
            f'{BASE_URL}/games/{GAME_ID}/mods/{int(mod_id)}/subscribe',
            headers=_bearer_headers_form(token),
            timeout=timeout,
        )
        # 204 No Content on success
        if res.status_code in (200, 204):
            return {'ok': True}
        ref, msg = _decode_error(res)
        return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


# ── collection follow ───────────────────────────────────────────────────────
# Follow/unfollow a collection on mod.io. The user-facing API uses @slug
# addressing (no numeric id endpoint exists). When you follow a collection
# on mod.io's website it auto-subscribes you to every mod in the bundle —
# we replicate that by calling /subscriptions right after /followers, just
# like the web frontend does (captured via HAR). Calling both keeps the
# server-side state consistent regardless of whether one would cascade to
# the other on its own.

def follow_collection(token: str, name_id: str, timeout: float = 10.0) -> dict:
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    if not name_id:
        return {'ok': False, 'error': 'collection name_id missing'}
    base = f'{USER_API_URL}/games/@{GAME_NAME_ID}/collections/@{name_id}'
    try:
        r1 = _SESSION.post(f'{base}/followers', headers=_bearer_headers_form(token),
                           data='noop=noop', timeout=timeout)
        if r1.status_code not in (200, 201):
            ref, msg = _decode_error(r1)
            return {'ok': False, 'error': msg, 'error_ref': ref, 'status': r1.status_code}
        # Best-effort cascade — failures here aren't fatal because mod.io may
        # already auto-subscribe on follow. We swallow any error so the
        # follow itself stays the source of truth.
        try:
            _SESSION.post(f'{base}/subscriptions', headers=_bearer_headers_form(token),
                          data='noop=noop', timeout=timeout)
        except requests.RequestException:
            pass
        return {'ok': True}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def unfollow_collection(token: str, name_id: str, timeout: float = 10.0) -> dict:
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    if not name_id:
        return {'ok': False, 'error': 'collection name_id missing'}
    base = f'{USER_API_URL}/games/@{GAME_NAME_ID}/collections/@{name_id}'
    try:
        r1 = _SESSION.delete(f'{base}/followers', headers=_bearer_headers_form(token),
                             timeout=timeout)
        if r1.status_code not in (200, 204):
            ref, msg = _decode_error(r1)
            return {'ok': False, 'error': msg, 'error_ref': ref, 'status': r1.status_code}
        try:
            _SESSION.delete(f'{base}/subscriptions',
                            headers=_bearer_headers_form(token), timeout=timeout)
        except requests.RequestException:
            pass
        return {'ok': True}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def list_followed_collections(token: str, *, search: str = '',
                              limit: int = 100, offset: int = 0,
                              sort: str = '', timeout: float = 15.0) -> dict:
    """Same shape as list_mods/list_subscribed so the Browser Collections
    tab can swap endpoints transparently when "Mes follows" is toggled."""
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    params: dict[str, Any] = {
        'game_id': GAME_ID,
        '_limit': max(1, min(100, int(limit))),
        '_offset': max(0, int(offset)),
    }
    if sort:
        params['_sort'] = sort
    if search:
        params['_q'] = search
    try:
        res = _SESSION.get(
            f'{USER_API_URL}/me/following/collections',
            headers=_bearer_headers(token),
            params=params,
            timeout=timeout,
        )
        if res.status_code != 200:
            ref, msg = _decode_error(res)
            return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
        body = res.json() or {}
        return {
            'ok': True,
            'data': body.get('data', []) or [],
            'result_count': int(body.get('result_count') or 0),
            'result_total': int(body.get('result_total') or 0),
            'result_offset': int(body.get('result_offset') or 0),
            'result_limit': int(body.get('result_limit') or 0),
        }
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def endorse(token: str, mod_id: int, positive: bool, timeout: float = 10.0) -> dict:
    """Set rating: 1=positive endorsement, -1=negative, 0=clear."""
    if not token:
        return {'ok': False, 'error': 'not authenticated'}
    try:
        res = _SESSION.post(
            f'{BASE_URL}/games/{GAME_ID}/mods/{int(mod_id)}/ratings',
            headers=_bearer_headers_form(token),
            data={'rating': '1' if positive else '0'},
            timeout=timeout,
        )
        if res.status_code in (200, 201):
            return {'ok': True}
        ref, msg = _decode_error(res)
        return {'ok': False, 'error': msg, 'error_ref': ref, 'status': res.status_code}
    except requests.RequestException as e:
        return {'ok': False, 'error': str(e)}


def download_modfile(url: str, dest_path: str, timeout: float = 60.0) -> dict:
    """Stream-download a modfile binary URL to ``dest_path`` (a local .zip).
    The mod.io modfile.binary_url is short-lived and pre-signed, so this is
    just a plain GET — no auth header needed."""
    try:
        with _SESSION.get(url, stream=True, timeout=timeout) as res:
            if res.status_code != 200:
                return {'ok': False, 'error': f'HTTP {res.status_code}', 'status': res.status_code}
            with open(dest_path, 'wb') as f:
                for chunk in res.iter_content(chunk_size=64 * 1024):
                    if chunk:
                        f.write(chunk)
        return {'ok': True, 'path': dest_path}
    except (requests.RequestException, OSError) as e:
        return {'ok': False, 'error': str(e)}
