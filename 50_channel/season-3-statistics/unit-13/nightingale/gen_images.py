#!/usr/bin/env python3
# gen_images.py — unit-13 나이팅게일(자료의 정리와 해석) Nano Banana (네이티브 16:9)
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

STYLE = ("STYLE: cinematic painterly illustration, mid-1800s Victorian era, Crimean War British military "
    "hospital, warm lamplight against cool night blue, palette amber-gold/slate-blue/white-linen/dark-wood, "
    "16:9, NO text, NO letters, NO numerals, NO modern objects, ample empty space for caption, "
    "historically accurate (Victorian nurse dress, oil lamp, iron beds).")
DIAGRAM = ("STYLE: a clean minimal DATA-GRAPHIC, flat, centered, NO people, NO scene, NO landscape, dark warm "
    "charcoal background, glowing clean lines, 16:9, cinematic but abstract, like an elegant chart figure. "
    "NO text, NO letters, NO numerals.")
CHAR = ("Florence Nightingale: a calm, resolute Victorian woman in her 30s, dark hair parted and pinned back, "
    "a white lace cap and a dark high-necked nurse's dress, gentle but determined eyes, warm lamplight.")
REF = OUT / "ref-nightingale.png"
HEAD = "IMPORTANT: ENTIRE head and face visible with headroom ABOVE the head — do NOT crop the top."
PROMPTS = {
  "ref-nightingale.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear face and "
    f"clothing, simple dark neutral background, holding a small oil lamp. {HEAD} No text.", None),
  "S1.png": (f"{STYLE}\nUsing the SAME Florence Nightingale from reference: at night she walks down a long "
    "row of iron hospital beds with wounded soldiers, holding a glowing oil lamp that lights her face, the "
    f"ward dim and somber, a sense of quiet resolve. {HEAD} Empty space for caption. No text, no numerals.", "REF"),
  "S2.png": (f"{STYLE}\nUsing the SAME Florence Nightingale from reference: seated at a wooden desk by "
    "lamplight, carefully sorting many small loose record slips into the neat ruled rows and columns of a "
    "large ledger / table (organizing scattered records into orderly groups). Focus on her hands and the "
    f"ledger grid (the grid has NO readable text or numbers). {HEAD} Empty space for caption.", "REF"),
  "S3.png": (f"{DIAGRAM}\nDraw a clean HISTOGRAM: a row of adjacent vertical bars of different heights side by "
    "side (tallest in the middle, shorter at the sides, a bell-like shape), glowing warm amber-gold on the "
    "dark ground; then a thin bright line connecting the top-centers of the bars (a frequency polygon). "
    "No axes numbers, no text. Generous empty space above for a caption.", None),
  "S4.png": (f"{DIAGRAM}\nDraw Florence Nightingale's famous polar-area 'rose' diagram (coxcomb chart): a "
    "circular diagram made of wedge-shaped segments radiating from the center like petals of a rose, the "
    "wedges colored — large pale BLUE wedges (deaths from disease), smaller RED wedges (deaths from wounds), "
    "and small dark wedges (other) — the blue area clearly dominating. Elegant Victorian data graphic on a "
    "warm parchment-dark ground. NO text, NO numerals. Empty space for caption.", None),
  "S5.png": (f"STYLE: an elegant late-1700s engraving-style data graphic plate, aged parchment / sepia and "
    "ink, fine engraved lines, 16:9, antique. Draw THREE classic charts together on the plate: a BAR chart "
    "(several vertical bars), a LINE chart (a rising and falling curve), and a PIE chart (a circle split "
    "into colored sectors) — the three inventions of William Playfair. NO readable text, NO numerals. Empty "
    "space for caption.", None),
  "S6.png": (f"{DIAGRAM}\nA warm montage on the FAR LEFT THIRD of the frame: a small glowing rose/coxcomb "
    "diagram, a little bar chart and a little pie chart clustered together, softly radiant; leave the entire "
    "RIGHT TWO-THIRDS as deep dark empty space with NOTHING in it, reserved for a single word overlay. Warm "
    "amber-gold on near-black. NO text, NO numerals.", None),
}
order = ["ref-nightingale.png","S1.png","S2.png","S3.png","S4.png","S5.png","S6.png"]
if len(sys.argv) > 1: order = sys.argv[1:]
fail = []
for name in order:
    prompt, ref = PROMPTS[name]; out = OUT / name
    if out.exists() and out.stat().st_size > 0: print(f"  = {name} skip", flush=True); continue
    if not gen(prompt, out, ref_paths=[str(REF)] if ref == "REF" else None): fail.append(name)
print("== DONE ==" if not fail else f"== 실패: {fail} ==", flush=True)
