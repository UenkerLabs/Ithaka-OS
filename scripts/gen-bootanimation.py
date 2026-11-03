#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the Leman OS boot animation frames.

Usage: scripts/gen-bootanimation.py OUT_DIR [--preview FILE.mp4]

Writes OUT_DIR/bootanimation.tar and OUT_DIR/desc.txt in the layout that
LineageOS's vendor/lineage/bootanimation expects: 3:1 PNG frames in part0
(intro, played once), part1 (loop until boot completes) and part2 (outro).
The build later scales the frames to the screen width and adds the size line
to desc.txt. The output is deterministic, so only this script is versioned.
Requires Pillow (pip install pillow).
"""
from pathlib import Path
import io
import math
import sys
import tarfile

from PIL import Image, ImageDraw

W, H = 1620, 540          # 3:1 canvas, as in LineageOS
SS = 2                    # supersampling for smooth dots
FPS = 60                  # fixed by gen-bootanimation.sh
BG = (0, 0, 0)
DOT = (255, 255, 255)
ACCENT = (255, 69, 69)    # the red of the project banner

# 5x7 dot-matrix glyphs
GLYPHS = {
    'L': ['X....', 'X....', 'X....', 'X....', 'X....', 'X....', 'XXXXX'],
    'E': ['XXXXX', 'X....', 'X....', 'XXXX.', 'X....', 'X....', 'XXXXX'],
    'M': ['X...X', 'XX.XX', 'X.X.X', 'X.X.X', 'X...X', 'X...X', 'X...X'],
    'A': ['.XXX.', 'X...X', 'X...X', 'XXXXX', 'X...X', 'X...X', 'X...X'],
    'N': ['X...X', 'XX..X', 'X.X.X', 'X..XX', 'X...X', 'X...X', 'X...X'],
    'O': ['.XXX.', 'X...X', 'X...X', 'X...X', 'X...X', 'X...X', '.XXX.'],
    'S': ['.XXXX', 'X....', 'X....', '.XXX.', '....X', '....X', 'XXXX.'],
    ' ': ['.....'] * 7,
}
TEXT = 'LEMAN OS'

cols = len(TEXT) * 6 - 1 + 2          # glyphs + gaps + accent dot column
pitch = int(W * 0.78 / cols)
radius = pitch * 0.36
x0 = (W - (cols - 1) * pitch) / 2
y0 = (H - 6 * pitch) / 2

dots = []                              # (x, y, column)
for i, ch in enumerate(TEXT):
    for r, row in enumerate(GLYPHS[ch]):
        for c, cell in enumerate(row):
            if cell == 'X':
                col = i * 6 + c
                dots.append((x0 + col * pitch, y0 + r * pitch, col))
accent = (x0 + (cols - 1) * pitch, y0 + 6 * pitch)


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def frame(levels, accent_level):
    img = Image.new('RGB', (W * SS, H * SS), BG)
    d = ImageDraw.Draw(img)
    for (x, y, _), level in zip(dots, levels):
        if level <= 0.01:
            continue
        r = radius * (0.55 + 0.45 * level) * SS
        v = tuple(int(c * level) for c in DOT)
        d.ellipse([x * SS - r, y * SS - r, x * SS + r, y * SS + r], fill=v)
    if accent_level > 0.01:
        r = radius * SS
        v = tuple(int(c * accent_level) for c in ACCENT)
        d.ellipse([accent[0] * SS - r, accent[1] * SS - r,
                   accent[0] * SS + r, accent[1] * SS + r], fill=v)
    return img.resize((W, H), Image.LANCZOS)


def intro(n=60):
    # Dots switch on column by column, left to right.
    for f in range(n):
        t = f / (n - 1)
        front = t * (cols + 6)
        levels = [ease((front - col) / 6) for _, _, col in dots]
        yield frame(levels, ease((t - 0.85) / 0.15))


def loop(n=90):
    # A soft brightness wave crosses the word; seamless over n frames.
    for f in range(n):
        phase = 2 * math.pi * f / n
        levels = [0.72 + 0.28 * math.cos(phase - col * 0.28) for _, _, col in dots]
        yield frame(levels, 0.75 + 0.25 * math.cos(phase))


def outro(n=30):
    for f in range(n):
        k = 1 - ease(f / (n - 1))
        yield frame([k] * len(dots), k)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    parts = {'part0': list(intro()), 'part1': list(loop()), 'part2': list(outro())}

    with tarfile.open(out / 'bootanimation.tar', 'w', format=tarfile.USTAR_FORMAT) as tar:
        for part, frames in parts.items():
            info = tarfile.TarInfo(part)
            info.type, info.mode, info.mtime = tarfile.DIRTYPE, 0o755, 0
            tar.addfile(info)
            for i, img in enumerate(frames):
                buf = io.BytesIO()
                img.save(buf, 'PNG', optimize=True)
                info = tarfile.TarInfo(f'{part}/{i:03d}.png')
                info.size, info.mode, info.mtime = buf.tell(), 0o644, 0
                buf.seek(0)
                tar.addfile(info, buf)
    # Same structure as LineageOS: intro once, loop until boot completes, outro once.
    (out / 'desc.txt').write_text('c 1 0 part0\nc 0 0 part1\nc 1 0 part2\n')
    print(f'Wrote {out}/bootanimation.tar ({sum(map(len, parts.values()))} frames)')

    if '--preview' in sys.argv:
        import subprocess
        target = sys.argv[sys.argv.index('--preview') + 1]
        frames = parts['part0'] + parts['part1'] * 2 + parts['part2']
        proc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo',
                                 '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                 '-vf', 'scale=810:-2', '-c:v', 'libx264', '-preset', 'veryfast',
                                 '-pix_fmt', 'yuv420p', target], stdin=subprocess.PIPE)
        for img in frames:
            proc.stdin.write(img.tobytes())
        proc.stdin.close()
        proc.wait()
        print(f'Preview: {target}')


if __name__ == '__main__':
    main()
