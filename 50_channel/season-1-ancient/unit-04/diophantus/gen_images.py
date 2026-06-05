#!/usr/bin/env python3
# gen_images.py — unit-04 디오판토스 Nano Banana (se-video-image §IM6, 네이티브 16:9)
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

STYLE = ("STYLE: cinematic painterly illustration, 3rd-century Alexandria in Roman Egypt, an aged "
    "Hellenistic harbor city of scholars, warm low evening light, palette of terracotta, ochre, "
    "bronze and slate-blue, weathered stone and papyrus scrolls, 16:9 aspect ratio, NO text, NO "
    "letters, NO numerals, NO modern objects, ample empty space for caption overlay, historically "
    "accurate (Greek himation robes; papyrus scrolls; carved stone steles; the Library of "
    "Alexandria).")
CHAR = ("Diophantus: a Greek scholar of Alexandria in his late 50s, weathered warm skin, short grey "
    "beard, wearing a pale Greek himation robe draped over one shoulder, holding a papyrus scroll, "
    "a thoughtful slightly mysterious expression (a man of whom little is known), warm lamplight.")

REF = OUT / "ref-diophantus.png"
HEADROOM = ("IMPORTANT: frame so the ENTIRE head and face are fully visible with comfortable "
    "headroom ABOVE the head — do NOT crop the top of the head.")
PROMPTS = {
    "ref-diophantus.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear "
        f"view of face and clothing, simple neutral warm background. {HEADROOM} No text.", None),
    "S1.png": (f"{STYLE}\nWide establishing shot of 3rd-century Alexandria at dusk: the Mediterranean "
        "harbor, the great Library's weathered stone columns, shelves of papyrus scrolls, the faint "
        "Pharos lighthouse far on the coast, a lone robed scholar silhouette. A sense of a city 600 "
        "years older than its golden age, nostalgic and quiet. Vast warm sky in the upper third for "
        "caption. No text.", None),
    "S2.png": (f"{STYLE}\nA weathered ancient Greek carved stone funerary stele (epitaph stone) "
        "standing upright, softly lit, decorative carved patterns and a faint laurel motif (but NO "
        "legible letters or numerals), a quiet mysterious mournful mood, shallow depth of field. "
        "Empty space above for caption. No text, no numerals.", None),
    "S3.png": (f"{STYLE}\nAn abstract conceptual image: a long horizontal life-ribbon / timeline bar "
        "made of warm glowing segments of different lengths laid across aged parchment, suggesting "
        "a human life divided into parts, a large glowing question mark hovering above transforming "
        "into a single luminous abstract glyph. Do NOT render real numerals or letters. Calm warm "
        "lamplight, empty space for caption. No text.", None),
    "S4.png": (f"{STYLE}\nAn abstract conceptual image of resolution and balance: a bronze two-pan "
        "balance scale perfectly level, and beside it a warm life-ribbon timeline bar fully and "
        "evenly filled with golden light from end to end, a sense of an answer found. Do NOT render "
        "numerals or letters. Warm triumphant lamplight, central empty space for a caption. No text.", None),
    "S5.png": (f"{STYLE}\nUsing the SAME Diophantus character from the reference image (same face, "
        "grey beard, pale himation): Diophantus seated, unrolling a large papyrus scroll (his book "
        "Arithmetica) covered in dense handwritten prose (NO legible letters — just the texture of "
        f"writing), a quill and inkpot nearby, contemplative. {HEADROOM} Empty space to one side. "
        "No legible text, no numerals.", "REF"),
    "S6.png": (f"{STYLE}\nClose-up of a very old leather-bound book lying open, with a wide blank "
        "margin, and a 17th-century quill pen in a hand writing a single short note in that margin "
        "(the hand and quill only, face hidden, NO legible text). Warm candlelight, a sense of a "
        "secret left across centuries, large empty space above for a single word overlay. No "
        "legible text, no numerals.", None),
}

order = ["ref-diophantus.png", "S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
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
