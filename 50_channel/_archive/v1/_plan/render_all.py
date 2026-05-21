"""
render_all.py — 13단원 일괄 렌더 파이프라인
  STAGE 4: edge-tts → narration.mp3
  STAGE 4.5: ffprobe → AUDIO_DURATION 측정 → config.json duration 갱신 → index.html 재빌드
  STAGE 6: hyperframes render → raw.mp4
  STAGE 7: ffmpeg 합성 → final.mp4

사용:
  python render_all.py                   # 모든 단원
  python render_all.py 01                # 단원 1개
  python render_all.py 01 02 03          # 여러 단원
  python render_all.py --skip-tts        # TTS 건너뛰고 기존 narration.mp3 사용
  python render_all.py --only-final      # raw.mp4 + narration.mp3가 있다고 가정, ffmpeg만
"""

import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # 90_video/
BUILD_INDEX = ROOT / "_plan" / "build_index.py"


def run(cmd: list, **kwargs):
    """프로세스 실행, exit code 반환. Windows에서 .cmd shim 호환 위해 shell=True 사용"""
    print(f"  $ {' '.join(str(c) for c in cmd[:4])}{'...' if len(cmd) > 4 else ''}")
    # 셸 문자열로 변환 (공백 포함 경로는 큰따옴표로 감쌈)
    shell_cmd = " ".join(f'"{c}"' if " " in str(c) else str(c) for c in cmd)
    return subprocess.run(shell_cmd, shell=True, **kwargs)


def get_audio_duration(mp3_path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3_path)],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def render_unit(unit_num: str, skip_tts: bool = False, only_final: bool = False):
    unit_dir = ROOT / f"unit{unit_num}"
    if not unit_dir.exists():
        return f"[SKIP] unit{unit_num}: dir not found"

    narration_txt = unit_dir / "narration.txt"
    narration_mp3 = unit_dir / "narration.mp3"
    raw_mp4 = unit_dir / "raw.mp4"
    final_mp4 = unit_dir / "final.mp4"
    config_json = unit_dir / "config.json"

    print(f"\n=== unit{unit_num} ===")

    # STAGE 4: TTS
    if not only_final and not skip_tts:
        if narration_mp3.exists():
            print(f"  [stage4] narration.mp3 exists, skipping TTS")
        else:
            r = run(["python", "-m", "edge_tts", "--voice", "ko-KR-SunHiNeural",
                     "--file", str(narration_txt), "--write-media", str(narration_mp3)])
            if r.returncode != 0:
                return f"[FAIL unit{unit_num}] TTS failed"

    # STAGE 4.5: duration 측정 + config 갱신 + index 재빌드
    if not only_final:
        dur = get_audio_duration(narration_mp3)
        target_dur = math.ceil(dur) + 1
        cfg = json.loads(config_json.read_text(encoding="utf-8"))
        if cfg.get("duration") != target_dur:
            print(f"  [stage4.5] duration update: {cfg.get('duration')} → {target_dur} (audio={dur:.2f}s)")
            cfg["duration"] = target_dur
            config_json.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
            r = run(["python", str(BUILD_INDEX), unit_num])
            if r.returncode != 0:
                return f"[FAIL unit{unit_num}] build_index failed"
        else:
            print(f"  [stage4.5] duration ok ({dur:.2f}s)")

    # STAGE 6: HyperFrames render
    if not only_final:
        if raw_mp4.exists():
            print(f"  [stage6] raw.mp4 exists, skipping render")
        else:
            r = run(["hyperframes", "render", str(unit_dir), "-o", str(raw_mp4),
                     "-f", "24", "-q", "standard"])
            # hyperframes는 정상 종료시 exit 0 또는 9
            if not raw_mp4.exists():
                return f"[FAIL unit{unit_num}] raw.mp4 not produced"

    # STAGE 7: FFmpeg compose
    r = run(["ffmpeg", "-y", "-i", str(raw_mp4), "-i", str(narration_mp3),
             "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
             "-shortest", str(final_mp4)], capture_output=True)
    if r.returncode != 0 or not final_mp4.exists():
        return f"[FAIL unit{unit_num}] ffmpeg compose failed"

    final_dur = get_audio_duration(final_mp4)
    final_size = final_mp4.stat().st_size / 1024
    return f"[OK unit{unit_num}] {final_dur:.2f}s · {final_size:.0f} KB · {final_mp4}"


def main():
    args = sys.argv[1:]
    skip_tts = "--skip-tts" in args
    only_final = "--only-final" in args
    units = [a for a in args if not a.startswith("--")]

    if not units:
        units = [f"{i:02d}" for i in range(1, 14)]

    results = []
    for u in units:
        try:
            r = render_unit(u, skip_tts=skip_tts, only_final=only_final)
            print(r)
            results.append(r)
        except Exception as e:
            err = f"[ERROR unit{u}] {e}"
            print(err)
            results.append(err)

    print("\n=== 일괄 렌더 완료 ===")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
