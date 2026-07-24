<!-- 260721_math_expansion.md -->
# 수학 앱 학기 확장 — 크로스링크 + 중2-2 + 중1-2

> 이어짐: `260719_seeun_math_phet.md`(탐험/PhET 완료). 승인된 계획 = `~/.claude/plans/fancy-meandering-patterson.md`.
> NCC = Claude. 프로그램 tracker.

## Round 0 — 계획 승인 (2026-07-21)
**Nick 결정:** ① 새 콘텐츠 = mid2 clean 엔진 표준 · ② 중1-2 = 기존 mid1 **제자리 업그레이드** · ③ 순서 = 크로스링크 → 중2-2 → 중1-2.
**1차 자율 범위:** Phase 0(크로스링크) + Phase 1a·1b(기하 엔진 + "중2 수학" 홈) + **중2-2 첫 단원 1개 완성** → 체크인.

**현 구조 파악:**
- deploy `mid1/index.html` = "중1 학습 앱" 래퍼(math1/story/map/history, **repo 소스 없음=deploy 전용**).
- 소스 `40_grades/middle/math1/index.html` = "중1 수학" 단원 그리드(13단원, design-system CSS) → deploy `mid1/math1/`.
- mid2 = `40_grades/middle/math2/app2/`(concept.js 엔진) → deploy `mid2/`.

## Round 1 — Phase 0 크로스링크 (진행)
- **mid2 index**(소스 app2/index.html): 상단 crumb에 "중1 수학 ↗"(→ `../mid1/index.html`) 추가.
- **mid1 래퍼**(deploy mid1/index.html, 소스없음→deploy 직접): 그리드 첫 카드 "중2 수학 →"(→ `../mid2/index.html`) 추가.
- 배포 커밋 `0e6581b`(다른 앱 작업 high1·mid-sci 위에 fast-forward, 무손실) → Pages built → **양방향 라이브 확인 완료**(mid2→중1, mid1→중2).

## Round 2 — Phase 1(중2-2) 스코프 확정 (2026-07-21)
- **중2-2 목차 확정(2022 개정, WebSearch 검증):** 삼각형의 성질 · 사각형의 성질 · 도형의 닮음(+평행선과 선분의 비) · 피타고라스 정리 · 확률. **피타고라스=중2 맞음.** 교재=개념+유형 2-2 라인 존재.
- **단원 번호(mid2 확장):** 7 삼각형의 성질 · 8 사각형의 성질 · 9 도형의 닮음 · 10 피타고라스 정리 · 11 확률(경우의 수·확률). = 5단원.
- **엔진 방침:** concept.js는 기하 부품 없음 → **자체 SVG 기하 헬퍼**(삼각형·각호·눈금·직각표시·꼭짓점 라벨) 추가(JSXGraph CDN 대신 self-contained 유지, 폰 우선, mid2 makePlane 방식 계승). 확률=경우의 수 트리/표 + PhET Plinko.
- **탐험:** 기하는 PhET 빈약 → 자체 기하 sim 중심. 확률=PhET Plinko(한국어). → **중2-2 PhET 조사 에이전트 실행 중.**
- **다음:** 기하 엔진 헬퍼 → 단원7(삼각형의 성질) 개념~탐험 완성(프로토타입) → 체크인.

## Round 3 — 중2-2 PhET 조사 결과 + 기하 탐험 갈림길 (2026-07-21)
**조사 결론(라이브 검증):**
- **확률(11)**: PhET **Plinko Probability(플린코 확률)** = STRONG·한국어 확인. 단 **경우의 수(합·곱의 법칙)는 갭**→자체 카운팅 도구.
- **닮음(9)**: **Proportion Playground(비율 놀이터)** / Ratio and Proportion = Medium(닮음비 직관). AA/SAS/SSS 조건은 갭.
- **삼각형(7)·사각형(8)·평행선과 선분의 비(10)·피타고라스**: **전면 갭** — PhET에 없음(기하는 GeoGebra 영역).
- **GeoGebra 대안:** 갭들에 딱 맞는 임베드 applet 다수(닮은삼각형·피타고라스 등). 단 **별도 플랫폼**·한국어/적합도 개별 검증 필요.

**갈림길(Nick 결정):** 기하 단원(7~10) 탐험을 어떻게 채울까?
- ⓐ **자체 SVG 기하 sim 중심**(self-contained·폰·톤 일관, mid2 계승) + 확률만 PhET Plinko + 닮음에 Proportion Playground. GeoGebra 안 씀.
- ⓑ **하이브리드 + GeoGebra**: 자체 sim + 기하 갭에 GeoGebra applet 임베드(세계 최고 기하 도구) + 확률 PhET. 플랫폼 다양화.
→ 결정 후 단원7 착수.

## Round 4 — 결정 ⓑ + 기하 엔진 착수 (2026-07-21)
- **(Nick) 결정 = ⓑ 하이브리드 + GeoGebra.** 기하 탐험 = 자체 SVG sim + GeoGebra applet(닮은삼각형·피타고라스 등) + Proportion Playground(닮음) + Plinko(확률). 플랫폼 다양화(Nick 가치와 부합).
- **기하 엔진 추가:** `concept.js`에 `MJ.makeGeo(svg)` — poly(삼각형)·seg·dot·label·angle(각호+같은각 tick)·tick(같은변 눈금)·right(직각표시). self-contained SVG, viewBox 좌표. `node --check` OK.
- **단원7 계획(삼각형의 성질):** u7 개념(이등변삼각형 정의·두 밑각·꼭지각이등분선=밑변수직이등분·외심·내심) → p7 유형 → d7 심화탐구(자체 삼각형 sim) → d7p 심화문제 → x7 탐험(GeoGebra 닮은삼각형/자체 + 링크). + 홈 "중2 수학" 2학기 섹션(7 활성, 8~11 준비중) + 탭 게이팅.
- **다음:** GeoGebra 임베드 검증(한국어·iframe) → u7~x7 제작·검증·배포 → 첫 단원 완성 체크인.


## Round 5 — 단원7(삼각형의 성질) 완성·배포 (2026-07-22)
- **엔진 확장:** pageInfo `[1-6]`→`([1-9]|1[01])`(7~11 인식), UNITS u7(초록 #4a9a5f, sem:2), EXPLORE_READY 7, `MJ.makeGeo`(poly/seg/dot/label/angle/tick/right), 사이드바 2학기 그룹, 브랜드 "중2 수학". concept.css `.geo/.hub-sec/.unit.soon/.u-soon/.sb-group`.
- **5페이지:** u7 개념(이등변 슬라이더 실험 + 외심/내심 그림, JS 기하 계산) / p7 6유형18문항 / d7 외심위치 실험실(예각·직각·둔각→안/변/밖) / d7p 6문항(외심중심각 2∠A·내심각 90+½∠A·직각삼각형 외접/내접원) / x7 탐험(GeoGebra m/TXdEnQVb 한국어 + 우리실험실 + 한줄기록).
- **홈:** 중2 수학 1학기(1~6)/2학기(7 활성·8~11 준비중). 캐시 ?v=20260722 전 32페이지 통일.
- **검증:** node --check + 전 html 파스0 + p7 id정합 + 기하 계산(외심 OA=OB=OC=94.6/내심 세변거리=r=50.4) + 반말0 → ALL PASSED.
- **배포:** `396cd62` push(mid1/타앱 무영향). Pages 빌드 확인 중.
- **✅ 중2-2 프로토타입(단원7) 완성.** 다음=Nick 체크인 → 승인 시 단원8~11 양산.


## Round 6 — 중2-2 전 단원(8~11) 양산 완성 (Nick "계속 자율진행", 2026-07-22)
단원7(프로토타입) 승인 후 자율로 8~11 순차 제작·배포. 각 단원 = u/p/d/dp/x 5페이지 + 엔진 등록(UNITS·EXPLORE·홈 활성) + Node 검증(파스+정답+id정합+반말) + 배포.

- **단원8 사각형의 성질**(`05b8306`): 평행사변형 대각선 이등분 실험 / 대각선 조건 토글 분류 실험실(직/마/정사각형) / GeoGebra 평행사변형(m/wwghwudv).
- **단원9 도형의 닮음**(`8a14d61`): 닮음비 확대 실험+평행선 선분비+무게중심 / 닮음비→넓이비/부피비 실험실 / PhET 비율 놀이터.
- **단원10 피타고라스 정리**(`03d62f4`): 3-4-5 넓이 그림+a²+b²=c² 실험 / 제곱의 합 실험실+피타고라스 수 / GeoGebra 증명 시각화(m/ztpnHEut).
- **단원11 확률**(`ff3e8ba`): 경우의수+주사위 상대도수 실험 / 두 주사위 합 분포 실험실(7 최다) / PhET 플린코 확률.

**엔진 성장:** `MJ.makeGeo`가 삼각형·사각형·닮음·피타고라스 전반 재사용됨. 캐시 `?v=20260722b→e` 순차. GeoGebra `/m/` 임베드(frame-ancestors *), PhET `_ko.html`, 브라우저 Math.random(확률 sim) 활용.

**🎉 중2-2 5단원(7~11) 전부 완성·배포·라이브.** 중2 수학 = 1학기(1~6, 대수·함수) + 2학기(7~11, 기하·확률) 완비. 탐험=PhET(2·3·4·5·6·9·11) + GeoGebra(7·8·10) + 자체 sim 하이브리드.

**남은 Phase 2:** 중1-2(mid1 7~13단원) 제자리 업그레이드 — 다음 세션.


## Round 7 — Phase 2(중1-2) 착수 + 구조 발견 (2026-07-22)

### ⚠️ 중요 발견: mid1 소스↔배포 분기
- **소스** `40_grades/middle/math1/07_기본도형/`(한글 폴더, concepts/story/problems/video) 와 **배포** `mid1/math1/07_basic-geometry/`(영문 슬러그, story.html만·video 없음) 가 **폴더명·내용이 다름.** 옛 마이그레이션 산출물로, **자동 동기화 없음.**
- 결론: mid1 "제자리 업그레이드"는 **배포본(라이브, jwj-nick.github.io git 추적)** 기준으로 편집. 소스 repo(math-story-telling)와는 분기 상태(사전 존재). → Nick 인지 필요.

### mid1 단원 구조
- 각 단원 index = 자체완결(파란 #4361EE 테마, KaTeX, 카드 네비, story 모달). 섹션: 학습자료(story/concepts) · 문제연습 · 유형별(type_01~07) · 심화탐구(deep_*). **탐험(인터랙티브 GeoGebra) 없음** = 업그레이드 지점.

### 단원7 탐험 프로토타입 (배포 `3e28ac4`)
- `mid1/math1/07_basic-geometry/explore.html` 신설: mid1 파란 테마 자체완결. GeoGebra **평행선과 동위각·엇각**(m/errnuurc) + **맞꼭지각**(m/r75hjmdu) lazy 임베드 + 발견 질문 + 전체화면.
- index에 "탐험·직접 만지기" 카드 추가.
- **패턴 확립:** 단원마다 explore.html(주제별 GeoGebra) + index 탐험 카드.

### 8~13 전파 계획 (주제→GeoGebra)
- 08 작도와 합동: 삼각형 합동/작도 · 09 다각형: 내각·외각의 합 · 10 원과 부채꼴: 호·부채꼴 · 11 다면체·회전체: 정다면체/회전체 · 12 겉넓이·부피: 전개도 · 13 자료 정리: 히스토그램/도수분포.
- 각 단원 GeoGebra 한국어 자료 조사 후 explore.html + index 카드.

**다음:** Nick 확인(분기 이슈·프로토타입) 후 8~13 전파.


## Round 8 — Phase 2 완료: mid1 탐험 (GeoGebra→자체 SVG) (2026-07-24)
Nick 피드백: **GeoGebra 별로** → 자체 SVG 인터랙티브로 전환 결정. 단원7 GeoGebra판 교체 + 8~13 신규.

### 방식
- `mid1/math1/geo.js` 신설: mid2 makeGeo 이식(window.MG). 각 단원 `explore.html`(mid1 파란 테마 자체완결) + index 탐험 카드. **GeoGebra 전면 폐기.**
- ⚠️ mid1은 소스↔배포 분기 → **배포본(라이브) 직접 편집.**

### 단원별 자체 sim (7~13, 각 배포 확인)
- 07 기본도형: 평행선 동위각(횡단선 슬라이더)+맞꼭지각 (`e7bc655`)
- 08 작도합동: SAS 결정(변·끼인각 슬라이더)+합동 회전 (`d0bec85`)
- 09 다각형: 내각합=(n−2)×180 삼각분할(n 슬라이더)+외각합 360 (`d0bec85`)
- 10 원과부채꼴: 부채꼴 호길이·넓이 중심각 정비례 (`d0bec85`)
- 11 다면체·회전체: 오일러 v−e+f=2 선택 + 회전체(평면→입체) (`2f3cfa2`)
- 12 겉넓이·부피: 직육면체 겉넓이/부피(a,b,c)+뿔=기둥 1/3 (`2f3cfa2`)
- 13 통계: 히스토그램 만들기(계급 도수)+평균 (`2f3cfa2`)

**🎉 Phase 2 완료.** mid1 전 기하·통계 단원(7~13)에 자체 인터랙티브 탐험 완비. 단원7 라이브 NATIVE 확인.

### 이번 확장 프로그램(260721~) 전체 완료
- Phase 0 크로스링크 ✅ / Phase 1 중2-2 5단원 신설 ✅ / Phase 2 중1-2 mid1 탐험 7단원 ✅.
- 탐험 방침: mid2=PhET+GeoGebra+자체, mid1=**자체 SVG만**(Nick 선호). 
