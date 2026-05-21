# mathtelling-design-system

> 수학·과목 학습 앱 + 영상 채널을 위한 공통 디자인 토큰 & 컴포넌트

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 한 줄

"양피지" 톤 다크 팔레트 기반. Pretendard + JetBrains Mono. 과목별 테마. 절제된 모션.

---

## 구조

```
tokens/
  colors.css       글로벌 팔레트 (양피지 + 과목 테마 + 시대 팔레트)
  typography.css   Pretendard + JetBrains Mono + 타입 스케일
  motion.css       3단계 속도 + ease 토큰
  spacing.css      8px 그리드 + 레이아웃 변수

subjects/
  math.css         수학 테마
  ...

components/
  card.css
  walkthrough.css
  problem.css
  ...

dist/
  all.css          단일 파일 (위 모두 @import)
```

---

## 빠른 사용

```html
<link rel="stylesheet" href="../../mathtelling-design-system/dist/all.css">
<!-- 과목 테마 추가 -->
<link rel="stylesheet" href="../../mathtelling-design-system/subjects/math.css">
```

또는 body에 `data-subject="math"` / `data-theme="light"` 속성 부여.

---

## 원칙

| 원칙 | 규칙 |
|---|---|
| 배경 | 어두운 양피지 (`#1F1814`) 기본. `[data-theme="light"]` 로 전환. |
| 폰트 | Pretendard (한글) + JetBrains Mono (영문/코드) **2종만** |
| 모션 | ease-in-out 기본. 0.3s / 0.6s / 1.0s **3단계만** |
| 수식 | `.math-block` / `.math-inline` 클래스 + KaTeX 렌더 |
| 색 강조 | 폰트 추가 없음. 굵기·색·크기로만. |

---

## 연관 프로젝트

- [`mathtelling`](../mathtelling) — 학습 앱 + 영상 채널 monorepo

---

## 변경 이력

- v0.1 (2026-05-19): tokens 4종 + subjects/math + dist/all.css
