# P06 — MathTelling 수학 앱 (교과서 챕터별 구조 + 자체 리뷰·업데이트)

## 발견 맥락

- **출처**: `30_MiddleSchool/260426_MathTelling_Idea/` — 중1 수학 13개 단원
- **5/12 update (commit 71d985a)**: 구조 개편 — `app/` 폴더 폐기, unit root로 이동, `problems/` 신규
- Q05 응답: "30_MS 수학 앱 (교과서 챕터별 짜임새 + 앱 리뷰·업데이트 과정) 참조 필수"

## 핵심 구조 (5/12 이후)

### 단원 폴더 구조
```
50_units/<NN_단원명>/
├── index.html                   ← 단원 진입 (메인 카드)
├── story.html                   ← 인물 서사 (축 B)
├── concepts.html                ← 개념 정리 (축 A)
├── story/                       ← 인물 서사 텍스트 .md (소스)
├── feedback/                    ← 딸의 글·반응 (수정 금지)
├── video/                       ← 영상 (스크립트 + mp4)
└── problems/
    ├── basic_app.html           ← 단원 전체 기본 (8~10문제, 축 D)
    ├── type_01_app.html ~ 07    ← 유형별 연습 (L×3 + M×3 + H×3)
    ├── deep_*_app.html          ← 유형별 깊이 탐구 (M+ 난이도)
    ├── walk_*_app.html          ← 추가 walk-through (5/12 신규)
    ├── types.html / types.md    ← 유형 목록
    └── Q1_source.md             ← 출처 정리
```

### 4축 매핑
- **A. 개념**: `concepts.html` + `40_BaseDocs/NN_단원명/`
- **B. 흥미·이야기**: `story.html` + `story/` + `video/`
- **C. 수학 언어**: `40_BaseDocs/00_literacy/L1~L7/` (단원 횡단)
- **D. 문제**: `problems/` 전체

### 13단원 × 39 메인 앱 + ~13×10 problem 앱
- 13단원 × 3 메인 (index/story/concepts) = 39
- 13단원 × 평균 10 problem 앱 = ~130
- 총 170개 앱 + supporting .md / .svg

## 재사용 단위

### Phase 파이프라인 (단원 1개 제작)
- Phase 0: `/unit-plan` → 디렉토리
- Phase 1: 개념 (축 A) → `/concept-review` + `/ncc_audit_concept`
- Phase 2: 이야기 (축 B) → `/story-write` + `/ncc_audit_story`
- Phase 3: 수학 언어 (축 C, 단원 횡단) → `/math-figure`
- Phase 4: 앱 (축 A+B 통합) → `index.html`, `story.html`, `concepts.html` 제작 + `/ncc_audit_app`
- Phase 5-a: 기본문제 → `basic_app.html` (`/ncc_audit_math` + `/ncc_audit_app`)
- Phase 5-b: 유형 목록 → `types.md` (`/ncc_audit_problem`)
- Phase 5-c: 유형별 연습 → `type_NN_app.html` (3/3/3) (`/math-practice` + audit 2종)
- Phase 5-d: 유형별 깊이 → `deep_*_app.html` (`type-explorer` + audit 2종)
- Phase 5-e (5/12 신규?): walk-through → `walk_*_app.html`

### 자체 리뷰·업데이트 사이클 ⭐
- 5/12 commit 메시지: "**앱 자체를 리뷰하고 업데이트 하는 과정**"
- 단원 만든 후 → 일정 후 → 다시 열어 검토 → 개선
- audit skill 5종 (`/ncc_audit_*`)이 이 사이클의 핵심
- → P06이 다른 패턴(P03·P04)에 주는 시사: **만들고 끝이 아니라, 리뷰·업데이트가 패턴의 일부**

## 일반화 가능 영역

### 수학 → 비수학 확장 시 차용 포인트
- **단원 = 챕터**: 교과서 챕터 단위로 묶기 (사회 V단원, 한국사 정도전 단원 등)
- **3장 메인 + 문제 폴더**: index/story/concepts + 연습 폴더 분리
- **Phase 파이프라인**: 0→1→2→4→5 흐름은 다른 영역도 적용 가능
- **audit skill**: 영역별 ncc_audit_* 시리즈로 확장 가능

### 적용 가능 자식 프로젝트
- HighSchool 2604 (현재): 시험·수행평가 단발 위주 → 단원 학습용 앱은 미정
- 향후 HighSchool 단원 학습 앱이 필요해지면 → P06 차용

## 검증 사례

- `50_units/01_소인수분해/` ~ `13_확률과통계/` (13개 단원)
- 5/12 commit 71d985a: 구조 개편 완료
- 39 메인 앱 + 130 problem 앱 (대략)

## 다음 진화

### Skill 후보: `/se_unit_app <단원번호> <Phase>` (B08)
- 50_BLUEPRINTS.md 참조
- `unit-orchestrator` agent가 이 skill을 phase별 호출하는 형태

### 다른 자식 프로젝트로 전파
- HighSchool에서 비슷한 "단원 학습 앱"이 필요해지면 차용
- 사회 V단원 자체를 단원 앱으로 만들면 → 메가시티 step과 별개의 또다른 layer

### 관련 OPEN QUESTION
- Q07 (인물 sub-skill) — 이 패턴의 story.html과 P04 (인물 3앱) 공통 부분
