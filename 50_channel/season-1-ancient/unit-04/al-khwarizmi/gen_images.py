#!/usr/bin/env python3
# gen_images.py — unit-04 알콰리즈미(secondary) Nano Banana (se-video-image §IM6, 네이티브 16:9)
# ★ ref = u03 알콰리즈미 얼굴 재사용 (../../unit-03-al-khwarizmi/5-images/ref-alkhwarizmi.png)
#   → S2(인물 등장)·S6(이어달리기 실루엣)에 전달 = u02·u03 과 동일 인물 얼굴 일관. 새 ref 생성 X.
# 개념 각도: 옮김(이항)·상쇄(동류항)·6유형 절차 = u03 "균형/저울" 과 차별.
import os, sys, pathlib, time
from google import genai
from google.genai import types

HERE = pathlib.Path(__file__).parent
OUT = HERE / "5-images"; OUT.mkdir(exist_ok=True)
# u03 알콰리즈미 얼굴 ref (동일 인물 일관). 절대/상대 모두 대비해 resolve.
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
    "white turban and a deep teal-and-sandstone scholar's robe, calm intelligent serene expression, "
    "warm lamplight on the face. KEEP THE SAME FACE as the reference image.")
HEADROOM = ("IMPORTANT: frame him so his ENTIRE head and face are fully visible with comfortable "
    "headroom (empty space) ABOVE his head — do NOT crop the top of his head.")

PROMPTS = {
    # S1: 지혜의 집 + 동에서 온 빛나는 두루마리(디오판토스 책 callback). 인물 X → ref 불필요
    "S1.png": (f"{STYLE}\nWide establishing shot of the House of Wisdom in 9th-century Baghdad: "
        "grand horseshoe arches, intricate turquoise geometric tilework, a dome, stacks of books "
        "and an astrolabe, two or three robed scholars translating by golden lamplight. On one "
        "side, a single Greek parchment scroll glowing softly as if newly arrived from the WEST "
        "(Alexandria, Egypt). Vast warm interior with space in the upper third for caption. "
        "No text, no numerals.", None),
    # S2: 알콰리즈미 인물 + 항이 등호 건너 옮겨지는 추상(이항). ★ ref 전달
    "S2.png": (f"{STYLE}\n{CHAR}\nA 16:9 WIDE upper-body shot of Al-Khwarizmi (USE THE SAME FACE, "
        "same black beard, same white turban and teal robe as the reference image) seated at a desk "
        "with parchment, gesturing with one hand as if MOVING a small glowing block from one side "
        "of an empty stone table to the OTHER side across a faint central dividing line (suggesting "
        "transposition / moving a term across an equals sign — render NO actual symbols, only the "
        "abstract sense of an object carried across). Blurred House of Wisdom interior behind "
        f"(shallow depth of field). {HEADROOM} Keep generous empty space to one side for caption. "
        "No text, no numerals.", "REF"),
    # S3: 양쪽 같은 블록 상쇄(동류항). 추상, 인물 X
    "S3.png": (f"{STYLE}\nAbstract minimal composition centered on a stone table: a faint central "
        "vertical dividing line (an equals line), with a matching PAIR of identical small glowing "
        "geometric blocks — one on each side — beginning to dissolve and vanish together "
        "simultaneously (the idea of cancelling identical things on both sides). The remaining "
        "arrangement looks cleaner and shorter. Dramatic warm side light, Islamic geometric pattern "
        "faintly in the background. Uncluttered, with empty space above for caption. "
        "No text, no numerals.", None),
    # S4: 흩어진 식이 정해진 유형·단계로 분류(알고리즘). 추상, 인물 X
    "S4.png": (f"{STYLE}\nAbstract sense of order emerging from chaos: scattered small glowing "
        "fragments on the left being sorted by gentle directional light into a few NEAT ORGANIZED "
        "groups on the right, then flowing down a clean ordered staircase / orderly path of steps "
        "(suggesting fixed procedures, an algorithm). Warm directional light moving left-to-right. "
        "Convey classification and step-by-step order with light and arrangement only — render NO "
        "numerals, NO letters. Empty space for caption. No text.", None),
    # S5: 좌 긴 절차서 양피지 ↔ 우 짧은 한 줄(축 C). 인물 X
    "S5.png": (f"{STYLE}\nA 16:9 split composition contrasting two ways of writing a method. LEFT "
        "half: an old parchment densely filled with long flowing handwritten paragraphs (a "
        "step-by-step procedure written entirely in words, NO symbols, NO legible letters — just "
        "the texture of dense prose), warm candlelight, a scholar's hand resting near it. RIGHT "
        "half: a clean bright modern surface nearly empty, suggesting a single short concise line "
        "(render NO actual letters or symbols). Clear vertical division. The contrast of a long "
        "prose procedure vs one short line. No legible text, no numerals.", None),
    # S6: 동→서 세 학자 실루엣 이어달리기 + 옮김 화살표. ★ ref 전달(알콰리즈미 동일 인물)
    "S6.png": (f"{STYLE}\nA warm cinematic sense of a relay across centuries: three faint robed "
        "scholar silhouettes in succession from WEST/east to west (Alexandria, then Baghdad — this "
        "MIDDLE scholar should clearly resemble the SAME Al-Khwarizmi face from the reference image, "
        "in white turban and teal robe — then Europe), faces mostly in shadow. In the foreground "
        "center, two faint glowing curved arrows arcing across a central dividing line as if "
        "carrying something from one side to the other (the idea of moving a term across an equals "
        "sign). Large empty central space above for a single word overlay. Hopeful, unifying mood. "
        "No text, no letters, no numerals.", "REF"),
}

order = ["S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
if len(sys.argv) > 1:
    order = sys.argv[1:]
if not REF.exists():
    print(f"  !! ref 없음: {REF} (u03 알콰리즈미 ref 필요 — S2/S6 일관성)", flush=True)
fail = []
for name in order:
    prompt, ref = PROMPTS[name]
    out = OUT / name
    if out.exists() and out.stat().st_size > 0:
        print(f"  = {name} 존재, skip", flush=True); continue
    ok = gen(prompt, out, ref_paths=[str(REF)] if ref == "REF" else None)
    if not ok: fail.append(name)
print("== DONE ==" if not fail else f"== 실패: {fail} ==", flush=True)
