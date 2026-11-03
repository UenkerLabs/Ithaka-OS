# Preinstalled apps

All preinstalled apps come from the official F-Droid repository and are listed with version code and SHA-256 in `userscripts/apps.list`. `scripts/prepare-deps.sh` downloads and verifies them before every build; `userscripts/before.sh` adds them to the source tree inside the builder. Each APK keeps its original signature, so F-Droid (with its privileged extension) updates them like any other app.

## Current apps

| App | Purpose |
| --- | --- |
| kSync | Infomaniak contacts and calendars in the system Contacts and Calendar apps |
| Infomaniak Mail | Mail; F-Droid edition without Google push libraries, chosen deliberately over instant push |
| kDrive | Infomaniak cloud files |

Aurora Store is deliberately not preinstalled (since the build after 2026-11-03): it accesses Google Play, whose terms of service make no allowance for third-party clients. It remains available in the F-Droid repository for users who choose it.

## Tangelo OS Apps repository

Apps that are not in the official F-Droid repository come from the project's own F-Droid repository, [tangelo-apps](https://github.com/YZUe1980/tangelo-apps) (`https://yzue1980.github.io/tangelo-apps/repo`, fingerprint `DDCB5AC1B9046E2F380E7AC086E318B0528C5CFA7D26FA148ACAC399209BE05C`). F-Droid has it enabled from the first start: `userscripts/before.sh` adds `userscripts/fdroid-repos.json` to microG's repository list in `/product/etc/org.fdroid.fdroid/`. First app: SafePlace. Proton Mail and Proton Drive are too large for GitHub Pages and are installed through Aurora Store.

## Removed LineageOS apps

`userscripts/removed-packages.list` names LineageOS apps that are left out of the ROM. Currently: Twelve (music player); audio files then open in any player installed later.

## Enabling an app

1. Remove the `#` in front of its line in `userscripts/apps.list`, or add a line `Module package - -`.
2. Run `scripts/pin-apps.py`. It looks up F-Droid's newest version, verifies the download against the F-Droid index and records version code and SHA-256. `--update` moves all apps to their newest versions.
3. Commit `userscripts/apps.list`.

A preinstalled system app cannot load compressed native libraries, so the build system rejects such APKs. `pin-apps.py` checks this in advance and stops with a message if an app is unsuitable; that app is then better installed from F-Droid after setup.

## Infomaniak integration

The ROM is set up around Infomaniak as the main service:

| Area | How |
| --- | --- |
| Contacts, calendars | kSync, Infomaniak's own CardDAV/CalDAV sync app, feeds the system Contacts and Calendar apps |
| Mail | Infomaniak Mail |
| Files | kDrive |
| Device backup | Seedvault (Settings → System → Backup) writes directly to kDrive: the kDrive app is a storage provider (`CloudStorageProvider`, enabled by its "Show in Files" setting) that supports creating and writing files, uploaded by kDrive in the background. This works without WebDAV, which my kSuite+ lacks. Still to be confirmed on the device; fallback: a USB drive |
| Other Infomaniak apps (kMeet, kChat, SwissTransfer, ...) | Install from F-Droid where available; otherwise via Aurora Store, which users can install from F-Droid themselves |

Accounts are signed in after the first boot; the ROM contains no credentials.
