#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Runs inside the builder before repo sync: undo the F-Droid repository list
# changes made by before.sh, so the sync can update vendor/partner_gms cleanly.
set -euo pipefail
gms=/srv/src/LINEAGE_23_2/vendor/partner_gms
if [[ -d "$gms/.git" || -f "$gms/.git" ]]; then
    git -C "$gms" checkout -- additional_repos.xml
fi
