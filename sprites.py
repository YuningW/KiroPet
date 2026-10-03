"""Pixel-art sprite builder for the Kiro pets.

Mascots are authored on a chunky low-res grid (easy to draw), then run
through hd(): a Scale2x upscale plus an auto light/shade pass that turns
the 8-bit art into a smoother 16/32-bit look."""

import tkinter as tk

W, H = 22, 24                     # sprite grid
TRANSPARENT = "#0b1e0c"           # -> transparent on the pet window

MASCOTS = ["muvmuv", "lunar", "any", "whitedog", "goldie_red", "goldie_brown",
           "lolo", "butterbear", "buriburi"]
LABELS = {
    "muvmuv": "MuvMuv", "lunar": "Lunar", "any": "Any",
    "whitedog": "Shiro", "goldie_red": "Goldie ❤", "goldie_brown": "Goldie \U0001f9e5",
    "lolo": "LOLO \U0001f353", "butterbear": "Butter bear",
    "buriburi": "Buriburizaemon \U0001f437",
}

EYE = "#39304a"
HI = "#ffffff"


# ----------------------------------------------------------- grid helpers
def new_grid():
    return [[None] * W for _ in range(H)]


def px(g, x, y, c):
    if c and 0 <= y < len(g) and 0 <= x < len(g[0]):
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
        "lolo": _lolo, "butterbear": _butterbear, "buriburi": _buriburi,
    }[mascot](g, blink, foot)
    if face < 0:
        g = [row[::-1] for row in g]
    for _ in range(rot % 4):
        g = rot_cw(g)
    return g


def _muvmuv(g, blink, foot):          # white pup in an orange tabby-cat hood
    hood, ol, red = "#f5a04a", "#c9772a", "#d6403a"
    w, wol = "#fffdf8", "#e3ddd2"
    nose, tong, bl = "#6b4636", "#f08a9a", "#f8c0cc"
    feet(g, 8, 14, 21, w, wol, foot)
    odisc(g, 11, 16, 6, w, wol)                 # fluffy white body
    for ex in (7, 15):                          # hood cat ears
        tri_up(g, ex, 5, 5, 6, ol)
        tri_up(g, ex, 4, 4, 4, hood)
        px(g, ex, 2, red)                       # red ear stripe
    odisc(g, 11, 9, 7, hood, ol)                # orange hood
    disc(g, 11, 11, 5, w)                       # white face opening
    rect(g, 9, 3, 9, 4, red)                    # tabby stripes on top
    rect(g, 11, 2, 11, 3, red)
    rect(g, 13, 3, 13, 4, red)
    px(g, 5, 8, red); px(g, 5, 9, red)          # cheek stripes on the hood
    px(g, 17, 8, red); px(g, 17, 9, red)
    eyes(g, 8, 14, 9, blink)
    px(g, 10, 12, nose); px(g, 12, 12, nose)    # heart nose…
    px(g, 11, 13, nose)
    px(g, 11, 14, tong)                         # …tongue peeking
    rect(g, 6, 13, 7, 13, bl); rect(g, 15, 13, 16, 13, bl)   # blush
    rect(g, 7, 15, 15, 16, hood)                # orange neckerchief
    px(g, 6, 15, hood); px(g, 16, 15, hood)
    px(g, 10, 17, hood); px(g, 12, 17, hood); px(g, 11, 18, hood)   # knot tails


def _lunar(g, blink, foot):
    w, ol, bk = "#ffffff", "#c9d0d8", "#26292f"
    ylo, yld, teal = "#ffcf3f", "#e6a81e", "#27bcd0"
    shell, shol = "#f0ddaa", "#c9ab6a"
    # egg / penguin body
    odisc(g, 11, 16, 6, w, ol)
    # hatched eggshell it sits in (zigzag cracked rim)
    rect(g, 6, 19, 16, 21, shell)
    rect(g, 6, 19, 6, 21, shol); rect(g, 16, 19, 16, 21, shol)
    rect(g, 7, 22, 15, 22, shol)
    for zx in (6, 8, 10, 12, 14, 16):           # crack teeth
        px(g, zx, 18, shell)
    px(g, 11, 20, shol); px(g, 12, 21, shol)    # hairline crack
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
    # tiny heart floating over the head
    px(g, 10, 0, "#ffd7e6"); px(g, 12, 0, "#ffd7e6"); px(g, 11, 1, "#ffd7e6")
    # head
    odisc(g, 11, 9, 7, w, ol)
    disc(g, 7, 8, 3, bk); disc(g, 15, 8, 3, bk)             # eye patches
    for ex, glint in ((7, "#ffd23f"), (15, "#3fd6e6")):      # heart-sparkle eyes
        disc(g, ex, 8, 2, w)
        if blink:
            rect(g, ex - 1, 8, ex + 1, 8, bk)
        else:
            disc(g, ex, 8, 1, bk)
            px(g, ex, 7, glint); px(g, ex - 1, 7, HI)
    # yellow duck beak
    rect(g, 9, 11, 13, 12, ylo); px(g, 8, 11, ylo); px(g, 14, 11, ylo)
    rect(g, 9, 13, 13, 13, yld)
    rect(g, 4, 11, 5, 12, "#ffb3c8"); rect(g, 17, 11, 18, 12, "#ffb3c8")


def _any(g, blink, foot):             # bunny-poncho girl (butterfly mark)
    w, ol, hair, skin = "#fffdf8", "#e3e0e8", "#2b2530", "#fdeee4"
    org, mag = "#f28c28", "#e0397e"
    feet(g, 8, 14, 21, "#f2a8bc", "#d87f98", foot)          # pink socks
    odisc(g, 11, 16, 6, w, ol)                  # poncho body
    px(g, 12, 19, org); px(g, 14, 19, mag)      # butterfly wings…
    px(g, 13, 20, mag)                          # …and body
    for ex in (8, 14):                          # bunny ears, pink tips
        rect(g, ex - 1, 0, ex + 1, 6, w); px(g, ex - 2, 4, w); px(g, ex + 2, 4, w)
        rect(g, ex - 1, 0, ex + 1, 1, "#f7b8cc")
        rect(g, ex, 2, ex, 4, "#ffd0e0")
    odisc(g, 11, 9, 7, w, ol)                   # hood
    disc(g, 11, 9, 6, hair)                     # bob hair
    disc(g, 11, 11, 4, skin)                    # pale face
    rect(g, 7, 6, 15, 8, hair)                  # bangs
    px(g, 8, 9, hair); px(g, 8, 10, hair)       # side-swept lock
    rect(g, 13, 5, 13, 6, org)                  # two little clips
    rect(g, 15, 5, 15, 6, mag)
    for ex in (9, 13):                          # small simple dot eyes
        if blink:
            rect(g, ex - 1, 11, ex, 11, hair)
        else:
            rect(g, ex - 1, 10, ex, 11, hair)
            px(g, ex - 1, 10, HI)
    px(g, 11, 13, "#e08898")                    # tiny nose-mouth
    rect(g, 7, 12, 8, 12, "#ffb3c8"); rect(g, 14, 12, 15, 12, "#ffb3c8")


def _whitedog(g, blink, foot):        # Shiro (Shin-chan's cloud-fluff dog)
    w, ol, bk, blu = "#ffffff", "#cfd4da", "#3a3540", "#4aa8e0"
    # small body under a big round head
    odisc(g, 11, 19, 4, w, ol)
    feet(g, 9, 13, 22, w, ol, foot)
    odisc(g, 6, 19, 2, w, ol); odisc(g, 16, 19, 2, w, ol)  # front paws
    odisc(g, 3, 21, 2, w, ol); px(g, 3, 21, ol)            # curly tail
    rect(g, 8, 16, 14, 17, blu)                 # blue collar
    # floppy left ear / perked right ear, both anchored to the skull
    rr(g, 2, 6, 5, 12, w, ol)
    rr(g, 17, 0, 20, 7, w, ol)
    odisc(g, 11, 8, 7, w, ol)                   # big head
    px(g, 8, 5, bk); px(g, 9, 4, bk)            # worried brow arcs
    px(g, 13, 4, bk); px(g, 14, 5, bk)
    for ex in (8, 14):                          # tiny wide-set dot eyes
        if blink:
            rect(g, ex - 1, 7, ex + 1, 7, bk)
        else:
            px(g, ex, 7, bk)
    for x, y in ((9, 10), (10, 11), (11, 10), (12, 11), (13, 10)):  # wavy mouth
        px(g, x, y, bk)


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


def _butterbear(g, blink, foot):  # butterbear.co café bear
    cr, ol, mz = "#ecc794", "#c99f63", "#f8ead0"
    grn, grnd = "#a8cdb4", "#7fae8d"
    apr = "#fdfbf2"
    brn = "#6b4432"
    feet(g, 8, 14, 21, cr, ol, foot)
    odisc(g, 11, 16, 6, cr, ol)                 # body
    odisc(g, 4, 16, 2, cr, ol); odisc(g, 18, 16, 2, cr, ol)   # arms
    rect(g, 8, 17, 14, 21, apr)                 # white café apron
    for sx in (8, 10, 12, 14):                  # green scallop trim
        px(g, sx, 22, grn)
    rect(g, 8, 21, 14, 21, grn)
    odisc(g, 5, 4, 3, cr, ol); odisc(g, 17, 4, 3, cr, ol)     # round ears
    disc(g, 5, 4, 1, mz); disc(g, 17, 4, 1, mz)
    odisc(g, 11, 9, 7, cr, ol)                  # big round head
    disc(g, 11, 12, 3, mz)                      # lighter muzzle
    for ex in (8, 14):                          # big white eyes, dark pupils
        if blink:
            rect(g, ex - 2, 9, ex + 1, 9, brn)
        else:
            disc(g, ex, 9, 2, HI)
            rect(g, ex - 1, 8, ex, 10, EYE)     # pupil
            px(g, ex, 8, HI)                    # glint
    px(g, 11, 11, brn)                          # little brown nose
    px(g, 10, 12, brn); px(g, 12, 12, brn)      # open smile…
    px(g, 11, 13, "#f2917e")                    # …with tongue
    rect(g, 5, 11, 6, 12, "#f5b3a0"); rect(g, 16, 11, 17, 12, "#f5b3a0")  # cheeks
    disc(g, 9, 15, 1, grn); disc(g, 13, 15, 1, grn)           # green neck bow
    px(g, 11, 15, grnd)


def _buriburi(g, blink, foot):    # Buriburizaemon, the "hero" pig
    pig, ol = "#f2a390", "#c97a66"
    sn, snol, nost = "#f7c3ad", "#d99680", "#8a5040"
    bk = "#26232b"
    pants, pol = "#8f7fc0", "#6f5fa0"
    red, gold, blade = "#d6403a", "#f2c94c", "#f6e6df"
    # pointy pig ears
    tri_up(g, 5, 4, 4, 5, ol); tri_up(g, 5, 3, 3, 3, pig)
    tri_up(g, 17, 4, 4, 5, ol); tri_up(g, 17, 3, 3, 3, pig)
    # big head
    odisc(g, 11, 8, 7, pig, ol)
    # thick angled scowl eyebrows
    rect(g, 5, 4, 6, 4, bk); rect(g, 7, 3, 9, 3, bk)
    rect(g, 13, 3, 15, 3, bk); rect(g, 16, 4, 17, 4, bk)
    # tiny wide-set eyes under the brows
    if blink:
        rect(g, 6, 6, 8, 6, bk); rect(g, 14, 6, 16, 6, bk)
    else:
        px(g, 7, 6, bk); px(g, 15, 6, bk)
    # huge snout mask
    disc(g, 9, 10, 3, snol); disc(g, 13, 10, 3, snol)
    disc(g, 9, 10, 2, sn); disc(g, 13, 10, 2, sn)
    rect(g, 10, 8, 12, 12, sn)
    px(g, 9, 10, nost); px(g, 13, 10, nost)     # nostrils
    px(g, 11, 12, nost)                         # small mouth
    # bare chest, hands on hips
    rect(g, 7, 15, 15, 18, pig)
    px(g, 6, 16, pig); px(g, 16, 16, pig)
    odisc(g, 4, 16, 2, pig, ol); odisc(g, 18, 16, 2, pig, ol)
    px(g, 8, 17, ol); px(g, 14, 17, ol)         # chest dots
    # purple pants, heroic wide stance
    rect(g, 6, 19, 16, 20, pants)
    rect(g, 6, 19, 16, 19, pol)                 # waistband
    off = 1 if foot else 0
    rect(g, 6, 21, 9, 23 - off, pants)          # left leg
    rect(g, 13, 21, 16, 22 + off, pants)        # right leg
    # toy sword at his side (drawn over the arm)
    rect(g, 19, 11, 19, 13, red)                # handle
    rect(g, 18, 14, 20, 14, gold)               # guard
    rect(g, 19, 15, 19, 20, blade)              # blade
    px(g, 20, 16, blade)


# ----------------------------------------------------------- action scenes
# The desktop buddy renders a wider "scene" grid: the mascot plus an 8-bit
# prop for whatever it's currently doing. Actions are shuffled at random.
SCENE_W, SCENE_H = 40, 28
_MASCOT_OX, _MASCOT_OY = 4, 3          # where the 22x24 mascot sits in the scene

ACTIONS = ["chicken", "music", "sleep", "read", "work", "tv", "bubbletea",
           "coffee", "game", "noodles", "phone", "plant"]
ACTION_LABELS = {
    "chicken": "eating fried chicken",
    "music": "listening to music",
    "sleep": "having a nap",
    "read": "reading a book",
    "work": "working hard",
    "tv": "watching TV",
    "bubbletea": "bubble tea break",
    "coffee": "coffee time",
    "game": "playing games",
    "noodles": "slurping noodles",
    "phone": "scrolling the phone",
    "plant": "watering the plant",
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
    elif action == "game":
        pad, dp = "#5a5f6e", "#33303f"
        rect(g, 9, 21, 21, 25, pad)             # gamepad held in front
        px(g, 8, 22, pad); px(g, 22, 22, pad)   # grips
        rect(g, 11, 22, 13, 22, dp); rect(g, 12, 21, 12, 23, dp)     # d-pad
        px(g, 18, 21, "#e05a4e"); px(g, 19, 23, "#4bbf5a")           # buttons
        px(g, 17, 23, "#ffd23f"); px(g, 20, 21, "#5b8def")
        for sx, sy in ((30, 8), (34, 5), (37, 10)):                  # sparks
            px(g, sx, sy, "#ffd23f")
    elif action == "noodles":
        bowl, rim, ndl, stick = "#e05a4e", "#b8443a", "#ffe08a", "#8a5a33"
        rect(g, 28, 20, 37, 25, bowl)
        rect(g, 28, 20, 37, 20, rim)
        for nx in (29, 31, 33, 35):             # noodles lifted over the rim
            px(g, nx, 19, ndl); px(g, nx + 1, 18, ndl)
        rect(g, 34, 12, 35, 18, stick)          # chopsticks
        px(g, 30, 15, "#c9c4dd"); px(g, 32, 13, "#c9c4dd")           # steam
    elif action == "phone":
        body, scr = "#2f3240", "#9fe0ff"
        rect(g, 12, 20, 18, 25, body)           # phone held in front
        rect(g, 13, 21, 17, 24, scr)
        px(g, 14, 22, HI)
        px(g, 25, 10, "#ff9ec4"); px(g, 27, 7, "#ff9ec4")            # floating likes
    elif action == "plant":
        pot, soil, leaf, leafd = "#c96f3a", "#6f4526", "#4bbf5a", "#2f8f3e"
        rect(g, 30, 21, 36, 25, pot)
        rect(g, 30, 21, 36, 21, soil)
        rect(g, 33, 16, 33, 20, leafd)          # stem
        disc(g, 31, 15, 2, leaf); disc(g, 35, 14, 2, leaf)
        disc(g, 33, 12, 2, leafd)
        px(g, 28, 16, "#7fd0ff"); px(g, 27, 18, "#7fd0ff")           # water drops


def build_scene(mascot, action, blink=False, foot=0, bob=0, face=1):
    """Wide grid: the mascot (2x-rendered by the caller) plus an action prop."""
    scene = [[None] * SCENE_W for _ in range(SCENE_H)]
    m = build(mascot, blink=blink or action == "sleep", foot=foot, face=face)
    _blit(scene, m, _MASCOT_OX, _MASCOT_OY - bob)
    _prop(scene, action)
    return scene


# ----------------------------------------------------------- 32-bit polish
_TINT_CACHE = {}


def _tint(c, f):
    """f > 0: mix toward white by f. f < 0: scale toward black by |f|."""
    key = (c, f)
    out = _TINT_CACHE.get(key)
    if out is None:
        r = int(c[1:3], 16); g = int(c[3:5], 16); b = int(c[5:7], 16)
        if f >= 0:
            r += (255 - r) * f; g += (255 - g) * f; b += (255 - b) * f
        else:
            r *= 1 + f; g *= 1 + f; b *= 1 + f
        out = f"#{int(r):02x}{int(g):02x}{int(b):02x}"
        _TINT_CACHE[key] = out
    return out


def scale2x(g):
    """EPX/Scale2x: double the grid, smoothing stair-step diagonals."""
    h, w = len(g), len(g[0])
    out = [[None] * (w * 2) for _ in range(h * 2)]
    for y in range(h):
        gy = g[y]
        up = g[y - 1] if y > 0 else None
        dn = g[y + 1] if y < h - 1 else None
        for x in range(w):
            p = gy[x]
            a = up[x] if up else None
            b = gy[x + 1] if x < w - 1 else None
            c = gy[x - 1] if x > 0 else None
            d = dn[x] if dn else None
            out[2 * y][2 * x] = a if (c == a and c != d and a != b) else p
            out[2 * y][2 * x + 1] = b if (a == b and a != c and b != d) else p
            out[2 * y + 1][2 * x] = c if (d == c and d != b and c != a) else p
            out[2 * y + 1][2 * x + 1] = d if (b == d and b != a and d != c) else p
    return out


def hd(g):
    """Scale2x + a light-from-above shading pass: top rim highlight, soft
    secondary highlight, bottom shadow. Turns the flat 8-bit fills into a
    rounded 16/32-bit look without redrawing any mascot."""
    g = scale2x(g)
    h, w = len(g), len(g[0])
    out = [row[:] for row in g]
    for y in range(h):
        for x in range(w):
            c = g[y][x]
            if not c:
                continue
            above = g[y - 1][x] if y > 0 else None
            below = g[y + 1][x] if y < h - 1 else None
            if above is None:
                out[y][x] = _tint(c, 0.30)
            elif below is None:
                out[y][x] = _tint(c, -0.22)
            elif y > 1 and g[y - 2][x] is None:
                out[y][x] = _tint(c, 0.12)
    return out


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
