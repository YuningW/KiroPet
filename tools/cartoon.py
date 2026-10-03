"""Cartoon (vector) versions of the KiroPet mascots, written as SVG.

Every mascot shares one layout on a 120 x 136 canvas (viewBox 0 -14 120 136):
a big wide head, two front paws, a small body and two feet. Parts the
extension animates carry ids:

    #eyes-open / #eyes-closed   blink (and sleep)
    #foot-l / #foot-r           stepping while walking

Run tools/export_web.py to write them into the extension.
"""

INK = "#2a2234"


# ------------------------------------------------------------- helpers
def heart(cx, cy, s, fill):
    return (f'<path transform="translate({cx} {cy}) scale({s})" fill="{fill}" '
            'd="M0 4C-4 1-6.5-2-4-4C-2.4-5.2-.7-4.4 0-3.2C.7-4.4 2.4-5.2 4-4'
            'C6.5-2 4 1 0 4Z"/>')


def sparkle(cx, cy, s, fill):
    return (f'<path transform="translate({cx} {cy}) scale({s})" fill="{fill}" '
            'd="M0-4L1 -1 4 0 1 1 0 4-1 1-4 0-1-1Z"/>')


def feet(fill, stroke, y=114, xs=(46, 74), rx=10, ry=6.5):
    return "".join(
        f'<ellipse id="foot-{side}" cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        for side, x in zip("lr", xs))


def paws(fill, stroke, y=99, xs=(31, 89), rx=13, ry=10.5):
    return "".join(
        f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="2"/>' for x in xs)


def blush(y, color="#f06c6c", xs=(28, 33, 84.4, 89.4)):
    return "".join(f'<rect x="{x}" y="{y}" width="2.6" height="6.5" rx="1.3" '
                   f'fill="{color}"/>' for x in xs)


def eyes(xs=(44, 76), y=65, rx=8, ry=9.2, iris=INK, shine=True, extra=""):
    """Big glossy anime eyes plus the matching closed (blink) arcs."""
    opened = "".join(
        f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{iris}"/>'
        for x in xs)
    if shine:
        opened += "".join(
            f'<circle cx="{x - rx * .4}" cy="{y - ry * .43}" r="{rx * .42}" fill="#fff"/>'
            f'<circle cx="{x + rx * .4}" cy="{y + ry * .48}" r="{rx * .2}" fill="#fff"/>'
            for x in xs)
    closed = "".join(
        f'<path d="M{x - rx} {y + 1}Q{x} {y + 7} {x + rx} {y + 1}"/>' for x in xs)
    return (f'<g id="eyes-open">{opened}{extra}</g>'
            f'<g id="eyes-closed" visibility="hidden" fill="none" stroke="{iris}" '
            f'stroke-width="2.8" stroke-linecap="round">{closed}</g>')


def cat_mouth(y=81, color="#7a4a3a", tongue="#f2899a"):
    t = f'<path d="M57 {y + 3}q3 5 6 0Z" fill="{tongue}"/>' if tongue else ""
    return (t + f'<path d="M52 {y}Q56 {y + 4} 60 {y}Q64 {y + 4} 68 {y}" '
            f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/>')


def grad(gid, light, dark):
    return (f'<radialGradient id="{gid}" cx="45%" cy="35%" r="72%">'
            f'<stop offset="0" stop-color="{light}"/>'
            f'<stop offset="1" stop-color="{dark}"/></radialGradient>')


def svg(defs, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -14 120 136">'
            f'<defs>{defs}</defs>{body}</svg>\n')


# ------------------------------------------------------------- mascots
def muvmuv():
    hood, hol, w, wol = "url(#mm-hood)", "#df9458", "url(#mm-fluff)", "#e2d7c8"
    return svg(grad("mm-hood", "#fcc895", "#f3a768") + grad("mm-fluff", "#fff", "#f4eee6"), f'''
{feet(w, wol)}
<ellipse cx="60" cy="98" rx="27" ry="20" fill="{w}" stroke="{wol}" stroke-width="2"/>
<path d="M16 46L20 8Q22 2 28 6L50 26Z" fill="{hood}" stroke="{hol}" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M104 46L100 8Q98 2 92 6L70 26Z" fill="{hood}" stroke="{hol}" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M23 36L25 14 39 27Z" fill="#fbd9b8"/><path d="M97 36L95 14 81 27Z" fill="#fbd9b8"/>
<ellipse cx="60" cy="60" rx="51" ry="41" fill="{hood}" stroke="{hol}" stroke-width="2.5"/>
<g fill="#ee7448">
 <rect x="11" y="56" width="13" height="4.5" rx="2.2"/><rect x="12" y="66" width="11" height="4.5" rx="2.2"/>
 <rect x="96" y="56" width="13" height="4.5" rx="2.2"/><rect x="97" y="66" width="11" height="4.5" rx="2.2"/>
 <rect x="44" y="22" width="4" height="9" rx="2"/><rect x="72" y="22" width="4" height="9" rx="2"/>
</g>
{sparkle(29, 46, 1, "#9edcc0")}{heart(93, 44, .7, "#f2686a")}
<circle cx="86" cy="32" r="1.6" fill="#fff6ec"/><circle cx="34" cy="30" r="1.4" fill="#fff6ec"/>
<ellipse cx="60" cy="68" rx="35" ry="28" fill="{w}"/>
{eyes()}
{heart(60, 75, .95, "#7a4a3a")}
{cat_mouth()}
{blush(75)}
<path d="M42 93Q60 99 78 93L62 110Q60 112 58 110Z" fill="#f7a96a" stroke="{hol}" stroke-width="2" stroke-linejoin="round"/>
<circle cx="60" cy="96" r="3.5" fill="#f39a55"/>
{paws(w, wol)}
<g transform="rotate(10 66 10)">
 <path d="M70-3L74-13" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>
 <rect x="55" y="-1" width="21" height="25" rx="3" fill="#f9c0cf" stroke="#e397ad" stroke-width="2"/>
 <path d="M55 3L58-5H73L76 3Z" fill="#a9dcc4" stroke="#7fc3a6" stroke-width="1.6" stroke-linejoin="round"/>
 {heart(65.5, 13.5, .95, "#fff")}
</g>''')


def lunar():
    w, ol, bk = "url(#lu-white)", "#cfd5dc", "#26292f"
    ylo, yld, blue, yel = "#f8d85e", "#dcb23a", "#6cc3d8", "#f3e36a"
    petals = "".join(
        f'<circle cx="{96 + 6.5 * c}" cy="{22 + 6.5 * s}" r="5" fill="{blue}"/>'
        for c, s in ((1, 0), (.5, .87), (-.5, .87), (-1, 0), (-.5, -.87), (.5, -.87)))
    patches = (f'<ellipse cx="42" cy="64" rx="15" ry="12.5" fill="{bk}" transform="rotate(-25 42 64)"/>'
               f'<ellipse cx="78" cy="64" rx="15" ry="12.5" fill="{bk}" transform="rotate(25 78 64)"/>')
    heart_eyes = (f'<circle cx="43" cy="64" r="7.5" fill="{bk}" stroke="#fff" stroke-width="2.2"/>'
                  f'<circle cx="77" cy="64" r="7.5" fill="{bk}" stroke="#fff" stroke-width="2.2"/>'
                  + heart(43, 65, .85, blue) + heart(77, 65, .85, yel)
                  + sparkle(39.5, 60.5, .55, "#fff") + sparkle(73.5, 60.5, .55, "#fff"))
    closed = ('<g id="eyes-closed" visibility="hidden" fill="none" stroke="#fff" '
              'stroke-width="2.6" stroke-linecap="round">'
              '<path d="M36 65Q43 71 50 65"/><path d="M70 65Q77 71 84 65"/></g>')
    return svg(grad("lu-white", "#ffffff", "#eef1f5"), f'''
<ellipse id="foot-l" cx="45" cy="115" rx="12" ry="6" fill="{ylo}" stroke="{yld}" stroke-width="2"/>
<ellipse id="foot-r" cx="75" cy="115" rx="12" ry="6" fill="{ylo}" stroke="{yld}" stroke-width="2"/>
<ellipse cx="60" cy="98" rx="27" ry="20" fill="{w}" stroke="{ol}" stroke-width="2"/>
<circle cx="22" cy="24" r="15" fill="{bk}"/><circle cx="98" cy="24" r="15" fill="{bk}"/>
<ellipse cx="60" cy="60" rx="51" ry="41" fill="{w}" stroke="{ol}" stroke-width="2.5"/>
{petals}<circle cx="96" cy="22" r="4.2" fill="{yel}"/>
{heart(19, 20, .8, "#f05a5a")}
{heart(51, 19, 1.1, blue)}{heart(62, 13, 1.4, yel)}
{sparkle(32, 44, .8, yel)}{sparkle(88, 47, .7, blue)}
{patches}
<g id="eyes-open">{heart_eyes}</g>{closed}
<ellipse cx="60" cy="80" rx="13" ry="7.5" fill="{ylo}" stroke="{yld}" stroke-width="2"/>
<path d="M50 81Q60 85 70 81" fill="none" stroke="{yld}" stroke-width="1.6" stroke-linecap="round"/>
{blush(83, xs=(26, 31, 86.4, 91.4))}
{paws(bk, bk)}''')


def any_():
    cr, ol, hair, skin = "url(#an-cream)", "#e4dcb8", "#1f1a22", "#fbeee6"
    return svg(grad("an-cream", "#fffef2", "#f8f0cf"), f'''
<ellipse cx="12" cy="66" rx="13" ry="23" fill="#a8e0ea" transform="rotate(-12 12 66)"/>
<ellipse cx="108" cy="66" rx="13" ry="23" fill="#a8e0ea" transform="rotate(12 108 66)"/>
<ellipse cx="14" cy="72" rx="7" ry="12" fill="#f6c4d4"/><ellipse cx="106" cy="72" rx="7" ry="12" fill="#f6c4d4"/>
<ellipse id="foot-l" cx="46" cy="114" rx="10" ry="6.5" fill="#f2a8bc" stroke="#d87f98" stroke-width="2"/>
<ellipse id="foot-r" cx="74" cy="114" rx="10" ry="6.5" fill="#f6a36a" stroke="#d97f45" stroke-width="2"/>
<ellipse cx="60" cy="98" rx="27" ry="20" fill="{cr}" stroke="{ol}" stroke-width="2"/>
<rect x="26" y="-10" width="22" height="52" rx="11" fill="{cr}" stroke="{ol}" stroke-width="2.5" transform="rotate(-8 37 30)"/>
<rect x="72" y="-10" width="22" height="52" rx="11" fill="{cr}" stroke="{ol}" stroke-width="2.5" transform="rotate(8 83 30)"/>
<rect x="31" y="-6" width="12" height="16" rx="6" fill="#f4c6d8" transform="rotate(-8 37 30)"/>
<rect x="77" y="-6" width="12" height="16" rx="6" fill="#f4c6d8" transform="rotate(8 83 30)"/>
<ellipse cx="60" cy="60" rx="50" ry="41" fill="{cr}" stroke="{ol}" stroke-width="2.5"/>
<ellipse cx="60" cy="66" rx="38" ry="31" fill="{hair}"/>
<ellipse cx="60" cy="80" rx="27" ry="16" fill="{skin}"/>
<path d="M32 74L38 62 44 72 50 59 57 70 63 58 69 69 75 60 80 71 88 66 86 55H34Z" fill="{hair}"/>
<rect x="68" y="42" width="13" height="5" rx="2.5" fill="#f08a5d" transform="rotate(-20 74 44)"/>
<rect x="76" y="48" width="13" height="5" rx="2.5" fill="#e86aa0" transform="rotate(-20 82 50)"/>
<g transform="translate(60 22)">
 <ellipse cx="-6" cy="-3" rx="6" ry="5" fill="#f3a0c2"/><ellipse cx="6" cy="-3" rx="6" ry="5" fill="#f3a0c2"/>
 <ellipse cx="-5" cy="4" rx="4.5" ry="3.5" fill="#f7c2d6"/><ellipse cx="5" cy="4" rx="4.5" ry="3.5" fill="#f7c2d6"/>
 <rect x="-1.4" y="-6" width="2.8" height="13" rx="1.4" fill="#b0507a"/>
</g>
{sparkle(30, 34, .8, "#f08a5d")}{heart(91, 34, .6, "#a8e0ea")}{sparkle(84, 54, .6, "#fff")}
{eyes(xs=(48, 72), y=80, rx=5.4, ry=6.4, iris=hair)}
<ellipse cx="60" cy="87" rx="2" ry="1.4" fill="#f2a0b0"/>
{blush(86, xs=(37, 41, 77.4, 81.4))}
{paws(cr, ol)}''')


def jewel():
    cr, col, ear, earin = "url(#jw-cream)", "#e6d4bf", "#97282c", "#f4b9b4"
    brown, lash, red = "#6b3420", "#3e2216", "#d4212a"
    eyes_open = "".join(
        f'<ellipse cx="{x}" cy="66" rx="8.5" ry="9.5" fill="{brown}"/>'
        f'<ellipse cx="{x}" cy="68" rx="5" ry="5.5" fill="#4a2214"/>'
        + heart(x - 2.5, 63, .75, "#fff")
        + f'<circle cx="{x + 3.5}" cy="71" r="1.5" fill="#fff"/>' for x in (43, 77))
    lashes = ('<g fill="none" stroke-linecap="round">'
              '<path d="M33 58Q43 52 53 58" stroke="#f7c0c0" stroke-width="3"/>'
              '<path d="M67 58Q77 52 87 58" stroke="#f7c0c0" stroke-width="3"/>'
              f'<path d="M34 60Q43 54 52 59M34 60L30 57" stroke="{lash}" stroke-width="2"/>'
              f'<path d="M68 59Q77 54 86 60M86 60L90 57" stroke="{lash}" stroke-width="2"/></g>')
    closed = (f'<g id="eyes-closed" visibility="hidden" fill="none" stroke="{lash}" '
              'stroke-width="2.6" stroke-linecap="round">'
              '<path d="M34 66Q43 73 52 66M34 66L30 64"/><path d="M68 66Q77 73 86 66M86 66L90 64"/></g>')
    fluff = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{cr}"/>'
                    for x, y in ((12, 72), (14, 84), (108, 72), (106, 84)))
    return svg(grad("jw-cream", "#fffdf8", "#fbeedd"), f'''
{feet(cr, col)}
<ellipse cx="60" cy="98" rx="27" ry="20" fill="{cr}" stroke="{col}" stroke-width="2"/>
<path d="M14 50L18 0Q20-6 26-2L50 26Z" fill="{ear}" stroke="#7a1c20" stroke-width="2" stroke-linejoin="round"/>
<path d="M106 50L102 0Q100-6 94-2L70 26Z" fill="{ear}" stroke="#7a1c20" stroke-width="2" stroke-linejoin="round"/>
<path d="M22 40L24 10 40 28Z" fill="{earin}"/><path d="M98 40L96 10 80 28Z" fill="{earin}"/>
<circle cx="18" cy="16" r="1.6" fill="#fff"/><circle cx="102" cy="20" r="1.6" fill="#fff"/>
{fluff}
<ellipse cx="60" cy="62" rx="50" ry="40" fill="{cr}" stroke="{col}" stroke-width="2"/>
<path d="M60 28C54 18 42 20 46 28C50 34 58 30 60 28C62 26 70 18 76 24C80 30 68 34 60 28" fill="none" stroke="{ear}" stroke-width="2.2" stroke-linecap="round"/>
<path d="M60 28C64 22 74 20 74 26" fill="none" stroke="#f4a4a8" stroke-width="2.2" stroke-linecap="round"/>
{heart(60, 17, .6, "#c0303a")}
<g fill="none" stroke="#e48c80" stroke-width="2" stroke-linecap="round">
 <path d="M48 46Q46 40 50 36"/><path d="M53 46Q51 40 55 36"/><path d="M58 46Q56 40 60 36"/>
</g>
<circle cx="66" cy="42" r="5" fill="#f4a4a8"/>
{sparkle(28, 50, .9, "#f6d24a")}{heart(92, 48, .6, red)}{heart(36, 38, .45, red)}
{lashes}
<g id="eyes-open">{eyes_open}</g>{closed}
<path d="M58 79H62L60 81.5Z" fill="#e05060"/>
<path d="M55 84Q57.5 87 60 84Q62.5 87 65 84" fill="none" stroke="{brown}" stroke-width="1.8" stroke-linecap="round"/>
{blush(80, color="#e8545a", xs=(25, 30, 87.4, 92.4))}
<path d="M30 92Q60 102 90 92L90 97Q60 107 30 97Z" fill="{red}"/>
<path d="M60 99L46 92 46 108ZM60 99L74 92 74 108Z" fill="{red}" stroke="#a8141c" stroke-width="1.5" stroke-linejoin="round"/>
<circle cx="60" cy="99" r="4" fill="#a8141c"/>
{paws(cr, col)}''')


def vimmy():
    cr, col, br, brd = "url(#vm-cream)", "#e0c39c", "#a86b3d", "#7e4c26"
    bee, ink = "#f6d33c", "#2a2420"
    curls = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="none" stroke="{brd}" stroke-width="1.6"/>'
                    for x, y in ((12, 58), (16, 76), (10, 92), (108, 58), (104, 76), (110, 92)))
    flower = "".join(
        f'<circle cx="{x + 3.2 * c}" cy="{63 + 3.2 * s}" r="1.9" fill="#fff"/>'
        for x in (43, 77)
        for c, s in ((0, -1), (.95, -.31), (.59, .81), (-.59, .81), (-.95, -.31)))
    flower += '<circle cx="43" cy="63" r="1.4" fill="#fff"/><circle cx="77" cy="63" r="1.4" fill="#fff"/>'
    return svg(grad("vm-cream", "#fff8ec", "#f6e2c4"), f'''
{feet("#eef0f6", "#c8ccd8")}
<ellipse cx="60" cy="98" rx="27" ry="20" fill="{bee}" stroke="#d8b42a" stroke-width="2"/>
<path d="M36 94H84M34 104H86" stroke="{ink}" stroke-width="5"/>
<ellipse cx="14" cy="76" rx="16" ry="30" fill="{br}" stroke="{brd}" stroke-width="2"/>
<ellipse cx="106" cy="76" rx="16" ry="30" fill="{br}" stroke="{brd}" stroke-width="2"/>
{curls}
<ellipse cx="60" cy="60" rx="47" ry="41" fill="{cr}" stroke="{col}" stroke-width="2"/>
<ellipse cx="40" cy="62" rx="17" ry="20" fill="{br}"/><ellipse cx="80" cy="62" rx="17" ry="20" fill="{br}"/>
<path d="M53 40Q50 32 56 32Q60 32 60 38Q60 32 64 32Q70 32 67 40" fill="none" stroke="#c9a27a" stroke-width="2" stroke-linecap="round"/>
<g fill="none" stroke="{ink}" stroke-width="3.2" stroke-linecap="round">
 <path d="M44 28Q36 14 40 2"/><path d="M76 28Q84 14 80 2"/>
</g>
<circle cx="40" cy="2" r="3.6" fill="{ink}"/><circle cx="80" cy="2" r="3.6" fill="{ink}"/>
<ellipse cx="55" cy="10" rx="6" ry="4.5" fill="#d8f0ff" stroke="#a9cde6" stroke-width="1.2"/>
<ellipse cx="64" cy="9" rx="6" ry="4.5" fill="#d8f0ff" stroke="#a9cde6" stroke-width="1.2"/>
<ellipse cx="60" cy="19" rx="11" ry="8" fill="{bee}" stroke="#d8b42a" stroke-width="1.6"/>
<path d="M59 11.5V26.5M65 13V25" stroke="{ink}" stroke-width="2.4"/>
<circle cx="53" cy="18" r="1.4" fill="{ink}"/>
{sparkle(24, 40, .9, "#f6d24a")}{heart(97, 38, .65, "#e8484a")}{sparkle(100, 52, .6, "#fff")}
{eyes(xs=(43, 77), y=64, rx=8.5, ry=9.5, iris="#161214", shine=False, extra=flower)}
<ellipse cx="60" cy="76" rx="4.4" ry="3.2" fill="#4a2a1a"/>
<path d="M54 81Q57 84 60 80Q63 84 66 81" fill="none" stroke="#4a2a1a" stroke-width="1.8" stroke-linecap="round"/>
{blush(76, color="#ee6a6a", xs=(30, 35, 82.4, 87.4))}
{paws(cr, col)}''')


def wesley():
    bl, bld, tan, tand = "url(#ws-blue)", "#2c5aa8", "#e2bd93", "#c39466"
    face, brown = "#fbead6", "#6b3f2a"
    return svg(grad("ws-blue", "#6f9fe6", "#3f74c8"), f'''
<ellipse id="foot-l" cx="45" cy="117" rx="11" ry="6" fill="#d93a3a" stroke="#a82828" stroke-width="2"/>
<ellipse id="foot-r" cx="75" cy="117" rx="11" ry="6" fill="#d93a3a" stroke="#a82828" stroke-width="2"/>
<ellipse cx="60" cy="64" rx="52" ry="52" fill="{bl}" stroke="{bld}" stroke-width="2.5"/>
<ellipse cx="60" cy="92" rx="32" ry="22" fill="#fff"/>
<path d="M49 18L52 10 55 16 58 8 61 16 64 9 67 16 70 10 72 18Z" fill="#e23b3b" stroke="#b02a2a" stroke-width="1.4" stroke-linejoin="round"/>
<g stroke="{bld}" stroke-width="2.2" stroke-linecap="round">
 <path d="M30 26L33 31"/><path d="M38 20L40 25"/><path d="M90 26L87 31"/><path d="M82 20L80 25"/>
</g>
<ellipse cx="60" cy="58" rx="33" ry="27" fill="{face}"/>
<ellipse cx="44" cy="54" rx="13" ry="11" fill="{tan}"/><ellipse cx="76" cy="54" rx="13" ry="11" fill="{tan}"/>
<ellipse cx="20" cy="60" rx="11" ry="21" fill="{tan}" stroke="{tand}" stroke-width="2" transform="rotate(12 20 60)"/>
<ellipse cx="100" cy="60" rx="11" ry="21" fill="{tan}" stroke="{tand}" stroke-width="2" transform="rotate(-12 100 60)"/>
<circle cx="24" cy="40" r="7" fill="{tan}" stroke="{tand}" stroke-width="1.6"/>
<circle cx="96" cy="40" r="7" fill="{tan}" stroke="{tand}" stroke-width="1.6"/>
{heart(28, 24, .8, "#e23b3b")}{sparkle(94, 26, .9, "#fff")}{heart(102, 34, .55, "#9cc8f5")}
{eyes(xs=(45, 75), y=56, rx=7.5, ry=8.5, iris=brown)}
<ellipse cx="60" cy="67" rx="4" ry="3" fill="{brown}"/>
<path d="M54 71Q57 74 60 71Q63 74 66 71" fill="none" stroke="{brown}" stroke-width="1.8" stroke-linecap="round"/>
<path d="M57 73q3 6 6 0Z" fill="#f08aa0"/>
{blush(66, color="#e8545a", xs=(31, 36, 81.4, 86.4))}
<ellipse cx="11" cy="92" rx="9" ry="12" fill="{bl}" stroke="{bld}" stroke-width="2" transform="rotate(-20 11 92)"/>
<ellipse cx="109" cy="92" rx="9" ry="12" fill="{bl}" stroke="{bld}" stroke-width="2" transform="rotate(20 109 92)"/>''')


def goldie(outfit):
    fur, ol, ear = "url(#gd-fur)", "#c9a874", "#dcbd8a"
    if outfit == "red":
        shirt = ('<ellipse cx="60" cy="98" rx="28" ry="20" fill="#d6403a" stroke="#b12f2a" stroke-width="2"/>'
                 '<path d="M50 99L53 92 56 99M51 97H55M58 92L60 99 62 95 64 99 66 92" fill="none" '
                 'stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        shirt = ('<ellipse cx="60" cy="98" rx="28" ry="20" fill="#8a5a33" stroke="#6f4526" stroke-width="2"/>'
                 '<rect x="52" y="96" width="16" height="11" rx="3" fill="#caa877"/>'
                 '<path d="M44 82V96M76 82V96" stroke="#6f4526" stroke-width="4" stroke-linecap="round"/>'
                 '<circle cx="44" cy="94" r="2" fill="#f2d28a"/><circle cx="76" cy="94" r="2" fill="#f2d28a"/>')
    return svg(grad("gd-fur", "#f8e6c4", "#e6c792"), f'''
{feet(fur, ol)}
{shirt}
<ellipse cx="14" cy="72" rx="14" ry="30" fill="{ear}" stroke="{ol}" stroke-width="2" transform="rotate(10 14 72)"/>
<ellipse cx="106" cy="72" rx="14" ry="30" fill="{ear}" stroke="{ol}" stroke-width="2" transform="rotate(-10 106 72)"/>
<ellipse cx="60" cy="60" rx="46" ry="40" fill="{fur}" stroke="{ol}" stroke-width="2"/>
<path d="M48 24Q50 14 56 20Q60 10 64 20Q70 14 72 24" fill="{fur}" stroke="{ol}" stroke-width="2" stroke-linejoin="round"/>
{eyes(xs=(42, 78), y=62, rx=7.5, ry=8.5)}
<ellipse cx="60" cy="74" rx="6" ry="4.4" fill="#5b4a3a"/>
<path d="M54 80Q57 84 60 80Q63 84 66 80" fill="none" stroke="#5b4a3a" stroke-width="1.8" stroke-linecap="round"/>
<ellipse cx="30" cy="76" rx="6" ry="3.5" fill="#f0a27a" opacity=".75"/>
<ellipse cx="90" cy="76" rx="6" ry="3.5" fill="#f0a27a" opacity=".75"/>
{paws(fur, ol)}''')


def lolo():
    fur, ol, cr, pk = "url(#lo-fur)", "#c9822f", "#fff3e6", "#ff8fb0"
    seeds = "".join(f'<ellipse cx="{x}" cy="{y}" rx="1" ry="1.5" fill="#ffe08a"/>'
                    for x, y in ((55, 6), (61, 4), (66, 8), (58, 12), (64, 14)))
    stripes = "".join(f'<path d="M{x} {y}h{d}" stroke="{ol}" stroke-width="3" stroke-linecap="round"/>'
                      for x, y, d in ((10, 60, 10), (11, 69, 8), (110, 60, -10), (109, 69, -8)))
    return svg(grad("lo-fur", "#f8cc94", "#eba762"), f'''
{feet(cr, ol)}
<ellipse cx="60" cy="98" rx="27" ry="20" fill="{fur}" stroke="{ol}" stroke-width="2"/>
<ellipse cx="60" cy="101" rx="15" ry="13" fill="{cr}"/>
<path d="M14 48L20 8Q22 2 28 6L50 28Z" fill="{fur}" stroke="{ol}" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M106 48L100 8Q98 2 92 6L70 28Z" fill="{fur}" stroke="{ol}" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M22 38L24 14 38 28Z" fill="{pk}"/><path d="M98 38L96 14 82 28Z" fill="{pk}"/>
<ellipse cx="60" cy="60" rx="50" ry="41" fill="{fur}" stroke="{ol}" stroke-width="2.5"/>
{stripes}
<path d="M60 22C46 16 48-2 60 2C72-2 74 16 60 22Z" fill="#e23b3b" stroke="#b52c2c" stroke-width="1.6"/>
{seeds}
<path d="M52 2Q56-6 60-1Q64-6 68 2Q60 5 52 2Z" fill="#4bbf5a"/>
<ellipse cx="60" cy="76" rx="24" ry="17" fill="{cr}"/>
{eyes(xs=(42, 78), y=62)}
{sparkle(36, 56, .5, "#fff")}{sparkle(72, 56, .5, "#fff")}
<ellipse cx="60" cy="73" rx="4.5" ry="3" fill="{pk}"/>
<path d="M54 79Q57 82 60 78Q63 82 66 79" fill="none" stroke="#a85a3a" stroke-width="1.8" stroke-linecap="round"/>
<ellipse cx="27" cy="76" rx="6" ry="3.5" fill="{pk}" opacity=".7"/>
<ellipse cx="93" cy="76" rx="6" ry="3.5" fill="{pk}" opacity=".7"/>
{paws(cr, ol)}''')


MASCOTS = {
    "muvmuv": muvmuv, "lunar": lunar, "any": any_, "jewel": jewel,
    "vimmy": vimmy, "wesley": wesley,
    "goldie_red": lambda: goldie("red"), "goldie_brown": lambda: goldie("brown"),
    "lolo": lolo,
}


# ------------------------------------------------------------- activity props
# Props share the mascot's coordinates but use a wider canvas (extra room on
# the right for things held beside the buddy). The webview overlays them on
# top of the mascot, so they flip with it when it turns around.
PROP_VIEWBOX = "-20 -14 200 136"


def zee(x, y, s, color="#8a86a8"):
    return (f'<path transform="translate({x} {y}) scale({s})" d="M0 0H8L0 9H8" '
            f'fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" '
            'stroke-linejoin="round"/>')


def note(x, y, color):
    return (f'<g fill="{color}"><ellipse cx="{x}" cy="{y}" rx="4.5" ry="3.4" '
            f'transform="rotate(-20 {x} {y})"/>'
            f'<rect x="{x + 3}" y="{y - 15}" width="2" height="15"/>'
            f'<path d="M{x + 3} {y - 15}q7 2 7 9q-2-4-7-5Z"/></g>')


def steam(xs, y, color="#c9c4dd"):
    return "".join(f'<path d="M{x} {y}q-4-6 0-12q4-6 0-12" fill="none" stroke="{color}" '
                   'stroke-width="2.4" stroke-linecap="round"/>' for x in xs)


def _drumstick():
    return ('<g transform="translate(104 84) rotate(-25)">'
            '<rect x="8" y="-3" width="22" height="6" rx="3" fill="#f6ead0" stroke="#d8c7a0" stroke-width="1.4"/>'
            '<circle cx="31" cy="-4" r="4" fill="#f6ead0" stroke="#d8c7a0" stroke-width="1.4"/>'
            '<circle cx="31" cy="4" r="4" fill="#f6ead0" stroke="#d8c7a0" stroke-width="1.4"/>'
            '<ellipse cx="0" cy="0" rx="14" ry="11" fill="#d4843f" stroke="#a85e26" stroke-width="2"/>'
            '<ellipse cx="-4" cy="-4" rx="6" ry="3" fill="#f0a865"/></g>')


PROPS = {
    "chicken": _drumstick,
    "music": lambda: (
        '<path d="M14 56Q14 4 60 4Q106 4 106 56" fill="none" stroke="#3a3550" '
        'stroke-width="6" stroke-linecap="round"/>'
        '<rect x="3" y="44" width="17" height="27" rx="8" fill="#ff8fb0" stroke="#3a3550" stroke-width="2.4"/>'
        '<rect x="100" y="44" width="17" height="27" rx="8" fill="#ff8fb0" stroke="#3a3550" stroke-width="2.4"/>'
        + note(140, 42, "#5b8def") + note(162, 20, "#f06c9a")),
    "sleep": lambda: zee(126, 44, 1.1) + zee(142, 26, 1.4) + zee(160, 6, 1.8),
    "read": lambda: (
        '<g transform="translate(60 101)" stroke-linejoin="round">'
        '<path d="M-32-10V14Q-16 8 0 14Q16 8 32 14V-10" fill="#c96f6f"/>'
        '<path d="M-29-12Q-15-18 0-12V11Q-15 5-29 11Z" fill="#fff6ea" stroke="#c96f6f" stroke-width="1.6"/>'
        '<path d="M29-12Q15-18 0-12V11Q15 5 29 11Z" fill="#fff6ea" stroke="#c96f6f" stroke-width="1.6"/>'
        '<path d="M-24-6Q-14-10-5-6M-24 0Q-14-4-5 0M5-6Q14-10 24-6M5 0Q14-4 24 0" '
        'fill="none" stroke="#e0cfc0" stroke-width="1.4"/></g>'),
    "work": lambda: (
        '<rect x="28" y="74" width="64" height="34" rx="4" fill="#6a7080" stroke="#4a4f5a" stroke-width="2"/>'
        '<circle cx="60" cy="91" r="4" fill="#dfe6f0"/>'
        '<rect x="20" y="106" width="80" height="8" rx="3" fill="#a9afbb" stroke="#7d8390" stroke-width="1.6"/>'),
    "tv": lambda: (
        '<path d="M153 48L142 32M153 48L164 32" stroke="#4a4f5a" stroke-width="2.4" stroke-linecap="round"/>'
        '<rect x="128" y="48" width="50" height="40" rx="7" fill="#4a4f5a"/>'
        '<rect x="133" y="53" width="40" height="30" rx="4" fill="#8fd0e0"/>'
        '<path d="M137 58l8 0M137 62l5 0" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".8"/>'
        '<path d="M138 88l-3 8M168 88l3 8" stroke="#4a4f5a" stroke-width="3" stroke-linecap="round"/>'),
    "bubbletea": lambda: (
        '<rect x="141" y="50" width="4" height="30" rx="2" fill="#ff6f91" transform="rotate(8 143 65)"/>'
        '<path d="M127 78H153L149 115H131Z" fill="#f6ead6" stroke="#d8c3a0" stroke-width="1.6"/>'
        '<path d="M128.5 88H151.5L149 115H131Z" fill="#d1a873"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#3a2a20"/>'
                  for x, y in ((135, 110), (140, 108), (145, 110), (137, 104), (143, 103)))
        + '<ellipse cx="140" cy="78" rx="14" ry="4" fill="#fff" stroke="#d8c3a0" stroke-width="1.4"/>'),
    "coffee": lambda: (
        steam((134, 144), 82)
        + '<path d="M152 95q11 0 11 8q0 8-11 8" fill="none" stroke="#d8d2c6" stroke-width="4"/>'
        '<rect x="126" y="88" width="27" height="27" rx="6" fill="#fff" stroke="#d8d2c6" stroke-width="2"/>'
        '<ellipse cx="139.5" cy="90.5" rx="11" ry="2.6" fill="#6b4226"/>'
        + heart(139.5, 103, 1, "#ff9ec4")),
    "game": lambda: (
        '<path d="M30 96Q30 88 40 88H80Q90 88 90 96L94 108Q96 116 86 114L78 108H42L34 114Q24 116 26 108Z" '
        'fill="#5a5f6e" stroke="#3f4350" stroke-width="1.6"/>'
        '<path d="M40 98h10M45 93v10" stroke="#2c2a36" stroke-width="3.4" stroke-linecap="round"/>'
        '<circle cx="76" cy="94" r="2.6" fill="#e05a4e"/><circle cx="82" cy="99" r="2.6" fill="#4bbf5a"/>'
        '<circle cx="70" cy="99" r="2.6" fill="#ffd23f"/><circle cx="76" cy="104" r="2.6" fill="#5b8def"/>'
        + sparkle(136, 44, 1.4, "#ffd23f") + sparkle(158, 62, 1.1, "#ffd23f")
        + sparkle(152, 22, .9, "#ff9ec4")),
    "noodles": lambda: (
        steam((136, 148), 80)
        + '<path d="M150 92L174 58M157 93L178 64" stroke="#8a5a33" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M120 94H168Q166 117 144 117Q122 117 120 94Z" fill="#e05a4e" stroke="#b8443a" stroke-width="1.8"/>'
        '<ellipse cx="144" cy="94" rx="24" ry="5" fill="#ffe08a" stroke="#e8c45a" stroke-width="1.4"/>'
        '<path d="M134 93q3-6 6 0q3-6 6 0q3-6 6 0" fill="none" stroke="#f2cf62" stroke-width="2"/>'
        '<path d="M126 104h36" stroke="#fff" stroke-width="2" stroke-dasharray="4 4" opacity=".7"/>'),
    "phone": lambda: (
        '<rect x="47" y="82" width="26" height="32" rx="5" fill="#2f3240"/>'
        '<rect x="50" y="86" width="20" height="24" rx="2.5" fill="#9fe0ff"/>'
        '<path d="M53 92h12M53 97h8" stroke="#fff" stroke-width="2" stroke-linecap="round"/>'
        + heart(138, 52, 1.5, "#ff7aa8") + heart(156, 32, 1.1, "#ff9ec4")
        + heart(164, 58, .9, "#ff7aa8")),
    "plant": lambda: (
        '<path d="M146 94Q146 76 146 66" stroke="#2f8f3e" stroke-width="2.6" fill="none"/>'
        '<ellipse cx="136" cy="76" rx="10" ry="5.5" fill="#4bbf5a" transform="rotate(-30 136 76)"/>'
        '<ellipse cx="156" cy="72" rx="10" ry="5.5" fill="#4bbf5a" transform="rotate(30 156 72)"/>'
        '<ellipse cx="146" cy="60" rx="6" ry="9" fill="#2f8f3e"/>'
        '<path d="M132 96H160L156 116H136Z" fill="#d07a44"/>'
        '<rect x="129" y="91" width="34" height="7" rx="2.5" fill="#b85f2e"/>'
        + "".join(f'<path d="M{x} {y}q-3 5 0 7q3-2 0-7Z" fill="#7fd0ff"/>'
                  for x, y in ((122, 62), (116, 74), (126, 80)))),
    "alarm": lambda: (
        '<path d="M130 70q-6 10 0 20M124 66q-9 14 0 28M166 70q6 10 0 20M172 66q9 14 0 28" '
        'fill="none" stroke="#f2c94c" stroke-width="2.6" stroke-linecap="round"/>'
        '<circle cx="138" cy="66" r="7" fill="#f2c94c" stroke="#d6a92a" stroke-width="1.6"/>'
        '<circle cx="158" cy="66" r="7" fill="#f2c94c" stroke="#d6a92a" stroke-width="1.6"/>'
        '<path d="M140 100l-5 12M156 100l5 12" stroke="#b83b3b" stroke-width="3.4" stroke-linecap="round"/>'
        '<circle cx="148" cy="84" r="18" fill="#e05050" stroke="#b83b3b" stroke-width="2"/>'
        '<circle cx="148" cy="84" r="13" fill="#fff"/>'
        '<path d="M148 84V75M148 84H155" stroke="#2a2234" stroke-width="2.4" stroke-linecap="round"/>'),
}


def prop_svg(action):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{PROP_VIEWBOX}">'
            f'{PROPS[action]()}</svg>\n')
