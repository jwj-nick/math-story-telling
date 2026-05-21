# Q07 — 인물 도우미 skill: MathTelling `/story-write` 와 합류할 것인가?

> 상태: 🔴 미결. 두 프로젝트 간 skill 공유의 첫 사례.

## 질문

- MathTelling: `/story-write unit01 에라토스테네스` → 수학자 스토리 1편 (단원과 결합)
- HighSchool (P04): 정도전 3 앱 (가이드·모범답안·심화) — 인물 분석 도우미

두 skill·패턴은 **"인물 리서치 + 학습용 콘텐츠"** 라는 공통 부분이 있음.

## 옵션

### (A) 두 skill 완전 별개

- `/story-write` 는 그대로 (수학 단원 컨텍스트)
- `/perf-eval-person` 신규 (수행평가 컨텍스트)
- 코드·리서치 자료 공유 X
- 단순, 결합도 ↓

### (B) 공통 sub-skill `/person-research` 추출

- `/person-research <인물>` → 인물 기본 정보 JSON 또는 .md 산출
  - 시대 배경 / 주요 사건 / 사상·저서 / 인용구 / 신뢰 출처
- `/story-write` 와 `/perf-eval-person` 둘 다 이걸 호출하고, 자기 형식으로 변환

### (C) 하나의 통합 skill `/person`

- `/person 정도전 --output=perfeval-3app`
- `/person 에라토스테네스 --output=mathtelling-unit01`
- 출력 모드를 인자로 분기
- skill 1개, 옵션 많음

## 비교

| | (A) 별개 | (B) sub-skill | (C) 통합 |
|---|---|---|---|
| 개발 | 빠름, 단순 | 중간 | 복잡 |
| 자료 정확성 | 각자 따로 검증 | 공통 검증 1회 | 공통 검증 1회 |
| 두 프로젝트 공유 | X | ✅ research 부분만 | ✅ 전체 |
| 시범 사례 후 평가 | 쉬움 | 중간 | 어려움 |

## NCC 제안

**(B) sub-skill 분리** 가 안정적.

- 인물 리서치는 정확성이 중요 → 공통 sub-skill에서 한 번 검증
- 출력은 프로젝트별 별도 skill에서 형식 변환
- Q02 (skill 중앙화) 와도 자연스럽게 맞물림 — `_canonical/skills/person-research/` 같은 형태

## (Nick) 응답

> (Nick): B. 내가 원하는 방향임. 다른 주제에 대해서도 비슷한 방식을 적용 가능.
전체적으로 agent, skill 의 prefix 를 사용합시다. 'se_agent_' (agent) , 'se_' (skill) 가 좋겠습나다. 내 아이들 이름과 관련됨.

---

## 결정 후 적용
- 50_BLUEPRINTS.md B02 항목 명세 갱신
- Q02 결정에 따라 sub-skill 위치 확정
