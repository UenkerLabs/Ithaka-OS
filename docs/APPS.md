# Preinstalled apps

All preinstalled apps come from the official F-Droid repository and are listed with version code and SHA-256 in `userscripts/apps.list`. `scripts/prepare-deps.sh` downloads and verifies them before every build; `userscripts/before.sh` adds them to the source tree inside the builder. Each APK keeps its original signature, so F-Droid (with its privileged extension) updates them like any other app.

## Current and planned apps

| App | Purpose | State |
| --- | --- | --- |
| Aurora Store | Google Play catalogue without a Google account | In the 2026-10-14 build |
| Organic Maps | Offline maps and navigation | Planned |
| Proton VPN | VPN | Planned |
| Proton Pass | Password manager (F-Droid edition, separate package from the Play version) | Planned |
| Infomaniak Mail | Mail | Planned |
| Infomaniak kDrive | Cloud files | Planned |
| DAVx⁵ | Contacts and calendar sync over CardDAV/CalDAV | Planned |

Planned apps are enabled in the build after the November 2026 source update, so that problems can be attributed to one change at a time.

## Enabling an app

1. Remove the `#` in front of its line in `userscripts/apps.list`, or add a line `Module package - -`.
2. Run `scripts/pin-apps.py`. It looks up F-Droid's newest version, verifies the download against the F-Droid index and records version code and SHA-256. `--update` moves all apps to their newest versions.
3. Commit `userscripts/apps.list`.

A preinstalled system app cannot load compressed native libraries, so the build system rejects such APKs. `pin-apps.py` checks this in advance and stops with a message if an app is unsuitable; that app is then better installed from F-Droid or Aurora after setup.

## Apps not preinstalled

Proton Mail, Proton Drive and Proton Calendar are not in the F-Droid repository, and no official, stable APK download with documented signing was found. Install them from Aurora Store; Aurora keeps them updated. Proton VPN preinstalled from F-Droid is updated through F-Droid; Aurora can only update it if the Play version is signed with the same key.

## Sync with Infomaniak and Proton

- **Infomaniak** offers CalDAV and CardDAV. With DAVx⁵ the Infomaniak calendars and address books appear in the system Contacts and Calendar apps. Files sync through kDrive, mail through Infomaniak Mail.
- **Proton** does not offer CalDAV or CardDAV for Android, so Proton contacts and calendars stay inside the Proton apps. Push notifications reach these apps through microG.
