<!-- 03_current_plan_C.md -->

> ⚠️ **이 발췌는 옛 표기 (R0/R1, D-NNN, β/δ, sub-project, Phase 0-A 등) 를 그대로 포함한다.**
> 자연어로 풀이된 본 프로젝트의 현재 계획은 [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md) 에 있다.
> 본 발췌는 발췌 당시 (2026-05-23) current-plan 상태 기록. 현재 current-plan 은 INTEGRATED_PLAN 으로 통합되어 변경됨.

# 발췌 — `current-plan.md` §0 + §2.C

- **원본**: `../../00_project_hub/20_plan/current-plan.md`
- **발췌 일자**: 2026-05-23 (R0+R1 직후 갱신본)
- **목적**: math-story-telling 큰 그림에서 본 sub-project 가 어디에 있는지

---

## 1. §0 한 줄

> **C 영상 v1.5 표준화 진행 중 — R0 진단(13편 가정) → R1 zoom out 재진단(시즌1=5편 권장).**
> Nick D6(scope) 결정 대기 + NCC 자율 진행 가능 4건.

### 🚪 새 세션 entry point (현 sub-project 추가 후 갱신 필요)

1. `CLAUDE.md`
2. `current-plan.md` (← 여기)
3. `260523_video_v1_5_standardize.md` (R0+R1 전문)
4. **→ NEW: 본 sub-project `11_video_gen_process/README.md` + `00_charter/VISION.md`**

---

## 2. §2.C 진행 중 작업

### 2.C.1 R0 핵심 발견
- unit-01 v1.5 baseline 정밀 분석 — narration_v1_5.xml = ElevenLabs/Azure SSML 풀스펙 input (이미 작성됨)
- image_prompts.md 의 공통 캐릭터 시트 패턴 — 19인 모두 시트 필요
- meta.json schema v2 → 12단원 시드 자동 생성 가능

### 2.C.2 R1 zoom out 핵심 발견
- R0의 "13편 일괄" 가정이 옛 채널 비전 (`260516_channel_vision_review.md`) 의 "시즌1 = Ancient 5단원" 결정과 어긋남
- 갭 7개 (scope / 4편 분할 / 5인 voice 매핑 / 캐릭터 시트 미반영 / length dry run 미반영 / 앱=백본 우선순위 / 창의 제안 8개)
- 현 위치 = Phase 0-A 진행 중, 영상 1/5 완성
- 옛 `10_system/70_meta/` outdated → 별도 처리(D9) 필요

### 2.C.3 Nick 결정 대기
- 🔴 D6 scope: α 13편 / **β 시즌1 5편 (NCC 권장)** / γ
- 🟡 D7~D10 보조 (NCC 권장 채택 시 자율 진행)
- 🟢 R0 D1~D5 결정 유지

### 2.C.4 NCC 자율 진행 가능 4건
1. `10_system/50_insights/_index.md` 미반영 2건 → STORY_VIDEO_v1_5.md 반영 + `[x]`
2. `se_story_video_v1_5` skill 점검
3. STORY_VIDEO_v1_5.md 4개 항목 갱신
4. 옛 `10_system/70_meta/` 정합성 audit 보고서

### 2.C.5 다음 액션 분기
- 분기 A: Nick D6 답 → R2 시작
- 분기 B: D6 미응답 → 자율 4건 진행 → 다시 요청
- 분기 C: Nick "다 권장대로" → β + 자율 4건 + R3 (캐릭터 시트)

---

## 3. §4 잔여 인프라 작업 (영상 관련)

### 4.5 옛 `10_system/70_meta/` 마스터 플랜 처리 (R1.6)
- 옵션 A 그대로 / **B 이동 + 신규 (NCC 권장)** / C "outdated" 헤더
- D9 결정 대기

### 4.6 진화 메커니즘 (Build/Retrospect/Distill/Apply) 본격 작동 (R1.5)
- `260520_system_architecture.md` R3 합의된 4단계 사이클
- 시점: C R2 (즉시)

---

## 4. §6 참조 문서 (영상 관련만 발췌)

| 분류 | 파일 |
|---|---|
| **C chatlog (R0+R1)** | `00_project_hub/10_chatlog/260523_video_v1_5_standardize.md` |
| 영상 표준 (현) | `10_system/10_principles/STORY_VIDEO_v1_5.md` ← R2에서 4개 항목 갱신 |
| 영상 v1.5 unit-01 회고 | `10_system/50_insights/260520_unit01_story_video_v1_5.md` (미반영 2건) |
| insights index | `10_system/50_insights/_index.md` |
| 채널 비전 리뷰 | `00_project_hub/10_chatlog/260516_channel_vision_review.md` (시즌1=5인, 창의 제안 8) |
| 시스템 아키텍처 합의 | `00_project_hub/10_chatlog/260520_system_architecture.md` (진화 메커니즘 4단계) |
| 메타 플래닝 | `00_project_hub/10_chatlog/260516_meta_planning.md` (앱=백본 / 영상=보조) |
| ⚠️ 옛 마스터 플랜 | `10_system/70_meta/{VISION,MASTER_PLAN,ROADMAP}.md` (D9 처리 대기) |

---

## 5. NCC 추가 분석 — sub-project 후 current-plan 갱신 의무

본 sub-project 분리 후 current-plan.md 갱신 필요:

| 갱신 항목 | 내용 |
|---|---|
| §0 entry point | 본 sub-project README 진입 안내 추가 |
| §2.C | 본 sub-project 로 작업 위치 이동 안내 (chatlog 안 진행이 아니라 sub-project 안 진행) |
| §6 참조 | `11_video_gen_process/` 추가 |

→ 본 sub-project 셋업 직후 current-plan.md edit 으로 처리 (본 세션 마지막 단계).

---

## 변경 이력

- 2026-05-23: 발췌. §0 + §2.C + §4.5/4.6 + §6 + NCC 의견.
