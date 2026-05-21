# 50_BLUEPRINTS — Skill / Agent 일반화 청사진

> Q07 응답으로 prefix 확정: skill = `se_<기능>` , agent = `se_agent_<역할>`.
> Q02 응답으로 canonical = 각 자식 프로젝트의 `.claude/`. 이 파일은 설계서.

## 청사진 표

| ID | 종류 | 이름 | 우선순위 | 출처 패턴 | Canonical 위치 | 상태 |
|---|---|---|---|---|---|---|
| B01 | skill | `/se_perf_eval_step` | 🔴 高 | P03 | (HS2604).claude/skills/se_perf_eval_step/ | ✅ 뼈대 완성 (2026-05-13) |
| B02 | skill | `/se_perf_eval_person` | 🟡 中 | P04 | (HS2604).claude/skills/se_perf_eval_person/ | ✅ 뼈대 완성 (2026-05-13) |
| B02a | skill | `/se_person_research` ⭐sub | 🟡 中 | P04+MathTelling | (HS2604).claude/skills/se_person_research/ | ✅ 뼈대 완성 (2026-05-13) |
| B03 | skill | `/se_writing_essay` | 🟡 中 | P05 (펜딩) | (HS2604).claude/skills/se_writing_essay/ | 패턴 추출 대기 |
| B04 | skill | `/se_concept_card` | 🟢 低 | P02 확장 | (HS2604).claude/skills/se_concept_card/ | 기존 science-chem-card 일반화 |
| B05 | agent | `se_agent_subject_helper` | 🔴 高 | 통합 분기 | (HS2604).claude/agents/se_agent_subject_helper.md | ✅ 구현 완료 (2026-05-13) |
| B06 | agent | `se_agent_pattern_extractor` | 🟡 中 | 메타 | 00_LS `.claude/agents/se_agent_pattern_extractor.md` | ✅ 뼈대 완성 (2026-05-13) |
| B07 | agent | `se_agent_app_reviewer` | 🟡 中 | 기존 확장 | (HS2604).claude/agents/se_agent_app_reviewer.md | ✅ 비수학 확장 완료 (2026-05-13) |
| B08 | skill | `/se_unit_app` | 🟡 中 | P06 (MathTelling 5/12) | (MathTelling).claude/skills/se_unit_app/ | 청사진 |

> Naming 변환: 자식 프로젝트의 기존 `app-reviewer`, `math-error-workflow` 등은 점진적으로 prefix 추가하여 이름 변경 (`se_agent_app_reviewer`, `se_agent_math_error_workflow`).

---

## B01. `/se_perf_eval_step` — 수행평가 다단계 도우미

### 의도
P03 패턴 일반화. 새 수행평가가 나오면 명령 하나로 Step별 도우미 앱 골격 생성.

### 인자
```
/se_perf_eval_step <과목> <과제명> <step번호>
/se_perf_eval_step 사회 메가시티 step3
/se_perf_eval_step 도덕 미디어윤리 step2
```

### 자동 수행
1. 과제 안내·예시 .md 읽기 (해당 과목 폴더)
2. 채점 기준·양식 항목 추출
3. 탭 5~7개 HTML 골격 생성 (40_PRINCIPLES/perf_eval.md 준수)
4. Step별 색 톤 자동 매핑

### 사람 개입 필수
- 모범답안 콘텐츠, 좋은 예/나쁜 예 (사례 의존), 자료 출처 추천

### Canonical 구현 위치
`C:/Kids/70_HighSchool/2604_고1_중간고사/.claude/skills/se_perf_eval_step/SKILL.md`

---

## B02. `/se_perf_eval_person` — 인물 수행평가 3앱 도우미

### 의도
P04 패턴 일반화. 인물 분석 수행평가에 가이드·모범답안·심화 3 앱 동시 생성.

### 인자
```
/se_perf_eval_person <인물> <과목> <과제포맷>
/se_perf_eval_person 류성룡 한국사 Q1Q5형
```

### 내부 호출
- 먼저 `/se_person_research <인물>` 호출 → 인물 데이터 .md 받음
- 그 위에 3 앱 골격 (가이드·모범답안·심화) 합성

### Canonical 위치
`C:/Kids/70_HighSchool/2604_고1_중간고사/.claude/skills/se_perf_eval_person/`

---

## B02a. `/se_person_research` — 인물 리서치 공통 sub-skill ⭐ (Q07로 분리)

### 의도
- 인물 리서치는 정확성이 중요 → 공통 sub-skill에서 한 번 검증
- MathTelling `/story-write` 와 HighSchool `/se_perf_eval_person` 둘 다 호출

### 산출
- 인물 기본 정보 .md (시대 / 주요 사건 / 사상·저서 / 인용 / 신뢰 출처)
- 표준 JSON 형식도 병행 (다른 skill이 파싱 용이)

### 인자
```
/se_person_research <인물명>
/se_person_research 정도전
/se_person_research 에라토스테네스
```

### 자료 출처
- 40_PRINCIPLES/common.md C1 신뢰 등급 ★★★~★★ 만
- 위키 X, 학술·교과서·1차 자료 우선

### Canonical 위치
- 양쪽 프로젝트의 `.claude/skills/se_person_research/`
- 동기화 필요 (Q02 (B) 현행, 수동)

---

## B03. `/se_writing_essay` — 글쓰기 도우미

### 상태
P05 (국어 견해문) 패턴 추출 대기. high1/korean/ 2 앱 (model, presentation_example) 분석 후 확정.

### 예상 컴포넌트
- char-counter (글자수 카운터)
- 논거 구조 카드 (주장→근거→사례)
- 좋은 예/나쁜 예 토글
- 교과 개념 참조

---

## B04. `/se_concept_card` — 개념카드 일반화

### 의도
기존 `science-chem-card` 가 화학 특화 → 더 일반적인 `/se_concept_card` 로 확장.

### 인자
```
/se_concept_card <과목> <단원> <항목ID>
/se_concept_card 과학 화학결합 nacl
/se_concept_card 국어 음운변동 비음화
/se_concept_card 사회 정치제도 의원내각제
```

### 자동 수행
- 항목 1개씩 추가, 전체 재생성 (`all`) 옵션
- 표준 JSON 배열에 push, 카드 그리드 HTML 자동 재생성

---

## B05. `se_agent_subject_helper` — 통합 분기 Agent ⭐

### 의도
자식 프로젝트에서 학생·Nick의 자연어 요청을 받아 적절한 skill로 분기.

### 트리거
- "사회 메가시티 step 3 도와줘"
- "한국사 인물 [이름]"
- "수학 Q[N] 오답"
- "과학 [단원] 개념카드"

### 동작
1. 입력 파싱 → 과목·과제·요청 종류 식별
2. `00_LS/20_PATTERNS/` 카탈로그 참조 (어떤 패턴인지)
3. 해당 .md 자료 (과제안내, CLAUDE.md) 읽기
4. 적절한 skill 선택 + 인자 구성 → 호출
5. 결과 보고 + chatlog 기록 (communication.md C1)

### Canonical 위치
`C:/Kids/70_HighSchool/2604_고1_중간고사/.claude/agents/se_agent_subject_helper.md`

### MathTelling과 차이
- MathTelling `unit-orchestrator` 와 유사하나 범위가 단원→단발 과제로 확대
- 두 agent는 별도 유지 (당분간)

---

## B06. `se_agent_pattern_extractor` — 패턴 자동 추출 Agent

### 의도
작업 끝나고 "새 패턴이 있나?" 자동 검토.

### 트리거
- 명시: "패턴 추출해줘"
- 자동: 한 과제 완료 후 git commit 시 hook (향후)

### 동작
1. 최근 변경 파일 분석 (HTML 앱, 새 컴포넌트)
2. `30_COMPONENTS.md` 와 비교 → 신규 컴포넌트 식별
3. `20_PATTERNS/` 추가 가치 판단
4. `P99_새_패턴_제안_템플릿.md` 채워 초안 → Nick 검토

### Canonical 위치
`C:/Kids/00_LearningSystem/.claude/agents/se_agent_pattern_extractor.md` (메타 디렉토리에)

---

## B07. `se_agent_app_reviewer` — 통합 앱 리뷰어

### 의도
기존 `app-reviewer` (수학 한정)를 확장 → 모든 영역 (수학·수행평가·글쓰기) 검토.

### 트리거
- "Q16 앱 검토해줘"
- "사회 step5 검토"
- skill 호출 후 자동 (옵션)

### 동작
1. 영역 식별 (수학·수행평가·...) → 해당 `40_PRINCIPLES/<영역>.md` 로드
2. + `common.md` 항상 로드
3. 앱 파일(HTML) 분석
4. 위반 항목 보고 (영역별 우선순위)

### Canonical 위치
`C:/Kids/70_HighSchool/2604_고1_중간고사/.claude/agents/se_agent_app_reviewer.md` (기존 `app-reviewer` 확장 명세로 교체)

---

## B08. `/se_unit_app` — MathTelling 단원 앱 도우미 ⭐ (Q05 응답 반영)

### 의도
P06 (5/12 update) 패턴 — 교과서 챕터별 짜임새 있는 단원 앱 + 자체 리뷰·업데이트 사이클.

### 인자
```
/se_unit_app <단원번호> <Phase>
/se_unit_app 02 0      # 디렉토리 초기화
/se_unit_app 02 4      # 앱 단계
/se_unit_app 02 review # 자체 리뷰·업데이트 사이클
```

### 자동 수행
- Phase 0: unit root 디렉토리 (index/story/concepts + problems/)
- Phase 4: 앱 3장 (index, story, concepts)
- Phase 5-x: problems/ (basic, type, deep, walk)
- review 모드: 기존 앱 분석 → 개선 제안 → 적용

### Canonical 위치
`C:/Kids/30_MiddleSchool/260426_MathTelling_Idea/.claude/skills/se_unit_app/`

### 기존 unit-orchestrator와의 관계
- `se_agent_unit_orchestrator` (기존 `unit-orchestrator`의 prefix 적용 rename) 가 이걸 호출
- B05 (`subject_helper`) 와는 호출 도메인 다름 (수행평가 vs 단원)

---

## 우선 순위 (단기 6주)

기존 우선순위 유지하되 Q05 응답 반영하여 **고정 X**.
필요한 순간이 오면 즉시 청사진 → 구현.

대기 청사진:
- B05 (subject_helper) — Nick 자연어 인터페이스
- B01 (perf_eval_step) — 다음 수행평가 즉시
- B07 (app_reviewer 통합) — 검토 일관성
- B02 + B02a — 다음 인물 수행평가 등장 시
- B08 — MathTelling 5/12 update에 맞춰

---

## 변경 이력
- 2026-05-11: 초안. 7 청사진.
- 2026-05-12: prefix `se_*` 적용 (Q07). B02a sub-skill 분리. B08 (MathTelling 단원) 추가. canonical 위치 명시.
