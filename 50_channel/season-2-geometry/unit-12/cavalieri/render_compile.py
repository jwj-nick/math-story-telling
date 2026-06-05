#!/usr/bin/env python3
# render_compile.py — unit-12 카발리에리: 6-motion-config.json → scene 클립(zoompan+drawtext+fade) → concat → 7-raw.mp4
# se-video-render §CL/CC 검증 패턴 자동화 (v0.2 컴파일러)
# EXECUTE 시: synth → 4-narration.mp3 실측 → 6-motion-config.draft.json 타이밍(rel 0~1)을 실측 절대초로 채워 6-motion-config.json 작성 후 본 스크립트 실행.
import json, subprocess, pathlib, sys

HERE = pathlib.Path(__file__).parent
CFG = json.loads((HERE / "6-motion-config.json").read_text(encoding="utf-8"))
CLIPS = HERE / "clips"; CLIPS.mkdir(exist_ok=True)
CAPTXT = HERE / "captxt"; CAPTXT.mkdir(exist_ok=True)
FPS = CFG["fps"]; W, H = CFG["resolution"]
FONT = CFG["font"].replace(":", "\\:")  # ffmpeg colon escape
PAL = CFG["palette"]
FADE = CFG["transition"]["in"]

def zoom_expr(motion, z0, z1, frames):
    if z1 >= z0:  # increasing (push_in, zoom_in, ken_burns, slow_zoom)
        incr = (z1 - z0) / frames
        if abs(z0 - 1.0) < 1e-6:
            return f"min(zoom+{incr:.6f},{z1})"
        return f"if(eq(on,0),{z0},min(zoom+{incr:.6f},{z1}))"
    else:  # decreasing (zoom_out)
        decr = (z0 - z1) / frames
        return f"if(eq(on,0),{z0},max(zoom-{decr:.6f},{z1}))"

def build_clip(sc):
    dur = round(sc["end"] - sc["start"], 3)
    frames = round(dur * FPS)
    z0, z1 = sc["zoom"]
    zexp = zoom_expr(sc["motion"], z0, z1, frames)
    vf = [
        "scale=2560:-1,crop=2560:1440",
        (f"zoompan=z='{zexp}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
         f":s={W}x{H}:fps={FPS}"),
    ]
    for i, cap in enumerate(sc.get("captions", [])):
        tf = CAPTXT / f"{sc['id']}_{i}.txt"
        tf.write_text(cap["text"], encoding="utf-8")  # UTF-8 no BOM
        tfp = tf.as_posix().replace(":", "\\:")
        color = PAL[cap["color"]]
        ls = cap["start"] - sc["start"]; le = cap["end"] - sc["start"]
        yexpr = f"h*{cap['y']}-text_h/2"
        xexpr = "(w-text_w)/2" if cap.get("x", "center") == "center" else f"w*{cap['x']}-text_w/2"
        vf.append(
            f"drawtext=fontfile='{FONT}':textfile='{tfp}':fontcolor={color}"
            f":fontsize={cap['size']}:x={xexpr}:y={yexpr}"
            f":shadowcolor={PAL['shadow']}:shadowx=2:shadowy=2"
            f":enable='between(t,{ls:.2f},{le:.2f})'")
    fade_out_st = round(dur - FADE, 3)
    vf.append(f"fade=t=in:st=0:d={FADE}")
    vf.append(f"fade=t=out:st={fade_out_st}:d={FADE}")
    vf.append("format=yuv420p")
    out = CLIPS / f"{sc['id']}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i",
           str(HERE / sc["img"]), "-t", str(dur), "-r", str(FPS),
           "-vf", ",".join(vf), "-c:v", "libx264", "-crf", "18",
           "-pix_fmt", "yuv420p", "-r", str(FPS), "-an", str(out)]
    subprocess.run(cmd, check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out)],
        capture_output=True, text=True).stdout.strip())
    print(f"  ✓ {sc['id']}.mp4  dur={d:.2f}s (target {dur:.2f})  motion={sc['motion']}  caps={len(sc.get('captions',[]))}", flush=True)
    return out

def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    print(f"== 렌더 {len(CFG['scenes'])} scene ==", flush=True)
    for sc in CFG["scenes"]:
        if only and sc["id"] not in only: continue
        build_clip(sc)
    if only: return
    listf = CLIPS / "list.txt"
    listf.write_text("\n".join(f"file '{sc['id']}.mp4'" for sc in CFG["scenes"]) + "\n", encoding="utf-8")
    raw = HERE / "7-raw.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(listf), "-c", "copy", str(raw)], check=True)
    # STEP 8 합성: 7-raw.mp4 (무음) + 4-narration.mp3 → 8-final.mp4
    final = HERE / "8-final.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
                    "-i", str(HERE / CFG["audio"]), "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", str(final)], check=True)
    # 표지: 1초 지점 프레임
    poster = HERE / "8-poster.jpg"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1", "-i", str(final),
                    "-frames:v", "1", "-q:v", "2", str(poster)], check=True)
    info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,pix_fmt",
        "-show_entries", "format=duration", "-of", "default=nw=1", str(final)],
        capture_output=True, text=True).stdout.strip()
    print(f"== 7-raw.mp4 / 8-final.mp4 / 8-poster.jpg ==\n{info}\ntarget total: {CFG['total_duration']}s", flush=True)

if __name__ == "__main__":
    main()
