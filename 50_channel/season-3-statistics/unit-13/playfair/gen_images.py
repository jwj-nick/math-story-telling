#!/usr/bin/env python3
# gen_images.py — unit-13 플레이페어(자료의 정리와 해석) Nano Banana (네이티브 16:9)
# ★신규 캐릭터: ref-playfair.png 를 가장 먼저 생성 → S1(+후속 인물 장면)에 reference 전달(일관성)
# era-modern 팔레트(#8E7E3C 올리브-카키 골드), 18~19C 스코틀랜드 엔지니어
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
                    print(f"  OK {pathlib.Path(out).name} ({len(p.inline_data.data)} bytes)", flush=True); return True
            print(f"  ! {pathlib.Path(out).name}: 이미지 없음 try {attempt}", flush=True)
        except Exception as e:
            print(f"  ERR {pathlib.Path(out).name} try {attempt}: {str(e)[:200]}", flush=True); time.sleep(3*attempt)
    return False

# era-modern: late-1700s/early-1800s industrial-era Britain, warm candlelight, olive-gold accent (#8E7E3C)
STYLE = ("STYLE: cinematic painterly illustration, late-1700s to early-1800s Georgian/industrial-era Britain, "
    "a scholar's study by candlelight, warm candle-amber against cool study shadow, palette "
    "olive-gold(#8E7E3C)/sepia-brown/parchment-cream/deep-charcoal, 16:9, NO text, NO letters, NO numerals, "
    "ample empty space for caption, historically accurate (Georgian frock coat, cravat, quill pen, ledgers, "
    "drafting tools, candlestick).")
DIAGRAM = ("STYLE: a clean minimal DATA-GRAPHIC, flat, centered, NO people, NO scene, NO landscape, dark warm "
    "charcoal background, glowing clean lines in olive-gold and amber, 16:9, cinematic but abstract, like an "
    "elegant antique chart figure. NO text, NO letters, NO numerals.")
# ★신규 캐릭터 — William Playfair
CHAR = ("William Playfair: a sharp, inventive Scottish engineer in his late 30s, short dark Georgian-era hair "
    "tied back, clean-shaven, a dark wool frock coat over a waistcoat and a white linen cravat at the neck, "
    "intelligent restless eyes, warm candlelight on his face.")
REF = OUT / "ref-playfair.png"
HEAD = "IMPORTANT: ENTIRE head and face visible with headroom ABOVE the head — do NOT crop the top."
PROMPTS = {
  "ref-playfair.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear face and "
    f"clothing, simple dark neutral background, holding a quill pen. {HEAD} No text.", None),
  "S1.png": (f"{STYLE}\nUsing the SAME William Playfair from reference: he sits at a wooden writing desk "
    "buried under towering stacks of dense commercial ledgers and endless columns of handwritten numbers "
    "(trade records), candlelight on his frustrated, thinking face, one hand on his brow — overwhelmed by "
    f"tables nobody reads. The ledger pages have NO readable text or numbers. {HEAD} Empty space for "
    "caption. No text, no numerals.", "REF"),
  "S2.png": (f"{DIAGRAM}\nDraw a clean BAR CHART: a row of separate upright rectangular bars of clearly "
    "different heights standing side by side on a baseline, glowing warm olive-gold and amber on the dark "
    "ground, the tallest bar prominent (numbers turned into lengths). No axes numbers, no text. Generous "
    "empty space above for a caption.", None),
  "S3.png": (f"{DIAGRAM}\nDraw a clean LINE CHART (time-series): a horizontal time axis and a vertical axis, "
    "a single bright zig-zag line of connected dots rising and falling across the frame showing a trend over "
    "time, glowing warm amber on the dark ground. No axes numbers, no text. Generous empty space above for a "
    "caption.", None),
  "S4.png": (f"{DIAGRAM}\nDraw a clean PIE CHART: a single circle divided into wedge-shaped sectors of "
    "different sizes (a whole split into proportional parts), each wedge a distinct warm color — a large "
    "olive-gold wedge, a medium amber wedge, smaller sepia and dark wedges — the proportions clearly varied. "
    "Elegant antique data graphic on a warm parchment-dark ground. NO text, NO numerals. Empty space for "
    "caption.", None),
  "S5.png": (f"STYLE: an elegant late-1700s engraving-style data graphic plate, aged parchment / sepia and "
    "olive-gold ink, fine engraved lines, 16:9, antique. Draw THREE classic charts together on the plate: a "
    "BAR chart (several upright bars), a LINE chart (a rising and falling connected line), and a PIE chart (a "
    "circle split into colored sectors) — the three inventions of William Playfair, arranged together. NO "
    "readable text, NO numerals. Empty space for caption.", None),
  "S6.png": (f"{DIAGRAM}\nA warm montage on the FAR LEFT THIRD of the frame: a small glowing bar chart, a "
    "little line chart, and a little pie chart clustered together, and beside them a tiny rose/coxcomb "
    "diagram (Nightingale's descendant), softly radiant in olive-gold and amber; leave the entire RIGHT "
    "TWO-THIRDS as deep dark empty space with NOTHING in it, reserved for a single word overlay. Warm "
    "olive-gold on near-black. NO text, NO numerals.", None),
}
order = ["ref-playfair.png","S1.png","S2.png","S3.png","S4.png","S5.png","S6.png"]
if len(sys.argv) > 1: order = sys.argv[1:]
fail = []
for name in order:
    prompt, ref = PROMPTS[name]; out = OUT / name
    if out.exists() and out.stat().st_size > 0: print(f"  = {name} skip", flush=True); continue
    if not gen(prompt, out, ref_paths=[str(REF)] if ref == "REF" else None): fail.append(name)
print("== DONE ==" if not fail else f"== 실패: {fail} ==", flush=True)
