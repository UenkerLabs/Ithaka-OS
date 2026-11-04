# Upstream changes since the pinned build

Check run: **2026-11-03**, against `manifests/build-2026-10-14.xml` with `scripts/check-upstream.py`.

Result: 42 projects changed, 257 unchanged, 872 tag-pinned AOSP projects skipped (still `android-16.0.0_r4`), 3 not checked.

## Device sources (NullDebris)

| Project | Change |
| --- | --- |
| `device/nothing/asteroids` | Glyph sepolicy moved out of the device tree; revert of the 120 Hz SurfaceFlinger `frame_rate_category_high` override; 8 MP ultra-wide camera info in README |
| `hardware/nothing` | Imports the ParanoidGlyph sepolicy; DeviceExtras no longer persistent and stops unnecessary OTG mode writes; vibrator dependency guard |
| `packages/apps/ParanoidGlyph` | Per-notification-channel Glyph animations, app-cache work, Powershare crash fixes (up to 2026-10-31) |
| Kernel, modules, device trees, Dolby, GlyphAdapter | Unchanged |

The device-tree and `hardware/nothing` changes belong together: update both or neither, otherwise the Glyph sepolicy is missing or duplicated.

## microG and apps

| Component | Built | Current |
| --- | --- | --- |
| `vendor/partner_gms` | `f264d80` | GmsCore/FakeStore 0.3.17.252432, F-Droid Privileged Extension 0.2.14, signature checks for all downloaded APKs |
| Aurora Store | 4.8.4 | Not checked automatically |

## LineageOS

- `LineageOS/android`: forks `external/conscrypt` and `system/ca-certificates` (2026-10-21). A fresh sync adds these two projects.
- Chromium WebView 156.0.8078.47.
- NFC: NXP HAL feature handling and an `nfc2` sepolicy label.
- `hardware/qcom-caf/sm8650/display`: `getDisplayConfigurations` API update.
- SystemUI keeps the pure-black theme preference; app updates (Settings, Dialer, Launcher3, Updater and others) and translations.
- No new AOSP security tag yet: the base is still `android-16.0.0_r4`.

## Not checked

- `vendor/nothing/asteroids` (GitLab) and `prebuilts/kernel-build-tools` (googlesource) were unreachable from the checking environment; run the script from the build machine.
- `external/vboot_reference` has no upstream branch in the manifest.
