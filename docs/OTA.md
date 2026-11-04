# Over-the-air updates

Goal: after one more manual installation, new builds arrive through the built-in LineageOS Updater (Settings → System → Updater), without fastboot.

## How it works

The Updater requests a JSON list over HTTPS and offers every entry that matches the device, release type (`unofficial`) and version (`23.2`) and is newer than the installed build. The list request must not redirect; the zip download may.

| Part | Location |
| --- | --- |
| Update list | `ota/v2/devices/asteroids/builds` in this repository, served by raw.githubusercontent.com |
| Built-in address | `OTA_URL` in `config/build.env.example`; the builder appends `/v2/devices/{device}/builds` and writes it into an Updater overlay |
| ROM zip | [SourceForge project files](https://sourceforge.net/projects/asteroids-lineage-microg/files/) (`asteroids/`). A comparable asteroids OTA zip is about 2.6 GB, above GitHub's 2 GiB release-asset limit; Google Drive interposes a virus-scan page for large files |

Builds from 2026-10-14 do not contain this address yet. The first build with `OTA_URL` (2026-11-03) must be installed by other means; afterwards updates come through the Updater.

## Installing the 2026-11-03 build over the 2026-10-14 build

Tested on the A059P on 2026-11-03:

1. Copy `lineage-23.2-20261103-UNOFFICIAL-asteroids.zip` to the phone (for example `adb push … /sdcard/Download/`) and check its SHA-256 against the build record.
2. Settings → System → Updater → ⋮ → "Install local update" (shown in English even on German phones), choose the zip.
3. After "Update imported", tap the imported update, choose Install, wait for the progress bar, then Reboot.

The update is written to the inactive slot; if it does not boot, the phone falls back to the previous slot. Data is kept.

**After the first boot, check the SIM.** On the test phone no SIM was detected until the eSIM was switched on again under Settings → Network & internet → eSIM settings → eSIM, and the profile was enabled under SIMs. Whether this recurs on later updates is not known yet.

## Publishing a build

1. Build with the same `BUILD_ROOT/keys/` as the installed system. A zip signed with different keys cannot be installed over it.
2. `./scripts/publish-sourceforge.sh path/to/zip` uploads the zip with rsync over SSH (rerun to resume) and runs `scripts/ota-add-build.py`, which reads the zip's OTA metadata, computes its SHA-256 and puts the build first in the list (the newest three are kept).
3. Wait a few minutes until SourceForge mirrors serve the file.
4. Commit and push `ota/`. Phones see the build at their next check; raw.githubusercontent.com may cache for a few minutes.

To withdraw a build, remove its entry and push. The Updater deletes partial downloads of entries that disappear from the list.

## Overriding the update address

`lineage.updater.uri` overrides the built-in address until the next reboot. Setting it needs root, which Tangelo OS does not have; it was only possible on the rooted 2026-10-14 build and was not used. Keep a backup and a known-good fastboot image set.
