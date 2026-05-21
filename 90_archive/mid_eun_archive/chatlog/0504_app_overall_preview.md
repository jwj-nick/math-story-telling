#  Round 1. 이 디렉토리 환경 잡기 (2026-05-04)

## 1. 참조 

### 현존 00_project_hub/plan, app, 20_research, 10_docs, 30_history, 50_stories, 60_her_writings/
모두 1차적으로 quick processing 한 내용.. 앞으로 할 작업의 기초 자료로 사용되길 원함. 충분한 맥락 파악 가능함. 그러나 그대로 따르는 것이 아니라 참조해서 제대로 셋업하는 것이 목표


### 다른 디렉토리의 참조 에이전트 스킬
필요하면 카피, 수정해서 여기서 사용 가능

../../70_HighSchool/2604_고1_중간고사/.claude/agents/
  app-reviewer.md
  math-error-workflow.md

../../70_HighSchool/2604_고1_중간고사/.claude/skills/ 
 figcrop/
 math-error-note/
 math-figure/
 math-practice/

## 2. 목표 : Setup
CLAUDE.md 를 재정리 하기 : 기존에는 단순 qna 로 임시로 만들어본 상황
.claude/ 내부 skill 등 셋팅 필요

중학교 1학년 딸에게 특화해서(감성적, 내성적, 수학 무관심) 각 단원의 컨셉을 명확하게 이해하고, 관심을 가질수 있도록하고, 수학의 언어를 이해하고, 문제 유형들에 익숙해지기. 기본 문제들은 시험 혹은 남들이 지켜보는 상황에서도 풀수있도록. 어려운 문제도 도전할 수 있는 자세를 갖도록. 

배우는 단원에 대해서 관련 수학자 혹은 생활 속에서 찾을 수 있는 것들, 에피소드 등을 찾아서 흥미 유발하는 스토리 텔링 (별도 앱 - 정적/동적, 동영상...) based on text script 

틀린 문제 뿐만 아니라 대표적인 문제들, 응용 문제들은 다른 디렉토리에서 작업한 오답노트관련 스킬/경험 체계를 잘 활용했으면 함. 

## 3. 진행
이 파일에서 대화 라운드 거듭하면서 할일/세부 목표 명확하게 하고 실제 액션 진행하기

---

# Round 2. 현황 파악 + 계획 수립을 위한 Q&A (Claude)

## 2-1. 현재 프로젝트에 뭐가 있는가 (팩트)

| 구분 | 위치 | 상태 |
|---|---|---|
| 기반 문서 (비전, 학습자 프로필, 컨셉, 수학언어 L1~L7) | `10_docs/`, `20_research/` | 04-26~28 작성, quick processing 수준 |
| Unit 1 시범 (에라토스테네스 + 소인수분해 5단계) | `50_stories/unit01`, `80_tools/unit01` | 이야기+인터랙티브+영상 완성. 딸 피드백 미수집 |
| L2 슬라이더 (`y=a/x` 인터랙티브) | `80_tools/L2-general-specific.html` | 완성 |
| 40_BaseDocs (13단원 × 개념 MD 뼈대) | `40_BaseDocs/01~13_*` | 이번 세션에 생성 (42파일) |
| .claude/ 스킬 | `.claude/commands/video-make.md` | video-make만 등록 |
| 오답노트/문제연습 체계 | 여기엔 없음. 고1 디렉토리에 참조 스킬 존재 | 미착수 |
| 딸 피드백/글 | `60_her-writings/` | 비어있음 |

## 2-2. Round 1 목표를 세분화하면 — 4개 축

| 축 | 무엇 | 산출물 형태 | 비고 |
|---|---|---|---|
| **A. 개념 이해** | 각 단원 핵심 개념을 명확히 | 40_BaseDocs (텍스트) + 인터랙티브 도구 | 뼈대 방금 완성 |
| **B. 흥미 유발** | 수학자 이야기, 생활 속 에피소드, 스토리텔링 | 이야기 텍스트 + 영상 + 앱 | 기존 "인물 서사" 축 |
| **C. 수학 언어** | 기호·표기·관습 자체를 메타 학습 | L1~L7 인터랙티브 도구 | 기존 축 2, L2만 시범 완성 |
| **D. 문제 연습** | 대표 문제, 오답노트, 유형 익숙해지기 | 스킬 기반 워크플로우 (고1 참조) | 미착수 |

## 2-3. 결정이 필요한 질문들

### Q1. 우선순위 재설정

기존: (a) 흥미·이해 > (c) AI 경험 > (b) 성적
Round 1에서: "기본 문제는 시험에서도 풀 수 있도록" → 실전력 비중 상승

**제안**: (a) 흥미·이해·자신감 > (b) 기본 문제 실전력 > (c) AI 경험
(c)는 딸이 관심 보일 때 자연스럽게. 우선은 a+b 집중)

→ 동의? 수정? 
(Nick) 내 이름은 Nick입니다. CLAUDE 가 그걸 알고있으면 됨
(Nick) 동의함.

### Q2. 4축 구조 동의 여부

위 A/B/C/D 4축이 맞는가? 빠진 것은? 과한 것은?
(Nick) 좋음

### Q3. 딸이 Unit 1을 써봤는가?

만든 결과물(이야기, 인터랙티브, 영상)을 딸이 실제로 사용해봤는지?
사용했다면 반응이 어땠는지가 이후 모든 방향의 핵심 입력.
(Nick) 안써봤음. 내가 5월에 준비를 하고 6월에 본격 작업 예정. 일단 chapter 1(소인수분해) ~ 4(일차방정식까지) 어느정도 자료를 완성한 후에 딸과 본격 수학공부 시작할 예정. 해당 챕터들 실제 내용 만드는데 나와 당신이 긴밀히 협의할 예정임. 초안 text 및 앱 형태 및 동영상 스크립트와 구성 등등 모두 체계적으로 정리할 예정임. (중요!!) claude / agent / skill 이 이 과정을 체계적으로 정리할 수 있도록 유도하고 규칙을 알아야 함. 

### Q4. 지금 이 세션의 스코프

이번 세션에서 할 것 = "Setup" 맞나?
- CLAUDE.md 재정리
- .claude/ 스킬 셋업
- 디렉토리 구조 확정
- (실제 콘텐츠 제작은 다음 세션부터)

(Nick) 동의함.

### Q5. 고1 스킬 중 가져올 것

고1 디렉토리의 스킬 중 어떤 것을 이쪽에 맞게 도입할지:
- `math-error-note/` — 오답노트 → D축 핵심
- `math-practice/` — 문제 연습 → D축
- `figcrop/` — 시험지 캡쳐 크롭 → 이미 등록됨
- `math-figure/` — 수학 도형 그리기 → 필요시
- `app-reviewer.md` — 앱 리뷰 에이전트 → 도구 품질관리
- `math-error-workflow.md` — 오답 워크플로우 에이전트 → D축 핵심

→ 어떤 것을 우선 도입?

(Nick) 우리가 할 일들을 체계적으로 정리하다 보면 자연스럽게 정리될 듯. 나는 모두다 쓸모있다고 생각하고 있기는 함.

---

# Round 3. 확정 사항 + 구체 실행 계획 (Claude)

## 3-1. 확정된 결정 사항

| # | 결정 | 내용 |
|---|---|---|
| D1 | 우선순위 | **(a) 흥미·이해·자신감 > (b) 기본 문제 실전력 > (c) AI 경험** |
| D2 | 4축 구조 | A.개념이해 / B.흥미유발 / C.수학언어 / D.문제연습 |
| D3 | 타임라인 | **5월: Ch1~4 자료 완성** → **6월: 딸과 본격 시작** |
| D4 | 작업 방식 | Nick과 Claude가 chatlog/ 파일에서 라운드 기반 협의. 초안 text → 앱 → 영상 모두 체계적 |
| D5 | 이번 세션 | Setup만 (CLAUDE.md + .claude/ 스킬 + 디렉토리 확정) |
| D6 | 고1 스킬 | 모두 유용. 작업 진행하며 자연스럽게 도입 |

## 3-2. 단원 파이프라인 — Ch 1개를 만드는 과정

Ch1~4를 5월에 만들려면, **1개 단원을 만드는 표준 워크플로우**가 있어야 합니다.

고1 스킬들을 읽고 중1에 맞게 재설계한 파이프라인:

```
[단원 N 제작 파이프라인]

Phase 1: 개념 (축 A)
  ├─ 40_BaseDocs/NN_단원명/ 검수·보완 (이미 뼈대 있음)
  └─ chatlog에서 Nick과 개념 범위·깊이 협의

Phase 2: 이야기 (축 B)
  ├─ 인물/에피소드 리서치
  ├─ 스토리 텍스트 초안 → Nick 리뷰 → 확정
  └─ 50_stories/unitNN/ 저장

Phase 3: 수학 언어 (축 C, 해당 단원에 맞는 L모듈)
  ├─ 어떤 L모듈이 이 단원과 연결되는지 결정
  └─ 인터랙티브 도구 제작 → 80_tools/

Phase 4: 도구 (축 A+B 통합)
  ├─ 인터랙티브 HTML 앱 (개념 탐구용)
  ├─ 영상 스크립트 → /video-make
  └─ 80_tools/unitNN/, 90_video/unitNN/

Phase 5: 문제 연습 (축 D)
  ├─ 대표 문제 선정 (교과서/문제집 기반)
  ├─ 오답노트 체계 (고1 math-error-note 중1 적응)
  └─ 70_problems/unitNN/
```

## 3-3. 이번 세션 Setup 실행 계획

### Action 1: CLAUDE.md 재작성

현재 CLAUDE.md는 04-28 기준 임시판. 아래 구조로 전면 재작성:

```
1. 프로젝트 한 줄
2. 확정 우선순위 (D1)
3. 4축 구조 (D2)
4. 작업 방식 — chatlog 라운드 기반 협의
5. 디렉토리 구조 (현재 실제 상태 반영)
6. 단원 파이프라인 (3-2)
7. 등록된 Skills/Agents 목록
8. 절대 원칙
9. 기술 스택
```

### Action 2: .claude/ 스킬·에이전트 셋업

고1에서 가져와 중1에 맞게 조정할 것:

| 원본 (고1) | 중1 적응 | 변경 포인트 |
|---|---|---|
| `math-error-note` | `/math-error-note` | 과목 → 중1수학, 디렉토리 → 70_problems/, 7섹션 포맷 유지 |
| `math-practice` | `/math-practice` | 범위 → 중1, L/M/H 3×3 구조 유지 |
| `math-figure` | `/math-figure` | JSXGraph+SVG 그대로, 중1 도형 단원 특화 |
| `app-reviewer` | `app-reviewer` agent | APP_PRINCIPLES 중1 버전 작성 필요 |
| `math-error-workflow` | `math-workflow` agent | 중1용 전체 오답 파이프라인 |

새로 만들 것:

| 스킬/에이전트 | 용도 |
|---|---|
| `/story-write` | 축 B: 인물 서사 초안 생성 (리서치 → 텍스트 → Nick 리뷰) |
| `/concept-review` | 축 A: 40_BaseDocs 개념 MD 검수·보완 |
| `/unit-plan` | 단원 파이프라인 킥오프 (chatlog 파일 생성 + Phase 1~5 체크리스트) |
| `figcrop` | 이미 등록됨, 그대로 유지 |
| `video-make` | 이미 등록됨, 그대로 유지 |

### Action 3: 디렉토리 구조 확정

현재 실제 존재하는 구조 + 확정할 구조:

```
260426_MathTelling_Idea/
├── CLAUDE.md
├── 00_GUIDE.md
├── 01_README.md
├── 00_project_hub/
│   ├── chatlog/          ← 라운드 기반 대화 (핵심 작업 방식)
│   └── plan/             ← current-plan.md
├── 10_docs/              ← 핵심 문서
├── 20_research/          ← 리서치
├── 30_history/           ← 의사결정 기록
├── 40_BaseDocs/          ← 13단원 개념 뼈대 (신규, 완성)
│   ├── 01_소인수분해/
│   ├── ...
│   └── 13_자료의정리와해석/
├── 50_stories/           ← 인물 서사 (축 B)
├── 60_her-writings/      ← 딸이 쓴 글 (수정 금지)
├── 70_problems/          ← 문제·오답노트 (축 D) ← 신규 확정
├── 80_tools/             ← 인터랙티브 HTML 앱
├── 90_video/             ← 영상
└── 70_dev_study/         ← 개발 학습 노트 (기존 유지)
```

## 3-4. 질문

### Q6. 위 3개 Action의 실행 순서

제안: Action 1 (CLAUDE.md) → Action 3 (디렉토리) → Action 2 (스킬)
CLAUDE.md가 잡혀야 스킬 작성 시 참조할 수 있으므로.

→ 이 순서로 바로 진행해도 되나요?
(Nick) Yes

### Q7. APP_PRINCIPLES.md

고1에는 `APP_PRINCIPLES.md`가 있어서 모든 HTML 앱의 디자인 원칙을 통일했습니다. 중1에도 비슷한 파일이 필요합니다. 위치를 `10_docs/` 아래에 두면 될까요?
(Nick) CLAUDE.md 옆에 두면 좋겠음

### Q8. 70_problems/ 와 기존 50_stories/unit01 내 문제

Unit 1에는 이미 `50_stories/unit01/unit01.md` 안에 문제가 포함되어 있습니다. 앞으로는 문제를 `70_problems/`로 분리할 건지, 아니면 story 안에 통합 유지할 건지?

**제안**: 분리. `50_stories/` = 이야기+개념, `70_problems/` = 문제+오답. 역할이 명확해집니다.

(Nick) 분리 동의. 다만 기존 70_dev_study 는 다른 prefix로...  01_dev_study 가 좋음... dev_study, app 개발, 영상 제작 등은 이 과정을 통해서 일단 내가 배우고 싶은것임...  30_history 는 부적절할 수 있음. 00_project_hub 아래의 sub directory 로 옮기는건 어떨지?

→ Nick, Q6~Q8 의견 주시면 바로 실행합니다.

---

# Round 4. 확정 + 실행 (Claude)

## 4-1. Q6~Q8 반영 결과

| 결정 | 내용 |
|---|---|
| Q6 | Action 1→3→2 순서 확정 |
| Q7 | `APP_PRINCIPLES.md` → 프로젝트 루트 (CLAUDE.md 옆) |
| Q8 | 문제 분리 동의 |
| 추가 | `70_dev_study/` → `01_dev_study/` (Nick의 개발 학습용) |
| 추가 | `30_history/` → `00_project_hub/history/` (프로젝트 허브 하위로) |

## 4-2. 확정 디렉토리 구조

```
260426_MathTelling_Idea/
├── CLAUDE.md                     ← Claude 진입점
├── APP_PRINCIPLES.md             ← HTML 앱 디자인 원칙 (신규)
├── 00_GUIDE.md
├── 01_README.md
├── 00_project_hub/
│   ├── chatlog/                  ← 라운드 기반 대화
│   ├── plan/                     ← current-plan.md
│   └── history/                  ← 의사결정 기록 (30_history에서 이동)
├── 01_dev_study/                 ← Nick의 개발 학습 (70_dev_study에서 이동)
├── 10_docs/                      ← 핵심 문서
├── 20_research/                  ← 리서치
├── 40_BaseDocs/                  ← 13단원 개념 뼈대
├── 50_stories/                   ← 인물 서사 (축 B)
├── 60_her-writings/              ← 딸이 쓴 글 (수정 금지)
├── 70_problems/                  ← 문제·오답노트 (축 D)
├── 80_tools/                     ← 인터랙티브 HTML 앱
└── 90_video/                     ← 영상
```

## 4-3. 실행 시작

아래 순서로 즉시 실행합니다:
1. 디렉토리 이동 (`30_history` → `00_project_hub/history`, `70_dev_study` → `01_dev_study`)
2. `70_problems/` 생성
3. CLAUDE.md 전면 재작성
4. APP_PRINCIPLES.md 초안 작성
5. .claude/ 스킬·에이전트 셋업

---

# Round 4 실행 결과 (Claude)

## 완료 항목

### Action 1: CLAUDE.md 전면 재작성
- 우선순위 (a)>(b)>(c), 4축 구조, chatlog 대화 방식, 단원 파이프라인, 스킬/에이전트 목록 모두 반영

### Action 3: 디렉토리 구조 확정
- `30_history/` → `00_project_hub/history/` 이동 완료
- `70_dev_study/` → `01_dev_study/` 이름 변경 완료
- `70_problems/` 생성 완료

### Action 2: .claude/ 스킬·에이전트 셋업

**스킬 6개:**
| 스킬 | 파일 | 용도 |
|---|---|---|
| `/math-error-note` | `.claude/skills/math-error-note/SKILL.md` | 오답노트 생성 (7섹션 MD + HTML) |
| `/math-practice` | `.claude/skills/math-practice/SKILL.md` | 연습 문제 L/M/H x 3 |
| `/math-figure` | `.claude/skills/math-figure/SKILL.md` | 그래프 렌더링 (SVG + JSXGraph) |
| `/story-write` | `.claude/skills/story-write/SKILL.md` | 인물 서사 초안 생성 |
| `/concept-review` | `.claude/skills/concept-review/SKILL.md` | 40_BaseDocs 개념 검수 |
| `/unit-plan` | `.claude/skills/unit-plan/SKILL.md` | 단원 파이프라인 킥오프 |

**에이전트 2개:**
| 에이전트 | 파일 | 용도 |
|---|---|---|
| `app-reviewer` | `.claude/agents/app-reviewer.md` | HTML 앱 품질 검토 |
| `math-workflow` | `.claude/agents/math-workflow.md` | 오답노트 전체 워크플로우 자동화 |

**기존 유지:**
| 스킬 | 파일 | 용도 |
|---|---|---|
| `/video-make` | `.claude/commands/video-make.md` | 영상 제작 |
| `/figcrop` | (global skill) | 시험지 캡쳐 크롭 |

### 추가: APP_PRINCIPLES.md 작성
- 프로젝트 루트에 생성 (CLAUDE.md 옆)
- 고1 버전을 기반으로 중1 특화 (개념 탐구 앱, 스토리 앱 원칙 추가)

---

## 이번 세션 Setup 완료 상태

| 항목 | 상태 |
|---|---|
| CLAUDE.md 재정리 | 완료 |
| .claude/ 스킬 셋업 | 완료 (6 skills + 2 agents) |
| 디렉토리 구조 확정 | 완료 |
| APP_PRINCIPLES.md | 완료 |
| 40_BaseDocs 뼈대 | 완료 (42 files, 13 dirs) |

## 다음 세션 제안

Setup이 끝났으니, 다음 세션부터 실제 콘텐츠 제작 시작.
`/unit-plan unit01 소인수분해`로 킥오프하여 기존 Unit 1 재정비부터 하거나,
새로운 chatlog 파일에서 Ch1~4 전체 제작 순서를 먼저 잡을 수 있습니다.

→ Nick, 다음 세션에서 어떤 것부터 할지 결정해주세요.

---

# Round 5. 디렉토리 재구조화 — 단원 중심 통합 (Nick 제안 + Claude 정리)

## 5-1. Nick의 문제 제기

- 80_tools에 문제 앱이 들어가 있는데 70_problems와 겹침
- 50/60/70/80/90이 따로 있으면 같은 단원의 자료가 5곳에 흩어짐
- **제안**: 큰 디렉토리 하나에 단원별 디렉토리, 그 안에 스토리/앱/영상/피드백 모두 포함

## 5-2. 제안 구조

```
260426_MathTelling_Idea/
├── CLAUDE.md
├── APP_PRINCIPLES.md
├── 00_GUIDE.md
├── 01_README.md
├── 00_project_hub/
│   ├── chatlog/
│   ├── plan/
│   └── history/
├── 01_dev_study/                 ← Nick의 개발 학습
├── 10_docs/                      ← 핵심 문서 (학습자 프로필, 컨셉 등)
├── 20_research/                  ← 리서치
├── 40_BaseDocs/                  ← 13단원 개념 뼈대 (참조 자료)
│   ├── 01_소인수분해/
│   └── ...
│
├── 50_units/                     ← ★ 단원별 통합 작업 디렉토리 ★
│   ├── unit01_소인수분해/
│   │   ├── story/               ← 인물 서사 텍스트
│   │   ├── app/                 ← 인터랙티브 HTML 앱 (개념 탐구 + 문제)
│   │   ├── video/               ← 영상 (스크립트 + mp4)
│   │   ├── problems/            ← 문제·오답노트 MD
│   │   └── feedback/            ← 딸의 글·피드백·반응
│   ├── unit02_정수와유리수/
│   │   └── (동일 구조)
│   ├── unit03_문자와식/
│   ├── unit04_일차방정식/
│   └── ...
│
└── 80_literacy/                  ← 수학 언어 트랙 (단원 횡단, 축 C)
    ├── L1_문자의정체/
    ├── L2_일반형과구체형/
    └── ...
```

## 5-3. 핵심 변경점

| 기존 | 변경 후 | 이유 |
|---|---|---|
| `50_stories/unitNN/` | `50_units/unitNN/story/` | 단원 안에 통합 |
| `60_her-writings/unitNN/` | `50_units/unitNN/feedback/` | 단원 안에 통합 |
| `70_problems/unitNN/` | `50_units/unitNN/problems/` | 단원 안에 통합 |
| `80_tools/unitNN/` | `50_units/unitNN/app/` | 단원 안에 통합 |
| `90_video/unitNN/` | `50_units/unitNN/video/` | 단원 안에 통합 |
| `80_tools/L2-*.html` | `80_literacy/L2_*/` | 수학 언어는 단원 횡단이므로 별도 유지 |

## 5-4. 왜 이게 낫나

1. **하나의 단원 = 하나의 폴더** — 작업할 때 한 곳만 보면 됨
2. 50/60/70/80/90 5곳 왔다갔다 안 해도 됨
3. 40_BaseDocs는 **참조 자료**(불변), 50_units는 **작업 산출물**(발전)로 역할 분리 명확
4. 수학 언어(축 C)는 단원 횡단이므로 80_literacy로 별도 유지

## 5-5. 질문

### Q9. 이 구조 동의?

특히:
- `50_units` 이름 괜찮은지 (다른 후보: `50_curriculum`, `50_chapters`)
- `80_literacy` 위치 괜찮은지
- `feedback/` 이름 (vs `her-writings/`, `response/`)

(Nick) 50_units 동의. 그러나 'unit01_소인수분해/' 는 '01_소인수분해/' 로 수정바람
80_literacy/ 는 40_BaseDocs/ 내부로 가면 좋을듯. 그러면 40_BaseDocs/는 전체 단원을 아우르는 기본 사항들과 단원 specific docs 로 구성하도록...

### Q10. 기존 파일 마이그레이션

이미 있는 파일:
- `50_stories/unit01_소인수분해/unit01.md`
- `80_tools/unit01_소인수분해/*.html`
- `80_tools/L2-general-specific.html`
- `90_video/unit01_소인수분해/sieve-video/*`
- `60_her-writings/unit01_소인수분해/README.md`

→ 새 구조로 이동해도 되나요?
(Nick) 당연히 이동바람

→ Nick, Q9~Q10 의견 주세요.

---

# Round 6. 디렉토리 재구조화 실행 (Claude)

## 6-1. 확정 구조

```
260426_MathTelling_Idea/
├── CLAUDE.md
├── APP_PRINCIPLES.md
├── 00_GUIDE.md
├── 01_README.md
├── 00_project_hub/
│   ├── chatlog/
│   ├── plan/
│   └── history/
├── 01_dev_study/
├── 10_docs/
├── 20_research/
├── 40_BaseDocs/                  ← 전체 기본 자료
│   ├── 00_literacy/              ← 수학 언어 트랙 (단원 횡단, 축 C)
│   │   ├── L1_문자의정체/
│   │   ├── L2_일반형과구체형/
│   │   └── ...
│   ├── 01_소인수분해/            ← 단원별 개념 MD
│   ├── 02_정수와유리수/
│   └── ...
├── 50_units/                     ← 단원별 통합 작업 디렉토리
│   ├── 01_소인수분해/
│   │   ├── story/
│   │   ├── app/
│   │   ├── video/
│   │   ├── problems/
│   │   └── feedback/
│   ├── 02_정수와유리수/
│   ├── 03_문자와식/
│   ├── 04_일차방정식/
│   └── ...
```

Nick 피드백 반영:
- `unit01_소인수분해` → `01_소인수분해` (unit 접두어 제거)
- `80_literacy/` → `40_BaseDocs/00_literacy/` (기본 자료 안으로 통합)

## 6-2. 실행 (완료 — 2026-05-09)

### 파일 마이그레이션

| 원본 | 이동 후 |
|---|---|
| `50_stories/unit01_소인수분해/unit01.md` | `50_units/01_소인수분해/story/unit01.md` |
| `80_tools/unit01_소인수분해/*.html`, `*.css` | `50_units/01_소인수분해/app/` |
| `80_tools/L2-general-specific.html` | `40_BaseDocs/00_literacy/L2_일반형과구체형/` |
| `90_video/unit01_소인수분해/sieve-video/*` | `50_units/01_소인수분해/video/sieve-video/` |
| `60_her-writings/unit01_소인수분해/README.md` | `50_units/01_소인수분해/feedback/README.md` |
| `90_video/VIDEO-PIPELINE-GUIDE.md` | `01_dev_study/VIDEO-PIPELINE-GUIDE.md` |

### 구 디렉토리 삭제

`50_stories/`, `60_her-writings/`, `70_problems/`, `80_tools/`, `90_video/` — 모두 삭제 완료

### 문서 업데이트

| 파일 | 변경 내용 |
|---|---|
| `CLAUDE.md` | 4축 산출물 위치, 파이프라인, 디렉토리 구조 — 새 경로로 전면 수정 |
| `00_GUIDE.md` | 디렉토리 구조, 현황 — 새 경로 반영 |
| `.claude/skills/story-write/SKILL.md` | 저장 경로 수정 |
| `.claude/skills/math-error-note/SKILL.md` | 저장 경로 수정 |
| `.claude/skills/math-practice/SKILL.md` | 저장 경로 수정 |
| `.claude/skills/unit-plan/SKILL.md` | 파이프라인 경로 전면 수정 |

### 최종 구조

```
260426_MathTelling_Idea/
├── CLAUDE.md / APP_PRINCIPLES.md / 00_GUIDE.md / 01_README.md
├── 00_project_hub/  chatlog/ / plan/ / history/
├── 01_dev_study/
├── 10_docs/
├── 20_research/
├── 40_BaseDocs/
│   ├── 00_literacy/L2_일반형과구체형/
│   └── 01_소인수분해/ ~ 13_*/
└── 50_units/
    └── 01_소인수분해/
        ├── story/unit01.md
        ├── app/index.html, concepts.html, problems.html, sieve.html, shared.css
        ├── video/sieve-video/
        ├── problems/  (비어있음 — 추후 오답노트)
        └── feedback/README.md
```

## 6-3. Setup 전체 완료

| 항목 | 상태 |
|---|---|
| CLAUDE.md 재작성 | 완료 |
| APP_PRINCIPLES.md | 완료 |
| .claude/ 스킬 6개 + 에이전트 2개 | 완료 |
| 40_BaseDocs/ 13단원 x 42 MD | 완료 |
| 50_units/ 단원 통합 구조 | 완료 |
| Unit 1 파일 마이그레이션 | 완료 |

## 다음 단계 제안

Setup 완료. 이제 실제 콘텐츠 제작 시작 가능.

1. **Unit 1 재정비**: 기존 story/app을 새 구조에서 검수·보완 (개념 검수 → 스토리 리뷰 → 앱 품질 확인)
2. **Unit 2 착수**: `/unit-plan unit02 정수와유리수` 로 킥오프

→ Nick, 다음에 무엇부터 할지 결정해주세요.
(Nick) 0508 - unit1 재정비 바람