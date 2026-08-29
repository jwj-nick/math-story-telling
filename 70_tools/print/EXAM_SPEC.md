<!-- EXAM_SPEC.md — 중1 실전 모의고사 문항 풀(exam.json) 저작 스펙 (2026-08-26) -->
# 중1 실전 모의고사 — exam.json 저작 스펙

> 목적: 학교 기말고사(중1 전 범위) 리허설용 모의고사 6회차의 재료가 되는 **단원별 시험 문항 풀**.
> 실제 학교 시험 형식(선택형 5지선다 + 단답형 + 서술형, 100점, 45분)을 따른다.
> 이 풀에서 `plan_exam.py`가 6회차를 조립하므로 **할당표의 id·format·level은 한 글자도 바꾸면 안 된다.**

## 1. 파일 위치와 최상위 구조

`30_content/problem_bank/math1/u{NN}/exam.json` (단원당 1파일, 신규. 기존 practice.json은 **읽기 전용**):

```json
{
  "meta": {
    "grade": "math1", "unit": 7, "unit_name": "기본도형",
    "purpose": "exam-pool", "authored": "2026-08-26",
    "note": "중1 전범위 실전 모의고사용 문항 풀. EXAM_SPEC.md 준수."
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
| `topic` | 무엇을 재는지 짧은 라벨 (예 "맞꼭지각") |
| `source_id` | cv/sh 만: 원본 practice.json 문항 id. cn/es 는 `null` |
| `stem_print` | 발문. 시험체(…를 구하시오 / …의 값은?) |
| `answer_print` | 정답 (choice5 는 정답 보기의 문자열과 완전 동일) |
| `answer_accept` | 이렇게 써도 맞는 표현 배열 또는 `null` (choice5 는 `null`) |
| `answer_unit` | 단위 또는 `null` |
| `answer_format` | 답의 형태 안내 (choice5: `"5지선다 — 번호로 답해요"` 권장) |
| `figure` | 인라인 SVG 또는 `null` |
| `hint` | 해요체 한 줄 |
| `solution` | 완전한 풀이 (해요체 존댓말 허용, 문어체 '~다.' 종결 금지) |
| `work_space` | `"sm"`/`"md"`/`"lg"` (essay 는 `"lg"`) |
| `misconceptions` | 관련 오개념 태그 배열 (없으면 `[]`) |

format별 추가 필드:

- `choice5`: `"choices"`: 문자열 5개 배열 (①~⑤ 기호는 넣지 않는다 — 렌더러가 붙임), `"answer_choice"`: 1~5 정수, `"distractor_why"`: 오답 4개가 각각 어떤 실수에서 나오는지 배열 4개 (보기 순서대로, 정답 위치는 건너뜀).
- `essay`: `"rubric"`: `[{"step": "…", "points": n}, …]` 2~4단계, **합계 정확히 8**.

## 3. 표기 규약 (practice.json 과 동일)

- KaTeX/`$` 금지. 거듭제곱은 `<sup>` (예 `2<sup>3</sup>`), 분수는 `<span class="frac"><b>분자</b><i>분모</i></span>`, 각도 `∠`·`°`, 평행 `∥`, 수직 `⊥`, 합동 `≡`, π 는 문자 `π`.
- 음수 부호는 유니코드 마이너스 `−`(U+2212) 로 통일 (stem·choices·answer 모두).
- 발문에 앱 의존 표현 금지: `□`, 버튼, 슬라이더, 클릭, "위 그림에서 값을" 등.
- 발문은 요구문으로 끝남: `…를 구하시오.` / `…을 쓰시오.` / `…은?` / `…까요?` 형태.
- hint 는 해요체 한 줄. solution 도 학생에게 말 걸듯 해요체 (— "~다." 문어체 종결 금지).
- figure 는 자체 완결 인라인 SVG 만 (외부 참조 금지, viewBox 지정, 폭 ≤ 260). 기존 practice.json 의 figure 를 cv/sh 에서 그대로 복사하는 것 권장. 신규 도형은 꼭 필요할 때만 간단히.

## 4. format 별 저작 규칙

### cn (choice_new — 신규 선택형)
- **기존 practice.json 28문항과 겹치지 않는 새 문제** (숫자만 바꾼 복제 금지, 새 상황/새 조합).
- 실제 학교 시험 스타일. 보기 5개, 정답 정확히 1개.
- **오답 보기 4개는 각각 "그럴듯한 실수의 결과"**: misconceptions 카탈로그의 오개념에서 도출하는 것을 우선 (부호 실수, 공식 혼동, 단위 착각, 한 단계 빠뜨림 등). `distractor_why`에 근거를 남긴다.
- 수치 보기는 작은 값 → 큰 값 순서로 배열. 정답 위치(`answer_choice`)는 문항마다 다르게 (한 단원 안에서 같은 번호 3회 이상 금지).
- 보기끼리 중복 금지, "정답 없음/모두 고르시오" 금지.

### cv (choice_conv — 기존 문항의 선택형 변환)
- 담당 단원 practice.json 에서 **할당 level 과 같은 level** 의 문항을 골라 (`source_id` 기록) 5지선다로 변환.
- 발문 어미는 선택형답게 다듬어도 됨 (`…를 구하시오` → `…은?`). 수학 내용·정답 값은 원본과 동일해야 한다.
- 오답 보기 설계 규칙은 cn 과 동일.
- cn 이 다루지 않는 유형을 우선 선택해 단원 내 유형 커버리지를 넓힌다. 답이 보기로 만들기 어색한 문항(서술 답·2지선다 재작성류)은 피한다.

### sh (short — 기존 단답 그대로 복사)
- practice.json 에서 할당 level 문항을 골라 필드 그대로 복사 (`source_id` 기록, `format:"short"` 와 `topic` 만 추가). cv 가 이미 쓴 문항은 제외.

### es (essay — 신규 서술형)
- **풀이 과정을 쓰게 하는 신규 문제.** 2~3단계 사고가 자연스럽게 드러나는 문제 (식 세우기 → 변형 → 답, 또는 조건 해석 → 계산 → 결론).
- `rubric` 은 채점자가 부분 점수를 줄 수 있게 단계를 나눈다 (합계 8점). 예: 식 세우기 3 / 과정 3 / 답 2.
- `solution` 은 rubric 단계가 그대로 보이는 완전한 풀이.
- 발문에 "풀이 과정을 함께 쓰시오." 를 포함.
- level 정의: L = 교과서 기본(1~2단계), M = 표준 시험(2~3단계), H = 고난도(조건 조합, 중1 과정 내에서만).

### 공통 품질 규칙
- 모든 문항을 **스스로 두 번 독립적으로 풀어** 정답을 재확인할 것 (특히 cn/es).
- choice5 는 5개 보기를 하나씩 검산해 "정답 정확히 1개"를 확인할 것.
- 단원 7유형 중 **5유형 이상**이 풀 전체(cn+cv+sh+es)에서 다뤄지게 할 것.
- 중1 교육과정 밖 개념(제곱근, 피타고라스, 인수분해 등) 금지.

## 5. 단원별 할당표 (id 순서 = 이 표 순서, level 고정)

| 단원 | cn (신규 선택형) | cv (변환) | sh (단답) | es (서술형) |
|---|---|---|---|---|
| u01 소인수분해 | cn1 L, cn2 M, cn3 H | cv1 L, cv2 M | sh1 L | es1 L, es2 M |
| u02 정수와유리수 | cn1 L, cn2 M, cn3 H | cv1 L, cv2 M | sh1 L | es1 M, es2 H |
| u03 문자와식 | cn1 L, cn2 M, cn3 H, cn4 H | cv1 L, cv2 M | — | es1 L, es2 M |
| u04 일차방정식 | cn1 L, cn2 M, cn3 M, cn4 H | cv1 L, cv2 M | — | es1 M, es2 H |
| u05 좌표와그래프 | cn1 L, cn2 M, cn3 H | cv1 L, cv2 M | sh1 L | es1 L, es2 M |
| u06 정비례와반비례 | cn1 L, cn2 M, cn3 H | cv1 L, cv2 M | sh1 L | es1 M, es2 H |
| u07 기본도형 | cn1 L, cn2 M, cn3 M, cn4 H | cv1 L, cv2 L, cv3 M, cv4 H | sh1 L, sh2 M | es1 L, es2 M |
| u08 작도와합동 | cn1 L, cn2 M, cn3 M, cn4 H | cv1 L, cv2 L, cv3 M, cv4 H | sh1 L, sh2 M | es1 M, es2 H |
| u09 다각형 | cn1 L, cn2 M, cn3 M, cn4 H | cv1 L, cv2 L, cv3 M, cv4 H, cv5 H | sh1 L, sh2 M | es1 H |
| u10 원과부채꼴 | cn1 L, cn2 M, cn3 M, cn4 H | cv1 L, cv2 L, cv3 M, cv4 H | sh1 L, sh2 M | es1 M, es2 H |
| u11 다면체와회전체 | cn1 L, cn2 M, cn3 M, cn4 H | cv1 L, cv2 L, cv3 M, cv4 H, cv5 H | sh1 L, sh2 M | es1 H |
| u12 입체도형의겉넓이와부피 | cn1 L, cn2 M, cn3 M, cn4 H | cv1 L, cv2 L, cv3 M, cv4 H | sh1 L, sh2 M | es1 M, es2 H |
| u13 자료의정리와해석 | cn1 L, cn2 M, cn3 M, cn4 H | cv1 L, cv2 L, cv3 M, cv4 H | sh1 L, sh2 M | es1 L, es2 M |

id 접두사: `e{NN}-` (예 u07 → `e07-cn1`). 합계 = 132문항 (cn48 + cv42 + sh18 + es24).

## 6. 예시

choice5 (cn) 예시 골격:

```json
{
  "id": "e07-cn1", "format": "choice5", "level": "L", "topic": "맞꼭지각",
  "source_id": null,
  "stem_print": "오른쪽 그림에서 두 직선이 한 점에서 만날 때, ∠x의 크기는?",
  "choices": ["35°", "45°", "55°", "125°", "145°"],
  "answer_choice": 3,
  "distractor_why": ["보각을 그대로 씀", "45로 어림", "180−55 를 답으로 착각", "둔각 쪽을 읽음"],
  "answer_print": "55°", "answer_accept": null, "answer_unit": null,
  "answer_format": "5지선다 — 번호로 답해요",
  "figure": "<svg viewBox=\"0 0 200 120\" width=\"200\">…</svg>",
  "hint": "마주 보는 각은 크기가 같아요.",
  "solution": "맞꼭지각은 서로 같아요. ∠x = 55°예요.",
  "work_space": "sm", "misconceptions": ["ang.vertical-supplement"]
}
```

essay (es) 예시 골격:

```json
{
  "id": "e04-es1", "format": "essay", "level": "M", "topic": "일차방정식 활용",
  "source_id": null,
  "stem_print": "어떤 수 x에 3을 더한 수의 2배는 x의 4배보다 2만큼 작다고 한다. 방정식을 세우고 x를 구하시오. 풀이 과정을 함께 쓰시오.",
  "rubric": [
    {"step": "조건을 방정식 2(x+3)=4x−2 로 바르게 세웠어요", "points": 3},
    {"step": "괄호를 풀고 이항해 2x=8 까지 정리했어요", "points": 3},
    {"step": "x=4 를 구하고 검산했어요", "points": 2}
  ],
  "answer_print": "x=4", "answer_accept": ["4"], "answer_unit": null,
  "answer_format": "풀이 과정 + 답",
  "figure": null,
  "hint": "'~보다 2만큼 작다'는 −2를 붙인다는 뜻이에요.",
  "solution": "2(x+3)=4x−2 로 세워요. 2x+6=4x−2, 6+2=4x−2x, 8=2x, x=4예요. 검산하면 2×7=14, 4×4−2=14로 맞아요.",
  "work_space": "lg", "misconceptions": []
}
```

## 7. 검증

작성 후 프로젝트 루트에서:

```
python 70_tools/print/verify_exam.py u{NN}
```

오류 0이 될 때까지 수정한다. (경고는 읽고 판단 — 사람 확인용.)
