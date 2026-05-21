# 02 — 정적·인터랙티브 웹 설계 가이드

> Vanilla HTML/CSS/JS 기준. 파일 1개 = 목적 1개, 500줄 이내.

---

## unit01 파일 구조 (제안)

```
80_tools/
└── unit01_소인수분해/
    ├── index.html        # 스토리 허브 + 네비게이션       < 200줄
    ├── sieve.html        # 소수의 체 인터랙티브            < 400줄
    ├── concepts.html     # 개념 카드 + 빈칸 채우기         < 400줄
    ├── problems.html     # 문제 세트 (힌트 토글)           < 400줄
    ├── shared.css        # 공통 스타일 (색상, 타이포)      < 200줄
    └── sieve-logic.js    # 체 알고리즘 (sieve.html에서 import) < 150줄
```

총 6개 파일, 각자 목적 명확, 500줄 이내.

---

## 파일별 설계

### index.html — 허브
```
역할: 단원 1 랜딩 페이지. 이야기 텍스트 + 4개 섹션 링크.
구조:
  - 헤더 (단원 제목, 인물 배지)
  - 이야기 텍스트 (unit01.md의 §1 내용, HTML로 예쁘게)
  - 섹션 카드 4개 → 각각 sieve / concepts / problems / [글쓰기] 링크
기술: 순수 HTML + CSS, JS 없음
```

### sieve.html — 소수의 체
```
역할: 에라토스테네스의 체를 직접 조작하는 애니메이션
UX 흐름:
  1. 1~50 숫자 그리드 표시
  2. "시작" 버튼 → 2의 배수부터 순서대로 지워짐 (딜레이 있음)
  3. 각 단계마다 "2의 배수를 지웁니다" 텍스트 표시
  4. 끝나면 소수만 강조 표시
  5. "직접 해보기" 모드: 사용자가 숫자 클릭 → 배수 지우기
기술: HTML + CSS + sieve-logic.js
```

### concepts.html — 개념 카드
```
역할: 소수·합성수·소인수분해·GCD·LCM을 카드로 정리
UX 흐름:
  - 개념 카드 (앞면: 이름, 뒷면: 설명) — 클릭으로 뒤집기
  - 소인수분해 단계 시각화 (숫자 → 팩터트리 애니메이션)
  - 빈칸 채우기 (단원 3 개념 정리 섹션을 인터랙티브하게)
기술: HTML + CSS + Vanilla JS (카드 flip은 CSS transform만으로 가능)
```

### problems.html — 문제 세트
```
역할: unit01.md §4의 12문제를 인터랙티브하게
UX 흐름:
  - 문제 나열
  - "힌트 보기" 버튼 토글
  - 직접 답 입력 → "확인" 버튼 → 정답/오답 피드백
  - 도전 문제 11번: 직접 체 그리기 인터랙티브
기술: HTML + CSS + Vanilla JS
```

---

## 공통 스타일 시스템 (shared.css)

```css
/* 색상 팔레트 — unit01 테마 */
--color-story:    #fffbf0;  /* 이야기 배경 (황금빛) */
--color-concept:  #f0f7ff;  /* 개념 배경 (파랑) */
--color-problem:  #f0fdf5;  /* 문제 배경 (초록) */
--color-prime:    #ef4444;  /* 소수 강조 (빨강) */
--color-composite:#9ca3af;  /* 합성수 (회색) */
--color-text:     #1c1c1c;
--color-muted:    #6b7280;

/* 타이포 */
--font-body: system-ui, -apple-system, 'Apple SD Gothic Neo', sans-serif;
--font-size-base: 16px;
--line-height-story: 1.8;   /* 이야기는 넓게 */
--line-height-math:  1.5;   /* 수식은 좁게 */

/* 레이아웃 */
--max-width: 680px;
--section-gap: 28px;
```

---

## 소수의 체 애니메이션 설계 (sieve-logic.js)

```javascript
// sieve-logic.js
// 소수의 체 알고리즘 + 단계별 이벤트 emit

export function buildSieveSteps(limit) {
  // returns: [{prime: 2, crossed: [4,6,8,...]}, {prime: 3, ...}, ...]
  const arr = Array.from({length: limit + 1}, (_, i) => i);
  const steps = [];
  for (let p = 2; p * p <= limit; p++) {
    if (!arr[p]) continue;
    const crossed = [];
    for (let m = p * p; m <= limit; m += p) {
      if (arr[m]) { arr[m] = 0; crossed.push(m); }
    }
    if (crossed.length) steps.push({ prime: p, crossed });
  }
  return steps;
}
// 이 함수를 sieve.html에서 import해서 쓴다.
// step별로 setTimeout으로 딜레이를 주면 애니메이션 효과.
```

`sieve.html`에서:
```html
<script type="module">
  import { buildSieveSteps } from './sieve-logic.js';
  // ... 애니메이션 루프
</script>
```

`type="module"` 사용 → `file://` 로컬 실행 시 CORS 에러 가능.  
→ 해결: VS Code Live Server 또는 `python -m http.server 8080`.

---

## 네비게이션 일관성

모든 파일 상단에 공통 nav:
```html
<nav class="unit-nav">
  <a href="index.html">📖 이야기</a>
  <a href="sieve.html">🔢 소수의 체</a>
  <a href="concepts.html">📝 개념</a>
  <a href="problems.html">🔑 문제</a>
</nav>
```

---

## type="module" 로컬 실행 문제 해결 옵션

| 방법 | 복잡도 | 비고 |
|---|---|---|
| `python -m http.server 8080` | ★☆☆ | Python 있으면 바로 |
| VS Code Live Server 확장 | ★☆☆ | 한 번만 설치, 이후 편함 |
| JS를 같은 파일에 인라인 | ★☆☆ | module 불필요, 단순 |
| 파일을 하나로 합치기 | ★☆☆ | sieve-logic을 sieve.html에 포함 |

**권장**: sieve-logic.js를 sieve.html 안에 인라인으로 `<script>` 태그에 넣기.  
파일이 500줄 이내라면 굳이 분리 불필요.
