<!-- 260830_math3_build.md -->
# 중3 수학(math3) 신규 제작 — 자율진행 기록

> 정본 = `00_project_hub/20_plan/0829_math3_handoff.md`. 단원표·규약 = `40_grades/middle/math3/UNITS.md`.
> Nick 지시(2026-08-29): "자율진행바람.(중3)". HITL 없음 — 단원 1 파일럿 후 2~12 자율 완주. 라운드 = 단원 1개(P0는 Round 0).
> 시작 태그 `concept-fun-p1-260829`(소스 `9983a5f` / 배포 `a93f92d`) · 착수 시점 소스 `8d190ca`.

---

# Round 0 — P0 골격 (2026-08-30)

## 단원표 재검증
- 나무위키 "2022 개정 교육과정/수학과/중학교/수학 3" 내용 체계: 수와 연산 **제곱근과 실수**(뜻·성질·대소, 무리수, 실수의 대소, 근호 사칙계산) / 변화와 관계 **다항식의 곱셈과 인수분해 · 이차방정식 · 이차함수와 그 그래프**(최댓값·최솟값 고1→중3, 실수 전체 범위만) / 도형과 측정 **삼각비 · 원의 성질**(현·접선·원주각) / 자료와 가능성 **산포도 · 상자 그림과 산점도**(사분위수·상자그림 신규, 상관관계). 교육부/NCIC 성취수준 자료 존재 확인(웹 검색). 2027년용 검정 교과서 목차 미공개.
- 핸드오프 §2 12단원표와 **빠짐·초과 없음** → 그대로 확정, `UNITS.md`에 기록. 교과서 굵기 분할(제곱근 2단원·이차함수 2단원·삼각비 2단원·원 2단원)은 NCC 판단.

## 만든 것
| 파일 | 내용 |
|---|---|
| `40_grades/middle/math3/UNITS.md` | 2022 개정 매핑표 · 12단원표(색 포함) · 엔진 연결 3곳 · 답 형식 규약 초안 · 진행 현황 |
| `40_grades/middle/math3/app3/concept.js` | math2 엔진 포크(`fork_engine.py`, 치환마다 개수 assert). `window.MJ3`, `m3theme/m3progress/m3checks`, UNITS 12(7~12 `sem:2`), 정규식 `1[0-2]`, deepq/drill 종류 제거, 탭 = 개념·(놀이터)·연습·심화 탐구(+탐험 조건부), 사이드바 브랜드 "중3 수학", 도구 = 중3 프린트 + 놀이터(첫 PLAY_READY 단원이 있을 때만). **`UNIT_READY`/`PLAY_READY`/`EXPLORE_READY` 빈 객체** — 미등록 단원은 사이드바에 회색 span(링크 없음)으로 → 404 없음. `MJ3.UNIT_READY/PLAY_READY` 노출. |
| `app3/concept.css` | math2 그대로 + `.sb-link.soon` 1줄 |
| `app3/index.html` | 허브. crumbs ← 중학 앱 · 중2 수학 ↗. 1학기/2학기 12장 전부 `.unit.soon`(div, 링크 없음, "준비 중"). 도구 카드 = 프린트만(놀이터 카드는 단원 1과 함께). 스크립트는 `a.unit`만 대상. |
| `40_grades/middle/math3/print/index.html` | 프린트 허브(mid2 패턴). 사이드바 12단원 = `.ps-link.soon` span. 본문 = 쓰는 순서 + 빈 TOC + "만들고 있어요" 안내. 마커 주석 `<!-- SB-Un -->`, `<!-- TOC -->`, `<!-- UNITS -->`, `<!-- SB-TOOLS -->`로 단원별 삽입 지점 고정(마지막 항목 경계 사고 방지). |
| 배포 `mid1/index.html` | 학년별 수학 grid에 **중3 수학 카드**(→ `../mid3/index.html`, 보라 `#8f7bd4`) — 배포 전용 파일이라 직접 편집 |

## 판단
- 사이드바 404 방지: 핸드오프는 허브 `.soon` 카드만 언급했으나 엔진 사이드바도 12단원 전부 링크하므로 `UNIT_READY` 게이트를 추가(엔진 1곳 + CSS 1줄). 단원 완성 시 `UNIT_READY`·`PLAY_READY` 두 곳에 번호 추가.
- math2 잔여 헬퍼(수직선·지수 블록·순환소수)는 삭제하지 않고 둠(무해, API 호환). 중3용 헬퍼(분수 판정 `frac`, √ 표기 등)는 파일럿에서 필요할 때 추가 + 캐시버전 bump.
- 캐시버전 `?v=20260830a`로 시작.

## 검증
- 신규 도구 `70_tools/qa/check_page.py`(태그 균형·인라인 JS 파싱·id 참조·중복 id·캐시버전 일치) → app3 index · print index · mid1 index **0건**.
- 새 포트 8561 서버 + headless Chrome: 허브·프린트 허브·mid1 **콘솔 0**. DOM 사실: 준비 중 카드 12 / `a.unit` 0 / 사이드바 회색 항목 12 · 단원 링크 0 / 도구 링크 = 프린트만 / 탭바 없음 / crumbs ← 중학 앱 · 중2 수학 ↗ / 프린트 허브 사이드바 span 12 · 빈 TOC · 안내 박스 / mid1 중3 카드 링크 존재. 서버 로그 404 = favicon뿐.
- 스크린샷 2장(허브·프린트 허브) 육안 확인 — 레이아웃·색·문구 정상.

## 배포
- 소스 커밋 → `mid3/`(concept.css·js·index.html·print/index.html) + `mid1/index.html` 파일 단위 add → 배포 커밋 → push 각각 단독. 해시는 Round 1 머리에 기록.
