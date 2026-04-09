# Anno 117 Mod Manager

![Anno 117 Mod Manager Logo](data/ui/modmanager_logo.png)

This project is not affiliated with or endorsed by Ubisoft and/or mod.io.

---

A desktop application for managing mods for **Anno 117: Pax Romana**. It covers the full mod workflow - activating and ordering mods, browsing and installing from [mod.io](https://mod.io/g/anno-117-pax-romana), following curated collections, tweaking mod options and keeping track of what is installed with your own Presets.

> Built with Python and Tkinter. Runs on Windows (packaged as a standalone `.exe`) and Linux (from source).


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
      - [Mod Tiles](#mod-tiles)
      - [Installation Flow](#installation-flow)
      - [Endorsement](#endorsement)
    - [Collections Tab](#collections-tab)
      - [Following a Collection](#following-a-collection)
      - [Unfollowing](#unfollowing)
    - [Manual Install Tab](#manual-install-tab)
    - [Modloader Log Tab](#modloader-log-tab)
    - [Tweaking Tab](#tweaking-tab)
    - [Settings Tab](#settings-tab)
      - [General](#general)
      - [Game Files](#game-files)
      - [Mod Storage](#mod-storage)
      - [mod.io Integration](#modio-integration)
      - [Footer](#footer)
  - [Mod Storage Locations](#mod-storage-locations)
  - [Presets](#presets-1)
  - [Load Order](#load-order)
  - [Localisation](#localisation)
    - [Known Issues](#known-issues)
  - [Troubleshooting](#troubleshooting)
  - [Support](#support)
  - [Credits](#credits)

---

## Requirements

| Dependency | Notes |
|---|---|
| Anno 117: Pax Romana | Game must be installed |
| Python 3.11+ | Only needed when running from source |
| `pillow`, `requests`, `beautifulsoup4` | Python packages (source only) |
| `tkinterdnd2` *(optional)* | Enables drag-and-drop ZIP installation |

---

## Installation

### Windows - Standalone Executable

1. Download the latest `Anno117ModManager.exe` from the [Releases](../../releases) page.
2. Place it anywhere - it bundles all assets internally.
3. Double-click to launch. No installation needed.

### Linux / From Source

```bash
git clone https://github.com/taludas/anno-117-mod-manager.git
cd anno117-mod-manager
pip install pillow requests beautifulsoup4 tkinterdnd2
python anno117-modmanager.py
```

The app stores its settings and logs under `~/.config/Anno 117 Mod Manager/` on Linux.

---

## First Launch

On the very first start the app presents a **language selection screen** before anything else loads. Pick your preferred UI language and confirm - this choice is saved and can be changed later in Settings.

After language selection the app will:

1. **Locate Anno 117 automatically** - it searches the Windows registry, Steam library folders and common install paths. If it cannot find the game you will be prompted to select the installation directory manually.
2. **Locate your Anno 117 documents folder** - on most systems this is `~/Documents/Anno 117 - Pax Romana`. If your Documents folder has been moved to a non-standard location, the app will search all drives and prompt you to point it to the right folder if it cannot be found automatically.
3. **Ask whether you want to enable mod.io integration** - this is optional. You can enable it later in Settings at any time.

---

## Sidebar

The left sidebar is always visible and contains:

- **Tab buttons** - switch between all eight sections of the app.
- **Discord** - opens the community Discord server.
- **Ko-fi** - opens the developer's Ko-fi page if you want to support development.
- **Documentation** - opens this Github readme for information about the features of the app.
- **LAUNCH GAME** - saves the current mod state and launches Anno 117 directly. Before launching, the app checks for missing required dependencies and warns you if any active mods have unresolved incompatibilities.

---

## Tabs

### News Tab

Aggregates news from multiple sources in a single feed:

- **Anno Union** - official blog posts from the Anno development team.
- **mod.io new mods** - recently published mods for Anno 117.
- **mod.io subscription updates** - updates to mods you are **subscribed** to (requires mod.io login).
- **Collection updates** - changes to collections you **follow** (requires mod.io login).
- **Reddit r/anno** *(optional, enable in Settings)* - latest posts from the Anno subreddit.

Each card shows the source badge, date, title, summary and an optional thumbnail. Cards for mod.io items include a shortcut button to jump directly to that mod in the Mod Browser or Collections tab.

News is cached for the current session and only re-fetched when you click **Refresh News** or restart the app.

---

### Mod Activation Tab

The primary tab for managing which mods are active when you launch the game.

#### Mod List

- Each installed mod appears as a row with a ✔️ **checkbox** to activate or deactivate it.
- **Category badge** - shows the mod's category from its `modinfo.json`.
- **Status icons** appear before the mod name:

  | Icon | Meaning |
  |---|---|
  | 🖋️ (golden pen) | Mod has customisable options — **clicking navigates directly to that mod in the Tweaking tab** |
  | ✘ (red X) | Active incompatibility conflict with another enabled mod |
  | ... (orange three dots) | A required dependency is not installed |
  | ⏳️ (orange hourglass) | This mod is deprecated by another active mod |
  | ⚙ (teal mod.io logo) | Mod was installed via mod.io — **clicking opens that mod in the Mod Browser** |
  | **!** (gold, before ⚙) | A newer version is available on mod.io — **clicking directly starts the update download** |

- Mod names are coloured **red** for conflicts, **orange** for missing dependencies or deprecation.
- Sub-mods (child folders inside a mod) appear indented below their parent and cannot be uninstalled on their own.
- At startup the app checks mod.io for available updates for all your subscribed mods in the background. The gold **!** badge disappears as soon as you install the update.

#### Sorting & Filtering

- Click the ✔️ / **Category** / **Mod Name** column headers to sort. Category supports A→Z, Z→A and off.
- Use the **search bar** to filter by name or category. Results update after three characters.
- **Activate All** resets the profile so every installed mod is active.
- **Load Order** toggle switches to a read-only view showing the exact order in which the game will load mods, computed from `LoadAfter` dependency rules in each mod's `modinfo.json`.

#### Right Panel

Clicking any mod opens its detail panel on the right:

- Banner or thumbnail image (with a placeholder if none is provided).
- Version, creator, description.
- Difficulty modifier and game setup flags (Requires New Game, Safe to Remove, Multiplayer Compatible, Campaign safe).
- Full dependency list - **Requires**, **Optional**, **Load After**, **Deprecates**, **Incompatible** - each entry shows whether it is currently installed with a ✔ / ✘ / • indicator.
- **Known Issues** section if the mod lists any.
- Folder path and file size on disk.
- **Open Folder** - opens the mod's directory in Explorer / file manager.
- **↻ Reinstall** *(mod.io mods only)* - fetches the latest version from mod.io and reinstalls it (useful for updates). Appears to the left of the Unsubscribe button.
- **Uninstall Mod** - deletes the local files after confirmation. Warns if other active mods depend on it.
- **Unsubscribe** *(mod.io mods only)* - removes the mod.io subscription and uninstalls. Warns if other active mods depend on it.

#### Presets

Presets save and restore your full activation state (which mods are on or off).

- The **Active Profile** dropdown at the top lists all saved presets plus two built-in system presets:
  - **Vanilla** — deactivates every installed mod in one click. Cannot be deleted.
  - **Default** — activates every installed mod. Cannot be deleted.
- **Save As New** - saves the current state under a new name.
- **Delete** - permanently removes the selected preset. System presets cannot be deleted.
- Collection presets are created automatically when you follow a collection and are labelled *(Collection)*.

---

### Mod Browser Tab

Browse and install mods directly from mod.io without leaving the app. Requires a mod.io account and API key (configured in Settings).

#### Search & Filters

- **Search bar** - full-text search against the mod.io catalogue.
- **Sort** - Most Downloads, Alphabetical, Newest, Highest Rating, Author.
- **Tag filter** - dropdown populated from the game's tag list on mod.io; filter by any single tag.
- **Subscribed** toggle - show only mods you are currently subscribed to.
- The **✕** button resets both the search text and the tag filter simultaneously.

#### Mod Tiles

Each tile shows the mod thumbnail, name, author, download count, rating and file size. Clicking a tile opens the **detail popup** with the full description, gallery images and an **Install Mod** button. If you have subscribed outside of the Mod Browser to mods on mod.io, their subscribed status will be automatically synced, and a golden "!" is warning you, if you are subscribed, but do not have a local copy of the mod installed. Reinstall it via the ↻ Reinstall button and the warning vanishes. Same is true if you had the mod installed and subscribed through the Mod Browser but have cancelled the subscription outside it on mod.io - the "!" will prompt you to resubscribe to get the latest version and updates of the mod.

#### Installation Flow

Clicking **Install** on a tile or in the detail popup:

1. Checks for required dependencies and downloads them first if missing, with a progress window.
2. Downloads the mod archive to a temporary folder (cleaned up automatically after install).
3. Extracts and installs the mod into your configured mod folder.
4. Subscribes your mod.io account so you receive future updates in the News feed.
5. Switches to the Activation tab — the mod.io icon (⚙) appears next to the new mod's name immediately.

Installed mods show a **↻ Reinstall** button (for updates or file repair) and a **★ Subscribed** button that turns into **Unsubscribe** on hover.

#### Endorsement

You can **endorse** a mod directly from its tile to give the creator a rating on mod.io. This is a one-way action - once endorsed the button stays disabled.

---

### Collections Tab

Collections are curated sets of mods maintained by the community on mod.io.

- **Search bar** and **Tag filter** work the same as in the Mod Browser.
- **Followed** toggle shows only collections you have followed.
- Clicking a tile opens a **detail popup** with the collection's description, tag list and full mod list (each mod is a clickable link to its mod.io page).

#### Following a Collection

Clicking **Follow** on a collection:

1. Subscribes you to every mod in the collection on mod.io.
2. Downloads and installs any mods not already present locally.
3. Creates a **collection preset** in the Activation tab with those mods active and all others deactivated.
4. Switches automatically to the Activation tab so you can review the result.

#### Unfollowing

The **Unfollow** button gives you three options:

- **Unfollow + Remove Mods** - unsubscribes and deletes mods that belong only to this collection.
- **Unfollow Only** - removes the follow without touching local files.
- **Go Back** - cancels.

---

### Manual Install Tab

For mods obtained outside of mod.io.

- **Select .zip Archive** - opens a file picker; choose any mod `.zip` and the app extracts and installs it.
- **Drag & Drop** - drag a `.zip` directly onto the drop zone (requires `tkinterdnd2`).

The app validates that the archive contains a `modinfo.json`, handles overwrite confirmation if the mod folder already exists, and optionally activates the mod immediately depending on your Settings.

---

### Modloader Log Tab

Displays the `mod-loader.log` file written by the Anno Mod Loader after each game session.

- Lines containing `ERROR` are highlighted in red.
- Lines containing `WARNING` are highlighted in yellow.
- **Refresh Log** - reloads the file from disk.
- **Copy Text to Clipboard** - copies the entire log, useful for sharing bug reports on Discord.

---

### Tweaking Tab

Some mods expose configurable value options in their `modinfo.json` (colour values, toggles, enum choices etc.) if set up correctly by the author. The Tweaking tab lets you adjust these without editing files manually.

- The left panel lists all installed mods that have options.
- Selecting a mod shows its options in the right panel:
  - **Enum** - dropdown with predefined choices.
  - **Toggle** - checkbox for boolean settings.
  - **Text / Colour** - free-text entry; colour options include a colour-picker button for specific mods.
- Changes are saved to `active-options.jsonc` in your mod folder and applied next time you launch the game.
- **Reset to Default** resets options for the selected mod. **Reset All to Default** resets every mod at once.

---

### Settings Tab

The Settings tab is scrollable — use the mouse wheel or the scrollbar on the right to reach all sections.

#### General

- **Language** - change the UI language. Takes effect immediately, but restart is recommended.
- **Tutorial Infotips** - enables/disables hover tooltips throughout the app.
- **Show r/anno posts in News feed** - includes Reddit posts in the News tab.
- **Automatically activate newly installed mods** - dropdown with three options:
  - *Always activate* — newly installed mods are enabled immediately.
  - *Always deactivate* — mods are added to the list but left disabled.
  - *Follow current state* — if the mod was already active (e.g. a reinstall or update), it stays active; otherwise it stays disabled.

#### Game Files

- **Anno 117 Installation Directory** - set manually if auto-detection failed. You can select the game folder at any level — the parent of `Anno 117 - Pax Romana`, the folder itself, or the inner `mods` subfolder all work correctly.
- **Anno 117 Documents Folder (override)** - only needed if your Windows Documents folder has been relocated to a non-standard location. Browse to your `Documents/Anno 117 - Pax Romana` folder. The **Clear** button is disabled when no override is set.

#### Mod Storage

Choose where the app installs mods:

| Mode | Path |
|---|---|
| **User Documents** | `~/Documents/Anno 117 - Pax Romana/mods/` |
| **Game Directory** | `<game install>/Anno 117 - Pax Romana/mods/` |

#### mod.io Integration

- **API Key** - paste your personal API key from [mod.io → API Keys](https://mod.io/me/access). Required for the Mod Browser and Collections tabs.
- **Connect / Disconnect** - authenticate via email or revoke your session.
- Authentication uses a one-time email code flow and stores only a 1 year time-limited access token locally. No password is ever stored.

#### Footer

- **Open Config Folder** - opens the app's data directory (`%APPDATA%\Anno 117 Mod Manager` on Windows, `~/.config/Anno 117 Mod Manager` on Linux).
- **View Debug Log** - opens `debug.log`, useful when reporting issues.

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
| `settings.json` | All app settings |
| `active-profile.txt` | Which mods are active (written to the mod folder) |
| `presets/` | Saved activation presets |
| `endorsements.json` | Locally cached endorsement states |
| `subscriptions.json` | mod.io subscription list |
| `subscription_map.json` | Maps local mod IDs to mod.io IDs |
| `collection_follows.json` | Followed collections |
| `debug.log` | Rolling debug log (max 2 MB, auto-archived to `.bak`) |

---

## Presets

A preset is a snapshot of your activation state - every mod and whether it is on or off. They are stored as plain `.txt` files in the `presets/` folder and can be shared and imported or backed up manually - just go to the settings tab and open the config folder and copy/paste preset files in `presets/`.

Two system presets are always available and cannot be deleted:

- **Vanilla** — deactivates every installed mod.
- **Default** — activates every installed mod.

When you follow a collection a preset named `<Collection Name> (Collection)` is created automatically.

---

## Load Order

The load order determines the sequence in which the game applies mod patches. The app computes it from `LoadAfter` entries in each mod's `modinfo.json` using a two-phase topological sort:

1. **Normal phase** - mods without a wildcard `*` in `LoadAfter`, sorted by category then name.
2. **Late phase** - mods with `LoadAfter: ["*"]`, loaded after all normal mods.

Enable **Load Order** view in the Activation tab header to see the computed sequence. The position badge `#` shows each mod's final index.

---

## Localisation

The app ships with support for all in-game languages. The UI language is selected on first launch and can be changed at any time in Settings.

| Language | File |
|---|---|
| English | `texts_english.xml` |
| Deutsch | `texts_german.xml` |
| Français | `texts_french.xml` |
| Español | `texts_spanish.xml` |
| Italiano | `texts_italian.xml` |
| Polski | `texts_polish.xml` |
| Русский | `texts_russian.xml` |
| Português (Brasil) | `texts_brazilian.xml` |
| 日本語 | `texts_japanese.xml` |
| 한국어 | `texts_korean.xml` |
| 简体中文 | `texts_simplified_chinese.xml` |
| 繁體中文 | `texts_traditional_chinese.xml` |

Translation files live in `data/base/config/gui/`. To add or correct a translation, copy `texts_english.xml`, translate the `<Text>` values (leave `<LineId>` unchanged) and name the file accordingly.

### Known Issues
Localisation has been checked by me for all MAIN app windows. Especially on pop-up/alert/warning/error windows it can very well be, that localised text is too long for a window or button space. If you notice such errors, try resizing the window to resolve. Please open an issue with a screenshot for each occurence, so that I can work my way through them. Same for spelling/grammar mistakes, please support me to fully localise the app with our help as a native speaker - all locas apart from English and German have been created by DeepL.

---

## Troubleshooting

**The app cannot find Anno 117**
Go to Settings → Game Files → Browse and point it at the game's installation folder. You can select at any level — the parent folder, `Anno 117 - Pax Romana` itself, or the inner `mods` subfolder all work.

**The app cannot find my documents folder**
If your Windows Documents folder has been relocated (e.g. to another drive), the app will search all drives automatically. If that fails, use the **Anno 117 Documents Folder (override)** field in Settings → Game Files to point it to your `Anno 117 - Pax Romana/mods` folder directly.

**Mods are not loading in-game**
Check your modloader log and also your active-profiles.txt in your `~/Documents/Anno 117 - Pax Romana/mods/` folder - if there is a **#** infront of the mod or a **# not installed** after it, the game does not load the mod. Check again in your Activation tab or ask on the Modding Discord for help.

**Mod Browser / Collections tab is greyed out**
These tabs require a mod.io API key. Go to Settings → mod.io Integration, enter your key and connect your account. Sometimes mod.io API is down - then try again later or do a restart of the app.

**A mod shows a missing dependency warning**
The mod lists another mod as a hard requirement in its `modinfo.json` that is not installed. Install the dependency first, or use the **Activate Missing** button in the dependency dialog.

**A mod installed from the browser shows no mod.io icon / shows Uninstall instead of Unsubscribe**
This can happen if the mod's name on mod.io differs significantly from the name in its `modinfo.json`. The app tries several fuzzy-matching strategies to link the two. If it consistently fails, please open an issue with the mod name.

**Something went wrong and the app misbehaves**
Check the debug log at Settings → View Debug Log. It captures all `print` output and exceptions from the current session. Open an issue and attach your log with a description of what you did to get it.

---

## Support

- **Discord** - join via the button in the app sidebar or [this link](https://discord.gg/m4e7ZanMVp) and ask your question in #Taludas' Mods in the feedback forum
- **Ko-fi** - [support the developer](https://ko-fi.com/W7W8L558T)
- **Issues** - open a GitHub issue and attach your `debug.log`

---

## Credits

- Jakob Harder for his continued work and documentation on the [Anno mod loader](https://jakobharder.github.io/anno-mod-loader) initially written and released by Meow.
- Claude and Google Gemini for the real work - large parts of the code have been written with the help of AI.
- The Anno Mod Discord for their support and help.
