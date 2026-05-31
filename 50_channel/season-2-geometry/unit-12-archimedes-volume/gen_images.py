#!/usr/bin/env python3
# gen_images.py — unit-12 아르키메데스(겉넓이와 부피) Nano Banana (네이티브 16:9)
import os, sys, pathlib, time
from google import genai
from google.genai import types

HERE = pathlib.Path(__file__).parent
OUT = HERE / "5-images"; OUT.mkdir(exist_ok=True)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash-image"

def gen(prompt, out, ref_paths=None):
    contents = [prompt]
    if ref_paths:
        for rp in ref_paths:
            contents.append(types.Part.from_bytes(data=pathlib.Path(rp).read_bytes(), mime_type="image/png"))
    for attempt in range(1, 5):
        try:
            resp = client.models.generate_content(model=MODEL, contents=contents,
                config=types.GenerateContentConfig(response_modalities=['Text', 'Image'],
                    image_config=types.ImageConfig(aspect_ratio="16:9")))
            for p in resp.candidates[0].content.parts:
                if getattr(p, "inline_data", None) and p.inline_data.data:
                    pathlib.Path(out).write_bytes(p.inline_data.data)
                    print(f"  OK {pathlib.Path(out).name} ({len(p.inline_data.data)} bytes)", flush=True); return True
            print(f"  ! {pathlib.Path(out).name}: 이미지 없음 try {attempt}", flush=True)
        except Exception as e:
            print(f"  ERR {pathlib.Path(out).name} try {attempt}: {str(e)[:200]}", flush=True); time.sleep(3*attempt)
    return False

STYLE = ("STYLE: cinematic painterly illustration, ancient Syracuse / Roman era, warm Mediterranean light "
    "fading to dusk, palette terracotta/ochre/bronze/olive and deep blue, weathered marble and stone, "
    "16:9, NO text, NO letters, NO numerals, NO modern objects, ample empty space for caption, "
    "historically accurate (Roman toga, Greek robes).")
DIAGRAM = ("STYLE: a clean minimal GEOMETRY DIAGRAM, flat, centered, NO people, NO scene, NO landscape, dark "
    "warm charcoal background, glowing thin gold and bronze lines (wireframe), 16:9, cinematic but abstract, "
    "like an elegant textbook figure. NO text, NO numerals.")
HEAD = "IMPORTANT: ENTIRE head and face visible with headroom ABOVE the head — do NOT crop the top."
PROMPTS = {
  "S1.png": (f"{STYLE}\nA somber dusk scene: a Roman nobleman (Cicero) in a toga discovering a forgotten, "
    "overgrown tombstone half-buried in tall weeds and brambles; carved in relief on the weathered stone "
    "is a single image — a SPHERE sitting inside a CYLINDER. He gazes at it with quiet reverence, soft "
    f"golden dusk light. {HEAD} Empty space for caption. No text, no numerals.", None),
  "S2.png": (f"{DIAGRAM}\nDraw a rectangular prism (a box) shown UNFOLDING / FLATTENING into its net: the 3D "
    "box on one side and its opened-out flat net of rectangles laid out beside it (the surface unrolled "
    "flat), glowing gold wireframe on dark. Show clearly that the surface of a solid becomes flat shapes. "
    "Generous empty space top and bottom for captions.", None),
  "S3.png": (f"{DIAGRAM}\nDraw a clear comparison: on the right a CYLINDER, and on the left a CONE with the "
    "SAME circular base and SAME height as the cylinder; show THREE identical cones flowing/pouring to "
    "fill the ONE cylinder exactly (suggesting the cone is one third of the cylinder). Glowing gold "
    "wireframe on dark ground. Empty space for caption.", None),
  "S4.png": (f"{DIAGRAM}\nDraw the famous Archimedes figure: a SPHERE fitting snugly INSIDE a CYLINDER — the "
    "sphere touches the top, the bottom, and the curved side of the cylinder exactly (the cylinder's "
    "height equals its diameter). Glowing gold wireframe, the sphere slightly brighter, on a dark ground. "
    "Clean and iconic, like a tombstone emblem. Empty space above and below for captions.", None),
  "S5.png": (f"{DIAGRAM}\nDraw a solid (a sphere or a dome) shown sliced horizontally into MANY thin flat "
    "disks stacked one on top of another like a stack of coins, the thin cross-section layers clearly "
    "visible, glowing gold on dark ground — the idea of building volume by stacking thin slices. Empty "
    "space for caption.", None),
  "S6.png": (f"{DIAGRAM}\nA glowing gold SPHERE nestled inside a CYLINDER (the Archimedes emblem) placed on "
    "the FAR LEFT THIRD of the frame, softly radiant like an engraving on a memorial; leave the entire "
    "RIGHT TWO-THIRDS as deep dark empty space with NOTHING in it, reserved for a single word overlay. "
    "Warm gold on near-black. No text, no numerals.", None),
}
order = ["S1.png","S2.png","S3.png","S4.png","S5.png","S6.png"]
if len(sys.argv) > 1: order = sys.argv[1:]
fail = []
for name in order:
    prompt, ref = PROMPTS[name]; out = OUT / name
    if out.exists() and out.stat().st_size > 0: print(f"  = {name} skip", flush=True); continue
    if not gen(prompt, out): fail.append(name)
print("== DONE ==" if not fail else f"== 실패: {fail} ==", flush=True)
