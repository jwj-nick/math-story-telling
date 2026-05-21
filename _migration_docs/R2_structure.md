<!-- 260521_repo_consolidation_r2.md -->

# Repo 통합 — Round 2 (확정 + Migration Outline)

> **참조**: Round 1 원본은 `260521_repo_consolidation.md` (Nick D1-D8 답변 포함).
> **이 파일**: 답변 반영한 최종 결정 + 마이그레이션 outline.
> **실행 가이드 (별도 파일)**: `00_project_hub/plan/260521_migration_plan.md` — 새 세션이 step-by-step 따라할 문서.

---

## Round 2.1 — Nick D1-D8 답변 반영 요약

| # | 결정 | Round 2 적용 |
|---|---|---|
| **D1** | repo 이름 = `math-story-telling`. 내부 디렉토리에 `##_` prefix | 최상위 모두 `00_`, `10_`, ... 형식 |
| **D2** | 깨끗 시작 (A). 옛 repo history는 metadata로 안내. `project_hub/context/` 신설. `archive/` 디렉토리 신설 | `00_project_hub/40_context/`, `90_archive/` 신설 |
| **D3** | 1 repo + packages 폴더 모듈화 (권장) | `20_packages/` |
| **D4** | 한 repo + 학년 구분 (권장) | `40_grades/middle/`, `40_grades/high/` |
| **D5** | 00_LearningSystem 통합 | `10_system/70_meta/` |
| **D6** | 일괄 마이그레이션 | 1 세션 안 완수 목표 (별도 세션) |
| **D7** | 배포는 현재 GH Pages repo 유지 (변화는 향후 재논의) | `60_deploy/` 빌드 산출물 push 대상 = 기존 `jwj-nick.github.io/mid1` 등 |
| **D8** | `.private/` gitignore | `.private/`, gitignore 추가 |

---

## Round 2.2 — 최종 폴더 구조 (확정)

```
math-story-telling/                           ── 새 git repo (깨끗 시작)
│
├── 00_project_hub/                           대화·플랜·메타데이터
│   ├── 10_chatlog/                             라운드 기반 대화 (이 파일도 여기 이동)
│   ├── 20_plan/                                확정 플랜 (master_plan 등)
│   ├── 30_history/                             의사결정 기록
│   └── 40_context/                             ⭐ 외부 참조 메타 — old repo URL, 마이그레이션 메모
│
├── 10_system/                                메타 — 원칙·skill·진화 (math-storytelling 전용)
│   ├── 10_principles/                          STORY_VIDEO_v1_5, APP_PRINCIPLES 등 SSOT
│   ├── 20_context/                             TONE_GUIDE, ERA_PALETTES, LEARNER_PROFILE 등
│   ├── 30_skills/                              ⭐ Claude Code skill SSOT
│   ├── 40_proposals/                           incubation (chatlog → proposals → skills)
│   ├── 50_insights/                            회고 누적
│   ├── 60_workflows/                           다단계 절차
│   └── 70_meta/                                ⭐ 메타-메타 (현 00_LearningSystem 통합)
│       ├── VISION.md
│       ├── PATTERNS/
│       ├── BLUEPRINTS.md
│       ├── ROADMAP.md
│       └── ...
│
├── 20_packages/                              떼서 다른 앱에 쓸 모듈
│   ├── design-system/                          현 mathtelling-design-system
│   ├── video-pipeline/                         HyperFrames+GSAP+templates
│   └── (future modules)
│
├── 30_content/                               학년·매체 무관 SSOT
│   ├── people/                                 13인물 사실
│   ├── concepts/                               단원별 개념 뼈대 (현 40_BaseDocs)
│   ├── literacy/                               수학 언어 트랙 L1~L7
│   └── research/                               deep research
│
├── 40_grades/                                학년별 산출물
│   ├── middle/
│   │   ├── math1/
│   │   │   ├── unit-01_소인수분해/
│   │   │   ├── ...
│   │   │   └── unit-13_*/
│   │   ├── math2/                            (future)
│   │   └── math3/                            (future)
│   └── high/                                 (future, 고1 통합 시)
│
├── 50_channel/                               영상 소스
│   ├── season-1-ancient/
│   │   └── unit-01/...
│   ├── _templates/
│   ├── _docs/
│   └── _archive/                               v1 영상 (현 mid_eun/90_video)
│
├── 60_deploy/                                빌드 출력 (gitignore — 빌드 시 생성)
│   ├── middle-school/                          → push to GH Pages (jwj-nick.github.io/mid1)
│   ├── high-school/                            (future)
│   └── channel/                                → YouTube 업로드 큐
│
├── 70_tools/                                 빌드·sync·배포 스크립트
│   ├── sync-skills.sh
│   ├── build-deploy.sh                       (future)
│   └── ...
│
├── 90_archive/                               ⭐ 옛 자료·반영완료 자료 보관
│   ├── mid_eun_layout_snapshot.md              옛 디렉토리 구조 참고용
│   ├── 00_LearningSystem_original/             통합 전 원본 백업
│   └── ...
│
├── .claude/                                  스킬 거울 (10_system/30_skills/에서 sync)
│   ├── skills/
│   ├── agents/                                 unit-orchestrator 등
│   └── settings.local.json
│
├── .private/                                 ⭐ gitignore — 민감 자료
│   ├── feedback/                               딸 글·반응
│   └── learner_personal.md
│
├── CLAUDE.md                                 ⭐ 진입점 (새 세션이 처음 읽는 파일)
├── README.md                                 repo 소개
├── .gitignore                                .private/, _assets/*.png, *.mp3, *.mp4 등
└── LICENSE                                   (Public 시)
```

### Prefix 규칙 (최상위만)
- 최상위 디렉토리: `##_<name>/` (00, 10, 20, 30, 40, 50, 60, 70, 90)
- 내부 (한 단계 아래)는 자유 — 단, 또 다른 카테고리화 필요하면 또 `##_` 사용 (예: `10_system/10_principles/`)
- 점수형이라 사이 사이 새 디렉토리 삽입 가능 (예: 80_ 추가 가능)

---

## Round 2.3 — 마이그레이션 매핑 (요약)

> **상세 매핑·실행 스크립트**: `00_project_hub/plan/260521_migration_plan.md` 참조.

### 4개 원본 → 새 repo

| From | To (in `math-story-telling/`) |
|---|---|
| **(1)** mathtelling-design-system/* | `20_packages/design-system/` |
| **(2)** mathtelling/apps/math1/* | `40_grades/middle/math1/` (50_units와 머지) |
| (2) mathtelling/channel/* | `50_channel/` |
| (2) mathtelling/content/* | `30_content/people/` (units 메타는 검토) |
| (2) mathtelling/system/* | `10_system/` (10~70 매핑) |
| (2) mathtelling/tools/* | `70_tools/` |
| (2) mathtelling/Nick_TODO.md | `00_project_hub/30_history/Nick_TODO.md` |
| **(3)** mid_eun/00_project_hub/* | `00_project_hub/` (chatlog/plan/history 매핑) |
| (3) mid_eun/10_docs/* | `10_system/20_context/` (learner-profile 등) + `30_content/literacy/` |
| (3) mid_eun/20_research/* | `30_content/research/` |
| (3) mid_eun/40_BaseDocs/* | `30_content/concepts/` + `30_content/literacy/` |
| (3) mid_eun/50_units/* | `40_grades/middle/math1/` |
| (3) mid_eun/80_professional_idea/* | `10_system/70_meta/professional/` |
| (3) mid_eun/90_video/* | `50_channel/_archive/v1/` |
| (3) mid_eun/APP_PRINCIPLES.md | `10_system/10_principles/APP_PRINCIPLES.md` |
| (3) mid_eun/.claude/skills/* | `10_system/30_skills/` + mirror to `.claude/skills/` |
| (3) mid_eun/.claude/agents/* | `.claude/agents/` |
| (3) mid_eun/CLAUDE.md | `90_archive/mid_eun_CLAUDE.md` (새 CLAUDE.md는 신규 작성) |
| (3) mid_eun/01_dev_study/* | `90_archive/dev_study/` (또는 별도 처리) |
| (3) mid_eun/archive/* | `90_archive/mid_eun_archive/` |
| (3) mid_eun/feedback/* | `.private/feedback/` (gitignore) |
| **(4)** 00_LearningSystem/* | `10_system/70_meta/` |

### 외부 참조 메타데이터 (D2 응답)

`00_project_hub/40_context/external_repos.md` 신설:
- 이전 git repo URL 목록 (mid_eun, mathtelling, mathtelling-design-system, 00_LearningSystem)
- 각 repo의 마지막 commit hash + 날짜
- "이전 히스토리 확인이 필요하면 이 URL을 체크아웃" 안내
- 옛 README 발췌 인용

---

## Round 2.4 — 새 세션 진입 가이드

### 새 세션이 처음 봐야 할 것

1. **이 파일** (`260521_repo_consolidation_r2.md`) — 결정·구조 이해
2. **`260521_migration_plan.md`** — step-by-step 실행
3. **`260521_repo_consolidation.md`** — Round 1 (Nick의 원본 답변·맥락)

### 새 세션이 만들 것

- 새 git repo `math-story-telling` (GitHub) — 위치 Nick 확인 필요 (open question Q1)
- 로컬 clone 후 마이그레이션 스크립트 실행
- 첫 commit + push
- 마이그레이션 완료 후 옛 repo들 archive 마킹

### 새 세션이 결정해야 할 것 (open questions)

→ 다음 섹션 Round 2.5 참조

---

## Round 2.5 — Open Questions (마이그 진행 중 결정 필요)

> 새 세션이 작업 시작 시 Nick에게 묻거나, 안전한 기본값으로 진행.

### Q1. 로컬 clone 위치 — Nick 확인 필요
- 후보: `C:/Kids/math-story-telling/` (최상위 새 폴더, 권장)
- 또는: `C:/Kids/90_Workspace/math-story-telling/`
- 또는: `C:/Kids/30_MiddleSchool/math-story-telling/` (현재 위치 근처)
- **기본값**: `C:/Kids/math-story-telling/` — 학년 무관 (D4 한 repo 학년 구분 정신)

### Q2. apps/math1 vs 50_units 중복 처리
- 현 mathtelling/apps/math1/unit-01/은 mid_eun/50_units에서 일부 복사된 신생
- 50_units 13단원 vs apps/math1 1단원
- **권장**: 50_units를 SSOT로, apps/math1은 1단원만 검토해서 더 새로운 부분만 머지
- 새 위치: `40_grades/middle/math1/unit-NN_*/`

### Q3. content/units 메타 vs 50_units 폴더 동일?
- mathtelling/content/units/01/meta.json 등 메타 데이터만
- mid_eun/50_units/01_*/는 실제 산출물 (HTML 등)
- **권장**: content/는 학년 무관 데이터 (meta·인물·개념)만, grades/는 학년별 산출물 (HTML 앱). meta.json은 `30_content/units/01/meta.json`으로.

### Q4. 디자인 토큰 — package import 방식
- mathtelling-design-system을 packages/design-system/으로 가져온 후, OSS 별 repo 유지할지?
- **권장**: 가져온 후 별 repo는 archive. 미래 OSS 다시 분리 필요 시 git filter-repo로 재추출.

### Q5. 70_HighSchool 통합 시점
- 고1 아들 자료 (`C:/Kids/70_HighSchool/`)는 별도 chatlog에서 통합 결정 (이번 마이그와 분리)
- **이번 마이그 범위**: `40_grades/high/` 빈 디렉토리만 생성

### Q6. .claude/agents/ 처리
- `se_agent_unit_orchestrator` 등 agents 정의
- **권장**: `10_system/30_skills/` 형제 디렉토리로 `10_system/35_agents/` 신설, mirror to `.claude/agents/`. sync-skills.sh를 sync-claude.sh로 일반화.

### Q7. CLAUDE.md 진입점
- 새 CLAUDE.md는 처음부터 작성 (옛 mid_eun CLAUDE.md는 90_archive로)
- **권장 구성**: 한 줄 요약 → 우선순위 → 4축 구조 → 새 폴더 구조 → 작업 방식 → 디렉토리 인덱스 → 절대 원칙 (옛 CLAUDE.md 기반)
- 새 세션이 이 파일 진입점 작성을 첫 작업으로 하도록.

### Q8. mathtelling.git, mathtelling-design-system.git GitHub 처리
- 마이그 완료 후 옛 repo는?
- **권장 (D2 정신)**: GitHub에 그대로 두되 README에 "→ moved to jwj-nick/math-story-telling" 한 줄 추가. 코드 변경 안 함. archive 효과.

### Q9. mid_eun.git의 미래
- 현재 active한 base repo. 마이그 후 어떻게?
- **권장**: 같은 처리 (README에 이동 안내). 코드 동결.
- 단, deploy/middle-school은 mid1 GH Pages (다른 repo)로 가니까 mid_eun이 deploy 역할 했다면 그건 새 repo가 인계.

---

## Round 2.6 — 다음 액션

### 이번 세션 (Round 2 완료)
- ✅ Round 2 chatlog (`_r2.md`) 작성 — 이 파일
- 🚧 `00_project_hub/plan/260521_migration_plan.md` — 새 세션용 step-by-step 가이드 작성 중

### 새 세션 (별도 시작) — Migration Session
1. GitHub에 `math-story-telling` repo 생성 (Nick 수동)
2. 로컬 clone (Nick 결정 후)
3. `260521_migration_plan.md` 따라 step-by-step 실행
4. 첫 commit + push
5. Open question Q1-Q9 차례로 결정

### 새 세션 이후
- Round 3: 마이그 완료 보고 + 진화 시작
- 다음 단원 (Unit 02) 새 구조에서 시작

---

## 변경 이력
- R2 (2026-05-21): Nick D1-D8 답변 반영. 최종 구조 (##_prefix), 매핑 표, open questions 9개. Migration plan은 별도 파일.
