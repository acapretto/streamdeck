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

Press once to show, press again to hide:

```python
from streamdeck_installer import make_multi_action_switch, make_obs_source_visibility

show_actions = [make_obs_source_visibility("Scene", "Source", 6, show=True)]
hide_actions = [make_obs_source_visibility("Scene", "Source", 6, show=False)]

{"label": "Toggle CTA", "_action": make_multi_action_switch(show_actions, hide_actions)}
```

### Filter toggle, record pause, chapter marker

```python
from streamdeck_installer import make_obs_filter_toggle, make_obs_record_pause, make_obs_chapter_marker

{"label": "Filter",  "_action": make_obs_filter_toggle("Camera Source")}
{"label": "Pause",   "_action": make_obs_record_pause()}
{"label": "Chapter", "_action": make_obs_chapter_marker()}
```

## Apple Music

```python
from streamdeck_installer import (
    make_music_play_pause, make_music_next, make_music_previous,
    make_music_love, make_music_shuffle, make_music_volume,
)

{"label": "Play",    "_action": make_music_play_pause()}
{"label": "Next",    "_action": make_music_next()}
{"label": "Prev",    "_action": make_music_previous()}
{"label": "Love",    "_action": make_music_love()}
{"label": "Shuffle", "_action": make_music_shuffle()}
{"label": "Vol Up",  "_action": make_music_volume("up")}
{"label": "Vol Down", "_action": make_music_volume("down")}
```

## Apple Shortcuts

Requires the [Shortcuts plugin](https://apps.elgato.com/plugins/com.sentinelite.streamdeckshortcuts).

```python
from streamdeck_installer import make_shortcut_action

{"label": "My Shortcut", "_action": make_shortcut_action("Shortcut Name")}

# With UUID (find via: shortcuts list)
{"label": "QR Code", "_action": make_shortcut_action("Generate QR Code", "F03400C9-...")}
```

## Zoom

Requires the [Zoom plugin](https://apps.elgato.com/plugins/com.lostdomain.zoom).

```python
from streamdeck_installer import (
    make_zoom_mute, make_zoom_video, make_zoom_share,
    make_zoom_record, make_zoom_leave, make_zoom_focus,
)

{"label": "Mute",   "_action": make_zoom_mute()}
{"label": "Video",  "_action": make_zoom_video()}
{"label": "Share",  "_action": make_zoom_share()}
{"label": "Record", "_action": make_zoom_record()}
{"label": "Leave",  "_action": make_zoom_leave()}
{"label": "Focus",  "_action": make_zoom_focus()}
```

## Navigation

```python
from streamdeck_installer import make_next_page_action, make_previous_page_action, make_back_to_parent_action

{"label": "Next",   "_action": make_next_page_action()}
{"label": "Back",   "_action": make_previous_page_action()}
{"label": "Parent", "_action": make_back_to_parent_action()}
```

## System Actions

```python
from streamdeck_installer import (
    make_website_action, make_text_action, make_hotkey_switch_action,
    make_multimedia_action, make_play_audio_action,
)

# Open a URL
{"label": "GitHub", "_action": make_website_action("https://github.com")}

# Paste text
{"label": "Email", "_action": make_text_action("hello@example.com")}

# Hotkey toggle (press 1 = key1, press 2 = key2)
{"label": "Mute", "_action": make_hotkey_switch_action("m", ["cmd", "shift"])}

# Multimedia keys
{"label": "Vol Up", "_action": make_multimedia_action("volume_up")}
# Options: play_pause, previous, next, stop, volume_down, volume_up, mute

# Sound effect
{"label": "Laugh", "_action": make_play_audio_action("/path/to/sound.mp3", volume=50)}
```

## Adding Support for Other Plugins

Any Stream Deck plugin can be automated. The process:

1. Create **one button manually** in the Stream Deck UI
2. Find the profile at `~/Library/Application Support/com.elgato.StreamDeck/ProfilesV3/`
3. Open `Profiles/*/manifest.json` and find the action JSON
4. Copy the `UUID`, `Plugin`, and `Settings` structure into a Python helper function

Every action follows the same skeleton:

```python
{
    "ActionID": str(uuid.uuid4()),   # random, unique per button
    "LinkedTitle": True,
    "Name": "Action Name",
    "Plugin": {"Name": "Plugin Name", "UUID": "com.example.plugin", "Version": "1.0"},
    "Resources": None,
    "Settings": {},                  # plugin-specific config
    "State": 0,
    "States": [{}],                  # one {} per state (toggles have 2)
    "UUID": "com.example.plugin.action",
}
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
