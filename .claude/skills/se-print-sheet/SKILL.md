---
name: se-print-sheet
description: 기존 학습앱 문제를 프린트 학습지(문제지·정답지·해설지·오개념카드·오답진단표 PDF)로 만든다. 추출→지면 발문 재작성→오개념 태깅→검증→PDF 까지 한 단원을 끝낸다. 호출 예시 — "/se-print-sheet math2 u03", "/se-print-sheet 중2 단원5 학습지 만들어", "/se-print-sheet math2 u03 --mock-only".
---

# se-print-sheet — 프린트 학습지 제작 스킬

기존 웹앱 문제 자산 → **종이로 푸는 학습지 PDF**.
규격 SSOT = `10_system/10_principles/PRINT_PRINCIPLES.md` · 계획 = `00_project_hub/20_plan/0728_print_worksheet_plan.md`

> **이 스킬의 핵심 명제:** 이 작업은 파일 변환이 아니라 **지면 발문 재작성**이다.
> 앱 문항은 폰 입력에 맞춰 "숫자 빈칸 채우기"로 분해되어 있고(`3a² × 2a` 의 계수칸·지수칸을 따로 물음),
> 종이에서는 답을 **통째로** 쓰게 해야 한다.
> 다행히 **정답 원자는 스크립트로 결정적으로 추출**되므로, 재작성이 원본과 어긋나면 기계가 잡는다.

## 인자 형태

```
/se-print-sheet math2 u03                 # 중2 단원3 전체 (유형 세트 + 모의 회차)
/se-print-sheet math2 u03 --sets-only     # 유형 세트(ㄱ)만
/se-print-sheet math2 u03 --mock-only     # 모의 회차(ㄴ)만
/se-print-sheet math2 u03 --rebuild       # 은행은 그대로, HTML/PDF 만 재생성
```

## ⚠️ 병렬 실행 규약 (여러 단원을 동시에 돌릴 때)

**단원 하나 = 에이전트 하나.** 단원 간 공유 상태가 없도록 설계되어 있다.

| 자원 | 단원별 분리 여부 |
|---|---|
| `problem_bank/<grade>/u<NN>/practice.json` | ✅ 단원 전용 |
| `problem_bank/misconceptions/<grade>_u<NN>.json` | ✅ 단원 전용 |
| `problem_bank/sets/<setid>.json` | ✅ setid 에 단원 포함 |
| `60_deploy/print/<grade>/u<NN>/` · `40_grades/middle/<grade>/print/u<NN>/` | ✅ 단원 전용 |
| `70_tools/print/*.py`, `*.ps1` | ⚠️ **공유 — 병렬 실행 중에는 고치지 않는다** |

- 도구를 고쳐야 하면 **병렬 배치를 멈추고** 고친 뒤 다시 시작한다.
- headless Chrome 은 호출마다 **임시 프로필**을 쓰므로 동시 실행해도 충돌하지 않는다.
- 단, 동시 Chrome 프로세스가 많으면 메모리를 먹는다. **동시 4단원 이하**를 권한다.
- 오개념 id 는 단원을 넘어 재등장한다. 병렬 저작 후 **`se-print-sheet --merge-misconceptions`** 로
  중복 id 의 문구가 갈리지 않았는지 마지막에 한 번 확인한다(수동 diff 로도 충분).

## 절차

### STEP 1 — 원본 확인 · 추출

**중2 (세대 D — `app2/p<N>.html`)**
```powershell
$env:PYTHONIOENCODING='utf-8'
python 70_tools/print/extract_math2_p.py 40_grades/middle/math2/app2/p<N>.html <N> <scratch>/m2_u<N>.json
```
→ `unmatched=0` 확인. `choice2=<n>` 은 **2지선다 문항 수**로, 그만큼 단답형 재작성이 필요하다는 뜻.

**중1 2학기 (세대 A/C — `math1/<NN>_*/problems/type_*_app.html`)**
```powershell
python 70_tools/print/extract_gen_ac.py 40_grades/middle/math1/<NN>_단원명/problems <NN> <scratch>/m1_u<NN>.json
```
→ `no_answer=0` 확인. `figures=<n>` 은 인라인 SVG 도형 수 (그대로 `figure` 필드에 넣어 인쇄된다).

**세대 판별표**

| 세대 | 마크업 | 정답 위치 | 해당 |
|---|---|---|---|
| D | `.mission > .pq` + `<input>` / `.picks` | JS `prob()/P()`, `num()`, `pick()`, `MJ.check()` | 중2 `p1~p11` |
| A | `.card.lv-{L\|M\|H}` + `.q-text` | `.sol-panel` 첫 `<strong>` | 중1 07~12 |
| C | `.q-card` + `.q-body` | `.panel[id$=a] .ans` | 중1 13 |

- `unmatched`/`no_answer` 가 0 이 아니면 **중단하고 원인부터 본다.** 바인딩 표기가 또 다른 것이다.
- 중1 범위는 **`type_01~07_app.html` (단원당 63문항)** 로 잡는다. `basic_app`·`deep_*`·`walk_*` 는 마크업이 또 달라 이번 범위 밖.
- 중2 심화문제(`d<N>p.html`, 세대 D')도 이번 범위 밖.

### STEP 2 — 지면 은행 저작 (핵심 작업)

`30_content/problem_bank/<grade>/u<NN>/practice.json` 을 쓴다. 문항마다:

| 필드 | 규칙 |
|---|---|
| `stem_src` | 원본 발문 (추적용, 인쇄 안 함) |
| `stem_print` | **§발문 규약 R1~R7 적용해 재작성** |
| `answer_atoms` | **추출값 그대로. 절대 손대지 않는다** |
| `answer_print` | 원자에서 합성한 지면 정답 |
| `answer_accept` | 동치 표현 (`a^7`, `8×a^3` 등) — 자기채점의 생명줄 |
| `answer_unit` | 단위 문자열 또는 `null` |
| `answer_format` | 답의 형태 지정 (`a의 거듭제곱 꼴로`, `기약분수로`, `수로 (단위 없음)`) |
| `hint` / `solution` | 원본 `.tip`/`.why`/`#sN` 재사용 · 해요체 |
| `work_space` | `sm`(L) / `md`(M) / `lg`(H) |
| `misconceptions` | 오개념 id 배열 |
| `level` | L / M / H |

유형마다 `principle` (해요체 한 줄 원리) 을 쓴다. `figure` 에는 추출된 `figure_svg` 를 그대로 넣는다.

**변환 규칙 2가지 — 이게 재작성의 실체다.**

**① 2지선다(`response: "choice2"`) → 단답형.** 종이에서 2지선다는 찍으면 50% 라 값어치가 없다.
원본의 정답 선택지 텍스트가 `answer_atoms` 로 들어와 있으니, 그것을 답으로 삼고 발문을 바꾼다.
- 원본 `"x는 3보다 크다"를 식으로?` + 선택지 `x > 3` / `x ≥ 3`
- 지면 `"x는 3보다 크다"를 부등식으로 나타내시오.` · `answer_print: "x &gt; 3"` · `answer_format: "부등호를 쓴 식으로"`

**② KaTeX(`$...$`) → HTML.** 중1 자료는 KaTeX 문법을 쓰는데 지면은 **CDN 없이** 렌더한다.
`verify_bank.py` V4 가 `$`·`\dfrac`·`\angle` 등 잔재를 **오류로 잡는다.**

| 원본 | 지면 |
|---|---|
| `$35°$` | `35°` |
| `$a^3$` · `$x_1$` | `a<sup>3</sup>` · `x<sub>1</sub>` |
| `$\dfrac{n(n-3)}{2}$` | `<span class="frac"><b>n(n−3)</b><i>2</i></span>` |
| `$\angle A$` · `$\overline{AB}$` · `$\overrightarrow{AB}$` | `∠A` · `AB̄`(또는 `선분 AB`) · `반직선 AB` |
| `$\times$` `$\div$` `$\pi$` `$\times$` | `×` `÷` `π` |
| `$180° - 35°$` | `180° − 35°` (빼기는 U+2212) |

표기가 애매하면 **기호 대신 우리말**을 쓴다 (`\overleftrightarrow{AB}` → `직선 AB`). 종이는 툴팁이 없다.

### STEP 3 — 오개념 카탈로그

`30_content/problem_bank/misconceptions/<grade>_u<NN>.json`.
**단원당 10~15개**를 목표로 한다. 문항 수보다 훨씬 적어야 정상이다.

각 항목 6요소 — `no`(지면 번호) · `label` · `empathy` · `counter`(반례) · `ask`(되돌리는 질문) · `check`{q,a} · `link`.

- **카드에 그 문제의 정답을 넣지 않는다.**
- ★ **정답이 두 글자 낱말(`외심`·`내심`·`평행`)이면 V5 가 카드 본문에서 그 낱말을 정답 누출로 잡는다.**
  카드를 억지로 비틀지 말고, **지면 정답에 뜻을 덧붙여** 써라 — `외심 (외접원의 중심)`.
  학생에게도 친절하고 V5 도 통과한다.
- `counter`·`ask` 를 설명으로 채우면 해설지와 같아진다. **짧은 반례 + 질문 하나.**
- 이미 있는 오개념(다른 단원)과 같은 개념이면 **같은 id 를 쓴다.**

### STEP 4 — 회차 config

`30_content/problem_bank/sets/<setid>.json`. setid = `m<학년>-u<NN>-<a|b|c|mock>`.

**회차 쪼개기 기준 — 한 회차 9~12문항.**
- 중2(유형당 3문항): 유형 3개씩 묶어 9문항 → 유형 6개면 `a,b` / 9개면 `a,b,c`
- 중1(유형당 9문항 = L3/M3/H3): **유형 1개 = 1회차 9문항** → `a`~`g` (7회차)
- `mock` 은 단원당 1개. 중1은 유형마다 L·M·H 1개씩 뽑아 12~15문항이 되게 `per_type` 을 잡는다

- **ㄱ 유형 세트**(`"kind": "type-set"`) — 이웃 유형 2~3개를 묶어 9~12문항. 평소 연습용
- **ㄴ 모의 회차**(`"kind": "mock"`) — 난이도 오름차순. 시험 대비용. 뽑는 방법 두 가지:
  - `"pick": {"quota": {"L":1, "M":1}}` — **유형마다 L 1개 + M 1개.** 난이도를 섞으려면 이걸 쓴다
  - `"pick": {"per_type": 2, "levels": ["L","M","H"]}` — 유형마다 앞에서 2개. `levels` 는 정렬 순서일 뿐이라
    **`per_type` 만으로는 "L 하나 M 하나"를 표현할 수 없다**(L 만 2개가 뽑힌다). 섞으려면 `quota` 를 써라
- **`"outputs": ["Q","K"]`** (기본) — **회차당 2파일**. `K` **해답 묶음** = 정답 → 진단표 → 오개념 카드 → 해설.
  따로 뽑으면 반쪽짜리 종이가 여러 장 남는다. 분리본이 꼭 필요하면 `"A"`, `"S"`, `"D"`, `"M"` 을 직접 넣는다.
- **`"columns": 2`** (기본) — 문제지를 문제집처럼 세로 2단. 도형이 큰 단원(중1 기하 등)만 `1` 로 내린다.
  K 안에서는 **표(정답·진단표)는 1단, 오개념 카드·해설은 2단**으로 자동 처리된다.

### STEP 5 — 검증 (건너뛰지 않는다)

```bash
python 70_tools/print/verify_bank.py <grade>/u<NN>/practice.json misconceptions/<grade>_u<NN>.json
```

**오류 0 이 될 때까지 다음 단계로 가지 않는다.** V1~V6 의미는 PRINT_PRINCIPLES §9.
`answer_atoms` 가 원본과 다르다고 나오면 **원본이 옳다.**

### STEP 6 — HTML · PDF 생성

```powershell
$env:PYTHONIOENCODING='utf-8'
python 70_tools/print/build_sheet.py 30_content/problem_bank/sets/<setid>.json 60_deploy/print/<grade>/u<NN>
powershell -NoProfile -ExecutionPolicy Bypass -File 70_tools/print/print_pdf.ps1 -Plan 60_deploy/print/<grade>/u<NN>/<setid>_pdfplan.json
```

PDF → `40_grades/middle/<grade>/print/u<NN>/`.

### STEP 7 — 눈으로 확인

**최소 2장은 실제로 본다** (Read 로 PDF 를 열어 렌더 확인).
- 문제지: **2단이 제대로 잡혔는가** / 유형 머리말이 페이지 끝에 홀로 남지 않았는가 / 풀이 공간이 적당한가 / 답란 단위가 맞는가
- 해답묶음(K): **표는 1단·카드와 해설은 2단**으로 나왔는가 / 안내문이 절마다 중복되지 않았는가 / 표 머리행이 페이지 넘어가도 반복되는가 / 오개념 카드에 정답이 새지 않았는가

### STEP 8 — 기록

chatlog 에 단원별 결과 한 줄: 문항 수 · 오개념 수 · 생성 PDF 수 · 검증 결과.

## 자주 걸리는 함정

1. **PowerShell 5.1 은 `.ps1` 을 cp949 로 읽는다.** 한글 리터럴을 넣으면 파서가 깨진다 → `print_pdf.ps1` 은 ASCII 전용, 한글 파일명은 `_pdfplan.json` 경유.
2. **headless Chrome 이 안 끝난다** (새 프로필 → GCM/sync 통신). PDF 는 이미 나와 있는데 프로세스가 남는다 → 네트워킹 비활성 플래그 + 90초 타임아웃 강제 종료. 이미 `print_pdf.ps1` 에 반영됨.
3. **`PYTHONIOENCODING=utf-8` 선제 설정** 안 하면 한글 stdout 에서 죽는다.
4. **중첩 PowerShell 은 `-NoProfile`** 을 붙인다.
5. **2지선다를 그대로 옮기지 않는다.** 종이에서 2지선다는 찍으면 50% 다 → 단답형으로 재작성.
6. **유형당 문항이 3개뿐인 단원(중2)** 은 평소 연습용으로 얇다. 증보가 필요하면 `/se-math-practice` 를 쓴다 (파일럿 게이트 통과 후에 판단).

## 산출물 체크리스트

- [ ] `unmatched=0` 으로 추출됐다
- [ ] 모든 `stem_print` 에 `□`·앱 의존 표현이 없다
- [ ] 모든 문항에 `answer_format` 이 있다 (단위 필요하면 `answer_unit` 도)
- [ ] 오개념 카드에 정답이 새지 않았다
- [ ] `verify_bank.py` 오류 0
- [ ] PDF 를 최소 2장 눈으로 봤다
- [ ] chatlog 기록
