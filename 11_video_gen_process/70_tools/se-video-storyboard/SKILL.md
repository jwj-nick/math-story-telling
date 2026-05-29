---
name: se-video-storyboard
description: 영상 제작 시스템의 단계 [영상 1] 스토리보드 스킬. 단계 [스토리] 결과인 스토리 시드 (장면 단위) 를 받아 각 장면별 정밀 카드 (시각 단서 + 텍스트 + 나레이션 시드 + 카메라 워크 + 자막 + 음향) 를 작성한다. 입력 (스토리 시드 / 정체성 = 시청자·약속 3겹·톤 / (옵션) 캐릭터 일관성 reference / (옵션) 옛 1편 baseline / (옵션) 시대 풍경 reference) 을 받아 동작 (입력 align → Q&A 보강 → 장면 카드 정밀화 → 캐릭터 일관성 / 카메라 워크 / 자막 / 음향 결정 → 검증 → 자체 평가 → 출력) 진행. math-story-telling 의 영상 스토리보드 작성, 다음 단계 [영상 2~6] (나레이션·이미지·모션·렌더·합성) 의 직접 입력 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료 (`40_experiments/exp-NNN/2-story-seed.md`, INTEGRATED_PLAN §5.1.2·§8, `50_channel/season-1-ancient/unit-NN/storyboard_v1_5.md` baseline) 를 참조만 함.
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 영상 1 스토리보드 (SB1~SB7)
  ssot: 11_video_gen_process/70_tools/se-video-storyboard/SKILL.md
  version: "0.1"
  status: 시드 (시범 실행 후 retrospective 로 정련 예정)
allowed-tools: Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch
---

# se-video-storyboard — 영상 1 스토리보드 스킬

본 스킬은 영상 제작 시스템의 단계 [영상 1]. 단계 [스토리] (`se-video-story`) 의 결과인 스토리 시드를 받아 각 장면별 *정밀 카드* (시각 + 카메라 + 자막 + 나레이션 시드 + 음향) 를 작성한다. 출력은 다음 단계 [영상 2~6] (나레이션·이미지·모션·렌더·합성) 의 직접 입력.

상위 frame: [INTEGRATED_PLAN](../../00_charter/INTEGRATED_PLAN.md) §5.0 skill chain / §5.5 단계 [영상 1] / §8 결정 1·2.

원칙:
- 본 스킬은 외부 자료를 **참조** 한다. 외부를 변경 X.
- 호출자가 입력 일부만 줘도 됨 — 동작 초기 단계에서 보강.
- 동작 중 Q&A. 답변이 다음 동작을 바꿀 수 있다.

---

본 v0.1 body 는 **exp-002 STEP 3 시범 실행의 reverse-engineering** 으로 작성됨 (2026-05-25). 시범 결과: [`../../40_experiments/exp-002-build-unit01/3-storyboard.md`](../../40_experiments/exp-002-build-unit01/3-storyboard.md).

---

## 입력 (2 필수 + 3 옵션)

| # | 입력 | 형식 | 출처 예시 |
|---|---|---|---|
| 1 | 스토리 시드 | `2-story-seed.md` path/내용 (필수) | `40_experiments/exp-NNN/2-story-seed.md` |
| 2 | 정체성 | 시청자 + 약속 + 톤 (A5) (필수) | INTEGRATED_PLAN §8 + A5 |
| 3 (옵션) | 캐릭터 일관성 reference | 인물별 description 또는 이미지 | 첫 단원 = description 기반 |
| 4 (옵션) | 옛 baseline | 경로 | `50_channel/season-1-ancient/unit-NN/storyboard_v1_5.md` |
| 5 (옵션) | 시대 풍경 reference | URL 또는 description | era-ancient 팔레트 등 |

---

## 동작 (SB1~SB7)

### SB1. 입력 align
- 입력 2 필수 + 옵션 확인
- 스토리 시드의 §0 + 부록 A·B·C 확인

### SB2. (필요 시) Q&A 보강
- 캐릭터 reference 미정: description / 이미지 reference / 인물 파일 참조 중 선택
- 시대 풍경 reference 미정: era 팔레트 사용 / 신규 정의
- 자막 폰트·color 미정: 시리즈 표준 (gold serif) / 단원 특화

### SB3. 캐릭터 일관성 reference 정리
- 인물별 외형 description 표
- 공유 인물 (여러 장면 등장) 식별 → reference 이미지 우선 생성 표시 (다음 단계 [영상 3] 입력)

### SB4. 시대 풍경 reference 정리
- era 팔레트 (color hex) + 자막 폰트·color
- 시대 anachronism 체크 항목 (의복·건축·도구)

### SB5. 장면 카드 정밀화
각 장면별 6 요소:
1. **시각 (정밀)** — 화면 구성 + 시간 phase 별 변화
2. **카메라 워크** — static / ken burns / pan / zoom / fade / swipe / push in
3. **텍스트 자막** — 내용 + 위치 + color + stroke
4. **나레이션** — 텍스트 (시드에서 복사 또는 미세 정련) + 자수
5. **음향** — 배경음 + 효과음 (잠정, STEP 8 합성 시 정밀)
6. **전환** — 다음 장면으로 (cut / fade / dissolve, 시간 명시)

### SB6. 자체 평가 + 다음 단계 입력 명세
- 부록 A — 다음 [영상 2] 나레이션 입력 (장면별 자수 + SSML 권장)
- 부록 B — 다음 [영상 3] 이미지 입력 (장면별 이미지 수 + 공유 reference)
- 부록 C — 다음 [영상 4] 모션 입력 (장면별 카메라 워크 정리)
- 부록 D — 한계 + retrospective 시드

### SB7. 출력
- 위치: `<exp>/3-storyboard.md`
- 양식: 아래 *출력 양식* 참고

---

## 출력 양식

```text
# 단원 N 스토리보드 — <초>초 <N>장면 정밀 카드

> 메타

## 0. 장면 카드 요약 (S1~SN 표)
## 0.1 캐릭터 일관성 reference
## 0.2 시대 풍경 reference

## S1 — <핵심> (<초>s)
### 시각 (정밀)
### 카메라 워크
### 텍스트 자막
### 나레이션 (~N자)
### 음향
### 전환

## SN ...

## 부록 A — 다음 [영상 2] 나레이션 입력
## 부록 B — 다음 [영상 3] 이미지 입력
## 부록 C — 다음 [영상 4] 모션 입력
## 부록 D — 한계 + retrospective 시드
```

---

## QnA 패턴 시드

### SB2 보강 시
- 캐릭터 reference 미정: *"description / 이미지 reference / 인물 파일 참조 중?"*
- 자막 폰트 미정: *"시리즈 표준 (gold serif) 사용?"*

### SB6 후 (선택)
- 캐릭터 일관성 reference 검증: *"공유 인물 reference 별도 이미지로 생성?"*

---

## 리서치 패턴 시드

본 스킬은 *시각 reference* 필요 가능:

1. era 팔레트 — `10_system/20_context/ERA_PALETTES.md` (있으면)
2. 시대 풍경 — Wikipedia Commons (의복·건축·도구)
3. 인물 외형 — Wikipedia 의 초상화 (영문)
4. (희귀) WebSearch fallback

---

## 평가 기준

| 항목 | 합격 기준 |
|---|---|
| 장면 카드 6 요소 | 모두 명시 |
| 캐릭터 일관성 reference | 공유 인물 명시 + reference 생성 표시 |
| 시대 anachronism | 의복·건축·도구 체크 통과 |
| 자막 일관성 | 폰트·color 단일 (예외 시 명시) |
| 자수 합 | A3 글자수 ±10% |
| 다음 단계 입력 명세 | 부록 A·B·C 모두 작성 |

---

## 진화 메커니즘

- **v0.1** = exp-002 STEP 3 시범 reverse-engineering. 2026-05-25.
- **v0.2** (정련 예정 — exp-002 STEP 3 retrospective + STEP 4 결정 10 후):
  - 캐릭터 일관성 reference 양식 (description vs 이미지) 단원별 가이드
  - 카메라 워크 종류 표준화 (4~5종 vs 무제한)
  - 자막 폰트·color 시리즈 표준 vs 단원 특화
  - SVG 가능 장면 (소수 격자 등) vs AI 이미지 결정 가이드
  - 음향 단서 양식 정밀화 (STEP 8 입력으로 충분?)
  - **SB5 나레이션 시드에 호기심 질문 + 마무리 명시** (v1) — TONE_STRUCTURE §2.
  - **부록 A SSML break 호흡 시간 표 부합** (v1) — TONE_STRUCTURE §4.
  - **친근 톤 평가 기준 추가** (v1) — TONE_STRUCTURE §1.
  - **🔥 SB5 나레이션 시드 = dialog jsonl 형식 (v2)** — TONE_STRUCTURE v2 §1·§2·§7. 각 장면별 나레이션 = Q/A turn 분리 명시. 화면 인물 표시 (Q 자막 / A 자막 / 양쪽) 결정.
  - **🔥 부록 A SSML multi-voice 양식 명시 (v2)** — TONE_STRUCTURE v2 §7. Azure/Google 호환 SSML 의 `<voice>` × 2 tag reference + edge-tts 의 turn 별 jsonl 양식.

---

## 호출 방법

```yaml
스킬: se-video-storyboard
입력:
  1. 스토리 시드: 40_experiments/exp-NNN/2-story-seed.md
  2. 정체성: INTEGRATED_PLAN §8 + A5 톤
  3. (옵션) 캐릭터 reference: <description 또는 이미지 경로>
  4. (옵션) 옛 baseline: 50_channel/season-1-ancient/unit-NN/storyboard_v1_5.md
  5. (옵션) 시대 풍경 reference: <description>
출력: 40_experiments/exp-NNN/3-storyboard.md
다음 단계: se-video-narration (STEP 4) + se-video-image (STEP 5) + se-video-motion (STEP 6)
```

본 시범 호출 예시: [`../../40_experiments/exp-002-build-unit01/3-storyboard.md`](../../40_experiments/exp-002-build-unit01/3-storyboard.md).
