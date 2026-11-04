# Installation record — A059P, 2026-10-14

The first development build was installed successfully on one Nothing Phone (3a) Pro A059P, starting from Nothing OS `B4.1-260810-1153` and kernel 6.1. It boots Android 16 / SDK 36 with kernel `6.6.114-android15-8-4k-g804d18139214`. Setup completed, file encryption is active and SELinux is Enforcing. This records one device test; other firmware baselines and the non-Pro model remain unvalidated.

## Confirmed sequence

1. Verify ROM artifacts and target-files. Keep original images and signing keys locally. All 38 original images passed published checksums; all 22 firmware/radio inputs matched the original baseline byte for byte.
2. Generate the full sparse `super.img` from the matching target-files using Android's `build_super_image`. Inspect its logical partition layout: this bootstrap image populated slot A, with `system_other` in B.
3. Flash this full super image through the **hardware bootloader**, after verifying its unlocked state. Recovery fastbootd could not be used for this build; see below.
4. Flash matching `boot_a`, `init_boot_a`, `dtbo_a`, `recovery_a`, `vendor_boot_a`, `vbmeta_a`, `vbmeta_system_a` and `vbmeta_vendor_a` images. Select slot A. All eight writes succeeded.
5. Erase and format userdata and metadata using `fastboot -w` with matching Android formatting tools, then reboot. This erased personal data. An unlocked bootloader was required; relocking was not performed.
6. Complete setup, enable USB debugging and authorize the computer. Confirm boot completion, slot, kernel, encryption and SELinux.

The kernel 6.1 → 6.6 transition required a complete matching image set. No public binary release or automated flash script is provided here.

## Observed installation issues

- The generated fastboot package required a different baseband version string from the stock device, despite all 22 firmware files matching exactly. Only the local package's version requirement was adapted after that comparison; image bytes were unchanged. This is not a general recommendation to bypass firmware checks.
- Recovery fastbootd reported a locked device while the hardware bootloader confirmed it was unlocked. The inherited compatibility patch reads `/proc/cmdline` for lock state; its interaction with bootconfig remains to be fixed and tested. Direct full-super flashing succeeded. Generic `fastboot update` is **not verified** for this build.
- During setup, Android's trade-in ADB mode exposed a transport but closed ordinary shell services. Completing setup and enabling USB debugging restored normal ADB operation.

## Root on the 2026-10-14 build (historical)

Tangelo OS has no root and no Magisk since the 2026-11-03 `user` build. For the record: on the 2026-10-14 `userdebug` build, after the unmodified ROM booted, official Magisk **30.7 (30700)** was installed. Following [Magisk's documentation](https://topjohnwu.github.io/Magisk/install.html), the exact ROM's `init_boot.img` was patched **on the same phone**, preserving verity and encryption, and flashed to the confirmed current partition `init_boot_a`.

The root daemon ran as root. A temporarily authorized Shell request returned `uid=0(root)` with Magisk's SELinux context. Shell permission was then revoked and a repeat request returned `Permission denied`, as requested by the owner. The test used `/debug_ramdisk/su`; plain `su` was not on the shell PATH. Patched images remain local and are not distributed for other devices. A further reboot completed successfully with Magisk active.

## Device-local network settings

Connectivity-check HTTP, HTTPS and fallback URLs were set to GrapheneOS's `connectivitycheck.grapheneos.network/generate_204` endpoints, using corresponding HTTP/HTTPS schemes. Additional fallback URL settings were cleared. NTP was configured as `ntp://pool.ntp.org`. These are device-local settings, not yet build-time defaults in this repository.

Values persisted across reboot. The phone had no active internet connection during validation, so connectivity checks and actual time synchronization remain unverified. Aurora accesses Google Play and optional microG services can use Google infrastructure; see the README's definition of “Google free”.
