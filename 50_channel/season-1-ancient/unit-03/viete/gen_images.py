#!/usr/bin/env python3
# gen_images.py — unit-03 viete Nano Banana (se-video-image §IM6, 네이티브 16:9)
# ★ 신규 캐릭터: ref-viete.png 를 S1보다 먼저 생성 → S2·S3·S5 에 ref_paths 전달(일관성)
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

# era-modern (16C 프랑스 르네상스) 팔레트: 올리브/카키 #7B6F49, 양피지 크림, 잉크 흑, 청회색, 촛불 금색
STYLE = ("STYLE: cinematic painterly illustration, 16th-century France (Renaissance), a learned "
    "lawyer-scholar's study, warm candlelight, palette of olive/khaki #7B6F49, cream parchment, "
    "ink black, muted slate blue-gray and candle gold, quill pens, inkwells, sealed letters, "
    "handwritten manuscripts, an alphabet table on the desk, 16:9 aspect ratio, NO text, "
    "NO legible letters, NO numerals, NO modern objects, ample empty space for caption overlay, "
    "historically accurate (16th-century French dress: ruff collar, dark olive doublet; quill and "
    "ink; vellum manuscripts; candle).")
CHAR = ("Francois Viete: a French lawyer-scholar in his 50s, fair skin, neat short brown beard, "
    "wearing a white ruff collar and a dark olive-khaki doublet, holding a quill pen, calm shrewd "
    "intelligent expression, warm candlelight on the face.")

REF = OUT / "ref-viete.png"
HEADROOM = ("IMPORTANT: frame him so his ENTIRE head and face are fully visible with comfortable "
    "headroom (empty space) ABOVE his head — do NOT crop the top of his head.")
PROMPTS = {
    "ref-viete.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear view "
        f"of face and clothing, simple neutral warm study background. {HEADROOM} No text.", None),
    "S1.png": (f"{STYLE}\nWide establishing shot of a 16th-century scholar's desk piled high with "
        "old manuscripts and vellum sheets DENSELY filled with long flowing handwritten paragraphs "
        "(equations written entirely in prose — only the TEXTURE of dense handwriting, NO legible "
        "letters or symbols), warm candlelight. On one side, a single short concise glowing line "
        "hovers as if a symbol just appeared (do NOT render actual symbols — just a glowing mark). "
        "The contrast of long prose vs one short line. Empty space in the upper third for caption. "
        "No legible text, no numerals.", None),
    "S2.png": (f"{STYLE}\nUsing the SAME Francois Viete character from the reference image (same "
        "face, same short brown beard, same ruff collar and olive doublet): a 16:9 WIDE upper-body "
        "shot of Viete seated at his study desk holding a quill, beside him a sealed cipher letter "
        "covered in mysterious unreadable marks (NO legible letters), an alphabet table and inkwell "
        f"on the desk, blurred candlelit study behind (shallow depth of field), shrewd scholarly "
        f"mood. {HEADROOM} Keep generous empty space to one side for caption. No text, no numerals.", "REF"),
    "S3.png": (f"{STYLE}\nUsing the SAME Francois Viete character from the reference image: a close "
        "view of Viete's hand with the quill writing on vellum. Beside it, an alphabet table that "
        "visibly SPLITS into two zones — the left zone of vowels glows warm and bright (suggesting "
        "the unknowns), the right zone of consonants stays calm and muted (suggesting the knowns). "
        "Render the table as elegant ruled columns and faint glyph shapes only, NO legible letters. "
        "A long dense paragraph compresses into a single short glowing line at the side. The birth "
        f"of symbolic writing. {HEADROOM} Empty space above for caption. No legible text, no numerals.", "REF"),
    "S4.png": (f"{STYLE}\nA few abstract glyph-marks (suggesting symbols, but NOT legible letters) "
        "hovering over the desk — at first they look heavy and dark and intimidating, then turning "
        "lighter, warmer and friendlier under the candlelight, as a hand and a wax seal stamp gently "
        "settle them into place. The feeling of a human CHOICE / agreement, not a law of nature. "
        "Quill, hand and wax seal motif (NO scales, NO locks). Empty central space for caption. "
        "No legible text, no numerals.", None),
    "S5.png": (f"{STYLE}\nA 16:9 split composition contrasting two ways of writing a power. LEFT "
        "half: old vellum with a LONG handwritten Latin word spelled out at length (suggesting 'the "
        "square of A' written as a word — render only the texture of a long word, NO legible "
        "letters), warm candlelight, a quill resting near it. RIGHT half: a clean bright surface "
        "with a single tiny faint superscript mark hovering high to the right of an implied symbol "
        "(suggesting the future small exponent — render NO actual letters or numerals). Clear "
        "vertical division. Long word vs tiny future mark. No legible text, no numerals.", "REF"),
    "S6.png": (f"{STYLE}\nA warm cinematic sense of a relay across centuries: a glowing timeline or "
        "hourglass, with three faint robed scholar silhouettes in succession (Baghdad medieval, "
        "Renaissance France, 17th-century Europe), faces hidden in shadow — the last one hinting at "
        "Descartes to come. In the foreground center, a single elegant quill pen crossed over an "
        "alphabet table, glowing softly. Large empty central space above for a single word overlay. "
        "Hopeful, unifying mood. No legible text, no letters, no numerals.", None),
}

order = ["ref-viete.png", "S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
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
