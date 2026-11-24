#!/usr/bin/env python3
# Builds index.html and the package description pages (depictions).
# Plain pages without JavaScript so they open well in Cydia on iOS 8.
import os, shutil, html

BASE = "https://douugr.github.io/repo"
APPS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PKGS = [
    dict(id="com.douglasneto.md16", name="MD16", app="MD16/build/MD16.app", gh="md16",
         tag="Mega Drive / Genesis emulator", needs_bt=True,
         features=["Mega Drive, Master System and Game Gear at 60 fps on an iPad 3",
                   "Bluetooth controller support (tested with the 8BitDo Pro 2) with a button setup assistant",
                   "On-screen controls, 3 save-state slots and autosave",
                   "Cloud saves: sync in-game saves through your own private GitHub repository",
                   "RetroAchievements: unlock achievements as you play and see your progress per game (Casual mode)",
                   "CRT TV filter with scanlines, phosphor mask, composite-video blending and an optional curved screen",
                   "Upload ROMs from your computer's browser (Wi-Fi)",
                   "Automatic IPS/BPS patching and optional run-ahead"],
         license="Uses Genesis Plus GX (non-commercial license; the full text is installed with the app)."),
    dict(id="com.douglasneto.snes16", name="SNES16", app="SNES16/build/SNES16.app", gh="snes16",
         tag="Super Nintendo emulator", needs_bt=True,
         features=["Snes9x 2005 core, light enough for 32-bit devices",
                   "Bluetooth controller support with a button setup assistant (A, B, X, Y, L, R, Start, Select)",
                   "On-screen controls shaped like the original pad",
                   "Cloud saves: sync in-game saves through your own private GitHub repository",
                   "RetroAchievements: unlock achievements as you play and see your progress per game (Casual mode)",
                   "CRT TV filter with scanlines, phosphor mask, composite-video blending and an optional curved screen",
                   "Upload ROMs from a browser and automatic IPS/BPS patching",
                   "3 save-state slots and autosave"],
         license="Uses Snes9x 2005 (non-commercial license; the full text is installed with the app)."),
    dict(id="com.douglasneto.psx32", name="PSX32", app="PSX32/build/PSX32.app", gh="psx32",
         tag="PlayStation emulator", needs_bt=True,
         features=["PCSX ReARMed core with its ARM dynamic recompiler (JIT): Tekken 3 at 60 fps on an iPad 3",
                   "Bluetooth controller support with a setup assistant for every button, plus DualShock analog sticks",
                   "On-screen controls with the four face buttons, L1/L2/R1/R2, Select and Start",
                   "Cloud saves: sync in-game saves through your own private GitHub repository",
                   "RetroAchievements: unlock achievements as you play and see your progress per game (Casual mode)",
                   "CRT TV filter with scanlines, phosphor mask, composite-video blending and an optional curved screen",
                   "Upload disc images from your computer's browser: .chd, .pbp, .cue + .bin, .iso, .m3u for multi-disc games",
                   "Optional BIOS: boot through the console's startup animation, or use the built-in BIOS",
                   "Memory cards per game or shared, with a console-style card screen to copy and delete saves",
                   "3 save-state slots and autosave"],
         license="Uses PCSX ReARMed (GNU GPL v2): the app as a whole is distributed under the GPL v2, and its complete source is on GitHub. No games or BIOS files are included."),
    dict(id="com.douglasneto.lifecounter", name="MTG Life", app="LifeCounter/build/Payload/LifeCounter.app", gh="vida-mtg",
         tag="Life counter for Magic", needs_bt=False,
         features=["2 to 6 players, with panels facing each side of the table",
                   "Poison and commander damage per opponent",
                   "Starting life 20/25/30/40, pick who goes first",
                   "The game is saved and the screen stays on while playing"],
         license=""),
    dict(id="com.douglasneto.tabletop", name="Tabletop", app="Tabletop/build/Payload/Tabletop.app", gh="mesa-rpg",
         tag="Tabletop RPG battle map with tokens", needs_bt=False,
         features=["Grid over any map image, with adjustable grid",
                   "Tokens with color, size, HP and a \"down\" state",
                   "Initiative order with turn and round counter",
                   "Maps from Photos or from images copied to /var/mobile/Documents",
                   "From files, the grid is read from the name (e.g. \"grid 128px (2 m)\")"],
         license=""),
    dict(id="com.douglasneto.paddeck", name="PadDeck", app="../paddeck/ipad/build/PadDeck.app", gh="paddeck",
         tag="Keyboard, trackpad and shortcuts for your Mac", needs_bt=False,
         features=["Needs the free PadDeck app on the Mac: download PadDeck-mac.zip from github.com/douugr/paddeck/releases (macOS 12+)",
                   "Trackpad: tap to click, two-finger right click and scroll with momentum (flick it like a Mac trackpad), double-tap and drag, three-finger swipes for Mission Control and Spaces",
                   "Scroll strip on the edge of the trackpad: scroll with one finger, on the right or left side (can be turned off in Settings)",
                   "Large keyboard with ABC, 123, symbols and fn tabs (esc, F1–F12, arrows, media keys); hold a letter for accents like ç, ã, é",
                   "Keyboard below or above the trackpad, your choice in Settings",
                   "Color profiles that match your Mac: MacBook Neo, Air and Pro finishes and the iMac colors",
                   "Works with any Mac keyboard layout; the iOS keyboard is one tap away for emoji and dictation",
                   "Stream Deck-style panel: 3 pages of 15 buttons for shortcuts, text, opening apps or websites and media keys",
                   "Finds the Mac on Wi-Fi by itself and pairs with a 4-digit PIN",
                   "USB cable mode: plug the iPad into the Mac for lower, steadier latency (no PIN needed)"],
         license="MIT license. Traffic on Wi-Fi is not encrypted: use it on a network you trust."),
    dict(id="com.douglasneto.padprobe", name="PadProbe", app="PadProbe/build/PadProbe.app", gh="padprobe",
         tag="Bluetooth controller diagnostics", needs_bt=True,
         features=["Searches for and connects Bluetooth controllers through BTstack",
                   "Shows the HID reports in hex and highlights what changed",
                   "Handy to find out how a new controller talks to the iPad"],
         license=""),
]

CSS = """
body{margin:0;font-family:-apple-system,'Helvetica Neue',Helvetica,sans-serif;background:#efeff4;color:#1c1c1e;-webkit-text-size-adjust:100%}
.wrap{max-width:640px;margin:0 auto;padding:12px}
.card{background:#fff;border-radius:10px;padding:14px 16px;margin:0 0 12px}
h1{font-size:22px;margin:0}h2{font-size:13px;text-transform:uppercase;letter-spacing:1px;color:#8e8e93;margin:0 0 8px}
.head{display:-webkit-box;display:flex;-webkit-box-align:center;align-items:center}
.head img{width:64px;height:64px;border-radius:14px;margin-right:14px}
.sub{color:#8e8e93;font-size:14px;margin-top:2px}
ul{margin:0;padding-left:20px}li{margin:4px 0;font-size:15px}
p{margin:6px 0;font-size:15px;line-height:1.4}
.warn{background:#fff4e5;color:#7a4b00}
a{color:#0a64d6;text-decoration:none}
.small{font-size:13px;color:#8e8e93}
.btn{display:block;text-align:center;background:#e5413a;color:#fff;border-radius:10px;padding:12px;font-weight:bold;font-size:17px}
.app{display:-webkit-box;display:flex;-webkit-box-align:center;align-items:center;padding:8px 0;border-bottom:1px solid #eee}
.app:last-child{border-bottom:0}.app img{width:44px;height:44px;border-radius:10px;margin-right:12px}
"""

def page(title, body):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head>
<body><div class="wrap">{body}</div></body></html>
"""

os.makedirs(os.path.join(ROOT, "depictions"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)

for p in PKGS:
    icon = f"assets/{p['id']}.png"
    shutil.copyfile(os.path.join(APPS, p["app"], "Icon-76@2x.png"), os.path.join(ROOT, icon))
    feats = "".join(f"<li>{html.escape(f)}</li>" for f in p["features"])
    bt = ""
    if p["needs_bt"]:
        bt = ("<div class='card warn'><p><b>Bluetooth controllers:</b> the BTstack package is installed with it. "
              "Before using it, <b>turn off iOS Bluetooth</b> in Settings and keep <b>Wi-Fi on</b> "
              "(on some iPads both share the same chip).</p></div>")
    lic = f"<p class='small'>{html.escape(p['license'])}</p>" if p["license"] else ""
    body = f"""
<div class="card"><div class="head"><img src="../{icon}"><div><h1>{html.escape(p['name'])}</h1>
<div class="sub">{html.escape(p['tag'])}</div></div></div></div>
<div class="card"><h2>Features</h2><ul>{feats}</ul></div>
{bt}
<div class="card"><h2>Compatibility</h2>
<p>Jailbroken iOS 8 to 10, 32-bit devices (armv7). Tested on an iPad 3 running iOS 8.4.1.</p></div>
<div class="card"><h2>Source code and license</h2>
<p>Open source: <a href="https://github.com/douugr/{p['gh']}">github.com/douugr/{p['gh']}</a></p>{lic}
<p class="small">No ROMs or third-party content are included.</p></div>
"""
    with open(os.path.join(ROOT, "depictions", p["id"] + ".html"), "w") as f:
        f.write(page(p["name"], body))

apps = "".join(
    f"<div class='app'><img src='{'assets/' + p['id'] + '.png'}'><div><b>{html.escape(p['name'])}</b>"
    f"<div class='small'>{html.escape(p['tag'])}</div></div></div>" for p in PKGS)
index = f"""
<div class="card"><div class="head"><img src="CydiaIcon.png"><div><h1>douugr repo</h1>
<div class="sub">Emulators and apps for old jailbroken iPads</div></div></div></div>
<a class="btn" href="cydia://url/https://cydia.saurik.com/api/share#?source={BASE}/">Add to Cydia</a>
<div class="card" style="margin-top:12px"><h2>Repository address</h2><p><b>{BASE}/</b></p>
<p class="small">In Cydia or Melder: Sources → Edit → Add, then paste the address above.</p></div>
<div class="card"><h2>Apps</h2>{apps}</div>
<div class="card"><p class="small">Made by Douglas Neto · source at <a href="https://github.com/douugr">github.com/douugr</a></p></div>
"""
with open(os.path.join(ROOT, "index.html"), "w") as f:
    f.write(page("douugr repo", index))
open(os.path.join(ROOT, ".nojekyll"), "w").close()
print("pages generated:", len(PKGS) + 1)
