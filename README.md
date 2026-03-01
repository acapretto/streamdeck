# Stream Deck Profiles

Installer and profile definitions for a Stream Deck 31 (3×5, 15 keys).

## Device
- **Model**: 20GBA9901
- **UUID**: `@(1)[4057/128/DL10L1A31880]`
- **Layout**: 3 columns × 5 rows = 15 keys

## Structure

```
streamdeck_installer.py   # Core installer — handles all V3 format complexity
profiles/
  finder.py               # Finder profile (clipboard slots, prompts, system tools)
  obs.py                  # OBS Studio (scenes, recording, callouts)
  fcp.py                  # Final Cut Pro basic (transport + editing tools)
  fcp_advanced.py         # Final Cut Pro advanced (complex multi-step workflows)
macros/
  SD_Finder_Macros.kmmacros  # Keyboard Maestro macros — double-click to import
```

## Installing a Profile

Stream Deck **must be closed** before running.

```bash
python3 profiles/finder.py
python3 profiles/obs.py
python3 profiles/fcp.py
python3 profiles/fcp_advanced.py
```

Reopen Stream Deck after running. Profiles auto-activate when the associated app is frontmost.

## Finder Profile Setup

After installing `finder.py`:

1. **Import KM macros** — double-click `macros/SD_Finder_Macros.kmmacros`
2. **Add hold actions** to the 3 Clip Slot buttons in Stream Deck UI:
   - Right-click → Add Hold Action → set to `Ctrl+Opt+Cmd+1` (or 2, 3)
3. **Assign Apple Shortcut hotkeys** in Shortcuts.app (Hyper = Ctrl+Shift+Opt+Cmd):
   - Tile Last 4 Windows → `Hyper+W`
   - Dictation and Paste → `Hyper+D`
   - Make QR Code → `Hyper+Q`
   - Shorten URL → `Hyper+U`
   - Universal Input → `Hyper+I`
4. **Set Snagit hotkey** → `Cmd+Shift+C` in Snagit preferences

## Adding a New Profile

```python
from streamdeck_installer import install_profile

buttons = [
    {"label": "Play",   "key": "space"},
    {"label": "Undo",   "key": "z", "mods": ["cmd"]},
    {"label": "Export", "key": "e", "mods": ["cmd", "shift"]},
    # With icon:
    {"label": "Record", "key": "r", "mods": ["shift", "ctrl"],
     "icon": "record.circle.fill", "color": "red"},
    # Multi-action:
    {"label": "Go Home", "actions": [
        {"key": "home"},
        {"key": "space"},
    ], "icon": "play.circle.fill", "color": "green"},
]

install_profile("My App", buttons, app="/Applications/MyApp.app")
```

**Modifier names**: `"cmd"`, `"shift"`, `"opt"`, `"ctrl"`

**Special keys**: `"space"`, `"return"`, `"escape"`, `"delete"`, `"tab"`,
`"home"`, `"end"`, `"page_up"`, `"page_down"`, `"up"`, `"down"`, `"left"`, `"right"`, `"f1"`–`"f20"`

**Icon colors**: `"blue"`, `"purple"`, `"orange"`, `"teal"`, `"red"`, `"green"`, `"gray"`

Icons use SF Symbols (requires macOS + PyObjC). Pillow required for label rendering:
```bash
pip3 install pillow
```
