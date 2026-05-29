---
name: se-video-compose
description: 영상 제작 시스템의 단계 [영상 6] 합성 스킬. 단계 [영상 5] 렌더의 raw 영상(7-raw.mp4, 무음)과 단계 [영상 2] 나레이션 음성(4-narration.mp3)을 받아 최종 영상(8-final.mp4) + 표지(8-poster.jpg) + 메타데이터(8-meta.json)를 생성한다. 입력(raw 영상 / 나레이션 음성 / (옵션) BGM·SFX / 정체성 = 시청자·약속·A7 시리즈 정체)을 받아 동작(CM1 입력 align·길이 측정 → CM2 sync 판정 → CM3 (옵션) 음향 mix → CM4 ffmpeg mux → CM5 sync·용량 검증 → CM6 표지 추출·오버레이 → CM7 메타데이터 생성 → CM8 자체 평가·옛 1편 비교)을 진행. math-story-telling 영상의 최종 합성, A/V mux, 표지 생성, 채널 메타데이터 작성 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료(40_experiments/exp-NNN/{7-raw.mp4,4-narration.mp3}, INTEGRATED_PLAN §5.5.6·§8, 50_channel/season-1-ancient/unit-NN/final_v1_5.mp4 baseline)를 참조만 함. 외부 도구: ffmpeg / ffprobe.
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 영상 6 합성 (CM1~CM8)
  ssot: 11_video_gen_process/70_tools/se-video-compose/SKILL.md
  version: "0.1"
  status: 시드 (exp-002 STEP 8 합성 시범 실행 후 reverse-engineering 정형화)
allowed-tools: Read Write Grep Glob Bash AskUserQuestion
---

# se-video-compose — 영상 6 합성 스킬

본 스킬은 영상 제작 시스템의 단계 [영상 6], **8단계 파이프라인의 마지막**. 단계 [영상 5] 렌더의 raw 영상(`7-raw.mp4`, 무음)과 단계 [영상 2] 나레이션 음성(`4-narration.mp3`)을 받아 *최종 영상* + 표지 + 메타데이터를 만든다. 출력은 vertical slice 의 종착물 — 이후는 `final-retrospective.md` 회고 + 단계 [이전](외부 `50_channel/` 로 덮어쓰기).

상위 frame: [INTEGRATED_PLAN](../../../11_video_gen_process/00_charter/INTEGRATED_PLAN.md) §5.0 skill chain / §5.5.6 단계 [영상 6] / §8 결정 1·2.

영화로 치면 **마스터링 + 패키징**, 방송으로 치면 **송출 직전 master out**. 세 가지 일을 한다.

1. **mux(먹싱)** — 무음 raw 영상 위에 나레이션 음성(+옵션 BGM·SFX)을 얹어 한 파일로 봉합.
2. **표지(poster) 생성** — 영상 한 프레임을 뽑아 시청자가 클릭하게 만드는 표지.
3. **메타데이터 생성** — 제목·설명·태그·재생목록. 여기서 **A7 시리즈 정체**(시즌+단원+인물 혼합)가 확정.

원칙:
- 본 스킬은 외부 자료를 **참조**만 한다. 외부를 변경 X.
- **영상을 다시 그리지 않는다.** raw video stream 을 `-c:v copy` 로 무손실 통과 + 음성만 AAC 봉합 → 품질 손실 0, 수초 내 완료(lossless rewrap).
- **음성을 자르지 않는다.** 약속 3(발견의 필연성)의 "정리" 마무리 멘트를 보호 — sync 보정은 영상 쪽에서.
- sync 의 책임은 STEP 4·6 에서 끌어올리는 게 이상적(`Σ scene_dur = audio_dur`). STEP 8 은 *검증*이 본분.

---

본 v0.1 body 는 **exp-002 STEP 8 합성 시범**으로 작성됨 (2026-05-29). 시범 입력: `7-raw.mp4`(렌더 산출) + `4-narration.mp3`(**Kanna+Kyle, 140.27s**, ElevenLabs). 시범 결과: [`../../../11_video_gen_process/40_experiments/exp-002-build-unit01/8-final.mp4`](../../../11_video_gen_process/40_experiments/exp-002-build-unit01/) + `8-poster.jpg` + `8-meta.json`.

---

## 입력 (2 필수 + 2 옵션)

| # | 입력 | 형식 | 출처 |
|---|---|---|---|
| 1 | raw 영상 (무음) | `7-raw.mp4` | 40_experiments/exp-NNN/ (STEP 7 렌더 산출) |
| 2 | 나레이션 음성 | `4-narration.mp3` (sync 기준선) | 40_experiments/exp-NNN/ (STEP 4 narration 산출) |
| 3 (옵션) | BGM·SFX | 음원 경로 + 레벨 | 현재 미도입(무음 위 나레이션만) |
| 4 (옵션) | 정체성 + A7 시리즈 정체 | 시청자 + 약속 3겹 + 표지·제목 양식 | INTEGRATED_PLAN §5.1.2 A7 + §8 |

---

## 동작 (CM1~CM8)

### CM1. 입력 align + 길이 측정
- `7-raw.mp4` + `4-narration.mp3` 존재 확인
- `ffprobe` 로 양쪽 길이 측정 → `video_dur`, `audio_dur` (단원 1 = `audio_dur=140.27s`)
- (옵션) `4-narration.vtt` 자막 자산 존재 확인 (soft-sub 동봉 후보)

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 7-raw.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 4-narration.mp3   # 140.27
```

### CM2. sync 판정 (±0.3s)
- `|video_dur − audio_dur| ≤ 0.3s` 검사 → 통과 시 CM4 직행
- 초과 시 보정 분기 (**음성 자르기 금지**):
  - **영상 < 음성** (마지막 멘트 잘림 위험): 영상 끝 마지막 프레임 `tpad` freeze 연장 또는 STEP 6 으로 돌아가 S6 시간 증가
  - **영상 > 음성** (끝이 정적): 음성 끝 무음 pad 추가 또는 영상 끝 fade-out 자연 종결

### CM3. (옵션) 음향 mix — 현재 미도입
- BGM(−20dB 이하) + SFX(S3 "ding" 등) 레이어, ducking(`sidechaincompress`)
- 도입 시: **나레이션 loudnorm(−14 LUFS) 먼저 → BGM −20dB** 순서로 밸런스
- 현 단원 1 = 무음 위 나레이션만으로 vertical slice 완성. 음향 가치는 A/B 검증(가설 3) 후 도입.

### CM4. mux ⭐ (검증된 핵심 명령)
- 영상 video stream 무손실 `copy` + 음성 AAC 192k, 짧은 쪽 기준 종료(`-shortest`)
- `+faststart`(moov atom 앞으로) — 스트리밍·미리보기 친화

```bash
ffmpeg -i 7-raw.mp4 -i 4-narration.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  -movflags +faststart 8-final.mp4
```

### CM5. sync·용량 검증
- stream 별 duration delta 측정 (sync 오차)
- 파일 크기 < 25MB (GitHub Releases / 일반 업로드 친화)

```bash
ffprobe -v error -show_entries stream=codec_type,duration \
  -of default=nw=1 8-final.mp4
```

### CM6. 표지 추출 + 오버레이 ⭐
- S1 황금시간대 프레임(예: 8초 지점) 추출 → A7 양식 gold serif 오버레이
- 시점은 `-ss <시점>` 로 지정. 베이스 프레임 후보: S1(시대, 1순위) / S2(인물) / S4(결정적 순간) — A/B 가능

```bash
# 표지 프레임 1장 추출
ffmpeg -ss 00:00:08 -i 8-final.mp4 -frames:v 1 -q:v 2 8-poster.jpg

# (옵션) A7 양식 gold serif 오버레이 — 인물 핵심 단어 + 한 단어
ffmpeg -i 8-poster.jpg -vf \
  "drawtext=fontfile='Noto Serif KR':text='에라토스테네스':fontcolor=0xE89B4F:fontsize=64:x=(w-tw)/2:y=h-180, \
   drawtext=fontfile='Noto Serif KR':text='정리':fontcolor=0xE89B4F:fontsize=96:x=(w-tw)/2:y=h-110" \
  8-poster.jpg
```

### CM7. 메타데이터 생성 (`8-meta.json`) — A7 시리즈 정체 확정
약속 3겹(시대/인물/필연성)을 설명 3문장으로, 제목은 `[인물] 한_단어 + 단원` 포맷으로 자동 초안 → Nick 윤문.

| 항목 | 예시 (단원 1) | 근거 |
|---|---|---|
| `title` | `[에라토스테네스] 책을 정리하다 수를 정리한 사람 · 중1 소수` | A7: 인물 제목 + 한 단어("정리") |
| `description` | 시대 한 줄 + 인물 한 줄 + 발견 한 줄 + 단원 연결 (CTA 없음) | 약속 3겹, A6(강제 CTA X) |
| `tags` | `에라토스테네스, 소인수분해, 소수, 에라토스테네스의 체, 중1수학, 수학자이야기, 알렉산드리아` | 검색 진입 |
| `season` | `season-1-ancient` | A7 메인 분류 |
| `unit` | `unit-01` | A7 sub 재생목록(학습자 진입) |
| `person` | `eratosthenes` | A7 영상 제목 핵심 |
| `one_word` | `정리` | 진화 원칙 5("한 단어" 압축) |
| `duration` | `140.27s` (음성 기준, sync 후 확정) | sync 검증값 |
| `not_yielded` | (양보하지 않은 것 한 줄) | 진화 원칙 6 — 모이면 "시리즈의 영혼" |

### CM8. 자체 평가 + 옛 1편 비교
- 평가 기준 자동 체크(아래) + 약속 3겹 부합 시드
- 옛 1편(`final_v1_5.mp4`) 비교 → 특히 약속 3(발견의 필연성) 보강 여부를 Nick 검증에 인계

---

## 출력

```text
<exp>/
├── 8-final.mp4    ← 최종 영상 (gitignore, GitHub Releases 로 배포)
├── 8-poster.jpg   ← 표지 (gitignore)
└── 8-meta.json    ← 제목 / 설명 / 태그 / 재생목록 / 시리즈 정체 (A7)
```

---

## 평가 기준

| 항목 | 합격 |
|---|---|
| **sync 오차** | `|video_dur − audio_dur| ≤ ±0.3s` (단원 1 = ±0.3 of 140.27) |
| **파일 크기** | < 25MB |
| mux 방식 | `-c:v copy` 무손실 (영상 재인코딩 회피) |
| 음향 밸런스 | BGM 도입 시 −20dB 이하 / 나레이션 −16~−14 LUFS |
| 표지 | 베이스 프레임 + A7 양식 gold serif 오버레이 |
| 메타데이터 | 제목·설명·태그·시즌·단원·인물·한 단어 작성 완료 |
| A7 시리즈 정체 | 시즌+단원+인물 혼합 양식 확정 (Nick) |
| 약속 3겹 | Nick 시청 — 특히 약속 3(발견의 필연성) 옛 1편 대비 보강 |

---

## QnA 패턴 시드

- *"sync 오차 > 0.3s → 영상 freeze/fade 보정 / STEP 6 재실행?"* (음성 자르기는 X)
- *"음향(BGM·SFX) = 미도입(무음) / 도입(−20dB + ducking)?"* (현재 미도입)
- *"표지 베이스 = S1 도서관 와이드(1순위) / S2 인물 / S4 결정적 순간?"*
- *"A7 제목 포맷·재생목록 단위·CTA 유무 확정?"* (시즌 전체 적용 — Nick 필수)
- *"자막 = 미동봉 / VTT soft-sub(`-c:s mov_text`) / 번인?"* (VTT 이미 존재 — 추가 비용 0)

---

## 리서치 패턴 시드

본 스킬은 입력 풍부(raw 영상 + 음성 + storyboard 표지 원료)하면 외부 리서치 *불필요*. 다음 경우만:

1. ffmpeg 필터 문법 (`tpad`/`sidechaincompress`/`loudnorm`/`drawtext`) — 공식 docs
2. BGM·SFX 라이브러리 탐색 (음향 도입 시 — sub-agent 위임 후보)
3. YouTube 메타데이터/챕터마커 spec — 배포 자동화(§8) 시

---

## 진화 메커니즘

- **v0.1** (2026-05-29) — exp-002 STEP 8 합성 시범. mux(`-c:v copy + AAC -shortest`) + 표지 추출(`-ss + drawtext`) + sync 검증(±0.3s) + 용량(<25MB) + A7 메타데이터 스키마. 음향 미도입(무음 위 나레이션). 현행.
- **v0.2** (예정 — vertical slice 회고 후):
  - sync 책임 STEP 4·6 으로 상향 (`Σ scene_dur = audio_dur`) → STEP 8 = 검증만
  - 표지 자동 후보 3장 + 점수화(여백·얼굴·대비) → Nick 고르기만
  - 메타데이터 자동 초안 템플릿 (약속 3겹 → description 3문장)
  - loudnorm(−14 LUFS) 표준화 + VTT soft-sub 동봉
  - `compose.py` 단일 스크립트화 (CM1~CM7 ffprobe JSON 파싱)
- **v0.3+** = 음향 stem 믹싱(BGM/SFX/ambience/ducking) + 인트로·아웃트로 + 시즌 LUT + 배포 자동화(YouTube Data API) + 다음 단원 일반화(입력값만 교체).

---

## 호출 방법

```yaml
스킬: se-video-compose
입력:
  1. raw 영상: 40_experiments/exp-NNN/7-raw.mp4 (무음, STEP 7 산출)
  2. 나레이션 음성: 40_experiments/exp-NNN/4-narration.mp3 (sync 기준선)
  3. (옵션) BGM·SFX: 음원 + 레벨 (현재 미도입)
  4. (옵션) 정체성 + A7: INTEGRATED_PLAN §5.1.2 A7 + §8
출력:
  - 40_experiments/exp-NNN/8-final.mp4 (gitignore)
  - 40_experiments/exp-NNN/8-poster.jpg (gitignore)
  - 40_experiments/exp-NNN/8-meta.json
다음 단계: 없음 (vertical slice 종착점) → final-retrospective.md + 단계 [이전](50_channel/)
```

본 시범 호출 예시: [`../../../11_video_gen_process/40_experiments/exp-002-build-unit01/8-final.mp4`](../../../11_video_gen_process/40_experiments/exp-002-build-unit01/) + `8-poster.jpg` + `8-meta.json`.
