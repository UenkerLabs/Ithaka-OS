# Second development build: 2026-11-03

First build under the name Tangelo OS, from current sources (`SOURCE_MODE=tracking`) in the same build directory and with the same signing keys as the [2026-10-14 build](BUILD-RECORD.md).

| Input | Recorded value |
| --- | --- |
| ROM branch | `lineage-23.2`, AOSP base still `android-16.0.0_r4` |
| Device | `asteroids`, test hardware A059P |
| Device tree | `1c195623f6012da206563f5ed370dda68c489b2a` |
| Kernel tree | `804d18139214e690695ce61908de59e689644778` (unchanged) |
| Vendor tree | `dec51e71456a55af3f5a4d4744c3e2aab726afc4` (unchanged) |
| `hardware/nothing` | `abfabda1602a1948dc153902fe3366dd5318c96d` |
| ParanoidGlyph | `343b5f4b819669591f48e2a0157f65f1eb28bc1f` |
| microG vendor | `8b49146a50de2c7185b63efb53412c972492d7cf` |
| Build type | `user`, `UNOFFICIAL` (2026-10-14: `userdebug`) |
| Preinstalled apps | kSync 4.4.12, Infomaniak Mail 1.31.0, kDrive 5.20.0 ([`apps.list`](../userscripts/apps.list)); Aurora Store and Twelve no longer included |
| Update address | `https://raw.githubusercontent.com/YZUe1980/tangelo-os/main/ota/v2/devices/{device}/builds` |
| Optional runtime patch SHA-256 | `090b9b5a64a78bb2fe2c8f020eda3926f86d473b0d436c4ea6c91f6486dd9bb3` (unchanged) |

The complete project revisions are in `manifests/build-2026-11-03.xml` (1,174 projects). Compared with the newest upstream heads right after the build, only `lineage/mirror` had moved, which the build does not use.

## Changes made during the build

`userscripts/before.sh` changes the synced tree as described in [PRIVACY.md](PRIVACY.md) and [APPS.md](APPS.md): Tangelo OS overlays in `vendor/tangelo` (Updater and setup wizard branding, PTB time servers), the statistics opt-in in the setup wizard, the Tangelo OS Apps repository in F-Droid's list, and the boot animation.

It also fixes an upstream sepolicy problem. Since NullDebris moved the Glyph policy into `hardware/nothing` (2026-10-18), `glyph_app` is a `coredomain` and is granted write access to `sysfs_leds` files, which `system/sepolicy` forbids; `precompiled_sepolicy` failed with a neverallow error. The five `aw20036_led` nodes are now labelled with the device-specific `vendor_sysfs_leds` type, and `glyph_app` is granted that type. Whether Glyph works with it must be confirmed on the device.

## Result

The build completed on 2026-11-03 (final run 31:53 after earlier interrupted runs on the same tree); the builder exited with status 0. All emitted checksums passed.

| Built artifact | SHA-256 |
| --- | --- |
| `lineage-23.2-20261103-UNOFFICIAL-asteroids.zip` (1,854,265,967 bytes) | `5064e09896d7cbcb69860651b466c55d9f26937a8ca9f7cf9a54a52bea5ee3f0` |
| `boot.img` | `d8116d1bf8722fc21929a7d03d45b5792a2159517e6486e197ca4d6fc1279256` |
| `init_boot.img` | `2a896584c7442a27d542c45e273f0d6b80ac62f226ef279fe537b2a2e9e8b09a` |
| `recovery.img` | `8ac11e9a9c83caa72f0906cdd504e462fb87cf5827d1c4066086d25b79fafc07` |
| `vendor_boot.img` | `f3d4ef44d91fa7d9ebf7fad723e2798434d06a4b921e1021b703e1d5481f806e` |
| `dtbo.img` | `94020930c104e6e8fe3e057154ce389080a39ca855d0591c4636ec5382a8cecc` |
| `vbmeta.img` | `203e2f219100915e927ff220960f93ee2c2621414421fdc8d6f552b649fa90f6` |

Checks on the result:

- The zip is an A/B OTA package signed with the 2026-10-14 release key; its OTA certificate matches the one installed on the test phone (SHA-256 `65:D2:A0:DD:…:5E:CC`).
- `ro.build.type=user`, `ro.debuggable=0`; security patch level 2026-10-01, as before.
- The product partition contains GmsCore, FakeStore, F-Droid with its privileged extension, kSync, Infomaniak Mail and kDrive, and the three Tangelo overlays; no Aurora Store, no Twelve. F-Droid's repository list contains microG's two repositories and Tangelo OS Apps. The boot animation is the Tangelo OS one.
- All 22 radio/firmware images in the target-files are byte-identical to the verified original firmware baseline, so no firmware update is needed before installing.

Device validation of this build is still to be done; see [STATUS.md](STATUS.md).
