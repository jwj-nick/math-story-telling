# Kids 학습 도우미 시스템 — 전체 가이드

> 작성: 2026-05-13 | Phase A~F 완료 기준
> 대상 독자: Nick (시스템 운영자)

---

## 1. 한 눈에 보는 전체 그림

```
                      [Nick / 학생 발화]
                             │
                    자연어 / slash command
                             ▼
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 LAYER 3 — Agents (자연어 → 흐름 결정)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [se_agent_subject_helper]    [se_agent_unit_orchestrator]
  HS 2604 범용 라우터           MathTelling 단원 파이프라인
       │                              │
       ├──수학──────────────►  [se_agent_math_error_workflow]
       ├──비수학 안내 반환             │
       └──모든 결과──────►  [se_agent_app_reviewer] ◄─────────────┐
                                                                   │
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━               │
 LAYER 2 — Composite Skills (도메인 특화 산출물)                   │
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━               │
                                                                   │ 검토
  [수학 오답]           [수행평가]          [MathTelling 단원]     │
  se_math_error_note    se_perf_eval_step   se_unit_plan          │
  se_math_practice      se_perf_eval_person se_concept_review     │
  se_math_figure        se_science_chem_card se_story_write       │
                                            se_math_figure        │
                                            se_math_practice      │
                                            se_type_explorer ─────┘
                                            se_unit_review

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 LAYER 1 — Atomic Skills (재사용 부품)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  se_person_research    se_figcrop    se_ncc_audit_* (5종)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 LAYER 0 — 자산 (원칙·패턴·컴포넌트 .md)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  40_PRINCIPLES/    20_PATTERNS/    30_COMPONENTS.md    60_LEARNERS.md

  [se_agent_pattern_extractor] → 새 작업 끝난 후 패턴 자동 추출 초안
```

---

## 2. 빠른 참조 — 상황별 명령어

### HS 2604 (아들/고1)

| 상황 | 명령 / 발화 |
|---|---|
| 수학 문제 1개 틀렸을 때 | `/se_math_error_note Q12` |
| 수학 여러 문제 틀렸을 때 | `"수학 오답 Q12, Q13, Q15 처리해줘"` |
| 수학 그림 있는 문제 | `/se_math_figure Q16` |
| 수학 연습문제 만들기 | `/se_math_practice Q12` |
| 시험지 그림 crop | `/se_figcrop Q16 수학` |
| 과학 개념 카드 | `/se_science_chem_card` |
| 사회·도덕 수행평가 Step형 | `/se_perf_eval_step 사회 메가시티 step3` |
| 한국사·사회 인물 수행평가 | `/se_perf_eval_person 정도전 한국사` |
| 인물 데이터만 먼저 조사 | `/se_person_research 정도전` |
| 앱 품질 검토 | `"Q16 앱 검토해줘"` 또는 `"social_step3 검토해줘"` |
| 뭘 해야 할지 모를 때 | `"수학 Q5 오답"` 또는 `"사회 step4 도와줘"` → 라우터가 분기 |

### MathTelling (딸/중1)

| 상황 | 명령 / 발화 |
|---|---|
| 단원 전체 파이프라인 | `"unit 03 만들어"` 또는 `"unit03 Phase 2부터"` |
| 단원 계획만 | `/se_unit_plan unit03 정수와유리수` |
| 개념 검수 | `/se_concept_review unit03` |
| 인물 스토리 | `/se_story_write unit01 에라토스테네스` |
| 수학 그림 | `/se_math_figure` (HS와 공유) |
| 수학 연습 | `/se_math_practice` (HS와 공유) |
| 수학 오답 | `/se_math_error_note` (HS와 공유) |
| 타입 탐구 | `/se_type_explorer` |
| 단원 완성 검토 | `/se_unit_review` |
| 콘텐츠 감사 | `/se_ncc_audit_concept` `/se_ncc_audit_math` `/se_ncc_audit_story` |
| 앱 감사 | `/se_ncc_audit_app` |

### 메타 (00_LearningSystem)

| 상황 | 명령 / 발화 |
|---|---|
| 작업 끝난 후 패턴 추출 | `"오늘 작업에서 패턴 추출해줘"` |

---

## 3. HS 2604 — Skill & Agent 상세

### Agents (자율 실행)

#### `se_agent_subject_helper` ⭐ 진입점

```
위치: .claude/agents/se_agent_subject_helper.md
역할: 자연어 → 적절한 skill 분기
```

라우팅 테이블:

| 발화 패턴 | → 연결 | 상태 |
|---|---|---|
| "수학 Q[N] 오답" | `se_math_error_note` | ✅ |
| 복수 문제 오답 | `se_agent_math_error_workflow` | ✅ |
| "사회 step[N]" | `se_perf_eval_step` | 🔶 안내 |
| "한국사 [인물]" | `se_perf_eval_person` | 🔶 안내 |
| "과학 개념카드" | `se_concept_card` | 🔶 안내 |
| "국어 글쓰기" | `se_writing_essay` | 🔶 안내 |

#### `se_agent_math_error_workflow`

```
위치: .claude/agents/se_agent_math_error_workflow.md
역할: 수학 오답 배치 처리
흐름: error_note → figure(그림 있으면) → practice → app_reviewer → todo 업데이트
```

#### `se_agent_app_reviewer`

```
위치: .claude/agents/se_agent_app_reviewer.md
역할: 모든 영역 앱 품질 검토
영역 감지: 파일명 패턴으로 자동 (수학/수행평가Step/인물/국어/과학)
원칙 파일: APP_PRINCIPLES.md + 40_PRINCIPLES/<영역>.md
```

---

### Skills (직접 실행)

#### ✅ 구현 완료

| 명령 | 입력 | 출력 |
|---|---|---|
| `/se_math_error_note Q<N>` | 문제 번호 | 7섹션 .md + HTML 앱 |
| `/se_math_practice Q<N>` | 문제 번호 | 연습문제 3×3=9개 .md + HTML |
| `/se_math_figure Q<N>` | 문제 번호 | 정적 SVG(문제) + JSXGraph(풀이) |
| `/se_figcrop Q<N> <과목>` | 문제·과목 | crop된 jpg + .md 삽입 |
| `/se_science_chem_card` | 물질/원소 ID | 과학 개념 카드 HTML |

#### 🔶 SKILL.md 뼈대 완성 (의뢰 시 즉시 실행)

| 명령 | 입력 | 출력 |
|---|---|---|
| `/se_perf_eval_step <과목> <과제> <step번호>` | 과목·과제명·step | 탭 HTML 골격 + TODO 표시 |
| `/se_perf_eval_person <인물> <과목>` | 인물명·과목 | 가이드·모범·심화 3 앱 |
| `/se_person_research <인물명>` | 인물명 | 인물 데이터 .md (표준 포맷) |

---

## 4. MathTelling — Skill & Agent 상세

### Agent

#### `se_agent_unit_orchestrator` ⭐ 진입점

```
위치: .claude/agents/se_agent_unit_orchestrator.md
역할: 단원 전체 파이프라인 (Phase 0~5c) 자동 실행
발화: "unit 03 만들어" / "unit03 Phase 2부터"
```

Phase 순서:
```
Phase 0: se_unit_plan (킥오프 + chatlog)
Phase 1: se_concept_review (개념 검수)
Phase 2: se_story_write (인물 스토리)
Phase 3: se_math_figure (그림)
Phase 4: [video 계획]
Phase 5a: se_math_practice (연습문제)
Phase 5b: se_type_explorer (타입 탐구)
Phase 5c: se_unit_review (완성 검토)
```

### Skills

| 명령 | 역할 | Layer |
|---|---|---|
| `/se_unit_plan` | 단원 킥오프·chatlog 생성 | L2 |
| `/se_concept_review` | 개념 MD 검수·보완 | L2 |
| `/se_story_write` | 인물 서사 초안 | L2 |
| `/se_math_figure` | 수학 그래프·도형 렌더링 | L2 |
| `/se_math_practice` | 연습문제 생성 | L2 |
| `/se_math_error_note` | 오답노트 | L2 |
| `/se_type_explorer` | 타입 탐구 | L2 |
| `/se_unit_review` | 단원 완성 검토 | L2 |
| `/se_ncc_audit_app` | 앱 감사 | L1 |
| `/se_ncc_audit_concept` | 개념 감사 | L1 |
| `/se_ncc_audit_math` | 수학 감사 | L1 |
| `/se_ncc_audit_problem` | 문제 감사 | L1 |
| `/se_ncc_audit_story` | 스토리 감사 | L1 |

---

## 5. 공통 자산 (Layer 0)

### `40_PRINCIPLES/` — 설계 원칙

| 파일 | 적용 대상 |
|---|---|
| `common.md` | 모든 skill/agent (신뢰 등급, 언어 규칙) |
| `math.md` | 수학 오답노트 앱 (page-0 금지사항, JSXGraph 규칙) |
| `perf_eval.md` | 수행평가 앱 (PE1~PE8: form-mirror, think-box, 모범답안 위치) |
| `writing.md` | 글쓰기·국어 앱 |
| `deploy.md` | 배포 원칙 (파일명 규칙, back-nav, GitHub Pages) |
| `communication.md` | Nick ↔ Claude 소통 규약 |

**핵심 원칙 요약**:
- 수학 page-0: 정적 SVG만, JSXGraph/슬라이더 금지
- 수행평가 PE1: form-mirror (색 테두리 = 실제 양식)
- 수행평가 PE2: 모범답안은 마지막 탭
- 수행평가 PE3: think-box (step5·6 필수)
- 배포: 모든 세부 앱에 back-nav 필수

### `20_PATTERNS/` — 재사용 패턴

| ID | 패턴 | 대표 사례 |
|---|---|---|
| P01 | 수학 오답노트 앱 | 공통수학1 Q12~Q20 |
| P02 | 과학 개념 카드 | 화학결합 카드 |
| P03 | 수행평가 Step형 앱 | 사회 메가시티 step1~6 |
| P04 | 인물 수행평가 3앱 | 한국사 정도전 (가이드·모범·심화) |
| P05 | 국어 글쓰기 | 견해문 모델·발표 예시 |
| P06 | MathTelling 단원 앱 | unit01~03 스토리+퀴즈 |

### `30_COMPONENTS.md` — UI 부품

| 컴포넌트 | 용도 |
|---|---|
| `form-mirror` | 양식 시각 미러 (PE1) |
| `think-box` | 사고 가이드 박스 (PE3) |
| `hint-toggle` | 힌트 접기/펼치기 |
| `good-vs-bad` | 좋은 예/나쁜 예 |
| `file-guide` | 교과서·자료 위치 안내 |
| `ccard` (개념카드) | 클릭 선택형 개념 카드 |
| `JSXGraph 슬라이더` | 수학 풀이 페이지 전용 |

---

## 6. 호출 흐름 예시

### 시나리오 A — 수학 시험 오답 처리

```
Nick: "수학 Q14, Q16, Q18 틀렸어"
  ↓
se_agent_subject_helper 감지 → se_agent_math_error_workflow 호출
  ↓
Q14: error_note 실행 → .md + Q14_app.html
     practice 실행 → Q14_practice_app.html
     app_reviewer → 검증
  ↓
Q16: error_note → Q16_app.html
     그림 있음 감지 → math_figure 실행 → SVG + JSXGraph 삽입
     practice → Q16_practice_app.html
  ↓
Q18: 동일 처리
  ↓
todo.md 업데이트 + study.md 약점 태그 갱신
완료 보고
```

### 시나리오 B — 수행평가 새 과제

```
Nick: "사회 기후변화 수행평가 step2 도와줘"
  ↓
se_agent_subject_helper → se_perf_eval_step 안내
  ↓
(현재 뼈대 모드) Claude가 직접 진행:
  1. 수행평가-사회/ 폴더 탐색
  2. 안내문·채점기준 없으면 Nick에게 요청
  3. social_step2.html 패턴(P03) 기반 기후변화_step2.html 생성
  4. app_reviewer 검토 → PE1~PE8 확인
```

### 시나리오 C — MathTelling 새 단원

```
Nick: "unit04 소수와 합성수 만들어"
  ↓
se_agent_unit_orchestrator 실행
  ↓
Phase 0: se_unit_plan → cht_log/unit04_chatlog.md 생성
Phase 1: se_concept_review → 개념 검수
Phase 2: se_story_write → 에라토스테네스 체 인물 스토리
Phase 3: se_math_figure → 체 도식 SVG
Phase 5a: se_math_practice → 연습문제
Phase 5b: se_type_explorer → 타입 탐구
Phase 5c: se_unit_review → 완성 검토
  ↓
각 Phase 완료 후 se_ncc_audit_* 자동 검수
```

### 시나리오 D — 새 작업 후 패턴 추출

```
Nick: "오늘 기후변화 수행평가 만든 것 패턴 추출해줘"
  ↓
se_agent_pattern_extractor 실행
  ↓
git diff 기반 변경 파일 분석
기존 P01~P06 비교 → 신규 패턴 여부 판단
20_PATTERNS/P99_기후변화수행평가_초안.md 생성
Nick 검토 요청 → 확정 시 P07 번호 부여
```

---

## 7. 배포 구조 (jwj-nick.github.io)

```
jwj-nick.github.io/high1/
├── index.html             ← 과목 카드 (수학/과학/사회/한국사/국어)
├── math/                  ← 수학 오답노트·연습 앱
├── science/               ← 과학 개념 앱
├── society/               ← 사회 수행평가 step1~6
│   ├── index.html
│   ├── social_step1.html ~ social_step6.html
├── history/               ← 한국사 수행평가
│   ├── index.html
│   ├── jeongdojeon_guide.html
│   ├── jeongdojeon_model.html
│   └── jeongdojeon_deep.html
└── korean/                ← 국어 (Nick 수동 추가)
```

**소스 위치**: `C:/Nick/30_Apps/jwj-nick.github.io/high1/`
**배포 원칙**: `40_PRINCIPLES/deploy.md` 참조 (back-nav, 파일명 규칙)

---

## 8. 현재 상태 & 다음 단계

### Phase 완료 현황 (2026-05-13)

| Phase | 내용 | 상태 |
|---|---|---|
| A | 전체 skill/agent prefix rename (`se_*`) | ✅ 완료 |
| B | `se_agent_subject_helper` (라우터) | ✅ 완료 |
| C | `se_perf_eval_step` (수행평가 Step형) | ⏳ 뼈대 — 의뢰 시 즉시 |
| D | `se_agent_app_reviewer` 비수학 확장 | ✅ 완료 |
| E | `se_person_research`, `se_perf_eval_person` | ⏳ 뼈대 — 의뢰 시 즉시 |
| F | `se_agent_pattern_extractor` | ✅ 완료 |
| G | B03·B04·B08 (글쓰기·개념카드·unit_app) | 청사진 — 패턴 추출 대기 |

### 실 의뢰 시 즉시 처리 가능

- 사회·도덕 새 수행평가 Step형 → `/se_perf_eval_step` (뼈대 완비)
- 한국사·사회 인물 수행평가 → `/se_perf_eval_person` (뼈대 완비)
- 국어 글쓰기 수행평가 → P05 패턴 분석 후 B03 구현 가능

### 시스템이 아직 모르는 영역 (Phase G)

- `/se_writing_essay` — 국어 글쓰기 일반화 (B03)
- `/se_concept_card` — science-chem-card 일반화 (B04)
- `/se_unit_app` — MathTelling 단원 앱 통합 (B08)

---

## 9. 파일 위치 빠른 참조

```
C:/Kids/
├── 00_LearningSystem/
│   ├── SYSTEM_GUIDE.md          ← 이 파일
│   ├── 51_MASTER_PLAN.md        ← 빌드 순서 + 진행 상태
│   ├── 50_BLUEPRINTS.md         ← 개별 skill/agent 명세
│   ├── 40_PRINCIPLES/           ← 설계 원칙 (common/math/perf_eval/writing/deploy)
│   ├── 20_PATTERNS/             ← 재사용 패턴 P01~P06
│   ├── 30_COMPONENTS.md         ← UI 컴포넌트 목록
│   └── .claude/agents/
│       └── se_agent_pattern_extractor.md
│
├── 70_HighSchool/2604_고1_중간고사/
│   ├── CLAUDE.md                ← HS 프로젝트 규칙 + skill 테이블
│   ├── APP_PRINCIPLES.md        ← 수학 앱 원칙 (상세)
│   └── .claude/
│       ├── skills/              ← 8개 skill
│       └── agents/              ← 3개 agent
│
└── 30_MiddleSchool/260426_MathTelling_Idea/
    ├── CLAUDE.md                ← MathTelling 프로젝트 규칙
    └── .claude/
        ├── skills/              ← 13개 skill
        ├── agents/              ← 1개 agent
        └── commands/            ← se_video_make
```
