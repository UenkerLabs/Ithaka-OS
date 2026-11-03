# Roadmap

Decisions as of 2026-11-03. Each build changes one area at a time, so problems can be attributed.

## Next build: current sources

- Tracking build with the upstream changes listed in [UPSTREAM.md](UPSTREAM.md), including the Glyph fixes.
- First build with the built-in update address ([OTA.md](OTA.md)); zips are published on SourceForge.
- Twelve (music player) is left out ([APPS.md](APPS.md)).
- Re-test Glyph, which is faulty on the 2026-10-14 build.

## Build after that: Leman OS

- **New name: Leman OS**, based on LineageOS 23.2. Shown in Settings and the Updater, README, GitHub repository name and SourceForge display name. Internal identifiers (`lineage-*.zip`, `ro.lineage.*`, release type) stay unchanged so OTA updates keep working. User-visible strings to override include the Updater's `brand_name`, `header_build_version`, `list_build_version` and `list_build_version_date`, in the default and German resources.
- **Infomaniak integration** ([APPS.md](APPS.md)): kSync, Infomaniak Mail and kDrive from F-Droid (fully free editions, no instant push needed); Seedvault backup to the kDrive storage provider.
- **Privacy defaults** and a **hardened `user` build** instead of `userdebug`; details still to be worked out.

## Later

- First public release on SourceForge.
