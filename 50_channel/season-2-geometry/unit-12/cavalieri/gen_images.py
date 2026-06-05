#!/usr/bin/env python3
# gen_images.py — unit-12 카발리에리(단면·불가분량) Nano Banana (네이티브 16:9)
# ★ 신규 캐릭터: S1 에서 ref-cavalieri.png 를 먼저 생성 → S1·S4 인물 장면에 reference 로 전달(얼굴 일관성).
# era-modern (#6C5B7B 자주빛), 17C 이탈리아 볼로냐, 수도사. 종이 빵(단면 쌓기).
import os, sys, pathlib, time
from google import genai
from google.genai import types

HERE = pathlib.Path(__file__).parent
OUT = HERE / "5-images"; OUT.mkdir(exist_ok=True)
REF = OUT / "ref-cavalieri.png"
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

# ── 캐릭터 reference (era-modern 17C 이탈리아 수도사) ──
CHAR = ("Bonaventura Cavalieri: a 17th-century Italian Jesuit monk and mathematician, around 45 years old, "
    "thin gaunt face (he suffered from gout), thoughtful contemplative eyes, short dark hair with a tonsure, "
    "wearing a dark friar's habit/cassock tinted deep muted PLUM-PURPLE (#6C5B7B). Quiet, scholarly, kind.")
REF_PROMPT = ("Character reference portrait, upper body, neutral plain dark background. " + CHAR +
    " Painterly cinematic illustration, soft warm candlelight, ENTIRE head and face visible with headroom "
    "ABOVE the head. 16:9. NO text, NO letters, NO numerals.")

# ── 공통 스타일 ──
STYLE = ("STYLE: cinematic painterly illustration, 17th-century Italy (Bologna), warm candlelit interior, "
    "palette deep plum-purple (#6C5B7B), aged parchment cream, bronze and muted gold, dark wood, "
    "16:9, NO text, NO letters, NO numerals, NO modern objects, ample empty space for caption, "
    "historically accurate early Baroque setting.")
DIAGRAM = ("STYLE: a clean minimal GEOMETRY DIAGRAM, flat, centered, NO people, NO scene, NO landscape, dark "
    "plum-charcoal background, glowing thin gold and pale violet lines (wireframe), 16:9, cinematic but abstract, "
    "like an elegant textbook figure. NO text, NO numerals.")
HEAD = "IMPORTANT: ENTIRE head and face visible with headroom ABOVE the head — do NOT crop the top."

PROMPTS = {
  # S1 — 인물 hook: ref 생성 후 본인 reference 로 일관성 유지
  "S1.png": (f"{STYLE}\nA quiet candlelit dining table in a 17th-century Italian monastery. The SAME monk from "
    "the reference image (Cavalieri) has sliced a loaf of bread into many thin even slices, and arranged them "
    "into TWO stacks side by side: one stack STRAIGHT and upright, the other stack SHEARED / leaning at a "
    "slant (like a tilted deck) — clearly different shapes, same number of slices. He looks at them with "
    f"curious wonder. {HEAD} Empty space at the bottom for caption. No text, no numerals.", [REF]),
  # S2 — diagram: 입체 → 무수한 얇은 단면(불가분량)
  "S2.png": (f"{DIAGRAM}\nDraw a solid (a smooth blob / a leaning column) shown DECOMPOSING into countless "
    "extremely thin flat horizontal cross-section layers stacked on top of one another — the wafer-thin slices "
    "clearly visible, an exploded slight gap between a few of them to show they are separate flat faces "
    "(the idea of 'indivisibles', thicknessless cross-sections). Glowing gold and pale violet on dark plum. "
    "Generous empty space top and bottom for captions.", None),
  # S3 — diagram: 모양 다른 두 입체, 같은 높이 단면 같음
  "S3.png": (f"{DIAGRAM}\nDraw a clear comparison of TWO solids of DIFFERENT outer shape standing side by side "
    "(e.g. a straight cylinder and a leaning/oblique cylinder), both the same height. A single horizontal "
    "plane cuts through BOTH at the same height, and the two resulting cross-sections (highlighted, brighter) "
    "have the SAME area — show the matching cross-sections clearly. Glowing gold wireframe, the cutting plane "
    "in pale violet, on dark plum ground. Empty space top and bottom for captions.", None),
  # S4 — 인물: 책 「Geometria」 + 카발리에리(ref 전달)
  "S4.png": (f"{STYLE}\nThe SAME monk from the reference image (Cavalieri) seated at a desk by candlelight, a "
    "thick open antique book / treatise in front of him (his 1635 work), a quill and a small wooden model of "
    "stacked slices nearby. He looks resolved yet a little anxious — the moment of finally publishing. A small "
    f"telescope rests on the shelf behind (a nod to his teacher Galileo). {HEAD} Empty space at the bottom "
    "for caption. No text, no numerals.", [REF]),
  # S5 — diagram: 동(중국 죽간)/서(유럽 양피지) 대칭, 가운데 같은 단면
  "S5.png": (f"{DIAGRAM}\nA SYMMETRIC split composition: on the LEFT a stylized ancient Chinese bamboo-slip "
    "scroll motif (suggesting Liu Hui, 3rd century), on the RIGHT a stylized European parchment/manuscript "
    "motif (Cavalieri); in the CENTER, the SAME glowing stacked cross-section figure bridging both sides — "
    "two cultures arriving at the identical idea. Glowing gold and pale violet on dark plum, abstract and "
    "elegant. NO readable text, NO numerals. Empty space top and bottom for captions.", None),
  # S6 — diagram 엠블럼: 단면 슬라이스, 좌측 / 우측 어두움(한 단어 자리)
  "S6.png": (f"{DIAGRAM}\nA glowing emblem of a solid built from thin stacked cross-section slices (the "
    "indivisibles), softly radiant like an engraving, placed on the FAR LEFT THIRD of the frame; leave the "
    "entire RIGHT TWO-THIRDS as deep dark plum empty space with NOTHING in it, reserved for a single word "
    "overlay. Warm gold and pale violet on near-black plum. No text, no numerals.", None),
}
order = ["S1.png","S2.png","S3.png","S4.png","S5.png","S6.png"]
if len(sys.argv) > 1: order = sys.argv[1:]

# ref-cavalieri.png 우선 생성 (없으면) — S1·S4 가 reference 로 사용
if not (REF.exists() and REF.stat().st_size > 0):
    print("== ref-cavalieri.png 생성 ==", flush=True)
    if not gen(REF_PROMPT, REF):
        print("  ! ref 생성 실패 → S1/S4 는 ref 없이 진행", flush=True)

fail = []
for name in order:
    prompt, ref = PROMPTS[name]; out = OUT / name
    if out.exists() and out.stat().st_size > 0: print(f"  = {name} skip", flush=True); continue
    # ref 가 필요한데 아직 없으면 ref 빼고 생성 (graceful)
    use_ref = [str(p) for p in (ref or []) if pathlib.Path(p).exists()] or None
    if not gen(prompt, out, use_ref): fail.append(name)
print("== DONE ==" if not fail else f"== 실패: {fail} ==", flush=True)
