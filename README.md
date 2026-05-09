# Anno 117 Mod Manager

![Anno 117 Mod Manager Logo](data/ui/modmanager_logo.png)

This project is not affiliated with or endorsed by Ubisoft and/or mod.io.

---

A desktop application for managing mods for **Anno 117: Pax Romana**. It covers the full mod workflow - activating and ordering mods, browsing and installing from [mod.io](https://mod.io/g/anno-117-pax-romana), following curated collections, tweaking mod options and keeping track of what is installed with your own Presets.

> Built with Python, [pywebview](https://pywebview.flowrl.com/) and [Alpine.js](https://alpinejs.dev/). The UI is rendered by the platform's native web engine — WebView2 on Windows, WebKit2GTK on Linux, WKWebView on macOS — and the Python backend exposes its API to the page over the pywebview JS bridge. Runs on Windows (packaged as a standalone `.exe`) and Linux (from source).


**Hier geht es zum Readme auf Deutsch!** -> [readme](README_de.md)

---

## Table of Contents

- [Anno 117 Mod Manager](#anno-117-mod-manager)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Windows - Standalone Executable](#windows---standalone-executable)
    - [Linux / From Source](#linux--from-source)
  - [First Launch](#first-launch)
  - [Sidebar](#sidebar)
  - [Tabs](#tabs)
    - [News Tab](#news-tab)
    - [Mod Activation Tab](#mod-activation-tab)
      - [Mod List](#mod-list)
      - [Sorting \& Filtering](#sorting--filtering)
      - [Right Panel](#right-panel)
      - [Presets](#presets)
    - [Mod Browser Tab](#mod-browser-tab)
      - [Search \& Filters](#search--filters)
      - [Mod Cards](#mod-cards)
      - [Endorsement](#endorsement)
    - [Collections Tab](#collections-tab)
      - [Installing a Collection](#installing-a-collection)
      - [Uninstalling a Collection](#uninstalling-a-collection)
    - [Manual Install Tab](#manual-install-tab)
    - [Modloader Log Tab](#modloader-log-tab)
    - [Tweaking Tab](#tweaking-tab)
    - [Settings Tab](#settings-tab)
      - [General](#general)
      - [Game Files (Paths card)](#game-files-paths-card)
      - [Mod Storage](#mod-storage)
      - [mod.io Integration](#modio-integration)
      - [Advanced](#advanced)
  - [Mod Storage Locations](#mod-storage-locations)
  - [Presets](#presets-1)
  - [Load Order](#load-order)
  - [mod.io Integration](#modio-integration-1)
  - [News from mod.io](#news-from-modio)
  - [Localisation](#localisation)
    - [Known Issues](#known-issues)
  - [Debugging](#debugging)
  - [Troubleshooting](#troubleshooting)
  - [Support](#support)
  - [Credits](#credits)

---

## Requirements

| Dependency | Notes |
|---|---|
| Anno 117: Pax Romana | Game must be installed |
| Python 3.10+ | Only needed when running from source — code uses PEP 604 unions (`X \| None`) and `from __future__ import annotations` |
| `pywebview` | The native-webview window the whole UI lives in |
| `requests` | mod.io / Anno Union / GitHub release HTTP calls |
| Native web engine | **Windows:** WebView2 runtime (preinstalled on Win10+, otherwise from Microsoft). **Linux:** WebKit2GTK (`webkit2gtk-4.1`) + PyGObject (`gi`). **macOS:** WKWebView (system-bundled) |

---

## Installation

### Windows - Standalone Executable

1. Download the latest `Anno117ModManager.exe` from the [Releases](../../releases) page.
2. Place it anywhere - it bundles all assets internally.
3. Double-click to launch. No installation needed.

### Linux / From Source

**1. Install Python 3.10+ and the system libraries pywebview needs** (WebKit2GTK for the embedded browser engine and PyGObject for the GTK drag-and-drop bridge):

- Arch / Manjaro: `sudo pacman -S python webkit2gtk-4.1 python-gobject`
- Debian / Ubuntu: `sudo apt install python3 python3-gi gir1.2-webkit2-4.1`
- Fedora: `sudo dnf install python3 python3-gobject webkit2gtk4.1`

PyGObject (`gi`) is required even though it's not in `requirements.txt` — it lives in your distro's package manager because it builds against the system's GLib/GObject. The Linux drag-and-drop install path (`Manual Install` tab) talks to the GTK widget directly and silently degrades if `gi` is missing.

**2. Clone and install Python dependencies:**

```bash
git clone https://github.com/taludas/anno-117-mod-manager.git
cd anno-117-mod-manager
pip install --user pywebview requests
python app.py
```

If `pip install` complains about an *externally-managed environment* (PEP 668), either add `--break-system-packages`, install the deps from your distro's package manager (e.g. `python-pywebview python-requests` on Arch), or use a virtualenv. When using a virtualenv on Linux you must also pass `--system-site-packages` so pywebview can still import `gi` from your distro's PyGObject:

```bash
python -m venv --system-site-packages .venv
source .venv/bin/activate
pip install pywebview requests
python app.py
```

The app stores its settings and logs under `~/.config/Anno 117 Mod Manager/` on Linux. Anno 117 itself runs through Steam + Proton — the mod manager auto-detects the game in `~/.steam/steam/steamapps/common/` and looks for the in-game `Documents` folder inside the Proton prefix at `~/.steam/steam/steamapps/compatdata/<appid>/pfx/drive_c/users/steamuser/Documents/`.

---

## First Launch

On first start the app picks the UI language from your system locale (override any time with the round flag button in the top-right of the title bar — see `core/i18n.py` for the supported set).

The first launch is otherwise empty by design — no wizard. Open **Settings** (gear icon, bottom-left of the HUD) and:

1. **Locate Anno 117** — click *Auto-detect*. It searches the Windows registry, Steam library folders, Steam Proton compatdata prefixes and common install paths. If that fails, point *Browse File* at `Anno117.exe` directly, or *Browse Folder* at any parent of `Anno 117 - Pax Romana` (the inner `mods` folder also works).
2. **Documents folder override** — only set this when your Windows Documents folder has been relocated (or you're on Linux/Proton with an unusual prefix layout). Otherwise leave it blank; the app derives `~/Documents/Anno 117 - Pax Romana` (Windows) or the Proton prefix (Linux) automatically.
3. **mod.io integration** — optional. Paste an API key from [mod.io → API Keys](https://mod.io/me/access) and connect by email to enable the Browser, Collections and the mod.io news cards.

---

## Sidebar

The new UI replaces the old left-side rail with a **bottom HUD bar** styled like the in-game build menu, plus a top title bar.

**Title bar (top):**

- **Version pill** — shows the running version. Turns **green** when up to date, **red** when GitHub has a newer release. Click the red pill to open the release page.
- **Discord / GitHub / Ko-fi quick-links** — inline icons that open in your default external browser.
- **Language picker** — round flag button + dropdown.

**HUD bar (bottom), top row — tabs grouped left-to-right:**

- *Mods* group: **Mod Activation**, **Mod Browser**, **Collections**, **Manual Install**.
- *Tools* group: **News**, **Modloader Log**, **Tweaking**.

**HUD bar, bottom row — utility actions:**

- **Settings** (gear) — opens the Settings tab.
- **Refresh** — context-sensitive: refreshes the mod list on Activation, the mod.io listing on Browser/Collections, the feed on News.
- **Search** — live-filter on Activation, full mod.io query on Enter for Browser/Collections, disabled elsewhere.
- **Open mods folder** — opens the resolved mods directory in your file manager.
- **LAUNCH GAME** (large round button) — starts `Anno117.exe` with the current activation profile.

Browser and Collections require a valid mod.io token. Clicking either tab without one redirects you straight to **Settings** with the mod.io card highlighted.

---

## Tabs

### News Tab

Aggregates news from multiple sources in a single chronologically-sorted feed:

- **Anno Union** — official blog posts from the Anno development team (always on).
- **mod.io — new mods** — the 8 most recently published mods for Anno 117 (badge `NEW MOD`, requires mod.io connection).
- **mod.io — new collections** — the 5 most recently published collections (badge `NEW COLLECTION`, requires mod.io connection).
- **Reddit r/anno** — latest posts from the Anno subreddit. Off by default; toggle with the *Include r/anno posts* checkbox at the top of the News tab (also persisted to `settings.json` as `show_reddit_news`).

Each card shows a coloured source badge, date, title, summary and an optional thumbnail. Clicking a card from Anno Union or Reddit opens the article in your default browser; clicking a mod.io card deep-links into the in-app **Mod Browser / Collections** detail page (see [News from mod.io](#news-from-modio)).

The merged feed is cached in memory for 10 minutes — the **Refresh** button in the bottom HUD bypasses the cache.

---

### Mod Activation Tab

The primary tab for managing which mods are active when you launch the game.

#### Mod List

- Each installed mod is a row: activation **checkbox** on the left, a **2-letter category medallion** (the first two characters of the mod's category, uppercase), the category name, the mod name + version, file size, and an **Active / Off** pill on the right.
- Sub-mods (child folders inside a parent mod's folder) appear indented under their parent and have no Uninstall button — they're handled by the loader through the parent.
- The header row shows a master checkbox that activates / deactivates every top-level mod at once.

#### Sorting & Filtering

- Click the **Category**, **Name** or **Status** column headers to cycle ascending → descending → off.
- The **search bar in the bottom HUD** live-filters the list by mod name or category as you type — no minimum character count.
- The **Manage / Order** toggle switches between the standard sortable list (Manage) and a drag-and-drop view (Order). In Order mode the rows show a `⋮⋮` grip in place of the medallion and reordering is persisted to `active-profile.txt`.

#### Right Panel

Clicking a mod opens its detail panel on the right:

- Banner image (or a parchment placeholder if none is set in `modinfo.json`).
- Mod name, creator and version.
- Description.
- Category, difficulty modifier, size on disk, folder name.
- **Open Folder** — reveals the mod directory in your file manager.
- **Uninstall Mod** — deletes the folder after confirmation. Hidden for sub-mods.

#### Presets

Presets save and restore your full activation state (which mods are on or off).

- The **Profile** dropdown at the top of the Activation tab lists all saved presets plus two built-in reserved presets:
  - **Vanilla** — deactivates every installed mod. Cannot be deleted.
  - **Default** — activates every installed mod. Cannot be deleted.
- **New** — saves the current activation state under a new name.
- **Delete** — permanently removes the selected preset. Reserved presets cannot be deleted.
- Installing a mod.io collection automatically creates a preset named after the collection (sanitised — see [Collections Tab](#installing-a-collection)) and switches to it.
- Your last selected preset is persisted to `settings.json` (`active_profile_name`) and restored on next launch.

---

### Mod Browser Tab

Browse and install mods directly from mod.io without leaving the app. Requires a mod.io API key and a connected account (Settings → mod.io Integration). If either is missing, opening this tab redirects you to Settings.

#### Search & Filters

- **Search** — typed into the bottom HUD search input; press Enter to query mod.io.
- **Sort dropdown** (in the tab's own toolbar) — Newest, Most popular, Most downloaded, Top rated, A → Z.
- **Tag filter** — populated live from mod.io's `/games/{id}/tags` endpoint and grouped by tag taxonomy ("Type", "Difficulty", …). Collections use a different taxonomy on mod.io that this endpoint doesn't expose, so the tag filter is hidden on the Collections tab.
- **Author filter** — click an author's name on any card to restrict the listing to their mods. A pill at the top shows the active filter; click the ✕ on the pill to clear it. The active search term works the same way.

#### Mod Cards

Mods render as a responsive **cards grid** (~280 px min). Each card shows the thumbnail, name, author (clickable), last-updated date, the first tag plus a `+ N more` count, subscriber count, mod size, total downloads, and a primary **Install** button at the bottom that turns into **Update** when the mod is already on disk.

Hovering the thumbnail reveals two small overlay actions:

- **♥ Endorse** — one-shot, disables once cast.
- **+ Subscribe** — toggles to **✓** when subscribed.

Clicking the body of a card opens the **detail page** (full-width, with a Back button at the top) — full description (mod.io's HTML rendered after sanitisation), changelog, hero image, big Endorse and Subscribe buttons, and the Install / Update CTA. The "Open on mod.io" button hands the page off to your default browser.

The "currently installed" badge is **self-healing**: when a mod is installed via the Browser, a small `_modio_install.json` marker is written inside its folder. The Browser scans these markers on every refresh, so manually `rm -rf`'ing a mod's folder also removes the marker and the Installed state instantly disappears — no stale settings to clean up.

#### Endorsement

The **♥ Endorse** action on a card or detail page sends a positive rating to mod.io. It's one-way per session: once endorsed, the button stays disabled.

---

### Collections Tab

Collections are curated mod bundles published by the community on mod.io. The Collections tab shares the Mod Browser's UI — same cards grid, same search/sort, same detail page — backed by mod.io's separate `/collections` endpoint. The tag filter is hidden here because collections use a different taxonomy than mods.

Each collection card shows the bundle's mod count (`📚 N`) instead of subscriber count, plus the total bundle size and download count. The detail page adds a **Bundled mods** section underneath the description: each row is a thumbnail + name + author and is **click-through** — clicking a bundled mod swaps the detail page to that individual mod, with a **← Back to collection** button at the top to return.

#### Installing a Collection

Clicking **Install Collection** on the detail page:

1. Resolves the collection's bundled mods via `/collections/{id}/mods`.
2. Downloads and installs every bundled mod into your configured mods folder (skipping ones already on disk).
3. Creates a **preset file** named after the collection (sanitised to `[A-Za-z0-9 _-]`, capped at 50 chars; falls back to `Collection_<id>` if the name is empty or collides with the reserved `Default` / `Vanilla`). The preset has only the bundled mods enabled and `EnableNewMods false` so unrelated mods stay off.
4. Activates that preset.

The "already installed" detection uses the same preset name — so if the preset exists, the Collections card / detail flips its CTA from **Install Collection** to **Update Collection**.

#### Uninstalling a Collection

When the preset already exists, an extra **Uninstall Collection** button appears on the detail page. It always deletes the preset file and gives you the option to also wipe every mod folder that belongs to this collection — resolved live from the bundled mod list and matched against each folder's `_modio_install.json` marker.

---

### Manual Install Tab

For mods obtained outside of mod.io.

- **Click the drop zone (or the Browse button)** — opens the OS native file picker; pick a `.zip` and it's extracted into your mods folder.
- **Drag & Drop** — drag a `.zip` from your file manager onto the drop zone. On Windows / macOS this works through pywebview's standard DOM bridge. On Linux WebKit2GTK strips dropped file paths from the JS event for security, so the app installs a private GTK-side handler (`drag-data-received` on the WebKit widget) that captures the URI list before WebKit can sanitise it — this is why PyGObject (`gi`) is needed on Linux.

The installer validates that the archive contains a `modinfo.json`, prompts for overwrite if the target folder already exists, and respects your *Automatically activate newly installed mods* setting.

---

### Modloader Log Tab

Displays the `mod-loader.log` file written by the Anno Mod Loader after each game session.

- Lines containing `ERROR` (or the `[ERRO`-prefixed loader severity) are highlighted in red.
- Lines containing `WARN` are highlighted in yellow.
- Lines containing `[INFO]` are dimmed to neutral.
- **Refresh Log** — reloads the file from disk. The log file is capped at ~2 MB on read; oversized logs are tail-truncated and a small notice is shown.
- **Copy** — copies the visible content to the clipboard, useful for sharing bug reports on Discord.
- **Open File** — opens `mod-loader.log` in your default text editor.

---

### Tweaking Tab

Some mods expose configurable value options in their `modinfo.json` (colour values, toggles, enum choices etc.) if set up correctly by the author. The Tweaking tab lets you adjust these without editing files manually.

- The left panel lists every installed mod that exposes an Options block.
- Selecting a mod shows its options in the right panel. Four control types (see `core/options.py`):
  - **Enum** — dropdown with predefined choices.
  - **Toggle** — checkbox for boolean settings.
  - **Slider** — slider with min, max and step from the schema.
  - **Text** — free-text input (the fallback for any unknown type).
- Changes are saved to `active-options.jsonc` in your mods folder and applied the next time you launch the game.
- **Reset Mod** resets options for the selected mod. **Reset All** resets every mod at once.

---

### Settings Tab

The Settings tab is scrollable. It is organised in four cards:

#### General

The General card is intentionally minimal — most behaviour lives in defaults that don't need a switch.

- **Show r/anno posts in News feed** *(toggle, on the News tab itself)* — includes Reddit posts in the News feed.
- **Automatically activate newly installed mods** — dropdown with three values (`enable_new_mods`):
  - *On* — newly installed mods are enabled immediately.
  - *Off* — mods land deactivated.
  - *Keep* — preserve whatever active state the previous install had (useful for in-place updates).
- **Mod Location** — radio: *User Documents* or *Game Directory* (see below).

The UI language is **not** in the Settings tab — it's controlled by the round flag button in the top-right of the title bar.

#### Game Files (Paths card)

- **Anno 117 Installation Directory** — three buttons: *Browse File* (point at `Anno117.exe`), *Browse Folder* (parent of `Anno 117 - Pax Romana`, the folder itself, or the inner `mods` subfolder), and *Auto-detect* (registry + Steam library + Proton compatdata sweep).
- **Anno 117 Documents Folder (override)** — only needed if your Documents folder has been relocated. *Clear* is disabled when no override is set.
- A read-only "derived paths" block underneath shows the resolved Documents-mods folder, game-mods folder and `active-profile.txt` location so you can verify what the app actually computed.

#### Mod Storage

Picked via the **Mod Location** radio in the General card:

| Mode | Path |
|---|---|
| **User Documents** *(default)* | `~/Documents/Anno 117 - Pax Romana/mods/` |
| **Game Directory** | `<game install>/Anno 117 - Pax Romana/mods/` |

#### mod.io Integration

- **API Key** — paste your personal API key from [mod.io → API Keys](https://mod.io/me/access). Required for the Mod Browser and Collections tabs as well as the mod.io news cards. *Save* persists it; *Clear key* removes it.
- **Connect / Disconnect** — see the [mod.io Integration](#modio-integration) section below for the full flow. The card title shows a coloured badge reflecting the current state (no key / key only / connected, with the token's expiry date).

#### Advanced

- The app's data directory (`%APPDATA%\Anno 117 Mod Manager` on Windows, `~/.config/Anno 117 Mod Manager` on Linux) and the presets folder, each with an *Open* button.

---

## Mod Storage Locations

The app stores its own data in:

| Platform | Path |
|---|---|
| Windows | `%APPDATA%\Anno 117 Mod Manager\` |
| Linux | `~/.config/Anno 117 Mod Manager/` |

Files stored there:

| File | Purpose |
|---|---|
| `settings.json` | All app settings — the JS bridge can write only this whitelist of keys: `selected_language`, `show_reddit_news`, `enable_new_mods`, `mod_location_mode`, `modio_api_key`, `active_profile_name`. The backend additionally manages: `game_path`, `custom_docs_path`, `modio_token`, `modio_token_expires`, `modio_terms_agreed`. |
| `presets/<name>.txt` | Saved activation presets — one mod ID per line, optional `EnableNewMods true/false` sentinel. Collection installs land here too, named after the collection (sanitised). |

Per-mod marker file written **inside each mod folder** (not under the app's config dir):

| File | Purpose |
|---|---|
| `<mod folder>/_modio_install.json` | Marker dropped by the Browser/Collection installer. Records the mod.io ID, name_id, modfile id + version and the install timestamp. Used to detect "this folder is a mod.io install" without keeping a separate sidecar database — deleting the folder takes the marker with it. |

`active-profile.txt` lives in the **mods folder** (`<documents>/Anno 117 - Pax Romana/mods/active-profile.txt`), not in the app's config dir — that's where the Anno mod loader reads it from.

---

## Presets

A preset is a snapshot of your activation state — every mod and whether it is on or off. They are stored as plain `.txt` files in the `presets/` folder under the app's data directory (Settings → Advanced → *Open* shows the path). Format: one mod ID per line, `#` to comment out (= deactivate), and an optional `EnableNewMods true|false` sentinel on its own line that decides whether mods absent from the preset count as on or off.

Presets are portable — copy a `.txt` file in or out of `presets/` to back it up or share it.

Two reserved presets are always available and cannot be deleted:

- **Vanilla** — deactivates every installed mod.
- **Default** — activates every installed mod.

Installing a mod.io **collection** also creates a preset, named after the collection (sanitised to `[A-Za-z0-9 _-]`, max 50 chars). The Collections tab uses that preset's existence as its "already installed" signal.

---

## Load Order

The Anno mod loader applies patches in the order mods appear in `active-profile.txt`. This app does not auto-compute a load order from `LoadAfter` rules — it gives you a **manual drag-and-drop reorder** instead.

Switch the Activation tab to **Order** mode (the toggle next to *Manage* in the toolbar). The medallion turns into a `⋮⋮` grip; drag a row up or down to move it. The new order is saved straight to `active-profile.txt`. Sub-mods are hidden in this view to keep the list flat — they travel with their parent.

---

## mod.io Integration

The Mod Browser, Collections and the mod.io news cards talk to mod.io over its REST API. Authentication uses mod.io's **email-based OAuth** (no password) — exactly the flow [the official desktop docs describe](https://docs.mod.io/restapiref/#email-authentication-flow).

**Setup:**

1. Open Settings → mod.io Integration.
2. Paste your personal API key from [mod.io → API Keys](https://mod.io/me/access) and click *Save*. The key alone is enough for the public read-only endpoints (e.g. tag lists), but write actions (subscribe, endorse, install) need a token.
3. Click *Connect*, enter your email. The backend POSTs to `/oauth/emailrequest` and mod.io sends you a 5-character security code.
4. Type the code into the next field. The backend POSTs to `/oauth/emailexchange` along with your terms-agreed flag and receives an **access token valid for ~1 year**.

**Storage:**

- The bearer token + its expiry timestamp + the terms-agreed flag are written to `settings.json` (`modio_token`, `modio_token_expires`, `modio_terms_agreed`). No password ever touches disk.
- The token is treated as already-expired ~60 s before its real expiry so calls don't race the clock.

**Disconnect** clears `modio_token` and `modio_token_expires` from `settings.json` but **keeps your `modio_api_key`** — disconnect is "log out", not "forget my account binding". To fully forget the account, also click *Clear key* in the API Key row.

**Auto-redirect:** clicking the Mod Browser or Collections tab without a valid token sends you straight to Settings, scrolls to the mod.io card and pulses it gold — instead of dumping you on an empty list with a quiet "go connect" message.

If mod.io reports `error_ref 11074` ("terms updated") on `/oauth/emailexchange`, the app silently resets `modio_terms_agreed` so the next connect attempt re-collects your consent.

---

## News from mod.io

When you're connected to mod.io, the News tab merges two extra feeds on top of Anno Union (and Reddit if enabled):

- **8 newest mods** — badge `NEW MOD` (green).
- **5 newest collections** — badge `NEW COLLECTION` (gold).

Both come from `/games/{gid}/mods` and `/games/{gid}/collections` sorted by `-date_added`. Cards show the mod / collection logo as the thumbnail and the author + summary as the excerpt.

**Deep-linking:** clicking a mod.io news card does **not** open the mod.io page in your browser. It opens the matching detail page **inside the in-app Mod Browser / Collections tab** so you can install or endorse straight away. Anno Union / Reddit cards still open in your default external browser.

The merged feed is cached in memory for 10 minutes — the **Refresh** button in the bottom HUD bypasses the cache.

---

## Localisation

The app ships with **12 supported UI languages**, each with a complete translation table. The language defaults to your system locale on first launch (see `core/i18n.py` → `detect_system_lang`) and can be changed at any time via the round flag button in the title bar — it takes effect immediately, no restart needed.

| Language | Key |
|---|---|
| English | `english` |
| Deutsch | `german` |
| Français | `french` |
| Español | `spanish` |
| Italiano | `italian` |
| Polski | `polish` |
| Русский | `russian` |
| Português (Brasil) | `brazilian` |
| 日本語 | `japanese` |
| 한국어 | `korean` |
| 简体中文 | `simplified_chinese` |
| 繁體中文 | `traditional_chinese` |

The full catalogue lives in `core/i18n.py` (the `LANGUAGES` tuple). UI translations are stored in `frontend/js/app.js` under the `I18N_TABLES` object — one block per language key, ~204 keys per language. To add or correct a translation, edit the table in place; the language picker reads the catalogue dynamically.

### Known Issues
Localisation has been proof-read for the main views. On dense panels (Settings cards, mod.io detail page, alerts) some translated strings can overflow their button or column. If you spot one, please open an issue with a screenshot. All locales apart from English, German and French have been bootstrapped with DeepL — native-speaker corrections via PR are very welcome.

---

## Debugging

Set the environment variable `ANNO117_DEBUG=1` before launching to open the embedded webview's **devtools** (Inspector) at startup. This works on every backend pywebview supports — WebView2 on Windows, WebKit2GTK on Linux, WKWebView on macOS — and is the fastest way to inspect Alpine state, DOM, network calls or to read JS errors.

```bash
# Linux / macOS
ANNO117_DEBUG=1 python app.py

# Windows (PowerShell)
$env:ANNO117_DEBUG=1; python app.py
```

The flag is read once on startup (see `app.py` → `webview.start(debug=...)`) — toggle it off again for normal use, the inspector adds noticeable startup latency.

---

## Troubleshooting

**The app cannot find Anno 117**
Open Settings → Game Files. Click *Auto-detect* first — that searches Steam libraries (including Proton compatdata prefixes), the Ubisoft Launcher registry keys on Windows, and globs every drive root for `Anno 117 - Pax Romana/Bin/Win64/Anno117.exe` up to five directories deep. If auto-detect fails, use *Browse File* (point at `Anno117.exe`) or *Browse Folder* (any parent of `Anno 117 - Pax Romana`, the folder itself, or its inner `mods` subfolder).

**The app cannot find my documents folder**
On Windows the resolved path is `~/Documents/Anno 117 - Pax Romana/mods`; on Linux the app picks the path inside the Steam Proton prefix that contains `Anno 117 - Pax Romana`. If your Documents folder is elsewhere, set **Anno 117 Documents Folder (override)** in Settings → Game Files. The override should point at the directory **that contains** `Anno 117 - Pax Romana` (not the inner mods folder).

**Mods are not loading in-game**
Check the Modloader Log tab and `active-profile.txt` in your `~/Documents/Anno 117 - Pax Romana/mods/` folder — if there is a `#` in front of a mod ID, or `# not installed` after it, the game won't load it. Re-check in the Activation tab or ask on the Modding Discord.

**Mod Browser / Collections tab keeps bouncing me to Settings**
Both tabs require a valid mod.io bearer token. Open Settings → mod.io Integration, paste your API key, click *Connect* and complete the email-code flow. The page that opens after the redirect is the one you need — its card pulses gold when you arrive there. Sometimes mod.io's API is down: try again later or restart the app.

**Drag-and-drop on Linux does nothing**
WebKit2GTK strips dropped file paths from the JS event for security; the app works around this by hooking the GTK widget's `drag-data-received` signal directly. That code path needs PyGObject — install `python-gobject` (Arch), `python3-gi` (Debian/Ubuntu) or `python3-gobject` (Fedora) and relaunch. The terminal will print `[gtk-dnd] bridge connected` on success.

**Something went wrong and the app misbehaves**
Re-run with `ANNO117_DEBUG=1` (see the [Debugging](#debugging) section) to open the webview inspector — the JS console + the Python stdout from the terminal together cover almost every failure mode. When opening an issue, please paste the relevant terminal output and a screenshot.

---

## Support

- **Discord** - join via the button in the title bar or [this link](https://discord.gg/m4e7ZanMVp) and ask your question in #Taludas' Mods in the feedback forum
- **Ko-fi** - [support the developer](https://ko-fi.com/W7W8L558T)
- **Issues** - open a GitHub issue and include the terminal output (re-run with `ANNO117_DEBUG=1` if you can — see the [Debugging](#debugging) section)

---

## Credits

- Jakob Harder for his continued work and documentation on the [Anno mod loader](https://jakobharder.github.io/anno-mod-loader) initially written and released by Meow.
- Claude and Google Gemini for the real work - large parts of the code have been written with the help of AI.
- The Anno Mod Discord for their support and help.
