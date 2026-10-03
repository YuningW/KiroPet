"""Render the cartoon (SVG) mascots to PNGs for the desktop Python app.

Tk can't draw SVG, so this pre-renders every frame the app needs with
headless Chrome (one page, one screenshot), then slices / scales / rotates
them with Pillow. Run it on any machine with Chrome after editing
tools/cartoon.py:

    python3 tools/render_cartoon_png.py

Writes assets/cartoon/:
    walk/<mascot>_<blink><foot>_r<rot>.png   window-edge walker, 4 rotations
    desk/<mascot>_<blink><foot>.png          desktop buddy
    props/<action>.png                       desktop-buddy activity props
    thumb/<mascot>.png                       picker thumbnails (soft edges)

The pet windows use a colour key for transparency, which can't show
half-transparent pixels, so every image except the thumbnails is cut to
fully opaque / fully transparent (no coloured halo on any background).
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import cartoon as C  # noqa: E402
import sprites as S  # noqa: E402

OUT = os.path.join(ROOT, "assets", "cartoon")
CHROME = os.environ.get(
    "CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
SS = 4                                   # supersample, then scale down

WALK = (35, 40)                          # matches the pixel walker's size
DESK = (74, 84)                          # matches the pixel desk buddy
PROP = (124, 84)                         # 200x136 prop canvas at desk scale
THUMB = (88, 100)


def variant(svg, blink, foot):
    if blink:
        svg = svg.replace('<g id="eyes-open">', '<g id="eyes-open" visibility="hidden">')
        svg = svg.replace('<g id="eyes-closed" visibility="hidden"', '<g id="eyes-closed"')
    lifted = "foot-l" if foot == 0 else "foot-r"
    return svg.replace(f'id="{lifted}"', f'id="{lifted}" transform="translate(0 -5)"', 1)


def hard_alpha(img):
    """Fully opaque or fully transparent, keeping each pixel's own colour."""
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 255) if a >= 128 else (0, 0, 0, 0)
    return img


def main():
    jobs = []                            # (svg, (w, h), save_fn)
    for m in S.MASCOTS:
        base = C.MASCOTS[m]()
        jobs.append((base, THUMB, lambda im, m=m: im.save(f"{OUT}/thumb/{m}.png")))
        for blink in (0, 1):
            for foot in (0, 1):
                svg = variant(base, blink, foot)

                def walk(im, m=m, b=blink, f=foot):
                    im = hard_alpha(im)
                    for rot, t in enumerate((None, Image.ROTATE_270,
                                             Image.ROTATE_180, Image.ROTATE_90)):
                        (im.transpose(t) if t else im).save(
                            f"{OUT}/walk/{m}_{b}{f}_r{rot}.png")
                jobs.append((svg, WALK, walk))
                jobs.append((svg, DESK, lambda im, m=m, b=blink, f=foot:
                             hard_alpha(im).save(f"{OUT}/desk/{m}_{b}{f}.png")))
    for action in S.ACTIONS + ["alarm"]:
        jobs.append((C.prop_svg(action), PROP, lambda im, a=action:
                     hard_alpha(im).save(f"{OUT}/props/{a}.png")))

    # lay every job out on one page at SS x size, screenshot once
    page_w, x, y, row_h, cells = 2400, 0, 0, 0, []
    for svg, (w, h), _ in jobs:
        W, H = w * SS, h * SS
        if x + W > page_w:
            x, y, row_h = 0, y + row_h, 0
        cells.append((x, y, W, H, svg))
        x, row_h = x + W, max(row_h, H)
    page_h = y + row_h
    html = "".join(
        f'<div style="position:absolute;left:{cx}px;top:{cy}px;width:{W}px;height:{H}px">'
        + svg.replace("<svg ", f'<svg width="{W}" height="{H}" ', 1) + "</div>"
        for cx, cy, W, H, svg in cells)
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "page.html")
        shot = os.path.join(tmp, "page.png")
        with open(page, "w", encoding="utf-8") as f:
            f.write('<html><body style="margin:0;background:transparent">' + html + "</body></html>")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--default-background-color=00000000",
                        f"--window-size={page_w},{page_h}", f"--screenshot={shot}",
                        f"file://{page}"], check=True, capture_output=True)
        sheet = Image.open(shot).convert("RGBA")

    for sub in ("walk", "desk", "props", "thumb"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
        for f in os.listdir(os.path.join(OUT, sub)):
            os.remove(os.path.join(OUT, sub, f))
    for (cx, cy, W, H, _), (_, size, save) in zip(cells, jobs):
        save(sheet.crop((cx, cy, cx + W, cy + H)).resize(size, Image.LANCZOS))
    print(f"rendered {len(jobs)} cartoon images -> {OUT}")


if __name__ == "__main__":
    main()
