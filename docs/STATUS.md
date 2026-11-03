# Leman OS development status

Initial status: **2026-10-14**; last updated **2026-11-03**. This page is updated at meaningful milestones, not for every build percentage.

| Item | Evidence / state |
| --- | --- |
| Target hardware | Nothing Phone (3a) Pro A059P, EEA test device |
| Source baseline | LineageOS 23.2 + NullDebris kernel 6.6 trees |
| Source snapshot | 1,174 project revisions exported and pinned |
| Original-firmware preparation | All 38 extracted original images passed their published SHA-256 checks locally |
| First ROM compilation | Completed successfully: 170,777 build steps, container exit 0; output checksums verified |
| Wrapper checks | Bash syntax, pinned/tracking dry runs and tracked-file/manifest checks passed; full fresh build not yet tested |
| GitHub Actions | [First hosted validation passed](https://github.com/YZUe1980/leman-os/actions/runs/38529313542); standard Ubuntu runner |
| Clean installation | Full super image and eight slot-A boot-chain images written; data/metadata formatted. Booted successfully; setup completed |
| First boot and encryption | Android 16 / SDK 36 boot completed; file encryption active; SELinux Enforcing |
| SIM / eSIM | eSIM detected and active (2026-11-03) |
| Calls, SMS | Outgoing/incoming calls and SMS work on eSIM (2026-11-03) |
| Mobile data, VoLTE / IMS | Mobile data works; calls stay on 4G/5G with VoLTE (2026-11-03) |
| Wi-Fi | Connects and works (2026-11-03) |
| Bluetooth, GPS | Bluetooth audio and GPS positioning work (2026-11-03) |
| Cameras, fingerprint, audio | Work (2026-11-03) |
| Glyph | Faulty on the 2026-10-14 build; upstream ParanoidGlyph and Glyph sepolicy changes to be verified in the next build |
| microG self-check / Aurora / F-Droid | microG self-check all green; Aurora Store sign-in and app installs work; F-Droid repository update and installs work (2026-11-03) |
| Optional Magisk root | Magisk 30.7 installed; `su -c id` returned UID 0. Temporary Shell permission revoked afterward |
| Network-default adjustments | Connectivity checks configured for GrapheneOS endpoints; NTP configured for pool.ntp.org. Connectivity and automatic time confirmed (2026-11-03) |
| Device validation | All checks pass on the A059P except Glyph (2026-11-03) |
| Tested public ROM release | None |

The device trees also cover the Phone (3a), but this project has not validated that model. Compilation success, [upstream changes](UPSTREAM.md), upstream reports and hardware testing are recorded separately.

Two installation issues were observed on the A059P: the initial fastboot package's baseband requirement differs from the stock device's version string despite all 22 bundled radio/firmware files being byte-identical, and recovery fastbootd reports a locked state while the hardware bootloader remains unlocked. The successful installation used a full super image directly through the hardware bootloader, with matching slot-A start images. Generic `fastboot update` is not a verified installation method for this build.
