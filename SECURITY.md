# Security

## Reporting a vulnerability

Please report security problems privately through GitHub's "Report a vulnerability" button in the Security tab of this repository, not in a public issue. Include the build date and what an attacker could do.

## How updates and apps are protected

| Part | Protection |
| --- | --- |
| System updates | Every OTA zip is signed with the project's release key; the phone only installs zips signed with the key it was built with. The update list (`ota/`) adds a SHA-256 per zip. A changed list alone cannot install foreign code. |
| Downgrades | The Updater refuses builds older than the installed one. |
| Build inputs | Builder container pinned by digest, source revisions recorded per build, prebuilt apps pinned by F-Droid version code and SHA-256. |
| Preinstalled apps | Original F-Droid signatures; Android only accepts updates signed with the same key. |
| Tangelo OS Apps repository | Built in with a pinned index certificate; F-Droid rejects any index not signed with that key. |
| microG signature spoofing | LineageOS's restricted variant: only `com.google.android.gms` and `com.android.vending`, only when signed with microG's own key, and only Google's signature can be presented. Tangelo OS removes the debuggable-only condition so it works on the `user` build (`userscripts/before.sh`). |
| Build type | `user`: not debuggable, no `adb root`, SELinux Enforcing. |

## What the security rests on

- **The release key** (`BUILD_ROOT/keys/` on the build machine) and the **Tangelo OS Apps keys** (`~/.config/tangelo-apps-keys`). Whoever holds them can sign system updates or repository indexes. The builder's keys are stored without a password, so their protection is the build machine's: disk encryption, no other users, an encrypted offline backup.
- **The GitHub and SourceForge accounts**, which decide what is offered. They cannot sign anything, but should use two-factor authentication.
- **The device trees and vendor files** from NullDebris and the LineageOS and microG projects, which are trusted as upstream sources.

## Known limits

- **Unlocked bootloader.** Anyone with physical access can flash other software. File-based encryption keeps data unreadable without the screen-lock credential, but a modified system could capture it afterwards. Use a PIN or password rather than a pattern. Relocking with a custom AVB key has not been investigated for this device; trying it without that research can make the phone unbootable.
- **No Play Integrity patch** (since the build after 2026-11-04). Earlier builds made the system report a locked bootloader and green verified boot to apps; Tangelo OS now reports the real state. Apps that insist on Google's device integrity checks, such as some banking apps and Google Wallet, may refuse to run.
- **USB debugging** is off by default; turn it off again after use.
