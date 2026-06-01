# CLAUDE.md — math-story-telling

> 새 Claude 세션이 시작되면 이 파일을 먼저 읽는다.

## 프로젝트 한 줄

수학 단원을 **인물 이야기 + 수학 언어 메타 학습 + 인터랙티브 도구 + 문제 연습**으로 구성하는 학습 시스템.
중학교 1학년부터 시작, 학년·과목 확장 가능. 시스템 일부 (`20_packages/`)는 다른 학습 앱에도 재사용 가능.

---

## 우선순위 (확정)

1. **(a) 흥미 + 이해 + 자신감** ← 최우선
2. **(b) 기본 문제 실전력** ← 시험에서 기본 문제는 풀 수 있도록
3. **(c) AI로 직접 만드는 경험** ← 딸이 관심 보일 때 자연스럽게

---

## 4축 구조

| 축 | 무엇 | 위치 |
|---|---|---|
| **A. 개념 이해** | 각 단원 핵심 개념 명확히 | `30_content/concepts/`, `40_grades/middle/math1/NN_단원명/{index,story,concepts}.html` |
| **B. 흥미 유발** | 수학자 이야기, 영상, 스토리텔링 | `30_content/people/`, `50_channel/`, `40_grades/middle/math1/NN_단원명/{story.html, story/, video/}` |
| **C. 수학 언어** | 기호·표기 메타 학습 (L1~L7) | `30_content/literacy/` |
| **D. 문제 연습** | 대표 문제, 오답노트, 유형 익히기 | `40_grades/middle/math1/NN_단원명/problems/` |

---

## 디렉토리 인덱스 (##_ prefix)

```
math-story-telling/
├── 00_project_hub/        대화·플랜·의사결정 메타데이터
│   ├── 10_chatlog/          라운드 기반 대화 (작업 방식의 핵심)
│   ├── 20_plan/             확정 플랜·current-plan
│   ├── 30_history/          의사결정 기록·Nick_TODO
│   └── 40_context/          ⭐ 외부 repo 참조 메타
├── 10_system/             원칙·skill·진화 메커니즘
│   ├── 10_principles/       APP_PRINCIPLES, STORY_VIDEO_v1_5 등 SSOT
│   ├── 20_context/          LEARNER_PROFILE, TONE_GUIDE, ERA_PALETTES
│   ├── 30_skills/           ⭐ Claude Code skill SSOT (22개, 전부 kebab)
│   ├── 35_agents/           ⭐ agent SSOT
│   ├── 40_proposals/        incubation (chatlog → proposals → skills)
│   ├── 50_insights/         회고 누적
│   ├── 60_workflows/        다단계 절차
│   └── 70_meta/             concept.md(서사 5단계)·LEARNERS·BLUEPRINTS 등. (VISION/MASTER_PLAN/ROADMAP = 폐기→90_archive/70_meta_legacy/)
├── 11_video_gen_process/  ⭐ 영상 제작 시스템 구축 (목적: `00_charter/PURPOSE.md` / 계획: `00_charter/INTEGRATED_PLAN.md`). 영상 양산 X, 시스템 구축.
├── 20_packages/           떼서 다른 앱에 쓸 모듈
│   ├── design-system/       CSS 토큰 4종 + subjects/math + dist
│   └── video-pipeline/      (future)
├── 30_content/            학년·매체 무관 SSOT
│   ├── people/              인물 사실
│   ├── concepts/            단원별 개념 뼈대 (구 40_BaseDocs)
│   ├── literacy/            수학 언어 트랙 L0/L2/…
│   ├── research/            deep research
│   └── units/               단원 메타 (meta.json)
├── 40_grades/             학년별 산출물
│   └── middle/math1/        13단원 (구 50_units) + apps/math1 머지
├── 50_channel/            영상 소스
│   ├── season-1-ancient/
│   ├── _templates/ _docs/ _assets/
│   └── _archive/v1/         구 90_video
├── 60_deploy/             빌드 출력 (gitignore)
├── 70_tools/              sync-skills.sh 등
├── 90_archive/            ⭐ 옛 자료 안전망 백업
├── .claude/skills/        ← 10_system/30_skills/ 미러 (sync-skills.sh)
├── .claude/agents/        ← 10_system/35_agents/ 미러
└── .private/              ⭐ gitignore — feedback, learner_personal 등
```

---

## 작업 방식 — chatlog 라운드 기반

**핵심 원칙: Nick이 `00_project_hub/10_chatlog/` 파일을 제시하면, 그 파일 안에서 라운드를 거듭하며 대화한다.**

- 모든 논의·결정·Q&A는 해당 파일에 `# Round N` 형태로 기록
- Claude는 파일을 읽고, 다음 라운드를 파일에 직접 append
- 화면 출력은 최소한의 요약만. **본문은 파일에 쓴다.**
- Nick이 파일에 `(Nick)` 태그로 답변 → Claude가 다시 다음 라운드 추가

### chatlog 파일 관행

- **파일명 주석**: 파일 맨 앞 첫 줄에 `<!-- 파일명 -->` HTML 주석
- **NCC**: Nick's Claude Code Co-worker = Claude. 이 프로젝트에서 AI 파트너 호칭.
- **세션 파일 없을 때**: NCC가 `YYMMDD_주제.md` 형식으로 `00_project_hub/10_chatlog/`에 새 파일 생성
- **세션 시작 시**: NCC는 항상 현재 작업 chatlog 파일명을 chat window에 밝힌다

---

## 단원 파이프라인 — 1개 단원 제작 과정

> **착수**: Nick이 "unit 02 만들어"라고 한 줄 의뢰 → `se-unit-orchestrator`가 Commission Brief(chatlog Round 0)를 자동 생성 → Nick이 확인 → 자율 실행.
> **HITL 없음**: NCC가 전 과정 자율 진행. 각 Phase 완료 시 chatlog 기록.
> 상세 워크플로우: `90_archive/10_docs_original/14_workflow_v4.md` (옛 기준), 신 워크플로우는 `10_system/60_workflows/`에 정리 예정.

```
Phase 0: 디렉토리 초기화
  └─ /se-unit-plan → 40_grades/middle/math1/NN_*/ 구조 생성

Phase 1: 개념 (축 A)
  ├─ 30_content/concepts/NN_*/ 검수·보완 → /se-concept-review
  └─ audit: /se-audit-concept

Phase 3 (비동기, 단원 파이프라인과 독립):
  └─ 수학 언어 업데이트 필요 여부 판단 → /se-math-figure → 30_content/literacy/

Phase 2: 이야기 (축 B)
  ├─ 인물 서사 = 영상 파이프라인 산출물 재사용 (50_channel/.../1-narrative.md, se-people-narrate 출력)
  └─ audit: /se-audit-story

Phase 4: 앱 (축 A+B 통합)
  ├─ HTML 앱 제작: index.html, story.html, concepts.html
  └─ audit: /se-audit-app

Phase 5-a: 기본문제
  ├─ 단원 전체 개념 커버 기본문제 (8~10개)
  └─ → problems/basic_app.html / audit: /se-audit-math + /se-audit-app

Phase 5-b: 유형 목록
  ├─ 시험 유형 목록 확정
  └─ → problems/types.md / audit: /se-audit-problem

Phase 5-c: 유형별 연습 (3/3/3 원칙)
  ├─ /se-math-practice → 유형별 L×3 + M×3 + H×3
  └─ → problems/type_NN_app.html / audit: /se-audit-math + /se-audit-app

Phase 5-d: 유형별 깊이 탐구 자료
  ├─ M+ 난이도 유형마다 /se-type-explorer 호출
  └─ → problems/deep_유형명_app.html / audit: /se-audit-math + /se-audit-app
```

---

## 등록된 Skills (Slash Commands)

### 제작 Skills
| 명령 | Phase | 용도 |
|---|---|---|
| `/se-unit-plan` | 0 | 단원 디렉토리 초기화 |
| `/se-concept-review` | 1 | 30_content/concepts/ 개념 MD 검수·보완 |
| `/se-math-figure` | 3, 5 | 수학 그래프 네이티브 렌더링 (SVG + JSXGraph) |
| `/se-math-practice` | 5c | 유형별 연습 문제 생성 (L/M/H 3×3) |
| `/se-math-error-note` | 5 in-loop | 오답노트 생성 (7섹션 MD + HTML 앱) |
| `/se-distill-principles` | meta | chatlog → principles 추출 |

### 영상 제작 Skills (8 STEP 파이프라인, 2026-05-29 졸업)
| 명령 | STEP | 용도 |
|---|---|---|
| `/se-people-pick` | 선정 | 단원 인물 발굴·평가·선정 |
| `/se-people-narrate` | 1 서사 | 인물 서사(약속 3겹 운반) 작성 |
| `/se-video-story` | 2 스토리 | 서사 → 6장면 스토리 시드 |
| `/se-video-storyboard` | 3 스토리보드 | 장면별 정밀 카드(부록 A/B/C) |
| `/se-video-narration` | 4 나레이션 | 2화자 dialog + ElevenLabs 음성 (config=voice-pool §0) |
| `/se-video-image` | 5 이미지 | 캐릭터 일관성 프롬프트 + Nano Banana 생성 |
| `/se-video-motion` | 6 모션 | scene 모션 + 자막 타이밍 config |
| `/se-video-render` | 7 렌더 | FFmpeg zoompan+자막 → raw mp4 |
| `/se-video-compose` | 8 합성 | A/V mux → final mp4 + 표지 |

> 구 `se_story_video_v1_5`(6장면 110초 edge-tts) = **폐기·아카이브** (`90_archive/skills_legacy/`). 신 파이프라인 = 위 8 STEP.
> 양산: `se-video-orchestrator` agent + `50_channel/season-1-ancient/_manifest.md`. 설계 = `11_video_gen_process/00_charter/PRODUCTION_SETUP.md`.

### NCC Audit Skills
| 명령 | 대상 | 기준 |
|---|---|---|
| `/se-audit-app` | HTML 앱 품질 | `10_system/10_principles/APP_PRINCIPLES.md` |
| `/se-audit-math` | 수학 정확성 (Wolfram 보조) | 중1 교육과정 |
| `/se-audit-concept` | 개념 수준·범위 | `10_system/20_context/LEARNER_PROFILE.md` |
| `/se-audit-problem` | 문제 커버리지·난이도 | 출제 원칙 |
| `/se-audit-story` | 스토리 적합성 + 피드백 분석 | LEARNER_PROFILE.md |
| `/se-unit-review` | 단원 전체 검토 | — |
| `/se-type-explorer` | 유형별 깊이 탐구 | Phase 5-d |

## 등록된 Agents

| 에이전트 | 용도 |
|---|---|
| `se-unit-orchestrator` | 단원 4축 파이프라인 (Phase 0~5c) — 개념·이야기·앱·문제 |
| `se-video-orchestrator` | **영상 8 STEP 파이프라인** — "unit NN [인물]" → 영상 1편 자율 제작 + batch(manifest) |

### Skill 동기화

SSOT는 `10_system/30_skills/`, `10_system/35_agents/`.
변경 후 mirror 갱신:
```bash
bash 70_tools/sync-skills.sh           # 실행
bash 70_tools/sync-skills.sh --dry     # dry run
```

---

## 절대 원칙

1. **우선순위 순서**: (a) 흥미·이해 > (b) 실전력 > (c) AI 경험
2. **페이스**: 단원 1개 = 2~3주. 진도보다 깊이.
3. **딸의 글 (`.private/feedback/`)은 임의 수정 금지.** 피드백은 별도 파일로. (gitignore된 위치)
4. **4축 모두 운영**: 한 축만 하면 불완전.
5. **빈칸·미완성을 의도적으로 남겨라.** 딸이 채울 자리가 있어야 한다.
6. **chatlog 파일 기반 대화.** 주요 결정은 반드시 `00_project_hub/10_chatlog/`에 기록.
7. **시간·토큰 효율**: 재읽기·재감사 사이클 금지. audit 1-shot 원칙.
8. **Rate limit 인식**: Anthropic API 5시간 sliding window. 단원 orchestrator 호출 전 잔량 확인.

---

## 학습 대상 (딸)

- 중1, 감성적·내성적, 국어/영어 강세, 수학 중하위
- "수학도 잘하고 싶은데 너무 어려움" (내적 동기 존재)
- 결정적 사례: `y=a/x, a=-2` 일 때 `y=-2/x` 로 변환 못함 → 축 C 발견 계기
- 상세: `10_system/20_context/LEARNER_PROFILE.md`

---

## 단원별 인물 배정 (Season 1: Ancient)

| 단원 | 개념 | 인물 |
|---|---|---|
| 1 | 소인수분해 | 에라토스테네스 |
| 2 | 정수·유리수 | 브라마굽타 |
| 3 | 문자·식 | 알콰리즈미 |
| 4 | 일차방정식 | 디오판토스 |
| 5~6 | 좌표·함수 | 데카르트 |

전체 메타: `30_content/units/NN/meta.json`, 인물 사실: `30_content/people/`.

---

## 타임라인

- **2026-05 (마이그 완료)**: math-story-telling 단일 repo로 통합. Ch1(소인수분해) ~ Ch4(일차방정식) 자료 완성.
- **2026-06~**: 딸과 본격 수학 공부 시작 + 추가 단원 확장.

---

## 기술 스택

- Claude Code + Local Markdown
- 인터랙티브: HTML+JS (바닐라, 빌드 없음), KaTeX, JSXGraph
- 영상: HyperFrames (GSAP) → FFmpeg, edge-tts (한국어 TTS)
- CSS 토큰: `20_packages/design-system/` (4종 토큰 + math subject)
- 앱 디자인 원칙: `10_system/10_principles/APP_PRINCIPLES.md`

---

## 참고 문서 (가장 자주 참조)

| 파일 | 내용 |
|---|---|
| `10_system/20_context/LEARNER_PROFILE.md` | 학습자 프로필 |
| `10_system/70_meta/concept.md` | 인물 서사 5단계 흐름 |
| `30_content/literacy/00_track_overview.md` | 수학 언어 트랙 L1~L7 |
| `10_system/10_principles/APP_PRINCIPLES.md` | HTML 앱 디자인 원칙 |
| `10_system/10_principles/STORY_VIDEO_v1_5.md` | 영상 v1.5 원칙 |
| `00_project_hub/40_context/external_repos.md` | 옛 4개 repo 참조 메타 |
| `90_archive/mid_eun_CLAUDE.md` | 옛 CLAUDE.md (참고) |
| `90_archive/10_docs_original/14_workflow_v4.md` | 옛 워크플로우 (참고) |
