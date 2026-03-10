#!/usr/bin/env python3
"""
OBS Profile — 2 Pages
Auto-activates when OBS is frontmost.

Page 1 (Main):
  Row 0: Talking Head 1, Head & Desk, Talking Head Angle 2
  Row 1: Screen Only, iPad Only, Brand Bumper
  Row 2: Mouse Follow, Whoosh, Emphasis
  Row 3: Next Overlay, Lower Third, CTA
  Row 4: Pause Rec, Chapter Mark, (empty)

Page 2 (Secondary):
  Row 0: Screen + Head, iPad + Head, (empty)
  Row 1: Section, DYK, (empty)
  Row 2: Rec Toggle, Mute Mic, (empty)

Scene hotkeys (Ctrl+Shift+1-8) assigned in OBS Settings > Hotkeys.
Overlay hotkeys (Ctrl+Opt+0/8/9) toggle source visibility in OBS.
Pattern interrupt hotkeys (Ctrl+Opt+W/D/S/F) toggle source visibility in OBS.
Recording hotkeys (Ctrl+Opt+Cmd+R/P/C/U) assigned in OBS Settings > Hotkeys.

OBS source visibility hotkeys to assign (in every scene except Brand Bumper):
  Ctrl+Opt+0 → Show/Hide "Sequence" source
  Ctrl+Opt+8 → Show/Hide "Lower Third" source
  Ctrl+Opt+9 → Show/Hide "CTA" source
  Ctrl+Opt+W → Show/Hide "Whoosh" source
  Ctrl+Opt+F → Show/Hide "Emphasis" source
  Ctrl+Opt+S → Show/Hide "Section" source
  Ctrl+Opt+D → Show/Hide "DYK" source
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamdeck_installer import install_profile

page1 = [
    # Row 0 — Primary scenes
    {"label": "Talk\nHead 1",      "key": "1", "mods": ["shift","ctrl"], "icon": "person.fill", "color": "blue"},
    {"label": "Head\n& Desk",      "key": "3", "mods": ["shift","ctrl"], "icon": "desktopcomputer", "color": "blue"},
    {"label": "Talk Head\nAngle 2", "key": "4", "mods": ["shift","ctrl"], "icon": "person.2.fill", "color": "blue"},

    # Row 1 — More scenes
    {"label": "Screen\nOnly",  "key": "5", "mods": ["shift","ctrl"], "icon": "rectangle.inset.filled", "color": "blue"},
    {"label": "iPad\nOnly",    "key": "6", "mods": ["shift","ctrl"], "icon": "ipad.landscape", "color": "blue"},
    {"label": "Brand\nBumper", "key": "8", "mods": ["shift","ctrl"], "icon": "photo", "color": "blue"},

    # Row 2 — Utilities + Pattern Interrupts
    {"label": "Mouse\nFollow", "key": "m", "mods": ["cmd","opt","ctrl"],
     "icon": "cursorarrow.motionlines", "color": "purple"},
    {"label": "Whoosh",        "key": "w", "mods": ["opt","ctrl"],
     "icon": "wind", "color": "green"},
    {"label": "Emphasis",      "key": "f", "mods": ["opt","ctrl"],
     "icon": "sparkles", "color": "green"},

    # Row 3 — Overlay controls
    {"label": "Next\nOverlay", "key": "0", "mods": ["opt","ctrl"],
     "icon": "forward.fill", "color": "teal"},
    {"label": "Lower\nThird",  "key": "8", "mods": ["opt","ctrl"],
     "icon": "person.text.rectangle", "color": "teal"},
    {"label": "CTA",           "key": "9", "mods": ["opt","ctrl"],
     "icon": "link", "color": "teal"},

    # Row 4 — Recording controls
    {"label": "Pause\nRec",    "key": "p", "mods": ["cmd","opt","ctrl"],
     "icon": "pause.circle.fill", "color": "red"},
    {"label": "Chapter\nMark", "key": "c", "mods": ["cmd","opt","ctrl"],
     "icon": "bookmark.fill", "color": "red"},
]

page2 = [
    # Row 0 — Secondary scenes
    {"label": "Screen\n+ Head", "key": "2", "mods": ["shift","ctrl"], "icon": "rectangle.badge.person.crop", "color": "blue"},
    {"label": "iPad\n+ Head",   "key": "7", "mods": ["shift","ctrl"], "icon": "ipad.badge.play", "color": "blue"},

    None,  # empty slot

    # Row 1 — Pattern Interrupts
    {"label": "Section",  "key": "s", "mods": ["opt","ctrl"],
     "icon": "minus", "color": "green"},
    {"label": "DYK",      "key": "d", "mods": ["opt","ctrl"],
     "icon": "questionmark.circle", "color": "green"},

    None,  # empty slot

    # Row 2 — Recording
    {"label": "Rec\nToggle", "key": "r", "mods": ["cmd","opt","ctrl"],
     "icon": "record.circle.fill", "color": "red"},
    {"label": "Mute\nMic",   "key": "u", "mods": ["cmd","opt","ctrl"],
     "icon": "mic.slash.fill", "color": "orange"},
]

if __name__ == "__main__":
    install_profile(
        name  = "OBS",
        app   = "/Applications/OBS.app",
        pages = [page1, page2],
    )
