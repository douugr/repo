# douugr Cydia repository

Emulators and apps made for **old jailbroken iPads** (iOS 8 to 10, 32-bit devices).

**Address:** `https://douugr.github.io/repo/`

In Cydia or Melder: **Sources → Edit → Add**, then paste the address.

| App | Description | Source |
| --- | --- | --- |
| MD16 | Mega Drive / Genesis emulator with Bluetooth controller support | [douugr/md16](https://github.com/douugr/md16) |
| SNES16 | Super Nintendo emulator with Bluetooth controller support | [douugr/snes16](https://github.com/douugr/snes16) |
| MTG Life | Life counter for Magic (Commander) | [douugr/vida-mtg](https://github.com/douugr/vida-mtg) |
| Tabletop | Tabletop RPG battle map with tokens and initiative | [douugr/mesa-rpg](https://github.com/douugr/mesa-rpg) |
| PadProbe | Bluetooth controller diagnostics | [douugr/padprobe](https://github.com/douugr/padprobe) |

## Updating the repository

The apps are built in the sibling folders (`../MD16`, `../SNES16`...). After building:

```bash
tools/update.sh     # builds the .debs, the indexes (Packages/Release) and the pages
git add -A && git commit -m "Update packages" && git push
```

To ship a new version of an app, bump `CFBundleShortVersionString` in its `Info.plist` before building: Cydia only offers the update when the version changes.

Needs `dpkg` on the Mac (`brew install dpkg`) for `dpkg-deb`, `dpkg-scanpackages` and `apt-ftparchive`.
