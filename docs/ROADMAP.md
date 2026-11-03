# Roadmap

Decisions as of 2026-11-03. Tangelo OS stays free; it avoids legal grey zones where it can and accepts them only where unavoidable (proprietary device firmware).

## Next build: current sources, Tangelo OS apps and privacy defaults

The first plan was to change one area per build. On 2026-11-03 the following were brought forward into one build instead; it needs a correspondingly thorough device test ([STATUS.md](STATUS.md)) before it is offered through the Updater.

- Tracking build with the upstream changes listed in [UPSTREAM.md](UPSTREAM.md), including the Glyph fixes; re-test Glyph, which is faulty on the 2026-10-14 build.
- First build with the built-in update address ([OTA.md](OTA.md)); zips are published on SourceForge.
- Tangelo OS boot animation (`scripts/gen-bootanimation.py`).
- **Apps** ([APPS.md](APPS.md)): F-Droid as the only bundled store (Aurora Store no longer preinstalled); kSync, Infomaniak Mail and kDrive preinstalled; the project's own F-Droid repository [tangelo-apps](https://github.com/YZUe1980/tangelo-apps) enabled from the first start; Twelve left out.
- **Branding:** "Tangelo OS · LineageOS 23.2" in the Updater and the setup wizard (`userscripts/vendor-tangelo/`). Internal identifiers (`lineage-*.zip`, `ro.lineage.*`, release type) stay unchanged so OTA updates keep working.
- **Privacy defaults** ([PRIVACY.md](PRIVACY.md)): LineageOS statistics opt-in; time from PTB instead of Google.
- **Hardened `user` build** instead of `userdebug`.

## Waiting for accounts

- SourceForge upload key and the project display name "Tangelo OS".

## Later

- Seedvault backup to kDrive, to be confirmed on the device ([APPS.md](APPS.md)).
- Assisted GPS without Qualcomm's servers, if a permitted alternative exists.
- First public release on SourceForge.
