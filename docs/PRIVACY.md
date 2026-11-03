# Privacy defaults

What Tangelo OS changes compared with LineageOS, and which default connections remain. Tangelo OS stays a free hobby project and avoids legal grey zones where it can, so it does not use other projects' servers without their explicit permission.

## Changed

| Area | LineageOS | Tangelo OS | Since |
| --- | --- | --- | --- |
| LineageOS statistics | Pre-ticked box in the setup wizard; when left on, a device hash, model, version, country and carrier go to `stats.lineageos.org` | Opt-in: the box starts unticked and its text names the LineageOS project and the data sent (`userscripts/before.sh`, `vendor-tangelo` overlay) | Build after 2026-11-03 |
| Build type | `userdebug` | `user`: no `adb root`, no debuggable system | Build after 2026-11-03 |
| Aurora Store | — | Not preinstalled; installable from F-Droid | Build after 2026-11-03 |

The setting can be changed at any time under LineageOS statistics in the Trust settings (Settings → Security & privacy → Trust). Installations from builds up to 2026-10-14 keep whatever was chosen during setup; check it there.

## Pending: own endpoints

Both need an account in the project owner's name; until then the Android defaults stay.

### Connectivity check (captive portal)

Android checks every network with an HTTP and an HTTPS request to Google (`connectivitycheck.gstatic.com`, `www.google.com`). GrapheneOS runs its own endpoints, but there is no statement that other systems may use them, so Tangelo OS does not ship them.

Plan: a minimal own endpoint that answers `/generate_204` with HTTP 204 and no body, for example a free Cloudflare Worker (`infra/connectivity-check/worker.js`). Requirements before it goes into a build:

1. The **HTTP** URL must answer 204 itself and must not redirect to HTTPS; Android detects captive portals through the plain HTTP request. With a Workers custom domain this means turning off "Always Use HTTPS" for that hostname. Verify with `curl -si http://HOST/generate_204` (expect `HTTP/1.1 204` and no `Location` header).
2. The HTTPS URL answers 204 too.
3. Then set `config_captive_portal_http_url`, `config_captive_portal_https_url` and `config_captive_portal_fallback_urls` in a `runtime_resource_overlay` for `com.android.networkstack` in `userscripts/vendor-tangelo/`.

### Time (NTP)

Android asks `time.android.com`. The NTP Pool asks operating systems and devices not to hard-code `pool.ntp.org` but to request a free vendor zone (for example `tangelo.pool.ntp.org`): https://www.ntppool.org/vendors.html. After approval, set `config_ntpServers` to `ntp://<zone>` in a `runtime_resource_overlay` for `android`.

## Not changed yet

- **Assisted GPS:** the Qualcomm GNSS stack downloads satellite data (XTRA) from Qualcomm servers. Replacing them would need a permitted alternative and a fresh GPS test; GPS was validated on the 2026-10-14 build.
- **microG:** optional features (Cloud Messaging, SafetyNet/Play Integrity, network location) connect to Google or other services only when enabled in the microG settings.
- **DNS:** Private DNS stays on Android's automatic mode.
