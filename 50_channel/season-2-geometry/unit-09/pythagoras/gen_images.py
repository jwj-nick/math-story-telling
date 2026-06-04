#!/usr/bin/env python3
# gen_images.py — unit-09 피타고라스(다각형) Nano Banana (네이티브 16:9)
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
                    print(f"  ✓ {pathlib.Path(out).name} ({len(p.inline_data.data)} bytes)", flush=True); return True
            print(f"  ! {pathlib.Path(out).name}: 이미지 없음 try {attempt}", flush=True)
        except Exception as e:
            print(f"  ERR {pathlib.Path(out).name} try {attempt}: {str(e)[:200]}", flush=True); time.sleep(3*attempt)
    return False

STYLE = ("STYLE: cinematic painterly illustration, ancient Greece (6th century BC, Greek colony of "
    "Croton in southern Italy), warm Mediterranean golden light, palette terracotta/ochre/bronze/"
    "olive-green, marble and lyre and geometric figures, 16:9, NO text, NO letters, NO numerals, NO "
    "modern objects, ample empty space for caption, historically accurate (Greek himation robes, a "
    "lyre, a five-pointed star pentagram emblem).")
CHAR = ("Pythagoras: an ancient Greek sage in his 60s, long white beard, white himation robe, a calm "
    "charismatic almost mystical expression, a faint pentagram (five-pointed star) emblem nearby, warm light.")
REF = OUT / "ref-pythagoras.png"
HEAD = "IMPORTANT: ENTIRE head and face visible with headroom ABOVE the head — do NOT crop the top."
PROMPTS = {
  "ref-pythagoras.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear face "
    f"and clothing, simple neutral background. {HEAD} No text.", None),
  "S1.png": (f"{STYLE}\nUsing the SAME Pythagoras from reference (white beard, himation): Pythagoras "
    "leading a small community of robed students in a sunlit Croton courtyard, a lyre and geometric "
    f"figures around, a sense of a school where math, music and philosophy are one. {HEAD} Empty space "
    "for caption. No text.", "REF"),
  "S2.png": (f"{STYLE}\nAn elegant glowing golden pentagram (a five-pointed star drawn inside a regular "
    "pentagon) floating on a dark warm ground, with faint other polygons (triangle, square, hexagon) "
    "around it, the secret emblem of the school. Do NOT render numerals or letters. Empty space for "
    "caption. No text.", None),
  "S3.png": (f"{STYLE}\nAn abstract geometry image: several polygons (a triangle, a square, a pentagon) "
    "each with their exterior angles marked as small colored wedges, and those wedges gathered "
    "together at one point forming a single full circle (one full turn), suggesting the exterior "
    "angles always sum to one full circle. Warm gold on dark. Do NOT render numerals or letters. "
    "Empty space for caption. No text.", None),
  "S4.png": (f"{STYLE}\nAn abstract image: a golden pentagram with its inner line segments highlighted, "
    "and a spiral / endless subdivision suggesting a ratio that never resolves into whole numbers "
    "(the golden ratio, an irrational number hidden in the pentagon). Mysterious warm glow on dark. "
    "Do NOT render numerals or letters. Empty space for caption. No text.", None),
  "S5.png": (f"{STYLE}\nA somber dramatic scene: a young Greek man (Hippasus) standing alone on a rocky "
    "Mediterranean seashore at dusk, looking troubled and burdened, dark waves below, a sense of a "
    "dangerous secret and exile. Do NOT render numerals or letters. Empty space for caption. No text.", None),
  "S6.png": (f"{STYLE}\nA warm finale: regular polygons — equilateral triangles, squares, and hexagons "
    "— tiling a flat plane perfectly with no gaps (a tessellation), glowing gold on warm ground, a "
    "sense of number-order covering the world. Large empty central space above for a single word "
    "overlay. No text, no numerals.", None),
}
order = ["ref-pythagoras.png","S1.png","S2.png","S3.png","S4.png","S5.png","S6.png"]
if len(sys.argv) > 1: order = sys.argv[1:]
fail = []
for name in order:
    prompt, ref = PROMPTS[name]; out = OUT / name
    if out.exists() and out.stat().st_size > 0: print(f"  = {name} skip", flush=True); continue
    if not gen(prompt, out, ref_paths=[str(REF)] if ref == "REF" else None): fail.append(name)
print("== DONE ==" if not fail else f"== 실패: {fail} ==", flush=True)
