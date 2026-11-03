#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Download and verify the prebuilt apps listed in userscripts/apps.list.
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
apps_dir="$repo_root/userscripts/apps"
mkdir -p "$apps_dir" "$repo_root/.cache"
download=$(mktemp "$repo_root/.cache/app.XXXXXX")
trap 'rm -f -- "$download"' EXIT
verify() { printf '%s  %s\n' "$1" "$2" | sha256sum --check --status; }

while read -r module package code sha; do
    [[ -z "$module" || "$module" == \#* ]] && continue
    [[ "$code" =~ ^[0-9]+$ && "$sha" =~ ^[0-9a-f]{64}$ ]] || {
        echo "$module is not pinned yet; run scripts/pin-apps.py" >&2
        exit 2
    }
    target="$apps_dir/$module.apk"
    if [[ -f "$target" ]] && verify "$sha" "$target"; then
        printf '%s %s: verified.\n' "$module" "$code"
        continue
    fi
    # F-Droid moves older versions from repo/ to archive/.
    curl --fail --location --retry 3 --connect-timeout 30 --silent --show-error \
        "https://f-droid.org/repo/${package}_${code}.apk" --output "$download" ||
    curl --fail --location --retry 3 --connect-timeout 30 --silent --show-error \
        "https://f-droid.org/archive/${package}_${code}.apk" --output "$download"
    verify "$sha" "$download" || { echo "$module: SHA-256 mismatch" >&2; exit 1; }
    install -m 0644 "$download" "$target"
    printf '%s %s: downloaded and verified.\n' "$module" "$code"
done < "$repo_root/userscripts/apps.list"

# Leman OS boot animation, generated from scripts/gen-bootanimation.py.
python3 -c 'import PIL' 2>/dev/null || {
    echo 'The boot animation needs Pillow: pip install --user pillow (or the python3-pil package)' >&2
    exit 2
}
python3 "$repo_root/scripts/gen-bootanimation.py" "$repo_root/userscripts/bootanimation"
