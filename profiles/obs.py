#!/usr/bin/env python3
"""
OBS Profile
Auto-activates when OBS is frontmost.

Scene hotkeys (Ctrl+Shift+1-7) must be assigned in OBS Settings → Hotkeys.
Callout hotkeys (Ctrl+Opt+1-3) trigger Show/Hide source hotkeys for overlay sources.
Recording hotkeys (Ctrl+Shift+R/P/C) assigned in OBS Settings → Hotkeys.
Vid→Cursor (Ctrl+Opt+Cmd+M) assigned in OBS Settings → Hotkeys.
Mute Mic (Ctrl+Shift+M) assigned in OBS Settings → Hotkeys.

Update the 7 scene labels to match your actual OBS scene names.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamdeck_installer import install_profile

buttons = [
    # Row 0-2, col 0 — Scenes 1-7  (update labels to your actual scene names)
    {"label": "Scene 1",  "key": "1", "mods": ["shift","ctrl"], "icon": "film", "color": "blue"},
    {"label": "Scene 2",  "key": "2", "mods": ["shift","ctrl"], "icon": "film", "color": "blue"},
    {"label": "Scene 3",  "key": "3", "mods": ["shift","ctrl"], "icon": "film", "color": "blue"},
    {"label": "Scene 4",  "key": "4", "mods": ["shift","ctrl"], "icon": "film", "color": "blue"},
    {"label": "Scene 5",  "key": "5", "mods": ["shift","ctrl"], "icon": "film", "color": "blue"},
    {"label": "Scene 6",  "key": "6", "mods": ["shift","ctrl"], "icon": "film", "color": "blue"},
    {"label": "Scene 7",  "key": "7", "mods": ["shift","ctrl"], "icon": "film", "color": "blue"},

    # Row 2 — Camera + Audio
    {"label": "Vid→\nCursor", "key": "m", "mods": ["cmd","opt","ctrl"],
     "icon": "cursorarrow.motionlines", "color": "purple"},
    {"label": "Mute\nMic",    "key": "m", "mods": ["shift","ctrl"],
     "icon": "mic.slash.fill", "color": "orange"},

    # Row 3 — Callout overlays
    {"label": "Big\nIdea",   "key": "1", "mods": ["opt","ctrl"],
     "icon": "lightbulb.fill", "color": "teal"},
    {"label": "Spotlight",   "key": "2", "mods": ["opt","ctrl"],
     "icon": "spotlight", "color": "teal"},
    {"label": "Agenda",      "key": "3", "mods": ["opt","ctrl"],
     "icon": "list.bullet.clipboard", "color": "teal"},

    # Row 4 — Recording controls
    {"label": "Rec\nToggle", "key": "r", "mods": ["shift","ctrl"],
     "icon": "record.circle.fill", "color": "red"},
    {"label": "Pause\nRec",  "key": "p", "mods": ["shift","ctrl"],
     "icon": "pause.circle.fill", "color": "red"},
    {"label": "Chapter\nMark","key": "c", "mods": ["shift","ctrl"],
     "icon": "bookmark.fill", "color": "red"},
]

if __name__ == "__main__":
    install_profile(
        name    = "OBS",
        app     = "/Applications/OBS.app",
        buttons = buttons,
    )
