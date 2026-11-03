#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Add a signed ROM zip to the update list read by the LineageOS Updater.

Usage: scripts/ota-add-build.py ZIP DOWNLOAD_URL [--keep N]

The Updater fetches OTA_URL + /v2/devices/asteroids/builds (see
config/build.env.example). This script reads the zip's OTA metadata, computes
its SHA-256 and writes the newest entry first into ota/v2/devices/<device>/builds.
It does not upload anything: publish the zip at DOWNLOAD_URL first.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys
import zipfile

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
parser.add_argument('zip', type=Path)
parser.add_argument('url')
parser.add_argument('--keep', type=int, default=3, help='number of builds to list (default 3)')
args = parser.parse_args()

if not args.url.startswith('https://'):
    sys.exit('DOWNLOAD_URL must use HTTPS')
name = args.zip.name
match = re.fullmatch(r'lineage-(\d+\.\d+)-\d{8}-([A-Za-z]+)-([a-z0-9_]+)\.zip', name)
if not match:
    sys.exit(f'Unexpected file name: {name}')
version, release_type, device = match.groups()

with zipfile.ZipFile(args.zip) as z:
    raw = z.read('META-INF/com/android/metadata').decode()
meta = dict(line.split('=', 1) for line in raw.splitlines() if '=' in line)
if meta.get('pre-device') != device:
    sys.exit(f"Zip is for {meta.get('pre-device')}, not {device}")

digest = hashlib.sha256()
with args.zip.open('rb') as f:
    for chunk in iter(lambda: f.read(1 << 20), b''):
        digest.update(chunk)

entry = {
    'datetime': int(meta['post-timestamp']),
    'files': [{
        'filename': name,
        'os_patch_level': meta.get('post-security-patch-level'),
        'os_sdk_level': int(meta['post-sdk-level']) if 'post-sdk-level' in meta else None,
        'ota_property_files': meta.get('ota-property-files'),
        'sha256': digest.hexdigest(),
        'size': args.zip.stat().st_size,
        'url': args.url,
    }],
    'type': release_type.lower(),
    'version': version,
}
entry['files'][0] = {k: v for k, v in entry['files'][0].items() if v is not None}

out = root / 'ota' / 'v2' / 'devices' / device / 'builds'
builds = json.loads(out.read_text()) if out.exists() else []
builds = [b for b in builds if b['files'][0]['filename'] != name]
builds = sorted(builds + [entry], key=lambda b: b['datetime'], reverse=True)[:args.keep]
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(builds, indent=2) + '\n')
print(f'{out.relative_to(root)}: {len(builds)} build(s), newest {builds[0]["files"][0]["filename"]}')
