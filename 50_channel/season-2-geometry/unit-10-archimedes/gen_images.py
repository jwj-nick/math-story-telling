#!/usr/bin/env python3
# gen_images.py — unit-10 아르키메데스(원과 부채꼴) Nano Banana (네이티브 16:9)
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

STYLE = ("STYLE: cinematic painterly illustration, ancient Greek city of Syracuse in Sicily (3rd century "
    "BC), warm Mediterranean afternoon light, palette terracotta/ochre/bronze/olive-green and deep sea "
    "blue, marble columns and a sandy tray for drawing, 16:9, NO text, NO letters, NO numerals, NO "
    "modern objects, ample empty space for caption, historically accurate (Greek himation robes).")
STYLE_CN = ("STYLE: cinematic painterly illustration, ancient China, 3rd century AD (Three Kingdoms / "
    "Wei dynasty era), warm lamplight in a scholar's study, palette deep red/ink-black/bamboo-green/gold, "
    "bamboo writing slips (jiandu) and ink brushes, 16:9, NO text, NO letters, NO numerals, NO modern "
    "objects, ample empty space for caption, historically accurate Han-Chinese scholar robes.")
CHAR = ("Archimedes: an ancient Greek sage in his 70s, long white beard, weathered tanned face, simple "
    "off-white himation robe, intense focused thoughtful eyes, kneeling over a flat sand tray, warm light.")
REF = OUT / "ref-archimedes.png"
HEAD = "IMPORTANT: ENTIRE head and face visible with headroom ABOVE the head — do NOT crop the top."
PROMPTS = {
  "ref-archimedes.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear face and "
    f"clothing, simple neutral warm background. {HEAD} No text.", None),
  "S1.png": (f"{STYLE}\nUsing the SAME Archimedes from reference (white beard, himation): the old "
    "Archimedes kneeling over a sand tray in a sunlit Syracuse courtyard by the sea, drawing a perfect "
    "circle in the sand with a stick, a few rolled papyrus letters beside him, marble columns and blue "
    f"Mediterranean behind. {HEAD} Empty space for caption. No text.", "REF"),
  "S2.png": ("STYLE: a clean minimal GEOMETRY DIAGRAM, flat, centered, NO people, NO scene, NO landscape, "
    "dark warm charcoal background, glowing thin gold and bronze lines only, 16:9, cinematic but abstract.\n"
    "Draw EXACTLY this: one perfect circle outline (its rim brightly glowing as the circumference), a "
    "small bright dot at the exact center, one straight thin line from the center dot to the rim (a "
    "radius), and one straight thin line passing through the center from one side of the rim to the other "
    "(a diameter). The inside of the circle stays dark. Clean, elegant, like a geometry textbook figure. "
    "Do NOT render any numerals or letters. Generous empty dark space at top and bottom for captions. No text.", None),
  "S3.png": ("STYLE: a clean minimal GEOMETRY DIAGRAM, flat, centered, NO people, NO scene, NO landscape, "
    "dark warm charcoal background, glowing thin gold and bronze lines only, 16:9, cinematic but abstract.\n"
    "Draw EXACTLY this: one perfect circle in the center; a regular polygon with many sides drawn INSIDE "
    "the circle touching it from within (inscribed); and a second regular polygon with many sides drawn "
    "OUTSIDE the circle enclosing it (circumscribed) — so the single circle is clearly sandwiched between "
    "an inner polygon and an outer polygon, all three nearly the same shape because the polygons have many "
    "sides and hug the circle tightly. The inner polygon a slightly different glow than the outer. A clear "
    "sense of squeezing toward the true circle from both sides. Do NOT render any numerals or letters. "
    "Large empty space at top and bottom for caption. No text.", None),
  "S4.png": (f"{STYLE_CN}\nA Chinese scholar (Liu Hui) in his 40s, calm and focused, sitting at a low desk "
    "in lamplight, unrolling bamboo writing slips, and on the desk a drawing of a circle with a polygon "
    "of very many tiny sides inscribed in it (finely subdivided, almost merging with the circle). "
    f"{HEAD} Empty space for caption. No text, no numerals.", None),
  "S5.png": (f"{STYLE}\nA glowing golden circle divided into pie-like sectors radiating from the center, "
    "with ONE sector clearly highlighted brighter — bounded by two straight radii and a curved arc, like "
    "a fan (a circular sector). Warm gold on dark ground. Do NOT render numerals or letters. Empty space "
    "for caption. No text.", None),
  "S6.png": (f"{STYLE}\nUsing the SAME Archimedes from reference: a somber dramatic dusk scene. COMPOSITION "
    "is important — place the old Archimedes kneeling protectively over his circle in the sand on the FAR "
    "LEFT THIRD of the frame only, and leave the entire RIGHT TWO-THIRDS as a vast empty deep-blue and "
    "dark dusk sky over the sea (fall of Syracuse, golden sunset fading to dark night), with NOTHING in "
    f"that right area. {HEAD} The large empty dark-sky right side is reserved for a single word overlay. "
    "No text, no numerals.", "REF"),
}
order = ["ref-archimedes.png","S1.png","S2.png","S3.png","S4.png","S5.png","S6.png"]
if len(sys.argv) > 1: order = sys.argv[1:]
fail = []
for name in order:
    prompt, ref = PROMPTS[name]; out = OUT / name
    if out.exists() and out.stat().st_size > 0: print(f"  = {name} skip", flush=True); continue
    if not gen(prompt, out, ref_paths=[str(REF)] if ref == "REF" else None): fail.append(name)
print("== DONE ==" if not fail else f"== 실패: {fail} ==", flush=True)
