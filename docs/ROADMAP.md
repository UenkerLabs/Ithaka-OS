# Roadmap

*Name:* Ithaka OS since 2026-11-04 (before: Leman OS, then Tangelo OS; "TANGELO" is a registered software trademark of another company).

Decisions as of 2026-11-03. Ithaka OS stays free; it avoids legal grey zones where it can and accepts them only where unavoidable (proprietary device firmware).

## Next build: current sources, Ithaka OS apps and privacy defaults

The first plan was to change one area per build. On 2026-11-03 the following were brought forward into one build instead; it needs a correspondingly thorough device test ([STATUS.md](STATUS.md)) before it is offered through the Updater.

- Tracking build with the upstream changes listed in [UPSTREAM.md](UPSTREAM.md), including the Glyph fixes; re-test Glyph, which is faulty on the 2026-10-14 build.
- First build with the built-in update address ([OTA.md](OTA.md)); zips are published on SourceForge.
- Ithaka OS boot animation (`scripts/gen-bootanimation.py`).
- **Apps** ([APPS.md](APPS.md)): F-Droid as the only bundled store (Aurora Store no longer preinstalled); kSync, Infomaniak Mail and kDrive preinstalled (an own F-Droid repository was enabled in the 2026-11-03 and 2026-11-04 builds and removed again on 2026-11-04); Twelve left out.
- **Branding:** "Ithaka OS · LineageOS 23.2" in the Updater and the setup wizard (`userscripts/vendor-ithaka/`). Internal identifiers (`lineage-*.zip`, `ro.lineage.*`, release type) stay unchanged so OTA updates keep working.
- **Privacy defaults** ([PRIVACY.md](PRIVACY.md)): LineageOS statistics opt-in; time from PTB instead of Google.
- **Hardened `user` build** instead of `userdebug`.

## Next build: microG fix, no Play Integrity patch

- microG signature spoofing restored on the `user` build (`userscripts/before.sh`); the 2026-11-03 build lost it.
- Play Integrity patch removed (`APPLY_PI_PATCH=false`): the system no longer claims a locked bootloader. Some banking apps may stop working.

## Investigating: relocking the bootloader

1. Build with verified boot enabled (drop `--flags 3`) and an own AVB key instead of the AOSP test key; install it with the bootloader still unlocked and confirm it boots with dm-verity active.
2. Find out whether the A059P accepts an own key (`fastboot flash avb_custom_key`; reported for Nothing phones, not confirmed for this model) and keep an unbrick path ready.
3. Only then lock (`fastboot flashing lock`, which erases all data). Later updates must be signed with the same AVB key.

A locked bootloader with an own key does not pass Google's device integrity check; it protects against tampering, not for app compatibility.

## Waiting for accounts

- SourceForge upload key and the project display name "Ithaka OS".

## Later

- Seedvault backup to kDrive, to be confirmed on the device ([APPS.md](APPS.md)).
- Assisted GPS without Qualcomm's servers, if a permitted alternative exists.
- First public release on SourceForge.
