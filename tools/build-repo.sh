#!/bin/bash
# Builds the .deb packages and the repository indexes from the already-built apps.
# Usage: tools/build-repo.sh   (run inside cydia-repo; needs dpkg-deb, dpkg-scanpackages and apt-ftparchive)
set -euo pipefail
cd "$(dirname "$0")/.."
APPS="$(cd .. && pwd)"
BASE_URL="https://douugr.github.io/repo"
MAINT="Douglas Neto <douugr@users.noreply.github.com>"
STAGE="$(mktemp -d)"
mkdir -p debs

# id|name|app|path to .app|section|depends|short description|github repo|extra licenses
PKGS=(
"com.douglasneto.md16|MD16|MD16.app|MD16/build/MD16.app|Games|ch.ringwald.btstack|Mega Drive / Genesis emulator with Bluetooth controller support (8BitDo and others), save states and ROM upload from a browser.|md16|MD16/core/gpgx/LICENSE.txt:genesis-plus-gx.txt"
"com.douglasneto.snes16|SNES16|SNES16.app|SNES16/build/SNES16.app|Games|ch.ringwald.btstack|Super Nintendo emulator (Snes9x 2005) with Bluetooth controller support, save states and ROM upload from a browser.|snes16|SNES16/core/s9x/copyright:snes9x.txt"
"com.douglasneto.psx32|PSX32|PSX32.app|PSX32/build/PSX32.app|Games|ch.ringwald.btstack|PlayStation emulator (PCSX ReARMed with its ARM recompiler) with Bluetooth controller and DualShock support, save states and disc upload from a browser.|psx32|PSX32/core/pcsx/COPYING:pcsx-rearmed-gpl-2.0.txt"
"com.douglasneto.lifecounter|MTG Life|LifeCounter.app|LifeCounter/build/Payload/LifeCounter.app|Games||Life counter for Magic: The Gathering (Commander), 2 to 6 players, with poison and commander damage.|vida-mtg|"
"com.douglasneto.tabletop|Tabletop|Tabletop.app|Tabletop/build/Payload/Tabletop.app|Games||Tabletop RPG battle map with a grid, tokens, HP and initiative order.|mesa-rpg|"
"com.douglasneto.paddeck|PadDeck|PadDeck.app|../paddeck/ipad/build/PadDeck.app|Utilities||Keyboard, trackpad and Stream Deck-style shortcuts for your Mac, over Wi-Fi or a USB cable. Needs the free PadDeck app on the Mac.|paddeck|"
"com.douglasneto.padprobe|PadProbe|PadProbe.app|PadProbe/build/PadProbe.app|Utilities|ch.ringwald.btstack|Bluetooth controller diagnostics via BTstack: shows the raw HID report for every button.|padprobe|"
)

for entry in "${PKGS[@]}"; do
    IFS='|' read -r id name app src section dep desc gh lic <<< "$entry"
    ver="$(python3 -c "import plistlib;print(plistlib.load(open('$APPS/$src/Info.plist','rb')).get('CFBundleShortVersionString','1.0'))")"
    root="$STAGE/$id"
    mkdir -p "$root/DEBIAN" "$root/Applications" "$root/usr/share/doc/$id"
    cp -R "$APPS/$src" "$root/Applications/$app"
    # Permissions: folders 755, files 644, executable 755
    find "$root/Applications" -type d -exec chmod 755 {} +
    find "$root/Applications" -type f -exec chmod 644 {} +
    chmod 755 "$root/Applications/$app/$(python3 -c "import plistlib;print(plistlib.load(open('$APPS/$src/Info.plist','rb'))['CFBundleExecutable'])")"
    deps="firmware (>= 8.0), firmware (<< 11.0)"
    [ -n "$dep" ] && deps="$deps, $dep"
    cat > "$root/DEBIAN/control" <<CTRL
Package: $id
Name: $name
Version: $ver
Architecture: iphoneos-arm
Description: $desc
Maintainer: $MAINT
Author: $MAINT
Section: $section
Depends: $deps
Depiction: $BASE_URL/depictions/$id.html
Homepage: https://github.com/douugr/$gh
Icon: file:///Applications/$app/Icon-76@2x.png
CTRL
    cat > "$root/DEBIAN/postinst" <<'POST'
#!/bin/sh
# Refresh the home screen so the app icon shows up
if [ -x /usr/bin/uicache ]; then su mobile -c /usr/bin/uicache >/dev/null 2>&1 || /usr/bin/uicache >/dev/null 2>&1; fi
exit 0
POST
    cp "$root/DEBIAN/postinst" "$root/DEBIAN/postrm"
    chmod 755 "$root/DEBIAN/postinst" "$root/DEBIAN/postrm"
    {
        echo "$name — https://github.com/douugr/$gh"
        echo "Copyright (C) 2026 Douglas Neto."
        echo
        if [ -n "$lic" ]; then
            f="${lic%%:*}"; out="${lic##*:}"
            echo "This app includes third-party software; the full license is in $out."
            cp "$APPS/$f" "$root/usr/share/doc/$id/$out"
        fi
        if [ -n "$dep" ]; then
            echo "Uses BTstack (C) BlueKitchen GmbH / Matthias Ringwald, installed separately by the $dep package."
        fi
    } > "$root/usr/share/doc/$id/copyright"
    find "$root/usr" -type d -exec chmod 755 {} +
    find "$root/usr" -type f -exec chmod 644 {} +
    deb="debs/${id}_${ver}_iphoneos-arm.deb"
    dpkg-deb -Zgzip --root-owner-group -b "$root" "$deb" >/dev/null
    echo "==> $deb ($(du -h "$deb" | cut -f1))"
done
rm -rf "$STAGE"

# Indexes
dpkg-scanpackages -m debs /dev/null > Packages 2>/dev/null
bzip2 -9c Packages > Packages.bz2
gzip -9nc Packages > Packages.gz
# Release (in Python, so it works on macOS without apt-ftparchive)
python3 - <<'PY'
import hashlib, os, time
files = ["Packages", "Packages.bz2", "Packages.gz"]
lines = [
    "Origin: douugr",
    "Label: douugr \u00b7 apps for legacy iOS",
    "Suite: stable",
    "Version: 1.0",
    "Codename: ios",
    "Architectures: iphoneos-arm",
    "Components: main",
    "Description: Emulators and apps made for old jailbroken iPads (iOS 8 to 10)",
    "Date: " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()),
]
for name, algo in [("MD5Sum", "md5"), ("SHA1", "sha1"), ("SHA256", "sha256")]:
    lines.append(name + ":")
    for f in files:
        data = open(f, "rb").read()
        lines.append(" %s %16d %s" % (hashlib.new(algo, data).hexdigest(), len(data), f))
open("Release", "w").write("\n".join(lines) + "\n")
PY
echo "==> Packages: $(grep -c '^Package:' Packages) packages"
