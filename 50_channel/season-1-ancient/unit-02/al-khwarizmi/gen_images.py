#!/usr/bin/env python3
# gen_images.py — unit-02 알콰리즈미(secondary) Nano Banana (se-video-image §IM6, 네이티브 16:9)
# ★ ref 재사용: unit03 의 ref-alkhwarizmi.png 를 상대경로로 resolve → S2·S5 에 전달(얼굴 일관).
#   (ref 신규 생성 X — 두 영상 같은 알콰리즈미)
import os, sys, pathlib, time
from google import genai
from google.genai import types

HERE = pathlib.Path(__file__).parent
OUT = HERE / "5-images"; OUT.mkdir(exist_ok=True)
# ★ 캐릭터 reference = unit03 산출물 재사용 (상대경로 resolve)
REF = (HERE / ".." / ".." / "unit-03-al-khwarizmi" / "5-images" / "ref-alkhwarizmi.png").resolve()
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
HEADROOM = ("IMPORTANT: frame him so his ENTIRE head and face are fully visible with comfortable "
    "headroom (empty space) ABOVE his head — do NOT crop the top of his head.")

PROMPTS = {
    "S1.png": (f"{STYLE}\nWide establishing shot of the House of Wisdom in 9th-century Baghdad: "
        "grand horseshoe arches, intricate turquoise geometric tilework, a dome, stacks of books "
        "and an astrolabe, two or three robed scholars translating by golden lamplight. On one "
        "side, a single book glowing softly as if newly arrived from the east (India) — the book "
        "of zero and negative numbers. Vast warm interior with space in the upper third for "
        "caption. No text.", None),
    "S2.png": (f"{STYLE}\nUsing the SAME Al-Khwarizmi character from the reference image (same face, "
        "same black beard, same turban and teal robe): a 16:9 WIDE upper-body shot of Al-Khwarizmi "
        "seated at a desk with parchment, a bronze balance scale beside him, blurred House of "
        "Wisdom interior behind (shallow depth of field). On the parchment, an abstract sense of a "
        "tangled, knotted equation (a dark snarled texture suggesting a subtraction term making "
        f"the calculation messy — NO actual numerals or letters), thoughtful mood. {HEADROOM} Keep "
        "generous empty space to one side for caption. No text, no numerals.", "REF"),
    "S3.png": (f"{STYLE}\nCentral subject: a large bronze two-pan balance scale on a stone table. "
        "On the LEFT pan a dark weight (representing a subtracted / negative term); a clear warm "
        "directional glow and a sense of MOTION carrying that weight ACROSS to the RIGHT pan, where "
        "it becomes a bright added weight. The scale stays level after the move. The idea is moving "
        "a term to the OTHER SIDE (transposition). Minimal uncluttered composition, empty space "
        "above for caption. No text, no numerals.", None),
    "S4.png": (f"{STYLE}\nCentral subject: a large bronze two-pan balance scale on a stone table, "
        "the two pans perfectly level. Each pan holds ONE identical small weight; a gentle warm "
        "glow suggests BOTH identical weights being lifted away TOGETHER while the scale remains "
        "perfectly horizontal (cancelling equal terms, keeping balance). Dramatic warm side light, "
        "Islamic geometric pattern faint in background. Equilibrium is the focus. Empty space "
        "above. No text, no numerals.", None),
    "S5.png": (f"{STYLE}\nUsing the SAME Al-Khwarizmi character from the reference image (same face, "
        "same beard, same turban and teal robe): a 16:9 composition showing transformation from "
        "chaos to order. On one side, a dark tangled knotted texture (a messy equation full of "
        "minus signs — NO actual symbols) gradually unraveling and becoming a calm, light, tidy "
        "flowing form. Al-Khwarizmi present to one side with a calm reassuring expression, warm "
        f"lamplight. The feeling: fear turned into a manageable technique. {HEADROOM} Empty space "
        "for caption. No legible text, no numerals.", "REF"),
    "S6.png": (f"{STYLE}\nA warm cinematic sense of a relay across centuries: a glowing timeline or "
        "hourglass, with three faint robed scholar silhouettes in succession from east to west "
        "(India — discovery of negatives, Baghdad — handling negatives, Europe — letters), faces "
        "hidden in shadow. In the foreground center, a single elegant bronze balance scale, "
        "perfectly level, glowing. Large empty central space above for a single word overlay. "
        "Hopeful, unifying mood. No text, no letters.", None),
}

order = ["S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
if len(sys.argv) > 1:
    order = sys.argv[1:]
if not REF.exists():
    print(f"  ⚠ ref 없음: {REF} (unit03 의 ref-alkhwarizmi.png 필요 — S2/S5 일관성)", flush=True)
fail = []
for name in order:
    prompt, ref = PROMPTS[name]
    out = OUT / name
    if out.exists() and out.stat().st_size > 0:
        print(f"  = {name} 존재, skip", flush=True); continue
    ok = gen(prompt, out, ref_paths=[str(REF)] if ref == "REF" else None)
    if not ok: fail.append(name)
print("== DONE ==" if not fail else f"== 실패: {fail} ==", flush=True)
