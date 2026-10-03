"""Pixel-art sprite builder for the Kiro pets.

Mascots are authored on a chunky low-res grid (easy to draw), then run
through hd(): a Scale2x upscale plus an auto light/shade pass that turns
the 8-bit art into a smoother 16/32-bit look."""

import tkinter as tk

W, H = 22, 24                     # sprite grid
TRANSPARENT = "#0b1e0c"           # -> transparent on the pet window

GMM = ["muvmuv", "lunar", "any", "jewel", "vimmy", "wesley"]
CLASSIC = ["goldie_red", "goldie_brown", "lolo"]
MASCOTS = GMM + CLASSIC
LABELS = {
    "muvmuv": "MuvMuv", "lunar": "Lunar", "any": "Any",
    "jewel": "Jewel", "vimmy": "Vimmy", "wesley": "Wesley",
    "goldie_red": "Goldie ❤", "goldie_brown": "Goldie \U0001f9e5",
    "lolo": "LOLO \U0001f353",
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
        "jewel": _jewel, "vimmy": _vimmy, "wesley": _wesley,
        "goldie_red": lambda g, b, f: _goldie(g, b, f, "red"),
        "goldie_brown": lambda g, b, f: _goldie(g, b, f, "brown"),
        "lolo": _lolo,
    }[mascot](g, blink, foot)
    if face < 0:
        g = [row[::-1] for row in g]
    for _ in range(rot % 4):
        g = rot_cw(g)
    return g


# --- GMMTV mascots, redrawn from "Design Reference GMM/". They share the
# official chibi pose: a big wide head, two front paws peeking out at the
# bottom and a little body underneath.
def oval(g, cx, cy, rx, ry, c):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.08:
                px(g, x, y, c)


def ooval(g, cx, cy, rx, ry, fill, outline):
    oval(g, cx, cy, rx, ry, outline)
    oval(g, cx, cy, rx - 1, ry - 1, fill)


def ear(g, tipx, tipy, h, w, c):
    """Triangle with its tip at (tipx, tipy), widening downward."""
    for i in range(h):
        half = int(round((w / 2) * i / max(1, h - 1)))
        rect(g, tipx - half, tipy + i, tipx + half, tipy + i, c)


def big_eye(g, ex, ey, blink, col=EYE, glint=HI):
    """Tall, round, shiny eye (3 wide x 4 tall) - the GMM look."""
    if blink:
        rect(g, ex - 1, ey + 1, ex + 1, ey + 1, col)
        px(g, ex - 2, ey, col); px(g, ex + 2, ey, col)
        return
    rect(g, ex - 1, ey - 1, ex + 1, ey + 2, col)
    px(g, ex, ey, glint)          # centred shine survives Scale2x cleanly


def heart(g, x, y, c):
    """3x3 heart with its top-left corner at (x, y)."""
    px(g, x, y, c); px(g, x + 2, y, c)
    rect(g, x, y + 1, x + 2, y + 1, c)
    px(g, x + 1, y + 2, c)


def blush(g, y, c, lx=5, rx=16):
    """The '||' blush marks every GMM mascot has under its eyes."""
    for x in (lx, rx):
        px(g, x, y, c); px(g, x + 1, y, c)


def _muvmuv(g, blink, foot):          # fluffy white pup in an orange cat hood
    hood, hol, stripe = "#f7b67e", "#d98c50", "#ee7046"
    w, wol = "#fffdf8", "#e4ddd3"
    nose, tong, red = "#7a4a3a", "#f2899a", "#e8545a"
    milk, milkd, mint = "#f7b9c8", "#d98aa2", "#9fd9c0"
    feet(g, 8, 14, 22, w, wol, foot)
    odisc(g, 11, 19, 4, w, wol)                 # fluffy white body
    for ex in (4, 18):                          # hood cat ears
        ear(g, ex, 1, 6, 6, hol)
        ear(g, ex, 2, 4, 3, hood)
    ooval(g, 11, 10, 10, 7, hood, hol)          # big orange hood
    oval(g, 11, 12, 6, 4.6, w)                  # white face opening
    for sy in (9, 11):                          # tabby stripes on both sides
        rect(g, 1, sy, 2, sy, stripe); rect(g, 19, sy, 20, sy, stripe)
    px(g, 8, 4, stripe); px(g, 8, 5, stripe)    # stripes under the carton
    # pink strawberry-milk carton balanced on the hood (signature prop)
    rect(g, 11, 0, 14, 4, milk)
    rect(g, 11, 0, 14, 0, mint)
    px(g, 12, 2, w); px(g, 13, 3, w); px(g, 12, 3, w)       # little heart
    px(g, 11, 4, milkd); px(g, 14, 4, milkd)
    big_eye(g, 8, 11, blink); big_eye(g, 14, 11, blink)
    px(g, 10, 14, nose); px(g, 12, 14, nose)    # heart nose…
    px(g, 11, 14, nose); px(g, 11, 15, nose)
    px(g, 10, 16, nose); px(g, 12, 16, nose)    # :3 mouth
    px(g, 11, 16, tong)                         # …tongue peeking
    blush(g, 14, red)
    rect(g, 8, 17, 14, 17, hood)                # orange neckerchief knot
    rect(g, 9, 18, 13, 18, hood); px(g, 11, 19, hol)
    odisc(g, 5, 18, 2, w, wol); odisc(g, 17, 18, 2, w, wol)   # front paws


def _lunar(g, blink, foot):           # panda-duck with heart eyes
    w, ol, bk = "#ffffff", "#cdd3da", "#26292f"
    ylo, yld = "#f6d55c", "#dcb23a"
    blue, yel, red = "#6cc3d8", "#f3e36a", "#e05050"
    off = 1 if foot else 0
    odisc(g, 8, 22 - off, 2, ylo, yld)          # yellow duck feet
    odisc(g, 14, 22 + off, 2, ylo, yld)
    odisc(g, 11, 19, 4, w, ol)                  # round white body
    disc(g, 4, 4, 3, bk); disc(g, 18, 4, 3, bk) # panda ears
    ooval(g, 11, 10, 10, 7, w, ol)              # big white head
    for dx, dy in ((0, -2), (-2, 0), (2, 0), (0, 2),        # blue flower
                   (-1, -1), (1, 1), (1, -1), (-1, 1)):
        px(g, 17 + dx, 4 + dy, blue)
    px(g, 17, 4, yel)
    heart(g, 8, 1, blue); heart(g, 10, 0, yel)  # two hearts on top
    px(g, 4, 3, red)                            # red heart on the left ear
    for ex, iris in ((7, blue), (15, yel)):     # black patches, heart eyes
        oval(g, ex, 11, 3.2, 2.6, bk)
        if blink:
            rect(g, ex - 1, 11, ex + 1, 11, w)
        else:
            disc(g, ex, 11, 1, w)
            px(g, ex, 11, iris); px(g, ex - 1, 11, iris)
            px(g, ex + 1, 10, HI)
    oval(g, 11, 14, 3, 1.5, ylo)                # yellow duck beak
    rect(g, 9, 15, 13, 15, yld)
    blush(g, 15, red, 4, 17)
    disc(g, 5, 18, 2, bk); disc(g, 17, 18, 2, bk)            # black paws


def _any(g, blink, foot):             # girl in a bunny hood with fairy wings
    hood, ol = "#fffbe2", "#e4dcb8"
    tip, hair, skin = "#f4c6d8", "#1f1a22", "#fbeee6"
    wing_b, wing_p = "#a8e0ea", "#f6c4d4"
    clip_o, clip_p, red = "#f08a5d", "#e86aa0", "#e8545a"
    oval(g, 2, 12, 2.5, 4, wing_b); oval(g, 20, 12, 2.5, 4, wing_b)   # wings
    oval(g, 2, 13, 1.5, 2, wing_p); oval(g, 20, 13, 1.5, 2, wing_p)
    off = 1 if foot else 0
    odisc(g, 8, 22 - off, 2, "#f2a8bc", "#d87f98")           # pink boot
    odisc(g, 14, 22 + off, 2, "#f6a36a", "#d97f45")          # orange boot
    odisc(g, 11, 19, 4, hood, ol)               # poncho body
    for x0 in (4, 14):                          # long bunny ears, pink tips
        rr(g, x0, 0, x0 + 4, 7, hood, ol)
        rect(g, x0 + 1, 1, x0 + 3, 2, tip)
    ooval(g, 11, 11, 9, 7, hood, ol)            # hood
    oval(g, 11, 11, 7, 5.6, hair)               # black bob
    oval(g, 11, 14, 5.5, 3, skin)               # face peeking under bangs
    px(g, 10, 11, hair); px(g, 13, 11, hair)    # spiky fringe
    rect(g, 13, 7, 14, 7, clip_o)               # two hair clips
    rect(g, 15, 8, 16, 8, clip_p)
    px(g, 10, 2, clip_p); px(g, 12, 2, clip_p)  # butterfly between the ears
    px(g, 11, 3, "#b0507a")
    px(g, 10, 4, wing_p); px(g, 12, 4, wing_p)
    big_eye(g, 8, 13, blink, hair); big_eye(g, 14, 13, blink, hair)
    px(g, 11, 15, "#f2a0b0")                    # tiny pink nose
    blush(g, 15, red, 6, 15)
    odisc(g, 5, 18, 2, hood, ol); odisc(g, 17, 18, 2, hood, ol)   # paws


def _jewel(g, blink, foot):           # cream fox-cat with a red bow
    cr, col = "#fff6ea", "#e6d4bf"
    red_ear, earin = "#97282c", "#f2b2ae"
    brown, lash, pink = "#6b3420", "#3e2216", "#f4a4a8"
    red, redd = "#d4212a", "#a8141c"
    feet(g, 8, 14, 22, cr, col, foot)
    odisc(g, 11, 19, 4, cr, col)                # body
    for ex in (4, 18):                          # tall dark-red ears
        ear(g, ex, 0, 8, 6, red_ear)
        ear(g, ex, 3, 5, 3, earin)
    ooval(g, 11, 11, 10, 7, cr, col)            # fluffy head
    for x, y in ((8, 4), (9, 3), (10, 4), (9, 5)):           # infinity curl
        px(g, x, y, red_ear)
    for x, y in ((12, 4), (13, 3), (14, 4), (13, 5)):
        px(g, x, y, pink)
    px(g, 11, 4, red_ear)
    px(g, 13, 7, pink); px(g, 14, 7, pink)      # pink pom-pom fringe
    for ex, out in ((7, -1), (15, 1)):          # big brown eyes, pink shadow
        if not blink:
            rect(g, ex - 1, 9, ex + 1, 9, "#f7c6c6")
            px(g, ex + 2 * out, 9, lash)        # winged outer lash
        big_eye(g, ex, 11, blink, brown)
    px(g, 11, 13, red)                          # tiny nose
    px(g, 10, 14, brown); px(g, 12, 14, brown)  # cat mouth
    blush(g, 14, red, 4, 17)
    rect(g, 6, 17, 16, 17, red)                 # red collar…
    rect(g, 9, 18, 13, 18, red)                 # …and bow
    px(g, 11, 18, redd); px(g, 9, 19, red); px(g, 13, 19, red)
    odisc(g, 5, 18, 2, cr, col); odisc(g, 17, 18, 2, cr, col)    # paws


def _vimmy(g, blink, foot):           # cavalier spaniel with a bee on her head
    cr, col = "#fbe9d0", "#e0c39c"
    brown, brownd = "#a86b3d", "#7e4c26"
    bee, beek, wing = "#f6d33c", "#2a2420", "#d8f0ff"
    nose, red = "#4a2a1a", "#e8545a"
    feet(g, 8, 14, 22, "#eef0f6", "#c8ccd8", foot)            # white boots
    odisc(g, 11, 19, 4, bee, "#d8b42a")         # bumblebee outfit
    rect(g, 8, 19, 14, 19, beek)
    ooval(g, 2, 13, 2.6, 6, brown, brownd)      # long curly ears
    ooval(g, 20, 13, 2.6, 6, brown, brownd)
    for ey in (10, 13, 16):                     # curls
        px(g, 2, ey, cr); px(g, 20, ey + 1, cr)
    ooval(g, 11, 10, 8.5, 7, cr, col)           # head
    oval(g, 7, 10, 3, 3.6, brown)               # brown patches round the eyes
    oval(g, 15, 10, 3, 3.6, brown)
    px(g, 10, 6, col); px(g, 11, 7, col); px(g, 12, 6, col)  # forehead curl
    px(g, 7, 2, beek); px(g, 6, 1, beek)        # antenna headband
    px(g, 15, 2, beek); px(g, 16, 1, beek)
    oval(g, 11, 3, 2.4, 1.6, bee)               # the bee
    px(g, 11, 3, beek); px(g, 12, 3, beek)
    px(g, 10, 1, wing); px(g, 11, 1, wing)
    for ex in (7, 15):                          # black eyes with flower glint
        if blink:
            rect(g, ex - 1, 11, ex + 1, 11, beek)
            continue
        big_eye(g, ex, 10, False, beek)
    px(g, 10, 13, nose); px(g, 11, 13, nose); px(g, 12, 13, nose)
    px(g, 11, 14, nose)
    px(g, 10, 15, nose); px(g, 12, 15, nose)    # smile
    blush(g, 14, red, 6, 15)
    odisc(g, 6, 18, 2, cr, col); odisc(g, 16, 18, 2, cr, col)    # paws


def _wesley(g, blink, foot):          # puppy in a blue shark hood
    blue, blued, white = "#4f86d8", "#2c5aa8", "#ffffff"
    tan, tand, face = "#e2bd93", "#c39466", "#fbead6"
    brown, red, tong = "#6b3f2a", "#d93a3a", "#f08aa0"
    off = 1 if foot else 0
    odisc(g, 8, 22 - off, 2, red, "#a82828")    # red shoes
    odisc(g, 14, 22 + off, 2, red, "#a82828")
    ooval(g, 11, 11, 10, 10, blue, blued)       # round shark-hood body
    oval(g, 11, 16, 6, 4, white)                # white shark belly
    rect(g, 9, 2, 13, 2, red)                   # shark teeth crown
    px(g, 9, 1, red); px(g, 11, 1, red); px(g, 13, 1, red)
    for sx in (5, 7, 15, 17):                   # stitch marks on the hood
        px(g, sx, 3 if sx in (7, 15) else 4, blued)
    oval(g, 11, 10, 6, 5, face)                 # face
    oval(g, 7, 9, 2.6, 2.2, tan)                # tan patches
    oval(g, 15, 9, 2.6, 2.2, tan)
    ooval(g, 3, 11, 2.2, 4, tan, tand)          # floppy ears held up
    ooval(g, 19, 11, 2.2, 4, tan, tand)
    for ex in (7, 15):
        if blink:
            rect(g, ex - 1, 10, ex + 1, 10, brown)
        else:
            big_eye(g, ex, 9, False, brown)
    px(g, 10, 12, brown); px(g, 11, 12, brown); px(g, 12, 12, brown)
    px(g, 10, 13, brown); px(g, 12, 13, brown)  # :3 mouth
    px(g, 11, 14, tong)                         # happy tongue
    blush(g, 13, red, 6, 15)
    odisc(g, 4, 17, 2, blue, blued); odisc(g, 18, 17, 2, blue, blued)  # fins


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
    "alarm": "time's up!",          # timer prop only, never picked at random
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
    if action == "chicken":                     # drumstick in the right paw, to the mouth
        meat, bone = "#c8763a", "#f2e4c2"
        px(g, 20, 19, bone); px(g, 21, 20, bone); px(g, 22, 21, bone)
        disc(g, 23, 22, 1, bone)
        disc(g, 19, 17, 2, meat)
    elif action == "music":                     # headphones hugging the head
        hp, cup, note = "#3a3550", "#ff8fb0", "#5b8def"
        rect(g, 7, 5, 23, 5, hp); px(g, 6, 6, hp); px(g, 24, 6, hp)
        rect(g, 5, 7, 5, 9, hp); rect(g, 25, 7, 25, 9, hp)
        rect(g, 4, 10, 6, 15, cup); rect(g, 24, 10, 26, 15, cup)
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
    elif action == "bubbletea":                 # cup in the right paw, straw to the mouth
        cup, tea, pearl, straw = "#f3e3c9", "#caa06a", "#3a2a20", "#ff6f91"
        rect(g, 19, 14, 23, 21, cup)
        rect(g, 19, 17, 23, 21, tea)
        px(g, 20, 20, pearl); px(g, 22, 20, pearl); px(g, 21, 19, pearl)
        px(g, 19, 15, straw); px(g, 18, 16, straw); px(g, 17, 17, straw)
    elif action == "coffee":                    # mug raised in the right paw
        mug, cof, steam = "#e8e2d6", "#5b3a24", "#c9c4dd"
        rect(g, 18, 15, 23, 20, mug)
        rect(g, 19, 15, 22, 15, cof)
        px(g, 24, 17, mug); px(g, 24, 18, mug)  # handle
        px(g, 20, 18, "#ff9ec4")
        px(g, 19, 12, steam); px(g, 20, 11, steam); px(g, 21, 12, steam)
    elif action == "game":
        pad, dp = "#5a5f6e", "#33303f"
        rect(g, 9, 21, 21, 25, pad)             # gamepad held in front
        px(g, 8, 22, pad); px(g, 22, 22, pad)   # grips
        rect(g, 11, 22, 13, 22, dp); rect(g, 12, 21, 12, 23, dp)     # d-pad
        px(g, 18, 21, "#e05a4e"); px(g, 19, 23, "#4bbf5a")           # buttons
        px(g, 17, 23, "#ffd23f"); px(g, 20, 21, "#5b8def")
        for sx, sy in ((30, 8), (34, 5), (37, 10)):                  # sparks
            px(g, sx, sy, "#ffd23f")
    elif action == "noodles":                   # bowl in both paws, chopsticks to the mouth
        bowl, rim, ndl, stick = "#e05a4e", "#b8443a", "#ffe08a", "#8a5a33"
        rect(g, 8, 20, 22, 23, bowl)
        rect(g, 8, 20, 22, 20, rim)
        for nx in (9, 12, 15, 18):              # noodles over the rim
            px(g, nx, 19, ndl)
        for k in range(4):                      # chopsticks from the right paw
            px(g, 21 - k, 19 - k, stick)
        px(g, 17, 17, ndl); px(g, 17, 18, ndl)
        px(g, 11, 16, "#c9c4dd"); px(g, 13, 15, "#c9c4dd")       # steam
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
    elif action == "alarm":
        red, redd, bell = "#e05050", "#b83b3b", "#f2c94c"
        disc(g, 30, 13, 2, bell); disc(g, 37, 13, 2, bell)        # bells
        odisc(g, 33, 18, 5, red, redd)          # clock body
        disc(g, 33, 18, 3, "#ffffff")           # face
        rect(g, 33, 16, 33, 18, EYE); rect(g, 33, 18, 35, 18, EYE)   # hands
        px(g, 30, 23, redd); px(g, 36, 23, redd)                  # legs
        for rx_, ry_ in ((26, 15), (25, 18), (40, 15), (41, 18)): # ringing
            px(g, rx_, ry_, bell)


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
