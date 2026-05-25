<!-- exp-002-build-unit01/CHECKLIST.md -->

# exp-002 — unit 01 Vertical Slice Build Checklist

> **목적**: unit 01 (소인수분해 / 에라토스테네스) 영상 1편을 본 프로젝트 안에서 실제 빌드. 그 과정에서 단계 [서사]~[영상 6] 의 8개 스킬 시드 작성.
>
> **frame**: INTEGRATED_PLAN §5.7 단계 [재빌드] 의 첫 시범 = vertical slice.
>
> **시작**: 2026-05-25
> **단일 진입점**: [`../../00_charter/INTEGRATED_PLAN.md`](../../00_charter/INTEGRATED_PLAN.md)
> **선행 입력**: [`../exp-001-selection-unit01/output.md`](../exp-001-selection-unit01/output.md)

---

## 0. 진행 추적 (대시보드)

| Step | 단계 | 스킬 | 스킬 상태 | 결과물 상태 | NCC 검증 | Nick 검증 |
|---|---|---|---|---|---|---|
| 1 | [서사] | `se-people-narrate` | ✅ v0.1 | ✅ [1-narrative.md](./1-narrative.md) | ✅ | ✅ all ok (2026-05-25) |
| 2 | [스토리] | `se-video-story` | ✅ v0.1 | ✅ [2-story-seed.md](./2-story-seed.md) | ✅ | ✅ all ok (2026-05-25) |
| 3 | [영상 1] 스토리보드 | `se-video-storyboard` | ✅ v0.1 | ✅ [3-storyboard.md](./3-storyboard.md) | ✅ | ✅ all ok (2026-05-25) |
| 4 | [영상 2] 나레이션 | `se-video-narration` | 🟡 진입 대기 | ⚪ | — | — |
| 5 | [영상 3] 이미지 | `se-video-image` | ⚪ 미정의 | ⚪ | — | — |
| 6 | [영상 4] 모션 | `se-video-motion` | ⚪ 미정의 | ⚪ | — | — |
| 7 | [영상 5] 렌더 | `se-video-render` | ⚪ 미정의 | ⚪ | — | — |
| 8 | [영상 6] 합성 | `se-video-compose` | ⚪ 미정의 | ⚪ | — | — |

**범례**: ⚪ 미시작 / 🟡 진행 중 / ✅ 완료 / ⚠️ 이슈 / ❌ 차단

**정체성 잔여** (병행 진화):
- A3 길이 → 영상 1 (스토리보드) 단계에서 결정 (잠정 110초)
- A4 장면 구조 → 영상 1 단계 결정 (잠정 6장면)
- A5 톤 → 서사 + 나레이션 단계 결정
- A6 시청 후 행동 → 스토리 단계 결정
- A7 시리즈 정체 → 영상 6 (합성) 단계 결정 (메타데이터·표지 양식)

---

## 1. 공통 패턴 (모든 단계에 적용)

### 단계 진입 시 NCC 작업 순서

1. **스킬 시드 작성** — `70_tools/<skill-name>/SKILL.md` 신설 (agentskills.io spec 준수)
   - frontmatter: name (kebab-case) / description / compatibility / metadata / allowed-tools
   - body: 입력 / 출력 / 동작 / QnA 패턴 / 리서치 패턴 / 평가 기준
2. **시범 실행 입력 align** — 이전 단계 출력 + 정체성 (§8 결정) 확인
3. **부족 입력 Nick QnA** (있다면) — 본 대화에서
4. **시범 실행** — NCC 직접 또는 배치 모드 (백그라운드 에이전트)
5. **결과물 작성** — `40_experiments/exp-002-build-unit01/<step>-<artifact>` 경로
6. **NCC 자동 검증** — 체크리스트 (단계별 §)
7. **Nick 검증** — 본 대화에서 핵심 요약 + 동의 확인
8. **Retrospective** — `40_experiments/exp-002-build-unit01/retro-<step>.md` (스킬 자체 개선점)
9. **다음 단계 진입 조건** 확인 후 다음 단계

### 산출물 위치 규약

```
exp-002-build-unit01/
├── CHECKLIST.md            ← 본 문서
├── 1-narrative.md          ← step 1 [서사] 출력
├── 2-story-seed.md         ← step 2 [스토리] 출력
├── 3-storyboard.md         ← step 3 [영상 1] 출력
├── 4-narration.txt         ← step 4 [영상 2] 출력 (텍스트)
├── 4-narration.xml         ← step 4 SSML
├── 4-narration.mp3         ← step 4 음성 (gitignore)
├── 5-image_prompts.md      ← step 5 [영상 3] 출력 (프롬프트)
├── 5-images/               ← step 5 이미지 (gitignore)
├── 6-motion-config.json    ← step 6 [영상 4] 출력
├── 7-raw.mp4               ← step 7 [영상 5] 출력 (gitignore)
├── 8-final.mp4             ← step 8 [영상 6] 최종 (gitignore, Releases)
├── 8-poster.jpg            ← step 8 표지 (gitignore)
├── retro-1-narrative.md    ← step 1 retrospective
├── retro-2-story.md        ← step 2 retrospective
├── ...
└── final-retrospective.md  ← 전체 vertical slice 종합 회고
```

### NCC 자동 검증 공통 항목

- [ ] 스킬 SKILL.md agentskills.io spec 준수 (name kebab-case / description 1024자 / body < 500줄)
- [ ] 산출물 위치 규약 준수
- [ ] 자료원 인용 (URL 또는 출처 명시)
- [ ] 정체성 약속 3겹 부합도 자체 평가
- [ ] 다음 단계 입력 명세 정리

### Nick 검증 공통 항목

- 핵심 산출물 요약 1~3분 읽기
- 정체성 약속 3겹 (특히 약속 3 = 발견의 필연성 서사) 운반 동의
- 다음 단계 진입 동의

---

## STEP 1 — 단계 [서사]

### 1.1 만들 것

| 항목 | 내용 |
|---|---|
| **스킬** | `70_tools/se-people-narrate/SKILL.md` (시드) |
| **결과물** | `1-narrative.md` — 에라토스테네스 인물 서사 |
| **목적** | exp-001 의 4 자산 (도서관 사명 / 베타 별명 / 아르키메데스 서신 / 노년) 을 약속 3겹 운반하는 텍스트로 |

### 1.2 입력

- exp-001 output.md §4.1 (에라토스테네스 사실 자료원 표) + §5 (영상 구조 안)
- 정체성 결정 1·2 (시청자 + 약속 3겹)
- 외부 19인 풀: `30_content/people/eratosthenes.md` (참조만)

### 1.3 출력 위치

`40_experiments/exp-002-build-unit01/1-narrative.md`

### 1.4 NCC 자동 검증

- [ ] 약속 3겹 모두 텍스트 안에서 식별 가능
- [ ] 약속 3 (필연성 서사) = "도서관 사명" + "아르키메데스 서신" 2개 축 명시
- [ ] 광범 시청자 (이름 모르는 시청자) 가독성
- [ ] 학습자 (중1) 수준 어휘
- [ ] 자료원 인용 (URL / 출처)
- [ ] fabrication 없음 (자료 없는 "왜" 추정 X)

### 1.5 Nick 검증

- 서사 한 줄 요약 + 약속 3겹 운반 동의
- 톤 적합도 (A5 잠정 결정 — 이야기 톤 vs 다큐 톤 등)
- 한 단어 압축 (에라토스테네스 = "정리" / 다른 단어?)

### 1.6 다음 단계 진입 조건

- [ ] Nick 동의
- [ ] 스킬 retrospective 작성
- [ ] A5 톤 잠정 결정

---

## STEP 2 — 단계 [스토리]

### 2.1 만들 것

| 항목 | 내용 |
|---|---|
| **스킬** | `70_tools/se-video-story/SKILL.md` (시드) |
| **결과물** | `2-story-seed.md` — 110초 영상 스토리 시드 (스토리보드 직전) |
| **목적** | 서사 (텍스트) → 영상 길이·장면 단위로 압축 + 약속 3겹 장면별 배치 |

### 2.2 입력

- step 1 출력 (`1-narrative.md`)
- 정체성 결정 1·2 + A3 길이 잠정 (110초) + A4 장면 수 잠정 (6장면)
- 옛 1편 baseline: `../../10_reference/02_baseline_unit01.md`

### 2.3 출력 위치

`40_experiments/exp-002-build-unit01/2-story-seed.md`

### 2.4 NCC 자동 검증

- [ ] 6장면 모두 정의 (S1~S6)
- [ ] 각 장면이 약속 3겹 중 무엇을 담는지 명시
- [ ] 결정적 순간 (S4) 의 약속 3 (필연성 서사) 강화
- [ ] 총 길이 95~120초 범위 (잠정)
- [ ] 다음 단계 [영상 1] 입력 명세 (각 장면 시각 단서 + 나레이션 시드)

### 2.5 Nick 검증

- 6장면 배치 동의 (특히 S3 → S4 의 필연성 서사 강화 확인)
- A3 길이 / A4 장면 구조 확정
- A6 시청 후 행동 (영상 끝났을 때 시청자가 무엇 하길 바라는가)

### 2.6 다음 단계 진입 조건

- [ ] Nick 동의
- [ ] A3·A4·A6 확정 + INTEGRATED_PLAN §8 결정 누적
- [ ] retrospective

---

## STEP 3 — 단계 [영상 1] 스토리보드

### 3.1 만들 것

| 항목 | 내용 |
|---|---|
| **스킬** | `70_tools/se-video-storyboard/SKILL.md` (시드) |
| **결과물** | `3-storyboard.md` — 6장면 스토리보드 (장면 번호 / 시간 / 시각 / 텍스트 / 나레이션 시드) |
| **목적** | 스토리 시드 → 장면별 카드. 시각 단서 + 나레이션 시드 분리. 다음 단계 [영상 2~4] 의 직접 입력 |

### 3.2 입력

- step 2 출력 (`2-story-seed.md`)
- 정체성 결정 (전체)
- 옛 1편 storyboard: `../../../50_channel/season-1-ancient/unit-01/storyboard_v1_5.md` (참조만)

### 3.3 출력 위치

`40_experiments/exp-002-build-unit01/3-storyboard.md`

### 3.4 NCC 자동 검증

- [ ] 6장면 각각: 시간 / 시각 주체 / 텍스트 / 나레이션 글자수
- [ ] S4 가 가장 김 (25~30초 권장)
- [ ] 장면 간 전환 규칙 (fade / ken burns 등)
- [ ] 나레이션 총 글자수 480~620 (5자/초 × 약 110초)
- [ ] 시대 시각 자료 정확성 (의복·건축·도구 anachronism 체크)

### 3.5 Nick 검증

- 6장면 카드 요약 동의
- 시대 시각 자료 정확성 (학자 검증 필요 시점)
- 텍스트 강조구절 위치

### 3.6 다음 단계 진입 조건

- [ ] Nick 동의
- [ ] 나레이션 시드 (텍스트 + 위치) 추출 가능 상태
- [ ] 이미지 프롬프트 시드 (각 장면 시각 단서) 추출 가능 상태
- [ ] retrospective

---

## STEP 4 — 단계 [영상 2] 나레이션

### 4.1 만들 것

| 항목 | 내용 |
|---|---|
| **스킬** | `70_tools/se-video-narration/SKILL.md` (시드) |
| **결과물** | `4-narration.txt` (텍스트) + `4-narration.xml` (SSML) + `4-narration.mp3` (음성) |
| **목적** | 나레이션 텍스트 작성 → SSML 풀스펙 → 음성 합성 → 길이 사전 검증 (1편 발견 표준 4가지 중 2건 운반) |

### 4.2 입력

- step 3 출력 (`3-storyboard.md` 의 나레이션 시드)
- 정체성 톤 (A5)
- 옛 1편 SSML: `../../../50_channel/season-1-ancient/unit-01/narration_v1_5.xml` (참조)

### 4.3 출력 위치

- `40_experiments/exp-002-build-unit01/4-narration.txt`
- `40_experiments/exp-002-build-unit01/4-narration.xml` (SSML)
- `40_experiments/exp-002-build-unit01/4-narration.mp3` (gitignore — 음성 파일)

### 4.4 도구 결정 시점 (이 단계에서)

INTEGRATED_PLAN §3.2 "다양한 플랫폼 체득":
- **edge-tts** (옛 1편 사용, 무료, SSML 미지원)
- **ElevenLabs** (감정 표현 우수, 무료 quota ~10000자)
- 잠정: 양쪽 모두 시범 → 비교 표 (`70_tools/se-video-narration/comparison.md`)

### 4.5 NCC 자동 검증

- [ ] 텍스트 글자수 480~620 (5자/초 × 95~120초)
- [ ] SSML 풀스펙 (break / prosody) 사용
- [ ] 음성 합성 후 길이 측정 → 95~120초 범위 검증 (1편 발견: 길이 사전 검증)
- [ ] 인물별 음성 매핑 표 작성 (1편 발견: 인물별 음성 매핑)
- [ ] 강의 톤 X / 이야기 톤 ✓

### 4.6 Nick 검증

- 음성 청취 (mp3 들어보기)
- 톤 적합도 — 학습자 시청 시 적합한가
- 결정적 순간 (S4) 의 떨림·여운 표현

### 4.7 다음 단계 진입 조건

- [ ] Nick 동의 (음성 청취 후)
- [ ] 도구 결정 (edge-tts / ElevenLabs / 양쪽 보존) — 비교 표 작성
- [ ] AUDIO_DURATION 측정값 다음 단계 (렌더) 에 전달 가능
- [ ] retrospective

---

## STEP 5 — 단계 [영상 3] 이미지

### 5.1 만들 것

| 항목 | 내용 |
|---|---|
| **스킬** | `70_tools/se-video-image/SKILL.md` (시드) |
| **결과물** | `5-image_prompts.md` (프롬프트) + `5-images/s2-*.png` ... 4~6장 |
| **목적** | 장면별 이미지 프롬프트 작성 (캐릭터 일관성 기법 포함) → AI 이미지 생성 |

### 5.2 입력

- step 3 출력 (`3-storyboard.md` 의 시각 단서)
- 정체성 약속 1 (시대 감각) + 인물 일관성
- 옛 1편 프롬프트: `../../../50_channel/season-1-ancient/unit-01/image_prompts.md` (참조)

### 5.3 출력 위치

- `40_experiments/exp-002-build-unit01/5-image_prompts.md`
- `40_experiments/exp-002-build-unit01/5-images/s2-*.png` ... (gitignore — 이미지 파일)

### 5.4 도구 결정 시점 (이 단계에서)

- **DALL-E 3** (옛 1편, ChatGPT 통해)
- **Midjourney** (`--cref` 캐릭터 일관성)
- **Stable Diffusion** (로컬·ComfyUI)
- 잠정: top 2 시범 → 비교 표

### 5.5 NCC 자동 검증

- [ ] 장면별 이미지 4~6장 (S2 1장 / S3 1장 / S4 1~2장 / S5 1장 / S6 0~1장)
- [ ] 프롬프트 최상단 공통 인물 묘사 분리 (1편 발견: 캐릭터 일관성 기법)
- [ ] 16:9 종횡비
- [ ] 시대 anachronism 체크 (의복·도구·건축)
- [ ] 이미지 내 텍스트(글자) 없음
- [ ] 여백 30% 이상 (텍스트 들어갈 공간)
- [ ] 시대 팔레트 (era-ancient) 일관

### 5.6 Nick 검증

- 이미지 4~6장 시청 (썸네일 보기)
- 인물 일관성 (같은 얼굴) 확인
- 시대·풍경 적합도

### 5.7 다음 단계 진입 조건

- [ ] Nick 동의 (이미지 시청 후)
- [ ] 도구 결정 (DALL-E / Midjourney / SD) — 비교 표 작성
- [ ] 인물별 reference 이미지 1장 보관 (다음 단원 재사용)
- [ ] retrospective

---

## STEP 6 — 단계 [영상 4] 모션

### 6.1 만들 것

| 항목 | 내용 |
|---|---|
| **스킬** | `70_tools/se-video-motion/SKILL.md` (시드) |
| **결과물** | `6-motion-config.json` — 장면별 시간 + 모션 (ken burns / pan / fade) |
| **목적** | 정적 이미지 + 텍스트를 동적 영상으로 만들 모션 정의 |

### 6.2 입력

- step 3 (스토리보드의 모션 단서)
- step 4 (나레이션 음성 길이 → 장면 시간)
- step 5 (이미지 파일)

### 6.3 출력 위치

`40_experiments/exp-002-build-unit01/6-motion-config.json`

### 6.4 NCC 자동 검증

- [ ] 장면별 시작·끝 시간 (총합 = 음성 길이 + 2초 여유)
- [ ] 각 장면 모션 정의 (정적 / ken burns / pan / fade)
- [ ] 장면 전환 1초 fade
- [ ] S4 (결정적 순간) 의 모션 강조

### 6.5 Nick 검증

- config 핵심 요약 동의
- 결정적 순간의 모션 적합도

### 6.6 다음 단계 진입 조건

- [ ] Nick 동의
- [ ] retrospective

---

## STEP 7 — 단계 [영상 5] 렌더

### 7.1 만들 것

| 항목 | 내용 |
|---|---|
| **스킬** | `70_tools/se-video-render/SKILL.md` (시드) |
| **결과물** | `7-raw.mp4` — 영상만 (음성 없음) |
| **목적** | 스토리보드 + 이미지 + 모션 → raw 영상 렌더 |

### 7.2 입력

- step 3·5·6 출력
- 렌더 엔진: HyperFrames (옛 1편 사용) 또는 대안

### 7.3 출력 위치

`40_experiments/exp-002-build-unit01/7-raw.mp4` (gitignore)

### 7.4 NCC 자동 검증

- [ ] 길이 = AUDIO_DURATION + 2초 (장면 시간 합과 일치)
- [ ] 1280×720 해상도
- [ ] 프레임 손실 없음
- [ ] 모든 장면 렌더 완료

### 7.5 Nick 검증

- raw 영상 시청 (음성 없이 보기)
- 시각 흐름 적합도

### 7.6 다음 단계 진입 조건

- [ ] Nick 동의
- [ ] retrospective

---

## STEP 8 — 단계 [영상 6] 합성

### 8.1 만들 것

| 항목 | 내용 |
|---|---|
| **스킬** | `70_tools/se-video-compose/SKILL.md` (시드) |
| **결과물** | `8-final.mp4` (최종) + `8-poster.jpg` (표지) + 메타데이터 (제목·설명) |
| **목적** | raw 영상 + 음성 + (옵션) 음향 합성 → 최종. 채널 메타데이터 (A7 시리즈 정체) |

### 8.2 입력

- step 4 (`4-narration.mp3`)
- step 7 (`7-raw.mp4`)
- (옵션) 배경음·효과음 (능력 흡수 §7.3 검증)

### 8.3 출력 위치

- `40_experiments/exp-002-build-unit01/8-final.mp4` (gitignore, Releases)
- `40_experiments/exp-002-build-unit01/8-poster.jpg` (gitignore)
- `40_experiments/exp-002-build-unit01/8-meta.json` (제목 / 설명 / 태그 / 시리즈 정체)

### 8.4 NCC 자동 검증

- [ ] sync 오차 ±0.3초 이내
- [ ] 파일 크기 < 25MB
- [ ] 음향 밸런스 (BGM 있다면 -20dB 이하)
- [ ] 표지 (S1 화면 기반)
- [ ] 메타데이터 (제목·설명·태그) 작성

### 8.5 Nick 검증

- 최종 영상 시청 (전체 110초)
- 옛 1편 (`../../../50_channel/season-1-ancient/unit-01/final_v1_5.mp4`) 과의 비교
- 약속 3겹 모두 운반되었는가 (특히 약속 3 = 발견의 필연성 서사 — 옛 1편 약점이 보강되었는가)

### 8.6 다음 단계 (vertical slice 종료)

- [ ] Nick 동의 (최종 영상)
- [ ] 옛 1편과의 비교 검증 (가설 1 §10.2)
- [ ] A7 시리즈 정체 확정
- [ ] **최종 retrospective** — `final-retrospective.md` 작성
  - vertical slice 전체 회고
  - 8 스킬 v0.1 → v0.2 정련 항목 누적
  - INTEGRATED_PLAN §8 결정 누적 (예: 결정 10 도구 비교 결과, 결정 11 A3~A7 확정 등)
  - 단계 [재빌드] 완료 신호 도달

---

## 9. Vertical Slice 종료 후 작업

### 9.1 단계 [선정] 의 SKILL.md v0.2 정련 (병행 진화)

exp-001 retrospective.md 의 6 정련 항목 반영. 본 vertical slice 진행 중 발견된 추가 정련 항목도 누적.

### 9.2 다음 단원 검증 (단계 [재빌드] §10.2 가설 1)

- exp-003 = 단원 2 (정수와유리수 / 브라마굽타) vertical slice — 8 스킬 일반화 검증
- 단원당 사람 시간 측정 (단계 1 = 60h → 단계 2 = 15h 목표)

### 9.3 단계 [이전] 준비

- 8 스킬 SSOT → 외부 `10_system/30_skills/` 덮어쓰기 또는 새 위치
- 표준 문서 (정체성·약속·6장면 구조) → 외부 `10_system/10_principles/STORY_VIDEO_*.md` 덮어쓰기
- 영상 1편 → 외부 `50_channel/people/eratosthenes/sieve/` 또는 `seasons/1-ancient/unit-01/`

---

## 10. 본 체크리스트의 운영 규칙

- 각 step 진입 시 §0 대시보드 상태 갱신 (⚪ → 🟡 → ✅)
- 각 step 결정·이슈는 본 폴더 안 `notes.md` (필요 시 신설) 에 누적
- 각 step retrospective 가 그 step 스킬의 v0.2 시드
- vertical slice 종료 시 `final-retrospective.md` 가 본 프로젝트의 *큰 회고*
- A3~A7 결정은 INTEGRATED_PLAN §8 에 정식 결정으로 누적 (결정 10, 11, ...)
- 모든 외부 자료는 **참조만**, 변경 X (외부 의존 0 원칙)

---

## 11. 변경 이력

- 2026-05-25: 신규. exp-002 시작.
