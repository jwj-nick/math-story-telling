<!-- 0829_math3_handoff.md -->
# 핸드오프 — 중3 수학(math3) 신규 제작 (compact 후 Sonnet 자율진행용)

> **이 문서 하나만 읽고 착수할 수 있게 쓴다.** 결정 배경 = `00_project_hub/10_chatlog/260829_concept_fun_ideas.md` Round 5.
> 작성 2026-08-29 · Nick 결정("중3수학으로 넘어가자", 자율진행) · 시작 시점 태그 `concept-fun-p1-260829`(소스 `9983a5f` / 배포 `a93f92d`).
> 진행 기록은 **새 chatlog `00_project_hub/10_chatlog/260830_math3_build.md`**를 만들어 단원마다 Round로 남긴다. 세션 시작 시 chat 창에 chatlog 파일명을 밝힐 것(CLAUDE.md 관행).

## 0. 한 줄 목표

중2 앱(`mid2`)과 같은 구조·같은 품질의 **중3 수학 앱 `mid3`**를 만든다 — 12단원 × (개념 u · 놀이터 g · 연습 p · 심화탐구 d) + 단원별 프린트 학습지. **2022 개정 교육과정** 기준(딸이 중3가 되는 해에 적용). 인물 이야기·영상(축 B)은 이번 범위 밖.

**HITL 없음.** 단원 1을 파일럿으로 자가 감사를 강하게 걸고, 그 뒤 단원 2~12를 같은 사이클로 자율 완주한다. Nick은 chatlog와 라이브 링크로 아무 때나 본다.

## 1. 반드시 지킬 것

- **우선순위 (a) 흥미·이해 > (b) 기본 문제 실전력 > (c)**. 스트레스 없는 진행이 KPI — `10_system/20_context/LEARNER_PROFILE.md`(중하위, 언어 우위, "왜?"가 있어야 흡수, 손그림·민트·과하지 않은 취향).
- 학생용 문구 전부 **해요체** (`10_system/10_principles/WRITING_VOICE.md`). 앱 원칙 `10_system/10_principles/APP_PRINCIPLES.md`, 프린트 규격 `10_system/10_principles/PRINT_PRINCIPLES.md`.
- **자체 문제만.** 교육과정의 표준 유형만 차용, 특정 교재(비상 등) 복제 금지.
- **소스가 정본** (`C:\Kids\math-story-telling`) → 검증 → 배포 리포(`C:\Nick\30_Apps\jwj-nick.github.io`)로 복사 → 양쪽 커밋. 배포 리포는 **파일 단위 `git add`만**(다른 세션의 `high1/hanja/` 작업이 공존). 처음 만지는 배포 파일은 덮어쓰기 전에 소스와 diff.
- **네트워크 명령(`git push`·curl·gh)은 단독 명령으로.** 로컬 작업·커밋을 먼저 끝내고 push. heredoc 금지, `PYTHONIOENCODING=utf-8` 선제, 스크립트는 파일로 Write→실행 (CLAUDE.md 멈춤 방지 프로토콜).
- **서브에이전트 병렬 다수 실행은 세션 한도를 트리거**한 전력이 있다 → 페이지 저작은 메인 세션 순차, 에이전트는 동시 1~2개 이하(문제은행 저작 정도). 단원 1개 = 1사이클, 사이클마다 커밋.
- 시험·교육과정 사실은 추측하지 말고 확인(§2 단원표는 P0에서 재검증).

## 2. 단원표 (2022 개정 기준 초안 — P0에서 재검증 후 확정)

2022 개정 중3 내용 체계(교육부 고시 2022-33호, 나무위키 "2022 개정 교육과정/수학과/중학교/수학 3" 요약): 수와 연산 **제곱근과 실수** / 변화와 관계 **다항식의 곱셈과 인수분해 · 이차방정식 · 이차함수와 그 그래프**(최댓값·최솟값이 고1에서 중3로 내려옴, 실수 전체 범위만) / 도형과 측정 **삼각비 · 원의 성질** / 자료와 가능성 **산포도 · 상자 그림과 산점도**(상자그림·산점도·상관관계가 처음 들어옴). 대푯값은 중1~3 통합 내용으로 다뤄지므로 통계 단원 앞에 짧은 복습으로.

교과서 단위로 쪼개면(중2의 11단원과 같은 굵기):

| # | 학기 | 단원(id) | 핵심 | 색 토큰(u / u2) 제안 |
|---|---|---|---|---|
| 1 | 1 | 제곱근과 실수 | 제곱근의 뜻·성질, 무리수, 실수의 대소 | `#4f92d6` / `#77b2ea` |
| 2 | 1 | 근호를 포함한 식의 계산 | 곱셈·나눗셈, 분모의 유리화, 덧셈·뺄셈 | `#3fa89a` / `#63c6b1` |
| 3 | 1 | 다항식의 곱셈과 인수분해 | 곱셈공식 4종, 인수분해 공식, 공식 활용 | `#8f7bd4` / `#b19ce6` |
| 4 | 1 | 이차방정식 | 인수분해·제곱근·완전제곱식·근의 공식, 근의 개수, 활용 | `#d76a9c` / `#e88fb0` |
| 5 | 1 | 이차함수와 그래프 | y=ax², 평행이동, y=a(x−p)²+q | `#e0973a` / `#f0b45f` |
| 6 | 1 | 이차함수의 활용 | y=ax²+bx+c 일반형→표준형, 축·꼭짓점, **최댓값·최솟값**(2022 신설) | `#e2698a` / `#f0929f` |
| 7 | 2 | 삼각비 | sin·cos·tan, 특수각, 삼각비의 표 | `#4a9a5f` / `#6fbf82` |
| 8 | 2 | 삼각비의 활용 | 길이·높이·넓이 구하기 | `#c77d9e` / `#e0a0bd` |
| 9 | 2 | 원과 직선 | 현의 성질, 접선의 길이 | `#4f9bb5` / `#75bcd0` |
| 10 | 2 | 원주각 | 원주각의 성질, 원에 내접하는 사각형, 접선과 현이 이루는 각 | `#d68a4a` / `#eaad70` |
| 11 | 2 | 산포도 | 대푯값 복습 → 편차·분산·표준편차 | `#7a8a9a` / `#9aabb8` |
| 12 | 2 | 상자 그림과 산점도 | 사분위수·상자그림, 산점도, 양·음·없음 상관관계 | `#b06ad0` / `#c98fe0` |

**P0 재검증 방법**: 나무위키 2022 개정 중3 페이지 + 교육부 성취기준(웹 검색)으로 위 12개가 빠짐·초과 없는지 확인. 2027년용 2022 개정 중3 검정 교과서 목차가 아직 공개 전이면 이 표를 그대로 쓴다. 확정 표는 `40_grades/middle/math3/UNITS.md`에 기록.

## 3. 디렉토리·엔진 (P0 스캐폴딩)

| 역할 | 소스(정본) | 배포 | 참고 원본 |
|---|---|---|---|
| 앱 | `40_grades/middle/math3/app3/` | `jwj-nick.github.io/mid3/` (**flat**, mid2와 동일. mid1처럼 `math1/app1` 중첩 아님) | `40_grades/middle/math2/app2/` |
| 엔진 | `app3/concept.js`·`concept.css` | `mid3/concept.js`·`concept.css` | **`math2/app2/concept.{js,css}` 현재본을 포크** — 재미 1순위(정답 애니·힌트 우선·완주 도장·이어하기)가 이미 들어 있는 상태 |
| 허브 | `app3/index.html` | `mid3/index.html` | `math2/app2/index.html` |
| 프린트 허브 | `40_grades/middle/math3/print/index.html`(신규) | `mid3/print/index.html` | `mid2/print/index.html`(자체 사이드바 패턴) |
| 문제은행 | `30_content/problem_bank/math3/uNN/practice.json` · `misconceptions/math3_uNN.json` · `sets/m3-uNN-{a,b,c,mock}.json` | — (PDF는 `40_grades/middle/math3/print/uNN/`, **git 미추적**, 배포 리포엔 복사) | math2 동명 파일 |
| 학년 허브 카드 | (소스 없음) | `mid1/index.html` "학년별 수학" grid에 **중3 수학 카드** 추가(→`../mid3/index.html`) | 이 파일은 배포 전용(소스 없음) — 직접 편집 |

**엔진 포크 시 바꿀 지점(전부):**
1. 헤더 주석·`window.MJ` → **`window.MJ3`** (페이지들도 `MJ3.boot()`, `MJ3.check…`). localStorage 키 `m2theme/m2progress/m2checks` → **`m3theme/m3progress/m3checks`**.
2. `UNITS` 12개(§2 표, 7~12에 `sem:2`). `pageInfo()` 정규식 `([1-9]|1[01])` → **`([1-9]|1[0-2])`** 6곳 전부.
3. 탭: **개념(u) → 놀이터(g) → 연습(p) → 심화 탐구(d)** 4탭(math1 app1 표준). `deepq`(dNp)는 tabs 배열에서 제거. `x`(탐험)는 `EXPLORE_READY`에 넣은 단원만 노출 — 자산 있을 때만(§7).
4. 사이드바 브랜드 "중3 수학<small>1·2학기</small>", 도구 링크 = **중3 프린트(`print/index.html`) · 놀이터(`g1.html`)** 두 개(계산 연습·탐험 링크 제거). `PLAY_READY`는 놀이터 완성 단원만 — 빈 객체에서 시작해 단원 완료마다 추가.
5. `concept.css`는 그대로(단원색은 JS가 덮어씀). 허브 `index.html`: crumbs `<a href="../mid1/index.html">← 중학 앱</a> · <a href="../mid2/index.html">중2 수학 ↗</a>`, 히어로 문구 중3용, 1학기/2학기 섹션, 미완성 단원은 `.unit.soon` 카드("준비 중")로 두어 404 없음.
6. 캐시버전은 앱 전체 **한 값**(`?v=20260830a`부터, 엔진 수정 시 bump). 확인: `grep -ho "concept\.\(css\|js\)?v=[0-9a-z]*" *.html | sort | uniq -c` → 두 줄 × 같은 수.
7. `mid2/index.html`·`mid1/math1/app1/index.html` crumbs에 "중3 수학 ↗"를 굳이 넣지 않는다(허브 카드로 충분).

P0 완료 기준: 엔진·허브·프린트 허브(빈 목록)·`mid3/`·`mid1` 카드가 배포돼 https://jwj-nick.github.io/mid3/ 가 열리고 12단원이 "준비 중" 카드로 보인다.

## 4. 단원당 표준 사이클 (P1 파일럿 = 단원 1, 이후 2~12 동일)

### ① 4페이지 저작 — 템플릿은 **중2 `app2/u10·g10·p10·d10`** + **중1 `app1/u6·g6·p6·d6`**(둘 다 읽고 구조를 따른다)
- **u{N}.html 개념**: 8~9섹션 여정(이어서 → 핵심 → ★직접 움직여 봐요(슬라이더/SVG) → … → 내 말로(teach-back textarea + "다른 설명도 보기" `reveal('showex','exbox')`) → 다음). 확인 문제 5~6개(`c1`/`c1b`/`c1o` 규약 엄수 — 이어하기가 이 규약을 씀), `makeProgress('prog',4~5)`, `did(k)` 키로 완주. `#done-note` 유지. 250줄 안팎.
- **g{N}.html 놀이터**: 4위젯(판별사/짝꿍찾기/감별사/오류탐정 류 — 중1 `0811_interest_playground_plan.md` §2b 톤). 점수 배지·`.stamp`·인라인 confetti(g6 참고, 또는 `MJ3.confetti(host)` 사용).
- **p{N}.html 연습**: 7유형 × 3문항(L/M/H) = 21문항, Generation D `.mission/.pq` 마크업(중1 p6 그대로) — **프린트 추출기 `70_tools/print/extract_math2_p.py`가 이 마크업을 읽는다**, 마크업을 바꾸지 말 것.
- **d{N}.html 심화탐구**: 시뮬레이터 1~2개(`.sim`) + 유도(`.derive .step`) + 도전 1개(`hintSteps`). 기하 단원은 `MJ3.makeGeo`, 함수 단원은 `MJ3.makePlane`.
- 문구 전부 해요체. 수식은 `.eq` + 유니코드(², √, −). KaTeX 없음.

### ② 검증 (전부 통과해야 ③)
- `node --check`는 엔진에만; 페이지 인라인 스크립트는 **Node로 파싱**(`new Function`)해 구문 확인. 참조 id 전수 정의 확인(`getElementById('x')`의 x가 HTML에 있는지) — 오타 하나로 페이지가 죽는다.
- `html.parser` 스택 기반 태그 균형 검증(대량 편집 후 구조 붕괴 사고 전력).
- 로컬 서버는 **반드시 새 포트**(`python -m http.server 85xx --bind 127.0.0.1 --directory <스크래치 srv>`; 끝나면 PID kill). 유령 서버가 옛 파일을 정상처럼 돌려준 사고 있음.
- **headless Chrome**(브라우저 확장 스크린샷은 이 환경에서 타임아웃 잦음): `"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless --disable-gpu --no-sandbox --disable-extensions --user-data-dir=<임시> --enable-logging=stderr --v=0 --virtual-time-budget=3000 --dump-dom <url> > out.html 2> err.txt` → `grep CONSOLE err.txt` 0건. 스크린샷은 `--window-size=1000,1400 --screenshot=x.png`로 찍어 Read.
- **동작 검증 하네스**: `70_tools/qa/iframe_harness_template.html`(같은 오리진 iframe에 페이지를 띄워 실제 클릭·입력 시나리오를 돌리고 `#log`에 사실을 남김 → `--dump-dom`으로 수확). 파일럿 단원(u1)은 이걸로 정답/오답/이어하기/완주 시나리오까지 돌린다. 이후 단원은 콘솔 0 + 스크린샷 2장(u·p)으로 충분.
- 정답 재계산: p 페이지의 모든 정답을 Node로 독립 재계산(중2 때 정립한 방식 — 연립=Cramer 등. 중3는 근의 공식·인수분해·삼각비 값·분산을 각각 함수로).

### ③ 엔진 연결 — `PLAY_READY`에 단원 번호 추가, 허브 `index.html` 카드 `.soon`→실카드, 캐시버전 bump(엔진 바뀐 경우만).

### ④ 커밋·배포 — 소스 `git add` 파일 지정 → 커밋 → 배포 폴더로 복사(html·js·css) → 배포 `git add` 파일 단위 → 커밋 → `git push` 단독(두 리포). 라이브 확인은 `WebFetch`로 `https://raw.githubusercontent.com/jwj-nick/jwj-nick.github.io/main/mid3/<file>`(Pages CDN은 몇 분 지연).

### ⑤ 프린트 — 스킬 `/se-print-sheet` + `70_tools/print/`
1. `misconceptions/math3_uNN.json` 저작(오개념 카드 6~8장: label/counter/ask/empathy/check/link) — **저작 전 V5 리크 사전점검**: counter/ask/empathy에 예정 정답 문자열이 literal로 들어가면 안 됨.
2. `python 70_tools/print/extract_math2_p.py`로 p{N}.html에서 21문항 추출 → `practice.json` 저작(7유형 × L/M/H, `answer_atoms`=앱 disp 문자 그대로, `answer_print`는 같은 문자 — ASCII `-`와 유니코드 `−` 혼용 금지). H(도전) 1문항/유형 추가 시 `<span class="chip lv3">도전</span>` 규약.
3. `python 70_tools/print/verify_bank.py math3 uNN` → **0 오류**. (P0에서 `build_sheet.py`/`verify_bank.py`가 `grade`를 경로에 그대로 쓰는지 grep 확인 — `cfg['grade']` → `40_grades/middle/{grade}/print/uNN`.)
4. sets `m3-uNN-{a,b,c}.json`(유형 세트 9문항, H 자동 제외) + `m3-uNN-mock.json`(`kind:"mock"`, `pick:{"quota":{"H":1}}`) → `build_sheet.py` → `print_pdf.ps1`(headless Chrome) → Q/K PDF 8장 → 육안 2장(Read) → `40_grades/middle/math3/print/uNN/`(미추적) + 배포 `mid3/print/uNN/` 복사 + `mid3/print/index.html`에 단원 블록 추가(**반복 삽입 스크립트의 마지막 항목 경계 주의** → html.parser 재검증).

### ⑥ chatlog Round — 무엇을 만들었고(페이지 4 + 문항 수 + 프린트 회차), 무엇을 검증했고(콘솔 0·스크린샷·verify 0), 커밋 해시 2개, 판단이 필요했던 지점.

## 5. 답 형식 규약 (중3 특유 — 파일럿에서 확정해 `UNITS.md`에 적어 둘 것)

앱 확인 문제는 `checkNum`(정수) 또는 `check(id, test, out, opt)`(함수 판정)만 쓴다. 중3는 답이 √·분수·두 근·좌표인 경우가 많으므로:

| 답 종류 | 규약 | 예 |
|---|---|---|
| a√b 꼴 | 질문에 "(근호 안의 수만)" 또는 "(근호 앞 계수만)" 병기, 숫자 하나만 입력 | 3√2 → "계수는?" 3 / "근호 안은?" 2 |
| 분수·삼각비 값 | `check`에 함수 판정: `"1/2"`·`"0.5"` 둘 다 허용(`raw` 문자열에서 `/` 파싱) | sin30° |
| 이차방정식 두 근 | "작은 근" 또는 "두 근의 합/곱"으로 한 수만 묻기. 두 근 다 필요하면 입력 2개(`c3`,`c4`) | x²−5x+6=0 → 작은 근 2 |
| 좌표·꼭짓점 | 입력 2개(x, y) 또는 "x좌표만" | 꼭짓점 (1, −3) |
| 부호 있는 답 | 입력은 `-`(ASCII) 그대로 받되 `check`가 `−`도 정규화(엔진이 이미 함) | −3 |
| 상관관계·분류 | 입력 대신 2~3지선다 버튼(`pick`) | 양/음/없음 |
| π·√ 표기(지면) | `answer_print`는 유니코드 √(U+221A)·² 사용, `.frac` 마크업 | — |

## 6. 순서·페이스

| 단계 | 내용 | 완료 판정 |
|---|---|---|
| P0 | 단원표 재검증 → `UNITS.md` · 엔진 포크 · 허브 · 프린트 허브(빈) · `mid3/` 배포 · `mid1` 카드 | https://jwj-nick.github.io/mid3/ 열림, 콘솔 0 |
| P1 ★파일럿 | 단원 1(제곱근과 실수) 전체 사이클 ①~⑥ + 하네스 동작 검증 + §5 규약 확정 | chatlog Round 1, 양 리포 push |
| P2 | 단원 2~6 순차 | 1학기 완료 시 태그 `math3-sem1-YYMMDD` |
| P3 | 단원 7~12 순차 | 2학기 완료 시 태그 `math3-sem2-YYMMDD` + 메모리 갱신 |
| P4(Nick 결정 대기) | 전범위 실전 모의고사(중1의 `70_tools/print/build_exam.py`·`EXAM_SPEC.md` 재사용) | — |

세션이 끊기면 다음 세션은 chatlog 마지막 Round + `git log`로 복구해 이어간다. "실패"로 보고된 에이전트도 산출물이 있을 수 있으니 파일로 확인.

## 7. 하지 않는 것 / 조건부

- 인물 이야기·영상(축 B), 수학 언어 트랙(축 C) 확장 — 범위 밖.
- `d{N}p`(심화문제)·`drill` — 만들지 않음.
- `x{N}`(탐험)은 **PhET 한국어 sim이 있는 단원만** 조건부: 이차함수(PhET "Graphing Quadratics"), 삼각비(PhET "Trig Tour"). GeoGebra는 쓰지 않음(Nick: "GeoGebra 별로"). 나머지는 d 페이지 자체 SVG sim.
- 중1·중2 앱 수정 — 이번 라운드엔 손대지 않음(허브 카드 추가만).

## 8. 완료 판정

12단원 × 4페이지 + 프린트 12단원(회차 4개씩) 배포, https://jwj-nick.github.io/mid3/ 에서 전 단원 열림·콘솔 0·이어하기/완주 동작, `mid1/` 허브에 중1·중2·중3 카드 3개, chatlog Round 12+ 기록, 태그 2개, 메모리(`project_math3_plan.md`) 갱신.
