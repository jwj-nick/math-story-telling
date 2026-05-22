<!-- UNIT_PAGE_STANDARD.md -->

# UNIT_PAGE_STANDARD — 단원 페이지 4파일 표준 + 인물·영상 UI

> SSOT for `40_grades/<grade>/<subject>/<NN_단원명>/` 페이지 구조.
> 초안: 2026-05-23. 기준: math1 13단원 일관성 audit + Round 2 합의 (chatlog `260522_math_chapter_standard.md`).
> 관련: `APP_PRINCIPLES.md` (HTML 앱 일반 디자인), `STORY_VIDEO_v1_5.md` (영상 v1.5).

---

## 0. 한 줄 요약

> **모든 단원은 같은 4 root file + 2 dir 구조.** 인물·시그니처·영상 link는 `30_content/units/NN/meta.json` 의 `persons[]` 에서 자동 채움.

---

## 1. 단원 폴더 표준 (`40_grades/middle/math1/NN_<한글명>/`)

```
NN_<한글명>/
├── index.html       ← 단원 hub (4축 진입 + 인물 카드)
├── story.html       ← 인물 서사 인터랙티브 (영상 link 위치)
├── concepts.html    ← 개념 탐구 인터랙티브
├── problems/        ← 문제 (축 D)
│   ├── basic_app.html
│   ├── type_01~07_app.html
│   ├── deep_*_app.html × 3
│   ├── walk_NN_HN.html × ~18-21
│   ├── types.html · types.md
│   └── Q{N}_source.md
├── story/           ← 인물 서사 텍스트 .md (작업용 소스)
└── video/           ← 영상 작업 임시 폴더 (최종 영상은 50_channel/)
```

규칙:
- **폴더명 한글 유지** (작업자 가독성). URL은 빌드 시 `meta.slug-en` 로 변환.
- 4 root file은 모두 존재. 미완성도 placeholder로 둠 (404 방지).
- `problems/` 의 7유형 표준은 R2.D meta.json `problem-types[]` 와 1:1 매칭.

---

## 2. `index.html` — 단원 hub 표준

목적: 단원의 **첫 화면**. 4축 모두에 닿는 진입점.

### 2.1 섹션 구조 (위 → 아래)

```
[Topbar]   메뉴 (← math1 hub / → 다른 단원)
[Hero]     단원 번호·한글명·영문명·핵심 한 줄
[Persons]  인물 카드 (persons[] 배열에서 자동) — role primary 먼저
[4축 진입] story / concepts / problems × 3 카드
[Footer]   meta (slug-en, grade, last-updated)
```

### 2.2 인물 카드 한 개의 모양 (Persons 섹션)

```
┌───────────────────────────────────┐
│ [signature-color 배경]            │
│  ┌─────┐                          │
│  │ 🪨  │  에라토스테네스          │  ← signature-object (이모지/SVG)
│  └─────┘  Eratosthenes · BC 276~  │
│                                   │
│  "막대기 하나로 지구를 잰 사람"      │  ← story-hook
│                                   │
│  [🎬 이야기 영상 보기]              │  ← 영상 link (있을 때)
│  [📖 사실 더 알기]                  │  ← 30_content/people/<ref>.md
└───────────────────────────────────┘
```

- `signature-color`: 카드 배경 또는 좌측 띠
- `signature-object`: 이모지(빠른 prototyping) 또는 SVG (정식)
- `role` 별 시각 차이:
  - `primary`: 큰 카드, 영상 버튼 강조
  - `secondary`: 중간 카드, 영상 버튼 표시
  - `cameo` (옵션): 작은 카드, 영상 버튼 없을 수도

### 2.3 4축 진입 카드 3개 (story·concepts·problems)

각 카드: 아이콘 + 축 이름 + 한 줄 설명 + 진입 버튼.

| 카드 | 진입 |
|---|---|
| 📖 이야기 (축 B) | `story.html` |
| 💡 개념 (축 A) | `concepts.html` |
| 📝 문제 (축 D) | `problems/basic_app.html` (또는 `problems/types.html` 선택지) |

축 C (수학 언어)는 단원 종속이 아니므로 hub에 직접 두지 않음. 필요 시 `concepts.html` 안에서 link.

---

## 3. `story.html` — 인물 서사 인터랙티브 표준

목적: **축 B (흥미)** 의 핵심 화면. 영상 link의 1차 자리.

### 3.1 섹션 구조

```
[Topbar]
[Cover]      한 줄 메시지 (인물 인용)
[Persons]    인물 카드 N개 (index.html 보다 큼·깊음)
   ↳ 각 카드: 사실 + 일화 + 영상 버튼 + 글쓰기 미션
[Reflection] 빈칸 슬롯 (딸이 채울 자리 — 원칙 5)
[Next]       단원 hub로 / 다음 단원으로
```

### 3.2 영상 카드 자리 (인물 카드 내부)

각 인물 카드의 **"🎬 영상" 버튼**은 다음 우선순위로 link:

1. **deploy URL** (배포 시): `<channel-base>/people/<ref>/<episode-key>/`
2. **dev URL** (로컬·미배포): `50_channel/people/<ref>/<episode-key>/index_v1_5.html`
3. **fallback** (영상 미존재): 버튼 비활성 + "영상 준비 중" tooltip

영상 ref는 `meta.persons[].videos[]` 에서 가져옴.

### 3.3 글쓰기 미션 표시

각 인물 사실 md 의 "글쓰기 미션 후보" 섹션을 카드 하단에 list. 딸이 골라 .private/feedback/ 에 자유롭게 적음.

---

## 4. `concepts.html` — 개념 탐구 표준

목적: **축 A (이해)**. 단원 핵심 개념의 인터랙티브 시각화.

### 4.1 섹션 구조

```
[Topbar]
[Concept Map]   key-concepts 한 줄씩 + 관련 그림/위젯 mini-card
[Interactive]   JSXGraph / SVG / KaTeX 활용 위젯들 (개념별 1-2개)
[Examples]      개념 적용 예시 (문제 아님, 직관)
[→ problems]    "이제 문제로 가기" 진입
```

`key-concepts` 는 `meta.key-concepts[]` 에서 자동 채움 가능.

축 C 수학 언어 자료 (`30_content/literacy/`) 와의 cross-link은 개념 별 footer 또는 hover.

---

## 5. `problems/` — 문제 표준

목적: **축 D (실전력)**. mid_eun에서 검증된 4-mode 구조.

### 5.1 표준 파일 목록

```
basic_app.html                    Phase 5-a: 단원 전체 개념 커버 기본 8~10문항
types.md / types.html             Phase 5-b: 7유형 목록 (meta.problem-types[] 와 1:1)
Q{N}_source.md                    출제 원본·시험지 캡쳐 (작업용)
type_01_app.html ~ type_07_app.html  Phase 5-c: 각 유형 L×3 + M×3 + H×3 = 9문항
deep_<key>_app.html × 3           Phase 5-d: M+ 난이도 유형 깊이 탐구
walk_NN_HN.html × ~18-21          H 난이도 step-by-step 풀이
```

### 5.2 진입 패턴

- 기본 학습: basic_app → types → 각 type_NN → 약한 유형의 deep
- 시험 대비: types에서 약한 유형 찾기 → type_NN → walk

`problems/types.html` 이 problems 폴더의 **목차 페이지** 역할.

---

## 6. 영상 주소트리 — 이중 트리 (Round 2.B 합의)

### 6.1 원본 (재사용 자산)

```
50_channel/people/<person>/<episode-key>/
├── storyboard_v1_5.md
├── image_prompts.md
├── narration_v1_5.{txt,xml,mp3}
├── poster_v1_5.jpg
├── final_v1_5.mp4
├── raw_v1_5.mp4
├── index_v1_5.html         ← dev preview
└── config_v1_5.json
```

여기에 영상의 **유일한 원본**이 존재. 단원에 종속되지 않음 — 인물의 이야기 단위.

### 6.2 view (시즌 큐레이션)

```
50_channel/seasons/season-<N>-<theme>/unit-<NN>/
└── (people/<ref>/<episode>/ 의 ref or symlink or build copy)
```

배포 시 사용. 한 episode가 여러 시즌·여러 단원에 나타날 수 있음.

### 6.3 단원 페이지에서 link

`story.html` 의 영상 버튼은 우선순위대로 시도:
1. `seasons/season-<N>/unit-<NN>/<episode>/` (배포 view) — 존재 시
2. `people/<ref>/<episode>/` (원본 dev preview) — fallback
3. 없으면 비활성

이 결정 트리는 build 스크립트(`E. 배포 매핑`)에서 자동화.

---

## 7. design-system 융합 규칙

### 7.1 base 토큰 + subject

모든 페이지 head:
```html
<link rel="stylesheet" href="<rel>/20_packages/design-system/dist/all.css">
<link rel="stylesheet" href="<rel>/20_packages/design-system/subjects/math.css">
```

`<rel>` 은 단원 페이지에서 `../../../../20_packages/...` (4 레벨 위), math1 hub에서 `../../../20_packages/...` (3 레벨).

### 7.2 시그니처 컬러 적용

인물 카드는 **CSS variable** 로 시그니처 컬러 주입:
```html
<article class="person-card" style="--mt-person-color: #D4A843">…</article>
```

design-system의 토큰과 충돌 시:
- 카드 자체 색은 `--mt-person-color` 우선
- 텍스트·여백·radius·shadow는 design-system 토큰

### 7.3 era-palette 매핑

`era-palette` 값 → 카드 보조색·배경 그라데이션:

| era-palette | 보조색 후보 |
|---|---|
| `era-ancient` | 베이지·테라코타 (parchment 느낌) |
| `era-medieval` | 짙은 청록·황금 (이슬람 황금기) |
| `era-modern` | 파스텔 청록·진녹·짙은 청 (르네상스·계몽기) |
| `era-contemporary` | 컬러풀 (빅토리아·산업혁명 이후) |

(정식 토큰은 향후 `20_packages/design-system/subjects/people.css` 신설 시 도입.)

---

## 8. 빈칸·미완성 원칙 (CLAUDE.md 5번 절대 원칙)

모든 페이지에 **딸이 채울 자리**:
- `story.html` Reflection 섹션: 자유 메모 입력 (LocalStorage 저장 또는 단순 안내)
- `concepts.html` Examples: 빈 예시 1개 ("내 예시" 슬롯)
- `problems/` Q{N}_source.md: 자기가 만든 문제 추가 칸

자동화하지 말 것. 빈칸이 보이는 게 중요.

---

## 9. 빌드 후 URL 변환 (E 배포 매핑 단계)

빌드 스크립트가 다음 변환 수행:
```
40_grades/middle/math1/01_소인수분해/  →  /math1/01_prime-factorization/
40_grades/middle/math1/02_정수와유리수/ →  /math1/02_integers-and-rational-numbers/
...
```

폴더명 `NN_<한글명>` → URL `NN_<slug-en>`. `NN_` prefix 유지하여 정렬 일관성.
`meta.json` 의 `slug-en` 이 SSOT.

---

## 10. 일관성 audit 도구

신규/수정 단원 페이지는 `/se_ncc_audit_app` 으로 점검:
- 4 root file 존재 여부
- meta.json schema v2 준수 (slug-en, persons[])
- 인물 카드 signature·영상 link 정확성
- design-system 경로 정확성
- 빈칸 슬롯 존재 여부

향후 `se_ncc_audit_unit_page` 신설 검토 (B 마무리 또는 후속 작업).

---

## 11. 변경 이력

- v0.1 (2026-05-23): 초안. math1 13단원 일관성 audit 기반. Round 2 (chatlog `260522_math_chapter_standard.md`) 합의 반영.
