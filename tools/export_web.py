"""Export the Python sprites + Thai deck for the VS Code / Kiro extension.

sprites.py and thai_vocab.py stay the single source of truth; run this after
editing either one:

    python3 tools/export_web.py

Writes vscode-extension/media/sprites/<mascot>_<blink><foot>.png (pixel),
vscode-extension/media/cartoon/<mascot>.svg (cartoon, from tools/cartoon.py),
vscode-extension/media/props/<action>.png|.svg (activity props) and
vscode-extension/media/data.json.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import cartoon as C  # noqa: E402
import sprites as S  # noqa: E402
import thai_vocab as TV  # noqa: E402
from preview import grid_to_image  # noqa: E402

MEDIA = os.path.join(ROOT, "vscode-extension", "media")


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
        "actions": [{"id": a, "label": S.ACTION_LABELS[a]} for a in S.ACTIONS],
        "levels": [{"id": key, "name": name,
                    "words": [list(w) for w in words]}
                   for key, name, words in TV.LEVELS],
    }
    with open(os.path.join(MEDIA, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"exported {len(S.MASCOTS)} mascots, {len(TV.VOCAB)} words -> {MEDIA}")


if __name__ == "__main__":
    main()
