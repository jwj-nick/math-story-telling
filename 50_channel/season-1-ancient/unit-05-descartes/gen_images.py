#!/usr/bin/env python3
# gen_images.py — unit-05 데카르트 Nano Banana (se-video-image §IM6, 네이티브 16:9)
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

STYLE = ("STYLE: cinematic painterly illustration, early 17th-century Europe, a candle-lit "
    "wood-paneled scholar's study, warm chiaroscuro candlelight, palette of deep walnut brown, "
    "candle gold, sky-blue and deep teal, leather-bound books and quill pens and a celestial "
    "globe, 16:9 aspect ratio, NO text, NO letters, NO numerals, NO modern objects, ample empty "
    "space for caption overlay, historically accurate (17th-century European dress: white lace "
    "collar, dark coat; candle; parchment).")
CHAR = ("Rene Descartes: a 17th-century European scholar in his 40s, shoulder-length dark brown "
    "wavy hair, a thin moustache, a white lace collar over a dark coat, a thoughtful slightly "
    "languid expression, warm candlelight on the face.")

REF = OUT / "ref-descartes.png"
HEADROOM = ("IMPORTANT: frame so the ENTIRE head and face are fully visible with comfortable "
    "headroom ABOVE the head — do NOT crop the top of the head.")
PROMPTS = {
    "ref-descartes.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear "
        f"view of face and clothing, simple neutral warm background. {HEADROOM} No text.", None),
    "S1.png": (f"{STYLE}\nUsing the SAME Descartes character from the reference (same wavy dark "
        "hair, moustache, lace collar): Descartes reclining lazily on a bed in his candle-lit study, "
        "a book and quill resting nearby, a warm dim dawn glow through a window, a relaxed "
        f"contemplative mood (the famous late-sleeper genius). {HEADROOM} Empty space to one side. "
        "No text.", "REF"),
    "S2.png": (f"{STYLE}\nA low-angle view looking up at a wood-beamed ceiling of a 17th-century "
        "room, a single small fly resting on the ceiling, faint dotted guide-lines suggesting two "
        "perpendicular distances from two walls reaching toward the fly (the birth of coordinates), "
        "warm candlelight from below, a quiet eureka mood. Do NOT render numerals or letters. Empty "
        "space for caption. No text.", None),
    "S3.png": (f"{STYLE}\nAn elegant abstract conceptual image of a coordinate plane being born: one "
        "glowing horizontal line and one glowing vertical line crossing at a central origin point, "
        "a faint warm grid spreading across a dark parchment plane, a single bright point glowing "
        "where two faint guide-lines meet. Do NOT render any numerals or letters. Warm gold on deep "
        "blue, central empty space for caption. No text.", None),
    "S4.png": (f"{STYLE}\nAn abstract conceptual image uniting equation and shape: on a glowing dark "
        "coordinate grid, a clean straight luminous line rising diagonally, and beside it a perfect "
        "glowing circle, both made of the same golden light, suggesting that a formula and a "
        "picture are the same thing. Do NOT render numerals or letters. Warm magical glow, empty "
        "space for caption. No text.", None),
    "S5.png": (f"{STYLE}\nUsing the SAME Descartes character (same hair, moustache, lace collar): "
        "Descartes seated at his desk writing with a quill on parchment by candlelight, focused, a "
        "celestial globe and books around him (the writing illegible, just texture — NO real "
        f"letters). {HEADROOM} Empty space to one side. No legible text, no numerals.", "REF"),
    "S6.png": (f"{STYLE}\nA warm cinematic finale image: a glowing coordinate plane seen in "
        "perspective, with five soft points of light converging toward a single bright meeting "
        "point at the center (five stories meeting), faint robed scholar silhouettes around the "
        "edges fading into warm darkness, a sense of unity across a thousand years. Large empty "
        "central space above for a single word overlay. No text, no letters.", None),
}

order = ["ref-descartes.png", "S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
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
