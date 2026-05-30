#!/usr/bin/env python3
# gen_images.py — unit-06 케플러 Nano Banana (se-video-image §IM6, 네이티브 16:9)
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

STYLE = ("STYLE: cinematic painterly illustration, early 17th-century Europe, an astronomer's "
    "candle-lit study and observatory at night, deep starry night-blue sky, palette of deep "
    "night-blue, brass/bronze, warm candle-gold and brown, a brass armillary sphere and stacks of "
    "observation logs, 16:9 aspect ratio, NO text, NO letters, NO numerals, NO modern objects, "
    "ample empty space for caption overlay, historically accurate (17th-century European dress: "
    "ruff collar, dark scholar's gown; brass astronomical instruments; quill).")
CHAR = ("Johannes Kepler: a 17th-century German astronomer in his 40s, short curly brown hair and "
    "beard, a white ruffled collar over a dark scholar's gown, a thoughtful warm expression, warm "
    "candlelight on the face against a starry night.")

REF = OUT / "ref-kepler.png"
HEADROOM = ("IMPORTANT: frame so the ENTIRE head and face are fully visible with comfortable "
    "headroom ABOVE the head — do NOT crop the top of the head.")
PROMPTS = {
    "ref-kepler.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear view "
        f"of face and clothing, simple neutral warm background. {HEADROOM} No text.", None),
    "S1.png": (f"{STYLE}\nUsing the SAME Kepler character from the reference (same curly hair, "
        "beard, ruff collar): Kepler in his observatory at night gazing up at a sky full of stars, "
        "a large brass armillary sphere beside him and thick stacks of observation logs on the "
        f"desk, candlelight, a sense of wonder. {HEADROOM} Empty sky space for caption. No text.", "REF"),
    "S2.png": (f"{STYLE}\nAn elegant antique diagram of the solar system as nested platonic solids: "
        "planetary orbital spheres with the five regular polyhedra (cube, tetrahedron, octahedron, "
        "dodecahedron, icosahedron) nested inside one another (Kepler's Mysterium Cosmographicum), "
        "beautiful but subtly flawed, warm brass-and-parchment tones, glowing softly. Do NOT render "
        "numerals or letters. Empty space for caption. No text.", None),
    "S3.png": (f"{STYLE}\nAn abstract conceptual image of a planet on an elliptical orbit around a "
        "glowing sun, with two equal pie-slice sweep areas marked (one near the sun, one far), a "
        "long motion-blur arrow where the planet is near the sun (fast) and a short arrow where it "
        "is far (slow), and a subtle seesaw motif suggesting distance-up / speed-down. Do NOT "
        "render numerals or letters. Deep night-blue with gold, empty space for caption. No text.", None),
    "S4.png": (f"{STYLE}\nA clean abstract image contrasting two graphs on dark coordinate grids "
        "side by side: on the LEFT a straight luminous line rising through the origin (direct "
        "proportion), on the RIGHT a smooth curve bending away (inverse proportion, a hyperbola "
        "shape). Both in warm gold light. Do NOT render numerals or letters. Empty space for "
        "caption, clear vertical division. No text.", None),
    "S5.png": (f"{STYLE}\nA 17th-century experiment: a glass tube/cylinder containing trapped air "
        "with a hand pressing a piston down, the air space visibly compressed smaller, warm "
        "candlelight in a study laboratory with brass instruments (Robert Boyle's experiment, his "
        "face hidden). A subtle seesaw motif of pressure-up / volume-down. Do NOT render numerals "
        "or letters. Empty space for caption. No text.", None),
    "S6.png": (f"{STYLE}\nA warm cinematic finale: glowing planets orbiting in graceful proportioned "
        "harmony around a soft light, a brass armillary sphere in the foreground, an open book "
        "glowing (Harmonices Mundi), a sense of order and consolation emerging from darkness, faint "
        "candlelight. Large empty central space above for a single word overlay. No text, no letters.", None),
}

order = ["ref-kepler.png", "S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
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
