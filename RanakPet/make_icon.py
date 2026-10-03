# -*- coding: utf-8 -*-
"""Render Lunar's head into ranak.ico (the RanakPet app icon).

Builds the Lunar pixel sprite, crops to the head+ears, draws it crisply
(nearest-neighbour) over a smooth pastel circle, and saves a multi-size .ico.
"""
from PIL import Image, ImageDraw
import sprites as S

OUT = "ranak.ico"
FINAL = 256
SS = 4                       # supersample factor for a smooth circle


def hex2rgba(c):
    c = c.lstrip("#")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), 255)


# 1) Lunar sprite grid (no Tk needed) -> crop to head + ears (top 18 rows)
grid = S.build("lunar", face=1)
crop = [row[:] for row in grid[0:18]]
gh, gw = len(crop), len(crop[0])

# 2) crisp character layer at final size (nearest-neighbour keeps pixels sharp)
side = max(gw, gh) + 2
cell = FINAL // side
pad_x = (FINAL - gw * cell) // 2
pad_y = (FINAL - gh * cell) // 2
char = Image.new("RGBA", (FINAL, FINAL), (0, 0, 0, 0))
cd = ImageDraw.Draw(char)
for y, row in enumerate(crop):
    for x, c in enumerate(row):
        if c and c != S.TRANSPARENT:
            x0 = pad_x + x * cell
            y0 = pad_y + y * cell
            cd.rectangle([x0, y0, x0 + cell - 1, y0 + cell - 1], fill=hex2rgba(c))

# 3) smooth pastel circle background (supersampled then downscaled)
big = Image.new("RGBA", (FINAL * SS, FINAL * SS), (0, 0, 0, 0))
bd = ImageDraw.Draw(big)
m = 6 * SS
bd.ellipse([m, m, FINAL * SS - m, FINAL * SS - m], fill=(255, 249, 235, 255),
           outline=(201, 208, 216, 255), width=3 * SS)
bg = big.resize((FINAL, FINAL), Image.LANCZOS)

# 4) composite character over circle, save multi-size .ico
icon = Image.alpha_composite(bg, char)
icon.save(OUT, sizes=[(16, 16), (24, 24), (32, 32), (48, 48),
                      (64, 64), (128, 128), (256, 256)])
print("wrote", OUT)
