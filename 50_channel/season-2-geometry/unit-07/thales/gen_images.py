#!/usr/bin/env python3
# gen_images.py — unit-07 탈레스 Nano Banana (se-video-image §IM6, 네이티브 16:9)
# ★탈레스 = 신규 캐릭터: ref-thales.png 를 가장 먼저 생성 → S1·S2·S3·S5 에 전달(일관성)
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

STYLE = ("STYLE: cinematic painterly illustration, ancient Greece and ancient Egypt (BCE 6th century), "
    "bright Mediterranean / desert sun, palette of terracotta, ochre, bronze and khaki-gold (#A89368), "
    "weathered stone, sand, olive trees and the great pyramids, long cast shadows, 16:9 aspect ratio, "
    "NO text, NO letters, NO numerals, NO modern objects (except the single modern scene S6 as noted), "
    "ample empty space for caption overlay, historically accurate (Greek himation robes; a plain wooden "
    "measuring staff / gnomon; Egyptian pyramids; Milesian harbour).")
CHAR = ("Thales of Miletus: an ancient Greek sage in his 60s, short neat grey-white beard, sun-tanned "
    "skin, wearing a khaki-gold (#A89368) Greek himation robe, holding a plain straight wooden measuring "
    "staff, deep thoughtful contemplative eyes, calm wise expression, warm sunlight.")

REF = OUT / "ref-thales.png"
HEADROOM = ("IMPORTANT: frame so the ENTIRE head and face are fully visible with comfortable "
    "headroom ABOVE the head — do NOT crop the top of the head.")
PROMPTS = {
    # ① 신규 캐릭터 reference (가장 먼저 생성) — 후속 장면에 전달
    "ref-thales.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear view "
        f"of face, beard and clothing, holding the wooden staff, simple neutral warm background. "
        f"{HEADROOM} No text.", None),
    # ② S1 밀레토스 항구 + 별밤 (ref 전달)
    "S1.png": (f"{STYLE}\nUsing the SAME Thales character from the reference (same grey-white beard, "
        "khaki-gold himation, wooden staff): Thales standing on the shore of the ancient Greek harbour "
        "city of Miletus at dusk turning to night, olive trees and moored boats nearby, gazing up at a "
        "star-filled sky with a faint sense of ordered geometric patterns among the stars (myth giving "
        f"way to natural law). Warm twilight light. {HEADROOM} Empty space for caption. No text.", "REF"),
    # ③ S2 거대 피라미드 앞 작은 탈레스 (ref 전달)
    "S2.png": (f"{STYLE}\nUsing the SAME Thales character from the reference: an enormous Egyptian "
        "pyramid towering under bright desert sun, and at its base a SMALL figure of Thales looking up "
        "at it, dwarfed by its scale, long shadows on the sand — conveying the impossibility of "
        f"measuring such a height. {HEADROOM} Empty sky for caption. No text.", "REF"),
    # ④ S3 막대기 + 그림자 = 높이 (ref 전달, 핵심)
    "S3.png": (f"{STYLE}\nUsing the SAME Thales character from the reference: Thales beside a vertical "
        "wooden staff planted upright in the sand, the staff casting a long shadow exactly as long as "
        "the staff is tall, and beside it the great pyramid casting its own long shadow on the sand — "
        "the two shadows shown side by side, faint dotted guide lines suggesting that the pyramid's "
        "shadow length equals its height (measuring by shadow). Low golden sun. Do NOT render numerals "
        "or letters. Empty space for caption. No text.", "REF"),
    # ⑤ S4 닮은꼴 두 삼각형 (ref 불필요, 추상)
    "S4.png": (f"{STYLE}\nAn elegant conceptual image: on the left a SMALL right triangle formed by a "
        "wooden staff and its shadow, on the right a LARGE right triangle of the SAME shape formed by "
        "the pyramid and its shadow — same shape, different size (similar triangles). Parallel sunbeams "
        "from one direction emphasise the shared sun angle. Warm gold on sand and sky. Do NOT render "
        "numerals or letters. Empty space for caption. No text.", None),
    # ⑥ S5 정리 + 빈 두루마리 + 유클리드 계승 (ref 전달)
    "S5.png": (f"{STYLE}\nUsing the SAME Thales character from the reference: glowing simple geometric "
        "theorem figures floating in warm light (a circle bisected by its diameter, equal vertical "
        "angles, a triangle in a semicircle), an empty unwritten papyrus scroll beside Thales "
        "(his own writings lost), and faintly in the background a second younger Greek scholar (Euclid) "
        "receiving and continuing the scroll across the centuries. Reverent mood. Do NOT render "
        "numerals or letters. Empty space for caption. No text.", "REF"),
    # ⑦ S6 현대 학생 깃대 그림자 측량 (ref 불필요, 단 하나의 현대 장면)
    "S6.png": (f"STYLE: cinematic painterly illustration, present-day schoolyard, warm golden afternoon "
        "light, palette echoing terracotta and khaki-gold, 16:9 aspect ratio, NO text, NO letters, NO "
        "numerals, ample empty space for caption.\nA modern teenage student standing in a schoolyard "
        "next to a tall flagpole, pointing at the flagpole's long shadow on the ground while a small "
        "stick beside them casts its own shadow — measuring the flagpole's height by shadow, just as "
        "Thales did. A faint ghostly overlay of an ancient figure with a staff on sand bridges past and "
        "present. Large empty central space above for a single word overlay. No text, no letters.", None),
}

order = ["ref-thales.png", "S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
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
