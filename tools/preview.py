"""Render mascots to a PNG contact sheet (no Tk window needed)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image  # noqa: E402

import sprites as S  # noqa: E402


def grid_to_image(grid, scale=1):
    h, w = len(grid), len(grid[0])
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pix = img.load()
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c:
                pix[x, y] = tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    if scale != 1:
        img = img.resize((w * scale, h * scale), Image.NEAREST)
    return img


def sheet(mascots, out, scale=4):
    tiles = []
    for m in mascots:
        for blink in (False, True):
            tiles.append(grid_to_image(S.hd(S.build(m, blink=blink)), scale))
    tw, th = tiles[0].size
    cols = 2
    rows = len(mascots)
    img = Image.new("RGBA", (cols * (tw + 8), rows * (th + 8)), (235, 238, 245, 255))
    for i, t in enumerate(tiles):
        img.alpha_composite(t, ((i % cols) * (tw + 8) + 4, (i // cols) * (th + 8) + 4))
    img.save(out)


if __name__ == "__main__":
    ms = sys.argv[2:] or S.MASCOTS
    sheet(ms, sys.argv[1])
