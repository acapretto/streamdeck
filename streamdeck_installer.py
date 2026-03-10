#!/usr/bin/env python3
"""
Stream Deck 31 Profile Installer
Device: 20GBA9901 | @(1)[4057/128/DL10L1A31880] | 3col x 5row

Usage:
    Define your buttons below and run:
        python3 ~/streamdeck_installer.py

    Stream Deck MUST be closed before running.
    Reopen Stream Deck after running.

Button format:
    {"label": "My Button", "key": "a"}
    {"label": "My Button", "key": "a", "mods": ["cmd", "shift"]}
    {"label": "Multi",     "actions": [
        {"key": "a", "mods": ["cmd"], "delay": 0},
        {"key": "z", "mods": ["shift"], "delay": 300},
    ]}
    {"label": "Open App",  "open": "/Applications/Final Cut Pro.app"}

Modifier names: "cmd", "shift", "opt", "ctrl"
Key names: letters a-z, digits 0-9, "space", "return", "escape",
           "delete", "forward_delete", "tab", "home", "end",
           "page_up", "page_down", "left", "right", "up", "down",
           "f1"-"f20"
"""

import json, uuid, os, plistlib, subprocess, sys, io, random, string

# ── Icon generation (SF Symbols via PyObjC + Pillow) ─────────────────────────
try:
    import AppKit
    from PIL import Image, ImageDraw, ImageFont
    _ICONS_AVAILABLE = True
except ImportError:
    _ICONS_AVAILABLE = False

_SFNS_FONT = "/System/Library/Fonts/SFNSRounded.ttf"

def _sf_icon(symbol, size, bg, fg=(255,255,255)):
    cfg = AppKit.NSImageSymbolConfiguration.configurationWithPointSize_weight_(
        size * 0.42, AppKit.NSFontWeightMedium
    )
    ns = AppKit.NSImage.imageWithSystemSymbolName_accessibilityDescription_(symbol, None)
    if ns is None:
        return None
    ns = ns.imageWithSymbolConfiguration_(cfg)
    rep = AppKit.NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
        None, size, size, 8, 4, True, False, AppKit.NSDeviceRGBColorSpace, 0, 0
    )
    ctx = AppKit.NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
    AppKit.NSGraphicsContext.saveGraphicsState()
    AppKit.NSGraphicsContext.setCurrentContext_(ctx)
    r,g,b = [c/255 for c in bg]
    AppKit.NSColor.colorWithRed_green_blue_alpha_(r,g,b,1.0).setFill()
    AppKit.NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(
        AppKit.NSMakeRect(0,0,size,size), size*0.2, size*0.2
    ).fill()
    fr,fg2,fb = [c/255 for c in fg]
    AppKit.NSColor.colorWithRed_green_blue_alpha_(fr,fg2,fb,1.0).set()
    sw,sh = ns.size()
    ns.drawInRect_fromRect_operation_fraction_(
        AppKit.NSMakeRect((size-sw)/2, (size-sh)/2 + size*0.07, sw, sh),
        AppKit.NSZeroRect, AppKit.NSCompositingOperationSourceOver, 1.0
    )
    AppKit.NSGraphicsContext.restoreGraphicsState()
    png = rep.representationUsingType_properties_(AppKit.NSBitmapImageFileTypePNG, {})
    return Image.open(io.BytesIO(bytes(png))).convert("RGBA")

def make_button_icon(symbol, label, bg_color, size=144):
    """Generate a 144x144 RGBA PIL Image: colored rounded-rect + SF Symbol + label."""
    if not _ICONS_AVAILABLE:
        return None
    img = _sf_icon(symbol, size, bg_color)
    if img is None:
        img = Image.new("RGBA", (size, size), bg_color + (255,))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(_SFNS_FONT, int(size * 0.155))
    except:
        font = ImageFont.load_default()
    lines = label.split("\n")
    line_h = int(size * 0.17)
    y0 = size - int(size * 0.06) - line_h * len(lines)
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0,0), line, font=font)
        x = (size - (bbox[2]-bbox[0])) // 2
        draw.text((x, y0 + i*line_h), line, font=font, fill=(255,255,255))
    return img

# ── Device constants ──────────────────────────────────────────────────────────
DEVICE_UUID  = "@(1)[4057/128/DL10L1A31880]"
DEVICE_MODEL = "20GBA9901"
COLS         = 3   # Stream Deck 31 layout: 3 columns, 5 rows
SD_SUPPORT   = os.path.expanduser("~/Library/Application Support/com.elgato.StreamDeck")
PROFILES_V3  = os.path.join(SD_SUPPORT, "ProfilesV3")
PLIST_PATH   = os.path.expanduser("~/Library/Preferences/com.elgato.StreamDeck.plist")

# ── Key name → macOS native keycode ──────────────────────────────────────────
KEY_CODES = {
    "a":0,"s":1,"d":2,"f":3,"h":4,"g":5,"z":6,"x":7,"c":8,"v":9,
    "b":11,"q":12,"w":13,"e":14,"r":15,"y":16,"t":17,"o":31,"u":32,
    "i":34,"p":35,"l":37,"j":38,"k":40,"n":45,"m":46,
    "1":18,"2":19,"3":20,"4":21,"6":22,"5":23,"9":25,"7":26,"8":28,"0":29,
    "space":49,"return":36,"enter":36,"tab":48,"escape":53,"esc":53,
    "delete":51,"backspace":51,"forward_delete":117,
    "home":115,"end":119,"page_up":116,"page_down":121,
    "left":123,"right":124,"up":126,"down":125,
    "f1":122,"f2":120,"f3":99,"f4":118,"f5":96,"f6":97,"f7":98,
    "f8":100,"f9":101,"f10":109,"f11":103,"f12":111,
    "f13":105,"f14":107,"f15":113,"f16":106,"f17":64,"f18":79,"f19":80,"f20":90,
}

# macOS native → Qt keycode
NATIVE_TO_QT = {
    0:65,1:83,2:68,3:70,4:72,5:71,6:90,7:88,8:67,9:86,
    11:66,12:81,13:87,14:69,15:82,16:89,17:84,
    31:79,32:85,34:73,35:80,37:76,38:74,40:75,45:78,46:77,
    18:49,19:50,20:51,21:52,22:54,23:53,25:57,26:55,28:56,29:48,
    36:16777220,48:16777217,49:32,51:16777219,53:16777216,
    115:16777232,116:16777238,117:16777223,119:16777233,
    121:16777239,123:16777234,124:16777236,125:16777237,126:16777235,
    122:16777264,120:16777265,99:16777266,118:16777267,96:16777268,97:16777269,
    98:16777270,100:16777271,101:16777272,109:16777273,103:16777274,111:16777275,
}

MOD_FLAGS = {"cmd":1048576,"command":1048576,"shift":131072,"opt":524288,
             "option":524288,"alt":524288,"ctrl":262144,"control":262144}

NULL_HK = {"KeyCmd":False,"KeyCtrl":False,"KeyModifiers":0,"KeyOption":False,
           "KeyShift":False,"NativeCode":-1,"QTKeyCode":33554431,"VKeyCode":-1}

def resolve_key(key_name):
    k = key_name.lower()
    if k not in KEY_CODES:
        raise ValueError(f"Unknown key: '{key_name}'. Check KEY_CODES in this script.")
    return KEY_CODES[k]

def build_modifier(mods):
    flags = sum(MOD_FLAGS.get(m.lower(), 0) for m in (mods or []))
    ks = bool(flags & 131072); kc = bool(flags & 262144)
    ko = bool(flags & 524288); km = bool(flags & 1048576)
    kmods = (1 if ks else 0)|(2 if kc else 0)|(4 if ko else 0)|(8 if km else 0)
    return {"KeyCmd":km,"KeyCtrl":kc,"KeyModifiers":kmods,"KeyOption":ko,"KeyShift":ks}

def build_hotkey_settings(key_name, mods=None):
    native = resolve_key(key_name)
    entry  = {**build_modifier(mods), "NativeCode":native,
              "QTKeyCode":NATIVE_TO_QT.get(native, native), "VKeyCode":native}
    return {"Coalesce":True, "Hotkeys":[entry, NULL_HK, NULL_HK, NULL_HK]}

def make_hotkey_action(key_name, mods=None, label=""):
    return {
        "ActionID": str(uuid.uuid4()),
        "LinkedTitle": False,
        "Name": "Hotkey",
        "Plugin": {"Name":"Activate a Key Command",
                   "UUID":"com.elgato.streamdeck.system.hotkey","Version":"1.0"},
        "Resources": None,
        "Settings": build_hotkey_settings(key_name, mods),
        "State": 0,
        "States": [{"Title": label}],
        "UUID": "com.elgato.streamdeck.system.hotkey",
    }

def make_open_action(app_path, label=""):
    return {
        "ActionID": str(uuid.uuid4()),
        "LinkedTitle": False,
        "Name": "Open",
        "Plugin": {"Name":"Open","UUID":"com.elgato.streamdeck.system.open","Version":"1.0"},
        "Resources": None,
        "Settings": {"path": app_path},
        "State": 0,
        "States": [{"Title": label}],
        "UUID": "com.elgato.streamdeck.system.open",
    }

def make_obs_source_visibility(scene, source_name, sceneitemid, show=True, collection="Untitled", label=""):
    """Create an OBS Source Visibility action for use in multi-actions.
    show=True → Show, show=False → Hide."""
    action = {
        "ActionID": str(uuid.uuid4()),
        "LinkedTitle": True,
        "Name": "Source Visibility",
        "Plugin": {"Name":"OBS Studio","UUID":"com.elgato.obsstudio","Version":"2.2.9.9"},
        "Resources": None,
        "Settings": {
            "collection": collection,
            "scene": scene,
            "sceneitemid": sceneitemid,
            "sceneitemname": source_name,
            "sceneitemscene": scene,
            "toplevelscene": scene,
        },
        "State": 0,
        "States": [{"Title": label}, {}],
        "UUID": "com.elgato.obsstudio.source",
    }
    if not show:
        action["OverrideState"] = 1
    return action

def make_delay_action(delay_ms):
    """Create a Delay action for use inside multi-actions."""
    return {
        "ActionID": str(uuid.uuid4()),
        "LinkedTitle": True,
        "Name": "Delay",
        "Plugin": {"Name":"Multi Action","UUID":"com.elgato.streamdeck.multiactions","Version":"1.0"},
        "Resources": None,
        "Settings": {"delay": delay_ms},
        "State": 0,
        "States": [{}],
        "UUID": "com.elgato.streamdeck.multiactions.delay",
    }

def make_obs_scene_action(scene, collection="Untitled", label=""):
    """Create an OBS Scene switch action."""
    return {
        "ActionID": str(uuid.uuid4()),
        "LinkedTitle": True,
        "Name": "Scene",
        "Plugin": {"Name":"OBS Studio","UUID":"com.elgato.obsstudio","Version":"2.2.9.9"},
        "Resources": None,
        "Settings": {"collection": collection, "scene": scene},
        "State": 0,
        "States": [{"Title": label}],
        "UUID": "com.elgato.obsstudio.scene",
    }

def make_multi_action_from_list(sub_actions, label=""):
    """Create a Multi Action from a list of pre-built action dicts."""
    return {
        "ActionID": str(uuid.uuid4()),
        "Actions": [{"Actions": sub_actions}, {"Actions": []}],
        "LinkedTitle": True,
        "Name": "Multi Action",
        "Plugin": {"Name":"Multi Action","UUID":"com.elgato.streamdeck.multiactions","Version":"1.0"},
        "Resources": None,
        "Settings": {},
        "State": 0,
        "States": [{"Title": label}],
        "UUID": "com.elgato.streamdeck.multiactions.routine",
    }

# Colour palette for auto-icons (used when btn has an "icon" key)
ICON_COLORS = {
    "blue":   (25,  65, 185),
    "purple": (100, 40, 190),
    "orange": (210, 90,  15),
    "teal":   (15, 130, 110),
    "red":    (185, 30,  30),
    "green":  (30, 140,  60),
    "gray":   (80,  80,  90),
}

def build_action(idx, btn):
    row = idx // COLS
    col = idx % COLS
    pos = f"{row},{col}"
    label = btn.get("label", "").replace("\\n", "\n")

    if "open" in btn:
        return pos, make_open_action(btn["open"], label)

    # Pre-built action dict (from make_multi_action_from_list, make_obs_scene_action, etc.)
    if "_action" in btn:
        action = btn["_action"]
        # Apply icon if present
        return pos, action

    if "actions" in btn:
        sub_actions = []
        for step in btn["actions"]:
            if "_action" in step:
                sub_actions.append(step["_action"])
            else:
                sub_actions.append(make_hotkey_action(step["key"], step.get("mods"), ""))
        return pos, {
            "ActionID": str(uuid.uuid4()),
            "Actions": [{"Actions": sub_actions}],
            "LinkedTitle": False,
            "Name": "Multi Action",
            "Plugin": {"Name":"Multi Action",
                       "UUID":"com.elgato.streamdeck.multiactions","Version":"1.0"},
            "Resources": None,
            "Settings": {},
            "State": 0,
            "States": [{"Title": label}],
            "UUID": "com.elgato.streamdeck.multiactions.routine",
        }

    if "key" in btn:
        return pos, make_hotkey_action(btn["key"], btn.get("mods"), label)

    # Fallback for buttons with only label/icon (spacer with icon)
    return pos, {"ActionID": str(uuid.uuid4()), "Name": "Spacer", "States": [{"Title": label}]}


def _build_page(buttons, profile_dir, page_uuid):
    """Build a single page: write manifest + generate icons. Returns action count."""
    actions = {}
    for idx, btn in enumerate(buttons):
        if btn is None:
            continue
        if not btn.get("key") and not btn.get("open") and not btn.get("actions") and not btn.get("_action"):
            continue
        pos, action = build_action(idx, btn)
        actions[pos] = action

    page_dir = os.path.join(profile_dir, "Profiles", page_uuid.upper())
    os.makedirs(page_dir, exist_ok=True)

    page_manifest = {
        "Controllers": [{"Actions": actions, "Type": "Keypad"}],
        "Icon": "",
        "Name": "",
    }

    # Generate icons for buttons that have "icon" and "color" keys
    images_dir = os.path.join(page_dir, "Images")
    for idx, btn in enumerate(buttons):
        if btn is None or "icon" not in btn:
            continue
        if not _ICONS_AVAILABLE:
            break
        os.makedirs(images_dir, exist_ok=True)
        label = btn.get("label", "").replace("\\n", "\n")
        color_name = btn.get("color", "blue")
        bg = ICON_COLORS.get(color_name, ICON_COLORS["blue"])
        img = make_button_icon(btn["icon"], label, bg)
        if img is None:
            continue
        img_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=26)) + 'Z'
        fname = f"{img_id}.png"
        img.save(os.path.join(images_dir, fname))
        pos = f"{idx//COLS},{idx%COLS}"
        if pos in page_manifest["Controllers"][0]["Actions"]:
            page_manifest["Controllers"][0]["Actions"][pos]["States"] = [{"Image": f"Images/{fname}"}]

    with open(os.path.join(page_dir, "manifest.json"), "w") as f:
        json.dump(page_manifest, f, indent=2)

    return len(actions)


def install_profile(name, buttons=None, pages=None, app=None):
    """Install a profile directly into Stream Deck's ProfilesV3 and register it.

    Args:
        name: Profile display name.
        buttons: List of button dicts for a single-page profile (max 15).
        pages: List of lists of button dicts for a multi-page profile (max 15 per page).
               Use this OR buttons, not both.
        app: Optional app bundle path for auto-activation.
    """
    if pages is None and buttons is not None:
        pages = [buttons]
    elif pages is None and buttons is None:
        raise ValueError("Provide either 'buttons' (single page) or 'pages' (multi-page).")

    for i, page_buttons in enumerate(pages):
        if len(page_buttons) > 15:
            print(f"Warning: Page {i+1} has {len(page_buttons)} buttons but only 15 fit. Extras ignored.")
            pages[i] = page_buttons[:15]

    # Generate UUIDs
    profile_uuid = str(uuid.uuid4()).upper()
    page_uuids   = [str(uuid.uuid4()) for _ in pages]
    default_uuid = str(uuid.uuid4())

    # Top-level manifest
    top_manifest = {
        "Device": {"Model": DEVICE_MODEL, "UUID": DEVICE_UUID},
        "Name": name,
        "Pages": {"Current": page_uuids[0], "Default": default_uuid, "Pages": page_uuids},
        "Version": "3.0",
    }
    if app:
        top_manifest["AppIdentifier"] = app

    # Write files
    profile_dir = os.path.join(PROFILES_V3, f"{profile_uuid}.sdProfile")

    total_buttons = 0
    for page_buttons, page_uuid in zip(pages, page_uuids):
        total_buttons += _build_page(page_buttons, profile_dir, page_uuid)

    with open(os.path.join(profile_dir, "manifest.json"), "w") as f:
        json.dump(top_manifest, f, indent=2)

    # Register in plist
    with open(PLIST_PATH, "rb") as f:
        plist = plistlib.load(f)

    dev  = plist.setdefault("Devices", {}).setdefault(DEVICE_UUID, {})
    info = dev.setdefault("ESDProfilesInfo", {})
    uid_lower = profile_uuid.lower()

    for key in ("ESDProfilesSorting", "ESDProfilesExpanded"):
        current = info.get(key, "")
        items   = [x for x in current.split(",") if x] if current else []
        if uid_lower not in items:
            items.append(uid_lower)
        info[key] = ",".join(items)

    with open(PLIST_PATH, "wb") as f:
        plistlib.dump(plist, f)

    page_label = f"{len(pages)} page{'s' if len(pages) > 1 else ''}"
    print(f"✓ Installed '{name}' ({total_buttons} buttons, {page_label})")
    print(f"  Profile UUID: {profile_uuid}")
    print(f"  Reopen Stream Deck to see it.")
    return profile_uuid


# ── Define your profiles here ─────────────────────────────────────────────────
if __name__ == "__main__":
    # Check Stream Deck is closed
    result = subprocess.run(["pgrep", "-x", "Stream Deck"], capture_output=True)
    if result.returncode == 0:
        print("ERROR: Stream Deck is running. Please quit it first, then run this script.")
        sys.exit(1)

    # Example — uncomment and edit to create a profile:
    #
    # install_profile(
    #     name    = "DaVinci Resolve",
    #     app     = "/Applications/DaVinci Resolve/DaVinci Resolve.app",
    #     buttons = [
    #         {"label": "Play",      "key": "space"},
    #         {"label": "Cut",       "key": "b"},
    #         {"label": "Undo",      "key": "z", "mods": ["cmd"]},
    #         {"label": "Redo",      "key": "z", "mods": ["cmd", "shift"]},
    #         {"label": "Color",     "key": "6", "mods": ["shift"]},
    #         {"label": "Edit",      "key": "4", "mods": ["shift"]},
    #         {"label": "Mark In",   "key": "i"},
    #         {"label": "Mark Out",  "key": "o"},
    #         {"label": "Export",    "key": "e", "mods": ["cmd", "shift"]},
    #         {"label": "Zoom Fit",  "key": "z", "mods": ["shift"]},
    #         {"label": "Blade All", "actions": [
    #             {"key": "b", "mods": ["cmd"]},
    #             {"key": "b"},
    #         ]},
    #     ],
    # )

    print("No profiles defined. Edit this script and uncomment an install_profile() call.")
