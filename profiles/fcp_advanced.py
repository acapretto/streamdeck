#!/usr/bin/env python3
"""
FCP Advanced Profile — complex workflows and multi-step actions.
Auto-activates when Final Cut Pro is frontmost.
All hotkeys are native FCP shortcuts — no additional setup required.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamdeck_installer import install_profile

buttons = [
    # Row 0 — Workspace modes
    {"label": "Rough\nCut",     "actions": [
        {"key": "s"},
        {"key": "s", "mods": ["shift"]},
        {"key": "z", "mods": ["shift"]},
        {"key": "a"},
     ], "icon": "scissors.badge.ellipsis", "color": "purple"},

    {"label": "Color\nGrade",   "actions": [
        {"key": "6", "mods": ["cmd"]},
        {"key": "7", "mods": ["cmd"]},
     ], "icon": "camera.filters", "color": "orange"},

    {"label": "Audio\nCleanup", "actions": [
        {"key": "i", "mods": ["cmd"]},
        {"key": "m", "mods": ["cmd", "opt"]},
     ], "icon": "waveform.badge.checkmark", "color": "teal"},

    # Row 1 — Project ops
    # Note: Open FCP + Import originally launched FCP then Cmd+I.
    # Represented here as just the Import shortcut since open is handled by the app profile trigger.
    {"label": "Open +\nImport", "actions": [
        {"key": "i", "mods": ["cmd"]},
     ], "icon": "arrow.down.doc.fill", "color": "blue"},

    {"label": "Export /\nShare", "key": "e", "mods": ["cmd"],
     "icon": "square.and.arrow.up", "color": "green"},

    {"label": "Sync\nClips",    "key": "g", "mods": ["cmd", "opt"],
     "icon": "arrow.triangle.2.circlepath", "color": "teal"},

    # Row 2 — Clip operations
    {"label": "Compound\nClip", "actions": [
        {"key": "g", "mods": ["opt"]},
        {"key": "return"},
     ], "icon": "photo.stack", "color": "purple"},

    {"label": "Paste\nAttribs", "key": "v", "mods": ["cmd", "opt"],
     "icon": "doc.on.clipboard.fill", "color": "orange"},

    {"label": "Freeze\nFrame",  "actions": [
        {"key": "f", "mods": ["opt"]},
        {"key": "a"},
     ], "icon": "camera.fill", "color": "blue"},

    # Row 3 — Editors
    {"label": "Precision\nEdit", "key": "d", "mods": ["cmd", "opt"],
     "icon": "slider.horizontal.3", "color": "blue"},

    {"label": "Retime\nEditor", "key": "r", "mods": ["cmd"],
     "icon": "clock.arrow.circlepath", "color": "purple"},

    {"label": "Marker\n+ Note", "actions": [
        {"key": "m"},
        {"key": "m"},
     ], "icon": "bookmark.fill", "color": "red"},

    # Row 4 — Advanced edits
    {"label": "Lift to\nConnect", "actions": [
        {"key": "up", "mods": ["cmd", "opt"]},
        {"key": "n"},
     ], "icon": "arrow.up.square.fill", "color": "teal"},

    {"label": "Silence\nHunter", "actions": [
        {"key": "2", "mods": ["cmd", "shift"]},
        {"key": "l"},
        {"key": "l"},
     ], "icon": "waveform.slash", "color": "orange"},

    {"label": "Jump &\nReview", "actions": [
        {"key": "home"},
        {"key": "space"},
     ], "icon": "play.circle.fill", "color": "green"},
]

if __name__ == "__main__":
    install_profile(
        name    = "FCP Advanced",
        app     = "/Applications/Final Cut Pro.app",
        buttons = buttons,
    )
