<!-- 10_docs/14_workflow_v4.md -->
# MathTelling — Workflow v4 (확정판)

> 마지막 업데이트: 2026-05-09
> 출처: `0509_workflow_v3_review.md` E-1~E-10 결정사항 전부 반영.
> 참조 관점: `20_guide_engineer.md` / `21_guide_teacher.md` / `22_guide_student.md`

---

## 1. v3 → v4 핵심 변경

| 항목 | v3 | v4 |
|---|---|---|
| Commission Brief | 별도 파일 | chatlog Round 0으로 통합 |
| 필수 HITL | 스토리·유형 2가지 | **없음** — NCC 전체 자율 진행 |
| app-reviewer | Agent | `/ncc_audit_app` Skill으로 흡수 |
| NCC Audit | 단일 `/ncc-audit` | 5개 전문 Skill로 세분화 |
| math-workflow | 오답노트 전용 Agent | `/type-explorer` Skill (유형 깊이 탐구) |
| Phase 5-d | 별도 독립 파이프라인 안 | Phase 5 in-loop |
| Phase 3 (수학언어) | 단원별 포함 | 단원과 비동기 독립 관리 |
| Agent 수 | 2개 (app-reviewer + math-workflow) | **1개** (`unit-orchestrator`) |

---

## 2. 시스템 구성도

```
Nick ─── "unit 02 만들어" ────► unit-orchestrator (유일한 Agent)
                                         │
                               ┌─────────┴──────────────────────┐
                               │  chatlog Round 0 (Brief 자동생성) │
                               │  Nick: 틀린 가정만 수정해주세요      │
                               └────────────────────────────────┘
                                         │
                            ┌────────────▼────────────┐
                            │  Phase 0 → 1 → 2 → 4    │
                            │       → 5-a → 5-b → 5-c │
                            └────────────┬────────────┘
                                         │
                            각 Phase 완료 → chatlog Round N 기록
                            (Nick이 언제든 확인 가능)
                                         │
                            ┌────────────▼────────────┐
                            │  Phase 5 in-loop        │
                            │  특정 유형 깊이 탐구 필요 시 │
                            │  → /type-explorer 호출    │
                            └─────────────────────────┘
                                         │
                            [수학 언어 레이어 — 비동기]
                            Phase 1 완료 후 Orchestrator가
                            literacy 업데이트 필요 여부 확인
                            → 필요 시 /math-figure 호출
```

---

## 3. Commission Process (착수 방법)

### 3-1. 의뢰 형태
Nick이 한 줄로 의뢰:
```
"unit 02 만들어"
"unit 03 Phase 2부터 해줘"
"unit 02 Phase 1만"
```

### 3-2. chatlog Round 0 — Commission Brief

`unit-orchestrator`가 CLAUDE.md 기반으로 Brief를 자동 작성하고 Nick에게 확인 요청:

```markdown
# Round 0 — Commission Brief (자동 생성)

## 단원 정보
- 단원: 02_정수와유리수
- 인물: 브라마굽타
- 디렉토리: 50_units/02_정수와유리수/

## 실행 범위
Phase 0 (디렉토리), 1 (개념), 2 (스토리),
4 (앱), 5-a (기본문제), 5-b (유형), 5-c (연습)

## 가정 (틀린 것만 수정해주세요)
- 전체 Phase 실행
- 인물: 브라마굽타 (기존 배정 유지)
- 기본문제: 8~10문제
- APP_PRINCIPLES.md + 중1 교육과정 적용

> (Nick): 맞아 / 또는 "Phase 4까지만"
```

Nick이 "맞아" 또는 수정사항 전달 → 실행 시작.

---

## 4. Phase별 I/O 명세

### Phase 0 — 디렉토리 초기화

| 항목 | 내용 |
|---|---|
| 입력 | 단원번호 |
| 도구 | `/unit-plan` Skill |
| 산출물 | `50_units/NN/{story,app,video,problems,feedback}/` |
| chatlog | Round 0 (Commission Brief) |

---

### Phase 1 — 개념 (축 A)

| 항목 | 내용 |
|---|---|
| 입력 | `40_BaseDocs/NN_단원명/` MD 파일들 |
| 도구 | `/concept-review` Skill |
| 작업 | 정확성·수준·범위 검수 + 보완 |
| audit | `/ncc_audit_concept` |
| 산출물 | 보완된 MD + 검수 보고 |
| chatlog | Round 1 |
| Phase 3 체크 | 새로운 수학 언어 업데이트 필요 여부 판단 |

---

### Phase 2 — 이야기 (축 B)

| 항목 | 내용 |
|---|---|
| 입력 | 단원번호, 인물명, `20_research/02_R2-people-map.md` |
| 도구 | `/story-write` Skill |
| 작업 | 인물 리서치 + 스토리 초안 생성 |
| audit | `/ncc_audit_story` |
| 산출물 | `50_units/NN/story/unitNN.md` |
| chatlog | Round 2 |

---

### Phase 3 — 수학 언어 (축 C, 비동기 독립 관리)

단원 파이프라인과 분리. `unit-orchestrator`가 Phase 1 완료 후 판단:

```
Phase 1 완료
  → Orchestrator: "이 단원의 핵심 기호·표기 중 40_BaseDocs/00_literacy/ 업데이트 필요한 것 있나?"
  → 있으면: /math-figure 호출 → 40_BaseDocs/00_literacy/LN_*/
  → 없으면: 패스 (Phase 2로 계속)
```

별도 agent 없음. Orchestrator 내부에서 처리.

---

### Phase 4 — 인터랙티브 앱 (축 A+B 통합)

| 항목 | 내용 |
|---|---|
| 입력 | Phase 1 개념 MD + Phase 2 스토리 |
| 도구 | NCC 직접 제작 → `/ncc_audit_app` |
| 앱 종류 | `index.html`, `story.html`, `concepts.html` + 단원 특수 앱 |
| 산출물 | `50_units/NN/app/*.html` |
| chatlog | Round 4 |

---

### Phase 5-a — 기본문제

| 항목 | 내용 |
|---|---|
| 입력 | `QN_source.md` |
| 도구 | NCC 직접 생성 → `/ncc_audit_math` → `/ncc_audit_app` |
| 목적 | 단원 핵심 개념 고루 확인 (8~10문제) |
| 산출물 | `50_units/NN/problems/basic_app.html` |
| chatlog | Round 5a |

---

### Phase 5-b — 유형 목록

| 항목 | 내용 |
|---|---|
| 입력 | 단원 개념 + 교과서 기출 패턴 |
| 도구 | NCC 초안 → `/ncc_audit_problem` |
| 목적 | 시험에 나올 법한 유형 목록 확정 |
| 산출물 | `50_units/NN/problems/types.md` |
| chatlog | Round 5b |

---

### Phase 5-c — 유형별 연습

| 항목 | 내용 |
|---|---|
| 입력 | `types.md` + 각 유형 문제 |
| 도구 | `/math-practice` Skill → `/ncc_audit_math` → `/ncc_audit_app` |
| 목적 | 유형별 × 중급 이상 (3/3/3 원칙) |
| 3/3/3 | L×3 + M×3 + H×3 = 유형당 9문제 |
| 산출물 | `50_units/NN/problems/type_NN_app.html` |
| chatlog | Round 5c |

---

### Phase 5-d — 유형별 깊이 탐구 자료

**단원 제작 파이프라인의 일부** — 딸의 학습 반응과 무관하게 단원 생성 시점에 만들어진다.
Phase 5-c에서 중간+ 난이도 유형이 확보된 직후 실행.

| 항목 | 내용 |
|---|---|
| 입력 | `types.md` + `type_NN_app.html` (5-c 결과) |
| 도구 | `/type-explorer` Skill |
| 목적 | 각 유형을 혼자서 깊이 공부할 수 있는 심화 자료 |
| 생성 조건 | M 또는 H 문제가 있는 유형만. L만 있는 기본형은 skip. |
| 산출물 | `50_units/NN/problems/deep_*.html` |
| chatlog | Round 5d |

**통합 앱 기준:**
- 같은 개념 체계 유형(예: GCD·LCM·관계식, 비례식·비율)은 탭 구조 단일 앱으로 통합
- 호출: `/type-explorer unitNN 유형A 유형B` (관련 유형명을 함께 전달)
- 파일명: `deep_유형A_유형B_app.html` 또는 의미 있는 통합명
- 독립 유형 또는 단독으로 복잡한 유형 → 별도 앱 유지

**각 deep 앱 포함 내용:**
- 이 유형이 어려운 이유 + 핵심 아이디어
- 단계별 풀이 흐름 (클릭으로 단계 공개)
- 자주 하는 실수 패턴
- 추가 문제 3~5개 (점진적 난이도, 5-c와 겹치지 않음)
- 연결 개념 (이 유형 이해 후 무엇이 쉬워지나)

---

## 5. 수학 검증 체계

### 기본: NCC 직접 풀이
모든 수학 문제는 NCC가 풀이 전개 후 정답 확인. 보기 있으면 오답 보기도 교차 확인.

### 보조: Wolfram Alpha MCP
- 목적: NCC 풀이 결과 독립 검증 (동일 모델 self-audit 한계 보완)
- 도입 배경: Unit 1에서 self-audit으로 잡지 못한 수학 버그 3건 발생
- 활용 지점: `/ncc_audit_math` Skill 내부
- 상세: `10_docs/15_wolfram_alpha_guide.md`

### 판정 기준
| 결과 | 의미 | 처리 |
|---|---|---|
| Pass | 정답 확인 | 문제 확정 |
| Warn | 계산 모호성 | NCC 재풀이 후 재판정 |
| Fail | 오류 확인 | 문제 수정 또는 폐기 |

---

## 6. NCC Audit Skill 명세

| Skill | 기준 문서 | 검토 대상 | Phase |
|---|---|---|---|
| `/ncc_audit_app` | APP_PRINCIPLES.md | HTML 앱 파일 | 4, 5 |
| `/ncc_audit_math` | 중1 교육과정, Wolfram Alpha | 수학 문제·풀이·정답 | 5 |
| `/ncc_audit_concept` | learner-profile.md, 교육과정 | 개념 MD 수준·범위 | 1 |
| `/ncc_audit_problem` | 문제 출제 원칙 | 문제 커버리지·난이도 분포 | 5 |
| `/ncc_audit_story` | learner-profile.md | 스토리 톤·사실성·적합성 | 2 |

---

## 7. 딸 피드백 루프

```
딸이 학습 후 → 50_units/NN/feedback/에 글 작성
                   ↓
  (자동) Orchestrator or Nick이 /ncc_audit_story 호출
                   ↓
  피드백 내용 분석 보고서 생성
  → 10_docs/01_learner-profile.md 업데이트 권고
                   ↓
  Nick 확인 후 learner-profile.md 업데이트
                   ↓
  다음 단원 audit 기준에 자동 반영
```

**원칙:**
- 딸의 글 원본 수정 절대 금지
- 분석은 별도 파일에 추가
- learner-profile.md 업데이트 항목: 흥미 패턴, 어려움 유형, 반응 톤

---

## 8. 가시성 정책 (Orchestrator Visibility)

- Phase 완료마다 chatlog에 Round 기록
- Nick이 중간에 chatlog를 보면 현재 상태 즉시 파악 가능
- Orchestrator가 불확실하거나 오류 발생 시:
  - chatlog에 상황 기록
  - 중단 후 Nick 확인 대기 (자동 진행 안 함)
- 자율 진행이지만 **언제든 Nick이 개입 가능한 투명한 구조**

---

## 9. Agent / Skill 전체 카탈로그

### Agent (1개)

| Agent | 역할 | 호출 방법 |
|---|---|---|
| `unit-orchestrator` | 단원 전체 파이프라인 관장 (Commission → Phase 0~5d) | "unit NN 만들어" |

### Skills

| Skill | Phase | 역할 | 산출물 |
|---|---|---|---|
| `/unit-plan` | 0 | 디렉토리 초기화 | `50_units/NN/` 구조 |
| `/concept-review` | 1 | 개념 MD 검수·보완 | 보완된 MD |
| `/story-write` | 2 | 인물 서사 초안 | `story/unitNN.md` |
| `/math-figure` | 3, 5 | 그래프·도형 시각화 | SVG / JSXGraph 인라인 |
| `/math-practice` | 5-c | 유형별 연습 문제 (3/3/3) | `type_NN_app.html` |
| `/type-explorer` | 5-d | 유형별 깊이 탐구 자료 (제작 파이프라인, M+유형만) | `deep_유형명_app.html` |
| `/ncc_audit_app` | 4, 5 | HTML 앱 품질 (APP_PRINCIPLES 기준) | 검토 보고 + 수정 |
| `/ncc_audit_math` | 5 | 수학 정확성 (Wolfram 보조) | Pass/Warn/Fail |
| `/ncc_audit_concept` | 1 | 개념 수준·범위 | 검토 보고 |
| `/ncc_audit_problem` | 5 | 문제 커버리지·난이도 | 검토 보고 |
| `/ncc_audit_story` | 2, feedback | 스토리 적합성 | 검토 보고 |
| `/video-make` | 4 | 영상 제작 파이프라인 | `video/*.mp4` |
| `/figcrop` | 5 | 시험지 이미지 크롭 | 크롭 이미지 |
| `/math-error-note` | ad-hoc | 오답노트 (Nick 수동 호출, 파이프라인 외) | `QN.md` + `QN_app.html` |

---

## 10. 파일 명명 규칙 (확정)

| 파일 유형 | 경로 |
|---|---|
| 스토리 텍스트 | `50_units/NN/story/unitNN.md` |
| 인덱스 앱 | `50_units/NN/app/index.html` |
| 스토리 앱 | `50_units/NN/app/story.html` |
| 개념 앱 | `50_units/NN/app/concepts.html` |
| 기본문제 앱 | `50_units/NN/problems/basic_app.html` |
| 유형 목록 | `50_units/NN/problems/types.md` |
| 유형 연습 앱 | `50_units/NN/problems/type_NN_app.html` |
| 유형 깊이 탐구 앱 | `50_units/NN/problems/deep_typeNN_app.html` |
| 오답노트 MD | `50_units/NN/problems/QN.md` |
| 오답노트 앱 | `50_units/NN/problems/QN_app.html` |
| 딸의 피드백 | `50_units/NN/feedback/` (수정 금지) |

---

## 11. Batch 처리 방식 (Unit 2~4)

"Batch"는 **병렬 준비 + 단원별 게이트 통과** 방식:

```
Phase 1: /concept-review × 3단원 — 자동, 순차
Phase 2: /story-write × 3단원 — 자동 생성
Phase 4: NCC 앱 × 3단원 — 자동 + /ncc_audit_app
Phase 5: 기본문제 × 3단원 — 자동 + 검증
```

**진행 방식 (Nick 선택):**
- **단원별 순차**: unit2 완성 → unit3 → unit4 (단원 단위 완성)
- **Phase별 일괄**: 모든 단원 Phase 1 → 모든 단원 Phase 2 → ...

추천: Phase 1~2는 일괄 빠르게, Phase 4~5는 단원별로 검토하며 진행.

---

## 12. 참조 문서

| 문서 | 대상 독자 |
|---|---|
| `10_docs/20_guide_engineer.md` | workflow 설계자 (기술 상세) |
| `10_docs/21_guide_teacher.md` | 기술 모르는 수학 선생님 (사용법 중심) |
| `10_docs/22_guide_student.md` | 딸 (어떻게 사용하는가) |
| `10_docs/15_wolfram_alpha_guide.md` | Wolfram Alpha MCP 도입 가이드 |

---

*참조: CLAUDE.md / APP_PRINCIPLES.md / .claude/agents/ / .claude/skills/*
