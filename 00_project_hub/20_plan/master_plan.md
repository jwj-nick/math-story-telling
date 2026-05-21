<!-- 00_project_hub/plan/master_plan.md -->
# MathTelling — 전체 단원 제작 마스터 플랜

> 생성: 2026-05-10
> 목적: 13개 단원 순차 제작 진행 현황 추적
> 병렬 진행 금지 — 단원 단위로 순서대로 완료 후 다음 단원 진행

---

## 진행 범례
- ✅ 완료
- 🔄 진행 중
- ⬜ 미시작
- ⏭ 스킵 (근거 있을 때만)

---

## 전체 체크리스트

| # | 단원명 | 인물 | 단원 Phase | chatlog | 완료일 |
|---|---|---|---|---|---|
| 01 | 소인수분해 | 에라토스테네스 | ✅ 완료 | 260509_unit01.md | 2026-05-10 |
| 02 | 정수와유리수 | 브라마굽타 | ✅ 완료 | 260510_unit02.md | 2026-05-10 |
| 03 | 문자와식 | 알콰리즈미 | ✅ 완료 | 260510_unit03.md | 2026-05-10 |
| 04 | 일차방정식 | 디오판토스 | ✅ 완료 | 260510_unit04.md | 2026-05-10 |
| 05 | 좌표와그래프 | 데카르트 | ✅ 완료 | 260510_unit05.md | 2026-05-10 |
| 06 | 정비례와반비례 | 데카르트 | ✅ 완료 | 260510_unit06.md | 2026-05-10 |
| 07 | 기본도형 | 유클리드 | ✅ 완료 | 260510_unit07.md | 2026-05-10 |
| 08 | 작도와합동 | 유클리드 | ✅ 완료 | 260510_unit08.md | 2026-05-10 |
| 09 | 다각형 | 가우스 | ✅ 완료 | 260510_unit09.md | 2026-05-10 |
| 10 | 원과부채꼴 | 아르키메데스 | ✅ 완료 | 260510_unit10.md | 2026-05-10 |
| 11 | 다면체와회전체 | 케플러 | ✅ 완료 | 260510_unit11.md | 2026-05-11 |
| 12 | 입체도형의겉넓이와부피 | (orchestrator 결정) | ⬜ | — | — |
| 13 | 자료의정리와해석 | 나이팅게일 | ✅ 완료 | 260511_unit13.md | 2026-05-11 |

---

## 단원별 Phase 상세

### Unit 01 — 소인수분해 🔄

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | 디렉토리 초기화 | ✅ |
| 1 | 개념 검수 (ncc_audit_concept) | ✅ |
| Phase 3 체크 | L0_거듭제곱표기 literacy 모듈 신규 생성 | ✅ |
| 2 | 이야기 (에라토스테네스, ncc_audit_story) | ✅ |
| 4 | 앱 3종 (index, story, concepts) (ncc_audit_app) | ✅ |
| 5-a | 기본문제 10문제 (basic_app.html) (audit) | ✅ |
| 5-b | 유형 목록 7유형 (types.md) (audit) | ✅ |
| 5-c | 유형별 연습 7×9=63문제 (type_NN_app.html) (audit) | ✅ |
| 5-d | 깊이 탐구 — 소인수분해 (deep_소인수분해_app.html) | ✅ |
| 5-d | 깊이 탐구 — 약수의개수 (deep_약수의개수_app.html) | ✅ |
| 5-d | 깊이 탐구 — 최대공약수 (deep_최대공약수_app.html) | 🔄 |
| 5-d | 깊이 탐구 — 최소공배수 (deep_최소공배수_app.html) | ⬜ |
| 5-d | 깊이 탐구 — GCDxLCM (deep_GCDxLCM_app.html) | ⬜ |

**산출물 현황**:
- story/unit01.md ✅
- app/index.html, story.html, concepts.html ✅
- problems/Q1_source.md, basic_app.html ✅
- problems/types.md ✅
- problems/type_01~07_app.html ✅ (7개)
- problems/deep_소인수분해_app.html, deep_약수의개수_app.html ✅ (2개)
- problems/deep_최대공약수_app.html, deep_최소공배수_app.html, deep_GCDxLCM_app.html ⬜ (3개)

---

### Unit 02 — 정수와유리수 ✅

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | 디렉토리 초기화 | ✅ |
| 1 | 개념 검수 (ncc_audit_concept) | ✅ |
| Phase 3 체크 | 절댓값 기호 → concepts.html 인라인 처리 | ✅ |
| 2 | 이야기 (브라마굽타, ncc_audit_story) | ✅ |
| 4 | 앱 3종 (index, story, concepts) (ncc_audit_app) | ✅ |
| 5-a | 기본문제 10문제 (basic_app.html) (audit) | ✅ |
| 5-b | 유형 목록 7유형 (types.md) (audit) | ✅ |
| 5-c | 유형별 연습 7×9=63문제 (type_NN_app.html) (audit) | ✅ |
| 5-d | deep_절댓값대소_app.html (유형 03+04, 탭 2개) | ✅ |
| 5-d | deep_연산_app.html (유형 05+06, 탭 2개) | ✅ |
| 5-d | deep_혼합계산_app.html (유형 07) | ✅ |

**산출물**: story/unit02.md, app/{index,story,concepts}.html, problems/{Q2_source.md, basic_app.html, types.md, type_01~07_app.html(7개), deep_*.html(3개)}

### Unit 03 — 문자와식 ✅

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | 디렉토리 초기화 | ✅ |
| 1 | 개념 검수 (ncc_audit_concept) | ✅ |
| Phase 3 체크 | L5 곱셈기호생략 → concepts.html 인라인 처리 | ✅ |
| 2 | 이야기 (알콰리즈미, ncc_audit_story) | ✅ |
| 4 | 앱 3종 (index, story, concepts) (ncc_audit_app) | ✅ |
| 5-a | 기본문제 9문제 (basic_app.html) (audit) | ✅ |
| 5-b | 유형 목록 7유형 (types.md) (audit) | ✅ |
| 5-c | 유형별 연습 7×9=63문제 (type_01~07_app.html) (audit) | ✅ |
| 5-d | deep_식세우기_기호생략_app.html (유형 1+2, 탭 4개) | ✅ |
| 5-d | deep_식의값_단다항식_app.html (유형 3+4, 탭 4개) | ✅ |
| 5-d | deep_일차식계산_app.html (유형 5+6+7, 탭 4개) | ✅ |

**산출물**: story/unit03.md, app/{index,story,concepts}.html, problems/{basic_app.html, types.md, type_01~07_app.html(7개), deep_*.html(3개)}

### Unit 04 — 일차방정식 ✅

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | 디렉토리 초기화 | ✅ |
| 1 | 개념 검수 (ncc_audit_concept) | ✅ |
| Phase 3 체크 | ≠ 기호 → concepts.html 인라인 처리 | ✅ |
| 2 | 이야기 (디오판토스, 묘비명 수수께끼·Arithmetica·페르마 연결, ncc_audit_story) | ✅ |
| 4 | 앱 3종 (index, story, concepts) — 저울 SVG, 이항 슬라이더 (ncc_audit_app) | ✅ |
| 5-a | 기본문제 9문제 L×5+M×4 (basic_app.html) (audit) | ✅ |
| 5-b | 유형 목록 7유형 (types.md) (audit) | ✅ |
| 5-c | 유형별 연습 7×9=63문제 (type_01~07_app.html) (audit) | ✅ |
| 5-d | deep_방정식기초_app.html (유형1+2, 탭 2개) | ✅ |
| 5-d | deep_방정식풀기_app.html (유형3+4+5, 탭 3개) | ✅ |
| 5-d | deep_복잡한방정식_app.html (유형6, 단독) | ✅ |
| 5-d | deep_활용_app.html (유형7, 단독) | ✅ |

**산출물**: story/unit04.md, app/{index,story,concepts}.html, problems/{Q4_source.md, basic_app.html, types.md, type_01~07_app.html(7개), deep_*.html(4개)}
**완료일**: 2026-05-10 | chatlog: 260510_unit04.md

### Unit 05 — 좌표와그래프 ✅

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | 디렉토리 초기화 | ✅ |
| 1 | 개념 검수 (ncc_audit_concept) | ✅ |
| Phase 3 체크 | 사분면 로마자(Ⅰ~Ⅳ), 좌표 표기 P(a,b) → concepts.html 인라인 처리 | ✅ |
| 2 | 이야기 (데카르트, 침대 파리·해석기하학·x,y,z 표기 정착, ncc_audit_story) | ✅ |
| 4 | 앱 3종 (index, story, concepts) — JSXGraph 인터랙티브, 사분면 반시계 표기 버그 수정 | ✅ |
| 5-a | 기본문제 9문제 L×5+M×4 (basic_app.html, SVG 미니그래프 2개) | ✅ |
| 5-b | 유형 목록 7유형 (types.md) | ✅ |
| 5-c | 유형별 연습 7×9=63문제 (type_01~07_app.html) | ✅ |
| 5-d | deep_좌표기초_app.html (유형 1+2+3, 탭 3개) | ✅ |
| 5-d | deep_좌표심화_app.html (유형 4+5, 탭 2개) | ✅ |
| 5-d | deep_그래프_app.html (유형 6+7, 탭 2개) | ✅ |

**산출물**: story/unit05.md, app/{index,story,concepts}.html, problems/{Q5_source.md, basic_app.html, types.md, type_01~07_app.html(7개), deep_*.html(3개)}
**완료일**: 2026-05-10 | chatlog: 260510_unit05.md

### Unit 06 — 정비례와반비례 ✅

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | 디렉토리 초기화 | ✅ |
| 1 | 개념 검수 (ncc_audit_concept) | ✅ |
| Phase 3 체크 | y=a/x 음수 a 표기 → concepts.html 인라인 + deep_반비례 강조 | ✅ |
| 2 | 이야기 (데카르트 Unit 05 연계 — 1637 「기하학」, 식↔그림) | ✅ |
| 4 | 앱 3종 (index, story, concepts) — JSXGraph 슬라이더 (a -3~3, -6~6) | ✅ |
| 5-a | 기본문제 9문제 L×5+M×4 (basic_app.html) | ✅ |
| 5-b | 유형 목록 7유형 (types.md) | ✅ |
| 5-c | 유형별 연습 7×9=63문제 (type_01~07_app.html) | ✅ |
| 5-d | deep_정비례_app.html (유형 1+2+5, 탭 3개) | ✅ |
| 5-d | deep_반비례_app.html (유형 3+4+5, 탭 3개, ★ 음수 표기 함정) | ✅ |
| 5-d | deep_식그래프_app.html (유형 6+7, 탭 2개) | ✅ |

**산출물**: story/unit06.md, app/{index,story,concepts}.html, problems/{basic_app.html, types.md, type_01~07_app.html(7개), deep_*.html(3개)}
**완료일**: 2026-05-10 | chatlog: 260510_unit06.md
**핵심**: 학습자 결정적 사례 ($y = -2/x$ 변환) 강력 노출 — concepts/basic/type_03/deep_반비례 4단계 누적

### Unit 07 — 기본도형 ✅

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | 디렉토리 초기화 | ✅ |
| 1 | 개념 검수 (ncc_audit_concept) | ✅ |
| Phase 3 체크 | 6개 기호($\overleftrightarrow{}, \overrightarrow{}, \overline{}, \angle, \perp, \parallel$) → concepts.html 인라인 처리 | ✅ |
| 2 | 이야기 (유클리드, 「원론」+왕도 일화, ncc_audit_story) | ✅ |
| 4 | 앱 3종 (index, story 7p, concepts 6p) — SVG 다이어그램 + 슬라이더 (각도, 맞꼭지각) + 동위각·엇각 셀렉터 | ✅ |
| 5-a | 기본문제 9문제 L×5+M×4 (basic_app.html, SVG 4개) | ✅ |
| 5-b | 유형 목록 7유형 (types.md) | ✅ |
| 5-c | 유형별 연습 7×9=63문제 (type_01~07_app.html) | ✅ |
| 5-d | deep_점선각_app.html (유형 1+2+3, 탭 3개) | ✅ |
| 5-d | deep_각의관계_app.html (유형 4+5, 탭 2개, ★ 보라 톤) | ✅ |
| 5-d | deep_위치관계_app.html (유형 6+7, 탭 2개) | ✅ |

**산출물**: story/unit07.md, app/{index,story,concepts}.html, problems/{basic_app.html, types.md, type_01~07_app.html(7개), deep_*.html(3개)}
**완료일**: 2026-05-10 | chatlog: 260510_unit07.md
**핵심**: 「원론」의 정신(정의→공준→정리) + "왕도 없다" 격려 + 도형 단원 SVG 시각화 적극 활용 + Unit 08 예고(자와 컴퍼스)

### Unit 08 — 작도와합동 ✅

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | 디렉토리 초기화 | ✅ |
| 1 | 개념 검수 (ncc_audit_concept) | ✅ |
| Phase 3 체크 | ≡ (합동) + 작도 약속 → concepts.html 인라인 처리 | ✅ |
| 2 | 이야기 (유클리드, 「원론」 명제 1·4, 자와 컴퍼스 정신, ncc_audit_story) | ✅ |
| 4 | 앱 3종 (index, story 7p, concepts 6p) — 단계별 작도 SVG (수직이등분선·각의 이등분선) + SSA 반례 + 합동 표기 순서 | ✅ |
| 5-a | 기본문제 9문제 L×5+M×4 (basic_app.html, SVG 1개) | ✅ |
| 5-b | 유형 목록 7유형 (types.md) | ✅ |
| 5-c | 유형별 연습 7×9=63문제 (type_01~07_app.html) | ✅ |
| 5-d | deep_작도기초_app.html (유형 1+2, 탭 2개) | ✅ |
| 5-d | deep_이등분선_app.html (유형 3+4, 탭 2개) | ✅ |
| 5-d | deep_삼각형합동_app.html (유형 5+6+7, 탭 3개, ★ 보라 톤) | ✅ |

**산출물**: story/unit08.md, app/{index,story,concepts}.html, problems/{basic_app.html, types.md, type_01~07_app.html(7개), deep_*.html(3개)}
**완료일**: 2026-05-10 | chatlog: 260510_unit08.md
**핵심**: 유클리드 2부작 완성 (Unit 07 책·정의 → Unit 08 손·도구·합동) + 작도-합동 일대일 대응 명시 + ★ SAS 끼인각·합동 표기 순서·AAA vs SSA 함정 다단계 노출 + Unit 09(다각형) 연결 (평행사변형 대각선 이등분)

### Unit 09 — 다각형 ✅
인물: 카를 프리드리히 가우스 (Carl Friedrich Gauss, 1777~1855)

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | 디렉토리 초기화 | ✅ |
| 1 | 개념 검수 (BaseDocs 보완 — 대각선 도출·내각합 분할·외각 한 바퀴 직관) | ✅ |
| Phase 3 체크 | 신규 literacy 모듈 불필요 (concepts.html 인라인) | ✅ |
| 2 | 이야기 (가우스 19살 정 17각형 + 1+2+..+100 짝짓기 정신) | ✅ |
| 4 | 앱 3종 (index, story 7p, concepts 6p) — 슬라이더 5개 (대각선·삼각형 ∠A∠B·분할·외각·정$n$각형) | ✅ |
| 5-a | 기본문제 9문제 L×5+M×4 (basic_app.html) | ✅ |
| 5-b | 유형 목록 7유형 (types.md) | ✅ |
| 5-c | 유형별 연습 7×9=63문제 (type_01~07_app.html) | ✅ |
| 5-d | deep_다각형기초_app.html (유형 1+2, 탭 2개) | ✅ |
| 5-d | deep_내각외각_app.html (유형 3+4+5, 탭 3개) | ✅ |
| 5-d | deep_정다각형종합_app.html (유형 6+7, 탭 2개, ★ 보라 톤) | ✅ |

**산출물**: story/unit09.md, app/{index,story,concepts}.html, problems/{Q9_source.md, basic_app.html, types.md, type_01~07_app.html(7개), deep_*.html(3개)}
**완료일**: 2026-05-10 | chatlog: 260510_unit09.md
**핵심**: Unit 07-08 유클리드 → Unit 09 가우스 인물 다양성 + 가우스 "패턴 발견" 정신 ↔ 다각형 분할 사고 + 정 17각형 → 페르마 소수 (deep) 연결

### Unit 10 — 원과부채꼴 ✅

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | 디렉토리 초기화 | ✅ |
| 1 | 개념 검수 (ncc_audit_concept) | ✅ |
| Phase 3 체크 | π 표기 → concepts.html 인라인 처리 | ✅ |
| 2 | 이야기 (아르키메데스 — 시라쿠사·유레카·원기둥 안의 구) | ✅ |
| 4 | 앱 3종 (index, story, concepts + JSXGraph 슬라이더) | ✅ |
| 5-a | 기본문제 9문제 (basic_app.html, 함정 25π 의도적 배치) | ✅ |
| 5-b | 유형 목록 7유형 (types.md) | ✅ |
| 5-c | 유형별 연습 7×9=63문제 (검산 포함) | ✅ |
| 5-d | deep_원기초_app.html (유형 1+2, 탭 2개) | ✅ |
| 5-d | deep_부채꼴_app.html (유형 3+4+5, 탭 3개) | ✅ |
| 5-d | deep_관계와색칠_app.html (유형 6+7, 탭 2개, ★ 보라 톤) | ✅ |

**산출물**: story/unit10.md, app/{index,story,concepts}.html, problems/{Q10_source.md, basic_app.html, types.md, type_01~07_app.html(7개), deep_*.html(3개)}
**완료일**: 2026-05-10 | chatlog: 260510_unit10.md
**핵심**: 아르키메데스 인물 신규 + 원의 측정 방법론 + ★ 호·현 비례 함정 다단계 노출 (concepts → type_06 → deep_관계와색칠)

### Unit 11 — 다면체와회전체 ✅
인물: 요하네스 케플러 (Johannes Kepler, 1571~1630) — 신규 인물

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | 디렉토리 초기화 | ✅ |
| 1 | 개념 검수 (BaseDocs 33+29행 → 풀 스펙 보완) | ✅ |
| Phase 3 체크 | V-E+F=2, 모선, 회전축·축단면 → concepts.html 인라인 처리 | ✅ |
| 2 | 이야기 (케플러 — 정다면체-행성 모델·어머니 변호·Stereometria) | ✅ |
| 4 | 앱 3종 (index, story 8p, concepts 7p — n슬라이더, 5정다면체 클릭, 회전체 클릭, 단면 클릭) | ✅ |
| 5-a | 기본문제 9문제 L×5+M×4 (basic_app.html, Q7-Q9 ★ 함정) | ✅ |
| 5-b | 유형 목록 7유형 (types.md) | ✅ |
| 5-c | 유형별 연습 7×9=63문제 (type_01~07_app.html) | ✅ |
| 5-d | deep_다면체기초_app.html (유형 1+2, 탭 2개) | ✅ |
| 5-d | deep_정다면체_app.html (유형 3, 단독, ★ 보라 톤) | ✅ |
| 5-d | deep_회전체_app.html (유형 4+5+6+7, 탭 4개) | ✅ |

**산출물**: story/unit11.md, app/{index,story,concepts}.html, problems/{Q11_source.md, basic_app.html, types.md, type_01~07_app.html(7개), deep_*.html(3개)}
**완료일**: 2026-05-11 | chatlog: 260510_unit11.md
**핵심**: 케플러 신규 인물 (16-17세기 독일) + 정다면체-행성 모델 "틀린 가설도 위대" 메시지 + ★ 수직 단면 vs 축단면 5단계 누적 노출 + ★ 정다면체 두 조건 (정사각뿔 X) 5단계 노출 + Unit 12(부피) 예고

### Unit 12 — 입체도형의겉넓이와부피 ✅
인물: 카발리에리 (Bonaventura Cavalieri, 1598~1647) — 단면 비교로 부피 측정 일반 원리

| Phase | 산출물 | 상태 |
|---|---|---|
| 0 | 디렉토리 5종 | ✅ |
| 1 | 40_BaseDocs/12_입체도형의겉넓이와부피 보완 | ✅ |
| 2 | story/unit12.md (8장 + 잡학 + 글쓰기 미션) | ✅ |
| 4 | app/{index, story, concepts}.html (슬라이더 4종 + SVG 3종) | ✅ |
| 5-a | problems/basic_app.html (9문제) | ✅ |
| 5-b | problems/types.md (7유형) | ✅ |
| 5-c | type_01~07_app.html (7개 × L/M/H 9문제 = 63문제) | ✅ |
| 5-d | deep_각기둥뿔/deep_원기둥뿔구/deep_복합회전_app.html (통합 3개) | ✅ |

**산출물**: story/unit12.md, app/{index,story,concepts}.html, problems/{Q12_source.md, basic_app.html, types.md, type_01~07_app.html(7개), deep_각기둥뿔/deep_원기둥뿔구/deep_복합회전_app.html(3개)}
**완료일**: 2026-05-11 | chatlog: 260511_unit12.md
**핵심**: 카발리에리 신규 인물 (17C 이탈리아, 갈릴레오 직제자) + 단면=부피 직관 (종이 더미) + Unit 10 아르키메데스(1:2:3) + Unit 11 케플러(술통) 자연 계보 + ★ 4대 함정 (1/3, h vs l, 반구 평면원, 단위 cm² vs cm³)

### Unit 13 — 자료의정리와해석 ✅
인물: 플로렌스 나이팅게일 (1820~1910, 영국) — 코크스콤 차트, 통계로 생명 구하기

| Phase | 산출물 | 상태 |
|---|---|---|
| 0 | 디렉토리 5종 | ✅ |
| 1 | 40_BaseDocs/13 보완 (이상/미만, 넓이 공식, 3변수 관계식) | ✅ |
| Phase 3 체크 | "이상/미만"은 일상어, 신규 literacy 모듈 불필요 | ✅ |
| 2 | story/unit13.md (12장, 코크스콤 발명 서사) | ✅ |
| 4 | app/{index, story, concepts}.html — 코크스콤 SVG 재현 + 상대도수 슬라이더 | ✅ |
| 5-a | problems/basic_app.html (9문제 L×5+M×4) | ✅ |
| 5-b | problems/types.md (7유형) | ✅ |
| 5-c | type_01~07_app.html (7개 × 9문제 = 63문제) | ✅ |
| 5-d | deep_자료정리/deep_그래프/deep_상대도수종합_app.html (통합 3개) | ✅ |

**산출물**: story/unit13.md, app/{index,story,concepts}.html, problems/{Q13_source.md, basic_app.html, types.md, type_01~07_app.html(7개), deep_자료정리/deep_그래프/deep_상대도수종합_app.html(3개)}
**완료일**: 2026-05-11 | chatlog: 260511_unit13.md
**핵심**: 나이팅게일 신규 인물 (19C 영국) + 여성 모델 + 데이터 시각화 시조 + 코크스콤 차트 SVG 재현 + ★ 상대도수 3변수 함정 다단계 노출 (concepts 인터랙티브 → basic Q7 → type_06 → deep_상대도수종합) + 13단원 마무리 메시지 (12명 수학자 여정)

---

## 🎉 13단원 전체 완료 (2026-05-11)

| 인물 | 단원 | 핵심 |
|---|---|---|
| 에라토스테네스 | 01 소인수분해 | 베타·소수의 체·지구 둘레 |
| 브라마굽타 | 02 정수와유리수 | 음수 발견·인도 수학 |
| 알콰리즈미 | 03 문자와식 | 지혜의 집·alJabr |
| 디오판토스 | 04 일차방정식 | 묘비명 수수께끼·Arithmetica |
| 데카르트 | 05 좌표와그래프 | 침대 위 파리·해석기하학 |
| 데카르트 | 06 정비례와반비례 | 식↔그림 결혼 |
| 유클리드 | 07 기본도형 | 원론·왕도 없음 |
| 유클리드 | 08 작도와합동 | 자와 컴퍼스 |
| 가우스 | 09 다각형 | 정17각형·1~100 짝짓기 |
| 아르키메데스 | 10 원과부채꼴 | 시라쿠사·1:2:3 |
| 케플러 | 11 다면체와회전체 | 정다면체-행성·Stereometria |
| 카발리에리 | 12 입체도형의겉넓이와부피 | 단면=부피·갈릴레오 직제자 |
| **나이팅게일** | **13 자료의정리와해석** | **코크스콤·통계로 생명** |

**총 산출물**: 13단원 × (story + app 3종 + basic + types + type 7개 + deep 3개) ≈ 200개 HTML/MD 파일
**기간**: 2026-05-09 ~ 2026-05-11 (3일)
**다음 단계**: Nick 리뷰 → 2026-06 딸과 본격 학습 시작

---

## 실행 이력

| 날짜 | 작업 | 결과 |
|---|---|---|
| 2026-05-09 | Unit 01 전체 파이프라인 (Phase 0~5-d 일부) | Phase 5-d 3개 미완, timeout |
| 2026-05-10 | Master plan 생성 | 이 파일 |
| 2026-05-10 | Unit 01 Phase 5-d 완료 (deep_GCD_LCM_app.html 통합) | ✅ |
| 2026-05-10 | Unit 02 전체 파이프라인 (Phase 0~5d) | ✅ 완료 |
| 2026-05-10 | Unit 03 Phase 5-a~5d 감사·버그수정·chatlog 완성 | ✅ 완료 |
| 2026-05-10 | Unit 04 전체 파이프라인 (Phase 0~5d) | ✅ 완료 |
| 2026-05-10 | Unit 05 전체 파이프라인 (Phase 0~5d) | ✅ 완료 |
| 2026-05-10 | Unit 06 전체 파이프라인 (Phase 0~5d) | ✅ 완료 |
| 2026-05-10 | Unit 07 전체 파이프라인 (Phase 0~5d) | ✅ 완료 |
| 2026-05-10 | Unit 08 전체 파이프라인 (Phase 0~5d) | ✅ 완료 |
| 2026-05-10 | Unit 09 전체 파이프라인 (Phase 0~5d) — 가우스 신규 인물 | ✅ 완료 |
| 2026-05-10 | Unit 10 전체 파이프라인 (Phase 0~5d) — 아르키메데스 신규 인물 | ✅ 완료 |
| 2026-05-11 | Unit 11 전체 파이프라인 (Phase 0~5d) — 케플러 신규 인물 | ✅ 완료 |
| 2026-05-11 | Unit 12 전체 파이프라인 (Phase 0~5d) — 카발리에리 신규 인물 | ✅ 완료 |
| 2026-05-11 | Unit 13 전체 파이프라인 (Phase 0~5d) — 나이팅게일 신규 인물 | ✅ 완료 |
| 2026-05-11 | **13단원 전체 마스터 플랜 완료** 🎉 | ✅ 완료 |
