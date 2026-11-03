#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Upload a signed ROM zip to SourceForge and add it to the OTA update list.
# Usage: SF_USER=login SF_PROJECT=project ./scripts/publish-sourceforge.sh path/to/lineage-...zip
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
zip=${1:?Usage: SF_USER=login SF_PROJECT=project $0 path/to/zip}
user=${SF_USER:?Set SF_USER to your SourceForge login name}
project=${SF_PROJECT:?Set SF_PROJECT to the project URL name}
name=$(basename -- "$zip")
[[ "$name" =~ ^lineage-[0-9]+\.[0-9]+-[0-9]{8}-[A-Za-z]+-([a-z0-9_]+)\.zip$ ]] || {
    echo "Unexpected file name: $name" >&2
    exit 2
}
device=${BASH_REMATCH[1]}

# rsync resumes an interrupted upload when the command is run again.
rsync -avP --partial -e ssh -- "$zip" "$user@frs.sourceforge.net:/home/frs/project/$project/$device/"

url="https://sourceforge.net/projects/$project/files/$device/$name/download"
"$repo_root/scripts/ota-add-build.py" "$zip" "$url"
printf '\nUploaded. SourceForge mirrors can take a few minutes to pick up a new file.\n'
printf 'Then commit and push ota/ to offer the build:\n  git add ota && git commit -m "OTA: %s" && git push\n' "$name"
