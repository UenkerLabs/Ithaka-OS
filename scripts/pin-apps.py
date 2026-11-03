#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Pin the apps in userscripts/apps.list to F-Droid versions.

Usage: scripts/pin-apps.py [--update]

Without --update only unpinned lines ("Module package - -") are filled in;
with --update every active line moves to F-Droid's newest version.
Each APK is downloaded and checked: as a preinstalled system app it must be
zip-aligned and store native libraries uncompressed (the same rule the build
system enforces for presigned, preprocessed apps), otherwise the app could
not load its libraries. Review and commit the resulting apps.list.
"""
from pathlib import Path
import hashlib
import json
import struct
import sys
import tempfile
import urllib.request
import zipfile

root = Path(__file__).resolve().parents[1]
list_path = root / 'userscripts' / 'apps.list'
update_all = '--update' in sys.argv
repo = 'https://f-droid.org/repo'


def fetch(url, dest=None):
    request = urllib.request.Request(url, headers={'User-Agent': 'asteroids-rom-pin-apps'})
    with urllib.request.urlopen(request, timeout=120) as response:
        if dest is None:
            return response.read()
        with open(dest, 'wb') as f:
            while chunk := response.read(1 << 20):
                f.write(chunk)


def embeddable(apk):
    """Return a problem description, or None if the APK can be preinstalled."""
    with zipfile.ZipFile(apk) as z, open(apk, 'rb') as raw:
        for info in z.infolist():
            if info.compress_type != zipfile.ZIP_STORED:
                if info.filename.startswith('lib/') and info.filename.endswith('.so'):
                    return f'compressed native library {info.filename}'
                continue
            raw.seek(info.header_offset)
            header = raw.read(30)
            name_len, extra_len = struct.unpack('<HH', header[26:30])
            data_offset = info.header_offset + 30 + name_len + extra_len
            alignment = 4096 if info.filename.endswith('.so') else 4
            if data_offset % alignment:
                return f'{info.filename} is not {alignment}-byte aligned'
    return None


print('Loading the F-Droid index ...')
index = json.loads(fetch(f'{repo}/index-v2.json'))['packages']

lines = list_path.read_text().splitlines()
changed = False
with tempfile.TemporaryDirectory() as tmp:
    for i, line in enumerate(lines):
        fields = line.split()
        if not fields or fields[0].startswith('#'):
            continue
        module, package, code = fields[0], fields[1], fields[2]
        if code != '-' and not update_all:
            continue
        if package not in index:
            sys.exit(f'{module}: {package} is not in the F-Droid repository')
        versions = index[package]['versions'].values()
        newest = max(versions, key=lambda v: v['manifest']['versionCode'])
        new_code = newest['manifest']['versionCode']
        if str(new_code) == code:
            print(f'{module}: {code} is current')
            continue
        apk = Path(tmp) / f'{module}.apk'
        fetch(repo + newest['file']['name'], apk)
        sha = hashlib.sha256(apk.read_bytes()).hexdigest()
        if sha != newest['file']['sha256']:
            sys.exit(f'{module}: download does not match the F-Droid index')
        if problem := embeddable(apk):
            sys.exit(f'{module} {new_code} cannot be preinstalled: {problem}. '
                     'Leave it to F-Droid or Aurora instead.')
        lines[i] = f'{module:<17} {package:<29} {str(new_code):<12} {sha}'
        name = newest['manifest'].get('versionName', '')
        print(f'{module}: pinned {name} ({new_code})')
        changed = True

if changed:
    list_path.write_text('\n'.join(lines) + '\n')
    print(f'Updated {list_path.relative_to(root)}; review and commit it.')
