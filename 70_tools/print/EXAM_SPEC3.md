<!-- EXAM_SPEC3.md — 중3 실전 모의고사 문항 풀(exam.json) 저작 스펙 (2026-08-31) -->
# 중3 실전 모의고사 — exam.json 저작 스펙

> `EXAM_SPEC.md`(중1판)를 math3(12단원)에 맞춰 이식. 목적·구조·검증 흐름은 동일하고, 할당표·금지 키워드·답 표기만 중3에 맞게 바뀐다.
> 이 풀에서 회차 조립 스크립트가 6회차를 뽑으므로 **할당표의 id·format·level은 한 글자도 바꾸면 안 된다.**

## 1. 파일 위치와 최상위 구조

`30_content/problem_bank/math3/u{NN}/exam.json` (단원당 1파일, 신규. 기존 practice.json은 **읽기 전용**):

```json
{
  "meta": {
    "grade": "math3", "unit": 7, "unit_name": "삼각비",
    "purpose": "exam-pool", "authored": "2026-08-31",
    "note": "중3 전범위 실전 모의고사용 문항 풀. EXAM_SPEC3.md 준수."
  },
  "problems": [ ...할당표 순서대로... ]
}
```

## 2. 문항 스키마

공통 필드 (practice.json과 같은 표기 규약):

| 필드 | 값 |
|---|---|
| `id` | 할당표 그대로. 예 `e07-cn1` |
| `format` | `"choice5"` \| `"short"` \| `"essay"` |
| `level` | 할당표 그대로 `"L"`/`"M"`/`"H"` |
| `topic` | 무엇을 재는지 짧은 라벨 (예 "삼각비의 뜻") |
| `source_id` | cv/sh 만: 원본 practice.json 문항 id. cn/es 는 `null` |
| `stem_print` | 발문. 시험체(…를 구하시오 / …의 값은?) |
| `answer_print` | 정답 (choice5 는 정답 보기의 문자열과 완전 동일) |
| `answer_accept` | 이렇게 써도 맞는 표현 배열 또는 `null` (choice5 는 `null`) |
| `answer_unit` | 단위 또는 `null` |
| `answer_format` | 답의 형태 안내 (choice5: `"5지선다 — 번호로 답해요"` 권장) |
| `figure` | 인라인 SVG 또는 `null` — **중3 풀은 practice.json 선례대로 도형·삼각비·원 문항도 전부 말로 서술하고 figure는 null로 둔다** (아래 §3 참조) |
| `hint` | 해요체 한 줄 |
| `solution` | 완전한 풀이 (해요체 존댓말 허용, 문어체 '~다.' 종결 금지) |
| `work_space` | `"sm"`/`"md"`/`"lg"` (essay 는 `"lg"`) |
| `misconceptions` | 관련 오개념 태그 배열 (없으면 `[]`, 단원 주제 dotted 태그 — 예 `sqrt.*`, `sector.*`는 쓰지 않고 `trig.*`/`circle.*`/`quad.*`/`factor.*`/`stat.*`/`scatter.*` 등 새 네임스페이스로) |

format별 추가 필드:

- `choice5`: `"choices"`: 문자열 5개 배열 (①~⑤ 기호는 넣지 않는다 — 렌더러가 붙임), `"answer_choice"`: 1~5 정수, `"distractor_why"`: 오답 4개가 각각 어떤 실수에서 나오는지 배열 4개 (보기 순서대로, 정답 위치는 건너뜀).
- `essay`: `"rubric"`: `[{"step": "…", "points": n}, …]` 2~4단계, **합계 정확히 8**.

## 3. 표기 규약 (practice.json 과 동일 + 중3 답 형식 규약 반영)

- KaTeX/`$` 금지. 거듭제곱은 `<sup>` (예 `2<sup>3</sup>`), 분수는 `<span class="frac"><b>분자</b><i>분모</i></span>`, 각도 `∠`·`°`, 평행 `∥`, 수직 `⊥`, 합동 `≡`, 근호는 유니코드 `√`(근호 안이 두 항 이상이면 괄호), π 는 문자 `π`.
- 음수 부호는 유니코드 마이너스 `−`(U+2212) 로 통일 (stem·choices·answer 모두).
- **도형·삼각비·원 문항도 그림 없이 전부 말로 서술한다** — math3 practice.json 전 단원(u07~u10 포함)이 이미 이 방식(figure:null)이다. "∠C=90°인 직각삼각형 ABC에서 AC=4, BC=3, AB=5일 때…" 처럼 변·각을 문장에 전부 명시하면 그림 없이도 유일하게 정해진다. 꼭 필요할 때만(예: 색칠한 부분) 자체 완결 인라인 SVG(viewBox 지정, 폭 ≤ 260, 외부 참조 금지).
- **산포도·상자그림·산점도(u11·u12)**: 자료를 다섯 수·순서쌍 나열 등 글로 제시 (UNITS.md §5 선례 그대로, 그림 없음).
- choice5 보기에서 근호·분수 답은 표기 그대로 문자열로 쓴다 (앱의 "한 성분만 입력" 제약은 지면 시험엔 적용하지 않는다 — `answer_choice`가 정답 번호이므로 답 전체를 자연스럽게 쓴다). 예: `"3√2"`, `"x=2 또는 x=3"`, `"(1, −3)"`.
- 이차방정식 두 근을 묻는 short/essay는 "두 근을 모두 쓰시오" 또는 "작은 근을 구하시오" 로 좁혀 답을 하나로 확정한다. 좌표를 묻는 문항은 "(x, y) 순서쌍으로" 또는 "x좌표만" 으로 답 형태를 명시한다.
- 발문에 앱 의존 표현 금지: `□`, 버튼, 슬라이더, 클릭, "위 그림에서 값을" 등.
- 발문은 요구문으로 끝남: `…를 구하시오.` / `…을 쓰시오.` / `…은?` / `…까요?` 형태.
- hint 는 해요체 한 줄. solution 도 학생에게 말 걸듯 해요체 (— "~다." 문어체 종결 금지).

## 4. format 별 저작 규칙

### cn (choice_new — 신규 선택형)
- **기존 practice.json 28문항과 겹치지 않는 새 문제** (숫자만 바꾼 복제 금지, 새 상황/새 조합).
- 실제 학교 시험 스타일. 보기 5개, 정답 정확히 1개.
- **오답 보기 4개는 각각 "그럴듯한 실수의 결과"**: 부호 실수, 공식 혼동(예: sin·cos 자리바꿈, 넓이·둘레 공식 혼동, 분산 계산에서 제곱 빠뜨림), 단위 착각, 한 단계 빠뜨림 등. `distractor_why`에 근거를 남긴다.
- 수치 보기는 작은 값 → 큰 값 순서로 배열(문자열 답은 논리적 순서). 정답 위치(`answer_choice`)는 문항마다 다르게 (한 단원 안에서 같은 번호 3회 이상 금지).
- 보기끼리 중복 금지, "정답 없음/모두 고르시오" 금지.

### cv (choice_conv — 기존 문항의 선택형 변환)
- 담당 단원 practice.json 에서 **할당 level 과 같은 level** 의 문항을 골라 (`source_id` 기록) 5지선다로 변환.
- 발문 어미는 선택형답게 다듬어도 됨. 수학 내용·정답 값은 원본과 동일해야 한다.
- 오답 보기 설계 규칙은 cn 과 동일.
- cn 이 다루지 않는 유형(7유형 중)을 우선 선택해 단원 내 유형 커버리지를 넓힌다.

### sh (short — 기존 단답 그대로 복사)
- practice.json 에서 할당 level 문항을 골라 필드 그대로 복사 (`source_id` 기록, `format:"short"` 와 `topic` 만 추가). cv 가 이미 쓴 문항은 제외.

### es (essay — 신규 서술형)
- **풀이 과정을 쓰게 하는 신규 문제.** 2~3단계 사고가 자연스럽게 드러나는 문제 (식 세우기 → 변형 → 답, 또는 조건 해석 → 계산 → 결론).
- `rubric` 은 채점자가 부분 점수를 줄 수 있게 단계를 나눈다 (합계 8점). 예: 식 세우기 3 / 과정 3 / 답 2.
- `solution` 은 rubric 단계가 그대로 보이는 완전한 풀이.
- 발문에 "풀이 과정을 함께 쓰시오." 를 포함.
- level 정의: L = 교과서 기본(1~2단계), M = 표준 시험(2~3단계), H = 고난도(조건 조합, 중3 과정 내에서만).

### 공통 품질 규칙
- 모든 문항을 **스스로 두 번 독립적으로 풀어** 정답을 재확인할 것 (특히 cn/es).
- choice5 는 5개 보기를 하나씩 검산해 "정답 정확히 1개"를 확인할 것.
- 단원 7유형 중 **5유형 이상**이 풀 전체(cn+cv+sh+es)에서 다뤄지게 할 것.
- **중3 교육과정 밖 개념 금지**: 미분, 적분, 로그, 지수함수, 수열, 벡터, 행렬, 허수, 복소수, 이차부등식, 판별식(용어로 부르는 것 금지 — "근의 개수"는 근의 공식 계산 과정에서 자연스럽게 다뤄도 됨). 반대로 제곱근·인수분해·이차방정식·삼각비·원주각·분산/표준편차·사분위수는 **중3 본 단원 내용이므로 정상 사용**.

## 5. 단원별 할당표 (id 순서 = 이 표 순서, level 고정)

> 12단원 합계 = **132문항** = choice5(cn+cv) 90 + short(sh) 18 + essay(es) 24 — 6회차(22문항: 선택15·단답3·서술4) 전체 수요와 정확히 일치.
> 난이도 합계 = L49·M52·H31 — 표준 3회(L9M10H3)+쉬움 1회(L22)+도전 2회(M11H11) 수요와 정확히 일치.

| 단원 | cn (신규 선택형) | cv (변환) | sh (단답) | es (서술형) | 계 |
|---|---|---|---|---|---|
| u01 제곱근과 실수 | cn1 L, cn2 M, cn3 H | cv1 L, cv2 M | sh1 L | es1 L, es2 M | 8 |
| u02 근호를 포함한 식의 계산 | cn1 L, cn2 M, cn3 H | cv1 L, cv2 M | sh1 L | es1 M, es2 H | 8 |
| u03 다항식의 곱셈과 인수분해 | cn1 L, cn2 M, cn3 M, cn4 H | cv1 L, cv2 M | sh1 L | es1 L, es2 M | 9 |
| u04 이차방정식 | cn1 L, cn2 M, cn3 M, cn4 H | cv1 L, cv2 M | sh1 L | es1 M, es2 H | 9 |
| u05 이차함수와 그래프 | cn1 L, cn2 M, cn3 H | cv1 L, cv2 M | sh1 L | es1 L, es2 M | 8 |
| u06 이차함수의 활용 | cn1 L, cn2 M, cn3 H | cv1 L, cv2 M | sh1 L | es1 M, es2 H | 8 |
| u07 삼각비 | cn1 L, cn2 M, cn3 M, cn4 M, cn5 H | cv1 L, cv2 L, cv3 M, cv4 H, cv5 H | sh1 L, sh2 M | es1 L, es2 M | 14 |
| u08 삼각비의 활용 | cn1 L, cn2 M, cn3 M, cn4 H | cv1 L, cv2 L, cv3 M, cv4 H, cv5 H | sh1 L, sh2 M | es1 M, es2 H | 13 |
| u09 원과 직선 | cn1 L, cn2 L, cn3 M, cn4 M, cn5 H | cv1 L, cv2 L, cv3 M, cv4 H, cv5 H | sh1 L, sh2 M | es1 L, es2 M | 14 |
| u10 원주각 | cn1 L, cn2 M, cn3 M, cn4 H, cn5 H | cv1 L, cv2 L, cv3 M, cv4 H, cv5 H | sh1 L, sh2 M | es1 M, es2 H | 14 |
| u11 산포도 | cn1 L, cn2 M, cn3 M, cn4 M, cn5 H | cv1 L, cv2 L, cv3 M, cv4 H, cv5 H | sh1 L, sh2 M | es1 L, es2 M | 14 |
| u12 상자 그림과 산점도 | cn1 L, cn2 M, cn3 M, cn4 H | cv1 L, cv2 L, cv3 M, cv4 H, cv5 H | sh1 L, sh2 M | es1 M, es2 H | 13 |

id 접두사 `e{NN}-`(예 u07 → `e07-cn1`). 합계 132문항 (cn48 + cv42 + sh18 + es24). 난이도 합계 L49 + M52 + H31.

## 6. 예시

choice5 (cn) 예시 골격 — 삼각비:

```json
{
  "id": "e07-cn1", "format": "choice5", "level": "L", "topic": "삼각비의 뜻",
  "source_id": null,
  "stem_print": "∠C = 90°인 직각삼각형 ABC에서 AB = 13, BC = 5, AC = 12일 때, sin B의 값은?",
  "choices": ["5/13", "12/13", "5/12", "12/5", "13/12"],
  "answer_choice": 2,
  "distractor_why": ["sin 대신 cos B를 구함(밑변／빗변)", "sin을 tan처럼 대변／밑변으로 계산", "분자·분모를 뒤집음", "AB를 밑변으로 잘못 보고 AB／AC로 계산"],
  "answer_print": "12/13", "answer_accept": ["12∕13"], "answer_unit": null,
  "answer_format": "5지선다 — 번호로 답해요",
  "figure": null,
  "hint": "sin B는 ∠B를 기준으로 대변／빗변이에요. 빗변은 직각의 대변인 AB예요.",
  "solution": "직각이 C이므로 빗변은 AB = 13이에요. ∠B의 대변은 AC = 12예요. sin B = 대변／빗변 = AC／AB = 12／13이에요.",
  "work_space": "sm", "misconceptions": ["trig.ratio-confusion"]
}
```

essay (es) 예시 골격 — 이차방정식 활용:

```json
{
  "id": "e04-es1", "format": "essay", "level": "M", "topic": "이차방정식의 활용",
  "source_id": null,
  "stem_print": "어떤 자연수를 제곱한 수는 그 수의 3배보다 10만큼 크다고 한다. 이 자연수를 구하시오. 풀이 과정을 함께 쓰시오.",
  "rubric": [
    {"step": "조건을 방정식 x² = 3x + 10 으로 바르게 세웠어요", "points": 3},
    {"step": "x² − 3x − 10 = 0 을 인수분해해 (x−5)(x+2)=0 까지 정리했어요", "points": 3},
    {"step": "자연수 조건으로 x=5를 골라 검산했어요", "points": 2}
  ],
  "answer_print": "5", "answer_accept": ["x=5"], "answer_unit": null,
  "answer_format": "풀이 과정 + 답",
  "figure": null,
  "hint": "'그 수의 3배보다 10만큼 크다'를 등식으로 옮겨 봐요.",
  "solution": "x² = 3x + 10 으로 세워요. x² − 3x − 10 = 0, (x−5)(x+2) = 0 이므로 x = 5 또는 x = −2예요. 자연수 조건에서 x = 5예요. 검산하면 5² = 25, 3×5+10 = 25로 맞아요.",
  "work_space": "lg", "misconceptions": []
}
```

## 7. 검증

작성 후 프로젝트 루트에서:

```
python 70_tools/print/verify_exam3.py u{NN}
```

오류 0이 될 때까지 수정한다. (경고는 읽고 판단 — 사람 확인용.)
