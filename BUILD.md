# Build and Installation

The Anno 117 Mod Manager can be built into a standalone `.exe` using PyInstaller, controlled via a Makefile.

## Prerequisites

- Python 3.10 or newer — [python.org](https://www.python.org/downloads/)
- GNU Make for Windows — install via winget:
  ```
  winget install GnuWin32.Make
  ```
  or via Chocolatey:
  ```
  choco install make
  ```

## Build Steps

**1. Create the virtual environment** (run this outside of any existing venv):
```
make venv
```

**2. Activate the virtual environment:**
```
.tamm.venv\Scripts\activate
```

**3. Install dependencies and build the executable:**
```
make all
```

The finished executable will be placed in the `dist` subdirectory as `Anno 117 Mod Manager.exe`.

**4. Test the executable:**
```
dist\Anno 117 Mod Manager.exe
```

## Cleanup

To remove build artefacts while still inside the virtual environment:
```
make clean
```

Then deactivate and remove the virtual environment:
```
deactivate
make venv.clean
```

## Notes

- The `data` folder (containing icons, fonts and UI assets) is automatically bundled into the executable via the `--add-data "data;data"` flag in the Makefile. Do not move or rename this folder before building.
- If you see font or icon errors when launching the exe, run `make exe.clean` followed by `make exe` to force a clean rebuild.
- The `requirements.txt` file must be present in the project root before running `make all`. It should contain at minimum:
  ```
    pillow
    requests
    bs4
    beautifulsoup4
    tkinterdnd2
    pyinstaller
  ```