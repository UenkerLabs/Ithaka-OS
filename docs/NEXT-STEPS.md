# Next steps

State of 2026-11-03, after the second build. The handoff of the same morning (rename, first OTA build, publication) is done; see [BUILD-RECORD-2026-11-03.md](BUILD-RECORD-2026-11-03.md), [STATUS.md](STATUS.md) and [ROADMAP.md](ROADMAP.md).

## Current GitHub identity and historical naming (verified 2026-11-11)

Ithaka OS replaced the historical Tangelo OS project name on 2026-11-04. The GitHub repository **already exists** at `UenkerLabs/Ithaka-OS`; **do not run the obsolete repository-rename command** from earlier versions of this guide. The old command remains recoverable in Git history.

- Current source: https://github.com/UenkerLabs/Ithaka-OS
- Current expected GitHub Pages URL: https://uenkerlabs.github.io/Ithaka-OS/ (live Pages hostname requires independent HTTPS verification)
- Repository topic `tangelo-os` was still listed in GitHub settings at audit time and should be removed manually; the GitHub connection available to this audit does not support updating topics.
- SourceForge project/user names are a **separate external identity**; do not change `SF_USER`, existing upload paths or OTA download URLs based on GitHub renaming alone.
- For future builds, the pinned-manifest Git remote and sample OTA URL use the current GitHub owner. Existing installed builds may still reference the former OTA URL and require a separate migration test.
- The public site deployment script requires an explicitly approved public Git author name/e-mail; it does not reuse a private or old address.

## Facts for every build

- **Signing keys:** installed phones only accept builds signed with the keys in the build directory's `keys/` (unchanged since 2026-10-14). Keep an offline backup.
- **Memory:** `soong_build` needs about 60 GiB of RAM plus swap; `scripts/build.sh` refuses to start with less.
- **Firmware:** compare the radio images in the new target-files with the original-firmware baseline before publishing (2026-11-03: all 22 identical).

## Making the next build

```bash
python3 scripts/check-upstream.py manifests/build-2026-11-03.xml
SOURCE_MODE=tracking BUILD_ROOT=/path/to/build-data ./scripts/build.sh
BUILD_ROOT=/path/to/build-data ./scripts/export-manifest.sh
```

Then write a build record, check the result on the test phone (update through the Updater, then [STATUS.md](STATUS.md)), and publish:

```bash
./scripts/publish-sourceforge.sh /path/to/lineage-23.2-YYYYMMDD-UNOFFICIAL-asteroids.zip
git add ota && git commit -m "OTA: <zip name>" && git push
```

From the 2026-11-03 build on, phones find new builds in Settings → System → Updater.

## Open

- Confirm that a regular update through the Updater (not a local import) works, and whether the eSIM switch has to be turned on again afterwards ([OTA.md](OTA.md)).
- Place a real call and SMS on the 2026-11-03 build.
- SourceForge display name "Ithaka OS".
- `userscripts/before.sh` carries a local Glyph sepolicy fix; drop it once NullDebris fixes `glyph_app` upstream.
