<!-- current-plan.md -->

# Current Plan — math-story-telling

> 가장 최신 상태와 다음 할 일. 새 세션 시작자는 이 파일과 `CLAUDE.md` 를 먼저 읽는다.
> 마지막 업데이트: 2026-05-23 (C R0+R1 진단 완료 시점).

---

## 0. 한 줄

**C 영상 v1.5 표준화 진행 중 — R0 진단(13편 가정) → R1 zoom out 재진단(시즌1=5편 권장).**
Nick D6(scope) 결정 대기 + NCC 자율 진행 가능 4건 (§3.C.4).

### 🚪 compact 후 새 세션 entry point

1. `CLAUDE.md` 읽기
2. **이 파일 (current-plan.md) 읽기** ← 여기
3. **`11_video_gen_process/README.md`** 읽기 (영상 R&D sub-project 진입점 — 2026-05-23 신설)
4. `11_video_gen_process/00_charter/{VISION,GOALS,DECISIONS}.md` (placeholder, compact 후 본격 작성)
5. `11_video_gen_process/10_reference/_origin.md` + `01_R0_R1_summary.md` (외부 자료 발췌)
6. (필요 시) `00_project_hub/10_chatlog/260523_video_v1_5_standardize.md` (원본 chatlog)
7. 다음 액션은 §3.C 의 "다음 액션" 분기 참조

---

## 1. 완료된 작업

### A. 마이그 (2026-05-22)
- mid_eun + mathtelling + design-system + 00_LearningSystem 4개 repo → math-story-telling 단일 repo
- `##_` prefix 9 최상위 디렉토리
- 15 skill SSOT + 1 agent SSOT + mirror
- 13단원 (01~13) + 19인 인물 자료
- 옛 자료 안전망 `90_archive/`
- gitignore 게이트 `.private/`
- 참조: `00_project_hub/10_chatlog/260521_repo_consolidation*.md`, `20_plan/260521_migration_plan.md`, `40_context/external_repos.md`

### A-잔재. math1 폴더 정리 (2026-05-22)
- `40_grades/middle/math1/unit-01/` (mathtelling 시드, 정보 가치 0) 삭제
- `_index_v_mathtelling.html` (충돌 회피 잔재) 삭제
- commit `13b0159`

### F. walk_01 보강 (2026-05-23)
- `40_grades/middle/math1/01_소인수분해/problems/walk_01_H{1,2,3}.html` 신규 3개
- H1: 100 이하 소수 25개 (에라토스테네스 체 100칸 시각화)
- H2: 소피 제르맹 소수 (p=2,3,5,7 검증표)
- H3: 자릿수 합 = 10인 가장 작은 세 자리 소수 = 109
- 양식: unit 02 walk_01_H1.html 5페이지 표준 (문제→1·2·3단계→정답+요약)

### B. 수학 챕터 표준 정의 (2026-05-22 ~ 05-23)

- **chatlog**: `00_project_hub/10_chatlog/260522_math_chapter_standard.md` (Round 0 → 2.G + 종합 마무리)

| sub-round | 산출물 |
|---|---|
| 2.A | schema v2 + slug-en 영미권 표준 갱신 (Common Core Grade 7) + unit 01 meta 시범 |
| 2.B | 13단원 인물 풀 26 entry (primary + secondary) |
| 2.C | 14인 인물 사실 md 신규 — `30_content/people/` 총 19인 |
| 2.D | 12 단원 `30_content/units/NN/meta.json` 신규 (총 13, schema v2) |
| 2.E | `10_system/10_principles/UNIT_PAGE_STANDARD.md` v0.1 (11 섹션) |
| 2.F | walk_01 누락 확인 — 보강은 후속 단발 |
| 2.G | `40_grades/middle/math1/index.html` (hub) 재정비 (design-system 경로·카드 link·인물 매핑·slug-en 표기) |

핵심 결정:
- **데이터 모델 v2**: `meta.persons[]` 배열 (N:M, 단원에 여러 인물 가능), 영상 episode-key ref
- **영상 이중 트리**: 원본 `50_channel/people/<ref>/<ep>/` + view `50_channel/seasons/season-N/unit-NN/`
- **URL slug 정책**: 폴더 한글 유지, `meta.slug-en` (Common Core 어휘) → 빌드 시 URL 변환
- **인물 N:M**: 한 단원에 여러 인물 OK, 한 인물이 여러 단원 OK (`kepler` 06·09·11, `archimedes` 10·12, `al-khwarizmi` 02·03·04, `euclid` 01·07·08)

---

## 2. 진행 중 작업

### 🟢 C. 영상 v1.5 표준화 (R0 + R1 완료, sub-project 셋업 완료, R2 대기)

> **작업 위치 이전**: 2026-05-23 — `11_video_gen_process/` sub-project 셋업 완료.
> 본격 R&D 는 sub-project 안에서 진행. 큰 결정 (D6 scope 등) 만 외부 chatlog.
>
> chatlog (origin): `00_project_hub/10_chatlog/260523_video_v1_5_standardize.md` (R0 ~ R1)
> sub-project 진입: `11_video_gen_process/README.md`
> sub-project 헌장: `11_video_gen_process/00_charter/{VISION,GOALS,DECISIONS}.md`
> plan (origin): `00_project_hub/20_plan/260522_plan_video_flow.md`
> TaskList #17 (in_progress)

#### 2.C.1 R0 (NCC 1차 진단) 핵심 발견
- unit-01 v1.5 baseline 정밀 분석 — narration_v1_5.xml은 **ElevenLabs/Azure SSML 풀스펙 input** 으로 이미 작성됨 (break ~40회 + prosody pitch/rate 강조)
- image_prompts.md 의 "공통 캐릭터 시트" 패턴 — 19인 모두 시트 필요
- meta.json schema v2 → 12단원 시드 자동 생성 가능

#### 2.C.2 R1 (NCC zoom out 재진단) 핵심 발견
- **R0의 "13편 일괄" 가정이 옛 채널 비전(`260516_channel_vision_review.md`)의 "시즌1 = Ancient 5단원" 결정과 어긋남**
- 어제 R0의 갭 7개 (chatlog §1.3): scope / 4편 분할 / 5인 voice 매핑 / 캐릭터 시트 미반영 / length dry run 미반영 / "앱=백본 영상=보조" 우선순위 / 창의 제안 8개 미검토
- 현 위치 = **Phase 0-A 진행 중, 영상 1/5 완성** (시즌1 = 5편 중 unit-01만)
- 옛 `10_system/70_meta/` (VISION/MASTER_PLAN/ROADMAP) = 00_LearningSystem 시절 문서, 마이그 후 outdated → 별도 처리(D9) 필요

#### 2.C.3 Nick 결정 대기 (R1 §1.8)
- 🔴 **D6 scope**: α 13편 일괄 / **β 시즌1 5편 우선 (NCC 권장)** / γ 시즌1+시즌2 일부
- 🟡 보조 (NCC 권장 채택 시 자율 진행): D7 단원→영상 분할 / D8 창의 제안 / D9 옛 70_meta 처리 / D10 진화 메커니즘 본격화 시점
- 🟢 R0의 D1~D5 (TTS·이미지·이중 트리·시드·audit) 결정 유지

#### 2.C.4 NCC 자율 진행 가능 4건 (Nick 응답 대기 중에도 OK — R1 §1.9)
1. `10_system/50_insights/_index.md` 의 미반영 2건을 STORY_VIDEO_v1_5.md 에 반영 + `[x]` 표시 (진화 메커니즘 본격화 첫걸음)
2. `se_story_video_v1_5` skill 점검 (`.claude/skills/`)
3. STORY_VIDEO_v1_5.md 4개 항목 갱신 (§2.2 캐릭터 시트 / §4 length dry run / §3.1 voice 매핑 / §7 디렉토리)
4. 옛 `10_system/70_meta/` 정합성 audit 보고서 (이동은 D9 후)

#### 2.C.5 다음 액션 분기 (compact 후 새 세션 진입 시)

> ⚠️ 모든 분기의 진행 장소 = `11_video_gen_process/` sub-project 안 `50_sessions/` 라운드.

- **분기 A**: Nick이 D6 답 → R2 시작 (scope 확정 + 5축 결정 → `20_principles/` 시드 작성 → `STORY_VIDEO_v1_5` promote)
- **분기 B**: Nick D6 미응답 → 1.9의 자율 4건 진행 (sub-project 내 R0 sprint) → 끝나면 다시 D6 응답 요청
- **분기 C**: Nick "다 권장대로" → β scope 채택 + 1.9 진행 + R3 (시즌1 5인 캐릭터 시트) 진입

#### 2.C.6 본 sub-project 셋업 완료 (2026-05-23)

- 디렉토리: 9 sub-dir + 30_pipeline 내 6 stages = 15 폴더 + 25 파일
- 헌장 placeholder: `00_charter/{VISION,GOALS,DECISIONS}.md`
  - D-001 (sub-project 분리) / D-002 (풀세팅 9) / D-003 (reference 발췌) 확정
  - D-004 ~ D-013 placeholder (= 상위 D6~D10 + sub-project 신규 결정)
- reference 발췌 3개: `10_reference/{01_R0_R1_summary, 02_baseline_unit01, 03_current_plan_C}.md`
- 외부 SSOT 와의 관계 명시: `10_reference/_origin.md`
- 빈 영역들 모두 README + 후보 목록 (compact 후 진입 가이드)

---

### 🟡 다음 다음: E. 배포 매핑·hookup

> plan: 별도 chatlog 예정 (`26mmdd_deploy_mapping.md`)
> TaskList #19

**전제**: C 결정 후 (영상 viewing 디렉토리 트리 확정 필요)

**탐색할 이슈**:
- `60_deploy/middle-school/` 빌드 출력 구조 정의
- 폴더 한글 `NN_<한글>` → URL `NN_<slug-en>` 변환 빌드 스크립트
- 현 GH Pages 배포 `jwj-nick.github.io/mid1/...` 대응
- channel 배포 `60_deploy/channel/` → YouTube 업로드 큐
- design-system 경로 dev (`../../../20_packages/...`) vs deploy (`/assets/all.css`) 매핑

---

### 🟠 가장 나중: D. 영상 단원별 확장

> TaskList #20
> 전제: C 표준 확정 + D6 scope 결정 + (선택) E 배포 매핑

**방식**: 단원당 별도 chatlog (mid_eun `260510_unit02.md` 패턴 답습)
- `260mmdd_unit02_video.md` (브라마굽타)
- `260mmdd_unit03_video.md` (알콰리즈미)
- ...

페이스 (β scope 가정): 시즌1 5편 unit-02~05 단원당 1~2주. unit-06~13은 시즌1 회고 후 결정.

---

## 4. 잔여 인프라 작업 (분리된 후속)

### 4.1 `30_content/concepts/` 13단원 개념 검수·보완
- 마이그된 옛 `40_BaseDocs` 의 raw 자료. Phase 1 작업.
- `/se_concept_review` skill로 단원당 작업
- 시점: 각 단원 진입 시 (D와 함께)

### 4.2 단원 페이지 (index/story/concepts.html) UNIT_PAGE_STANDARD 준수 audit
- 13단원 모두 mid_eun 시절 작성된 HTML
- 새 standard (`10_system/10_principles/UNIT_PAGE_STANDARD.md` v0.1) 와 격차 검토
- 옛 design-system 경로 → 새 경로 갱신 (math1/index.html 외 단원 내부 HTML 들)
- `/se_ncc_audit_app` 활용. 시점: C 표준 확정 + 단원 진입 시.

### 4.3 episode md 분리 (선택)
- 현재 인물 사실 md에 일화 통합. schema v2 정신은 분리.
- 영상 작업(C) 시점에 `50_channel/people/<ref>/<ep>/storyboard_v1_5.md` 가 자연스러운 episode md 역할.
- 인물 사실 md 안 일화 섹션은 그대로 유지 가능 (중복 허용).

### 4.4 era-palette CSS 토큰 정식화
- 현재 `30_content/units/NN/meta.json` 의 `era-palette` 값은 string ref만
- `20_packages/design-system/subjects/people.css` (또는 era.css) 신설해 토큰 정의 검토
- 시점: UNIT_PAGE_STANDARD 활용 본격화 시

### 4.5 ⭐ 옛 `10_system/70_meta/` 마스터 플랜 정합성 처리 (NEW, R1.6 발견)
- 현 `VISION.md` / `MASTER_PLAN.md` / `ROADMAP.md` = 옛 00_LearningSystem 시절 (여러 자식 프로젝트 통합 메타). math-story-telling 단일 repo 마이그 후 outdated.
- 처리 옵션: A 그대로 유지 / **B `90_archive/` 이동 + 신규 VISION 작성 (NCC 권장)** / C "outdated" 헤더 한 줄
- D9 결정 대기. 별도 chatlog `260mmdd_meta_realignment.md` 권장.

### 4.6 ⭐ 진화 메커니즘 (Build/Retrospect/Distill/Apply) 본격 작동 (NEW, R1.5)
- `260520_system_architecture.md` R3 에서 합의된 4단계 사이클. unit-01 v1.5 retrospective 1건 작성 후 멈춰있음.
- `10_system/50_insights/_index.md` 미반영 2건 (length dry run + 캐릭터 시트 분리) 처리 → STORY_VIDEO_v1_5.md 반영 → `[x]` 표시
- `se_story_video_v1_5` skill 에 Phase E (자동 retrospective) 추가
- 시점: C R2 (즉시) — NCC 자율 진행 가능 (R1.9 §1)

---

## 5. 외부 의존 (Nick 직접 챙길 사항)

> 참조: `00_project_hub/30_history/Nick_TODO.md`

- **T1. ElevenLabs 한국어 TTS** 가입 (영상 품질 향상)
- **T2. AI 이미지 생성 워크플로우** 손에 익히기 (Stable Diffusion 로컬 또는 API)
- **(옛 repo 처리)** mid_eun / mathtelling / mathtelling-design-system GitHub README에 "moved to" 한 줄 추가 — 시점은 Nick 판단 (지금 안 함)

---

## 6. 참조 문서 (빠른 link)

| 분류 | 파일 |
|---|---|
| 진입점 | `CLAUDE.md` |
| 마이그 기록 | `00_project_hub/10_chatlog/260521_repo_consolidation*.md`, `20_plan/260521_migration_plan.md` |
| 외부 repo | `00_project_hub/40_context/external_repos.md` |
| B chatlog | `00_project_hub/10_chatlog/260522_math_chapter_standard.md` |
| B plan | `00_project_hub/20_plan/260522_plan_math_chapter.md` |
| C plan | `00_project_hub/20_plan/260522_plan_video_flow.md` |
| **C chatlog (R0+R1, origin)** | `00_project_hub/10_chatlog/260523_video_v1_5_standardize.md` |
| ⭐ **본 sub-project entry** | **`11_video_gen_process/README.md`** |
| 본 sub-project 헌장 | `11_video_gen_process/00_charter/{VISION,GOALS,DECISIONS}.md` |
| 본 sub-project reference index | `11_video_gen_process/10_reference/_origin.md` |
| 단원 페이지 표준 | `10_system/10_principles/UNIT_PAGE_STANDARD.md` |
| 영상 표준 (구) | `10_system/10_principles/STORY_VIDEO_v1_5.md` ← C R2에서 4개 항목 갱신 예정 |
| 앱 표준 | `10_system/10_principles/APP_PRINCIPLES.md` |
| 학습자 프로필 | `10_system/20_context/LEARNER_PROFILE.md` |
| 인물 사실 19인 | `30_content/people/*.md` |
| 단원 메타 13개 | `30_content/units/NN/meta.json` |
| Nick TODO | `00_project_hub/30_history/Nick_TODO.md` |
| **영상 v1.5 unit-01 회고** | `10_system/50_insights/260520_unit01_story_video_v1_5.md` (미반영 2건) |
| **insights index** | `10_system/50_insights/_index.md` |
| **채널 비전 리뷰** | `00_project_hub/10_chatlog/260516_channel_vision_review.md` (시즌1=5인, 창의 제안 8) |
| **시스템 아키텍처 합의** | `00_project_hub/10_chatlog/260520_system_architecture.md` (진화 메커니즘 4단계) |
| **메타 플래닝** | `00_project_hub/10_chatlog/260516_meta_planning.md` (앱=백본 / 영상=보조) |
| ⚠️ 옛 마스터 플랜 (outdated) | `10_system/70_meta/{VISION,MASTER_PLAN,ROADMAP}.md` (D9 처리 대기) |

---

## 7. TaskList 현황 (Claude Code 세션 내)

| # | 상태 | 작업 |
|---|---|---|
| 16 | ✅ completed | A. 마이그 잔재 정리 |
| 18 | ✅ completed | B. 수학 챕터 표준 정의 |
| 21 | ✅ completed | F. walk_01 보강 (01단원 H1·H2·H3) |
| 17 | 🔄 in_progress | **C. 영상 v1.5 표준화** (R0+R1 완료, R2 대기) |
| 19 | ⏳ pending | E. 배포 매핑·hookup |
| 20 | ⏳ pending | D. 영상 단원별 확장 (β scope = 시즌1 4편) |

---

## 8. 진행 로그 (timeline)

| 날짜 | 내용 |
|---|---|
| 2026-04-26 | mid_eun: 웹 세션 → 로컬 이관, 문서 전체 재정리 |
| 2026-04-28 | mid_eun: 길 B+A 완성 (L2 슬라이더 + Unit 1 시범) |
| 2026-05-04~05 | mid_eun: 전면 Setup — CLAUDE.md 재작성, 4축 구조, 스킬/에이전트, 40_BaseDocs |
| 2026-05-09 | mid_eun: 디렉토리 재구조화, 50_units 통합 |
| 2026-05-10~11 | mid_eun: 13단원 문제 일괄 (260510_unit02~13.md) |
| 2026-05-14 | mid_eun: 영상 v1.5 unit-01 완성 |
| 2026-05-21 | repo 통합 결정 (Round 1·2), migration plan 확정 |
| **2026-05-22** | **A. 마이그 실행 + B 챕터 표준 정의 (Round 0~2.D)** |
| **2026-05-23** | **B Round 2.E~G 마무리 + current-plan 갱신 + F walk_01 보강 + C R0(13편 진단) + C R1(zoom out 5편 권장 + 7갭 발견) + `11_video_gen_process/` sub-project 셋업 (풀세팅 9 sub-dir)** |
