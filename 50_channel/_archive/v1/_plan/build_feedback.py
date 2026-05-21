"""
build_feedback.py — 13단원 feedback_hitl.md 일괄 생성

각 단원의 config.json + narration.txt + final.mp4 메타데이터를 합쳐
Nick이 영상 검토 시 코멘트 남기기 쉬운 양식을 만든다.
"""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # 90_video/


def get_dur(mp4: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
        capture_output=True, text=True,
    )
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def fmt_dur(d: float) -> str:
    return f"{d:.2f}초"


def count_chars(text: str) -> int:
    # 공백과 줄바꿈 제외한 글자수
    return len(text.replace(" ", "").replace("\n", "").replace(".", ""))


def build_unit(unit_num: str) -> Path:
    unit_dir = ROOT / f"unit{unit_num}"
    cfg = json.loads((unit_dir / "config.json").read_text(encoding="utf-8"))
    narration = (unit_dir / "narration.txt").read_text(encoding="utf-8")
    final_mp4 = unit_dir / "final.mp4"
    actual_dur = get_dur(final_mp4) if final_mp4.exists() else 0.0
    chars = count_chars(narration)

    md = f"""<!-- feedback_hitl.md — Unit {unit_num} -->

# Unit {unit_num} Story 영상 — 검토 노트 (HITL)

> 이 파일은 Nick의 영상 검토 작업판입니다.
> NCC가 어떻게 만들었는지 + 검토 포인트가 정리되어 있습니다.
> 각 섹션의 [ ] 체크박스와 ✏️ 빈 자리에 의견을 남겨주세요.

---

## 1. 영상 정보

| 항목 | 값 |
|---|---|
| 파일 | `90_video/unit{unit_num}/final.mp4` |
| 인물 | **{cfg["person"]}** |
| 시대·장소 | {cfg["era"]} |
| 단원 | {cfg["unit_title"]} |
| 길이 | **{fmt_dur(actual_dur)}** |
| 나레이션 글자수 | 약 {chars}자 |
| 톤 (팔레트) | `.unit-{unit_num}` |

재생 방법:
- 로컬: `python 00_project_hub/plan/serve.py` → 브라우저에서 직접 mp4 열기
- 또는 `ffplay 90_video/unit{unit_num}/final.mp4` (있으면)

---

## 2. NCC 제작 방식

### 2.1 사용한 자료(Source)
- `50_units/{unit_num}_*/story/unit{unit_num}.md` — 인물 서사 원문
- `50_units/{unit_num}_*/story.html` — 인터랙티브 서사 (5장 구조 확인)
- `20_research/02_R2-people-map.md` — R2 인물 자료 (있는 경우)
- 일반 수학사 지식 (NCC 학습 기반)

### 2.2 파이프라인
1. `90_video/unit{unit_num}/storyboard.md` — 5장면 설계
2. `narration.txt` ({chars}자) → edge-tts (ko-KR-SunHiNeural)
3. `config.json` → `build_index.py`로 마스터 템플릿 + 단원 데이터 주입
4. `index.html` (GSAP 5장면 타임라인) → HyperFrames 렌더
5. `raw.mp4` + `narration.mp3` → FFmpeg 합성 → `final.mp4`

### 2.3 시각 자산 (SVG 심볼)
- Scene 2 (인물 등장): `_assets/symbols/{cfg["s2_symbol"]}.svg`
- Scene 3 (결정적 순간): `_assets/symbols/{cfg["s3_symbol"]}.svg`
- Scene 4 (수학 연결): `_assets/symbols/{cfg["s4_symbol"]}.svg`

### 2.4 5장면 구조 (실제 길이 {fmt_dur(actual_dur)} 기준 스케일링)

| 장면 | 시간 (50초 기준) | 내용 |
|---|---|---|
| S1 (0~5s) | 타이틀 | "{cfg["person"]}" / {cfg["era"]} |
| S2 (5~15s) | 인물 등장 | "{cfg["s2_head"]}" |
| S3 (15~32s) | 결정적 순간 | 키워드: "{cfg["s3_keyword"]}" |
| S4 (32~45s) | 수학 연결 | "{cfg["s4_head"]}" |
| S5 (45~50s) | 마무리 | "{cfg["s5_text"]}" |

GSAP 타임라인은 `data-duration` 기반 비례 스케일링 (마스터 템플릿 자동).

---

## 3. 나레이션 전문

```
{narration.strip()}
```

---

## 4. 검토 체크리스트

### 4.1 기술 (객관)
- [ ] 영상이 정상 재생됨
- [ ] 한국어 폰트 깨짐 없음
- [ ] 음성-영상 sync 적절 (장면 전환과 음성 흐름 일치)
- [ ] 5장면이 명확히 구분됨
- [ ] 마지막 페이드 아웃 자연스러움

### 4.2 내용 (주관)
- [ ] 첫 5초 안에 인물명·시대 노출
- [ ] 인물의 매력이 전달되는가
- [ ] 핵심 메타포가 직관적인가
- [ ] 수학 연결이 자연스러운가 (강의 톤이 아닌가)
- [ ] 마지막 5초가 "단원 진입"의 기대감을 주는가

### 4.3 학습자 적합성 (중1 딸 기준)
- [ ] 어휘가 너무 어렵지 않음
- [ ] 톤이 따뜻하고 호기심 유발
- [ ] 영상 길이가 적당함 (지루하지 않음, 너무 짧지도 않음)
- [ ] 다시 보고 싶은 마음이 드는가

### 4.4 시각 디자인
- [ ] 단원 팔레트(색)가 인물·시대에 어울림
- [ ] SVG 심볼이 메시지와 어울림
- [ ] 텍스트가 읽히는 시간이 충분
- [ ] 여백이 충분 (산만하지 않음)

---

## 5. Nick 피드백

### 5.1 잘된 점
✏️

### 5.2 개선이 필요한 점
✏️

### 5.3 다음 버전(v2) 제안
✏️

### 5.4 종합 판정
- [ ] OK — story.html에 임베드 진행
- [ ] 부분 수정 (narration 또는 SVG 교체)
- [ ] 재제작 필요

---

## 6. 수정 작업 시 참고

수정이 필요하면 다음 중 어느 단계로 돌아갈지 명시:

- **나레이션 수정만**: `narration.txt` 편집 → `python 90_video/_plan/render_all.py {unit_num}` (TTS부터 재실행)
- **타이밍·SVG·텍스트 슬롯 수정**: `config.json` 편집 → `python 90_video/_plan/build_index.py {unit_num}` → 렌더 (`--skip-tts` 옵션)
- **장면 구조 자체 변경**: `storyboard.md` 갱신 → 위 두 단계 모두 재실행
"""
    out = unit_dir / "feedback_hitl.md"
    out.write_text(md, encoding="utf-8")
    return out


def main():
    for i in range(1, 14):
        u = f"{i:02d}"
        try:
            out = build_unit(u)
            print(f"[OK] unit{u}: {out}")
        except Exception as e:
            print(f"[FAIL] unit{u}: {e}")


if __name__ == "__main__":
    main()
