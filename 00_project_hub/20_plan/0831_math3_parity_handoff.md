<!-- 0831_math3_parity_handoff.md -->
# math3 → math1 수준 완전 패리티 핸드오프 (2026-08-31, 모델 전환용)

> Nick 지시: "남은 작업 모두 진행. 중3 피드백 예정 없음. **math1·2 수준으로 전부 업데이트**."
> 이 문서 = Fable 세션이 Phase A(심화)를 마감한 시점의 정확한 상태 + Phase B(전범위 실전 모의고사) 실행 계획.
> 규약 SSOT = `40_grades/middle/math3/UNITS.md` · 진행 기록 = `00_project_hub/10_chatlog/260830_math3_build.md`(Round 0~14).

## 1. 완료된 것 (Phase A — 단원 심화, 2026-08-31 마감)

- **12단원 전부**: p{N}.html 각 유형 4번째 심화(H) 문항(chips 심화·도전 + `(4)` + 왜? 박스), `TYPES 4×7`, `TOTAL 28`. 은행 `math3/uNN/practice.json` 28문항(L7·M14·H7). 회차 `sets/m3-uNN-d.json`(kind mock, quota {H:1}, "…심화 모의고사", 7문항).
- 도구: `70_tools/print/add_h_problems.py`(스펙 → p페이지+은행+회차, 재실행 방지), `hub_add_unit.py`가 quota={H}이면 태그 "심화"로 표시(a,b,c,**d**,mock 순서 인식).
- 검증 완료: 12단원 verify_bank **오류 0**(V5 누출 3건은 카드 태그 교체로 해결: u04 t01-04/t05-04, u06 t06-04, u08 t07-04) · H 정답 독립 재계산(`70_tools/qa/session/h_check.js` + 스펙 expr) 12단원 0건 · check_page 49페이지 0건 · headless 콘솔 12단원 × u/g/p/d 전부 0 · 캐시 v**20260830n**.
- 프린트: d 회차 빌드 + PDF 24장(`print/uNN/m3-uNN-d_*심화모의고사_*.pdf`) + 허브에 단원당 5회차(유형 a/b/c + 심화 + 모의).
- 이 시점의 커밋/배포: 이 문서와 함께 소스 커밋·배포 리포 mid3 복사·커밋·push까지 완료했음(직전 push 로그 참조). **Phase A는 손댈 것 없음.**

## 2. 남은 것 (Phase B — 중3 전범위 실전 모의고사 6회차, math1 방식)

정본 참조: `70_tools/print/EXAM_SPEC.md`(중1용 원본) · `project_math1_exam_mock.md`(프로젝트 메모리) · 중1 산출물 `30_content/problem_bank/math1/uNN/exam.json`, `sets/exam/m1-exam-{a~f}.json`.

### 2-1. 도구 일반화 (grade 파라미터)
- `verify_exam.py`: `math1`·13단원·`m1-exam-*` 하드코딩 → grade 인자(`--grade math3`) 또는 math3 전용 사본 `verify_exam3.py`(더 안전, 원본 무변형 — **권장**). 바꿀 것: QUOTA 표(아래 2-2), BANK 경로 `math3`, SETS glob `m3-exam-*`, S4 커버리지(2학기 = 단원 **7~12** 회차당 1~3문항, 1학기 = 1~6 합 7~9·단원당 최대 2), BANNED 키워드(중3엔 √·인수분해·이차방정식·삼각비가 **교육과정 안**이므로 중1용 금지어 제거, 대신 고1 밖 키워드: 근의 판별식 D 표기 언급 금지 아님 — 금지어는 `['미분','적분','로그','지수함수','수열','벡터','행렬','허수','복소수']` 정도).
- `build_exam.py`: 88행 `BANK_ROOT / 'math1'` → cfg의 `grade` 필드를 읽게 한 줄 수정(이미 cfg에 grade 있음). 나머지는 무변형으로 재사용 가능.

### 2-2. math3 할당표 (12단원, 합계 = cn45 + cv40 + sh16 + es23 = **124문항**)
중1 표(EXAM_SPEC §5)를 12단원으로 옮긴 제안 — 2학기(7~12)를 두껍게:

| 단원 | cn | cv | sh | es |
|---|---|---|---|---|
| u01 제곱근과실수 | L,M,H | L,M | L | L,M |
| u02 근호계산 | L,M,H | L,M | L | M,H |
| u03 곱셈공식·인수분해 | L,M,M,H | L,M | — | L,M |
| u04 이차방정식 | L,M,M,H | L,M | — | M,H |
| u05 이차함수그래프 | L,M,H | L,M | L | L,M |
| u06 이차함수활용 | L,M,H | L,M | L | M,H |
| u07 삼각비 | L,M,M,H | L,L,M,H | L,M | L,M |
| u08 삼각비활용 | L,M,M,H | L,L,M,H | L,M | M,H |
| u09 원과직선 | L,M,M,H | L,L,M,H,H | L,M | H |
| u10 원주각 | L,M,M,H | L,L,M,H | L,M | M,H |
| u11 산포도 | L,M,M,H | L,L,M,H,H | L,M | H |
| u12 상자그림·산점도 | L,M,M,H | L,L,M,H | L,M | L,M |

id 접두사 `e{NN}-`(예 `e07-cn1`). cv/sh 는 각 단원 practice.json(28문항)에서 골라 `source_id` 기록. **회차 config 6개**: `sets/exam/m3-exam-{a~f}.json` — a/b/c=std(L9 M10 H3), d=easy(L22), e/f=hard(M11 H11), 각 22문항(choice5 15·short 3·essay 4), 배점 choice 3~4·short 4·essay 8, 합 100, **124문항 전부 정확히 1회씩 사용**(122? → 22×6=132 > 124 이므로 위 표를 132가 되게 조정할 것! 예: u03·u04·u05·u06 에 sh1 L 을 넣고(+4), u09·u11 에 es 를 1개씩 추가(H→M,H)(+2), u01·u12 에 cv3 M 추가(+2) = 132. **정확히 132 로 맞춘 뒤 verify 의 "미사용 0" 을 통과시켜야 함**).
- 저작은 **메인 세션 순차**(단원당 10~11문항, EXAM_SPEC §4 규칙: cn 신규·오답보기=오개념 유래·distractor_why 4개·정답 위치 편중 금지, es rubric 합 8, 두 번 독립 검산).
- 검증: `verify_exam3.py uNN` 단원별 0오류 → `--sets` 0오류 → `build_exam.py sets/exam/m3-exam-X.json 60_deploy/print/math3/exam` ×6 → `print_pdf.ps1` ×6(12 PDF) → 육안 2장.
- 허브: `40_grades/middle/math3/print/index.html`의 `<div class="toc">` **앞**에 math1 스타일 `.examhub` 섹션(CSS 포함 — mid1/math1/print/index.html 40~60행 참조, "📝 중3 전 범위 실전 모의고사", 권장 3·쉬움 1·도전 2 카드). PDF는 `print/exam/`(소스, 미추적) + 배포 `mid3/print/exam/`.
- 기록: UNITS.md §6 + chatlog Round 15 + 메모리(project_math3_plan.md) 갱신. 커밋·배포·push 는 기존 규약(파일 단위 add, 네트워크 단독 명령).

## 3. 세션 도구 (스크래치 → repo 로 복사됨)
`70_tools/qa/session/`: `bump_ver.py <dir> <ver>`(캐시 버전 일괄), `run_unit.sh N port`(스크래치 서버+headless 콘솔 — 내부 경로가 옛 스크래치를 가리키면 SP 변수만 수정), `h_check.js`(H 스펙 검산), `units_row.py`(UNITS.md 행 — 12단원 이후엔 불필요). 새 세션 스크래치가 달라지므로 **repo 사본을 쓰거나 새 스크래치로 복사**해서 사용.

## 4. 불변 규약 (요약)
파일 단위 git add(배포 리포) · push/curl/gh 단독 명령 · heredoc 금지 · PYTHONIOENCODING=utf-8 · 해요체 · 자체 문항만 · PDF 소스 리포 미추적 · V5(부분 문자열!) 누출은 카드 태그/문구 교체로 해결 · 캐시 버전은 app3 전 페이지 공통 범프.
