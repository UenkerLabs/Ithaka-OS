# Privacy defaults

What Ithaka OS changes compared with LineageOS, and which default connections remain. Ithaka OS stays a free hobby project and avoids legal grey zones where it can, so it does not use other projects' servers without their explicit permission.

## Changed

| Area | LineageOS | Ithaka OS | Since |
| --- | --- | --- | --- |
| LineageOS statistics | Pre-ticked box in the setup wizard; when left on, a device hash, model, version, country and carrier go to `stats.lineageos.org` | Opt-in: the box starts unticked and its text names the LineageOS project and the data sent (`userscripts/before.sh`, `vendor-ithaka` overlay) | Build after 2026-11-03 |
| Build type | `userdebug` | `user`: no `adb root`, no debuggable system | Build after 2026-11-03 |
| Aurora Store | — | Not preinstalled; installable from F-Droid | Build after 2026-11-03 |
| Time (NTP) | `time.android.com` (Google) | `ptbtime1`–`ptbtime3.ptb.de`, the public NTP service of Germany's national metrology institute PTB (`IthakaFrameworkOverlay`) | Build after 2026-11-03 |

The setting can be changed at any time under LineageOS statistics in the Trust settings (Settings → Security & privacy → Trust). Installations from builds up to 2026-10-14 keep whatever was chosen during setup; check it there.

## Connectivity check: Android default kept

Android checks every network with an HTTP and an HTTPS request to Google (`connectivitycheck.gstatic.com`, `www.google.com`); Google learns that the device is online, nothing else. Ithaka OS keeps this default (decision of 2026-11-03):

- GrapheneOS runs its own endpoints, but there is no statement that other systems may use them.
- Turning the check off would also turn off captive-portal sign-in pages (hotel, train Wi-Fi) and the switch to mobile data when Wi-Fi has no internet.
- An own endpoint needs a hosting account. Should one exist later: `infra/connectivity-check/worker.js` answers `/generate_204` with HTTP 204. The **HTTP** URL must answer 204 itself, without redirecting to HTTPS, because captive portals are detected through the plain HTTP request (`curl -si http://HOST/generate_204`: `HTTP/1.1 204`, no `Location` header). Then set `config_captive_portal_http_url`, `config_captive_portal_https_url` and `config_captive_portal_fallback_urls` in a `runtime_resource_overlay` for `com.android.networkstack`.

## Not changed yet

- **Assisted GPS:** the Qualcomm GNSS stack downloads satellite data (XTRA) from Qualcomm servers. Replacing them would need a permitted alternative and a fresh GPS test; GPS was validated on the 2026-10-14 build.
- **microG:** optional features (Cloud Messaging, SafetyNet/Play Integrity, network location) connect to Google or other services only when enabled in the microG settings.
- **DNS:** Private DNS stays on Android's automatic mode.
