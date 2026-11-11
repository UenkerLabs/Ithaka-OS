#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Publish site/ to the gh-pages branch (https://uenkerlabs.github.io/Ithaka-OS/).
# Screenshots in site/assets/screens/ are listed by site/screens.txt
# ("file|title|caption" per line) and inserted at <!-- SCREENS -->; without
# screenshots the section is left out.
# Usage: scripts/publish-site.sh [--dry-run DIR]   (dry run: build into DIR only)
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
if [[ "${1:-}" == --dry-run ]]; then
    site=${2:?--dry-run needs a directory}
    rm -rf -- "$site"; mkdir -p -- "$site"
else
    site=$(mktemp -d)
    trap 'rm -rf -- "$site"' EXIT
fi
cp -r "$repo_root/site/." "$site/"
rm -f "$site/screens.txt"
touch "$site/.nojekyll"

python3 - "$repo_root/site/screens.txt" "$site/index.html" <<'PY'
import html, re, sys
from pathlib import Path
listing, page = Path(sys.argv[1]), Path(sys.argv[2])
items = []
if listing.exists():
    for line in listing.read_text().splitlines():
        if line.strip() and not line.startswith('#'):
            name, title, caption = (part.strip() for part in line.split('|', 2))
            items.append(
                f'    <figure><div class="phone"><img src="assets/screens/{name}" '
                f'alt="{html.escape(title)}: {html.escape(caption)}" loading="lazy"></div>'
                f'<figcaption><b>{html.escape(title)}</b>{html.escape(caption)}</figcaption></figure>')
text = page.read_text()
if items:
    text = text.replace('<!-- SCREENS -->', '\n'.join(items))
else:
    text = re.sub(r'<section id="screens".*?</section>\n', '', text, flags=re.S)
    text = text.replace('<a href="#screens">Screens</a>', '')
page.write_text(text)
print(f'{len(items)} screenshot(s)')
PY

[[ "${1:-}" == --dry-run ]] && { echo "Built in $site (dry run)"; exit 0; }
git -C "$site" init -q -b gh-pages
git -C "$site" add -A
# Require a deliberately chosen public commit author; never guess a private e-mail.
: "${ITHAKA_PUBLISH_NAME:?Set ITHAKA_PUBLISH_NAME to the approved public author name}"
: "${ITHAKA_PUBLISH_EMAIL:?Set ITHAKA_PUBLISH_EMAIL to the approved public author e-mail}"
git -C "$site" -c user.name="$ITHAKA_PUBLISH_NAME" -c user.email="$ITHAKA_PUBLISH_EMAIL" \
    commit -q -m "Publish site $(date -u +%F)"
git -C "$site" push -q --force "$(git -C "$repo_root" remote get-url origin)" gh-pages
echo 'Published to gh-pages.'
