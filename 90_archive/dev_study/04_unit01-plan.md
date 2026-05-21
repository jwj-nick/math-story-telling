# 04 — unit01 구현 계획

> 소인수분해 단원을 정적·인터랙티브·영상으로 만드는 단계별 계획.

---

## 전체 결과물 목표

```
80_tools/unit01_소인수분해/
├── index.html          # 스토리 허브 (이야기 + 섹션 카드)
├── sieve.html          # 소수의 체 인터랙티브 애니메이터
├── concepts.html       # 개념 카드 + 빈칸 채우기
├── problems.html       # 문제 12개 (힌트 토글, 답 확인)
└── shared.css          # 공통 스타일

(영상 — 별도 Phase)
90_video/unit01_소인수분해/
└── sieve-scene.html    # HyperFrames composition → sieve.mp4
```

---

## Phase 1: 인터랙티브 웹 (4개 HTML)

### Step 1-A: shared.css 먼저
- 색상, 타이포, 레이아웃 변수 정의
- unit01 테마: 황금빛(이야기) / 파랑(개념) / 초록(문제) / 빨강(소수 강조)
- nav 공통 컴포넌트 스타일
- 예상 작업 시간: 30분

### Step 1-B: sieve.html ← 핵심, 먼저 만들기
```
기능 목록:
  [ ] 1~50 숫자 그리드 (5열 × 10행)
  [ ] "자동 시작" 버튼 → 애니메이션
  [ ] 단계별 텍스트: "2의 배수를 지웁니다..."
  [ ] 소수 강조 (빨강), 합성수 회색 처리
  [ ] "직접 해보기" 모드 (버튼 토글)
  [ ] 범위 선택: 30 / 50 / 100 (라디오 버튼)
```
예상 줄 수: ~350줄

### Step 1-C: index.html (스토리 허브)
```
기능 목록:
  [ ] unit01.md §1 이야기를 HTML로 예쁘게 편집
  [ ] 인물 배지 (에라토스테네스, BCE 276~194)
  [ ] 섹션 카드 4개: 소수의 체 / 개념 / 문제 / 글쓰기
  [ ] 핵심 인용문 풀아웃 박스
```
예상 줄 수: ~200줄

### Step 1-D: concepts.html
```
기능 목록:
  [ ] 개념 플래시카드 (앞/뒤 뒤집기, CSS transform)
      소수 / 합성수 / 거듭제곱 / 소인수분해 / GCD / LCM
  [ ] 소인수분해 팩터트리 시각화 (SVG 또는 CSS flex)
  [ ] "1은 소수?" 인터랙티브 질문 박스
```
예상 줄 수: ~380줄

### Step 1-E: problems.html
```
기능 목록:
  [ ] 12문제 나열 (웜업 5, 기본 5, 도전 2)
  [ ] 문제별 "힌트 보기" 토글 버튼
  [ ] 답 입력 → "확인" → 정답/오답 피드백
  [ ] 문제 11번: 체 그리기 (sieve.html 미니 버전)
  [ ] 진행 바 (몇 개 풀었는지)
```
예상 줄 수: ~420줄

---

## Phase 2: 영상 (HyperFrames)

### Step 2-A: HyperFrames 설치 확인
```bash
node --version   # v18+ 필요
npm install -g @heygen/hyperframes
hyperframes --version
```

### Step 2-B: sieve-scene.html 작성
```
이 파일은 "영상으로 출력될" HTML.
브라우저에서 열면 타임라인 기반 애니메이션이 자동 재생됨.
HyperFrames가 이걸 프레임별로 캡처 → MP4.

포함할 것:
  [ ] 제목 자막: "소수의 체 — 에라토스테네스의 발견"
  [ ] 1~30 숫자 그리드 (더 작은 범위로 영상용)
  [ ] CSS animation: 2의 배수 fade-out (1.5초)
  [ ] 자막 텍스트 페이드인
  [ ] 각 소수 발견 시 빨간색 강조 + 팝 효과
  [ ] 아웃트로: "남은 수들이 모두 소수입니다"
총 영상 길이: 60~90초 목표
```

### Step 2-C: 렌더링
```bash
hyperframes render \
  --input 90_video/unit01_소인수분해/sieve-scene.html \
  --output 90_video/unit01_소인수분해/sieve.mp4 \
  --fps 30 \
  --duration 90
```

---

## Phase 3 (선택): Motion Canvas 수학 애니메이션

이 단계는 Phase 1, 2가 검증된 후에 결정.

```
후보 영상:
  - "소인수분해란?" — 60을 팩터트리로 쪼개는 과정
  - "GCD vs LCM" — 두 수를 소인수분해해서 비교하는 과정
  - "에라토스테네스의 체 전체" — 100까지, 3분짜리
```

---

## 파일 명명 규칙

```
80_tools/unit{NN}_{단원명}/     # 인터랙티브 웹 도구
90_video/unit{NN}_{단원명}/     # 영상 관련 파일
  sieve-scene.html              # HyperFrames composition
  sieve.mp4                     # 렌더링 결과
```

---

## 즉시 시작 추천 순서

1. `shared.css` 먼저 (빠름, 나머지 파일의 토대)
2. `sieve.html` (가장 임팩트 있는 결과물, 딸이 바로 써볼 수 있음)
3. `index.html` (스토리 텍스트 정리)
4. `concepts.html`
5. `problems.html`
6. HyperFrames 설치 → `sieve-scene.html` → `sieve.mp4`
