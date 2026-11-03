# Next steps on the build machine

Handoff of 2026-11-03 for continuing on the Linux development PC. This is context and a suggested path, not a fixed procedure: where you find a better way, take it, and record what you changed.

Three facts matter whatever the path:

- **Signing keys:** the installed phone only accepts builds signed with the keys from the 2026-10-14 build (in that build's `BUILD_ROOT/keys/`).
- **Repository name before publishing:** builds embed the update address `raw.githubusercontent.com/YZUe1980/tangelo-os/...`, and the Updater does not follow redirects, so the repository should be named `tangelo-os` before a build is offered through it.
- **Firmware:** if the GitLab vendor tree moved to newer Nothing OS firmware, the phone's firmware has to match before flashing.

## 1. Rename the GitHub repository to `tangelo-os`

The repository content already uses the name Tangelo OS and the address `github.com/YZUe1980/tangelo-os`, including the built-in update address. Renaming must happen **before** the next build is published, because the Updater does not follow redirects.

```bash
gh repo rename tangelo-os -R YZUe1980/nothing-phone-3a-pro-lineageos-google-free-aurora --yes
gh repo edit YZUe1980/tangelo-os \
  --description "Tangelo OS: unofficial Android 16 ROM for the Nothing Phone (3a) Pro, based on LineageOS 23.2 with microG, F-Droid and Aurora Store; Infomaniak integration in progress. Open build recipes and documented device tests." \
  --add-topic tangelo-os,infomaniak,fdroid,degoogled
git remote set-url origin https://github.com/YZUe1980/tangelo-os.git
git pull
```

Check that the update list is reachable without a redirect (expect `200`):

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://raw.githubusercontent.com/YZUe1980/tangelo-os/main/ota/v2/devices/asteroids/builds
```

On SourceForge, set the project's display name to **Tangelo OS** (Admin → Project Info). The project address `asteroids-lineage-microg` cannot change and stays.

## 2. Prepare the build machine

```bash
python3 -c 'import PIL' || pip install --user pillow   # boot animation
python3 scripts/check-upstream.py                        # includes the GitLab vendor tree
```

If the vendor tree moved to newer Nothing OS firmware, stop and report before building (see [BUILD.md](BUILD.md), "Updating to current sources").

Optional preview of the boot animation (needs ffmpeg):

```bash
python3 scripts/gen-bootanimation.py /tmp/tangelo-anim --preview /tmp/tangelo-anim/preview.mp4
```

## 3. Build from current sources

Use the **same `BUILD_ROOT`** as the 2026-10-14 build, so the same signing keys are used; otherwise the result cannot update the installed phone.

```bash
SOURCE_MODE=tracking BUILD_ROOT=/path/to/existing/build-data ./scripts/build.sh
BUILD_ROOT=/path/to/existing/build-data ./scripts/export-manifest.sh
```

Then add a build record for the new date in `docs/` (like [BUILD-RECORD.md](BUILD-RECORD.md)) and commit it together with the new manifest.

## 4. Publish and install

```bash
./scripts/publish-sourceforge.sh /path/to/lineage-23.2-YYYYMMDD-UNOFFICIAL-asteroids.zip
git add ota && git commit -m "OTA: <zip name>" && git push
```

On the phone, install the zip with Settings → System → Updater → "Install local update", or follow the Magisk route in [OTA.md](OTA.md). Afterwards check: boot animation, Glyph, the Updater sees the update list, and the full test list in [STATUS.md](STATUS.md).

## 5. After that

The Tangelo OS branding in Settings and the Updater, the Infomaniak apps, privacy defaults and the `user` build follow in the next build; see [ROADMAP.md](ROADMAP.md).
