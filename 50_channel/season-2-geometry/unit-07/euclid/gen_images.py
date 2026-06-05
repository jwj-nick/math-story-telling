#!/usr/bin/env python3
# gen_images.py — unit-07 유클리드 Nano Banana (se-video-image §IM6, 네이티브 16:9)
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

STYLE = ("STYLE: cinematic painterly illustration, ancient Greece / Hellenistic Alexandria, warm "
    "golden hour light, palette of terracotta, ochre, bronze and sage-green, weathered marble and "
    "papyrus scrolls, 16:9 aspect ratio, NO text, NO letters, NO numerals, NO modern objects, "
    "ample empty space for caption overlay, historically accurate (Greek himation robes; papyrus; "
    "a wooden compass and straightedge; the Library of Alexandria).")
CHAR = ("Euclid: an ancient Greek scholar in his late 50s, a full white beard, wearing a pale Greek "
    "himation robe, holding a wooden drawing compass and a papyrus scroll, a calm composed orderly "
    "expression, warm golden light.")

REF = OUT / "ref-euclid.png"
HEADROOM = ("IMPORTANT: frame so the ENTIRE head and face are fully visible with comfortable "
    "headroom ABOVE the head — do NOT crop the top of the head.")
PROMPTS = {
    "ref-euclid.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear view "
        f"of face and clothing, simple neutral warm background. {HEADROOM} No text.", None),
    "S1.png": (f"{STYLE}\nUsing the SAME Euclid character from the reference (same white beard, "
        "himation): Euclid standing in the ancient Library of Alexandria among papyrus scrolls and "
        "shelves, holding a compass and a thick bound book (the Elements) glowing softly, warm "
        f"golden interior light, a sense of the gateway into geometry. {HEADROOM} Empty space for "
        "caption. No text.", "REF"),
    "S2.png": (f"{STYLE}\nAncient Egypt: a great pyramid under bright desert sun, an old Greek sage "
        "(Thales) standing with a vertical measuring staff, the man's shadow and the staff's shadow "
        "cast on the sand, faint dotted guide-lines suggesting similar triangles between the staff "
        "shadow and the pyramid's long shadow (measuring height by proportion). Do NOT render "
        "numerals or letters. Empty sky for caption. No text.", None),
    "S3.png": (f"{STYLE}\nAn elegant abstract image on a deep dark background: a single glowing point "
        "of light, from which a luminous line extends, and from the line a faint translucent plane "
        "unfolds — showing point becoming line becoming surface (the birth of basic geometric "
        "elements). Soft gold light, minimal and clean. Do NOT render numerals or letters. Empty "
        "space for caption. No text.", None),
    "S4.png": (f"{STYLE}\nAn abstract conceptual image: five glowing foundation blocks at the bottom "
        "(a few simple axioms), and rising above them a tall elegant tower built of luminous "
        "geometric shapes — points, lines, angles, triangles stacked layer upon layer (many "
        "theorems built from few axioms). A small base supporting a great structure. Do NOT render "
        "numerals or letters. Warm gold on dark, empty space for caption. No text.", None),
    "S5.png": (f"{STYLE}\nAn ancient scene: a Hellenistic king (Ptolemy) in royal robes seated, "
        "gesturing a question, and Euclid (same white beard, himation) standing and calmly shaking "
        "his head — declining to offer a shortcut. Behind them, the Elements book and warm library "
        "light. Dignified mood. Do NOT render numerals or letters. Empty space for caption. No text.", "REF"),
    "S6.png": (f"{STYLE}\nA bridging abstract image: a single glowing geometric point on the left "
        "transforming into a point on a faint coordinate grid on the right (geometry becoming "
        "algebra across two thousand years), with a wooden compass and an unmarked straightedge "
        "resting in the foreground (hinting at construction). Warm gold light, large empty central "
        "space above for a single word overlay. No text, no letters.", None),
}

order = ["ref-euclid.png", "S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
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
