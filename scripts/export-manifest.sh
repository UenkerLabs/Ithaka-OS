#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Record the exact source revisions of the current build tree as
# manifests/build-YYYY-MM-DD.xml, so the build can be repeated in pinned mode.
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
image=$(sed -n 's/^image=//p' "$repo_root/scripts/build.sh")
root=$(realpath -m -- "${BUILD_ROOT:-$repo_root/build-data}")
date=${BUILD_DATE:-$(date +%F)}
[[ "$date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || { echo 'BUILD_DATE must be YYYY-MM-DD' >&2; exit 2; }
out="$repo_root/manifests/build-$date.xml"
[[ -d "$root/src/LINEAGE_23_2/.repo" ]] || { echo "No source tree in $root/src/LINEAGE_23_2" >&2; exit 2; }
[[ ! -e "$out" ]] || { echo "$out already exists" >&2; exit 2; }

docker run --rm --entrypoint /bin/bash --volume "$root/src:/srv/src:ro" "$image" -c \
    'cd /srv/src/LINEAGE_23_2 && repo manifest -r -o -' > "$out.tmp"
mv -- "$out.tmp" "$out"
printf 'Wrote %s with %s projects.\n' "${out#"$repo_root"/}" "$(grep -c '<project' "$out")"
python3 "$repo_root/scripts/check-publication.py" >/dev/null || {
    echo 'Publication check failed; review the manifest before committing.' >&2
    exit 1
}
