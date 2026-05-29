---
name: se-video-motion
description: 영상 제작 시스템의 단계 [영상 4] 모션 스킬. 단계 [영상 1] 스토리보드의 카메라 워크(부록 C) + 단계 [영상 2] 나레이션의 scene별 음성 길이 + 단계 [영상 3] 이미지 목록을 받아 scene별 모션(push in / zoom out / ken burns / pan / slow zoom)과 자막 타이밍을 정합한 모션 config.json을 생성한다. 입력(스토리보드 부록 C / 나레이션 mp3·jsonl 의 scene별 시간 / 이미지 목록 + 재사용 맵 / (옵션) 카메라 워크 승인·수정)을 받아 동작(입력 align → 음성 길이 측정 → scene별 시간 확정 → 모션 매핑 → 자막 타이밍 배치 → config 직렬화 → 자가 검증)을 진행. math-story-telling 영상의 scene 모션 결정, 음성-모션-자막 동기화, ken burns/pan/zoom 연출, STEP 7 렌더(FFmpeg zoompan) 입력 config 작성 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료(40_experiments/exp-NNN/3-storyboard.md 부록 C, 4-narration.{mp3,jsonl}, 5-images/*.png)를 참조만 함. 외부 도구: ffprobe(음성 길이·경계 측정). 출력 config는 다음 단계 [영상 5] 렌더의 FFmpeg zoompan/drawtext가 기계 판독.
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 영상 4 모션 (MO1~MO6)
  ssot: 11_video_gen_process/70_tools/se-video-motion/SKILL.md
  version: "0.1"
  status: 시드 (exp-002 STEP 6 시범 실행 후 reverse-engineering 정형화)
allowed-tools: Read Write Grep Glob Bash AskUserQuestion
---

# se-video-motion — 영상 4 모션 스킬

본 스킬은 영상 제작 시스템의 단계 [영상 4]. STEP 5까지 만든 *정적 자원*(이미지 4~6장 + 나레이션 음성)을 *움직이는 영상의 설계도*로 바꾼다. 각 그림에 **시간**(언제부터 언제까지 화면에 머무는가), **카메라 운동**(push in / zoom out / ken burns / pan / slow zoom), **자막의 등장·퇴장 타이밍**을 부여한다. 출력 `NN-motion-config.json`은 "이 그림을 18.23초 동안 1.0→1.08배로 천천히 밀고 들어가라, 그동안 23.5초에 'β' 자막을 띄워라"라는 **프레임 단위 연출 명세**다. 실제 픽셀은 다음 단계 [영상 5] 렌더가 FFmpeg `zoompan`/`drawtext`로 그리지만, **무엇을 어떻게 움직일지의 결정**은 전부 이 단계에서 끝난다.

상위 frame: [INTEGRATED_PLAN](../../00_charter/INTEGRATED_PLAN.md) §5.0 skill chain / §5.5.4 단계 [영상 4] 모션.

원칙:
- 본 스킬은 외부 자료를 **참조**만 한다. 외부를 변경 X.
- **음성이 시간을 정한다** — 모션의 시간은 자유롭게 정할 수 없다. 이미 합성된 음성(`4-narration.mp3`)이 시간의 절대 기준이다. scene 경계는 음성의 화제 전환점에 고정되고, 모션은 그 칸 안에서만 움직인다.
- **정적 입력으로 동적 인상** — 촬영본이 없으므로 한 장의 그림에서 ken burns(서서히 확대·이동)로 운동감을 짜낸다.
- **자막은 음성에 종속** — 자막 start/end는 스토리보드 초 단위가 아니라 합성된 음성의 **발화 시점**(jsonl turn)에 맞춘다.
- 4축 기여: **B. 흥미 유발(주축)** — 모션은 "지루한 슬라이드쇼"와 "한 편의 짧은 다큐"를 가르는 차이. **A. 개념 이해(보조)** — 자막 타이밍이 개념 설명과 정확히 맞물릴 때.

---

본 v0.1 body 는 **exp-002 STEP 6 시범**으로 작성됨 (2026-05-29). 시범 결과: [`../../40_experiments/exp-002-build-unit01/6-motion-config.json`](../../40_experiments/exp-002-build-unit01/6-motion-config.json) (8 scene, 140.27s).

---

## 입력 (3 필수 + 1 옵션)

| # | 입력 | 형식 | 출처 |
|---|---|---|---|
| 1 | 스토리보드 카메라 워크 | `3-storyboard.md` 부록 C (S1 push in / S2 zoom out / S3 ken burns / S4 pan / S5 swipe / S6 fade) | 40_experiments/exp-NNN/ |
| 2 | 나레이션 음성 + 발화 시점 | `4-narration.mp3`(시간의 절대 기준) + `4-narration.jsonl`(자막 발화 시점) + `concat.txt`(turn+silence 누적) | 40_experiments/exp-NNN/ |
| 3 | 이미지 목록 + 재사용 맵 | `5-images/*.png` + 부록 B(캐릭터 reuse, 예: S6=S1) | 40_experiments/exp-NNN/ |
| 4 (옵션) | 카메라 워크 승인·수정 | "S4는 pan으로" 같은 한 줄 + 결정적 순간 지정 | 기본 = 카메라 언어 사전 자동 |

---

## 동작 (MO1~MO6)

### MO1. 입력 align
- storyboard 부록 C(scene별 카메라 워크) + `4-narration.mp3`/`jsonl` + `5-images/` 파일 경로·재사용 맵 수신·검증
- scene 정서 단서 식별: 도입/회귀(빨려들기), 인물 소개(물러나기), 발견의 과정(응시), 공간 이동(이동), 병렬 인물(정적·대등)
- 결정적 순간(약속 3겹 중 발견의 필연성 서사) scene 표시 — 스토리보드 ★ 자동 인식

### MO2. 음성 길이 측정 (시간의 절대 기준)
- `ffprobe`로 mp3 총길이 측정 + `concat.txt`의 turn+silence(scene 경계 1000ms) 누적으로 scene 경계 타임코드 추출 → start/end 확정
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 4-narration.mp3
# concat.txt(turn별 + scene 경계 silence)를 누적해 scene 경계 타임코드 산출
```
- **분기 (HITL): scene 분할** — 음성이 길어 한 이미지가 ~22초 이상 연속 머물면 이미지를 2장으로 분할. exp-002에서 S3(소수의 체)가 39.74초로 길어 `7-S3-Hands.png`(손)와 `8-S3.5-Sieve.png`(체)로 **S3a/S3b 분할**. 시간 구조를 바꾸므로 Nick 확인.

### MO3. 모션 매핑 (scene 정서 → 카메라 언어)
카메라 언어 사전(아래)에서 scene 정서에 맞는 motion·zoom 선택:

| motion | zoom | 정서·용도 | exp-002 scene |
|---|---|---|---|
| `push_in` | 1.0→1.08 | 도입, 세계로 빨려들기 | S1 무세이온 |
| `zoom_out` | 1.08→1.0 | 인물 클로즈업 → 맥락으로 물러나기 | S2 베타 |
| `ken_burns` | 1.0→1.05 | 발견의 과정, 살아있는 응시 | S3a 손 ★ |
| `slow_zoom` | 1.0→1.05 (또는 1.02→1.06) | 정적·대등(병렬 인물·격자 응시) | S3b 체 / S5a 유클리드 / S5b 류후이 |
| `pan_right` | 1.05 고정 | 공간 이동(지중해 건너기) | S4 시러큐스 |
| `zoom_in` | 1.0→1.08 | 클로징, 회귀·수렴(수미상관) | S6 정리 |

- **분기**: 자막·내부 도식이 이미 정보를 운반하면 카메라는 약한 motion으로 양보(S3 체).
- **HITL**: 결정적 순간을 어느 카메라로 살릴지는 연출 감각이 들어가는 지점.

### MO4. 자막 타이밍 배치 (음성 발화 시점 종속)
- 스토리보드 자막 핵심 단어가 `4-narration.jsonl`의 어느 turn에서 발화되는지 찾아 그 시점에 start/end 배치
- start = 발화 직전~직후, end = 다음 화제 전까지 (여운이 필요하면 음성 끝 후에도 잔존)
- 각 caption = text·x(center 등)·y(상대좌표 0~1)·size·color(palette key)·start·end
- **색 정책**: `gold`=개념·인물명 강조 / `white`=부가정보
- **자막 릴레이**: 한 자막이 사라지는 순간 핵심 메시지가 솟아오르게 배치(S5b "류후이…" 사라짐 → "인류, 같은 답에 두 번" 등장)
- **y좌표 충돌 회피**: 동시 표시 자막 ≤ 2개, y 분리(예 0.30/0.45/0.82)

### MO5. config 직렬화 (`NN-motion-config.json`)
전역 메타 + `scenes[]` + `transition`을 JSON으로 출력 (STEP 7이 그대로 기계 판독):

```jsonc
{
  "_comment": "scene별 시간=음성 sync 기준(scene 이미지는 다음 scene 음성 시작까지 표시). 자막=storyboard 기준 한글.",
  "fps": 25,
  "resolution": [1280, 720],
  "total_duration": 140.27,
  "audio": "4-narration.mp3",
  "font": "C:/Windows/Fonts/NotoSerifCJKkr-Regular.otf",
  "palette": { "gold": "0xE89B4F", "white": "0xFFFFFF", "shadow": "0x000000" },
  "scenes": [
    {
      "id": "S2", "img": "5-images/2-S2-Close-up.png",
      "start": 18.23, "end": 33.87, "motion": "zoom_out",
      "zoom": [1.08, 1.0],
      "captions": [
        { "text": "β", "x": "center", "y": "0.30", "size": 130, "color": "gold", "start": 23.5, "end": 30.0 },
        { "text": "베타 — 모든 분야 2등", "x": "center", "y": "0.82", "size": 40, "color": "white", "start": 26.0, "end": 33.0 }
      ]
    }
    // ... scene 반복
  ],
  "transition": { "type": "fade", "in": 0.6, "out": 0.6, "_note": "각 scene 클립 시작/끝 fade. concat으로 길이 보존(음성 sync)." }
}
```

### MO6. 자가 검증 (자동 lint)
- [ ] **시간 정합**: Σ(scene.end − scene.start) = `total_duration` (예: 140.27)
- [ ] scene start/end 가 음성 sync 타임코드와 일치 (이미지 = 다음 scene 음성 시작까지)
- [ ] 모든 `caption.end` ≤ 소속 scene.end
- [ ] zoom 범위 1.0~1.12 이내 (과다 시 픽셀 보간 흐려짐)
- [ ] 동시 표시 자막 ≤ 2개 + y좌표 충돌 없음
- [ ] 재사용 이미지(S6=S1)는 motion만 바꿔 차별(push_in→zoom_in 수미상관)

---

## 출력

- `<exp>/6-motion-config.json` (STEP 번호 prefix `6-`. 전역 메타 + `scenes[]` + `transition`)

### scenes[] 구조 (exp-002 실제 8 scene)

| scene | 시간(s) | 길이 | img | motion | zoom | 정서 |
|---|---|---|---|---|---|---|
| S1 | 0–18.23 | 18.23 | 4-S1-Museion | push_in | 1.0→1.08 | 세계로 빨려들기 |
| S2 | 18.23–33.87 | 15.64 | 2-S2-Close-up | zoom_out | 1.08→1.0 | 인물→맥락 물러나기 |
| S3a ★ | 33.87–56.36 | 22.49 | 7-S3-Hands | ken_burns | 1.0→1.05 | 발견의 과정(손) |
| S3b | 56.36–73.61 | 17.25 | 8-S3.5-Sieve | slow_zoom | 1.02→1.06 | 소수의 체 응시 |
| S4 | 73.61–95.31 | 21.70 | 3-S4-Syracuse | pan_right | 1.05 고정 | 지중해 건너기 |
| S5a | 95.31–106.4 | 11.09 | 5-S5-Euclid | slow_zoom | 1.0→1.05 | 병렬 인물 1 |
| S5b | 106.4–117.54 | 11.14 | 6-S5-LiuHui | slow_zoom | 1.0→1.05 | 병렬 인물 2 |
| S6 | 117.54–140.27 | 22.73 | 4-S1-Museion(재사용) | zoom_in | 1.0→1.08 | 회귀·수렴 |

**핵심 연출 (exp-002)**:
- **scene 분할** = "음성이 시간을 정한다"의 실현 — S3가 39.74초로 길어 **S3a(손)/S3b(체)** 2분할.
- **자막은 음성 종속** — "소수의 체"(gold, y0.88) **67.0–73.3** = turn19 "소수의 체!" 발화 시점. 39초 장면의 끝 6초에만 등장.
- **자막 릴레이** — S5b "류후이 · 기원후 263년"(107.5–114.0) 사라짐 → "인류, 같은 답에 두 번"(gold, y0.45, **114.0–117.5**) 솟아오름.
- **수미상관** — S6 = S1 무세이온 재사용, motion만 push_in→zoom_in.
- **한 단어 닻** — S6 "정리"(gold, size 150 = 최대, y0.40, 123.0–136.0) + 부제(white).

### 다음 STEP 연결
STEP 7 렌더가 이 JSON을 그대로 기계 판독: `img`+`zoom[0→1]`+`motion` → FFmpeg `zoompan` / `captions[]` → `drawtext`(`enable='between(t,…)'`) / `transition.fade` → 각 clip `fade` / `concat`으로 clip 이어붙여 **길이 보존**(음성 sync). clips/ 디렉토리에 scene별 mp4가 떨어지고, STEP 8에서 `4-narration.mp3`와 합성된다.

---

## 평가 기준

| 항목 | 합격 |
|---|---|
| 시간 정합 | Σ(end−start) = total_duration (자동 MO6) |
| scene 경계 = 음성 sync | scene start/end = 화제 전환 타임코드 |
| 자막 경계 | 모든 caption.end ≤ scene.end |
| sync 체감 | (Nick) 음성 듣고 자막이 말과 맞는가 |
| 정서 적합 | (Nick) 결정적 순간 모션이 감정을 살리는가 |
| 가독성 | y좌표 충돌 없음, 자막이 얼굴/핵심 안 가림 |
| zoom 범위 | 1.0~1.12 이내 |
| 카메라 언어 일관 | 사전(MO3)대로 정서→motion 매핑 |

---

## QnA 패턴 시드

- *"이 scene의 정서는?(빨려들기/물러나기/응시/이동/대등) 그것을 운반할 카메라 언어는?"*
- *"결정적 순간(약속 3겹 중 발견의 필연성 서사)은 어느 scene? 거기 모션을 어떻게 살릴까?"*
- *"자막은 음성보다 먼저 떠야 하는가, 동시인가, 여운으로 남는가?"*
- *"음성이 길어 한 이미지가 22초 이상 머무는 scene = 둘로 분할해도 됨?"* (HITL)

## 리서치 패턴 시드

본 단계는 정합·연출 결정 위주로 외부 리서치 거의 불필요. 다음 경우만:
1. 모션 라이브러리 비교(FFmpeg zoompan vs GSAP/Lottie/Remotion) — zoompan 단일 운동 한계 부딪힐 때
2. 다큐 카메라워크(켄 번스)·영화 편집 리듬 어휘 차용 — 카메라 언어 사전 확장 시
3. forced alignment(Whisper/MFA) — 자막 프레임 단위 동기화 자동화 검토 시

---

## 진화 메커니즘

- **v0.1** (2026-05-29) — exp-002 STEP 6 시범 reverse-engineering. 카메라 언어 사전 6종 + 음성 sync 시간 확정 + scene 분할(S3a/S3b) + 자막 음성 종속(jsonl turn) + 자막 릴레이 + 수미상관(S6=S1 재사용) + MO6 자가 검증. 부록 C 카메라 워크와 정합(S1 push/S2 zoom out/S3 ken burns)하되 zoompan 단일 표현 한계로 S4 복합 운동(pan up+over+zoom in)→pan_right, S5 swipe split→이미지 2분할+slow_zoom으로 축약. 현행.
- **v0.2** (예정 — 렌더 전 단원 완주 후):
  - **자막 타이밍 자동화** — `4-narration.jsonl` turn 텍스트 + `ffprobe` turn 길이 누적으로 핵심 단어 발화 시점 기계 산출 (현재 수동 측정)
  - **config JSON Schema 고정** — 스키마 위반 즉시 검출, 빌드 시간 단축
  - **transition scene별 배열** — 부록 C cut/fade 구분 데이터화 (현재 일괄 fade 0.6s)
  - **MO6 Python lint 스크립트** — Σ시간·자막 경계·y충돌·zoom 범위 자동 검사
- **v0.3+** (비전):
  - **데이터 기반 자동 모션** — 음성 RMS 강세→zoom 펄스, 무음 1000ms→scene cut 자동 검출, 인물별 운율→카메라 개성
  - **키네틱 타이포그래피** — S3 격자(소수의 체) 배수 지우기 애니메이션 등 자막을 개념 시연 도구로 (현 한계 ② 정면 돌파)
  - **모션 프리셋 라이브러리** — 카메라 언어 사전을 `motion-presets.json`으로 외부화, 정서 태그만 주면 motion·zoom·duration 자동 매핑

### v0.1 한계 (다음 진화 입력)
- 카메라 언어 6종이 zoompan 단일 운동으로 축약(부록 C 복합 운동 손실)
- S3 격자(소수의 체) 내부 동적 도식 미구현 — 핵심 시각화가 정적 그림+늦은 자막에 머묾
- 자막 타이밍 손으로 측정·입력(자동화 안 됨)
- transition 일괄 fade 0.6초로 cut/fade 구분(부록 C) 미반영

---

## 호출 방법

```yaml
스킬: se-video-motion
입력:
  1. 스토리보드 부록 C: 40_experiments/exp-NNN/3-storyboard.md (카메라 워크)
  2. 나레이션: 40_experiments/exp-NNN/4-narration.{mp3,jsonl} + concat.txt (음성 길이 = 시간의 절대 기준)
  3. 이미지 목록: 40_experiments/exp-NNN/5-images/*.png + 부록 B 재사용 맵
  4. (옵션) 카메라 워크 승인·수정: "S4는 pan으로" / 결정적 순간 지정 / scene 분할 동의
출력:
  - 40_experiments/exp-NNN/6-motion-config.json
다음 단계: se-video-render (STEP 7, FFmpeg zoompan/drawtext) + se-video-compose (STEP 8)
```

본 시범 호출 예시: [`../../40_experiments/exp-002-build-unit01/6-motion-config.json`](../../40_experiments/exp-002-build-unit01/6-motion-config.json).
