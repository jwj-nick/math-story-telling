<!-- 0829_concept_fun_handoff.md -->
# 핸드오프 — 개념 페이지 "재미 1순위 묶음" 구현 (compact 후 Sonnet 세션용)

> **이 문서 하나만 읽고 착수할 수 있게 쓴다.** 배경 토론은 `00_project_hub/10_chatlog/260829_concept_fun_ideas.md`(Round 1~2).
> 작성 2026-08-29 · Nick 승인 완료(Q1~Q3) · 시작 시점 태그 `m1-exam6-nav-260829`.

## 0. 한 줄 목표

중1 수학 개념 페이지(u1~u13)의 **공용 엔진 `concept.js`/`concept.css` 한 곳**을 고쳐, 13단원 52페이지에 다음 4가지가 자동 적용되게 한다:
**B1 정답 마이크로 애니 · B2 오답 시 힌트 먼저 · A1 완주 도장+꽃가루 · B6 이어하기.** 개별 u/g/p/d 페이지 본문은 손대지 않는다(캐시버전 bump만).

## 1. 반드시 지킬 것 (딸 프로필 기반 — LEARNER_PROFILE.md)

- **스트레스 없는 진행이 최우선 KPI.** 오답에 흔들림(shake)·빨간색·경고음 금지. 오답은 부드럽게(노란/민트 톤) "다시 한 번?".
- **화려함은 완주 순간에만.** 정답 하나하나에 큰 효과 금지 — 작은 ✓ 정도.
- **취향: 손그림 느낌 · 민트 계열 · 과하지 않은(고등학생 언니 취향) 절제된 스타일.** 유아용 귀여움·과장 애니 금지. 이번 1순위엔 그림 자산이 없으니 색·타이밍에서만 반영(민트 = 기존 `--sage #4fa892` 계열 활용).
- 학생용 문구는 전부 **해요체**(`10_system/10_principles/WRITING_VOICE.md`).
- `prefers-reduced-motion` 존중(기존 CSS 패턴 있음).

## 2. 파일 위치 (소스가 정본, 배포로 복사)

| 역할 | 소스(정본) | 배포 |
|---|---|---|
| 엔진 JS | `C:\Kids\math-story-telling\40_grades\middle\math1\app1\concept.js` | `C:\Nick\30_Apps\jwj-nick.github.io\mid1\math1\app1\concept.js` |
| 엔진 CSS | `…\40_grades\middle\math1\app1\concept.css` | `…\jwj-nick.github.io\mid1\math1\app1\concept.css` |
| 단원 페이지 | `…\40_grades\middle\math1\app1\u1~u13.html` (+ g/p/d) | 같은 이름으로 배포 폴더에 |
| 참고(포팅 원본) | `…\app1\g6.html` 85~118행: `.stamp` 마크업 + 인라인 `confetti()` 함수 | |

**소스에서 고치고 → 검증 → 배포 폴더로 복사 → 양쪽 커밋.** 현재 두 곳은 동기화돼 있음(2026-08-29 확인).

## 3. 현재 엔진 구조 (concept.js, `window.MJ1`)

- `pageInfo()` — 파일명으로 단원 번호·종류(`concept`/`play`/`practice`/`deep`) 판정.
- `initTheme()`·`bindToggle()` — 라이트/다크, localStorage `m1theme`.
- `store()`/`saveStore()` — localStorage `m1progress` = `{u6:true,...}` (단원 완료 여부만).
- `completeUnit(id)` — 완료 저장 + `#done-note`에 `.show` + 사이드바 링크에 `.done`.
- `makeProgress(barId,total)` — 진행바 `<i>` 조각 생성, 반환된 함수를 호출할 때마다 한 칸 `.on`.
- `check(id,test,outId,opt)` / `checkNum(inputId,correct,outId,onOk)` — 정답 판정. **현재 정답=`<span class="good">정답이에요</span>`, 오답=`아니에요. 답은 X이에요` 텍스트만.** 각 u 페이지는 `MJ1.checkNum('c1',15,'c1o',function(){did('direct');})` 식으로 호출하고, 페이지 내부 `did(k)`가 `prog()`를 올려 5개 채우면 `MJ1.completeUnit('uN')`.
- `hintSteps(btnId,boxIds)` — 단계별 힌트 공개(놀이터용, u 페이지 미사용).
- `initChrome()` — 사이드바 주입·히어로·탭바·단원 색(`--u`,`--u-2`,`--u-soft`).
- 입력/버튼 id 규약: 입력 `c1`, 버튼 `c1b`, 출력 `c1o` (전 단원 동일).

CSS에 이미 있는 것: `.good`, `.progress i.on`(fillbar 애니), `.done-note.show`(pop), `.stamp`/`.seal`(stampin 애니), `.pg-confetti i`(pgfall 애니), `@keyframes pop/fillbar/stampin/pgbump/pgfall`.

## 4. 구현 스펙

### B1. 정답 마이크로 애니 (check·checkNum 공통)
- 정답: 입력에 클래스 `ok` 부여 → CSS `@keyframes okpulse`(테두리 민트색 0.6s 부드럽게 밝아졌다 돌아옴, 크기 변화 없음) + out 에 `<span class="good"><i class="tick">✓</i> 정답이에요</span>`, `.tick`은 `pop` 0.35s로 톡 떠오름. 진행바 새 칸엔 기존 fillbar에 더해 `scaleY(1.25)` 0.3s 살짝 부풂(`@keyframes barbump`).
- 오답: 입력에 클래스 `retry`(테두리 연노랑, 0.4s 페이드) — **흔들림 없음.** 정답 시 `retry` 제거.
- 입력 이벤트로 클래스 정리(다시 타이핑하면 `ok`/`retry` 제거).

### B2. 오답 시 힌트 먼저, 두 번째부터 정답
- `check()`·`checkNum()`에 입력 id별 시도 횟수 맵(클로저 `var tries={}`).
- 1회째 오답: out = `아직이에요 — 한 번 더 생각해 봐요 🙂` (정답 비공개). `opt.hint`가 있으면 그 문장을 함께.
- 2회째부터: 기존대로 `아니에요. 답은 <b class="gold">X</b>이에요`.
- 정답 맞히면 tries 초기화. **u 페이지는 수정 불필요**(generic).

### A1. 완주 도장 + 꽃가루 (completeUnit 확장)
- `completeUnit(id)`가 처음 완료될 때(이미 `store()[id]`가 true였으면 재생 안 함):
  1. `#done-note` 안을 `.stamp` 구조로 바꿈: `<div class="seal">🌸</div><div class="seal-t">단원 N 완주!</div><div class="seal-d">(단원 제목) — 끝까지 해냈어요.</div>` (제목은 `UNITS[n-1].t`).
  2. `document.body`에 `<div class="pg-confetti on">` 생성하고 g6.html 107~117행의 `confetti()` 로직을 `MJ1.confetti(host,colors)`로 포팅. 색은 단원 시그니처 `[--u, --u-2]` + 민트 `#4fa892`, `#63c6b1` 4색. 46개, 2초 뒤 host 제거.
  3. `prefers-reduced-motion`이면 꽃가루 생략(도장만).
- `.done-note` 위치까지 부드럽게 스크롤(`scrollIntoView({behavior:'smooth',block:'center'})`).

### B6. 이어하기 (페이지가 나를 기억함)
- 저장: `check()`/`checkNum()` 정답 시 localStorage `m1checks` = `{u6:['c1','c2',...]}`에 입력 id 추가(단원 id는 `pageInfo()`로).
- 복원(`initChrome`에서 `kind==='concept'`일 때, 단원 미완료인 경우):
  - 저장된 id마다: 입력 `disabled`, 버튼(`id+'b'`) `disabled`, out = `<span class="good">✓ 지난번에 맞혔어요</span>`, 입력에 `ok` 클래스(애니 없이).
  - 진행바: `makeProgress(barId,total)`가 복원 개수만큼 미리 `.on` 처리하고 `done` 카운터를 그 값으로 시작. `done>=total`이 되면 엔진이 직접 `completeUnit(unit.id)` 호출(페이지 쪽 `n>=5` 조건과 무관하게 완료 가능).
  - 히어로 아래에 배너 `<div class="resume">지난번에 <b>N/5</b>까지 했어요 — <a>이어서 볼까요? →</a></div>`; 클릭 시 첫 번째 **미복원** `.check`로 smooth scroll. 복원 0개면 배너 없음.
- 주의: 복원된 입력은 disabled라 재정답으로 진행바가 이중 카운트되지 않음. 완료된 단원(`m1progress[id]===true`)은 복원 생략(기존 done-note만).
- 복잡하면 **폴백**: 복원 없이 배너+스크롤만.

### 0단계(먼저): 캐시버전 통일
app1의 52+개 html이 `concept.css?v=…`/`concept.js?v=…`를 11가지 값으로 쓰고 있음. 엔진 수정 후 **소스·배포 양쪽 app1/*.html 전부** 한 값으로 bump:
```
cd 40_grades/middle/math1/app1 && sed -i 's/concept\.\(css\|js\)?v=[0-9a-z]*/concept.\1?v=20260830a/g' *.html
grep -ho "concept\.\(css\|js\)?v=[0-9a-z]*" *.html | sort | uniq -c    # 두 줄(css/js) × 같은 수만 나와야 함
```
배포 폴더에도 동일 실행(또는 html 전부 복사).

## 5. 검증 (전부 통과해야 배포)

1. `node --check 40_grades/middle/math1/app1/concept.js`
2. 로컬 서버: **반드시 새 포트**(예 8541)로 `python -m http.server 8541 --bind 127.0.0.1` — 과거 세션의 유령 서버가 옛 파일을 정상처럼 돌려주는 사고 있었음. 끝나면 `netstat -ano | grep :8541`로 PID 찾아 `taskkill //F //PID`.
3. **브라우저 확장(mcp claude-in-chrome) 스크린샷은 이 환경에서 타임아웃이 잦았음** → headless Chrome CLI 사용:
   `"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless --disable-gpu --no-sandbox --disable-extensions --window-size=1400,1400 --screenshot=<scratchpad>/x.png http://127.0.0.1:8541/mid1/math1/app1/u6.html` → Read 도구로 png 확인. (배포 폴더 `C:\Nick\30_Apps\jwj-nick.github.io`를 서버 루트로 하면 경로가 라이브와 같음.)
4. 콘솔 오류 0: headless로 `--enable-logging=stderr --v=0` 붙여 stderr에 `Uncaught` 없는지 grep, 또는 `--dump-dom`으로 사이드바·done-note가 DOM에 있는지 확인.
5. 동작 시나리오(u6에서): 정답 → ✓ 톡, 진행바 부풂 / 오답 1회 → 힌트 톤, 정답 미공개 / 오답 2회 → 정답 공개 / 5개 완료 → 도장+꽃가루 1회 / 새로고침 → 맞힌 문항 복원·배너·이어가기 스크롤 / 완료 단원 재방문 → 꽃가루 재생 안 함.
6. 회귀: g6·p6·d6도 열어 사이드바·테마 토글 정상(엔진 공용이므로).
7. `PYTHONIOENCODING=utf-8` 선제. heredoc 금지(스크립트는 파일로 Write→실행).

## 6. 배포 절차

1. 소스 커밋: `git add 40_grades/middle/math1/app1/concept.js 40_grades/middle/math1/app1/concept.css 40_grades/middle/math1/app1/*.html` (파일 지정, `-A` 금지).
2. 복사: 위 파일들을 `C:\Nick\30_Apps\jwj-nick.github.io\mid1\math1\app1\`로.
3. 배포 리포는 **파일 단위로만 `git add`** — `high1/hanja/` 아래에 이 작업과 무관한 미커밋 변경이 남아 있음(건드리지 말 것).
4. `git push`는 단독 명령으로(네트워크 명령은 다른 작업과 한 줄에 묶지 않음 — CLAUDE.md 멈춤 방지 프로토콜).
5. 라이브 확인은 `WebFetch`로 `https://raw.githubusercontent.com/jwj-nick/jwj-nick.github.io/main/mid1/math1/app1/concept.js` 에 새 함수명이 있는지(Pages CDN은 몇 분 지연).
6. chatlog `260829_concept_fun_ideas.md`에 Round 3 기록(무엇을 넣었고, 스크린샷으로 무엇을 확인했는지).

## 7. 이번 라운드에서 하지 않는 것

- 2순위(C1 인물 아바타·C3 내 수학 노트)·3순위(A2 전환점·C2 스티커·A4 별자리) — 딸 반응 본 뒤.
- math2(`mid2/concept.js`)에는 아직 옮기지 않음 — math1에서 확정된 뒤 같은 방식으로.
- 개별 u 페이지 본문·문구 수정 없음.

## 8. 완료 판정

13단원 어느 u 페이지를 열어도 위 4가지가 동작하고, 검증 5·6·7 통과, 소스·배포 양쪽 커밋·push, chatlog Round 3 기록.
