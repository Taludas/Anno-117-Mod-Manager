import os
import sys
import json
import ctypes
import platform
import tkinter as tk

# ── Platform detection ─────────────────────────────────────────────────────
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX   = platform.system() == "Linux"

# Guard Windows-only imports
if IS_WINDOWS:
    import winreg
    import ctypes.wintypes
from tkinter import ttk, filedialog, messagebox, simpledialog, scrolledtext, colorchooser
import subprocess
import shutil
import zipfile
import string
import glob
import re
from PIL import Image, ImageTk
import threading
import webbrowser
from io import BytesIO
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import html
import time
import io
import html as html_lib
import tempfile

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False

# --- Visual Styles & Fonts ---
BG_MAIN = "#0b192c"
BG_SECTION = "#162a45"
BG_HOVER = "#253b59"
FG_MAIN = "#ffffff"
FG_DIM = "#aaaaaa"
FG_GOLD = "#f1c40f"
FG_SEPARATOR = "#2a3b4c"

FONT_TITLE = ("Playfair Display SC", 16, "bold")
FONT_DESC = ("Marcellus", 11, "italic")
FONT_HEADER = ("Playfair Display SC", 13, "bold")
FONT_BODY = ("Marcellus", 13)
FONT_UI_BOLD = ("Marcellus", 14, "bold")
FONT_TAB_BOLD = ("Marcellus", 13, "bold")
FONT_BOLD_SMALL = ("Marcellus", 11, "bold")
FONT_SMALL = ("Marcellus", 11)
FONT_XSMALL = ("Marcellus", 10)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Icon Registry ---
ICONS = {
    "news":                   "data/ui/4k/base/icon_content/hud_rumor/icon_2d_rumor_generic.png",
    "modactivation":          "data/ui/4k/base/icon_content/generic/icon_2d_tendency.png",
    "modbrowser":             "data/ui/4k/base/icon_content/modio/icon_2d_modio_logo_white.png",
    "collections":            "data/ui/4k/base/icon_content/generic/icon_2d_specialist.png",
    "installation":           "data/ui/4k/base/icon_content/generic/icon_2d_install.png",
    "modloaderlog":           "data/ui/4k/base/icon_content/generic/icon_2d_questlog.png",
    "tweaking":               "data/ui/4k/base/icon_content/generic/icon_2d_rename.png",
    "settings":               "data/ui/4k/base/icon_content/generic/icon_2d_load_options.png",
    "kofi":                   "data/ui/4k/base/icon_content/kofi/kofi_symbol.png",
    "discord":                "data/ui/4k/base/icon_content/discord/discord_symbol.png",
    "docu":                   "data/ui/4k/base/icon_content/github/github_symbol.png",
    "launch":                 "data/ui/4k/base/icon_content/generic/icon_2d_options_controller.png",
    "refresh":                "data/ui/4k/base/icon_content/generic/icon_2d_reset.png",
    "open_folder":            "data/ui/4k/base/icon_content/generic/icon_2d_generic_item.png",
    "load_order":             "data/ui/4k/base/icon_content/generic/icon_2d_questlog.png",
    "activate_all":           "data/ui/4k/base/icon_content/generic/icon_2d_total_amount.png",
    "activation_sort_active": "data/ui/4k/base/icon_content/generic/icon_2d_check_mark.png",
    "activation_sort_inactive":"data/ui/4k/base/icon_content/generic/icon_2d_close_x.png",
    "save_preset":            "data/ui/4k/base/icon_content/generic/icon_2d_save.png",
    "delete_preset":          "data/ui/4k/base/icon_content/generic/icon_2d_bin.png",
    "install":                "data/ui/4k/base/icon_content/generic/icon_2d_install.png",
    "endorse":                "data/ui/4k/base/icon_content/attributes/icon_2d_health.png",
    "subscribed":             "data/ui/4k/base/icon_content/generic/icon_2d_favourite_generic.png",
    "follow":                 "data/ui/4k/base/icon_content/questtracker/icon_2d_questlog_writting_black.png",
    "unfollow":               "data/ui/4k/base/icon_content/diplomacy/icon_2d_contract_unavailable.png",
    "uninstall":              "data/ui/4k/base/icon_content/generic/icon_2d_bin.png",
    "unsubscribe":            "data/ui/4k/base/icon_content/diplomacy/icon_2d_diplomacy_reputation_threat_black.png",
    "visit":                  "data/ui/4k/base/icon_content/generic/icon_2d_region_global.png",
    "arrow_right":            "data/ui/4k/base/icon_content/generic/icon_2d_arrow_stylized_right.png",
    "arrow_left":             "data/ui/4k/base/icon_content/generic/icon_2d_arrow_stylized_left.png",
    "arrow_up":               "data/ui/4k/base/icon_content/generic/icon_2d_arrow_stylized_up.png",
    "arrow_down":             "data/ui/4k/base/icon_content/generic/icon_2d_arrow_stylized_down.png",
    "x":                      "data/ui/4k/base/icon_content/generic/icon_2d_close_x_red.png",
    "tick":                   "data/ui/4k/base/icon_content/generic/icon_2d_check_mark.png",
    "customized":             "data/ui/4k/base/icon_content/generic/icon_2d_rename_gold.png",
    "normal":                 "data/ui/4k/base/icon_content/generic/icon_2d_options.png",
    "missing_dependency":     "data/ui/4k/base/icon_content/generic/icon_2d_options_red.png",
    "deprecated":             "data/ui/4k/base/icon_content/generic/icon_2d_remaining_time_red.png",
    "modio_mod":              "data/ui/4k/base/icon_content/modio/icon_2d_modio_logo_blue.png",
    # News tab
    "news_refresh":          "data/ui/4k/base/icon_content/generic/icon_2d_reset.png",
    "news_visit":            "data/ui/4k/base/icon_content/generic/icon_2d_region_global.png",
    "open_in_browser":       "data/ui/4k/base/icon_content/modio/icon_2d_modio_logo_white.png",
    "open_in_collections":   "data/ui/4k/base/icon_content/modio/icon_2d_modio_logo_white.png",
    # Mod browser
    "subscribed_filter":     "data/ui/4k/base/icon_content/generic/icon_2d_favourite_generic.png",
    "endorsed":              "data/ui/4k/base/icon_content/generic/icon_2d_check_mark.png",
    "mod_visit":             "data/ui/4k/base/icon_content/generic/icon_2d_region_global.png",
    "install_mod":           "data/ui/4k/base/icon_content/generic/icon_2d_install_black.png",
    "reinstall":             "data/ui/4k/base/icon_content/generic/icon_2d_reset.png",
    "subscribed_state":      "data/ui/4k/base/icon_content/generic/icon_2d_favourite_generic_black.png",
    "unsubscribe_hover":     "data/ui/4k/base/icon_content/diplomacy/icon_2d_diplomacy_reputation_threat.png",
    # Tweaking
    "colorpicker_btn":       "data/ui/4k/base/icon_content/generic/icon_2d_appearance.png",
    "tweaking_shortcut":     "data/ui/4k/base/icon_content/generic/icon_2d_rename.png",
    "tweak_description":     "data/ui/4k/base/icon_content/questtracker/icon_2d_questlog_writting.png",
    # Right panel
    "open_folder_panel":     "data/ui/4k/base/icon_content/generic/icon_2d_generic_item.png",
    # Collections
    "followed_filter":       "data/ui/4k/base/icon_content/generic/icon_2d_favourite_generic.png",
    "collection_visit":      "data/ui/4k/base/icon_content/generic/icon_2d_region_global.png",
    "followed_state":        "data/ui/4k/base/icon_content/generic/icon_2d_favourite_generic_black.png",
    "unfollow_remove":       "data/ui/4k/base/icon_content/diplomacy/icon_2d_contract_unavailable.png",
    "unfollow_only":         "data/ui/4k/base/icon_content/diplomacy/icon_2d_trade_history.png",
}

_icon_cache: dict = {}

# Loads 117 Icons
def load_icon(key: str, size: tuple = (16, 16)):
    """Returns a PhotoImage for the icon key at the given pixel size. Returns None gracefully if the file is missing or fails to load."""
    cache_key = (key, size)
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]
    rel_path = ICONS.get(key)
    if not rel_path:
        return None
    abs_path = resource_path(rel_path)
    if not os.path.exists(abs_path):
        return None
    try:
        img   = Image.open(abs_path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        _icon_cache[cache_key] = photo
        return photo
    except Exception as e:
        print(f"[Icon] Failed to load '{key}': {e}")
        return None

# --- Fonts ---
FONT_FILES = [
    "data/fonts/PlayfairDisplaySC-Regular.ttf",
    "data/fonts/Marcellus-Regular.ttf"
]

def load_custom_font(font_path):
    """Registers a font file with the Windows system for the current process. On Linux Tkinter resolves fonts from the system font cache automatically."""
    if not os.path.exists(font_path):
        print(f"Font not found: {font_path}")
        return False
    if not IS_WINDOWS:
        return True  # Linux: font files are bundled; Tkinter resolves them via fontconfig
    FR_PRIVATE = 0x10
    res = ctypes.windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
    return res > 0

for f in FONT_FILES:
    load_custom_font(resource_path(f))

# --- Localisation ---
import xml.etree.ElementTree as _loca_et
import locale as _loca_locale

_loca_strings: dict = {}

_LANGUAGE_DISPLAY_NAMES = [
    ("english",            "English"),
    ("german",             "Deutsch"),
    ("french",             "Français"),
    ("spanish",            "Español"),
    ("italian",            "Italiano"),
    ("polish",             "Polski"),
    ("russian",            "Русский"),
    ("brazilian",          "Português (Brasil)"),
    ("japanese",           "日本語"),
    ("korean",             "한국어"),
    ("simplified_chinese", "简体中文"),
    ("traditional_chinese","繁體中文"),
]

_LANGUAGE_SETTINGS_KEY = "selected_language"

_LOCA_LANG_MAP = {
    'pt': 'brazilian', 'pt_br': 'brazilian',
    'en': 'english',
    'fr': 'french',
    'de': 'german',
    'it': 'italian',
    'ja': 'japanese',
    'ko': 'korean',
    'pl': 'polish',
    'ru': 'russian',
    'zh': 'simplified_chinese',
    'zh_cn': 'simplified_chinese',
    'es': 'spanish',
    'zh_tw': 'traditional_chinese',
}

def _load_loca(lang_name: str) -> dict:
    """Load a texts_<lang>.xml and return {int(LineId): str(Text)}."""
    path = resource_path(f"data/base/config/gui/texts_{lang_name}.xml")
    result = {}
    if not os.path.exists(path):
        return result
    try:
        tree = _loca_et.parse(path)
        for text_el in tree.getroot().findall('Text'):
            lid_el = text_el.find('LineId')
            txt_el = text_el.find('Text')
            if lid_el is not None and txt_el is not None:
                try:
                    result[int(lid_el.text)] = (txt_el.text or '')
                except ValueError:
                    pass
    except Exception as e:
        print(f"[Loca] Failed to load {path}: {e}")
    return result

def _detect_lang() -> str:
    """Detect system language and map to a loca filename stem."""
    try:
        loc = _loca_locale.getlocale()[0] or 'en'
        code = loc.lower().replace('-', '_')
        # Try full code first (e.g. zh_tw), then prefix (e.g. zh)
        if code in _LOCA_LANG_MAP:
            return _LOCA_LANG_MAP[code]
        prefix = code.split('_')[0]
        if prefix in _LOCA_LANG_MAP:
            return _LOCA_LANG_MAP[prefix]
    except Exception:
        pass
    return 'english'

def _init_loca(override_lang: str = None):
    global _loca_strings
    lang = override_lang or _detect_lang()
    _loca_strings = _load_loca(lang)
    if not _loca_strings:
        _loca_strings = _load_loca('english')

def T(line_id: int, *args) -> str:
    """Return localised string, optionally formatting with positional {0} args."""
    s = _loca_strings.get(line_id, f"[{line_id}]")
    if args:
        try:
            return s.format(*args)
        except (IndexError, KeyError):
            return s
    return s

# _init_loca() is called inside AnnoModManagerApp.__init__ after language selection

# --- Mod.io integration ---
MODIO_GAME_ID = "11358"
MODIO_BASE_URL = "https://g-11358.modapi.io/v1"

# Virtual-scroll constants for the Mod Browser
_VR_H   = 645   # pixel height per tile row (tile 620px + 10px top/bottom padding)
_VR_C   = 3     # tile columns
_VR_BUF = 2   # extra rows above/below viewport kept alive
_VR_COL_H = 545  # pixel height per collections tile row (tile 520px + 10+15px padding)



# --- Main Application Class ---
def _open_path(path):
    """Opens a file or directory in the system's default application, cross-platform: Explorer on Windows, xdg-open on Linux, open on macOS."""
    try:
        if IS_WINDOWS:
            os.startfile(path)
        elif IS_LINUX:
            subprocess.Popen(['xdg-open', path])
        else:
            subprocess.Popen(['open', path])
    except Exception as e:
        print(f"[open_path] Could not open '{path}': {e}")

class AnnoModManagerApp(TkinterDnD.Tk):
    def __init__(self):
        """Initialises the main application window, sets up all state variables, loads settings and metadata, builds the UI and schedules the language-picker / first-run sequence."""
        super().__init__()
        self.title("Anno 117 Mod Manager")
        self.iconbitmap(resource_path("data/ui/anno117_mod_manager.ico"))
        self.geometry("1440x900")
        self.configure(bg=BG_MAIN)

        # 1. Initialize variables
        self.game_exe_path = ""
        self.mod_path = ""
        self.mod_loc_mode = tk.StringVar(value="Documents")
        self.sort_active_first = True
        self.sort_cat_dir = 0
        self.sort_name_dir = 1
        self.last_clicked_col = "status"
        self._news_images = []
        self.browser_offset = 0

        # Globals for settings, stats and Search and mod.io
        self.mod_statuses = {}
        self.current_profile_name = "Default"
        self.current_search_query = ""
        self.enable_new_mods_var = tk.StringVar(value="on") # "on"=always activate, "off"=always deactivate, "keep"=preserve prior state
        self.show_load_order = False
        self.show_reddit_news_var = tk.BooleanVar(value=False)
        self.show_tooltips_var = tk.BooleanVar(value=True)
        self._endorsement_states = {}
        self._modio_update_available: set = set() # local mod IDs with a newer version on mod.io
        self._subscription_states = {}
        self._subscription_modio_map = {}
        self._collection_follow_states = {}

        # 2. Setup AppData Folder (cross-platform)
        if IS_WINDOWS:
            appdata_root = (os.getenv('APPDATA') or os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming'))
        else:
            # Linux: follow XDG Base Directory spec
            appdata_root = (os.getenv('XDG_CONFIG_HOME') or os.path.join(os.path.expanduser('~'), '.config'))
        self.appdata_dir = os.path.join(appdata_root, "Anno 117 Mod Manager")
        if not os.path.exists(self.appdata_dir):
            os.makedirs(self.appdata_dir)
        self.settings_file = os.path.join(self.appdata_dir, "settings.json")
        self.custom_docs_path = ""  # override for relocated Documents folder

        self.settings = {}

        # 3. Setup Presets Storage
        self.presets_dir = os.path.join(self.appdata_dir, "presets")
        if not os.path.exists(self.presets_dir):
            os.makedirs(self.presets_dir)

        self.available_presets = []
        self.refresh_presets_list()

        # 4. Load Settings with Mod.io integration or Run Initial Setup
        self.modio_terms_agreed = False
        self.modio_token_expires = 0  # Unix timestamp from API
        self.load_settings()
        self.modio_api_key = self.settings.get("modio_api_key", "")
        self.use_mod_browser = self.settings.get("use_mod_browser", None)
        self.modio_declined = self.settings.get("modio_declined", False)
        self.modio_token = self.settings.get("modio_token", "")
        self._endorsement_states = self._load_endorsements()
        self._subscription_states = self._load_subscriptions()
        self._subscription_modio_map = self._load_subscription_map()
        self._collection_follow_states = self._load_collection_follows()
        self.jump_to_activation = self.settings.get("jump_to_activation", True)
        self.after(150, self._start_sequence)

        # After paths are set, get metadata
        self.get_all_mod_metadata()
        self.build_ui()

    # --- Find/selet Anno Installation Folder ---
    def get_drive_letters(self):
        """Returns a list of all logical drive letters (Windows) or mount points (Linux). On Windows queries the kernel bitmask; on Linux returns common mount roots."""
        if not IS_WINDOWS:
            # On Linux the game would be installed via Steam under /home or /mnt
            candidates = ['/']
            for entry in ['/home', '/mnt', '/media', '/run/media']:
                if os.path.isdir(entry):
                    try:
                        for sub in os.scandir(entry):
                            if sub.is_dir():
                                candidates.append(sub.path)
                    except PermissionError:
                        pass
            return candidates
        drives = []
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(f"{letter}:")
            bitmask >>= 1
        return drives

    def find_anno_exe(self):
        """Searches the Windows registry (Ubisoft launcher and Steam) and common installation directories for Anno117.exe. Returns the full path if found, otherwise an empty string."""
        possible_roots = []

        if IS_WINDOWS:
            reg_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Ubisoft\Launcher\Installs\117"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Ubisoft\Launcher\Installs\117"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 3274580"),
            ]
            for hive, key_path in reg_paths:
                try:
                    with winreg.OpenKey(hive, key_path) as key:
                        for val_name in ["InstallDir", "InstallLocation"]:
                            try:
                                path, _ = winreg.QueryValueEx(key, val_name)
                                if path: possible_roots.append(path)
                            except FileNotFoundError: continue
                except (FileNotFoundError, OSError): continue

            program_files = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
            possible_roots.append(os.path.join(program_files, "Ubisoft", "Ubisoft Game Launcher", "games", "Anno 117 - Pax Romana", "Anno 117"))
            possible_roots.append(os.path.join(program_files, "Steam", "steamapps", "common", "Anno 117 - Pax Romana", "Anno 117"))
        else:
            # Linux: Steam typical install locations
            home = os.path.expanduser('~')
            possible_roots += [
                os.path.join(home, '.steam', 'steam', 'steamapps', 'common', 'Anno 117 - Pax Romana', 'Anno 117'),
                os.path.join(home, '.local', 'share', 'Steam', 'steamapps', 'common', 'Anno 117 - Pax Romana', 'Anno 117'),
                '/usr/share/steam/steamapps/common/Anno 117 - Pax Romana/Anno 117',
            ]

        drives = self.get_drive_letters()

        # Glob directly for the exe at every plausible depth, on every drive.
        # This finds the path regardless of what folder structure precedes it.
        exe_patterns = [
            os.path.join("Anno 117 - Pax Romana", "Bin", "Win64", "Anno117.exe"),
            os.path.join("*", "Anno 117 - Pax Romana", "Bin", "Win64", "Anno117.exe"),
            os.path.join("*", "*", "Anno 117 - Pax Romana", "Bin", "Win64", "Anno117.exe"),
            os.path.join("*", "*", "*", "Anno 117 - Pax Romana", "Bin", "Win64", "Anno117.exe"),
            os.path.join("*", "*", "*", "*", "Anno 117 - Pax Romana", "Bin", "Win64", "Anno117.exe"),
            os.path.join("*", "*", "*", "*", "*", "Anno 117 - Pax Romana", "Bin", "Win64", "Anno117.exe"),
        ]

        for drive in drives:
            for pattern in exe_patterns:
                full_pattern = os.path.join(drive + os.sep, pattern)
                try:
                    for match in glob.glob(full_pattern):
                        if os.path.isfile(match):
                            return os.path.abspath(match)
                except Exception:
                    continue

        # Fall back to the known-root candidates collected above (registry / fixed paths)
        for root in list(dict.fromkeys(possible_roots)):
            if not root or not os.path.exists(root):
                continue
            for target in [
                os.path.join(root, "Bin", "Win64", "Anno117.exe"),
                os.path.join(root, "Anno 117 - Pax Romana", "Bin", "Win64", "Anno117.exe"),
                os.path.join(root, "Anno117.exe"),
            ]:
                if os.path.exists(target):
                    return os.path.abspath(target)

        return None

    # --- First Start Logic ---
    def _start_sequence(self):
        """Covers the main window with a language picker wall, then proceeds."""
        self._show_language_picker()
        try:
            if not self.winfo_exists():
                return
        except Exception:
            return
        self._build_sidebar()
        self.switch_tab("News")
        self.check_first_run()

    def _show_language_picker(self):
        """Shows a full-window BG_SECTION overlay for language selection on first launch. Blocks until the user confirms, then destroys the overlay."""
        saved = self.settings.get(_LANGUAGE_SETTINGS_KEY)
        if saved:
            _init_loca(saved)
            return

        # Full-window covering wall
        wall = tk.Frame(self, bg=BG_SECTION)
        wall.place(x=0, y=0, relwidth=1, relheight=1)
        wall.lift()
        self.update_idletasks()

        # Centre column
        inner = tk.Frame(wall, bg=BG_SECTION)
        inner.place(relx=0.5, rely=0.5, anchor="center")

        _banner_path = resource_path("data/ui/modmanager_logo.png")
        if os.path.exists(_banner_path):
            try:
                _banner_img = Image.open(_banner_path).convert("RGBA")
                _bw, _bh = _banner_img.size
                _target_w = min(350, _bw)
                _target_h = int(_bh * (_target_w / _bw))
                _banner_img = _banner_img.resize((_target_w, _target_h), Image.Resampling.LANCZOS)
                _banner_photo = ImageTk.PhotoImage(_banner_img)
                _banner_lbl = tk.Label(inner, image=_banner_photo, bg=BG_SECTION)
                _banner_lbl.image = _banner_photo
                _banner_lbl.pack(pady=(0, 0))
            except Exception:
                tk.Label(inner, text="Anno 117 Mod Manager", font=FONT_TITLE, bg=BG_SECTION, fg=FG_GOLD).pack(pady=(0, 6))
        else:
            tk.Label(inner, text="Anno 117 Mod Manager", font=FONT_TITLE, bg=BG_SECTION, fg=FG_GOLD).pack(pady=(0, 6))

        tk.Label(inner, text="Select your language  /  Wählen Sie Ihre Sprache  /  Choisissez votre langue / Seleziona la tua lingua / Selecciona tu idioma / Selecione seu idioma / Wybierz swój język / Выберите язык / 言語を選択してください / 언어를 선택하십시오 / 选择您的语言 / 選擇您的語言", font=FONT_XSMALL, bg=BG_SECTION, fg=FG_DIM, wraplength=420, justify="center").pack(pady=(0, 16))

        # Language list
        list_frame = tk.Frame(inner, bg=BG_MAIN, highlightthickness=1, highlightbackground=FG_SEPARATOR)
        list_frame.pack(fill="x", padx=0, pady=(0, 16))

        selected_var = tk.StringVar(value="english")

        for lang_key, lang_display in _LANGUAGE_DISPLAY_NAMES:
            row = tk.Frame(list_frame, bg=BG_MAIN)
            row.pack(fill="x")
            rb = tk.Radiobutton(row, text=lang_display, variable=selected_var, value=lang_key, font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN, selectcolor=BG_SECTION, activebackground=BG_HOVER, activeforeground=FG_MAIN, cursor="hand2", anchor="w")
            rb.pack(fill="x", padx=16, pady=3)

        def _confirm():
            chosen = selected_var.get()
            self.settings[_LANGUAGE_SETTINGS_KEY] = chosen
            self.save_settings()
            _init_loca(chosen)
            wall.destroy()

        btn_ok = tk.Button(inner, text="Okay", font=FONT_UI_BOLD, bg="#2ecc71", fg="#000000", width=14, cursor="hand2", relief="raised", command=_confirm)
        btn_ok.pack(pady=(0, 4))
        wall.bind_all("<Return>", lambda e: _confirm())

        def _on_main_close():
            sys.exit(0)

        self.protocol("WM_DELETE_WINDOW", _on_main_close)

        try:
            self.wait_window(wall)
        except Exception:
            sys.exit(0)

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _find_or_prompt_docs_folder(self):
        """Searches all available drives for the Documents/Anno 117 - Pax Romana mods folder. If found automatically, stores it; otherwise prompts the user to locate it."""
        import glob as _glob
        drives = self.get_drive_letters()
        patterns = [
            os.path.join("Documents", "Anno 117 - Pax Romana", "mods"),
            os.path.join("*", "Documents", "Anno 117 - Pax Romana", "mods"),
            os.path.join("*", "*", "Documents", "Anno 117 - Pax Romana", "mods"),
        ]
        for drive in drives:
            for pat in patterns:
                for match in _glob.glob(os.path.join(drive + os.sep, pat)):
                    profile = os.path.join(match, "active-profile.txt")
                    if os.path.exists(profile):
                        # match is the /mods folder — step up to "Anno 117 - Pax Romana"
                        self.custom_docs_path = os.path.normpath(os.path.dirname(match))
                        self.update_mod_path_from_mode()
                        self.save_settings()
                        print(f"[docs] Auto-detected Anno docs folder: {self.custom_docs_path}")
                        return
        # Not found — prompt user
        self._imperial_alert(T(1999101473), T(1999101474))
        chosen = filedialog.askdirectory(title=T(1999101475))
        if chosen:
            chosen = os.path.normpath(chosen)
            # Accept either "Anno 117 - Pax Romana" or its "mods" subfolder
            if os.path.basename(chosen).lower() == "mods":
                chosen = os.path.dirname(chosen)
            self.custom_docs_path = chosen
            self.update_mod_path_from_mode()
            self.save_settings()

    def check_first_run(self):
        """Called once at startup after language selection. Locates the game executable, prompts the user if not found, configures mod paths and kicks off the mod.io setup flow when needed."""
        # Only search if load_settings didn't already give us a valid path
        if not self.game_exe_path or not os.path.exists(self.game_exe_path):
            self.game_exe_path = self.find_anno_exe()

        if not self.game_exe_path:
            self._imperial_alert(T(1999101187), T(1999101220))
            manual_root = filedialog.askdirectory(title="Select Anno 117 Installation Directory")
            if manual_root:
                if not self.set_game_path_from_root(os.path.normpath(manual_root)):
                    self.game_exe_path = ""
            else:
                self.game_exe_path = ""

        self.update_mod_path_from_mode()

        # Robust docs folder detection — search all drives if default path has no profile
        if not os.path.exists(self.active_profile_path) and not getattr(self, "custom_docs_path", ""):
            self._find_or_prompt_docs_folder()

        if self.use_mod_browser is None:
            # Custom mod.io-branded prompt with logo
            win_w, win_h = 520, 420
            mb_win = tk.Toplevel(self)
            mb_win.title(T(1999101141))
            mb_win.geometry(f"{win_w}x{win_h}")
            self.update_idletasks()
            x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
            y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
            mb_win.geometry(f"+{x}+{y}")
            mb_win.configure(bg=BG_MAIN)
            mb_win.transient(self)
            mb_win.grab_set()

            result = {"ans": False}
            def _sel(val):
                result["ans"] = val
                mb_win.destroy()

            self._add_modio_logo(mb_win, bg=BG_MAIN)
            tk.Label(mb_win, text=T(1999101001), font=FONT_TITLE, bg=BG_MAIN, fg=FG_GOLD).pack(pady=(0, 8))
            tk.Label(mb_win, text=T(1999101002), font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, wraplength=440, justify="center").pack(pady=8, expand=True)

            btn_frame = tk.Frame(mb_win, bg=BG_MAIN)
            btn_frame.pack(pady=(0, 24))
            btn_yes = tk.Button(btn_frame, text=T(1999101003), font=FONT_UI_BOLD, bg="#2ecc71", fg="#000000", width=12, cursor="hand2", command=lambda: _sel(True))
            btn_yes.pack(side="left", padx=10)
            self._bind_hover(btn_yes, "#2ecc71", "#36e780")
            btn_no = tk.Button(btn_frame, text=T(1999101004), font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, width=12, cursor="hand2", command=lambda: _sel(False))
            btn_no.pack(side="left", padx=10)
            self._bind_hover(btn_no, BG_SECTION, BG_HOVER)

            mb_win.bind("<Return>", lambda e: _sel(True))
            mb_win.bind("<Escape>", lambda e: _sel(False))
            self.wait_window(mb_win)
            ans = result["ans"]

            if ans:
                self.settings["use_mod_browser"] = True
                self.save_settings()
                self._prompt_api_key_setup()
            else:
                self.settings["use_mod_browser"] = False
                self.save_settings()
                self.refresh_sidebar_state()
        elif self.settings.get("use_mod_browser") and not self.settings.get("modio_api_key"):
            self._prompt_api_key_setup()
        elif self.settings.get("use_mod_browser") and self.settings.get("modio_api_key"):
            if not self.settings.get("modio_token"):
                self._prompt_modio_auth()
            else:
                expires = getattr(self, 'modio_token_expires', 0)
                now_ts  = int(datetime.now().timestamp())
                if expires and now_ts >= expires:
                    # Token has definitively expired per server-issued timestamp
                    self.modio_token = ""
                    self.modio_token_expires = 0
                    self.settings["modio_token"] = ""
                    self.settings["modio_token_expires"] = 0
                    self.save_settings()
                    self.refresh_sidebar_state()
                    self._imperial_alert(T(1999101188), T(1999101221), is_error=True)
                    self._prompt_modio_auth()

    # --- Mod Activation and Presets ---
    def parse_active_profile(self):
        """Parses active-profile.txt to determine mod status and saves it globally."""
        mod_status_map = {}
        self.enable_new_mods = True

        if not os.path.exists(self.active_profile_path):
            self.mod_statuses = mod_status_map
            return mod_status_map

        with open(self.active_profile_path, 'r', encoding='utf-8') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line or clean_line.startswith("##"):
                    continue

                if "EnableNewMods" in clean_line:
                    self.enable_new_mods = not clean_line.startswith("#")
                    continue

                is_uninstalled = "# not installed" in clean_line.lower()
                is_active = not clean_line.startswith("#")

                mod_id = clean_line.replace("#", "").replace("not installed", "").strip()
                if mod_id:
                    mod_status_map[mod_id] = {
                        "active": is_active,
                        "uninstalled": is_uninstalled
                    }

        self.mod_statuses = mod_status_map
        return mod_status_map

    def get_dir_size(self, path):
        """Helper to calculate total folder size in bytes."""
        total = 0
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file(): total += entry.stat().st_size
                    elif entry.is_dir(): total += self.get_dir_size(entry.path)
        except: pass
        return total

    def get_all_mod_metadata(self):
        """Scans all configured mod directories (User Documents and/or Game Directory depending on the storage mode setting) and returns a flat list of mod metadata dicts."""
        all_mods = []
        search_paths = []

        # 1. Use custom docs path if provided, otherwise default to ~/Documents
        if getattr(self, 'custom_docs_path', ''):
            docs_base = os.path.normpath(self.custom_docs_path)
        else:
            docs_base = os.path.normpath(os.path.join(os.path.expanduser("~/Documents"), "Anno 117 - Pax Romana"))

        docs_mods = os.path.join(docs_base, "mods")
        if os.path.exists(docs_mods):
            search_paths.append(docs_mods)

        # 2. Check the Game Directory
        if self.game_exe_path:
            game_root = os.path.dirname(os.path.dirname(os.path.dirname(self.game_exe_path)))
            game_mods = os.path.normpath(os.path.join(game_root, "mods"))
            if os.path.exists(game_mods) and game_mods not in search_paths:
                search_paths.append(game_mods)

        # 3. Fallback: Ensure the active mod_path is included just in case
        if getattr(self, 'mod_path', '') and os.path.exists(self.mod_path) and self.mod_path not in search_paths:
            search_paths.append(self.mod_path)

        seen_folders = set()
        for base in search_paths:
            try:
                for entry in os.scandir(base):
                    if entry.is_dir() and not entry.name.startswith(".") and not entry.name.startswith("-"):
                        if entry.name not in seen_folders:
                            self._scan_folder(entry.path, all_mods)
                            seen_folders.add(entry.name)
            except Exception as e:
                print(f"Error scanning {base}: {e}")

        self.mods = all_mods
        return all_mods

    def _scan_folder(self, path, mod_list, parent_path=None):
        """Recursively reads a single mod folder, parses its modinfo.json/.jsonc and appends a metadata dict to mod_list. Skips folders whose name starts with '-'. Also descends into sub-mod directories."""
        if os.path.basename(path).startswith("-"):
            return

        info_json = os.path.join(path, "modinfo.json")
        info_jsonc = os.path.join(path, "modinfo.jsonc")

        target_file = info_json if os.path.exists(info_json) else (info_jsonc if os.path.exists(info_jsonc) else None)

        if target_file:
            try:
                with open(target_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                    if target_file.endswith(".jsonc"):
                        content = self.strip_jsonc_comments(content)

                    data = json.loads(content)

                    if not isinstance(data, dict):
                        return

                    m_id = data.get("ModID")
                    if not m_id: return

                    # Map app language keys → modinfo.json language keys
                    _MODINFO_LANG_MAP = {
                        "english": "English",
                        "german": "German",
                        "french": "French",
                        "spanish": "Spanish",
                        "italian": "Italian",
                        "polish": "Polish",
                        "russian": "Russian",
                        "brazilian": "Portugese",
                        "japanese": "Japanese",
                        "korean": "Korean",
                        "simplified_chinese": "Chinese",
                        "traditional_chinese":"Taiwanese",
                    }
                    _app_lang = self.settings.get(
                        _LANGUAGE_SETTINGS_KEY, _detect_lang())
                    _modinfo_lang = _MODINFO_LANG_MAP.get(_app_lang, "English")

                    def get_localized(key, default=""):
                        val = data.get(key)
                        if isinstance(val, list):
                            # KnownIssues is a list of dicts
                            parts = []
                            for entry in val:
                                if isinstance(entry, dict):
                                    text = (entry.get(_modinfo_lang)
                                            or entry.get("English")
                                            or "")
                                    if text:
                                        parts.append(text.strip())
                            return "\n\n".join(parts) if parts else default
                        if isinstance(val, dict):
                            return (val.get(_modinfo_lang)
                                    or val.get("English")
                                    or default)
                        elif isinstance(val, str):
                            return val
                        return default

                    raw_category = get_localized("Category")
                    category_display = f"{raw_category} " if raw_category else ""

                    deps = data.get("Dependencies", {})
                    if not isinstance(deps, dict):
                        deps = {}

                    mod_entry = {
                        "id": m_id,
                        "name": get_localized("ModName", get_localized("Name", m_id)),
                        "category": category_display,
                        "version": str(data.get("Version", "1.0.0")),
                        "desc": get_localized("Description", "No description."),
                        "known_issues": get_localized("KnownIssues", ""),
                        "creator": data.get("CreatorName", ""),
                        "contact": data.get("CreatorContact", ""),
                        "has_options": "Options" in data,
                        "path": path,
                        "parent_path": parent_path,
                        "manually_disabled": os.path.basename(path).startswith("-"),
                        "setup": data.get("GameSetup", {}) if isinstance(data.get("GameSetup"), dict) else {},
                        "diff": data.get("Difficulty", "Normal"),
                        "deps": {
                            "Require": data.get("Dependencies", {}).get("Require", []) if isinstance(data.get("Dependencies"), dict) else [],
                            "Optional": data.get("Dependencies", {}).get("Optional", []) if isinstance(data.get("Dependencies"), dict) else [],
                            "LoadAfter": data.get("Dependencies", {}).get("LoadAfter", []) if isinstance(data.get("Dependencies"), dict) else [],
                            "Deprecate": data.get("Dependencies", {}).get("Deprecate", []) if isinstance(data.get("Dependencies"), dict) else [],
                            "Incompatible": data.get("Dependencies", {}).get("Incompatible", []) if isinstance(data.get("Dependencies"), dict) else []
                        }
                    }
                    mod_list.append(mod_entry)

                    for sub in os.scandir(path):
                        if sub.is_dir():
                            self._scan_folder(sub.path, mod_list, parent_path=path)

            except Exception as e:
                print(f"Error parsing {target_file}: {e}")

    def strip_jsonc_comments(self, text):
        """Removes both block (/* … */) and line (//) comments from a JSONC string while leaving string literals untouched, returning valid JSON."""
        pattern = r'("(?:\\.|[^\\"])*")|(/\*[\s\S]*?\*/)|(//.*)'
        def replace(match):
            if match.group(1): return match.group(1)
            return ""
        return re.sub(pattern, replace, text)

    def save_preset(self):
        """Prompts the user for a preset name via a styled dialog, then writes the current active-profile.txt state to a named .txt file in the presets directory."""
        if not os.path.exists(self.active_profile_path):
            self._imperial_alert(T(1999101189), T(1999101222), is_error=True)
            return

        # --- Custom Styled Input for Preset Name ---
        name_win = tk.Toplevel(self)
        name_win.title(T(1999101005))

        # Define size
        win_w, win_h = 500, 280
        name_win.geometry(f"{win_w}x{win_h}")

        # 2. Centering logic
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        name_win.geometry(f"+{x}+{y}")

        name_win.configure(bg=BG_MAIN)
        name_win.transient(self)
        name_win.grab_set()

        tk.Label(name_win, text=T(1999101006), font=FONT_TITLE, bg=BG_MAIN, fg=FG_GOLD).pack(pady=(30, 10))
        tk.Label(name_win, text=T(1999101007), font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN).pack(pady=5)

        name_var = tk.StringVar()
        entry = tk.Entry(name_win, textvariable=name_var, font=FONT_BODY, bg=BG_SECTION, fg=FG_MAIN, insertbackground=FG_MAIN, relief="flat", width=30, justify="center")
        entry.pack(pady=15, ipady=5)
        entry.focus_set()

        result = {"name": None}

        def _confirm():
            raw_name = name_var.get().strip()
            if raw_name:
                # Sanitize filename
                clean_name = "".join([c for c in raw_name if c.isalnum() or c in ' ']).strip()
                result["name"] = clean_name
            name_win.destroy()

        btn_confirm = tk.Button(name_win, text=T(1999101008), font=FONT_UI_BOLD, bg="#07C1D8", fg=FG_MAIN, padx=20, cursor="hand2", command=_confirm)
        btn_confirm.pack(pady=10)
        self._bind_hover(btn_confirm, "#07C1D8", "#09E2FF")

        self.wait_window(name_win)

        preset_name = result["name"]

        if preset_name:
            file_path = os.path.join(self.presets_dir, f"{preset_name}.txt")
            try:
                self._write_clean_preset(self.active_profile_path, file_path)
                self.current_profile_name = preset_name
                self.refresh_presets_list()
                self.save_settings()
                self.render_activation_tab()
                self._imperial_alert(T(1999101280), T(1999101355, preset_name))
            except Exception as e:
                self._imperial_alert(T(1999101189), T(1999101385, e), is_error=True)

    def _write_clean_preset(self, source_path, dest_path):
        """Write a copy of the profile with '# not installed' lines stripped. Saves the active/disabled state of installed mods only."""
        clean_lines = []
        with open(source_path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith("##"):
                    clean_lines.append(line)
                    continue
                if "# not installed" in stripped.lower():
                    continue
                clean_lines.append(line)
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.writelines(clean_lines)

    def _apply_preset_with_full_coverage(self, preset_path):
        """Loads a preset file and writes active-profile.txt with explicit entries for every currently installed mod — active if listed in the preset, commented out otherwise. This prevents mods installed after the preset was saved from being implicitly active because they're absent from the file."""
        # Parse which mod IDs the preset activates
        preset_active = set()
        preset_disabled = set()
        header_lines = []
        with open(preset_path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith('##'):
                    header_lines.append(line)
                    continue
                if 'EnableNewMods' in stripped:
                    header_lines.append(line)
                    continue
                if '# not installed' in stripped.lower():
                    continue
                if stripped.startswith('#'):
                    mod_id = stripped.lstrip('#').strip()
                    # Only treat as a mod ID if it looks like one (no spaces, reasonable length)
                    if mod_id and ' ' not in mod_id and len(mod_id) < 100:
                        preset_disabled.add(mod_id)
                    else:
                        header_lines.append(line)
                else:
                    # Capture the active mods!
                    mod_id = stripped.split('#')[0].strip() # Strip inline comments if any
                    if mod_id and ' ' not in mod_id and len(mod_id) < 100:
                        preset_active.add(mod_id)

        # Build a complete profile covering every installed top-level mod
        all_mods = self.get_all_mod_metadata()
        out_lines = header_lines if header_lines else ['# Preset\n', '# EnableNewMods\n']
        for m in all_mods:
            if m.get('parent_path'):
                continue
            mid = m['id']
            if mid in preset_active:
                out_lines.append(f"{mid}\n")
            else:
                out_lines.append(f"# {mid}\n")

        with open(self.active_profile_path, 'w', encoding='utf-8') as f:
            f.writelines(out_lines)

    def load_preset(self):
        """Opens a file-picker so the user can import an external preset file, backs up the current profile, applies the loaded preset and refreshes the activation tab."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Select Mod Profile to Load"
        )

        if file_path:
            try:
                # Create backup
                if os.path.exists(self.active_profile_path):
                    backup_path = self.active_profile_path + ".bak"
                    shutil.copy2(self.active_profile_path, backup_path)

                self._apply_preset_with_full_coverage(file_path)

                preset_name = os.path.basename(file_path).replace(".txt", "")
                self.current_profile_name = preset_name
                self.save_settings()

                self._imperial_alert(T(1999101209), T(1999101356, preset_name))
                self._warn_missing_preset_mods(self.active_profile_path)

                if self.current_tab == "Mod Activation":
                    self.render_activation_tab()
            except Exception as e:
                self._imperial_alert(T(1999101208), T(1999101386, e), is_error=True)

    def refresh_presets_list(self):
        """Scans the presets folder for .txt files."""
        if not os.path.exists(self.presets_dir):
            os.makedirs(self.presets_dir, exist_ok=True)

        # Get all files except we reserve "Default"
        files = [f.replace(".txt", "") for f in os.listdir(self.presets_dir) if f.endswith(".txt") and f.lower() != "default"]

        self.available_presets = ["Vanilla", "Default"] + sorted(files)

    def on_preset_dropdown_change(self, event):
        """Fires when the user picks a different entry in the preset combobox. Switches to the Default profile or loads the selected named preset and refreshes the view."""
        selection = self.preset_combo.get()

        if selection == "Vanilla":
            self._reset_to_no_mods_profile()
            self._imperial_alert(T(1999101190), T(1999101465))
        elif selection == "Default":
            self.reset_to_default_profile()
            self._imperial_alert(T(1999101190), T(1999101223))
        else:
            preset_path = os.path.join(self.presets_dir, f"{selection}.txt")
            if os.path.exists(preset_path):
                self._apply_preset_with_full_coverage(preset_path)
                self.current_profile_name = selection
                self._warn_missing_preset_mods(self.active_profile_path)

        self.save_settings()
        self.render_activation_tab()

    def reset_to_default_profile(self):
        """Force-activates all discovered mods in the active-profile.txt"""
        all_mods = self.get_all_mod_metadata()
        prefix = "" if self.enable_new_mods_var.get() in ("on", "keep") else "# "
        lines = ["# Anno 117 Default Profile\n", f"{prefix}EnableNewMods\n"]

        for mod in all_mods:
            # We skip sub-mods (nested folders) as the loader handles them via the parent or internal logic
            if not mod.get('parent_path'):
                lines.append(f"{mod['id']}\n")

        with open(self.active_profile_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        self.current_profile_name = "Default"
        self.save_settings()

    def _reset_to_no_mods_profile(self):
        """Deactivates all mods by out-commenting every mod ID in active-profile.txt."""
        all_mods = self.get_all_mod_metadata()
        lines = ["# Anno 117 No Mods Active Profile\n", "# EnableNewMods\n"]
        for mod in all_mods:
            if not mod.get('parent_path'):
                lines.append(f"# {mod['id']}\n")
        with open(self.active_profile_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        self.current_profile_name = "Vanilla"
        self.save_settings()

    def _warn_missing_preset_mods(self, profile_path):
        """Reads a preset profile file and warns if any active mod IDs are not currently installed. Call after the preset has been copied into place."""
        if not os.path.exists(profile_path):
            return

        installed_ids = {m['id'] for m in self.get_all_mod_metadata()}

        missing = []
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                for line in f:
                    clean = line.strip()
                    if not clean or clean.startswith("#"):
                        continue
                    if "EnableNewMods" in clean:
                        continue
                    mod_id = clean.split("#")[0].strip()
                    if mod_id and mod_id not in installed_ids:
                        missing.append(mod_id)
        except Exception as e:
            print(f"Failed to check preset for missing mods: {e}")
            return

        if missing:
            mod_list = "\n".join(f"  •  {mid}" for mid in missing)
            self._imperial_alert(T(1999101409), T(1999101410, mod_list), is_error=True, scrollable=True)

    def delete_preset(self):
        """Asks for confirmation then permanently deletes the currently selected named preset file, reverts the active profile to Default and re-renders the activation tab."""
        selection = self.preset_combo.get()
        if selection in ("Vanilla", "Default"):
            self._imperial_alert(T(1999101191), T(1999101224), is_error=True)
            return

        msg = T(1999101350, selection)
        confirm = self._imperial_question(T(1999101281), msg)

        if confirm:
            try:
                file_path = os.path.join(self.presets_dir, f"{selection}.txt")
                if os.path.exists(file_path):
                    os.remove(file_path)

                # Force switch to Default and trigger the all-mod activation logic
                self.current_profile_name = "Default"
                self.reset_to_default_profile()

                self.save_settings()
                self.render_activation_tab()

                self._imperial_alert(T(1999101201), T(1999101357, selection))
            except Exception as e:
                self._imperial_alert(T(1999101189), T(1999101387, e), is_error=True)

    # ==========================================
    # --- MANUALL INSTALLATION TAB ---
    # ==========================================
    def browse_for_zip(self):
        """Opens a file-picker filtered to .zip files and passes the selected archive to run_install_logic."""
        zip_path = filedialog.askopenfilename(
            title="Select Mod ZIP File",
            filetypes=[("ZIP Files", "*.zip")]
        )
        if zip_path:
            self.run_install_logic(zip_path)

    def handle_dnd_drop(self, event):
        """Tkinter drag-and-drop handler. Extracts the dropped file path and forwards it to run_install_logic if it is a .zip archive, otherwise shows an error."""
        file_path = event.data.strip('{}')
        if file_path.lower().endswith('.zip'):
            self.run_install_logic(file_path)
        else:
            self._imperial_alert(T(1999101192), T(1999101225), is_error=True)

    def run_install_logic(self, zip_path, silent=False):
        """Validates the mod storage path, extracts the dropped or selected .zip archive into the correct mod folder (handling overwrites and conflicts), activates the mod if the setting is on and refreshes the UI."""
        target_base_dir = self.mod_path

        if not target_base_dir:
            self._imperial_alert(T(1999101193), T(1999101226), is_error=True)
            return

        if not os.path.exists(target_base_dir):
            os.makedirs(target_base_dir, exist_ok=True)

        try:
            with zipfile.ZipFile(zip_path, 'r') as zref:
                mod_internal_path = None
                for file_info in zref.infolist():
                    if file_info.filename.endswith("modinfo.json"):
                        mod_internal_path = os.path.dirname(file_info.filename)
                        break

                if mod_internal_path is None:
                    self._imperial_alert(T(1999101194), T(1999101227), is_error=True)
                    return

                if mod_internal_path:
                    folder_name = os.path.basename(mod_internal_path)
                else:
                    folder_name = os.path.basename(zip_path).replace(".zip", "")

                final_destination = os.path.join(target_base_dir, folder_name)

                if os.path.exists(final_destination):
                    msg = T(1999101351, folder_name)

                    confirm = self._imperial_question(T(1999101210), msg)

                    if not confirm:
                        return
                    shutil.rmtree(final_destination)

                temp_extract = os.path.join(target_base_dir, "_temp_ext")
                zref.extractall(temp_extract)
                actual_mod_src = os.path.join(temp_extract, mod_internal_path)

                os.makedirs(target_base_dir, exist_ok=True)
                shutil.move(actual_mod_src, final_destination)

                if os.path.exists(temp_extract):
                    shutil.rmtree(temp_extract)

                new_mod_id = None
                for info_file in ["modinfo.json", "modinfo.jsonc"]:
                    info_path = os.path.join(final_destination, info_file)
                    if os.path.exists(info_path):
                        try:
                            with open(info_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if info_file.endswith(".jsonc"):
                                    content = self.strip_jsonc_comments(content)
                                info_data = json.loads(content)
                                new_mod_id = info_data.get("ModID")
                        except:
                            pass
                        break

                if new_mod_id:
                    # Refresh metadata now so the new mod's deps are available for the incompatibility check before we decide to activate it.
                    self.mods = self.get_all_mod_metadata()
                    self.parse_active_profile()

                    _av = self.enable_new_mods_var.get()
                    if _av == "keep":
                        # If the mod existed before, preserve its prior active state; otherwise default to inactive
                        auto_activate = self.mod_statuses.get(new_mod_id, {}).get("active", False)
                    else:
                        auto_activate = (_av == "on")

                    if self._check_and_confirm_incompatible(new_mod_id):
                        self.toggle_mod_status(new_mod_id, auto_activate)
                    else:
                        # User chose to keep the mod disabled – add it to the profile as inactive so it appears in the list.
                        self.toggle_mod_status(new_mod_id, False)
                        self.mods = self.get_all_mod_metadata()
                        self.parse_active_profile()
                        self._imperial_alert(T(1999101212), T(1999101388, folder_name))
                        if getattr(self, 'jump_to_activation', True):
                            self.switch_tab("Mod Activation", select_id=new_mod_id)
                        return

                self.mods = self.get_all_mod_metadata()
                self.parse_active_profile()

                # Apply any pending mod.io mapping now that self.mods is fresh
                if getattr(self, '_pending_modio_mapping', None):
                    modio_id, modio_name = self._pending_modio_mapping
                    # If we successfully parsed the real ModID, map it directly without guessing!
                    if new_mod_id:
                        self._subscription_modio_map[new_mod_id] = str(modio_id)
                        self._save_subscription_map()
                    else:
                        self._store_modio_mapping(modio_id, modio_name)
                    self._pending_modio_mapping = None

                if not silent:
                    if new_mod_id and self.enable_new_mods_var.get() == "off":
                        self._imperial_alert(T(1999101212), T(1999101389, folder_name))
                    else:
                        self._imperial_alert(T(1999101201), T(1999101354, folder_name))
                    if getattr(self, 'jump_to_activation', True):
                        self.switch_tab("Mod Activation", select_id=new_mod_id)

        except Exception as e:
            self._imperial_alert(T(1999101282), T(1999101390, e), is_error=True)

    def render_installation_tab(self):
        """Builds the Manual Install tab UI: a Nexus URL paste field, a ZIP file picker and a drag-and-drop target rectangle."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        tk.Label(self.main_content, text=T(1999101038), font=FONT_TITLE, bg=BG_MAIN, fg=FG_MAIN).pack(pady=(20, 10))

        install_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        install_frame.pack(pady=10)

        tk.Label(install_frame, text=T(1999101039), font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN).pack(side="left", padx=10)

        btn_select = tk.Button(install_frame, text=T(1999101040), font=FONT_SMALL, bg=BG_SECTION, fg=FG_MAIN, cursor="hand2", command=self.browse_for_zip, activebackground=FG_DIM, relief="raised", padx=10, bd=2)
        btn_select.pack(side="left")
        self._bind_hover(btn_select, BG_SECTION, BG_HOVER)

        dnd_text = T(1999101428) if HAS_DND else T(1999101429)

        self.dnd_rect = tk.Label(self.main_content, text=dnd_text, font=FONT_DESC, bg=BG_SECTION, fg=FG_DIM, width=50, height=8, relief="groove", bd=2)
        self.dnd_rect.pack(pady=20, padx=40)

        if HAS_DND:
            self.dnd_rect.drop_target_register(DND_FILES)
            self.dnd_rect.dnd_bind('<<Drop>>', self.handle_dnd_drop)
            self.dnd_rect.dnd_bind('<<DropEnter>>', lambda e: self.dnd_rect.config(bg="#1c3a5e"))
            self.dnd_rect.dnd_bind('<<DropLeave>>', lambda e: self.dnd_rect.config(bg=BG_SECTION))

    # ==========================================
    # --- MAIN UI LAYOUT ---
    # ==========================================
    def build_ui(self):
        """Constructs the full application window layout: sidebar with tab buttons, launch button, ko-fi / discord buttons, the main content area and the right info panel. Called once after language init."""
        INFO_WIDTH = 500
        self.sidebar_buttons = {}
        self.current_tab = "News"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0, minsize=INFO_WIDTH)

        self.sidebar = tk.Frame(self, bg=BG_SECTION, width=200)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.sidebar.pack_propagate(False)

        # Sidebar contents built in _build_sidebar(), called after _init_loca()

        self.main_content = tk.Frame(self, bg=BG_MAIN)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.right_panel = tk.Frame(self, bg=BG_SECTION, width=INFO_WIDTH, borderwidth=0, highlightthickness=0)
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=(5, 5), pady=5)
        self.right_panel.grid_propagate(False)

        self.lbl_right_title = tk.Label(self.right_panel, text=T(1999101009), font=FONT_HEADER, bg=BG_SECTION, fg=FG_MAIN)
        self.lbl_right_title.pack(pady=10)

        # switch_tab called from _start_sequence after sidebar is built

    # Sidebar Buttons
    def _build_sidebar(self):
        """Populates the sidebar with tab buttons and the launch button. Must be called after _init_loca() so T() returns correct strings."""
        # Clear any existing content (handles language switch rebuilds)
        for widget in self.sidebar.winfo_children():
            widget.destroy()
        self.sidebar_buttons = {}

        _TAB_ICON_KEYS = {"News": "news", "Mod Activation": "modactivation", "Manual Install": "installation", "Mod Browser": "modbrowser", "Collections": "collections", "Modloader Log": "modloaderlog", "Tweaking": "tweaking", "Settings": "settings"}
        _TAB_DISPLAY = {
            "News": T(1999101148),
            "Mod Activation": T(1999101149),
            "Mod Browser": T(1999101150),
            "Collections": T(1999101151),
            "Manual Install": T(1999101152),
            "Modloader Log": T(1999101153),
            "Tweaking": T(1999101154),
            "Settings": T(1999101155)
        }
        tabs = ["News", "Mod Activation", "Mod Browser", "Collections", "Manual Install", "Modloader Log", "Tweaking", "Settings"]

        for tab in tabs:
            border_frame = tk.Frame(self.sidebar, bg=BG_MAIN, highlightthickness=1, highlightbackground=BG_MAIN, bd=0)
            border_frame.pack(fill="x", padx=10, pady=5)

            tab_ico = load_icon(_TAB_ICON_KEYS.get(tab, ""), (24, 24))
            label = f"  {_TAB_DISPLAY.get(tab, tab)}"
            btn = tk.Button(border_frame, text=label, font=FONT_TAB_BOLD, cursor="hand2", bg=BG_MAIN, fg=FG_MAIN, activebackground=BG_HOVER, relief="flat", bd=0, image=tab_ico, anchor="w", compound="left" if tab_ico else "none", command=lambda t=tab: self.switch_tab(t))
            if tab_ico:
                btn.image = tab_ico
            btn.pack(fill="both", expand=True)

            self.sidebar_buttons[tab] = btn
            self._bind_sidebar_hover(btn, tab)

            if tab == "Mod Browser":
                self.mod_browser_btn = btn
            if tab == "Collections":
                self.collections_btn = btn

            if tab == "Settings":
                separator_top = tk.Frame(self.sidebar, bg=FG_DIM, height=1, bd=0, highlightthickness=0)
                separator_top.pack(fill="x", padx=20, pady=(10, 10))

                def open_kofi():
                    webbrowser.open("https://ko-fi.com/W7W8L558T")

                def open_discord():
                    webbrowser.open("https://discord.gg/m4e7ZanMVp")

                def open_docs():
                    webbrowser.open("https://github.com/taludas/anno-117-mod-manager")

                self.discord_border = tk.Frame(self.sidebar, bg="#5865F2", highlightthickness=1, highlightbackground="#5865F2", bd=0)
                self.discord_border.pack(fill="x", padx=10, pady=(5, 2))

                discord_ico = load_icon("discord", (24, 24))
                self.discord_btn = tk.Button(self.discord_border, text="  Mod Corner\nDiscord", command=open_discord, image=discord_ico, compound="left", bg="#5865F2", fg="white", font=("Marcellus", 10, "bold"), relief="flat", bd=0, cursor="hand2", pady=8)
                self.discord_btn.pack(fill="both", expand=True)
                self._bind_border_button_hover(self.discord_btn, "#5865F2", "#6c75f3")

                docu_ico = load_icon("docu", (24, 24))
                self.docs_border = tk.Frame(self.sidebar, bg="#4c565f", highlightthickness=1, highlightbackground="#4c565f", bd=0)
                self.docs_border.pack(fill="x", padx=10, pady=(2, 2))
                self.docs_btn = tk.Button(self.docs_border, text="  Github\n  Readme", command=open_docs, image=docu_ico, compound="left", bg="#4c565f", fg="white", font=("Marcellus", 10, "bold"), relief="flat", bd=0, cursor="hand2", pady=8)
                self.docs_btn.pack(fill="both", expand=True)
                self._bind_border_button_hover(self.docs_btn, "#4c565f", "#65717c")

                separator_bottom = tk.Frame(self.sidebar, bg=FG_DIM, height=1, bd=0, highlightthickness=0)
                separator_bottom.pack(fill="x", padx=20, pady=(10, 10))

                kofi_ico = load_icon("kofi", (24, 24))
                self.kofi_border = tk.Frame(self.sidebar, bg="#5F032E", highlightthickness=1, highlightbackground="#5F032E", bd=0)
                self.kofi_border.pack(fill="x", padx=10, pady=(5, 5))
                self.kofi_btn = tk.Button(self.kofi_border, text=" Support me on Ko-fi!", command=open_kofi, image=kofi_ico, compound="left", bg="#5F032E", fg="white", font=("Marcellus", 10, "bold"), relief="flat", bd=0, cursor="hand2", pady=8)
                self.kofi_btn.pack(fill="both", expand=True)
                self._bind_border_button_hover(self.kofi_btn, "#5F032E", "#82043f")

        self.refresh_sidebar_state()

        # Launch button
        self.launch_broder = tk.Frame(self.sidebar, bg="#2e7d32", highlightthickness=1, highlightbackground="#2e7d32", bd=0)
        self.launch_broder.pack(side="bottom", fill="x", padx=10, pady=(0, 5))
        _launch_ico = load_icon("launch", (42, 42))
        self.btn_launch = tk.Button(self.launch_broder, text=T(1999101159), font=FONT_TITLE, bg="#2e7d32", fg=FG_MAIN, cursor="hand2", command=self.launch_game, relief="flat", pady=5, image=_launch_ico, compound="left" if _launch_ico else "none")
        if _launch_ico:
            self.btn_launch.image = _launch_ico
        self.btn_launch.pack(fill="both", expand=True)
        self._bind_border_button_hover(self.btn_launch, "#2e7d32", "#388e3c")

    def _update_sidebar_highlights(self):
        """Sets the gold outline on the wrapper frame and dark background on the button."""
        if not hasattr(self, 'sidebar_buttons'):
            return
        for tab_name, btn in self.sidebar_buttons.items():
            is_disabled = str(btn['state']) == 'disabled'
            border_frame = btn.master

            if tab_name == self.current_tab and not is_disabled:
                # Active and Enabled: Gold border (on frame) + Permanent Hover BG (on both)
                btn.config(bg=BG_HOVER, fg=FG_MAIN)
                border_frame.config(bg=BG_HOVER, highlightbackground=FG_GOLD)
            elif is_disabled:
                # DISABLED STATE
                btn.config(bg=BG_MAIN, fg=FG_DIM)
                border_frame.config(bg=BG_MAIN, highlightbackground=BG_MAIN)
            else:
                # Inactive: No gold border, standard background
                btn.config(bg=BG_MAIN, fg=FG_MAIN)
                border_frame.config(bg=BG_MAIN, highlightbackground=BG_MAIN)

    def _bind_sidebar_hover(self, btn, tab_name):
        """Attaches Enter/Leave hover effects to a sidebar tab button and its containing border frame, highlighting both on mouse-over when the button is not disabled."""
        border_frame = btn.master

        def on_enter(e):
            if str(btn['state']) != 'disabled':
                btn.config(bg=BG_HOVER)
                border_frame.config(bg=BG_HOVER)

        def on_leave(e):
            # Keep BG_HOVER only if it's the active tab and NOT disabled
            if self.current_tab == tab_name and str(btn['state']) != 'disabled':
                btn.config(bg=BG_HOVER)
                border_frame.config(bg=BG_HOVER)
            else:
                btn.config(bg=BG_MAIN)
                border_frame.config(bg=BG_MAIN)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def refresh_sidebar_state(self):
        """Greys out the Mod Browser if the API key is missing."""
        has_api_key = bool(self.settings.get("modio_api_key"))

        for attr in ('mod_browser_btn', 'collections_btn'):
            btn = getattr(self, attr, None)
            if btn:
                if not has_api_key:
                    btn.config(state="disabled", fg=FG_DIM, cursor="X_cursor")
                else:
                    btn.config(state="normal", fg=FG_MAIN, cursor="hand2")

        # Refresh all buttons to ensure the active one stays highlighted
        self._update_sidebar_highlights()

    def switch_tab(self, tab_name, select_id=None, **kwargs):
        """Switches the main content area to the requested tab, guards mod.io tabs behind an API-key check, updates the sidebar highlight and dispatches to the correct render_* method."""
        if tab_name in ("Mod Browser", "Collections") and not self.settings.get("modio_api_key"):
            self._imperial_alert(T(1999101196), T(1999101229), is_error=True)
            return

        self.current_tab = tab_name
        self._update_sidebar_highlights()
        self.selected_row_frame = None

        self.right_panel.grid_remove()

        if tab_name == "Mod Activation":
            self.right_panel.grid()
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure(2, weight=0, minsize=500)

        else:
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure(2, weight=0, minsize=0)

        self._news_images = []
        for widget in self.main_content.winfo_children():
            widget.destroy()

        if tab_name == "News":
            self.render_news_tab()
        elif tab_name == "Mod Activation":
            self.render_activation_tab(select_id=select_id)
        elif tab_name == "Manual Install":
            self.render_installation_tab()
        elif tab_name == "Modloader Log":
            self.render_log_tab()
        elif tab_name == "Tweaking":
            self.render_tweaking_tab(select_id=select_id)
        elif tab_name == "Settings":
            self.render_settings_tab()
        elif tab_name == "Mod Browser":
            self.render_mod_browser_tab()
        elif tab_name == "Collections":
            self.render_collections_tab()

        self.update_idletasks()

    def launch_game(self):
        """Checks for a valid game executable and missing required mod dependencies, then launches Anno117.exe via subprocess. Schedules a UI refresh after launch."""
        if not self.game_exe_path or not os.path.exists(self.game_exe_path):
            self._imperial_alert(T(1999101189), T(1999101232), is_error=True)
            return

        # Check for missing required dependencies before launching
        missing = self._check_missing_dependencies()
        if missing:
            lines = "\n".join(
                T(1999101446, dep_id, mod_name)
                for mod_name, dep_id in missing
            )
            body = T(1999101419, lines)
            missing_dep_ids = {dep_id for _, dep_id in missing}
            choice = self._imperial_dependency_warning(T(1999101416), body, btn_accept=T(1999101414), missing_dep_ids=missing_dep_ids)
            if choice == "back":
                return
            if choice == "activated":
                if self.current_tab == "Mod Activation":
                    self.render_activation_tab()
                # Dependencies are now active - proceed with launch
                try:
                    subprocess.Popen([self.game_exe_path], creationflags=subprocess.CREATE_NO_WINDOW if IS_WINDOWS else 0)
                    self.after(2000, self.refresh_ui_after_launch)
                except Exception as e:
                    self._imperial_alert(T(1999101207), T(1999101394, e), is_error=True)
                return

        try:
            subprocess.Popen([self.game_exe_path], creationflags=subprocess.CREATE_NO_WINDOW if IS_WINDOWS else 0)
            self.after(2000, self.refresh_ui_after_launch)
        except Exception as e:
            self._imperial_alert(T(1999101207), T(1999101394, e), is_error=True)

    def refresh_ui_after_launch(self):
        """Re-scans all mod metadata and re-parses the active profile after the game has been launched so that any changes the game made are reflected in the UI."""
        self.get_all_mod_metadata()
        self.parse_active_profile()

    # ==========================================
    # --- NEWS TAB ---
    # ==========================================

    def render_news_tab(self, force_refresh=False):
        """Prepares the News tab and checks for cached data before fetching."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Header
        header_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        header_frame.pack(fill="x", padx=20, pady=20)
        tk.Label(header_frame, text=T(1999101010), font=FONT_TITLE, bg=BG_MAIN, fg=FG_MAIN).pack(side="left")

        # Refresh Button
        _ico_nref = load_icon("news_refresh", (14, 14))
        btn_refresh = tk.Button(header_frame, text=T(1999101160), font=FONT_XSMALL, bg=BG_SECTION, fg=FG_MAIN, relief="raised", cursor="hand2", padx=10, image=_ico_nref, compound="left" if _ico_nref else "none", command=lambda: self.render_news_tab(force_refresh=True))
        if _ico_nref: btn_refresh.image = _ico_nref
        btn_refresh.pack(side="right", padx=5)
        self._bind_hover(btn_refresh, BG_SECTION)

        _ico_nvis = load_icon("news_visit", (14, 14))
        btn_visit = tk.Button(header_frame, text=T(1999101161), font=FONT_XSMALL, bg=BG_SECTION, fg=FG_MAIN, relief="raised", cursor="hand2", padx=10, image=_ico_nvis, compound="left" if _ico_nvis else "none", command=lambda: webbrowser.open_new_tab("https://www.anno-union.com/en/blogs/"))
        if _ico_nvis: btn_visit.image = _ico_nvis
        btn_visit.pack(side="right")
        self._bind_hover(btn_visit, BG_SECTION)

        # Check session memory - instant if the user switches tabs and back
        if not force_refresh and hasattr(self, '_session_news') and self._session_news:
            self._build_news_ui(self._session_news)
            return

        # Always fetch fresh on first open or manual refresh
        self.news_loading_lbl = tk.Label(self.main_content, text=T(1999101013), font=FONT_BODY, bg=BG_MAIN, fg=FG_DIM)
        self.news_loading_lbl.pack(pady=50)

        threading.Thread(target=self._fetch_all_news, daemon=True).start()

    def _fetch_all_news(self):
        """Fetches Anno Union posts, new mod.io mods, and subscribed mod updates in parallel, then merges them chronologically and renders the feed."""
        results = []
        lock = threading.Lock()
        done = [0]
        include_reddit = self.show_reddit_news_var.get()
        include_collections = bool(self.modio_token and self._collection_follow_states)
        total_sources = 3
        if include_reddit: total_sources += 1
        if include_collections: total_sources += 1

        def on_source_done(items):
            with lock:
                results.extend(items)
                done[0] += 1
                if done[0] < total_sources:
                    return
            results.sort(key=lambda x: x.get('sort_ts', 0), reverse=True)
            if results:
                self._session_news = results
                self.after(0, lambda r=results: self._build_news_ui(r) if self.current_tab == "News" else None)
            else:
                self.after(0, lambda: self.news_loading_lbl.config(text=T(1999101014)) if self.current_tab == "News" and hasattr(self, 'news_loading_lbl') and self.news_loading_lbl.winfo_exists() else None)

        threading.Thread(target=self._fetch_anno_union_worker, args=(on_source_done,), daemon=True).start()
        threading.Thread(target=self._fetch_modio_new_mods_worker, args=(on_source_done,), daemon=True).start()
        threading.Thread(target=self._fetch_modio_updates_worker, args=(on_source_done,), daemon=True).start()
        # Separately check for version updates in the activation tab (independent of news)
        threading.Thread(target=self._check_modio_version_updates, daemon=True).start()
        if include_reddit:
            threading.Thread(target=self._fetch_reddit_worker, args=(on_source_done,), daemon=True).start()
        if include_collections:
            threading.Thread(target=self._fetch_collection_updates_worker, args=(on_source_done,), daemon=True).start()

    def _fetch_anno_union_worker(self, done_cb):
        """Fetches the latest Anno Union blog posts."""
        items = []
        try:
            api_url = "https://www.anno-union.com/wp-json/wp/v2/posts?_embed&per_page=10"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            for post in response.json():
                title = html.unescape(post.get('title', {}).get('rendered', 'Unknown Dispatch'))
                link  = post.get('link', 'https://www.anno-union.com/en/blogs/')
                date_raw = post.get('date', '')
                try:
                    dt = datetime.strptime(date_raw, '%Y-%m-%dT%H:%M:%S')
                    sort_ts  = dt.timestamp()
                    date_text = dt.strftime('%b %d, %Y')
                except Exception:
                    sort_ts   = 0.0
                    date_text = date_raw

                excerpt_html = post.get('excerpt', {}).get('rendered', '')
                excerpt = html.unescape(re.sub('<[^<]+?>', '', excerpt_html).strip())
                excerpt = (excerpt[:160] + "...") if len(excerpt) > 160 else excerpt

                img_url = None
                try:
                    media   = post.get('_embedded', {}).get('wp:featuredmedia', [{}])[0]
                    img_url = (media.get('media_details', {}).get('sizes', {})
                                    .get('medium', {}).get('source_url')
                               or media.get('source_url'))
                except Exception:
                    pass

                items.append({
                    "title": title,
                    "url": link,
                    "date": date_text,
                    "excerpt": excerpt,
                    "img_url": img_url,
                    "source": "anno_union",
                    "sort_ts": sort_ts,
                    "badge_text": "ANNO UNION",
                    "badge_color": "#5f022e",
                })
        except Exception as e:
            print(f"Anno Union fetch failed: {e}")
        finally:
            done_cb(items)

    def _fetch_modio_new_mods_worker(self, done_cb):
        """Fetches the most recently published mods on mod.io for this game. Mods already in the subscription list are skipped (they appear in updates)."""
        items = []
        if not self.modio_token:
            done_cb(items)
            return
        try:
            headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
            url = f"{MODIO_BASE_URL}/games/11358/mods?_sort=-date_live&_limit=10"
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 401:
                self.after(0, self._handle_modio_401)
                return
            res.raise_for_status()
            for mod in res.json().get('data', []):
                # Skip subscribed mods - they will appear in the updates feed instead
                if str(mod.get('id')) in self._subscription_states:
                    continue
                ts = float(mod.get('date_live') or 0)
                dt = datetime.fromtimestamp(ts) if ts else datetime.now()
                items.append({
                    "title": html.unescape(mod.get('name', 'Unknown Mod')),
                    "url": mod.get('profile_url', ''),
                    "date": dt.strftime('%b %d, %Y'),
                    "excerpt": html.unescape(mod.get('summary', 'No description.')),
                    "img_url": mod.get('logo', {}).get('thumb_320x180'),
                    "source": "new_mod",
                    "sort_ts": ts,
                    "badge_text": "NEW MOD",
                    "badge_color": "#2ecc71",
                    "mod_name": html.unescape(mod.get('name', '')),
                    "mod_id": str(mod.get('id'))
                })
        except Exception as e:
            print(f"mod.io new mods fetch failed: {e}")
        finally:
            done_cb(items)

    def _fetch_modio_updates_worker(self, done_cb):
        """Fetches recently updated mods on mod.io from the user's subscription list."""
        items = []
        if not self.modio_token or not self._subscription_states:
            done_cb(items)
            return
        try:
            headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
            # Query the user's active subscriptions directly, sorted by newest updates
            url = f"{MODIO_BASE_URL}/me/subscribed?game_id=11358&_sort=-date_updated&_limit=20"
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 401:
                self.after(0, self._handle_modio_401)
                return
            res.raise_for_status()

            for mod in res.json().get('data', []):
                ts = float(mod.get('date_updated') or 0)
                dt = datetime.fromtimestamp(ts) if ts else datetime.now()

                version = mod.get('modfile', {}).get('version', '')
                excerpt = f"Version {version} is now available." if version else "An update is available."

                changelog = (mod.get('modfile') or {}).get('changelog') or ''
                summary    = html.unescape(mod.get('summary', ''))

                if changelog:
                    clean = html.unescape(re.sub(r'<[^<]+?>', '', changelog)).strip()
                    clean = re.sub(r'\s{2,}', ' ', clean)
                    # Format line by line: "-" lines stay on their own line, non-bullet lines are joined with " • "
                    raw_lines = [l.strip() for l in clean.splitlines() if l.strip()]
                    out_parts = []
                    pending = ''
                    for cl in raw_lines:
                        if cl.startswith('-'):
                            if pending:
                                out_parts.append(pending)
                                pending = ''
                            out_parts.append(cl)
                        else:
                            pending = (pending + ' • ' + cl) if pending else cl
                    if pending:
                        out_parts.append(pending)
                    clean = '\n'.join(out_parts)
                    if clean:
                        display = clean[:500] + ('...' if len(clean) > 500 else '')
                        excerpt += f"\n\nChangelog:\n {display}"
                elif summary:
                    excerpt += f"\n\n{summary[:500]}"

                items.append({
                    "title": f"Update: {html.unescape(mod.get('name', 'Unknown Mod'))}",
                    "url": mod.get('profile_url', ''),
                    "date": dt.strftime('%b %d, %Y'),
                    "excerpt": excerpt,
                    "img_url": mod.get('logo', {}).get('thumb_320x180'),
                    "source": "mod_update",
                    "sort_ts": ts,
                    "badge_text": "★ UPDATE",
                    "badge_color": FG_GOLD,
                    "mod_name": html.unescape(mod.get('name', '')),
                    "mod_id": str(mod.get('id'))
                })
        except Exception as e:
            print(f"mod.io updates fetch failed: {e}")
        finally:
            done_cb(items)

    def _check_modio_version_updates(self):
        """Background worker that runs once at startup. Compares the locally installed version (from modinfo.json) against the latest version on mod.io for each subscribed mod. Populates self._modio_update_available with local mod IDs that have a newer version available, then re-renders the activation tab."""
        if not self.modio_token or not self._subscription_modio_map:
            return
        try:
            headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
            updated = set()
            # Build reverse map: modio_id → local_mod_id
            reverse_map = {v: k for k, v in self._subscription_modio_map.items()}
            # Fetch latest info for subscribed mods in one call
            url = f"{MODIO_BASE_URL}/me/subscribed?game_id=11358&_limit=100"
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code != 200:
                return
            for mod in res.json().get('data', []):
                modio_id = str(mod.get('id', ''))
                local_id = reverse_map.get(modio_id)
                if not local_id:
                    continue
                remote_ver = (mod.get('modfile') or {}).get('version', '')
                if not remote_ver:
                    continue
                # Find matching local mod
                local_mod = next((m for m in self.mods if m['id'] == local_id), None)
                if not local_mod:
                    continue
                local_ver = local_mod.get('version', '')
                # Simple string comparison — flag if different (remote is newer)
                def _norm(v): return v.strip().lstrip('vV')
                if local_ver and remote_ver and _norm(local_ver) != _norm(remote_ver):
                    updated.add(local_id)
            self._modio_update_available = updated
            if updated:
                self.after(0, lambda: self.render_activation_tab() if self.current_tab == "Mod Activation" else None)
        except Exception as e:
            print(f"[update check] failed: {e}")

    def _fetch_reddit_worker(self, done_cb):
        """Fetches the latest posts from r/anno via Reddit's public JSON API."""
        items = []
        try:
            url = "https://www.reddit.com/r/anno/new.json?limit=10"
            headers = {
                'User-Agent': 'Anno117ModManager/1.0 (Windows; mod manager app)',
                'Accept': 'application/json'
            }
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 401:
                self.after(0, self._handle_modio_401)
                return
            res.raise_for_status()

            posts = res.json().get('data', {}).get('children', [])
            for post in posts:
                d = post.get('data', {})
                if d.get('stickied'):
                    continue  # skip pinned mod posts

                title = html.unescape(d.get('title', 'Unknown Post'))
                url_post = f"https://www.reddit.com{d.get('permalink', '')}"
                ts = float(d.get('created_utc', 0))
                dt = datetime.fromtimestamp(ts) if ts else datetime.now()
                author = d.get('author', 'unknown')
                score = d.get('score', 0)
                excerpt = f"by u/{author}  ·  {score} upvotes"
                selftext = html.unescape(d.get('selftext', ''))
                if selftext:
                    selftext = selftext[:140].replace('\n', ' ').strip()
                    if len(d.get('selftext', '')) > 140:
                        selftext += '...'
                    excerpt += f"\n{selftext}"

                # Extract preview image - Reddit HTML-encodes the URL
                img_url = None
                try:
                    preview = d.get('preview', {}).get('images', [{}])[0]
                    src = preview.get('source', {}).get('url', '')
                    if src:
                        img_url = html.unescape(src)
                except Exception:
                    pass

                items.append({
                    "title": title,
                    "url": url_post,
                    "date": dt.strftime('%b %d, %Y'),
                    "excerpt": excerpt,
                    "img_url": img_url,
                    "source": "reddit",
                    "sort_ts": ts,
                    "badge_text": "r/anno",
                    "badge_color": "#ff4500"   # Reddit orange
                })
        except Exception as e:
            print(f"Reddit fetch failed: {e}")
        finally:
            done_cb(items)

    def _open_mod_in_browser(self, mod_id, mod_name):
        """Switches to the Mod Browser tab and locks the view to exactly this mod by ID."""
        self._browser_exact_id = mod_id
        self._browser_from_news = True
        self.switch_tab("Mod Browser")
        # Update the search bar label after the tab has built its widgets
        if hasattr(self, 'browser_search_var'):
            self.browser_search_var.set(mod_name)

    def _fetch_exact_mod_worker(self, parent_frame, loading_lbl, mod_id):
        """Fetches a single mod by ID to ensure it is the ONLY one displayed."""
        headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
        url = f"{MODIO_BASE_URL}/games/11358/mods?id={mod_id}"

        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 401:
                self.after(0, self._handle_modio_401)
                return
            res.raise_for_status()
            data = res.json()
            mods = data.get('data', [])
            total_count = data.get('result_total', 0)

            current_viewing = len(mods)
            stats_text = T(1999101449, current_viewing, total_count) if mods else T(1999101449, 0, total_count)
            self.after(0, lambda t=stats_text: self.browser_stats_lbl.config(text=t) if hasattr(self, 'browser_stats_lbl') and self.browser_stats_lbl.winfo_exists() else None)

            self.after(0, loading_lbl.destroy)

            if not mods:
                self.after(0, lambda: parent_frame.create_window((parent_frame.winfo_width()//2 or 400, 40), window=tk.Label(parent_frame, text=T(1999101015), bg=BG_MAIN, fg=FG_DIM), anchor="n"))
                return

            self.after(0, lambda: self._build_mod_tiles(parent_frame, mods, total_count))
        except Exception as e:
            self.after(0, lambda e=e: loading_lbl.config(text=T(1999101392, e)))

    def _bind_mousewheel_recursive(self, widget, canvas):
        """Recursively binds mousewheel to a widget and all its children."""
        widget.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        for child in widget.winfo_children():
            self._bind_mousewheel_recursive(child, canvas)

    def _build_news_ui(self, news_items):
        """Renders the News tab scroll area from a pre-fetched list of news items, building a card for each entry with image, badge, title, date and optional shortcut buttons. Guarded against stale tab switches."""
        try:
            if not self.main_content.winfo_exists():
                return
            if self.current_tab != "News":
                return
        except tk.TclError:
            return
        if hasattr(self, 'news_loading_lbl'):
            try:
                self.news_loading_lbl.destroy()
            except tk.TclError:
                pass

        container = tk.Frame(self.main_content, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=20)

        canvas = tk.Canvas(container, bg=BG_MAIN, highlightthickness=0)
        v_scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_MAIN)

        canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scroll.set)

        # Sync width
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))

        canvas.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")

        def update_scroll_region(event=None):
            try:
                if canvas.winfo_exists():
                    canvas.configure(scrollregion=canvas.bbox("all"))
            except tk.TclError:
                pass
        scroll_frame.bind("<Configure>", update_scroll_region)

        self._news_img_refs = []

        for item in news_items:
            card = tk.Frame(scroll_frame, bg=BG_SECTION, cursor="hand2", pady=10)
            card.pack(fill="x", pady=10, padx=10)

            if item.get('source') == 'reddit' and not item.get('img_url'):
                thumb_lbl = tk.Label(card, text="No image\nattached", font=FONT_XSMALL, bg="#0d1b2a", fg=FG_DIM, width=12, height=4, justify="center")
            else:
                thumb_lbl = tk.Label(card, text="⌛", font=FONT_TITLE, bg="#0d1b2a", fg=FG_DIM, width=12, height=4)

            thumb_lbl.pack(side="left", padx=15)

            if item.get('img_url'):
                threading.Thread(target=self._load_news_image_async, args=(item['img_url'], thumb_lbl), daemon=True).start()

            txt_frame = tk.Frame(card, bg=BG_SECTION)
            txt_frame.pack(side="left", fill="both", expand=True, padx=5)

            clickable = [card, thumb_lbl, txt_frame]

            l1 = tk.Label(txt_frame, text=item['date'].upper(), font=FONT_XSMALL, bg=BG_SECTION, fg=FG_DIM)
            l1.pack(anchor="w")
            clickable.append(l1)

            l2 = tk.Label(txt_frame, text=item['title'], font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, wraplength=800, justify="left")
            l2.pack(anchor="w")
            clickable.append(l2)

            l3 = tk.Label(txt_frame, text=item.get('excerpt', ''), font=FONT_SMALL, bg=BG_SECTION, fg=FG_DIM, wraplength=800, justify="left")
            l3.pack(anchor="w", pady=(5, 0))
            clickable.append(l3)

            # Hover, scroll and click are bound HERE - before badge/button are created - so those widgets are not captured in the hover closure and their backgrounds are never overwritten by card hover.
            self._bind_hover(card, BG_SECTION)
            self._bind_mousewheel_recursive(card, canvas)

            url = item.get('url', '')
            for w in clickable:
                w.bind("<Button-1>", lambda e, u=url: webbrowser.open_new_tab(u))

            # Badge - inserted visually between date and title via pack(after=l1)
            if item.get('badge_text'):
                _bc  = item['badge_color']
                _bfg = "#000000" if _bc in ("#2ecc71", FG_GOLD) else FG_MAIN
                badge_lbl = tk.Label(txt_frame, text=item['badge_text'], font=FONT_BOLD_SMALL, bg=_bc, fg=_bfg, padx=6, pady=1)
                badge_lbl.pack(anchor="w", pady=(2, 3), after=l1)
                badge_lbl.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
                badge_lbl.bind("<Button-1>", lambda e, u=url: webbrowser.open_new_tab(u))

            # Mod Browser shortcut button
            if item.get('mod_id'):
                _mn = item.get('mod_name', item.get('title', ''))
                _ico_oib = load_icon("open_in_browser", (14, 14))
                btn_open = tk.Button(txt_frame, text=T(1999101163), font=FONT_XSMALL, bg=BG_MAIN, fg=FG_GOLD, relief="raised", cursor="hand2", anchor="e", image=_ico_oib, compound="left" if _ico_oib else "none", command=lambda mid=item['mod_id'], mn=_mn: self._open_mod_in_browser(mid, mn))
                if _ico_oib: btn_open.image = _ico_oib
                btn_open.pack(anchor="e", pady=(6, 0))
                self._bind_hover(btn_open, BG_MAIN, BG_HOVER)
                btn_open.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
            # Collections shortcut button
            if item.get('collection_id'):
                _cid  = item['collection_id']
                _cn   = item.get('collection_name', '')
                _ico_oic = load_icon("open_in_collections", (14, 14))
                btn_col = tk.Button(txt_frame, text=T(1999101164), font=FONT_XSMALL,  bg=BG_MAIN, fg=FG_GOLD, relief="raised", cursor="hand2", anchor="e", image=_ico_oic, compound="left" if _ico_oic else "none", command=lambda cid=_cid: self._open_collection_tab(cid))
                if _ico_oic: btn_col.image = _ico_oic
                btn_col.pack(anchor="e", pady=(4, 0))
                self._bind_hover(btn_col, BG_MAIN, BG_HOVER)
                btn_col.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Final layout pass
        self.after(100, update_scroll_region)

        # Bind scroll to background areas too
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        scroll_frame.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def _load_news_image_async(self, img_url, label_widget):
        """Downloads an image and updates the UI safely."""
        try:
            resp = requests.get(img_url, timeout=5)
            img_data = Image.open(BytesIO(resp.content))

            # Resize image to fit the thumbnail box nicely
            img_data.thumbnail((150, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img_data)

            # Update Tkinter from main thread
            self.after(0, self._apply_news_image, label_widget, photo)
        except Exception as e:
            print(f"Could not load image {img_url}: {e}")

    def _apply_news_image(self, label_widget, photo):
        """Applies the downloaded image to the label and stores reference."""
        try:
            if label_widget.winfo_exists():
                label_widget.config(image=photo, text="", width=150, height=100)
                # Store reference in the CLASS instance list
                self._news_images.append(photo)
        except Exception as e:
            print(f"Error applying image: {e}")

    # ==========================================
    # --- ACTIVATION TAB ---
    # ==========================================

    def update_stats_label(self):
        """Calculates mod counts and sizes for both Active and Total Installed mods."""
        # 1. Setup Totals
        installed_count = 0
        active_count = 0
        total_size_bytes = 0
        active_size_bytes = 0

        # 2. Get fresh statuses to check what is active
        statuses = self.parse_active_profile()

        # 3. Helper for directory size
        def get_dir_size(path):
            total = 0
            try:
                for entry in os.scandir(path):
                    if entry.is_file(): total += entry.stat().st_size
                    elif entry.is_dir(): total += get_dir_size(entry.path)
            except: pass
            return total

        # 4. Iterate through discovered mods
        for mod in self.mods:
            # We only count top-level mods for the primary stats
            if mod['parent_path'] is None:
                installed_count += 1

                # Calculate size once per top-level folder
                m_size = get_dir_size(mod['path'])
                total_size_bytes += m_size

                # Determine if Active
                m_id = mod['id']
                is_uninstalled = statuses.get(m_id, {}).get("uninstalled", False)
                is_active = False if is_uninstalled else statuses.get(m_id, {}).get("active", self.enable_new_mods)

                if is_active:
                    active_count += 1
                    active_size_bytes += m_size

        # 5. Conversion Logic (MB)
        def format_bytes(b):
            mb = b / (1024 * 1024)
            if mb < 0.1:
                return f"{b / 1024:.1f} KB"
            return f"{mb:.1f} MB"

        active_size_str = format_bytes(active_size_bytes)
        total_size_str = format_bytes(total_size_bytes)

        # 6. Update the String Variable
        stats_text = T(1999101445, active_count, installed_count, active_size_str, total_size_str)

        if hasattr(self, 'stats_label_var'):
            self.stats_label_var.set(stats_text)

    def _compute_load_order(self, top_mods):
        """Computes the Anno mod loader load order for active top-level mods.

        Phase split (determined by the mod's own LoadAfter only):
          Normal — LoadAfter does NOT contain '*'
          Late   — LoadAfter DOES contain '*'

        Normal phase ordering (category+name alphabetical, observed in modloader.log):
          Group 1 — mods whose LoadAfter references ONLY late/cross-phase mods
                    (their dep is ignored but they still load before everything else)
          Group 2 — mods with real same-phase LoadAfter deps (topological sort)
          Group 3 — mods with no LoadAfter at all (category+name alphabetical)
          Cross-phase LoadAfter entries are silently ignored for ordering.

        Late phase ordering (ModID alphabetical, topological for late→late deps):
          All late mods sorted by ModID; late→late LoadAfter respected,
          cross-phase and '*' entries ignored.
        """
        statuses = self.mod_statuses

        active = [
            m for m in top_mods
            if not m.get('manually_disabled')
            and bool(statuses.get(m['id'], {}).get('active',
                     self.enable_new_mods_var.get() in ('on', 'keep')))
            and not statuses.get(m['id'], {}).get('uninstalled', False)
        ]

        installed_ids = {m['id'] for m in active}
        normal = [m for m in active if '*' not in m.get('deps', {}).get('LoadAfter', [])]
        late   = [m for m in active if '*' in  m.get('deps', {}).get('LoadAfter', [])]

        def sort_normal(phase_mods):
            if not phase_mods:
                return []
            phase_ids = {m['id'] for m in phase_mods}
            by_id     = {m['id']: m for m in phase_mods}
            cat_name  = lambda m: (m.get('category', '') + m['name'])

            # Classify each mod
            cross_phase_only = []   # Group 1: LoadAfter exists but all refs are late/missing
            has_real_deps    = []   # Group 2: at least one same-phase LoadAfter dep
            no_deps          = []   # Group 3: empty LoadAfter

            for m in phase_mods:
                la_all = [la for la in m.get('deps', {}).get('LoadAfter', []) if la != '*']
                la_real = [la for la in la_all if la in phase_ids and la in installed_ids]
                if not la_all:
                    no_deps.append(m)
                elif la_real:
                    has_real_deps.append(m)
                else:
                    cross_phase_only.append(m)

            # Group 1: cross-phase-only — load first, category+name order
            result = sorted(cross_phase_only, key=cat_name)

            # Group 2: real same-phase deps — Kahn's topological sort, category+name tiebreak
            in_degree  = {m['id']: 0 for m in has_real_deps}
            successors = {m['id']: [] for m in has_real_deps}
            real_dep_ids = {m['id'] for m in has_real_deps}
            for m in has_real_deps:
                for la in m.get('deps', {}).get('LoadAfter', []):
                    if la != '*' and la in real_dep_ids and la in installed_ids:
                        successors[la].append(m['id'])
                        in_degree[m['id']] += 1
            queue = sorted(
                [mid for mid, deg in in_degree.items() if deg == 0],
                key=lambda mid: cat_name(by_id[mid])
            )
            visited = set()
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                result.append(by_id[current])
                newly_ready = sorted(
                    [s for s in successors[current] if in_degree[s] - 1 == 0],
                    key=lambda mid: cat_name(by_id[mid])
                )
                for s in successors[current]:
                    in_degree[s] -= 1
                queue = newly_ready + queue
            # Circular dep fallback
            result.extend(sorted(
                [m for m in has_real_deps if m['id'] not in visited],
                key=cat_name))

            # Group 3: no LoadAfter — category+name order
            result.extend(sorted(no_deps, key=cat_name))
            return result

        def sort_late(phase_mods):
            if not phase_mods:
                return []
            phase_ids  = {m['id'] for m in phase_mods}
            by_id      = {m['id']: m for m in phase_mods}
            in_degree  = {m['id']: 0 for m in phase_mods}
            successors = {m['id']: [] for m in phase_mods}

            for m in phase_mods:
                for la in m.get('deps', {}).get('LoadAfter', []):
                    if la != '*' and la in phase_ids and la in installed_ids:
                        successors[la].append(m['id'])
                        in_degree[m['id']] += 1

            queue = sorted(
                [mid for mid, deg in in_degree.items() if deg == 0],
                key=lambda mid: mid   # ModID alphabetical
            )
            result = []
            visited = set()
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                result.append(by_id[current])
                newly_ready = sorted(
                    [s for s in successors[current]],
                    key=lambda mid: mid
                )
                for s in successors[current]:
                    in_degree[s] -= 1
                queue = newly_ready + queue

            result.extend(sorted(
                [m for m in phase_mods if m['id'] not in visited],
                key=lambda m: m['id']
            ))
            return result

        return sort_normal(normal) + sort_late(late)

    def render_activation_tab(self, select_id=None, search_query=None):
        """Renders the Mod Activation tab: preset management row, stats bar, search/filter row, sortable column header and the full scrollable mod list with checkboxes, icons and sub-mod rows."""
        if search_query is not None:
            self.current_search_query = search_query

        for widget in self.main_content.winfo_children():
            widget.destroy()

        self.update_right_panel(None)

        # 1. Gather Fresh Data
        self.parse_active_profile()
        self.get_all_mod_metadata()
        self.active_options_cache = self._load_active_options()

        # 2. FOCUS BAR
        focus_frame = tk.Frame(self.main_content, bg=BG_SECTION, padx=15, pady=10)
        focus_frame.pack(fill="x", padx=(10, 0), pady=(5, 10))

        # Row 1: Preset Management
        preset_row = tk.Frame(focus_frame, bg=BG_SECTION)
        preset_row.pack(fill="x", pady=(0, 10))

        tk.Label(preset_row, text=T(1999101019), font=FONT_BOLD_SMALL, bg=BG_SECTION, fg=FG_DIM).pack(side="left")

        self.refresh_presets_list()
        self.preset_combo = ttk.Combobox(preset_row, values=self.available_presets, state="readonly", font=FONT_SMALL, width=25)
        self.preset_combo.set(self.current_profile_name)
        self.preset_combo.pack(side="left", padx=10)
        self.preset_combo.bind("<<ComboboxSelected>>", self.on_preset_dropdown_change)

        _ico_save = load_icon("save_preset", (22, 22))
        btn_newpreset = tk.Button(preset_row, text=T(1999101183), font=FONT_XSMALL, bg="#2e7d32", fg=FG_MAIN, cursor="hand2", command=self.save_preset, relief="raised", padx=10, image=_ico_save, compound="left" if _ico_save else "none")
        if _ico_save: btn_newpreset.image = _ico_save
        btn_newpreset.pack(side="left", padx=2)
        self._bind_hover(btn_newpreset, "#2e7d32", "#36943a")

        _ico_del = load_icon("delete_preset", (22, 22))
        btn_deletepreset = tk.Button(preset_row, text=T(1999101184), font=FONT_XSMALL, bg="#8b0000", fg=FG_MAIN, cursor="hand2", command=self.delete_preset, relief="raised", padx=10, image=_ico_del, compound="left" if _ico_del else "none")
        if _ico_del: btn_deletepreset.image = _ico_del
        btn_deletepreset.pack(side="left", padx=2)
        self._bind_hover(btn_deletepreset, "#8b0000", "#AF0202")

        # Row 2: Stats
        stats_row = tk.Frame(focus_frame, bg=BG_SECTION)
        stats_row.pack(fill="x", pady=(0, 10))

        self.stats_label_var = tk.StringVar()
        self.update_stats_label()
        tk.Label(stats_row, textvariable=self.stats_label_var, font=FONT_BOLD_SMALL, bg=BG_SECTION, fg=FG_MAIN).pack(side="left")

        # Row 3: Search
        search_row = tk.Frame(focus_frame, bg=BG_SECTION)
        search_row.pack(fill="x")

        tk.Label(search_row, text=T(1999101022), font=FONT_SMALL, bg=BG_SECTION, fg=FG_DIM).pack(side="left")

        # Search bar with embedded ✕ clear button - same pattern as Mod Browser
        search_bg = tk.Frame(search_row, bg=BG_MAIN, padx=5, pady=2)
        search_bg.pack(side="left", padx=5)

        search_var = tk.StringVar(value=self.current_search_query)
        search_entry = tk.Entry(search_bg, textvariable=search_var, font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN, insertbackground=FG_MAIN, width=18, relief="flat")
        search_entry.pack(side="left")

        btn_x = tk.Button(search_bg, text="✕", font=FONT_XSMALL, bg=BG_MAIN, fg=FG_DIM, relief="flat", cursor="hand2", command=lambda: self.render_activation_tab(search_query=""))
        btn_x.pack(side="left")
        self._bind_hover(btn_x, BG_MAIN, BG_HOVER)
        self._attach_tooltip(btn_x, T(1999101250))

        def _on_search_type(*args):
            val = search_var.get()
            if len(val) >= 3 or val == "":
                self.render_activation_tab(search_query=val)
        search_var.trace_add("write", _on_search_type)

        _ico_all = load_icon("activate_all", (22, 22))
        btn_activate_all = tk.Button(search_row, text=T(1999101185), font=FONT_XSMALL, bg="#2e7d32", fg=FG_MAIN, cursor="hand2", relief="raised", padx=10, image=_ico_all, compound="left" if _ico_all else "none", command=lambda: [self.reset_to_default_profile(), self.render_activation_tab()])
        if _ico_all: btn_activate_all.image = _ico_all
        btn_activate_all.pack(side="left", padx=2)
        self._bind_hover(btn_activate_all, "#2e7d32", "#36943a")
        self._attach_tooltip(btn_activate_all, T(1999101251))

        search_entry.bind("<Return>", lambda e: self.render_activation_tab(search_query=search_var.get()))
        search_entry.bind("<Escape>", lambda e: self.render_activation_tab(search_query=""))


        _ico_folder  = load_icon("open_folder", (24, 24))
        _ico_refresh = load_icon("refresh", (24, 24))
        _ico_lordord = load_icon("load_order", (22, 22))
        # Open mod folder button
        btn_open_folder = tk.Button(search_row, text="" if _ico_folder else "📁", font=FONT_XSMALL, bg=BG_MAIN, fg=FG_MAIN, cursor="hand2", relief="raised", padx=8, image=_ico_folder, compound="center" if _ico_folder else "none", command=lambda: _open_path(self.mod_path) if self.mod_path and os.path.exists(self.mod_path) else self._imperial_alert(T(1999101197), T(1999101230), is_error=True))
        if _ico_folder: btn_open_folder.image = _ico_folder
        btn_open_folder.pack(side="right", padx=(2, 0))
        self._bind_hover(btn_open_folder, BG_MAIN)
        self._attach_tooltip(btn_open_folder, T(1999101252))

        # Refresh mod list button
        btn_refresh = tk.Button(search_row, text="" if _ico_refresh else "↻", font=FONT_XSMALL, bg=BG_MAIN, fg=FG_MAIN, cursor="hand2", relief="raised", padx=8, image=_ico_refresh, compound="center" if _ico_refresh else "none", command=lambda: self.render_activation_tab( search_query=self.current_search_query))
        if _ico_refresh: btn_refresh.image = _ico_refresh
        btn_refresh.pack(side="right", padx=2)
        self._bind_hover(btn_refresh, BG_MAIN)
        self._attach_tooltip(btn_refresh, T(1999101253))

        # Load Order toggle button
        _lo_bg  = FG_GOLD if self.show_load_order else BG_MAIN
        _lo_fg  = "#000000" if self.show_load_order else FG_MAIN
        btn_loadorder = tk.Button(search_row, text=T(1999101186), font=FONT_XSMALL, cursor="hand2", relief="raised", padx=8, bg=_lo_bg, fg=_lo_fg, image=_ico_lordord, compound="left" if _ico_lordord else "none", command=self._toggle_load_order)
        if _ico_lordord: btn_loadorder.image = _ico_lordord
        btn_loadorder.pack(side="right", padx=2)
        if not self.show_load_order:
            self._bind_hover(btn_loadorder, BG_MAIN)
            self._attach_tooltip(btn_loadorder, T(1999101254))

        if self.current_search_query:
            search_entry.focus_set()
            search_entry.icursor(tk.END)

        # --- End Focus Bar / Start Mod List ---
        if not self.mods:
            tk.Label(self.main_content, text=T(1999101088), font=FONT_BODY, bg=BG_MAIN, fg=FG_DIM).pack(pady=20)
            return

        # --- SORTING LOGIC ---
        statuses = self.mod_statuses
        query = self.current_search_query.lower().strip()

        def get_sorting_key(m):
            m_id = m['id']
            # A. Activation Group (0 for the top group, 1 for the bottom)
            _status = statuses.get(m_id)
            if _status is not None:
                is_active = bool(_status.get("active", False))
            else:
                is_active = self.enable_new_mods_var.get() in ("on", "keep")
            active_group = 0 if is_active == self.sort_active_first else 1

            # B. Category Weight (Only applies if sort_cat_dir is not 0)
            cat_val = str(m.get('category', 'zzz')).lower()
            if self.sort_cat_dir == 0:
                cat_sort = "" # Ignore
            elif self.sort_cat_dir == 1:
                cat_sort = cat_val
            else:
                # Z-A: invert characters
                cat_sort = "".join(chr(255 - ord(c)) for c in cat_val)

            # C. Name Weight
            name_val = str(m.get('name', '')).lower()
            if self.sort_name_dir == -1:
                name_sort = "".join(chr(255 - ord(c)) for c in name_val)
            else:
                name_sort = name_val

            return (active_group, cat_sort, name_sort)

        # Filter top-level mods and apply search
        all_top_mods = [m for m in self.mods if m['parent_path'] is None and not m.get('manually_disabled')]
        filtered_mods = []
        for m in all_top_mods:
            if not query or (query in str(m.get('name','')).lower() or query in str(m.get('category','')).lower()):
                filtered_mods.append(m)

        filtered_mods.sort(key=get_sorting_key)

        # --- 2. HEADER ---
        header_container = tk.Frame(self.main_content, bg=BG_MAIN)
        header_container.pack(fill="x", padx=0, pady=(10, 0))

        header_frame = tk.Frame(header_container, bg=BG_SECTION, pady=8)
        header_frame.pack(fill="x", padx=(10, 0))

        if self.show_load_order:
            # Only the position badge column - sort arrows are hidden entirely
            tk.Label(header_frame, text="#", font=FONT_BOLD_SMALL, bg=BG_SECTION, fg=FG_GOLD, width=3, anchor="e").pack(side="left", padx=(4, 0))
            tk.Label(header_frame, text=T(1999101026), font=FONT_BOLD_SMALL, bg=BG_SECTION, fg=FG_DIM, anchor="w").pack(side="left", padx=(8, 0), fill="x", expand=True)
        else:
            # Status icon
            _ico_st = load_icon("activation_sort_active" if self.sort_active_first else "activation_sort_inactive", (16, 16))
            lbl_stat = tk.Label(header_frame, text="" if _ico_st else ("✔" if self.sort_active_first else "X"), image=_ico_st or "", font=FONT_BOLD_SMALL, bg=BG_SECTION, fg=FG_MAIN, cursor="hand2", width=8 if _ico_st else 1)
            if _ico_st: lbl_stat.image = _ico_st
            lbl_stat.pack(side="left", padx=(8, 0))
            lbl_stat.bind("<Button-1>", lambda e: self.toggle_sort("status"))

            _ico_cat = load_icon(
                "arrow_down" if self.sort_cat_dir == 1 else
                ("arrow_up"  if self.sort_cat_dir == -1 else None),
                (18, 18)) if self.sort_cat_dir != 0 else None
            if _ico_cat is None:
                _ico_cat = ImageTk.PhotoImage(Image.new("RGBA", (18, 18), (0, 0, 0, 0)))
            lbl_cat = tk.Label(header_frame, text=T(1999101027), image=_ico_cat, compound="right", font=FONT_BOLD_SMALL, bg=BG_SECTION, fg=FG_MAIN, cursor="hand2", anchor="w")
            lbl_cat.image = _ico_cat
            lbl_cat.pack(side="left", padx=(11, 1))
            lbl_cat.bind("<Button-1>", lambda e: self.toggle_sort("category"))

            # Name column with direction arrow icon
            _ico_nm = load_icon("arrow_down" if self.sort_name_dir == 1 else "arrow_up",(18, 18))
            lbl_name = tk.Label(header_frame, text=T(1999101026), image=_ico_nm or "", compound="right" if _ico_nm else "none", font=FONT_BOLD_SMALL, bg=BG_SECTION, fg=FG_MAIN, cursor="hand2", anchor="w")
            if _ico_nm: lbl_name.image = _ico_nm
            lbl_name.pack(side="left", fill="x", expand=True)
            lbl_name.bind("<Button-1>", lambda e: self.toggle_sort("name"))

        # 3. Setup Canvas and Scrollbar
        container = tk.Frame(self.main_content, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=0, pady=(0, 10))

        self.canvas = tk.Canvas(container, bg=BG_MAIN, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_MAIN)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        def _on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def _on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)

        self.scrollable_frame.bind("<Configure>", _on_frame_configure)
        self.canvas.bind("<Configure>", _on_canvas_configure)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 4. Draw Mods
        if self.show_load_order:
            ordered = self._compute_load_order(all_top_mods)
            if query:
                ordered = [m for m in ordered
                           if query in m.get('name', '').lower()
                           or query in m.get('category', '').lower()]

            load_order_positions = {m['id']: i + 1 for i, m in enumerate(ordered)}
            ordered_ids = {m['id'] for m in ordered}

            # Active mods in load order
            if ordered:
                self._draw_separator(T(1999101437))
            for mod in ordered:
                self._draw_mod_row(self.scrollable_frame, mod, self.mods, statuses, True, indent=0, select_id=select_id, load_order_pos=load_order_positions[mod['id']])

            # Inactive mods at the bottom, alphabetical
            inactive = sorted(
                [m for m in all_top_mods if m['id'] not in ordered_ids],
                key=lambda m: m['name'].lower()
            )
            if query:
                inactive = [m for m in inactive
                            if query in m.get('name', '').lower()
                            or query in m.get('category', '').lower()]
            if inactive:
                self._draw_separator(T(1999101438))
            for mod in inactive:
                self._draw_mod_row(self.scrollable_frame, mod, self.mods, statuses, False, indent=0, select_id=select_id)

        else:
            active_sep_needed = True
            inactive_sep_needed = True

            for mod in filtered_mods:
                m_id = mod['id']
                _status = statuses.get(m_id)
                if _status is not None:
                    is_active = bool(_status.get("active", False))
                else:
                    is_active = self.enable_new_mods_var.get() in ("on", "keep")

                if is_active == self.sort_active_first and active_sep_needed:
                    label = T(1999101439) if self.sort_active_first else T(1999101438)
                    self._draw_separator(label)
                    active_sep_needed = False

                if is_active != self.sort_active_first and inactive_sep_needed:
                    label = T(1999101438) if self.sort_active_first else T(1999101439)
                    self._draw_separator(label)
                    inactive_sep_needed = False

                self._draw_mod_row(self.scrollable_frame, mod, self.mods, statuses, is_active, indent=0, select_id=select_id)

        # --- Mousewheel logic ---
        def _on_mousewheel(event):
            try:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except: pass

        def bind_mousewheel_recursive(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel_recursive(child)

        container.bind('<Enter>', lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        container.bind('<Leave>', lambda e: self.canvas.unbind_all("<MouseWheel>"))
        bind_mousewheel_recursive(self.scrollable_frame)

    def _draw_separator(self, text):
            """Draws a horizontal divider line with a centred text label into the activation tab's scrollable frame, used to visually separate ACTIVE MODS from DEACTIVATED MODS sections."""
            sep_container = tk.Frame(self.scrollable_frame, bg=BG_MAIN, pady=15)
            sep_container.pack(fill="x")
            line_color = FG_SEPARATOR
            tk.Frame(sep_container, bg=line_color, height=2).pack(fill="x", padx=10, side="left", expand=True)
            tk.Label(sep_container, text=f" {text} ", font=FONT_BOLD_SMALL, bg=BG_MAIN, fg=FG_DIM).pack(side="left", padx=10)
            tk.Frame(sep_container, bg=line_color, height=2).pack(fill="x", padx=10, side="left", expand=True)

    def _draw_mod_row(self, parent_widget, current_mod, all_mods, statuses, is_active, indent=0, select_id=None, load_order_pos=None):
        """Renders a single mod entry row inside the activation tab list: checkbox or indent marker, category badge, status/warning icons (conflict, missing dep, deprecated, tweaks) and the mod name coloured by state. Binds hover, click and keyboard navigation."""
        row_bg = BG_SECTION
        hover_bg = "#253b59"
        select_bg = "#253b59"

        row = tk.Frame(parent_widget, bg=row_bg, takefocus=1, highlightthickness=1, highlightbackground=row_bg, highlightcolor=FG_MAIN)
        row.pack(fill="x", padx=(10 + (indent * 25), 10), pady=2)

        def scroll_to_view(widget):
            self.canvas.update_idletasks()
            y_top = widget.winfo_y()
            y_bottom = y_top + widget.winfo_height()
            c_height = self.canvas.winfo_height()
            v_top, v_bottom = self.canvas.yview()
            content_height = parent_widget.winfo_height()
            current_view_top = v_top * content_height
            current_view_bottom = v_bottom * content_height

            if y_top < current_view_top:
                self.canvas.yview_moveto(y_top / content_height)
            elif y_bottom > current_view_bottom:
                self.canvas.yview_moveto((y_bottom - c_height) / content_height)

        def update_row_color(color):
            row.config(bg=color)
            for child in row.winfo_children():
                if not isinstance(child, tk.Checkbutton):
                    child.config(bg=color)
                else:
                    child.config(background=color, activebackground=color)

        def on_enter(e):
            if getattr(self, 'selected_row_frame', None) != row:
                update_row_color(hover_bg)

        def on_leave(e):
            if getattr(self, 'selected_row_frame', None) != row:
                update_row_color(row_bg)

        def on_click(e=None):
            if hasattr(self, 'selected_row_frame') and self.selected_row_frame:
                try:
                    self.selected_row_frame.config(bg=row_bg, highlightbackground=row_bg)
                    for child in self.selected_row_frame.winfo_children():
                        if not isinstance(child, tk.Checkbutton):
                            child.config(bg=row_bg)
                        else:
                            child.config(background=row_bg, activebackground=row_bg)
                except: pass

            self.selected_row_frame = row
            update_row_color(select_bg)
            row.config(highlightbackground=FG_MAIN)
            row.focus_set()
            self.update_right_panel(current_mod)
            scroll_to_view(row)

        def on_arrow_key(event):
            if event.keysym == "Down":
                next_w = row.tk_focusNext()
            else:
                next_w = row.tk_focusPrev()

            if next_w and next_w.master == parent_widget:
                next_w.event_generate("<Button-1>")
                scroll_to_view(next_w)
            return "break"

        row.bind("<Button-1>", on_click)
        row.bind("<Key-Up>", on_arrow_key)
        row.bind("<Key-Down>", on_arrow_key)
        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)

        if indent == 0:
            # Load order position badge
            if load_order_pos is not None:
                pos_lbl = tk.Label(row, text=f"{load_order_pos}", font=FONT_XSMALL, bg=row_bg, fg=FG_GOLD, width=3, anchor="e")
                pos_lbl.pack(side="left", padx=(4, 0))
                pos_lbl.bind("<Enter>", on_enter)
                pos_lbl.bind("<Leave>", on_leave)
                pos_lbl.bind("<Button-1>", on_click)

            var = tk.BooleanVar(value=is_active)

            def on_check_toggle():
                # Only run the incompatibility check when the user is *activating* a mod
                if var.get():
                    if not self._check_and_confirm_incompatible(current_mod['id']):
                        # User chose "Keep Disabled" – revert the checkbox silently
                        var.set(False)
                        return

                self.toggle_mod_status(current_mod['id'], var.get())
                self.parse_active_profile()
                # Dynamically update the top bar without refreshing the whole list
                self.update_stats_label()
                self.render_activation_tab()
                if getattr(self, 'selected_row_frame', None) == row:
                    self.update_right_panel(current_mod)

            chk = tk.Checkbutton(row, variable=var, bg=row_bg, activebackground=hover_bg, selectcolor=FG_MAIN, cursor="hand2", takefocus=0, command=on_check_toggle)
            chk.pack(side="left", padx=(0, 0))
            chk.bind("<Enter>", on_enter)
            chk.bind("<Leave>", on_leave)
        else:
            indent_lbl = tk.Label(row, text="└─", font=FONT_SMALL, bg=row_bg, fg=FG_DIM)
            indent_lbl.pack(side="left", padx=(12, 0))
            indent_lbl.bind("<Enter>", on_enter)
            indent_lbl.bind("<Leave>", on_leave)

        if current_mod.get('category'):
            cat_text = current_mod.get('category', '')
            cat_lbl = tk.Label(row, text=cat_text, font=FONT_BOLD_SMALL, bg=row_bg, fg=FG_MAIN, width=8, anchor="w")
            cat_lbl.pack(side="left", padx=(0, 0))
            cat_lbl.bind("<Enter>", on_enter)
            cat_lbl.bind("<Leave>", on_leave)
            cat_lbl.bind("<Button-1>", on_click)

        has_tweaks   = current_mod['id'] in getattr(self, 'active_options_cache', {})
        has_conflict = bool(self._get_active_incompatible_conflicts(current_mod['id']))
        has_missing_dep = (is_active and not has_conflict and bool(self._get_missing_required_deps(current_mod['id'])))
        has_deprecated  = (is_active and not has_conflict and not has_missing_dep and self._is_deprecated_by_active(current_mod['id']))
        any_warning  = has_conflict or has_missing_dep or has_deprecated
        is_modio_mod = (indent == 0 and not current_mod.get('parent_path') and current_mod['id'] in self._subscription_modio_map)
        has_update   = current_mod['id'] in getattr(self, '_modio_update_available', set())

        # All icon groups share the same 20 px start indent;
        # subsequent icons in the same row follow at 0 px.
        _ISTART = 20
        _iused  = [False]
        def _pad():
            p = 0 if _iused[0] else _ISTART
            _iused[0] = True
            return p

        # Gear (tweaks) — click selects row AND navigates to Tweaking tab
        if has_tweaks:
            _ico_gear = load_icon("customized", (16, 16))
            if _ico_gear:
                gear_lbl = tk.Label(row, image=_ico_gear, bg=row_bg, cursor="hand2")
                gear_lbl.image = _ico_gear
            else:
                gear_lbl = tk.Label(row, text="⚙", font=FONT_XSMALL, bg=row_bg, fg=FG_DIM, cursor="hand2")
            gear_lbl.pack(side="left", padx=(_pad(), 2))
            gear_lbl.bind("<Enter>", on_enter)
            gear_lbl.bind("<Leave>", on_leave)
            gear_lbl.bind("<Button-1>",
                lambda e, m=current_mod: [on_click(),
                    self.switch_tab("Tweaking", select_id=m['id'])])

        # Warning icons — informational only; no hand2 cursor, row-selection only
        if any_warning:
            _wk = ("x" if has_conflict else "missing_dependency" if has_missing_dep else "deprecated")
            _wfb = ("✘" if has_conflict else "!" if has_missing_dep else "↓")
            _wfg = "#e74c3c" if has_conflict else "#e67e22"
            _ico_w = load_icon(_wk, (16, 16))
            if _ico_w:
                warn_lbl = tk.Label(row, image=_ico_w, bg=row_bg)
                warn_lbl.image = _ico_w
            else:
                warn_lbl = tk.Label(row, text=_wfb, font=FONT_XSMALL,
                                    bg=row_bg, fg=_wfg)
            warn_lbl.pack(side="left", padx=(_pad(), 2))
            warn_lbl.bind("<Enter>", on_enter)
            warn_lbl.bind("<Leave>", on_leave)
            warn_lbl.bind("<Button-1>", on_click)

        # mod.io badge + update "!" — click opens Mod Browser for this specific mod
        if is_modio_mod:
            _mid = self._subscription_modio_map.get(current_mod['id'])
            def _go_browser(e, mid=_mid, mname=current_mod['name']):
                on_click()
                if mid:
                    setattr(self, '_browser_exact_id', int(mid))
                    setattr(self, '_browser_from_news', True)
                self.switch_tab("Mod Browser")
                if hasattr(self, 'browser_search_var'):
                    self.browser_search_var.set(mname)
            if has_update:
                def _quick_update(e, mid=_mid, mn=current_mod['name'], lid=current_mod['id']):
                    on_click()
                    def _fetch_and_install():
                        try:
                            headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
                            res = requests.get(f"{MODIO_BASE_URL}/games/11358/mods/{mid}", headers=headers, timeout=10)
                            res.raise_for_status()
                            dl_url = (res.json().get('modfile') or {}).get('download', {}).get('binary_url')
                            if dl_url:
                                self.after(0, lambda u=dl_url, n=mn, m=mid: self._download_and_install(u, n, mod_id=m))
                            else:
                                self.after(0, lambda: self._imperial_alert(T(1999101189), T(1999101472), is_error=True))
                        except Exception as ex:
                            self.after(0, lambda: self._imperial_alert(T(1999101189), str(ex), is_error=True))
                    if self._imperial_question(T(1999101213), T(1999101359, mn)):
                        # Remove from update set immediately so the badge disappears
                        self._modio_update_available.discard(lid)
                        threading.Thread(target=_fetch_and_install, daemon=True).start()
                upd_lbl = tk.Label(row, text="!", font=FONT_BOLD_SMALL, bg=row_bg, fg=FG_GOLD, cursor="hand2")
                upd_lbl.pack(side="left", padx=(_pad(), 1))
                upd_lbl.bind("<Enter>", on_enter)
                upd_lbl.bind("<Leave>", on_leave)
                upd_lbl.bind("<Button-1>", _quick_update)
                self._attach_tooltip(upd_lbl, T(1999101479))
            _ico_mb = load_icon("modio_mod", (14, 14))
            if _ico_mb:
                mb_lbl = tk.Label(row, image=_ico_mb, bg=row_bg, cursor="hand2")
                mb_lbl.image = _ico_mb
            else:
                mb_lbl = tk.Label(row, text="●", font=FONT_XSMALL, bg=row_bg, fg="#07C1D8", cursor="hand2")
            mb_lbl.pack(side="left", padx=(_pad(), 2))
            mb_lbl.bind("<Enter>", on_enter)
            mb_lbl.bind("<Leave>", on_leave)
            mb_lbl.bind("<Button-1>", _go_browser)

        name_fg = ("#e74c3c" if has_conflict else "#e67e22" if (has_missing_dep or has_deprecated) else FG_MAIN)

        lbl = tk.Label(row, text=current_mod['name'], font=FONT_SMALL, bg=row_bg, fg=name_fg, anchor="w")
        lbl.pack(side="left", fill="x", expand=True, padx=(0 if _iused[0] else _ISTART, 0))
        lbl.bind("<Enter>", on_enter)
        lbl.bind("<Leave>", on_leave)
        lbl.bind("<Button-1>", on_click)

        if select_id and current_mod.get('id') == select_id:
            self.after(100, on_click)

        submods = sorted(
            [m for m in all_mods if m['parent_path'] == current_mod['path']],
            key=lambda x: x['name'].lower()
        )

        for sm in submods:
            self._draw_mod_row(parent_widget, sm, all_mods, statuses, is_active, indent + 1, select_id=select_id)

        return row

    def _unsubscribe_from_activation_tab(self, local_mod_id, modio_id, mod_name):
        """Handles unsubscription triggered from the Activation tab right panel. Runs the same dependency warning, confirmation, API call, and local cleanup as the browser unsubscribe - but without a browser install_area."""
        # Dependent-mod warning (same check as uninstall_mod)
        dependents = [
            m['name'] for m in self.mods
            if m['id'] != local_mod_id
            and self.mod_statuses.get(m['id'], {}).get('active', False)
            and not self.mod_statuses.get(m['id'], {}).get('uninstalled', False)
            and local_mod_id in m.get('deps', {}).get('Require', [])
        ]
        if dependents:
            dep_lines = "\n".join(f"  •  {n}" for n in dependents)
            body = T(1999101417, mod_name, dep_lines)
            choice = self._imperial_dependency_warning(T(1999101411), body, btn_accept=T(1999101412), missing_dep_ids=None)
            if choice != "accept":
                return

        msg = T(1999101352, mod_name)
        if not self._imperial_question(T(1999101283), msg):
            return

        def worker():
            headers = {
                'Authorization': f'Bearer {self.modio_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            try:
                res = requests.delete(f"{MODIO_BASE_URL}/games/11358/mods/{modio_id}/subscribe", headers=headers, timeout=10)
                if res.status_code in [204, 404, 200]:
                    sid = str(modio_id)
                    if sid in self._subscription_states:
                        del self._subscription_states[sid]
                        self._save_subscriptions()
                    if local_mod_id in self._subscription_modio_map:
                        del self._subscription_modio_map[local_mod_id]
                        self._save_subscription_map()

                    self._delete_unsubscribed_mod(modio_id, mod_name)

                    def _success_then_orphan(mn=mod_name, mid=modio_id):
                        self._imperial_alert(T(1999101201),T(1999101420, mn))
                        threading.Thread(
                            target=self._check_and_remove_orphan_deps, args=(mid, mn), daemon=True).start()

                    self.after(0, _success_then_orphan)
                    self.after(0, self.render_activation_tab)
                else:
                    err = res.json().get('error', {}).get('message', 'Unknown Error')
                    self.after(0, lambda: self._imperial_alert(T(1999101298), T(1999101380, err), is_error=True))
            except Exception as e:
                self.after(0, lambda: self._imperial_alert(T(1999101189), T(1999101400, e), is_error=True))

        threading.Thread(target=worker, daemon=True).start()

    def uninstall_mod(self, mod_id):
        """Checks whether other active mods depend on the target mod, confirms with the user, then deletes the mod folder from disk and removes it from the active profile."""
        all_mods_list = self.get_all_mod_metadata()
        target_mod = next((m for m in all_mods_list if m['id'] == mod_id), None)

        if not target_mod:
            self._imperial_alert(T(1999101189), T(1999101231), is_error=True)
            return

        # Check if this mod is required by any other currently active mod
        dependents = [
            m['name'] for m in self.mods
            if m['id'] != mod_id
            and self.mod_statuses.get(m['id'], {}).get('active', False)
            and mod_id in m.get('deps', {}).get('Require', [])
        ]
        if dependents:
            dep_lines = "\n".join(f"  •  {n}" for n in dependents)
            body = T(1999101418, target_mod['name'], dep_lines)
            choice = self._imperial_dependency_warning(T(1999101411), body, btn_accept=T(1999101413), missing_dep_ids=None)
            if choice != "accept":
                return
        else:
            msg = T(1999101353, target_mod['name'])
            if not self._imperial_question(T(1999101211), msg):
                return

        try:
            if os.path.exists(target_mod['path']):
                shutil.rmtree(target_mod['path'])

            updated_lines = []
            found = False

            if os.path.exists(self.active_profile_path):
                with open(self.active_profile_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for line in lines:
                    clean = line.strip()
                    if not clean:
                        updated_lines.append(line)
                        continue
                    current_id = clean.lstrip('#').split('#')[0].strip()

                    if current_id == mod_id:
                        updated_lines.append(f"{mod_id} # not installed\n")
                        found = True
                    else:
                        updated_lines.append(line)

            if not found:
                updated_lines.append(f"{mod_id} # not installed\n")

            with open(self.active_profile_path, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)

            self.selected_row_frame = None
            self.update_right_panel({})

            self.get_all_mod_metadata()
            self.parse_active_profile()

            self._imperial_alert(T(1999101201), T(1999101358, target_mod['name']))
            self.render_activation_tab()

        except Exception as e:
            self._imperial_alert(T(1999101189), T(1999101393, e), is_error=True)

    def update_right_panel(self, mod):
        """Populates the right info panel with details for the selected mod: banner/thumbnail, name, creator, version, difficulty, setup flags, dependencies, known issues, folder path and file size."""
        if not mod or 'id' not in mod:
            for w in self.right_panel.winfo_children():
                w.destroy()
            tk.Label(self.right_panel, text=T(1999101028), font=FONT_TITLE, bg=BG_SECTION, fg=FG_DIM).pack(expand=True)
            return

        for w in self.right_panel.winfo_children():
            w.destroy()

        footer_btn_frame = tk.Frame(self.right_panel, bg=BG_SECTION)
        footer_btn_frame.pack(side="bottom", fill="x", pady=10)

        _ico_pfolder = load_icon("open_folder_panel", (24, 24))
        btn_openfolder = tk.Button(footer_btn_frame, text="" if _ico_pfolder else "📁", font=FONT_BOLD_SMALL, bg=BG_MAIN, fg=FG_MAIN, cursor="hand2", relief="raised", padx=10, image=_ico_pfolder, compound="center" if _ico_pfolder else "none", command=lambda: _open_path(mod['path']))
        if _ico_pfolder: btn_openfolder.image = _ico_pfolder
        btn_openfolder.pack(side="left", padx=15)
        self._bind_hover(btn_openfolder, BG_MAIN, BG_HOVER)
        self._attach_tooltip(btn_openfolder, T(1999101255))

        if not mod.get('parent_path'):
            modio_id = self._subscription_modio_map.get(mod['id'])
            if modio_id:
                _ico_unsub = load_icon("unsubscribe", (24, 24))
                btn_unsub = tk.Button(footer_btn_frame, text=T(1999101029), font=FONT_BOLD_SMALL, bg=FG_GOLD, fg="#000000", cursor="hand2", padx=10, image=_ico_unsub, compound="left" if _ico_unsub else "none", command=lambda mid=modio_id, mn=mod['name']: self._unsubscribe_from_activation_tab(mod['id'], mid, mn))
                if _ico_unsub: btn_unsub.image = _ico_unsub
                btn_unsub.pack(side="right", padx=15)
                self._bind_hover(btn_unsub, FG_GOLD, "#f9d23a")
                self._attach_tooltip(btn_unsub, T(1999101256))
                # Reinstall button — fetches fresh dl_url from mod.io then triggers download
                def _do_reinstall(mid=modio_id, mn=mod['name'], lid=mod['id']):
                    def _fetch_and_install():
                        try:
                            headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
                            res = requests.get(f"{MODIO_BASE_URL}/games/11358/mods/{mid}", headers=headers, timeout=10)
                            res.raise_for_status()
                            dl_url = (res.json().get('modfile') or {}).get('download', {}).get('binary_url')
                            if dl_url:
                                self._pending_modio_mapping = (str(mid), mn)
                                self.after(0, lambda u=dl_url, n=mn: self._download_and_install(u, n))
                                # Remove from update set immediately; re-check all after install settles
                                self._modio_update_available.discard(lid)
                                self.after(5000, lambda: threading.Thread(target=self._check_modio_version_updates, daemon=True).start())
                            else:
                                self.after(0, lambda: self._imperial_alert(T(1999101189), T(1999101472), is_error=True))
                        except Exception as e:
                            self.after(0, lambda: self._imperial_alert(T(1999101189), str(e), is_error=True))
                    if self._imperial_question(T(1999101213), T(1999101359, mn)):
                        threading.Thread(target=_fetch_and_install, daemon=True).start()
                _ico_rei = load_icon("reinstall", (20, 20))
                btn_reinstall = tk.Button(footer_btn_frame, text="" if _ico_rei else "↻", font=FONT_BOLD_SMALL, bg=BG_MAIN, fg=FG_MAIN, cursor="hand2", padx=8, image=_ico_rei, compound="center" if _ico_rei else "none", command=_do_reinstall)
                if _ico_rei: btn_reinstall.image = _ico_rei
                btn_reinstall.pack(side="right", padx=(0, 4))
                self._bind_hover(btn_reinstall, BG_MAIN, BG_HOVER)
                self._attach_tooltip(btn_reinstall, T(1999101268))
            else:
                _ico_uninst = load_icon("uninstall", (24, 24))
                btn_uninstall = tk.Button(footer_btn_frame, text=T(1999101030), font=FONT_BOLD_SMALL, bg="#8b0000", fg=FG_MAIN, cursor="hand2", padx=10, image=_ico_uninst, compound="left" if _ico_uninst else "none", command=lambda: self.uninstall_mod(mod['id']))
                if _ico_uninst: btn_uninstall.image = _ico_uninst
                btn_uninstall.pack(side="right", padx=15)
                self._bind_hover(btn_uninstall, "#8b0000", "#b10000")
                self._attach_tooltip(btn_uninstall, T(1999101257))

        canvas = tk.Canvas(self.right_panel, bg=BG_SECTION, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.right_panel, orient="vertical", command=canvas.yview)

        container = tk.Frame(canvas, bg=BG_SECTION)
        canvas_window = canvas.create_window((0, 0), window=container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
            bbox = canvas.bbox("all")
            canvas.configure(scrollregion=bbox)

            if bbox[3] <= canvas.winfo_height():
                scrollbar.pack_forget()
                canvas.unbind_all("<MouseWheel>")
            else:
                scrollbar.pack(side="right", fill="y")
                canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel_right))

        canvas.bind("<Configure>", _on_configure)

        def _on_mousewheel_right(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        canvas.pack(side="left", fill="both", expand=True)

        SAFE_WRAP = 450
        def add_divider():
            tk.Frame(container, height=1, bg=FG_DIM).pack(fill="x", padx=20, pady=10)

        full_title = f"{mod['name']}"
        tk.Label(container, text=full_title, font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, wraplength=SAFE_WRAP, justify="center").pack(pady=(15, 5), fill="x")

        if mod.get('has_options'):
            _ico_tweak = load_icon("tweaking_shortcut", (14, 14))
            btn_tweak_shortcut = tk.Button(container, text=T(1999101165), font=FONT_BOLD_SMALL, bg=BG_MAIN, fg=FG_GOLD, activebackground=BG_HOVER, activeforeground=FG_GOLD, cursor="hand2", relief="raised", image=_ico_tweak, compound="left" if _ico_tweak else "none", command=lambda m=mod: self.switch_tab("Tweaking", select_id=m.get('id')))
            if _ico_tweak: btn_tweak_shortcut.image = _ico_tweak
            btn_tweak_shortcut.pack(pady=5, fill="x", padx=20)
            self._bind_hover(btn_tweak_shortcut, BG_MAIN, BG_HOVER)
            self._attach_tooltip(btn_tweak_shortcut, T(1999101258))

            add_divider()

        banner_label = tk.Label(container, bg=BG_SECTION)
        banner_label.pack(pady=5)

        banner_found = False
        MAX_HEIGHT = 250

        for img_name in ["banner.png", "banner.jpg", "thumbnail.png", "thumbnail.jpg"]:
            img_path = os.path.join(mod['path'], img_name)
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    orig_w, orig_h = img.size

                    w_ratio = SAFE_WRAP / float(orig_w)
                    new_w = SAFE_WRAP
                    new_h = int(float(orig_h) * w_ratio)

                    if new_h > MAX_HEIGHT:
                        h_ratio = MAX_HEIGHT / float(orig_h)
                        new_h = MAX_HEIGHT
                        new_w = int(float(orig_w) * h_ratio)

                    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

                    photo = ImageTk.PhotoImage(img)
                    banner_label.config(image=photo)
                    banner_label.image = photo
                    banner_found = True
                    break
                except Exception as e:
                    print(f"Failed to load image {img_name}: {e}")

        if not banner_found:
            placeholder_path = resource_path("data/ui/modbanner_placeholder.jpg")
            if os.path.exists(placeholder_path):
                try:
                    img = Image.open(placeholder_path)
                    orig_w, orig_h = img.size
                    w_ratio = SAFE_WRAP / float(orig_w)
                    new_w = SAFE_WRAP
                    new_h = int(float(orig_h) * w_ratio)
                    if new_h > MAX_HEIGHT:
                        h_ratio = MAX_HEIGHT / float(orig_h)
                        new_h = MAX_HEIGHT
                        new_w = int(float(orig_w) * h_ratio)
                    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    banner_label.config(image=photo)
                    banner_label.image = photo
                except Exception as e:
                    print(f"Failed to load placeholder banner: {e}")
                    banner_label.pack_forget()
            else:
                banner_label.pack_forget()

        meta_line = tk.Frame(container, bg=BG_SECTION)
        meta_line.pack(fill="x", padx=20, pady=2)

        tk.Label(meta_line, text=T(1999101375, mod['version']), font=FONT_SMALL, bg=BG_SECTION, fg=FG_DIM).pack(side="left")

        if mod.get('creator'):
            tk.Label(meta_line, text=T(1999101376, mod['creator']), font=FONT_SMALL, bg=BG_SECTION, fg=FG_DIM).pack(side="right")

        add_divider()
        tk.Label(container, text=mod.get('desc', ""), font=FONT_DESC, bg=BG_SECTION, fg=FG_MAIN, wraplength=SAFE_WRAP, justify="left").pack(anchor="w", padx=20, pady=5)
        add_divider()

        # --- Difficulty & GameSetup Entries ---
        difficulty = mod.get('diff', 'Unchanged').lower()
        setup = mod.get('setup', {})

        # Only draw this section if there is actually data to show
        if difficulty or setup:
            # 1. Difficulty Display
            if difficulty:
                # Map internal keys to user-friendly labels if desired
                diff_map = {
                    "cheat": ("subscribed", "Cheat"),
                    "easier": ("arrow_down", "Easier"),
                    "harder": ("arrow_up",   "Harder"),
                    "unchanged": ("normal",     "Normal"),
                }
                diff_ico_key, diff_label = diff_map.get(difficulty, (None, difficulty.capitalize()))
                _ico_diff = load_icon(diff_ico_key, (16, 16)) if diff_ico_key else None

                diff_row = tk.Frame(container, bg=BG_SECTION)
                diff_row.pack(anchor="w", padx=20)
                tk.Label(diff_row, text=T(1999101032), font=FONT_BOLD_SMALL, bg=BG_SECTION, fg=FG_MAIN).pack(side="left")
                diff_lbl = tk.Label(diff_row, text=f" {diff_label}", image=_ico_diff or "", compound="left" if _ico_diff else "none", font=FONT_BOLD_SMALL, bg=BG_SECTION, fg=FG_MAIN)
                if _ico_diff: diff_lbl.image = _ico_diff
                diff_lbl.pack(side="left")

                # Small space between difficulty and the bullet points
                if setup:
                    tk.Frame(container, height=5, bg=BG_SECTION).pack()

            # 2. Game Setup (Bullet points)
            if setup:
                setup_text = ""
                if setup.get('RequiresNewGame'): setup_text += T(1999101453) + "\n"
                if setup.get('SafeToRemove'):   setup_text += T(1999101454) + "\n"
                if setup.get('Multiplayer'):    setup_text += T(1999101455) + "\n"
                if setup.get('Campaign'):       setup_text += T(1999101456)

                if setup_text:
                    tk.Label(container, text=setup_text.strip(), font=FONT_SMALL, bg=BG_SECTION, fg=FG_MAIN, justify="left").pack(anchor="w", padx=20)

            add_divider()

        # --- Dependencies Section ---
        deps = mod.get('deps', {})
        dep_sections = [
            # (label_T, entries, colour, show_status)
            # show_status: True  = ✔/✘ based on install state
            #              False = bullet point only (informational)
            #              "incompatible" = reversed logic (✘ if installed = bad)
            (T(1999101458), deps.get('Require',      []), "#e74c3c",  True),
            (T(1999101459), deps.get('Optional',     []), "#07C1D8",  False),
            (T(1999101460), deps.get('LoadAfter',    []), FG_GOLD,    False),
            (T(1999101461), deps.get('Deprecate',    []), "#e74c3c",  "incompatible"),
            (T(1999101462), deps.get('Incompatible', []), "#e74c3c",  "incompatible"),
        ]

        if any(entries for _, entries, _, __ in dep_sections):
            tk.Label(container, text=T(1999101033), font=FONT_BOLD_SMALL, bg=BG_SECTION, fg=FG_DIM).pack(anchor="w", padx=20, pady=(0, 6))

            installed_ids = {m['id']: m['name'] for m in self.mods}

            for label, entries, colour, show_status in dep_sections:
                if not entries:
                    continue

                section_frame = tk.Frame(container, bg=BG_SECTION)
                section_frame.pack(fill="x", padx=20, pady=(2, 4))

                tk.Label(section_frame, text=f"{label}:", font=FONT_XSMALL, bg=BG_SECTION, fg=colour).pack(anchor="w")

                for dep_id in entries:
                    row_frame = tk.Frame(section_frame, bg=BG_SECTION)
                    row_frame.pack(fill="x", padx=10, pady=1)

                    if dep_id == "*":
                        status_icon  = "•"
                        status_fg    = FG_MAIN
                        display_name = T(1999101463)
                        name_fg      = FG_MAIN
                    else:
                        is_installed = dep_id in installed_ids
                        display_name = installed_ids.get(dep_id, dep_id)

                        if show_status == "incompatible":
                            # Installed = conflict = bad (red ✘), absent = safe (dim ✔)
                            status_icon = "✘" if is_installed else "✔"
                            status_fg   = "#e74c3c" if is_installed else FG_DIM
                            name_fg     = FG_MAIN if is_installed else FG_DIM
                        elif show_status:
                            # Hard requirement: installed = good (✔), missing = bad (✘)
                            status_icon = "✔" if is_installed else "✘"
                            status_fg   = "#2ecc71" if is_installed else "#e74c3c"
                            name_fg     = FG_MAIN if is_installed else FG_DIM
                        else:
                            # Informational only: always a neutral bullet
                            status_icon = "•"
                            status_fg   = FG_DIM
                            name_fg     = FG_MAIN

                    icon_width = 0 if dep_id == "*" else 2
                    tk.Label(row_frame, text=status_icon, font=FONT_XSMALL, bg=BG_SECTION, fg=status_fg, width=icon_width).pack(side="left")
                    tk.Label(row_frame, text=display_name, font=FONT_XSMALL, bg=BG_SECTION, fg=name_fg, wraplength=360, justify="left").pack(side="left")

            add_divider()

        # --- Known Issues Section ---
        known_issues = mod.get('known_issues', '').strip()
        if known_issues:
            tk.Label(container, text=T(1999101457), font=FONT_BOLD_SMALL, bg=BG_SECTION, fg=FG_DIM).pack(anchor="w", padx=20, pady=(0, 6))
            tk.Label(container, text=known_issues, font=FONT_SMALL, bg=BG_SECTION, fg="#e67e22", wraplength=450, justify="left").pack(anchor="w", padx=30, pady=(0, 4))
            add_divider()

        folder_frame = tk.Frame(container, bg=BG_SECTION)
        folder_frame.pack(fill="x", padx=20)

        tk.Label(folder_frame, text=T(1999101034), font=FONT_XSMALL, bg=BG_SECTION, fg=FG_DIM).pack(side="left", anchor="nw")
        tk.Label(folder_frame, text=os.path.basename(mod['path']), font=FONT_XSMALL, bg=BG_SECTION, fg=FG_MAIN, wraplength=400, justify="right").pack(side="right")

        size_line = tk.Frame(container, bg=BG_SECTION)
        size_line.pack(fill="x", padx=20, pady=(5, 15))

        size_bytes = self.get_dir_size(mod['path'])
        size_mb = size_bytes / (1024 * 1024)

        if size_mb < 0.1:
            size_kb = size_bytes / 1024
            size_display = f"{size_kb:.2f} KB"
        else:
            size_display = f"{size_mb:.2f} MB"

        tk.Label(size_line, text=T(1999101035), font=FONT_XSMALL, bg=BG_SECTION, fg=FG_DIM).pack(side="left")
        tk.Label(size_line, text=size_display, font=FONT_XSMALL, bg=BG_SECTION, fg=FG_MAIN).pack(side="right")

    def toggle_mod_status(self, mod_id, should_be_active):
        """Reads the active-profile.txt line by line and comments or uncomments the entry for the given mod_id, writing the result back to disk."""
        if not os.path.exists(self.active_profile_path):
            return

        updated_lines = []
        found = False
        with open(self.active_profile_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            clean = line.strip()
            parts = clean.split()
            if not clean or clean.startswith("##"):
                updated_lines.append(line)
                continue

            current_id = clean.lstrip('#').split('#')[0].strip().split()[0]

            if current_id == mod_id:
                found = True
                comment = ""
                if "#" in clean:
                    comment_idx = clean.find("#", 1)
                    if comment_idx != -1:
                        comment = " " + clean[comment_idx:].strip()
                        if should_be_active:
                            comment = comment.replace("# not installed", "").strip()
                            if comment: comment = " " + comment

                prefix = "" if should_be_active else "# "
                updated_lines.append(f"{prefix}{mod_id}{comment}\n")
            else:
                updated_lines.append(line)

        if not found:
            prefix = "" if should_be_active else "# "
            updated_lines.append(f"{prefix}{mod_id}\n")

        with open(self.active_profile_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)

    def toggle_sort(self, col):
        """Cycles the sort direction for the given column (status, category or name) and re-renders the activation tab to reflect the new order."""
        if col == "status":
            self.sort_active_first = not self.sort_active_first
        elif col == "category":
            # Cycle: A-Z (1) -> Z-A (-1) -> Off (0)
            if self.sort_cat_dir == 1: self.sort_cat_dir = -1
            elif self.sort_cat_dir == -1: self.sort_cat_dir = 0
            else: self.sort_cat_dir = 1
        elif col == "name":
            self.sort_name_dir *= -1

        self.last_clicked_col = col
        self.render_activation_tab()

    def _toggle_load_order(self):
        """Toggles load order view on/off and re-renders the activation tab."""
        self.show_load_order = not self.show_load_order
        self.render_activation_tab()

    def _check_missing_dependencies(self):
        """Returns a list of (mod_name, missing_dep_id) tuples for all active mods that have a required dependency not present in the active mod list."""
        active_ids = {
            mid for mid, status in self.mod_statuses.items()
            if status.get('active', False) and not status.get('uninstalled', False)
        }
        missing = []
        for mod in self.mods:
            if mod.get('parent_path'):
                continue
            if not self.mod_statuses.get(mod['id'], {}).get(
                    'active', self.enable_new_mods_var.get()):
                continue
            for req_id in mod.get('deps', {}).get('Require', []):
                if req_id not in active_ids:
                    missing.append((mod['name'], req_id))
        return missing

    def _imperial_dependency_warning(self, title, body, btn_accept, missing_dep_ids=None):
        """Three-button dependency warning dialog."""

        win_w, win_h = 600, 380
        warn_win = tk.Toplevel(self)
        warn_win.title(title)
        warn_win.geometry(f"{win_w}x{win_h}")

        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        warn_win.geometry(f"+{x}+{y}")

        warn_win.configure(bg=BG_MAIN)
        warn_win.transient(self)
        warn_win.grab_set()

        result = {"ans": "back"}

        def _select(val):
            result["ans"] = val
            warn_win.destroy()

        tk.Label(warn_win, text=title.upper(), font=FONT_TITLE, bg=BG_MAIN, fg="#e74c3c").pack(pady=(22, 8))

        tk.Label(warn_win, text=body, font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, wraplength=540, justify="center").pack(pady=8, expand=True)

        btn_frame = tk.Frame(warn_win, bg=BG_MAIN)
        btn_frame.pack(pady=(0, 24))

        accept_btn = tk.Button(btn_frame, text=btn_accept, font=FONT_UI_BOLD, bg="#c0392b", activebackground="#db4332", fg=FG_MAIN, width=14, cursor="hand2", relief="raised", command=lambda: _select("accept"))
        accept_btn.pack(side="left", padx=8)
        self._bind_hover(accept_btn, "#c0392b", "#db4332")

        if missing_dep_ids:
            locally_found = [
                m for m in self.mods
                if m['id'] in missing_dep_ids and not m.get('parent_path')
            ]
            all_found_locally = len(locally_found) == len(missing_dep_ids)

            def _activate_deps():
                for m in locally_found:
                    self.toggle_mod_status(m['id'], True)
                self.parse_active_profile()
                _select("activated")

            btn_activate = tk.Button(btn_frame, text=T(1999101036), font=FONT_UI_BOLD, bg="#2e7d32" if all_found_locally else BG_SECTION, fg=FG_MAIN, activebackground="#388e3c" if all_found_locally else BG_SECTION, width=14, cursor="hand2" if all_found_locally else "arrow", relief="raised", state="normal" if all_found_locally else "disabled", command=_activate_deps)
            btn_activate.pack(side="left", padx=8)
            self._bind_hover(btn_activate, "#2e7d32", "#388e3c") if all_found_locally else self._bind_hover(btn_activate, BG_SECTION, BG_HOVER)
            self._attach_tooltip(btn_activate, T(1999101259))

        btn_back = tk.Button(btn_frame, text=T(1999101037), font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, activebackground=BG_HOVER, width=14, cursor="hand2", relief="raised", command=lambda: _select("back"))
        btn_back.pack(side="left", padx=8)
        self._bind_hover(btn_back, BG_SECTION, BG_HOVER)

        self.wait_window(warn_win)
        return result["ans"]

    # ==========================================
    # --- MODLOADER LOG TAB ---
    # ==========================================
    def copy_log_text(self):
        """Copies the entire content of the mod-loader.log text area to the system clipboard and alerts the user on success."""
        try:
            content = self.log_text_area.get("1.0", "end")
            self.clipboard_clear()
            self.clipboard_append(content)
            self._imperial_alert(T(1999101195), T(1999101228))
        except Exception as e:
            self._imperial_alert(T(1999101189), T(1999101391, e), is_error=True)
    def render_log_tab(self):
        """Renders the Modloader Log tab: refresh and clipboard-copy buttons, and a read-only scrollable text area that loads and syntax-highlights the mod-loader.log file."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        btn_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        btn_frame.pack(fill="x", pady=5, padx=10)

        refresh_btn = tk.Button(btn_frame, text=T(1999101041), font=FONT_SMALL, bg=BG_SECTION, fg=FG_MAIN, cursor="hand2", command=self.render_log_tab)
        refresh_btn.pack(side="left", padx=5)
        self._bind_hover(refresh_btn, BG_SECTION, BG_HOVER)
        self._attach_tooltip(refresh_btn, T(1999101260))
        clipboard_btn = tk.Button(btn_frame, text=T(1999101042), font=FONT_SMALL, bg=BG_SECTION, fg=FG_MAIN, cursor="hand2", command=self.copy_log_text)
        clipboard_btn.pack(side="left", padx=5)
        self._bind_hover(clipboard_btn, BG_SECTION, BG_HOVER)
        self._attach_tooltip(clipboard_btn, T(1999101261))

        log_container = tk.Frame(self.main_content, bg=BG_MAIN)
        log_container.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(log_container)
        scrollbar.pack(side="right", fill="y")

        self.log_text_area = tk.Text(log_container, bg="#050c17", fg=FG_MAIN, font=("Consolas", 10), yscrollcommand=scrollbar.set, wrap="word", state="normal")
        self.log_text_area.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.log_text_area.yview)

        self.log_text_area.tag_config("ERROR", foreground="#ff4c4c")
        self.log_text_area.tag_config("WARNING", foreground="#ffcc00")

        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        start_index = self.log_text_area.index("end-1c")
                        self.log_text_area.insert("end", line)
                        line_end_index = self.log_text_area.index(f"{start_index} lineend")

                        upper_line = line.upper()
                        if "ERROR" in upper_line or "[ERRO]" in upper_line:
                            self.log_text_area.tag_add("ERROR", start_index, line_end_index)
                        elif "WARN" in upper_line:
                            self.log_text_area.tag_add("WARNING", start_index, line_end_index)
            except Exception as e:
                self.log_text_area.insert("end", T(1999101425, e))
        else:
            self.log_text_area.insert("end", T(1999101426, self.log_path))

        self.log_text_area.config(state="disabled")

    # ==========================================
    # --- SETTINGS TAB ---
    # ==========================================
    def _attach_tooltip(self, widget, text):
        """Attaches a hover tooltip to widget when Tutorial Infotips is enabled."""
        tip_win = [None]

        def _show(e):
            if not self.show_tooltips_var.get():
                return
            if tip_win[0] and tip_win[0].winfo_exists():
                return
            x = widget.winfo_rootx() + 10
            y = widget.winfo_rooty() + widget.winfo_height() + 4
            tw = tk.Toplevel(self)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            tw.configure(bg=BG_MAIN)
            border = tk.Frame(tw, bg=FG_GOLD, padx=1, pady=1)
            border.pack(fill="both", expand=True)
            inner = tk.Frame(border, bg=BG_MAIN)
            inner.pack(fill="both", expand=True)
            tk.Label(inner, text=text, font=FONT_XSMALL, bg=BG_MAIN, fg=FG_MAIN, padx=7, pady=3, wraplength=300, justify="left").pack()
            tip_win[0] = tw

        def _hide(e):
            if tip_win[0] and tip_win[0].winfo_exists():
                tip_win[0].destroy()
            tip_win[0] = None

        widget.bind("<Enter>", _show, add="+")
        widget.bind("<Leave>", _hide, add="+")
        widget.bind("<ButtonPress>", _hide, add="+")

    def render_settings_tab(self):
        """Renders the Settings tab with a scrollable body."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Title — above the scroll area
        tk.Label(self.main_content, text=T(1999101043), font=FONT_TITLE, bg=BG_MAIN, fg=FG_MAIN).pack(pady=(0, 10), anchor="w")

        # Footer — pinned at bottom before canvas so pack(side="bottom") wins
        footer_row = tk.Frame(self.main_content, bg=BG_MAIN)
        footer_row.pack(side="bottom", fill="x", pady=10, padx=20)
        tk.Label(footer_row, text=T(1999101373, self.settings_file), font=FONT_XSMALL, bg=BG_MAIN, fg=FG_DIM).pack(side="left")
        _dlp = _debug_log_path
        def _open_log():
            if os.path.exists(_dlp): _open_path(_dlp)
            else: self._imperial_alert(T(1999101199), T(1999101234))
        def _open_config():
            if os.path.exists(self.appdata_dir): _open_path(self.appdata_dir)
            else: self._imperial_alert(T(1999101200), T(1999101235))
        _bcf = tk.Button(footer_row, text=T(1999101062), font=FONT_XSMALL, bg=BG_SECTION, fg=FG_DIM, cursor="hand2", relief="raised", padx=10, command=_open_config)
        _bcf.pack(side="right")
        self._bind_hover(_bcf, BG_SECTION, BG_HOVER)
        self._attach_tooltip(_bcf, T(1999101423))
        _blg = tk.Button(footer_row, text=T(1999101063), font=FONT_XSMALL, bg=BG_SECTION, fg=FG_DIM, cursor="hand2", relief="raised", padx=10, command=_open_log)
        _blg.pack(side="right")
        self._bind_hover(_blg, BG_SECTION, BG_HOVER)
        self._attach_tooltip(_blg, T(1999101424, _dlp))

        # Scrollable body
        _sc = tk.Canvas(self.main_content, bg=BG_MAIN, highlightthickness=0)
        _sb = ttk.Scrollbar(self.main_content, orient="vertical", command=_sc.yview)
        _sf = tk.Frame(_sc, bg=BG_MAIN)
        _sc.configure(yscrollcommand=_sb.set)
        _cw = _sc.create_window((0, 0), window=_sf, anchor="nw")
        def _frame_cfg(e):
            _sc.configure(scrollregion=_sc.bbox("all"))
        _sf.bind("<Configure>", _frame_cfg)
        def _canvas_cfg(e):
            _sc.itemconfig(_cw, width=e.width)
        _sc.bind("<Configure>", _canvas_cfg)
        _sc.bind("<Enter>", lambda e: _sc.bind_all("<MouseWheel>",
            lambda ev: _sc.yview_scroll(int(-1*(ev.delta/120)), "units")))
        _sc.bind("<Leave>", lambda e: _sc.unbind_all("<MouseWheel>"))
        _sb.pack(side="right", fill="y")
        _sc.pack(side="left", fill="both", expand=True)
        _mc = _sf  # all widgets below go into _mc

        display_root = ""
        if self.game_exe_path:
            display_root = os.path.dirname(os.path.dirname(os.path.dirname(self.game_exe_path)))
        self.game_path_var = tk.StringVar(value=os.path.normpath(display_root))

        # GENERAL
        general_frame = tk.LabelFrame(_mc, text=T(1999101044), font=FONT_BOLD_SMALL, bg=BG_MAIN, fg=FG_DIM, padx=15, pady=15)
        general_frame.pack(fill="x", pady=10, padx=5)

        # Language selector
        lang_row = tk.Frame(general_frame, bg=BG_MAIN)
        lang_row.pack(anchor="w", pady=(8, 0))
        tk.Label(lang_row, text=T(1999101156), font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN).pack(side="left")

        lang_options = {display: key for key, display in _LANGUAGE_DISPLAY_NAMES}
        current_lang_key = self.settings.get(_LANGUAGE_SETTINGS_KEY, _detect_lang())
        current_display = next(
            (d for k, d in _LANGUAGE_DISPLAY_NAMES if k == current_lang_key),
            "English")
        lang_var = tk.StringVar(value=current_display)

        lang_menu = tk.OptionMenu(lang_row, lang_var, *lang_options.keys())
        lang_menu.config(font=FONT_XSMALL, bg=BG_SECTION, fg=FG_MAIN, highlightthickness=0, width=20)
        lang_menu["menu"].config(bg=BG_SECTION, fg=FG_MAIN)
        lang_menu.pack(side="left", padx=10)

        def _apply_lang_change(*_):
            chosen_key = lang_options[lang_var.get()]
            self.settings[_LANGUAGE_SETTINGS_KEY] = chosen_key
            self.save_settings()
            _init_loca(chosen_key)
            self._build_sidebar()                  # rebuild with new language
            self._update_sidebar_highlights()      # restore active tab highlight
            self.switch_tab(self.current_tab)      # re-render tab content

        lang_var.trace_add("write", _apply_lang_change)
        tk.Label(general_frame, text=T(1999101157), font=FONT_XSMALL, bg=BG_MAIN, fg=FG_DIM).pack(anchor="w", padx=25)

        # Tutorial tooltips
        def on_tooltip_toggle():
            self.settings["show_tooltips"] = self.show_tooltips_var.get()
            self.save_settings()

        tk.Checkbutton(general_frame, text=T(1999101045), variable=self.show_tooltips_var, command=on_tooltip_toggle, font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN, selectcolor=BG_SECTION, activebackground=BG_MAIN, activeforeground=FG_MAIN, cursor="hand2").pack(anchor="w")
        tk.Label(general_frame, text=T(1999101046), font=FONT_XSMALL, bg=BG_MAIN, fg=FG_DIM).pack(anchor="w", padx=25)

        # reddit news
        def on_reddit_toggle():
            self.settings["show_reddit_news"] = self.show_reddit_news_var.get()
            self.save_settings()
            self._session_news = []  # force re-fetch on next News tab visit

        tk.Checkbutton(general_frame, text=T(1999101047), variable=self.show_reddit_news_var, command=on_reddit_toggle, font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN, selectcolor=BG_SECTION, activebackground=BG_MAIN, activeforeground=FG_MAIN, cursor="hand2").pack(anchor="w")
        tk.Label(general_frame, text=T(1999101048), font=FONT_XSMALL, bg=BG_MAIN, fg=FG_DIM).pack(anchor="w", padx=25)

        # Automatically activate installed mods — tri-state dropdown
        _auto_row = tk.Frame(general_frame, bg=BG_MAIN)
        _auto_row.pack(anchor="w", fill="x", pady=(4, 0))
        tk.Label(_auto_row, text=T(1999101049), font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN).pack(side="left")
        _auto_opts = {T(1999101469): "on", T(1999101470): "off", T(1999101471): "keep"}
        _cur_ad = next((d for d, v in _auto_opts.items() if v == self.enable_new_mods_var.get()), T(1999101469))
        _adv = tk.StringVar(value=_cur_ad)
        _am = tk.OptionMenu(_auto_row, _adv, *_auto_opts.keys())
        _am.config(font=FONT_XSMALL, bg=BG_SECTION, fg=FG_MAIN, highlightthickness=0, width=20)
        _am["menu"].config(bg=BG_SECTION, fg=FG_MAIN)
        _am.pack(side="left", padx=10)
        def _on_ac(*_):
            self.enable_new_mods_var.set(_auto_opts[_adv.get()])
            self.update_enable_new_mods_in_file()
        _adv.trace_add("write", _on_ac)
        tk.Label(general_frame, text=T(1999101050), font=FONT_XSMALL, bg=BG_MAIN, fg=FG_DIM).pack(anchor="w", padx=25)

        # jump to activation tab after mod browser install setting
        self.var_jump_activation = tk.BooleanVar(value=getattr(self, 'jump_to_activation', True))

        def _toggle_jump():
            self.jump_to_activation = self.var_jump_activation.get()
            self.save_settings()

        chk_jump = tk.Checkbutton(general_frame, text=T(1999101478), variable=self.var_jump_activation, bg=BG_MAIN, fg=FG_MAIN, selectcolor=BG_SECTION,  activebackground=BG_MAIN, activeforeground=FG_MAIN,  font=FONT_SMALL, cursor="hand2", command=_toggle_jump)
        chk_jump.pack(anchor="w", pady=2)

        # GAME INSTALLATION PATH
        path_frame = tk.LabelFrame(_mc, text=T(1999101051), font=FONT_BOLD_SMALL, bg=BG_MAIN, fg=FG_DIM, padx=15, pady=15)
        path_frame.pack(fill="x", pady=10, padx=5)

        tk.Label(path_frame, text=T(1999101052), font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN).pack(anchor="w")

        e_frame = tk.Frame(path_frame, bg=BG_MAIN)
        e_frame.pack(fill="x", pady=5)

        tk.Entry(e_frame, textvariable=self.game_path_var, font=FONT_SMALL, bg=BG_SECTION, fg=FG_MAIN, relief="flat").pack(side="left", fill="x", expand=True, ipady=4)
        browse_btn = tk.Button(e_frame, text=T(1999101053), font=FONT_SMALL, bg=BG_SECTION, fg=FG_MAIN, cursor="hand2", command=self.browse_game_path)
        browse_btn.pack(side="right", padx=(10, 0))
        self._bind_hover(browse_btn, BG_SECTION, BG_HOVER)
        self._attach_tooltip(browse_btn, T(1999101262))

        # Custom Anno 117 Documents folder override
        tk.Label(path_frame, text=T(1999101466), font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN).pack(anchor="w", pady=(10, 0))
        tk.Label(path_frame, text=T(1999101467), font=FONT_XSMALL, bg=BG_MAIN, fg=FG_DIM).pack(anchor="w", padx=25)
        _dov_row = tk.Frame(path_frame, bg=BG_MAIN)
        _dov_row.pack(fill="x", pady=4)
        _docs_var = tk.StringVar(value=getattr(self, "custom_docs_path", ""))
        tk.Entry(_dov_row, textvariable=_docs_var, font=FONT_SMALL, bg=BG_SECTION, fg=FG_MAIN, relief="flat").pack(side="left", fill="x", expand=True, ipady=4)
        def _browse_docs():
            ch = filedialog.askdirectory(title=T(1999101475))
            if ch:
                # Accept either the "Anno 117 - Pax Romana" folder or its "mods" subfolder
                ch = os.path.normpath(ch)
                if os.path.basename(ch).lower() == "mods":
                    ch = os.path.dirname(ch)  # step up to "Anno 117 - Pax Romana"
                self.custom_docs_path = ch
                _docs_var.set(self.custom_docs_path)
                _clr.config(state="normal")
                self.update_mod_path_from_mode()
                self.save_settings()
                # Refresh the mod storage radio label to show the updated path
                new_docs_display = os.path.normpath(os.path.join(self.custom_docs_path, "mods"))
                for w in loc_frame.winfo_children():
                    if isinstance(w, tk.Radiobutton):
                        cfg = w.config()
                        if "Documents" in str(cfg.get("value", [""])):
                            w.config(text=T(1999101371, new_docs_display))
                            break
        def _clear_docs():
            self.custom_docs_path = ""
            _docs_var.set("")
            _clr.config(state="disabled")
            self.update_mod_path_from_mode()
            self.save_settings()
        tk.Button(_dov_row, text=T(1999101053), font=FONT_SMALL, bg=BG_SECTION, fg=FG_MAIN, cursor="hand2", command=_browse_docs).pack(side="left", padx=(6, 0))
        _clr = tk.Button(_dov_row, text=T(1999101468), font=FONT_SMALL, bg=BG_SECTION, fg=FG_DIM, cursor="hand2" if getattr(self, "custom_docs_path", "") else "arrow", state="normal" if getattr(self, "custom_docs_path", "") else "disabled", command=_clear_docs)
        _clr.pack(side="left", padx=(4, 0))

        # MOD INSTALLATION PATH
        loc_frame = tk.Frame(path_frame, bg=BG_MAIN)
        loc_frame.pack(fill="x", pady=5)

        if getattr(self, 'custom_docs_path', ''):
            docs_raw = os.path.join(self.custom_docs_path, "mods")
        else:
            user_docs = os.path.expanduser("~/Documents")
            docs_raw = os.path.join(user_docs, "Anno 117 - Pax Romana", "mods")
        docs_display = os.path.normpath(docs_raw)

        if self.game_exe_path:
            game_root = os.path.dirname(os.path.dirname(os.path.dirname(self.game_exe_path)))
            game_display = os.path.join(game_root, "mods")
        else:
            game_display = ".../Anno 117 - Pax Romana/mods"

        tk.Label(loc_frame, text=T(1999101054), font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN).pack(anchor="w")
        tk.Radiobutton(loc_frame, text=T(1999101371, docs_display), variable=self.mod_loc_mode, value="Documents", font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN, selectcolor=BG_SECTION, cursor="hand2", command=self.save_settings).pack(anchor="w", pady=5)
        tk.Radiobutton(loc_frame, text=T(1999101372, game_display), variable=self.mod_loc_mode, value="Game", font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN, selectcolor=BG_SECTION, cursor="hand2", command=self.save_settings).pack(anchor="w", pady=5)

        # MOD.IO SETTINGS
        auth_frame = tk.LabelFrame(_mc, text=T(1999101055), font=FONT_BOLD_SMALL, bg=BG_MAIN, fg=FG_DIM, padx=15, pady=15)
        auth_frame.pack(fill="x", pady=10, padx=5)
        logo_path = resource_path("data/ui/4k/base/icon_content/modio/icon_2d_modio_logo_blue_white.png")
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path).convert("RGBA")
                orig_w, orig_h = img.size
                new_h = 46
                new_w = int(new_h * (orig_w / orig_h))
                img   = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl   = tk.Label(auth_frame, image=photo, bg=BG_MAIN)
                lbl.image = photo
                lbl.pack(anchor="w", pady=(0, 8))
            except Exception as e:
                print(f"[Logo] Failed to load mod.io logo in settings: {e}")

        # 1. API KEY ROW (Horizontal)
        api_row = tk.Frame(auth_frame, bg=BG_MAIN)
        api_row.pack(fill="x", pady=5)

        tk.Label(api_row, text=T(1999101056), font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, width=15, anchor="w").pack(side="left")

        self.api_key_var = tk.StringVar(value=self.settings.get("modio_api_key", ""))
        api_entry = tk.Entry(api_row, textvariable=self.api_key_var, font=FONT_BODY, bg=BG_SECTION, fg=FG_MAIN, show="*", width=40)
        api_entry.pack(side="left", padx=(0, 10))

        def save_settings_key():
            new_key = self.api_key_var.get().strip()
            self.settings["modio_api_key"] = new_key
            self.modio_api_key = new_key
            self.settings["use_mod_browser"] = bool(new_key)
            self.save_settings()
            self.refresh_sidebar_state()
            self._imperial_alert(T(1999101198), T(1999101233))
            if new_key and not self.settings.get("modio_token"):
                self._prompt_modio_auth()

        btn_savekey = tk.Button(api_row, text=T(1999101057), font=FONT_BOLD_SMALL, bg="#07C1D8", fg=FG_MAIN, cursor="hand2", activebackground="#39a8f1", command=save_settings_key)
        btn_savekey.pack(side="left")
        self._bind_hover(btn_savekey, "#07C1D8", "#09E2FF")
        self._attach_tooltip(btn_savekey, T(1999101263))

        # 2. STATUS ROW (New line under the API Key)
        status_row = tk.Frame(auth_frame, bg=BG_MAIN)
        status_row.pack(fill="x", pady=(10, 0))

        # We use anchor="w" and pack(side="top") here to stack the status and button vertically or we pack them side-by-side in this second row.
        if self.modio_token:
            tk.Label(status_row, text=T(1999101058), font=FONT_SMALL, bg=BG_MAIN, fg="#2ecc71").pack(side="left", pady=5)
            disc_btn = tk.Button(status_row, text=T(1999101059), command=self._disconnect_modio, bg=BG_SECTION, fg=FG_MAIN, relief="raised", cursor="hand2", padx=10)
            disc_btn.pack(side="left", padx=20)
            self._bind_hover(disc_btn, BG_MAIN, BG_HOVER)
            self._attach_tooltip(disc_btn, T(1999101264))
        else:
            tk.Label(status_row, text=T(1999101060), font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN).pack(side="left", pady=5)
            connect_btn = tk.Button(status_row, text=T(1999101061), command=lambda: self._prompt_api_key_setup() if not self.settings.get("modio_api_key") else self._prompt_modio_auth(), bg="#2ecc71", fg="#000000", relief="raised", cursor="hand2", padx=10)
            connect_btn.pack(side="left", padx=20)
            self._bind_hover(connect_btn, "#2ecc71", "#36e780")
            self._attach_tooltip(connect_btn, T(1999101265))


    def set_game_path_from_root(self, root_path):
        """Given an Anno 117 installation root directory, validates that Anno117.exe exists inside it and updates game_exe_path and all derived mod paths accordingly. Returns True on success."""
        if not root_path:
            return False

        candidates = [
            os.path.join(root_path, "Bin", "Win64", "Anno117.exe"),
            os.path.join(root_path, "Anno 117 - Pax Romana", "Bin", "Win64", "Anno117.exe"),
        ]

        for candidate in candidates:
            candidate = os.path.normpath(candidate)
            if os.path.exists(candidate):
                self.game_exe_path = candidate
                pax_romana_dir = os.path.dirname(os.path.dirname(os.path.dirname(candidate)))
                if hasattr(self, 'game_path_var'):
                    self.game_path_var.set(os.path.normpath(pax_romana_dir))
                self.save_settings()
                return True

        self._imperial_alert(T(1999101284), T(1999101395, root_path), is_error=True)
        return False

    def browse_game_path(self):
        """Opens a directory picker and passes the chosen path to set_game_path_from_root."""
        path = filedialog.askdirectory(title="Select Anno 117 Installation Directory")
        if path:
            normalized_path = os.path.normpath(path)
            self.set_game_path_from_root(normalized_path)

    def update_mod_path_from_mode(self):
        """Recalculates mod_path and the active-profile/log/options file paths. Respects a custom Anno 117 documents folder if the user has configured one."""
        if getattr(self, 'custom_docs_path', ''):
            docs_base = os.path.normpath(os.path.join(self.custom_docs_path, "mods"))
        else:
            if IS_WINDOWS:
                user_docs = os.path.expanduser("~/Documents")
            else:
                # On Linux the game runs under Proton; try the Proton documents path first
                home = os.path.expanduser("~")
                proton_docs = None
                _compat_root = os.path.join(home, ".steam", "steam", "steamapps", "compatdata")
                if os.path.isdir(_compat_root):
                    for _appid in os.listdir(_compat_root):
                        _candidate = os.path.join(_compat_root, _appid, "pfx", "drive_c", "users", "steamuser", "Documents")
                        if os.path.isdir(os.path.join(_candidate, "Anno 117 - Pax Romana")):
                            proton_docs = _candidate
                            break
                user_docs = proton_docs or os.path.join(home, "Documents")
            docs_base = os.path.normpath(os.path.join(user_docs, "Anno 117 - Pax Romana", "mods"))

        self.active_profile_path = os.path.join(docs_base, "active-profile.txt")
        self.log_path = os.path.join(docs_base, "mod-loader.log")
        self.options_path = os.path.join(docs_base, "active-options.jsonc")

        if self.mod_loc_mode.get() == "Documents":
            self.mod_path = docs_base
        else:
            if self.game_exe_path:
                game_root = os.path.dirname(os.path.dirname(os.path.dirname(self.game_exe_path)))
                self.mod_path = os.path.normpath(os.path.join(game_root, "mods"))
            else:
                self.mod_path = docs_base

        for p in [docs_base, self.mod_path]:
            if p and not os.path.exists(p):
                try:
                    os.makedirs(p, exist_ok=True)
                except Exception as e:
                    print(f"Could not create directory {p}: {e}")

    def update_enable_new_mods_in_file(self):
        """Syncs the UI toggle with the active-profile.txt file."""
        if not os.path.exists(self.active_profile_path):
            return

        with open(self.active_profile_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_val = self.enable_new_mods_var.get() in ("on", "keep")
        found = False
        updated_lines = []

        for line in lines:
            if "EnableNewMods" in line:
                found = True
                # Remove any existing '#' and set based on toggle
                prefix = "" if new_val else "# "
                updated_lines.append(f"{prefix}EnableNewMods\n")
            else:
                updated_lines.append(line)

        if not found:
            prefix = "" if new_val else "# "
            updated_lines.append(f"{prefix}EnableNewMods\n")

        with open(self.active_profile_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)

        self.save_settings()

    def save_settings(self):
        """Serialises all current settings to the JSON settings file in %APPDATA%, including game path, mod.io credentials, language, UI preferences and expiry timestamps."""
        # 1. Update the game path logic
        ui_path = self.game_path_var.get() if hasattr(self, 'game_path_var') else self.game_exe_path
        if ui_path and not ui_path.lower().endswith(".exe"):
            for sub in [
                os.path.join(ui_path, "Anno 117 - Pax Romana", "Bin", "Win64", "Anno117.exe"),
                os.path.join(ui_path, "Bin", "Win64", "Anno117.exe"),
            ]:
                if os.path.exists(sub):
                    self.game_exe_path = os.path.normpath(sub)
                    break
        else:
            self.game_exe_path = ui_path

        self.update_mod_path_from_mode()

        # 2. Update the PERSISTENT settings dictionary
        self.settings.update({
            "game_path": self.game_exe_path,
            "mod_location_mode": self.mod_loc_mode.get(),
            "current_profile_name": getattr(self, "current_profile_name", "Default"),
            "enable_new_mods": self.enable_new_mods_var.get(),
            "show_reddit_news": self.show_reddit_news_var.get(),
            "show_tooltips":    self.show_tooltips_var.get(),
            "modio_token": getattr(self, "modio_token", ""),
            "modio_terms_agreed": getattr(self, "modio_terms_agreed", False),
            "modio_token_expires": getattr(self, "modio_token_expires", 0),
            "modio_declined": getattr(self, "modio_declined", False),
            "custom_docs_path": getattr(self, "custom_docs_path", ""),
            **({"use_mod_browser": self.settings["use_mod_browser"]}
               if self.settings.get("use_mod_browser") is not None else {}),
            "jump_to_activation": getattr(self, "jump_to_activation", True)
        })

        # 3. Save the entire dictionary to the file
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

        # 4. Refresh metadata
        self.get_all_mod_metadata()

    def load_settings(self):
        """Reads the JSON settings file from %APPDATA% and populates all corresponding instance variables. Silently uses defaults if the file is missing or unreadable."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    # Load directly into the class attribute
                    self.settings = json.load(f)

                    # Now extract the variables using self.settings instead of a local 'config'
                    self.game_exe_path = self.settings.get("game_path", "")
                    self.modio_terms_agreed = self.settings.get("modio_terms_agreed", False)
                    self.modio_token_expires = self.settings.get("modio_token_expires", 0)
                    mode = self.settings.get("mod_location_mode", "Documents")
                    self.mod_loc_mode.set(mode)
                    self.custom_docs_path = self.settings.get("custom_docs_path", "")
                    _raw = self.settings.get("enable_new_mods", "on")
                    if isinstance(_raw, bool): _raw = "on" if _raw else "off"
                    self.enable_new_mods_var.set(_raw)
                    self.show_reddit_news_var.set(self.settings.get("show_reddit_news", False))
                    self.show_tooltips_var.set(self.settings.get("show_tooltips", True))
                    self.current_profile_name = self.settings.get("current_profile_name", "Default")
                    # Restore use_mod_browser so check_first_run doesn't re-show the prompt
                    umb = self.settings.get("use_mod_browser")
                    if umb is not None:
                        self.use_mod_browser = umb

                    self.update_mod_path_from_mode()
                    return True
            except Exception as e:
                print(f"Failed to load settings: {e}")

        # Reset to empty dict if file missing or corrupt
        self.settings = {}
        return False

    # ==========================================
    # --- HOVER AND NOTIFICATIONS ---
    # ==========================================
    def _bind_hover(self, widget, normal_bg, hover_bg="#253b59"):
        """Ensures the card and ALL internal labels/frames switch colors simultaneously to prevent 'fading' or flickering."""
        # Collect the card and all its children (labels, frames, etc.)
        all_elements = [widget]
        for child in widget.winfo_children():
            all_elements.append(child)
            # If there's a nested frame (like txt_frame), get its children too
            if isinstance(child, tk.Frame):
                all_elements.extend(child.winfo_children())

        def on_enter(e):
            for el in all_elements:
                try:
                    el.config(bg=hover_bg)
                except: pass

        def on_leave(e):
            for el in all_elements:
                try:
                    el.config(bg=normal_bg)
                except: pass

        # Bind the events to every single element in the group. This way, moving from the card bg to the text doesn't trigger a 'Leave'
        for el in all_elements:
            el.bind("<Enter>", on_enter)
            el.bind("<Leave>", on_leave)

    def _imperial_alert(self, title, message, is_error=False, scrollable=False):
        """A themed replacement for standard messageboxes.

        scrollable=True replaces the fixed Label with a scrollable read-only Text widget - useful when the message may contain many lines.
        """
        alert_win = tk.Toplevel(self)
        alert_win.title(title)

        # Taller window when scrollable so the list has room to breathe
        win_w, win_h = (675, 460) if scrollable else (675, 330)
        alert_win.geometry(f"{win_w}x{win_h}")

        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        alert_win.geometry(f"+{x}+{y}")

        alert_win.configure(bg=BG_MAIN)
        alert_win.transient(self)
        alert_win.grab_set()

        header_color = "#e74c3c" if is_error else FG_GOLD
        btn_color = "#c0392b" if is_error else "#07C1D8"
        btn_color_hover = "#db4332" if is_error else "#09E2FF"

        tk.Label(alert_win, text=title.upper(), font=FONT_TITLE, bg=BG_MAIN, fg=header_color).pack(pady=(20, 10))

        btn_okay = tk.Button(alert_win, text=T(1999101064), font=FONT_UI_BOLD, bg=btn_color, activebackground=btn_color_hover, fg=FG_MAIN, padx=20, cursor="hand2", relief="raised", command=alert_win.destroy)
        btn_okay.pack(side="bottom", pady=(0, 20))
        self._bind_hover(btn_okay, btn_color, btn_color_hover)
        alert_win.bind("<Return>", lambda e: alert_win.destroy())
        alert_win.bind("<space>", lambda e: alert_win.destroy())

        if scrollable:
            txt_frame = tk.Frame(alert_win, bg=BG_MAIN)
            txt_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))

            scrollbar = ttk.Scrollbar(txt_frame, orient="vertical")
            scrollbar.pack(side="right", fill="y")

            txt = tk.Text(
                txt_frame, font=FONT_BODY, bg=BG_SECTION, fg=FG_MAIN,
                relief="flat", wrap="word", state="normal",
                yscrollcommand=scrollbar.set, cursor="arrow",
                highlightthickness=0, padx=12, pady=8
            )
            txt.insert("end", message)
            txt.config(state="disabled")
            txt.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=txt.yview)
        else:
            msg_lbl = tk.Label(alert_win, text=message, font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, wraplength=630, justify="center")
            msg_lbl.pack(pady=10, expand=True)

        self.wait_window(alert_win)

    def _imperial_question(self, title, message):
        """A themed replacement for askyesno."""
        quest_win = tk.Toplevel(self)
        quest_win.title(title)

        # Define size
        win_w, win_h = 675, 460
        quest_win.geometry(f"{win_w}x{win_h}")

        # Centering logic
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        quest_win.geometry(f"+{x}+{y}")

        quest_win.configure(bg=BG_MAIN)
        quest_win.transient(self)
        quest_win.grab_set()

        tk.Label(quest_win, text=title.upper(), font=FONT_TITLE, bg=BG_MAIN, fg=FG_GOLD).pack(pady=(25, 15))

        tk.Label(quest_win, text=message, font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, wraplength=420, justify="center").pack(pady=10, expand=True)

        btn_frame = tk.Frame(quest_win, bg=BG_MAIN)
        btn_frame.pack(pady=25)

        result = {"ans": False}

        def _select(val):
            result["ans"] = val
            quest_win.destroy()

        # Themed "Yes" and "No" buttons
        btn_yes = tk.Button(btn_frame, text=T(1999101065), font=FONT_UI_BOLD, bg="#2ecc71", activebackground="#36e780", fg="#000", width=12, cursor="hand2", command=lambda: _select(True))
        btn_yes.pack(side="left", padx=10)
        self._bind_hover(btn_yes, "#2ecc71", "#36e780")

        btn_no = tk.Button(btn_frame, text=T(1999101066), font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, activebackground=BG_HOVER, width=12, cursor="hand2", command=lambda: _select(False))
        btn_no.pack(side="left", padx=10)
        self._bind_hover(btn_no, BG_SECTION, BG_HOVER)

        quest_win.bind("<Return>",  lambda e: _select(True))
        quest_win.bind("<Escape>",  lambda e: _select(False))
        self.wait_window(quest_win)
        return result["ans"]

    # ==========================================
    # --- MOD.IO INTEGRATION ---
    # ==========================================
    def _add_modio_logo(self, parent, bg=BG_MAIN, max_height=46):
        """Packs the mod.io logo above the first header in a modio-branded popup."""
        logo_path = resource_path("data/ui/4k/base/icon_content/modio/icon_2d_modio_logo_blue_white.png")
        if not os.path.exists(logo_path):
            return
        try:
            img = Image.open(logo_path).convert("RGBA")
            orig_w, orig_h = img.size
            ratio  = orig_w / orig_h
            new_h  = max_height
            new_w  = int(new_h * ratio)
            img    = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            photo  = ImageTk.PhotoImage(img)
            lbl    = tk.Label(parent, image=photo, bg=bg)
            lbl.image = photo
            lbl.pack(pady=(18, 4))
        except Exception as e:
            print(f"[Logo] Failed to load mod.io logo: {e}")

    def _prompt_api_key_setup(self):
        """Creates a styled modal for the user to input their Mod.io API Key."""
        api_win = tk.Toplevel(self)
        api_win.title(T(1999101067))
        api_win.geometry("600x575")

        # Define size
        win_w, win_h = 600, 575
        api_win.geometry(f"{win_w}x{win_h}")

        # 2. Centering logic
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        api_win.geometry(f"+{x}+{y}")

        api_win.configure(bg=BG_MAIN)
        api_win.transient(self)
        api_win.grab_set()

        # Header
        self._add_modio_logo(api_win, bg=BG_MAIN)
        tk.Label(api_win, text=T(1999101068), font=FONT_TITLE, bg=BG_MAIN, fg=FG_GOLD).pack(pady=(0, 10))

        instructions = T(1999101430)
        tk.Label(api_win, text=instructions, font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, justify="left", wraplength=500).pack(pady=10)

        # Link to Mod.io
        link_lbl = tk.Label(api_win, text=T(1999101069), font=FONT_BOLD_SMALL, bg="#07C1D8", fg=FG_MAIN, cursor="hand2", relief="raised")
        link_lbl.pack(pady=5)
        link_lbl.bind("<Button-1>", lambda e: webbrowser.open("https://mod.io/me/access"))
        self._bind_hover(link_lbl, "#07C1D8", "#09E2FF")

        # Input Area
        entry_frame = tk.Frame(api_win, bg=BG_SECTION, bd=1, relief="solid", padx=20, pady=20)
        entry_frame.pack(fill="x", padx=40, pady=20)

        tk.Label(entry_frame, text=T(1999101056), font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN).pack(side="left")

        api_var = tk.StringVar()
        api_entry = tk.Entry(entry_frame, textvariable=api_var, font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, show="*", width=35)
        api_entry.pack(side="left", padx=10)

        # Save Action
        def _save_key():
            key = api_var.get().strip()
            if not key:
                self._imperial_alert(T(1999101189), T(1999101236), is_error=True)
                return

            self.settings["modio_api_key"] = key
            self.modio_api_key = key
            self.save_settings()
            self.refresh_sidebar_state()

            api_win.destroy()
            self._imperial_alert(T(1999101201), T(1999101237))
            self._prompt_modio_auth()

        btn_authorize = tk.Button(api_win, text=T(1999101070), font=FONT_UI_BOLD, bg="#2ecc71", fg="#000", padx=20, cursor="hand2", relief="raised", command=_save_key)
        btn_authorize.pack(pady=10)
        self._bind_hover(btn_authorize, "#2ecc71", "#36e780")

    def _handle_modio_401(self):
        """Called when any mod.io API returns 401 — token has expired or been revoked."""
        self.modio_token = ""
        self.settings["modio_token"] = ""
        self.save_settings()
        self.after(0, lambda: [
            self.refresh_sidebar_state(),
            self._imperial_alert(T(1999101188), T(1999101238), is_error=True),
            self.switch_tab("Settings")
        ])

    def _prompt_modio_auth(self):
        """Fetches latest agreements from mod.io and shows the consent dialog."""
        try:
            # 1. Fetch the latest terms from mod.io
            url = f"{MODIO_BASE_URL}/authenticate/terms"
            headers = {
                'X-Modio-Platform': 'Windows', # Tailors text for PC
                'Accept-Language': 'en'        # Can be dynamic based on OS language
            }
            params = {'api_key': self.modio_api_key}
            res = requests.get(url, headers=headers, params=params, timeout=5)

            if res.status_code == 200:
                terms_data = res.json()
                self._show_consent_dialog(terms_data)
            else:
                # Fallback if API is down
                msg = T(1999101300)
                confirm = self._imperial_question(T(1999101285), msg)

                if confirm:
                    self._run_modio_email_flow()
        except Exception as e:
            print(f"Agreement fetch failed: {e}")

    def _show_consent_dialog(self, data):
        """Creates a compliant mod.io agreement window with clickable legal links."""
        self.consent_win = tk.Toplevel(self)
        self.consent_win.title(T(1999101071))

        # Define size
        win_w, win_h = 550, 600
        self.consent_win.geometry(f"{win_w}x{win_h}")

        # Add the centering logic
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        self.consent_win.geometry(f"+{x}+{y}")

        self.consent_win.configure(bg=BG_SECTION)
        self.consent_win.transient(self)
        self.consent_win.grab_set()

        # Logic for Declining/Closing
        def on_decline():
            self.consent_win.destroy()
            self.modio_declined = True
            self.save_settings()
            print("Mod.io integration declined.")

        # Intercept the "X" button in the corner
        self.consent_win.protocol("WM_DELETE_WINDOW", on_decline)

        # Center the window
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (550 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (600 // 2)
        self.consent_win.geometry(f"+{x}+{y}")

        # Agreement Text (from API)
        self._add_modio_logo(self.consent_win, bg=BG_SECTION)
        msg_text = data.get('message', T(1999101431))
        tk.Label(self.consent_win, text=msg_text, font=FONT_BODY, bg=BG_SECTION, fg=FG_MAIN, wraplength=450, justify="center").pack(padx=20, pady=20)

        # Viewer Buttons
        links_frame = tk.Frame(self.consent_win, bg=BG_SECTION)
        links_frame.pack(pady=10)

        btn_view_tou = tk.Button(links_frame, text=T(1999101072), font=FONT_XSMALL, bg=BG_MAIN, fg="#07C1D8", relief="raised", cursor="hand2", command=lambda: self._show_legal_text_window(1))
        btn_view_tou.pack(side="left", padx=15)
        self._bind_hover(btn_view_tou, BG_MAIN, BG_HOVER)

        btn_view_pp = tk.Button(links_frame, text=T(1999101073), font=FONT_XSMALL, bg=BG_MAIN, fg="#07C1D8", relief="raised", cursor="hand2", command=lambda: self._show_legal_text_window(2))
        btn_view_pp.pack(side="left", padx=15)
        self._bind_hover(btn_view_pp, BG_MAIN, BG_HOVER)

        # Footer Buttons
        btn_frame = tk.Frame(self.consent_win, bg=BG_SECTION)
        btn_frame.pack(side="bottom", fill="x", pady=30)

        def on_agree():
            self.consent_win.destroy()
            self.modio_terms_agreed = True
            self.settings["modio_terms_agreed"] = True
            self.save_settings()
            self._run_modio_email_flow(terms_agreed=True)

        def on_decline():
            # 1. Update the live attribute
            self.modio_declined = True

            # 2. Update the settings dictionary
            if not hasattr(self, 'settings'):
                self.settings = {}
            self.settings["modio_declined"] = True

            # 3. Explicitly save to disk
            self.save_settings()

            # 4. Close window
            self.consent_win.destroy()

        self.consent_win.protocol("WM_DELETE_WINDOW", on_decline)

        agree_btn = tk.Button(btn_frame, text=T(1999101074), font=FONT_UI_BOLD, bg="#2ecc71", fg="#000000", relief="raised", width=12, cursor="hand2", command=on_agree)
        agree_btn.pack(side="right", padx=40)
        self._bind_hover(agree_btn, "#2ecc71", "#36e780")

        no_btn = tk.Button(btn_frame, text=T(1999101075), font=FONT_UI_BOLD, bg=BG_MAIN, fg=FG_MAIN, relief="raised", width=12, cursor="hand2", command=on_decline)
        no_btn.pack(side="left", padx=40)
        self._bind_hover(no_btn, BG_MAIN, BG_HOVER)

    def _show_legal_text_window(self, agreement_type):
        """Fetches and displays full legal text internally with proper formatting and scrolling."""

        # Prevent duplicate windows
        win_id = f"legal_win_{agreement_type}"
        if hasattr(self, win_id) and getattr(self, win_id).winfo_exists():
            getattr(self, win_id).lift()
            return

        view_win = tk.Toplevel(self)
        setattr(self, win_id, view_win) # Track this window

        title = "Terms of Use" if agreement_type == 1 else "Privacy Policy"
        view_win.title(title)

        # Define size
        win_w, win_h = 650, 750
        view_win.geometry(f"{win_w}x{win_h}")

        # Centering logic
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        view_win.geometry(f"+{x}+{y}")

        view_win.configure(bg=BG_MAIN)

        view_win.grab_set()

        container = tk.Frame(view_win, bg=BG_MAIN)
        container.pack(expand=True, fill="both", padx=10, pady=10)

        scrollbar = tk.Scrollbar(container, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        txt_area = tk.Text(container, wrap=tk.WORD, bg=BG_MAIN, fg=FG_MAIN, font=("Marcellus", 11), padx=20, pady=20, relief="flat", yscrollcommand=scrollbar.set)
        txt_area.pack(side="left", expand=True, fill="both")
        scrollbar.config(command=txt_area.yview)

        txt_area.insert(tk.END, T(1999101427) + "\n")
        txt_area.config(state=tk.DISABLED)

        def fetch():
            try:
                url = f"{MODIO_BASE_URL}/agreements/types/{agreement_type}/current"
                params = {'api_key': self.modio_api_key}
                res = requests.get(url, params=params, timeout=10)

                if res.status_code == 200:
                    data = res.json()
                    raw_html = data.get('description', "No content available.")

                    # 1. Replace List Items with dashes so they aren't lost
                    text = raw_html.replace('<li>', '\n- ').replace('</li>', '')
                    # 2. Replace Paragraphs/Headers with double newlines
                    text = re.sub(r'<(p|h1|h2|h3|br|hr)>', '\n\n', text)
                    # 3. Strip all remaining tags
                    clean_text = re.sub(r'<[^<]+?>', '', text).strip()
                    # 4. Fix excessive whitespace
                    clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)

                    self.after(0, lambda: self._update_legal_ui(txt_area, clean_text))
                else:
                    self.after(0, lambda: self._update_legal_ui(txt_area, T(1999101447)))
            except Exception as e:
                self.after(0, lambda: self._update_legal_ui(txt_area, T(1999101448, e)))

        def on_close_viewer():
            view_win.grab_release()
            # Clear the reference so the Duplicate check works next time
            if hasattr(self, win_id):
                delattr(self, win_id)
            view_win.destroy()
            if hasattr(self, 'consent_win') and self.consent_win.winfo_exists():
                self.consent_win.grab_set()

        view_win.protocol("WM_DELETE_WINDOW", on_close_viewer)

        threading.Thread(target=fetch, daemon=True).start()

    def _update_legal_ui(self, widget, text):
        """Thread-safe update for the legal text area."""
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.config(state=tk.DISABLED)

    def _run_modio_email_flow(self, terms_agreed=False):
        """Handles the 2-step Mod.io Email OAuth process."""

        def _get_email():
            # Create Custom Email Modal
            email_win = tk.Toplevel(self)
            email_win.title(T(1999101076))

            # Define size
            win_w, win_h = 500, 400
            email_win.geometry(f"{win_w}x{win_h}")

            # Add the centering logic
            self.update_idletasks()
            x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
            y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
            email_win.geometry(f"+{x}+{y}")

            email_win.configure(bg=BG_MAIN)
            email_win.transient(self)
            email_win.grab_set()

            self._add_modio_logo(email_win, bg=BG_MAIN)
            tk.Label(email_win, text=T(1999101077), font=FONT_TITLE, bg=BG_MAIN, fg=FG_GOLD).pack(pady=(30, 10))
            tk.Label(email_win, text=T(1999101078), font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, wraplength=400).pack(pady=10)

            email_var = tk.StringVar()
            entry = tk.Entry(email_win, textvariable=email_var, font=FONT_BODY, bg=BG_SECTION, fg=FG_MAIN, insertbackground=FG_MAIN, relief="flat", width=35)
            entry.pack(pady=10, ipady=5)
            entry.focus_set()

            result = {"email": None}

            def _submit():
                result["email"] = email_var.get().strip()
                email_win.destroy()

            btn_email = tk.Button(email_win, text=T(1999101079), font=FONT_UI_BOLD, bg="#07C1D8", fg=FG_MAIN, padx=20, cursor="hand2", command=_submit)
            btn_email.pack(pady=20)
            self._bind_hover(btn_email, "#07C1D8", "#09E2FF")
            self._attach_tooltip(btn_email, T(1999101266))

            self.wait_window(email_win)
            return result["email"]

        def _get_code(email):
            # Create Custom Code Modal
            code_win = tk.Toplevel(self)
            code_win.title(T(1999101080))
            code_win.geometry("500x360")

            # Define size
            win_w, win_h = 500, 400
            code_win.geometry(f"{win_w}x{win_h}")

            # Add the centering logic
            self.update_idletasks()
            x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
            y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
            code_win.geometry(f"+{x}+{y}")

            code_win.configure(bg=BG_MAIN)
            code_win.transient(self)
            code_win.grab_set()

            self._add_modio_logo(code_win, bg=BG_MAIN)
            tk.Label(code_win, text=T(1999101081), font=FONT_TITLE, bg=BG_MAIN, fg="#e74c3c").pack(pady=(30, 10))
            tk.Label(code_win, text=T(1999101374, email), font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, justify="center").pack(pady=10)

            code_var = tk.StringVar()
            # Style the code entry specifically (larger letters/spacing)
            entry = tk.Entry(code_win, textvariable=code_var, font=("Courier New", 20, "bold"), bg=BG_SECTION, fg="#2ecc71", insertbackground=FG_MAIN, relief="flat", width=10, justify="center")
            entry.pack(pady=10, ipady=5)
            entry.focus_set()

            result = {"code": None}

            def _submit():
                result["code"] = code_var.get().strip()
                code_win.destroy()

            credentials_btn = tk.Button(code_win, text=T(1999101082), font=FONT_UI_BOLD, bg="#2ecc71", fg="#000", padx=20, cursor="hand2", command=_submit)
            credentials_btn.pack(pady=20)
            self._bind_hover(credentials_btn, "#2ecc71", "#36e780")

            self.wait_window(code_win)
            return result["code"]

        # --- Execution Flow ---
        email = _get_email()
        if not email: return

        try:
            url_req = f"{MODIO_BASE_URL}/oauth/emailrequest"
            data_req = {'api_key': self.modio_api_key, 'email': email}
            res_req = requests.post(url_req, data=data_req, headers={'Accept': 'application/json'})

            if res_req.status_code != 200:
                err_msg = res_req.json().get('error', {}).get('message', 'Unknown Identification Error')
                self._imperial_alert(T(1999101196), err_msg, is_error=True)
                return

            code = _get_code(email)
            if not code: return

            url_exch = f"{MODIO_BASE_URL}/oauth/emailexchange"
            data_exch = {
                'api_key': self.modio_api_key,
                'security_code': code,
                'terms_agreed': 'true' if terms_agreed else 'false',
            }
            res_exch = requests.post(url_exch, data=data_exch, headers={'Accept': 'application/json'})

            if res_exch.status_code == 200:
                token_data = res_exch.json()
                self.modio_token = token_data['access_token']
                # Store the server-provided expiry timestamp directly
                self.modio_token_expires = token_data.get('date_expires', 0)
                self.settings["modio_token"] = self.modio_token
                self.settings["modio_token_expires"] = self.modio_token_expires
                self.save_settings()
                self.switch_tab("Settings")
                self.refresh_sidebar_state()
                self._session_news = []
                self._imperial_alert(T(1999101202), T(1999101239))
            elif res_exch.status_code == 403:
                err_ref = res_exch.json().get('error', {}).get('error_ref', 0)
                if err_ref == 11074:
                    # Terms have been updated — must re-collect agreement
                    self.modio_terms_agreed = False
                    self.settings["modio_terms_agreed"] = False
                    self.save_settings()
                    self._imperial_alert( T(1999101203), T(1999101240), is_error=True)
                    self._prompt_modio_auth()
                else:
                    self._imperial_alert(T(1999101196), res_exch.json().get('error', {}).get('message', 'Unknown error.'), is_error=True)
            else:
                self._imperial_alert(T(1999101204), T(1999101241), is_error=True)
        except Exception as e:
            self._imperial_alert(T(1999101286), T(1999101396, e), is_error=True)

    def _disconnect_modio(self):
        """Asks for confirmation, then clears the stored mod.io token and expiry, saves settings and resets the mod browser and news session caches."""
        msg = T(1999101301)
        confirm = self._imperial_question(T(1999101287), msg)

        if confirm:
            # Clear tokens
            self.modio_token = ""
            self.modio_token_expires = 0
            self.settings["modio_token"] = ""
            self.settings["modio_token_expires"] = 0

            # Save and Update UI
            self.save_settings()
            self._session_news = []
            self.refresh_sidebar_state() # Greys out the button
            self.render_settings_tab() # Refreshes the settings view
            self._imperial_alert(T(1999101205), T(1999101242))

    def _check_modio_response(self, response):
        """Checks for the specific error that terms need re-accepting."""
        if response.status_code == 403:
            err_data = response.json().get('error', {})
            if err_data.get('error_ref') == 11074:
                self._imperial_alert(T(1999101203), T(1999101243))
                self._run_modio_email_flow() # Redirect to the flow
                return False
        return True

    # ==========================================
    # --- MOD BROWSER TAB ---
    # ==========================================
    def render_mod_browser_tab(self):
        """Builds the Mod.io Browser interface with Search and Sort."""
        if not getattr(self, '_browser_from_news', False):
            self._browser_exact_id = None
        self._browser_from_news = False

        for widget in self.main_content.winfo_children():
            widget.destroy()

        # --- HEADER ---
        header_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        header_frame.pack(fill="x", padx=20, pady=20)
        tk.Label(header_frame, text=T(1999101083), font=FONT_TITLE, bg=BG_MAIN, fg=FG_MAIN).pack(side="left")

        # New Stats Label (e.g., "Showing 50 of 412")
        self.browser_stats_lbl = tk.Label(header_frame, text="", font=FONT_SMALL, bg=BG_MAIN, fg=FG_DIM)
        self.browser_stats_lbl.pack(side="left", padx=15, pady=(5, 0))

        # Search & Sort Container (Right Aligned)
        controls_frame = tk.Frame(header_frame, bg=BG_MAIN)
        controls_frame.pack(side="right")

        # 1. Search Entry with Clear Button
        search_bg = tk.Frame(controls_frame, bg=BG_SECTION, padx=5, pady=2)
        search_bg.pack(side="left", padx=10)

        self.browser_search_var = tk.StringVar()
        search_entry = tk.Entry(search_bg, textvariable=self.browser_search_var, font=FONT_SMALL, bg=BG_SECTION, fg=FG_MAIN, insertbackground=FG_MAIN, width=20, relief="flat")
        search_entry.pack(side="left")
        search_entry.bind("<Return>", lambda e: [setattr(self, '_browser_exact_id', None), self.refresh_browser()])

        search_btn = tk.Button(search_bg, text="✕", font=FONT_XSMALL, bg=BG_SECTION, fg=FG_DIM, relief="flat", cursor="hand2", command=lambda: [setattr(self, 'browser_tag_filter', ''), self.browser_tag_var.set("All Tags"), self._clear_search()])
        search_btn.pack(side="left")
        self._bind_hover(search_btn, BG_SECTION, BG_HOVER)

        # Tag filter state (persists across refreshes within the session)
        if not hasattr(self, 'browser_tag_var'):
            self.browser_tag_var = tk.StringVar(value="All Tags")
        if not hasattr(self, 'browser_tag_filter'):
            self.browser_tag_filter = ""

        # 2. Sort Dropdown
        self.browser_sort_options = {
            T(1999101432): "-downloads_total",
            T(1999101433): "name",
            T(1999101434): "-date_live",
            T(1999101435): "-ratings_weighted_aggregate",
            T(1999101436): "submitted_by"
        }
        self.browser_sort_var = tk.StringVar(value=T(1999101432))
        sort_menu = tk.OptionMenu(controls_frame, self.browser_sort_var, *self.browser_sort_options.keys(), command=lambda _: [setattr(self, '_browser_exact_id', None), self.refresh_browser()])
        sort_menu.config(font=FONT_XSMALL, bg=BG_SECTION, fg=FG_MAIN, highlightthickness=0, width=15)
        sort_menu["menu"].config(bg=BG_SECTION, fg=FG_MAIN)
        sort_menu.pack(side="left")

        # 2b. Tag filter dropdown (populated async from mod.io)
        self.browser_tag_var = tk.StringVar(value="All Tags")
        self.browser_tag_filter = ""
        self.browser_tag_menu = tk.OptionMenu(controls_frame, self.browser_tag_var, "All Tags")
        self.browser_tag_menu.config(font=FONT_XSMALL, bg=BG_SECTION, fg=FG_MAIN, highlightthickness=0, width=14)
        self.browser_tag_menu["menu"].config(bg=BG_SECTION, fg=FG_MAIN)
        self.browser_tag_menu.pack(side="left", padx=(4, 0))

        def _on_tag_selected(*_):
            selected = self.browser_tag_var.get()
            self.browser_tag_filter = "" if selected == "All Tags" else selected
            setattr(self, '_browser_exact_id', None)
            self.refresh_browser()

        self.browser_tag_var.trace_add("write", _on_tag_selected)

        def _populate_browser_tags(tags):
            menu = self.browser_tag_menu["menu"]
            menu.delete(0, "end")
            menu.add_command(label="All Tags", command=lambda: self.browser_tag_var.set("All Tags"))
            for tag in tags:
                menu.add_command(label=tag, command=lambda t=tag: self.browser_tag_var.set(t))

        if self.modio_token:
            self._fetch_game_tags(_populate_browser_tags)

        # 3. Subscribed-only filter toggle
        self.browser_subscribed_only = tk.BooleanVar(value=False)

        def _toggle_subscribed_filter():
            self._browser_exact_id = None
            is_on = self.browser_subscribed_only.get()

            if is_on:
                # Active State: Gold
                self.btn_subscribed_filter.config(bg=FG_GOLD, fg="#000000", image=_ico_subf_black)
                self._bind_hover(self.btn_subscribed_filter, FG_GOLD, "#ffd013")
            else:
                # Inactive State: Return to standard UI colors
                self.btn_subscribed_filter.config(bg=BG_SECTION, fg=FG_MAIN, image=_ico_subf)
                self._bind_hover(self.btn_subscribed_filter, BG_SECTION, BG_HOVER)

            self.refresh_browser()

        _ico_subf = load_icon("subscribed_filter", (14, 14))
        _ico_subf_black = load_icon("subscribed_state", (14, 14))
        self.btn_subscribed_filter = tk.Button(controls_frame, text=T(1999101166), font=FONT_XSMALL, bg=BG_SECTION, fg=FG_MAIN, relief="flat", cursor="hand2", padx=8, image=_ico_subf, compound="left" if _ico_subf else "none", command=lambda: [self.browser_subscribed_only.set(not self.browser_subscribed_only.get()), _toggle_subscribed_filter()])
        if _ico_subf: self.btn_subscribed_filter.image = _ico_subf
        self.btn_subscribed_filter.pack(side="left", padx=(8, 0))
        self._bind_hover(self.btn_subscribed_filter, BG_SECTION, BG_HOVER)
        self._attach_tooltip(self.btn_subscribed_filter, T(1999101267))

        if not self.modio_token:
            tk.Label(self.main_content, text=T(1999101085), font=FONT_BODY, bg=BG_MAIN, fg=FG_DIM).pack(pady=50)
            return

        # --- SCROLLABLE AREA ---
        self.browser_canvas = tk.Canvas(self.main_content, bg=BG_MAIN, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.main_content, orient="vertical", command=self.browser_canvas.yview)

        self.browser_canvas.configure(yscrollcommand=scrollbar.set)
        self.browser_canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")

        # Virtual scroll state
        self._all_browser_mods = []
        self._virt_rows = {}   # {row_idx: (tk.Frame, canvas_window_id)}
        self._browser_total_count = 0
        self._load_more_btn = None
        self._load_more_btn_win = None

        # Resize event: Update the width of all visible rows directly on the canvas
        def _on_canvas_resize(e):
            for r, (frame, cw_id) in self._virt_rows.items():
                self.browser_canvas.itemconfig(cw_id, width=e.width)
            if getattr(self, '_load_more_btn_win', None):
                self.browser_canvas.itemconfig(self._load_more_btn_win, width=e.width)
            self._render_visible_browser_rows()

        self.browser_canvas.bind("<Configure>", _on_canvas_resize)

        # Re-render visible rows whenever the user scrolls
        def _on_vscroll(*args):
            scrollbar.set(*args)
            self.after_idle(self._render_visible_browser_rows)
        self.browser_canvas.configure(yscrollcommand=_on_vscroll)

        # Mousewheel binding
        self.browser_canvas.bind_all("<MouseWheel>", lambda e: self.browser_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.browser_canvas.bind("<Destroy>", lambda e: self.browser_canvas.unbind_all("<MouseWheel>"))

        # Sync external subscriptions in background before rendering tiles
        threading.Thread(target=self._sync_subscriptions_from_modio, daemon=True).start()
        self.refresh_browser()

    def _fetch_game_tags(self, callback):
        """Fetches the tag option groups for Anno 117 from mod.io and calls callback(tag_list) on the main thread. tag_list is a flat sorted list of tag name strings. Results are cached for the session."""
        if hasattr(self, '_cached_game_tags'):
            self.after(0, lambda: callback(self._cached_game_tags))
            return

        def _worker():
            try:
                headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
                res = requests.get(
                    f"{MODIO_BASE_URL}/games/11358/tags", headers=headers, timeout=10)
                tags = []
                if res.status_code == 200:
                    for group in res.json().get('data', []):
                        tags.extend(group.get('tags', []))
                    tags = sorted(set(tags))
                self._cached_game_tags = tags
                self.after(0, lambda t=tags: callback(t))
            except Exception:
                self.after(0, lambda: callback([]))

        threading.Thread(target=_worker, daemon=True).start()

    def _clear_search(self):
        """Resets search, sort and subscribed filter to default."""
        self.browser_search_var.set("")
        self.browser_sort_var.set(T(1999101432))
        if hasattr(self, 'browser_subscribed_only'):
            self.browser_subscribed_only.set(False)
        if hasattr(self, 'btn_subscribed_filter'):
            self.btn_subscribed_filter.config(bg=BG_SECTION, fg=FG_MAIN)

        self._browser_exact_id = None
        self.refresh_browser()

    def refresh_browser(self):
        """Resets offset and clears view for a fresh search."""
        self.browser_offset = 0
        self._all_browser_mods = []
        self._browser_total_count = 0

        # Clear virtual rows
        if hasattr(self, '_virt_rows'):
            for r, (frame, cw_id) in self._virt_rows.items():
                try: frame.destroy()
                except tk.TclError: pass
        self._virt_rows = {}

        if getattr(self, "_load_more_btn", None):
            try: self._load_more_btn.destroy()
            except tk.TclError: pass
            self._load_more_btn = None
            self._load_more_btn_win = None

        if hasattr(self, 'browser_stats_lbl'):
            self.browser_stats_lbl.config(text=T(1999101086))

        if hasattr(self, 'browser_canvas'):
            self.browser_canvas.delete("all")
            self.browser_canvas.yview_moveto(0)

            # Center the loading label dynamically on the Canvas
            c_width = self.browser_canvas.winfo_width()
            x_pos = c_width // 2 if c_width > 1 else 400

            loading_lbl = tk.Label(self.browser_canvas, text=T(1999101087), font=FONT_BODY, bg=BG_MAIN, fg=FG_DIM)
            self.browser_canvas.create_window((x_pos, 40), window=loading_lbl, anchor="n")

        # Start Workers (We now pass self.browser_canvas instead of a frame)
        if hasattr(self, '_browser_exact_id') and self._browser_exact_id:
            threading.Thread(target=self._fetch_exact_mod_worker, args=(self.browser_canvas, loading_lbl, self._browser_exact_id), daemon=True).start()
        elif hasattr(self, 'browser_subscribed_only') and self.browser_subscribed_only.get():
            # Fetch the UI states just like in the 'else' block
            q = self.browser_search_var.get()
            s = self.browser_sort_options.get(self.browser_sort_var.get(), "-downloads_total")
            tag = getattr(self, 'browser_tag_filter', '')
            threading.Thread(
                target=self._fetch_subscribed_mods, args=(self.browser_canvas, loading_lbl, q, s, 0, tag), daemon=True).start()
        else:
            q = self.browser_search_var.get()
            s = self.browser_sort_options.get(self.browser_sort_var.get(), "-downloads_total")
            tag = getattr(self, 'browser_tag_filter', '')
            threading.Thread(target=self._fetch_and_render_mods, args=(self.browser_canvas, loading_lbl, q, s, self.browser_offset, tag), daemon=True).start()

    def _fetch_and_render_mods(self, parent_frame, loading_lbl, query="", sort="-downloads_total", offset=0, tag_filter=""):
        """Background worker that fetches a page of mods from the mod.io API (with optional text query and tag filter), updates the stats label and schedules _build_mod_tiles on the main thread."""
        headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}

        # Increased limit to 51 for a better 'first look'
        url = f"{MODIO_BASE_URL}/games/11358/mods?_sort={sort}&_limit=51&_offset={offset}"
        if query: url += f"&_q={query}"
        if tag_filter: url += f"&tags={requests.utils.quote(tag_filter)}"

        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 401:
                self.after(0, self._handle_modio_401)
                return
            res.raise_for_status()
            data = res.json()
            mods = data.get('data', [])
            total_count = data.get('result_total', 0)

            # We use offset + len(mods) to show the current progress
            current_viewing = offset + len(mods)
            stats_text = T(1999101449, current_viewing, total_count) if mods else T(1999101449, 0, total_count)
            self.after(0, lambda t=stats_text: self.browser_stats_lbl.config(text=t) if hasattr(self, 'browser_stats_lbl') and self.browser_stats_lbl.winfo_exists() else None)

            self.after(0, loading_lbl.destroy)

            if not mods and offset == 0:
                self.after(0, lambda: parent_frame.create_window((parent_frame.winfo_width()//2 or 400, 40), window=tk.Label(parent_frame, text=T(1999101088), bg=BG_MAIN, fg=FG_DIM), anchor="n"))
                return

            self.after(0, lambda: self._build_mod_tiles(parent_frame, mods, total_count)
                       if parent_frame.winfo_exists() else None)
        except Exception as e:
            self.after(0, lambda e=e: loading_lbl.config(text=T(1999101392, e)))

    def _sync_subscriptions_from_modio(self):
        """Fetches the user's current mod.io subscriptions and merges them into _subscription_states. This catches mods subscribed via the mod.io website that the app hasn't seen before, ensuring the Mod Browser shows the correct Subscribed state even for externally-subscribed mods."""
        if not self.modio_token:
            return
        try:
            headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
            url = f"{MODIO_BASE_URL}/me/subscribed?game_id=11358&_limit=100"
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 401:
                self.after(0, self._handle_modio_401)
                return
            if res.status_code != 200:
                return
            api_ids = {str(m.get("id", "")) for m in res.json().get("data", [])}
            added   = [mid for mid in api_ids if mid and not self._subscription_states.get(mid)]
            removed = [mid for mid, v in list(self._subscription_states.items()) if v and mid not in api_ids]
            for mid in added:
                self._subscription_states[mid] = True
            for mid in removed:
                del self._subscription_states[mid]
            if added or removed:
                self._save_subscriptions()
                # Re-render tiles if the browser is still open
                self.after(0, lambda: self.refresh_browser() if self.current_tab == "Mod Browser" else None)
        except Exception as e:
            print(f"[sub sync] {e}")

    def _fetch_subscribed_mods(self, parent_frame, loading_lbl, q="", s="-id", offset=0, tag=""):
        """Fetches mods the authenticated user is subscribed to with sorting and filtering."""
        headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}

        # Base URL
        url = f"{MODIO_BASE_URL}/me/subscribed?game_id=11358&_limit=51&_offset={offset}"

        # Append Search
        if q:
            url += f"&_q={q}"

        # Append Sort
        if s:
            url += f"&_sort={s}"

        # Append Tag Filter (excluding the 'All Tags' default)
        if tag and tag != T(1999101082):
            url += f"&tags={tag}"

        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 401:
                self.after(0, self._handle_modio_401)
                return
            res.raise_for_status()
            data = res.json()
            mods = data.get('data', [])
            total_count = data.get('result_total', 0)

            current_viewing = offset + len(mods)
            stats_text = T(1999101450, current_viewing, total_count)
            self.after(0, lambda t=stats_text: self.browser_stats_lbl.config(text=t))
            self.after(0, loading_lbl.destroy)

            if not mods and offset == 0:
                self.after(0, lambda: parent_frame.create_window((parent_frame.winfo_width()//2 or 400, 40), window=tk.Label(parent_frame, text=T(1999101089), bg=BG_MAIN, fg=FG_DIM), anchor="n"))
                return

            self.after(0, lambda: self._build_mod_tiles(parent_frame, mods, total_count) if parent_frame.winfo_exists() else None)
        except Exception as e:
            self.after(0, lambda e=e: loading_lbl.config(text=T(1999101397, e)))

    def _build_mod_tiles(self, canvas, mods, total_count):
        """Accumulates fetched mod data and updates the virtual scrollregion."""
        try:
            if not canvas.winfo_exists():
                return
        except tk.TclError:
            return

        # Fresh search: wipe slate
        if self.browser_offset == 0:
            for r, (frame, cw_id) in self._virt_rows.items():
                try: frame.destroy()
                except tk.TclError: pass
            self._virt_rows = {}
            self._all_browser_mods = []
            if getattr(self, "_load_more_btn", None):
                try: self._load_more_btn.destroy()
                except tk.TclError: pass
                self._load_more_btn = None
                self._load_more_btn_win = None
            canvas.delete("all")

        # Accumulate data
        self._all_browser_mods.extend(mods)
        self.browser_offset = len(self._all_browser_mods)
        self._browser_total_count = total_count

        n_rows = (len(self._all_browser_mods) + _VR_C - 1) // _VR_C
        frame_h = n_rows * _VR_H + (70 if self.browser_offset < total_count else 0)

        # Update canvas scrollregion immediately! (No master frame height limits anymore)
        canvas.configure(scrollregion=(0, 0, canvas.winfo_width() or 1, frame_h))

        # Place Load More button at the very bottom using Canvas Window
        if getattr(self, "_load_more_btn", None):
            try: self._load_more_btn.destroy()
            except tk.TclError: pass
            self._load_more_btn = None
            if self._load_more_btn_win:
                canvas.delete(self._load_more_btn_win)
                self._load_more_btn_win = None

        if self.browser_offset < total_count:
            more_border = tk.Frame(canvas, bg=BG_SECTION, highlightthickness=1, highlightbackground=BG_SECTION, bd=0)
            _mb = tk.Button(more_border, text=T(1999101095), font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, pady=10, relief="flat", bd=0, cursor="hand2", command=self.load_next_page)
            _mb.pack(fill="both", expand=True)
            self._bind_border_button_hover(_mb, BG_SECTION, "#253b59")

            self._load_more_btn = more_border
            self._load_more_btn_win = canvas.create_window((0, n_rows * _VR_H), window=more_border, anchor="nw", width=canvas.winfo_width(),height=60)

        # Render tiles that are currently visible
        self._render_visible_browser_rows()

    def _render_visible_browser_rows(self):
        """Render only the row frames near the current canvas viewport natively on the Canvas."""
        try:
            if not self.browser_canvas.winfo_exists():
                return
        except tk.TclError:
            return

        n_mods = len(self._all_browser_mods)
        if n_mods == 0:
            return

        n_rows = (n_mods + _VR_C - 1) // _VR_C

        y0_frac, y1_frac = self.browser_canvas.yview()
        sr = self.browser_canvas.cget("scrollregion")
        if not sr:
            total_h = n_rows * _VR_H
        else:
            try:
                total_h = float(sr.split()[3])
            except (IndexError, ValueError):
                total_h = n_rows * _VR_H

        view_top = y0_frac * total_h
        view_bot = y1_frac * total_h

        first_r = max(0, int(view_top / _VR_H) - _VR_BUF)
        last_r  = min(n_rows-1, int(view_bot / _VR_H) + _VR_BUF)

        # Destroy rows outside the buffer zone
        stale = [r for r in list(self._virt_rows) if r < first_r or r > last_r]
        for r in stale:
            frame, cw_id = self._virt_rows[r]
            self.browser_canvas.delete(cw_id)
            try: frame.destroy()
            except tk.TclError: pass
            del self._virt_rows[r]

        # Render new rows
        for r in range(first_r, last_r + 1):
            if r in self._virt_rows:
                continue
            start = r * _VR_C
            row_mods = self._all_browser_mods[start : start + _VR_C]
            if not row_mods:
                continue

            row_frame = tk.Frame(self.browser_canvas, bg=BG_MAIN)
            for c in range(_VR_C):
                row_frame.grid_columnconfigure(c, weight=1, uniform="browser_tile")

            # Place directly on Canvas coordinate map
            cw_id = self.browser_canvas.create_window((0, r * _VR_H), window=row_frame, anchor="nw", width=self.browser_canvas.winfo_width(), height=_VR_H)

            for col_pos, mod in enumerate(row_mods):
                self._build_browser_tile(row_frame, mod, col_pos)

            self._virt_rows[r] = (row_frame, cw_id)

    def _build_browser_tile(self, row_frame, mod, col_pos):
        """Builds one tile widget inside row_frame at the given column position."""
        tile = tk.Frame(row_frame, bg=BG_SECTION, highlightbackground=FG_GOLD, highlightthickness=1, padx=15, pady=15)
        tile.grid(row=0, column=col_pos, padx=10, pady=10, sticky="nsew")
        tile.pack_propagate(False)
        tile.grid_propagate(False)
        tile.config(width=320, height=620)

        # 1. Image
        img_container = tk.Frame(tile, bg=BG_MAIN, width=290, height=163)
        img_container.pack_propagate(False)
        img_container.pack(fill="x", pady=(0, 10))
        img_lbl = tk.Label(img_container, text=T(1999101090), bg=BG_MAIN, fg=FG_DIM, cursor="hand2")
        img_lbl.pack(expand=True, fill="both")

        # BIND CLICK TO IMAGE
        img_lbl.bind("<Button-1>", lambda e, m=mod: self._show_mod_details(m))

        # Endorse button
        mod_id = str(mod.get('id'))
        already_endorsed = self._endorsement_states.get(mod_id, False)
        _ico_end = load_icon("endorsed" if already_endorsed else "endorse", (14, 14))
        endorse_btn = tk.Button(img_container, text=T(1999101167) if already_endorsed else T(1999101092), font=FONT_XSMALL, bg="#2ecc71" if already_endorsed else BG_SECTION, fg=FG_MAIN, disabledforeground=FG_MAIN, relief="flat", cursor="arrow" if already_endorsed else "hand2", padx=6, pady=2, state="disabled" if already_endorsed else "normal", image=_ico_end, compound="left" if _ico_end else "none")
        if _ico_end: endorse_btn.image = _ico_end
        endorse_btn.place(x=4, y=4)
        if not already_endorsed:
            endorse_btn.config(command=lambda mid=mod_id, btn=endorse_btn: self._endorse_mod(mid, btn))
            self._bind_hover(endorse_btn, BG_SECTION, "#39f085")

        # 2. Content
        content_frame = tk.Frame(tile, bg=BG_SECTION)
        content_frame.pack(fill="both", expand=True)

        # Title
        raw_name = html.unescape(mod['name']).upper()
        display_name = (raw_name[:40] + "...") if len(raw_name) > 43 else raw_name
        title_lbl = tk.Label(content_frame, text=display_name, font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, wraplength=280, justify="left", anchor="nw", height=2, cursor="hand2")
        title_lbl.pack(fill="x")

        # BIND CLICK TO MAIN TILE
        for widget in [tile, content_frame, title_lbl]:
            widget.bind("<Button-1>", lambda e, m=mod: self._show_mod_details(m))

        tk.Frame(content_frame, height=1, bg=FG_DIM).pack(fill="x", pady=(5, 5))

        # Meta Header
        meta_header = tk.Frame(content_frame, bg=BG_SECTION)
        meta_header.pack(fill="x", pady=(5, 2))
        author = mod.get('submitted_by', {}).get('username', 'Unknown')
        tk.Label(meta_header, text=author, font=FONT_SMALL, bg=BG_SECTION, fg="#07C1D8").pack(side="left")
        ts = mod.get('date_updated', 0)
        date_v = datetime.fromtimestamp(ts).strftime('%Y-%m-%d') if ts else "???"
        tk.Label(meta_header, text=f"📅 {date_v}", font=FONT_SMALL, bg=BG_SECTION, fg=FG_DIM).pack(side="right")

        # Tags
        tags_list = [t.get('name', '') for t in mod.get('tags', [])]
        raw_t = " | ".join(tags_list) if tags_list else "No Tags"
        display_t = (raw_t[:72] + "...") if len(raw_t) > 75 else raw_t
        tk.Label(content_frame, text=display_t, font=FONT_XSMALL, bg=BG_SECTION, fg="#2ecc71", wraplength=280, justify="left", anchor="nw", height=2).pack(fill="x")

        summary = html.unescape(mod.get('summary', 'No description.'))
        tk.Label(content_frame, text=summary, font=FONT_SMALL, bg=BG_SECTION, fg="#bbbbbb", wraplength=280, justify="left", anchor="nw").pack(fill="both", expand=True, pady=10)

        # Bottom stack: buttons → separator → stats
        btn_frame = tk.Frame(tile, bg=BG_SECTION)
        btn_frame.pack(side="bottom", fill="x", pady=(15, 0))
        tk.Frame(tile, height=1, bg=FG_DIM).pack(side="bottom", fill="x", pady=(5, 5))
        stats_frame = tk.Frame(tile, bg=BG_SECTION)
        stats_frame.pack(side="bottom", fill="x")
        for c in range(3): stats_frame.columnconfigure(c, weight=1)

        # Buttons
        _ico_mvis = load_icon("mod_visit", (14, 14))
        btn_visit = tk.Button(btn_frame, text=T(1999101168), font=FONT_XSMALL, bg=BG_MAIN, fg=FG_MAIN, activebackground=BG_HOVER, relief="flat", cursor="hand2", image=_ico_mvis, compound="left" if _ico_mvis else "none", command=lambda u=mod['profile_url']: webbrowser.open_new_tab(u))
        if _ico_mvis: btn_visit.image = _ico_mvis
        btn_visit.pack(side="left")
        self._bind_hover(btn_visit, BG_MAIN)

        modfile = mod.get('modfile', {})
        dl_url = modfile.get('download', {}).get('binary_url')
        tile_mod_id = str(mod.get('id'))
        is_subscribed = self._subscription_states.get(tile_mod_id, False)

        # Robust check against ACTUAL files on disk (self.mods)
        # 1. Does any physically present mod map to this mod.io ID?
        is_installed_locally = any(
            self._subscription_modio_map.get(m['id']) == tile_mod_id
            for m in self.mods if not m.get('parent_path')
        )

        # 2. Fallback: Does any physically present mod have the exact same normalized name? (Catches manually installed mods that aren't in the subscription map yet)
        if not is_installed_locally:
            import re as _re
            norm_target = _re.sub(r'[^a-z0-9]', '', mod.get('name', '').lower())
            for m in self.mods:
                if m.get('parent_path'): continue
                if _re.sub(r'[^a-z0-9]', '', m.get('name', '').lower()) == norm_target:
                    is_installed_locally = True
                    break

        install_area = tk.Frame(btn_frame, bg=BG_SECTION)
        install_area.pack(side="right")

        if dl_url:
            if is_subscribed:
                # Pass the flag to draw the "!" if it is completely missing from disk
                self._apply_subscribed_state(install_area, dl_url, mod['name'], tile_mod_id, missing_local=not is_installed_locally)
            else:
                # Not subscribed, but installed locally
                if is_installed_locally:
                    _lbl_nosub = tk.Label(install_area, text="!", font=FONT_UI_BOLD, fg=FG_GOLD, bg=BG_SECTION)
                    _lbl_nosub.pack(side="left", padx=(0, 4))
                    self._attach_tooltip(_lbl_nosub, T(1999101477))

                _ico_inst = load_icon("install_mod", (32, 32))
                btn_install = tk.Button(install_area, text=T(1999101169), font=FONT_UI_BOLD, bg="#2ecc71", fg="#000000", activebackground="#39f085", relief="flat", cursor="hand2", image=_ico_inst, compound="left" if _ico_inst else "none", command=lambda u=dl_url, nm=mod['name'], mid=tile_mod_id, ia=install_area: self._download_and_install(u, nm, mid, ia))
                if _ico_inst: btn_install.image = _ico_inst
                btn_install.pack()
                self._bind_hover(btn_install, "#2ecc71", "#39f085")
        else:
            tk.Label(install_area, text=T(1999101170), font=FONT_XSMALL, bg=BG_SECTION, fg=FG_DIM).pack()

        # Stats logic
        st = mod.get('stats', {})
        sz = modfile.get('filesize', 0)
        sz_str = f"{round(sz/1024, 1)} KB" if sz < 102400 else f"{round(sz/(1024*1024), 1)} MB"
        tk.Label(stats_frame, text=f"📥 {st.get('downloads_total', 0):,}", font=FONT_SMALL, bg=BG_SECTION, fg=FG_DIM).grid(row=0, column=0, sticky="w")
        tk.Label(stats_frame, text=f"⭐ {st.get('ratings_display_text', 'N/A')}", font=FONT_SMALL, bg=BG_SECTION, fg=FG_DIM).grid(row=0, column=1, sticky="n")
        tk.Label(stats_frame, text=f"📦 {sz_str}", font=FONT_SMALL, bg=BG_SECTION, fg=FG_DIM).grid(row=0, column=2, sticky="e")

        # Image
        t_url = mod.get('logo', {}).get('thumb_320x180')
        if t_url:
            threading.Thread(target=self._load_mod_image, args=(img_lbl, t_url), daemon=True).start()

    def _endorse_mod(self, mod_id, btn):
        """Submits a positive rating for mod_id via the mod.io API."""
        mod_id = str(mod_id)
        btn.config(state="disabled", text=T(1999101171), cursor="arrow", fg=FG_MAIN)

        def task():
            try:
                url = f"{MODIO_BASE_URL}/games/11358/mods/{mod_id}/ratings"
                headers = {
                    'Authorization': f'Bearer {self.modio_token}',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json'
                }
                res = requests.post(url, headers=headers, data={'rating': 1}, timeout=10)

                if res.status_code in (200, 201):
                    self._endorsement_states[mod_id] = True
                    self._save_endorsements()
                    self.after(0, lambda: self._apply_endorsed_state(btn))
                elif res.status_code == 400:
                    try:
                        err_ref = res.json().get('error', {}).get('error_ref', 0)
                    except Exception:
                        err_ref = 0
                    if err_ref == 15028:  # Already positively rated
                        self._endorsement_states[mod_id] = True
                        self._save_endorsements()
                        self.after(0, lambda: self._apply_endorsed_state(btn))
                    else:
                        self.after(0, lambda: self._endorse_failed(btn, f"mod.io error {err_ref}."))
                else:
                    self.after(0, lambda: self._endorse_failed(btn, f"Server returned {res.status_code}."))
            except Exception as e:
                self.after(0, lambda: self._endorse_failed(btn, str(e)))

        threading.Thread(target=task, daemon=True).start()

    def _apply_endorsed_state(self, btn):
        """Updates an endorse button to the endorsed appearance in full colour. Uses state='normal' with no command so the icon is never stippled grey."""
        try:
            _ico_endorsed = load_icon("endorsed", (14, 14))
            btn.config(
                text=T(1999101167), bg="#2ecc71", fg=FG_MAIN, activebackground="#2ecc71", state="normal", cursor="arrow", relief="flat", image=_ico_endorsed if _ico_endorsed else "", compound="left" if _ico_endorsed else "none", command="")
            btn.image = _ico_endorsed
            btn.unbind("<Enter>")
            btn.unbind("<Leave>")
        except tk.TclError:
            pass

    def _endorse_failed(self, btn, reason):
        """Resets an endorse button to its normal state and shows an error alert after a failedendorsement API call."""
        try:
            btn.config(text=T(1999101173), bg=BG_SECTION, state="normal", cursor="hand2")
        except tk.TclError:
            pass
        self._imperial_alert(T(1999101288), T(1999101398, reason), is_error=True)

    def _load_endorsements(self):
        """Loads persisted endorsement states from appdata. Returns a dict of str(mod_id) → True for every mod endorsed in a previous session."""
        endorse_path = os.path.join(self.appdata_dir, "endorsements.json")
        if os.path.exists(endorse_path):
            try:
                with open(endorse_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load endorsements: {e}")
        return {}

    def _save_endorsements(self):
        """Persists the current endorsement states to appdata."""
        endorse_path = os.path.join(self.appdata_dir, "endorsements.json")
        try:
            with open(endorse_path, 'w', encoding='utf-8') as f:
                json.dump(self._endorsement_states, f)
        except Exception as e:
            print(f"Failed to save endorsements: {e}")

    def _bind_border_button_hover(self, btn, normal_bg, hover_bg):
        """Generic hover binder for buttons wrapped in a border frame."""
        border_frame = btn.master

        def on_enter(e):
            btn.config(bg=hover_bg)
            border_frame.config(bg=hover_bg, highlightbackground=FG_GOLD)

        def on_leave(e):
            btn.config(bg=normal_bg)
            border_frame.config(bg=normal_bg, highlightbackground=normal_bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def load_next_page(self):
        """Fetches the next batch of mods directly on the Canvas."""
        if getattr(self, "_load_more_btn", None):
            try: self._load_more_btn.destroy()
            except tk.TclError: pass
            self._load_more_btn = None
            if getattr(self, "_load_more_btn_win", None):
                self.browser_canvas.delete(self._load_more_btn_win)
                self._load_more_btn_win = None

        n_rows = (len(getattr(self, "_all_browser_mods", [])) + _VR_C - 1) // _VR_C

        load_lbl = tk.Label(self.browser_canvas, text=T(1999101096), bg=BG_MAIN, fg=FG_DIM)
        self.browser_canvas.create_window((self.browser_canvas.winfo_width()//2 or 400, n_rows * _VR_H + 20), window=load_lbl, anchor="n")

        if hasattr(self, 'browser_subscribed_only') and self.browser_subscribed_only.get():
            q = self.browser_search_var.get()
            s = self.browser_sort_options.get(self.browser_sort_var.get(), "-downloads_total")
            tag = getattr(self, 'browser_tag_filter', '')
            threading.Thread(target=self._fetch_subscribed_mods, args=(self.browser_canvas, load_lbl, q, s, self.browser_offset, tag), daemon=True).start()
        else:
            q = self.browser_search_var.get()
            s = self.browser_sort_options.get(self.browser_sort_var.get(), "-downloads_total")
            tag = getattr(self, 'browser_tag_filter', '')
            threading.Thread(target=self._fetch_and_render_mods, args=(self.browser_canvas, load_lbl, q, s, self.browser_offset, tag), daemon=True).start()

    def _load_mod_image(self, label, url):
        """Downloads and scales image without blocking the UI."""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                img = Image.open(io.BytesIO(response.content))
                photo = ImageTk.PhotoImage(img)
                self.after(0, lambda: self._apply_image(label, photo))

        except Exception:
            self.after(0, lambda: label.config(text=T(1999101097)))

    def _apply_image(self, label, photo):
        """Applies the PhotoImage and keeps a reference to avoid garbage collection."""
        try:
            label.config(image=photo, text="", height=0)
            label.image = photo
        except tk.TclError:
            pass

    def _show_mod_details(self, mod):
        """Opens a robust, scrollable detail modal for a specific mod."""
        detail_win = tk.Toplevel(self)
        detail_win.title(f"Imperial Archives: {mod['name']}")

        # Define size
        win_w, win_h = 900, 850
        detail_win.geometry(f"{win_w}x{win_h}")

        # Add the centering logic
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        detail_win.geometry(f"+{x}+{y}")

        detail_win.configure(bg=BG_MAIN)
        detail_win.transient(self)
        detail_win.grab_set()

        # 1. FOOTER
        footer = tk.Frame(detail_win, bg=BG_SECTION, pady=20, padx=40, bd=1, relief="raised")
        footer.pack(side="bottom", fill="x")

        close_btn = tk.Button(footer, text=T(1999101098), font=FONT_UI_BOLD, bg=BG_MAIN, fg=FG_MAIN, padx=20, command=detail_win.destroy, cursor="hand2")
        close_btn.pack(side="left")
        self._bind_hover(close_btn, BG_MAIN, BG_HOVER)

        dl_url = mod.get('modfile', {}).get('download', {}).get('binary_url')
        if dl_url:
            _ico_imod = load_icon("install_mod", (24, 24))
            install_btn = tk.Button(footer, text=T(1999101099), font=FONT_UI_BOLD, bg="#2ecc71", fg="#000000", padx=30, cursor="hand2", image=_ico_imod, compound="left" if _ico_imod else "none", command=lambda: self._download_and_install(dl_url, mod['name'], mod_id=mod.get('id')))
            if _ico_imod: install_btn.image = _ico_imod
            install_btn.pack(side="right")
            self._bind_hover(install_btn, "#2ecc71", "#39f085")

        # 2. SCROLLABLE AREA
        container = tk.Frame(detail_win, bg=BG_MAIN)
        container.pack(side="top", fill="both", expand=True)

        canvas = tk.Canvas(container, bg=BG_MAIN, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_MAIN)

        scroll_frame_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def _on_canvas_configure(event):
            canvas.itemconfig(scroll_frame_id, width=event.width)

        canvas.bind('<Configure>', _on_canvas_configure)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        inner_content = tk.Frame(scroll_frame, bg=BG_MAIN, padx=40, pady=20)
        inner_content.pack(fill="both", expand=True)

        # 3. HEADER & IMAGES
        tk.Label(inner_content, text=mod['name'].upper(), font=FONT_TITLE, bg=BG_MAIN, fg=FG_MAIN, wraplength=750, justify="left").pack(anchor="w")

        meta_text = f"By {mod.get('submitted_by', {}).get('username')} | Updated: {datetime.fromtimestamp(mod.get('date_updated', 0)).strftime('%Y-%m-%d')}"
        tk.Label(inner_content, text=meta_text, font=FONT_BODY, bg=BG_MAIN, fg="#07C1D8").pack(anchor="w", pady=(5, 20))

        img_container = tk.Frame(inner_content, bg=BG_SECTION, bd=1, relief="solid")
        img_container.pack(fill="x", pady=(10, 5))
        self.main_detail_img = tk.Label(img_container, text=T(1999101100), bg=BG_SECTION, fg=FG_DIM, pady=100)
        self.main_detail_img.pack(expand=True, fill="both")

        logo_url = mod.get('logo', {}).get('original')
        if logo_url:
            threading.Thread(target=self._load_large_image, args=(self.main_detail_img, logo_url), daemon=True).start()

        # --- GALLERY THUMBNAILS (3 Columns, 1/2 Size Look) ---
        media = mod.get('media', {})
        images = media.get('images', [])
        if images:
            gal_scroll_frame = tk.Frame(inner_content, bg=BG_MAIN)
            gal_scroll_frame.pack(fill="x", pady=5)
            # Configure 3 columns to expand equally
            gal_scroll_frame.columnconfigure(0, weight=1)
            gal_scroll_frame.columnconfigure(1, weight=1)
            gal_scroll_frame.columnconfigure(2, weight=1)

            for idx, img_obj in enumerate(images):
                # Calculate grid for 3 columns (row = i // 3, col = i % 3)
                row, col = idx // 3, idx % 3
                t_url = img_obj.get('thumb_320x180')
                f_url = img_obj.get('original')

                thumb_frame = tk.Frame(gal_scroll_frame, bg=BG_SECTION, bd=1, relief="solid")
                thumb_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

                # Reduced width/height and pady for smaller look
                # Width/Height here are text lines/characters, not pixels
                t_lbl = tk.Label(thumb_frame, text="⌛", bg=BG_SECTION, fg=FG_DIM, cursor="hand2", pady=10) # Less vertical padding
                t_lbl.pack(expand=True, fill="both")

                # Update main image on click
                t_lbl.bind("<Button-1>", lambda e, url=f_url: threading.Thread(
                    target=self._load_large_image, args=(self.main_detail_img, url), daemon=True).start())

                if t_url:
                    # We pass 'is_gallery=True' to the loader so it uses the smaller scale
                    threading.Thread(target=self._load_gallery_image, args=(t_lbl, t_url, True), daemon=True).start()

        # 4. THE DESCRIPTION (One single pass)
        tk.Frame(inner_content, height=1, bg=FG_DIM).pack(fill="x", pady=20)
        tk.Label(inner_content, text=T(1999101101), font=FONT_UI_BOLD, bg=BG_MAIN, fg=FG_DIM).pack(anchor="w", pady=(0, 10))

        desc_text = tk.Text(inner_content, font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, relief="flat", highlightthickness=0, wrap="word", spacing3=8, cursor="arrow")
        desc_text.pack(fill="x", expand=False)

        desc_text.tag_configure("bold", font=FONT_UI_BOLD)
        desc_text.tag_configure("gap", spacing3=8)

        # INSERT CONTENT ONCE
        raw_html = mod.get('description', 'No description provided.')
        formatted_content = self._format_html_for_tk(raw_html)

        desc_text.config(state="normal")
        for text, tag in formatted_content:
            desc_text.insert("end", text, tag)

        # Recalculate height
        desc_text.update_idletasks()
        line_count = int(desc_text.index('end-1c').split('.')[0])
        desc_text.config(height=line_count + 2, state="disabled") # +2 for safety margin

        # 5. SCROLLING
        def _on_popup_mousewheel(event):
            # Only scroll if the popup window is currently the one under the mouse/active
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass

        detail_win.bind_all("<MouseWheel>", _on_popup_mousewheel)

        # When closing, we ONLY unbind the mousewheel from the global listener but we do it safely so it doesn't kill other windows
        def _cleanup():
            # 1. Kill the global mousewheel redirect
            detail_win.unbind_all("<MouseWheel>")

            # 2. Release the 'grab' (Focus Lock)
            detail_win.grab_release()

            # 3. Destroy the window
            detail_win.destroy()

            # 4. Force the main app to notice the mouse again
            if hasattr(self, 'browser_canvas'):
                self.browser_canvas.focus_set()
                # Re-bind the main window's scroll just in case unbind_all was too aggressive
                self._bind_mousewheel_to_main()

        detail_win.protocol("WM_DELETE_WINDOW", _cleanup)

        # Update your CLOSE button to use this new cleanup function
        for child in footer.winfo_children():
            if "button" in child.winfo_name() and child.cget("text") == "CLOSE":
                child.configure(command=_cleanup)

    def _bind_mousewheel_to_main(self):
        """Re-establishes scrolling for the primary Mod Browser."""
        def _on_main_mousewheel(event):
            if hasattr(self, 'browser_canvas'):
                self.browser_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Bind back to the root or main canvas
        self.bind_all("<MouseWheel>", _on_main_mousewheel)

    def _format_html_for_tk(self, html_str):
        """Converts an HTML-formatted mod description string to plain text with inline [[B]]/[[/B]] bold markers and normalised whitespace, suitable for rendering in the detail popup text widget.
        """
        import html as html_lib
        import re

        text = html_lib.unescape(html_str)

        # 1. Map Headers to Bold
        text = re.sub(r'<(h1|h2|h3|h4|strong|b)>', '[[B]]', text, flags=re.I)
        text = re.sub(r'</(h1|h2|h3|h4|strong|b)>', '[[/B]]\n', text, flags=re.I) # Add newline after headers

        # 2. Cleanup Lists and Breaks
        text = text.replace("<li>", "\n • ").replace("</li>", "")
        text = text.replace("<br>", "\n").replace("<p>", "\n").replace("</p>", "\n")

        # 3. Final Strip
        clean_text = re.sub('<[^<]+?>', '', text)
        # Collapse 3+ newlines into 2
        clean_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', clean_text).strip()

        segments = []
        parts = re.split(r'(\[\[/?B\]\])', clean_text)
        is_bold = False

        for part in parts:
            if part == "[[B]]":
                is_bold = True
            elif part == "[[/B]]":
                is_bold = False
            else:
                if part: segments.append((part, "bold" if is_bold else "gap"))
        return segments

    def _load_large_image(self, label, url):
        """Background worker that downloads and scales the main hero image for a mod detail popup, then calls _apply_large_image on the main thread."""
        try:
            # Show a small loading hint on the label while fetching
            self.after(0, lambda: label.config(text=T(1999101174)))

            res = requests.get(url, timeout=10)
            img = Image.open(io.BytesIO(res.content))

            # Maintain Aspect Ratio based on width
            target_w = 800
            w_percent = (target_w / float(img.size[0]))
            target_h = int((float(img.size[1]) * float(w_percent)))

            # If the image is extremely tall, cap the height
            if target_h > 600:
                target_h = 600
                h_percent = (target_h / float(img.size[1]))
                target_w = int((float(img.size[0]) * float(h_percent)))

            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            self.after(0, lambda: self._apply_large_image(label, photo))
        except Exception as e:
            print(f"Image Error: {e}")
            self.after(0, lambda: label.config(text=T(1999101102)))

    def _apply_large_image(self, label, photo):
        """Sets the fetched PhotoImage on the detail popup's image label and clears any loading placeholder text."""
        label.config(image=photo, text="", pady=0)
        label.image = photo

    def _load_gallery_image(self, label, url, is_gallery=False):
        """Downloads and scales gallery images (or standard thumbnails) proportionally."""
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status() # Ensure the download worked
            img = Image.open(io.BytesIO(res.content))

            # Target Width Calculation
            # Define target width based on use case
            if is_gallery:
                # 1/2 Size look (Balanced for 3-column popup)
                target_w = 180
            else:
                # Main Browser Tile size (3-column browser)
                target_w = 290

            # Calculate height to maintain Aspect Ratio
            w_percent = (target_w / float(img.size[0]))
            target_h = int((float(img.size[1]) * float(w_percent)))

            # Cap extremely tall images for the gallery look
            if is_gallery and target_h > 150:
                target_h = 150
                # Recalculate width based on height cap
                h_percent = (target_h / float(img.size[1]))
                target_w = int((float(img.size[0]) * float(h_percent)))

            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            self.after(0, lambda: self._apply_large_image(label, photo))
        except Exception as e:
            # Silent fallback, just keeps the loading hint
            pass

    def _apply_large_image(self, label, photo):
        """Applies the PhotoImage and keeps reference."""
        label.config(image=photo, text="", pady=0)
        label.image = photo

    def _download_and_install(self, url, mod_name, mod_id=None, install_area=None):
        """Downloads the mod and passes it to the existing run_install_logic."""
        dl_win = tk.Toplevel(self)
        dl_win.title(T(1999101103))
        dl_win.geometry("400x250")

        # Define size
        win_w, win_h = 400, 250
        dl_win.geometry(f"{win_w}x{win_h}")

        # Add the centering logic
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        dl_win.geometry(f"+{x}+{y}")

        dl_win.configure(bg=BG_SECTION)
        dl_win.transient(self)
        dl_win.grab_set()

        tk.Label(dl_win, text=T(1999101104), font=FONT_SMALL, bg=BG_SECTION, fg=FG_DIM).pack(pady=(20, 5))
        tk.Label(dl_win, text=mod_name.upper(), font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, wraplength=350).pack(pady=5)

        progress = ttk.Progressbar(dl_win, orient="horizontal", length=300, mode="determinate")
        progress.pack(pady=20)

        status_lbl = tk.Label(dl_win, text=T(1999101105), font=FONT_XSMALL, bg=BG_SECTION, fg="#2ecc71")
        status_lbl.pack()

        def run_task():
            try:
                # 1. Prepare Download Path
                _tmp_dir = tempfile.mkdtemp(prefix="anno117_mod_")
                safe_name = "".join([c for c in mod_name if c.isalnum() or c in (' ', '_')]).rstrip()
                zip_path = os.path.join(_tmp_dir, f"{safe_name.replace(' ', '_')}.zip")

                # 2. Download with Progress
                self.after(0, lambda: status_lbl.config(text=T(1999101106)))
                response = requests.get(url, stream=True, timeout=15)
                total_size = int(response.headers.get('content-length', 0))

                downloaded = 0
                with open(zip_path, 'wb') as f:
                    for data in response.iter_content(chunk_size=8192):
                        f.write(data)
                        downloaded += len(data)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            self.after(0, lambda p=percent: progress.config(value=p))

                # 3. Hand over to your existing Logic
                self.after(0, lambda: status_lbl.config(text=T(1999101107)))

                # We use .after(0) because run_install_logic has UI elements (messageboxes) and those MUST be called from the main thread.
                self.after(0, lambda zp=zip_path, td=_tmp_dir: self._finalize_installation(dl_win, zp, mod_id, install_area, url, mod_name, td))

            except Exception as e:
                try:
                    shutil.rmtree(_tmp_dir, ignore_errors=True)
                except Exception:
                    pass
                self.after(0, lambda: self._install_failed(dl_win, str(e)))

        threading.Thread(target=run_task, daemon=True).start()

    def _finalize_installation(self, window, zip_path, mod_id=None, install_area=None, dl_url=None, mod_name=None, tmp_dir=None):
        """Called after a zip download completes. If a mod.io mod_id is provided it runs the dependency preflight flow; otherwise it calls run_install_logic directly to extract and install the zip."""
        window.destroy()

        def _cleanup():
            if tmp_dir:
                shutil.rmtree(tmp_dir, ignore_errors=True)

        if mod_id is not None:
            def _preflight_then_cleanup():
                self._preflight_deps_then_install(zip_path, mod_id, install_area, dl_url, mod_name)
                _cleanup()
            threading.Thread(target=_preflight_then_cleanup, daemon=True).start()
        else:
            self.run_install_logic(zip_path)
            _cleanup()

    def _install_failed(self, window, error_msg):
        """Cleanup on network or download failure."""
        window.destroy()
        self._imperial_alert(T(1999101189), T(1999101399, error_msg), is_error=True)

    def _subscribe_to_mod(self, mod_id, install_area, dl_url, mod_name):
        """Subscribes the user to mod_id, subscribes to its dependencies server-side, then any dependencies not yet present."""
        def task():
            try:
                url = f"{MODIO_BASE_URL}/games/11358/mods/{mod_id}/subscribe"
                headers = {
                    'Authorization': f'Bearer {self.modio_token}',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json'
                }
                # include_dependencies=true lets mod.io subscribe to deps server-side
                res = requests.post(url, headers=headers, data={'include_dependencies': 'true'}, timeout=10)

                success = res.status_code in (200, 201)
                if not success and res.status_code == 400:
                    try:
                        err_ref = res.json().get('error', {}).get('error_ref', 0)
                        success = (err_ref == 15004)  # already subscribed
                    except Exception:
                        pass

                if success:
                    self._subscription_states[str(mod_id)] = True
                    self._save_subscriptions()
                    # Only store mapping if not already present — run_install_logic sets it precisely via ModID; _store_modio_mapping uses fuzzy matching which can corrupt the map when two mods share tokens
                    if str(mod_id) not in self._subscription_modio_map.values():
                        self._store_modio_mapping(mod_id, mod_name)
                    self._store_modio_mapping(mod_id, mod_name)
                    if install_area is not None:
                        self.after(0, lambda: self._apply_subscribed_state(install_area, dl_url, mod_name, mod_id))
                    # Map is now populated - refresh the right panel if the activation tab is still showing this mod so the button switches from Uninstall to Unsubscribe immediately.
                    def _refresh_right_panel():
                        if self.current_tab != "Mod Activation":
                            return
                        import re as _re
                        def _tok(s):
                            return set(_re.sub(r'[^a-z0-9]', ' ', s.lower()).split())
                        name_tokens = _tok(mod_name)
                        for m in self.mods:
                            lt = _tok(m.get('name', ''))
                            if lt and (lt.issubset(name_tokens) or
                                       name_tokens.issubset(lt)):
                                self.update_right_panel(m)
                                break
                    self.after(0, _refresh_right_panel)
                else:
                    print(f"[Subscribe] Not saved - status {res.status_code}")

            except Exception as e:
                print(f"[Subscribe] Exception for mod {mod_id}: {e}")

        threading.Thread(target=task, daemon=True).start()

    def _preflight_deps_then_install(self, main_zip_path, mod_id, install_area, dl_url, mod_name):
        """Background: installs any missing dependencies first (with alerts), then installs the main mod and subscribes. Uses threading.Event to sequence all main-thread blocking calls correctly."""
        headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}

        # 1. Fetch dependency list from mod.io
        to_install = []
        try:
            dep_res = requests.get(f"{MODIO_BASE_URL}/games/11358/mods/{mod_id}/dependencies", headers=headers, timeout=10)
            deps = dep_res.json().get('data', []) if dep_res.status_code == 200 else []

            installed_names = {
                m.get('name', '').lower().replace(' ', '')
                for m in self.get_all_mod_metadata()
            }

            for dep in deps:
                dep_mod_id = dep.get('mod_id')
                dep_mod_name = html.unescape(dep.get('name', ''))
                if dep_mod_name.lower().replace(' ', '') in installed_names:
                    self._subscription_states[str(dep_mod_id)] = True
                    continue
                mod_res = requests.get(
                    f"{MODIO_BASE_URL}/games/11358/mods/{dep_mod_id}",
                    headers=headers, timeout=10)
                if mod_res.status_code != 200:
                    continue
                dep_dl_url = (mod_res.json().get('modfile', {})
                                            .get('download', {})
                                            .get('binary_url'))
                if dep_dl_url:
                    to_install.append((dep_mod_id, dep_mod_name, dep_dl_url))
        except Exception as e:
            print(f"[Preflight] Dependency fetch failed: {e}")

        # 2. Install each missing dependency before the main mod
        if to_install:
            dep_names = "\n".join(f"  •  {n}" for _, n, _ in to_install)
            msg = T(1999101369, mod_name, dep_names)

            # Show info alert - block until user clicks OK
            alert_done = threading.Event()
            self.after(0, lambda: [self._imperial_alert(T(1999101289), msg), alert_done.set()])
            alert_done.wait()

            for dep_mod_id, dep_mod_name, dep_dl_url in to_install:
                try:
                    download_dir = "downloads"
                    os.makedirs(download_dir, exist_ok=True)
                    safe_name = "".join(
                        c for c in dep_mod_name if c.isalnum() or c in (' ', '_')).rstrip()
                    dep_zip = os.path.abspath(
                        os.path.join(download_dir, f"{safe_name.replace(' ', '_')}.zip"))

                    response = requests.get(dep_dl_url, stream=True, timeout=30)
                    response.raise_for_status()
                    with open(dep_zip, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    # Install silently on main thread and wait for it to finish
                    install_done = threading.Event()
                    def _do_dep_install(zp=dep_zip, mid=dep_mod_id, mn=dep_mod_name, ev=install_done):
                        self._silent_finalize(zp, mid, mn)
                        self._imperial_alert(T(1999101302), T(1999101364, mn))
                        ev.set()
                    self.after(0, _do_dep_install)
                    install_done.wait()

                except Exception as e:
                    print(f"[Preflight] Download failed for '{dep_mod_name}': {e}")

        # 3. Install the main mod on the main thread, then subscribe
        self._pending_modio_mapping = (str(mod_id), mod_name)

        main_done = threading.Event()
        def _do_main_install(ev=main_done):
            self.run_install_logic(main_zip_path)
            ev.set()
        self.after(0, _do_main_install)
        main_done.wait()

        # 4. Subscribe (starts its own background thread)
        self._subscribe_to_mod(str(mod_id), install_area, dl_url, mod_name)

    def _install_mod_dependencies(self, mod_id):
        """Fetches the dependency list for mod_id from mod.io and silently downloads + installs any that are not already present locally."""
        try:
            headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
            dep_url = f"{MODIO_BASE_URL}/games/11358/mods/{mod_id}/dependencies"
            res = requests.get(dep_url, headers=headers, timeout=10)
            if res.status_code != 200:
                return

            deps = res.json().get('data', [])
            if not deps:
                return

            # Build set of already-installed mod names (lowercased, spaceless)
            installed_names = {
                m.get('name', '').lower().replace(' ', '')
                for m in self.get_all_mod_metadata()
            }

            to_install = []
            for dep in deps:
                dep_mod_id   = dep.get('mod_id')
                dep_mod_name = html.unescape(dep.get('name', ''))

                # Skip if already installed locally
                if dep_mod_name.lower().replace(' ', '') in installed_names:
                    self._subscription_states[str(dep_mod_id)] = True
                    continue

                # Grab the download URL for this dependency
                mod_url = f"{MODIO_BASE_URL}/games/11358/mods/{dep_mod_id}"
                mod_res = requests.get(mod_url, headers=headers, timeout=10)
                if mod_res.status_code != 200:
                    continue

                mod_data = mod_res.json()
                dl_url = (mod_data.get('modfile', {})
                                  .get('download', {})
                                  .get('binary_url'))
                if dl_url:
                    to_install.append((dep_mod_id, dep_mod_name, dl_url))

            if not to_install:
                return

            dep_names = "\n".join(f"  •  {n}" for _, n, _ in to_install)
            msg = T(1999101370, dep_names)
            self.after(0, lambda: self._imperial_alert(T(1999101289), msg))

            for dep_mod_id, dep_mod_name, dep_dl_url in to_install:
                self._silent_download_and_install(dep_mod_id, dep_mod_name, dep_dl_url)

        except Exception as e:
            print(f"[Dependencies] Failed to resolve deps for mod {mod_id}: {e}")

    def _silent_download_and_install(self, mod_id, mod_name, dl_url):
        """Downloads and installs a dependency mod without showing the progress popup - used for automatic dependency installation."""
        try:
            download_dir = "downloads"
            os.makedirs(download_dir, exist_ok=True)
            safe_name = "".join(c for c in mod_name if c.isalnum() or c in (' ', '_')).rstrip()
            zip_path  = os.path.abspath(
                os.path.join(download_dir, f"{safe_name.replace(' ', '_')}.zip"))

            response = requests.get(dl_url, stream=True, timeout=30)
            response.raise_for_status()
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # run_install_logic must run on the main thread
            self.after(0, lambda zp=zip_path, mid=mod_id, mn=mod_name:self._silent_finalize(zp, mid, mn))

        except Exception as e:
            print(f"[Dependencies] Download failed for '{mod_name}': {e}")

    def _silent_finalize(self, zip_path, mod_id, mod_name):
        """Main-thread finalizer for a silently installed dependency."""
        # Set the pending map BEFORE calling run_install_logic so it can consume it
        self._pending_modio_mapping = (str(mod_id), mod_name)

        self.run_install_logic(zip_path, silent=True)
        self._subscription_states[str(mod_id)] = True
        self._save_subscriptions()
        # _store_modio_mapping is no longer needed here because run_install_logic handles it directly.

    def _apply_subscribed_state(self, install_area, dl_url, mod_name, mod_id, missing_local=False):
        """Clears install_area and rebuilds it with the Refresh icon and the interactive Subscribed button."""
        try:
            for w in install_area.winfo_children():
                w.destroy()

            # Draw the warning badge here, AFTER destroying the old children
            if missing_local:
                _lbl_sub = tk.Label(install_area, text="!", font=FONT_UI_BOLD, fg=FG_GOLD, bg=BG_SECTION)
                _lbl_sub.pack(side="left", padx=(0, 4))
                self._attach_tooltip(_lbl_sub, T(1999101476))

            # --- 1. THE REINSTALL BUTTON (↻) ---
            def _confirm_reinstall():
                msg = T(1999101359, mod_name)

                if self._imperial_question(T(1999101213), msg):
                    self._download_and_install(dl_url, mod_name, mod_id=mod_id)

            _ico_rei = load_icon("reinstall", (22, 22))
            refresh_btn = tk.Button(install_area, text="" if _ico_rei else "↻", font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN, activebackground=BG_HOVER, relief="flat", cursor="hand2", padx=6, image=_ico_rei, compound="center" if _ico_rei else "none", command=_confirm_reinstall)
            if _ico_rei: refresh_btn.image = _ico_rei
            refresh_btn.pack(side="left")
            self._bind_hover(refresh_btn, BG_MAIN)
            self._attach_tooltip(refresh_btn, T(1999101268))

            # --- 2. THE SUBSCRIBED/UNSUBSCRIBE BUTTON ---
            # We change state to "normal" so it can be clicked
            _ico_sub  = load_icon("subscribed_state",  (24, 24))
            _ico_usub = load_icon("unsubscribe_hover",  (24, 24))
            sub_btn = tk.Button(install_area, text=T(1999101175), font=FONT_UI_BOLD, bg=FG_GOLD, fg="#000000", relief="flat", cursor="hand2", image=_ico_sub, compound="left" if _ico_sub else "none", command=lambda: self._unsubscribe_from_mod(mod_id, mod_name, install_area, dl_url))
            if _ico_sub: sub_btn.image = _ico_sub
            sub_btn.pack(side="left", padx=(4, 0))

            def on_enter(e):
                if str(mod_id) in self._subscription_states:
                    sub_btn.config(text=T(1999101176), bg="#c0392b", fg=FG_MAIN, image=_ico_usub or _ico_sub, compound="left" if (_ico_usub or _ico_sub) else "none")

            def on_leave(e):
                if str(mod_id) in self._subscription_states:
                    sub_btn.config(text=T(1999101175), bg=FG_GOLD, fg="#000000", image=_ico_sub, compound="left" if _ico_sub else "none")

            sub_btn.bind("<Enter>", on_enter)
            sub_btn.bind("<Leave>", on_leave)

        except tk.TclError:
            pass

    def _load_subscriptions(self):
        """Loads persisted subscription states from appdata."""
        path = os.path.join(self.appdata_dir, "subscriptions.json")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load subscriptions: {e}")
        return {}

    def _save_subscriptions(self):
        """Persists current subscription states to appdata."""
        path = os.path.join(self.appdata_dir, "subscriptions.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self._subscription_states, f)
        except Exception as e:
            print(f"Failed to save subscriptions: {e}")

    def _load_subscription_map(self):
        """Loads the local ModID → mod.io ID mapping from appdata."""
        path = os.path.join(self.appdata_dir, "subscription_map.json")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load subscription map: {e}")
        return {}

    def _save_subscription_map(self):
        """Persists the local ModID → mod.io ID mapping to appdata."""
        path = os.path.join(self.appdata_dir, "subscription_map.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self._subscription_modio_map, f)
        except Exception as e:
            print(f"Failed to save subscription map: {e}")

    def _store_modio_mapping(self, modio_id, modio_name):
        """After a successful install, find the local mod that matches modio_name and store local_ModID → modio_id in the persistent map, if earlier attempts failed."""
        import re as _re
        def _tok(s):
            # Strip special chars and split into a set of words
            return set(_re.sub(r'[^a-z0-9]', ' ', str(s).lower()).split())

        # 0. Remove any stale entries that point to this modio_id but belong to a different local mod — prevents two local mods sharing one modio ID
        mid_str = str(modio_id)
        stale = [k for k, v in self._subscription_modio_map.items() if v == mid_str]
        for k in stale:
            del self._subscription_modio_map[k]

        name_tokens = _tok(modio_name)
        local_match = None

        # 1. Exact normalised match first (Checks both Name and ID)
        norm_target = _re.sub(r'[^a-z0-9]', '', modio_name.lower())
        for m in self.mods:
            if m.get('parent_path'): continue
            norm_name = _re.sub(r'[^a-z0-9]', '', m.get('name', '').lower())
            norm_id = _re.sub(r'[^a-z0-9]', '', m.get('id', '').lower())

            if norm_name == norm_target or norm_id == norm_target:
                local_match = m
                break

        # 2. Intersection Scoring (Fuzzy Match)
        if local_match is None:
            best_match = None
            best_score = 0
            for m in self.mods:
                if m.get('parent_path'): continue

                id_tokens = _tok(m.get('id', ''))
                name_toks = _tok(m.get('name', ''))

                # Count how many words overlap
                overlap_id = len(name_tokens.intersection(id_tokens))
                overlap_name = len(name_tokens.intersection(name_toks))

                score = max(overlap_id, overlap_name)

                # Tie-breakers: bump the score slightly if it's a perfect subset
                if name_tokens.issubset(id_tokens) or name_tokens.issubset(name_toks):
                    score += 0.5
                if id_tokens.issubset(name_tokens) or name_toks.issubset(name_tokens):
                    score += 0.5

                # Require at least 1 matching word to prevent wild false positives
                if score > best_score and score >= 1:
                    best_score = score
                    best_match = m

            if best_match:
                local_match = best_match

        if local_match:
            self._subscription_modio_map[local_match['id']] = str(modio_id)
            self._save_subscription_map()
        else:
            print(f"[modio_map] WARNING: could not match mod.io '{modio_name}' (id={modio_id}) to any local mod.")

    def _unsubscribe_from_mod(self, mod_id, mod_name, install_area, dl_url):
        """Prompt user and trigger the unsubscription/uninstallation process."""
        # Check if this mod is a required dependency of any other active mod
        import re as _re
        def _tokens(s):
            return set(_re.sub(r'[^a-z0-9]', ' ', s.lower()).split())

        mod_name_norm   = mod_name.lower().replace(' ', '')
        mod_name_tokens = _tokens(mod_name)

        local_mod = next(
            (m for m in self.mods
             if m.get('name', '').lower().replace(' ', '') == mod_name_norm
             and not m.get('parent_path')),
            None
        )
        if local_mod is None:
            for m in self.mods:
                if m.get('parent_path'):
                    continue
                lt = _tokens(m.get('name', ''))
                if lt and lt.issubset(mod_name_tokens):
                    local_mod = m
                    break
        if local_mod is None:
            for m in self.mods:
                if m.get('parent_path'):
                    continue
                lt = _tokens(m.get('name', ''))
                if mod_name_tokens and mod_name_tokens.issubset(lt):
                    local_mod = m
                    break
        if local_mod:
            dependents = [
                m['name'] for m in self.mods
                if m['id'] != local_mod['id']
                and self.mod_statuses.get(m['id'], {}).get('active', False)
                and not self.mod_statuses.get(m['id'], {}).get('uninstalled', False)
                and local_mod['id'] in m.get('deps', {}).get('Require', [])
            ]
            if dependents:
                dep_lines = "\n".join(f"  •  {n}" for n in dependents)
                body = T(1999101417, mod_name, dep_lines)
                choice = self._imperial_dependency_warning(T(1999101411), body, btn_accept=T(1999101415), missing_dep_ids=None)
                if choice != "accept":
                    return

        msg = T(1999101352, mod_name)

        if self._imperial_question(T(1999101283), msg):
            for child in install_area.winfo_children():
                if child.cget("text") in ["★ SUBSCRIBED", "❌ UNSUBSCRIBE"]:
                    child.config(text=T(1999101110), state="disabled", bg=BG_HOVER)

            threading.Thread(target=self._unsubscribe_from_mod_worker, args=(mod_id, mod_name, install_area, dl_url), daemon=True).start()

    def _unsubscribe_from_mod_worker(self, mod_id, mod_name, install_area, dl_url):
        """API worker to delete subscription and local files."""
        headers = {
            'Authorization': f'Bearer {self.modio_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = f"{MODIO_BASE_URL}/games/11358/mods/{mod_id}/subscribe"

        try:
            # 1. API Call to Unsubscribe
            res = requests.delete(url, headers=headers, timeout=10)

            # If 204 (No Content) or 404 (Already gone), consider it a success
            if res.status_code in [204, 404, 200]:
                # 2. Update local state
                sid = str(mod_id)
                if sid in self._subscription_states:
                    del self._subscription_states[sid]
                    self._save_subscriptions()
                # Remove reverse mapping entry for this mod.io ID
                self._subscription_modio_map = {
                    k: v for k, v in self._subscription_modio_map.items()
                    if v != sid
                }
                self._save_subscription_map()

                # 3. Local File Removal
                # We need to find the mod object to get its local folder path
                self._delete_unsubscribed_mod(mod_id, mod_name)

                # 4. UI Refresh
                if hasattr(self, 'browser_subscribed_only') and self.browser_subscribed_only.get():
                    self.after(0, self.refresh_browser)
                else:
                    self.after(0, lambda: self._reset_install_area_to_install(install_area, mod_id, mod_name, dl_url))

                # Show success alert first, then offer orphan cleanup after user clicks OK
                def _success_then_orphan_check(mn=mod_name, mid=mod_id):
                    self._imperial_alert(T(1999101201), T(1999101365, mod_name))
                    threading.Thread(
                        target=self._check_and_remove_orphan_deps,
                        args=(mid, mn), daemon=True
                    ).start()

                self.after(0, _success_then_orphan_check)
            else:
                error_msg = res.json().get('error', {}).get('message', 'Unknown Error')
                print(f"[Unsubscribe] API Error: {error_msg}")
                self.after(0, lambda: self._imperial_alert(T(1999101298), T(1999101380, error_msg), is_error=True))
                # Restore button state on failure
                self.after(0, lambda: self._apply_subscribed_state(install_area, dl_url, mod_name, mod_id))

        except Exception as e:
            print(f"[Unsubscribe] Critical Exception: {e}")
            self.after(0, lambda: self._imperial_alert(T(1999101189), T(1999101400, e), is_error=True))
            self.after(0, lambda: self._apply_subscribed_state(install_area, dl_url, mod_name, mod_id))

    def _delete_unsubscribed_mod(self, mod_id, mod_name):
        """Finds and deletes the local folder for a mod.io mod by numeric ID, falling back to name-matching if the subscription map doesn't have it."""

        # 1. Physical Scan of local modinfo files
        all_local_metadata = self.get_all_mod_metadata()

        # Fast path: resolve via subscription map (local_mod_id → modio_id)
        mid_str = str(mod_id)
        rev_map = {v: k for k, v in self._subscription_modio_map.items()}
        local_id = rev_map.get(mid_str)
        target = next((m for m in all_local_metadata if m['id'] == local_id), None) if local_id else None

        import re as _re
        def _tok(s):
            return set(_re.sub(r'[^a-z0-9]', ' ', s.lower()).split())

        search_name   = mod_name.lower().replace(" ", "")
        search_tokens = _tok(mod_name)

        # Fallback: name matching (for mods not yet in the subscription map)
        if target is None:
            for m in all_local_metadata:
                local_name = m.get('name', '').lower().replace(" ", "")
                if search_name == local_name or search_name in local_name:
                    target = m
                    break

        if target is None:
            for m in all_local_metadata:
                lt = _tok(m.get('name', ''))
                if lt and lt.issubset(search_tokens):
                    target = m
                    break

        if target is None:
            for m in all_local_metadata:
                lt = _tok(m.get('name', ''))
                if search_tokens and search_tokens.issubset(lt):
                    target = m
                    break

        # 2. Execution
        if target and target.get('path') and os.path.exists(target['path']):
            try:
                local_path = target['path']
                local_id_string = target['id']

                shutil.rmtree(local_path)

                # Use the helper to fix the profile file
                self._remove_from_active_profile(local_id_string)

                # Force refresh of internal mod lists
                self.get_all_mod_metadata()
                return True
            except Exception as e:
                print(f"[Cleanup] Error during deletion: {e}")
                return False

        print(f"[Cleanup] No local folder found for '{mod_name}'. Nothing to delete.")
        return False

    def _check_and_remove_orphan_deps(self, mod_id, mod_name):
        """Fetches deps of mod_id, finds which are not required by any other installed mod, and offers to remove them."""
        try:
            headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
            dep_url = f"{MODIO_BASE_URL}/games/11358/mods/{mod_id}/dependencies"
            res = requests.get(dep_url, headers=headers, timeout=10)
            if res.status_code != 200:
                return

            deps = res.json().get('data', [])
            if not deps:
                return

            all_local = self.get_all_mod_metadata()

            other_required = set()
            for m in all_local:
                for dep_id in m.get('deps', {}).get('Require', []):
                    other_required.add(dep_id)

            import re as _re
            def _tokens(s):
                return set(_re.sub(r'[^a-z0-9]', ' ', s.lower()).split())

            orphans = []
            for dep in deps:
                dep_modio_id  = str(dep.get('mod_id', ''))
                dep_name      = html.unescape(dep.get('name', dep_modio_id))
                dep_name_norm = dep_name.lower().replace(' ', '')
                dep_tokens    = _tokens(dep_name)

                # 1. Exact normalised match
                local_dep = next(
                    (m for m in all_local
                     if m.get('name', '').lower().replace(' ', '') == dep_name_norm),
                    None
                )
                # 2. Token-overlap: all local tokens present in dep tokens
                if local_dep is None:
                    for m in all_local:
                        local_tokens = _tokens(m.get('name', ''))
                        if local_tokens and local_tokens.issubset(dep_tokens):
                            local_dep = m
                            break
                # 3. Reverse subset: dep tokens ⊆ local tokens
                if local_dep is None:
                    for m in all_local:
                        local_tokens = _tokens(m.get('name', ''))
                        if dep_tokens and dep_tokens.issubset(local_tokens):
                            local_dep = m
                            break

                local_mod_id = local_dep['id'] if local_dep else None
                if local_mod_id not in other_required:
                    orphans.append((dep_modio_id, dep_name, local_dep))

            if not orphans:
                return

            orphan_names = "\n".join(f"  •  {n}" for _, n, _ in orphans)
            msg = T(1999101360, mod_name, orphan_names)

            def prompt_and_remove():
                if self._imperial_question(T(1999101323), msg):
                    def _remove_worker():
                        hdrs = {
                            'Authorization': f'Bearer {self.modio_token}',
                            'Accept': 'application/json',
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                        removed_names  = []
                        not_found_names = []
                        for dep_modio_id, dep_name, local_dep in orphans:
                            try:
                                requests.delete(
                                    f"{MODIO_BASE_URL}/games/11358/mods/{dep_modio_id}/subscribe",
                                    headers=hdrs, timeout=10)
                            except Exception as e:
                                print(f"[OrphanRemove] Unsubscribe exception: {e}")

                            if local_dep:
                                local_name = local_dep['name']
                                if self._delete_unsubscribed_mod(dep_modio_id, local_name):
                                    removed_names.append(local_name)
                            else:
                                not_found_names.append(dep_name)

                            if dep_modio_id in self._subscription_states:
                                del self._subscription_states[dep_modio_id]

                        self._save_subscriptions()
                        self.after(0, self.get_all_mod_metadata)
                        self.after(0, self.parse_active_profile)

                        if hasattr(self, 'browser_subscribed_only') and self.browser_subscribed_only.get():
                            self.after(0, self.refresh_browser)

                        if removed_names:
                            names_str = "\n".join(f"  •  {n}" for n in removed_names)
                            self.after(0, lambda: self._imperial_alert(T(1999101303), T(1999101401, names_str)))
                        if not_found_names:
                            nf_str = "\n".join(f"  •  {n}" for n in not_found_names)
                            self.after(0, lambda: self._imperial_alert(T(1999101304), T(1999101402, nf_str), is_error=True))

                    threading.Thread(target=_remove_worker, daemon=True).start()

            self.after(0, prompt_and_remove)

        except Exception as e:
            print(f"[OrphanCheck] Exception: {e}")

    def _remove_from_active_profile(self, mod_id):
        """Ensures the deleted mod is scrubbed from active-profile.txt immediately."""
        if not os.path.exists(self.active_profile_path):
            return

        updated_lines = []
        found = False
        with open(self.active_profile_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
                clean = line.strip()
                if not clean:
                    updated_lines.append(line)
                    continue
                current_id = clean.lstrip('#').split('#')[0].strip()

                if current_id == mod_id:
                    updated_lines.append(f"{mod_id} # not installed\n")
                    found = True
                else:
                    updated_lines.append(line)

        if not found:
            updated_lines.append(f"{mod_id} # not installed\n")

        with open(self.active_profile_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)

    def _reset_install_area_to_install(self, install_area, mod_id, mod_name, dl_url):
        """Reverts the entire frame back to the single 'INSTALL' button."""
        # 1. Clear the area
        for w in install_area.winfo_children():
            w.destroy()

        # 2. Create the button using the arguments passed to this function
        btn_newinstall = tk.Button(install_area, text=T(1999101177), font=FONT_UI_BOLD, bg="#2ecc71", fg="#000000", activebackground="#39f085", relief="flat", width=12, cursor="hand2", command=lambda mid=mod_id, ia=install_area, u=dl_url, n=mod_name: self._subscribe_to_mod(mid, ia, u, n))
        btn_newinstall.pack()
        self._bind_hover(btn_newinstall, "#2ecc71", "#39f085")

    # ==========================================
    # --- TWEAKING TAB ---
    # ==========================================

    def _load_active_options(self):
        """Reads the user's tweaked settings from active-options.jsonc."""
        if not os.path.exists(self.options_path):
            return {}
        try:
            with open(self.options_path, 'r', encoding='utf-8') as f:
                content = f.read()
                content = self.strip_jsonc_comments(content)
                return json.loads(content)
        except Exception as e:
            print(f"Failed to load active-options.jsonc: {e}")
            return {}

    def _save_active_options(self, data):
        """Writes the tweaked settings to active-options.jsonc."""
        try:
            with open(self.options_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Failed to save active-options.jsonc: {e}")

    def _get_mod_options_schema(self, path):
        """Reads the modinfo.json purely to extract the 'Options' block."""
        info_json = os.path.join(path, "modinfo.json")
        info_jsonc = os.path.join(path, "modinfo.jsonc")
        target = info_json if os.path.exists(info_json) else (info_jsonc if os.path.exists(info_jsonc) else None)

        if target:
            try:
                with open(target, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if target.endswith(".jsonc"):
                        content = self.strip_jsonc_comments(content)
                    data = json.loads(content)
                    return data.get("Options", {})
            except:
                pass
        return {}

    def _save_single_option(self, mod_id, opt_key, new_value):
        """Updates a single option and saves the file."""
        data = self._load_active_options()
        if mod_id not in data:
            data[mod_id] = {}

        data[mod_id][opt_key] = new_value
        self._save_active_options(data)

    def _reset_all_options(self):
        """Deletes the entire active-options.jsonc file."""
        if self._imperial_question(T(1999101206), T(1999101244)):
            if os.path.exists(self.options_path):
                os.remove(self.options_path)
            self.render_tweaking_tab()
            self._imperial_alert(T(1999101201), T(1999101245))

    def _reset_single_mod_options(self, mod):
        """Removes only the selected mod's configuration from the file."""
        msg = T(1999101361, mod['name'])
        if self._imperial_question(T(1999101324), msg):
            data = self._load_active_options()
            if mod['id'] in data:
                del data[mod['id']]
                self._save_active_options(data)
            self._render_tweaking_right_panel(mod)
            self._imperial_alert(T(1999101201), T(1999101379, mod['name']))

    def render_tweaking_tab(self, select_id=None):
        """Renders the Tweaking tab: a scrollable left list of customisable mods and a right panel that shows and saves their configurable options, dispatching _render_tweaking_right_panel when a mod is selected."""
        # 1. Setup layout (Middle and Right Panel)
        self.right_panel.grid()
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0, minsize=500) # Enforces fixed width!

        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Bind arrow keys for navigation
        self.bind("<Up>", self._navigate_tweaks_up)
        self.bind("<Down>", self._navigate_tweaks_down)

        # Ensure bindings are removed when leaving the tab
        self.main_content.bind("<Destroy>", lambda e: [self.unbind("<Up>"), self.unbind("<Down>")])

        # 2. Header & Reset All
        header_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        header_frame.pack(fill="x", padx=10, pady=20)

        tk.Label(header_frame, text=T(1999101111), font=FONT_TITLE, bg=BG_MAIN, fg=FG_MAIN).pack(side="left")

        btn_reset_all = tk.Button(header_frame, text=T(1999101112), font=FONT_BOLD_SMALL, bg="#8b0000", fg=FG_MAIN, cursor="hand2", command=self._reset_all_options, relief="raised", padx=10)
        btn_reset_all.pack(side="right", padx=10)
        self._bind_hover(btn_reset_all, "#8b0000", "#AF0202")
        self._attach_tooltip(btn_reset_all, T(1999101269))

        # 3. Setup Middle Scrollable Canvas
        container = tk.Frame(self.main_content, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        canvas = tk.Canvas(container, bg=BG_MAIN, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_MAIN)
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            try: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except: pass

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        container.bind('<Leave>', lambda e: canvas.unbind_all("<MouseWheel>"))

        # 4. Filter, Sort, and Draw Mods
        tweakable_mods = [m for m in self.mods if m.get('has_options') and not m.get('parent_path')]

        if not tweakable_mods:
            tk.Label(scrollable_frame, text=T(1999101113), font=FONT_BODY, bg=BG_MAIN, fg=FG_DIM).pack(pady=40)
            self._render_tweaking_right_panel(None)
            return

        statuses = self.parse_active_profile()

        # Sort identical to Activation Tab: Active First (or based on self.sort_active_first)
        def tweak_sort_key(m):
            is_active = statuses.get(m['id'], {}).get("active", self.enable_new_mods_var.get())
            return 0 if is_active == self.sort_active_first else 1

        tweakable_mods.sort(key=tweak_sort_key)

        active_sep_needed = True
        inactive_sep_needed = True

        target_row_frame = None
        target_mod_data = None

        for mod in tweakable_mods:
            is_active = statuses.get(mod['id'], {}).get("active", self.enable_new_mods_var.get())

            if is_active == self.sort_active_first and active_sep_needed:
                label = T(1999101439) if self.sort_active_first else T(1999101438)
                self._draw_separator_tweaks(scrollable_frame, label)
                active_sep_needed = False

            if is_active != self.sort_active_first and inactive_sep_needed:
                label = T(1999101438) if self.sort_active_first else T(1999101439)
                self._draw_separator_tweaks(scrollable_frame, label)
                inactive_sep_needed = False

            row_frame = self._draw_tweak_row(scrollable_frame, mod)

            if select_id and mod.get('id') == select_id:
                target_row_frame = row_frame
                target_mod_data = mod

        # 5. Handle Auto-Selection and Scrolling
        if select_id and target_row_frame:
            # We use after(10) to ensure the row is fully drawn before clicking
            self.after(10, lambda: self._on_tweak_row_click(target_row_frame, target_mod_data))

            # Scroll to it after a tiny delay so the canvas can update its scrollregion
            self.after(100, lambda: self._scroll_to_selected_tweak(canvas, target_row_frame))
        else:
            # Only reset if we are NOT trying to select something specific
            if not select_id:
                self.selected_tweak_row = None
                self._render_tweaking_right_panel(None)

    def _navigate_tweaks_up(self, event=None):
        """Keyboard handler that moves the tweaking-tab selection up by one row."""
        self._navigate_tweaks(-1)

    def _navigate_tweaks_down(self, event=None):
        """Keyboard handler that moves the tweaking-tab selection down by one row."""
        self._navigate_tweaks(1)

    def _navigate_tweaks(self, direction):
        """Moves the current tweaking-tab selection by the given direction (+1 down, -1 up), clicking the target row to trigger its selection callback."""
        # 1. Get all frames in the middle list (excluding separators)
        all_rows = [w for w in self.main_content.nametowidget(self.main_content.winfo_children()[-1].winfo_children()[0].winfo_children()[0]).winfo_children()
                    if isinstance(w, tk.Frame) and w.cget("cursor") == "hand2"]

        if not all_rows:
            return

        # 2. Find current index
        current_idx = -1
        if hasattr(self, 'selected_tweak_row') and self.selected_tweak_row in all_rows:
            current_idx = all_rows.index(self.selected_tweak_row)

        # 3. Calculate next index
        next_idx = current_idx + direction
        if 0 <= next_idx < len(all_rows):
            target_row = all_rows[next_idx]

            # 4. Programmatically click the row
            target_row.event_generate("<Button-1>")

            # 5. Scroll into view if needed
            canvas = self.main_content.winfo_children()[-1].winfo_children()[0]
            self._ensure_row_visible(canvas, target_row)

    def _ensure_row_visible(self, canvas, row):
        """Helper to adjust scrollbar so the selected row is visible."""
        self.update_idletasks()
        row_top = row.winfo_y()
        row_bottom = row_top + row.winfo_height()

        # Get canvas scroll region
        _, _, _, c_height = canvas.bbox("all")
        v_top, v_bottom = canvas.yview()

        # Convert pixel positions to scroll fractions (0.0 to 1.0)
        view_top = v_top * c_height
        view_bottom = v_bottom * c_height

        if row_top < view_top:
            canvas.yview_moveto(row_top / c_height)
        elif row_bottom > view_bottom:
            canvas.yview_moveto((row_bottom - canvas.winfo_height()) / c_height)

    def _draw_separator_tweaks(self, parent, text):
        """Dedicated separator for the Tweaking tab to match Activation visual logic."""
        sep_container = tk.Frame(parent, bg=BG_MAIN, pady=15)
        sep_container.pack(fill="x")
        line_color = FG_SEPARATOR
        tk.Frame(sep_container, bg=line_color, height=2).pack(fill="x", padx=10, side="left", expand=True)
        tk.Label(sep_container, text=f" {text} ", font=FONT_BOLD_SMALL, bg=BG_MAIN, fg=FG_DIM).pack(side="left", padx=10)
        tk.Frame(sep_container, bg=line_color, height=2).pack(fill="x", padx=10, side="left", expand=True)

    def _draw_tweak_row(self, container, mod):
        """Renders a single selectable mod row in the tweaking tab's left list with hover and click bindings."""
        row_bg = BG_SECTION
        hover_bg = BG_HOVER

        row = tk.Frame(container, bg=row_bg, highlightthickness=1, highlightbackground=row_bg, highlightcolor=FG_MAIN, cursor="hand2")
        row.pack(fill="x", padx=10, pady=2)

        lbl = tk.Label(row, text=mod['name'], font=FONT_SMALL, bg=row_bg, fg=FG_MAIN, anchor="w")
        lbl.pack(side="left", fill="x", expand=True, padx=(20, 0), pady=0)

        # Update bindings to use the new class method
        row.bind("<Button-1>", lambda e: self._on_tweak_row_click(row, mod))
        lbl.bind("<Button-1>", lambda e: self._on_tweak_row_click(row, mod))

        self._bind_hover(row, row_bg, hover_bg)

        def on_leave_tweak(e, r=row):
            if hasattr(self, 'selected_tweak_row') and self.selected_tweak_row == r:
                r.config(bg=BG_HOVER)
                for c in r.winfo_children(): c.config(bg=BG_HOVER)
            else:
                r.config(bg=BG_SECTION)
                for c in r.winfo_children(): c.config(bg=BG_SECTION)

        row.bind("<Leave>", on_leave_tweak)

        return row

    def _on_tweak_row_click(self, row, mod):
        """Unified selection logic for the tweaking list that preserves your styling."""
        row_bg = BG_SECTION
        select_bg = BG_HOVER

        # 1. Reset previous selection to default
        if hasattr(self, 'selected_tweak_row') and self.selected_tweak_row:
            try:
                prev_row = self.selected_tweak_row
                prev_row.config(bg=row_bg, highlightbackground=row_bg)
                for child in prev_row.winfo_children():
                    child.config(bg=row_bg)
            except:
                pass

        # 2. Apply new selection styling
        self.selected_tweak_row = row
        # Force the row and all its labels to use BG_HOVER
        row.config(bg=select_bg, highlightbackground=FG_MAIN)
        for child in row.winfo_children():
            child.config(bg=select_bg)

        # 3. Update the right panel
        self._render_tweaking_right_panel(mod)

    def _render_tweaking_right_panel(self, mod):
        """Populates the right panel of the Tweaking tab with the selected mod's configurable options: enum dropdowns, toggle checkboxes and free-text entries, each with a live insight label."""
        for w in self.right_panel.winfo_children():
            w.destroy()

        if not mod:
            tk.Label(self.right_panel, text=T(1999101114), font=FONT_TITLE, bg=BG_SECTION, fg=FG_DIM).pack(expand=True)
            return

        # --- Header Section ---
        header_frame = tk.Frame(self.right_panel, bg=BG_SECTION)
        header_frame.pack(fill="x", pady=10, padx=15)

        btn_reset = tk.Button(header_frame, text=T(1999101115), font=FONT_XSMALL, bg="#8b0000", fg=FG_MAIN, cursor="hand2", command=lambda: self._reset_single_mod_options(mod), relief="raised")
        btn_reset.pack(side="right", anchor="ne", padx=(10, 0))
        self._bind_hover(btn_reset, "#8b0000", "#AF0202")
        self._attach_tooltip(btn_reset, T(1999101270))

        lbl_name = tk.Label(header_frame, text=mod['name'], font=FONT_HEADER, bg=BG_SECTION, fg=FG_MAIN, wraplength=320, justify="left", anchor="nw")
        lbl_name.pack(side="left", fill="x", expand=True)

        tk.Frame(self.right_panel, height=1, bg=FG_DIM).pack(fill="x", padx=15, pady=5)

        # --- Scrollable Area ---
        canvas = tk.Canvas(self.right_panel, bg=BG_SECTION, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.right_panel, orient="vertical", command=canvas.yview)
        container = tk.Frame(canvas, bg=BG_SECTION)
        canvas_window = canvas.create_window((0, 0), window=container, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind('<Enter>', lambda e: canvas.bind_all("<MouseWheel>", lambda ev: canvas.yview_scroll(int(-1 * (ev.delta / 120)), "units")))
        canvas.bind('<Leave>', lambda e: canvas.unbind_all("<MouseWheel>"))

        active_options = self._load_active_options()
        mod_active_opts = active_options.get(mod['id'], {})
        options_schema = self._get_mod_options_schema(mod['path'])

        if not options_schema:
            tk.Label(container, text=T(1999101116), font=FONT_BODY, bg=BG_SECTION, fg=FG_DIM).pack(pady=20)
            return

        for opt_key, opt_details in options_schema.items():
            opt_frame = tk.Frame(container, bg=BG_SECTION, highlightthickness=1, highlightbackground=FG_DIM)
            opt_frame.pack(fill="x", padx=20, pady=5)

            inner_padding = tk.Frame(opt_frame, bg=BG_SECTION)
            inner_padding.pack(fill="x", padx=15, pady=(8, 12))

            label_text = opt_details.get('label', opt_key)
            tk.Label(inner_padding, text=label_text, font=FONT_BODY, bg=BG_SECTION, fg=FG_MAIN, wraplength=420, justify="left").pack(anchor="w", pady=(0, 5))

            opt_type = opt_details.get('type', 'text').lower()
            default_val = str(opt_details.get('default', ''))
            current_val = str(mod_active_opts.get(opt_key, default_val))

            # 2. Input Box Area
            input_container = tk.Frame(inner_padding, bg=BG_SECTION)
            input_container.pack(anchor="w", fill="x")

            # Shared Insight Updater
            _ico_tweak_desc = load_icon("tweak_description", (14, 14))
            insight_lbl = tk.Label(inner_padding, text="", font=FONT_SMALL, bg=BG_SECTION, fg=FG_GOLD, justify="left", wraplength=400)

            def update_insight(current_val, details=opt_details, lbl=insight_lbl):
                """Updates the sub-label based on the current selection."""
                labels = details.get('labels', [])
                vals = details.get('values', [])
                o_type = details.get('type', 'text').lower()

                text = ""
                if o_type == "enum" and current_val in vals:
                    idx = vals.index(current_val)
                    if idx < len(labels): text = labels[idx]
                elif o_type == "toggle":
                    # Toggle logic: Index 0 is True, Index 1 is False
                    idx = 0 if str(current_val).lower() == "true" else 1
                    if idx < len(labels): text = labels[idx]
                elif o_type == "text" and labels:
                    # For text types, we usually just show the first label as a hint
                    text = labels[0]

                if text.strip():
                    lbl.config(text=f"  {text}", image=_ico_tweak_desc or "", compound="left" if _ico_tweak_desc else "none")
                    if _ico_tweak_desc: lbl.image = _ico_tweak_desc
                    # Pack only if there is text to show
                    lbl.pack(anchor="w", pady=(2, 0), padx=10)
                else:
                    # Hide completely so it takes 0 pixels
                    lbl.pack_forget()

            # Render Inputs
            if opt_type == "enum":
                values = opt_details.get('values', [])
                combo_var = tk.StringVar(value=current_val)
                combo = ttk.Combobox(inner_padding, textvariable=combo_var, values=values, state="readonly", font=FONT_SMALL, width=30)
                combo.pack(anchor="w")

                def make_combo_callback(k=opt_key, v=combo_var, l=insight_lbl):
                    return lambda e: [
                        self._save_single_option(mod['id'], k, v.get()),
                        update_insight(v.get()) # Update the text immediately
                    ]
                combo.bind("<<ComboboxSelected>>", make_combo_callback())

            elif opt_type == "toggle":
                is_on = current_val.lower() == "true"
                toggle_var = tk.BooleanVar(value=is_on)

                chk = tk.Checkbutton(inner_padding, text=str(is_on), variable=toggle_var, font=FONT_SMALL, bg=BG_SECTION, fg=FG_GOLD if is_on else FG_DIM, selectcolor=BG_MAIN, activebackground=BG_SECTION, cursor="hand2")
                chk.pack(anchor="w")

                def make_toggle_callback(k=opt_key, v=toggle_var, c=chk):
                    return lambda: [
                        c.config(text=str(v.get()), fg=FG_GOLD if v.get() else FG_DIM),
                        self._save_single_option(mod['id'], k, "true" if v.get() else "false"),
                        update_insight("true" if v.get() else "false") # Update text
                    ]
                chk.config(command=make_toggle_callback())

            else:
                input_frame = tk.Frame(inner_padding, bg=BG_SECTION)
                input_frame.pack(anchor="w", fill="x")

                entry_var = tk.StringVar(value=current_val)
                entry = tk.Entry(input_frame, textvariable=entry_var, font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN, insertbackground=FG_MAIN, relief="flat", width=25)
                entry.pack(side="left", ipady=4)

                def make_entry_callback(k=opt_key, v=entry_var):
                    return lambda e: [
                        self._save_single_option(mod['id'], k, v.get()),
                        update_insight(v.get()) # Update text
                    ]
                entry.bind("<FocusOut>", make_entry_callback())
                entry.bind("<Return>", make_entry_callback())

                # --- CUSTOM COLOR PICKER INJECTION ---
                if mod['id'] in ["taludas-customnpccolours", "taludas-customplayercolour"]:
                    # Create the picker button
                    _ico_cp = load_icon("colorpicker_btn", (24, 24))
                    btn_color = tk.Button(input_frame, text="" if _ico_cp else "🎨", font=FONT_XSMALL, bg=BG_MAIN, fg=FG_MAIN, cursor="hand2", relief="raised", image=_ico_cp, compound="center" if _ico_cp else "none")
                    if _ico_cp: btn_color.image = _ico_cp
                    btn_color.pack(side="left", padx=10)
                    self._bind_hover(btn_color, BG_MAIN, BG_HOVER)
                    self._attach_tooltip(btn_color, T(1999101271))

                    def _open_color_picker(v=entry_var, k=opt_key):
                        try:
                            # Anno uses signed 32-bit ARGB integers. Extract R, G, B for the picker.
                            val = int(v.get())
                            a = (val >> 24) & 255
                            if a == 0: a = 255 # Assume opaque if missing
                            r = (val >> 16) & 255
                            g = (val >> 8) & 255
                            b = val & 255
                            init_hex = f"#{r:02x}{g:02x}{b:02x}"
                        except:
                            a = 255
                            init_hex = "#ffffff"

                        chosen_color = colorchooser.askcolor(initialcolor=init_hex, title="NPC Colour Selection")

                        if chosen_color[1]: # If a color was picked (returns hex #RRGGBB)
                            rgb_int = int(chosen_color[1][1:], 16)
                            # Reconstruct ARGB signed 32-bit integer
                            new_val = (a << 24) | rgb_int
                            signed_val = ctypes.c_int32(new_val).value

                            v.set(str(signed_val))
                            self._save_single_option(mod['id'], k, str(signed_val))

                    btn_color.config(command=_open_color_picker)

            # Initial call to set the label on load
            update_insight(current_val)

    def _scroll_to_selected_tweak(self, canvas, widget):
        """Scrolls the tweaking tab's left-list canvas so that the currently selected row is fully visible."""
        self.update_idletasks()
        try:
            # Get the position of the widget relative to the scrollable_frame
            y_pos = widget.winfo_y()
            # Get the total height of the scrollable content
            total_height = canvas.bbox("all")[3]

            if total_height > 0:
                # Move the canvas so the widget is at the top (fraction 0.0 to 1.0), we subtract a small amount (like 0.05) to give it some padding at the top
                fraction = max(0, (y_pos / total_height) - 0.02)
                canvas.yview_moveto(fraction)
        except Exception as e:
            print(f"Scrolling failed: {e}")

    # ------------------------------------------------------------------
    # --- Incompatibility Feature ---
    # ------------------------------------------------------------------
    def _get_active_incompatible_conflicts(self, mod_id):
        """Returns a list of (conflict_id, conflict_name) tuples for mods that are listed as Incompatible in *mod_id*'s modinfo and are currently active in the loaded profile."""
        target_mod = next((m for m in self.mods if m['id'] == mod_id), None)
        if not target_mod:
            return []

        incompatible_ids = target_mod.get('deps', {}).get('Incompatible', [])
        if not incompatible_ids:
            return []

        # Build a set of IDs that are currently marked active.
        active_ids = {
            mid for mid, status in self.mod_statuses.items()
            if status.get('active', False) and not status.get('uninstalled', False)
        }

        conflicts = []
        for inc_id in incompatible_ids:
            if inc_id in active_ids:
                conflict_mod = next((m for m in self.mods if m['id'] == inc_id), None)
                display_name = conflict_mod['name'] if conflict_mod else inc_id
                conflicts.append((inc_id, display_name))

        return conflicts

    def _get_missing_required_deps(self, mod_id):
        """Returns a list of required dep IDs that are not installed at all."""
        target = next((m for m in self.mods if m['id'] == mod_id), None)
        if not target:
            return []
        installed_ids = {m['id'] for m in self.mods}
        return [dep for dep in target.get('deps', {}).get('Require', [])
                if dep not in installed_ids]

    def _is_deprecated_by_active(self, mod_id):
        """Returns True if any currently active mod lists mod_id in its Deprecate entry."""
        active_ids = {
            mid for mid, status in self.mod_statuses.items()
            if status.get('active', False) and not status.get('uninstalled', False)
        }
        for m in self.mods:
            if m['id'] in active_ids and m['id'] != mod_id:
                if mod_id in m.get('deps', {}).get('Deprecate', []):
                    return True
        return False

    def _imperial_conflict_warning(self, activating_mod_name, conflicts):
        """A dedicated, red-accented warning dialog for mod incompatibilities."""
        warn_win = tk.Toplevel(self)
        warn_win.title(T(1999101117))

        win_w, win_h = 675, 450
        warn_win.geometry(f"{win_w}x{win_h}")

        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        warn_win.geometry(f"+{x}+{y}")

        warn_win.configure(bg=BG_MAIN)
        warn_win.transient(self)
        warn_win.grab_set()

        result = {"ans": "keep"}

        def _select(val):
            result["ans"] = val
            warn_win.destroy()

        # Header – red for danger
        tk.Label(
            warn_win, text=T(1999101118),
            font=FONT_TITLE, bg=BG_MAIN, fg="#e74c3c"
        ).pack(pady=(22, 6))

        # Body
        conflict_names = "\n".join(f"  •  {name}  ({cid})" for cid, name in conflicts)
        body_text = T(1999101440, activating_mod_name, conflict_names)
        tk.Label(warn_win, text=body_text, font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, wraplength=480, justify="center").pack(pady=8, expand=True)

        # Buttons
        btn_frame = tk.Frame(warn_win, bg=BG_MAIN)
        btn_frame.pack(pady=(0, 24))

        btn_accept = tk.Button(btn_frame, text=T(1999101119), font=FONT_UI_BOLD, bg="#c0392b", activebackground="#db4332", fg=FG_MAIN, width=14, cursor="hand2", relief="raised", command=lambda: _select("accept"))
        btn_accept.pack(side="left", padx=8)
        self._bind_hover(btn_accept, "#c0392b", "#db4332")

        btn_keep = tk.Button(btn_frame, text=T(1999101120), font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, activebackground=BG_HOVER, width=14, cursor="hand2", relief="raised", command=lambda: _select("keep"))
        btn_keep.pack(side="left", padx=8)
        self._bind_hover(btn_keep, BG_SECTION, BG_HOVER)

        btn_disableoposing = tk.Button(btn_frame, text=T(1999101121), font=FONT_UI_BOLD, bg="#2e7d32", activebackground="#388e3c", fg=FG_MAIN, width=20, cursor="hand2", relief="raised", command=lambda: _select("disable_other"))
        btn_disableoposing.pack(side="left", padx=8)
        self._bind_hover(btn_disableoposing, "#2e7d32", "#388e3c")
        self._attach_tooltip(btn_disableoposing, T(1999101272))

        self.wait_window(warn_win)
        return result["ans"]

    def _check_and_confirm_incompatible(self, mod_id):
        """Returns True if it is safe to activate mod_id (no conflicts, user accepted the risk, or conflicting mods were disabled). Returns False if the mod should remain disabled."""
        conflicts = self._get_active_incompatible_conflicts(mod_id)
        if not conflicts:
            return True

        target_mod = next((m for m in self.mods if m['id'] == mod_id), None)
        mod_name = target_mod['name'] if target_mod else mod_id

        choice = self._imperial_conflict_warning(mod_name, conflicts)

        if choice == "disable_other":
            for conflict_id, _ in conflicts:
                self.toggle_mod_status(conflict_id, False)
            return True

        return choice == "accept"

    # ==========================================
    # --- COLLECTIONS ---
    # ==========================================
    def _load_collection_follows(self):
        """Loads the persisted collection-follow state dict from collection_follows.json in %APPDATA%. Returns an empty dict if the file does not exist or cannot be read."""
        path = os.path.join(self.appdata_dir, "collection_follows.json")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load collection follows: {e}")
        return {}

    def _save_collection_follows(self):
        """Serialises the current _collection_follow_states dict to collection_follows.json in %APPDATA%."""
        path = os.path.join(self.appdata_dir, "collection_follows.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self._collection_follow_states, f, indent=2)
        except Exception as e:
            print(f"Failed to save collection follows: {e}")

    def render_collections_tab(self):
        """Renders the Collections tab header, search bar, tag filter dropdown, followed-only toggle andthe scrollable tile grid. Fetches the collection list from mod.io in a background thread."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Header
        header_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        header_frame.pack(fill="x", padx=20, pady=20)
        tk.Label(header_frame, text=T(1999101122), font=FONT_TITLE, bg=BG_MAIN, fg=FG_MAIN).pack(side="left")

        self.col_stats_lbl = tk.Label(header_frame, text="", font=FONT_SMALL, bg=BG_MAIN, fg=FG_DIM)
        self.col_stats_lbl.pack(side="left", padx=15, pady=(5, 0))

        controls_frame = tk.Frame(header_frame, bg=BG_MAIN)
        controls_frame.pack(side="right")

        # Search
        search_bg = tk.Frame(controls_frame, bg=BG_SECTION, padx=5, pady=2)
        search_bg.pack(side="left", padx=10)
        self.col_search_var = tk.StringVar()
        search_entry = tk.Entry(search_bg, textvariable=self.col_search_var, font=FONT_SMALL, bg=BG_SECTION, fg=FG_MAIN, insertbackground=FG_MAIN, width=20, relief="flat")
        search_entry.pack(side="left")
        search_entry.bind("<Return>", lambda e: self._refresh_collections())
        tk.Button(search_bg, text="✕", font=FONT_XSMALL, bg=BG_SECTION, fg=FG_DIM, relief="flat", cursor="hand2", command=lambda: [self.col_search_var.set(""), self.col_tag_var.set("All Tags"), self._refresh_collections()]).pack(side="left")

        # Tag filter dropdown (populated async)
        self.col_tag_var = tk.StringVar(value="All Tags")
        self.col_tag_filter = ""
        self.col_tag_menu = tk.OptionMenu(controls_frame, self.col_tag_var, "All Tags")
        self.col_tag_menu.config(font=FONT_XSMALL, bg=BG_SECTION, fg=FG_MAIN, highlightthickness=0, width=14)
        self.col_tag_menu["menu"].config(bg=BG_SECTION, fg=FG_MAIN)
        self.col_tag_menu.pack(side="left", padx=(4, 0))

        def _on_col_tag_selected(*_):
            selected = self.col_tag_var.get()
            self.col_tag_filter = "" if selected == "All Tags" else selected
            self._refresh_collections()

        self.col_tag_var.trace_add("write", _on_col_tag_selected)

        # Collection tags are harvested live from collection results as they load (mod.io game tag options only cover mods, not collections)
        self._collection_tags_seen = set()

        # Followed filter
        self.col_followed_only = tk.BooleanVar(value=False)

        def _toggle_followed():
            is_on = self.col_followed_only.get()
            if is_on:
                # Active State: Gold
                self.btn_col_followed.config(bg=FG_GOLD, fg="#000000", image=_ico_colf_black)
                self._bind_hover(self.btn_col_followed, FG_GOLD, "#ffd013")
            else:
                # Inactive State: Return to standard UI colors
                self.btn_col_followed.config(bg=BG_SECTION, fg=FG_MAIN, image=_ico_colf)
                self._bind_hover(self.btn_col_followed, BG_SECTION, BG_HOVER)
            self._refresh_collections()

        _ico_colf = load_icon("followed_filter", (14, 14))
        _ico_colf_black = load_icon("followed_state", (14, 14))
        self.btn_col_followed = tk.Button(controls_frame, text=T(1999101178), font=FONT_XSMALL, bg=BG_SECTION, fg=FG_MAIN, relief="flat", cursor="hand2", padx=8, image=_ico_colf, compound="left" if _ico_colf else "none", command=lambda: [self.col_followed_only.set( not self.col_followed_only.get()), _toggle_followed()])
        if _ico_colf: self.btn_col_followed.image = _ico_colf
        self.btn_col_followed.pack(side="left", padx=(8, 0))
        self._bind_hover(self.btn_col_followed, BG_SECTION, BG_HOVER)
        self._attach_tooltip(self.btn_col_followed, T(1999101273))

        if not self.modio_token:
            tk.Label(self.main_content, text=T(1999101085), font=FONT_BODY, bg=BG_MAIN, fg=FG_DIM).pack(pady=50)
            return

        # Scrollable area
        self.col_canvas = tk.Canvas(self.main_content, bg=BG_MAIN, highlightthickness=0)
        col_scrollbar = tk.Scrollbar(self.main_content, orient="vertical", command=self.col_canvas.yview)
        self.col_scroll_frame = tk.Frame(self.col_canvas, bg=BG_MAIN)
        _col_cw = self.col_canvas.create_window((0, 0), window=self.col_scroll_frame, anchor="nw")
        # Keep inner frame width matched to the canvas
        self.col_canvas.bind("<Configure>", lambda e: self.col_canvas.itemconfig(_col_cw, width=e.width))
        self.col_canvas.configure(yscrollcommand=col_scrollbar.set)
        self.col_canvas.pack(side="left", fill="both", expand=True, padx=20)
        col_scrollbar.pack(side="right", fill="y")
        self.col_canvas.bind("<Destroy>", lambda e: self.col_canvas.unbind_all("<MouseWheel>"))

        # Virtual-scroll state
        self._all_col_data    = []
        self._col_virt_rows   = {}
        self._col_total_count = 0
        self._col_load_more   = None

        # Re-render visible rows on scroll
        def _col_vscroll(*args):
            col_scrollbar.set(*args)
            self.after_idle(self._render_visible_col_rows)
        self.col_canvas.configure(yscrollcommand=_col_vscroll)

        self.col_canvas.bind_all("<MouseWheel>", lambda e:
            self.col_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.col_offset = 0
        self._refresh_collections()

    def _refresh_collections(self):
        """Resets the collection offset, clears the tile grid and restarts a background fetch."""
        self.col_offset = 0
        self._all_col_data    = []
        self._col_virt_rows   = {}
        self._col_total_count = 0
        self._col_load_more   = None
        if hasattr(self, 'col_stats_lbl'):
            self.col_stats_lbl.config(text=T(1999101086))
        # Destroy only the loading label (virtual rows are gone via state reset)
        for widget in self.col_scroll_frame.winfo_children():
            try: widget.destroy()
            except: pass
        if hasattr(self, 'col_canvas'):
            self.col_canvas.yview_moveto(0)
        loading_lbl = tk.Label(self.col_scroll_frame, text=T(1999101087), font=FONT_BODY, bg=BG_MAIN, fg=FG_DIM)
        loading_lbl.pack(pady=40)

        if hasattr(self, 'col_followed_only') and self.col_followed_only.get():
            threading.Thread(target=self._fetch_followed_collections, args=(self.col_scroll_frame, loading_lbl), daemon=True).start()
        else:
            q = self.col_search_var.get() if hasattr(self, 'col_search_var') else ""
            tag = getattr(self, 'col_tag_filter', '')
            threading.Thread(target=self._fetch_collections_worker, args=(self.col_scroll_frame, loading_lbl, q, 0, tag), daemon=True).start()

    def _update_collection_tag_dropdown(self, new_tags: set):
        """Merges new_tags into the collection tag dropdown, called from background threads."""
        existing = getattr(self, '_collection_tags_seen', set())
        added = new_tags - existing
        if not added:
            return
        self._collection_tags_seen = existing | added
        all_tags = sorted(self._collection_tags_seen)

        def _rebuild():
            if not hasattr(self, 'col_tag_menu'):
                return
            try:
                menu = self.col_tag_menu["menu"]
                menu.delete(0, "end")
                menu.add_command(label="All Tags", command=lambda: self.col_tag_var.set("All Tags"))
                for tag in all_tags:
                    menu.add_command(label=tag, command=lambda t=tag: self.col_tag_var.set(t))
            except tk.TclError:
                pass

        self.after(0, _rebuild)

    def _fetch_collections_worker(self, parent_frame, loading_lbl, query="", offset=0, tag_filter=""):
        """Background worker that fetches a page of mod.io collections (with optional text query and tagfilter), updates the stats label and schedules _build_collection_tiles on the main thread."""
        headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
        url = f"{MODIO_BASE_URL}/games/11358/collections?_sort=-date_updated&_limit=50&_offset={offset}"
        if query: url += f"&_q={query}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 401:
                self.after(0, self._handle_modio_401)
                return
            res.raise_for_status()
            data = res.json()
            collections = data.get('data', [])
            total = data.get('result_total', 0)

            # Harvest tags from this batch and refresh the dropdown
            batch_tags = set()
            for col in collections:
                for t in (col.get('tags') or []):
                    name = t if isinstance(t, str) else t.get('name', '')
                    if name:
                        batch_tags.add(name)
            if batch_tags:
                self._update_collection_tag_dropdown(batch_tags)

            # Client-side tag filter (API cannot filter nested tag objects)
            if tag_filter:
                collections = [
                    c for c in collections
                    if any(
                        (t if isinstance(t, str) else t.get('name', '')) == tag_filter
                        for t in (c.get('tags') or [])
                    )
                ]
                total = len(collections)
            current_viewing = offset + len(collections)
            stats = T(1999101464, current_viewing, total) if collections else T(1999101464, 0, total)

            def _safe_update(t=stats, cols=collections, tot=total):
                try:
                    if not parent_frame.winfo_exists():
                        return
                    if hasattr(self, 'col_stats_lbl') and self.col_stats_lbl.winfo_exists():
                        self.col_stats_lbl.config(text=t)
                    try:
                        loading_lbl.destroy()
                    except tk.TclError:
                        pass
                    if not cols and offset == 0:
                        tk.Label(parent_frame, text=T(1999101125), font=FONT_BODY, bg=BG_MAIN, fg=FG_DIM).pack(pady=40)
                        return
                    self._build_collection_tiles(parent_frame, cols, tot)
                except tk.TclError:
                    pass

            self.after(0, _safe_update)
        except Exception as e:
            self.after(0, lambda e=e: loading_lbl.config(text=T(1999101392, e))
                       if loading_lbl.winfo_exists() else None)

    def _fetch_followed_collections(self, parent_frame, loading_lbl):
        """Renders tiles only for locally followed collections, fetching their details."""
        headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
        collections = []
        for cid in list(self._collection_follow_states.keys()):
            try:
                res = requests.get(f"{MODIO_BASE_URL}/games/11358/collections/{cid}", headers=headers, timeout=10)
                if res.status_code == 200:
                    collections.append(res.json())
            except Exception as e:
                print(f"Failed to fetch collection {cid}: {e}")

        def _safe_followed_update(cols=collections):
            try:
                if not parent_frame.winfo_exists():
                    return
                # Apply active tag filter client-side
                tag_filter = getattr(self, 'col_tag_filter', '')
                if tag_filter:
                    cols = [
                        c for c in cols
                        if any(
                            (t if isinstance(t, str) else t.get('name', '')) == tag_filter
                            for t in (c.get('tags') or [])
                        )
                    ]
                if hasattr(self, 'col_stats_lbl') and self.col_stats_lbl.winfo_exists():
                    self.col_stats_lbl.config(text=T(1999101378, len(cols)))
                try:
                    loading_lbl.destroy()
                except tk.TclError:
                    pass
                if not cols:
                    tk.Label(parent_frame, text=T(1999101126), font=FONT_BODY, bg=BG_MAIN, fg=FG_DIM).pack(pady=40)
                    return
                self._build_collection_tiles(parent_frame, cols, len(cols))
            except tk.TclError:
                pass

        self.after(0, _safe_followed_update)

    def _build_collection_tiles(self, parent_frame, collections, total):
        """Accumulates fetched collection data and triggers a virtual render."""
        try:
            if not parent_frame.winfo_exists(): return
        except tk.TclError:
            return

        if self.col_offset == 0:
            for rf in self._col_virt_rows.values():
                try: rf.destroy()
                except tk.TclError: pass
            self._col_virt_rows = {}
            self._all_col_data = []
            if getattr(self, "_col_load_more", None):
                try: self._col_load_more.destroy()
                except tk.TclError: pass
                self._col_load_more = None
            for w in parent_frame.winfo_children():
                try: w.destroy()
                except: pass

        self._all_col_data.extend(collections)
        self.col_offset = len(self._all_col_data)
        self._col_total_count = total

        n_rows  = (len(self._all_col_data) + _VR_C - 1) // _VR_C
        frame_h = n_rows * _VR_COL_H + (70
            if (self.col_offset < total and not getattr(self, "col_followed_only", tk.BooleanVar()).get())
            else 0)
        parent_frame.configure(height=frame_h)
        self.col_canvas.configure(scrollregion=(0, 0, self.col_canvas.winfo_width() or 1, frame_h))

        # Load More button via place()
        if getattr(self, "_col_load_more", None):
            try: self._col_load_more.destroy()
            except tk.TclError: pass
            self._col_load_more = None

        if (self.col_offset < total and not getattr(self, "col_followed_only", tk.BooleanVar()).get()):
            self._col_load_more = tk.Frame(parent_frame, bg=BG_SECTION, highlightthickness=1, highlightbackground=BG_SECTION, bd=0)
            self._col_load_more.place(x=0, y=n_rows * _VR_COL_H, relwidth=1, height=60)
            _cb = tk.Button(self._col_load_more, text=T(1999101124), font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, pady=10, relief="flat", bd=0, cursor="hand2", command=self._load_more_collections)
            _cb.pack(fill="both", expand=True)
            self._bind_border_button_hover(_cb, BG_SECTION, "#253b59")

        self._render_visible_col_rows()

    def _render_visible_col_rows(self):
        """Render only row frames near the current collections canvas viewport."""
        try:
            if not self.col_canvas.winfo_exists(): return
        except tk.TclError:
            return

        n_cols = len(self._all_col_data)
        if n_cols == 0:
            return

        n_rows = (n_cols + _VR_C - 1) // _VR_C
        y0_frac, y1_frac = self.col_canvas.yview()
        sr = self.col_canvas.cget("scrollregion")
        try:
            total_h = float(sr.split()[3]) if sr else n_rows * _VR_COL_H
        except (IndexError, ValueError):
            total_h = n_rows * _VR_COL_H

        view_top = y0_frac * total_h
        view_bot = y1_frac * total_h
        first_r = max(0, int(view_top / _VR_COL_H) - _VR_BUF)
        last_r = min(n_rows-1, int(view_bot / _VR_COL_H) + _VR_BUF)

        stale = [r for r in list(self._col_virt_rows) if r < first_r - _VR_BUF or r > last_r + _VR_BUF]
        for r in stale:
            try: self._col_virt_rows[r].destroy()
            except tk.TclError: pass
            del self._col_virt_rows[r]

        parent = self.col_scroll_frame
        for r in range(first_r, last_r + 1):
            if r in self._col_virt_rows:
                continue
            start = r * _VR_C
            row_cols = self._all_col_data[start : start + _VR_C]
            if not row_cols:
                continue
            row_frame = tk.Frame(parent, bg=BG_MAIN)
            for c in range(_VR_C):
                row_frame.columnconfigure(c, weight=1, minsize=370)
            row_frame.place(x=0, y=r * _VR_COL_H, relwidth=1, height=_VR_COL_H)
            for col_pos, col in enumerate(row_cols):
                self._build_collection_tile(row_frame, col, col_pos)
            self._col_virt_rows[r] = row_frame

    def _build_collection_tile(self, row_frame, col, col_pos):
        """Builds one collection tile at the given column position inside row_frame."""
        tile = tk.Frame(row_frame, bg=BG_SECTION, highlightbackground=FG_GOLD, highlightthickness=1, padx=15, pady=15)
        tile.grid(row=0, column=col_pos, padx=10, pady=10, sticky="nsew")
        tile.pack_propagate(False)
        tile.grid_propagate(False)
        tile.config(width=320, height=520)

        img_container = tk.Frame(tile, bg=BG_MAIN, width=290, height=163)
        img_container.pack_propagate(False)
        img_container.pack(fill="x", pady=(0, 10))
        img_lbl = tk.Label(img_container, text=T(1999101090), bg=BG_MAIN, fg=FG_DIM, cursor="hand2")
        img_lbl.pack(expand=True, fill="both")
        logo_url = (col.get("logo") or {}).get("thumb_320x180")
        if logo_url:
            threading.Thread(target=self._load_mod_image, args=(img_lbl, logo_url), daemon=True).start()

        content_frame = tk.Frame(tile, bg=BG_SECTION)
        content_frame.pack(fill="both", expand=True)

        raw_name = html.unescape(col.get("name", "Unknown Collection")).upper()
        display_name = (raw_name[:40] + "...") if len(raw_name) > 43 else raw_name
        title_lbl = tk.Label(content_frame, text=display_name, font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, wraplength=280, justify="left", anchor="nw", height=2, cursor="hand2")
        title_lbl.pack(fill="x")
        tk.Frame(content_frame, height=1, bg=FG_DIM).pack(fill="x", pady=(5, 5))

        meta = tk.Frame(content_frame, bg=BG_SECTION)
        meta.pack(fill="x", pady=(5, 2))
        author = (col.get("submitted_by") or {}).get("username", "Unknown")
        tk.Label(meta, text=author, font=FONT_SMALL, bg=BG_SECTION, fg="#07C1D8").pack(side="left")
        mod_count = (col.get("stats") or {}).get("mods_total", 0)
        _ico_mc = load_icon("install", (12, 12))
        tk.Label(meta, text=f"  {T(1999101407, mod_count) if mod_count == 1 else T(1999101408, mod_count)}", image=_ico_mc or "", compound="left" if _ico_mc else "none", font=FONT_SMALL, bg=BG_SECTION, fg=FG_DIM).pack(side="right")

        raw_tags = col.get("tags") or []
        tags_list = [t if isinstance(t, str) else t.get("name", "") for t in raw_tags]
        raw_t = " | ".join(tags_list) if tags_list else "No Tags"
        display_t = (raw_t[:72] + "...") if len(raw_t) > 75 else raw_t
        tk.Label(content_frame, text=display_t, font=FONT_XSMALL, bg=BG_SECTION, fg="#2ecc71", wraplength=280, justify="left", anchor="nw", height=2).pack(fill="x")

        summary = html.unescape(col.get("summary") or col.get("description_plaintext") or "No description.")
        summary_lbl = tk.Label(content_frame, text=summary[:200], font=FONT_SMALL, bg=BG_SECTION, fg="#bbbbbb", wraplength=280, justify="left", anchor="nw", cursor="hand2")
        summary_lbl.pack(fill="both", expand=True, pady=10)

        btn_frame = tk.Frame(tile, bg=BG_SECTION)
        btn_frame.pack(side="bottom", fill="x", pady=(10, 0))

        cid = str(col.get("id"))
        cname = html.unescape(col.get("name", ""))
        is_followed = cid in self._collection_follow_states
        col_url = (col.get("profile_url") or col.get("url")
                   or f"https://mod.io/g/anno-117-pax-romana/c/{col.get('name_id', '')}")

        _ico_cvis = load_icon("collection_visit", (14, 14))
        visit_btn = tk.Button(btn_frame, text=T(1999101168), font=FONT_XSMALL, bg=BG_MAIN, fg=FG_MAIN, relief="flat", cursor="hand2", image=_ico_cvis, compound="left" if _ico_cvis else "none", command=lambda u=col_url:webbrowser.open_new_tab(u))
        if _ico_cvis: visit_btn.image = _ico_cvis
        visit_btn.pack(side="left")
        self._bind_hover(visit_btn, BG_MAIN)

        for widget in [img_lbl, img_container, content_frame, summary_lbl, title_lbl]:
            widget.bind("<Button-1>", lambda e, c=col, u=col_url, ci=cid, cn=cname:self._show_collection_details(c, u, ci, cn))

        follow_area = tk.Frame(btn_frame, bg=BG_SECTION)
        follow_area.pack(side="right")
        if is_followed:
            self._apply_followed_state(follow_area, cid, cname)
        else:
            _ico_fol = load_icon("follow", (24, 24))
            btn_follow = tk.Button(follow_area, text=T(1999101179), font=FONT_UI_BOLD, bg="#2ecc71", fg="#000000", activebackground="#39f085", relief="flat", cursor="hand2", image=_ico_fol, compound="left" if _ico_fol else "none", command=lambda ci=cid, cn=cname, fa=follow_area: self._follow_collection(ci, cn, fa))
            if _ico_fol: btn_follow.image = _ico_fol
            btn_follow.pack()
            self._bind_hover(btn_follow, "#2ecc71", "#39f085")

    def _show_collection_details(self, col, col_url, cid, cname):
        """Opens a scrollable detail popup for a collection, listing all its mods."""
        detail_win = tk.Toplevel(self)
        detail_win.title(f"Collection: {cname}")

        win_w, win_h = 900, 850
        detail_win.geometry(f"{win_w}x{win_h}")
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        detail_win.geometry(f"+{x}+{y}")
        detail_win.configure(bg=BG_MAIN)
        detail_win.transient(self)
        detail_win.grab_set()

        # Footer
        footer = tk.Frame(detail_win, bg=BG_SECTION, pady=20, padx=40, bd=1, relief="raised")
        footer.pack(side="bottom", fill="x")

        def _cleanup():
            detail_win.unbind_all("<MouseWheel>")
            detail_win.grab_release()
            detail_win.destroy()
            self._bind_mousewheel_to_collections()

        close_btn = tk.Button(footer, text=T(1999101098), font=FONT_UI_BOLD, bg=BG_MAIN, fg=FG_MAIN, padx=20, cursor="hand2", command=_cleanup)
        close_btn.pack(side="left")
        self._bind_hover(close_btn, BG_MAIN, BG_HOVER)

        # Follow / Unfollow button in footer
        follow_area = tk.Frame(footer, bg=BG_SECTION)
        follow_area.pack(side="right")
        is_followed = cid in self._collection_follow_states
        if is_followed:
            self._apply_followed_state(follow_area, cid, cname)
        else:
            btn_fol = tk.Button(follow_area, text=T(1999101140), font=FONT_UI_BOLD, bg="#2ecc71", fg="#000000", width=12, cursor="hand2", relief="flat", command=lambda: self._follow_collection(cid, cname, follow_area))
            btn_fol.pack()
            self._bind_hover(btn_fol, "#2ecc71", "#39f085")

        # Scrollable content
        container = tk.Frame(detail_win, bg=BG_MAIN)
        container.pack(side="top", fill="both", expand=True)

        canvas = tk.Canvas(container, bg=BG_MAIN, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_MAIN)
        scroll_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(scroll_id, width=e.width))
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except Exception:
                pass
        detail_win.bind_all("<MouseWheel>", _on_mousewheel)
        detail_win.protocol("WM_DELETE_WINDOW", _cleanup)

        inner = tk.Frame(scroll_frame, bg=BG_MAIN, padx=40, pady=20)
        inner.pack(fill="both", expand=True)

        # Header
        tk.Label(inner, text=cname.upper(), font=FONT_TITLE, bg=BG_MAIN, fg=FG_MAIN, wraplength=750, justify="left").pack(anchor="w")

        author   = (col.get('submitted_by') or {}).get('username', 'Unknown')
        date_upd = datetime.fromtimestamp(col.get('date_updated', 0)).strftime('%Y-%m-%d')
        count_var = tk.StringVar(value=T(1999101090))
        tk.Label(inner, text=T(1999101377, author, date_upd), font=FONT_BODY, bg=BG_MAIN, fg="#07C1D8").pack(anchor="w", pady=(5, 2))
        tk.Label(inner, textvariable=count_var, font=FONT_XSMALL, bg=BG_MAIN, fg=FG_DIM).pack(anchor="w", pady=(0, 15))

        # Logo
        logo_url = (col.get('logo') or {}).get('original') or (col.get('logo') or {}).get('thumb_320x180')
        if logo_url:
            img_frame = tk.Frame(inner, bg=BG_SECTION, bd=1, relief="solid")
            img_frame.pack(fill="x", pady=(0, 15))
            img_lbl = tk.Label(img_frame, text=T(1999101090), bg=BG_SECTION, fg=FG_DIM, pady=80)
            img_lbl.pack(expand=True, fill="both")
            threading.Thread(target=self._load_large_image, args=(img_lbl, logo_url), daemon=True).start()

        # Description
        desc = html.unescape(col.get('description_plaintext') or col.get('summary') or '')
        if desc:
            tk.Frame(inner, height=1, bg=FG_DIM).pack(fill="x", pady=10)
            tk.Label(inner, text=desc, font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, wraplength=780, justify="left").pack(anchor="w")

        # Mod list
        tk.Frame(inner, height=1, bg=FG_DIM).pack(fill="x", pady=15)
        tk.Label(inner, text=T(1999101127), font=FONT_UI_BOLD, bg=BG_MAIN, fg=FG_DIM).pack(anchor="w", pady=(0, 10))

        mod_list_frame = tk.Frame(inner, bg=BG_MAIN)
        mod_list_frame.pack(fill="x")

        loading_mods = tk.Label(mod_list_frame, text=T(1999101128), font=FONT_BODY, bg=BG_MAIN, fg=FG_DIM)
        loading_mods.pack(anchor="w")

        def fetch_mods():
            try:
                headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
                res = requests.get(
                    f"{MODIO_BASE_URL}/games/11358/collections/{cid}/mods?_limit=100",
                    headers=headers, timeout=15)
                mods = res.json().get('data', []) if res.status_code == 200 else []
                self.after(0, lambda: render_mods(mods))
            except Exception as e:
                self.after(0, lambda: loading_mods.config(text=T(1999101403, e)))

        def render_mods(mods):
            try:
                loading_mods.destroy()
            except tk.TclError:
                return
            count_var.set(T(1999101451, len(mods)) if len(mods) == 1 else T(1999101452, len(mods)))
            if not mods:
                tk.Label(mod_list_frame, text=T(1999101129), font=FONT_BODY, bg=BG_MAIN, fg=FG_DIM).pack(anchor="w")
                return
            for mod in mods:
                mname   = html.unescape(mod.get('name', 'Unknown Mod'))
                mauthor = (mod.get('submitted_by') or {}).get('username', '')
                mrow = tk.Frame(mod_list_frame, bg=BG_SECTION, pady=6, padx=12, highlightthickness=1, highlightbackground=FG_SEPARATOR)
                mrow.pack(fill="x", pady=3)

                murl = mod.get('profile_url', '')
                mlbl = tk.Label(mrow, text=mname, font=FONT_BOLD_SMALL, bg=BG_SECTION, fg=FG_GOLD, anchor="w", cursor="hand2")
                mlbl.pack(side="left")
                if murl:
                    mlbl.bind("<Button-1>", lambda e, u=murl: webbrowser.open_new_tab(u))
                if mauthor:
                    tk.Label(mrow, text=T(1999101376, mauthor), font=FONT_XSMALL, bg=BG_SECTION, fg=FG_DIM).pack(side="right")

        threading.Thread(target=fetch_mods, daemon=True).start()

    def _bind_mousewheel_to_collections(self):
        """Re-establishes scrolling for the Collections canvas after a popup closes."""
        if hasattr(self, 'col_canvas') and self.col_canvas.winfo_exists():
            self.bind_all("<MouseWheel>", lambda e: self.col_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def _apply_followed_state(self, follow_area, collection_id, collection_name):
        """Rebuilds follow_area as ↻ REFRESH + ★ FOLLOWED."""
        try:
            for w in follow_area.winfo_children():
                w.destroy()

            def _confirm_refresh():
                if self._imperial_question(T(1999101308), T(1999101362, collection_name)):
                    threading.Thread(target=self._install_collection_mods, args=(collection_id, collection_name, None), daemon=True).start()

            _ico_cref = load_icon("reinstall", (22, 22))
            refresh_btn = tk.Button(follow_area, text="" if _ico_cref else "↻", font=FONT_SMALL, bg=BG_MAIN, fg=FG_MAIN, relief="flat", cursor="hand2", padx=6, image=_ico_cref, compound="center" if _ico_cref else "none", command=_confirm_refresh)
            if _ico_cref: refresh_btn.image = _ico_cref
            refresh_btn.pack(side="left")
            self._bind_hover(refresh_btn, BG_MAIN)
            self._attach_tooltip(refresh_btn, T(1999101274))

            _ico_fols  = load_icon("followed_state", (24, 24))
            _ico_unfol = load_icon("unfollow", (24, 24))
            fol_btn = tk.Button(follow_area, text=T(1999101180), font=FONT_UI_BOLD, bg=FG_GOLD, fg="#000000", relief="flat", cursor="hand2", padx=6, image=_ico_fols, compound="left" if _ico_fols else "none")
            if _ico_fols: fol_btn.image = _ico_fols
            fol_btn.pack(side="left", padx=(4, 0))

            def on_enter(e):
                fol_btn.config(text=T(1999101181), bg="#c0392b", fg=FG_MAIN, image=_ico_unfol or _ico_fols, compound="left" if (_ico_unfol or _ico_fols) else "none")
            def on_leave(e):
                fol_btn.config(text=T(1999101180), bg=FG_GOLD, fg="#000000", image=_ico_fols, compound="left" if _ico_fols else "none")

            fol_btn.bind("<Enter>", on_enter)
            fol_btn.bind("<Leave>", on_leave)
            fol_btn.config(command=lambda: self._unfollow_collection(
                collection_id, collection_name, follow_area))
        except tk.TclError:
            pass

    def _load_more_collections(self):
        """Fetches the next batch of collections (virtual-scroll aware)."""
        if getattr(self, "_col_load_more", None):
            try: self._col_load_more.destroy()
            except tk.TclError: pass
            self._col_load_more = None
        n_rows = (len(getattr(self, "_all_col_data", [])) + _VR_C - 1) // _VR_C
        load_lbl = tk.Label(self.col_scroll_frame, text=T(1999101096), bg=BG_MAIN, fg=FG_DIM)
        load_lbl.place(x=0, y=n_rows * _VR_COL_H, relwidth=1, height=40)
        q = self.col_search_var.get() if hasattr(self, "col_search_var") else ""
        tag = getattr(self, "col_tag_filter", "")
        threading.Thread(target=self._fetch_collections_worker, args=(self.col_scroll_frame, load_lbl, q, self.col_offset, tag), daemon=True).start()

    def _follow_collection(self, collection_id, collection_name, follow_area):
        """Follows the collection on mod.io and installs all its mods."""
        follow_area.winfo_children()[0].config(state="disabled", text=T(1999101132))

        def task():
            headers = {
                'Authorization': f'Bearer {self.modio_token}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }
            try:
                res = requests.post(
                    f"{MODIO_BASE_URL}/games/11358/collections/{collection_id}/followers",
                    headers=headers, timeout=10)
                success = res.status_code in (200, 201)
                if not success and res.status_code == 400:
                    try:
                        success = res.json().get('error', {}).get('error_ref') == 15004
                    except Exception:
                        pass

                if success:
                    ts = datetime.now().timestamp()
                    self._collection_follow_states[str(collection_id)] = {
                        "name": collection_name, "last_seen_ts": ts
                    }
                    self._save_collection_follows()
                    self.after(0, lambda: self._apply_followed_state(
                        follow_area, str(collection_id), collection_name))
                    # Install all mods in the collection
                    self._install_collection_mods(collection_id, collection_name, follow_area)
                else:
                    err = res.text[:200]
                    self.after(0, lambda: self._imperial_alert(T(1999101319), T(1999101421, err), is_error=True))
                    self.after(0, lambda: follow_area.winfo_children()[0].config(
                        state="normal", text=T(1999101140)))
            except Exception as e:
                self.after(0, lambda: self._imperial_alert(T(1999101189), T(1999101422, e), is_error=True))

        threading.Thread(target=task, daemon=True).start()

    def _install_collection_mods(self, collection_id, collection_name, follow_area):
        """Fetches all mods in a collection, subscribes to each on mod.io and downloads/installs any not yet present locally."""

        # --- Progress window (must be created on main thread) ---
        prog_win = tk.Toplevel(self)
        prog_win.title(T(1999101133))
        win_w, win_h = 480, 220
        prog_win.geometry(f"{win_w}x{win_h}")
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        prog_win.geometry(f"+{x}+{y}")
        prog_win.configure(bg=BG_SECTION)
        prog_win.transient(self)
        prog_win.grab_set()
        prog_win.resizable(False, False)

        tk.Label(prog_win, text=collection_name.upper(), font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, wraplength=440).pack(pady=(20, 5))

        phase_lbl = tk.Label(prog_win, text=T(1999101134), font=FONT_SMALL, bg=BG_SECTION, fg=FG_DIM)
        phase_lbl.pack()

        mod_lbl = tk.Label(prog_win, text="", font=FONT_XSMALL, bg=BG_SECTION, fg="#2ecc71", wraplength=440)
        mod_lbl.pack(pady=(2, 10))

        progress = ttk.Progressbar(prog_win, orient="horizontal", length=400, mode="determinate")
        progress.pack(pady=(0, 20))

        def _set_phase(text):
            self.after(0, lambda: phase_lbl.config(text=text))

        def _set_mod(text):
            self.after(0, lambda: mod_lbl.config(text=text))

        def _set_progress(val):
            self.after(0, lambda: progress.config(value=val))

        def _close_progress():
            try:
                prog_win.grab_release()
                prog_win.destroy()
            except tk.TclError:
                pass

        def task():
            headers = {
                'Authorization': f'Bearer {self.modio_token}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }
            try:
                res = requests.get(f"{MODIO_BASE_URL}/games/11358/collections/{collection_id}/mods", headers=headers, timeout=15)
                if res.status_code != 200:
                    self.after(0, _close_progress)
                    print(f"[Collection] Could not fetch mods for collection {collection_id}")
                    return

                mods = res.json().get('data', [])
                if not mods:
                    self.after(0, _close_progress)
                    return

                installed_names = {
                    m.get('name', '').lower().replace(' ', '')
                    for m in self.get_all_mod_metadata()
                }

                total_mods = len(mods)
                to_install  = []

                # Phase 1 - Subscribe all mods (0–50% of bar)
                _set_phase(T(1999101441, total_mods))
                for idx, mod in enumerate(mods):
                    mid   = str(mod.get('id'))
                    mname = html.unescape(mod.get('name', ''))
                    _set_mod(mname)
                    _set_progress((idx / total_mods) * 50)

                    try:
                        sub_res = requests.post(
                            f"{MODIO_BASE_URL}/games/11358/mods/{mid}/subscribe",
                            headers=headers,
                            data={'include_dependencies': 'false'},
                            timeout=10)
                        success = sub_res.status_code in (200, 201)
                        if not success and sub_res.status_code == 400:
                            err_ref = sub_res.json().get('error', {}).get('error_ref', 0)
                            success = (err_ref == 15004)
                        if success:
                            self._subscription_states[mid] = True
                            # Removed premature mapping from here
                    except Exception as e:
                        print(f"[Collection] Subscribe failed for '{mname}': {e}")

                    if mname.lower().replace(' ', '') not in installed_names:
                        dl_url = (mod.get('modfile') or {}).get('download', {}).get('binary_url')
                        if dl_url:
                            to_install.append((mid, mname, dl_url))
                    else:
                        # Only attempt fuzzy-mapping if the mod is ALREADY installed locally. (If it's in to_install, run_install_logic will map it perfectly during extraction).
                        self._store_modio_mapping(mid, mname)

                self._save_subscriptions()
                _set_progress(50)

                # Phase 2 - Download + install missing mods (50–100% of bar)
                if not to_install:
                    _set_progress(100)
                    _set_phase(T(1999101442))
                    _set_mod("")
                    if str(collection_id) in self._collection_follow_states:
                        self._collection_follow_states[str(collection_id)]['last_seen_ts'] = datetime.now().timestamp()
                        self._save_collection_follows()
                    # All mods already installed — still create the collection preset
                    self.mods = self.get_all_mod_metadata()
                    rev = {v: k for k, v in self._subscription_modio_map.items()}
                    already_ids = []
                    for mod in mods:
                        local_id = rev.get(str(mod.get('id', '')))
                        if local_id:
                            already_ids.append(local_id)
                    import time as _time
                    _time.sleep(0.8)
                    self.after(0, _close_progress)
                    self.after(0, lambda: self._imperial_alert(T(1999101305), T(1999101404, collection_name)))
                    self.after(0, lambda ids=already_ids, pn=collection_name: self._create_collection_preset(pn, ids))
                    return

                _set_phase(T(1999101443, len(to_install)))
                for idx, (mid, mname, dl_url) in enumerate(to_install):
                    _set_mod(mname)
                    _set_progress(50 + (idx / len(to_install)) * 50)
                    try:
                        import tempfile as _tf
                        _tmp_dir = _tf.mkdtemp(prefix="anno117_col_")
                        safe  = "".join(c for c in mname if c.isalnum() or c in (' ', '_')).rstrip()
                        zpath = os.path.join(_tmp_dir, f"{safe.replace(' ', '_')}.zip")
                        r = requests.get(dl_url, stream=True, timeout=30)
                        r.raise_for_status()
                        with open(zpath, 'wb') as f:
                            for chunk in r.iter_content(8192):
                                f.write(chunk)
                        done_ev = threading.Event()
                        def _col_install(zp=zpath, td=_tmp_dir, m=mid, mn=mname, ev=done_ev):
                            self._silent_finalize(zp, m, mn)
                            shutil.rmtree(td, ignore_errors=True)
                            ev.set()
                        self.after(0, _col_install)
                        done_ev.wait()
                    except Exception as e:
                        print(f"[Collection] Failed to install '{mname}': {e}")

                _set_progress(100)
                _set_phase(T(1999101444))
                _set_mod("")

                if str(collection_id) in self._collection_follow_states:
                    self._collection_follow_states[str(collection_id)]['last_seen_ts'] = datetime.now().timestamp()
                    self._save_collection_follows()

                # Resolve local ModIDs using the subscription map (populated during the subscribe loop above) — more reliable than name-matching
                self.mods = self.get_all_mod_metadata()
                # Build reverse map: modio_id → local_mod_id
                rev = {v: k for k, v in self._subscription_modio_map.items()}
                local_mod_ids = []
                for mod in mods:
                    mid_str = str(mod.get('id', ''))
                    local_id = rev.get(mid_str)
                    if local_id:
                        local_mod_ids.append(local_id)
                    else:
                        # Fallback: name match for mods whose mapping wasn't stored yet
                        import re as _re
                        def _tok(s): return set(_re.sub(r'[^a-z0-9]', ' ', s.lower()).split())
                        mname = html.unescape(mod.get('name', ''))
                        mtok  = _tok(mname)
                        local = next(
                            (m for m in self.mods
                             if not m.get('parent_path')
                             and (m.get('name', '').lower().replace(' ', '') == mname.lower().replace(' ', '')
                                  or _tok(m.get('name', '')).issubset(mtok)
                                  or mtok.issubset(_tok(m.get('name', ''))))),
                            None)
                        if local:
                            local_mod_ids.append(local['id'])

                import time as _time
                _time.sleep(0.8)
                self.after(0, _close_progress)

                installed_names_list = [mn for _, mn, _ in to_install]
                preset_name = f"{collection_name}"

                self.after(0, lambda: self._imperial_alert(T(1999101306), T(1999101405, collection_name, "\n".join(f"  ✔  {name}" for name in installed_names_list)), scrollable=True))

                self.after(0, lambda ids=local_mod_ids, pn=preset_name:self._create_collection_preset(pn, ids))

            except Exception as e:
                self.after(0, _close_progress)
                print(f"[Collection] Install error: {e}")

        threading.Thread(target=task, daemon=True).start()

    def _unfollow_collection(self, collection_id, collection_name, follow_area):
        """Prompts the user, unfollows on mod.io, and optionally removes all collection mods."""
        msg = T(1999101363, collection_name)

        win_w, win_h = 600, 360
        unf_win = tk.Toplevel(self)
        unf_win.title(T(1999101135))
        unf_win.geometry(f"{win_w}x{win_h}")
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (win_w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (win_h // 2)
        unf_win.geometry(f"+{x}+{y}")
        unf_win.configure(bg=BG_MAIN)
        unf_win.transient(self)
        unf_win.grab_set()

        result = {"ans": None}
        def _sel(v):
            result["ans"] = v
            unf_win.destroy()

        tk.Label(unf_win, text=T(1999101136), font=FONT_TITLE, bg=BG_MAIN, fg="#e74c3c").pack(pady=(22, 8))
        tk.Label(unf_win, text=msg, font=FONT_BODY, bg=BG_MAIN, fg=FG_MAIN, wraplength=540, justify="center").pack(pady=8, expand=True)

        btn_f = tk.Frame(unf_win, bg=BG_MAIN)
        btn_f.pack(pady=(0, 24))
        _ico_ufr = load_icon("unfollow_remove", (14, 14))
        btn_unfollowuninstall = tk.Button(btn_f, text=T(1999101137), font=FONT_UI_BOLD, bg="#c0392b", fg=FG_MAIN, cursor="hand2", relief="raised", image=_ico_ufr, compound="left" if _ico_ufr else "none", command=lambda: _sel("remove"))
        if _ico_ufr: btn_unfollowuninstall.image = _ico_ufr
        btn_unfollowuninstall.pack(side="left", padx=8)
        self._bind_hover(btn_unfollowuninstall, "#c0392b", "#db4332")
        _ico_ufo = load_icon("unfollow_only", (14, 14))
        btn_unfollow = tk.Button(btn_f, text=T(1999101138), font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_MAIN, cursor="hand2", relief="raised", image=_ico_ufo, compound="left" if _ico_ufo else "none", command=lambda: _sel("unfollow"))
        if _ico_ufo: btn_unfollow.image = _ico_ufo
        btn_unfollow.pack(side="left", padx=8)
        self._bind_hover(btn_unfollow, BG_SECTION, BG_HOVER)
        btn_back = tk.Button(btn_f, text=T(1999101037), font=FONT_UI_BOLD, bg=BG_SECTION, fg=FG_DIM, width=10, cursor="hand2", relief="raised", command=lambda: _sel(None))
        btn_back.pack(side="left", padx=8)
        self._bind_hover(btn_back, BG_SECTION, BG_HOVER)
        self.wait_window(unf_win)

        if result["ans"] is None:
            return

        remove_mods = (result["ans"] == "remove")

        def task():
            headers = {
                'Authorization': f'Bearer {self.modio_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            try:
                requests.delete(
                    f"{MODIO_BASE_URL}/games/11358/collections/{collection_id}/followers",
                    headers=headers, timeout=10)

                cid_str = str(collection_id)
                if cid_str in self._collection_follow_states:
                    del self._collection_follow_states[cid_str]
                    self._save_collection_follows()

                if remove_mods:
                    # Fetch collection mods and remove those not needed elsewhere
                    res = requests.get(f"{MODIO_BASE_URL}/games/11358/collections/{collection_id}/mods?_limit=100", headers=headers, timeout=15)
                    if res.status_code == 200:
                        col_mods = res.json().get('data', [])
                        for mod in col_mods:
                            mid     = str(mod.get('id'))
                            mname   = html.unescape(mod.get('name', ''))
                            requests.delete(
                                f"{MODIO_BASE_URL}/games/11358/mods/{mid}/subscribe",
                                headers=headers, timeout=10)
                            if mid in self._subscription_states:
                                del self._subscription_states[mid]
                            self._delete_unsubscribed_mod(mid, mname)
                        self._save_subscriptions()

                # Delete the collection preset - mirror exact naming from _create_collection_preset
                safe_name    = "".join(
                    c for c in collection_name if c.isalnum() or c in (' ', '-', '_')).strip()
                display_name = f"{safe_name} (Collection)"
                preset_path  = os.path.join(self.presets_dir, f"{display_name}.txt")
                if os.path.exists(preset_path):
                    try:
                        os.remove(preset_path)
                        if self.current_profile_name == display_name:
                            self.after(0, self.reset_to_default_profile)
                            self.current_profile_name = "Default"
                        self.after(0, self.refresh_presets_list)
                    except Exception as e:
                        print(f"[Unfollow] Could not delete preset: {e}")

                self.after(0, lambda: self._apply_follow_btn_after_unfollow(follow_area, cid_str, collection_name))
                self.after(0, lambda: self._imperial_alert(T(1999101307), T(1999101366, collection_name)))
            except Exception as e:
                self.after(0, lambda: self._imperial_alert(T(1999101189), T(1999101406, e), is_error=True))

        threading.Thread(target=task, daemon=True).start()

    def _apply_follow_btn_after_unfollow(self, follow_area, collection_id, collection_name):
        """After unfollowing a collection, either removes the tile entirely (when the followed-only filter is active) or swaps its button back to the FOLLOW state."""
        try:
            # In followed-only view the tile should disappear; in all-collections view just swap the button back to FOLLOW.
            if hasattr(self, 'col_followed_only') and self.col_followed_only.get():
                # Walk up to the tile frame (follow_area → btn_frame → tile)
                tile = follow_area.master.master
                tile.destroy()
                # Update the canvas scroll region after removing the tile
                if hasattr(self, 'col_canvas'):
                    self.col_canvas.update_idletasks()
                    self.col_canvas.configure(scrollregion=self.col_canvas.bbox("all"))
            else:
                for w in follow_area.winfo_children():
                    w.destroy()
                _ico_rfl = load_icon("follow", (14, 14))
                btn = tk.Button(follow_area, text=T(1999101179), font=FONT_UI_BOLD, bg="#2ecc71", fg="#000000", activebackground="#39f085", relief="flat", cursor="hand2", image=_ico_rfl, compound="left" if _ico_rfl else "none", command=lambda: self._follow_collection(collection_id, collection_name, follow_area))
                if _ico_rfl: btn.image = _ico_rfl
                btn.pack()
                self._bind_hover(btn, "#2ecc71", "#39f085")
        except tk.TclError:
            pass

    def _open_collection_tab(self, collection_id):
        """Switches to Collections tab and highlights the given collection."""
        self.switch_tab("Collections")
        # After the tab renders, search for this collection
        def _highlight():
            if hasattr(self, 'col_search_var'):
                cid_str = str(collection_id)
                info = self._collection_follow_states.get(cid_str, {})
                name = info.get('name', '') if isinstance(info, dict) else ''
                if name:
                    self.col_search_var.set(name)
                self._refresh_collections()
        self.after(300, _highlight)

    def _fetch_collection_updates_worker(self, done_cb):
        """Checks followed collections for updates since last seen and generates news items."""
        items = []
        if not self.modio_token or not self._collection_follow_states:
            done_cb(items)
            return
        try:
            headers = {'Authorization': f'Bearer {self.modio_token}', 'Accept': 'application/json'}
            for cid, info in self._collection_follow_states.items():
                if not isinstance(info, dict):
                    continue
                last_seen = info.get('last_seen_ts', 0)
                cname = info.get('name', f'Collection {cid}')
                try:
                    res = requests.get(
                        f"{MODIO_BASE_URL}/games/11358/collections/{cid}",
                        headers=headers, timeout=10)
                    if res.status_code != 200:
                        continue
                    col = res.json()
                    ts = float(col.get('date_updated') or 0)
                    if ts <= last_seen:
                        continue
                    dt = datetime.fromtimestamp(ts)
                    mod_count = col.get('mod_count', 0)
                    items.append({
                        "title": f"Collection Updated: {cname}",
                        "url": col.get('profile_url', ''),
                        "date": dt.strftime('%b %d, %Y'),
                        "excerpt": f"This collection was updated and now contains {mod_count} mod(s). Open the Collections tab to refresh your installed mods.",
                        "img_url": (col.get('logo') or {}).get('thumb_320x180'),
                        "source": "collection_update",
                        "sort_ts": ts,
                        "badge_text": "📦 COLLECTION",
                        "badge_color": "#8e44ad",
                        "collection_id": cid,
                        "collection_name": cname,
                    })
                except Exception as e:
                    print(f"[CollectionNews] Failed for {cid}: {e}")
        except Exception as e:
            print(f"[CollectionNews] Worker error: {e}")
        finally:
            done_cb(items)

    def _create_collection_preset(self, preset_name, mod_ids):
        """Creates a preset with collection mods active and all other installed mods explicitly commented out, then loads it and switches to Activation."""
        safe_name = "".join(
            c for c in preset_name if c.isalnum() or c in (' ', '-', '_')).strip()
        display_name = f"{safe_name} (Collection)"
        file_path = os.path.join(self.presets_dir, f"{display_name}.txt")

        try:
            active_set = set(mod_ids)
            # Force fresh scan so mods installed by _silent_finalize are included
            self.mods = self.get_all_mod_metadata()
            all_mods  = self.mods
            top_mods  = [m for m in all_mods if not m.get("parent_path")]
            # Expand active_set: translate modio numeric IDs to local ModIDs so the preset correctly activates collection mods
            rev = {v: k for k, v in self._subscription_modio_map.items()}
            for cid in list(active_set):
                local_id = rev.get(str(cid))
                if local_id:
                    active_set.add(local_id)

            lines = [f"# {safe_name}\n", "# EnableNewMods\n"]  # new mods OFF by default
            for m in top_mods:
                if m['id'] in active_set:
                    lines.append(f"{m['id']}\n")          # active
                else:
                    lines.append(f"# {m['id']}\n")        # explicitly inactive

            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            # Load as active profile
            if os.path.exists(self.active_profile_path):
                shutil.copy2(self.active_profile_path, self.active_profile_path + ".bak")
            self._apply_preset_with_full_coverage(file_path)

            self.current_profile_name = display_name
            self.refresh_presets_list()
            self.save_settings()

            if getattr(self, 'jump_to_activation', True):
                self.switch_tab("Mod Activation")

        except Exception as e:
            print(f"[CollectionPreset] Failed to create preset: {e}")



# --- Debug log redirector — captures all print() output to a file ---
class _LogRedirector:
    """Tees stdout/stderr to both the original stream and a rolling log file."""
    def __init__(self, original, log_path):
        """Stores the original stream and the path to the rolling log file that all output is mirrored to."""
        self._orig     = original
        self._path     = log_path
        self._encoding = "utf-8"

    def write(self, msg):
        """Writes msg to both the original stream and the rolling log file on disk."""
        try:
            self._orig.write(msg)
        except Exception:
            pass
        try:
            with open(self._path, "a", encoding=self._encoding) as f:
                f.write(msg)
        except Exception:
            pass

    def flush(self):
        """Flushes the original stream, ignoring any errors."""
        try:
            self._orig.flush()
        except Exception:
            pass

def _init_log_redirector():
    """Points stdout and stderr at a log file inside %APPDATA%."""
    if IS_WINDOWS:
        appdata = (os.getenv("APPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Roaming"))
    else:
        appdata = (os.getenv("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config"))
    log_dir = os.path.join(appdata, "Anno 117 Mod Manager")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "debug.log")
    # Roll over if file exceeds 2 MB
    try:
        if os.path.exists(log_path) and os.path.getsize(log_path) > 2 * 1024 * 1024:
            bak = log_path + ".bak"
            if os.path.exists(bak):
                os.remove(bak)
            os.rename(log_path, bak)
    except Exception:
        pass
    # Write session header
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*60}\n"
                    f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"{'='*60}\n")
    except Exception:
        pass
    sys.stdout = _LogRedirector(sys.stdout, log_path)
    sys.stderr = _LogRedirector(sys.stderr, log_path)
    return log_path

_debug_log_path = _init_log_redirector()

if __name__ == "__main__":
    # Required for PyInstaller --onefile on Windows with multiprocessing
    import multiprocessing
    multiprocessing.freeze_support()
    app = AnnoModManagerApp()
    app.mainloop()