#!/usr/bin/env python3
"""
Generate an icon pack from all Stream Deck profile buttons.
Outputs named 144x144 PNGs to streamdeck/icon-pack/ for drag-and-drop import.
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from streamdeck_installer import make_button_icon, ICON_COLORS, _ICONS_AVAILABLE

if not _ICONS_AVAILABLE:
    print("ERROR: Pillow and/or PyObjC not available. Install with:")
    print("  pip3 install pillow")
    sys.exit(1)

# Collect all buttons from all profiles
from profiles.obs import page1 as obs_page1, page2 as obs_page2
from profiles.finder import buttons as finder_buttons
from profiles.fcp import buttons as fcp_buttons
from profiles.fcp_advanced import buttons as fcp_advanced_buttons

all_buttons = {
    "obs": [b for b in obs_page1 + obs_page2 if b is not None],
    "finder": finder_buttons,
    "fcp": fcp_buttons,
    "fcp-advanced": fcp_advanced_buttons,
}

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon-pack")
os.makedirs(out_dir, exist_ok=True)

count = 0
for profile_name, buttons in all_buttons.items():
    profile_dir = os.path.join(out_dir, profile_name)
    os.makedirs(profile_dir, exist_ok=True)

    for btn in buttons:
        if "icon" not in btn:
            continue
        label = btn.get("label", "").replace("\\n", "\n")
        color_name = btn.get("color", "blue")
        bg = ICON_COLORS.get(color_name, ICON_COLORS["blue"])
        img = make_button_icon(btn["icon"], label, bg)
        if img is None:
            print(f"  Skip (SF Symbol not found): {btn['icon']}")
            continue

        # Build filename from label
        fname = label.replace("\n", "-").replace(" ", "-").replace("/", "-")
        fname = fname.replace("→", "").replace("&", "and").strip("-")
        fname = fname.lower() + ".png"
        img.save(os.path.join(profile_dir, fname))
        count += 1

print(f"✓ Generated {count} icons in: {out_dir}")
print(f"  Drag any icon onto a Stream Deck button to use it.")
