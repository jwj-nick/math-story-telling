<!-- 0818_math1_upgrade_plan.md -->

# 0818 math1 전면 재설계 — math2(app2) 수준으로

> 확정 2026-08-18 · 대화 = `00_project_hub/10_chatlog/260818_math1_upgrade.md`
> **핸드오프 가이드.** 이 문서 하나로 이어서 작업 가능해야 한다.

---

## 0. 결정 요약 (Nick, 2026-08-18)

| 항목 | 결정 |
|---|---|
| 재설계 깊이 | **전면 재설계**. concepts/basic_app/type_NN(7)/walk_NN_H1~H3(21)의 콘텐츠를 math2(app2) 스타일 u/p/d/g 구조로 다시 쓴다. 재포장이 아니라 압축·재작성 |
| 착수 이유 | 기존 math1에 아이가 큰 관심 없었음 + 2학기(07~13)는 실제 시험과 직결 |
| 순서 | **2학기(07~13) 먼저**, 이후 1학기(01~06) |
| 프린트 | math2 프린트(72개, 배포 완료)는 그대로 둠. **math1 2학기 콘텐츠가 바뀌므로 그 부분 프린트를 재설계 콘텐츠에 맞춰 새로 생성**해야 함(기존 234개 중 07~13분 대체) |
| 착수 방식 | 새 공유 엔진(`concept.js`/`concept.css` math1판) 스캐폴딩 → **단원07(기본도형) 파일럿** 전체 재설계 → Nick 검수 → 나머지 순차 |

---

## 1. 현재 상태 (실측)

### math1 (`40_grades/middle/math1/`) — 재설계 대상
- 13단원, 폴더당: `concepts.html`(개념) · `index.html`(단원 홈) · `story/`+`story.html`(인물 서사, **유지 — 재설계 범위 아님**) · `video/`(영상, **유지**) · `problems/`
- `problems/`: `basic_app.html` · `deep_*_app.html`(2~4개) · `type_01~07_app.html`(7개) · `walk_01~07_H1~H3.html`(21개) · `types.md`/`types.html`
- 예: 단원01 하나만 concepts(491줄)+index(296줄)+basic_app(647줄) = 이미 1400줄+, type/walk 28개 페이지는 별도
- 공유 엔진 없음. 페이지마다 자체 `<script>`, KaTeX CDN 개별 로드, 탭바 없음
- `geo.js`(namespace `MG`) — **math2 `MJ.makeGeo`와 API 100% 호환** (poly/seg/dot/label/angle/tick/right). 07~12 단원의 `explore.html`이 이미 이걸로 만든 인터랙티브 위젯 보유(각도 슬라이더, 작도 시뮬레이션 등) — **버리지 말고 d탭 콘텐츠로 흡수**
- 프린트: `40_grades/middle/math1/print/u01~u13/`, 234개 PDF, 배포 완료(`jwj-nick.github.io/mid1/math1/print/`)

### math2 app2 (`40_grades/middle/math2/app2/`) — 목표 수준
- 공유 엔진 `concept.js`(261줄)+`concept.css` — `MJ` 네임스페이스, `pageInfo()`가 파일명(`u/p/d/dp/x/g` + 번호)으로 페이지 종류 판별 → `initChrome()`이 탭바 자동 생성
- 단원당: `u{N}.html`(개념, ~235줄) · `p{N}.html`(연습, ~197줄) · `d{N}.html`(심화탐구) · `d{N}p.html`(심화문제) · `x{N}.html`(PhET 탐험) · `g{N}.html`(놀이터, 신규 — 07~10 완료)
- 프린트: `40_grades/middle/math2/print/u01~u11/`, 72개 PDF, 배포 완료

---

## 2. 아키텍처 설계

### 2-1. 공유 엔진 — **math1 전용 파일로 분리** (math2와 공유 안 함)
이유: 자기완결 원칙 + 단원표·색상 토큰이 학년마다 다름(기존 `geo.js`가 이미 이 패턴 — 로직 이식·독립 파일 유지).

```
40_grades/middle/math1/concept.js   ← app2/concept.js를 뼈대로 포크
40_grades/middle/math1/concept.css  ← app2/concept.css를 뼈대로 포크 (.pg-* 놀이터 레이어 포함)
```

포크 시 변경 지점:
- `UNITS` 배열: 13단원(01~13), math1 고유 제목·색상 토큰(`--u`/`--u2`)
- `pageInfo()`: 파일명 정규식 범위 `1~13`으로 확장 (`^u([1-9]|1[0-3])$` 등)
- `MJ.makeGeo` 로직은 **이미 `geo.js`(`MG`)로 이식되어 검증됨** — concept.js에 흡수하거나 `geo.js`를 계속 별도 include(택1, 취향 문제)
- `MJ.decimalOf`/`gcd`/`makePlane`/`animateCount` 등 도메인 무관 헬퍼는 그대로 복붙

### 2-2. 탭 체계 — **x(PhET 탐험) 제외, u/p/d/g 4탭으로**
- 기존 math1 `explore.html`은 PhET 임베드가 아니라 `geo.js` 기반 **커스텀 위젯**(math2의 `d` 성격) → 신규 `d{N}.html`에 흡수
- `x`(PhET) 탭은 math1에 PhET 임베드 자산이 없으므로 **1차 범위 제외**. 필요해지면 후속 추가(현재도 math2는 도형 단원 x7~10에 PhET 자산 있음 — math1 도형 단원도 잠재 후보지만 이번 스코프 아님)
- `d{N}p.html`(심화문제)도 **1차 제외** — math2도 얕게 쓰이는 탭이라 math1 재설계 초기엔 부담 대비 이득 낮음. 필요시 후속

**최종 탭**: 개념(`u`) → 놀이터(`g`) → 연습(`p`) → 심화탐구(`d`) — 순서는 app2와 동일(놀이터가 연습보다 앞)

### 2-3. 콘텐츠 압축 매핑 (단원당, 가장 큰 작업)

| 기존 (28+ 파일) | 신규 (1 파일) | 압축 전략 |
|---|---|---|
| `concepts.html` | `u{N}.html` | 핵심 개념만 추출, math2 개념 페이지 분량(~250줄) 목표. 인물 서사 링크는 유지(축B는 안 건드림) |
| `basic_app.html` + `type_01~07_app`(7) + `walk_01~07_H1~H3`(21) = **29개** | `p{N}.html` | math2 `p*.html` 패턴(유형별 L/M/H×3, 탭 안에서 난이도 전환) 재작성. **유형(type) 수는 유지하되 walk 단계별 풀이는 문제별 힌트 펼치기로 압축** |
| `deep_*_app.html`(2~4개) + `explore.html`(geo.js 위젯) | `d{N}.html` | 심화 개념 + 인터랙티브 위젯 한 페이지로 통합 |
| — (신규) | `g{N}.html` | **07~12는 이미 카탈로그 있음**(`0811_interest_playground_plan.md` §2b), 13(자료의 정리와 해석)은 신규 아이디어 필요 |

### 2-4. 프린트 재생성
- 2학기(07~13) 콘텐츠가 바뀌므로, 각 단원 재설계 완료 직후 `/se-print-sheet` 스킬로 해당 단원 프린트 재생성 → 기존 `40_grades/middle/math1/print/u07~u13/` 대체, 배포 갱신
- 1학기(01~06)는 콘텐츠를 안 건드리므로 프린트도 유지(재생성 불필요)

---

## 3. Phase 계획

| Phase | 내용 | 상태 |
|---|---|---|
| **P0** | 공유 엔진 스캐폴딩(`concept.js`/`concept.css` math1판) + 허브 `index.html` 개편 | ⏳ 다음 |
| **P1 ★파일럿** | 단원07(기본도형) 전체 재설계: `u7.html`+`p7.html`+`d7.html`+`g7.html` + 프린트 재생성 | — |
| P1.5 | 파일럿 리뷰(Nick) — 압축 강도·톤·놀이터 난이도 확정 | Nick |
| P2 | 2학기 나머지(08~13) 순차 재설계 — 단원13(자료의 정리와 해석)은 놀이터 아이디어 신규 브레인스토밍 필요 | — |
| P3 | 1학기(01~06) 순차 재설계 | P2 완료 후 |
| P4 | 허브 통합 + 전체 감사(`/se-audit-app`) + 배포 마감 | — |

**P1이 게이트다.** 파일럿에서 압축 강도(29개→1개로 줄이면서 얼마나 남기는지)와 놀이터 톤이 맞는지 확인한 뒤 12단원으로 확산한다 — 트랙A/B 때와 동일 원칙.

---

## 4. 리스크·주의사항

- **콘텐츠 유실 위험**: 29개 연습 파일을 1개로 압축하면서 유형 커버리지가 빠지지 않도록, 압축 전 `types.md`(유형 목록 SSOT)를 먼저 읽고 그걸 기준으로 재작성
- **story/video 폴더는 건드리지 않음** — 인물 서사 축(B)은 이 재설계와 무관, 그대로 링크 유지
- **기존 234개 PDF 중 07~13분(약 126개 추정)은 재설계 후 폐기 대상** — 삭제는 Nick 승인 후, 그 전엔 남겨둠(새 프린트와 병행 배포 후 정리)
- **세션당 진행 속도**: 단원 1개 = u+p+d+g 4페이지 + 프린트 재생성 = 놀이터 단독 작업(단원당 g 1개)보다 훨씬 큼. 무리하게 몰아치지 말고 파일럿 검수 후 페이스 조정
