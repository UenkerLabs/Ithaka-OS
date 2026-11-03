# Preinstalled apps

All preinstalled apps come from the official F-Droid repository and are listed with version code and SHA-256 in `userscripts/apps.list`. `scripts/prepare-deps.sh` downloads and verifies them before every build; `userscripts/before.sh` adds them to the source tree inside the builder. Each APK keeps its original signature, so F-Droid (with its privileged extension) updates them like any other app.

## Current apps

| App | Purpose |
| --- | --- |
| Aurora Store | Google Play catalogue without a Google account |

## Enabling an app

1. Remove the `#` in front of its line in `userscripts/apps.list`, or add a line `Module package - -`.
2. Run `scripts/pin-apps.py`. It looks up F-Droid's newest version, verifies the download against the F-Droid index and records version code and SHA-256. `--update` moves all apps to their newest versions.
3. Commit `userscripts/apps.list`.

A preinstalled system app cannot load compressed native libraries, so the build system rejects such APKs. `pin-apps.py` checks this in advance and stops with a message if an app is unsuitable; that app is then better installed from F-Droid or Aurora after setup.
