#!/usr/bin/env python3
# gen_images.py — unit-02 Nano Banana 이미지 생성 (se-video-image §IM6)
# ref 먼저 → S2/S3는 ref로 캐릭터 일관성 → S1/S4/S5/S6 독립
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
                    image_config=types.ImageConfig(aspect_ratio="16:9")))  # 네이티브 16:9 (크롭 무손실)
            for p in resp.candidates[0].content.parts:
                if getattr(p, "inline_data", None) and p.inline_data.data:
                    pathlib.Path(out).write_bytes(p.inline_data.data)
                    print(f"  ✓ {pathlib.Path(out).name} ({len(p.inline_data.data)} bytes)", flush=True)
                    return True
            print(f"  ! {pathlib.Path(out).name}: 이미지 없음 (텍스트만) try {attempt}", flush=True)
        except Exception as e:
            print(f"  ERR {pathlib.Path(out).name} try {attempt}: {str(e)[:200]}", flush=True)
            time.sleep(3 * attempt)
    return False

STYLE = ("STYLE: cinematic painterly illustration, 7th-century classical India, warm dusk / "
    "lamplit night mood, palette of saffron, ochre, plum-purple, warm clay-brown and deep "
    "night-blue, soft warm lamplight, 16:9 aspect ratio, NO text, NO letters, NO numerals, "
    "NO modern objects, ample empty space for caption overlay, historically accurate "
    "(7th-century Indian dress: dhoti and draped shoulder cloth; stone observatory; clay "
    "tablets and palm-leaf manuscripts).")
CHAR = ("Brahmagupta: an Indian astronomer-mathematician in his late 50s, warm brown skin, "
    "short greying beard, wearing a white-and-saffron dhoti with a draped shoulder cloth, a "
    "faint tilak mark on the forehead, holding a clay tablet, serene thoughtful gentle expression.")

REF = OUT / "ref-brahmagupta.png"
PROMPTS = {
    "ref-brahmagupta.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear "
        "view of face and clothing, simple neutral warm background. No text.", None),
    "S1.png": (f"{STYLE}\nWide establishing shot of a 7th-century Indian stone astronomical "
        "observatory in the city of Ujjain at night, a sky full of stars, warm oil lamps glowing on "
        "stone terraces, one or two distant robed scholar silhouettes observing the sky, deep "
        "night-blue sky meeting warm saffron lamplight, vast starry sky in the upper third for "
        "caption space. No text.", None),
    "S2.png": (f"{STYLE}\nUsing the SAME Brahmagupta character from the reference image (same face, "
        "same greying beard, same white-saffron dhoti): a 16:9 WIDE landscape upper-body shot of "
        "Brahmagupta seated, holding a clay tablet, a warm oil lamp beside him, blurred stone "
        "observatory interior behind (shallow depth of field), calm scholarly mood. IMPORTANT: "
        "frame him so his ENTIRE head and face are fully visible with comfortable headroom (empty "
        "space) ABOVE his head — do NOT crop the top of his head. Keep generous empty space to one "
        "side for caption. No text, no numerals.", "REF"),
    "S3.png": (f"{STYLE}\nUsing the SAME Brahmagupta character (same hands, same dhoti): top-down "
        "close-up of Brahmagupta's hands inscribing a blank clay tablet with a stylus by warm "
        "lamplight, the tablet surface mostly empty and clean (space for overlaid rule lines "
        "later), focused intent. No text, no numerals, no symbols.", "REF"),
    "S4.png": (f"{STYLE}\nA glowing single point of golden light resting at the center of a long "
        "horizontal luminous line that stretches left and right into soft darkness, abstract and "
        "contemplative, the right side warm and the left side cooler, faint evenly-spaced tick "
        "marks along the line (but NO numerals, NO text), a quiet mysterious mood with deep shadow "
        "around, central composition with empty space. No text, no numbers.", None),
    "S5.png": (f"{STYLE}\nA 16:9 split-screen composition. LEFT half: cool white Greek marble "
        "setting with geometric line segments and a measuring rod, cold pale daylight, classical "
        "Greek aesthetic. RIGHT half: warm Indian setting with a clay accounting tablet and warm "
        "saffron lamplight, a horizontal line extending both directions. The right half is brighter "
        "and warmer than the left. Clear vertical division down the middle. No text, no numerals.", None),
    "S6.png": (f"{STYLE}\nA palm-leaf manuscript / bound book glowing softly, with a faint old-map "
        "feeling of travel from India westward toward Baghdad (suggested by warm directional light "
        "and distance, NOT by any written labels). On the far right, the dim silhouette of a robed "
        "scholar opening the book in a Baghdad study, face hidden in shadow. Warm, hopeful, "
        "cinematic. Large empty central space for a single word overlay. No text, no letters.", None),
}

# ref 먼저
order = ["ref-brahmagupta.png", "S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
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
