<!-- current-plan.md -->

# Current Plan — math-story-telling

> 가장 최신 상태와 다음 할 일. 새 세션 시작자는 이 파일과 `CLAUDE.md` 를 먼저 읽는다.
> 마지막 업데이트: 2026-05-24 (영상 제작 프로젝트 단일 진입점화 완료).

---

## 0. 한 줄

**영상 제작 시스템 구축 (`11_video_gen_process/`) 본격 시작.** 1단계 (수동 깊이) 출발점. 자율 작업 5건 대기.

이 트랙은 영상을 양산하는 곳이 아니다 — **영상 제작 시스템 (프로세스 + 자동화) 을 구축**. 절대 목적: [`11_video_gen_process/00_charter/PURPOSE.md`](../../11_video_gen_process/00_charter/PURPOSE.md). 현재 계획: [`INTEGRATED_PLAN.md`](../../11_video_gen_process/00_charter/INTEGRATED_PLAN.md).

본 큰 그림 문서는 다른 트랙(A·B·F·E + 잔여 인프라) 의 위치 관리만 책임.

### 🚪 새 세션 entry point

1. `CLAUDE.md` 읽기 (큰 그림)
2. **이 파일 (current-plan.md) 읽기** ← 여기 (큰 그림 현재 상태)
3. **[`11_video_gen_process/00_charter/INTEGRATED_PLAN.md`](../../11_video_gen_process/00_charter/INTEGRATED_PLAN.md)** ← **영상 제작 프로젝트 단일 진입점** (이 한 편으로 전체 이해)
4. (필요 시) `11_video_gen_process/README.md` (디렉토리 안내)
5. (필요 시) `11_video_gen_process/10_reference/_origin.md` (외부 자료 path 인덱스)

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

### 🟢 C. 영상 제작 프로젝트

> **이 트랙의 상세 모두 → [`11_video_gen_process/00_charter/INTEGRATED_PLAN.md`](../../11_video_gen_process/00_charter/INTEGRATED_PLAN.md)**
>
> 본 current-plan 에서는 큰 그림 위치만. 결정·일정·결정 항목·자율 작업 모두 INTEGRATED_PLAN 한 곳에서 관리.
>
> TaskList #17 (in_progress)

**본질**:
영상을 양산하는 트랙이 아니다. **영상 제작 시스템 (프로세스 + 자동화) 을 구축하는 트랙**. 절대 변하지 않는 목적은 → [`11_video_gen_process/00_charter/PURPOSE.md`](../../11_video_gen_process/00_charter/PURPOSE.md)

**현재 상태**:
3단계 진화 모델 (수동 깊이 → 반복 적용 → 자동화) 중 1단계 (수동 깊이) 의 출발점에 있다. 1편 (에라토스테네스, 소인수분해) 빌드 경험은 있고, 그 경험에서 추출한 표준 4가지가 영상 표준 문서에 반영 대기.

**바로 다음 행동**:
INTEGRATED_PLAN §7 결정 ① (영상 표준 갱신 본격화) 가 활성화되면 §8 자율 작업 5건 시작.

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

### (옛 D 트랙: "영상 단원별 확장" — 폐기됨)

> 옛 frame 의 "13단원 영상 일괄 확장" 트랙은 폐기되었다.
> 영상 산출물은 본 프로젝트의 **부산물** 이지 별도 트랙이 아니다.
> 큰 그림 트랙이 어떤 단원을 진행할 때, `11_video_gen_process/` 의 시스템이 그 단원의 영상을 만들어낸다. 단원 진행 자체는 다른 트랙 (학습자 진도) 의 책임.

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

### 4.5 옛 `10_system/70_meta/` 마스터 플랜 정합성 처리
- 현 `VISION.md` / `MASTER_PLAN.md` / `ROADMAP.md` = 옛 00_LearningSystem 시절 (여러 자식 프로젝트 통합 메타). math-story-telling 단일 repo 마이그 후 outdated.
- 영상 제작 프로젝트의 [INTEGRATED_PLAN 결정 ⑮](../../11_video_gen_process/00_charter/INTEGRATED_PLAN.md) 에서 함께 다뤄짐.

### 4.6 진화 메커니즘 (Build/Retrospect/Distill/Apply) 본격 작동
- `260520_system_architecture.md` 에서 합의된 4단계 사이클. unit-01 retrospective 1건 작성 후 멈춰있음.
- 영상 제작 프로젝트의 [INTEGRATED_PLAN 결정 ① + 자율 작업 1~5](../../11_video_gen_process/00_charter/INTEGRATED_PLAN.md) 에서 본격화.

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
| ⭐ **영상 제작 프로젝트 단일 진입점** | **[`11_video_gen_process/00_charter/INTEGRATED_PLAN.md`](../../11_video_gen_process/00_charter/INTEGRATED_PLAN.md)** |
| 영상 프로젝트 디렉토리 안내 | `11_video_gen_process/README.md` |
| 영상 프로젝트 외부 자료 인덱스 | `11_video_gen_process/10_reference/_origin.md` |
| 영상 프로젝트 출발점 대화 | `00_project_hub/10_chatlog/260523_video_v1_5_standardize.md` |
| 단원 페이지 표준 | `10_system/10_principles/UNIT_PAGE_STANDARD.md` |
| 영상 표준 (갱신 대상) | `10_system/10_principles/STORY_VIDEO_v1_5.md` |
| 앱 표준 | `10_system/10_principles/APP_PRINCIPLES.md` |
| 학습자 프로필 | `10_system/20_context/LEARNER_PROFILE.md` |
| 인물 사실 19인 | `30_content/people/*.md` |
| 단원 메타 13개 | `30_content/units/NN/meta.json` |
| Nick TODO | `00_project_hub/30_history/Nick_TODO.md` |
| 1편 회고 (미반영 2건) | `10_system/50_insights/260520_unit01_story_video_v1_5.md` |
| 회고 인덱스 | `10_system/50_insights/_index.md` |
| 채널 비전 리뷰 | `00_project_hub/10_chatlog/260516_channel_vision_review.md` |
| 진화 메커니즘 4단계 합의 | `00_project_hub/10_chatlog/260520_system_architecture.md` |
| 메타 플래닝 (앱=백본) | `00_project_hub/10_chatlog/260516_meta_planning.md` |
| ⚠️ 옛 마스터 플랜 (outdated) | `10_system/70_meta/{VISION,MASTER_PLAN,ROADMAP}.md` |

---

## 7. TaskList 현황 (Claude Code 세션 내)

| # | 상태 | 작업 |
|---|---|---|
| 16 | ✅ completed | A. 마이그 잔재 정리 |
| 18 | ✅ completed | B. 수학 챕터 표준 정의 |
| 21 | ✅ completed | F. walk_01 보강 (01단원 H1·H2·H3) |
| 17 | 🔄 in_progress | **C. 영상 제작 시스템 구축** (`11_video_gen_process/`, [PURPOSE](../../11_video_gen_process/00_charter/PURPOSE.md) + [INTEGRATED_PLAN](../../11_video_gen_process/00_charter/INTEGRATED_PLAN.md)) |
| 19 | ⏳ pending | E. 배포 매핑·hookup |

---

## 8. 진행 로그 (timeline)

| 날짜 | 내용 |
|---|---|
| 2026-04-26 | mid_eun: 웹 세션 → 로컬 이관, 문서 전체 재정리 |
| 2026-04-28 | mid_eun: 길 B+A 완성 (L2 슬라이더 + Unit 1 시범) |
| 2026-05-04~05 | mid_eun: 전면 Setup — CLAUDE.md 재작성, 4축 구조, 스킬/에이전트, 40_BaseDocs |
| 2026-05-09 | mid_eun: 디렉토리 재구조화, 50_units 통합 |
| 2026-05-10~11 | mid_eun: 13단원 문제 일괄 (260510_unit02~13.md) |
| 2026-05-14 | mid_eun: 영상 1편 (에라토스테네스) 완성 |
| 2026-05-21 | repo 통합 결정 (Round 1·2), migration plan 확정 |
| **2026-05-22** | **A. 마이그 실행 + B 챕터 표준 정의 (Round 0~2.D)** |
| **2026-05-23** | **B Round 2.E~G 마무리 + current-plan 갱신 + F walk_01 보강 + 영상 트랙 디렉토리 (`11_video_gen_process/`) 셋업 + 출발점 분석** |
| **2026-05-24** | **영상 트랙 frame 재정렬 — 산출물 양산 frame 폐기. 본질이 "영상 제작 시스템 구축" 임을 명시 (`PURPOSE.md` 신설). `INTEGRATED_PLAN.md` 3단계 진화 frame 으로 전면 재작성.** |
