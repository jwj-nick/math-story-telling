<!-- 0509_workflow_v4_impl.md -->
# Workflow v4 — 구현 세션

> 세션: 2026-05-09
> 목적: v3 재평가(E-1~E-10) 결정사항을 실제 파일로 구현
> 전제: `0509_workflow_v3_review.md` Round 2 결정사항 확정 완료

---

# Round 1 — 구현 계획 및 실행

## 구현 항목 목록

### 신규 생성
| 파일 | 설명 |
|---|---|
| `10_docs/14_workflow_v4.md` | 확정판 워크플로우 명세 |
| `.claude/agents/unit-orchestrator.md` | 단일 Orchestrator Agent |
| `.claude/agents/type-explorer.md` | 유형 깊이 탐구 (math-workflow 대체) |
| `.claude/skills/ncc_audit_app/SKILL.md` | HTML 앱 품질 검토 (app-reviewer 통합) |
| `.claude/skills/ncc_audit_math/SKILL.md` | 수학 정확성 검증 |
| `.claude/skills/ncc_audit_concept/SKILL.md` | 개념 수준·범위 검토 |
| `.claude/skills/ncc_audit_problem/SKILL.md` | 문제 커버리지·난이도 검토 |
| `.claude/skills/ncc_audit_story/SKILL.md` | 스토리 적합성 검토 |
| `10_docs/15_wolfram_alpha_guide.md` | Wolfram Alpha MCP 가이드 |
| `10_docs/20_guide_engineer.md` | 엔지니어 관점 가이드 |
| `10_docs/21_guide_teacher.md` | 수학선생님 관점 가이드 |
| `10_docs/22_guide_student.md` | 학생(딸) 관점 가이드 |

### 아카이브 (10_docs/archive/, .claude/archive/)
| 파일 | 이유 |
|---|---|
| `10_docs/04_unit-production-guide.md` | v4로 대체 |
| `10_docs/11_workflow.md` | v4로 대체 |
| `10_docs/12_workflow_update.md` | v4로 대체 |
| `10_docs/13_workflow_v3.md` | v4로 대체 |
| `.claude/agents/app-reviewer.md` | /ncc_audit_app으로 통합 |
| `.claude/agents/math-workflow.md` | type-explorer로 대체 |

### 업데이트
| 파일 | 변경 내용 |
|---|---|
| `CLAUDE.md` | Agent/Skill 카탈로그, 피드백 루프, 커미션 프로세스 |
| `10_docs/01_learner-profile.md` | 피드백 루프 섹션 추가 |

---

## 실행 결과

### 신규 생성 ✅

| 파일 | 상태 |
|---|---|
| `10_docs/14_workflow_v4.md` | ✅ 생성 |
| `.claude/agents/unit-orchestrator.md` | ✅ 생성 |
| `.claude/agents/type-explorer.md` | ✅ 생성 (math-workflow 대체) |
| `.claude/skills/ncc_audit_app/SKILL.md` | ✅ 생성 (app-reviewer 흡수) |
| `.claude/skills/ncc_audit_math/SKILL.md` | ✅ 생성 |
| `.claude/skills/ncc_audit_concept/SKILL.md` | ✅ 생성 |
| `.claude/skills/ncc_audit_problem/SKILL.md` | ✅ 생성 |
| `.claude/skills/ncc_audit_story/SKILL.md` | ✅ 생성 |
| `10_docs/15_wolfram_alpha_guide.md` | ✅ 생성 |
| `10_docs/20_guide_engineer.md` | ✅ 생성 |
| `10_docs/21_guide_teacher.md` | ✅ 생성 |
| `10_docs/22_guide_student.md` | ✅ 생성 |

### 아카이브 ✅ (최상위 `archive/`로 통합)

| 파일 | 이동처 |
|---|---|
| `00_project_hub/chatlog/0504_app_overall_preview.md` | `archive/chatlog/` |
| `00_project_hub/chatlog/0509_unit01_재정비.md` | `archive/chatlog/` |
| `00_project_hub/chatlog/0509_workflow_v3_review.md` | `archive/chatlog/` |
| `10_docs/04_unit-production-guide.md` | `archive/10_docs/` |
| `10_docs/11_workflow.md` | `archive/10_docs/` |
| `10_docs/12_workflow_update.md` | `archive/10_docs/` |
| `10_docs/13_workflow_v3.md` | `archive/10_docs/` |
| `.claude/agents/app-reviewer.md` | `archive/.claude/` |
| `.claude/agents/math-workflow.md` | `archive/.claude/` |
| `50_units/01_소인수분해/` (전체) | `archive/50_units/` |

### 업데이트 ✅

| 파일 | 변경 내용 |
|---|---|
| `CLAUDE.md` | 파이프라인 Phase 구조, Skills/Agents 카탈로그, 참고문서 목록 |
| `10_docs/01_learner-profile.md` | 피드백 루프 섹션 추가 |

---

## 다음 단계

```
Step 2: Nick 리뷰 (이 chatlog 파일 확인)
  → 수정 필요 시 refine loop

Step 3: Unit 1 backup → 처음부터 재제작
  → before/after 비교 가능

Step 4: Unit 2 batch 시작
  → "unit 02 만들어" 한 마디로 unit-orchestrator 실행
```

---

> (Nick): archive 최상위로. unit1 실무 진행 가이드 필요. 명시적으로 unit-orchestrator 를 멘션하면 되나?

---

# Round 2 — Unit 1 실무 진행 가이드

## unit-orchestrator 호출 방법

**"명시적으로 멘션하면 되나?"** — 둘 다 가능하다.

### 방법 A: 자연어 (권장)
```
"unit 01 만들어"
"소인수분해 단원 처음부터 만들어줘"
```
Claude Code가 `unit-orchestrator.md`의 description을 보고 자동으로 해당 agent를 실행한다.

### 방법 B: 명시적 멘션
```
"unit-orchestrator로 unit 01 제작 시작해줘"
"unit-orchestrator: unit 01, Phase 0부터 전체 실행"
```
더 확실하게 agent를 지정하고 싶을 때 사용.

> **실제 실행 흐름**: Claude Code가 agent 파일을 읽고 `tools: [Agent]` 권한으로 sub-agent를 spawn → unit-orchestrator가 독립 실행.

---

## Unit 1 착수 전 준비 체크리스트

### NCC가 읽어야 할 파일 (자동)
- [x] `CLAUDE.md`
- [x] `APP_PRINCIPLES.md`
- [x] `10_docs/14_workflow_v4.md`
- [x] `10_docs/01_learner-profile.md`
- [x] `20_research/02_R2-people-map.md`
- [x] `40_BaseDocs/01_소인수분해/` — 개념 MD 전체

### Nick이 확인해두면 좋은 것
- [ ] `40_BaseDocs/01_소인수분해/`에 개념 MD들이 있는지 확인
- [ ] 특별 지시가 있으면 의뢰 메시지에 포함

```
예시:
"unit 01 만들어. 에라토스테네스 스토리는 체 발견 순간 중심으로."
"unit 01 만들어. Phase 4까지만 (문제 파트 제외)."
"unit 01 만들어. 기존 unit01.md 스토리 참고해서 더 감성적으로."
```

### 특별 지시 없으면 기본 가정
- 인물: 에라토스테네스 (CLAUDE.md 단원별 인물 배정 기준)
- 전체 Phase 실행 (Phase 0 → 5c)
- 기본문제: 8~10문제
- APP_PRINCIPLES.md + 중1 교육과정 전면 적용

---

## Unit 1 실행 시나리오 (예상 흐름)

```
Nick: "unit 01 만들어"
  ↓
unit-orchestrator 시작
  ↓
chatlog 파일 생성: 00_project_hub/chatlog/YYMMDD_unit01.md
  ↓
Round 0 작성:
  "단원: 01_소인수분해 / 인물: 에라토스테네스
   전체 Phase 실행 예정. 맞으면 계속 진행합니다."
  ↓
(Nick이 확인하거나 30초 후 자동 진행)
  ↓
Phase 0: 50_units/01_소인수분해/ 디렉토리 초기화
Phase 1: /concept-review → /ncc_audit_concept → Round 1 기록
Phase 3 체크: 수학언어 업데이트 필요 여부 판단
Phase 2: /story-write → /ncc_audit_story → Round 2 기록
Phase 4: HTML 앱 3종 제작 → /ncc_audit_app → Round 4 기록
Phase 5a: basic_app.html → /ncc_audit_math + /ncc_audit_app → Round 5a 기록
Phase 5b: types.md → /ncc_audit_problem → Round 5b 기록
Phase 5c: type 연습 앱 → /ncc_audit_math + /ncc_audit_app → Round 5c 기록
  ↓
완료 보고 (chat window에 요약)
```

Nick은 **중간에 언제든** chatlog 파일을 열어 진행 상황 확인 가능.
중단하고 싶으면 그냥 대화창에 "잠깐 멈춰"라고 말하면 된다.

---

## 파일 명명 (Unit 1 기준)

| 파일 | 경로 |
|---|---|
| chatlog | `00_project_hub/chatlog/YYMMDD_unit01.md` |
| 스토리 | `50_units/01_소인수분해/story/unit01.md` |
| 인덱스 앱 | `50_units/01_소인수분해/app/index.html` |
| 스토리 앱 | `50_units/01_소인수분해/app/story.html` |
| 개념 앱 | `50_units/01_소인수분해/app/concepts.html` |
| 에라토스테네스 체 앱 | `50_units/01_소인수분해/app/sieve.html` (단원 특수) |
| 기본문제 앱 | `50_units/01_소인수분해/problems/basic_app.html` |
| 유형 목록 | `50_units/01_소인수분해/problems/types.md` |
| 유형 연습 앱 | `50_units/01_소인수분해/problems/type_NN_app.html` |

---

## Wolfram Alpha MCP (권장 선행 작업)

수학 검증 품질을 높이려면 착수 전에 설정하는 것이 좋다.

```
1. https://developer.wolframalpha.com 에서 무료 API 키 발급
2. .claude/settings.json에 MCP 설정 추가
   (상세: 10_docs/15_wolfram_alpha_guide.md)
3. Claude Code 재시작
```

설정 없이도 실행 가능하나, 수학 오류 검출률이 낮아진다.

---

> (Nick):
