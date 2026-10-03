"""Background scenes for the ThaiDevPet panel (cartoon SVG source).

Every scene is a 480 x 150 SVG anchored to the bottom of the panel, with the
floor top at y = 128 (22 px above the panel's bottom edge, where the pet
stands). Narrower panels crop the sides; taller ones fill the space above
with the scene's `top` colour and wider ones extend the `floor` colour.

The pixel versions are made from these same drawings by
tools/export_web.py (rendered small, palette-reduced, shown pixelated).
"""

W, H, FLOOR = 480, 150, 128

CATEGORIES = [
    ("everyday", "Everyday"),
    ("thailand", "Thailand"),
    ("festivals", "Festivals"),
    ("party", "Party"),
]


def _svg(body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'preserveAspectRatio="xMidYMax slice"><defs>{defs}</defs>{body}</svg>\n')


def _vgrad(gid, *stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">{s}</linearGradient>'


_GLOW = ('<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">'
         '<feGaussianBlur stdDeviation="2.2" result="b"/><feMerge>'
         '<feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def _star(x, y, s, fill, opacity=1):
    return (f'<path transform="translate({x} {y}) scale({s})" opacity="{opacity}" fill="{fill}" '
            'd="M0-4L1-1 4 0 1 1 0 4-1 1-4 0-1-1Z"/>')


# ------------------------------------------------------------------ everyday
def office():
    sky = "#cfe8f7"
    towers = "".join(
        f'<rect x="{x}" y="{78 - h}" width="{w}" height="{h}" fill="#a9c6dc"/>'
        + "".join(f'<rect x="{x + 3 + c * 6}" y="{82 - h + r * 7}" width="3" height="3" fill="#e9f4fb"/>'
                  for r in range(h // 8) for c in range(w // 7))
        for x, w, h in ((32, 20, 30), (54, 16, 42), (72, 22, 24), (96, 18, 36), (116, 16, 20)))
    books = "".join(f'<rect x="{x}" y="{y - h}" width="5" height="{h}" rx="1" fill="{c}"/>'
                    for x, y, h, c in ((330, 60, 16, "#e86a6a"), (336, 60, 13, "#6aa8e8"), (342, 60, 15, "#f2c94c"),
                                       (348, 60, 12, "#7cc28a"), (360, 90, 14, "#b08ae8"), (366, 90, 16, "#e8a06a"),
                                       (372, 90, 12, "#6ac8c0")))
    code = "".join(f'<rect x="{252 + i}" y="{70 + n * 5}" width="{w}" height="2" rx="1" fill="{c}"/>'
                   for n, (i, w, c) in enumerate(((0, 18, "#c792ea"), (6, 24, "#82aaff"), (6, 14, "#c3e88d"),
                                                  (12, 20, "#f78c6c"), (6, 10, "#82aaff"), (0, 8, "#c792ea"))))
    notes = "".join(f'<rect x="{x}" y="{y}" width="9" height="9" fill="{c}" transform="rotate({r} {x} {y})"/>'
                    for x, y, c, r in ((182, 40, "#fff3a3", -6), (194, 46, "#ffc6dd", 5), (186, 56, "#c6f0d8", -3)))
    return _svg(f'''
<rect width="480" height="150" fill="#eaf0f7"/>
<rect y="104" width="480" height="24" fill="#dfe6f0"/>
<path d="M0 104H480" stroke="#cdd7e4" stroke-width="2"/>
<rect x="26" y="20" width="104" height="66" rx="4" fill="{sky}" stroke="#fff" stroke-width="4"/>
{towers}
<path d="M78 20V86M26 52H130" stroke="#fff" stroke-width="3"/>
<circle cx="168" cy="30" r="12" fill="#fff" stroke="#9aa8bc" stroke-width="2.4"/>
<path d="M168 30V22M168 30h6" stroke="#4a5568" stroke-width="2" stroke-linecap="round"/>
{notes}
<rect x="324" y="60" width="60" height="4" rx="1" fill="#b08a64"/><rect x="324" y="90" width="60" height="4" rx="1" fill="#b08a64"/>
{books}
<path d="M398 90q-6-16 4-26q10 10 4 26Z" fill="#6fbf73"/><path d="M410 90q2-14 10-18q4 12-4 18Z" fill="#88cf8a"/>
<rect x="398" y="90" width="20" height="14" rx="2" fill="#e8a06a"/>
<rect x="216" y="100" width="128" height="6" rx="2" fill="#c9a27a"/>
<rect x="222" y="106" width="5" height="22" fill="#a8845f"/><rect x="333" y="106" width="5" height="22" fill="#a8845f"/>
<rect x="244" y="62" width="64" height="38" rx="3" fill="#2d3343"/>{code}
<rect x="272" y="100" width="8" height="2" fill="#2d3343"/>
<rect x="312" y="88" width="10" height="12" rx="2" fill="#fff" stroke="#d8d2c6" stroke-width="1.2"/>
<path d="M322 91q4 0 4 3t-4 3" fill="none" stroke="#d8d2c6" stroke-width="1.6"/>
<path d="M315 85q-2-3 0-6M319 85q-2-3 0-6" stroke="#c9c4dd" stroke-width="1.2" fill="none"/>
<rect x="226" y="94" width="14" height="6" rx="1" fill="#f2c94c"/>
<rect y="128" width="480" height="22" fill="#b9c4d8"/>
<path d="M0 128H480" stroke="#a7b3c9" stroke-width="2"/>''')


def cafe():
    planks = "".join(f'<path d="M0 {y}H480" stroke="#b07f52" stroke-width="1"/>' for y in (136, 144))
    panels = "".join(f'<path d="M{x} 96V128" stroke="#d9bb93" stroke-width="1.2"/>' for x in range(14, 480, 22))
    awning = "".join(
        f'<path d="M{x} 24h10v10q-5 5-10 0Z" fill="{"#f4a3b5" if i % 2 else "#fff7f0"}"/>'
        for i, x in enumerate(range(22, 102, 10)))
    cups = "".join(f'<rect x="{x}" y="42" width="7" height="8" rx="1.5" fill="{c}"/>'
                   for x, c in ((334, "#fff"), (344, "#f4a3b5"), (354, "#9fd9c0"), (364, "#fff"), (374, "#ffe08a")))
    lamps = "".join(f'<path d="M{x} 0V18" stroke="#8a6a4f" stroke-width="1"/>'
                    f'<path d="M{x - 9} 26L{x} 16 {x + 9} 26Z" fill="#f2b46b"/>'
                    f'<circle cx="{x}" cy="28" r="6" fill="#fff3c4" opacity=".7"/>' for x in (200, 262, 420))
    return _svg(f'''
<rect width="480" height="150" fill="#f7e8d4"/>
<rect y="92" width="480" height="36" fill="#ecd3b2"/>{panels}
<rect x="28" y="34" width="70" height="52" rx="3" fill="#bfe6f3" stroke="#fffaf3" stroke-width="4"/>
<circle cx="80" cy="52" r="9" fill="#fff4c2"/>
<circle cx="44" cy="76" r="14" fill="#8fd08a"/><circle cx="60" cy="80" r="10" fill="#7cc27a"/>
<path d="M63 34V86M28 60H98" stroke="#fffaf3" stroke-width="3"/>
{awning}{lamps}
<rect x="126" y="40" width="62" height="40" rx="2" fill="#33413a" stroke="#a77b4f" stroke-width="3"/>
<text x="157" y="52" fill="#fff" font-size="8" text-anchor="middle" font-family="sans-serif">เมนู</text>
<text x="132" y="64" fill="#f6e7c8" font-size="6.5" font-family="sans-serif">กาแฟ ··· 45</text>
<text x="132" y="74" fill="#f6e7c8" font-size="6.5" font-family="sans-serif">ชาไทย ··· 40</text>
<rect x="328" y="50" width="66" height="3.5" rx="1" fill="#a5713f"/>{cups}
<path d="M386 50q-2-10 4-12q6 2 4 12Z" fill="#6fbf73"/>
<rect x="232" y="88" width="64" height="40" rx="3" fill="#a5713f"/><rect x="228" y="84" width="72" height="6" rx="2" fill="#c08850"/>
<rect x="244" y="72" width="12" height="12" rx="2" fill="#5a4a42"/><rect x="246" y="66" width="8" height="6" fill="#3a2f2a"/>
<path d="M276 84l2-10h10l2 10Z" fill="#fff" stroke="#e0d0c0" stroke-width="1"/>
<ellipse cx="420" cy="108" rx="26" ry="4.5" fill="#a5713f"/>
<rect x="417" y="110" width="6" height="18" fill="#8a5a33"/><rect x="408" y="126" width="24" height="3" rx="1.5" fill="#8a5a33"/>
<rect x="412" y="98" width="10" height="9" rx="2" fill="#fff"/><path d="M422 100q4 0 4 3t-4 3" fill="none" stroke="#fff" stroke-width="1.6"/>
<path d="M415 95q-2-3 0-6M419 95q-2-3 0-6" stroke="#c9b9a8" stroke-width="1.2" fill="none"/>
<rect y="128" width="480" height="22" fill="#c8935f"/>{planks}''')


# ------------------------------------------------------------------ party
def stage():
    folds = lambda x0, d: "".join(f'<path d="M{x0 + d * i * 9} 18V128" stroke="#8e1d2c" stroke-width="2.4"/>'
                                  for i in range(1, 6))
    valance = "".join(f'<path d="M{x} 0h40v14q-20 10-40 0Z" fill="#b8263a"/>'
                      f'<circle cx="{x + 20}" cy="20" r="2.4" fill="#f2c94c"/>' for x in range(0, 480, 40))
    beams = "".join(f'<path d="M{x} 18L{x - 40} 128H{x + 40}Z" fill="{c}" opacity=".18"/>'
                    for x, c in ((140, "#fff3c4"), (240, "#ffd6ea"), (340, "#fff3c4")))
    lights = "".join(f'<circle cx="{x}" cy="129" r="2" fill="#ffe08a" filter="url(#glow)"/>'
                     for x in range(10, 480, 24))
    crowd = "".join(f'<circle cx="{x}" cy="{146 - (x % 3)}" r="7" fill="#1c1430"/>' for x in range(4, 480, 13))
    sticks = "".join(f'<rect x="{x}" y="{132 - (x % 5)}" width="2.4" height="9" rx="1.2" fill="{c}" '
                     f'transform="rotate({(x % 7) * 4 - 12} {x} 140)" filter="url(#glow)"/>'
                     for x, c in zip(range(12, 480, 26), ["#ff7ab0", "#8fd8ff", "#ffd66b", "#b38cff"] * 5))
    return _svg(f'''
<rect width="480" height="150" fill="#2a1c3f"/>
<rect x="110" y="26" width="260" height="76" rx="4" fill="#1a1230" stroke="#4a3a6a" stroke-width="2"/>
<rect x="116" y="32" width="248" height="64" rx="2" fill="url(#screen)"/>
<text x="240" y="62" fill="#fff" font-size="15" font-weight="700" text-anchor="middle" font-family="sans-serif" filter="url(#glow)">SAMTUABAHT Fanmeet</text>
<text x="240" y="82" fill="#ffd6ea" font-size="9" text-anchor="middle" font-family="sans-serif">♥ ขอบคุณที่มานะ ♥</text>
{_star(132, 44, 1.2, "#fff")}{_star(350, 84, 1, "#fff")}{_star(344, 42, .8, "#ffd66b")}
{beams}
<path d="M0 0H78V128Q60 90 74 50Q40 70 0 60Z" fill="#c8283f"/>{folds(4, 1)}
<path d="M480 0H402V128Q420 90 406 50Q440 70 480 60Z" fill="#c8283f"/>{folds(476, -1)}
<path d="M70 52q8 4 4 14" stroke="#f2c94c" stroke-width="2.4" fill="none"/>
<path d="M410 52q-8 4-4 14" stroke="#f2c94c" stroke-width="2.4" fill="none"/>
{valance}
<rect x="84" y="108" width="16" height="20" rx="2" fill="#2d2440"/><circle cx="92" cy="116" r="4" fill="#4a3a6a"/>
<rect x="380" y="108" width="16" height="20" rx="2" fill="#2d2440"/><circle cx="388" cy="116" r="4" fill="#4a3a6a"/>
<rect y="124" width="480" height="5" fill="#c08850"/>
<rect y="128" width="480" height="22" fill="#130d22"/>{lights}{crowd}{sticks}''',
                _vgrad("screen", (0, "#ff7ab0"), (1, "#7a5af8")) + _GLOW)


def party():
    beams = "".join(f'<path d="M{x} 0L{x - 40} 128H{x + 40}Z" fill="{c}" opacity=".16"/>'
                    for x, c in ((60, "#ff7ab0"), (170, "#8fd8ff"), (310, "#ffd66b"), (420, "#b38cff")))
    tiles = "".join(f'<rect x="{x}" y="128" width="20" height="22" fill="{c}" opacity=".85"/>'
                    for x, c in zip(range(0, 480, 20), ["#ff7ab0", "#7a5af8", "#8fd8ff", "#ffd66b"] * 6))
    ball = ('<path d="M240 0V12" stroke="#bbb" stroke-width="1"/><circle cx="240" cy="22" r="10" fill="#cfd6e6"/>'
            + "".join(f'<path d="M{230 + i * 4} 14V30" stroke="#9aa3b8" stroke-width=".6"/>' for i in range(6))
            + "".join(f'<path d="M230 {15 + i * 4}H250" stroke="#9aa3b8" stroke-width=".6"/>' for i in range(4)))
    sparks = "".join(_star(x, y, 1, "#fff", .9)
                     for x, y in ((210, 30), (272, 38), (190, 60), (296, 56), (360, 24), (120, 40), (60, 70), (430, 64)))
    notes = "".join(f'<text x="{x}" y="{y}" fill="{c}" font-size="12" font-family="sans-serif">♪</text>'
                    for x, y, c in ((130, 78, "#ff7ab0"), (330, 70, "#8fd8ff"), (260, 92, "#ffd66b"), (40, 50, "#b38cff")))
    garland = "".join(f'<path d="M{x} 2l7 0-3.5 8Z" fill="{c}"/>'
                      for x, c in zip(range(4, 480, 16), ["#ff7ab0", "#ffd66b", "#8fd8ff", "#7cc35b"] * 8))
    return _svg(f'''
<rect width="480" height="150" fill="url(#club)"/>{beams}{garland}{ball}{sparks}{notes}
<rect y="122" width="480" height="6" fill="#2d2150"/>{tiles}''',
                _vgrad("club", (0, "#140c2e"), (1, "#2b1854")))


# ------------------------------------------------------------------ more everyday
def bedroom():
    stars = "".join(f'<circle cx="{x}" cy="{y}" r=".9" fill="#fff"/>' for x, y in ((44, 40), (70, 30), (96, 50), (58, 62)))
    bulbs = "".join(f'<circle cx="{x}" cy="{10 + 6 * ((x - 240) / 240) ** 2}" r="2" fill="{c}" filter="url(#glow)"/>'
                    for x, c in zip(range(130, 470, 20), ["#ffd66b", "#ff9ec4", "#9fe0ff"] * 6))
    plush = "".join(f'<circle cx="{x}" cy="56" r="5" fill="{c}"/><circle cx="{x - 3}" cy="51" r="2" fill="{c}"/>'
                    f'<circle cx="{x + 3}" cy="51" r="2" fill="{c}"/>' for x, c in ((176, "#f7b67e"), (192, "#fff"), (208, "#f4c6d8")))
    planks = "".join(f'<path d="M0 {y}H480" stroke="#b58a62" stroke-width="1"/>' for y in (136, 144))
    return _svg(f'''
<rect width="480" height="150" fill="#efe6f5"/>
<path d="M0 10Q240 30 480 10" fill="none" stroke="#b9a8c9" stroke-width=".8"/>{bulbs}
<rect x="30" y="24" width="84" height="60" rx="4" fill="#2b2f5e" stroke="#fff" stroke-width="4"/>{stars}
<path d="M98 34a8 8 0 1 0 5 13a6 6 0 1 1-5-13Z" fill="#fff3c4"/>
<path d="M72 24V84M30 54H114" stroke="#fff" stroke-width="3"/>
<path d="M24 22h12v66h-12ZM108 22h12v66h-12Z" fill="#f4c6d8" opacity=".9"/>
<rect x="140" y="30" width="26" height="34" rx="2" fill="#fff" stroke="#d9c8e6" stroke-width="2"/><circle cx="153" cy="44" r="6" fill="#ffb3c8"/>
<rect x="166" y="60" width="54" height="4" rx="1" fill="#b58a62"/>{plush}
<rect x="238" y="96" width="46" height="32" rx="3" fill="#d8b892"/><rect x="236" y="92" width="50" height="5" rx="2" fill="#c9a27a"/>
<path d="M252 92l6-22h8l6 22Z" fill="#ffe08a" opacity=".5"/><rect x="258" y="66" width="10" height="6" rx="2" fill="#f2c94c"/>
<rect x="254" y="84" width="16" height="8" rx="1" fill="#7a5af8"/>
<rect x="330" y="78" width="140" height="10" rx="3" fill="#b58a62"/>
<rect x="332" y="86" width="136" height="28" rx="6" fill="#9fd0f0"/>
<path d="M332 96h136" stroke="#fff" stroke-width="2" stroke-dasharray="6 6" opacity=".7"/>
<rect x="430" y="72" width="34" height="16" rx="7" fill="#fff" stroke="#d9c8e6" stroke-width="1.5"/>
<rect x="326" y="62" width="10" height="66" rx="3" fill="#b58a62"/><rect x="464" y="72" width="8" height="56" rx="3" fill="#b58a62"/>
<rect y="128" width="480" height="22" fill="#d2ab84"/>{planks}
<ellipse cx="170" cy="138" rx="60" ry="7" fill="#f4c6d8" opacity=".85"/>''', _GLOW)


def rainy():
    drops = "".join(f'<path d="M{x} {y}l-3 9" stroke="#e3edf7" stroke-width="1.2" stroke-linecap="round" opacity=".7"/>'
                    for x in range(4, 500, 13) for y in range(((x * 7) % 23) - 30, 140, 26))
    rain = (f'<g>{drops}<animateTransform attributeName="transform" type="translate" '
            'from="0 -26" to="-8 0" dur="0.5s" repeatCount="indefinite"/></g>')
    blocks = "".join(f'<rect x="{x}" y="{100 - h}" width="{w}" height="{h}" fill="#7e90a8"/>'
                     for x, w, h in ((150, 40, 60), (194, 30, 44), (228, 44, 70), (276, 30, 40), (310, 50, 56), (420, 60, 66)))
    puddles = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="2" fill="#c9d6e3" opacity=".8"/>'
                      for x, y, r in ((60, 138, 16), (210, 144, 22), (340, 136, 14), (440, 142, 18)))
    return _svg(f'''
<rect width="480" height="150" fill="url(#rain)"/>
<ellipse cx="80" cy="18" rx="60" ry="12" fill="#a7b4c4"/><ellipse cx="300" cy="14" rx="80" ry="12" fill="#a7b4c4"/>
{blocks}
<rect x="10" y="40" width="120" height="88" fill="#d9c2a8"/>
<path d="M4 40h132l-8 14H12Z" fill="#3f8f7a"/><path d="M12 54h116" stroke="#2f6f5e" stroke-width="2"/>
<rect x="22" y="62" width="96" height="44" rx="2" fill="#ffe6a8"/><rect x="22" y="62" width="96" height="44" rx="2" fill="#fff6d6" opacity=".4"/>
<text x="70" y="88" fill="#a8743f" font-size="10" text-anchor="middle" font-family="sans-serif">ร้านกาแฟ</text>
<rect x="56" y="106" width="28" height="22" fill="#8a5a3e"/>
<path d="M380 128V44q0-8 8-8h10" stroke="#55606e" stroke-width="3" fill="none"/>
<circle cx="400" cy="40" r="5" fill="#ffe08a" filter="url(#glow)"/>
<rect y="104" width="480" height="24" fill="#8a97a8"/>
<rect y="128" width="480" height="22" fill="#9eabbb"/>{puddles}
{rain}''', _vgrad("rain", (0, "#7d8ea6"), (1, "#b9c6d4")) + _GLOW)


# ------------------------------------------------------------------ Thailand
def _prang(cx, base, h, w, c):
    tiers = "".join(f'<rect x="{cx - w * (1 - i / 7) / 2}" y="{base - h * i / 6 - h / 6}" '
                    f'width="{w * (1 - i / 7)}" height="{h / 6 + .5}" rx="1.5" fill="{c}"/>' for i in range(6))
    return tiers + f'<path d="M{cx - 2} {base - h}L{cx} {base - h - 14}L{cx + 2} {base - h}Z" fill="{c}"/>'


def wat_arun():
    refl = "".join(f'<path d="M{x} {y}h{l}" stroke="#ffe3b3" stroke-width="1" opacity=".55"/>'
                   for x, y, l in ((210, 110, 40), (250, 116, 30), (190, 120, 24), (300, 112, 26), (120, 114, 20)))
    birds = "".join(f'<path d="M{x} {y}q3-3 6 0q3-3 6 0" fill="none" stroke="#7a4a6a" stroke-width="1"/>'
                    for x, y in ((90, 26), (108, 18), (122, 30)))
    posts = "".join(f'<rect x="{x}" y="131" width="4" height="19" fill="#6a4430"/>' for x in range(16, 480, 60))
    return _svg(f'''
<rect width="480" height="150" fill="url(#dusk)"/>
<circle cx="330" cy="70" r="20" fill="#fff1c1" opacity=".85"/>{birds}
{_prang(240, 104, 72, 40, "#7a4a6a")}{_prang(198, 104, 36, 22, "#86536f")}{_prang(282, 104, 36, 22, "#86536f")}
{_prang(170, 104, 22, 13, "#93607a")}{_prang(310, 104, 22, 13, "#93607a")}
<rect y="104" width="480" height="46" fill="url(#river)"/>{refl}
<path d="M360 112h50l-5 6h-40Z" fill="#6a3f2e"/><path d="M406 112l8-6" stroke="#6a3f2e" stroke-width="2"/>
<rect y="124" width="480" height="5" fill="#8a5a3e"/><rect y="129" width="480" height="2" fill="#6a4430"/>{posts}''',
                _vgrad("dusk", (0, "#ff9a76"), (.55, "#ffc48c"), (1, "#ffe3b3"))
                + _vgrad("river", (0, "#f2a07b"), (1, "#b8708a")))


def market():
    def boat(x, y, fruit):
        piles = "".join(f'<circle cx="{x + 10 + i * 7}" cy="{y - 3 - (i % 2) * 2}" r="3.4" fill="{c}"/>'
                        for i, c in enumerate(fruit))
        return f'<path d="M{x} {y}h{14 + 7 * len(fruit)}l-6 6h-{6 + 7 * len(fruit)}Z" fill="#5a3a28"/>{piles}'
    hat = lambda x, y: f'<path d="M{x - 9} {y}L{x} {y - 6}L{x + 9} {y}Z" fill="#e8d29a" stroke="#c9ad6a" stroke-width=".8"/>'
    palms = "".join(
        f'<path d="M{x} 96q2-24-2-34" stroke="#8a6a3f" stroke-width="3" fill="none"/>'
        + "".join(f'<path d="M{x - 2} 62q{dx} {dy} {dx * 2} {dy + 8}" stroke="#4f9a4f" stroke-width="3" fill="none" stroke-linecap="round"/>'
                  for dx, dy in ((-9, -6), (9, -6), (-11, 2), (11, 2)))
        for x in (210, 330, 450))
    ripples = "".join(f'<path d="M{x} {y}q4-2 8 0" fill="none" stroke="#c8f0e8" stroke-width="1" opacity=".7"/>'
                      for x, y in ((40, 110), (170, 116), (260, 108), (400, 114)))
    return _svg(f'''
<rect width="480" height="150" fill="url(#day)"/>
<ellipse cx="80" cy="98" rx="110" ry="22" fill="#86c98a"/><ellipse cx="360" cy="100" rx="150" ry="22" fill="#7bbf80"/>
{palms}
<rect x="16" y="56" width="70" height="42" fill="#b07f52"/><path d="M8 58L51 34 94 58Z" fill="#8a4f3a"/>
<rect x="28" y="68" width="14" height="14" fill="#5a3a28"/><rect x="58" y="68" width="14" height="14" fill="#5a3a28"/>
<rect y="98" width="480" height="30" fill="#62b9a6"/>{ripples}
{boat(150, 112, ["#f6a623", "#f6d55c", "#7cc35b", "#e2554a"])}{hat(172, 106)}
{boat(300, 116, ["#e2554a", "#f6a623", "#9b6ad8", "#7cc35b"])}{hat(318, 110)}
<rect y="122" width="480" height="7" fill="#9a6a44"/><path d="M0 125H480" stroke="#7a4e30" stroke-width="1"/>
<rect y="129" width="480" height="21" fill="#4fa594"/>
{boat(390, 146, ["#f6d55c", "#e2554a"])}''',
                _vgrad("day", (0, "#aee3f5"), (1, "#e3f7fb")))


def beach():
    karst = ('<path d="M30 92q-2-40 14-46q12-2 14 20q4-26 18-20q10 8 6 46Z" fill="#6f9a7f"/>'
             '<path d="M36 52q8-10 18 0M64 50q8-8 16 0" stroke="#4f8a5f" stroke-width="5" fill="none" stroke-linecap="round"/>'
             '<path d="M300 92q2-30 14-34q12 4 12 34Z" fill="#7aa58a"/><path d="M304 62q8-8 16 0" stroke="#4f8a5f" stroke-width="5" fill="none" stroke-linecap="round"/>'
             '<path d="M150 92q4-22 14-24q10 4 10 24Z" fill="#86b195"/>')
    waves = "".join(f'<path d="M{x} {y}q5-3 10 0" fill="none" stroke="#fff" stroke-width="1.2" opacity=".75"/>'
                    for x, y in ((40, 100), (130, 106), (220, 98), (290, 108), (380, 102), (450, 110)))
    fronds = "".join(f'<path d="M420 44q{dx} {dy} {dx * 2} {dy + 10}" stroke="#3f9a55" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
                     for dx, dy in ((-12, -8), (12, -8), (-14, 2), (14, 2), (0, -12)))
    return _svg(f'''
<rect width="480" height="150" fill="url(#sky)"/>
<ellipse cx="110" cy="24" rx="20" ry="6" fill="#fff" opacity=".9"/><ellipse cx="124" cy="20" rx="12" ry="6" fill="#fff" opacity=".9"/>
<ellipse cx="290" cy="30" rx="16" ry="5" fill="#fff" opacity=".8"/>
<rect y="92" width="480" height="30" fill="url(#sea)"/>{karst}{waves}
<path d="M210 104h40l-5 5h-32Z" fill="#7a4a30"/><path d="M248 104l6-8" stroke="#7a4a30" stroke-width="2"/>
<path d="M253 96l2-4M251 97l-1-4" stroke="#ff6fa0" stroke-width="1.4"/>
<path d="M0 120Q240 112 480 120V150H0Z" fill="#f6dfa8"/>
<path d="M420 128q-6-40 2-84" stroke="#a5743f" stroke-width="4" fill="none"/>{fronds}
<path d="M340 128L360 100" stroke="#fff" stroke-width="1.4"/>
<path d="M342 104q18-14 36 0Z" fill="#ff8fb0"/>
<rect x="356" y="122" width="26" height="6" rx="2" fill="#7fd0ff"/>''',
                _vgrad("sky", (0, "#7fd2f2"), (1, "#d8f3fb")) + _vgrad("sea", (0, "#2fb8c4"), (1, "#86e3d8")))


def yaowarat():
    houses = ""
    for i, (x, w, h, c) in enumerate(((0, 60, 84, "#4a2f3f"), (60, 50, 96, "#3f2a40"), (110, 64, 78, "#523043"),
                                      (174, 56, 100, "#3a2638"), (230, 70, 86, "#4a2f3f"), (300, 54, 94, "#43293d"),
                                      (354, 66, 80, "#523043"), (420, 60, 98, "#3f2a40"))):
        houses += f'<rect x="{x}" y="{106 - h}" width="{w}" height="{h}" fill="{c}"/>'
        houses += "".join(f'<rect x="{x + 8 + c2 * 18}" y="{106 - h + 10 + r * 18}" width="10" height="10" fill="#ffcf7a" opacity=".55"/>'
                          for r in range(h // 22) for c2 in range(w // 20))
    signs = "".join(
        f'<rect x="{x}" y="{y}" width="12" height="{h}" rx="1" fill="#d62f2f" stroke="#ffd23f" stroke-width="1.2" filter="url(#glow)"/>'
        + "".join(f'<rect x="{x + 3}" y="{y + 4 + k * 9}" width="6" height="5" fill="#ffe8a3"/>' for k in range((h - 6) // 9))
        for x, y, h in ((48, 20, 46), (164, 14, 52), (292, 18, 48), (410, 12, 56)))
    lanterns = "".join(f'<ellipse cx="{x}" cy="{18 + (x % 3) * 4}" rx="5" ry="6" fill="#e8343a" filter="url(#glow)"/>'
                       for x in range(20, 480, 34))
    return _svg(f'''
<rect width="480" height="150" fill="url(#ynight)"/>
{houses}
<path d="M0 14Q240 34 480 14" fill="none" stroke="#6a4a5a" stroke-width=".8"/>{lanterns}
{signs}
<text x="236" y="78" fill="#ffd23f" font-size="16" font-weight="700" text-anchor="middle" font-family="sans-serif" filter="url(#glow)">เยาวราช</text>
<rect x="360" y="86" width="56" height="30" rx="3" fill="#c9c3bb"/><rect x="364" y="90" width="48" height="14" fill="#e6f4f8" opacity=".8"/>
<circle cx="372" cy="98" r="4" fill="#d4843f"/><circle cx="384" cy="98" r="4" fill="#e2b04f"/><circle cx="396" cy="98" r="4" fill="#d4843f"/>
<path d="M356 84q32-20 64 0Z" fill="#e8343a"/><path d="M388 70v14" stroke="#ccc"/>
<circle cx="368" cy="122" r="5" fill="#2a2232"/><circle cx="408" cy="122" r="5" fill="#2a2232"/>
<path d="M374 82q-3-6 0-10M384 80q-3-6 0-10" stroke="#ddd" stroke-width="1.2" fill="none" opacity=".7"/>
<rect y="106" width="480" height="22" fill="#5a4552"/><path d="M0 106H480" stroke="#7a6070" stroke-width="2"/>
<rect y="128" width="480" height="22" fill="#2a2232"/>''',
                _vgrad("ynight", (0, "#1a1030"), (1, "#3a1f3f")) + _GLOW)


def tuktuk():
    houses = "".join(f'<rect x="{x}" y="{104 - h}" width="{w}" height="{h}" fill="{c}"/>'
                     + "".join(f'<rect x="{x + 6 + k * 16}" y="{104 - h + 10}" width="10" height="12" fill="#fff" opacity=".6"/>'
                               for k in range(w // 16))
                     for x, w, h, c in ((0, 64, 58, "#f2c6a0"), (64, 52, 66, "#a8d8c8"), (116, 60, 54, "#f6e0a0"),
                                        (176, 56, 62, "#c8b8e8"), (232, 64, 56, "#f2b8b8"), (296, 52, 64, "#a8c8e8"),
                                        (348, 70, 58, "#f6d0a8"), (418, 62, 62, "#b8e0b0")))
    wires = "".join(f'<path d="M0 {y}Q240 {y + d} 480 {y + 4}" fill="none" stroke="#3a3a40" stroke-width=".9"/>'
                    for y, d in ((40, 18), (44, 12), (47, 22), (52, 8)))
    pillars = "".join(f'<rect x="{x}" y="28" width="8" height="76" fill="#b8bec8"/>' for x in (90, 300))
    return _svg(f'''
<rect width="480" height="150" fill="#bfe3f7"/>
<ellipse cx="80" cy="16" rx="40" ry="7" fill="#fff" opacity=".9"/>
{houses}{pillars}
<rect y="20" width="480" height="10" fill="#c8ced8"/><rect y="18" width="480" height="3" fill="#9aa2ae"/>
<rect x="150" y="8" width="90" height="12" rx="3" fill="#7cc35b"/><rect x="152" y="10" width="86" height="5" fill="#dff3d0"/>
{wires}

<rect y="104" width="480" height="24" fill="#d8d2c8"/><path d="M0 104H480" stroke="#bdb6aa" stroke-width="2"/>
<rect y="128" width="480" height="22" fill="#6b6f78"/>
<path d="M0 139H480" stroke="#fff" stroke-width="2" stroke-dasharray="16 12"/>
<g transform="translate(286 92)">
 <path d="M10 6h58v34H4V14Z" fill="#2f6fd6"/><path d="M0 4h74v6H0Z" fill="#1f4fa6"/>
 <path d="M14 14h22v14H14ZM40 14h22v14H40Z" fill="#cfe8ff" opacity=".8"/>
 <path d="M4 36h70" stroke="#ffd23f" stroke-width="3"/>
 <text x="40" y="34" fill="#fff" font-size="7" text-anchor="middle" font-family="sans-serif">ตุ๊กตุ๊ก</text>
 <circle cx="16" cy="42" r="6" fill="#22252b"/><circle cx="62" cy="42" r="6" fill="#22252b"/>
 <circle cx="16" cy="42" r="2" fill="#aaa"/><circle cx="62" cy="42" r="2" fill="#aaa"/>
</g>''')


# ------------------------------------------------------------------ festivals
def songkran():
    houses = "".join(f'<rect x="{x}" y="{106 - h}" width="{w}" height="{h}" fill="{c}"/>'
                     for x, w, h, c in ((0, 70, 60, "#ffe0b8"), (70, 60, 70, "#c8f0e0"), (130, 80, 56, "#ffd0e0"),
                                        (210, 60, 66, "#d8e0ff"), (270, 80, 58, "#fff0b0"), (350, 60, 68, "#c8f0e0"), (410, 70, 60, "#ffd0e0")))
    flags = "".join(f'<path d="M{x} 30l7 0-3.5 8Z" fill="{c}"/>'
                    for x, c in zip(range(4, 480, 14), ["#ff7ab0", "#ffd66b", "#4fc3f7", "#7cc35b"] * 9))
    splashes = "".join(f'<path d="M{x} 108q{d} -40 {d * 2} 0" fill="none" stroke="#4fc3f7" stroke-width="3" opacity=".55" stroke-linecap="round"/>'
                       for x, d in ((60, 20), (200, -16), (330, 22), (420, -18)))
    drops = "".join(f'<path d="M{x} {y}q-3 5 0 7q3-2 0-7Z" fill="#4fc3f7" opacity=".8"/>'
                    for x, y in ((70, 70), (90, 84), (190, 64), (176, 80), (344, 66), (366, 82), (414, 72), (400, 86)))
    puddles = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="2.2" fill="#8fd8ff" opacity=".7"/>'
                      for x, y, r in ((50, 140, 20), (180, 136, 14), (300, 144, 24), (430, 138, 16)))
    return _svg(f'''
<rect width="480" height="150" fill="#8fd8ff"/>
<circle cx="430" cy="22" r="12" fill="#fff3a3"/>
{houses}
<path d="M0 30Q240 44 480 30" fill="none" stroke="#999" stroke-width=".8"/>{flags}
<rect x="130" y="46" width="220" height="20" rx="4" fill="#ff7ab0"/>
<text x="240" y="60" fill="#fff" font-size="11" font-weight="700" text-anchor="middle" font-family="sans-serif">สุขสันต์วันสงกรานต์ 💦</text>
{splashes}{drops}
<rect x="440" y="110" width="20" height="18" rx="3" fill="#4f86d8"/><ellipse cx="450" cy="110" rx="10" ry="3" fill="#8fd8ff"/>
<rect y="106" width="480" height="22" fill="#e8e0d0"/>
<rect y="128" width="480" height="22" fill="#a9b7c2"/>{puddles}''')


def loykrathong():
    lanterns = "".join(
        f'<g transform="translate({x} {y})"><path d="M-4 0h8l-1.5 9h-5Z" fill="#ffb347" filter="url(#glow)"/>'
        f'<animateTransform attributeName="transform" type="translate" values="{x} {y};{x + 3} {y - 18};{x} {y}" '
        f'dur="{d}s" repeatCount="indefinite"/></g>'
        for x, y, d in ((60, 50, 9), (120, 30, 11), (170, 60, 8), (300, 40, 10), (350, 22, 12), (420, 56, 9), (250, 70, 13)))
    stars = "".join(f'<circle cx="{x}" cy="{y}" r=".9" fill="#fff" opacity=".8"/>'
                    for x, y in ((30, 14), (90, 24), (200, 10), (260, 34), (330, 12), (400, 30), (460, 16)))
    def krathong(x, y):
        return (f'<ellipse cx="{x}" cy="{y}" rx="11" ry="3.5" fill="#3f8f4f"/>'
                f'<path d="M{x - 8} {y - 1}q8-12 16 0Z" fill="#f7a8c8"/><path d="M{x - 4} {y - 2}q4-8 8 0Z" fill="#ffd0e0"/>'
                f'<rect x="{x - .8}" y="{y - 12}" width="1.6" height="7" fill="#fff6d6"/>'
                f'<circle cx="{x}" cy="{y - 13}" r="1.8" fill="#ffd66b" filter="url(#glow)"/>'
                f'<path d="M{x - 6} {y + 6}h12" stroke="#ffd66b" stroke-width="1" opacity=".4"/>')
    return _svg(f'''
<rect width="480" height="150" fill="url(#lknight)"/>{stars}
<circle cx="380" cy="34" r="16" fill="#fff6d6" filter="url(#glow)"/>
{lanterns}
<path d="M0 98Q120 88 240 96T480 94V104H0Z" fill="#1a1f4a"/>
<rect y="100" width="480" height="24" fill="#24306a"/>
<path d="M376 104v16" stroke="#fff6d6" stroke-width="3" opacity=".25"/>
{krathong(80, 112)}{krathong(190, 116)}{krathong(300, 110)}{krathong(430, 117)}
<rect y="124" width="480" height="5" fill="#6a6a8a"/>
<rect y="128" width="480" height="22" fill="#3a3a5a"/>''',
                _vgrad("lknight", (0, "#0c1238"), (1, "#2a2a6a")) + _GLOW)


# ------------------------------------------------------------------ party (more)
def bar():
    stars = "".join(f'<circle cx="{x}" cy="{y}" r=".9" fill="#fff" opacity=".8"/>'
                    for x, y in ((20, 14), (80, 30), (150, 10), (220, 22), (282, 8), (330, 18), (400, 30), (460, 12)))
    towers = ""
    for x, w, h in ((0, 26, 50), (24, 18, 70), (40, 30, 44), (68, 16, 84), (82, 28, 58), (112, 22, 36),
                    (300, 20, 62), (318, 26, 48), (342, 28, 72), (370, 20, 40), (392, 30, 66), (424, 24, 52), (448, 32, 76)):
        towers += f'<rect x="{x}" y="{108 - h}" width="{w}" height="{h}" fill="#28214d"/>'
        towers += "".join(f'<rect x="{x + 4 + c * 6}" y="{108 - h + 6 + r * 8}" width="2.5" height="3" fill="#ffd66b" '
                          f'opacity="{.35 + ((x + r + c) % 3) * .2}"/>'
                          for r in range(h // 10) for c in range(w // 7))
    bulbs = "".join(f'<circle cx="{x}" cy="{20 - 10 * ((x - 240) / 240) ** 2}" r="2.2" fill="{c}" filter="url(#glow)"/>'
                    for x, c in zip(range(10, 480, 22), ["#ffd66b", "#ff8fb0", "#8fd8ff"] * 8))
    stools = "".join(f'<rect x="{x - 1.5}" y="112" width="3" height="16" fill="#3a2f55"/>'
                     f'<ellipse cx="{x}" cy="111" rx="8" ry="2.5" fill="#e05a7a"/>' for x in (150, 300))
    return _svg(f'''
<rect width="480" height="150" fill="url(#night)"/>{stars}
<path d="M246 22a10 10 0 1 0 6 18a8 8 0 1 1-6-18Z" fill="#fff3c4"/>
{towers}
<path d="M220 108V24l4-10 4 10V108Z" fill="#332a63"/>
<path d="M0 10Q240 30 480 10" fill="none" stroke="#5a4f80" stroke-width=".8"/>{bulbs}
<text x="160" y="96" fill="#ff7ab0" font-size="15" font-family="sans-serif" font-weight="700" filter="url(#glow)">บาร์ ✦</text>
<rect y="98" width="480" height="10" fill="#8a5a3e"/>
<path d="M390 84l8 8 8-8Z" fill="#8fd8ff" opacity=".85"/><path d="M398 92v6M394 98h8" stroke="#cfe" stroke-width="1.4"/>
<rect x="416" y="86" width="8" height="12" rx="1.5" fill="#ffcf5c" opacity=".9"/>
<rect y="108" width="480" height="20" fill="#5b3a2e"/>
{stools}
<rect y="128" width="480" height="22" fill="#221b3a"/>''',
                _vgrad("night", (0, "#17133a"), (1, "#3b2a6b")) + _GLOW)


# id -> label, category, builder, top fill colour, floor colour, group size
SCENES = {
    "office": ("Office", "everyday", office, "#eaf0f7", "#b9c4d8", 1),
    "cafe": ("Café", "everyday", cafe, "#f7e8d4", "#c8935f", 1),
    "bedroom": ("Bedroom", "everyday", bedroom, "#efe6f5", "#d2ab84", 1),
    "rainy": ("Rainy day", "everyday", rainy, "#7d8ea6", "#9eabbb", 1),
    "wat_arun": ("Wat Arun", "thailand", wat_arun, "#ff9a76", "#8a5a3e", 1),
    "market": ("Floating market", "thailand", market, "#aee3f5", "#4fa594", 1),
    "beach": ("Krabi beach", "thailand", beach, "#7fd2f2", "#f6dfa8", 1),
    "yaowarat": ("Yaowarat", "thailand", yaowarat, "#1a1030", "#2a2232", 1),
    "tuktuk": ("Tuk-tuk street", "thailand", tuktuk, "#bfe3f7", "#6b6f78", 1),
    "songkran": ("Songkran", "festivals", songkran, "#8fd8ff", "#a9b7c2", 3),
    "loykrathong": ("Loy Krathong", "festivals", loykrathong, "#0c1238", "#3a3a5a", 2),
    "stage": ("SAMTUABAHT Fanmeet", "party", stage, "#2a1c3f", "#130d22", 3),
    "party": ("Dance party", "party", party, "#140c2e", "#2b1854", 3),
    "bar": ("Rooftop bar", "party", bar, "#17133a", "#221b3a", 2),
}

# Activities a lone buddy prefers in each scene (group scenes dance instead).
SCENE_ACTIVITIES = {
    "office": ["work", "coffee", "phone", "read", "plant"],
    "cafe": ["coffee", "bubbletea", "read", "phone", "music", "chicken"],
    "bedroom": ["sleep", "read", "game", "phone", "tv", "music"],
    "rainy": ["coffee", "phone", "music"],
    "wat_arun": ["phone", "read"],
    "market": ["noodles", "bubbletea", "chicken"],
    "beach": ["sleep", "music", "bubbletea"],
    "yaowarat": ["noodles", "chicken", "bubbletea"],
    "tuktuk": ["phone", "music"],
}

# How a group scene moves together: dance, stage show, splash fight or a calm hangout.
GROUP_STYLE = {"party": "dance", "stage": "stage", "songkran": "splash",
               "loykrathong": "hangout", "bar": "hangout"}
