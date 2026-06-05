#!/usr/bin/env python3
# synth.py — unit-10 류후이 ElevenLabs 합성 (voice-pool §0.6 절차 재현)
# turn별 합성 → post-process(volume) → concat(silence) → 4-narration.mp3
# voice: Q=Kanna(speed1.15, post 없음) / A=Kyle(+3.8dB) — 아르키메데스 영상과 반대 pairing
import os, sys, json, time, subprocess, pathlib, urllib.request, urllib.error

HERE = pathlib.Path(__file__).parent
JSONL = HERE / "4-narration.jsonl"
TURNS = HERE / "turns"; TURNS.mkdir(exist_ok=True)
NORM = HERE / "turns_norm"; NORM.mkdir(exist_ok=True)
OUT = HERE / "4-narration.mp3"
MODEL = "eleven_multilingual_v2"
KEY = os.environ["ELEVENLABS_API_KEY"]

# post-process volume per voice (voice-pool §0.2): Kyle +3.8dB, Mike +8dB, Mina/Kanna 없음
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
            if e.code in (401, 422):  # auth/validation — no retry
                raise
            time.sleep(2 * attempt)
        except Exception as e:
            print(f"  ERR turn {t['id']} (try {attempt}): {e}", flush=True)
            time.sleep(2 * attempt)
    raise RuntimeError(f"turn {t['id']} 합성 실패")

def main():
    turns = [json.loads(l) for l in JSONL.read_text(encoding="utf-8").splitlines() if l.strip()]
    # smoke test 모드: 첫 turn만
    if "--smoke" in sys.argv:
        turns = turns[:1]
    print(f"== 합성 {len(turns)} turn ==", flush=True)
    for t in turns:
        raw = TURNS / f"turn-{t['id']:03d}.mp3"
        if not raw.exists() or raw.stat().st_size == 0:
            data = synth_turn(t)
            raw.write_bytes(data)
            print(f"  ✓ turn {t['id']:03d} {t['speaker']} ({len(data)} bytes)", flush=True)
        # post-process: volume + 리미터(클리핑 방지) + 재인코딩 44100 mono 128k
        db = VOLUME_DB.get(t["voice"], 0.0)
        norm = NORM / f"turn-{t['id']:03d}.mp3"
        # 부스트 시 alimiter로 피크만 억제(음량 유지, 감탄문 클리핑 깨짐 방지) — unit-04 학습
        af = f"volume={db}dB,alimiter=limit=0.95" if db != 0.0 else "anull"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
                        "-af", af, "-ar", "44100", "-ac", "1", "-b:a", "128k", str(norm)], check=True)
    if "--smoke" in sys.argv:
        print("smoke OK", flush=True); return
    # silence 파일
    def silence(ms):
        f = HERE / f"silence_{ms}ms.mp3"
        if not f.exists():
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                            "-i", "anullsrc=r=44100:cl=mono", "-t", str(ms/1000),
                            "-acodec", "libmp3lame", "-b:a", "128k", str(f)], check=True)
        return f
    s300, s1000 = silence(220), silence(750)
    # concat list: turn + (다음 turn scene 경계면 1000 / 아니면 300)
    lines, prev_scene = [], None
    for i, t in enumerate(turns):
        if prev_scene is not None:
            gap = s1000 if t["scene"] != prev_scene else s300
            lines.append(f"file '{gap.as_posix()}'")
        lines.append(f"file '{(NORM / f'turn-{t['id']:03d}.mp3').as_posix()}'")
        prev_scene = t["scene"]
    concat = HERE / "concat.txt"
    concat.write_text("\n".join(lines) + "\n", encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(concat), "-c", "copy", str(OUT)], check=True)
    # 길이 측정
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", str(OUT)],
                         capture_output=True, text=True).stdout.strip()
    print(f"== 완료: {OUT.name} / {float(dur):.2f}s ==", flush=True)

if __name__ == "__main__":
    main()
