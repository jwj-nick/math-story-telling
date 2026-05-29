<!-- 20_step_guides/08_step8_compose.md / STEP 8 [영상 6 합성] 심화 가이드 -->

# STEP 8 — [영상 6] 합성 (compose) 심화 가이드

> **스킬**: `se-video-compose` (⚠️ SKILL.md 미작성 — 본 문서 §3 에 설계 제안)
> **단계**: 8단계 파이프라인의 *마지막*. raw 영상 + 음성 → 최종 영상 + 표지 + 메타데이터
> **상위 frame**: [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md) §5.5.6 / [`../00_charter/PURPOSE.md`](../00_charter/PURPOSE.md)
> **실제 사례**: [`../40_experiments/exp-002-build-unit01/`](../40_experiments/exp-002-build-unit01/) (단원 1 / 에라토스테네스)
> **본 문서 작성일**: 2026-05-29

---

## 1. Step 개요

### 무엇을 하는가

STEP 8 은 **영상(7-raw.mp4) 과 음성(4-narration.mp3) 을 하나로 합쳐 최종 영상(8-final.mp4) 을 만들고, 그 영상을 세상에 내보낼 채비 — 표지(poster) 와 메타데이터(제목·설명·시리즈 정체) — 를 갖추는 마지막 단계**다. 앞의 7단계가 "영상을 *만드는*" 단계였다면, STEP 8 은 "영상을 *완성하고 내보내는*" 단계다. 영화로 치면 **마스터링 + 패키징**, 방송으로 치면 **송출 직전 master out** 에 해당한다.

구체적으로 세 가지 일을 한다.

1. **mux(먹싱)** — 소리 없는 raw 영상 트랙 위에 나레이션 음성 트랙(+ 옵션 BGM·SFX)을 얹어 한 파일로 봉합한다.
2. **표지(poster) 생성** — 영상의 한 프레임(S1 도서관 풍경)을 뽑아 시청자가 "클릭하게 만드는" 표지 이미지를 만든다.
3. **메타데이터 생성** — 제목·설명·태그·재생목록을 만들어 시청자가 *찾고 진입하는* 길을 깐다. 여기서 **A7 시리즈 정체** (시즌+단원+인물 혼합) 가 확정된다.

### 4축 중 어디에 기여하는가

| 축 | 기여 |
|---|---|
| **B. 흥미 유발** | ⭐ 직접 기여. 영상 자체가 축 B. 표지·제목이 시청자를 *끌어들이는* 첫 접점 |
| A. 개념 이해 | 간접. 합쳐진 영상이 소수의 체(S3) 개념을 운반 |
| C. 수학 언어 | 간접. S2 의 "β / 베타" 자막 등 표기 노출 |
| D. 문제 연습 | 무관 (영상은 흥미 트랙) |

### 파이프라인에서의 위치

```
... STEP 6 모션(config) → STEP 7 렌더(7-raw.mp4, 무음) → ★STEP 8 합성(8-final.mp4)→ [vertical slice 종료]
                                                        ↖ STEP 4 나레이션(4-narration.mp3, Kanna+Kyle 140.27s)
```

- **선행 입력 (2 필수)**: STEP 7 `7-raw.mp4` (영상, 무음), STEP 4 `4-narration.mp3` (음성)
- **선행 입력 (옵션)**: BGM·SFX (능력 흡수 §7.3 검증 항목 — 현재 미도입)
- **후행**: 없음. **STEP 8 = vertical slice 의 종착점.** 이후는 `final-retrospective.md` 작성 + 단계 [이전] (외부 `50_channel/` 로 덮어쓰기)

### 이 step 의 본질적 난제

1. **A/V 동기(sync) 의 누적 오차** — 영상은 모션 config 의 장면 시간 합으로 길이가 정해지고, 음성은 STEP 4 에서 turn 별 합성 + silence concat 으로 길이가 정해진다. **두 길이가 정확히 같다는 보장이 없다.** 영상이 음성보다 짧으면 마지막 멘트가 잘리고, 길면 끝이 정적으로 늘어진다. 본 영상은 음성 = **140.27s** 인데, raw 영상 길이가 이와 ±0.3s 안에서 맞아야 한다. 이 오차를 *어디서* (STEP 6 모션 / STEP 7 렌더 / STEP 8 합성) 흡수할지가 난제다.
2. **"끝내는" 단계 특유의 비가역성** — 합성은 모든 앞 단계의 결과가 한 파일로 굳는 지점이다. 여기서 발견된 결함(자막 오타, 음량 불균형, 표지 부적합)은 *어느 앞 단계로* 되돌아가야 하는지를 동반한다. 가장 늦게, 가장 비싸게 발견되는 결함이 여기 모인다.

---

## 2. Workflow (절차)

### 전체 흐름

```
입력 align (7-raw.mp4 + 4-narration.mp3 길이 측정)
   │
   ├─ [의사결정 1] 길이 오차 |video_dur − audio_dur| ≤ 0.3s ?
   │     ├─ YES → 그대로 mux
   │     └─ NO  → 어디서 보정? (영상 pad/trim / STEP 6·7 재실행 권고)
   │
   ├─ (옵션) 음향 레이어 — BGM·SFX mix (현재 미도입, §8 설계)
   │
   mux (ffmpeg: 영상 stream copy + 음성 AAC) → 8-final.mp4
   │
   ├─ sync 검증 (ffprobe: video/audio duration delta)
   ├─ 파일 크기 검증 (< 25MB)
   │
   ├─ 표지 추출 (ffmpeg: S1 프레임 → 8-poster.jpg + 텍스트 오버레이)
   │
   ├─ 메타데이터 생성 (제목·설명·태그·재생목록 → 8-meta.json)
   │     └─ [의사결정 2] A7 시리즈 정체 적용 (시즌+단원+인물)
   │
   └─ 자체 검증 + Nick 검증 (옛 1편 비교)
```

### 단계별 상세

| # | 동작 | 도구 | 산출 |
|---|---|---|---|
| 1 | 입력 align + 길이 측정 | `ffprobe` | `video_dur`, `audio_dur` |
| 2 | 길이 오차 판정 (±0.3s) | 계산 | 분기 결정 |
| 3 | (옵션) 음향 mix | `ffmpeg amix/sidechaincompress` | mixed audio |
| 4 | mux | `ffmpeg -c:v copy -c:a aac` | `8-final.mp4` |
| 5 | sync 검증 | `ffprobe` | delta 측정값 |
| 6 | 표지 추출 + 오버레이 | `ffmpeg -ss / drawtext` | `8-poster.jpg` |
| 7 | 메타데이터 생성 | NCC + 템플릿 | `8-meta.json` |
| 8 | 옛 1편 비교 | Nick | 약속 3겹 운반 확인 |

### 의사결정 포인트 (분기)

- **분기 1 — 길이 오차 처리**: `|video_dur − audio_dur| ≤ 0.3s` 이면 그대로 mux. 초과 시:
  - **영상 < 음성** (마지막 멘트 잘림 위험): 영상 끝에 마지막 프레임을 `tpad` 로 freeze 연장하거나, STEP 6 으로 돌아가 S6 시간을 늘린다. **음성을 자르지 않는다** (약속 3 "정리" 마무리 멘트 보호).
  - **영상 > 음성** (끝이 정적): 음성 끝에 무음 pad 를 더해 영상 길이에 맞추거나, 영상 끝 fade-out 으로 자연 종결.
- **분기 2 — 음향 도입 여부**: BGM·SFX 는 능력 §7.3 검증 대상. 현 단원 1 = **미도입(무음 영상)** 으로 vertical slice 완성 후, 음향 유무 A/B 비교(가설 3)로 가치 검증.
- **분기 3 — 표지 베이스 프레임**: S1 도서관 와이드(황금시간대)가 1순위. 인물 정체성이 강한 S2(에라토스테네스 클로즈업)도 후보 — A/B 가능.

---

## 3. Skill / Agent / Tools / Context

### 3.1 스킬 — `se-video-compose` (⚠️ 미작성, 설계 제안)

> **현 상태**: 본 단계의 SKILL.md 는 아직 작성되지 않았다(`70_tools/se-video-compose/SKILL.md` 부재). 8-final.mp4 도 미생성. 본 절은 앞 6개 스킬(`se-video-narration` 등)의 agentskills.io spec 형식을 따른 **설계 제안**이다. STEP 8 실제 실행 시 이 시드로 SKILL.md 를 신설한다.

**제안 frontmatter (agentskills.io spec / kebab-case)**

```yaml
---
name: se-video-compose
description: 영상 제작 시스템의 단계 [영상 6] 합성 스킬. raw 영상(7-raw.mp4)과
  나레이션 음성(4-narration.mp3)을 받아 최종 영상(8-final.mp4) + 표지(8-poster.jpg)
  + 메타데이터(8-meta.json)를 생성한다. 입력(raw 영상 / 음성 / (옵션) BGM·SFX /
  정체성 = 시청자·약속·A7 시리즈 정체)을 받아 동작(CM1 입력 align·길이 측정 →
  CM2 sync 판정 → CM3 (옵션) 음향 mix → CM4 ffmpeg mux → CM5 sync·용량 검증 →
  CM6 표지 추출·오버레이 → CM7 메타데이터 생성 → CM8 자체 평가·옛 1편 비교)을
  진행. math-story-telling 영상의 최종 합성, A/V mux, 표지 생성, 채널 메타데이터 작성 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/.
  외부 자료(40_experiments/exp-NNN/{7-raw.mp4,4-narration.mp3}, INTEGRATED_PLAN
  §5.5.6·§8, 50_channel/season-1-ancient/unit-NN/final_v1_5.mp4 baseline)는 참조만.
  외부 도구: ffmpeg / ffprobe.
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 영상 6 합성 (CM1~CM8)
  ssot: 11_video_gen_process/70_tools/se-video-compose/SKILL.md
  version: "0.1"
  status: 미작성 (본 가이드 §3 = 설계 시드)
allowed-tools: Read Write Grep Glob Bash AskUserQuestion
---
```

**제안 동작 (CM1~CM8)**

| 액션 | 무엇 | 핵심 |
|---|---|---|
| **CM1** 입력 align | `7-raw.mp4` + `4-narration.mp3` 확인, `ffprobe` 로 양쪽 길이 측정 | `audio_dur=140.27s` 기준 |
| **CM2** sync 판정 | `|video−audio| ≤ 0.3s` 검사 | 초과 시 보정 분기(§2 분기1) |
| **CM3** 음향 mix (옵션) | BGM(-20dB) + SFX(ding 등) 레이어 | 현재 미도입, §8 설계 |
| **CM4** mux | `ffmpeg -c:v copy -c:a aac -shortest` | 영상 재인코딩 회피(무손실·빠름) |
| **CM5** 검증 | sync delta + 용량(<25MB) + 음량 | 자동 |
| **CM6** 표지 | S1 프레임 추출 + 텍스트 오버레이 | A7 양식(시즌색+단원번호+인물한단어) |
| **CM7** 메타데이터 | 제목·설명·태그·재생목록 | A7 시리즈 정체 확정 |
| **CM8** 자체 평가 | 약속 3겹 부합 + 옛 1편 비교 시드 | Nick 검증 인계 |

### 3.2 외부 도구 — FFmpeg / ffprobe (선택 근거)

| 도구 | 용도 | 선택 근거 |
|---|---|---|
| **ffmpeg** | mux / 표지 추출 / 오버레이 / (향후)음향 mix | 무료·범용·스트림 무손실 copy 지원. STEP 7 렌더(zoompan)와 동일 툴체인 → 일관성 |
| **ffprobe** | 길이·스트림·음량 측정 | sync 검증의 SSOT. JSON 출력 → 자동 파싱 |

> **선택 사유 핵심**: 합성 단계는 *영상을 다시 그리지 않는다*. raw 영상 video stream 을 **copy** 로 그대로 통과시키고 음성만 AAC 로 봉합하면 품질 손실 0 + 수 초 내 완료. 영화 후반작업의 "lossless rewrap" 개념을 그대로 차용.

### 3.3 참조 context (SSOT)

| 파일 | 무엇을 제공 |
|---|---|
| [`INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md) §5.1.2 A7 | 시리즈 정체(시즌+단원+인물 혼합), 표지 양식 |
| [`INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md) §8 결정 1·2 | 시청자(학습자+광범) / 약속 3겹 — 메타데이터 톤 결정 |
| [`TONE_STRUCTURE.md`](../00_charter/TONE_STRUCTURE.md) | 어투·voice(Kanna/Kyle) — 영상의 음향 정체 |
| [`exp-002 CHECKLIST.md`](../40_experiments/exp-002-build-unit01/CHECKLIST.md) §8 | STEP 8 검증 기준(±0.3s / <25MB / -20dB / 표지 / 메타) |
| [`3-storyboard.md`](../40_experiments/exp-002-build-unit01/3-storyboard.md) | 표지 후보 프레임(S1·S2), 자막 폰트(gold serif), "정리" 한 단어 압축 |
| [`6-motion-config.json`](../40_experiments/exp-002-build-unit01/6-motion-config.json) | 장면 시간 → 영상 길이 결정원(sync 의 한쪽) |

### 3.4 agent 활용

본 단계는 **skill 형식**이 자연스럽다. mux·표지·메타데이터는 결정적(deterministic) 절차이고 Q&A(분기 판정·메타데이터 어투)는 본 대화 안에서 처리. 단, 음향 도입 시 BGM·SFX 라이브러리 탐색(§8)은 sub-agent(Task) 위임 후보.

---

## 4. User Input (Nick 입력)

### 무엇을 / 언제 / 어떤 형식으로

| 시점 | Nick 입력 | 형식 | 필수/선택 |
|---|---|---|---|
| 단계 진입 | "STEP 8 합성 진행" 한 줄 의뢰 | 자연어 | 필수 (트리거) |
| 음향 결정 | BGM·SFX 도입 여부 | Y/N + (Y면)라이브러리·곡 | 선택 (현재 N) |
| **A7 확정** | 시리즈 정체 양식 동의 (제목 포맷 / 재생목록 단위 / CTA 유무) | 확인 | **필수** (vertical slice 종료 직전) |
| 표지 결정 | poster 베이스 프레임 + 텍스트 동의 | 확인 | 선택 (NCC 1순위 제안) |
| 최종 검증 | 8-final.mp4 시청 + 옛 1편 비교 | 청취·시청 | **필수** |

### HITL (사람 개입) 지점

1. **A7 시리즈 정체 확정** — 메타데이터·표지의 양식이 여기서 *결정*된다. 한 번 정하면 시즌 전체 영상에 적용되므로 Nick 결정 필수.
2. **최종 영상 시청** — 자동 검증(sync·용량)이 통과해도, "약속 3겹이 *느껴지는가*"는 Nick 의 눈·귀로만 판정 가능. 특히 옛 1편의 약점(발견의 필연성 서사가 약했음)이 보강됐는지.
3. **CTA(시청 후 행동) 유무** — A6 결정(광범 시청자 = 침묵, 강제 CTA X)을 메타데이터에 어떻게 반영할지.

### 자동 진행 vs HITL

mux·sync 검증·표지 추출·메타데이터 *초안*은 NCC 자율. **양식 확정(A7)과 정서 판정(약속 3겹)만 Nick.** 시간·토큰 효율(절대 원칙 7)을 위해 재읽기·재합성 사이클은 금지하고 1-shot 검증을 원칙으로 한다.

---

## 5. Step Output (산출물)

### 산출 파일 + 위치 규약

```
exp-002-build-unit01/
├── 8-final.mp4      ← 최종 영상 (gitignore, GitHub Releases 로 배포)
├── 8-poster.jpg     ← 표지 (gitignore)
└── 8-meta.json      ← 제목 / 설명 / 태그 / 재생목록 / 시리즈 정체
```

### `8-meta.json` 메타데이터 항목 (제안 스키마)

| 항목 | 예시 (단원 1) | 근거 |
|---|---|---|
| `title` | `[에라토스테네스] 책을 정리하다 수를 정리한 사람 · 중1 소수` | A7: 인물(제목 핵심 단어) + 인물 한 단어("정리") |
| `description` | 시대 한 줄 + 인물 한 줄 + 발견 한 줄 + 단원 연결 + (CTA 없음) | 약속 3겹 요약, A6(강제 CTA X) |
| `tags` | `에라토스테네스, 소인수분해, 소수, 에라토스테네스의 체, 중1수학, 수학자이야기, 알렉산드리아` | 검색 진입 |
| `season` | `season-1-ancient` | A7 메인 분류 |
| `unit` | `unit-01` | A7 sub 재생목록(학습자 진입) |
| `person` | `eratosthenes` | A7 영상 제목 핵심 |
| `one_word` | `정리` | 진화 원칙 5("한 단어" 압축) |
| `duration` | `140.27s` (음성 기준, 영상 sync 후 확정) | sync 검증값 |
| `not_yielded` | (양보하지 않은 것 한 줄) | 진화 원칙 6 — 모이면 "시리즈의 영혼" |

### 다음 step 연결

STEP 8 = **종착점**. "다음 step" 은 없고 대신:
1. `final-retrospective.md` (vertical slice 전체 회고, 8 스킬 v0.1→v0.2 정련)
2. 단계 [이전] — `8-final.mp4` → 외부 `50_channel/season-1-ancient/unit-01/` 또는 `50_channel/people/eratosthenes/sieve/`

### 품질 검증 기준

**자동 (NCC)** — exp-002 CHECKLIST §8.4

- [ ] **sync 오차 ±0.3s 이내** (`|video_dur − 140.27| ≤ 0.3`)
- [ ] 파일 크기 **< 25MB** (GitHub Releases / 일반 업로드 친화)
- [ ] 음향 밸런스 (BGM 도입 시 **−20dB 이하**, 나레이션 −16~−14 LUFS 권장)
- [ ] 표지 = S1 프레임 기반 + A7 양식 오버레이
- [ ] 메타데이터(제목·설명·태그) 작성 완료

**Nick** — exp-002 CHECKLIST §8.5

- 최종 영상 시청 (전체 약 140s)
- 옛 1편(`final_v1_5.mp4`)과 비교 (참조만)
- **약속 3겹 운반** — 특히 약속 3(발견의 필연성 서사). 옛 1편 약점이 보강됐는가

---

## 6. 현재 구현 (exp-002 실제 사례)

### unit01(에라토스테네스) 에서 현재 어디까지 왔나

| 입력 | 상태 | 비고 |
|---|---|---|
| `4-narration.mp3` | ✅ 완료 | **Kanna(Q) + Kyle(A), 140.27s**, ElevenLabs |
| `6-motion-config.json` | ✅ 존재 | 장면 시간 → 영상 길이 결정원 |
| `7-raw.mp4` | 🟡 STEP 7 산출 예정 | 합성의 또 다른 필수 입력 |
| `8-final.mp4` | ⚪ **미생성** | 본 단계 = 진행 예정 |
| `se-video-compose/SKILL.md` | ⚪ **미작성** | §3 설계 제안 단계 |

### 음성 입력의 구체

STEP 4 회고([`retro-4-narration.md`](../40_experiments/exp-002-build-unit01/retro-4-narration.md))에 따르면 단원 1 최종 음성은 **Kanna+Kyle, 140s**(대안: Mina/Mike 152s). 38 turn dialog(Q 존댓말 + A 친절 반말), ElevenLabs `eleven_multilingual_v2`. 합성 config SSOT = `voice-pool.md §0`. 이 **140.27s** 가 STEP 8 sync 의 *기준선*이다 — 영상이 이 길이에 ±0.3s 로 맞아야 한다.

### 자막(접근성) 자산은 이미 존재

STEP 4 가 `4-narration.vtt`(타임코드 자막)를 함께 산출했다. 예:

```
1
00:00:00,100 --> 00:00:04,839
여러분, 기원전 3세기 알렉산드리아 들어봤어요?
```

→ STEP 8 합성 시 이 VTT 를 영상에 **번인(hard-sub)** 하거나 **사이드카(soft-sub)** 로 동봉할 수 있다(§8 접근성).

### 표지·메타데이터의 원료는 스토리보드에 이미 있다

`3-storyboard.md` 가 표지·메타데이터의 원료를 제공한다.

- **표지 베이스**: S1 "알렉산드리아 무세이온 외관(도리아식 기둥 6개), 황금 시간대" 와이드
- **자막 양식**: gold(#E89B4F) + serif(Noto Serif KR) + 화면 중앙 — A7 시리즈 정체 표준 후보
- **시대 팔레트**: era-ancient(테라코타 #C2683E / 황토 #D4A574 / 청동 #876A4E / 등대 화염 #E89B4F)
- **인물 한 단어**: "정리"(gold, S6 클로징) — 제목·표지 핵심 단어

### 실제 겪은 시행착오 (STEP 4 에서 합성에 인계된 교훈)

STEP 4 의 음성 합성이 워낙 험난했다(retro-4): edge-tts → ElevenLabs Free(HTTP 402 차단) → Google Cloud TTS(결제 보류) → ElevenLabs $10 충전. voice 도 Jessica/Will → Mono Beige → Annie/Onyu → **Mina/Kanna 확정**의 연쇄 폐기. 이 경험이 STEP 8 에 주는 교훈:

- **음량 balance** — voice 마다 default 음량이 달라 ffmpeg `volumedetect` 측정 후 boost(Mike +8dB, Kyle +3.8dB)했다. → 합성에서 BGM 을 얹을 때도 **나레이션 음량을 먼저 정규화(loudnorm)** 한 뒤 BGM 을 −20dB 로 깔아야 밸런스가 잡힌다.
- **pause 설계** — turn 사이 300ms + scene 경계 1000ms silence 가 음성 길이(140.27s)에 이미 반영돼 있다. 영상 장면 전환(1s fade)과 이 음성 호흡이 *어긋나지 않게* sync 를 맞춰야 한다.

### 예상 ffmpeg 레시피 (구체)

```bash
# 1) 길이 측정 (sync 기준)
ffprobe -v error -show_entries format=duration -of csv=p=0 7-raw.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 4-narration.mp3   # 140.27

# 2) mux — 영상 무손실 copy + 음성 AAC, 짧은 쪽 기준 종료
ffmpeg -i 7-raw.mp4 -i 4-narration.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  -movflags +faststart 8-final.mp4

# 3) sync 검증 (delta 출력)
ffprobe -v error -show_entries stream=codec_type,duration \
  -of default=nw=1 8-final.mp4

# 4) 표지 추출 — S1 황금시간대 프레임(예: 8초 지점) + gold serif 오버레이
ffmpeg -ss 00:00:08 -i 8-final.mp4 -frames:v 1 -q:v 2 _poster_raw.jpg
ffmpeg -i _poster_raw.jpg -vf \
  "drawtext=fontfile='Noto Serif KR':text='에라토스테네스':fontcolor=0xE89B4F:fontsize=64:x=(w-tw)/2:y=h-180, \
   drawtext=fontfile='Noto Serif KR':text='정리':fontcolor=0xE89B4F:fontsize=96:x=(w-tw)/2:y=h-110" \
  8-poster.jpg
```

### 현재 구현의 강점과 한계

| | 내용 |
|---|---|
| **강점** | mux 는 ffmpeg `-c:v copy` 로 무손실·수초 완료. 입력(음성 140.27s, 자막 VTT, 표지 원료)이 모두 준비됨. 검증 기준(±0.3s / <25MB)이 CHECKLIST 에 명확 |
| **한계** | (1) `7-raw.mp4` 미생성 → 실제 sync 미검증 (2) SKILL.md 미작성 (3) **음향(BGM·SFX) 미도입** — 현재 영상은 무음 위 나레이션만 (4) 표지·메타데이터 *양식*(A7)이 미확정 (5) 영상/음성 길이 일치를 *누가* 보장하는지 책임 단계 미정 |

---

## 7. 개선 방향 탐색 / 아이디어

### 단기 실현 가능 개선

1. **sync 의 책임을 STEP 4·6 으로 끌어올린다.** 합성에서 길이를 맞추는 것은 *사후약방문*이다. STEP 4 가 음성 길이(140.27s)를 확정하면, STEP 6 모션 config 의 장면 시간 합을 **그 값에 못 박는다**(`Σ scene_dur = audio_dur`). 그러면 STEP 8 의 sync 오차는 구조적으로 0 에 가까워진다. STEP 8 은 *검증만* 한다.
2. **표지 자동 후보 3장 + 점수화.** S1(시대)·S2(인물)·S4(결정적 순간) 프레임을 모두 뽑아, 여백 비율(텍스트 공간)·얼굴 검출·색 대비를 점수화해 1순위를 자동 추천. Nick 은 *고르기만* 한다.
3. **메타데이터 자동 초안 → Nick 윤문.** 약속 3겹(시대/인물/필연성)을 description 3문장으로 자동 구성하는 템플릿. 제목은 `[인물] 한_단어 + 단원` 포맷으로 자동 생성.
4. **loudness 정규화(loudnorm)** 를 mux 전 표준화. YouTube 타겟 −14 LUFS 로 나레이션을 맞춰 두면, 어느 voice 조합(Kanna/Kyle vs Mina/Mike)이든 음량이 일정.
5. **자막 동봉(VTT soft-sub)** — 이미 있는 `4-narration.vtt` 를 `-c:s mov_text` 로 mp4 에 넣거나 사이드카로 배포. 접근성 즉시 향상, 추가 비용 0.

### 자동화·효율·품질 아이디어

- **mux + 검증 + 표지 + 메타 를 한 스크립트로** (`compose.py`) — CM1~CM7 을 ffprobe JSON 파싱 기반 단일 실행. 사람 시간 ↓.
- **회귀 검증 게이트** — `assert sync_delta ≤ 0.3 and size < 25MB`. 통과 못 하면 *어느 단계로 돌아가라*까지 메시지로 출력.

### 실패/리스크 요소와 대응

| 리스크 | 증상 | 대응 |
|---|---|---|
| sync 누적 오차 | 마지막 "정리" 멘트 잘림 | 음성 자르기 금지 → 영상 끝 freeze/fade(§2 분기1) |
| 음량 불균형 | 나레이션 대비 BGM 큼 | loudnorm 먼저 → BGM −20dB |
| 파일 과대 | >25MB | CRF 조정(STEP 7) 또는 bitrate cap. 단 *재인코딩*은 STEP 7 책임 |
| 표지 텍스트 충돌 | 인물 얼굴 위 글자 | 여백 30% 규칙(이미지 단계) + 하단 배치 |
| anachronism 표지 | 시대 부정합 이미지 | STEP 5 이미지 단계 검수로 이미 차단 |

---

## 8. 고급 Workflow (상상력·창의력)

> 이 절은 "이상적이라면 이렇게"의 비전이다. 현 단계를 뛰어넘는 미래형 합성 파이프라인.

### 8.1 음향 믹싱 — 영화 후반작업의 다층 차용

현재 영상은 *무음 위 나레이션*뿐이다. 영화 사운드 디자인의 **stem(분리 트랙) 믹싱**을 차용하면:

```
Final Mix = Dialogue(나레이션) + Music(BGM) + SFX(효과음) + Ambience(환경음)
            −14 LUFS         −20dB        spot       −30dB(베드)
```

- **시대 팔레트별 BGM 1곡** (능력 §7.3) — era-ancient = 리라/현악 잔잔. 시즌마다 시그니처 악기(시즌1 고대=리라, 시즌2 중세=류트)를 두면 *소리만 들어도 시즌이 떠오르는* 청각 브랜딩.
- **결정적 순간 SFX** — 스토리보드 S3 의 소수 강조 "ding"(2·3·5, 3회), S4 "두루마리 펴지는 소리", S5 "동방 5음 음계 미세(3s)"가 이미 설계돼 있다. 이것을 실제 SFX 로 spot 배치.
- **Ducking(사이드체인 컴프레션)** — 나레이션이 들어올 때 BGM 음량을 자동으로 −6dB 낮춰 말소리를 *항상 또렷하게*. ffmpeg `sidechaincompress` 로 구현. 방송 송출의 표준 기법.
- **Ambience 베드** — S1 도서관의 *희미한 군중·발소리*, S4 *파도소리*를 −30dB 베드로 깔아 "그 시대에 들어갔다 옴"(약속 1)을 청각으로 보강.

### 8.2 인트로/아웃트로 + 채널 브랜딩

- **3초 인트로 sting** — 시즌 시그니처 사운드 + 로고 모션. 모든 영상 공통 → *채널 정체성*.
- **아웃트로 카드** — S6 "정리" 클로징 후, 동일 시즌 다음 인물 썸네일을 5초 노출(단, A6 = 강제 CTA X 원칙 → "구독" 외치지 않고 *조용히 다음 영상 카드만*).
- **로워서드(name plate)** — 인물 첫 등장 시 "에라토스테네스 · BCE 276–194 · 알렉산드리아"를 gold serif 로 — 다큐(BBC/NHK) 차용. 시즌 공통 양식 = 브랜딩.
- **컬러 그레이딩 LUT** — 시즌별 색조 LUT(시즌1=황금빛 따뜻). 합성 단계 마지막에 일괄 적용해 *시리즈 통일감*.

### 8.3 자동 썸네일·메타데이터 생성 (AI 보조)

- **썸네일 A/B 자동 생성** — 인물 표정·텍스트 배치를 달리한 2~3안을 자동 생성, CTR 데이터(§8.5)로 승자 학습.
- **메타데이터 LLM 생성** — 스토리보드·나레이션을 입력으로 제목 5안 + 설명 + 태그 + 챕터마커(타임코드)를 자동 초안. 챕터마커는 VTT 의 scene 경계(S1~S6)에서 자동 추출.
- **다국어 메타데이터** — 제목·설명을 영/일/중으로 자동 번역해 글로벌 검색 노출.

### 8.4 다국어 / 접근성 (포용 설계)

| 기능 | 구현 | 가치 |
|---|---|---|
| **한국어 자막 번인/사이드카** | 기존 `4-narration.vtt` mux | 청각장애·소음 환경 시청 |
| **다국어 자막** | VTT → 번역 트랙 추가(en/ja) | 글로벌 학습자 |
| **청각장애(SDH) 자막** | 자막에 효과음 표기 `[리라 음악]`, 화자 구분 `[Q]/[A]` | 진정한 접근성 |
| **오디오 디스크립션** | 시각 장면을 음성 설명하는 부 트랙 | 시각장애 — 영상도 "들을" 수 있게 |
| **음성 더빙(다국어)** | 같은 voice 엔진으로 en/ja 나레이션 재합성 | 시즌 확장 시 |

> 자막은 *추가 비용 0*(이미 VTT 존재) — **가장 먼저 켜야 할 접근성 스위치**.

### 8.5 배포 자동화 + 시청 데이터 피드백 루프

```
8-final.mp4 ──→ YouTube Data API v3 (upload)
                  ├─ title/description/tags/playlist 자동 세팅(8-meta.json)
                  ├─ 썸네일 업로드(8-poster.jpg)
                  └─ 자막 트랙 업로드(VTT)
                        │
                        ▼
              YouTube Analytics API
                  ├─ CTR(표지 효과) / 평균 시청 지속 / 이탈 지점
                  └─ ┐
   ┌──────────────────┘
   ▼ 피드백 루프 (진화 원칙 2)
 "S3(소수의 체) 25s 에서 이탈 급증" → STEP 3 스토리보드 호흡 재설계
 "표지 A 가 B 보다 CTR 1.8배" → 표지 양식 표준 갱신
 "자막 켠 비율 40%" → 다국어 자막 우선순위 ↑
```

- **이탈 곡선(retention) → 스토리보드 환류** — 어느 장면에서 시청자가 떠나는지가 *다음 단원 스토리보드*의 입력. 진화 원칙 1(다듬기 사이클)의 외부 데이터 채널.
- **영화 마스터링 차용** — 최종 출력 직전 `loudnorm`(EBU R128, −14 LUFS) + 색 LUT + faststart(moov atom 앞으로) = "방송 송출 master".
- **버전 관리** — `8-final_v1.mp4`(무음) / `v2`(음향) / `v3`(음향+자막)을 Releases 로 보존, 가설 3(음향 가치) A/B 검증의 물증.

---

## 9. 고급 Contents 생성 방법 (품질 도약)

### 9.1 합성 단계에서만 가능한 "차별화 포인트"

합성은 *모든 트랙이 한자리에 모이는 유일한 지점*이다. 여기서만 가능한 질적 도약:

1. **소리·그림·글자의 동시 정렬(multimodal sync)** — S3 에서 "2, 3, 5는 소수"라는 나레이션 음성, 격자에서 배수가 지워지는 모션, gold "소수의 체" 자막, "ding" SFX 가 *같은 0.5초*에 터지면 — 세 감각이 한 점에 모여 **기억에 박힌다.** 이 정렬은 합성에서만 조율 가능.
2. **여운의 침묵(약속 3 보호)** — S6 "한 단어로, 정리!" 이후 BGM 만 1.5초 잔향으로 남기고 fade. A6(강제 CTA X)와 일치하는 *정서적 마침표*. 침묵도 디자인이다.

### 9.2 학습 효과·몰입·정서 연결 강화

- **약속 3겹의 청각 대응** — (1)시대=Ambience 베드(도서관 군중·파도) (2)인물 정서=voice 톤(Kyle 의 차분 친절) (3)발견 필연성=결정적 순간 SFX+음악 고조(S3→S4). 세 약속을 *소리로도* 한 번 더 운반.
- **think-box 여백(진화 원칙 7)** — S6 마지막을 *질문으로 끝나는 30초 보조 영상*으로 분기 생성 가능. 본편 끝의 "한 단어로 뭘까?"(A 의 되묻기)를 *답 없이* 끝내는 버전 = 학습자가 채울 빈칸.

### 9.3 시리즈 정체성·일관성·확장성 (A7 운영)

> **A7 시리즈 정체 = 본 단계의 핵심 결정.** INTEGRATED_PLAN §5.1.2 A7 의 "혼합"안(시즌+단원+인물)을 합성 단계에서 *물성*으로 구현.

| 층 | 묶음 | 합성에서의 구현 | 진입 동선 |
|---|---|---|---|
| **메인** | 시즌 (season-1-ancient) | 시즌 색 LUT + 시그니처 BGM 악기(리라) | 채널 분류 |
| **sub** | 단원 (unit-01) | 재생목록 "중1 수학 단원별" | 학습자 진입(교과서 순서) |
| **제목** | 인물 (에라토스테네스) | 표지 인물 얼굴 + 제목 핵심 단어 | 광범 시청자 진입(인물 검색) |

- **표지 시리즈 grammar** — `[시즌 색 띠] + [단원 번호 배지] + [인물 얼굴] + [인물 한 단어(gold serif)]`. 어느 영상이든 *한눈에 "이 채널·이 시즌"*. 단원 1 = era-ancient 황금색 + "01" + 에라토스테네스 + "정리".
- **인물별 voice 고정(미래)** — retro-4 의 미해결 항목. 인물 = 고정 voice 면, *목소리만 들어도 그 인물*. 시리즈 청각 정체성의 정점.
- **"양보하지 않은 것" 기록(진화 원칙 6)** — 단원마다 `8-meta.json` 에 `not_yielded` 한 줄. 모이면 "시리즈의 영혼". 단원 1 후보: *"발견의 필연성(왜 그가 그 발견을 했는가)을 결정적 순간 연출보다 우선했다."*
- **확장성** — 표지·메타·음향 grammar 를 템플릿화하면, 다음 단원(브라마굽타 등)은 *입력값만 갈아끼우면* 동일 정체성으로 즉시 합성. 이것이 PURPOSE.md 3단계 진화(수동 깊이 → 반복 적용 → 자동화)의 합성 단계 종착점이다.

---

## 부록 — STEP 8 한눈 요약

| 항목 | 값 |
|---|---|
| 입력 | `7-raw.mp4`(예정) + `4-narration.mp3`(**Kanna+Kyle, 140.27s**) (+옵션 BGM·SFX) |
| 출력 | `8-final.mp4` + `8-poster.jpg` + `8-meta.json` |
| 핵심 도구 | ffmpeg(mux `-c:v copy`) / ffprobe(sync 검증) |
| 핵심 기준 | sync **±0.3s** / 용량 **<25MB** / BGM **−20dB 이하** |
| 핵심 결정 | **A7 시리즈 정체**(시즌+단원+인물 혼합) |
| 한 단어 압축 | 에라토스테네스 = **"정리"** |
| 스킬 상태 | `se-video-compose` **미작성** (§3 설계 제안) |
| 종착 | vertical slice 종료 → `final-retrospective.md` → 단계 [이전] |

---

## 변경 이력

- 2026-05-29: 신규. STEP 8 [영상 6 합성] 심화 가이드 작성(9섹션). se-video-compose SKILL.md 설계 제안 포함. 음성 = Kanna+Kyle 140.27s 기준. 8-final.mp4 미생성(진행 예정) 상태 반영.
