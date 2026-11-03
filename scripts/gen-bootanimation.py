#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the Tangelo OS boot animation frames.

Usage: scripts/gen-bootanimation.py OUT_DIR [--preview FILE.mp4]

Writes OUT_DIR/bootanimation.tar and OUT_DIR/desc.txt in the layout that
LineageOS's vendor/lineage/bootanimation expects: 3:1 PNG frames in part0
(intro, played once), part1 (loop until boot completes) and part2 (outro).
The build later scales the frames to the screen width and adds the size line
to desc.txt. The output is deterministic, so only this script is versioned.

The picture: a tangelo slice drawn in dots (orange rind, yellow-to-orange
segments) next to a dot-matrix TANGELO wordmark. The segments fan in one by
one, the slice then glows with a slow ripple while the phone boots.
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
RIND = (255, 112, 20)
FLESH_IN = (255, 214, 92)
FLESH_OUT = (255, 150, 30)
WORD = (255, 244, 224)

# --- the slice -------------------------------------------------------------
CX, CY, R = 330, 270, 205
SEGMENTS = 8
PS = 19                    # dot pitch inside the slice
slice_dots = []            # (x, y, colour, radius, angle 0..1 from top, r/R)
for gy in range(-R, R + 1, PS):
    for gx in range(-R, R + 1, PS):
        r = math.hypot(gx, gy)
        if r > R:
            continue
        ang = (math.atan2(gx, -gy) / (2 * math.pi)) % 1.0
        rr = r / R
        if rr > 0.86:
            colour, size = RIND, 0.42
        else:
            if rr < 0.13:
                continue                       # pale centre
            seg = ang * SEGMENTS
            gap = min(seg % 1, 1 - seg % 1) / SEGMENTS * 2 * math.pi * r
            if gap < PS * 0.75:
                continue                       # white pith between segments
            t = (rr - 0.13) / 0.73
            colour = tuple(int(a + (b - a) * t) for a, b in zip(FLESH_IN, FLESH_OUT))
            size = 0.40
        slice_dots.append((CX + gx, CY + gy, colour, PS * size, ang, rr))

# --- the wordmark ----------------------------------------------------------
GLYPHS = {
    'T': ['XXXXX', '..X..', '..X..', '..X..', '..X..', '..X..', '..X..'],
    'A': ['.XXX.', 'X...X', 'X...X', 'XXXXX', 'X...X', 'X...X', 'X...X'],
    'N': ['X...X', 'XX..X', 'X.X.X', 'X..XX', 'X...X', 'X...X', 'X...X'],
    'G': ['.XXX.', 'X...X', 'X....', 'X.XXX', 'X...X', 'X...X', '.XXXX'],
    'E': ['XXXXX', 'X....', 'X....', 'XXXX.', 'X....', 'X....', 'XXXXX'],
    'L': ['X....', 'X....', 'X....', 'X....', 'X....', 'X....', 'XXXXX'],
    'O': ['.XXX.', 'X...X', 'X...X', 'X...X', 'X...X', 'X...X', '.XXX.'],
}
TEXT = 'TANGELO'
cols = len(TEXT) * 6 - 1
left, right = 640, W - 90
pitch = (right - left) / (cols - 1)
wx0, wy0 = left, CY - 3 * pitch
word_dots = []             # (x, y, column)
for i, ch in enumerate(TEXT):
    for r, row in enumerate(GLYPHS[ch]):
        for c, cell in enumerate(row):
            if cell == 'X':
                col = i * 6 + c
                word_dots.append((wx0 + col * pitch, wy0 + r * pitch, col))
word_radius = pitch * 0.36


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def dot(d, x, y, radius, colour, level):
    if level <= 0.01:
        return
    r = radius * (0.55 + 0.45 * min(level, 1.0)) * SS
    v = tuple(min(255, int(c * level)) for c in colour)
    d.ellipse([x * SS - r, y * SS - r, x * SS + r, y * SS + r], fill=v)


def frame(slice_levels, word_levels):
    img = Image.new('RGB', (W * SS, H * SS), BG)
    d = ImageDraw.Draw(img)
    for (x, y, colour, radius, _, _), level in zip(slice_dots, slice_levels):
        dot(d, x, y, radius, colour, level)
    for (x, y, _), level in zip(word_dots, word_levels):
        dot(d, x, y, word_radius, WORD, level)
    return img.resize((W, H), Image.LANCZOS)


def intro(n=72):
    # Segments fan in clockwise from the top, then the word scans in.
    for f in range(n):
        t = f / (n - 1)
        sweep = t * 1.6
        s = [ease((sweep - ang) / 0.18) for *_, ang, _ in slice_dots]
        front = (t - 0.35) / 0.65 * (cols + 6)
        w = [ease((front - col) / 6) for _, _, col in word_dots]
        yield frame(s, w)


def loop(n=90):
    # A slow ripple runs outward through the slice and along the word.
    for f in range(n):
        phase = 2 * math.pi * f / n
        s = [0.80 + 0.20 * math.cos(phase - rr * 5.0) for *_, rr in slice_dots]
        w = [0.80 + 0.20 * math.cos(phase - col * 0.22) for _, _, col in word_dots]
        yield frame(s, w)


def outro(n=30):
    for f in range(n):
        k = 1 - ease(f / (n - 1))
        yield frame([k] * len(slice_dots), [k] * len(word_dots))


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
