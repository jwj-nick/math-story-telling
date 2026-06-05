#!/usr/bin/env python3
# gen_images.py — unit-05 페르마 Nano Banana (se-video-image §IM6, 네이티브 16:9)
# ★ 페르마 = 신규 캐릭터: ref-fermat.png 를 가장 먼저 생성 → 후속 인물 장면(S1,S2,S5,S6)에 ref 전달.
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

# era-modern 팔레트 + signature 청록 #5E8C7D (페르마). 17C 프랑스 툴루즈 법률가.
STYLE = ("STYLE: cinematic painterly illustration, early-to-mid 17th-century France (Toulouse), a "
    "candle-lit wood-paneled study, warm chiaroscuro candlelight, palette of deep walnut brown, "
    "candle gold, muted teal-green (#5E8C7D) and parchment cream, leather-bound books and quill "
    "pens and old volumes with wide margins, 16:9 aspect ratio, NO text, NO letters, NO numerals, "
    "NO modern objects, ample empty space for caption overlay, historically accurate (17th-century "
    "French magistrate's dress: dark robe and white collar; candle; parchment).")
# 신규 캐릭터: 데카르트(침대·파리)와 시각 차별 — 법복·책상·여백 메모
CHAR = ("Pierre de Fermat: a 17th-century French magistrate (judge) in his 40s, shoulder-length dark "
    "brown wavy hair, a thin moustache, a dark judicial robe with a white collar, a calm intelligent "
    "scholarly expression, warm candlelight on the face.")

REF = OUT / "ref-fermat.png"
HEADROOM = ("IMPORTANT: frame so the ENTIRE head and face are fully visible with comfortable "
    "headroom ABOVE the head — do NOT crop the top of the head.")
PROMPTS = {
    "ref-fermat.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear "
        f"view of face and judicial robe, simple neutral warm background. {HEADROOM} No text.", None),
    "S1.png": (f"{STYLE}\nUsing the SAME Fermat character from the reference (same wavy dark hair, "
        "moustache, dark judicial robe, white collar): Fermat seated at his desk in his candle-lit "
        "study in the evening after his day at court, opening a leather-bound mathematics book, a "
        "calm contemplative mood (the judge who loved math as a hobby), warm teal-green and gold "
        f"tones. {HEADROOM} Empty space to one side. No text.", "REF"),
    "S2.png": (f"{STYLE}\nUsing the SAME Fermat character (same hair, moustache, dark robe): a close "
        "warm view of Fermat's hand writing a note with a quill in the narrow MARGIN of an old open "
        "book, the page text and the marginal note both just illegible texture (NO real letters or "
        "numerals), candlelight glow, a quiet intimate mood of a private hobby. Empty space for "
        "caption. No legible text.", "REF"),
    "S3.png": (f"{STYLE}\nAn elegant split conceptual image: on the LEFT a robed scholar silhouette at "
        "a desk, on the RIGHT another robed scholar silhouette at a separate desk (two men who do "
        "not know each other), and above each the SAME glowing crossed coordinate axes rising and "
        "overlapping toward the center — suggesting the same discovery reached twice, independently. "
        "Do NOT render numerals or letters. Warm gold on deep teal, central empty space for caption. "
        "No text.", None),
    "S4.png": (f"{STYLE}\nAn abstract conceptual image of one glowing bridge being crossed from BOTH "
        "ends: from the left, a circle shape transforming into a stream of equation-like glow "
        "(picture to formula); from the right, an equation-like glow transforming into a shape "
        "(formula to picture); the two streams meeting in the middle as a two-way arrow. Do NOT "
        "render any real numerals or letters. Warm gold on deep teal, empty space for caption. No "
        "text.", None),
    "S5.png": (f"{STYLE}\nAn abstract conceptual image of a formula becoming a picture on a glowing "
        "dark coordinate grid: faint guide-light descending to plot a few bright points, the points "
        "then connected into one clean straight luminous line rising diagonally (a formula commanding "
        "points into a line). Do NOT render numerals or letters. Warm magical gold-teal glow, empty "
        "space for caption. No text.", None),
    "S6.png": (f"{STYLE}\nUsing the SAME Fermat character (same hair, moustache, dark robe): a warm "
        "finale image — two glowing panels, one suggesting a formula and one suggesting a shape, with "
        "a soft two-way arrow flowing between them (a translation between two languages), and Fermat's "
        "hand gently setting down a quill beside an open book. Do NOT render real letters or "
        f"numerals. {HEADROOM} Large empty central space above for a single word overlay. No text.",
        "REF"),
}

order = ["ref-fermat.png", "S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
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
