<!-- 260719_seeun_math_phet.md -->
# seeun-math-phet — 킥오프

> 현재 작업 chatlog. NCC = Claude. 주제 = 세은 수학 학습에 PhET(인터랙티브 시뮬레이션) 접목.

## Round 0 — NCC 업무 파악 + 계획 초안 (2026-07-19)

### A. 현재 상태 파악

- **mid2(중2-1 세은 수학앱)**: `40_grades/middle/math2/app2/` 6단원 × 4축 = 24파일.
  2026-07-13 콘텐츠 대폭 보강·유형별 재편·Node 전수검증·`jwj-nick.github.io/mid2` 배포 완료 → **Nick 리뷰 대기**.
- **이미 있는 자체 인터랙티브**: 순환소수 변환기, 지수폭발/복리(ECharts), 부등식 풀이+수직선(음수÷ 뒤집기), 두 직선 교점(평행·일치), 일차함수 랩(기울기 삼각형·절편·평행), 식↔그래프 통합 실험실.
  → 이미 "미니 PhET"급 조작형이 단원마다 1개씩 있음.
- **repo 내 "phet" 흔적 = 0.** 완전히 새 주제.

### B. "seeun-math-phet"에 대한 NCC 해석

**PhET** = University of Colorado Boulder의 무료 HTML5 인터랙티브 시뮬레이션(수학·과학). 한국어 번역판 다수. iframe 임베드 가능(CC 라이선스). 대표 수학 sim: Graphing Lines / Graphing Slope-Intercept / Function Builder / Equality Explorer / Area Model / Fraction Matcher / Unit Rates 등.

→ 세은 수학(우선순위 a=흥미·이해·자신감)에 **조작하며 원리를 발견하는 트랙**을 추가하려는 것으로 해석.

### C. 방향 3안 (NCC 판단 포함)

| 안 | 무엇 | 장점 | 단점 |
|---|---|---|---|
| **A. 실물 PhET 큐레이션** | 단원별로 관련 PhET sim을 골라 임베드/링크한 "탐험 허브" | 세계 최고 품질 즉시 활용, 제작 빠름, 한국어판 존재 | 외부 의존(인터넷 필요), 중2 교육과정과 100% 안 맞음, 폰/iframe 편차, self-contained 원칙과 충돌 |
| **B. 자체 PhET급 sim 제작** | 기존 concept.css/js 엔진으로 조작형 sim을 새로 제작 | 교육과정 정확, self-contained, 폰 우선, 톤 통일 | 제작 느림(이미 몇 개는 있음) |
| **C. 하이브리드(NCC 추천)** | 단원별 "탐험" 허브 = 잘 맞는 실물 PhET 링크 + PhET가 안 맞는 중2 급소는 자체 sim | 폭(PhET)+정확(자체) 둘 다, 세은이 즐기며 이해 | 큐레이션+제작 둘 다 필요 |

**NCC 추천 = C (하이브리드), 단 1단계는 "실물 PhET 큐레이션 조사"부터.** 무엇이 이미 있고 한국어판이 있는지 먼저 봐야 자체 제작 범위가 정해짐.

### D. 계획 초안 (Phase)

- **Phase 0 (조사)**: 세은 단원(중2-1: 순환소수·식계산·부등식·연립·일차함수·함수와방정식)에 매핑되는 실물 PhET sim 목록화 — 한국어 여부, 폰 지원, 임베드 가능 여부, 교육과정 적합도 평가.
- **Phase 1 (매핑 확정)**: 단원별 "이 sim으로 이걸 발견" 학습 의도 1줄씩. PhET로 충분한 곳 / 자체 제작 필요한 곳 분리.
- **Phase 2 (허브 앱)**: 세은이 들어와 노는 "탐험" 페이지. mid2 앱 안 새 탭 vs 별도 앱 — 아래 열린 질문.
- **Phase 3 (자체 sim 보강)**: PhET 갭 채우는 자체 sim 제작(기존 엔진).

### E. 열린 질문 (Nick 결정 원함)

1. **"phet" 의미 확인**: 위 해석(PhET 시뮬레이션 접목)이 맞나? 다른 뜻이면 알려줘.
2. **방향**: A(실물 큐레이션) / B(자체 제작) / C(하이브리드) 중?
3. **범위**: 지금 mid2(중2-1) 6단원 대상? 아니면 세은 수학 전반(중2 전체/중1 포함)의 범용 "수학 놀이터"?
4. **거주지**: 기존 mid2 앱 안에 "탐험" 탭 추가? 아니면 별도 standalone 앱/배포?
5. **우선순위**: mid2 리뷰 대기 중인데, phet는 병렬 새 트랙인가, 리뷰 먼저인가?

### (Nick) — 결정 (2026-07-19)

1. **phet = PhET 시뮬레이션 접목 맞음.**
2. **방향 = C 하이브리드** (실물 PhET 큐레이션 + 갭은 자체 sim).
3. **범위 = mid2 중2-1 6단원.**
4. **거주지 = mid2 앱 안 '탐험' 탭** (개념→연습→심화→탐험 동선).
5. 우선순위: (명시 안 됨 → NCC는 phet를 새 트랙으로 병렬 진행. mid2 리뷰는 Nick 몫으로 열어둠.)

## Round 1 — Phase 0 착수: PhET 실물 인벤토리 조사 (NCC)

**목표:** 중2-1 6단원에 매핑되는 실물 PhET math sim을 조사해, 단원별 "이 sim으로 이걸 발견" 매핑표 초안 작성. 각 sim의 (한국어판 여부 / HTML5·폰 지원 / iframe 임베드·라이선스 / 교육과정 적합도)를 확인해 **PhET로 충분한 단원 vs 자체 sim 필요한 단원**을 가른다.

**6단원 ↔ PhET 후보 (NCC 사전 가설, 조사로 검증):**
| 단원 | 개념 | PhET 후보 | 예상 |
|---|---|---|---|
| 1 순환소수 | 유리수·순환소수 | Fractions/Fraction Matcher (배경만) | **갭 → 자체**(이미 변환기 있음) |
| 2 식의 계산 | 지수·다항식 | Area Model Algebra, Expression Exchange | PhET 강함 |
| 3 일차부등식 | 부등식 성질·풀이 | (전용 sim 없음 추정) | **갭 → 자체**(이미 수직선 있음) |
| 4 연립방정식 | 두 미지수·교점 | Equality Explorer: Two Variables, Graphing Lines | PhET 강함 |
| 5 일차함수 | 기울기·절편 | Graphing Lines, Graphing Slope-Intercept, Function Builder | PhET 매우 강함 |
| 6 함수와 방정식 | 그래프↔방정식·교점 | Graphing Lines | PhET 강함 |

→ 조사 에이전트 1개(백그라운드) 실행. 결과로 매핑표 확정 후 Round 2에서 Nick 확인.

## Round 2 — PhET 인벤토리 결과 + 단원 매핑 확정 (NCC)

**조사 결론(라이브 검증):** 후보 19개 전부 **HTML5·한국어판·iframe 임베드 가능·CC-BY**. 죽은 Java/Flash 없음. 임베드 URL 패턴 = `https://phet.colorado.edu/sims/html/<slug>/latest/<slug>_ko.html`. CC-BY → 페이지에 "PhET Interactive Simulations, University of Colorado Boulder" 출처 표기 필수.

### 단원별 매핑 (하이브리드 확정)

| 단원 | PhET (실물) | 한글 sim | 적합 | 갭 → 자체 |
|---|---|---|---|---|
| **1 순환소수** | — (없음) | — | **전면 갭** | 자체: 기존 d1 순환소수 변환기 승격 (긴나눗셈→순환마디 애니 향후) |
| **2 식의 계산** | Expression Exchange(동류항·대입) + Area Model Algebra(전개) | 식 교환 / 면적 모형: 대수 | **강함** | 지수법칙만 갭 → 기존 d2 지수폭발 |
| **3 부등식** | Equality Explorer(양변 균형 직관) | 등식 연습하기 | 부분(직관만) | **핵심 갭**(음수 뒤집기·수직선 해) → 기존 d3 부등식 풀이기 |
| **4 연립방정식** | Equality Explorer: Two Variables + Graphing Lines(교점) | 등식 연습하기: 2변수 | 중간 | 대입/가감 단계·교점=해 → 기존 d4 교점 탐색기 |
| **5 일차함수** | Graphing Slope-Intercept + Graphing Lines | 그래프 기울기-절편 / 그래프에 선 그리기 | **매우 강함(완전 커버)** | 없음 |
| **6 함수와 방정식** | Graphing Lines(그래프↔식) | 그래프에 선 그리기 | 강함 | 표준형 ax+by+c=0·교점=연립해 → 기존 d6 실험실 |

**slug:** graphing-lines · graphing-slope-intercept · equality-explorer · equality-explorer-two-variables · expression-exchange · area-model-algebra.

**핵심 통찰:** 단원 5는 PhET로 완전 커버(최고 쇼케이스) → **단원5부터 프로토타입**. 단원 1·3은 PhET 갭 → 자체 sim(이미 있음)을 '탐험' 톤으로 재배치. 그래서 하이브리드가 정확히 맞아떨어짐.

### 탐험 탭 주입 설계 (엔진 확인 완료)

- `concept.js`의 `initChrome()` `tabs` 배열에 5번째 `{k:'explore', href:'x'+no+'.html', i:'🧭', t:'탐험'}` 추가.
- `pageInfo()`에 `if(m=f.match(/^x([1-6])$/)) return {no:+m[1],kind:'explore'};` 추가.
- `.utabs`는 가로 스크롤 flex → 5탭 폰에서 안전(스크롤).
- ⚠️ 공용 엔진이라 탭 추가 즉시 전 단원에 노출 → **x1~x6를 한 번에 만들어 404 방지**(단원1은 자체 sim만이라도).
- 탐험 페이지 `x{N}.html` = 기존 chrome(사이드바+히어로+탭바) + sim 카드들. 각 카드 = 한글 sim명 + "이 sim으로 발견할 것" 1줄 + 발견 질문 2~3개(딸이 조작하며 답) + 열기 버튼 + 출처.

### 폰 주의(조사 반영)
- PhET는 가로 ~1024 캔버스 기준 → 폰 세로에서 컨트롤(기울기 핸들·스피너)이 잔손질 어려움.
- 대책: iframe **min-height ~600**, **lazy 로드**(탭 시 로드=페이지 빠름·인터넷 절약), "가로로 돌리면 잘 보여요" 안내, **전체화면 새 탭** fallback 링크.

### 열린 질문 (Nick) — sim 표시 방식
아래 질문으로 결정. 확정되면 단원5 프로토타입 → Nick 확인 → 나머지 5단원 확장.

### (Nick) 결정 — sim 표시
**카드 + 탭하면 인라인 lazy 확장 + 전체화면 fallback.** (폰 우선·페이지 빠름)

## Round 3 — 단원5 탐험 프로토타입 제작·검증 (NCC, 2026-07-19)

**만든 것:**
- **엔진(`concept.js`)** — ① `pageInfo()`에 `x([1-6])→explore` ② `EXPLORE_READY={5:1}`로 준비된 단원만 탐험 탭 노출(404 방지) ③ 탭 배열에 5번째 🧭 탐험 탭. 전부 additive·기존 24페이지 무영향.
- **`x5.html`(단원5 탐험)** — 카드 3개:
  1. **그래프 기울기-절편**(graphing-slope-intercept) — a·b 조작으로 기울기·y절편 발견 (딱 맞음).
  2. **그래프에 선 그리기**(graphing-lines) — 선 끌기→식 변화·x절편·선맞히기 게임 (딱 맞음).
  3. **함수 제조기**(function-builder) — 함수(대응) 감 잡기 (가볍게).
- 각 카드 = 한글 sim명 + English + "발견할 것" 1줄 + 발견 질문 2~3개 + [여기서 열기(탭 시 iframe lazy 로드)] + [전체화면 ↗ 새 탭] + CC-BY 출처. 가로 회전 안내 + 폰 min-height 600.
- 스타일은 x5 인라인 `<style>`(프로토타입) — 확정 후 concept.css로 승격 예정.

**검증(Node + 라이브):**
- `node --check concept.js` OK. x5 인라인 스크립트 파스 0에러.
- 카드 3·iframe 3·data-src 3·PhET _ko URL 6개(slug 일치)·CC-BY 4곳.
- **PhET `_ko.html` 라이브 확인(WebFetch): 3개 전부 VALID.** 실제 한글 제목 확인 → graphing-slope-intercept="그래프 기울기-절편", graphing-lines="그래프에 선 그리기", function-builder="함수 제조기"(카드 제목 실제와 일치하도록 수정).

**배포 완료 (2026-07-19, Nick "지금 배포" 지시):**
- app2 → `C:/Nick/30_Apps/jwj-nick.github.io/mid2/` 복사(27파일). concept.js 참조 `?v=20260719` 캐시 무효화(bump.js, 26 html).
- 로컬 커밋(`4a5c56e`) 먼저 → 단독 push(`98bdf21..4a5c56e`) [멈춤방지 프로토콜].
- GitHub Pages 빌드 커밋 4a5c56e = building 확인. **Live: https://jwj-nick.github.io/mid2/x5.html** (또는 u5→🧭 탐험 탭).

**다음:** Nick이 단원5 탐험 확인 → 피드백 반영 → x1~x4·x6 확장(단원1·3은 자체 sim '탐험' 톤 재배치, 2·4·6은 PhET+자체) → concept.css로 스타일 승격 → EXPLORE_READY 확장.

## Round 4 — 전 단원 확장 (Nick "다른 챕터들도 진행", 2026-07-19)

**추가 PhET 라이브검증(한글 제목):** 분수 짝짓기(fraction-matcher) · 식 교환(expression-exchange) · 면적 모형: 대수(area-model-algebra) · 등식 연습하기(equality-explorer) · 등식 연습하기: 2변수(equality-explorer-two-variables) — 5개 전부 VALID.

**만든 것 (x1~x4·x6):**
| 페이지 | PhET 카드 | 우리 실험실(자체) |
|---|---|---|
| x1 순환소수 | 분수 짝짓기(가볍게) | 순환소수 변환기 → d1 (PhET 갭) |
| x2 식의 계산 | 식 교환 + 면적 모형: 대수 | 지수 폭발 → d2 (지수법칙 갭) |
| x3 부등식 | 등식 연습하기(직관) | 부등식 풀이기 → d3 (음수 뒤집기 갭) |
| x4 연립 | 등식 연습하기:2변수 + 그래프에 선 그리기 | 교점 탐색기·대입법 → d4 |
| x6 함수와 방정식 | 그래프에 선 그리기 | 식↔그래프 실험실 → d6 (표준형·교점 갭) |

- 갭 단원(1·3)은 "PhET에 없어서 우리가 만들었어요"라고 **정직하게** 프레이밍 + 자체 sim(dN)으로 링크(`.phet.ours` 초록 액센트).
- 엔진: `EXPLORE_READY={1..6}` 전 단원 개방. 스타일 x5 인라인 → **concept.css 컴포넌트 승격**(`.phet/.ph-btn/.xhint/.phet.ours`). 캐시 `?v=20260719b`로 js·css 전 페이지 통일.

**검증:** `node --check concept.js` OK + 6페이지 인라인 파스 0에러 + PhET slug 8종 라이브검증·slug일치 + CC-BY==iframe+1 + 내부 dN 링크 존재 + 반말스캔 0. → **ALL PASSED.**

**배포:** app2→mid2(34파일) 로컬커밋(`62f54c3`) → 단독 push(`4a5c56e..62f54c3`). Pages 빌드 확인 중.
- **전 단원 탐험 탭 라이브:** https://jwj-nick.github.io/mid2/x1.html … x6.html (또는 각 단원 u/p/d 상단 🧭 탐험 탭).

**남은 것:** Nick 폰 리뷰(6단원 탐험 톤·발견질문·PhET 폰 조작감) → 피드백 반영. (선택) 우리 실험실 sim들 자체 강화.

## Round 5 — 홈 발견성 추가 (2026-07-19)
- 홈(index.html): ① 히어로 흐름 "개념→연습→심화→🧭 탐험" ② 탭 안내 문구에 탐험 추가 ③ **탐험 소개 tool-card**(→x5 맛보기, "각 단원 🧭 탐험 탭에 있어요"). 세은이 홈에서 새 기능을 놓치지 않도록.
- 검증: index 인라인 파스 0에러·tool-card 2·x5 링크·버전 OK. 배포 커밋 `6c78235` push(`62f54c3..6c78235`).
- **✅ seeun-math-phet 1차 완료:** 6단원 탐험 탭 + 홈 발견성까지 라이브. Nick 폰 리뷰 대기.

## Round 6 — 기술 검증 + 품질 감사 (2026-07-19)
- **iframe 임베드 가능성 확인(핵심):** PhET `_ko.html`은 `X-Frame-Options`·`CSP frame-ancestors` **없음** → "여기서 열기" 인라인 임베드 실제 동작 확인(curl -sI 200, 헤더 무제한). 인라인 임베드 리스크 해소.
- **APP_PRINCIPLES 자체 감사:** 탐험 페이지 = 해요체 ✓ / 유도 메시지(발견 질문) ✓ / 점진적 공개(답 미노출) ✓ / 빈칸(열린 발견 질문) ✓ / 반응형 ✓. 색상 원칙은 math1 기준→mid2 자체 팔레트로 비적용. **강제 수정 위반 없음.**
- 홈 index 라이브 확인: 탐험 카드·흐름 갱신 반영됨(commit 6c78235).

### 선택 후속(Nick 결정) — 지금은 미착수
1. **탐험 반영 '빈칸' 강화:** 각 탐험 끝에 "오늘 발견한 것 한 줄 쓰기"(teach-back) 추가? (현재는 열린 발견 질문으로 빈칸 충족 중) — 탐험을 '순수 놀이'로 둘지 '놀이+기록'으로 할지 Nick 취향.
2. **우리 실험실(dN) 자체 sim 강화** (특히 갭 단원 1·3).
3. **소스 repo(math-story-telling) 커밋** — 현재 x1~x6·concept.*·index·chatlog 미커밋(배포 repo는 push 완료). CLAUDE.md "요청 시 커밋" 원칙이라 대기.

## Round 7 — 후속 2·1·3 모두 진행 (Nick "2,1,3 순서대로", 2026-07-19)

**Task 2 — 갭 단원 자체 실험실 강화:**
- **d1 긴 나눗셈 애니메이터**(분수→순환소수): 프리셋 6개(1/3·2/7·1/6·5/11·1/4·3/8), 나눗셈 스텝 애니 + "나머지가 되돌아옴 = 순환마디 탄생"(pigeonhole 직관). Node 6/6 정답 검증.
- **d3 뒤집힘 실험실**(양변 ×k 반사 수직선): 2<5에 k(−3~3) 곱해 두 점이 0 기준 반사→순서 뒤집힘 실시간. 음수 곱=부등호 뒤집힘의 근본 시각화(PhET 못 함).

**Task 1 — 탐험 한 줄 기록:** x1~x6 각 끝에 "한 줄 기록·오늘의 발견" teach-back 섹션(단원별 맞춤 placeholder + localStorage `m2reflect_<page>` 저장·복원). 세은 언어 강점 활용, 빈칸 원칙.

**Task 3 — 소스 repo 커밋:** `C:/Kids/math-story-telling` main에 app2 전체 + 이 chatlog 커밋(`8f212bb`, 35파일). 무관한 사전 변경(CLAUDE.md·기타 chatlog·app/·prototypes/·__pycache__)은 제외=Nick 몫. push는 안 함(요청=커밋).

**검증·배포:** node --check + 8페이지 파스 0에러 + d1 6/6 + 탐험 정합 유지 → 배포 커밋 `6486456` push(`6c78235..6486456`), Pages built. 라이브 확인: d1 긴나눗셈·d3 뒤집힘·x5 한 줄 기록 모두 정상.

**✅ seeun-math-phet 후속 3건 완료.** 남은 것: Nick 폰 리뷰 → 피드백. (선택) 나머지 갭/우리실험실 추가 강화, 자체 sim 확대.


