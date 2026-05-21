<!-- 260521_repo_consolidation.md -->

# Repo 통합 — Math Story Telling 전용 단일 Source Repo

> Nick 요청 (2026-05-21):
> "directory를 결국 하나만 사용하면 좋겠어요. 거기 필요한 skill/context/qna system이 다 있도록.
> 완전 다시 정리해서 math story telling 전용으로 하나만의 git repo for source, 배포는 계속 contents 늘리고 몇군데에 나눠서. 중학생용/고등학생용 따로.
> 일단 math story에 집중하면 계속 고도화. 그 시스템의 일부를 떼가서 다른 앱에서 사용. 이런 건 다 가능할듯."
>
> Round 1 — NCC 진단·미래 모습 제안·결정 질문. 라운드 거듭하며 합의 → 일괄 마이그레이션 플랜 수립 → 실행.

---

## Round 1.1 — 현재 4개 디렉토리 진단

### 1.1.1 inventory

| # | 경로 | Git | 무엇 | 성숙도 | 비고 |
|---|---|---|---|---|---|
| **(1)** | `C:\Kids\90_Workspace\mathtelling-design-system` | `jwj-nick/mathtelling-design-system` (public) | CSS 토큰·디자인 어휘 | 🟢 안정 | OSS-able. 작음. |
| **(2)** | `C:\Kids\90_Workspace\mathtelling` | `jwj-nick/mathtelling` (public) | monorepo 골격: apps/, channel/, content/, system/, tools/ | 🟡 신생 (5 commits, 2026-05) | **system/ 방금 만듦**. 미래 중심 후보. |
| **(3)** | `C:\Kids\30_MiddleSchool\260426_MathTelling_Idea` | `jwj-nick/mid_eun` (?) | 13단원 50_units, 40_BaseDocs, 10_docs, 20_research, 90_video, .claude/skills/, 00_project_hub | 🟢 **가장 성숙** | 모든 실제 산출물·히스토리. 이름이 딸 이름. |
| **(4)** | `C:\Kids\00_LearningSystem` | (git 아님) | 메타 레이어 — VISION, PATTERNS, BLUEPRINTS, MASTER_PLAN, ROADMAP | 🟡 중간 | 중1+고1 양쪽 패턴 추출. math 전용 아님. |

### 1.1.2 현재 중복·분산

| 자원 | (1) design | (2) mathtelling | (3) mid_eun | (4) Learning |
|---|---|---|---|---|
| 콘텐츠 (단원·인물) | — | content/people, content/units (신생) | **50_units, 40_BaseDocs (성숙)** | — |
| 영상 소스 | — | channel/ (v1.5) | 90_video/ (v1) | — |
| Skill 정의 | — | system/skills/se_distill_principles | **.claude/skills/ 14개 (SSOT)** | — |
| 대화·플랜 | — | — | **00_project_hub/chatlog/** | 00_chatlog/ |
| 디자인 토큰 | **tokens/ (SSOT)** | (mathtelling-design-system import) | inline CSS | — |
| 메타 (원칙) | — | system/principles, system/context (신생) | APP_PRINCIPLES.md, 10_docs/* | 30~50_*.md |
| 학습자 프로필 | — | — | **10_docs/01_learner-profile.md** | 60_LEARNERS.md |
| 메타 비전 | — | — | — | **10_VISION.md (양 학년)** |

→ **3 곳에 분산 + 4번이 한 단계 위 메타**. 그래서 헷갈리고 좌충우돌.

---

## Round 1.2 — 미래 모습 제안 (창의적 비전)

### 1.2.1 한 줄 원칙

> **"Source 1개, 배포 N개, 모듈 떼어쓰기 가능"**

### 1.2.2 새 repo 구조 (제안)

```
math-story-telling/                  ← 1개 git repo, public (민감 자료 gitignore)
│
├── packages/                         ── 떼서 다른 앱에 쓸 수 있는 모듈
│   ├── design-system/                  CSS 토큰 (현 mathtelling-design-system)
│   ├── video-pipeline/                 HyperFrames+GSAP 템플릿 (현 channel/_templates, tools)
│   └── (future: ui-components/, math-figures/, ...)
│
├── content/                          ── 학년·매체 무관 SSOT
│   ├── people/                         13인물 사실 (현 mathtelling/content/people)
│   ├── concepts/                       단원별 개념 뼈대 (현 40_BaseDocs)
│   ├── literacy/                       수학 언어 트랙 L1~L7 (현 40_BaseDocs/00_literacy)
│   └── research/                       deep research (현 20_research)
│
├── grades/                           ── 학년별 산출물 (학습자가 보는 결과)
│   ├── middle/                         ── 중학 (현 50_units + apps/math1)
│   │   ├── math1/
│   │   │   ├── unit-01_소인수분해/
│   │   │   │   ├── index.html
│   │   │   │   ├── story.html
│   │   │   │   ├── concepts.html
│   │   │   │   ├── problems/
│   │   │   │   └── feedback/         (gitignore 가능)
│   │   │   └── unit-02~13/
│   │   ├── math2/                    (future)
│   │   └── math3/                    (future)
│   └── high/                           ── 고등 (현 70_HighSchool에서 통합)
│       └── math1/...
│
├── channel/                          ── 영상 소스 (콘텐츠 vs 산출물 위해 별도)
│   ├── season-1-ancient/
│   │   └── unit-01/...
│   └── ...
│
├── deploy/                           ── 배포 출력 (build 결과 — gitignore or 별도 branch)
│   ├── middle-school/                  → jwj-nick.github.io/mid1/math1
│   ├── high-school/                    → jwj-nick.github.io/highX/...
│   └── channel/                        → YouTube 업로드 큐
│
├── system/                           ── 메타 — 원칙·skill·진화 (현 mathtelling/system 그대로)
│   ├── principles/                     STORY_VIDEO_v1_5, APP_PRINCIPLES 등
│   ├── context/                        TONE_GUIDE, ERA_PALETTES, LEARNER_PROFILE 등
│   ├── skills/                         (SSOT) — sync-skills.sh로 .claude로 미러
│   ├── proposals/                      incubation
│   ├── insights/                       회고 누적
│   ├── workflows/                      다단계 절차
│   └── meta/                           VISION, ROADMAP, BLUEPRINTS (현 00_LearningSystem 일부)
│
├── project_hub/                      ── 대화·플랜 — 모든 의사결정 (현 00_project_hub)
│   ├── chatlog/
│   ├── plan/
│   └── history/
│
├── tools/                            ── 빌드·배포·sync 스크립트
│   ├── sync-skills.sh
│   ├── build-deploy.sh
│   └── ...
│
├── .claude/                          ── 스킬 미러 (system/skills/에서 sync)
│   └── skills/
│
├── CLAUDE.md                         ── 진입점
├── APP_PRINCIPLES.md                 ── (system/principles로 이동 검토)
├── README.md
└── .gitignore                        ── feedback/, _assets/*.png, *.mp3, *.mp4 등
```

### 1.2.3 "모듈 떼어쓰기" 시나리오

미래 다른 앱 (예: anthropic_skilljar_study, uvm-drill)이 이 repo의 일부를 가져다 쓰기:

| 모듈 | 방법 | 비고 |
|---|---|---|
| `packages/design-system` | npm 또는 git submodule | CSS 토큰만 |
| `packages/video-pipeline` | git submodule 또는 단순 cp | HyperFrames 템플릿 |
| `system/skills/*` | sync 스크립트 또는 cp | 다른 프로젝트도 .claude/skills에 미러 |
| `system/principles/*` | git submodule (read-only) | 공유 원칙 |

→ packages/는 **export 가능**, system/은 **참조 가능**. content/grades/는 이 repo 전속.

### 1.2.4 배포 분리 시나리오

```
[Source repo: math-story-telling]
        │
        ├─ build:middle  → deploy/middle-school/  → push to jwj-nick.github.io/mid1
        ├─ build:high    → deploy/high-school/    → push to jwj-nick.github.io/high1
        └─ build:channel → deploy/channel/        → YouTube upload queue
```

배포 repo는 별도 (jwj-nick.github.io/mid1 등 그대로), source repo에서 빌드 후 push.
현 `mid_eun` repo는 결국 source 역할 종료 → deploy/middle-school/로 대체.

---

## Round 1.3 — 마이그레이션 시 고려사항

### 1.3.1 git 히스토리 — 3 가지 선택지

| 옵션 | 방법 | 장점 | 단점 |
|---|---|---|---|
| **A. 깨끗 시작** | 새 repo init, 파일만 복사 | 단순. 폴더 구조 자유. | 히스토리 잃음. |
| **B. mathtelling 확장** | 현 mathtelling.git을 main으로, 다른 곳 파일 import | 5 commits 보존. 폴더는 mathtelling 따라감. | mid_eun의 풍부한 히스토리(68+ commits) 잃음. |
| **C. git subtree merge** | mathtelling.git에 mid_eun.git을 subtree로 merge | **양쪽 히스토리 보존**. | 복잡. 정리 필요. |

NCC 권고: **C** — 한 번만 하는 작업이고 양쪽 히스토리 가치 큼. 또는 **B + mid_eun을 archive로 fork**.

### 1.3.2 점진 vs 일괄

| 페이스 | 추천 |
|---|---|
| 일괄 (1세션) | 새 폴더 구조에 cp 일괄, git 새로. 빠름. |
| 점진 (단원별) | Unit 02 만들 때 새 위치에 작성, 기존은 그대로. 안전하지만 분산 지속. |

NCC 권고: **일괄** — 분산 상태가 가장 큰 문제. 빨리 끊자.

### 1.3.3 Public vs Private

| 자료 | 권장 |
|---|---|
| Source 코드, skill, principles, context | Public OK (OSS 가치) |
| 학습자(딸) 프로필, feedback, 사적 인용 | **private** — gitignore 또는 별도 private repo |
| 콘텐츠 (인물 사실, 단원 산출물) | Public OK (교육 공공재) |
| 영상 binary (mp4, mp3, png) | gitignore (이미 적용) |

→ 1 public repo + `.private/` gitignore 디렉토리 또는 별도 private submodule.

### 1.3.4 이름 후보

| 이름 | 느낌 | 비고 |
|---|---|---|
| `math-story-telling` | 정직, 영문, 검색 잘됨 | 길음 |
| `mathstory` | 짧음, 브랜드성 | 중복 ?  |
| `mathstory-kids` | 대상 명확 | 약간 캐주얼 |
| `storymath` | 어순 자연 | — |
| `mathtelling` (현재) | 이미 사용 중. monorepo 컨셉 | "telling" 어색? |
| (새 후보 Nick 제안) | — | — |

---

## Round 1.4 — Nick 결정 대기

### 핵심 4문항 (Round 1 결정)

- [ ] **D1. Repo 이름** — `math-story-telling` / `mathstory` / `mathtelling`(현재 유지) / 기타?
(Nick) math-story-telling 가 좋음. 단 이 내부 디렉토리들은 '##_' prefix 가 있으면 좋겠음. 이 파일을 _r2 로 다시 업데이트 하기 바람. round 1 nick's comment 는 원본 유지하기
- [ ] **D2. Git 히스토리 처리** — A 깨끗 시작 / B mathtelling 확장 / C subtree merge로 양쪽 보존?
(Nick) A - 단 다른 git repo 의 history 를 갖고와서 metadata 형태로 하나 보관해두면 어떨까? 어렵다면 양쪽 git history 확인을 휘해서는 그 repository들을 확인하라는 context 한 파일 남겨두기. project_hub/context/ 같은 디렉토리도 필요. '##_' prefix 는 필요  . archive directory 도 하나 필요
- [ ] **D3. 단일 repo vs packages/ 모듈 분리** — 1 repo 안에 packages 폴더로 모듈화 (권장) vs packages도 별 repo로?
(Nick) 권장에 따름
- [ ] **D4. 학년 처리** — `grades/middle/` `grades/high/` 한 repo (권장) vs 학년별 별 repo?
(Nick) 한 repo 아래 학년 구분 (현재 권장 좋음)

### 추가 질문 (Round 2 결정 보류 가능) <-- Round 1에서 처리

- [ ] D5. `00_LearningSystem`(메타 비전) — 새 repo `system/meta/`로 통합 vs 별도 유지?
(Nick) 통합해보면 좋겠음
- [ ] D6. 마이그레이션 페이스 — 일괄(권장) vs 점진?
(Nick) 일괄
- [ ] D7. 배포 — 현 `mid1` GH Pages repo 유지 (deploy 출력 push) vs deploy도 새 repo 안에 branch?
(Nick) deploy 일단은 현재 repo 유지함. (변경에 대해서는 나중에 자료가 더 정리되면 재논의... github.io 가 아닌 완전 다른 곳에서 서비스 하는 것 생각 중) --> 앞으로 많은 발전을 생각하고 있음. 계속 계속 함께 진화시켜나갑시다. 
- [ ] D8. 민감 자료 처리 — `.private/` gitignore vs private submodule vs 별 repo?
(Nick) .private/ gitignore

### NCC 통합 권고 (한 줄 요약)

> **새 repo `mathtelling` (현재 이름 유지) + subtree merge로 mid_eun 히스토리 흡수 + packages/grades/content/system 폴더 구조 + .private 게이트로 민감 자료 격리 + 일괄 마이그레이션 1세션.**

근거: ① 이름은 이미 mathtelling으로 굳어짐 (충분히 좋음). ② mid_eun 히스토리 가치 큼 (68 커밋, 13단원 작업). ③ packages는 같은 repo 안에 두는 게 sync 부담 적음. ④ 분산은 가능한 빨리 끊는 게 이득.

---

## 다음 단계

Round 1 D1~D4 답변 후:
- Round 2: 폴더 매핑 표 (현재 → 미래) 작성. 옮기는 파일 목록.
- Round 3: 마이그레이션 스크립트 (bash) 작성 + dry run.
- Round 4: 실행 + .gitignore + CLAUDE.md 재작성.

---

## 변경 이력

- R1 (2026-05-21): NCC 4-dir 진단, 미래 모습 제안, 결정 4문항 + 보류 4문항.
