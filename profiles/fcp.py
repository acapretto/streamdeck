#!/usr/bin/env python3
"""
Final Cut Pro (basic) Profile — transport controls and core editing tools.
Auto-activates when Final Cut Pro is frontmost.
All hotkeys are native FCP shortcuts — no additional setup required.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamdeck_installer import install_profile

buttons = [
    # Row 0 — Playback
    {"label": "Play\nBack",    "key": "j",     "mods": [],
     "icon": "backward.fill", "color": "blue"},
    {"label": "Pause",         "key": "k",     "mods": [],
     "icon": "pause.fill", "color": "blue"},
    {"label": "Play /\nPause", "key": "space", "mods": [],
     "icon": "play.fill", "color": "green"},

    # Row 1 — Playback cont. + In/Out points
    {"label": "Play\nFwd",     "key": "l",     "mods": [],
     "icon": "forward.fill", "color": "blue"},
    {"label": "Mark In",       "key": "i",     "mods": [],
     "icon": "arrowtriangle.right.square.fill", "color": "orange"},
    {"label": "Mark Out",      "key": "o",     "mods": [],
     "icon": "arrowtriangle.left.square.fill", "color": "orange"},

    # Row 2 — Editing tools
    {"label": "Marker",        "key": "m",     "mods": [],
     "icon": "flag.fill", "color": "red"},
    {"label": "Blade",         "key": "b",     "mods": [],
     "icon": "scissors", "color": "red"},
    {"label": "Select",        "key": "a",     "mods": [],
     "icon": "cursorarrow", "color": "gray"},

    # Row 3 — Edit modes + timeline ops
    {"label": "Trim\nTool",    "key": "t",     "mods": [],
     "icon": "crop", "color": "purple"},
    {"label": "Connect",       "key": "q",     "mods": [],
     "icon": "link", "color": "teal"},
    {"label": "Insert",        "key": "w",     "mods": [],
     "icon": "plus.rectangle.fill", "color": "teal"},

    # Row 4 — Edit modes cont.
    {"label": "Overwrite",     "key": "d",     "mods": [],
     "icon": "square.fill.on.square.fill", "color": "orange"},
    {"label": "Append",        "key": "e",     "mods": [],
     "icon": "arrowshape.right.fill", "color": "teal"},
    {"label": "Zoom Fit",      "key": "z",     "mods": ["shift"],
     "icon": "arrow.up.left.and.arrow.down.right", "color": "gray"},
]

if __name__ == "__main__":
    install_profile(
        name    = "Final Cut Pro",
        app     = "/Applications/Final Cut Pro.app",
        buttons = buttons,
    )
