<!-- 0509_workflow_v3_review.md -->
# Workflow v3 — 창의적·실효성·비판적 재평가

> 세션: 2026-05-09
> 대상: `10_docs/13_workflow_v3.md`
> 목적: v3 설계를 3가지 관점(창의적/실효성/비판적)으로 재평가하고 개선 방향과 미결 질문 제시.

---

# Round 1 — 재평가 보고

---

## A. 창의적 관점 (Creative)

> "이 설계가 더 잘 될 수 있는 방법은?"

---

### A-1. Commission Brief — Q&A가 아닌 "Assumption-first" 방식

**현재 설계:**
Nick에게 Q&A를 3가지 묻고 Brief를 만든다.

**더 나은 아이디어:**
Q&A 없이 Orchestrator가 먼저 **가정해서 전체 brief를 완성**하고, Nick에게는 "이렇게 가정했습니다. 틀린 것만 수정해주세요"라고 제시한다.

```
현재:
  Nick → Q1, Q2, Q3 답변 → Brief 생성

개선:
  Orchestrator → Brief 완성 (전부 가정) → Nick에게 제시
  Nick → "맞아" or "3번만 바꿔줘" → 실행
```

이것이 진짜 minimal friction이다. 질문 자체가 friction이다.

---

### A-2. NCC Audit — 단일 모델 self-review의 한계 극복

**현재 설계:**
NCC가 만든 것을 NCC가 검토 → 같은 모델, 같은 편향.

**창의적 접근:**
- **동일 프롬프트 × 다른 temperature 2회 실행** → 결과 불일치 시 Warn
- **app-reviewer와 /ncc-audit 역할 통합** (현재 중복)
- **딸의 반응(Phase 5 feedback/)을 다음 단원 audit 기준으로 피드백 루프**

```
Unit 1 결과 → 딸 반응 → audit 기준 보정 → Unit 2 audit에 반영
```

학습 피드백 루프가 있다면 audit이 점점 정교해진다.

---

### A-3. Phase 3 (수학언어) — 단원 내부가 아닌 공통 레이어로 승격

**현재:**
Phase 3는 단원별로 있지만 `40_BaseDocs/00_literacy/`에 저장.

**창의적 제안:**
Phase 3를 "단원 제작" 파이프라인 밖으로 완전히 분리.

```
MathTelling = [단원 파이프라인] + [수학언어 레이어 (별도 관리)]
```

수학언어 레이어는 `/literacy-make` 전용 Skill + 별도 유지 관리 사이클.
단원 파이프라인은 Phase 1, 2, 4, 5만 있는 것이 더 단순하다.

---

### A-4. commission/unitNN_brief.md — 실행 로그와 합치기

**현재:**
- commission brief → 실행 설정
- chatlog → 대화 기록
- 두 파일이 중복 관리된다.

**창의적 제안:**
commission brief를 chatlog의 **Round 0 (착수 섹션)**으로 통합.

```
chatlog/0509_unit02.md
  # Round 0 — Commission Brief
    (자동 생성)
  # Round 1 — Phase 1 결과
  # Round 2 — Phase 2 결과
  ...
```

파일 수를 줄이고 작업 흐름이 한 파일에서 보인다.

---

## B. 실효성 관점 (Effectiveness)

> "이 설계가 실제로 작동하는가?"

---

### B-1. Unit 1을 이 워크플로우로 돌렸다면 작동했을까?

Unit 1 재정비 과정을 돌아보면:

| 작업 | v3 설계 대로 됐나? |
|---|---|
| 개념 검수 | ✅ Phase 1 → /concept-review OK |
| 스토리 경로 수정 | ⚠️ Orchestrator가 경로 오류를 발견했을까? 불확실 |
| problems.html 수학 버그 3건 | ❌ /ncc-audit(math)가 잡았을까? 같은 모델이면 동일 오류 가능 |
| 합성수 정의 수정 | ✅ /ncc-audit(concept) + 개념 MD 비교로 가능 |
| sieve.html Big-O | ✅ /ncc-audit(app) + APP_PRINCIPLES.md로 가능 |

**결론:** math 버그는 self-audit으로 못 잡을 수 있다. 이것이 가장 큰 실효성 문제.

---

### B-2. "자율 진행" vs. "chatlog 라운드 기반" 긴장

v3 설계는 자율 진행을 전제하지만, CLAUDE.md는 "chatlog 라운드 기반 대화"를 핵심으로 한다.

**이 둘은 공존할 수 있는가?**

```
Option A: Orchestrator가 chatlog에 Round 단위로 기록하며 자율 진행
  → chatlog가 실행 로그 역할도 겸함
  → Nick이 언제든 개입 가능

Option B: Orchestrator가 독립 실행, 완료 후 요약 보고
  → chatlog에는 완료 요약만 기록
  → 중간 과정이 보이지 않음
```

Option A가 현재 프로젝트 방식과 일치한다. 그런데 v3에 이것이 명시되지 않았다.

---

### B-3. /ncc-audit이 실제로 실행되려면

현재 `/ncc-audit` 정의는 입출력이 있지만, **실제 skill 파일에 무엇이 들어가야 하는지** 불분명하다.

Skill 파일이 작동하려면:
1. 감사 유형별 기준 체크리스트가 있어야 함 (지금은 없음)
2. APP_PRINCIPLES.md가 기계적으로 읽을 수 있는 체크리스트 형식이어야 함
3. learner-profile.md가 "이 수준에 맞나?" 판단에 실제로 사용 가능한 형식이어야 함

**→ 선행 작업 필요: 기준 문서들을 audit-ready 체크리스트 형식으로 정비**

---

### B-4. Batch 처리 현실성

"Unit 2~4를 batch처럼 처리" 계획이 있다. 실제로 가능한 Batch와 불가능한 것:

| 작업 | Batch 가능 여부 |
|---|---|
| Phase 1 (개념 검수) × 3단원 | ✅ 완전 자동 가능 |
| Phase 2 (스토리) × 3단원 | ❌ 단원마다 Nick 스토리 확정 필요 |
| Phase 4 (앱 제작) × 3단원 | ⚠️ 부분 가능, 단원별 커스터마이징 있음 |
| Phase 5-b (유형 확정) × 3단원 | ❌ 단원마다 Nick 판단 필요 |

"Batch"라는 단어가 기대치를 과장하고 있다. "병렬 준비 + 단원별 HITL 게이트"가 더 정확한 표현이다.

---

### B-5. problems.html 경로 불일치

현재 설계:

| 파일 | 위치 |
|---|---|
| problems.html (기본문제, 5-a) | `50_units/NN/app/problems.html` |
| types.md (5-b) | `50_units/NN/problems/types.md` |
| type_NN_app.html (5-c) | `50_units/NN/problems/type_NN_app.html` |
| QN_app.html (5-d) | `50_units/NN/problems/QN_app.html` |

problems.html만 `app/`에 있고 나머지는 `problems/`에 있다. 이유가 있는가?

Unit 1처럼 기존에 만든 것이라 `app/`에 있는 것. 신규 단원부터는 모두 `problems/`로 통일하는 것이 좋을 수 있다.

---

## C. 비판적 관점 (Critical)

> "이 설계의 가정이 틀렸다면?"

---

### C-1. 가장 큰 가정: NCC는 중1 딸에게 맞는 콘텐츠를 판단할 수 있다

NCC Audit이 `learner-profile.md`를 기준으로 콘텐츠가 딸에게 맞는지 판단한다고 가정한다.

**이 가정이 성립하는 범위:**
- 텍스트 수준 (단어 난이도, 문장 길이) → 가능
- 수학 개념 수준 (중1 교육과정 기준) → 가능

**이 가정이 성립하지 않는 범위:**
- "딸이 이 스토리를 좋아할까?" → 불가능
- "딸이 이 문제 수준에서 자신감을 얻을까?" → 불가능
- "딸의 현재 감정 상태에 맞는 학습량인가?" → 불가능

→ **NCC Audit은 규칙 기반 검토까지만 가능. 딸과의 맞춤은 Nick 몫.**

이것을 v3가 충분히 명시하지 않는다.

---

### C-2. Orchestrator가 "자율 진행"하면 chatlog는 누가 읽는가?

현재 설계에서 Orchestrator는 자율 실행한다. 하지만:
- Nick이 중간에 읽고 싶을 때 어디를 봐야 하는가?
- Orchestrator가 chatlog에 라운드를 써야 한다면, 그 라운드는 언제 작성되는가?
- 완료 후 요약 보고만 있다면, Nick이 프로세스를 신뢰할 수 있는가?

**→ Orchestrator의 가시성(visibility) 정책이 없다.**

---

### C-3. unit-orchestrator는 너무 많은 것을 안다

Orchestrator가 알아야 하는 것:
- CLAUDE.md 전체
- 모든 Phase의 I/O
- 모든 Skill/Agent 호출 방법
- /ncc-audit 결과 해석
- HITL 판단 기준

**이것이 하나의 agent로 구현 가능한가?**

현실적으로 Orchestrator는 매우 긴 system prompt가 필요하다. 컨텍스트 한계나 지시 충돌 가능성이 있다.

**대안:** Orchestrator는 "라우터"만 담당하고, 각 Phase는 전용 sub-agent가 처리한다.

```
unit-orchestrator (라우터)
  └─ phase1-agent (개념 전문)
  └─ phase2-agent (스토리 전문)
  └─ phase4-agent (앱 전문)
  └─ phase5-agent (문제 전문)
```

→ 과도한 설계일 수 있다. 지금은 Orchestrator가 "명시적으로 정의된 단일 agent"이면 충분하다.

---

### C-4. /ncc-audit와 app-reviewer의 역할 중복

현재:
- `app-reviewer` Agent: HTML 앱을 APP_PRINCIPLES.md 기준으로 검토
- `/ncc-audit(app)`: 앱을 APP_PRINCIPLES.md 기준으로 Pass/Warn/Fail 판정

이 둘은 사실상 같은 작업을 한다. 중복이다.

**정리 필요:**
- Option A: `/ncc-audit(app)` = app-reviewer를 호출하는 wrapper
- Option B: app-reviewer를 `/ncc-audit`에 통합
- Option C: app-reviewer는 Phase 4 전용, /ncc-audit는 Phase 5 문제 앱 전용

---

### C-5. "처음에 Nick은 아주 간단하게 의뢰" — 실제로 몇 단어인가?

"unit 02 만들어"가 충분한 의뢰인가?

Orchestrator가 CLAUDE.md에서 모든 단원 정보를 읽을 수 있다면 → 충분하다.

하지만 CLAUDE.md에 없는 경우:
- 새로운 인물 배정
- Phase 범위 변경 (예: Phase 5 제외)
- 특별 지시 (예: "이 단원은 게임 요소 추가해줘")

이런 경우 Q&A가 3개를 초과할 수 있다. **"3개 이내"는 일반 케이스에만 해당.**

---

### C-6. Phase 5-d (오답노트)는 Orchestrator와 독립적이어야 한다

Phase 5-d는 "딸이 실제로 틀렸을 때" 발동한다.
이것은 단원 제작 파이프라인(Phase 0~5-c)과 별개의 트리거다.

**현재 v3의 문제:**
Phase 5-d가 마치 Phase 5-c 다음에 자연스럽게 오는 것처럼 그려져 있다.

**실제:**
```
[단원 제작 파이프라인]   ← unit-orchestrator 관장
Phase 0 → 1 → 2 → 4 → 5-a → 5-b → 5-c

[오답 대응 파이프라인]   ← 독립적, 별도 트리거
딸의 오답 → math-workflow → 5-d 산출물
```

이 두 파이프라인은 **완전히 분리**되어야 한다.

---

## D. 컴포넌트별 재평가 요약

| 컴포넌트 | 평가 | 주요 이슈 |
|---|---|---|
| unit-orchestrator | ✅ 방향 맞음 | 가시성 정책 미정, 컨텍스트 한계 가능성 |
| /ncc-audit | ⚠️ 방향 맞지만 한계 명확 | 수학 버그는 self-audit으로 못 잡음 |
| Commission Brief | ✅ 좋은 아이디어 | chatlog와 통합하면 더 단순 |
| HITL Optional | ✅ 맞는 방향 | 필수 2가지가 충분한지 재검토 필요 |
| Phase 5-d 위치 | ❌ 잘못됨 | 단원 파이프라인과 분리 필요 |
| Batch 처리 | ⚠️ 과장됨 | "병렬 준비 + 단원별 HITL"로 표현 수정 |
| app-reviewer 중복 | ❌ 중복 | /ncc-audit(app)와 통합 방안 결정 필요 |
| problems.html 경로 | ⚠️ 불일치 | 신규 단원부터 problems/ 통일 검토 |

---

## E. 질문 목록 — Nick 리뷰

### [구조 결정 필요]

**E-1.** Commission Brief와 chatlog를 통합할까요?
- 현재: commission/ + chatlog/ 별도 파일
- 제안: chatlog의 Round 0가 commission brief 역할
- → 파일 수 줄이고 흐름 한 파일에서 확인 가능

(Nick) Yes

**E-2.** Phase 5-d (오답노트)를 단원 파이프라인에서 완전히 분리할까요?
- 현재 v3: Phase 5-a~d가 연속으로 그려짐
- 제안: 단원 파이프라인(0~5-c)과 오답 대응(5-d, 별도 트리거)을 명확히 분리
- → math-workflow가 Orchestrator와 독립적으로 존재하는 것이 맞음

(Nick) 분리 하지 않고 inloop 로 처리. 여기서는 오답노트 보다는 "한 유형의 문제 대해서 깊이 탐구"하는 flow 임. 이미 문제 생성 단계에서 중간 이상 난이도 문제들의 유형이 다양하게 존재해야 함. 그러면 각 유형의 문제에 대해서 혼자서 깊이있게 공부할 수 있는 추가 자료 및 문제가 생성되는 과정임. 너무 쉬운문제들은 이 flow 불필요. in the loop 가 핵심임.  
용어 수정 : math-workflow 라는 말은 우리 전체 업무를 아우르는 것 같음. 이름 적절히 수정 필요

**E-3.** app-reviewer와 /ncc-audit(app)의 중복을 어떻게 해결할까요?
- A: /ncc-audit(app)이 app-reviewer를 내부 호출
- B: app-reviewer를 /ncc-audit으로 통합
- C: app-reviewer(HTML 앱 전용) / /ncc-audit(MD·개념·수학 전용) 역할 분리

(Nick) agent 보다는 skill 로 "/ncc_audit" 이 필요없고, /ncc_audit_math, /ncc_audit_concept, /ncc_audit_app, /ncc_audit_problem, /ncc_audit_story 이런식으로 세분화 되어서 존재하고, app-reviewer 가 /ncc_audit_app 과 통합되면 좋을 것 같음. 생각이 다르면 얘기해주세욤.
---

### [설계 철학 확인]

**E-4.** Orchestrator의 "가시성" 수준은?
- A: 각 Phase 완료마다 chatlog에 자동 기록 (Nick이 언제든 볼 수 있음)
- B: 완료 후 요약 보고만 (빠르지만 중간 과정 불투명)
- → Nick이 중간에 개입하려면 A가 필요

(Nick) A absolutely

**E-5.** 필수 HITL 2가지 (스토리, 유형) — 충분한가요?
- 스토리: NCC 자체 판단 가능한 기준이 있으면 optional로 해도 되는가?
- 유형: 교육과정 기준만 있으면 NCC가 초안을 신뢰할 수 있는가?
- → 아니면 이 2가지는 반드시 Nick이 확인해야 하는 이유가 있는가?

(Nick) HITL 필수는 존재하지 않음. 모두 NCC 가 자체적으로 진도 나갈 수 있음. 나중에 실제로 딸과 공부하면서 모자란/이상한 부분을 발견한다면 chatlog 등의 문서들과 만들어진 markdown/app 등을 따라가보면서 재수정 round 를 진행하는 것이 쉬우면 됨. 각 만들어질 문서들 체계적 정리가 중요함.

**E-6.** NCC Audit 수학 검증의 한계를 어떻게 보완할 건가요?
- NCC가 만든 수학 문제를 NCC가 검증 → 동일 오류 반복 가능성
- Unit 1에서 이미 3건 발생
- 옵션: A. Wolfram Alpha MCP 도입, B. Nick이 수학만 확인, C. 허용 오류율 인정

(Nick) A. Wolfram Alpha MCP 도입이 가장 효과적일 것 같음.
"Wolfram Alpha 는 무엇인가? 왜 이 mcp 를 여기서 사용하나? 확장된 활용처는? 대체제는?" 에 대한 답 및 우리는 해당 mcp 를 사용한다는 guide 문서를 하나 만들어 주길. 10_docs/ 내부에 저장. 이 앱의 수준에서는 무료플랜 사용 가능한지도 궁금함.  
---

### [실행 우선순위]

**E-7.** unit-orchestrator와 /ncc-audit을 지금 당장 구현해야 할까요?
- Unit 1은 이미 chatlog 라운드 방식으로 잘 진행됨
- Unit 2 전에 구현하면 batch 처리에 실질적 도움이 됨
- 아니면 Unit 2를 수동으로 한 번 더 진행하면서 Orchestrator 설계를 실전 검증한 뒤 구현?

(Nick) 작업 순서
1. NCC 가 workflow_v4 생성, 그리고 각 agent, skill 구현 (기존에 생성한 앞으로는 불필요한 것들 archive dir 하나 만들어서 옮기기) - 이때 별도 chatlog 에서 진행
2. Nick 이 모두 리뷰 예정, 필요하면 1번 단계 refine loop 진행. 나는 agent 는 단 하나만 존재하고 나머지는 skill 로 구현되면 좋을 것 같음. 
3. unit 1 을 backup 하고 처음부터 다시 만들기... --> 이러면 내가 before/after 비교가 쉬워서 품질과 생성에 걸린 시간 등을 잘 알 수 있음.
4. unit 2 부터 batch 진행. unit 2 완성 -> unit 3 완성 이런 식일지? 혹은 모든 unit 의 phase a 완료 후 phase b 완료 이런식으로 진행할지 궁금함.


**E-8.** problems.html 경로를 Unit 2부터 problems/로 통일할까요?
- 현재 Unit 1: `app/problems.html`
- 제안: Unit 2부터 `problems/problems.html` (또는 `problems/basic_app.html`)
- 일관성 vs. 기존 유지

(Nick) unit 1 부터 새로 만들어낼 예정이고 적절한 naming 을 적용해야 함.

---

### [부가 아이디어 — 가능성 검토]

**E-9.** 딸의 반응(feedback/)을 다음 단원 audit 기준으로 활용하는 피드백 루프 — 관심 있으신가요?
- 딸이 feedback/ 폴더에 글을 쓰면 NCC가 읽고 다음 단원 learner-profile 업데이트
- 시스템이 딸에 맞게 점점 정교해짐

(Nick) 좋은 생각임. 가능하게 해주세요. 

**E-10.** Phase 3 (수학언어)를 단원 파이프라인에서 완전히 분리해 별도 유지 관리 사이클로 운영하는 것을 고려하실 의향이 있으신가요?
- 현재: 단원마다 Phase 3 있음
- 제안: 수학언어 레이어를 독립 관리 (단원과 비동기)

(Nick) "수학언어 레이어를 독립 관리 (단원과 비동기)" 좋습니다. 그런데 각 단원의 내용을 만들어 나갈때 '수학언어' 새로운 업데이트 추가가 필요한지 확인하고 실제로 수정하는 작업을 진행해야겠네요. 내가 별도의 agent 를 실행시키고 싶지는 않아요..

Ochestrator 가 처음 작업 의뢰를 받고 세부 사항 정리해가는 template 포함해서 NCC 가 필요로 하는 각종 문서 제대로 정리되어야 함. (여기엔 agent, skill and reference doc as context, claude.md 모두 포함함) 
이 전 과정을 기술적인 측면에서 (workflow 설계 엔지니어 측면) 바라보는 어떤 문서, 
기술을 모르지만 이 workflow 로 자료를 만들어내는 수학선생님 관점에서의 문서, 
이것을 사용하는 user(학생) 입장에서의 문서들이 존재하면 좋겠습니다. 체계적으로 정리 바랍니다.
---

> (Nick): (답변 완료 — 위 E-1~E-10 참조)

---

# Round 2 — Nick 답변 요약 및 다음 세션 작업 계획

## 확정 결정사항 (E-1~E-10)

| 항목 | 결정 |
|---|---|
| E-1. Brief+chatlog 통합 | ✅ chatlog Round 0 = commission brief |
| E-2. Phase 5-d 분리 | ❌ 분리 안 함. "유형 깊이 탐구" in-loop. math-workflow **이름 변경 필요** |
| E-3. audit 세분화 | `/ncc_audit_math` `/ncc_audit_concept` `/ncc_audit_app` `/ncc_audit_problem` `/ncc_audit_story` 5개 skill로 분리. app-reviewer → `/ncc_audit_app` 통합 |
| E-4. 가시성 | Phase 완료마다 chatlog 자동 기록 (Option A) |
| E-5. 필수 HITL | **없음**. NCC 전체 자율 진행. 딸과 공부 후 재수정 round로 보완. 문서 체계 정리가 핵심 |
| E-6. 수학 검증 | **Wolfram Alpha MCP 도입**. 10_docs/에 가이드 문서 작성 (개념·용도·무료플랜 여부 포함) |
| E-7. 구현 순서 | 아래 "다음 세션 작업 순서" 참조 |
| E-8. problems 경로 | Unit 1부터 새로 만들 예정. 적절한 naming 적용 |
| E-9. 딸 피드백 루프 | ✅ 구현. feedback/ → learner-profile 업데이트 |
| E-10. Phase 3 독립 | ✅ 단원과 비동기 독립 관리. 단, 별도 agent 아님 — Orchestrator 내에서 필요 시 확인·수정 |

---

## 추가 확정사항 (E-7 상세 + 추가 요청)

### Agent/Skill 아키텍처
- **Agent**: 단 하나 (`unit-orchestrator`)
- **나머지 전부 Skill** (phase별 ncc_audit × 5 포함)

### 다음 세션 작업 순서

```
Step 1: workflow_v4.md 생성 + 모든 agent/skill 구현
  - 기존 불필요 파일 → archive/ 이동
  - 별도 chatlog 세션으로 진행
  - Agent: unit-orchestrator 1개만
  - Skill: /ncc_audit_* × 5 (app-reviewer 통합)

Step 2: Nick 리뷰 + refine loop

Step 3: Unit 1 backup → 처음부터 재제작 (before/after 비교)

Step 4: Unit 2 batch 시작
  - 방식 미결: 단원별 순차 (unit2 → unit3) vs 전체 phase별 (모든 unit phase1 → phase2 ...)
```

### 문서 체계 (추가 요청)
3가지 관점의 문서를 별도 작성:

| 문서 | 대상 독자 | 위치 (예정) |
|---|---|---|
| 엔지니어 관점 | workflow 설계자 (기술 상세) | `10_docs/` |
| 선생님 관점 | 기술 모르는 수학 선생님 (사용법 중심) | `10_docs/` |
| 학생 관점 | 딸 (어떻게 사용하는가) | `10_docs/` |

### Wolfram Alpha MCP 가이드 문서
- 내용: 개념 / 왜 사용하나 / 확장 활용처 / 대체제 / 무료 플랜 여부
- 위치: `10_docs/` (번호 미정)

### Orchestrator 작업 의뢰 template
- CLAUDE.md, agent, skill, reference doc 포함한 전체 컨텍스트 정리

---

## 다음 세션 시작 방법

새 chatlog 파일 생성: `0509_workflow_v4_impl.md`

NCC가 할 일:
1. `10_docs/14_workflow_v4.md` 생성 (위 결정사항 반영)
2. `.claude/agents/unit-orchestrator.md` 구현
3. `.claude/skills/ncc_audit_*.md` × 5 구현 (app-reviewer 통합)
4. `10_docs/` Wolfram Alpha MCP 가이드 작성
5. 불필요 기존 파일 archive 이동
6. 3관점 문서 작성

> (Nick):
