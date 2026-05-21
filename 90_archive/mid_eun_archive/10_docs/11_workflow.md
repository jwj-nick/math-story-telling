<!-- 10_docs/11_workflow.md -->
# MathTelling — Unit Production Workflow

> 마지막 업데이트: 2026-05-09
> AI tool · 산출물 관점 명세서. Phase별 입출력 · agent/skill 관계 정의.

---

## 1. 전체 흐름도 (AI Tool + Results 관점)

```
Nick (Human in the Loop)  ── chatlog 라운드 기반 대화 ──  NCC (Claude)
      ↓ 착수 지시                                              ↓
 ┌──────────────────────────────────────────────────────────────────┐
 │                   MathTelling 단원 제작                           │
 │                                                                  │
 │  INPUT              AI TOOL (NCC)              OUTPUT            │
 │  ────────           ──────────────             ──────────        │
 │  단원번호      ──►  /unit-plan          ──►  chatlog             │
 │                                               50_units/NN/      │
 │                                                                  │
 │  40_BaseDocs/  ──►  /concept-review     ──►  개념 MD (검수)      │
 │  기존 MD              (Skill)                                    │
 │                         ↕ HITL(1)                               │
 │                                                                  │
 │  인물+리서치   ──►  /story-write        ──►  story/unitNN.md    │
 │                       (Skill)                                    │
 │                         ↕ HITL(2)                               │
 │                                                                  │
 │  개념+스토리   ──►  NCC 직접 제작       ──►  app/*.html         │
 │                  ──►  app-reviewer      ──►  위반 보고·수정      │
 │                       (Agent)                                    │
 │                         ↕ HITL(3)                               │
 │                                                                  │
 │  문제 정의     ──►  NCC + 문제검토체계  ──►  problems/*.html    │
 │  (§4 참조)          (§4 참조)                                    │
 │                         ↕ HITL(4)                               │
 │                                                                  │
 │  오답 발생     ──►  math-workflow       ──►  QN_app.html        │
 │                       (Agent)                QN_practice.html   │
 └──────────────────────────────────────────────────────────────────┘
```

---

## 2. Phase별 I/O 명세

### Phase 0 — 킥오프

| 항목 | 내용 |
|---|---|
| **입력** | 단원번호 (예: 01) |
| **AI 도구** | `/unit-plan` Skill |
| **NCC 작업** | chatlog 파일 생성 + `50_units/NN/` 디렉토리 초기화 |
| **산출물** | `chatlog/YYMMDD_unitNN.md` + `50_units/NN/{story,app,video,problems,feedback}/` |

---

### Phase 1 — 개념 (축 A)

| 항목 | 내용 |
|---|---|
| **입력** | `40_BaseDocs/NN_단원명/` MD 파일 5~7개 |
| **AI 도구** | `/concept-review` Skill |
| **NCC 작업** | 각 MD 정확성·수준·범위 검수 → 보완 제안 |
| **산출물** | 검수 보고 (chatlog) + `40_BaseDocs/NN/` 보완된 MD |
| **HITL(1)** | 개념 범위·깊이 확정 (중1 수준 적합성 판단) |

---

### Phase 2 — 이야기 (축 B)

| 항목 | 내용 |
|---|---|
| **입력** | 단원번호, 인물명, `20_research/02_R2-people-map.md` |
| **AI 도구** | `/story-write` Skill |
| **NCC 작업** | 인물 리서치 + 스토리 초안 생성 |
| **산출물** | `50_units/NN/story/unitNN.md` |
| **HITL(2)** | 스토리 확정 (사실 검증, 딸에게 맞는 감성) |

---

### Phase 3 — 수학 언어 (축 C, 단원 횡단)

| 항목 | 내용 |
|---|---|
| **입력** | 단원 핵심 개념, `10_docs/03_literacy-track.md` |
| **AI 도구** | NCC 직접 제작 + `/math-figure` |
| **NCC 작업** | 연결 L모듈 결정 + 인터랙티브 HTML 제작 |
| **산출물** | `40_BaseDocs/00_literacy/LN_주제/LN_app.html` |
| **비고** | 단원 횡단 → `50_units/`가 아닌 `40_BaseDocs/`에 저장 |

---

### Phase 4 — 인터랙티브 앱 (축 A+B 통합)

| 항목 | 내용 |
|---|---|
| **입력** | Phase 1 개념 MD + Phase 2 스토리 |
| **AI 도구** | NCC 직접 제작 → `app-reviewer` Agent |
| **NCC 작업** | 앱 4종 제작 (index / story / sieve / concepts / problems) |
| **app-reviewer** | APP_PRINCIPLES.md 기준 체크 → 단순 위반 즉시 수정, 구조적 변경 → HITL |
| **산출물** | `50_units/NN/app/*.html` |
| **HITL(3)** | 구조적 앱 변경 승인, 수학적 정확성 최종 확인 |

---

### Phase 5 — 문제 연습 (축 D) ← 재정비 중

§4에서 상세 논의.

---

## 3. Agent / Skill 카탈로그

### Skills (대화 중 즉시 실행, 단일 작업)

| 명령 | Phase | 입력 | 산출물 |
|---|---|---|---|
| `/unit-plan` | 0 | 단원번호 | chatlog + `50_units/NN/` 구조 |
| `/concept-review` | 1 | 단원번호 | 개념 MD 검수 보고 |
| `/story-write` | 2 | 인물명, 단원명 | `story/unitNN.md` |
| `/math-figure` | 3, 5 | 개념 또는 문제번호 | SVG / JSXGraph 인라인 |
| `/math-error-note` | 5 | 문제번호, 단원 | `QN.md` + `QN_app.html` |
| `/math-practice` | 5 | 문제번호 | `QN_practice.md` + `QN_practice_app.html` |
| `/video-make` | 4 | 스크립트 | `video/*.mp4` |
| `/figcrop` | 5 | 시험지 이미지 | 크롭된 문제 그림 |

### Agents (여러 작업 자율 조합·순차 실행)

| 에이전트 | Phase | 입력 | 내부 도구 | 산출물 |
|---|---|---|---|---|
| `app-reviewer` | 4, 5 | HTML 앱 경로 | Read, Grep, Edit | 위반 보고 + 단순 위반 즉시 수정 |
| `math-workflow` | 5 (오답) | 틀린 문제 번호 목록 | `/math-error-note` → `/math-figure` → `/math-practice` → `app-reviewer` | Phase 5 오답노트 전체 산출물 |

---

## 4. Phase 5 — 문제 연습 구조 재정비

### 4-1. 현재 구조 (오답노트 중심)

```
[딸이 틀린 문제 발생]
       ↓
math-workflow Agent
  ├─ /math-error-note  →  QN.md + QN_app.html        (오답노트)
  ├─ /math-figure      →  그래프 보강 (필요 시)
  ├─ /math-practice    →  QN_practice_app.html        (L/M/H 3×3)
  └─ app-reviewer      →  앱 품질 검토·수정
```

**현재 3/3/3 원칙 위치**: `/math-practice` 스킬 내. 오답 복습 맥락.  
문제 유형 기획보다 **딸이 틀린 특정 문제** 복습에 최적화된 구조.

---

### 4-2. 발전 방향 (Nick 제안)

단원 전체를 학습하는 흐름으로 확장:

```
[단원 학습 흐름]

Phase 5-a. 기본문제 (problems.html)
  입력:  QN_source.md (Nick 검수)
  도구:  NCC 직접 생성 → app-reviewer
  목적:  개념을 고루 확인하는 충실한 기본문제 (단원 전체 커버)
  출력:  50_units/NN/app/problems.html
         ↓

Phase 5-b. 유형 파악 (problems_types.md — 미정)
  입력:  단원 개념 + 교과서 기출 패턴
  도구:  NCC 초안 → Nick 검수·확정
  목적:  시험에 나올 법한 유형 목록 확정
  출력:  50_units/NN/problems/types.md
         ↓

Phase 5-c. 유형별 연습 앱 (미정)
  입력:  types.md + QN_source.md
  도구:  /math-practice 확장 또는 신규 skill
  목적:  유형별 × 중급 이상 문제 (3/3/3 원칙 적용 지점)
  출력:  50_units/NN/problems/QN_type_app.html
         ↓

Phase 5-d. 오답노트 (기존 math-workflow 유지)
  입력:  딸이 틀린 문제 번호
  도구:  math-workflow Agent (현행 그대로)
  목적:  오답 발생 시 즉각 복습
  출력:  QN.md + QN_app.html + QN_practice_app.html
```

**확정 시 영향 받는 항목:**

| 대상 | 현재 | 변경 후 |
|---|---|---|
| `problems.html` | 단원 앱 (구조 불명확) | 5-a 기본문제 앱으로 특화 |
| `/math-practice` | 오답노트 연습 전용 | 5-d 전용 유지 or 5-c까지 확장 (결정 필요) |
| `math-workflow` | Phase 5 전체 | 5-d 오답노트 전용으로 범위 명확히 한정 |
| QN_source.md | Unit 2부터 도입 예정 | 5-a의 기본 입력 단위로 전체 확장 |

> **현재 상태**: 발전 방향 초안. Nick 검토 후 확정. 확정되면 skill/agent 수정 착수.

---

### 4-3. 문제 출제·검토 흐름 (세부)

문제 출제는 단순 생성이 아니라 **정확성 검증 포함**이 필요:

```
[문제 출제 흐름]

① Nick 또는 NCC가 QN_source.md 초안 작성
   — 문제 원문 / 정답 / 힌트 / 연결 개념 / 유형 / 출처 포함

② NCC 수학 검증
   — 풀이 직접 전개 → 정답 확인
   — 보기 목록이 있으면 보기와 정답 교차 확인
   — 단위·표기 규칙 (APP_PRINCIPLES.md) 준수 여부

③ Nick HITL
   — 문제 수준·유형 적합성 최종 확인
   — "딸이 풀 수 있는가?" 판단

④ NCC가 HTML 앱 생성 → app-reviewer 검토
```

**외부 도구 활용 포인트 (Nick 제안 - 검토 필요):**

| 도구 | 용도 | 검토 상태 |
|---|---|---|
| Wolfram Alpha (MCP) | 수식 계산 검증, 정답 독립 확인 | MCP 연결 가능 여부 확인 필요 |
| Khan Academy 문제 DB | 유형별 기출 패턴 참고 | 웹 리서치로 NCC가 참조 가능 |
| Desmos | 그래프 시각화 (JSXGraph 대안) | 현재 JSXGraph 사용 중 |
| 교육청 기출 문제 | 시험 유형 근거 자료 | Nick이 PDF 제공 시 figcrop + NCC 처리 |

> 현재 수학 검증은 NCC 직접 풀이로 처리. Unit 1에서 실제 버그 3건 발견·수정.  
> Wolfram Alpha MCP 연결은 별도 검토 필요.

---

## 5. HITL 포인트 요약

| Phase | 포인트 | 이유 |
|---|---|---|
| 1 | 개념 범위·깊이 확정 | 중1 수준 판단은 Nick만 가능 |
| 2 | 스토리 최종 확정 | 딸에게 맞는 감성·사실 검증 |
| 4 | 구조적 앱 변경 | UX 방향은 Nick 판단 |
| 5-a | 기본문제 유형·수 확정 | 개념 커버리지 판단 |
| 5-b | 시험 유형 목록 확정 | 시험 맥락은 Nick만 파악 |
| 5-d | 수학 정확성 최종 확인 | 오류가 딸에게 전달되면 안 됨 |

---

## 6. Batch 처리 계획

Unit 1 = 기준 템플릿 확립:
- skill/agent 입출력 확정
- APP_PRINCIPLES.md 기준 확립
- QN_source.md 포맷 확정
- Phase 5 구조 확정

```
Unit 1 완성 (기준 확립)
  ↓
Unit 2, 3, 4 — Phase별 batch 처리
  Phase 1: /concept-review × 3단원 (빠름)
  Phase 2: /story-write × 3단원 (빠름)
  Phase 4: NCC 직접 + app-reviewer × 3단원
  Phase 5: 확정된 구조 기반 일괄 생성
```

---

*참조: CLAUDE.md / APP_PRINCIPLES.md / .claude/skills/ / .claude/agents/*
