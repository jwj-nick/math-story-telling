<!-- 0525_selection_skill.md -->

# 단계 [선정] — 인물 선정 스킬 정의 (Q&A 세션 로그)

> 단일 진입점: [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md)
> 결정 누적: INTEGRATED_PLAN §8
> 상위 frame: skill chain (§5.0)
>
> 시작: 2026-05-25

---

## 단계 [선정] 의 산출물

- 스킬 `se-people-pick` (입력 / 출력 / 동작 / QnA / 리서치 패턴 내재화)
- 첫 결과물 1건: 본 시즌의 단원-인물 매핑

## 진행 항목

| P# | 무엇 | 상태 |
|---|---|---|
| P1 스킬 입력 | 외부에서 받을 입력 목록 | ✅ 결정 3 |
| P2 동작 흐름 | 스킬이 단계별로 무엇을 하는가 | ✅ 결정 4 |
| 모드 전환 | 디자인 → 실행 / SKILL.md 작성 | ✅ 결정 5 |
| P3 출력 양식 | 매핑 표 형식 (1:1 / 1:N / 후보 비교) | SKILL.md 시드 (시범 후 정련) |
| P4 QnA 패턴 | Nick 에게 던질 질문의 patterns | SKILL.md 시드 (시범 후 정련) |
| P5 리서치 패턴 | 후보 수집 깊이·도구 | SKILL.md 시드 (시범 후 정련) |
| P6 skill vs agent | 구현 형식 | SKILL.md 형식 + NCC 내재화 (사실상 skill) |
| P7 첫 결과물 1건 대상 | 어느 단원 대상으로 시범 실행 | ⏳ 다음 라운드 |

---

# Round 1 — P1 스킬 입력 (2026-05-25)

## NCC 질문

`se-people-pick` 의 입력 후보 9개 표 제시 (필수 3 / 보조 4 / 메타 2). 이대로 확정할지 + 추가할 것 있는지.

## Nick 답변

**표 이대로 입력 9개 확정**.

## 결정 → INTEGRATED_PLAN §8 결정 3

스킬 입력 = 9개 (필수 3 / 보조 4 / 메타 2). 발굴 프롬프트·평가 기준·QnA 패턴은 스킬 안 내재화 (입력 아님).

## 다음 라운드의 변화

P2 (동작 흐름) / P3 (출력 양식) / P4 (QnA 패턴) / P5 (리서치 패턴) / P6 (skill vs agent) 모두 입력 후 자연스러운 다음. P2 동작 흐름이 가장 자연스러움 — 입력→출력의 흐름을 잡으면 나머지가 따라옴.

---

# Round 2 — P2 동작 흐름 (2026-05-25)

## NCC 질문

`se-people-pick` 동작 흐름 7단계 잠정 안 제시. 확정·조정 여부.

## Nick 답변

**7단계 흐름 그대로 확정**.

## 결정 → INTEGRATED_PLAN §8 결정 4

7단계: 입력 align → Nick QnA → 리서치 판단 → 리서치 수행 → 후보 평가 → Nick 검토 QnA → 선정+이유 출력. Q&A 2회 내장.

## 영향

- Q&A 2회 패턴 → skill (slash command) 자연스러움
- 리서치는 sub-agent 위임 가능 (하이브리드)

---

# Round 3 — 모드 전환 + SKILL.md 작성 (2026-05-25)

## Nick 지시

"실제로 스킬을 만들어서 그것을 활용하면서 앞으로 다음 단계 진행 필요함."

## NCC 작업

- `70_tools/se-people-pick/SKILL.md` 신설 (약 170줄)
- 입력 9개 / 동작 7단계 / 출력 양식 / QnA 패턴 시드 / 리서치 패턴 시드 / 평가 기준 / 진화 메커니즘 / 호출 방법 모두 내재화
- P3·P4·P5 는 SKILL.md 안 시드. 시범 실행 후 retrospective 로 정련.

## 결정 → INTEGRATED_PLAN §8 결정 5

디자인 → 실행 모드 전환. SKILL.md 신설. 호출 방식은 본 프로젝트 진행 중 NCC 가 본 문서 참조해서 동작 수행 (슬래시 명령 등록은 단계 [이전] 에서).

## 다음 라운드의 변화

P7 시범 단원 선택 — 어느 chapter 로 첫 시범 실행할지가 다음 핵심.

---

# Round 4 — 단원 1 시범 단원 선택 (2026-05-25)

## Nick 답변

**단원 1 소인수분해 (에라토스테네스 비교 검증)**.

## 결정 → INTEGRATED_PLAN §8 결정 6

스킬 첫 시범 = 단원 1. 옛 1편 + 19인 풀에 에라토스테네스 존재 → 비교 검증 frame.

---

# Round 5 — agentskills.io spec 준수 (2026-05-25)

## Nick 지시

"skill 은 https://agentskills.io/specification 내용에 의거해서 작성해야 함."

## NCC 작업

- WebFetch 로 spec 확인
- SKILL.md frontmatter 명세 준수로 갱신 (name kebab-case + description 보강 + compatibility / metadata / allowed-tools 추가)
- 디렉토리 rename: `se_people_pick/` → `se-people-pick/`
- 본 프로젝트 다른 문서 (INTEGRATED_PLAN, _index, 0525_selection_skill, 70_tools/README) 의 9개 신규 스킬 이름 일괄 변경 — 백그라운드 에이전트 위임
- 메모리에 [Agent Skills spec reference](file://C:/Users/admin/.claude/projects/C--Kids-math-story-telling/memory/reference_agentskills_spec.md) 저장

## 결정 → INTEGRATED_PLAN §8 결정 7

agentskills.io spec 준수. 신규 스킬 이름 kebab-case. 외부 옛 스킬 underscore 유지.

---

# Round 6 — 동작 1·2 (입력 align + Nick QnA) (2026-05-25)

## NCC 동작 1 — 입력 align 결과

| # | 입력 | 상태 |
|---|---|---|
| 1 | 교과서 chapter | ✅ `30_content/units/01/meta.json` |
| 2 | 정체성 결정 | ✅ §8 결정 1·2 |
| 3 | 시즌·시대 frame | ✅ 시즌 1 ancient |
| 4 | 학년·과정 | ✅ mid1 |
| 5 | 기존 인물 풀 | ✅ 19인 |
| 6 | 후보 수 | ⏳ 미명시 → Q&A |
| 7 | 발굴 우선순위 frame | ⏳ 미명시 → Q&A |
| 8 | 학습자 반응 | ⚠️ .private/feedback/ 별도 확인 |
| 9 | 외부 리서치 허용 범위 | ⏳ 미명시 → Q&A |

## NCC 동작 2 Q — 잠정 안

- #6 top 3 / #7 잘알려진+새발굴 혼합 / #9 Wikipedia + 수학사 얕은~중간

## Nick 답변

"일부 조정 필요" → 후속 raun:
- #6 top 3 유지
- #7 혼합 유지
- #9 **더 깊게 (학술 데이터베이스 포함)**

## 결정 → INTEGRATED_PLAN §8 결정 8

입력 9개 값 확정 표. #9 만 조정 (깊은 리서치).

## 영향

- 동작 3 리서치 판단 = 깊은 patterns 채택
- 동작 4·5 시간 budget ↑
- 발견의 필연성 서사 (약속 3) 원료 확보

## 다음 라운드의 변화

동작 3·4·5 (리서치 + 평가) 진행 방식 결정 — NCC 직접 / 백그라운드 위임 / Nick 함께.

---

# Round 7 — 동작 3·4·5 진행 방식 (2026-05-25)

## NCC 질문

동작 3·4·5 (리서치 + 평가) 실행 방식 — NCC 직접 / 백그라운드 위임 / 하이브리드 / Nick 함께.

## Nick 답변

**하이브리드 (Recommended)**.

## NCC 동작 3 plan (Nick 동의)

- 후보군: 19인 풀 6인 + 신규 발굴 3~5인
- 자료원 3단: Wikipedia → 수학사 → 학술 데이터베이스 (MacTutor)
- 평가: 약속 3겹 + 분포 + 수준 + 시청자 + 시즌

## 백그라운드 위임

`40_experiments/exp-001-selection-unit01/` 신설. output.md / log.md / retrospective.md 생성.

## 결정 → INTEGRATED_PLAN §8 결정 9

진행 방식 = 하이브리드. 동작 3 plan + 동작 4·5 백그라운드.

## 다음 라운드의 변화

백그라운드 완료 → 동작 6 Nick 검토 QnA. top 3 + 선정 이유 + 비교 검증 (에라토스테네스 다시 고르는가) 가 핵심 검토 포인트.

---

(다음 라운드는 백그라운드 완료 후 — 동작 6 진입)
