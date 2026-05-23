<!-- current-plan.md -->

# Current Plan — math-story-telling

> 가장 최신 상태와 다음 할 일. 새 세션 시작자는 이 파일과 `CLAUDE.md` 를 먼저 읽는다.
> 마지막 업데이트: 2026-05-23.

---

## 0. 한 줄

마이그 + 수학 챕터 표준 정의 + F walk_01 보강 완료. **다음은 영상 v1.5 표준화 (C)** 가 우선 큰 작업.

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

(없음 — B 완료 후 다음 큰 작업 시작 대기)

---

## 3. 다음 할 일 (TaskList #17·19·20)

### 🟢 다음 큰 작업: C. 영상 v1.5 표준화

> Nick 비전 "그림 프롬프트 → 그림 → 영상" 파이프라인 정교화.
> plan: `00_project_hub/20_plan/260522_plan_video_flow.md`

**시작 방법**: 새 chatlog `00_project_hub/10_chatlog/260523_video_v1_5_standardize.md` (또는 작업 일자 prefix) Round 0 — NCC 진단부터.

**현재 reference**: `50_channel/season-1-ancient/unit-01/` (v1.5 산출물 13파일, final_v1_5.mp4 포함)
**unit-02~13**: `50_channel/_archive/v1/unit02~13/` 에 v1 버전만 (옛 mid_eun/90_video)

**탐색할 이슈**:
- v1.5 unit-01 구조를 13단원 표준으로 정제
- `10_system/10_principles/STORY_VIDEO_v1_5.md` + `se_story_video_v1_5` skill 점검·갱신
- 품질 게이트 (TTS 자연스러움, 길이·페이스, 가독성, 음악·SFX)
- workflow 정도: HyperFrames(GSAP) → FFmpeg → edge-tts 자동화
- 단원 1 vs N 세션 페이스
- audit skill 신설 검토 (`se_ncc_audit_video`?)
- **영상 디렉토리 재구조화**: B에서 합의된 `people/<ref>/<ep>/` 원본 + `seasons/` view 로 이동 (현 `season-1-ancient/unit-01/` → `people/eratosthenes/sieve-of-eratosthenes/` + `seasons/season-1-ancient/unit-01/`)
- AI 이미지 생성 워크플로우 (Nick_TODO T2 — Stable Diffusion 로컬 vs API)
- ElevenLabs 한국어 TTS 도입 (Nick_TODO T1)

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

### 🟠 가장 나중: D. 13단원 영상 일괄 확장

> TaskList #20
> 전제: C 표준 확정 + (선택) E 배포 매핑 정도 마련

**방식**: 단원당 별도 chatlog (mid_eun `260510_unit02.md` 패턴 답습)
- `260mmdd_unit02_video.md`
- `260mmdd_unit03_video.md`
- ...

페이스: 단원당 1~2주. 시즌 1(Ancient) 우선 → 시즌 2 Modern (확장 시).

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
| 단원 페이지 표준 | `10_system/10_principles/UNIT_PAGE_STANDARD.md` |
| 영상 표준 (구) | `10_system/10_principles/STORY_VIDEO_v1_5.md` ← C에서 갱신 예정 |
| 앱 표준 | `10_system/10_principles/APP_PRINCIPLES.md` |
| 학습자 프로필 | `10_system/20_context/LEARNER_PROFILE.md` |
| 인물 사실 19인 | `30_content/people/*.md` |
| 단원 메타 13개 | `30_content/units/NN/meta.json` |
| Nick TODO | `00_project_hub/30_history/Nick_TODO.md` |

---

## 7. TaskList 현황 (Claude Code 세션 내)

| # | 상태 | 작업 |
|---|---|---|
| 16 | ✅ completed | A. 마이그 잔재 정리 |
| 18 | ✅ completed | B. 수학 챕터 표준 정의 |
| 21 | ✅ completed | F. walk_01 보강 (01단원 H1·H2·H3) |
| 17 | ⏳ pending | **C. 영상 v1.5 표준화** ← 다음 |
| 19 | ⏳ pending | E. 배포 매핑·hookup |
| 20 | ⏳ pending | D. 13단원 영상 일괄 확장 |

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
| **2026-05-23** | **B Round 2.E~G 마무리 + current-plan 갱신 + F walk_01 보강** |
