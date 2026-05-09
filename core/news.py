"""News-feed aggregators for the News tab.

Each fetch_* function returns a list of news-item dicts in the shape:

    {
      'title':       str,
      'url':         str,           # opens in the user's external browser
      'date':        str,           # 'Mar 14, 2026' style for display
      'sort_ts':     float,         # unix timestamp for the merged sort
      'excerpt':     str,           # short plain-text summary
      'img_url':     str | None,    # remote thumbnail
      'source':      str,           # 'anno_union' | 'reddit'
      'badge_text':  str,           # short uppercase label, eg 'ANNO UNION'
      'badge_color': str,           # CSS hex for the source pill
    }

Fetches are best-effort: any exception → empty list (logged to stderr) so a
broken source never blocks the others.
"""
from __future__ import annotations

import html
import re
import sys
from datetime import datetime
from typing import Callable

import requests

_UA = 'Mozilla/5.0 (X11; Linux x86_64) Anno117ModManager/1.0'

# Reuse one HTTP session per process — saves the TLS handshake on every
# 5-minute refresh poll. requests.Session is thread-safe for our usage.
_SESSION = requests.Session()


def _fmt_date(ts: float) -> str:
    try:
        return datetime.fromtimestamp(ts).strftime('%b %d, %Y')
    except Exception:
        return ''


# Anno Union runs on WordPress + WPBakery, whose page-builder shortcodes
# ([vc_row], [vc_column_text css="..."], …) are returned verbatim by the
# WP REST API instead of being rendered. Strip them everywhere — they
# look like raw markup when displayed and confuse the reader.
_WP_SHORTCODE_RE = re.compile(r'\[/?vc_[^\]]*\]', re.IGNORECASE)


def _strip_wp_shortcodes(raw: str) -> str:
    return _WP_SHORTCODE_RE.sub('', raw or '')


def _strip_html(raw: str, max_len: int = 160) -> str:
    cleaned = _strip_wp_shortcodes(raw or '')
    text = html.unescape(re.sub(r'<[^<]+?>', '', cleaned).strip())
    return (text[:max_len] + '...') if len(text) > max_len else text


def fetch_anno_union(timeout: float = 10.0) -> list[dict]:
    """Pull the 10 latest blog posts from anno-union.com via its WordPress
    REST API. Featured-media thumbnails are extracted from the embedded data
    when available."""
    items: list[dict] = []
    try:
        url = 'https://www.anno-union.com/wp-json/wp/v2/posts?_embed&per_page=10'
        res = _SESSION.get(url, headers={'User-Agent': _UA, 'Accept': 'application/json'},
                           timeout=timeout)
        res.raise_for_status()
        for post in res.json():
            try:
                dt = datetime.strptime(post.get('date', ''), '%Y-%m-%dT%H:%M:%S')
                sort_ts = dt.timestamp()
                date_text = dt.strftime('%b %d, %Y')
            except Exception:
                sort_ts = 0.0
                date_text = post.get('date', '')

            img_url = None
            try:
                media = (post.get('_embedded') or {}).get('wp:featuredmedia', [{}])[0]
                img_url = ((media.get('media_details') or {}).get('sizes', {})
                                .get('medium', {}).get('source_url')
                           or media.get('source_url'))
            except Exception:
                pass

            items.append({
                'title':       html.unescape((post.get('title') or {}).get('rendered', 'Unknown')),
                'url':         post.get('link', 'https://www.anno-union.com/en/blogs/'),
                'date':        date_text,
                'sort_ts':     sort_ts,
                'excerpt':     _strip_html((post.get('excerpt') or {}).get('rendered', '')),
                'img_url':     img_url,
                'source':      'anno_union',
                'badge_text':  'ANNO UNION',
                'badge_color': '#5f022e',
                # WP post id — used by fetch_anno_union_post() to pull the
                # full content lazily when the user clicks the card.
                'wp_id':       int(post.get('id') or 0),
            })
    except Exception as e:
        print(f'[news] anno_union fetch failed: {e}', file=sys.stderr)
    return items


def fetch_anno_union_post(post_id: int, timeout: float = 10.0) -> dict:
    """Fetch the full HTML content for one Anno Union blog post. Called
    lazily when the user clicks a news card so we don't pay the cost of
    pulling 10 full posts at every News tab open. Returns a dict with the
    rendered content and a few metadata fields the front already had from
    the list call (kept for caller convenience)."""
    if not post_id:
        return {'ok': False, 'error': 'no post_id'}
    try:
        url = f'https://www.anno-union.com/wp-json/wp/v2/posts/{int(post_id)}?_embed'
        res = _SESSION.get(url, headers={'User-Agent': _UA, 'Accept': 'application/json'},
                           timeout=timeout)
        res.raise_for_status()
        post = res.json() or {}
        # Hero image for the in-app reader — go for the full-resolution
        # original (`source_url` at the top level of the media object) so
        # the banner doesn't end up pixelated when shown at ~880px wide.
        # Fall back to large/medium only if the original is somehow missing.
        img_url = None
        try:
            media = (post.get('_embedded') or {}).get('wp:featuredmedia', [{}])[0]
            sizes = (media.get('media_details') or {}).get('sizes', {})
            img_url = (media.get('source_url')
                       or sizes.get('large', {}).get('source_url')
                       or sizes.get('medium', {}).get('source_url'))
        except Exception:
            pass
        return {
            'ok':           True,
            'wp_id':        int(post.get('id') or 0),
            'title':        html.unescape((post.get('title') or {}).get('rendered', '')),
            'url':          post.get('link', ''),
            # Strip WPBakery shortcodes only — keep real HTML tags so the
            # in-app reader can format the post (paragraphs, headings,
            # images, …). The frontend sanitiser still scrubs anything
            # script-y on top.
            'content_html': _strip_wp_shortcodes((post.get('content') or {}).get('rendered', '')),
            'img_url':      img_url,
        }
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def fetch_reddit(timeout: float = 10.0) -> list[dict]:
    """Pull the 10 latest /r/anno posts via Reddit's public JSON endpoint."""
    items: list[dict] = []
    try:
        url = 'https://www.reddit.com/r/anno/new.json?limit=10'
        res = _SESSION.get(url, headers={'User-Agent': _UA}, timeout=timeout)
        res.raise_for_status()
        for child in (res.json().get('data') or {}).get('children', []):
            d = child.get('data') or {}
            ts = float(d.get('created_utc') or 0.0)
            img_url = None
            preview = (d.get('preview') or {}).get('images', [])
            if preview and preview[0].get('source', {}).get('url'):
                img_url = html.unescape(preview[0]['source']['url'])
            items.append({
                'title':       d.get('title', 'Untitled'),
                'url':         f'https://www.reddit.com{d.get("permalink", "")}',
                'date':        _fmt_date(ts),
                'sort_ts':     ts,
                'excerpt':     _strip_html(d.get('selftext') or ''),
                'img_url':     img_url,
                'source':      'reddit',
                'badge_text':  'r/anno',
                'badge_color': '#ff4500',
            })
    except Exception as e:
        print(f'[news] reddit fetch failed: {e}', file=sys.stderr)
    return items


_MODIO_GAME_ID = '11358'
_MODIO_BASE = f'https://g-{_MODIO_GAME_ID}.modapi.io/v1'


def fetch_modio(token: str, timeout: float = 12.0) -> list[dict]:
    """Pull the most recently added mods + collections from mod.io and turn
    them into news items. Two requests in parallel:
    - 8 newest mods  (badge: NEW MOD)
    - 5 newest collections (badge: NEW COLLECTION)
    The user must be authenticated — these endpoints reject anonymous
    requests on per-game bases.
    """
    if not token:
        return []
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'X-Modio-Platform': 'Linux',
    }

    def _hit(endpoint: str, limit: int) -> list[dict]:
        try:
            r = _SESSION.get(
                f'{_MODIO_BASE}/games/{_MODIO_GAME_ID}/{endpoint}',
                headers=headers,
                params={'_sort': '-date_added', '_limit': limit},
                timeout=timeout,
            )
            r.raise_for_status()
            return (r.json() or {}).get('data') or []
        except Exception as e:
            print(f'[news] modio {endpoint} fetch failed: {e}', file=sys.stderr)
            return []

    items: list[dict] = []

    for m in _hit('mods', 8):
        ts = float(m.get('date_added') or 0)
        logo = m.get('logo') or {}
        author = (m.get('submitted_by') or {}).get('username') or '?'
        items.append({
            'title':       m.get('name') or 'Untitled',
            'url':         m.get('profile_url') or f'https://mod.io/g/anno-117-pax-romana/m/{m.get("name_id", "")}',
            'date':        _fmt_date(ts),
            'sort_ts':     ts,
            'excerpt':     _strip_html(m.get('summary') or '') or f'by {author}',
            'img_url':     logo.get('thumb_320x180') or logo.get('original'),
            'source':      'modio',
            'badge_text':  'NEW MOD',
            'badge_color': '#3d5a30',
            # Extras the frontend uses to deep-link into the in-app Browser
            # tab instead of bouncing the user out to mod.io in a browser.
            'modio_id':    int(m.get('id') or 0),
            'modio_kind':  'mod',
        })

    for c in _hit('collections', 5):
        ts = float(c.get('date_added') or 0)
        logo = c.get('logo') or {}
        author = (c.get('submitted_by') or {}).get('username') or '?'
        mods_total = ((c.get('stats') or {}).get('mods_total')) or 0
        items.append({
            'title':       c.get('name') or 'Untitled',
            'url':         c.get('profile_url') or f'https://mod.io/g/anno-117-pax-romana/c/{c.get("name_id", "")}',
            'date':        _fmt_date(ts),
            'sort_ts':     ts,
            'excerpt':     _strip_html(c.get('summary') or '') or f'by {author} · {mods_total} mods',
            'img_url':     logo.get('thumb_320x180') or logo.get('original'),
            'source':      'modio_collection',
            'badge_text':  'NEW COLLECTION',
            'badge_color': '#7a6730',
            'modio_id':    int(c.get('id') or 0),
            'modio_kind':  'collection',
        })

    return items


def fetch_all(include_reddit: bool, parallel: bool = True,
              modio_token: str = '') -> list[dict]:
    """Pull every enabled source (in parallel by default) and return one
    chronologically-sorted list. ``modio_token`` is optional — when present
    we also surface new mods + collections from mod.io as news cards."""
    workers: list[Callable[[], list[dict]]] = [fetch_anno_union]
    if include_reddit:
        workers.append(fetch_reddit)
    if modio_token:
        workers.append(lambda: fetch_modio(modio_token))

    if not parallel or len(workers) == 1:
        out: list[dict] = []
        for w in workers:
            out += w()
    else:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=len(workers)) as pool:
            out = []
            for items in pool.map(lambda fn: fn(), workers):
                out += items

    out.sort(key=lambda x: x.get('sort_ts', 0.0), reverse=True)
    return out
