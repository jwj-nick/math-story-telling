#!/usr/bin/env python3
# gen_images.py — unit-10 류후이(원주율 정밀화·할원술) Nano Banana (네이티브 16:9)
# ★ 류후이 = 신규 캐릭터: order 첫 항목 ref-liuhui.png 먼저 생성 → S1/S6 인물 장면에 reference 전달(얼굴 일관성).
# era-ancient(중국 위나라, 3C): 죽간(bamboo slips)·등잔불 서재·#A04D4D 톤. STYLE_CN.
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
                config=types.GenerateContentConfig(response_modalities=['Text', 'Image'],
                    image_config=types.ImageConfig(aspect_ratio="16:9")))
            for p in resp.candidates[0].content.parts:
                if getattr(p, "inline_data", None) and p.inline_data.data:
                    pathlib.Path(out).write_bytes(p.inline_data.data)
                    print(f"  ✓ {pathlib.Path(out).name} ({len(p.inline_data.data)} bytes)", flush=True); return True
            print(f"  ! {pathlib.Path(out).name}: 이미지 없음 try {attempt}", flush=True)
        except Exception as e:
            print(f"  ERR {pathlib.Path(out).name} try {attempt}: {str(e)[:200]}", flush=True); time.sleep(3*attempt)
    return False

# 중국 위나라(3세기) 학자 서재 톤 — 죽간·등잔불·먹·#A04D4D 계열
STYLE_CN = ("STYLE: cinematic painterly illustration, ancient China, 3rd century AD (Three Kingdoms / Wei "
    "dynasty era), warm oil-lamp light in a scholar's study at night, palette deep crimson-red (#A04D4D) / "
    "ink-black / bamboo-green / muted gold, bamboo writing slips (jiandu) bound with cord, ink brushes and "
    "an inkstone, low wooden desk, 16:9, NO text, NO letters, NO numerals, NO modern objects, ample empty "
    "space for caption, historically accurate Han-Chinese scholar robes.")
# 사람 없는 기하 다이어그램 톤 (아르키메데스 템플릿 패턴, era-ancient 中 톤으로 살짝 붉게)
STYLE_DIAGRAM = ("STYLE: a clean minimal GEOMETRY DIAGRAM, flat, centered, NO people, NO scene, NO landscape, "
    "dark warm charcoal background with a faint crimson tone, glowing thin gold and warm-red lines only, "
    "16:9, cinematic but abstract.")

CHAR = ("Liu Hui: a Chinese scholar of the Wei dynasty in his 40s, calm and thoughtful focused eyes, neat "
    "dark topknot hair with a simple scholar's headcloth, thin mustache and short beard, wearing a deep "
    "crimson-and-charcoal Han-Chinese scholar robe, seated by an oil lamp.")
REF = OUT / "ref-liuhui.png"
HEAD = "IMPORTANT: ENTIRE head and face visible with headroom ABOVE the head — do NOT crop the top."

PROMPTS = {
  # ★ 신규 캐릭터 reference — 가장 먼저 생성, 이후 S1/S6에 전달
  "ref-liuhui.png": (f"{STYLE_CN}\n{CHAR}\nComposition: front-facing reference portrait, clear face and "
    f"clothing, simple neutral warm-dark background. {HEAD} No text.", None),
  # S1: 동일 류후이가 죽간에 옛 책 주석을 다는 서재 장면
  "S1.png": (f"{STYLE_CN}\nUsing the SAME Liu Hui from the reference image (same face, topknot, crimson "
    "robe): the scholar Liu Hui seated at a low desk by warm oil-lamp light at night, unrolling a long "
    "bamboo-slip book (jiandu) across the desk, an ink brush in hand pausing thoughtfully as if questioning "
    f"a line, a circle faintly sketched on a slip. {HEAD} Empty space at the bottom for caption. No text.", "REF"),
  # S2: 원 구성요소 + 굽은 둘레 강조 (사람 없는 다이어그램)
  "S2.png": (f"{STYLE_DIAGRAM}\n"
    "Draw EXACTLY this: one perfect circle outline whose curved rim glows brightly to emphasize that the "
    "CIRCUMFERENCE is a CURVED line, a small bright dot at the exact center, and one straight thin line from "
    "the center dot to the rim (a radius). The contrast between the straight radius and the glowing curved "
    "rim is the point. The inside stays dark. Clean, elegant, like a geometry textbook figure. Do NOT render "
    "any numerals or letters. Generous empty dark space at top and bottom for captions. No text.", None),
  # S3: 할원술 — 다각형 변이 늘며 원에 합쳐짐
  "S3.png": (f"{STYLE_DIAGRAM}\n"
    "Draw EXACTLY this: one perfect circle in the center, with a sequence of regular polygons inscribed "
    "INSIDE it showing progressive subdivision — a hexagon, then a 12-gon, then a many-sided polygon — each "
    "with more sides hugging the circle more tightly, conveying the idea of cutting the circle into ever "
    "finer pieces until the polygon nearly MERGES with the circle. The finest polygon glows brightest, "
    "almost indistinguishable from the circle. A clear sense of approaching the true circle from within. "
    "Do NOT render any numerals or letters. Large empty space at top and bottom for caption. No text.", None),
  # S4: 다각형이 원과 거의 합쳐진 다이어그램 (정밀화 결과)
  "S4.png": (f"{STYLE_DIAGRAM}\n"
    "Draw EXACTLY this: one perfect circle with a regular polygon of very many tiny sides inscribed so "
    "finely that it is ALMOST indistinguishable from the circle itself — the polygon and circle nearly one "
    "single glowing ring. A serene sense of a precise value reached. Do NOT render any numerals or letters. "
    "Generous empty dark space at the bottom for caption. No text.", None),
  # S5: 조충지 — 또 다른 중국 학자(다른 인물), 더 미세한 원 분할 (ref 없음, 다른 사람)
  "S5.png": (f"{STYLE_CN}\nA DIFFERENT Chinese scholar (Zu Chongzhi, NOT the same man as the reference) — an "
    "elderly scholar in his 60s with a long grey beard, seated by lamplight, leaning over bamboo slips on "
    "which a circle is divided into an even FINER polygon of many more tiny sides than before, carrying on a "
    f"continued tradition. {HEAD} Empty space at the bottom for caption. No text, no numerals.", None),
  # S6: 황혼 서재, 주석가 류후이 — 우측 여백(한 단어 "더 잘게")
  "S6.png": (f"{STYLE_CN}\nUsing the SAME Liu Hui from the reference image: a quiet contemplative dusk scene "
    "in his study. COMPOSITION is important — place Liu Hui seated with a brush, hand resting over the "
    "bamboo-slip book, on the FAR LEFT THIRD of the frame only, and leave the entire RIGHT TWO-THIRDS as a "
    "vast empty deep dark-crimson and shadowed wall, with NOTHING in that right area. "
    f"{HEAD} The large empty dark right side is reserved for a single word overlay. No text, no numerals.", "REF"),
}
order = ["ref-liuhui.png","S1.png","S2.png","S3.png","S4.png","S5.png","S6.png"]
if len(sys.argv) > 1: order = sys.argv[1:]
fail = []
for name in order:
    prompt, ref = PROMPTS[name]; out = OUT / name
    if out.exists() and out.stat().st_size > 0: print(f"  = {name} skip", flush=True); continue
    if not gen(prompt, out, ref_paths=[str(REF)] if ref == "REF" else None): fail.append(name)
print("== DONE ==" if not fail else f"== 실패: {fail} ==", flush=True)
