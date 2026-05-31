#!/usr/bin/env python3
# gen_images.py — unit-11 플라톤(다면체와 회전체) Nano Banana (네이티브 16:9)
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

STYLE = ("STYLE: cinematic painterly illustration, ancient Athens (4th century BC), Plato's Academy, warm "
    "Mediterranean light, palette marble-white/olive-green/terracotta/deep-blue and soft gold, marble "
    "columns and olive trees, 16:9, NO text, NO letters, NO numerals, NO modern objects, ample empty "
    "space for caption, historically accurate Greek himation robes.")
DIAGRAM = ("STYLE: a clean minimal GEOMETRY DIAGRAM, flat, centered, NO people, NO scene, NO landscape, dark "
    "warm charcoal background, glowing thin gold and bronze lines (wireframe), 16:9, cinematic but abstract, "
    "like an elegant textbook figure. NO text, NO numerals.")
STYLE_MODERN = ("STYLE: cinematic painterly illustration, early 1600s European astronomer's study by "
    "candlelight, palette deep brown/brass-gold/ink-blue, brass instruments and parchment, 16:9, NO text, "
    "NO letters, NO numerals, historically accurate.")
CHAR = ("Plato: a dignified ancient Greek philosopher in his late 50s, short grey beard, broad calm face, "
    "white-and-olive himation robe, wise serene expression, warm light.")
REF = OUT / "ref-plato.png"
HEAD = "IMPORTANT: ENTIRE head and face visible with headroom ABOVE the head — do NOT crop the top."
PROMPTS = {
  "ref-plato.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear face and clothing, "
    f"simple neutral warm background. {HEAD} No text.", None),
  "S1.png": (f"{STYLE}\nUsing the SAME Plato from reference (grey beard, himation): Plato teaching a small "
    "group of robed students at the entrance of his Academy, marble gateway and columns, olive trees, a "
    f"sense of a school where geometry is the gateway to philosophy. {HEAD} Empty space for caption. No text.", "REF"),
  "S2.png": (f"{DIAGRAM}\nDraw ONE single polyhedron as a glowing gold wireframe floating centered on the dark "
    "ground — a clear solid with flat polygon faces, visible edges, and bright dots at the vertices where "
    "edges meet (showing faces, edges and vertices of a polyhedron). Clean and elegant. Generous empty dark "
    "space top and bottom for captions.", None),
  "S3.png": (f"{DIAGRAM}\nDraw EXACTLY FIVE distinct regular polyhedra in a row, each a glowing gold wireframe "
    "on the dark ground, clearly different from each other: (1) a tetrahedron (a 4-faced triangular pyramid), "
    "(2) a cube (6 square faces), (3) an octahedron (8 triangular faces, like two pyramids joined base to "
    "base), (4) a dodecahedron (12 pentagon faces), (5) an icosahedron (20 triangular faces, almost round). "
    "Five solids, evenly spaced, the famous five perfect solids. Empty dark space above for a caption.", None),
  "S4.png": (f"{DIAGRAM}\nDraw five glowing gold wireframe regular polyhedra arranged in an arc, EACH softly "
    "infused with an element: a sharp tetrahedron glowing with flame (fire), an octahedron with swirling air "
    "(air), a round icosahedron with flowing water (water), a steady cube with earth/soil tones (earth), and "
    "a dodecahedron filled with tiny stars (the cosmos). Mystical, warm, painterly but on a dark ground. "
    "Empty space for caption.", None),
  "S5.png": (f"{DIAGRAM}\nDraw a clear illustration of solids of revolution: on the left a flat rectangle with "
    "a curved arrow showing it spinning around one edge to sweep out a CYLINDER; in the middle a right "
    "triangle spinning to sweep out a CONE; on the right a semicircle spinning to sweep out a SPHERE. Each "
    "flat shape shown faintly and the resulting 3D solid glowing brighter beside it, gold wireframe on dark. "
    "Empty space for caption.", None),
  "S6.png": (f"{STYLE_MODERN}\nAn astronomer (Kepler) in early-1600s clothes seated on the FAR LEFT THIRD of "
    "the frame, studying a beautiful brass model of the five Platonic solids nested one inside another with "
    "planetary orbit rings, by candlelight; leave the entire RIGHT TWO-THIRDS as deep dark study shadow with "
    f"NOTHING in it, reserved for a single word overlay. {HEAD} No text, no numerals.", None),
}
order = ["ref-plato.png","S1.png","S2.png","S3.png","S4.png","S5.png","S6.png"]
if len(sys.argv) > 1: order = sys.argv[1:]
fail = []
for name in order:
    prompt, ref = PROMPTS[name]; out = OUT / name
    if out.exists() and out.stat().st_size > 0: print(f"  = {name} skip", flush=True); continue
    if not gen(prompt, out, ref_paths=[str(REF)] if ref == "REF" else None): fail.append(name)
print("== DONE ==" if not fail else f"== 실패: {fail} ==", flush=True)
