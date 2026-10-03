"""Scene activities for the ThaiDevPet panel (cartoon SVG + pixel versions).

The original 12 activities (sprites.ACTIONS, drawn by sprites._prop and
cartoon.PROPS) can happen anywhere. The ones here belong to one scene each,
so an umbrella only comes out on a rainy day and a krathong only at
Loy Krathong. Every activity also carries the Thai word the word card shows
while it's happening.

Coordinates
  cartoon: the prop canvas of cartoon.PROP_VIEWBOX (-20 -14 200 136); the
           buddy fills 0..120 x 0..122 - head centre (60, 60), eyes y 65,
           mouth (60, 81), paws (31, 99) and (89, 99), feet y 114.
  pixel:   the 40x28 scene grid of sprites.build_scene - the buddy sits at
           (4, 3): head x 5-25 / y 6-20, eyes (12, 14) (18, 14), mouth
           (15, 18), paws (9, 21) and (21, 21), feet y 25.

kind:   "held" (in the paws / on the body, drawn 1:1), "side" (stands
        beside the buddy, drawn bigger), "head" (worn).
motion: None, "ride" (moves across the floor), "float" / "rise" (the prop
        drifts away), "hop", "sparkle", "confetti", "hearts", "wave".
"""

from cartoon import heart, note, sparkle, steam
from sprites import disc, odisc, px, rect

SPARKLE = "#ffd23f"


def _hands(cx=60, cy=90):
    """Paws pressed together (wai / making a wish)."""
    return (f'<path d="M{cx} {cy - 16}C{cx - 10} {cy - 10} {cx - 11} {cy + 4} {cx - 3} {cy + 10}'
            f'H{cx + 3}C{cx + 11} {cy + 4} {cx + 10} {cy - 10} {cx} {cy - 16}Z" '
            'fill="#fff6ea" stroke="#d8c7a0" stroke-width="1.8"/>'
            f'<path d="M{cx} {cy - 14}V{cy + 9}" stroke="#d8c7a0" stroke-width="1.4"/>')


def _px_hands(g):
    rect(g, 14, 17, 16, 21, "#fff6ea")
    px(g, 15, 16, "#fff6ea")
    rect(g, 15, 17, 15, 21, "#d8c7a0")


# id: (scene, label, emoji, kind, motion, closed_eyes, (thai, rom, eng), cartoon_svg, pixel_fn)
ACTIVITIES = {}


def activity(sid, scene, label, emoji, word, kind="held", motion=None, closed=False):
    def wrap(fn):
        ACTIVITIES[sid] = dict(scene=scene, label=label, emoji=emoji, kind=kind, motion=motion,
                               closed=closed, word=word, draw=fn)
        return fn
    return wrap


def _pixel(fn):
    """Attach a pixel drawing to the last registered activity."""
    last = list(ACTIVITIES)[-1]
    ACTIVITIES[last]["pixel"] = fn
    return fn


# ------------------------------------------------------------------ office
@activity("lunchbox", "office", "eating a lunch box", "🍱", ("กินข้าวกล่อง", 'gin khâao-glàwng', "Eating a lunch box"))
def _():
    return ('<rect x="32" y="86" width="56" height="24" rx="4" fill="#2b2b33" stroke="#c0392b" stroke-width="2.4"/>'
            '<rect x="36" y="90" width="22" height="16" rx="2" fill="#fffdf6"/>'
            '<rect x="61" y="90" width="23" height="7" rx="2" fill="#f6d55c"/>'
            '<rect x="61" y="99" width="11" height="7" rx="2" fill="#e8584a"/>'
            '<circle cx="78" cy="102.5" r="4" fill="#5fae5a"/><circle cx="47" cy="96" r="2" fill="#e8584a"/>'
            '<path d="M86 94L66 78M90 95L71 77" stroke="#c9a27a" stroke-width="2.6" stroke-linecap="round"/>')


@_pixel
def _(g):
    rect(g, 8, 19, 22, 23, "#2b2b33"); rect(g, 9, 20, 13, 22, "#fffdf6")
    rect(g, 15, 20, 21, 20, "#f6d55c"); rect(g, 15, 22, 17, 22, "#e8584a"); px(g, 20, 22, "#5fae5a")
    for k in range(4):
        px(g, 21 - k, 18 - k, "#c9a27a")


@activity("sticky", "office", "writing sticky notes", "✍️", ("เขียนโน้ต", 'khǐan nóot', "Writing a note"))
def _():
    return ('<rect x="40" y="84" width="34" height="30" rx="2" fill="#fff3a3" stroke="#e6cf5c" stroke-width="1.6" transform="rotate(-6 57 99)"/>'
            '<path d="M46 94h20M46 100h16M46 106h12" stroke="#c9b24a" stroke-width="1.6" stroke-linecap="round"/>'
            '<path d="M92 100L74 86" stroke="#f2a25c" stroke-width="5" stroke-linecap="round"/>'
            '<path d="M75 87L71 83" stroke="#3a3550" stroke-width="2.4" stroke-linecap="round"/>'
            '<rect x="128" y="60" width="16" height="16" fill="#ffc6dd" transform="rotate(8 136 68)"/>'
            '<rect x="146" y="74" width="16" height="16" fill="#c6f0d8" transform="rotate(-6 154 82)"/>')


@_pixel
def _(g):
    rect(g, 10, 19, 16, 23, "#fff3a3"); rect(g, 11, 20, 15, 20, "#c9b24a"); rect(g, 11, 22, 14, 22, "#c9b24a")
    px(g, 21, 21, "#f2a25c"); px(g, 20, 20, "#f2a25c"); px(g, 19, 19, "#3a3550")
    rect(g, 29, 12, 31, 14, "#ffc6dd"); rect(g, 32, 15, 34, 17, "#c6f0d8")


@activity("meeting", "office", "in an online meeting", "🎧", ("ประชุมออนไลน์", 'bprà-chum awn-lai', "Online meeting"), kind="head")
def _():
    return ('<path d="M9 62Q9 12 60 12Q111 12 111 62" fill="none" stroke="#3a3550" stroke-width="5" stroke-linecap="round"/>'
            '<rect x="1" y="52" width="15" height="24" rx="7" fill="#5b6478" stroke="#3a3550" stroke-width="2"/>'
            '<rect x="104" y="52" width="15" height="24" rx="7" fill="#5b6478" stroke="#3a3550" stroke-width="2"/>'
            '<path d="M108 74Q104 90 74 86" fill="none" stroke="#3a3550" stroke-width="2.6" stroke-linecap="round"/>'
            '<circle cx="72" cy="86" r="3.6" fill="#3a3550"/>'
            '<rect x="128" y="34" width="38" height="20" rx="9" fill="#fff" stroke="#c9d3e3" stroke-width="1.6"/>'
            '<circle cx="138" cy="44" r="2.4" fill="#8a96ab"/><circle cx="147" cy="44" r="2.4" fill="#8a96ab"/>'
            '<circle cx="156" cy="44" r="2.4" fill="#8a96ab"/>')


@_pixel
def _(g):
    rect(g, 7, 5, 23, 5, "#3a3550"); px(g, 6, 6, "#3a3550"); px(g, 24, 6, "#3a3550")
    rect(g, 4, 10, 6, 15, "#5b6478"); rect(g, 24, 10, 26, 15, "#5b6478")
    px(g, 23, 16, "#3a3550"); px(g, 22, 17, "#3a3550"); rect(g, 18, 18, 21, 18, "#3a3550")
    rect(g, 29, 8, 36, 11, "#ffffff"); px(g, 31, 9, "#8a96ab"); px(g, 33, 9, "#8a96ab"); px(g, 35, 9, "#8a96ab")


# ------------------------------------------------------------------ cafe
@activity("cake", "cafe", "eating cake", "🍰", ("กินเค้ก", 'gin khéek', "Eating cake"))
def _():
    return ('<ellipse cx="54" cy="104" rx="26" ry="6" fill="#fff" stroke="#e0d6ea" stroke-width="1.6"/>'
            '<path d="M36 102L72 102L72 86L36 94Z" fill="#fff6e6" stroke="#ead7b8" stroke-width="1.4"/>'
            '<path d="M36 94L72 86L72 92L36 99Z" fill="#ff9ec4"/>'
            '<path d="M36 94L72 86" stroke="#fffaf0" stroke-width="3" stroke-linecap="round"/>'
            '<circle cx="64" cy="82" r="5" fill="#e8343a"/><path d="M62 77l2 2 2-2" stroke="#5fae5a" stroke-width="1.6" fill="none"/>'
            '<path d="M92 98L72 80" stroke="#c9ced8" stroke-width="2.6" stroke-linecap="round"/>')


@_pixel
def _(g):
    rect(g, 8, 23, 18, 23, "#ffffff"); rect(g, 9, 20, 16, 22, "#fff6e6"); rect(g, 9, 20, 16, 20, "#ff9ec4")
    px(g, 15, 19, "#e8343a"); px(g, 21, 20, "#c9ced8"); px(g, 20, 19, "#c9ced8"); px(g, 19, 18, "#c9ced8")


@activity("croissant", "cafe", "eating a croissant", "🥐", ("กินครัวซองต์", 'gin khrua-sawng', "Eating a croissant"))
def _():
    return ('<path d="M62 92Q66 70 90 74Q100 80 96 96Q86 84 74 96Z" fill="#e8a24a" stroke="#b8742a" stroke-width="2" stroke-linejoin="round"/>'
            '<path d="M72 84q4 6 2 10M82 78q2 7-1 12" fill="none" stroke="#b8742a" stroke-width="1.6"/>'
            '<path d="M68 82q10-6 20-4" fill="none" stroke="#f6c87a" stroke-width="2"/>')


@_pixel
def _(g):
    rect(g, 17, 17, 21, 19, "#e8a24a"); px(g, 16, 18, "#e8a24a"); px(g, 22, 19, "#e8a24a")
    px(g, 18, 18, "#b8742a"); px(g, 20, 18, "#b8742a")


@activity("foodphoto", "cafe", "taking a photo of the food", "📸", ("ถ่ายรูปอาหาร", 'thàai-rûup aa-hǎan', "Taking a photo of the food"), motion="sparkle")
def _():
    return ('<rect x="40" y="84" width="40" height="24" rx="4" fill="#2f3240"/>'
            '<circle cx="60" cy="96" r="7.5" fill="#5b6478" stroke="#9fe0ff" stroke-width="2"/>'
            '<rect x="70" y="87" width="6" height="3" rx="1" fill="#ffd23f"/>'
            + sparkle(88, 80, 1.5, "#fff3a3"))


@_pixel
def _(g):
    rect(g, 10, 19, 20, 23, "#2f3240"); disc(g, 15, 21, 1, "#9fe0ff"); px(g, 18, 19, "#ffd23f")
    px(g, 23, 17, "#fff3a3")


# ------------------------------------------------------------------ bedroom
@activity("plushie", "bedroom", "hugging a plushie", "🧸", ("กอดตุ๊กตา", 'gàwt dtúk-gà-dtaa', "Hugging a plushie"), motion="hearts")
def _():
    return ('<circle cx="46" cy="84" r="5" fill="#b07a4a"/><circle cx="74" cy="84" r="5" fill="#b07a4a"/>'
            '<circle cx="60" cy="92" r="14" fill="#c48a56"/><ellipse cx="60" cy="108" rx="16" ry="10" fill="#c48a56"/>'
            '<ellipse cx="60" cy="96" rx="6" ry="4.6" fill="#f2d2a8"/>'
            '<circle cx="55" cy="89" r="1.8" fill="#3a2a20"/><circle cx="65" cy="89" r="1.8" fill="#3a2a20"/>'
            '<circle cx="60" cy="95" r="1.6" fill="#3a2a20"/>' + heart(60, 108, .9, "#ff8fb0"))


@_pixel
def _(g):
    disc(g, 15, 21, 3, "#c48a56"); px(g, 12, 18, "#b07a4a"); px(g, 18, 18, "#b07a4a")
    px(g, 14, 20, "#3a2a20"); px(g, 16, 20, "#3a2a20"); px(g, 15, 22, "#f2d2a8")


@activity("facemask", "bedroom", "relaxing in a face mask", "🧖", ("มาส์กหน้า", 'mâak nâa', "Face mask"), kind="head", closed=True)
def _():
    return ('<path fill-rule="evenodd" fill="#fbfbff" opacity=".95" stroke="#d9dbe6" stroke-width="1.4" '
            'd="M60 46C83 46 92 58 92 70C92 86 78 96 60 96C42 96 28 86 28 70C28 58 37 46 60 46Z'
            'M36 65a8 5 0 1 0 16 0a8 5 0 1 0 -16 0ZM68 65a8 5 0 1 0 16 0a8 5 0 1 0 -16 0Z'
            'M54 82a6 3 0 1 0 12 0a6 3 0 1 0 -12 0Z"/>'
            '<circle cx="42" cy="54" r="1.4" fill="#cfd8f0"/><circle cx="80" cy="56" r="1.4" fill="#cfd8f0"/>')


@_pixel
def _(g):
    rect(g, 10, 12, 20, 19, "#fbfbff")
    rect(g, 11, 14, 13, 14, "#39304a"); rect(g, 17, 14, 19, 14, "#39304a"); px(g, 15, 18, "#f2a0b0")


@activity("blanket", "bedroom", "snuggling under a blanket", "🛌", ("ห่มผ้า", 'hòm phâa', "Snuggling under a blanket"), closed=True)
def _():
    return ('<path d="M10 86Q30 78 60 84Q90 78 110 86L114 118H6Z" fill="#9fd0f0" stroke="#6fa8d6" stroke-width="2" stroke-linejoin="round"/>'
            '<path d="M14 96H106M12 106H108" stroke="#fff" stroke-width="2.4" stroke-dasharray="6 6" opacity=".8"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="2.4" fill="#ffd0e0"/>' for x, y in ((30, 92), (60, 100), (90, 92), (44, 112), (76, 112))))


@_pixel
def _(g):
    rect(g, 5, 20, 25, 25, "#9fd0f0"); rect(g, 6, 22, 24, 22, "#ffffff")
    px(g, 10, 24, "#ffd0e0"); px(g, 15, 21, "#ffd0e0"); px(g, 20, 24, "#ffd0e0")


# ------------------------------------------------------------------ rainy
@activity("umbrella", "rainy", "under an umbrella", "☂️", ("กางร่ม", 'gaang rôm', "Opening an umbrella"))
def _():
    stripes = "".join(f'<path d="M{x} 13Q{x + 6} -24 {66} -26" fill="none" stroke="#fff" stroke-width="2" opacity=".55"/>'
                      for x in (16, 44, 88, 116))
    return ('<path d="M66 -26V104q0 8-7 8" fill="none" stroke="#6b4a3a" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M-4 14Q66 -66 136 14Q119 6 101 14Q84 6 66 14Q48 6 31 14Q14 6 -4 14Z" fill="#e8584a" stroke="#b83b3b" stroke-width="2" stroke-linejoin="round"/>'
            + stripes + '<circle cx="66" cy="-27" r="2.6" fill="#b83b3b"/>')


@_pixel
def _(g):
    for y, half in ((0, 3), (1, 7), (2, 10), (3, 11)):
        rect(g, 15 - half, y, 15 + half, y, "#e8584a")
    for x in (6, 11, 15, 20, 25):
        px(g, x, 4, "#b83b3b")
    rect(g, 15, 1, 15, 21, "#6b4a3a"); px(g, 14, 22, "#6b4a3a")


@activity("puddle", "rainy", "jumping in puddles", "💦", ("กระโดดแอ่งน้ำ", 'grà-dòot àeng-náam', "Jumping in puddles"), motion="hop")
def _():
    drops = "".join(f'<path d="M{x} {y}q-3 5 0 7q3-2 0-7Z" fill="#7fc8ef"/>' for x, y in ((24, 96), (96, 94), (14, 106), (106, 104), (36, 90), (84, 88)))
    return ('<ellipse cx="60" cy="117" rx="48" ry="7" fill="#8fd0f0" opacity=".85"/>'
            '<path d="M24 115q6-8 12 0M84 115q6-8 12 0" fill="none" stroke="#fff" stroke-width="2"/>' + drops)


@_pixel
def _(g):
    rect(g, 5, 26, 25, 27, "#8fd0f0")
    for x, y in ((6, 22), (24, 21), (4, 24), (26, 24)):
        px(g, x, y, "#7fc8ef")


@activity("raincoat", "rainy", "in a yellow raincoat", "🧥", ("ใส่เสื้อกันฝน", 'sài sûea gan-fǒn', "Wearing a raincoat"))
def _():
    return ('<path d="M22 84Q60 74 98 84L106 116H14Z" fill="#ffd23f" stroke="#d6a92a" stroke-width="2" stroke-linejoin="round"/>'
            '<path d="M60 82V116" stroke="#d6a92a" stroke-width="1.6"/>'
            '<circle cx="60" cy="92" r="2.2" fill="#d6a92a"/><circle cx="60" cy="104" r="2.2" fill="#d6a92a"/>'
            '<path d="M28 84Q60 94 92 84" fill="none" stroke="#d6a92a" stroke-width="2"/>')


@_pixel
def _(g):
    rect(g, 7, 20, 23, 25, "#ffd23f"); rect(g, 15, 20, 15, 25, "#d6a92a"); px(g, 15, 22, "#d6a92a")


# ------------------------------------------------------------------ Wat Arun
@activity("wai", "wat_arun", "making a wai", "🙏", ("ไหว้", 'wâi', "Wai (a respectful greeting)"), motion="wave", closed=True)
def _():
    return _hands() + sparkle(96, 66, 1, SPARKLE) + sparkle(26, 70, .8, SPARKLE)


@_pixel
def _(g):
    _px_hands(g); px(g, 24, 15, SPARKLE); px(g, 6, 16, SPARKLE)


@activity("selfie", "wat_arun", "taking a selfie", "🤳", ("ถ่ายเซลฟี่", 'thàai sen-fîi', "Taking a selfie"), motion="sparkle")
def _():
    return ('<path d="M92 98L132 40" stroke="#5b6478" stroke-width="3" stroke-linecap="round"/>'
            '<rect x="124" y="20" width="18" height="28" rx="3" fill="#2f3240" transform="rotate(-20 133 34)"/>'
            '<rect x="127" y="24" width="12" height="18" rx="1.5" fill="#9fe0ff" transform="rotate(-20 133 34)"/>')


@_pixel
def _(g):
    for k in range(6):
        px(g, 22 + k, 20 - k * 2, "#5b6478"); px(g, 22 + k, 19 - k * 2, "#5b6478")
    rect(g, 27, 5, 30, 9, "#2f3240"); rect(g, 28, 6, 29, 8, "#9fe0ff")


@activity("lotus", "wat_arun", "holding a lotus", "🪷", ("ดอกบัว", 'dàwk-bua', "Lotus flower"))
def _():
    petals = "".join(f'<ellipse cx="{60 + dx}" cy="{88 + dy}" rx="6" ry="12" fill="#f7a8c8" stroke="#e07aa0" stroke-width="1.2" '
                     f'transform="rotate({r} {60 + dx} {88 + dy})"/>' for dx, dy, r in ((-10, 2, -30), (10, 2, 30), (0, -2, 0)))
    return ('<path d="M60 100V112" stroke="#4f9a4f" stroke-width="3"/>' + petals
            + '<ellipse cx="60" cy="100" rx="16" ry="4" fill="#5fae5a"/>')


@_pixel
def _(g):
    px(g, 14, 18, "#f7a8c8"); px(g, 15, 17, "#f7a8c8"); px(g, 16, 18, "#f7a8c8")
    rect(g, 13, 19, 17, 20, "#f7a8c8"); rect(g, 13, 21, 17, 21, "#5fae5a"); px(g, 15, 22, "#4f9a4f")


# ------------------------------------------------------------------ floating market
@activity("ngob", "market", "wearing a ngob hat", "👒", ("ใส่หมวกงอบ", 'sài mùak ngâwp', "Wearing a ngob hat"), kind="head")
def _():
    return ('<path d="M10 24Q60 34 110 24Q100 18 60 16Q20 18 10 24Z" fill="#e8d29a" stroke="#b8975a" stroke-width="2"/>'
            '<path d="M30 20Q60 -14 90 20Q60 26 30 20Z" fill="#f0dca8" stroke="#b8975a" stroke-width="2" stroke-linejoin="round"/>'
            '<path d="M40 14Q60 4 80 14M48 6Q60 0 72 6" fill="none" stroke="#c9ad6a" stroke-width="1.4"/>')


@_pixel
def _(g):
    rect(g, 3, 6, 27, 6, "#e8d29a"); rect(g, 8, 4, 22, 5, "#f0dca8"); rect(g, 11, 2, 19, 3, "#f0dca8")
    rect(g, 14, 1, 16, 1, "#f0dca8"); rect(g, 3, 7, 27, 7, "#b8975a")


@activity("stickyrice", "market", "eating mango sticky rice", "🥭", ("กินข้าวเหนียวมะม่วง", 'gin khâao-nǐao má-mûang', "Eating mango sticky rice"))
def _():
    return ('<ellipse cx="60" cy="104" rx="30" ry="7" fill="#fff" stroke="#e0d6ea" stroke-width="1.6"/>'
            '<ellipse cx="50" cy="98" rx="13" ry="8" fill="#fffdf6" stroke="#e8e0cc" stroke-width="1.2"/>'
            '<path d="M60 102Q66 86 84 92Q82 104 60 102Z" fill="#ffc83a" stroke="#e8a21a" stroke-width="1.4"/>'
            '<path d="M44 96q6 4 12 0" stroke="#f6f0e0" stroke-width="2.4" fill="none"/>')


@_pixel
def _(g):
    rect(g, 8, 23, 22, 23, "#ffffff"); rect(g, 9, 20, 13, 22, "#fffdf6"); rect(g, 15, 20, 20, 22, "#ffc83a")


@activity("coconut", "market", "drinking a coconut", "🥥", ("ดื่มน้ำมะพร้าว", 'dùem náam má-phráao', "Drinking coconut water"))
def _():
    return ('<path d="M89 74L68 80" stroke="#ff6f91" stroke-width="3.4" stroke-linecap="round"/>'
            '<circle cx="90" cy="88" r="15" fill="#6fb85a" stroke="#4f8a3f" stroke-width="2"/>'
            '<ellipse cx="90" cy="76" rx="9" ry="4" fill="#fffdf0" stroke="#d8d0b0" stroke-width="1.2"/>'
            '<path d="M80 92q10 6 20 0" stroke="#8fcf7a" stroke-width="2" fill="none"/>')


@_pixel
def _(g):
    disc(g, 21, 19, 3, "#6fb85a"); rect(g, 20, 16, 22, 16, "#fffdf0")
    px(g, 19, 16, "#ff6f91"); px(g, 18, 17, "#ff6f91"); px(g, 17, 18, "#ff6f91")


# ------------------------------------------------------------------ beach
@activity("sandcastle", "beach", "building a sandcastle", "🏰", ("ก่อปราสาททราย", 'gàw bpraa-sàat saai', "Building a sandcastle"), kind="side")
def _():
    return ('<rect x="126" y="94" width="42" height="24" fill="#f2d28a" stroke="#d6b060" stroke-width="1.6"/>'
            '<rect x="122" y="80" width="12" height="16" fill="#f2d28a" stroke="#d6b060" stroke-width="1.6"/>'
            '<rect x="160" y="80" width="12" height="16" fill="#f2d28a" stroke="#d6b060" stroke-width="1.6"/>'
            '<rect x="140" y="74" width="14" height="22" fill="#f6dc9a" stroke="#d6b060" stroke-width="1.6"/>'
            '<path d="M147 74V62" stroke="#8a6a3f" stroke-width="1.6"/><path d="M147 62l8 3-8 3Z" fill="#e8584a"/>'
            '<rect x="142" y="104" width="10" height="14" rx="5" fill="#d6b060"/>'
            '<path d="M104 118l8-14" stroke="#4f86d8" stroke-width="3" stroke-linecap="round"/>')


@_pixel
def _(g):
    rect(g, 28, 21, 36, 25, "#f2d28a"); rect(g, 27, 18, 29, 21, "#f2d28a"); rect(g, 35, 18, 37, 21, "#f2d28a")
    rect(g, 31, 17, 33, 21, "#f6dc9a"); px(g, 32, 15, "#8a6a3f"); px(g, 33, 15, "#e8584a"); px(g, 32, 16, "#8a6a3f")
    rect(g, 32, 23, 32, 25, "#d6b060")


@activity("sunglasses", "beach", "sunbathing in sunglasses", "😎", ("ใส่แว่นกันแดด", 'sài wâen gan-dàet', "Wearing sunglasses"), kind="head")
def _():
    return ('<rect x="31" y="57" width="26" height="17" rx="7" fill="#22252b"/>'
            '<rect x="63" y="57" width="26" height="17" rx="7" fill="#22252b"/>'
            '<path d="M57 63h6M31 62L18 58M89 62l13-4" stroke="#22252b" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M36 61l7 0M68 61l7 0" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".7"/>')


@_pixel
def _(g):
    rect(g, 9, 13, 13, 15, "#22252b"); rect(g, 17, 13, 21, 15, "#22252b"); rect(g, 14, 13, 16, 13, "#22252b")
    px(g, 10, 13, "#ffffff"); px(g, 18, 13, "#ffffff")


@activity("swimring", "beach", "wearing a swim ring", "🛟", ("ห่วงยาง", 'hùang-yaang', "Swim ring"))
def _():
    return ('<ellipse cx="60" cy="102" rx="44" ry="13" fill="none" stroke="#ff8fb0" stroke-width="12"/>'
            '<ellipse cx="60" cy="102" rx="44" ry="13" fill="none" stroke="#fff" stroke-width="12" stroke-dasharray="14 18"/>')


@_pixel
def _(g):
    rect(g, 4, 21, 26, 23, "#ff8fb0")
    for x in (6, 12, 18, 24):
        rect(g, x, 21, x + 1, 23, "#ffffff")


# ------------------------------------------------------------------ Yaowarat
@activity("dimsum", "yaowarat", "eating dim sum", "🥟", ("กินติ่มซำ", 'gin dtìm-sam', "Eating dim sum"))
def _():
    return ('<rect x="34" y="94" width="50" height="16" rx="5" fill="#d8b47a" stroke="#a8844a" stroke-width="2"/>'
            '<path d="M38 100h42M38 105h42" stroke="#a8844a" stroke-width="1.2"/>'
            '<path d="M42 94q6-10 12 0Z M56 94q6-10 12 0Z" fill="#fffaf0" stroke="#e8dcc0" stroke-width="1.2"/>'
            '<path d="M88 96L68 80M92 97L72 79" stroke="#8a5a33" stroke-width="2.6" stroke-linecap="round"/>'
            '<circle cx="68" cy="80" r="4.4" fill="#fffaf0" stroke="#e8dcc0" stroke-width="1.2"/>')


@_pixel
def _(g):
    rect(g, 9, 20, 19, 23, "#d8b47a"); rect(g, 10, 22, 18, 22, "#a8844a")
    px(g, 11, 19, "#fffaf0"); px(g, 14, 19, "#fffaf0"); px(g, 17, 19, "#fffaf0")
    for k in range(4):
        px(g, 21 - k, 20 - k, "#8a5a33")
    px(g, 17, 16, "#fffaf0")


@activity("lantern", "yaowarat", "carrying a red lantern", "🏮", ("ถือโคมแดง", 'thǔe khoom daeng', "Carrying a red lantern"))
def _():
    return ('<path d="M92 98L120 34" stroke="#8a5a33" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M120 34V42" stroke="#c9a24a" stroke-width="1.4"/>'
            '<ellipse cx="120" cy="56" rx="15" ry="14" fill="#e8343a" stroke="#b02028" stroke-width="2"/>'
            '<rect x="111" y="40" width="18" height="4" rx="1" fill="#f2c94c"/><rect x="111" y="68" width="18" height="4" rx="1" fill="#f2c94c"/>'
            '<path d="M114 56h12M120 46v20" stroke="#f2c94c" stroke-width="1.2" opacity=".7"/>'
            '<path d="M120 72v8" stroke="#f2c94c" stroke-width="2"/>')


@_pixel
def _(g):
    for k in range(6):
        px(g, 22 + k, 20 - k * 2, "#8a5a33")
    odisc(g, 29, 12, 3, "#e8343a", "#b02028"); rect(g, 27, 9, 31, 9, "#f2c94c"); rect(g, 27, 15, 31, 15, "#f2c94c")
    px(g, 29, 16, "#f2c94c")


@activity("angpao", "yaowarat", "getting a red envelope", "🧧", ("ได้อั่งเปา", 'dâai àng-bpao', "Getting a red envelope"), motion="sparkle")
def _():
    return ('<rect x="44" y="82" width="32" height="26" rx="3" fill="#e8343a" stroke="#b02028" stroke-width="2"/>'
            '<path d="M44 86L60 96L76 86" fill="none" stroke="#b02028" stroke-width="1.6"/>'
            '<circle cx="60" cy="98" r="5" fill="#f2c94c"/><circle cx="60" cy="98" r="2" fill="#e8343a"/>')


@_pixel
def _(g):
    rect(g, 11, 18, 19, 23, "#e8343a"); px(g, 15, 21, "#f2c94c"); px(g, 12, 18, "#b02028"); px(g, 18, 18, "#b02028")


# ------------------------------------------------------------------ tuk-tuk street
@activity("ride", "tuktuk", "riding a tuk-tuk", "🛺", ("นั่งตุ๊กตุ๊ก", 'nâng dtúk-dtúk', "Riding a tuk-tuk"), motion="ride")
def _():
    return ('<path d="M-12 2H138V12H-12Z" fill="#1f4fa6"/>'
            '<path d="M-6 12V86M132 12V86" stroke="#1f4fa6" stroke-width="4"/>'
            '<path d="M-12 84H140V112Q140 118 134 118H-6Q-12 118-12 112Z" fill="#2f6fd6" stroke="#1f4fa6" stroke-width="2"/>'
            '<path d="M-12 96H140" stroke="#ffd23f" stroke-width="4"/>'
            '<path d="M140 88h18v22h-18" fill="#2f6fd6" stroke="#1f4fa6" stroke-width="2"/>'
            '<circle cx="152" cy="94" r="4" fill="#fff3a3"/>'
            '<circle cx="8" cy="120" r="9" fill="#22252b"/><circle cx="118" cy="120" r="9" fill="#22252b"/>'
            '<circle cx="8" cy="120" r="3" fill="#aaa"/><circle cx="118" cy="120" r="3" fill="#aaa"/>')


@_pixel
def _(g):
    rect(g, 1, 2, 31, 3, "#1f4fa6"); rect(g, 2, 4, 2, 21, "#1f4fa6"); rect(g, 30, 4, 30, 21, "#1f4fa6")
    rect(g, 1, 21, 32, 25, "#2f6fd6"); rect(g, 1, 23, 32, 23, "#ffd23f"); rect(g, 33, 21, 35, 25, "#2f6fd6")
    px(g, 35, 22, "#fff3a3"); disc(g, 4, 26, 1, "#22252b"); disc(g, 28, 26, 1, "#22252b")


@activity("teabag", "tuktuk", "drinking Thai tea from a bag", "🧋", ("ชาเย็นใส่ถุง", 'chaa-yen sài thǔng', "Thai iced tea in a bag"))
def _():
    return ('<path d="M90 64L68 79" stroke="#ff6f91" stroke-width="3.4" stroke-linecap="round"/>'
            '<path d="M80 66Q78 92 84 100Q92 106 100 100Q106 92 102 66Z" fill="#fff" opacity=".55" stroke="#c9d6e3" stroke-width="1.4"/>'
            '<path d="M80.5 76Q79.5 92 84 99Q92 104 99.5 99Q104 92 101.5 76Z" fill="#f28c38"/>'
            '<path d="M80 66q11 5 22 0" fill="none" stroke="#e05050" stroke-width="2.6"/>'
            '<path d="M84 66q-6-8 0-12" fill="none" stroke="#e05050" stroke-width="2"/>')


@_pixel
def _(g):
    rect(g, 19, 15, 23, 21, "#e6eef5"); rect(g, 19, 17, 23, 21, "#f28c38"); rect(g, 19, 15, 23, 15, "#e05050")
    px(g, 18, 16, "#ff6f91"); px(g, 17, 17, "#ff6f91")


@activity("moopink", "tuktuk", "eating moo ping skewers", "🍢", ("หมูปิ้ง", 'mǔu bpîng', "Grilled pork skewers"))
def _():
    sticks = ""
    for d in (-6, 0, 6):
        sticks += (f'<path d="M{95 + d} 100L{76 + d} 74" stroke="#d8c7a0" stroke-width="2" stroke-linecap="round"/>'
                   + "".join(f'<rect x="{x + d - 4}" y="{y - 3}" width="8" height="6" rx="2" fill="#a8582a" '
                             f'transform="rotate(-55 {x + d} {y})"/>' for x, y in ((79, 78), (84, 85))))
    return sticks


@_pixel
def _(g):
    for d in (0, 2):
        px(g, 22 + d, 21, "#d8c7a0"); px(g, 21 + d, 20, "#d8c7a0")
        rect(g, 19 + d, 17, 20 + d, 19, "#a8582a")


# ------------------------------------------------------------------ Songkran
@activity("watergun", "songkran", "squirting a water gun", "🔫", ("เล่นปืนฉีดน้ำ", 'lên bpuen chìit-náam', "Playing with a water gun"), motion="sparkle")
def _():
    return ('<path d="M84 90h26q6 0 6 6v4h-20l-4 12h-8l2-14h-2Z" fill="#4fc3f7" stroke="#2f8fc7" stroke-width="2" stroke-linejoin="round"/>'
            '<rect x="88" y="82" width="16" height="10" rx="4" fill="#ffd23f" stroke="#d6a92a" stroke-width="1.6"/>'
            '<path d="M118 96Q140 88 164 98" fill="none" stroke="#8fd8ff" stroke-width="4" stroke-linecap="round" opacity=".85"/>'
            + "".join(f'<path d="M{x} {y}q-3 5 0 7q3-2 0-7Z" fill="#8fd8ff"/>' for x, y in ((168, 96), (160, 104), (172, 106))))


@_pixel
def _(g):
    rect(g, 21, 19, 26, 20, "#4fc3f7"); px(g, 22, 21, "#4fc3f7"); rect(g, 22, 18, 24, 18, "#ffd23f")
    for x in range(27, 33):
        px(g, x, 19 - (1 if 29 <= x <= 31 else 0), "#8fd8ff")


@activity("bucket", "songkran", "splashing a bucket of water", "🪣", ("ถังน้ำ", 'thǎng náam', "Water bucket"), motion="sparkle")
def _():
    return ('<path d="M40 84H80L76 110H44Z" fill="#c9ced8" stroke="#8a93a3" stroke-width="2" stroke-linejoin="round"/>'
            '<ellipse cx="60" cy="84" rx="20" ry="4" fill="#8fd8ff"/>'
            '<path d="M48 82Q58 50 82 56M60 80Q72 54 96 66" fill="none" stroke="#8fd8ff" stroke-width="3" stroke-linecap="round" opacity=".8"/>'
            + "".join(f'<path d="M{x} {y}q-3 5 0 7q3-2 0-7Z" fill="#8fd8ff"/>' for x, y in ((86, 52), (100, 62), (74, 44))))


@_pixel
def _(g):
    rect(g, 11, 19, 19, 23, "#c9ced8"); rect(g, 11, 19, 19, 19, "#8fd8ff")
    px(g, 13, 17, "#8fd8ff"); px(g, 16, 15, "#8fd8ff"); px(g, 20, 14, "#8fd8ff"); px(g, 23, 15, "#8fd8ff")


@activity("flowershirt", "songkran", "in a flower shirt", "🌺", ("ใส่เสื้อลายดอก", 'sài sûea laai dàwk', "Wearing a flower-print shirt"))
def _():
    flowers = "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/><circle cx="{x}" cy="{y}" r="1.4" fill="#ffd23f"/>'
                      for x, y, c in ((34, 98, "#ff7ab0"), (52, 108, "#ffd23f"), (70, 96, "#ff7ab0"),
                                      (86, 108, "#fff"), (44, 88, "#fff"), (80, 88, "#ffd23f")))
    return ('<path d="M24 86Q60 78 96 86L100 114H20Z" fill="#4fc3f7" stroke="#2f8fc7" stroke-width="2" stroke-linejoin="round"/>'
            '<path d="M50 82L60 96L70 82" fill="none" stroke="#2f8fc7" stroke-width="2"/>' + flowers)


@_pixel
def _(g):
    rect(g, 8, 20, 22, 25, "#4fc3f7")
    for x, y, c in ((10, 21, "#ff7ab0"), (14, 23, "#ffd23f"), (18, 21, "#ff7ab0"), (21, 24, "#ffd23f")):
        px(g, x, y, c)


# ------------------------------------------------------------------ Loy Krathong
@activity("krathong", "loykrathong", "floating a krathong", "🪷", ("ลอยกระทง", 'loi grà-thong', "Floating a krathong"), motion="float")
def _():
    return ('<ellipse cx="60" cy="104" rx="26" ry="7" fill="#3f8f4f" stroke="#2f6f3e" stroke-width="1.6"/>'
            '<path d="M38 102q22-26 44 0Z" fill="#f7a8c8" stroke="#e07aa0" stroke-width="1.4"/>'
            '<path d="M48 100q12-16 24 0Z" fill="#ffd0e0"/>'
            '<rect x="58" y="80" width="4" height="16" fill="#fff6d6"/>'
            '<ellipse cx="60" cy="77" rx="3" ry="4.4" fill="#ffd66b"/>')


@_pixel
def _(g):
    rect(g, 9, 22, 21, 23, "#3f8f4f"); rect(g, 11, 20, 19, 21, "#f7a8c8"); px(g, 15, 19, "#f7a8c8")
    rect(g, 15, 17, 15, 19, "#fff6d6"); px(g, 15, 16, "#ffd66b")


@activity("skylantern", "loykrathong", "releasing a sky lantern", "🏮", ("ปล่อยโคมลอย", 'bplòi khoom-loi', "Releasing a sky lantern"), motion="rise")
def _():
    return ('<path d="M44 -4H76L72 30H48Z" fill="#ffb347" stroke="#e08a2a" stroke-width="1.6" opacity=".95"/>'
            '<path d="M44 -4H76L72 30H48Z" fill="#fff3c4" opacity=".35"/>'
            '<ellipse cx="60" cy="31" rx="12" ry="3" fill="#e08a2a"/>'
            '<ellipse cx="60" cy="36" rx="3" ry="4" fill="#ffd66b"/>')


@_pixel
def _(g):
    rect(g, 12, 0, 18, 4, "#ffb347"); rect(g, 13, 5, 17, 5, "#e08a2a"); px(g, 15, 6, "#ffd66b")


@activity("sparkler", "loykrathong", "waving a sparkler", "✨", ("จุดพลุ", 'jùt phlú', "Lighting sparklers"), motion="sparkle")
def _():
    rays = "".join(f'<path d="M116 46l{dx} {dy}" stroke="#fff3a3" stroke-width="1.6" stroke-linecap="round"/>'
                   for dx, dy in ((10, 0), (-10, 0), (0, 10), (0, -10), (7, 7), (-7, -7), (7, -7), (-7, 7)))
    return ('<path d="M92 98L116 46" stroke="#8a8f9a" stroke-width="2.4" stroke-linecap="round"/>'
            '<circle cx="116" cy="46" r="4" fill="#ffd66b"/>' + rays)


@_pixel
def _(g):
    for k in range(5):
        px(g, 22 + k, 20 - k * 2, "#8a8f9a"); px(g, 22 + k, 19 - k * 2, "#8a8f9a")
    px(g, 27, 10, "#ffd66b"); px(g, 26, 9, "#fff3a3"); px(g, 28, 9, "#fff3a3"); px(g, 27, 8, "#fff3a3")
    px(g, 26, 11, "#fff3a3"); px(g, 28, 11, "#fff3a3")


@activity("wish", "loykrathong", "making a wish", "🤞", ("อธิษฐาน", 'à-thít-thǎan', "Making a wish"), closed=True)
def _():
    return _hands() + sparkle(60, 10, 2, "#fff3a3") + sparkle(40, 22, 1, SPARKLE) + sparkle(82, 20, 1, SPARKLE)


@_pixel
def _(g):
    _px_hands(g); px(g, 15, 1, "#fff3a3"); px(g, 14, 2, "#fff3a3"); px(g, 16, 2, "#fff3a3"); px(g, 15, 3, "#fff3a3")


# ------------------------------------------------------------------ SAMTUABAHT Fanmeet
@activity("sing", "stage", "singing on stage", "🎤", ("ร้องเพลง", 'ráwng-phleeng', "Singing"))
def _():
    return ('<path d="M92 98L74 84" stroke="#2b2b33" stroke-width="5" stroke-linecap="round"/>'
            '<circle cx="70" cy="81" r="6.5" fill="#c9ced8" stroke="#8a93a3" stroke-width="1.6"/>'
            + note(132, 40, "#ff7ab0") + note(152, 22, "#8fd8ff"))


@_pixel
def _(g):
    px(g, 21, 21, "#2b2b33"); px(g, 20, 20, "#2b2b33"); px(g, 19, 19, "#2b2b33"); disc(g, 18, 18, 1, "#c9ced8")
    rect(g, 30, 9, 30, 13, "#ff7ab0"); px(g, 29, 14, "#ff7ab0")


@activity("lightstick", "stage", "waving a lightstick", "🪄", ("โบกแท่งไฟ", 'bòok thâeng-fai', "Waving a lightstick"), motion="wave")
def _():
    return ('<path d="M92 98L110 52" stroke="#3a3550" stroke-width="4" stroke-linecap="round"/>'
            '<ellipse cx="113" cy="44" rx="9" ry="12" fill="#ff7ab0" stroke="#fff" stroke-width="2" transform="rotate(20 113 44)"/>'
            '<ellipse cx="113" cy="44" rx="15" ry="18" fill="#ff7ab0" opacity=".25" transform="rotate(20 113 44)"/>')


@_pixel
def _(g):
    for k in range(4):
        px(g, 22 + k // 2, 20 - k, "#3a3550")
    rect(g, 23, 12, 25, 16, "#ff7ab0"); px(g, 24, 11, "#ffd0e0")


@activity("hearthands", "stage", "making heart hands", "🫶", ("ทำมือรูปหัวใจ", 'tham mue rûup hǔa-jai', "Making heart hands"), motion="hearts")
def _():
    return heart(60, 4, 3.4, "#ff6f91") + heart(30, 20, 1.2, "#ff9ec4") + heart(92, 18, 1.2, "#ff9ec4")


@_pixel
def _(g):
    for x, y in ((13, 0), (17, 0), (12, 1), (13, 1), (14, 1), (16, 1), (17, 1), (18, 1), (13, 2), (14, 2), (15, 2),
                 (16, 2), (17, 2), (14, 3), (15, 3), (16, 3), (15, 4)):
        px(g, x, y, "#ff6f91")


@activity("flowers", "stage", "receiving flowers", "💐", ("ได้ดอกไม้", 'dâai dàwk-máai', "Receiving flowers"), motion="hearts")
def _():
    blooms = "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{c}"/><circle cx="{x}" cy="{y}" r="2" fill="#ffd23f"/>'
                     for x, y, c in ((50, 78, "#e8343a"), (62, 72, "#ff7ab0"), (74, 80, "#fff"),
                                     (56, 86, "#ff9ec4"), (70, 88, "#e8343a")))
    return ('<path d="M44 86L60 116L76 86Z" fill="#ffd0e0" stroke="#e07aa0" stroke-width="1.6" stroke-linejoin="round"/>'
            + blooms + '<path d="M54 100h12" stroke="#e07aa0" stroke-width="3"/>')


@_pixel
def _(g):
    rect(g, 12, 20, 18, 21, "#ffd0e0"); rect(g, 13, 22, 17, 23, "#ffd0e0"); px(g, 15, 24, "#ffd0e0")
    for x, y, c in ((12, 18, "#e8343a"), (14, 17, "#ff7ab0"), (16, 17, "#ffd23f"), (18, 18, "#ff7ab0"), (15, 19, "#e8343a")):
        px(g, x, y, c)


# ------------------------------------------------------------------ dance party
@activity("partyhat", "party", "wearing a party hat", "🥳", ("ใส่หมวกปาร์ตี้", 'sài mùak bpaa-dtîi', "Wearing a party hat"), kind="head")
def _():
    return ('<path d="M46 22L72 -12L84 24Z" fill="#7a5af8" stroke="#5a3ad8" stroke-width="2" stroke-linejoin="round"/>'
            '<path d="M54 12L78 6M62 2L80 -2" stroke="#ffd23f" stroke-width="3"/>'
            '<circle cx="72" cy="-13" r="4.6" fill="#ff7ab0"/>')


@_pixel
def _(g):
    rect(g, 13, 4, 19, 5, "#7a5af8"); rect(g, 14, 2, 18, 3, "#7a5af8"); rect(g, 15, 0, 17, 1, "#7a5af8")
    rect(g, 14, 3, 18, 3, "#ffd23f"); px(g, 16, 0, "#ff7ab0")


@activity("confetti", "party", "popping confetti", "🎉", ("โปรยกระดาษ", 'bproi grà-dàat', "Throwing confetti"), motion="confetti")
def _():
    bits = "".join(f'<rect x="{x}" y="{y}" width="5" height="3" rx="1" fill="{c}" transform="rotate({r} {x} {y})"/>'
                   for x, y, c, r in ((118, 50, "#ff7ab0", 20), (132, 40, "#ffd23f", -30), (126, 62, "#8fd8ff", 45),
                                      (146, 54, "#7cc35b", 10), (140, 30, "#b38cff", -15), (156, 44, "#ff7ab0", 60)))
    return ('<path d="M92 100L112 66L120 74Z" fill="#f2c94c" stroke="#d6a92a" stroke-width="1.6" stroke-linejoin="round"/>'
            '<path d="M100 88l10-4M96 94l10-4" stroke="#e8584a" stroke-width="2"/>' + bits)


@_pixel
def _(g):
    px(g, 21, 21, "#f2c94c"); px(g, 22, 20, "#f2c94c"); px(g, 23, 19, "#f2c94c"); px(g, 24, 18, "#f2c94c")
    for x, y, c in ((27, 15, "#ff7ab0"), (29, 12, "#ffd23f"), (31, 16, "#8fd8ff"), (33, 13, "#7cc35b"), (30, 10, "#b38cff")):
        px(g, x, y, c)


# ------------------------------------------------------------------ rooftop bar
@activity("cocktail", "bar", "sipping a cocktail", "🍸", ("จิบค็อกเทล", 'jìp khák-theen', "Sipping a cocktail"))
def _():
    return ('<path d="M76 70H104L90 86Z" fill="#ff8fb0" stroke="#fff" stroke-width="1.6" stroke-linejoin="round" opacity=".95"/>'
            '<path d="M90 86V98M84 99h12" stroke="#e6eef5" stroke-width="2.4" stroke-linecap="round"/>'
            '<path d="M98 60L92 76" stroke="#8a5a33" stroke-width="1.6"/><circle cx="98" cy="60" r="3" fill="#5fae5a"/>'
            '<path d="M78 70l-8-10" stroke="#ffd23f" stroke-width="1.6"/><path d="M64 56q6-6 12 0Z" fill="#ff7ab0"/>')


@_pixel
def _(g):
    rect(g, 18, 15, 24, 15, "#ff8fb0"); rect(g, 19, 16, 23, 16, "#ff8fb0"); rect(g, 20, 17, 22, 17, "#ff8fb0")
    rect(g, 21, 18, 21, 20, "#e6eef5"); px(g, 23, 14, "#5fae5a")


@activity("cheers", "bar", "clinking glasses", "🥂", ("ชนแก้ว", 'chon gâew', "Cheers! (clinking glasses)"), motion="sparkle")
def _():
    return ('<path d="M96 52H114L111 72H99Z" fill="#ffe08a" stroke="#fff" stroke-width="1.6" opacity=".95"/>'
            '<path d="M96 52H114L113 58H97Z" fill="#fffdf0"/>'
            '<path d="M105 72V96" stroke="#e6eef5" stroke-width="2.4"/><path d="M92 98L104 94" stroke="#e6eef5" stroke-width="2.4"/>'
            + sparkle(122, 46, 1.6, "#fff3a3") + sparkle(130, 58, 1, SPARKLE))


@_pixel
def _(g):
    rect(g, 22, 10, 25, 13, "#ffe08a"); rect(g, 22, 10, 25, 10, "#fffdf0"); rect(g, 23, 14, 23, 19, "#e6eef5")
    px(g, 22, 20, "#e6eef5"); px(g, 27, 9, "#fff3a3")


@activity("citycam", "bar", "photographing the view", "📸", ("ถ่ายรูปวิว", 'thàai-rûup wiw', "Photographing the view"), motion="sparkle")
def _():
    return ('<rect x="40" y="84" width="40" height="26" rx="4" fill="#2b2b33"/>'
            '<rect x="46" y="80" width="12" height="6" rx="2" fill="#2b2b33"/>'
            '<circle cx="60" cy="97" r="9" fill="#5b6478" stroke="#c9ced8" stroke-width="2.4"/>'
            '<circle cx="57" cy="94" r="2.4" fill="#fff" opacity=".7"/><rect x="70" y="88" width="6" height="3" rx="1" fill="#ffd23f"/>')


@_pixel
def _(g):
    rect(g, 10, 19, 20, 24, "#2b2b33"); rect(g, 11, 18, 13, 18, "#2b2b33"); disc(g, 15, 21, 1, "#c9ced8")
    px(g, 18, 19, "#ffd23f")


# ------------------------------------------------------------------ the original 12
# Thai words for the activities that can happen in any scene.
GENERAL_WORDS = {
    "chicken": ("กินไก่ทอด", 'gin gài thâwt', "Eating fried chicken"),
    "music": ("ฟังเพลง", 'fang phleeng', "Listening to music"),
    "sleep": ("นอนหลับ", 'nawn-làp', "Sleeping"),
    "read": ("อ่านหนังสือ", 'àan nǎng-sǔe', "Reading a book"),
    "work": ("ทำงาน", 'tham-ngaan', "Working"),
    "tv": ("ดูทีวี", 'duu thii-wii', "Watching TV"),
    "bubbletea": ("ชานมไข่มุก", 'chaa-nom khài-múk', "Bubble tea"),
    "coffee": ("ดื่มกาแฟ", 'dùem gaa-fae', "Drinking coffee"),
    "game": ("เล่นเกม", 'lên geem', "Playing games"),
    "noodles": ("กินก๋วยเตี๋ยว", 'gin gǔai-dtǐao', "Eating noodle soup"),
    "phone": ("เล่นโทรศัพท์", 'lên thoo-rá-sàp', "Using the phone"),
    "plant": ("รดน้ำต้นไม้", 'rót náam dtôn-máai', "Watering the plant"),
}
GENERAL_EMOJI = {
    "chicken": "🍗", "music": "🎧", "sleep": "💤", "read": "📖", "work": "💻", "tv": "📺",
    "bubbletea": "🧋", "coffee": "☕", "game": "🎮", "noodles": "🍜", "phone": "📱", "plant": "🪴",
}
GENERAL_SIDE = {"tv", "plant", "sleep"}
