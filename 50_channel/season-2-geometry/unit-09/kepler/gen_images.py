#!/usr/bin/env python3
# gen_images.py — unit-09 케플러(테셀레이션) Nano Banana (네이티브 16:9)
# ★ S1·S6 = u06 ref-kepler.png 를 reference 로 전달 → 동일 인물 일관성
import os, sys, pathlib, time
from google import genai
from google.genai import types

HERE = pathlib.Path(__file__).parent
OUT = HERE / "5-images"; OUT.mkdir(exist_ok=True)
# u06 확정 케플러 얼굴 reference (캐릭터 재사용)
REF_KEPLER = (HERE / ".." / ".." / ".." / "season-1-ancient" / "unit-06" / "kepler"
              / "5-images" / "ref-kepler.png").resolve()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash-image"

def gen(prompt, out, ref_paths=None):
    contents = [prompt]
    if ref_paths:
        for rp in ref_paths:
            contents.append(types.Part.from_bytes(data=pathlib.Path(rp).read_bytes(), mime_type="image/png"))
    for attempt in range(1, 6):
        try:
            resp = client.models.generate_content(model=MODEL, contents=contents,
                config=types.GenerateContentConfig(response_modalities=['Text', 'Image'],
                    image_config=types.ImageConfig(aspect_ratio="16:9")))
            for p in resp.candidates[0].content.parts:
                if getattr(p, "inline_data", None) and p.inline_data.data:
                    pathlib.Path(out).write_bytes(p.inline_data.data)
                    print(f"  OK {pathlib.Path(out).name} ({len(p.inline_data.data)} bytes)", flush=True); return True
            print(f"  ! {pathlib.Path(out).name}: no image try {attempt}", flush=True)
        except Exception as e:
            msg = str(e)[:200]
            print(f"  ERR {pathlib.Path(out).name} try {attempt}: {msg}", flush=True)
            # 429 rate-limit backoff
            wait = 8 * attempt if "429" in msg or "RESOURCE_EXHAUSTED" in msg else 3 * attempt
            time.sleep(wait)
    return False

STYLE = ("STYLE: cinematic painterly illustration, early 17th-century astronomer's candle-lit "
    "study/observatory at night, deep starry night-blue, palette night-blue/brass/candle-gold/brown, "
    "a brass armillary sphere present, 16:9, NO text, NO letters, NO numerals, NO modern objects, "
    "ample empty space for a caption, historically accurate (white ruff collar, dark scholarly gown, "
    "brass astronomical instruments, candlelight).")
KEPLER = ("Johannes Kepler: a 17th-century German astronomer in his 40s, short curly brown hair and "
    "beard, a white ruff collar over a dark gown, a warm thoughtful expression. Keep the SAME face "
    "and clothing as the reference portrait.")
HEAD = "IMPORTANT: ENTIRE head and face visible with headroom ABOVE the head — do NOT crop the top."

PROMPTS = {
  "S1.png": (f"{STYLE}\nUsing the SAME Kepler from the reference image (same face, curly brown hair, "
    "white ruff collar, dark gown): Kepler standing in his candle-lit observatory at night beside a "
    "large brass armillary sphere, a window of stars behind him, and on his desk a sketch of regular "
    f"polygon tiles fitting together. {HEAD} Empty space for a caption. No text.", "REF"),
  "S2.png": (f"{STYLE}\nAn abstract warm image: a flat plane perfectly covered by identical regular "
    "hexagons (like a honeycomb / bathroom tiling) with NO gaps and NO overlaps, glowing brass-gold "
    "tiles on a warm dark ground, suggesting tessellation of the plane. Do NOT render numerals or "
    "letters. Empty space for caption. No text.", None),
  "S3.png": (f"{STYLE}\nAn abstract geometry image: at a single meeting point, several polygon corner "
    "angles (colored wedges) come together and exactly complete one full circle (one full turn / 360 "
    "degrees), shown as wedges filling a perfect circle with no gap and no overlap. Brass-gold on deep "
    "night-blue. Do NOT render numerals or letters. Empty space for caption. No text.", None),
  "S4.png": (f"{STYLE}\nAn abstract image divided into three calm panels showing three different "
    "tessellations meeting at a point: left = six equilateral triangles around one point, middle = "
    "four squares around one point, right = three regular hexagons around one point, each set "
    "completing a full turn with no gap. Glowing brass-gold tiles on dark. Do NOT render numerals or "
    "letters. Empty space for caption. No text.", None),
  "S5.png": (f"{STYLE}\nAn abstract image: regular pentagons trying to meet at a single point but "
    "failing — three pentagons leave an awkward empty wedge-shaped GAP between them (and a faint hint "
    "that four would overlap), conveying that pentagons cannot tile the plane by themselves. Slightly "
    "uneasy, off-balance composition, brass-gold pentagons on deep dark blue. Do NOT render numerals "
    "or letters. Empty space for caption. No text.", None),
  "S6.png": (f"{STYLE}\nUsing the SAME Kepler from the reference image (same face and clothing): Kepler "
    "beside his brass armillary sphere, with glowing planetary orbits arcing in the starry sky ABOVE "
    "him and a floor of regular-polygon tessellation tiles glowing BELOW him — the heavens and the "
    f"ground sharing one geometry. Warm reverent finale glow. {HEAD} Large empty space above for a "
    "single-word caption. No text, no numerals.", "REF"),
}
order = ["S1.png","S2.png","S3.png","S4.png","S5.png","S6.png"]
if len(sys.argv) > 1: order = sys.argv[1:]
print(f"ref-kepler: {REF_KEPLER} exists={REF_KEPLER.exists()}", flush=True)
fail = []
for name in order:
    prompt, ref = PROMPTS[name]; out = OUT / name
    if out.exists() and out.stat().st_size > 0: print(f"  = {name} skip", flush=True); continue
    if not gen(prompt, out, ref_paths=[str(REF_KEPLER)] if ref == "REF" else None): fail.append(name)
    time.sleep(2)  # gentle pacing for Tier1
print("== DONE ==" if not fail else f"== FAIL: {fail} ==", flush=True)
