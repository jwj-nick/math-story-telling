<!-- 10_docs/20_guide_engineer.md -->
# MathTelling — 엔지니어 관점 가이드

> 대상: Nick (워크플로우 설계자, 기술 상세 참조용)
> 마지막 업데이트: 2026-05-09

---

## 1. 시스템 아키텍처 개요

MathTelling은 **Claude Code 기반 자율 콘텐츠 생성 파이프라인**이다.

```
[Nick] ── 자연어 의뢰 ──► [unit-orchestrator Agent]
                                  │
              ┌───────────────────┼──────────────────────┐
              ▼                   ▼                      ▼
         Skills 호출          파일 I/O              chatlog 기록
    /concept-review          Read/Write/Edit      00_project_hub/
    /story-write             Glob/Grep            chatlog/YYMMDD_unitNN.md
    /math-practice           ...
    /ncc_audit_* × 5
    ...
```

**단일 Agent, 복수 Skill** 구조:
- Agent = 1개 (`unit-orchestrator`) — 파이프라인 전체 관장
- Skill = 13개 — 단일 작업 단위, Agent가 호출

---

## 2. Agent / Skill 기술 명세

### unit-orchestrator (Agent)

| 항목 | 내용 |
|---|---|
| 파일 위치 | `.claude/agents/unit-orchestrator.md` |
| 도구 | Read, Write, Edit, Bash, Glob, Grep, Agent |
| 입력 | Nick의 자연어 의뢰 ("unit 02 만들어") |
| 출력 | 단원 전체 산출물 + chatlog 업데이트 |
| 상태 관리 | chatlog Round-N 방식 (파일 기반) |

**실행 흐름:**
```
1. CLAUDE.md + 컨텍스트 문서 읽기
2. chatlog Round 0 (Commission Brief) 작성
3. Nick 응답 확인 (또는 30초 후 가정 진행)
4. Phase 0 → 1 → [3 check] → 2 → 4 → 5a → 5b → 5c 순차 실행
5. 각 Phase 후: /ncc_audit_* 실행 → chatlog Round N 기록
6. 완료 보고
```

---

### Skills 기술 명세

| Skill | 파일 위치 | 입력 | 주요 출력 | 사용 Phase |
|---|---|---|---|---|
| `/unit-plan` | `.claude/skills/unit-plan/SKILL.md` | 단원번호 | 디렉토리 구조 | 0 |
| `/concept-review` | `.claude/skills/concept-review/SKILL.md` | 단원번호 | 보완된 MD | 1 |
| `/story-write` | `.claude/skills/story-write/SKILL.md` | 단원명, 인물명 | story/unitNN.md | 2 |
| `/math-figure` | `.claude/skills/math-figure/SKILL.md` | 개념명 | SVG/JSXGraph | 3, 5 |
| `/math-practice` | `.claude/skills/math-practice/SKILL.md` | 문제번호, 단원 | type_NN_app.html | 5c |
| `/math-error-note` | `.claude/skills/math-error-note/SKILL.md` | 문제번호 | QN.md + QN_app.html | 5 in-loop |
| `/ncc_audit_app` | `.claude/skills/ncc_audit_app/SKILL.md` | HTML 파일경로 | 검토+수정 | 4, 5 |
| `/ncc_audit_math` | `.claude/skills/ncc_audit_math/SKILL.md` | HTML/MD 경로 | Pass/Warn/Fail | 5 |
| `/ncc_audit_concept` | `.claude/skills/ncc_audit_concept/SKILL.md` | 단원번호 | 검토 보고 | 1 |
| `/ncc_audit_problem` | `.claude/skills/ncc_audit_problem/SKILL.md` | 파일경로 | 검토 보고 | 5 |
| `/ncc_audit_story` | `.claude/skills/ncc_audit_story/SKILL.md` | 단원번호 | 검토 보고 | 2, feedback |

### type-explorer (Agent)

| 항목 | 내용 |
|---|---|
| 파일 위치 | `.claude/agents/type-explorer.md` |
| 트리거 | 딸이 특정 유형 반복 오답 / Nick 명시 요청 |
| 입력 | 단원번호 + 유형명 |
| 출력 | deep_유형명.md + deep_유형명_app.html |

---

## 3. 파일 I/O 전체 맵

### 입력 파일 (읽기 전용)

| 파일 | 사용처 |
|---|---|
| `CLAUDE.md` | Orchestrator 컨텍스트 |
| `APP_PRINCIPLES.md` | /ncc_audit_app 기준 |
| `10_docs/01_learner-profile.md` | /ncc_audit_concept, /ncc_audit_story 기준 |
| `10_docs/14_workflow_v4.md` | Orchestrator 워크플로우 명세 |
| `20_research/02_R2-people-map.md` | /story-write 인물 정보 |
| `40_BaseDocs/NN_단원명/` | Phase 1 개념 입력 |

### 산출물 파일 (쓰기)

| 파일 유형 | 경로 | 생성 Phase |
|---|---|---|
| chatlog | `00_project_hub/chatlog/YYMMDD_unitNN.md` | 0~5 |
| 스토리 | `50_units/NN/story/unitNN.md` | 2 |
| 인덱스 앱 | `50_units/NN/app/index.html` | 4 |
| 스토리 앱 | `50_units/NN/app/story.html` | 4 |
| 개념 앱 | `50_units/NN/app/concepts.html` | 4 |
| 기본문제 앱 | `50_units/NN/problems/basic_app.html` | 5a |
| 유형 목록 | `50_units/NN/problems/types.md` | 5b |
| 유형 연습 앱 | `50_units/NN/problems/type_NN_app.html` | 5c |
| 유형 깊이 탐구 앱 | `50_units/NN/problems/deep_유형명_app.html` | in-loop |

---

## 4. NCC Audit 체인

각 Phase의 audit 흐름:

```
Phase 1: 개념 → /ncc_audit_concept → [Warn/Fail 시 보완]
Phase 2: 스토리 → /ncc_audit_story → [수정]
Phase 4: HTML 앱 → /ncc_audit_app → [Fail-단순: 즉시수정 / Fail-구조: Nick 보고]
Phase 5a: basic_app.html → /ncc_audit_math → /ncc_audit_app → /ncc_audit_problem
Phase 5b: types.md → /ncc_audit_problem
Phase 5c: type_NN_app.html → /ncc_audit_math → /ncc_audit_app
```

---

## 5. 수학 검증 체계

```
문제 생성
  ↓
NCC 독립 풀이 (풀이 과정 전개)
  ↓
Wolfram Alpha MCP 호출 (계산식 독립 확인)
  ↓
두 결과 비교:
  일치 → Pass
  불일치 → Warn (재풀이) → 재비교
  명확 오류 → Fail (문제 수정)
```

Wolfram Alpha 설정: `10_docs/15_wolfram_alpha_guide.md`

---

## 6. 상태 관리 및 가시성

상태는 **파일 시스템 + chatlog**로만 관리한다. DB, 인메모리 상태 없음.

- `chatlog/YYMMDD_unitNN.md`: 실행 로그 (Round 0~N)
- Nick이 언제든 chatlog 파일을 열어 현재 상태 확인 가능
- 오류·불확실 발생 시: chatlog에 기록 후 중단 (Nick 확인 대기)

---

## 7. 피드백 루프

```
딸 학습 → feedback/ 파일 작성 (Nick 또는 딸이)
  ↓
/ncc_audit_story unit01 feedback 실행
  ↓
분석 보고서 생성 (feedback/ 원본 수정 안 함)
  ↓
Nick 확인 후 → 10_docs/01_learner-profile.md 업데이트
  ↓
다음 단원 /ncc_audit_concept, /ncc_audit_story에 자동 반영
```

---

## 8. 확장 포인트

| 항목 | 현재 | 확장 가능 방향 |
|---|---|---|
| Wolfram Alpha MCP | 수동 설정 필요 | settings.json에 기본 포함 |
| Phase 3 수학언어 | Orchestrator 내부 판단 | `/literacy-check` 전용 Skill 추가 가능 |
| 피드백 분석 | /ncc_audit_story 내 수동 트리거 | 딸이 파일 쓰면 자동 분석 (훅 설정) |
| Unit 번호 확장 | Ch1~4 (현재) | Ch5~13 동일 파이프라인 적용 |

---

## 9. 디렉토리 구조 (기술 관점)

```
260426_MathTelling_Idea/
├── CLAUDE.md                  ← Orchestrator 진입점
├── APP_PRINCIPLES.md          ← /ncc_audit_app 기준
├── .claude/
│   ├── agents/
│   │   ├── unit-orchestrator.md   ← 유일한 Agent
│   │   └── type-explorer.md       ← in-loop 탐구
│   ├── skills/
│   │   ├── unit-plan/
│   │   ├── concept-review/
│   │   ├── story-write/
│   │   ├── math-figure/
│   │   ├── math-practice/
│   │   ├── math-error-note/
│   │   ├── ncc_audit_app/
│   │   ├── ncc_audit_math/
│   │   ├── ncc_audit_concept/
│   │   ├── ncc_audit_problem/
│   │   └── ncc_audit_story/
│   └── archive/               ← 구버전 agent/skill
├── 10_docs/
│   ├── 01_learner-profile.md
│   ├── 14_workflow_v4.md      ← 현행 워크플로우
│   ├── 15_wolfram_alpha_guide.md
│   ├── 20_guide_engineer.md   ← 이 파일
│   ├── 21_guide_teacher.md
│   ├── 22_guide_student.md
│   └── archive/               ← 구버전 워크플로우
├── 40_BaseDocs/               ← 개념 입력 (읽기 전용)
└── 50_units/                  ← 단원별 산출물
```
