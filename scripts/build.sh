#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
image=lineageos4microg/docker-lineage-cicd@sha256:c2591e263815182f1d8469bda40708297d5a28d024ad664bae08bf96bfd9d3fa
mode=${SOURCE_MODE:-pinned}
container=${CONTAINER_NAME:-asteroids-microg-build}
root=$(realpath -m -- "${BUILD_ROOT:-$repo_root/build-data}")
env_file=${BUILD_ENV:-$repo_root/config/build.env.example}
dry_run=false
case "${1:-}" in
    --dry-run) dry_run=true ;;
    '') ;;
    *) printf 'Usage: %s [--dry-run]\n' "$0" >&2; exit 2 ;;
esac
[[ $# -le 1 ]] || exit 2
[[ "$mode" == pinned || "$mode" == tracking ]] || { echo 'SOURCE_MODE must be pinned or tracking' >&2; exit 2; }
[[ "$root" != / && "$root" != "$repo_root" ]] || { echo 'Choose a dedicated BUILD_ROOT directory' >&2; exit 2; }
[[ -f "$env_file" ]] || { echo 'Build environment file not found' >&2; exit 2; }

run() {
    if "$dry_run"; then printf '%q ' "$@"; printf '\n'; else "$@"; fi
}
if "$dry_run"; then
    printf 'Source mode: %s\nBuild directory: %s\n' "$mode" "$root"
else
    command -v docker >/dev/null
    "$repo_root/scripts/prepare-deps.sh"
    mkdir -p "$root"/{src,zips,logs,keys,ccache,tmp,empty-manifests}
    chmod 0700 "$root/keys"
fi

manifests="$repo_root/manifests/tracking"
call_init=true
marker="$root/src/LINEAGE_23_2/.asteroids-pinned-manifest"
if [[ "$mode" == pinned ]]; then
    manifests="$root/empty-manifests"
    call_init=false
    snapshot=${PINNED_MANIFEST:-$(cd "$repo_root" && ls manifests/build-*.xml | sort | tail -n 1)}
    [[ "$snapshot" =~ ^manifests/build-[0-9]{4}-[0-9]{2}-[0-9]{2}\.xml$ && -f "$repo_root/$snapshot" ]] || {
        echo 'PINNED_MANIFEST must name a manifests/build-YYYY-MM-DD.xml file' >&2
        exit 2
    }
    snapshot_hash=$(sha256sum "$repo_root/$snapshot" | cut -d ' ' -f 1)
    "$dry_run" && printf 'Pinned manifest: %s\n' "$snapshot"
    if [[ ! -d "$root/src/LINEAGE_23_2/.repo" ]]; then
        run docker run --rm --entrypoint /bin/bash \
            --volume "$root/src:/srv/src" --env "SNAPSHOT_SHA256=$snapshot_hash" --env "SNAPSHOT=$snapshot" "$image" -c \
            'set -e; mkdir -p /srv/src/LINEAGE_23_2; cd /srv/src/LINEAGE_23_2; repo init -u https://github.com/YZUe1980/leman-os.git -b main -m "$SNAPSHOT" -g default,-darwin --git-lfs; printf "%s\n" "$SNAPSHOT_SHA256" > .asteroids-pinned-manifest'
    elif ! "$dry_run"; then
        [[ -f "$marker" && $(cat "$marker") == "$snapshot_hash" ]] || {
            echo 'Existing sources do not match the recorded pinned checkout. Use a fresh BUILD_ROOT.' >&2
            exit 2
        }
    fi
else
    # A tracking sync moves the tree away from any pinned snapshot.
    run rm -f -- "$marker"
fi

packages=$(awk '!/^#/ && NF {printf "%s%s", sep, $1; sep=" "}' "$repo_root/userscripts/apps.list")
"$dry_run" && printf 'Prebuilt apps: %s\n' "$packages"

run docker run --name "$container" \
    --env-file "$env_file" --env "CALL_REPO_INIT=$call_init" --env "CUSTOM_PACKAGES=$packages" \
    --volume "$root/src:/srv/src" \
    --volume "$root/zips:/srv/zips" \
    --volume "$root/logs:/srv/logs" \
    --volume "$root/keys:/srv/keys" \
    --volume "$root/ccache:/srv/ccache" \
    --volume "$root/tmp:/srv/tmp" \
    --volume "$manifests:/srv/local_manifests:ro" \
    --volume "$repo_root/userscripts:/root/userscripts:ro" \
    "$image"
