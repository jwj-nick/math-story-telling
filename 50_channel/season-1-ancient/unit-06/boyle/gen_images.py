#!/usr/bin/env python3
# gen_images.py — unit-06 보일 Nano Banana (se-video-image §IM6, 네이티브 16:9)
# 케플러와 다른 인물·다른 톤(낮의 청회색 실험실). ref-boyle 우선 → 후속 일관성.
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
                    image_config=types.ImageConfig(aspect_ratio="16:9")))
            for p in resp.candidates[0].content.parts:
                if getattr(p, "inline_data", None) and p.inline_data.data:
                    pathlib.Path(out).write_bytes(p.inline_data.data)
                    print(f"  OK {pathlib.Path(out).name} ({len(p.inline_data.data)} bytes)", flush=True)
                    return True
            print(f"  ! {pathlib.Path(out).name}: 이미지 없음 try {attempt}", flush=True)
        except Exception as e:
            print(f"  ERR {pathlib.Path(out).name} try {attempt}: {str(e)[:200]}", flush=True)
            time.sleep(3 * attempt)
    return False

# 보일 ver: 낮의 옥스퍼드 실험실, 차분한 청회색(#5C7A8E)/황동/촛불금색/목재갈색 — 케플러 별밤과 의도적 대비
STYLE = ("STYLE: cinematic painterly illustration, mid 17th-century England, a natural philosopher's "
    "daylight study and laboratory at Oxford, soft overcast daylight through a window, calm palette of "
    "slate blue-grey, brass/bronze, warm candle-gold and wood-brown, glass tubes and flasks and a brass "
    "air-pump on a wooden table, 16:9 aspect ratio, NO text, NO letters, NO numerals, NO modern objects, "
    "ample empty space for caption overlay, historically accurate (mid-17th-century English dress: lace "
    "falling band collar, dark coat; brass scientific instruments; quill and notebook).")
CHAR = ("Robert Boyle: a mid-17th-century English natural philosopher in his 30s-40s, long flowing brown "
    "curly hair to the shoulders (English Restoration style), mostly clean-shaven calm face, a white lace "
    "falling-band collar over a dark slate-blue coat, a calm inquisitive expression, soft daylight on the "
    "face. He is clearly a DIFFERENT person from any astronomer: English, longer hair, daytime laboratory.")

REF = OUT / "ref-boyle.png"
HEADROOM = ("IMPORTANT: frame so the ENTIRE head and face are fully visible with comfortable "
    "headroom ABOVE the head — do NOT crop the top of the head.")
PROMPTS = {
    "ref-boyle.png": (f"{STYLE}\n{CHAR}\nComposition: front-facing reference portrait, clear view of "
        f"face and clothing, simple neutral warm background. {HEADROOM} No text.", None),
    "S1.png": (f"{STYLE}\nUsing the SAME Boyle character from the reference (same long brown curly hair, "
        "lace collar, slate-blue coat): Boyle in his daylight Oxford laboratory holding up a glass tube "
        "and studying it closely, glass flasks and a brass air-pump on the wooden table, soft overcast "
        f"window light, a sense of calm inquiry. {HEADROOM} Empty space for caption. No text.", "REF"),
    "S2.png": (f"{STYLE}\nUsing the SAME Boyle character from the reference: a wisp of faint pale mist/air "
        "slipping through open fingers (something formless and uncatchable), and Boyle looking at it with "
        "a determined resolve to capture and measure it; on the table an empty open notebook and a quill "
        f"(soon to be filled), warm candlelight. {HEADROOM} Empty space for caption. No text.", "REF"),
    "S3.png": (f"{STYLE}\nUsing the SAME Boyle character from the reference: a 17th-century brass air-pump "
        "apparatus with a sealed glass tube containing trapped air; Boyle and an assistant (Robert Hooke, "
        "face indistinct/turned away) working the instrument together with four hands; beside them a "
        "measurement notebook with ruled lines and a quill. Do NOT render numerals or letters. Empty space "
        "for caption. No text.", "REF"),
    "S4.png": ("A clean minimal scientific diagram on a plain dark slate-blue background. NO people, NO "
        "faces, NO furniture, NO room. Just THREE tall thin vertical glass test-tubes standing in a row, "
        "evenly spaced, painterly cinematic style with warm gold rim-light. Each tube has at its very TOP "
        "a sealed pocket of pale glowing trapped AIR, and below it a shiny dark mercury liquid column "
        "filling the rest. The KEY POINT, make it obvious and exaggerated: the trapped AIR pocket shrinks "
        "step by step from LEFT to RIGHT. LEFT tube: the glowing air pocket fills the TOP THIRD of the "
        "tube (tall). MIDDLE tube: the air pocket is only HALF as tall as the left one. RIGHT tube: the "
        "air pocket is a tiny thin sliver, about a QUARTER of the left one, the mercury has risen almost "
        "to the top. So left big, middle medium, right tiny — clearly decreasing. Above the row of tubes, "
        "a simple glowing seesaw plank tilted diagonally (one end up, other end down). Empty dark space at "
        "the top for a caption. Do NOT render ANY numerals, letters, words, symbols or labels of any kind. "
        "Absolutely no text anywhere.", None),
    "S5.png": ("A clean minimal conceptual diagram on a plain dark slate-blue background. NO people, NO "
        "faces, NO portraits anywhere, painterly cinematic style. In the TOP-LEFT, a small round vignette "
        "showing a starry night sky with one planet on an elliptical orbit around a small glowing sun. In "
        "the TOP-RIGHT, a small round vignette showing a single upright glass tube of compressed air next "
        "to a small brass air-pump on a plain surface. From each round vignette a thin glowing gold line "
        "descends and the two lines MERGE into ONE single smooth DECREASING curve across the BOTTOM of the "
        "image: the curve begins HIGH near the left, drops steeply, then bends and flattens out as it goes "
        "to the right, staying above and approaching a horizontal baseline — exactly the shape of the "
        "graph y = k / x in the first quadrant (a falling hyperbola branch; it must NEVER rise, NEVER form "
        "a V, U, parabola or wave). Glowing warm gold curve on dark background, empty space for caption. "
        "Do NOT render ANY numerals, letters, words, equations or labels of any kind. Absolutely no text "
        "anywhere.", None),
    "S6.png": (f"{STYLE}\nA warm cinematic finale: formless air being resolved into a clean glowing curve "
        "and an orderly measurement chart, a brass measuring rule and a glass tube in the foreground, a "
        "sense of a new age of measurement emerging, soft daylight and candlelight. Large empty central "
        "space above for a single word overlay. No text, no letters, no numerals.", None),
}

order = ["ref-boyle.png", "S1.png", "S2.png", "S3.png", "S4.png", "S5.png", "S6.png"]
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
