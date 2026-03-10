# Stream Deck Profile Installer (macOS)

Define Stream Deck profiles in Python. Skip the drag-and-drop UI — write your buttons as code, run a script, done.

Supports hotkeys, multi-actions, app launchers, auto-generated SF Symbol icons, multi-page profiles, and OBS Studio plugin actions (scenes, source visibility, multi-action switches).

**macOS only** — uses native keycodes and the Stream Deck V3 profile format.

## Why This Exists

The Stream Deck UI is fine for a few buttons, but painful when you have multiple profiles with dozens of buttons, multi-actions with 15+ sub-actions, or need to rebuild profiles after changes. This lets you define everything in Python and install it in seconds.

## Quick Start

### 1. Find your device info

Open Stream Deck, go to **Preferences > Devices**. Note your device model and serial. Then find the device UUID in:

```
~/Library/Preferences/com.elgato.StreamDeck.plist
```

Look under `Devices` for a key like `@(1)[4057/128/XXXXXXXXXX]`.

### 2. Update the constants

Edit `streamdeck_installer.py` and set these two lines near the top:

```python
DEVICE_UUID  = "@(1)[4057/128/YOUR_DEVICE_ID]"
DEVICE_MODEL = "YOUR_MODEL"
```

### 3. Create a profile

```python
# profiles/my_app.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamdeck_installer import install_profile

buttons = [
    {"label": "Play",   "key": "space"},
    {"label": "Undo",   "key": "z", "mods": ["cmd"]},
    {"label": "Export", "key": "e", "mods": ["cmd", "shift"]},
]

if __name__ == "__main__":
    install_profile("My App", buttons, app="/Applications/MyApp.app")
```

### 4. Install it

**Quit Stream Deck first** — it overwrites the plist on quit.

```bash
python3 profiles/my_app.py
```

Reopen Stream Deck. The profile auto-activates when the associated app is frontmost.

## Button Types

### Hotkey

```python
{"label": "Save", "key": "s", "mods": ["cmd"]}
```

### Multi-action (sequential hotkeys)

```python
{"label": "Select All\n& Copy", "actions": [
    {"key": "a", "mods": ["cmd"]},
    {"key": "c", "mods": ["cmd"]},
]}
```

### Open app or file

```python
{"label": "FCP", "open": "/Applications/Final Cut Pro.app"}
```

### With auto-generated icon

```python
{"label": "Record", "key": "r", "mods": ["shift", "ctrl"],
 "icon": "record.circle.fill", "color": "red"}
```

Icons use [SF Symbols](https://developer.apple.com/sf-symbols/) names. Requires PyObjC (ships with macOS Python) and Pillow (`pip3 install pillow`).

**Colors**: `"blue"`, `"purple"`, `"orange"`, `"teal"`, `"red"`, `"green"`, `"gray"`

### Spacer (empty slot)

```python
None  # skips this button position
```

### Multi-page profiles

```python
page1 = [{"label": "A", "key": "a"}, {"label": "B", "key": "b"}]
page2 = [{"label": "C", "key": "c"}, {"label": "D", "key": "d"}]

install_profile("My App", pages=[page1, page2], app="/Applications/MyApp.app")
```

## OBS Studio Plugin Actions

If you have the [OBS Studio plugin](https://marketplace.elgato.com/product/obs-studio-08d01b04-7e37-4a6b-a19c-3beab5c849a4) for Stream Deck, you can create buttons that directly control OBS without hotkeys.

### Scene switch

```python
from streamdeck_installer import make_obs_scene_action

{"label": "Camera 1", "_action": make_obs_scene_action("Talking Head 1")}
```

### Source visibility (show/hide overlays)

```python
from streamdeck_installer import (
    make_obs_source_visibility, make_delay_action, make_multi_action_from_list,
)

# Show an overlay in a specific scene, wait, then hide it
sub_actions = [
    make_obs_source_visibility("Scene Name", "Source Name", sceneitemid=6, show=True),
    make_delay_action(5000),  # milliseconds
    make_obs_source_visibility("Scene Name", "Source Name", sceneitemid=6, show=False),
]
{"label": "My Overlay", "_action": make_multi_action_from_list(sub_actions)}
```

The `sceneitemid` is OBS's internal ID for the source within a scene. Find it in your scene collection JSON:

```
~/Library/Application Support/obs-studio/basic/scenes/YOUR_COLLECTION.json
```

### Multi-action switch (toggle)

Press once to show, press again to hide. Uses a different UUID than regular multi-actions:

```python
import uuid

show_actions = [make_obs_source_visibility("Scene", "Source", 6, show=True)]
hide_actions = [make_obs_source_visibility("Scene", "Source", 6, show=False)]

toggle = {
    "ActionID": str(uuid.uuid4()),
    "Actions": [
        {"Actions": show_actions},  # First press
        {"Actions": hide_actions},  # Second press
    ],
    "LinkedTitle": True,
    "Name": "Multi Action Switch",
    "Plugin": {"Name":"Multi Action",
               "UUID":"com.elgato.streamdeck.multiactions","Version":"1.0"},
    "Resources": None,
    "Settings": {},
    "State": 0,
    "States": [{}, {}],
    "UUID": "com.elgato.streamdeck.multiactions.routine2",  # routine2, NOT routine
}
{"label": "Toggle CTA", "_action": toggle}
```

## Key Reference

**Modifiers**: `"cmd"`, `"shift"`, `"opt"` (or `"option"`, `"alt"`), `"ctrl"` (or `"control"`)

**Keys**: `a`–`z`, `0`–`9`, `space`, `return`, `escape`, `delete`, `forward_delete`, `tab`, `home`, `end`, `page_up`, `page_down`, `left`, `right`, `up`, `down`, `f1`–`f20`

## Important Notes

- **Quit Stream Deck before installing** — it overwrites the plist on quit
- **Each install creates a new profile** — old installs are not replaced. Delete old profiles manually from `~/Library/Application Support/com.elgato.StreamDeck/ProfilesV3/` if needed
- **Layout is row-major** — button index 0 is top-left, fills left-to-right, top-to-bottom
- **Profile format is V3** — stored in `ProfilesV3/` (not `ProfilesV2/`)
- **Device UUID matters** — profiles are bound to a specific device. Check your plist if profiles don't appear

## Example Profiles

The `profiles/` directory has working examples:

| File | App | What It Does |
|---|---|---|
| `obs_overlays.py` | OBS Studio | Auto-reads OBS scene collection, builds multi-actions for overlay show/delay/hide across all scenes |
| `obs.py` | OBS Studio | Simpler hotkey-based OBS control |

## License

MIT — do whatever you want with it.
