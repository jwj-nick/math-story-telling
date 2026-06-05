#!/usr/bin/env python3
# gen_images.py — unit-08 가우스(작도가능성) Nano Banana (네이티브 16:9)
# ★ 신규 캐릭터: ref-gauss.png 를 가장 먼저 생성 → S3(ref="REF")에 전달해 가우스 얼굴 일관성.
# era-modern: 18-19C 독일, 슬레이트블루(#3E5A6E)·촛불. 유클리드 작도 전통은 도구/도형으로만 연결.
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

# era-modern (가우스): late-18th/early-19th-century Germany, slate-blue + candle-gold + brown
STYLE = ("STYLE: cinematic painterly illustration, late-18th to early-19th-century Germany, a quiet "
    "candle-lit study, palette slate-blue (#3E5A6E) / candle-gold / warm brown, weathered wood and "
    "paper, 16:9, NO text, NO letters, NO numerals, NO modern objects, ample empty space for caption, "
    "historically accurate (a wooden compass and an unmarked straightedge; period paper with geometric "
    "figures).")
# era-ancient 잔향 (S1만): 그리스 작도 전통의 도구·도형
STYLE_ANCIENT = ("STYLE: cinematic painterly illustration transitioning from ancient-Greek warmth "
    "(terracotta/ochre, papyrus) toward a cooler slate-blue mood, 16:9, NO text NO letters NO numerals "
    "NO modern objects, ample caption space, a wooden compass and an unmarked straightedge.")
GAUSS = ("Carl Friedrich Gauss as a serious, passionate German youth of about nineteen, short brown "
    "hair, a simple late-18th-century white shirt and dark coat, calm intense eyes, bright with quiet "
    "discovery.")
HEAD = ("IMPORTANT: frame so the ENTIRE head and face are fully visible with headroom ABOVE the head "
    "— do NOT crop the top of the head.")

REF = OUT / "ref-gauss.png"
PROMPTS = {
    # ① 신규 캐릭터 reference (가장 먼저 생성)
    "ref-gauss.png": (f"{STYLE}\n{GAUSS}\nComposition: front-facing reference portrait, clear view of "
        f"face and clothing, seated at a candle-lit wooden desk, simple neutral background. {HEAD} No text.", None),
    # ② S1 — 두 도구의 오랜 질문 (인물 없음, 작도 전통 도구/도형)
    "S1.png": (f"{STYLE_ANCIENT}\nA wooden compass and an unmarked straightedge resting on aged paper, "
        "having drawn a clean regular triangle and a regular pentagon (abstract geometric figures, no "
        "numerals), a faint air of an unanswered question lingering above — how far can these two tools "
        "reach? Empty space for caption. No text, no numerals.", None),
    # ③ S2 — 막힌 벽 (정3·4·5·15 빛남, 그 위는 어두운 벽)
    "S2.png": (f"{STYLE}\nAn abstract image: a few regular polygons (a triangle, a square, a pentagon) "
        "glowing in warm gold at the bottom, and ABOVE them a dark, impassable stone-like wall blocking "
        "further regular polygons in shadow — a sense of a limit no one could cross for two thousand "
        "years. Do NOT render numerals or letters. Empty space for caption. No text.", None),
    # ④ S3 — 열아홉 살 가우스 정십칠각형 (★ ref-gauss 전달)
    "S3.png": (f"{STYLE}\nUsing the SAME young Gauss from the reference (short brown hair, white shirt "
        "and dark coat): the nineteen-year-old Gauss at his candle-lit wooden desk at dawn, having just "
        "drawn a regular polygon with many equal sides (a regular seventeen-sided figure) using a wooden "
        "compass and an unmarked straightedge, an open diary beside him, his face bright with the joy of "
        f"discovery. {HEAD} Empty space for caption. No text, no numerals.", "REF"),
    # ⑤ S4 — 가능/불가능 경계
    "S4.png": (f"{STYLE}\nAn abstract image of constructibility: on one side several regular polygons "
        "glowing in clear gold (POSSIBLE), on the other side regular polygons rendered in cold grey and "
        "faded (IMPOSSIBLE), with a sharp luminous boundary line cleanly separating the two groups — the "
        "first drawn line between possible and impossible. Do NOT render numerals or letters. Empty space "
        "for caption. No text.", None),
    # ⑥ S5 — 한계를 아는 힘 (헛수고 → 명확한 길)
    "S5.png": (f"{STYLE}\nAn abstract, warm image: on the left, faint tangled grey lines of futile, "
        "repeated failed attempts; on the right these resolve into a single clear, confident path / a "
        "clean map glowing gold — knowing the limit turns vague impossibility into a clear map. Do NOT "
        "render numerals or letters. Empty space for caption. No text.", None),
    # ⑦ S6 — 같은 도구 새 질문 (마무리)
    "S6.png": (f"{STYLE}\nA warm finale: a wooden compass and an unmarked straightedge crossed, and above "
        "them a single glowing regular many-sided polygon (seventeen sides) radiating light, a sense of "
        "an old tool answering a brand-new question. Large empty central space above for a single word "
        "overlay. No text, no numerals.", None),
}

# ★ ref-gauss.png 가 반드시 가장 먼저 (S3 가 이를 ref로 사용)
order = ["ref-gauss.png", "S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
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
