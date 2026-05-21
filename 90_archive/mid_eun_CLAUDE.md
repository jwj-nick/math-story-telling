# CLAUDE.md — MathTelling Project

> 새 Claude 세션이 시작되면 이 파일을 먼저 읽는다.

## 프로젝트 한 줄

중1 딸을 위해 중1 수학 단원을 **인물 이야기 + 수학 언어 메타 학습 + 인터랙티브 도구 + 문제 연습**으로 체계적으로 구성하는 학습 시스템.

---

## 우선순위 (확정)

1. **(a) 흥미 + 이해 + 자신감** ← 최우선
2. **(b) 기본 문제 실전력** ← 시험에서 기본 문제는 풀 수 있도록
3. **(c) AI로 직접 만드는 경험** ← 딸이 관심 보일 때 자연스럽게

---

## 4축 구조

| 축 | 무엇 | 산출물 위치 |
|---|---|---|
| **A. 개념 이해** | 각 단원 핵심 개념 명확히 | `40_BaseDocs/`, `50_units/NN/{index,story,concepts}.html` |
| **B. 흥미 유발** | 수학자 이야기, 생활 속 에피소드, 스토리텔링 | `50_units/NN/story/`, `50_units/NN/video/` |
| **C. 수학 언어** | 기호·표기·관습 자체의 메타 학습 (L1~L7) | `40_BaseDocs/00_literacy/`, `10_docs/03_literacy-track.md` |
| **D. 문제 연습** | 대표 문제, 오답노트, 유형 익숙해지기 | `50_units/NN/problems/` |

---

## 작업 방식 — chatlog 라운드 기반

**핵심 원칙: Nick이 `00_project_hub/chatlog/` 파일을 제시하면, 그 파일 안에서 라운드를 거듭하며 대화한다.**

- 모든 논의·결정·Q&A는 해당 파일에 `# Round N` 형태로 기록
- Claude는 파일을 읽고, 다음 라운드를 파일에 직접 append
- 화면 출력은 최소한의 요약만. **본문은 파일에 쓴다.**
- Nick이 파일에 `(Nick)` 태그로 답변 → Claude가 다시 다음 라운드 추가

### chatlog 파일 관행

- **파일명 주석**: 파일 맨 앞 첫 줄에 `<!-- 파일명 -->` HTML 주석 (copy/paste 편의)
- **NCC**: Nick's Claude Code Co-worker = Claude. 이 프로젝트에서 AI 파트너 호칭.
- **세션 파일 없을 때**: NCC가 `YYMMDD_주제.md` 형식으로 새 파일 생성 → chat window에서 파일명 명확히 언급
- **세션 시작 시**: NCC는 항상 현재 작업 chatlog 파일명을 chat window에 밝힌다

---

## 단원 파이프라인 — 1개 단원 제작 과정

> **착수 방법**: Nick이 "unit 02 만들어"라고 한 줄 의뢰 → `se_agent_unit_orchestrator`가 Commission Brief(chatlog Round 0)를 자동 생성 → Nick이 확인 → 자율 실행.
> **HITL 없음**: NCC가 전 과정 자율 진행. 각 Phase 완료 시 chatlog 기록으로 진행 상황 투명하게 유지.
> 상세 명세: `10_docs/14_workflow_v4.md`

```
Phase 0: 디렉토리 초기화
  └─ /se_unit_plan → 50_units/NN/ 구조 생성

Phase 1: 개념 (축 A)
  ├─ 40_BaseDocs/NN_단원명/ 검수·보완 → /se_concept_review
  └─ audit: /se_ncc_audit_concept

Phase 3 체크 (비동기, 단원 파이프라인과 독립):
  └─ 수학 언어 업데이트 필요 여부 판단 → /se_math_figure → 40_BaseDocs/00_literacy/

Phase 2: 이야기 (축 B)
  ├─ 인물 리서치 + 스토리 초안 → /se_story_write
  └─ audit: /se_ncc_audit_story

Phase 4: 앱 (축 A+B 통합)
  ├─ HTML 앱 제작: index.html, story.html, concepts.html
  └─ audit: /se_ncc_audit_app

Phase 5-a: 기본문제
  ├─ 단원 전체 개념 커버 기본문제 (8~10개)
  └─ → problems/basic_app.html / audit: /se_ncc_audit_math + /se_ncc_audit_app

Phase 5-b: 유형 목록
  ├─ 시험 유형 목록 확정
  └─ → problems/types.md / audit: /se_ncc_audit_problem

Phase 5-c: 유형별 연습 (3/3/3 원칙)
  ├─ /se_math_practice → 유형별 L×3 + M×3 + H×3
  └─ → problems/type_NN_app.html / audit: /se_ncc_audit_math + /se_ncc_audit_app

Phase 5-d: 유형별 깊이 탐구 자료 (제작 파이프라인의 일부)
  ├─ M+ 난이도 유형마다 /se_type_explorer 호출 (L만 있는 유형 skip)
  └─ → problems/deep_유형명_app.html / audit: /se_ncc_audit_math + /se_ncc_audit_app
```

---

## 디렉토리 구조

```
260426_MathTelling_Idea/
├── CLAUDE.md                     ← Claude 진입점
├── APP_PRINCIPLES.md             ← HTML 앱 디자인 원칙
├── 00_GUIDE.md                   ← 폴더 사용 설명서
├── 01_README.md                  ← 비전·구조
├── 00_project_hub/
│   ├── chatlog/                  ← 라운드 기반 대화 (핵심 작업 방식)
│   ├── plan/                     ← current-plan.md
│   └── history/                  ← 의사결정 기록
├── 01_dev_study/                 ← Nick의 개발 학습 (앱, 영상 제작 등)
├── 10_docs/                      ← 핵심 문서 (학습자 프로필, 컨셉, 수학 언어 트랙)
├── 20_research/                  ← Deep research 결과
├── 40_BaseDocs/                  ← 13단원 개념 뼈대 + 수학 언어 (참조 자료)
│   ├── 00_literacy/              ← 수학 언어 트랙 L1~L7 (단원 횡단, 축 C)
│   │   └── L2_일반형과구체형/
│   ├── 01_소인수분해/
│   └── ... (13단원)
└── 50_units/                     ← 단원별 통합 작업 디렉토리
    ├── 01_소인수분해/
    │   ├── index.html           ← 단원 허브 (축 A+B 통합) ⭐
    │   ├── story.html           ← 인물 서사 인터랙티브
    │   ├── concepts.html        ← 개념 탐구 인터랙티브
    │   ├── story/               ← 인물 서사 텍스트 .md (축 B)
    │   ├── video/               ← 영상 (스크립트 + mp4)
    │   ├── problems/            ← 문제·오답노트 (축 D) — basic, type_*, deep_*
    │   └── feedback/            ← 딸의 글·피드백·반응 (수정 금지)
    └── 02~13_*/                 ← 동일 구조
```

---

## 절대 원칙

1. **우선순위 순서**: (a) 흥미·이해 > (b) 실전력 > (c) AI 경험
2. **페이스**: 단원 1개 = 2~3주. 진도보다 깊이.
3. **딸의 글 (`50_units/NN/feedback/`)은 임의 수정 금지.** 피드백은 별도 파일로.
4. **4축 모두 운영**: 한 축만 하면 불완전.
5. **빈칸·미완성을 의도적으로 남겨라.** 딸이 채울 자리가 있어야 한다.
6. **chatlog/ 파일 기반 대화.** 주요 결정은 반드시 파일에 기록.
7. **시간·토큰 효율**: 재읽기·재감사 사이클 금지. audit 1-shot 원칙. 자세한 규칙은 `.claude/agents/unit-orchestrator.md` "시간·토큰 효율 원칙" 섹션 참조.
8. **Rate limit 인식**: Anthropic API 5시간 sliding window. 단원 orchestrator 호출 전 잔량 충분한지 확인. 의심 시 Nick에게 확인 요청.

---

## 학습 대상 (딸)

- 중1, 감성적·내성적, 국어/영어 강세, 수학 중하위
- "수학도 잘하고 싶은데 너무 어려움" (내적 동기 존재)
- 결정적 사례: `y=a/x, a=-2` 일 때 `y=-2/x` 로 변환 못함 → 축 C 발견 계기
- 상세: `10_docs/01_learner-profile.md`

---

## 타임라인

- **2026-05 (현재)**: Ch1(소인수분해) ~ Ch4(일차방정식) 자료 완성
- **2026-06~**: 딸과 본격 수학 공부 시작

---

## 등록된 Skills (Slash Commands)

### 제작 Skills
| 명령 | Phase | 용도 |
|---|---|---|
| `/se_unit_plan` | 0 | 단원 디렉토리 초기화 |
| `/se_concept_review` | 1 | 40_BaseDocs 개념 MD 검수·보완 |
| `/se_story_write` | 2 | 인물 서사 초안 생성 |
| `/se_math_figure` | 3, 5 | 수학 그래프 네이티브 렌더링 (SVG + JSXGraph) |
| `/se_math_practice` | 5c | 유형별 연습 문제 생성 (L/M/H 3×3) |
| `/se_math_error_note` | 5 in-loop | 오답노트 생성 (7섹션 MD + HTML 앱) |
| `/se_video_make` | 4 | 영상 제작 파이프라인 (TTS → GSAP → FFmpeg) |
| `/figcrop` | 5 | 시험지 캡쳐에서 그림 크롭 |

### NCC Audit Skills
| 명령 | 대상 | 기준 문서 |
|---|---|---|
| `/se_ncc_audit_app` | HTML 앱 품질 | APP_PRINCIPLES.md |
| `/se_ncc_audit_math` | 수학 정확성 (Wolfram 보조) | 중1 교육과정 |
| `/se_ncc_audit_concept` | 개념 수준·범위 | learner-profile.md |
| `/se_ncc_audit_problem` | 문제 커버리지·난이도 | 문제 출제 원칙 |
| `/se_ncc_audit_story` | 스토리 적합성 + 피드백 분석 | learner-profile.md |

## 등록된 Agents

| 에이전트 | 용도 |
|---|---|
| `se_agent_unit_orchestrator` | **단일 Orchestrator** — 단원 전체 파이프라인 (Phase 0~5c) |
| `se_type_explorer` | **Skill** — 유형별 깊이 탐구 자료 생성 (Phase 5-d, 제작 파이프라인 내) |

---

## 기술 스택

- Claude Code + Local Markdown
- 인터랙티브 도구: HTML+JS (바닐라, 빌드 없음), KaTeX, JSXGraph
- 영상: HyperFrames (GSAP) → FFmpeg, edge-tts (한국어 TTS)
- 앱 디자인: `APP_PRINCIPLES.md` 준수

---

## 참고: 단원별 인물 배정

| 단원 | 개념 | 인물 |
|---|---|---|
| 1 | 소인수분해 | 에라토스테네스 |
| 2 | 정수·유리수 | 브라마굽타 |
| 3 | 문자·식 | 알콰리즈미 |
| 4 | 일차방정식 | 디오판토스 |
| 5~6 | 좌표·함수 | 데카르트 |

## 참고 문서

| 파일 | 내용 |
|---|---|
| `10_docs/01_learner-profile.md` | 학습자 프로필 상세 |
| `10_docs/02_concept.md` | 인물 서사 5단계 흐름 |
| `10_docs/03_literacy-track.md` | 수학 언어 트랙 L1~L7 |
| `10_docs/14_workflow_v4.md` | **현행 워크플로우 확정판** |
| `10_docs/15_wolfram_alpha_guide.md` | Wolfram Alpha MCP 설정 가이드 |
| `10_docs/20_guide_engineer.md` | 엔지니어 관점 가이드 |
| `10_docs/21_guide_teacher.md` | 수학선생님 관점 가이드 |
| `10_docs/22_guide_student.md` | 딸(학생) 가이드 |
| `20_research/01_R1-curriculum-map.md` | 교육과정 매핑 |
| `20_research/02_R2-people-map.md` | 인물 지도 |
