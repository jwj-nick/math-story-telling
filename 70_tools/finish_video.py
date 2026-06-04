#!/usr/bin/env python3
# finish_video.py — EXECUTE 단계(STEP4~8) 단일 드라이버.
#
# 근본해결(2026-06-04): background agent는 API(ElevenLabs/Gemini)·PowerShell 키추출이
# 정책상 차단됨 → "prep(agent)/execute(메인세션)" 분리. 이 스크립트는 메인세션이 단원당
# 명령 1개로 STEP4~8을 끝낸다. (도구 불안정 노출 최소화)
#
# 전제(= PREP 산출물, agent가 만들어 둠):
#   synth.py            (STEP4 음성 — voice/turns 단원별)
#   gen_images.py       (STEP5 이미지 — 프롬프트 단원별, ref 재사용 포함)
#   render_compile.py   (STEP7 렌더 — generic, 6-motion-config.json 읽음)
#   6-motion-config.draft.json  (자막 텍스트/위치/색/크기 + rel_start/rel_end[0~1] + motion/zoom)
#   4-narration.jsonl   (turn→scene 매핑)
#
# 동작: synth.py → gen_images.py → (concat.txt+jsonl로 SCENE_ENDS 실측)
#       → draft를 실측 길이에 매핑해 6-motion-config.json 생성 → render_compile.py → mux+poster
#
# 사용:
#   python 70_tools/finish_video.py <unit_video_dir>
#   옵션: --skip-synth  --skip-images  --render-only(=둘다 skip + config 재생성도 skip)
import json, subprocess, sys, re, pathlib

def ffdur(p):
    out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",str(p)],capture_output=True,text=True).stdout.strip()
    return float(out)

def run(cmd, cwd):
    print(f"  $ {' '.join(str(c) for c in cmd)}", flush=True)
    env = {**__import__('os').environ, "PYTHONIOENCODING":"utf-8"}
    r = subprocess.run(cmd, cwd=str(cwd), env=env)
    if r.returncode != 0:
        sys.exit(f"!! 실패: {cmd} (rc={r.returncode})")

def scene_ends_from_concat(d):
    """concat.txt + 4-narration.jsonl → {S1:end,...} (turn 마지막의 누적시각)."""
    rows = [json.loads(l) for l in (d/"4-narration.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    turn_scene = {r["id"]: r["scene"] for r in rows}
    cum, scene_end, cache = 0.0, {}, {}
    def D(p):
        if p not in cache: cache[p] = ffdur(p)
        return cache[p]
    for line in (d/"concat.txt").read_text(encoding="utf-8").splitlines():
        m = re.search(r"file '(.+)'", line.strip())
        if not m: continue
        cum += D(m.group(1))
        mm = re.search(r"turn-(\d+)\.mp3", m.group(1))
        if mm:
            sc = turn_scene.get(int(mm.group(1)))
            if sc: scene_end[sc] = round(cum, 3)
    return scene_end

DEFAULT_PAL = {"gold":"0xD9A441","white":"0xFFFFFF","olive":"0x7A8C5C","ink":"0x5C7DA8","shadow":"0x000000"}

def build_config(d):
    draft = json.loads((d/"6-motion-config.draft.json").read_text(encoding="utf-8"))
    audio = d/"4-narration.mp3"
    total = round(ffdur(audio), 3)
    ends = scene_ends_from_concat(d)
    scenes_draft = draft["scenes"]
    ids = [s["id"] for s in scenes_draft]
    # 마지막 scene end = audio total(영상=음성 길이 일치). 누락 scene은 균등 보간.
    measured = [ends.get(i) for i in ids]
    for k,v in enumerate(measured):
        if v is None: measured[k] = round(total*(k+1)/len(ids),3)
    measured[-1] = total
    cfg = {
        "_comment": f"AUTO finish_video. total={total}s, SCENE_ENDS={measured}",
        "fps": draft.get("fps",25), "resolution": draft.get("resolution",[1280,720]),
        "total_duration": total, "audio": "4-narration.mp3",
        "font": draft.get("font","C:/Windows/Fonts/NotoSerifCJKkr-Regular.otf"),
        "palette": {**DEFAULT_PAL, **draft.get("palette",{})}, "scenes": [],
        "transition": draft.get("transition", {"type":"fade","in":0.6,"out":0.6}),
    }
    start = 0.0
    for i, sd in enumerate(scenes_draft):
        end = measured[i]; dur = max(0.1, end-start)
        caps = []
        for c in sd.get("captions", []):
            rs = c.get("rel_start", 0.45); re_ = c.get("rel_end", 0.97)
            cs = round(start + rs*dur, 2); ce = round(min(end-0.05, start + re_*dur), 2)
            caps.append({"text":c["text"], "x":c.get("x","center"), "y":c["y"],
                         "size":c["size"], "color":c["color"], "start":cs, "end":ce})
        cfg["scenes"].append({"id":sd["id"], "img":f"5-images/{sd['id']}.png",
            "start":round(start,3), "end":round(end,3),
            "motion":sd.get("motion","ken_burns"), "zoom":sd.get("zoom",[1.0,1.05]),
            "captions":caps})
        start = end
    (d/"6-motion-config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ 6-motion-config.json (total {total}s, scenes {len(cfg['scenes'])})", flush=True)
    return total

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = set(a for a in sys.argv[1:] if a.startswith("--"))
    if not args: sys.exit("사용: python finish_video.py <unit_video_dir> [--skip-synth --skip-images --render-only]")
    d = pathlib.Path(args[0]).resolve()
    render_only = "--render-only" in flags
    skip_synth = render_only or "--skip-synth" in flags
    skip_images = render_only or "--skip-images" in flags

    print(f"== finish_video: {d} ==", flush=True)
    if not skip_synth:  run([sys.executable,"synth.py"], d)
    if not skip_images: run([sys.executable,"gen_images.py"], d)
    if not render_only or not (d/"6-motion-config.json").exists():
        build_config(d)
    run([sys.executable,"render_compile.py"], d)
    # STEP8 mux + poster
    raw, mp3, final = d/"7-raw.mp4", d/"4-narration.mp3", d/"8-final.mp4"
    subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y","-i",str(raw),"-i",str(mp3),
        "-c:v","copy","-c:a","aac","-b:a","160k","-shortest",str(final)], check=True)
    subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y","-ss","6","-i",str(final),
        "-frames:v","1","-q:v","3",str(d/"8-poster.jpg")], check=True)
    dur = ffdur(final)
    print(f"== DONE: {final.name} {dur:.2f}s + 8-poster.jpg ==", flush=True)

if __name__ == "__main__":
    main()
