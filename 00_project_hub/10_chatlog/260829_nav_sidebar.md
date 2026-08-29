<!-- 260829_nav_sidebar.md -->
# 배포 사이트 내비게이션 정리 — 학년 허브 좌측 사이드바

> 2026-08-29 Nick 발제: `mid1/index.html`에서 중1수학·중2수학을 같은 크기로, 하위(프린트/인물/지도)는 숨기고,
> 중1·중2 각 허브와 프린트 페이지에 1학기/2학기 접이식 좌측 사이드바 + 프린트/인물이야기/수학지도(또는 중2의 놀이터/탐험/계산연습) 상시 노출.

## Round 1 — NCC: 배포 리포지토리(`jwj-nick.github.io`) 내비게이션 재구성 완료 (2026-08-29)

**대상 리포**: `C:\Nick\30_Apps\jwj-nick.github.io` (math-story-telling과 별도 배포 전용 리포 — 이 리포의 `mid1/`, `mid2/` 페이지들은 소스 저장소에 대응 파일이 없는 배포 전용 자산).

### 발견 — 사이드바 CSS가 이미 존재했지만 미사용

`mid1/math1/app1/concept.css`·`concept.js`(및 math2의 동일 포크본)에 **완전한 사이드바 컴포넌트**(`.sidebar`, `.sb-link`, `.sb-group`, `.hamb`, `.sb-scrim`, 900px 브레이크포인트 데스크톱 고정/모바일 드로어)가 이미 정의돼 있었고, `initChrome()`이 이미 모든 단원 페이지(u/g/p/d 전부, `MJ1.boot()`/`MJ.boot()` 호출)에 **동적으로 사이드바를 주입**하고 있었음 — 다만 1학기 라벨 없음·접기 불가·프린트 등 도구 링크 없음 상태로 미완성이었다. 이 기존 엔진을 완성하는 방향으로 작업.

### 변경 사항

1. **`mid1/index.html`**: "중1 수학" featured 카드 + 하위 children 그리드(프린트/인물이야기/수학지도)를 제거. "학년별 수학" 섹션에 중1·중2 수학을 동일한 `.grid .card` 스타일로 나란히 배치. "다른 과목"(중학 과학·역사 이야기)은 별도 섹션 유지.
2. **`mid1/math1/app1/concept.js`+`concept.css`**: `initChrome()`의 사이드바 링크 생성 로직에 ① 프린트·인물 이야기·수학 지도 3개 도구 링크(홈 바로 아래, `.sb-link.tool`) ② "1학기" 라벨 추가 ③ 1학기·2학기 단원 목록을 각각 `<details class="sb-sem" open>`로 감싸 네이티브 접기/펼치기 지원. 이 파일은 **13개 전 단원(u/g/p/d, 52페이지) 공용 엔진**이라 이 변경이 모든 단원 페이지에 자동 반영됨.
3. **`mid1/math1/print/index.html`**: concept.css/js와 별개 자기완결 페이지라 **동일 패턴의 독립 사이드바**를 자체 CSS(`.psidebar`/`.ps-link`/`.ps-sem` 등)로 신설 — 홈·중1 프린트(active)·인물이야기·수학지도 + 1학기·2학기 접이식 단원 목록(단원 링크는 `../app1/uN.html`로 개념 앱을 가리킴 — 페이지 내 기존 상단 가로 TOC는 그대로 두어 "이 페이지 안에서 유형 세트로 점프"용으로 역할 분리). 데스크톱 900px+ 고정, 모바일은 햄버거 버튼으로 드로어.
4. **`mid2/concept.js`+`concept.css`**: math1과 동일한 개선 — 다만 도구 링크는 math2 실제 자산에 맞춰 프린트·**놀이터**·**탐험**·**계산 연습**(기존 `mid2/index.html`의 tool-card와 동일 대상)로 구성. 기존 사이드바 말미의 단독 "계산 연습" 링크는 통합된 도구 그룹으로 이동.
5. **`mid2/print/index.html`**: math1 print와 동일 패턴의 독립 사이드바(홈·중2 프린트·놀이터·탐험·계산연습 + 1·2학기 접기, 단원 링크는 `../uN.html`).

### 검증

- `html.parser` 스택 기반 태그 균형 검증(5개 페이지 전부 errors:[] leftover:[]) — 대량 편집 후 구조 붕괴를 잡아낸 과거 사고([[project_math1_app1_redesign]] 교훈)를 재적용.
- 전체 href 정적 해석 검증(math1 print 133개, math2 print 88개 링크 전부 실제 파일 존재 확인).
- `node --check`로 두 `concept.js` 파일 구문 검증.
- 사이드바 HTML 생성 로직을 Node로 시뮬레이션해 `<details>` 태그 짝 맞음 확인(중첩 오류 사전 차단).
- **브라우저 확장 스크린샷 도구가 이 세션에서 응답하지 않아**(script injection timeout, 새 탭에서도 동일 재현) headless Chrome CLI(`--headless --screenshot=`)로 대체 — 데스크톱 5장 + 모바일 1장(햄버거 드로어 동작) 스크린샷으로 최종 육안 확인 완료. 5개 페이지 전부 의도대로 렌더링됨.

### 배포

배포(`jwj-nick.github.io` `3120c86`) push 완료. 소스(`math-story-telling`)에는 대응 파일이 없어 변경 없음(이 chatlog만 신규). **주의**: `high1/hanja/` 하위에 이 세션과 무관한 미커밋 변경(다른 워크스페이스 vocab-app 작업분으로 추정)이 배포 리포에 남아 있어 손대지 않고 그대로 두었음 — 다음에 그 리포를 열 때 확인 필요.

**라이브 링크**: https://jwj-nick.github.io/mid1/index.html (학년 허브) · https://jwj-nick.github.io/mid1/math1/app1/index.html (중1 수학, 좌측 사이드바) · https://jwj-nick.github.io/mid1/math1/print/index.html (중1 프린트) · https://jwj-nick.github.io/mid2/index.html (중2 수학) · https://jwj-nick.github.io/mid2/print/index.html (중2 프린트)
