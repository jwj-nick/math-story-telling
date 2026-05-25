<!-- 0525_step1_skill_body.md -->

# exp-002 / STEP 1 / Issue — `se-people-narrate` SKILL.md body 설계

> **issue**: 단계 [서사] 스킬의 body 6 sub-section 확정.
> **step**: STEP 1 (CHECKLIST.md §1)
> **선행 issue**: [`0525_step1_skill_frontmatter.md`](./0525_step1_skill_frontmatter.md) (5 Round 완료)
> **산출물 (이 issue)**: `70_tools/se-people-narrate/SKILL.md` 의 body 부분 (placeholder 교체)
> **단일 진입점**: [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md)
> **상위 체크리스트**: [`../40_experiments/exp-002-build-unit01/CHECKLIST.md`](../40_experiments/exp-002-build-unit01/CHECKLIST.md)
> **선행 양식**: [`../70_tools/se-people-pick/SKILL.md`](../70_tools/se-people-pick/SKILL.md) body
> **시작**: 2026-05-25

---

## 이 issue 의 micro-step 흐름 (예정)

| Round | 결정할 것 |
|---|---|
| 1 | 입력 6개 정련 (선정 결과 / 인물 사실 자료원 / 정체성 / 단원 frame / 영상 길이 잠정 / 한 단어 압축 후보) |
| 2 | 동작 7단계 정련 (align → QnA → 자료원 → 초안 → 평가 → 검토 → 출력) |
| 3 | 출력 양식 (`1-narrative.md` 의 구조) |
| 4 | QnA 패턴 시드 (보강 시 / 검토 시 어떤 질문 패턴) |
| 5 | 리서치 패턴 시드 (자료 부족 시 어떤 순서로 리서치) |
| 6 | 평가 기준 (약속 3겹 운반도 / 글자 수 / fabrication 체크) |

각 Round 결정 → 다음 Round Q&A 의 답이 바뀔 수 있음. 한 Round 가 길어지면 별도 issue 로 분리 가능.

---

# Round 1 — 입력 6개 정련 (2026-05-25)

## NCC 질문

본 스킬의 입력 항목을 확정합니다. frontmatter description 에 잠정 기재된 6개:

| # | 입력 | 형식 | 예시 (단원 1) |
|---|---|---|---|
| 1 | 선정 결과 | 인물 ID + 선정 이유 텍스트 | 에라토스테네스 + exp-001 output.md §3.1 |
| 2 | 인물 사실 자료원 | URL + 인용 가능 텍스트 (4 자산) | 도서관 사명 / 베타 별명 / 아르키메데스 서신 / 노년 — exp-001 output.md §4.1 |
| 3 | 정체성 | 시청자 + 약속 3겹 + 톤 | 결정 1·2 (학습자+광범 / 시대감각+인물정서+필연성서사 / 톤 A5 잠정) |
| 4 | 단원 frame | 단원 번호 + 핵심 개념 | 단원 1 / 소인수분해 |
| 5 | 영상 길이 잠정 | 초 + 글자수 계산 (5자/초) | 110초 / 약 550자 |
| 6 | 한 단어 압축 후보 | 인물을 한 단어로 | "정리" (도서관 사명 → 지식 정리 + 베타) |

**참고 — `se-people-pick` 의 입력 = 9개** (교과서 chapter / 정체성 / 시즌 frame / 학년 / 인물 풀 / 후보 수 / 발굴 우선순위 / 학습자 반응 / 리서치 허용 범위)

본 스킬은 *다음 단계* 라 선정 단계의 풀·후보 수·발굴 우선순위 등 불필요 → 입력 수 6개 (잠정).

**옵션** (NCC 추천 = 1번):

### 옵션 1 — 잠정 6개 그대로 (Recommended)

위 6개 그대로 시범 진행. 부족 시 retrospective 에서 정련 (입력 7~8 로 확장 또는 5 로 축소).

### 옵션 2 — 5개로 축소 (#6 한 단어 압축 제외)

#6 한 단어 압축은 본 스킬의 *출력* (서사를 보고 NCC 가 도출) 으로 빼면 cleaner.
→ 입력 5개 + 동작 마지막 단계에서 한 단어 압축 도출.

### 옵션 3 — 7개로 확장 (외부 시청자 어휘 수준 별도 분리)

광범 시청자 가독성은 #3 정체성에 포함되나, 별도 입력으로 분리하면 검증 명확.
→ 입력 7개 = 6개 + #7 외부 시청자 어휘 수준 단서 (예: "중1 이상이 이해 가능한 어휘 / 학술 용어 X").

**NCC 추천 이유**:
- 옵션 1 = 잠정 그대로 시범 진행이 가장 빠른 검증 경로. 정련 항목 도출 자체가 학습.
- 옵션 2 도 매력적이나 (출력으로 빼면 cleaner), 한 단어 압축 *후보* 가 미리 있으면 서사 작성 시 방향 잡기 쉬움 → 입력 유지가 실용
- 옵션 3 은 정체성 분해 시작. 정체성을 부풀려두면 다음 6 스킬도 다 부풀어야 → 입력 단순 유지

## Nick 답변

**옵션 1** (잠정 6개 그대로) 채택.

## 결정

본 스킬 입력 = 6개.

| # | 입력 | 형식 |
|---|---|---|
| 1 | 선정 결과 | 인물 ID + 선정 이유 텍스트 |
| 2 | 인물 사실 자료원 | URL + 인용 가능 텍스트 (4 자산) |
| 3 | 정체성 | 시청자 + 약속 3겹 + 톤 |
| 4 | 단원 frame | 단원 번호 + 핵심 개념 |
| 5 | 영상 길이 잠정 | 초 + 글자수 계산 (5자/초) |
| 6 | 한 단어 압축 후보 | 인물을 한 단어로 |

## 영향

- 다음 Round 2 (동작 7단계) 의 동작 #1 = "입력 6개 align" / 동작 #6 = "한 단어 압축 검토" 로 자연 매핑
- 시범 (exp-002 STEP 1) 시 입력 6개 모두 확정 후 동작 시작 — 부족 입력은 동작 #2 Q&A 에서 보강
- 정련 항목 (retrospective 후보): 시범 후 입력 추가/축소 필요성 평가

---

# Round 2~6 통합 — 본 시범 reverse-engineering 으로 일괄 결정 (2026-05-25)

## 배경

Round 1 (입력 6개) 합의 후 Nick 의 핵심 redirect:

> "se-people-narrate 의 실행결과를 봐야 하는 거 아닌가?"

본 프로젝트 frame (`se-people-pick` 도 동일 패턴) — **추상 설계 X / 즉시 시범 실행 → reverse-engineering 으로 SKILL.md 정형화 → retrospective 정련**.

→ Round 2~6 (동작 / 출력 양식 / QnA / 리서치 / 평가) 의 추상 Q&A 일괄 *생략*. NCC 가 본 시범 실행 (`1-narrative.md` 작성) 후, 그 동작을 SKILL.md body 로 정형화.

## 시범 실행 (NCC 직접 동작)

- 입력 6개 정리 (Round 1 합의안) + exp-001 output.md §3.1·§4.1 + 30_content/people/eratosthenes.md 확인 + INTEGRATED_PLAN §8 결정 1·2
- 결과물: [`../40_experiments/exp-002-build-unit01/1-narrative.md`](../40_experiments/exp-002-build-unit01/1-narrative.md) (약 1900자, §1~§7 + 부록 A~D)

## SKILL.md body 정형화 (reverse-engineering)

본 시범에서 NCC 가 실제로 한 동작을 N1~N7 로 정형화 + 출력 양식·QnA·리서치·평가 기준 작성.

결과: [`../70_tools/se-people-narrate/SKILL.md`](../70_tools/se-people-narrate/SKILL.md) body 부분 (placeholder 교체 완료).

## 결정 (Round 2~6 통합)

| 항목 | 결정 |
|---|---|
| 동작 | N1 align / N2 Q&A 보강 / N3 자료원 / N4 자산-약속 매핑 / N5 서사 초안 / N6 자체 평가 / N7 출력 |
| 출력 양식 | 본문 §1~§N + 한 단어 압축 § + 부록 A·B·C·D |
| QnA 패턴 | N2 보강 시드 3건 + N6 후 검토 시드 2건 |
| 리서치 패턴 | fallback 6단계 (people 파일 → exp output → MacTutor → Wikipedia → Britannica → WebSearch) |
| 평가 기준 | 약속 운반 / fabrication 분리 / 가독성 / 어휘 / 인용 / 압축 / 길이 7항 |

## 본 issue 종료

- ✅ SKILL.md body 작성 완료 (frontmatter + body = v0.1 시드)
- ✅ 시범 실행 결과물 `1-narrative.md` 생성 완료
- ➡️ 다음 issue = **STEP 1 검증** (NCC 자동 검증 + Nick 검증 + retrospective)

## 다음 issue session log

`0525_step1_review.md` 신설 예정 (Nick "검증 시작" 신호 후).

이 검증 issue 에서:
- NCC 자동 검증 (CHECKLIST.md §1.4 체크리스트)
- Nick 검증 (서사 품질 / §3 NCC 해석 처리 / 출력 양식 / fabrication 표현)
- retrospective 작성 (`retro-1-narrative.md`) — SKILL.md v0.2 정련 시드
- STEP 1 종료 → STEP 2 [스토리] 진입
