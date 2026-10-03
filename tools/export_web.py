"""Export the Python sprites + Thai deck for the VS Code / Kiro extension.

sprites.py and thai_vocab.py stay the single source of truth; run this after
editing either one:

    python3 tools/export_web.py

Writes vscode-extension/media/sprites/<mascot>_<blink><foot>.png (pixel),
vscode-extension/media/cartoon/<mascot>.svg (cartoon, from tools/cartoon.py),
vscode-extension/media/props/<action>.png|.svg (activity props),
vscode-extension/media/scenes/<scene>.svg|.png (backgrounds, from tools/scenes.py;
needs Chrome for the pixel versions) and vscode-extension/media/data.json.
"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import activities as A  # noqa: E402
import cartoon as C  # noqa: E402
import scenes as SC  # noqa: E402
import sprites as S  # noqa: E402
import thai_vocab as TV  # noqa: E402
from preview import grid_to_image  # noqa: E402

MEDIA = os.path.join(ROOT, "vscode-extension", "media")
CHROME = os.environ.get(
    "CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
PIXEL = 2                                  # pixel scenes: 1 art pixel = 2 screen px


def render_pixel_scenes(svgs, outdir):
    """Pixel versions of the scenes: render each SVG with headless Chrome,
    shrink 2x, cut to a 32-colour palette. Shown 2x with crisp pixels."""
    from PIL import Image
    ids = list(svgs)
    html = "".join(
        f'<div style="position:absolute;left:0;top:{i * SC.H}px;width:{SC.W}px;height:{SC.H}px">'
        + svgs[sid].replace("<svg ", f'<svg width="{SC.W}" height="{SC.H}" ', 1) + "</div>"
        for i, sid in enumerate(ids))
    with tempfile.TemporaryDirectory() as tmp:
        page, shot = os.path.join(tmp, "p.html"), os.path.join(tmp, "p.png")
        with open(page, "w", encoding="utf-8") as f:
            f.write(f'<html><body style="margin:0">{html}</body></html>')
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--window-size={SC.W},{SC.H * len(ids)}", f"--screenshot={shot}",
                        f"file://{page}"], check=True, capture_output=True)
        sheet = Image.open(shot).convert("RGB")
    os.makedirs(outdir, exist_ok=True)
    for i, sid in enumerate(ids):
        im = sheet.crop((0, i * SC.H, SC.W, (i + 1) * SC.H))
        im = im.resize((SC.W // PIXEL, SC.H // PIXEL), Image.BOX)
        im = im.quantize(32, method=0).convert("RGB")
        im.save(os.path.join(outdir, f"{sid}.png"))


def main():
    out = os.path.join(MEDIA, "sprites")
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):                  # drop frames of removed mascots
        os.remove(os.path.join(out, f))
    for m in S.MASCOTS:
        for blink in (0, 1):
            for foot in (0, 1):
                grid = S.hd(S.build(m, blink=bool(blink), foot=foot))
                grid_to_image(grid).save(os.path.join(out, f"{m}_{blink}{foot}.png"))
    vec = os.path.join(MEDIA, "cartoon")
    os.makedirs(vec, exist_ok=True)
    for f in os.listdir(vec):
        os.remove(os.path.join(vec, f))
    for m in S.MASCOTS:
        with open(os.path.join(vec, f"{m}.svg"), "w", encoding="utf-8") as f:
            f.write(C.MASCOTS[m]())

    # activity props: pixel PNG + cartoon SVG overlays (same file stem)
    props = os.path.join(MEDIA, "props")
    os.makedirs(props, exist_ok=True)
    for action in S.ACTIONS + ["alarm"]:
        scene = [[None] * S.SCENE_W for _ in range(S.SCENE_H)]
        S._prop(scene, action)
        grid_to_image(S.hd(scene)).save(os.path.join(props, f"{action}.png"))
        with open(os.path.join(props, f"{action}.svg"), "w", encoding="utf-8") as f:
            f.write(C.prop_svg(action))
    # scene activities (tools/activities.py)
    for aid, a in A.ACTIVITIES.items():
        scene = [[None] * S.SCENE_W for _ in range(S.SCENE_H)]
        a["pixel"](scene)
        grid_to_image(S.hd(scene)).save(os.path.join(props, f"{aid}.png"))
        with open(os.path.join(props, f"{aid}.svg"), "w", encoding="utf-8") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{C.PROP_VIEWBOX}">{a["draw"]()}</svg>\n')

    # background scenes: cartoon SVG + pixel PNG
    scene_dir = os.path.join(MEDIA, "scenes")
    os.makedirs(scene_dir, exist_ok=True)
    for f in os.listdir(scene_dir):
        os.remove(os.path.join(scene_dir, f))
    scene_svgs = {sid: spec[2]() for sid, spec in SC.SCENES.items()}
    for sid, svg in scene_svgs.items():
        with open(os.path.join(scene_dir, f"{sid}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
    render_pixel_scenes(scene_svgs, scene_dir)

    # 128x128 marketplace / extensions-list icon
    from PIL import Image
    icon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    face = grid_to_image(S.hd(S.build("muvmuv")), 2)
    icon.alpha_composite(face, ((128 - face.width) // 2, (128 - face.height) // 2))
    icon.save(os.path.join(MEDIA, "icon.png"))

    data = {
        "mascots": [{"id": m, "label": S.LABELS[m],
                     "group": "GMMTV" if m in S.GMM else "Classic"}
                    for m in S.MASCOTS],
        "actions": [{"id": a, "label": S.ACTION_LABELS[a], "emoji": A.GENERAL_EMOJI[a],
                     "side": a in A.GENERAL_SIDE, "motion": None, "closed": a == "sleep",
                     "scene": None, "word": list(A.GENERAL_WORDS[a])} for a in S.ACTIONS]
                   + [{"id": aid, "label": a["label"], "emoji": a["emoji"], "side": a["kind"] == "side",
                       "motion": a["motion"], "closed": a["closed"], "scene": a["scene"],
                       "word": list(a["word"])} for aid, a in A.ACTIVITIES.items()],
        "categories": [{"id": c, "label": label} for c, label in SC.CATEGORIES],
        "scenes": [{"id": sid, "label": label, "category": cat, "top": top, "floor": floor,
                    "group": group, "acts": SC.SCENE_ACTIVITIES.get(sid, []),
                    "moves": SC.GROUP_STYLE.get(sid, "hangout")}
                   for sid, (label, cat, _, top, floor, group) in SC.SCENES.items()],
        "sceneWords": {sid: [list(w) for w in words]
                       for sid, words in TV.SCENE_WORDS.items()},
        "levels": [{"id": key, "name": name,
                    "words": [list(w) for w in words]}
                   for key, name, words in TV.LEVELS],
    }
    with open(os.path.join(MEDIA, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    extra = sum(len(w) for w in TV.SCENE_WORDS.values())
    print(f"exported {len(S.MASCOTS)} mascots, {len(SC.SCENES)} scenes, "
          f"{len(S.ACTIONS) + len(A.ACTIVITIES)} activities, "
          f"{len(TV.VOCAB)} + {extra} scene words -> {MEDIA}")


if __name__ == "__main__":
    main()
