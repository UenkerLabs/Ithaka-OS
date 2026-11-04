# Tangelo OS development status

Initial status: **2026-10-14**; last updated **2026-11-03**. This page is updated at meaningful milestones, not for every build percentage.

| Item | Evidence / state |
| --- | --- |
| Target hardware | Nothing Phone (3a) Pro A059P, EEA test device |
| Source baseline | LineageOS 23.2 + NullDebris kernel 6.6 trees |
| Source snapshot | 1,174 project revisions exported and pinned |
| Original-firmware preparation | All 38 extracted original images passed their published SHA-256 checks locally |
| First ROM compilation | Completed successfully: 170,777 build steps, container exit 0; output checksums verified |
| Wrapper checks | Bash syntax, pinned/tracking dry runs and tracked-file/manifest checks passed; full fresh build not yet tested |
| GitHub Actions | [First hosted validation passed](https://github.com/YZUe1980/tangelo-os/actions/runs/38529313542); standard Ubuntu runner |
| Clean installation | Full super image and eight slot-A boot-chain images written; data/metadata formatted. Booted successfully; setup completed |
| First boot and encryption | Android 16 / SDK 36 boot completed; file encryption active; SELinux Enforcing |
| SIM / eSIM | eSIM detected and active (2026-11-03) |
| Calls, SMS | Outgoing/incoming calls and SMS work on eSIM (2026-11-03) |
| Mobile data, VoLTE / IMS | Mobile data works; calls stay on 4G/5G with VoLTE (2026-11-03) |
| Wi-Fi | Connects and works (2026-11-03) |
| Bluetooth, GPS | Bluetooth audio and GPS positioning work (2026-11-03) |
| Cameras, fingerprint, audio | Work (2026-11-03) |
| Glyph | Faulty on the 2026-10-14 build. Works on the 2026-11-03 build: LEDs respond to the brightness preview, no SELinux denials for the Glyph app (2026-11-03) |
| microG self-check / Aurora / F-Droid | microG self-check all green; Aurora Store sign-in and app installs work; F-Droid repository update and installs work (2026-11-03) |
| Root | None since the 2026-11-03 `user` build: no root, no Magisk. (Magisk 30.7 root had been verified on the 2026-10-14 `userdebug` build.) |
| Network-default adjustments | On the 2026-10-14 build set by hand (GrapheneOS connectivity check, pool.ntp.org). After the update these manual settings were removed, so the build defaults apply: Android's connectivity check, PTB time servers, LineageOS statistics off (2026-11-03) |
| Device validation | All checks pass on the A059P except Glyph (2026-11-03) |
| Update to the 2026-11-03 build | Installed over the 2026-10-14 build with the Updater's local-update import (A/B, now slot B); data kept. Tangelo OS boot animation, `user` build, SELinux Enforcing, Tangelo overlays active, kSync/Infomaniak Mail/kDrive present, Aurora Store and Twelve gone (2026-11-03) |
| eSIM after the update | No SIM detected after the first boot from slot B: the device's eSIM switch was off and the profile disabled. Turning on Settings → Network & internet → eSIM settings → eSIM and then enabling the profile under SIMs restored service (2026-11-03) |
| Network on the 2026-11-03 build | In service on LTE, mobile data works, IMS/VoLTE registered over LTE; network time synced from `ptbtime1.ptb.de`. A real call and SMS were not placed during this check (2026-11-03) |
| microG signature spoofing on the 2026-11-03 build | **Not working**: the microG self-check shows no signature spoofing and wrong signatures for microG Services and microG Companion. Cause: LineageOS 23.2 honours microG's fake signature only on debuggable builds, and this is the first `user` build. Visible effect: the Claude app refuses sign-in with "Google Play Store missing or disabled"; other Play-dependent apps and push are likely affected too. Fixed for the next build in `userscripts/before.sh` (2026-11-04) |
| 2026-11-04 build | microG signature spoofing restored for the `user` build and the Play Integrity patch removed; both checked in the built system (see [BUILD-RECORD-2026-11-04.md](BUILD-RECORD-2026-11-04.md)). Offered through the Updater; microG self-check and Claude sign-in on the device still to be confirmed (2026-11-04) |
| Tested public ROM release | None yet; the 2026-11-03 build is offered as a development build through the Updater |

The device trees also cover the Phone (3a), but this project has not validated that model. Compilation success, [upstream changes](UPSTREAM.md), upstream reports and hardware testing are recorded separately.

Two installation issues were observed on the A059P: the initial fastboot package's baseband requirement differs from the stock device's version string despite all 22 bundled radio/firmware files being byte-identical, and recovery fastbootd reports a locked state while the hardware bootloader remains unlocked. The successful installation used a full super image directly through the hardware bootloader, with matching slot-A start images. Generic `fastboot update` is not a verified installation method for this build.
