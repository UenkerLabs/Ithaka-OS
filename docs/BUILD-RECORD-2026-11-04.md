# Third development build: 2026-11-04

Fix-up build after the [2026-11-03 build](BUILD-RECORD-2026-11-03.md), from current sources in the same build directory and with the same signing keys.

## Changes

- **microG signature spoofing on the `user` build.** LineageOS 23.2 honours microG's fake signature only on debuggable builds, so on the 2026-11-03 `user` build the microG self-check failed and apps looking for the Play Store (for example Claude) refused to work. `userscripts/before.sh` removes that single `isDebuggable()` check in `ComputerEngine.isMicrogSigned`; the package allowlist (`com.google.android.gms`, `com.android.vending`) and the check for microG's own signing key stay.
- **No Play Integrity patch** (`APPLY_PI_PATCH=false`, see [SECURITY.md](../SECURITY.md)): the system reports its real bootloader and verified-boot state. The builder resets `system/core` only when it applies the patch, so the patch from the previous build was still in the tree; `userscripts/begin.sh` now removes it before the sync.

Upstream changes since 2026-11-03 (`manifests/build-2026-11-04.xml`, 1,174 projects): only `android`, `hardware/broadcom/libbt`, `hardware/broadcom/wlan`, `lineage/hudson` and `lineage/mirror`; none of them is used by this device's build except the manifest itself.

## Result

The build completed on 2026-11-04 (incremental run 16:01); the builder exited with status 0. All emitted checksums passed.

| Built artifact | SHA-256 |
| --- | --- |
| `lineage-23.2-20261104-UNOFFICIAL-asteroids.zip` (1,854,264,959 bytes) | `b780a2770c17808c8882492157f79dcd1013f6ac2bd0c898027fa604c1972cec` |
| `boot.img` | `70aa3791712b821bf0958f90af99017e1cfee11718670aa3db5e9e841e9af472` |
| `init_boot.img` | `08fc7d0d006b62ac31312b71d8ce78a32a214407b549c44ed9320063d53283f6` |
| `recovery.img` | `3e46467363f02a5c67a70d7938d29758112fbc1508e0c7b4fb407fd8b0da168b` |

Checks on the result:

- **Spoofing fix compiled in:** in the built `system/framework/services.jar`, `ComputerEngine.isMicrogSigned` no longer calls `isDebuggable()`; it checks only the two package names and microG's signature (`Signature.areExactMatch`), verified with `dexdump`.
- **Play Integrity patch absent:** the built `system/bin/init` contains none of the property names the patch adds (`ro.boot.warranty_bit`, `ro.boot.vbmeta.device_state`, `ro.vendor.warranty_bit` and others); `system/core` had no local changes after the sync.
- Signed with the 2026-10-14 release key (OTA certificate SHA-256 `65:D2:A0:DD:…:5E:CC`, as installed on the test phone); A/B OTA package; `ro.build.type=user`, `ro.debuggable=0`; security patch level 2026-10-01.
- Same apps and overlays as the 2026-11-03 build; all 22 radio/firmware images byte-identical to the original firmware baseline.

Device confirmation (microG self-check, Claude sign-in) is pending; see [STATUS.md](STATUS.md).
