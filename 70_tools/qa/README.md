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
