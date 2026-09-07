# 70_tools/qa — 앱 동작 검증 하네스 (headless Chrome + 같은 오리진 iframe)

브라우저 확장 스크린샷이 이 환경에서 자주 타임아웃 나서 정립한 방식(2026-08-29, 개념 재미 1순위 검증에 사용).

## 원리
`iframe_harness_template.html`을 **검증할 페이지와 같은 폴더(같은 오리진)**에 복사해 두고, 하네스가 iframe에 페이지를 띄워 실제로 입력·클릭한 뒤 DOM 사실을 `#log`(JSON 한 줄씩)에 남긴다. headless Chrome의 `--dump-dom`으로 그 로그를 수확한다. 스크린샷이 필요하면 같은 URL을 `--screenshot`으로.

## 사용
1. 스크래치 폴더에 앱을 복사(리포 안에 하네스를 두지 않는다): `srv/mid3/` 등 라이브와 같은 경로로.
2. 템플릿을 그 폴더에 `_h.html`로 복사하고 `scen==='flow'` 블록의 시나리오(입력 id·정답·기대값)를 대상 단원에 맞게 고친다. 로그 키에 기대값을 괄호로 적어 두면 읽기 쉽다(예 `bar_after_c1(=2)`).
3. **새 포트**로 서버: `python -m http.server 8543 --bind 127.0.0.1 --directory <srv>` (끝나면 `netstat -ano | grep :8543` → `taskkill //F //PID`).
4. 실행(Git Bash):
   ```
   C="/c/Program Files/Google/Chrome/Application/chrome.exe"
   "$C" --headless --disable-gpu --no-sandbox --disable-extensions --user-data-dir=<임시프로필> \
        --enable-logging=stderr --v=0 --virtual-time-budget=25000 --window-size=1000,1200 \
        --dump-dom "http://127.0.0.1:8543/mid3/_h.html#flow" > flow.html 2> flow.err
   python -c "import re,html,sys;t=open(sys.argv[1],encoding='utf-8').read();m=re.search(r'<div id=\"log\">(.*?)</div>',t,re.S);sys.stdout.buffer.write(html.unescape(m.group(1)).encode('utf-8'))" flow.html
   grep -c CONSOLE flow.err     # 콘솔 오류 0이어야 함
   ```
5. 스크린샷: `--virtual-time-budget=6000 --window-size=1000,1700 --screenshot=x.png "<url>#restored"` → Read로 확인. `?tall=1`이면 iframe 4300px(페이지 하단까지), `?short=1`이면 700px(스크롤 검증용).

## 주의
- 동시 실행 시 Chrome 인스턴스마다 `--user-data-dir`를 다르게.
- **가상 시간(`--virtual-time-budget`)에서는 smooth 스크롤이 움직이지 않는다** → 스크롤 검증은 `--force-prefers-reduced-motion`(즉시 스크롤)으로. 같은 플래그로 reduced-motion 분기(꽃가루 생략 등)도 검증.
- 하네스 시작 시 `localStorage.clear()`를 하므로 실제 사용 프로필에서 열지 말 것(임시 프로필만).
- 배포 리포·소스 리포에 `_h.html`을 커밋하지 않는다.

---

## smoke_playground.js — 놀이터 런타임 스모크 (2026-09-07 신설)

세 학년 놀이터 36페이지(게임 144개)를 **jsdom 으로 띄워 실제로 눌러 본다.** Chrome 하네스보다 가볍고, 한 번에 전 학년을 훑는다.

```
cd <스크래치 폴더> && npm install jsdom          # 리포에 node_modules 를 두지 않는다
NODE_PATH=<스크래치 폴더>/node_modules node 70_tools/qa/smoke_playground.js
```

검사 — 런타임 오류 0 / 게임 4개와 제목·id / 마지막이 오류 탐정인지 / 점수판 목표치 = 게임 수 /
**버튼을 눌렀을 때 게임 블록이 실제로 바뀌는지** / 슬라이더 반응 / 조작 뒤에도 오류가 없는지 / 반말 0.

**왜 필요한가**: `check_page.py` 는 정적이라 "문법은 맞지만 실행하면 터지는" 코드를 못 잡는다.
실제로 이 스모크가 `classList.add('')` 때문에 **학생이 정답을 맞힌 순간** 게임이 멈추던 버그를 math2 놀이터 두 곳에서 찾아냈다.
(`classList.add` 에 빈 문자열을 넘기면 DOMException 이 난다. 삼항 연산자의 "아무 표시도 안 함" 갈래를 `''` 로 두면 이렇게 된다.)

**주의** — 놀이터를 글자 수로 재지 말 것. 놀이터는 글이 300~570자뿐이고 스크립트가 8,000~10,000자다.
잣대는 분량이 아니라 **게임이 몇 개이고 실제로 도는가** 이다.

## check_page.py 의 짝 id 검사 — 이름 규칙이 아니라 배선으로 (2026-09-07 수정)

원래는 "입력 a1 → 버튼 a1b · 출력 a1o" 라는 **한 가지 이름 규칙**만 인정했다. 그런데 심화 문제(dNp) 페이지는
"입력 a1 → 버튼 b1 · 출력 o1" 을 쓴다. 배선은 멀쩡한데 **가짜 경고가 116건** 나서 진짜 결함이 묻혀 있었다.

지금은 출력 id 를 `check()` / `checkNum()` 호출의 **세 번째 인자에서 읽고**, 버튼은 그 호출 지점에서
**거슬러 올라가 가장 가까운 클릭 핸들러**의 대상이 실재하는 id 인지로 판정한다.
(길이로 자르는 방식은 `g11` 처럼 핸들러 본문이 긴 경우를 놓친다.)

**검사를 무르게 고치지 않았는지 확인하는 자체 검사**를 함께 둔다:

    python 70_tools/qa/selftest_check_page.py

멀쩡한 페이지는 통과하고, 출력 id·버튼 id·참조 id 를 하나씩 일부러 망가뜨리면 각각 잡아내는지 본다.
**검사기를 손댈 때마다 이걸 먼저 돌린다** — 가짜 경고를 없애다가 진짜를 놓치면 아무 소용이 없다.

---

## 도구 한눈에 (2026-09-08 정리)

    cd <스크래치 폴더> && npm install jsdom          # 리포에 node_modules 를 두지 않는다
    NODE_PATH=<스크래치>/node_modules node 70_tools/qa/<도구>.js

| 도구 | 무엇을 보는가 | 규모 |
|---|---|---|
| `check_page.py` | 정적 — 태그 균형·스크립트 구문·id 참조와 짝·중복 id·캐시 버전·**위험 패턴** | 전 페이지 |
| `check_screen_bank.py` | 화면 연습과 문제 은행의 **유형 구성**이 갈라졌는지 | 36단원 |
| `smoke_all.js` | 런타임 넓은 그물 — 전 페이지의 **모든 버튼을 세 바퀴** 누르고, 그 뒤 오류·죽은 링크·중복 id·안내 문구 어투 | 192페이지 · 클릭 9,800회 |
| `smoke_playground.js` | 놀이터 — 게임 4개·점수판·반응. **시드를 바꿔 8판**을 돌려 무작위 문제의 갈래를 두루 밟는다 | 36페이지 |
| `smoke_pn.js` | 연습 — TYPES·TOTAL·진행바 칸·도장 문구가 미션 수와 맞는지 + 새 미션 실제 조작 | 중2 11페이지 |
| `smoke_dnp.js` | 심화 문제 — 문항마다 입력·힌트 둘·풀이가 실제로 도는지 | 중2 11페이지 |
| `smoke_concept_d.js` | 중1 심화 — 유도 단계·도전 문제·다음 링크 | 13페이지 |
| `smoke_wordbox.js` | 낱말 상자·왜 상자가 실제로 렌더되는지 | 3페이지 |
| `selftest_check_page.py` | **check_page 가 무르지 않았는지** | — |
| `selftest_smoke_all.py` | **smoke_all 이 무르지 않았는지** | — |

### 정적과 런타임은 서로를 대신하지 못한다

- 정적은 **문법은 맞지만 실행하면 터지는** 코드를 못 잡는다.
- 런타임은 **조건이 맞아야 터지는** 코드를 놓칠 수 있다. 특정 답을 골랐을 때만,
  특정 문제가 나왔을 때만 터지는 종류가 그렇다.

2026-09-07 의 놀이터 버그(`classList.add('')` — 정답을 맞힌 순간 게임이 멈춤)가 정확히
후자였다. 버튼을 여러 바퀴 누르고 시드를 바꿔 봐도 재현이 들쭉날쭉했다.
**그래서 이 패턴은 `check_page.py` 의 `RISKY` 목록에 넣어 정적으로 막는다** — 조건과 상관없이 늘 걸린다.
위험 패턴을 새로 알게 되면 런타임으로 쫓기 전에 먼저 그 목록에 넣을 것.

### 검사기를 손댈 때

**자체 검사를 먼저 돌린다.** 가짜 경보를 없애다 진짜를 놓치기 쉽다. 실제로 이번에 겪은 것들:

- `check_page` 의 짝 id 검사가 한 가지 이름 규칙만 인정해 **가짜 116건**
- 놀이터 스모크가 `.out` 만 보아 **가짜 13건** (진짜 2건이 그 속에 묻혔다)
- 심화 문제 스모크가 `a1a`·`a1x` 같은 id 를 못 읽어 **가짜 14건**
- `smoke_all` 이 `bubbles: false` 로 이벤트를 보내 **위임 방식 핸들러를 아예 안 건드림**
- jsdom 은 리스너가 던진 예외를 `window.error` 가 아니라 **`jsdomError`** 로 보고한다

마지막 둘은 자체 검사가 없었다면 "전부 통과"라는 거짓 안심으로 끝났을 것이다.
