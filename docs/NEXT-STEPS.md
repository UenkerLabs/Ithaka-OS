# Next steps

State of 2026-11-03, after the second build. The handoff of the same morning (rename, first OTA build, publication) is done; see [BUILD-RECORD-2026-11-03.md](BUILD-RECORD-2026-11-03.md), [STATUS.md](STATUS.md) and [ROADMAP.md](ROADMAP.md).

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
- SourceForge display name "Tangelo OS".
- `userscripts/before.sh` carries a local Glyph sepolicy fix; drop it once NullDebris fixes `glyph_app` upstream.
