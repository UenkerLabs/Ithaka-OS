# Next steps

State of 2026-11-03, after the second build. The handoff of the same morning (rename, first OTA build, publication) is done; see [BUILD-RECORD-2026-11-03.md](BUILD-RECORD-2026-11-03.md), [STATUS.md](STATUS.md) and [ROADMAP.md](ROADMAP.md).

## Renamed to Ithaka OS (2026-11-04)

The project was called Tangelo OS until 2026-11-04; "TANGELO" is a registered software trademark of another company. Repository content, overlays, boot animation and website already use Ithaka OS and `github.com/YZUe1980/ithaka-os`. Still to do on GitHub and SourceForge:

```bash
gh repo rename ithaka-os -R YZUe1980/tangelo-os --yes
gh repo edit YZUe1980/ithaka-os --description "Ithaka OS: a personal Android 16 system for the Nothing Phone (3a) Pro, based on LineageOS 23.2 with microG, F-Droid and Infomaniak. Open build recipes and documented device tests." --add-topic ithaka-os --remove-topic tangelo-os
git remote set-url origin https://github.com/YZUe1980/ithaka-os.git
./scripts/publish-site.sh
```

and the SourceForge display name "Ithaka OS". Builds up to 2026-11-04 still look for updates at the old `tangelo-os` address; the test phone returns to Nothing OS on 2026-11-04 anyway.

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
