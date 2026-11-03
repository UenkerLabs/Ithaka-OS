#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compare a pinned build manifest with the current upstream branch heads.

Usage: scripts/check-upstream.py [manifests/build-YYYY-MM-DD.xml] [--all]

Projects pinned to a tag (the AOSP base) are skipped, because tags do not
move; a new AOSP release shows up as a change in LineageOS/android instead.
Only remote refs are queried with `git ls-remote`; nothing is cloned.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
args = [a for a in sys.argv[1:] if not a.startswith('--')]
show_all = '--all' in sys.argv
manifest = Path(args[0]) if args else sorted((root / 'manifests').glob('build-*.xml'))[-1]

tree = ET.parse(manifest).getroot()
remotes = {r.get('name'): r.get('fetch').rstrip('/') for r in tree.findall('remote')}
default = tree.find('default')
default_remote = default.get('remote') if default is not None else None


def check(project):
    remote = project.get('remote', default_remote)
    url = f"{remotes[remote]}/{project.get('name')}"
    upstream = project.get('upstream') or ''
    ref = upstream if upstream.startswith('refs/') else f'refs/heads/{upstream}'
    try:
        out = subprocess.run(['git', 'ls-remote', url, ref], capture_output=True,
                             text=True, timeout=90).stdout.split()
    except subprocess.TimeoutExpired:
        out = []
    head = out[0] if out else None
    if head is None:
        state = 'unreachable'
    elif head == project.get('revision'):
        state = 'unchanged'
    else:
        state = 'changed'
    return state, project.get('path'), url, upstream


projects = [p for p in tree.findall('project')
            if not (p.get('upstream') or '').startswith('refs/tags/')]
skipped = len(tree.findall('project')) - len(projects)
with ThreadPoolExecutor(16) as pool:
    results = list(pool.map(check, projects))

counts = {}
for state, path, url, upstream in sorted(results, key=lambda r: (r[0], r[1])):
    counts[state] = counts.get(state, 0) + 1
    if state != 'unchanged' or show_all:
        print(f'{state:12} {path}  ({upstream})')
summary = ', '.join(f'{n} {s}' for s, n in sorted(counts.items()))
print(f'\n{manifest.name}: {summary}; {skipped} tag-pinned projects skipped.')
