#!/usr/bin/env python3
"""
Generate Stream Deck icons for Apple Shortcuts.
Icons use SF Symbols that match the shortcut's purpose (not the Shortcuts app icons).
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from streamdeck_installer import make_button_icon, ICON_COLORS, _ICONS_AVAILABLE

if not _ICONS_AVAILABLE:
    print("ERROR: Pillow and/or PyObjC not available. Install with:")
    print("  pip3 install pillow")
    sys.exit(1)

# (label, SF Symbol, color)
shortcuts = [
    ("Speak",                    "speaker.wave.3.fill",          "blue"),
    ("Photo\nGrid 1",           "square.grid.2x2.fill",         "green"),
    ("Clipboard\nMD → …",      "doc.richtext",                  "orange"),
    ("Weekly\nBook Insight",    "book.fill",                     "purple"),
    ("Universal\nInput",        "keyboard.fill",                 "purple"),
    ("Watch\nDictate",          "applewatch.radiowaves.left.and.right", "teal"),
    ("Dictation\nAnd Paste",    "waveform.and.mic",              "teal"),
    ("Tile Last\n2 Windows",    "rectangle.split.2x1.fill",      "blue"),
    ("Shorten\nURL",            "link.circle.fill",              "green"),
    ("Daily\nPlan",             "calendar.badge.clock",          "red"),
    ("Rock Paper\nScissors",    "hand.raised.fingers.spread.fill", "teal"),
    ("Reflection\nPrompts",     "text.bubble.fill",              "green"),
    ("Tile Last\n4 Windows",    "square.grid.2x2.fill",          "blue"),
    ("What Got\nDone?",         "checkmark.circle.fill",         "purple"),
    ("Flatten\nPDF",            "doc.fill",                      "red"),
    ("MP3 to\nBase 64",        "waveform.circle.fill",          "teal"),
    ("Capretto\nSound FX",     "speaker.wave.2.circle.fill",    "green"),
    ("Generate\nQR Code",      "qrcode",                        "blue"),
]

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon-pack", "shortcuts")
os.makedirs(out_dir, exist_ok=True)

count = 0
for label, symbol, color_name in shortcuts:
    bg = ICON_COLORS.get(color_name, ICON_COLORS["blue"])
    img = make_button_icon(symbol, label, bg)
    if img is None:
        print(f"  Skip (SF Symbol not found): {symbol} for {label}")
        continue

    fname = label.replace("\n", "-").replace(" ", "-").replace("/", "-")
    fname = fname.replace("→", "to").replace("…", "").replace("?", "").strip("-")
    fname = fname.lower() + ".png"
    img.save(os.path.join(out_dir, fname))
    count += 1

print(f"✓ Generated {count} icons in: {out_dir}")
