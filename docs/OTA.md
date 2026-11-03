# Over-the-air updates

Goal: after one more manual installation, new builds arrive through the built-in LineageOS Updater (Settings → System → Updater), without fastboot.

## How it works

The Updater requests a JSON list over HTTPS and offers every entry that matches the device, release type (`unofficial`) and version (`23.2`) and is newer than the installed build. The list request must not redirect; the zip download may.

| Part | Location |
| --- | --- |
| Update list | `ota/v2/devices/asteroids/builds` in this repository, served by raw.githubusercontent.com |
| Built-in address | `OTA_URL` in `config/build.env.example`; the builder appends `/v2/devices/{device}/builds` and writes it into an Updater overlay |
| ROM zip | Any public HTTPS address that supports range requests; GitHub release assets are limited to 2 GiB per file |

Builds from 2026-10-14 do not contain this address yet. The first build with `OTA_URL` must be installed by other means; afterwards updates come through the Updater.

## Publishing a build

1. Build with the same `BUILD_ROOT/keys/` as the installed system. A zip signed with different keys cannot be installed over it.
2. Upload `lineage-23.2-YYYYMMDD-UNOFFICIAL-asteroids.zip` and note its download URL.
3. `./scripts/ota-add-build.py path/to/zip DOWNLOAD_URL` reads the zip's OTA metadata, computes its SHA-256 and puts the build first in the list (the newest three are kept).
4. Commit and push `ota/`. Phones see the build at their next check; raw.githubusercontent.com may cache for a few minutes.

To withdraw a build, remove its entry and push. The Updater deletes partial downloads of entries that disappear from the list.

## Testing on a rooted device

`lineage.updater.uri` overrides the built-in address until the next reboot, so the list can be tested on the 2026-10-14 build with Magisk root:

```bash
adb shell su -c 'setprop lineage.updater.uri https://raw.githubusercontent.com/YZUe1980/nothing-phone-3a-pro-lineageos-google-free-aurora/main/ota/v2/devices/{device}/builds'
```

An OTA replaces the patched `init_boot`, so Magisk root is lost after the update unless Magisk's "Install to inactive slot" is used before rebooting.

The override could also deliver the next build to the current installation without fastboot. Neither path has been tested on the A059P yet; keep a backup and a known-good fastboot image set.
