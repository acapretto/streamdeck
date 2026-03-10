#!/usr/bin/env python3
"""
OBS Overlay Profile Generator

Reads the OBS scene collection JSON to discover all overlay sources and their
per-scene item IDs, then builds a Stream Deck profile with multi-actions that
show/delay/hide across all scenes.

Usage:
    python3 profiles/obs_overlays.py

Run this AFTER creating all overlay browser sources in OBS and paste-referencing
them to all scenes. The script reads the scene collection to get correct IDs.
"""
import sys, os, json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamdeck_installer import (
    install_profile, make_obs_source_visibility, make_delay_action,
    make_obs_scene_action, make_multi_action_from_list,
    make_hotkey_action,
)

# ── Configuration ────────────────────────────────────────────────────────────

OBS_SCENE_COLLECTION = os.path.expanduser(
    "~/Library/Application Support/obs-studio/basic/scenes/Untitled.json"
)

# Scenes that have overlay sources (skip Brand Bumper)
OVERLAY_SCENES = [
    "Talking Head 1",
    "Screen and Head",
    "Head & Desk",
    "Talking Head Angle 2",
    "Screen Only",
    "iPad Only",
    "IPad + Head",
]

# Overlay sources and their behavior
# "auto" = multi-action: show all → delay → hide all
# "toggle" = multi-action switch: press 1 shows all, press 2 hides all
OVERLAY_SOURCES = {
    # Callout types (auto-dismiss after duration)
    "Big Idea":        {"mode": "auto", "delay": 7000,  "icon": "lightbulb.fill",    "color": "green"},
    "Teacher Move":    {"mode": "auto", "delay": 7000,  "icon": "star.fill",         "color": "orange"},
    "Why This Works":  {"mode": "auto", "delay": 7000,  "icon": "checkmark.seal.fill","color": "red"},
    "Common Mistake":  {"mode": "auto", "delay": 7000,  "icon": "exclamationmark.triangle.fill", "color": "red"},
    "Next Connection": {"mode": "auto", "delay": 7000,  "icon": "arrow.right.circle.fill", "color": "blue"},
    "Agenda":          {"mode": "auto", "delay": 25000, "icon": "list.bullet",       "color": "teal"},

    # Pattern interrupts (auto-dismiss)
    "Whoosh":          {"mode": "auto", "delay": 3000,  "icon": "wind",              "color": "green"},
    "Emphasis":        {"mode": "auto", "delay": 3000,  "icon": "sparkles",          "color": "green"},
    "Section":         {"mode": "auto", "delay": 5000,  "icon": "minus",             "color": "green"},

    # Toggle overlays (manual show/hide)
    "DYK":             {"mode": "toggle", "icon": "questionmark.circle", "color": "green"},
    "CTA":             {"mode": "toggle", "icon": "link",               "color": "teal"},

    # Lower Third (auto-dismiss)
    "Lower Third":     {"mode": "auto", "delay": 7000,  "icon": "person.text.rectangle", "color": "teal"},
}

# ── Read OBS Scene Collection ────────────────────────────────────────────────

def read_obs_sources():
    """Read OBS scene collection and return {source_name: {scene: sceneitemid}}."""
    with open(OBS_SCENE_COLLECTION) as f:
        data = json.load(f)

    source_map = {}  # source_name → {scene_name: sceneitemid}

    for src in data.get("sources", []):
        if src.get("versioned_id") != "scene":
            continue
        scene_name = src["name"]
        if scene_name not in OVERLAY_SCENES:
            continue
        for item in src.get("settings", {}).get("items", []):
            name = item.get("name", "")
            sid = item.get("id", 0)
            if name in OVERLAY_SOURCES:
                source_map.setdefault(name, {})[scene_name] = sid

    return source_map


# ── Build Multi-Actions ──────────────────────────────────────────────────────

def build_auto_button(source_name, source_map, config):
    """Build an auto-dismiss overlay button: show all → delay → hide all."""
    scenes = source_map.get(source_name, {})
    if not scenes:
        print(f"  WARNING: '{source_name}' not found in any scene — skipping")
        return None

    sub_actions = []

    # Show in all scenes
    for scene in OVERLAY_SCENES:
        if scene in scenes:
            sub_actions.append(
                make_obs_source_visibility(scene, source_name, scenes[scene], show=True)
            )

    # Delay
    sub_actions.append(make_delay_action(config["delay"]))

    # Hide in all scenes
    for scene in OVERLAY_SCENES:
        if scene in scenes:
            sub_actions.append(
                make_obs_source_visibility(scene, source_name, scenes[scene], show=False)
            )

    label = source_name.replace(" ", "\n") if len(source_name) > 10 else source_name
    action = make_multi_action_from_list(sub_actions, label)

    return {
        "label": label,
        "_action": action,
        "icon": config.get("icon", "circle"),
        "color": config.get("color", "blue"),
    }


def build_toggle_button(source_name, source_map, config):
    """Build a toggle overlay button: press 1 = show all, press 2 = hide all."""
    scenes = source_map.get(source_name, {})
    if not scenes:
        print(f"  WARNING: '{source_name}' not found in any scene — skipping")
        return None

    show_actions = []
    hide_actions = []

    for scene in OVERLAY_SCENES:
        if scene in scenes:
            show_actions.append(
                make_obs_source_visibility(scene, source_name, scenes[scene], show=True)
            )
            hide_actions.append(
                make_obs_source_visibility(scene, source_name, scenes[scene], show=False)
            )

    import uuid as _uuid
    label = source_name.replace(" ", "\n") if len(source_name) > 10 else source_name

    # Multi Action Switch: two states (routine2, not routine)
    action = {
        "ActionID": str(_uuid.uuid4()),
        "Actions": [
            {"Actions": show_actions},   # State 0 (first press → show)
            {"Actions": hide_actions},   # State 1 (second press → hide)
        ],
        "LinkedTitle": True,
        "Name": "Multi Action Switch",
        "Plugin": {"Name":"Multi Action",
                   "UUID":"com.elgato.streamdeck.multiactions","Version":"1.0"},
        "Resources": None,
        "Settings": {},
        "State": 0,
        "States": [{"Title": label}, {"Title": f"{label}\n(ON)"}],
        "UUID": "com.elgato.streamdeck.multiactions.routine2",
    }

    return {
        "label": label,
        "_action": action,
        "icon": config.get("icon", "circle"),
        "color": config.get("color", "blue"),
    }


# ── Build Profile Layout ────────────────────────────────────────────────────

def build_profile():
    source_map = read_obs_sources()

    print(f"Found overlay sources in OBS:")
    for name, scenes in sorted(source_map.items()):
        print(f"  {name}: {len(scenes)} scenes")
    print()

    # Build buttons for each overlay
    buttons = {}
    missing = []
    for name, config in OVERLAY_SOURCES.items():
        if name not in source_map:
            missing.append(name)
            continue
        if config["mode"] == "auto":
            btn = build_auto_button(name, source_map, config)
        else:
            btn = build_toggle_button(name, source_map, config)
        if btn:
            buttons[name] = btn

    if missing:
        print(f"Sources NOT found in OBS (create them first):")
        for name in missing:
            print(f"  - {name}")
        print()

    # ── Page 1: Scenes ──
    page1 = [
        {"label": "Talk\nHead 1",      "_action": make_obs_scene_action("Talking Head 1"),
         "icon": "person.fill", "color": "blue"},
        {"label": "Head\n& Desk",      "_action": make_obs_scene_action("Head & Desk"),
         "icon": "desktopcomputer", "color": "blue"},
        {"label": "Angle 2",           "_action": make_obs_scene_action("Talking Head Angle 2"),
         "icon": "person.2.fill", "color": "blue"},

        {"label": "Screen\nOnly",      "_action": make_obs_scene_action("Screen Only"),
         "icon": "rectangle.inset.filled", "color": "blue"},
        {"label": "iPad\nOnly",        "_action": make_obs_scene_action("iPad Only"),
         "icon": "ipad.landscape", "color": "blue"},
        {"label": "Brand\nBumper",     "_action": make_obs_scene_action("Brand Bumper"),
         "icon": "photo", "color": "blue"},

        {"label": "Screen\n+ Head",    "_action": make_obs_scene_action("Screen and Head"),
         "icon": "rectangle.badge.person.crop", "color": "blue"},
        {"label": "iPad\n+ Head",      "_action": make_obs_scene_action("IPad + Head"),
         "icon": "ipad.badge.play", "color": "blue"},
        {"label": "Mouse\nFollow",     "key": "m", "mods": ["cmd","opt","ctrl"],
         "icon": "cursorarrow.motionlines", "color": "purple"},

        # Row 3 — Recording
        {"label": "Rec\nToggle",       "key": "r", "mods": ["cmd","opt","ctrl"],
         "icon": "record.circle.fill", "color": "red"},
        {"label": "Pause\nRec",        "key": "p", "mods": ["cmd","opt","ctrl"],
         "icon": "pause.circle.fill", "color": "red"},
        {"label": "Chapter\nMark",     "key": "c", "mods": ["cmd","opt","ctrl"],
         "icon": "bookmark.fill", "color": "red"},

        # Row 4 — Quick overlays
        {"label": "Mute\nMic",         "key": "u", "mods": ["cmd","opt","ctrl"],
         "icon": "mic.slash.fill", "color": "orange"},
        buttons.get("Lower Third"),
        buttons.get("CTA"),
    ]

    # ── Page 2: Callout types ──
    page2 = [
        buttons.get("Big Idea"),
        buttons.get("Teacher Move"),
        buttons.get("Why This Works"),

        buttons.get("Common Mistake"),
        buttons.get("Next Connection"),
        buttons.get("Agenda"),

        # Pattern interrupts
        buttons.get("Whoosh"),
        buttons.get("Emphasis"),
        buttons.get("Section"),

        buttons.get("DYK"),
        None,
        None,

        None, None, None,
    ]

    # Replace None with empty slots
    page1 = [b if b else None for b in page1]
    page2 = [b if b else None for b in page2]

    return [page1, page2]


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not os.path.exists(OBS_SCENE_COLLECTION):
        print(f"ERROR: OBS scene collection not found at:\n  {OBS_SCENE_COLLECTION}")
        sys.exit(1)

    pages = build_profile()

    install_profile(
        name="OBS Overlays",
        app="/Applications/OBS.app",
        pages=pages,
    )
