#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Runs inside the builder before repo sync: undo the source changes made by
# before.sh outside vendor/lineage (which the builder resets itself), so the
# sync can update these projects cleanly.
set -euo pipefail
top=/srv/src/LINEAGE_23_2
reset() {
    if [[ -e "$top/$1/.git" ]]; then
        git -C "$top/$1" checkout -- "$2"
    fi
}
reset vendor/partner_gms additional_repos.xml
reset packages/apps/SetupWizard src/org/lineageos/setupwizard/LineageSettingsActivity.java
reset device/nothing/asteroids sepolicy/vendor/genfs_contexts
reset hardware/nothing sepolicy/glyph/vendor/glyph_app.te
reset frameworks/base services/core/java/com/android/server/pm/ComputerEngine.java
