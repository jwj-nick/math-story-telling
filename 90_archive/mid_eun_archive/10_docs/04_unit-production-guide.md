# Unit 제작 워크플로우 — AI-Native Production Guide

> 최종 업데이트: 2026-05-09
> 참조: CLAUDE.md, APP_PRINCIPLES.md

---

## Overview — AI-Native Workflow with Human in the Loop

```
Nick (승인·피드백)
    ↕  chatlog 라운드
NCC  (실행·생성·검증)
    ↕
산출물 (40_BaseDocs/, 50_units/)
```

**NCC** = Nick's Claude Code Co-worker (Claude)

전체 흐름:
1. Nick이 단원 착수 지시 → NCC가 `/unit-plan` 실행 → chatlog 파일 생성
2. Phase 1~5를 chatlog에서 라운드로 진행
3. Human in the loop: Phase별 Nick 확인·승인 포인트 존재
4. Unit 1 완성 기준 확립 → Unit 2~4 batch 방식으로 속도 업

---

## Phase별 상세

### Phase 1 — 개념 (축 A)

| 항목 | 내용 |
|---|---|
| **입력** | 단원번호, `40_BaseDocs/NN_단원명/` |
| **NCC 작업** | `/concept-review` 실행: 개념 MD 5~7개 검수·보완 |
| **Nick 역할** | 개념 범위·깊이 협의. 중1 수준 적합성 판단 |
| **산출물** | `40_BaseDocs/NN_단원명/` (보완된 개념 MD) |
| **HITL 포인트** | 개념 범위 확정 — 더할지 뺄지 |

### Phase 2 — 이야기 (축 B)

| 항목 | 내용 |
|---|---|
| **입력** | 인물명, 단원명, `20_research/02_R2-people-map.md` |
| **NCC 작업** | `/story-write`: 인물 리서치 + 스토리 초안 생성 |
| **Nick 역할** | 스토리 리뷰 → 피드백 → NCC 수정 → 최종 확정 |
| **산출물** | `50_units/NN/story/unitNN.md` |
| **HITL 포인트** | 스토리 확정 — 사실 검증, 감성·수준 적합성 |

### Phase 3 — 수학 언어 (축 C)

| 항목 | 내용 |
|---|---|
| **입력** | 단원 핵심 개념, `10_docs/03_literacy-track.md` |
| **NCC 작업** | 연결 L모듈 결정 + 인터랙티브 도구 제작 |
| **Nick 역할** | L모듈 선택 협의 |
| **산출물** | `40_BaseDocs/00_literacy/LN_주제/LN_app.html` |
| **비고** | 단원 횡단 자료 → `50_units/`가 아닌 `40_BaseDocs/`에 저장 |

### Phase 4 — 도구 (축 A+B 통합)

| 항목 | 내용 |
|---|---|
| **입력** | Phase 1 개념 + Phase 2 스토리 |
| **NCC 작업** | HTML 앱 제작 (story/sieve/concepts/problems 4종) + app-reviewer 검증 |
| **Nick 역할** | 앱 구조 변경 승인, 앱 최종 확인 |
| **산출물** | `50_units/NN/app/*.html`, `50_units/NN/video/` |
| **HITL 포인트** | 구조적 앱 변경 승인, 수학적 정확성 확인 |

### Phase 5 — 문제 연습 (축 D)

| 항목 | 내용 |
|---|---|
| **입력** | 딸이 틀린 문제 번호 (또는 대표 문제 선정) |
| **NCC 작업** | `/math-error-note` + `/math-figure` + `/math-practice` + app-reviewer |
| **Nick 역할** | 문제 선정, 수학적 정확성 최종 확인 |
| **산출물** | `50_units/NN/problems/QN.md + QN_app.html + QN_practice_app.html` |
| **자동화** | `math-workflow` 에이전트로 여러 문제 일괄 처리 가능 |

---

## Skills & Agents 역할 분담

| 도구 | 유형 | Phase | 입력 | 산출물 |
|---|---|---|---|---|
| `/unit-plan` | Skill | 킥오프 | 단원번호 | chatlog + `50_units/NN/` 디렉토리 |
| `/concept-review` | Skill | 1 | 단원번호 | 40_BaseDocs 검수 보고 |
| `/story-write` | Skill | 2 | 인물·단원명 | `story/unitNN.md` |
| `/math-error-note` | Skill | 5 | 문제번호, 단원 | `QN.md` + `QN_app.html` |
| `/math-figure` | Skill | 5 | 문제번호 | SVG/JSXGraph 그래프 |
| `/math-practice` | Skill | 5 | 문제번호 | `QN_practice.md` + `QN_practice_app.html` |
| `/video-make` | Skill | 4 | 스크립트 | `video/` |
| `/figcrop` | Skill | 5 | 시험지 이미지 | 크롭된 문제 그림 |
| `app-reviewer` | Agent | 4, 5 | HTML 앱 경로 | 위반 보고 + 즉시 수정 |
| `math-workflow` | Agent | 5 | 틀린 문제 목록 | Phase 5 전체 자동화 |

---

## Human in the Loop (HITL) 포인트

Nick이 반드시 확인/승인해야 진행되는 단계:

| Phase | HITL 포인트 | 이유 |
|---|---|---|
| 1 | 개념 범위 협의 | 중1 수준·깊이 판단은 Nick만 가능 |
| 2 | 스토리 최종 확정 | 딸에게 맞는 감성·사실 검증 |
| 4 | 구조적 앱 변경 | UX 방향은 Nick 판단 |
| 5 | 수학 정확성 | 오류가 딸에게 전달되면 안 됨 |

---

## 단원 재정비 vs 신규 제작

### 재정비 (기존 콘텐츠 → 새 구조로 검수)

```
1. 현황 파악: 40_BaseDocs + 50_units/ 기존 파일 목록
2. Phase 1: 개념 MD 검수 (/concept-review)
3. Phase 2: story 내용·경로 검수
4. Phase 4: app-reviewer 실행 → 위반 수정
5. Phase 5: 문제 QN_source.md 정의 → html 생성
```

### 신규 제작 (처음부터)

```
1. /unit-plan 실행 → chatlog + 디렉토리 생성
2. Phase 1 → 2 → 3 → 4 → 5 순차 진행
3. 각 Phase: NCC 초안 → Nick 리뷰 → NCC 수정 → 확정
```

---

## math-workflow 에이전트 — Phase 5 전용 자동화

```
트리거: 딸이 틀린 문제 번호 전달
    └─ /math-error-note → QN.md + QN_app.html
    └─ /math-figure     → (그림 있는 경우) SVG/JSXGraph
    └─ /math-practice   → QN_practice.md + QN_practice_app.html
    └─ app-reviewer     → 위반 즉시 수정
    └─ 완료 보고
```

현재 Unit 1 재정비는 math-workflow 범위 밖 — Phase 1~4 재검수 작업이기 때문.

---

## 문제 출제 — MD 우선 원칙 (Unit 2부터 적용)

```
50_units/NN/problems/
  ├── QN_source.md       ← 문제 정의 (Nick 검수, NCC 생성)
  └── QN_app.html        ← QN_source.md 기반으로 NCC가 생성
```

**QN_source.md 포맷**: 문제 원문 / 정답 / 힌트 / 연결 개념 / 출처

Unit 1: 기존 html 유지. 필요 시 역방향으로 QN_source.md 추출 가능.

---

## chatlog 기반 대화 방식

- 파일명: `YYMMDD_단원명_주제.md`
- 파일 첫 줄: `<!-- 파일명 -->` HTML 주석
- NCC가 세션 파일 없으면 생성, chat window에서 파일명 명확히 언급
- Nick의 답변: 파일 내 직접 편집 (자유형)
- Round 단위 진행, NCC는 Round마다 파일에 append

---

*참조: CLAUDE.md / APP_PRINCIPLES.md / .claude/skills/ / .claude/agents/*
