---
name: se_math_figure
description: 수학 그래프를 네이티브 HTML로 렌더링한다. 정적 SVG 또는 JSXGraph 인터랙티브 보드를 생성. 호출 예시 — "/se_math_figure Q3", "/se_math_figure unit04 좌표평면".
---

# se_math_figure — 수학 그래프 네이티브 렌더링 스킬

## 언제 사용하나

`/se_math_figure Q3` 처럼 호출. 오답노트 또는 개념 탐구 앱의 그래프를 Native HTML로 생성.

- **정적 그림** (좌표, 점, 선만 필요): Pure SVG
- **탐구형** (슬라이더로 파라미터 변화 관찰): JSXGraph 인터랙티브 보드

## APP_PRINCIPLES 적용 규칙

| 페이지 | 그림 형식 | 금지 사항 |
|---|---|---|
| **page-0 (문제)** | **정적 SVG** | JSXGraph, 슬라이더, 좌표 수치 눈금 |
| **page-1~N (풀이)** | **JSXGraph (lazy init)** | 해당 단계 이전에 도출되지 않은 정보 |
| **개념 탐구 앱** | **JSXGraph** | 제한 없음 (탐구 목적) |

## 사용 라이브러리

**JSXGraph**
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jsxgraph/1.11.1/jsxgraph.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jsxgraph/1.11.1/jsxgraphcore.min.js"></script>
```

## 절차

1. 문제/개념 파일 읽기
2. 판단: 정적 SVG vs JSXGraph
3. HTML 파일에 삽입/생성
4. 색상: 함수 `#4361EE`, 포인트 `#22c55e`/`#ef4444`

## JSXGraph lazy init 패턴
```javascript
let _boardInit = false;
function goTo(n) {
  if (n === 1 && !_boardInit) { initBoard(); _boardInit = true; }
}
```

## 중1 특화 — 자주 쓰는 유형

| 단원 | 유형 | 구현 |
|---|---|---|
| 좌표와 그래프 | 점 찍기, 사분면 | SVG + 클릭 인터랙션 |
| 정비례·반비례 | y=ax, y=a/x 그래프 | JSXGraph 슬라이더(a) |
| 기본도형 | 각, 수직, 평행 | SVG 정적 |
| 원과 부채꼴 | 호, 부채꼴 넓이 | JSXGraph 슬라이더(각도) |
| 입체도형 | 전개도, 회전체 | SVG 또는 CSS 3D |
