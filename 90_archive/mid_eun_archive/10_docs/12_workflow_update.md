<!-- 10_docs/12_workflow_update.md -->
# MathTelling — Workflow v2

> 날짜: 2026-05-09  
> `11_workflow.md` 각 단계 재검토 후 Mermaid 다이어그램 포함 재정리.

---

## 재검토 요약 — 11_workflow.md 대비 주요 변경

| 항목 | 변경 내용 |
|---|---|
| `problems.html` 위치 | Phase 4 → Phase 5-a 이동 (문제 정의 먼저 필요) |
| 3/3/3 원칙 위치 | 5-d 오답노트 연습 → **5-c 유형별 연습**으로 명확히 재정의 |
| Phase 3 타이밍 | Phase 1 완료 후 병렬 착수 가능으로 명시 |
| 문제 검증 흐름 | 출제→검증→HITL→HTML 4단계 별도 다이어그램으로 분리 |
| 신설 Skill 필요 목록 | `/problems-make`, `/problem-types` 명시 (5-a, 5-b용) |
| 외부 도구 | Wolfram Alpha MCP / 기출 PDF / Khan Academy 세분화 |

---

## 1. Overview

### 개념

```
Nick(Human) ←── chatlog 라운드 ──► NCC(Claude)
각 Phase 완료 시 Nick HITL. 확인 후 다음 Phase 착수.
Unit 1 기준 확립 → Unit 2~4 Batch 처리.
```

### Overview Diagram

```mermaid
flowchart LR
    START(["착수<br>Nick"])

    subgraph PIPE["단원 제작 파이프라인"]
        direction LR
        P0["⓪ 킥오프<br>/unit-plan"]
        P1["① 개념<br>/concept-review"]
        P2["② 이야기<br>/story-write"]
        P3["③ 수학언어<br>독립진행"]
        P4["④ 도구<br>NCC + app-reviewer"]
        P5["⑤ 문제연습<br>5-a~5-d"]

        P0 --> P1 --> P2 --> P4 --> P5
        P3 -.->|"Phase 1 후<br>병렬 가능"| P4
    end

    NICK(["👤 Nick HITL"])
    START --> P0
    P1 <-->|"개념 범위"| NICK
    P2 <-->|"스토리 확정"| NICK
    P4 <-->|"앱 승인"| NICK
    P5 <-->|"문제 확정"| NICK
```

### 산출물 위치

| Phase | 산출물 경로 |
|---|---|
| 0 | `chatlog/YYMMDD_unitNN.md` + `50_units/NN/` 폴더 구조 |
| 1 | `40_BaseDocs/NN_단원명/*.md` |
| 2 | `50_units/NN/story/unitNN.md` |
| 3 | `40_BaseDocs/00_literacy/LN_주제/LN_app.html` |
| 4 | `50_units/NN/app/` (index / story / 개념탐구 / concepts) |
| 5-a | `50_units/NN/app/problems.html` |
| 5-b | `50_units/NN/problems/types.md` |
| 5-c | `50_units/NN/problems/type_NN_app.html` |
| 5-d | `50_units/NN/problems/QN.md + QN_app.html + QN_practice_app.html` |

---

## 2. Phase 0 — 킥오프

```mermaid
flowchart LR
    IN["단원번호<br>예: 01"] --> SK["/unit-plan<br>Skill"]
    SK --> O1["chatlog/YYMMDD_unitNN.md<br>(Round 1 헤더 포함)"]
    SK --> O2["50_units/NN/<br>story/ app/ video/<br>problems/ feedback/"]
    O1 & O2 --> NEXT["Phase 1 착수"]
```

| 항목 | 내용 |
|---|---|
| **입력** | 단원번호 |
| **AI 도구** | `/unit-plan` Skill |
| **산출물** | chatlog 파일 + 디렉토리 구조 |
| **HITL** | 없음 (자동 실행) |

**검토 메모**: chatlog에 Round 1 섹션 헤더 + 검수 대상 파일 목록이 자동 생성되면 다음 작업 속도 향상. 현재는 수동.

---

## 3. Phase 1 — 개념 (축 A)

```mermaid
flowchart LR
    IN["40_BaseDocs/NN/<br>기존 개념 MD"] --> SK["/concept-review<br>Skill"]
    SK --> R["검수 보고<br>chatlog 기록"]
    SK --> OUT["40_BaseDocs/NN/*.md<br>보완본"]
    OUT --> HITL(["👤 Nick<br>범위·깊이 확정"])
    HITL -->|"확정"| NEXT["Phase 2 착수<br>Phase 3 병렬 착수 가능"]
```

| 항목 | 내용 |
|---|---|
| **입력** | `40_BaseDocs/NN_단원명/` MD 파일 5~7개 |
| **AI 도구** | `/concept-review` Skill |
| **NCC 작업** | 정확성·중1 수준·범위 검수 → 보완 제안 |
| **산출물** | 검수 보고 (chatlog) + 보완된 개념 MD |
| **HITL** | 개념 범위·깊이 확정 |

**검토 메모**: 신규 단원처럼 `40_BaseDocs` 없을 때 "신규 작성" 모드 미지원. Phase 1 완료 후 Phase 3을 Phase 2와 병렬로 착수 가능 — 이전 버전에 명시 안 됨.

---

## 4. Phase 2 — 이야기 (축 B)

```mermaid
flowchart LR
    IN1["인물명 + 단원명"] --> SK["/story-write<br>Skill"]
    IN2["20_research/<br>R2-people-map.md"] --> SK
    SK --> DRAFT["story/unitNN.md<br>초안"]
    DRAFT --> NICK(["👤 Nick<br>리뷰·피드백"])
    NICK -->|"수정 요청"| NCC["NCC 수정"]
    NCC --> NICK
    NICK -->|"확정"| FINAL["story/unitNN.md<br>확정본"]
    FINAL --> NEXT["Phase 4 착수"]
```

| 항목 | 내용 |
|---|---|
| **입력** | 인물명, 단원명, 리서치 자료 |
| **AI 도구** | `/story-write` Skill |
| **NCC 작업** | 인물 리서치 + 스토리 초안 |
| **산출물** | `story/unitNN.md` 확정본 |
| **HITL** | 스토리 확정 — 반복 가능 (초안 → 피드백 → 수정 × N회) |

**검토 메모**: 이전 버전에 리뷰 반복 루프가 명시 안 됨. Phase 4는 반드시 스토리 확정 후 착수.

---

## 5. Phase 3 — 수학 언어 (축 C)

```mermaid
flowchart LR
    IN1["단원 핵심 개념<br>Phase 1 완료 후"] --> NCC1["NCC<br>L모듈 결정"]
    IN2["03_literacy-track.md"] --> NCC1
    NCC1 --> HITL(["👤 Nick<br>L모듈 선택"])
    HITL --> NCC2["NCC 직접 제작<br>+ /math-figure"]
    NCC2 --> OUT["40_BaseDocs/00_literacy/<br>LN_주제/LN_app.html"]
    OUT -.->|"Phase 4에 연결"| P4(["Phase 4"])
```

| 항목 | 내용 |
|---|---|
| **입력** | 단원 핵심 개념, literacy-track.md |
| **AI 도구** | NCC 직접 제작 + `/math-figure` |
| **NCC 작업** | L모듈 결정 + 인터랙티브 HTML 제작 |
| **산출물** | `40_BaseDocs/00_literacy/LN_*/LN_app.html` |
| **HITL** | L모듈 선택 협의 |
| **비고** | 단원 횡단 자료 → `50_units/` 아닌 `40_BaseDocs/`에 저장 |

**검토 메모**: Phase 2와 병렬 진행 가능 (Phase 1 완료 후 즉시 착수 가능). L모듈 없는 단원은 Phase 3 생략 가능 — 명시 필요. 전용 Skill 없음 → 반복 시 `/literacy-make` 신설 검토.

---

## 6. Phase 4 — 인터랙티브 앱 (축 A+B 통합)

```mermaid
flowchart TD
    IN1["Phase 1<br>40_BaseDocs/NN/*.md"] --> NCC
    IN2["Phase 2<br>story/unitNN.md"] --> NCC
    IN3["Phase 3<br>LN_app.html (있으면)"] --> NCC

    NCC["NCC 직접 제작"] --> APPS

    subgraph APPS["app/ 제작 4종"]
        direction LR
        A1["index.html<br>단원 홈"]
        A2["story.html<br>스토리 앱"]
        A3["개념탐구.html<br>예: sieve.html"]
        A4["concepts.html<br>플래시카드·빈칸"]
    end

    APPS --> AR["app-reviewer<br>Agent"]
    AR -->|"단순 위반"| FIX["즉시 수정"]
    AR -->|"구조적 변경"| HITL(["👤 Nick 승인"])
    HITL --> NCCFIX["NCC 수정"]
    FIX & NCCFIX --> DONE["app/*.html 완성"]
    DONE --> NEXT["Phase 5 착수"]
```

| 항목 | 내용 |
|---|---|
| **입력** | Phase 1, 2, 3 산출물 |
| **AI 도구** | NCC 직접 제작 → `app-reviewer` Agent |
| **제작 앱** | index / story / 개념탐구 / concepts (4종, problems.html 제외) |
| **app-reviewer** | APP_PRINCIPLES.md 기준 검토. 단순 위반 즉시 수정, 구조적 변경 → HITL |
| **산출물** | `50_units/NN/app/*.html` |
| **HITL** | 구조적 앱 변경 승인, 수학 정확성 확인 |

**검토 메모**: `problems.html`은 Phase 4에서 분리 → Phase 5-a로 이동. 이유: 문제 내용(QN_source.md)이 먼저 확정돼야 앱 생성 가능.

---

## 7. Phase 5 — 문제 연습 (축 D)

### Phase 5 전체 구조

```mermaid
flowchart TD
    subgraph P5["Phase 5 — 문제 연습"]
        direction TB
        P5A["5-a<br>기본문제<br>problems.html"]
        P5B["5-b<br>유형 파악<br>types.md"]
        P5C["5-c<br>유형별 연습<br>type_NN_app.html"]
        P5D["5-d<br>오답노트<br>math-workflow"]

        P5A --> P5B --> P5C
    end

    ERR(["딸의 오답 발생"]) --> P5D
    NICK(["👤 Nick HITL"]) <-->|"각 단계 확인"| P5
```

---

### Phase 5-a — 기본문제

```mermaid
flowchart LR
    IN["QN_source.md<br>문제원문/정답/힌트<br>연결개념/유형"] --> NICK(["👤 Nick 검수"])
    NICK -->|"확정"| NCC["NCC HTML 생성<br>(/problems-make 예정)"]
    NCC --> AR["app-reviewer"]
    AR --> OUT["app/problems.html<br>기본문제 앱"]
```

| 항목 | 내용 |
|---|---|
| **입력** | `QN_source.md` (문제 원문 / 정답 / 힌트 / 연결 개념) |
| **AI 도구** | NCC 직접 제작 → `app-reviewer` |
| **목적** | 단원 전체 개념을 고루 확인하는 충실한 기본문제 |
| **산출물** | `50_units/NN/app/problems.html` |
| **HITL** | QN_source.md 확정 (개념 커버리지 판단) |
| **현재 Skill** | 없음 → `/problems-make` 신설 필요 (🔴 높음) |

---

### Phase 5-b — 유형 파악

```mermaid
flowchart LR
    IN1["단원 개념<br>Phase 1 산출물"] --> NCC["NCC 리서치<br>교육과정 + 기출 패턴"]
    IN2["기출 PDF<br>(Nick 제공, 선택)"] --> FC["/figcrop<br>문제 이미지 추출"]
    FC --> NCC
    NCC --> DRAFT["types.md 초안<br>유형 목록"]
    DRAFT --> NICK(["👤 Nick<br>유형 확정"])
    NICK --> OUT["problems/types.md<br>확정본"]
```

| 항목 | 내용 |
|---|---|
| **입력** | 단원 개념 + 교육과정 기출 패턴 + (선택) 기출 PDF |
| **AI 도구** | NCC 리서치 (WebSearch / `/figcrop`) |
| **목적** | 시험에 나올 법한 유형 목록 확정 |
| **산출물** | `problems/types.md` |
| **HITL** | 유형 목록 확정 (시험 맥락은 Nick만 파악) |
| **현재 Skill** | 없음 → `/problem-types` 신설 검토 (🟡 중간) |

**Unit 1 유형 예시 (초안):**

| 유형 | 내용 |
|---|---|
| T1 | 소인수분해 직접 계산 |
| T2 | 소인수분해 이용한 GCD |
| T3 | 소인수분해 이용한 LCM |
| T4 | 약수 개수 구하기 |
| T5 | GCD·LCM 활용 (실생활) |

> Nick 확정 필요.

---

### Phase 5-c — 유형별 연습

```mermaid
flowchart LR
    IN1["problems/types.md<br>확정 유형 목록"] --> SK["(확장) /math-practice<br>또는 신규 Skill"]
    IN2["난이도 설정<br>L / M / H"] --> SK
    SK --> GEN["유형별 3×3<br>문제 생성"]
    GEN --> AR["app-reviewer"]
    AR --> OUT["problems/<br>type_NN_app.html"]
    OUT --> NICK(["👤 Nick<br>수학 정확성 확인"])
```

| 항목 | 내용 |
|---|---|
| **입력** | `types.md` + 난이도 설정 |
| **AI 도구** | `/math-practice` 확장 또는 신규 Skill |
| **목적** | 유형별 × L/M/H 3×3 = 9문제 연습 앱 |
| **산출물** | `problems/type_NN_app.html` |
| **HITL** | 수학 정확성 확인 |
| **3/3/3 원칙** | 이 단계에 적용 — 유형 × (L×3 + M×3 + H×3) |

> **3/3/3 위치 재정의**: 기존에는 오답노트(5-d) 뒤에 붙었으나, **5-c 유형별 연습이 3/3/3의 원래 의도**에 맞음. 5-d `/math-practice`는 오답 문제 1개에 집중하는 용도로 재한정.

---

### Phase 5-d — 오답노트

```mermaid
flowchart LR
    IN["딸의 오답<br>문제 번호 목록"] --> MW["math-workflow<br>Agent"]

    subgraph MWINT["math-workflow 내부"]
        direction LR
        EN["/math-error-note"] --> MF["/math-figure<br>그림 있을 때"]
        MF --> MP["/math-practice<br>오답 문제 전용"]
        MP --> AR2["app-reviewer"]
    end

    MW --> MWINT
    MWINT --> O1["problems/QN.md<br>오답노트"]
    MWINT --> O2["problems/QN_app.html<br>오답노트 앱"]
    MWINT --> O3["problems/QN_practice_app.html<br>연습 앱"]
    O1 & O2 & O3 --> NICK(["👤 Nick<br>수학 정확성 확인"])
```

| 항목 | 내용 |
|---|---|
| **입력** | 딸이 실제로 틀린 문제 번호 목록 |
| **AI 도구** | `math-workflow` Agent |
| **내부 Skill** | `/math-error-note` → `/math-figure` → `/math-practice` → `app-reviewer` |
| **산출물** | `QN.md` + `QN_app.html` + `QN_practice_app.html` |
| **HITL** | 수학 정확성 최종 확인 |
| **비고** | 기존 구조 유지. 딸이 실제 공부 시작 후 발동. |

---

## 8. 문제 출제·검증 흐름 (상세)

```mermaid
flowchart TD
    subgraph DRAFT["① 출제"]
        D1["Nick 또는 NCC<br>QN_source.md 초안"]
        D1 --> D2["QN_source.md 포맷<br>문제원문/정답/힌트<br>연결개념/유형/출처"]
    end

    subgraph VERIFY["② 검증"]
        V1["NCC 수학 검증<br>직접 풀이 전개"]
        V2["보기 목록 교차 확인<br>(객관식일 때)"]
        V3["표기·단위 규칙<br>APP_PRINCIPLES.md"]
        V1 --> V2 --> V3
    end

    subgraph HITLSTEP["③ HITL"]
        H1["👤 Nick<br>수준·유형 적합성"]
        H2["딸이 풀 수 있는가?"]
        H1 --> H2
    end

    subgraph BUILD["④ 앱 생성"]
        B1["NCC HTML 생성<br>(/problems-make 예정)"]
        B2["app-reviewer<br>품질 검토"]
        B1 --> B2
    end

    DRAFT --> VERIFY --> HITLSTEP --> BUILD
    BUILD --> DONE["problems/*.html<br>완성"]

    EXT_W["Wolfram Alpha MCP<br>복잡한 계산 독립 검증"]
    EXT_F["/figcrop<br>기출 PDF → 이미지"]
    VERIFY -.->|"선택"| EXT_W
    DRAFT -.->|"기출 활용 시"| EXT_F
```

---

## 9. Agent / Skill 카탈로그

### 현재 등록 도구

| 도구 | 유형 | Phase | 입력 | 산출물 | 상태 |
|---|---|---|---|---|---|
| `/unit-plan` | Skill | 0 | 단원번호 | chatlog + 디렉토리 | ✅ |
| `/concept-review` | Skill | 1 | 단원번호 | 개념 MD 검수 보고 | ✅ |
| `/story-write` | Skill | 2 | 인물명, 단원명 | `story/unitNN.md` | ✅ |
| `/math-figure` | Skill | 3, 5 | 개념/문제번호 | SVG/JSXGraph | ✅ |
| `/math-error-note` | Skill | 5-d | 문제번호, 단원 | `QN.md` + `QN_app.html` | ✅ |
| `/math-practice` | Skill | 5-d | 문제번호 | `QN_practice_app.html` | ✅ (5-d 전용 재한정) |
| `/video-make` | Skill | 4 | 스크립트 | `video/*.mp4` | ✅ |
| `/figcrop` | Skill | 5-b | 시험지 이미지 | 크롭된 그림 | ✅ |
| `app-reviewer` | Agent | 4, 5 | HTML 앱 경로 | 위반 보고 + 수정 | ✅ |
| `math-workflow` | Agent | 5-d | 오답 번호 목록 | 오답노트 전체 산출물 | ✅ (5-d 전용으로 범위 한정) |

### 신설 필요 도구

| 도구 | 유형 | Phase | 역할 | 우선순위 |
|---|---|---|---|---|
| `/problems-make` | Skill | 5-a | QN_source.md → problems.html 자동 생성 | 🔴 높음 (Unit 2부터 필요) |
| `/problem-types` | Skill | 5-b | 단원 개념 + 기출 → types.md 초안 생성 | 🟡 중간 |

### Skill vs Agent 구분

```mermaid
flowchart LR
    subgraph SK["Skill"]
        SK1["단일 작업<br>입력 → 산출물"]
        SK2["NCC가 대화 중 직접 실행"]
        SK3["예: /story-write → MD 1개"]
    end
    subgraph AG["Agent"]
        AG1["복합 파이프라인<br>여러 Skill 자율 조합"]
        AG2["독립 서브에이전트로 실행"]
        AG3["예: math-workflow<br>= Skill 4개 연쇄"]
    end
```

---

## 10. 외부 도구 연동

| 도구 | 용도 | 연동 방법 | 상태 |
|---|---|---|---|
| **Wolfram Alpha MCP** | 수식·정답 독립 검증 (NCC 검증 이중화) | `.claude/settings.json` MCP 설정 | 🔲 미결정 |
| **교육청 기출 PDF** | 유형 목록 근거, 실제 시험 문제 확인 | Nick 제공 → `/figcrop` → NCC 분석 | 🔲 Nick 제공 필요 |
| **Khan Academy** | 유형·난이도 패턴 참고 | NCC WebSearch 즉시 사용 가능 | ✅ |
| **Desmos embed** | 그래프 대안 (JSXGraph 비교) | `<iframe>` embed, 별도 연동 불필요 | 🔲 필요 시 |

> **현재 검증 방식**: NCC 직접 풀이. Unit 1에서 버그 3건 발견·수정. 복잡한 계산 포함 문제가 많아질 경우 Wolfram Alpha MCP 도입 효과 있음.

---

## 11. HITL 포인트 전체 요약

| Phase | HITL 포인트 | 이유 |
|---|---|---|
| 1 | 개념 범위·깊이 확정 | 중1 수준 판단은 Nick만 가능 |
| 2 | 스토리 확정 (반복 가능) | 딸에게 맞는 감성·사실 검증 |
| 4 | 구조적 앱 변경 승인 | UX 방향은 Nick 판단 |
| 5-a | QN_source.md 확정 | 개념 커버리지 적합성 |
| 5-b | 유형 목록 확정 | 시험 맥락은 Nick만 파악 |
| 5-c | 수학 정확성 확인 | 오류가 딸에게 전달되면 안 됨 |
| 5-d | 수학 정확성 확인 | 오류가 딸에게 전달되면 안 됨 |

---

## 12. Batch 처리 계획

```mermaid
flowchart TD
    U1["Unit 1 완성<br>기준 확립"]
    U1 --> BATCH

    subgraph BATCH["Unit 2·3·4 Batch"]
        direction LR
        B1["Phase 1<br>/concept-review ×3<br>병렬 가능"]
        B2["Phase 2<br>/story-write ×3<br>순차·HITL 포함"]
        B4["Phase 4<br>NCC+app-reviewer ×3"]
        B5A["Phase 5-a<br>/problems-make ×3<br>QN_source.md 먼저"]
        B5BC["Phase 5-b,c<br>유형 확정 후 일괄"]
        B5D["Phase 5-d<br>딸 공부 시작 후<br>오답 발생 시 발동"]

        B1 --> B2 --> B4 --> B5A --> B5BC
        B5D -.->|"독립 트리거"| B5D
    end
```

---

*참조: CLAUDE.md / APP_PRINCIPLES.md / .claude/skills/ / .claude/agents/*
