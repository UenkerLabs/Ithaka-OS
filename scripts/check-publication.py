#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check this small build-config repository before committing or publishing."""
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
blocked_parts = {'keys', 'user-keys', 'build-data', '.cache', 'original-firmware', 'logs', 'src', 'zips'}
blocked_suffixes = {'.apk', '.img', '.zip', '.pk8', '.pem', '.key', '.jks', '.keystore', '.p12', '.pfx', '.log'}
errors = []
for name in filter(None, paths):
    p = root / name
    if blocked_parts.intersection(p.relative_to(root).parts) or p.suffix in blocked_suffixes or '.7z' in p.name or p.name.startswith('adbkey'):
        errors.append(f'Private, binary or generated file: {name}')
        continue
    data = p.read_bytes()
    # Website images (boot animation, icons, reviewed screenshots) are the
    # only binary files allowed, and only below site/assets/.
    if name.startswith('site/assets/') and p.suffix in {'.png', '.webp'}:
        continue
    if b'\x00' in data:
        errors.append(f'Binary file: {name}')
        continue
    content = data.decode('utf-8')
    if re.search(r'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|/mnt/[^/]+/(?:claude|codex)/|(?<![A-Za-z0-9])[0-9A-F]{15,16}(?![A-Za-z0-9])', content):
        errors.append(f'Possible credential or machine-specific data: {name}')

for p in (root / 'manifests').rglob('*.xml'):
    tree = ET.parse(p)
    if p.name.startswith('build-'):
        for project in tree.findall('project'):
            if not re.fullmatch(r'[0-9a-f]{40}', project.get('revision', '')):
                errors.append(f'Unpinned project: {project.get("path", project.get("name"))}')
    for remote in tree.findall('remote'):
        if not remote.get('fetch', '').startswith('https://'):
            errors.append(f'Unexpected remote: {remote.attrib}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Publication checks passed for {len(list(filter(None, paths)))} tracked files.')
