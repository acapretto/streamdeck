#!/usr/bin/env python3
"""
Finder Profile
Auto-activates when Finder is frontmost.

Hotkeys (all KM macros in SD_Finder_Macros.kmmacros unless noted):
  Clip Slot 1-3  : tap = Hyper+1/2/3 (paste), hold = Ctrl+Opt+Cmd+1/2/3 (copy)
  Expert Prompt  : Hyper+P
  Step Prompt    : Hyper+R
  Copy Full Path : Cmd+Opt+C  (native Finder shortcut — no KM needed)
  AirDrop        : Hyper+A
  Terminal Here  : Hyper+T
  Snagit         : Cmd+Shift+C  (set in Snagit prefs)
  Tile Windows   : Hyper+W  (Apple Shortcut)
  Dictation+Paste: Hyper+D  (Apple Shortcut)
  QR Code        : Hyper+Q  (Apple Shortcut)
  Shorten URL    : Hyper+U  (Apple Shortcut)
  Paste Plain    : Hyper+V
  Universal Input: Hyper+I  (Apple Shortcut)

Hyper = Ctrl+Shift+Opt+Cmd
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamdeck_installer import install_profile

buttons = [
    # Row 0 — Clipboard slots (tap=paste, hold=copy — configure hold in SD UI after install)
    {"label": "Clip\nSlot 1", "key": "1", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "1.circle.fill", "color": "purple"},
    {"label": "Clip\nSlot 2", "key": "2", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "2.circle.fill", "color": "teal"},
    {"label": "Clip\nSlot 3", "key": "3", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "3.circle.fill", "color": "green"},

    # Row 1 — Prompt templates + Copy Path
    {"label": "Expert\nPrompt", "key": "p", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "brain.head.profile", "color": "orange"},
    {"label": "Step-by-\nStep", "key": "r", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "list.number", "color": "orange"},
    {"label": "Copy\nPath", "key": "c", "mods": ["cmd","opt"],
     "icon": "doc.on.doc.fill", "color": "blue"},

    # Row 2 — Finder actions
    {"label": "AirDrop", "key": "a", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "dot.radiowaves.left.and.right", "color": "blue"},
    {"label": "Terminal\nHere", "key": "t", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "terminal.fill", "color": "gray"},
    {"label": "Snagit\nCapture", "key": "c", "mods": ["cmd","shift"],
     "icon": "camera.viewfinder", "color": "red"},

    # Row 3 — Apple Shortcuts
    {"label": "Tile\nWindows", "key": "w", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "square.grid.2x2.fill", "color": "blue"},
    {"label": "Dictation\n+ Paste", "key": "d", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "waveform.and.mic", "color": "teal"},
    {"label": "QR\nCode", "key": "q", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "qrcode", "color": "green"},

    # Row 4 — More shortcuts + utilities
    {"label": "Shorten\nURL", "key": "u", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "link.circle.fill", "color": "blue"},
    {"label": "Paste\nPlain", "key": "v", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "doc.plaintext.fill", "color": "gray"},
    {"label": "Universal\nInput", "key": "i", "mods": ["cmd","shift","opt","ctrl"],
     "icon": "keyboard.fill", "color": "purple"},
]

if __name__ == "__main__":
    install_profile(
        name    = "Finder",
        app     = "/System/Library/CoreServices/Finder.app",
        buttons = buttons,
    )
