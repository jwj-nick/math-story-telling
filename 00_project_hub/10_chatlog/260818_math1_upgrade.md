<!-- 260818_math1_upgrade.md -->

# math1 전면 재설계 — math2(app2) 수준으로

## Round 0 — 착수 결정 (2026-08-18)

**Nick 요청**: "math1을 많이 수정하더라도 math2 2학기 수준으로 업그레이드 필요함. 기존 math1에 아이가 큰 관심은 없었고, 2학기때는 시험도 치며, math2의 프린트 버전도 있으면 좋겠음. 계획 알려주기바람."

**NCC 사전 조사**:
- math2 프린트는 이미 72개 PDF 배포 완료(`jwj-nick.github.io/mid2/print/`) — 별도 작업 불필요로 판단, Nick에게 확인 질문.
- math1 프린트도 이미 234개 PDF 배포 완료(`jwj-nick.github.io/mid1/math1/print/`) — 다만 위치가 `mid1/print/`가 아니라 `mid1/math1/print/`라 처음엔 못 찾음.
- math1은 13단원 각자 독립 정적 HTML(concepts+index+basic_app+type_01~07+walk_01~07_H1~H3+deep_*, 단원당 28개+ 파일), 공유 엔진 없음. `geo.js`(MG)는 `MJ.makeGeo`와 API 호환 확인(트랙B 리서치 때 이미 확인한 사실 재확인).

**Q&A (AskUserQuestion)**:
1. 재설계 깊이 — 기존 콘텐츠 재포장 vs 전면 재설계 → **전면 재설계**
2. 순서 — 파일럿 먼저/2학기 먼저/1학기부터 순서대로 → **2학기(07~13) 먼저**
3. "math2 프린트 버전" 확인 — 이미 있음/새 놀이터용 프린트 원함/다른 의미 → **"math1 2학기 프린트 있어야함"**. 즉 math2 프린트가 아니라, **math1 2학기 콘텐츠가 전면 재설계되니 그에 맞는 프린트를 새로 만들어야 한다**는 뜻으로 확인.

**결정**: `00_project_hub/20_plan/0818_math1_upgrade_plan.md` 작성 완료. 요약:
- 공유 엔진 `concept.js`/`concept.css`를 math1 전용으로 포크(math2와 공유 안 함, 자기완결 원칙)
- 탭 체계 = u(개념)→g(놀이터)→p(연습)→d(심화탐구) 4탭. x(PhET)·dp(심화문제)는 1차 제외
- 콘텐츠 압축: concepts+basic_app+type_NN(7)+walk_NN_H1~H3(21) = 29개 파일 → u{N}+p{N} 2개로. deep_*+explore(geo.js 위젯) → d{N} 1개로
- 놀이터(g)는 07~12는 기존 카탈로그(`0811_interest_playground_plan.md` §2b) 재사용, 13(자료의 정리와 해석)은 신규 아이디어 필요
- 2학기(07~13) 콘텐츠 재설계 후 프린트도 `/se-print-sheet`로 재생성
- **P1(단원07 파일럿)이 게이트** — 파일럿 완성 후 Nick 검수, 패턴 확정 후 나머지 12단원 순차

**다음**: P0(엔진 스캐폴딩) → P1(단원07 기본도형 파일럿: u7+p7+d7+g7+프린트) 착수.
