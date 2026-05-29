---
name: se-video-story
description: 영상 제작 시스템의 단계 [스토리] 스킬. 단계 [서사] 결과인 인물 서사 (원료 분량, ~1500~2000자) 을 받아 영상 1편 분량의 스토리 시드 (장면 단위) 로 압축한다. 입력 (서사 원료 / 정체성 = 시청자·약속 3겹·톤 / A3 영상 길이 / A4 장면 수 / 한 단어 압축 / (옵션) 옛 1편 baseline 참조) 을 받아 동작 (입력 align → Q&A 보강 → 서사 §→장면 매핑 → 장면 카드 초안 → 약속 3겹 장면 배치 검증 → 자체 평가 → 출력) 진행. math-story-telling 의 인물 서사 → 영상 스토리 시드 변환, 6장면 약속 운반 배치, A3·A4·A6 (시청 후 행동) 결정 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료 (`40_experiments/exp-NNN/1-narrative.md`, INTEGRATED_PLAN §5.1.2·§8, `50_channel/season-1-ancient/unit-NN/` baseline 참조) 를 참조만 함.
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 스토리 (S1~S7)
  ssot: 11_video_gen_process/70_tools/se-video-story/SKILL.md
  version: "0.1"
  status: 시드 (시범 실행 후 retrospective 로 정련 예정)
allowed-tools: Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch
---

# se-video-story — 영상 스토리 스킬

본 스킬은 영상 제작 시스템의 단계 [스토리]. 단계 [서사] (`se-people-narrate`) 의 결과인 인물 서사 (원료 분량) 을 받아 영상 1편 분량의 스토리 시드 (장면 단위) 로 압축한다. 출력은 다음 단계 [영상 1] (`se-video-storyboard`) 의 직접 입력.

상위 frame: [INTEGRATED_PLAN](../../00_charter/INTEGRATED_PLAN.md) §5.0 skill chain / §5.4 단계 [스토리] / §8 결정 1·2 / §5.1.2 A3·A4·A6.

원칙:
- 본 스킬은 외부 자료를 **참조** 한다. 외부를 변경 X.
- 호출자가 입력 일부만 줘도 됨 — 동작 초기 단계에서 보강.
- 동작 중 Q&A. 답변이 다음 동작을 바꿀 수 있다.

---

본 v0.1 body 는 **exp-002 STEP 2 시범 실행의 reverse-engineering** 으로 작성됨 (2026-05-25). 시범 결과: [`../../40_experiments/exp-002-build-unit01/2-story-seed.md`](../../40_experiments/exp-002-build-unit01/2-story-seed.md).

---

## 입력 (5 필수 + 1 옵션)

| # | 입력 | 형식 | 출처 예시 |
|---|---|---|---|
| 1 | 서사 원료 | `1-narrative.md` path/내용 | `40_experiments/exp-NNN/1-narrative.md` |
| 2 | 정체성 | 시청자 + 약속 3겹 + 톤 (A5) | INTEGRATED_PLAN §8 + A5 잠정 |
| 3 | A3 영상 길이 | 초 + 글자수 | INTEGRATED_PLAN §5.1.2 A3 (잠정 110초/550자) |
| 4 | A4 장면 수 | 정수 | INTEGRATED_PLAN §5.1.2 A4 (잠정 6) |
| 5 | 한 단어 압축 | 인물 한 단어 | 서사 마지막 § (예: "정리") |
| 6 (옵션) | 옛 baseline | 경로 | `50_channel/season-1-ancient/unit-NN/storyboard_v1_5.md` |

---

## 동작 (S1~S7)

### S1. 입력 align
- 입력 5+1 확인. 누락·모호 항목 식별.
- 서사 원료 *부록 B* (다음 단계 [스토리] 입력 명세) 확인 — § → S 매핑 안.

### S2. (필요 시) Q&A 보강
- A5 톤 미정 시: 톤 결정 (이야기 / 다큐 / 혼합)
- baseline 참조 여부: 외부 의존 0 vs 참조 효과 비교
- 한 단어 압축 confirm

### S3. 서사 § → 장면 매핑
- A4 장면 수 == 서사 § 수: 1:1 매핑 (부록 B 참조).
- 불일치 시 통합·분할:
  - § > A4: 짧은 §끼리 통합 (예: §6+§7 → S6)
  - § < A4: 핵심 § 확장 (★ 약속 3 자산 우선)

### S4. 장면 카드 초안
각 장면별 5~6 요소:
1. 시간 (s) — A3 / A4 ± 가중치 (S3·S4 핵심 = 길게)
2. 시각 단서 — 화면 구성·캐릭터·시대 팔레트
3. 나레이션 시드 — 텍스트 + 자수 (5자/s × 장면 시간 ±10%)
4. 운반 약속 — 약속 1·2·3 매핑 + 강도 ★
5. 전환 — cut / fade / dissolve
6. (선택) 자막 강조

### S5. 약속 3겹 장면 배치 검증
- 부록 A 표 (행=약속, 열=운반 장면 + 강도 합).
- 합격 기준:
  - 약속 1·3 ★4 이상
  - 약속 3 최소 2 장면 운반 권장
  - 약속 2 ★3 이상

### S6. 글자수·시간 검증
- 부록 B 표 (장면별 자수 / 시간 / 속도).
- 합격 기준: 총합 = A3 글자수 ±10% / 각 장면 4.5~5.5 자/s

### S7. 자체 평가 + 출력
- 부록 A — 약속 3겹 장면 배치 검증
- 부록 B — 나레이션 글자수 합계
- 부록 C — 다음 단계 [영상 1] 스토리보드 입력 명세 (✅ 결정 / ⚠️ 정밀화)
- 부록 D — 본 시범의 한계 + retrospective 시드
- 출력 = `<exp>/2-story-seed.md`

---

## 출력 양식

```text
# 단원 N 영상 스토리 시드 — <초>초 <N>장면

> 메타 (스킬 / 입력 / 출력 / 일자)

## 0. 장면 구조 요약 (S1~SN 표)

## S1 — <핵심> (<초>s)
### 시각 단서
### 나레이션 시드 (~N자)
### 운반 약속
### 전환

## SN — <핵심> ...

## 부록 A — 약속 3겹 장면 배치 검증
## 부록 B — 나레이션 글자수 합계
## 부록 C — 다음 단계 [영상 1] 입력 명세
## 부록 D — 한계 + retrospective 시드
```

---

## QnA 패턴 시드

### S2 보강 시
- 정체성 톤 (A5) 미정: *"톤 (이야기 / 다큐 / 혼합) 중 선택?"*
- baseline 참조 여부: *"외부 의존 0 유지 / baseline 참조 / 양쪽 비교?"*
- 한 단어 압축 confirm: *"서사 마지막 § 단어 그대로 / 변경 / NCC 제안?"*

### S5 검증 후 (약속 운반 미달 시)
- *"약속 X (★ 미달) 보강 — 어느 장면에 추가?"*

---

## 리서치 패턴 시드

본 스킬은 *서사 원료* 가 충분히 풍부 (부록 B 매핑 안 포함) 하면 외부 리서치 *대부분 불필요*. 다음 경우만:

1. 옛 baseline 참조 (시각 단서 비교)
2. 시대 풍경 시각 reference (Wikipedia Commons, 의복·건축 자료)
3. (희귀) 인물 외형 자료 부족 — WebSearch

---

## 평가 기준

| 항목 | 합격 기준 |
|---|---|
| 약속 운반 | 약속 1·3 ★4 이상 / 약속 2 ★3 이상 / 약속 3 최소 2 장면 |
| 총 시간 | A3 ±5s |
| 글자수 | A3 글자수 ±10% (5자/s) |
| 장면 카드 요소 | 5~6 요소 모두 명시 |
| 한 단어 압축 | 마지막 장면에 자막 + 나레이션 모두 명시 |
| fabrication | 서사 원료 분류 유지 — 압축 시 새 fabrication 도입 X |
| 부록 C ✅/⚠️ | 결정·정밀화 분리 명시 |

---

## 진화 메커니즘

- **v0.1** = exp-002 STEP 2 시범 (단원 1 / 에라토스테네스) reverse-engineering. 2026-05-25.
- **v0.2** (정련 예정 — exp-002 STEP 2 retrospective + STEP 4 결정 10 후):
  - 출력 양식 장면 카드 sub-section 수 결정 (4/5/6)
  - 약속 2 최소 운반 장면 수 — 1 vs 2
  - 옛 baseline 참조 옵션 효과 측정 (다음 단원 시범)
  - S3 통합·분할 규칙 정밀화
  - **S4 장면 카드 초안 시 호기심 chain 명시** (v1) — TONE_STRUCTURE §2.
  - **S6 마무리 멘트 명시** (v1) — TONE_STRUCTURE §2.
  - **A3 영상 길이 신 범위 적용** (v1) — 잠정 110s → 시즌 1 = 150~180s.
  - **친근 톤 + 풍부 배경 평가 기준 추가** (v1) — TONE_STRUCTURE §1·§3.
  - **🔥 S4 장면 카드 = Q/A turn 분리 (v2)** — TONE_STRUCTURE v2 §1·§2. 각 장면 카드의 "나레이션 시드" 를 dialog jsonl 형식 (Q/A turn 별) 로 재작성. S6 마무리 = Q 시도 + A 확인 패턴.
  - **🔥 A3 길이 신 범위 v2 = 150~210s** — dialog 자연 호흡으로 약간 더 김. TONE_STRUCTURE v2 §9.
- **v0.3+** = 다음 단원 (브라마굽타 등) 시범 후 일반화 검증.

---

## 호출 방법

```yaml
스킬: se-video-story
입력:
  1. 서사 원료: 40_experiments/exp-NNN/1-narrative.md
  2. 정체성: INTEGRATED_PLAN §8 결정 1·2 + A5 톤
  3. A3 영상 길이: 110초 (잠정) / ~550자 (5자/s)
  4. A4 장면 수: 6 (잠정)
  5. 한 단어 압축: <서사 마지막 §의 단어>
  6. (옵션) baseline: 50_channel/season-1-ancient/unit-NN/storyboard_v1_5.md
출력: 40_experiments/exp-NNN/2-story-seed.md
다음 단계: se-video-storyboard (STEP 3)
```

본 시범 호출 예시: [`../../40_experiments/exp-002-build-unit01/2-story-seed.md`](../../40_experiments/exp-002-build-unit01/2-story-seed.md).
