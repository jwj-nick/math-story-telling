#!/usr/bin/env python3
# gen_images.py — unit-03 알콰리즈미 Nano Banana (se-video-image §IM6, 네이티브 16:9)
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
                    image_config=types.ImageConfig(aspect_ratio="16:9")))  # 네이티브 16:9
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

STYLE = ("STYLE: cinematic painterly illustration, 9th-century Baghdad, Islamic Golden Age, House "
    "of Wisdom, warm golden lamplight, palette of turquoise-teal, gold, sandstone, deep blue and "
    "terracotta, Islamic geometric tile patterns and horseshoe arches, 16:9 aspect ratio, NO text, "
    "NO letters, NO numerals, NO modern objects, ample empty space for caption overlay, "
    "historically accurate (9th-century Persian/Islamic scholar dress: turban and robe; bronze "
    "balance scale; parchment scrolls; astrolabe).")
CHAR = ("Al-Khwarizmi: a Persian scholar in his 50s, warm brown skin, neat black beard, wearing a "
    "white turban and a deep teal-and-sandstone scholar's robe, holding a parchment scroll, calm "
    "intelligent serene expression, warm lamplight on the face.")

REF = OUT / "ref-alkhwarizmi.png"
HEADROOM = ("IMPORTANT: frame him so his ENTIRE head and face are fully visible with comfortable "
    "headroom (empty space) ABOVE his head — do NOT crop the top of his head.")
PROMPTS = {
    "ref-alkhwarizmi.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear "
        f"view of face and clothing, simple neutral warm background. {HEADROOM} No text.", None),
    "S1.png": (f"{STYLE}\nWide establishing shot of the House of Wisdom in 9th-century Baghdad: "
        "grand horseshoe arches, intricate turquoise geometric tilework, a dome, stacks of books "
        "and an astrolabe, two or three robed scholars translating by golden lamplight. On one "
        "side, a single book glowing softly as if newly arrived from the east (India). Vast warm "
        "interior with space in the upper third for caption. No text.", None),
    "S2.png": (f"{STYLE}\nUsing the SAME Al-Khwarizmi character from the reference image (same face, "
        "same black beard, same turban and teal robe): a 16:9 WIDE upper-body shot of Al-Khwarizmi "
        "seated at a desk with parchment, a bronze balance scale beside him, blurred House of "
        f"Wisdom interior behind (shallow depth of field), calm scholarly mood. {HEADROOM} Keep "
        "generous empty space to one side for caption. No text, no numerals.", "REF"),
    "S3.png": (f"{STYLE}\nCentral subject: a large bronze two-pan balance scale standing on a stone "
        "table, the two pans perfectly level and balanced, small weights resting on each pan, "
        "dramatic warm side light, Islamic geometric pattern faintly in the background. The idea of "
        "equilibrium is the focus. Minimal uncluttered composition with empty space above. No text, "
        "no numerals.", None),
    "S4.png": (f"{STYLE}\nAn antique-map feeling of numerals spreading like a wave from the EAST "
        "(India) westward toward Europe across a stylized old world map, warm directional light "
        "moving left-to-right, suggestion of knowledge traveling and translation. Do NOT render "
        "actual numerals or letters — convey the flow with light and motion only. Empty space for "
        "caption. No text.", None),
    "S5.png": (f"{STYLE}\nA 16:9 split composition contrasting two ways of writing. LEFT half: an "
        "old parchment densely filled with long flowing handwritten paragraphs (an equation "
        "written entirely in words, NO symbols, NO legible letters — just the texture of dense "
        "prose), warm candlelight, a scholar's hand resting near it. RIGHT half: a clean bright "
        "modern surface nearly empty, suggesting a single short concise line (render NO actual "
        "letters or symbols). Clear vertical division. The contrast of long prose vs one short "
        "line. No legible text, no numerals.", "REF"),
    "S6.png": (f"{STYLE}\nA warm cinematic sense of a relay across centuries: a glowing timeline or "
        "hourglass, with three faint robed scholar silhouettes in succession from east to west "
        "(India, Baghdad, Europe), faces hidden in shadow. In the foreground center, a single "
        "elegant bronze balance scale, perfectly level, glowing. Large empty central space above "
        "for a single word overlay. Hopeful, unifying mood. No text, no letters.", None),
}

order = ["ref-alkhwarizmi.png", "S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
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
