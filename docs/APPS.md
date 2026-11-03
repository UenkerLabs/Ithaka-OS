# Preinstalled apps

All preinstalled apps come from the official F-Droid repository and are listed with version code and SHA-256 in `userscripts/apps.list`. `scripts/prepare-deps.sh` downloads and verifies them before every build; `userscripts/before.sh` adds them to the source tree inside the builder. Each APK keeps its original signature, so F-Droid (with its privileged extension) updates them like any other app.

## Current apps

| App | Purpose |
| --- | --- |
| Aurora Store | Google Play catalogue without a Google account |
| kSync | Infomaniak contacts and calendars in the system Contacts and Calendar apps (planned) |
| Infomaniak Mail | Mail (planned) |
| kDrive | Infomaniak cloud files (planned) |

## Enabling an app

1. Remove the `#` in front of its line in `userscripts/apps.list`, or add a line `Module package - -`.
2. Run `scripts/pin-apps.py`. It looks up F-Droid's newest version, verifies the download against the F-Droid index and records version code and SHA-256. `--update` moves all apps to their newest versions.
3. Commit `userscripts/apps.list`.

A preinstalled system app cannot load compressed native libraries, so the build system rejects such APKs. `pin-apps.py` checks this in advance and stops with a message if an app is unsuitable; that app is then better installed from F-Droid or Aurora after setup.

## Infomaniak integration

The ROM is set up around Infomaniak as the main service:

| Area | How |
| --- | --- |
| Contacts, calendars | kSync, Infomaniak's own CardDAV/CalDAV sync app, feeds the system Contacts and Calendar apps |
| Mail | Infomaniak Mail |
| Files | kDrive |
| Device backup | Seedvault (Settings → System → Backup). kDrive WebDAV is not available on the my kSuite+ plan used here, so the backup target is a storage app that Seedvault lists (to be tested with kDrive) or a USB drive |
| Other Infomaniak apps (kMeet, kChat, SwissTransfer, ...) | Install from Aurora Store after setup |

Accounts are signed in after the first boot; the ROM contains no credentials.
