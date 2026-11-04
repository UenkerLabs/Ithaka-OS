#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the Ithaka OS boot animation frames.

Usage: scripts/gen-bootanimation.py OUT_DIR [--preview FILE.mp4]

Writes OUT_DIR/bootanimation.tar and OUT_DIR/desc.txt in the layout that
LineageOS's vendor/lineage/bootanimation expects: 3:1 PNG frames in part0
(intro, played once), part1 (loop until boot completes) and part2 (outro).
The build later scales the frames to the screen width and adds the size line
to desc.txt. The output is deterministic, so only this script is versioned.

The picture: a round window onto the sea, drawn in dots: the sun rises over
the island of Ithaka while waves run across the water, next to a dot-matrix
ITHAKA wordmark. While the phone boots, the waves keep moving and the sun
glows softly.
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
SUN = (255, 196, 64)
ISLAND = (236, 214, 170)
SEA_NEAR = (40, 120, 220)
SEA_FAR = (110, 190, 255)
WORD = (232, 242, 255)

# --- the window onto the sea -------------------------------------------------
CX, CY, R = 330, 270, 205
PS = 19                    # dot pitch inside the window
HORIZON = CY + 18          # sea below, sky above
SUN_X, SUN_R = CX + 92, 52
scene_dots = []            # (x, y, colour, radius, kind, row)
for gy in range(-R, R + 1, PS):
    for gx in range(-R, R + 1, PS):
        if math.hypot(gx, gy) > R:
            continue
        x, y = CX + gx, CY + gy
        # island: a low hill on the horizon, left of centre
        hill = HORIZON - 62 * math.exp(-((x - (CX - 85)) / 62) ** 2)
        if y >= HORIZON:
            row = (y - HORIZON) // PS
            t = min(row / 9, 1)
            colour = tuple(int(a + (b - a) * t) for a, b in zip(SEA_FAR, SEA_NEAR))
            scene_dots.append((x, y, colour, PS * 0.40, 'sea', row))
        elif y >= hill:
            scene_dots.append((x, y, ISLAND, PS * 0.40, 'island', 0))
        elif math.hypot(x - SUN_X, y - (HORIZON - 22)) <= SUN_R:
            scene_dots.append((x, y, SUN, PS * 0.42, 'sun', 0))
# a ring of dots frames the window
for i in range(72):
    a = 2 * math.pi * i / 72
    scene_dots.append((CX + (R + 16) * math.cos(a), CY + (R + 16) * math.sin(a),
                       (150, 170, 200), PS * 0.22, 'ring', i))

# --- the wordmark ----------------------------------------------------------
GLYPHS = {
    'I': ['XXXXX', '..X..', '..X..', '..X..', '..X..', '..X..', 'XXXXX'],
    'H': ['X...X', 'X...X', 'X...X', 'XXXXX', 'X...X', 'X...X', 'X...X'],
    'K': ['X...X', 'X..X.', 'X.X..', 'XX...', 'X.X..', 'X..X.', 'X...X'],
    'T': ['XXXXX', '..X..', '..X..', '..X..', '..X..', '..X..', '..X..'],
    'A': ['.XXX.', 'X...X', 'X...X', 'XXXXX', 'X...X', 'X...X', 'X...X'],
    'N': ['X...X', 'XX..X', 'X.X.X', 'X..XX', 'X...X', 'X...X', 'X...X'],
    'G': ['.XXX.', 'X...X', 'X....', 'X.XXX', 'X...X', 'X...X', '.XXXX'],
    'E': ['XXXXX', 'X....', 'X....', 'XXXX.', 'X....', 'X....', 'XXXXX'],
    'L': ['X....', 'X....', 'X....', 'X....', 'X....', 'X....', 'XXXXX'],
    'O': ['.XXX.', 'X...X', 'X...X', 'X...X', 'X...X', 'X...X', '.XXX.'],
}
TEXT = 'ITHAKA'
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


def frame(scene_levels, word_levels):
    img = Image.new('RGB', (W * SS, H * SS), BG)
    d = ImageDraw.Draw(img)
    for (x, y, colour, radius, _, _), level in zip(scene_dots, scene_levels):
        dot(d, x, y, radius, colour, level)
    for (x, y, _), level in zip(word_dots, word_levels):
        dot(d, x, y, word_radius, WORD, level)
    return img.resize((W, H), Image.LANCZOS)


def scene_level(kind, x, y, row, t_intro, phase):
    """Brightness of one scene dot. t_intro runs 0..1 during the intro."""
    if kind == 'ring':
        return 0.55 * ease(t_intro * 3)
    if kind == 'sea':
        reveal = ease(t_intro * 2.2 - (x - (CX - R)) / (2 * R))
        wave = 0.78 + 0.22 * math.sin(phase - (x - CX) / 38 + row * 0.9)
        return reveal * wave
    if kind == 'island':
        return ease((t_intro - 0.25) / 0.3)
    # the sun rises: dots appear from the horizon upwards
    rise = (t_intro - 0.15) / 0.55 * (SUN_R * 2 + 60)
    level = ease((rise - (HORIZON - y)) / 40)
    return level * (0.86 + 0.14 * math.cos(phase * 0.5))


def intro(n=78):
    # Ring, then the sea from the left, the island, the sun rising; then the word.
    for f in range(n):
        t = f / (n - 1)
        s = [scene_level(k, x, y, row, t, 0.0) for x, y, _, _, k, row in scene_dots]
        front = (t - 0.4) / 0.6 * (cols + 6)
        w = [ease((front - col) / 6) for _, _, col in word_dots]
        yield frame(s, w)


def loop(n=90):
    # Waves run across the sea; the sun and the word breathe gently. Seamless.
    for f in range(n):
        phase = 2 * math.pi * f / n
        s = [scene_level(k, x, y, row, 1.0, phase) for x, y, _, _, k, row in scene_dots]
        w = [0.84 + 0.16 * math.cos(phase - col * 0.22) for _, _, col in word_dots]
        yield frame(s, w)


def outro(n=30):
    for f in range(n):
        k = 1 - ease(f / (n - 1))
        s = [k * scene_level(kd, x, y, row, 1.0, 0.0) for x, y, _, _, kd, row in scene_dots]
        yield frame(s, [k] * len(word_dots))


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
