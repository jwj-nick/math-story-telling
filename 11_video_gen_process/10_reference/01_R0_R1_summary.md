<!-- 01_R0_R1_summary.md -->

# 발췌 — `260523_video_v1_5_standardize.md` R0+R1 핵심

- **원본**: `../../00_project_hub/10_chatlog/260523_video_v1_5_standardize.md`
- **발췌 일자**: 2026-05-23 (sub-project 셋업 시점)
- **발췌 범위**: R0 전체 + R1 전체 (chatlog 전체)

---

## 1. R0 (NCC 1차 진단) 핵심

### 1.1 unit-01 v1.5 baseline 정밀 분석

| 파일 | 핵심 |
|---|---|
| `narration_v1_5.txt` | 549자 / 5자/초 / 단문+빈줄 호흡 패턴 |
| `narration_v1_5.xml` | **SSML 풀스펙** (break ~40회 + prosody pitch/rate 강조 2회) — edge-tts에선 미동작이지만 **ElevenLabs/Azure 전환의 직접 input** |
| `storyboard_v1_5.md` | 6장면, 각 장면 시간·시각·이미지·모션·텍스트·나레이션 글자수 |
| `image_prompts.md` | 영문 5장 + Negative + Style notes 3블록 표준 + **공통 캐릭터 시트** 패턴 |
| `config_v1_5.json` | HyperFrames 렌더 데이터 (motion: scale_from/to, pan_x, scene_times) |
| `final_v1_5.mp4` | 21MB / 107.4s |

### 1.2 13단원 표준화 격차 5축

| # | 격차 | NCC 권장 |
|---|---|---|
| **D1** | TTS 도구 | ElevenLabs 전환 — SSML 풀스펙 활용 |
| **D2** | AI 이미지 도구 | Midjourney + `--cref` — 19인 캐릭터 일관성 |
| **D3** | 이중 트리 이동 시점 | 지금 (`people/<ref>/<ep>/` + `seasons/`) |
| **D4** | 시드 자동 생성 vs 단원별 | 12단원 시드 일괄 + unit-02 파일럿 |
| **D5** | `se_ncc_audit_video` 신설 | R2 점검 후 결정 |

### 1.3 R0 로드맵 (β scope 채택 후 무효, R1에서 재정렬)

R0의 R1~R18 로드맵은 "13편 일괄" 가정. 시즌1 5편 가정 시 축소됨.

---

## 2. R1 (zoom out 재진단) 핵심

### 2.1 마스터 플랜 위치

```
[~05-20] 13단원 앱 완성 + 영상 v1.5 unit-01 완성
[05-21~22] repo 통합 + 마이그 + 수학 챕터 표준 정의
[05-23 ← 현재] C R0+R1 = Phase 0-A 중간, 영상 1/5
```

채널 비전 (260516) 기준: 시즌1 = Ancient 5단원 (unit-01·02·03·04·05). 영상 1/5 완성.

### 2.2 R0 가정의 갭 7개

| # | 갭 | 출처 |
|---|---|---|
| **G1** | scope: 13편 vs **시즌1 5편 (옛 비전)** | 260516 채널 비전 D1 |
| G2 | "4편 분할 구조" — 1단원 1편 vs 분할 | 260516 D3 |
| G3 | ElevenLabs **5인 voice 매핑** | 260516 D4 |
| G4 | 인물 캐릭터 시트 분리 미반영 | 260520 insight 후보 4번 |
| G5 | narration length dry run 미반영 | 260520 insight 후보 2번 |
| G6 | "앱=백본 / 영상=보조" 우선순위 | 260516 meta planning |
| G7 | 창의 제안 8개 미검토 | 260516 §5 |

### 2.3 scope 권장 — β (시즌1 5편 우선)

| 옵션 | 작업량 | 기간 | NCC 평가 |
|---|---|---|---|
| α 13편 | 65장 이미지 + 13 TTS·렌더 | 8~12주 | 비전 불일치 |
| **β 5편** | **25장 + 5 TTS·렌더** | **3~5주** | ✅ 권장 |
| γ 시즌1 + 시즌2(3편) | 40장 + 8 | 6~9주 | 후속 결정 |

### 2.4 시즌1 5편 명세

| Ep | 단원 | 인물 | episode-key | era-palette |
|---|---|---|---|---|
| Ep1 | 01 소인수분해 | 에라토스테네스 | sieve-of-eratosthenes | era-ancient |
| Ep2 | 02 정수와 유리수 | 브라마굽타 | zero-and-negatives | era-medieval (India) |
| Ep3 | 03 문자와 식 | 알콰리즈미 | birth-of-algebra | era-medieval (Islamic) |
| Ep4 | 04 일차방정식 | 디오판토스 | arithmetica-puzzles | era-ancient (Late antiquity) |
| Ep5 | 05 좌표와 그래프 | 데카르트 | coordinate-revolution | era-modern (Early) |

→ 총 110s × 5 = 약 9분. narration 약 3000자. ElevenLabs 무료 quota (10000자) 충분.

### 2.5 진화 메커니즘 본격화 — 즉시 가능 sub-tasks

`10_system/50_insights/_index.md` 의 미반영 1건 (5 후보 중 2개) 처리:

1. **STORY_VIDEO_v1_5.md 4개 항목 갱신**
   - §2.2 캐릭터 시트 분리 (`image_prompts.md` 최상단 공통 묘사)
   - §4 [6.5] 길이 dry run 분기 (TTS 1회 합성 → 95~120s 검증)
   - §3.1 인물별 voice 매핑 표 (ElevenLabs 시즌1 5인)
   - §7 디렉토리 구조 (이중 트리 반영)
2. **`se_story_video_v1_5` skill Phase E 추가** — 빌드 직후 자동 retrospective
3. **insight `[x]` 표시** — `_index.md` 미반영 entry 처리

### 2.6 R0+R1 신규 결정 항목

| 결정 | 옵션 | NCC 권장 |
|---|---|---|
| **D6 scope** | α / **β** / γ | β |
| D7 단원→영상 분할 | 1단원 1편 / 분할 | 1단원 1편 (시즌1) |
| D8 창의 제안 채택 | 8개 중 일부 | 지금 0개, 시즌1 후 검토 |
| D9 옛 70_meta 처리 | A/B/C | B (`90_archive/` 이동 + 신규 작성) |
| D10 진화 메커니즘 본격화 | 지금 / 시즌1 후 | 지금 |

### 2.7 Nick 응답 없이 NCC 자율 진행 가능 4건 (R1.9)

1. **insights 미반영 2건 STORY_VIDEO_v1_5.md 반영** + `[x]` 표시
2. **`se_story_video_v1_5` skill 점검** (현 SKILL.md 격차 audit)
3. **STORY_VIDEO_v1_5.md 4개 항목 갱신**
4. **옛 `10_system/70_meta/` 정합성 audit 보고서** (이동은 D9 후)

→ D6~D10 어떤 답이 와도 가치 있음. compact 후 NCC 자율 진행 후보.

---

## 3. NCC 추가 분석 (sub-project 분리 후 시점)

### 3.1 본 sub-project 의 첫 책무

R1 §1.9의 자율 진행 4건 = **본 sub-project의 첫 sprint 후보**.

- 4건 중 1·3·4 = `20_principles/` + `60_evaluation/` 영역
- 4건 중 2 = `70_tools/` 영역 (skill 점검) 또는 `20_principles/` (skill = principle 의 코드화)

→ sprint 0 (compact 후 첫 라운드): 자율 진행 4건 + VISION/GOALS 작성.

### 3.2 sub-project 분리의 의미

R0+R1 까지는 "math-story-telling 큰 그림" 안에서의 C 작업. R1.4 (scope β) 결정으로 **영상 작업 = 별도 sub-project** 로 분리 가능.

이유:
- 영상 1편 작업이 단순 산출물 아니라 **단계·실험·평가·진화의 R&D 과정**
- 진화 메커니즘 (Build→Retrospect→Distill→Apply) 작동에 전용 공간 필요
- math-story-telling 큰 그림의 다른 트랙 (앱·축 C·이북) 과 책임 분리 명확

→ `11_video_gen_process/` 셋업 (본 세션 임무).

### 3.3 sub-project 외부에 남는 것

| 외부 잔존 | 위치 | 이유 |
|---|---|---|
| 영상 SSOT 표준 | `../10_system/10_principles/STORY_VIDEO_v1_5.md` | math-story-telling 단일 SSOT 정신 — sub-project 의 갱신은 promote 형태 |
| 영상 skill SSOT | `../10_system/30_skills/se_story_video_v1_5/` | 동일 |
| 영상 회고 (정제분) | `../10_system/50_insights/` | sub-project 60_evaluation/ → 정제 후 promote |
| 영상 산출물 (검증된) | `../50_channel/` | sub-project 40_experiments/ → 검증 후 promote |

본 sub-project = **워크플로우 + 실험 + 평가의 R&D 공간**. SSOT 와 산출물은 외부.

---

## 변경 이력

- 2026-05-23: 발췌. R0+R1 전체. NCC 추가 분석 3섹션.
