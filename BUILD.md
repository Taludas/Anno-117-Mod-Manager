# Build and Installation

The Anno 117 Mod Manager can be built into a standalone `.exe` using PyInstaller. The repository ships a Makefile for the Windows build, but the entry point in the Makefile (`PACKAGE = anno117-modmanager`) still points at the **legacy Tk script** — the new pywebview app lives in `app.py`. Until the Makefile is updated, run PyInstaller against `app.py` directly.

## Prerequisites

- Python 3.10 or newer — [python.org](https://www.python.org/downloads/)
- The Microsoft Edge **WebView2** runtime (preinstalled on Windows 10 21H1+ and Windows 11; otherwise grab the [Evergreen Bootstrapper](https://developer.microsoft.com/en-us/microsoft-edge/webview2/))
- Optional: GNU Make for Windows — `winget install GnuWin32.Make` or `choco install make`

## Build Steps

**1. Create the virtual environment** (run this outside any existing venv):

```
python -m venv .tamm.venv
```

**2. Activate the virtual environment:**

```
.tamm.venv\Scripts\activate
```

**3. Install runtime dependencies + PyInstaller:**

```
pip install pywebview requests pyinstaller
```

(`requirements.txt` in the repo root is currently stale — it still lists `Pillow`, `bs4`, `beautifulsoup4` and `tkinterdnd2`, none of which the pywebview app imports. Installing them is harmless but adds nothing.)

**4. Build the executable** (against `app.py`, not the legacy script):

```
pyinstaller --onefile --windowed ^
    --add-data "data;data" ^
    --add-data "frontend;frontend" ^
    --add-data "_version.py;." ^
    --icon="app_icon.ico" ^
    --version-file="file_version_info.txt" ^
    --name "Anno 117 Mod Manager" app.py
```

Both `data` (icons, fonts) and `frontend` (HTML / CSS / JS / Alpine vendor file) must be bundled — the runtime resolves them via `resource_path()` in `app.py`, which falls back to `sys._MEIPASS` when frozen.

The finished executable will be placed in the `dist` subdirectory as `Anno 117 Mod Manager.exe`.

**5. Test the executable:**

```
dist\Anno 117 Mod Manager.exe
```

If the window opens blank, re-run the build with `--debug=all` and check the console for missing files — the most common cause is forgetting `--add-data "frontend;frontend"`.

## Linux / macOS

A frozen build is not currently part of the release pipeline — Linux users run from source. PyInstaller works on Linux/macOS too (drop the `.exe` extension and swap the `;` separator for `:` in `--add-data`), but you'll have to bundle WebKit2GTK / WKWebView dependencies yourself; the simpler path is `python app.py` from a virtualenv built with `--system-site-packages` so PyGObject (`gi`) resolves.

## Cleanup

```
rd /s /q build
del /q dist\*
del /q "Anno 117 Mod Manager.spec"
```

Then deactivate and remove the virtual environment:

```
deactivate
rd /s /q .tamm.venv
```

## Notes

- The `data` and `frontend` folders are bundled into the executable via the `--add-data` flags. Do not move or rename them before building.
- If you see "no frontend/index.html" or font/icon errors when launching the exe, you almost certainly missed `--add-data "frontend;frontend"`. Force a clean rebuild after fixing.
- Set `ANNO117_DEBUG=1` in the environment before launching to open the embedded webview's devtools at startup — useful when chasing frontend issues in a frozen build.

## Debugging the Frozen Build

Frozen pywebview apps can fail silently on Windows when WebView2 is missing — the window opens, stays blank, and there's no error message. Symptoms:

- `dist\Anno 117 Mod Manager.exe` window is empty / white.
- The terminal prints nothing useful.

Fix: install the WebView2 Evergreen Bootstrapper, then re-launch.
