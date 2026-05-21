<!-- 260522_plan_math_chapter.md -->

# Plan — 수학 챕터 정리 + 인물↔영상 Link 구조

> 출발점. 다음 라운드에서 넓혀나갈 이슈 메모.
> 작성: 2026-05-22

---

## 1. 비전 한 줄

수학 챕터(math1) 인물 페이지에서 → 영상(story 페이지)로 자연스럽게 흐르도록 link 구조 표준화.
예) `mid1/math1/01_prime-factorization/index.html` ↔ `mid1/story/unit01/index.html`

---

## 2. 즉시 정리 안건 (마이그 잔재)

### 2.1 `40_grades/middle/math1/unit-01/` 삭제
- mathtelling apps에서 카피된 시드. 내용은 `basic.html`, `concepts.html`, `index.html`, `story.html`, `types.html` 뿐.
- SSOT는 `01_소인수분해/` (50_units 계열, problems/ 30+ 파일).
- **합의 시 삭제.** 정보 손실 없음.

### 2.2 `40_grades/middle/math1/_index_v_mathtelling.html` 삭제
- `index.html`과 byte 동일 (10455). 충돌 회피용 임시 사본일 뿐.
- **합의 시 삭제.**

### 2.3 `40_grades/middle/math1/index.html` 위치 검토
- math1 root에 index.html이 있음 — math1 홈 페이지 역할
- mathtelling apps 시드인지, 50_units 시드인지 출처 확인 + 13단원 hub 역할로 재정비할지 결정

---

## 3. 다음 라운드 토론 이슈

### 3.1 인물 ↔ 영상 link 구조 표준
- 13단원 각 인물 페이지에 영상 진입 버튼 (단원 hub `index.html` or `story.html`에서?)
- 영상에서 다시 챕터로 돌아오는 link
- 인물 메타 (`30_content/units/NN/meta.json`의 `person`, `era-palette`) → 양쪽 페이지 공유 어휘

### 3.2 단원 페이지 표준 재정의
- `40_grades/middle/math1/NN_*/` 안의 표준 파일 목록:
  - `index.html` — 단원 hub (축 A+B 통합)
  - `story.html` — 인물 서사 인터랙티브 (영상 link 위치)
  - `concepts.html` — 개념 탐구
  - `problems/` — 4-mode (basic / type_NN / deep_* / walk_*)
- 13단원 일관성 audit 필요

### 3.3 배포 매핑
- 현재 GH Pages: `jwj-nick.github.io/mid1/math1/01_prime-factorization/` 와 `jwj-nick.github.io/mid1/story/unit01/`
- 새 repo 구조: `40_grades/middle/math1/01_소인수분해/` (한글) ↔ `01_prime-factorization/` (영문 URL)
- 폴더명 vs URL slug 매핑 정책 (한글 유지 vs 영문 slug 도입) — 결정 필요
- `60_deploy/middle-school/` 빌드 출력 구조 정의

### 3.4 13단원 인물 페이지 일괄 점검
- Phase 2 (이야기 축 B) 완성도 단원별 상태 파악
- 영상 hookup 추가 필요한 단원 목록화

---

## 4. 연관 문서

- `CLAUDE.md` 단원 파이프라인 섹션
- `30_content/units/NN/meta.json` — 인물·시그니처 메타
- `30_content/people/` — 인물 사실
- `260522_plan_video_flow.md` — 영상 flow plan (배포 hookup 양면)
- `00_project_hub/40_context/external_repos.md` — 옛 mid1 배포 repo 상황
