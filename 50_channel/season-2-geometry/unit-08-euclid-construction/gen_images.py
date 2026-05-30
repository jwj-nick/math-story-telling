#!/usr/bin/env python3
# gen_images.py — unit-08 유클리드(작도) Nano Banana (네이티브 16:9)
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
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image'],
                    image_config=types.ImageConfig(aspect_ratio="16:9")))
            for p in resp.candidates[0].content.parts:
                if getattr(p, "inline_data", None) and p.inline_data.data:
                    pathlib.Path(out).write_bytes(p.inline_data.data)
                    print(f"  ✓ {pathlib.Path(out).name} ({len(p.inline_data.data)} bytes)", flush=True)
                    return True
            print(f"  ! {pathlib.Path(out).name}: 이미지 없음 try {attempt}", flush=True)
        except Exception as e:
            print(f"  ERR {pathlib.Path(out).name} try {attempt}: {str(e)[:200]}", flush=True)
            time.sleep(3 * attempt)
    return False

STYLE = ("STYLE: cinematic painterly illustration, ancient Greece / Hellenistic, warm golden light, "
    "palette terracotta/ochre/bronze/sage-green, weathered marble and papyrus, 16:9, NO text, NO "
    "letters, NO numerals, NO modern objects, ample empty space for caption, historically accurate "
    "(Greek himation; wooden compass and an unmarked straightedge; papyrus with geometric figures).")
CHAR = ("Euclid: an ancient Greek scholar in his late 50s, full white beard, pale Greek himation "
    "robe, holding a wooden compass and an unmarked straightedge, calm orderly expression, warm light.")
GAUSS = ("a serious passionate German youth of about nineteen, short brown hair, a simple late-18th-"
    "century shirt and coat, at a wooden desk with compass and straightedge, candlelight.")

REF = OUT / "ref-euclid2.png"
HEAD = ("IMPORTANT: frame so the ENTIRE head and face are fully visible with headroom ABOVE the "
    "head — do NOT crop the top of the head.")
PROMPTS = {
    "ref-euclid2.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear view "
        f"of face and clothing, holding compass and straightedge, simple neutral background. {HEAD} No text.", None),
    "S1.png": (f"{STYLE}\nUsing the SAME Euclid from the reference (white beard, himation): Euclid "
        "holding up a wooden compass and an unmarked straightedge, a papyrus with clean geometric "
        f"figures (lines, a triangle) before him, warm library light, a sense of precise craft. {HEAD} "
        "Empty space for caption. No text.", "REF"),
    "S2.png": (f"{STYLE}\nAn abstract clean geometry image: a wooden compass drawing two intersecting "
        "arcs over a line segment, constructing a perpendicular bisector, and nearby an angle being "
        "bisected by arcs — elegant construction lines in gold on dark parchment. Do NOT render "
        "numerals or letters. Empty space for caption. No text.", None),
    "S3.png": (f"{STYLE}\nAn abstract image of congruence: two identical triangles, one sliding to "
        "overlap perfectly onto the other (exactly superimposed), glowing gold outlines on a dark "
        "ground, a sense of perfect match. Do NOT render numerals or letters. Empty space for caption. No text.", None),
    "S4.png": (f"{STYLE}\nAn abstract image: several identical geometric figures drawn by compass and "
        "straightedge, all perfectly overlapping into one crisp shape, suggesting that following the "
        "same rule yields the same result. Warm gold on dark, clean and minimal. Do NOT render "
        "numerals or letters. Empty space for caption. No text.", None),
    "S5.png": (f"STYLE: cinematic painterly illustration, late 18th-century Germany, a candle-lit "
        f"study, palette of slate-blue, brown and candle-gold, 16:9, NO text NO letters NO numerals "
        f"NO modern objects, caption space.\n{GAUSS}\nThe young Gauss at his desk, having just drawn "
        "a regular polygon with many equal sides (a regular 17-sided figure) using compass and "
        f"straightedge, glowing softly, his face bright with discovery. {HEAD} Empty space for caption. "
        "No text, no numerals.", None),
    "S6.png": (f"{STYLE}\nA warm finale: a wooden compass and unmarked straightedge crossed, and above "
        "them a glowing regular many-sided polygon (17 sides) radiating light, a sense of rules "
        "opening new possibility. Large empty central space above for a single word overlay. No text, "
        "no numerals.", None),
}

order = ["ref-euclid2.png", "S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
if len(sys.argv) > 1:
    order = sys.argv[1:]
fail = []
for name in order:
    prompt, ref = PROMPTS[name]
    out = OUT / name
    if out.exists() and out.stat().st_size > 0:
        print(f"  = {name} 존재, skip", flush=True); continue
    ok = gen(prompt, out, ref_paths=[str(REF)] if ref == "REF" else None)
    if not ok: fail.append(name)
print("== DONE ==" if not fail else f"== 실패: {fail} ==", flush=True)
