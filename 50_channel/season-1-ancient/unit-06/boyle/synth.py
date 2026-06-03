#!/usr/bin/env python3
# synth.py — unit-06 보일 ElevenLabs 합성 (voice-pool §0.6 절차 재현)
# turn별 합성 → post-process(volume) → concat(silence) → 4-narration.mp3
# Q=Kanna(speed1.15, post 없음) / A=Kyle(+3.8dB+alimiter)
import os, sys, json, time, subprocess, pathlib, urllib.request, urllib.error

HERE = pathlib.Path(__file__).parent
JSONL = HERE / "4-narration.jsonl"
TURNS = HERE / "turns"; TURNS.mkdir(exist_ok=True)
NORM = HERE / "turns_norm"; NORM.mkdir(exist_ok=True)
OUT = HERE / "4-narration.mp3"
MODEL = "eleven_multilingual_v2"
KEY = os.environ["ELEVENLABS_API_KEY"]

# post-process volume per voice (voice-pool §0.2): Kyle +3.8dB, Kanna 없음
VOLUME_DB = {"Kyle": 3.8, "Mike": 8.0, "Mina": 0.0, "Kanna": 0.0}

def synth_turn(t):
    vid = t["voice_id"]
    body = json.dumps({
        "text": t["text"],
        "model_id": MODEL,
        "voice_settings": t["voice_settings"],
    }).encode("utf-8")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg",
    })
    for attempt in range(1, 5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "ignore")[:300]
            print(f"  HTTP {e.code} turn {t['id']} (try {attempt}): {msg}", flush=True)
            if e.code in (401, 422):
                raise
            time.sleep(2 * attempt)
        except Exception as e:
            print(f"  ERR turn {t['id']} (try {attempt}): {e}", flush=True)
            time.sleep(2 * attempt)
    raise RuntimeError(f"turn {t['id']} 합성 실패")

def main():
    turns = [json.loads(l) for l in JSONL.read_text(encoding="utf-8").splitlines() if l.strip()]
    if "--smoke" in sys.argv:
        turns = turns[:1]
    print(f"== 합성 {len(turns)} turn ==", flush=True)
    for t in turns:
        raw = TURNS / f"turn-{t['id']:03d}.mp3"
        if not raw.exists() or raw.stat().st_size == 0:
            data = synth_turn(t)
            raw.write_bytes(data)
            print(f"  OK turn {t['id']:03d} {t['speaker']} ({len(data)} bytes)", flush=True)
        db = VOLUME_DB.get(t["voice"], 0.0)
        norm = NORM / f"turn-{t['id']:03d}.mp3"
        af = f"volume={db}dB,alimiter=limit=0.95" if db != 0.0 else "anull"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
                        "-af", af, "-ar", "44100", "-ac", "1", "-b:a", "128k", str(norm)], check=True)
    if "--smoke" in sys.argv:
        print("smoke OK", flush=True); return
    def silence(ms):
        f = HERE / f"silence_{ms}ms.mp3"
        if not f.exists():
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                            "-i", "anullsrc=r=44100:cl=mono", "-t", str(ms/1000),
                            "-acodec", "libmp3lame", "-b:a", "128k", str(f)], check=True)
        return f
    s300, s1000 = silence(300), silence(1000)
    lines, prev_scene = [], None
    for t in turns:
        if prev_scene is not None:
            gap = s1000 if t["scene"] != prev_scene else s300
            lines.append(f"file '{gap.as_posix()}'")
        lines.append(f"file '{(NORM / f'turn-{t['id']:03d}.mp3').as_posix()}'")
        prev_scene = t["scene"]
    concat = HERE / "concat.txt"
    concat.write_text("\n".join(lines) + "\n", encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(concat), "-c", "copy", str(OUT)], check=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", str(OUT)],
                         capture_output=True, text=True).stdout.strip()
    print(f"== 완료: {OUT.name} / {float(dur):.2f}s ==", flush=True)

if __name__ == "__main__":
    main()
