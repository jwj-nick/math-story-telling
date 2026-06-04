#!/usr/bin/env python3
# gen_images.py — unit-11 케플러(Mysterium Cosmographicum) Nano Banana (네이티브 16:9)
# 캐릭터 일관성: u06 ref-kepler.png 재사용 (S1/S6 에 ref 전달). 5정다면체 정확.
import os, sys, pathlib, time, shutil
from google import genai
from google.genai import types

HERE = pathlib.Path(__file__).parent
OUT = HERE / "5-images"; OUT.mkdir(exist_ok=True)
# u06 ref-kepler.png 재사용 (생성 X) — 동일 인물 일관성
SRC_REF = pathlib.Path("C:/Kids/math-story-telling/50_channel/season-1-ancient/unit-06/kepler/5-images/ref-kepler.png")
REF = OUT / "ref-kepler.png"
if not REF.exists() and SRC_REF.exists():
    shutil.copy(SRC_REF, REF); print(f"  copied ref-kepler.png from u06", flush=True)

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
            print(f"  ! {pathlib.Path(out).name}: 이미지 없음 try {attempt}", flush=True)
        except Exception as e:
            msg = str(e)[:200]
            print(f"  ERR {pathlib.Path(out).name} try {attempt}: {msg}", flush=True)
            # 429 rate-limit backoff (Tier1)
            wait = 30 * attempt if "429" in msg or "RESOURCE_EXHAUSTED" in msg else 3 * attempt
            time.sleep(wait)
    return False

STYLE_MODERN = ("STYLE: cinematic painterly illustration, early-1600s European astronomer's study by "
    "candlelight, palette deep brown/brass-gold/ink-blue, brass astronomical instruments, telescope and "
    "parchment, leather books, 16:9, NO text, NO letters, NO numerals, historically accurate.")
DIAGRAM = ("STYLE: a clean minimal ASTRONOMY DIAGRAM, flat, centered, NO people, NO scene, NO landscape, dark "
    "warm charcoal/midnight background with faint stars, glowing thin gold and bronze lines (wireframe), 16:9, "
    "cinematic but abstract, like an elegant antique star-chart figure. NO text, NO numerals, NO letters.")
CHAR = ("Kepler: the SAME man as in the reference image — a European astronomer in his late 20s to 30s, short "
    "brown wavy hair, white ruff collar, dark scholar's robe, thoughtful intelligent face, early-1600s.")
HEAD = "IMPORTANT: ENTIRE head and face visible with headroom ABOVE the head — do NOT crop the top."

PROMPTS = {
  "S1.png": (f"{STYLE_MODERN}\n{CHAR}\nComposition: Kepler seated at his desk by candlelight, gazing thoughtfully "
    "upward, surrounded by a brass armillary sphere, a small telescope, and open books; a window showing a "
    f"night sky full of stars behind him. A scholar trying to read the heavens with mathematics. {HEAD} "
    "Ample empty space for a caption. No text, no numerals.", "REF"),
  "S2.png": (f"{DIAGRAM}\nDraw SIX concentric circular planetary orbit rings (thin glowing gold circles, evenly "
    "nested from a small center outward) representing six planetary orbits. Between consecutive rings, softly "
    "highlight the FIVE gaps with a warmer brighter glow, so the viewer sees six orbits and five gaps between "
    "them. Centered, elegant, on a dark starry ground. Generous empty space top and bottom for captions.", None),
  "S3.png": (f"{DIAGRAM}\nDraw Kepler's nested cosmos model: a large glowing wireframe SPHERE, with a CUBE "
    "inscribed snugly inside it, and inside the cube a smaller sphere, and inside that sphere a TETRAHEDRON, "
    "and inside that another smaller sphere — alternating sphere, polyhedron, sphere, polyhedron nested like "
    "an onion, all as glowing gold and bronze wireframes on a dark starry ground. Show clearly that each "
    "polyhedron fits snugly between an outer sphere and an inner sphere. Centered. Empty dark space for "
    "captions.", None),
  "S4.png": (f"{DIAGRAM}\nDraw EXACTLY FIVE distinct regular polyhedra in a single neat row, each a glowing gold "
    "wireframe on the dark ground, clearly different: (1) a tetrahedron (4 triangular faces, a triangular "
    "pyramid), (2) a cube (6 square faces), (3) an octahedron (8 triangular faces, two pyramids base to "
    "base), (4) a dodecahedron (12 pentagon faces), (5) an icosahedron (20 triangular faces, almost round). "
    "Five solids, evenly spaced, the famous five regular solids. Empty dark space above and below for "
    "captions.", None),
  "S5.png": (f"{DIAGRAM}\nLEFT HALF: a nested polyhedra-and-spheres model that is visibly skewed and "
    "mismatched, the orbits NOT fitting the solids, drawn in dim broken-looking gold wireframe (a model that "
    "failed). RIGHT HALF: a single beautiful smooth glowing ELLIPSE (an elliptical planetary orbit) with the "
    "sun as a bright point at one focus, drawn in bright clear gold — the true orbit. A faint stack of "
    "observation parchments at the bottom. Dark starry ground. Empty space for captions.", None),
  "S6.png": (f"{STYLE_MODERN}\n{CHAR}\nComposition: Kepler in PROFILE seated on the FAR LEFT THIRD of the "
    "frame, looking right toward a faint glowing nested brass model of spheres and polyhedra; leave the entire "
    "RIGHT TWO-THIRDS as deep dark study shadow with NOTHING in it, reserved for a single word overlay. "
    f"{HEAD} No text, no numerals.", "REF"),
}
order = ["S1.png","S2.png","S3.png","S4.png","S5.png","S6.png"]
if len(sys.argv) > 1: order = sys.argv[1:]
fail = []
for name in order:
    prompt, ref = PROMPTS[name]; out = OUT / name
    if out.exists() and out.stat().st_size > 0: print(f"  = {name} skip", flush=True); continue
    if not gen(prompt, out, ref_paths=[str(REF)] if ref == "REF" else None): fail.append(name)
print("== DONE ==" if not fail else f"== 실패: {fail} ==", flush=True)
