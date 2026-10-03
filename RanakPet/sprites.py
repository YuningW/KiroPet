"""Pixel-art sprite builder for the Kiro pets (8-bit style)."""

import tkinter as tk

W, H = 22, 24                     # sprite grid
TRANSPARENT = "#0b1e0c"           # -> transparent on the pet window

MASCOTS = ["muvmuv", "lunar", "any", "whitedog", "goldie_red", "goldie_brown",
           "lolo", "butterbear"]
LABELS = {
    "muvmuv": "MuvMuv", "lunar": "Lunar", "any": "Any",
    "whitedog": "Shiro", "goldie_red": "Goldie ❤", "goldie_brown": "Goldie \U0001f9e5",
    "lolo": "LOLO \U0001f353", "butterbear": "Butter bear",
}

EYE = "#39304a"
HI = "#ffffff"


# ----------------------------------------------------------- grid helpers
def new_grid():
    return [[None] * W for _ in range(H)]


def px(g, x, y, c):
    if c and 0 <= x < W and 0 <= y < H:
        g[y][x] = c


def rect(g, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px(g, x, y, c)


def disc(g, cx, cy, r, c):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + 1:
                px(g, x, y, c)


def odisc(g, cx, cy, r, fill, outline):
    disc(g, cx, cy, r, outline)
    disc(g, cx, cy, r - 1, fill)


def tri_up(g, tipx, basey, h, w, c):
    for i in range(h):
        half = int((w / 2) * i / max(1, h - 1))
        rect(g, tipx - half, basey - i, tipx + half, basey - i, c)


def eyes(g, lx, rx, ey, blink, col=EYE):
    for ex in (lx, rx):
        if blink:
            rect(g, ex - 2, ey, ex + 2, ey, col)
            continue
        rect(g, ex - 1, ey - 1, ex + 1, ey + 1, col)          # 3x3 core
        px(g, ex, ey + 2, col)                                 # teardrop chin
        rect(g, ex - 1, ey - 1, ex, ey, HI)                    # 2x2 glossy shine


def dot_eyes(g, lx, rx, ey, blink, col=EYE):
    for ex in (lx, rx):
        if blink:
            rect(g, ex - 1, ey, ex + 1, ey, col)
        else:
            rect(g, ex - 1, ey - 1, ex + 1, ey + 1, col)       # 3x3 dot
            px(g, ex - 1, ey - 1, HI)                          # shine


def feet(g, lx, rx, y, fill, outline, foot):
    off = 1 if foot else 0
    odisc(g, lx, y + off, 2, fill, outline)
    odisc(g, rx, y - off, 2, fill, outline)


# ----------------------------------------------------------- mascots
def rot_cw(g):
    """Rotate a grid 90 degrees clockwise."""
    return [list(row) for row in zip(*g[::-1])]


def build(mascot, blink=False, foot=0, face=1, rot=0):
    g = new_grid()
    {
        "muvmuv": _muvmuv, "lunar": _lunar, "any": _any,
        "whitedog": _whitedog,
        "goldie_red": lambda g, b, f: _goldie(g, b, f, "red"),
        "goldie_brown": lambda g, b, f: _goldie(g, b, f, "brown"),
        "lolo": _lolo, "butterbear": _butterbear,
    }[mascot](g, blink, foot)
    if face < 0:
        g = [row[::-1] for row in g]
    for _ in range(rot % 4):
        g = rot_cw(g)
    return g


def _muvmuv(g, blink, foot):
    b, ol, cr, pk, bl = "#f4a259", "#cf7a30", "#fff3e6", "#ff8fb0", "#ffc2cf"
    feet(g, 8, 14, 20, cr, ol, foot)
    odisc(g, 11, 15, 6, b, ol)                 # body
    for ex in (7, 15):                          # ears
        tri_up(g, ex, 5, 5, 6, ol)
        tri_up(g, ex, 4, 4, 4, b)
        tri_up(g, ex, 3, 2, 2, pk)
    odisc(g, 11, 9, 7, b, ol)                   # head
    disc(g, 11, 11, 4, cr)                      # cream muzzle
    eyes(g, 7, 15, 8, blink)
    rect(g, 10, 10, 12, 10, pk); px(g, 11, 11, "#a85a3a")   # nose
    for wy in (10, 12):                         # whiskers
        px(g, 3, wy, ol); px(g, 4, wy, ol); px(g, 18, wy, ol); px(g, 19, wy, ol)
    rect(g, 5, 11, 6, 12, bl); rect(g, 16, 11, 17, 12, bl)  # blush


def _lunar(g, blink, foot):
    w, ol, bk = "#ffffff", "#c9d0d8", "#26292f"
    ylo, yld, teal = "#ffcf3f", "#e6a81e", "#27bcd0"
    # egg / penguin body
    odisc(g, 11, 16, 6, w, ol)
    disc(g, 5, 15, 2, bk); disc(g, 17, 15, 2, bk)           # black flippers
    off = 1 if foot else 0
    odisc(g, 8, 22 - off, 2, ylo, yld)                       # yellow duck feet
    odisc(g, 14, 22 + off, 2, ylo, yld)
    # panda ears
    disc(g, 5, 3, 3, bk); disc(g, 17, 3, 3, bk)
    # teal flower on right ear
    for dx, dy in ((0, -2), (-2, 0), (2, 0), (0, 2), (-1, -1), (1, 1), (1, -1), (-1, 1)):
        px(g, 17 + dx, 3 + dy, teal)
    px(g, 17, 3, "#fff6b0")
    # head
    odisc(g, 11, 9, 7, w, ol)
    disc(g, 7, 8, 3, bk); disc(g, 15, 8, 3, bk)             # eye patches
    for ex in (7, 15):                                       # eyes in patches
        disc(g, ex, 8, 2, w)
        if blink:
            rect(g, ex - 1, 8, ex + 1, 8, bk)
        else:
            disc(g, ex, 8, 1, bk)
            px(g, ex, 7, "#3fd6e6"); px(g, ex - 1, 7, HI)
    # yellow duck beak
    rect(g, 9, 11, 13, 12, ylo); px(g, 8, 11, ylo); px(g, 14, 11, ylo)
    rect(g, 9, 13, 13, 13, yld)
    rect(g, 4, 11, 5, 12, "#ffb3c8"); rect(g, 17, 11, 18, 12, "#ffb3c8")


def _any(g, blink, foot):
    w, ol, hair, skin = "#ffffff", "#e3e5ea", "#2b2530", "#fdeee4"
    feet(g, 8, 14, 21, w, ol, foot)
    odisc(g, 11, 16, 6, w, ol)                  # body/hood
    disc(g, 11, 20, 1, "#ff9ec4")               # tiny heart
    for ex in (8, 14):                          # bunny ears
        rect(g, ex - 1, 0, ex + 1, 6, w); px(g, ex - 2, 4, w); px(g, ex + 2, 4, w)
        rect(g, ex, 1, ex, 4, "#ffd0e0")
    odisc(g, 11, 9, 7, w, ol)                   # hood
    disc(g, 11, 9, 6, hair)                     # bob hair
    disc(g, 11, 11, 4, skin)                    # pale face
    rect(g, 7, 6, 15, 8, hair)                  # bangs
    px(g, 8, 9, hair); px(g, 8, 10, hair)       # side-swept lock
    px(g, 5, 7, "#ff7aa8"); px(g, 5, 8, "#ffb14a"); px(g, 6, 6, "#7fd0ff")  # clips
    dot_eyes(g, 9, 13, 11, blink)
    px(g, 11, 13, "#cc6680")                    # tiny mouth
    rect(g, 7, 12, 8, 12, "#ffb3c8"); rect(g, 14, 12, 15, 12, "#ffb3c8")


def _whitedog(g, blink, foot):        # Shiro
    w, ol, bk, blu = "#ffffff", "#d3d8de", "#3a3540", "#4aa8e0"
    odisc(g, 11, 16, 6, w, ol)                  # body
    feet(g, 8, 14, 21, w, ol, foot)
    odisc(g, 4, 16, 2, w, ol); odisc(g, 18, 16, 2, w, ol)  # arms
    rect(g, 6, 14, 16, 15, blu); px(g, 11, 16, blu)        # blue collar
    rr(g, 3, 5, 5, 11, w, ol); rr(g, 17, 5, 19, 11, w, ol)  # floppy ears
    odisc(g, 11, 8, 6, w, ol)                   # head
    for ex in (9, 13):                          # small close-set dot eyes
        if blink:
            rect(g, ex - 1, 7, ex + 1, 7, bk)
        else:
            rect(g, ex - 1, 6, ex, 7, bk); px(g, ex - 1, 6, HI)
    px(g, 11, 10, bk)                           # tiny nose
    for x, y in ((9, 12), (10, 13), (11, 12), (12, 13), (13, 12)):  # wavy worried mouth
        px(g, x, y, bk)
    rect(g, 5, 9, 6, 10, "#ffd0d8"); rect(g, 16, 9, 17, 10, "#ffd0d8")


def _goldie(g, blink, foot, outfit):
    fur, ol, ear = "#ecd3a6", "#c9a874", "#dcbd8a"
    if outfit == "red":
        cloth, dark, logo = "#d6403a", "#b12f2a", "#ffffff"
    else:
        cloth, dark, logo = "#8a5a33", "#6f4526", "#caa877"
    feet(g, 8, 14, 21, fur, ol, foot)
    # outfit body
    rect(g, 6, 16, 16, 22, cloth)
    rect(g, 6, 16, 16, 16, dark)
    if outfit == "red":
        px(g, 9, 19, logo); px(g, 11, 19, logo); px(g, 13, 19, logo)   # tiny "AW"
        px(g, 9, 20, logo); px(g, 13, 20, logo)
    else:                                       # overall straps + pocket
        rect(g, 8, 14, 8, 16, dark); rect(g, 14, 14, 14, 16, dark)
        rect(g, 10, 18, 12, 20, logo)
    odisc(g, 5, 15, 2, fur, ol); odisc(g, 17, 15, 2, fur, ol)          # paws
    # long floppy ears
    rr(g, 1, 6, 5, 16, ear, ol)
    rr(g, 17, 6, 21, 16, ear, ol)
    odisc(g, 11, 9, 7, fur, ol)                 # head
    for fx in (7, 11, 15):                       # fluffy tuft
        px(g, fx, 2, fur); px(g, fx, 1, ear)
    eyes(g, 7, 15, 9, blink)
    odisc(g, 11, 12, 1, "#5b4a3a", "#5b4a3a")   # nose
    px(g, 11, 13, "#5b4a3a")
    rect(g, 9, 13, 10, 13, "#e79a6a"); rect(g, 12, 13, 13, 13, "#e79a6a")  # cheeks


def rr(g, x0, y0, x1, y1, fill, outline):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            corner = (x in (x0, x1)) and (y in (y0, y1))
            if corner:
                continue
            edge = x in (x0, x1) or y in (y0, y1)
            px(g, x, y, outline if edge else fill)


def _lolo(g, blink, foot):        # strawberry kitten (Lingorm)
    b, ol, cr, pk = "#efb173", "#c9822f", "#fff3e6", "#ff8fb0"
    strwb, sdark, leaf, seed = "#e23b3b", "#b52c2c", "#4bbf5a", "#ffe08a"
    feet(g, 8, 14, 20, cr, ol, foot)
    odisc(g, 11, 15, 6, b, ol)                 # body
    disc(g, 11, 17, 3, cr)                     # white belly
    for ex in (7, 15):                          # ears
        tri_up(g, ex, 5, 5, 6, ol)
        tri_up(g, ex, 4, 4, 4, b)
        tri_up(g, ex, 3, 2, 2, pk)
    odisc(g, 11, 9, 7, b, ol)                   # head
    disc(g, 11, 11, 4, cr)                      # cream muzzle
    # strawberry perched on top of the head
    disc(g, 11, 3, 2, strwb)
    px(g, 11, 1, strwb); px(g, 10, 5, sdark); px(g, 12, 5, sdark)
    px(g, 9, 3, seed); px(g, 13, 3, seed); px(g, 11, 4, seed)
    px(g, 9, 0, leaf); px(g, 11, 0, leaf); px(g, 13, 0, leaf); px(g, 11, 1, leaf)
    # big sparkly eyes
    eyes(g, 7, 15, 9, blink)
    if not blink:
        px(g, 6, 8, HI); px(g, 14, 8, HI)       # extra star glint
    rect(g, 10, 11, 12, 11, pk); px(g, 11, 12, "#a85a3a")   # nose + mouth
    for sx, sy in ((3, 9), (4, 9), (18, 9), (19, 9)):        # tiger cheek stripes
        px(g, sx, sy, ol)
    rect(g, 5, 12, 6, 13, pk); rect(g, 16, 12, 17, 13, pk)  # blush


def _butterbear(g, blink, foot):  # round cream café bear
    cr, ol, mz = "#f0cf9c", "#cba465", "#fbe8c6"
    nose, ndark = "#e23b3b", "#b12f2a"
    feet(g, 8, 14, 21, cr, ol, foot)
    odisc(g, 11, 16, 6, cr, ol)                 # body
    disc(g, 11, 17, 3, mz)                      # lighter tummy
    odisc(g, 4, 16, 2, cr, ol); odisc(g, 18, 16, 2, cr, ol)   # arms
    odisc(g, 5, 4, 3, cr, ol); odisc(g, 17, 4, 3, cr, ol)     # round ears
    disc(g, 5, 4, 1, mz); disc(g, 17, 4, 1, mz)
    odisc(g, 11, 9, 7, cr, ol)                  # big round head
    for ex in (8, 14):                          # big round eyes
        if blink:
            rect(g, ex - 2, 9, ex + 1, 9, EYE)
        else:
            disc(g, ex, 9, 2, EYE)
            px(g, ex - 1, 8, HI)
    odisc(g, 11, 11, 1, nose, ndark)            # red nose
    for x, y in ((9, 13), (10, 14), (11, 14), (12, 14), (13, 13)):   # smile
        px(g, x, y, "#7a5a30")
    rect(g, 5, 11, 6, 12, "#ffc0a0"); rect(g, 16, 11, 17, 12, "#ffc0a0")  # cheeks


# ----------------------------------------------------------- action scenes
# The desktop buddy renders a wider "scene" grid: the mascot plus an 8-bit
# prop for whatever it's currently doing. Actions are shuffled at random.
SCENE_W, SCENE_H = 40, 28
_MASCOT_OX, _MASCOT_OY = 4, 3          # where the 22x24 mascot sits in the scene

ACTIONS = ["chicken", "music", "sleep", "read", "work", "tv", "bubbletea", "coffee"]
ACTION_LABELS = {
    "chicken": "eating fried chicken",
    "music": "listening to music",
    "sleep": "having a nap",
    "read": "reading a book",
    "work": "working hard",
    "tv": "watching TV",
    "bubbletea": "bubble tea break",
    "coffee": "coffee time",
}


def _blit(dst, src, ox, oy):
    for y, row in enumerate(src):
        for x, c in enumerate(row):
            if c:
                yy, xx = y + oy, x + ox
                if 0 <= yy < len(dst) and 0 <= xx < len(dst[0]):
                    dst[yy][xx] = c


def _draw_z(g, x, y, col):
    rect(g, x, y, x + 3, y, col)                # top bar
    px(g, x + 2, y + 1, col); px(g, x + 1, y + 2, col)   # diagonal
    rect(g, x, y + 3, x + 3, y + 3, col)        # bottom bar


def _prop(g, action):
    if action == "chicken":
        meat, bone = "#c8763a", "#f2e4c2"
        disc(g, 25, 15, 2, meat)                # near the muzzle
        rect(g, 26, 15, 30, 16, bone)
        disc(g, 31, 15, 1, bone)
    elif action == "music":
        hp, note = "#3a3550", "#5b8def"
        rect(g, 9, 5, 21, 5, hp)                # headband over head
        rect(g, 8, 6, 9, 10, hp); rect(g, 21, 6, 22, 10, hp)   # earcups
        for nx, ny in ((32, 9), (37, 6)):       # floating notes
            rect(g, nx, ny, nx, ny + 4, note)
            rect(g, nx, ny, nx + 2, ny, note)
            disc(g, nx - 1, ny + 5, 1, note)
    elif action == "sleep":
        z = "#8a86a8"
        _draw_z(g, 26, 14, z); _draw_z(g, 30, 9, z); _draw_z(g, 35, 4, z)
    elif action == "read":
        cover, page = "#c96f6f", "#fff6ea"
        rect(g, 9, 20, 21, 25, cover)
        rect(g, 10, 21, 20, 24, page)
        rect(g, 15, 21, 15, 24, cover)          # spine
    elif action == "work":
        lap, scr = "#4a4f5a", "#8fd0e0"
        rect(g, 9, 22, 21, 25, lap)             # keyboard base
        rect(g, 10, 17, 20, 22, lap)            # lid
        rect(g, 11, 18, 19, 21, scr)            # screen
        px(g, 13, 19, HI)
    elif action == "tv":
        tv, scr = "#4a4f5a", "#8fd0e0"
        rect(g, 28, 11, 38, 20, tv)
        rect(g, 29, 12, 37, 19, scr)
        px(g, 30, 21, tv); px(g, 36, 21, tv)    # legs
        px(g, 31, 14, HI); px(g, 32, 15, HI)
    elif action == "bubbletea":
        cup, tea, pearl, straw = "#f3e3c9", "#caa06a", "#3a2a20", "#ff6f91"
        rect(g, 30, 16, 35, 25, cup)
        rect(g, 30, 16, 35, 17, tea)
        px(g, 31, 23, pearl); px(g, 33, 24, pearl)
        px(g, 32, 22, pearl); px(g, 34, 23, pearl)
        rect(g, 33, 12, 34, 17, straw)
    elif action == "coffee":
        mug, cof, steam = "#e8e2d6", "#5b3a24", "#c9c4dd"
        rect(g, 30, 18, 36, 24, mug)
        rect(g, 31, 18, 35, 19, cof)
        px(g, 37, 20, mug); px(g, 37, 21, mug); px(g, 38, 20, mug)   # handle
        px(g, 32, 14, steam); px(g, 33, 13, steam); px(g, 34, 14, steam)


def build_scene(mascot, action, blink=False, foot=0, bob=0):
    """Wide grid: the mascot (2x-rendered by the caller) plus an action prop."""
    scene = [[None] * SCENE_W for _ in range(SCENE_H)]
    m = build(mascot, blink=blink or action == "sleep", foot=foot)
    _blit(scene, m, _MASCOT_OX, _MASCOT_OY - bob)
    _prop(scene, action)
    return scene


# ----------------------------------------------------------- image
def make_photo(grid, num, den=1, bg=TRANSPARENT):
    h = len(grid)
    w = len(grid[0])
    data = " ".join(
        "{" + " ".join((c if c else bg) for c in row) + "}" for row in grid
    )
    img = tk.PhotoImage(width=w, height=h)
    img.put(data)
    img = img.zoom(num)
    if den > 1:
        img = img.subsample(den)      # num/den lets us do fractional scale
    return img
