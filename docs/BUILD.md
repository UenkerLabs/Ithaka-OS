# Building Tangelo OS

This is a documented development recipe. The first ROM build predates this wrapper; a complete fresh build using the wrapper is still unverified. Nothing here flashes a connected phone automatically.

## Prerequisites

Use Linux with Docker, Bash, curl, Git, Python 3 with Pillow (for the boot animation) and GNU coreutils. A full Android source checkout needs substantial SSD storage. Our first build uses a 12-thread Ryzen 7600X, 30 GiB RAM, an additional 40 GiB swap file, eight parallel jobs and a 50 GiB compiler cache. It started with about 480 GiB free disk space. These are observed development conditions, not a tested minimum specification. The source-generation phase previously exceeded the available physical RAM.

## Source selection

`SOURCE_MODE=pinned` is the default. It initializes a fresh checkout from the newest `manifests/build-*.xml` (set `PINNED_MANIFEST=manifests/build-YYYY-MM-DD.xml` to choose another). The first one, `manifests/build-2026-10-14.xml`, records 1,174 project commit IDs exported from the first build. Its GitHub remote is made explicit and an unused remote was removed; project revisions are unchanged. The wrapper refuses an existing checkout without its matching initialization marker.

`SOURCE_MODE=tracking` uses LineageOS's current `lineage-23.2` manifest plus `manifests/tracking/asteroids.xml`. Device and kernel trees follow NullDebris's `6.6/lineage-23.2` branches. Tracking builds can change when upstream changes. A tracking run removes the pinned-checkout marker, so the same tree is not later mistaken for a pinned checkout.

The container is fixed to:

```text
lineageos4microg/docker-lineage-cicd@sha256:c2591e263815182f1d8469bda40708297d5a28d024ad664bae08bf96bfd9d3fa
```

Pinned source commits do not establish bit-for-bit reproducible binaries. Signing keys, timestamps, runtime downloads and the host environment still matter. The optional runtime Play Integrity patch is checked against the SHA-256 recorded in [BUILD-RECORD.md](BUILD-RECORD.md); a change stops the wrapper build for review.

## Commands

```bash
./scripts/build.sh --dry-run
BUILD_ROOT=/path/to/dedicated/build-data ./scripts/build.sh
```

`--dry-run` prints commands without downloading, creating directories or starting Docker. To follow upstream branches instead:

```bash
SOURCE_MODE=tracking BUILD_ROOT=/path/to/another/build-data ./scripts/build.sh
```

The default output directory is `build-data/` inside the checkout and is Git-ignored. Choose a fresh dedicated directory; do not point the wrapper at another running build. The default container name is `asteroids-microg-build`. An existing container with that name must be deliberately resumed or removed by its operator before creating another.

Prebuilt apps are listed with F-Droid version code and SHA-256 in `userscripts/apps.list`. `prepare-deps.sh` downloads them and refuses any mismatch before they enter the source tree; the APKs are not committed to this repository. Their original signatures are preserved by `android_app_import`. See [APPS.md](APPS.md) for adding apps.

## Settings

`config/build.env.example` records the initial build settings. For local changes, copy it to the ignored `config/build.env` and select it:

```bash
cp config/build.env.example config/build.env
BUILD_ENV="$PWD/config/build.env" ./scripts/build.sh --dry-run
```

`WITH_GMS=true` is the builder's variable name. Here, `vendor/partner_gms` is explicitly the **lineageos4microg** repository, whose package list selects microG, FakeStore, F-Droid and its privileged extension. This is not a bundle of proprietary Google Play Services. `INCLUDE_PROPRIETARY=false` prevents automatic TheMuppets manifest inclusion; the device-specific vendor repository is still required and contains proprietary hardware files.

`BUILD_TYPE=user` (since the build after 2026-11-03; the 2026-10-14 build was `userdebug`) gives a hardened system without `adb root`. `APPLY_PI_PATCH=true` reproduces the initial development configuration. The latter requests an upstream compatibility patch and does not promise Play Integrity, banking or DRM compatibility. `SIGNATURE_SPOOFING=no` is also the recorded setting; microG's actual self-check remains a device-validation item. Change these options deliberately and record the resulting build separately.

## Outputs and signing

The builder writes artifacts under `BUILD_ROOT/zips/asteroids/` and logs under `BUILD_ROOT/logs/asteroids/`. `CLEAN_AFTER_BUILD=false` retains target-files under the source checkout for inspection. Image filenames include the Lineage version, date, release type and codename; do not assume they are simply named `boot.img`.

`SIGN_BUILDS=true` uses locally generated keys under `BUILD_ROOT/keys/`. Keep an offline backup: losing these keys prevents signing updates compatible with the same installation. Never commit the keys or upload the build-data directory. This repository's publication check complements its `.gitignore` by inspecting tracked files before publication.

See [INSTALLATION.md](INSTALLATION.md) for the current installation-validation boundary.

## Checking for upstream changes

`scripts/check-upstream.py` compares the newest pinned manifest with the current upstream branch heads, using `git ls-remote` only. Add `--all` to list unchanged projects too. Tag-pinned AOSP projects are skipped; a new AOSP release appears as a change in `LineageOS/android`. The latest result is recorded in [UPSTREAM.md](UPSTREAM.md).

## Updating to current sources

Steps for the next development build on the build machine:

1. `python3 scripts/check-upstream.py` to see what changed, including the GitLab vendor tree.
2. `SOURCE_MODE=tracking BUILD_ROOT=/path/to/build-data ./scripts/build.sh`. Reusing the existing `BUILD_ROOT` only syncs the changes; keep the same `keys/` directory, otherwise the result cannot update the installed system.
3. `BUILD_ROOT=/path/to/build-data ./scripts/export-manifest.sh` records the exact revisions as `manifests/build-YYYY-MM-DD.xml`; commit it with a new build record.
4. Before flashing, compare the radio/firmware files in the new target-files with the verified original-firmware baseline. If the vendor tree moved to newer Nothing OS firmware, the device firmware must match it.

To offer the result through the Updater, follow [OTA.md](OTA.md).

Updating an installed device in place (for example `adb sideload` of the signed zip in recovery) has not been validated for this project yet. Back up first.
