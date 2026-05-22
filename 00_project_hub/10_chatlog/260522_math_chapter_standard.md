<!-- 260522_math_chapter_standard.md -->

# 수학 챕터 표준 정의 — math1 13단원 통일·인물↔영상 link 구조

> 작업 B (`00_project_hub/20_plan/260522_plan_math_chapter.md`) 라운드 진행.
> 시작: 2026-05-22.
> 선행: 마이그 잔재 정리 commit `13b0159` (math1/unit-01/, _index_v_mathtelling.html 삭제).

---

## Round 0 — NCC 진단 + 결정 요청

### 0.1 13단원 현재 상태 (audit)

#### 구조 일관성: 매우 좋음
13단원 전부 동일 패턴:
- root: `index.html`, `story.html`, `concepts.html`
- `story/` 디렉토리 (인물 서사 텍스트 md)
- `video/` 디렉토리 (영상 source)
- `problems/` (30~33 파일)

#### problems 통일 패턴 (모든 단원)
```
basic_app.html              ← Phase 5-a 기본문제
Q{N}_source.md              ← 출제 원본
types.html / types.md       ← Phase 5-b 유형 목록
type_01~07_app.html         ← Phase 5-c 유형별 (총 7개)
deep_*_app.html  × 3        ← Phase 5-d 유형 깊이 탐구 (단원마다 다른 3개)
walk_NN_HN.html × ~18-21    ← H 난이도 step-by-step 풀이
```

⚠️ 미세 차이: `01_소인수분해`는 `walk_01`이 없고 `walk_02~07` 시작 — 의도? 누락?

#### 30_content 공백 (B의 핵심 작업)

| 자원 | 현재 | 필요 |
|---|---|---|
| `30_content/units/NN/meta.json` | 01만 | **02~13 신규 작성** |
| `30_content/people/` | 5인 (al-khwarizmi, descartes, eratosthenes, euclid, nightingale) | **인물 배정 + 누락 인물 8~10인 추가** |

#### CLAUDE.md 명시 Season 1 인물 매핑
| 단원 | 인물 | people/ 존재? |
|---|---|---|
| 1 소인수분해 | 에라토스테네스 | ✓ eratosthenes |
| 2 정수와유리수 | 브라마굽타 | ✗ 누락 |
| 3 문자와식 | 알콰리즈미 | ✓ al-khwarizmi |
| 4 일차방정식 | 디오판토스 | ✗ 누락 |
| 5~6 좌표·정비례 | 데카르트 | ✓ descartes |
| 7~13 | **미배정** | (euclid, nightingale은 있으나 어느 단원?) |

### 0.2 math1/index.html 재정비 필요
- 출처: mathtelling/apps/math1/index.html (mathtelling 시드)
- 옛 경로 참조: `../../mathtelling-design-system/dist/all.css` ← 새 repo에 안 맞음
- 13단원 hub 역할로 재정비 + design-system 경로 갱신 필요

### 0.3 결정 요청 (Round 1)

> Nick은 `(Nick)` 태그로 같은 파일에 답변. 한 번에 다 안 정해도 됨 — 라운드 거듭.

#### Q1. 인물 배정 (7~13단원)
권장안 (시대순 흐름 유지):
| 단원 | 개념 | 권장 인물 | 시대 |
|---|---|---|---|
| 7 기본도형 | 유클리드 | euclid ✓ | 기원전 3세기 |
| 8 작도와합동 | 유클리드 (계속) 또는 가우스? | — | — |
| 9 다각형 | 피타고라스 또는 케플러? | — | — |
| 10 원과부채꼴 | 아르키메데스 | — | 기원전 3세기 |
| 11 다면체와회전체 | 카발리에리 또는 케플러? | — | 17세기 |
| 12 입체 겉넓이·부피 | 아르키메데스 (계속) | — | — |
| 13 자료의정리와해석 | 나이팅게일 | nightingale ✓ | 19세기 |

→ Nick의 선호·아이디어? (Nick) 한 단원에 두명의 이야기를 준비해도 좋음. 한 인물의 서로 다른 얘기가 여러 단원에 걸쳐도 좋음. 최대한 풍부하게 컨텐츠 갖춰두면 좋음.

#### Q2. 인물 ↔ 영상 link 구조 (Nick 비전 구체화)
Nick 메시지: "인물이 `mid1/story/unit01/index.html` 이런식으로 연결되어야 함"

권장 구조 (영상 = `50_channel/season-1-ancient/unit-NN/final_v1_5.mp4`):
```
[단원 hub]                     [영상 페이지]
40_grades/.../NN_*/index.html   60_deploy/channel/unit-NN/index.html
   ↓ 인물 카드                       (또는 직접 mp4)
   "🎬 이야기 영상 보기" 버튼
   ↓
   영상 페이지 (poster + mp4 + 자막)
   ↓ "단원으로 돌아가기"
```

또는 직접 `index.html`에 영상 embed?

→ 어느 게 Nick 의도? (Nick) 갖춰진 인물 자료(영상)는 나중에 다른데도 사용할 수 있다. 원본만 어디 잘 저장되어있으면 됨. 수학앱에서는 영상들있는 주소트리와 연결되면됨. 아마 당신 권장 구조가 내 의도와 맞는거같음 

#### Q3. 폴더명 vs URL slug
현 폴더: `01_소인수분해/` (한글). 옛 GH Pages URL: `mid1/math1/01_prime-factorization/` (영문 slug).

권장:
- **(a)** 폴더 한글 유지 + `30_content/units/NN/meta.json`에 `slug-en` 필드 추가 → 빌드시 URL 변환
- (b) 폴더를 영문 rename + 한글 title은 meta에만
- (c) 둘 다 유지 (한글 폴더 + symlink/build redirect)

→ (a) 권장 (폴더는 작업자 가독성, URL은 배포용 분리). Nick 선호? (Nick) browser 에 적히는 웹 주소는 반드시 영어로. 상위의 하이퍼링크(카드)에 한글로 표기가 있어서 보기 쉬우면 충분 

#### Q4. math1/index.html (hub) 처리
- 지금 재정비할지 vs B 마무리 단계에서 한꺼번에?
- 권장: B 마무리 단계 — 모든 단원 메타·인물 정해진 후 hub에 반영
(Nick) NCC 권장 존중함.

#### Q5. walk_01 누락 (01단원만)
- 누락 vs 의도? 검토 필요
- 권장: Round 2에서 빠르게 확인 (다른 단원과 type_01의 난이도 분포 비교)
(Nick) NCC 권장 따름.

### 0.4 B 작업 산출물 (예상)

| # | 산출물 | 위치 |
|---|---|---|
| 1 | 인물 배정 표 (13단원) | 이 chatlog Round N에 합의 후 CLAUDE.md 반영 |
| 2 | `30_content/units/NN/meta.json` × 12 신규 | `30_content/units/` |
| 3 | `30_content/people/` 누락 인물 md × 8~10 | `30_content/people/` |
| 4 | 단원 페이지 표준 명세 | `10_system/10_principles/UNIT_PAGE_STANDARD.md` (신규) |
| 5 | 인물↔영상 link UI 패턴 | UNIT_PAGE_STANDARD.md에 통합 또는 별 파일 |
| 6 | URL slug 정책 + slug-en 필드 | 위 #2 meta.json에 통합 |
| 7 | math1/index.html 재정비 | (B 마무리) |

### 0.5 다음 라운드

Nick이 Q1~Q5 답변 → Round 1 (NCC가 답변 정리·추가 질문) → Round 2 (산출물 생성 시작) …

---

## Round 1 — Nick 답변 정리 + 데이터 모델 영향 + 다음 결정

### 1.1 Nick 답변 한 줄 요약

| Q | Nick 답 | 영향 |
|---|---|---|
| Q1 | **단원↔인물 N:M 가능. 최대한 풍부하게.** | 데이터 모델 single→array (큰 변경) |
| Q2 | **영상은 재사용 가능 원본 자산. 수학앱은 영상 주소트리에 link만.** + NCC 권장 인물 카드+버튼 구조 채택 | 영상 디렉토리 구조 재설계 필요 |
| Q3 | **URL은 반드시 영문 slug. 상위 카드는 한글 표기 OK.** | meta.json `slug-en` 필수 + 빌드 시 한글 폴더 → 영문 URL 변환 |
| Q4 | NCC 권장 (B 마무리 hub 재정비) | — |
| Q5 | NCC 권장 (Round 2 빠른 확인) | — |

### 1.2 데이터 모델 재설계 (Q1·Q2 직접 영향)

Q1·Q2 답변이 기존 시드 `30_content/units/01/meta.json` 구조를 흔듭니다.

**현 schema (single person, single hook)**
```json
{
  "id": "01",
  "title-ko": "소인수분해",
  "person": "eratosthenes",
  "era-palette": "era-ancient",
  "signature-color": "#D4A843",
  "signature-object": "막대기",
  "learner-hook": "...",
  ...
}
```

**제안 schema v2 (N:M + 영상 array)**
```json
{
  "id": "01",
  "slug-en": "prime-factorization",
  "title-ko": "소인수분해",
  "title-en": "Prime Factorization",
  "grade": "mid1",
  "chapter": 1,
  "persons": [
    {
      "ref": "eratosthenes",
      "role": "primary",
      "era-palette": "era-ancient",
      "signature-color": "#D4A843",
      "signature-object": "막대기",
      "story-hook": "에라토스테네스의 체로 소수를 걸러내는 과정이 소인수분해의 시작",
      "videos": ["sieve-of-eratosthenes"]
    }
    // 단원에 두번째 인물 있으면 여기 추가
  ],
  "key-concepts": [...],
  "problem-types": [...],
  ...
}
```

**인물 episode (영상)는 별 schema — 인물 종속, 단원 비종속.**
```
30_content/people/eratosthenes.md                 ← 사실/배경
30_content/people/eratosthenes/episodes/
  sieve-of-eratosthenes.md                        ← episode-level 이야기 (이 단원 1에서 쓰임)
  measuring-earth.md                              ← episode-level (다른 단원에서도 쓸 수 있음)
```

영상 주소트리도 인물 단위 권장:
```
50_channel/people/<person>/<episode>/final_v1_5.mp4
50_channel/people/<person>/<episode>/poster.jpg
50_channel/people/<person>/<episode>/storyboard.md
```
→ 현 `season-1-ancient/unit-01/`은 **인물·episode 단위로 리매핑** (C에서 실행) 또는 `seasons/`는 큐레이션 view로 별도 유지.

### 1.3 영상 디렉토리 — B vs C 경계 정리

B 범위 (지금): **link 구조·meta schema**가 어떻게 인물·episode를 가리키는지 결정.
C 범위 (별도 chatlog): 실제 영상 파일 디렉토리 이동·STORY_VIDEO_v1_5 표준 갱신.

B에서 정해두면 C가 따라옴.

### 1.4 추가 결정 요청 (Round 2)

#### R1-A. 데이터 모델 v2 schema 동의?
- `persons: [...]` 배열 (N:M)
- 인물 episode를 `30_content/people/<person>/episodes/<episode>.md` 로 분리
- meta.json에서 `persons[].videos[]` 로 episode를 ref

→ Nick 동의? 수정 의견? (Nick) 동의

#### R1-B. 영상 주소트리 — 두 가지 큐레이션
권장 = **이중 트리** (원본 1곳, view 1곳):
- **원본 (재사용 친화)**: `50_channel/people/<person>/<episode>/`
- **view (시즌/단원 진열)**: `50_channel/seasons/season-1-ancient/unit-01/` → 원본에 symlink 또는 빌드시 copy

이렇게 하면 Nick 의도 ("영상은 재사용 가능, 다른 데서 쓸 수 있음") 충족 + 시즌 큐레이션도 가능.

또는 단순화: 원본만 (`people/<person>/<episode>/`), `seasons/`는 meta로만 표현 (디렉토리 없음).

→ Nick 선호? (Nick) 이중트리 권장에 동의

#### R1-C. slug-en 표준 어휘 (13단원)
권장:
| 단원 | 한글 | slug-en |
|---|---|---|
| 01 | 소인수분해 | `prime-factorization` |
| 02 | 정수와유리수 | `integers-rationals` |
| 03 | 문자와식 | `letters-and-expressions` |
| 04 | 일차방정식 | `linear-equations` |
| 05 | 좌표와그래프 | `coordinates-and-graphs` |
| 06 | 정비례와반비례 | `proportion-inverse-proportion` |
| 07 | 기본도형 | `basic-figures` |
| 08 | 작도와합동 | `construction-and-congruence` |
| 09 | 다각형 | `polygons` |
| 10 | 원과부채꼴 | `circles-and-sectors` |
| 11 | 다면체와회전체 | `polyhedra-and-solids-of-revolution` |
| 12 | 입체도형의겉넓이와부피 | `surface-area-and-volume` |
| 13 | 자료의정리와해석 | `data-and-statistics` |

→ Nick OK? 수정 의견?(Nick) 다시 영미권에서 사용하는 공식 수학 교과서 용어를 찾아서 수정 바람. 내가 잘 모르긴하지만 좀 어색한 것들 섞여있음. 신뢰할만하게 확인/업데이트 완료하면 나에게 다시 물어볼 필요는 없음

#### R1-D. 인물 풀 — Round 2에서 NCC가 13단원 풍부 제안 + Nick 선택?
Nick 의도: 풍부하게. NCC가 단원당 1~3명 후보 + 각 인물 episode 핵을 적극 제안하고, Nick은 솎아내는 방식 — 동의?

→ Yes 면 Round 2에서 13단원 인물 풀 제안 (큰 작업).
(Nick) Yes. 최대한 풍부한 것 좋음. Nick 이 솎아내지 않고 여러개 사용가능함.  한단원에 여러인물 소개 가능한 구조여야 함.

#### R1-E. Round 2 작업 순서
권장:
1. **schema v2 확정** (R1-A 답변)
2. **인물 풀 제안 + Nick 솎아냄** (R1-D)
3. **누락 인물 md 작성** (브라마굽타, 디오판토스, …) — Round 2 마지막 또는 별 Round
4. **13단원 meta.json 작성** (slug-en + persons 배열)
5. **UNIT_PAGE_STANDARD.md 작성** (인물 카드, 영상 link UI, 폴더 표준)
6. **walk_01 누락 확인** (빠른 단발)
7. **math1/index.html hub 재정비** (B 마무리)

이 순서로 Round 2 시작 OK?
( Nick) OK 그런데 Round 2 뒤의 다음 라운드 들은 어디에 정의됨.? 실제 좋은 그림 프롬프트 -> 그림 -> 영상 등?? 다른일 하다 오니 이전 계획 기억안남. 
### 1.5 다음

Nick R1-A~E 답변 → Round 2 (NCC가 schema 확정 + 인물 풀 작성 시작) ……

---

## Round 1.6 — 큰 그림 Recap (Nick "이전 계획 기억 안 남" 답)

### 1.6.1 작업 전체 로드맵

마이그 직후 NCC가 제안하고 Nick이 "A, B 순서대로"로 확정한 큰 작업 목록 (TaskList #16-20):

```
A. math1 마이그 잔재 정리  ✅ 완료 (commit 13b0159)
   └─ unit-01/, _index_v_mathtelling.html 삭제

B. 수학 챕터 표준 정의  🟢 진행 중 ← 이 chatlog
   └─ Round 0~2: schema + 인물 풀 + UNIT_PAGE_STANDARD + meta.json × 13 + hub 재정비
   └─ plan 파일: 00_project_hub/20_plan/260522_plan_math_chapter.md

C. 영상 v1.5 표준화  ⏳ 다음
   └─ 별도 chatlog 예정 (260523_video_v1_5_standardize.md 같은)
   └─ "그림 프롬프트 → 그림 → 영상" 파이프라인 정교화는 여기
   └─ plan 파일: 00_project_hub/20_plan/260522_plan_video_flow.md
   └─ 핵심: storyboard → image_prompts → AI 이미지 생성 → HyperFrames/GSAP → TTS → FFmpeg
   └─ 산출물: 인물·episode 단위 final_v1_5.mp4 (B에서 합의된 50_channel/people/<person>/<episode>/)

E. 배포 매핑·hookup  ⏳ 나중
   └─ 60_deploy/ 빌드 출력, mid1 GH Pages 대응
   └─ slug-en 한글 폴더 → 영문 URL 변환 빌드 스크립트

D. 13단원 영상 일괄 확장  ⏳ 가장 나중
   └─ B/C 표준 확정 후 단원당 별도 chatlog (260529_unit02_video.md 패턴)
```

### 1.6.2 B 내부 sub-round 계획 (R1-E에서 합의된 순서)

```
Round 2.A — schema v2 확정 + slug-en 영미권 갱신          ← 이 다음
Round 2.B — 13단원 인물 풀 제안 (NCC 풍부하게 다 채움)
Round 2.C — 누락 인물 사실 md 작성 (브라마굽타, 디오판토스, ... 8-10인)
Round 2.D — 13단원 meta.json 작성 (slug-en + persons 배열 + episode ref)
Round 2.E — UNIT_PAGE_STANDARD.md 작성 (인물 카드, 영상 link UI)
Round 2.F — walk_01 누락 확인 (단발)
Round 2.G — math1/index.html hub 재정비 (B 마무리)
```

### 1.6.3 즉, "그림 프롬프트 → 그림 → 영상"은 C에서

Nick이 물은 "실제 좋은 그림 프롬프트 → 그림 → 영상" 파이프라인은 **C(영상 v1.5 표준화)** 의 핵심.
지금 B는 그 영상이 **어디 저장되고 어떻게 link 되는지의 트리·meta**까지만 정함. 영상 만드는 방법론은 C에서 별도 chatlog로.

---

## Round 2.A — schema v2 확정 + slug-en 영미권 갱신

### 2.A.1 schema v2 확정 (R1-A 동의)

`30_content/units/NN/meta.json` 표준 schema. Round 2.D에서 13단원 적용.

```json
{
  "id": "NN",
  "slug-en": "<영미권 표준>",
  "title-ko": "<한글 단원명>",
  "title-en": "<영문 단원명>",
  "grade": "mid1",
  "chapter": <int>,
  "persons": [
    {
      "ref": "<person-key>",
      "role": "primary|secondary|cameo",
      "era-palette": "era-ancient|era-medieval|era-modern|era-contemporary",
      "signature-color": "#RRGGBB",
      "signature-object": "<short-noun>",
      "story-hook": "<one-line>",
      "videos": ["<episode-key>", ...]
    }
  ],
  "key-concepts": [...],
  "problem-types": [
    { "id": "TNN", "name": "..." }
  ]
}
```

인물 episode 분리 구조 (R1-A 동의):

```
30_content/people/<person>.md                          ← 인물 사실/배경
30_content/people/<person>/episodes/<episode-key>.md   ← episode-level 이야기
                                                       (단원 비종속, 재사용 가능)

50_channel/people/<person>/<episode-key>/              ← 영상 원본 (재사용 source)
  ├── storyboard_v1_5.md
  ├── image_prompts.md
  ├── narration_v1_5.{txt,xml,mp3}
  ├── poster_v1_5.jpg
  ├── final_v1_5.mp4
  └── ...

50_channel/seasons/season-1-ancient/unit-NN/           ← 큐레이션 view
  └── (people/<person>/<episode>/ 의 ref or symlink)
```

### 2.A.2 slug-en 영미권 표준 갱신 (R1-C 자체 결정)

Common Core Grade 7 표준 + 영미권 중학 교과서 (Khan Academy, AoPS, Pearson, McGraw-Hill) 관례 종합. 7개 단원이 R1 권장안에서 영미권 표준과 어긋나 수정.

| # | 한글 | R1 권장 | **R2.A 확정 (영미권 표준)** | 근거 |
|---|---|---|---|---|
| 01 | 소인수분해 | prime-factorization | **`prime-factorization`** | 표준 (변경 없음) |
| 02 | 정수와 유리수 | integers-rationals | **`integers-and-rational-numbers`** | 영미권: "Integers"·"Rational Numbers"가 각각 표준 명칭. R1 단축형은 어색 |
| 03 | 문자와 식 | letters-and-expressions | **`algebraic-expressions`** | 영미권 표준은 "Algebraic Expressions". "letters and expressions"는 한국식 직역 |
| 04 | 일차방정식 | linear-equations | **`linear-equations`** | 표준 |
| 05 | 좌표와 그래프 | coordinates-and-graphs | **`coordinate-plane`** | Common Core: "The Coordinate Plane". 좌표평면 도입 단원이므로 정확 |
| 06 | 정비례와 반비례 | proportion-inverse-proportion | **`direct-and-inverse-variation`** | 영미권 정통 표현 (y=kx direct variation, y=k/x inverse variation). "proportion"보다 정확 |
| 07 | 기본도형 | basic-figures | **`points-lines-and-angles`** | 영미권 단원명 "Points, Lines, and Angles". "basic figures"는 모호 |
| 08 | 작도와 합동 | construction-and-congruence | **`constructions-and-congruence`** | 영미권 표준은 복수 "constructions" |
| 09 | 다각형 | polygons | **`polygons`** | 표준 |
| 10 | 원과 부채꼴 | circles-and-sectors | **`circles-and-sectors`** | 표준 |
| 11 | 다면체와 회전체 | polyhedra-and-solids-of-revolution | **`polyhedra-and-solids-of-revolution`** | 직역 유지 (한국 단원 고유 구성) |
| 12 | 입체도형 겉넓이·부피 | surface-area-and-volume | **`surface-area-and-volume`** | 표준 |
| 13 | 자료의 정리와 해석 | data-and-statistics | **`data-analysis-and-statistics`** | 영미권 표준: "Data Analysis and Statistics" |

**참고 출처:**
- [Grade 7 Common Core State Standards Initiative](https://www.thecorestandards.org/Math/Content/7/)
- [Common Core State Standards Mathematics Grade 7 (Oregon DOE)](https://www.oregon.gov/ode/educator-resources/standards/mathematics/Documents/ccssm7.pdf)

### 2.A.3 title-en (영문 단원명) 동시 확정

slug-en은 URL 어휘 (kebab-case), title-en은 사람 읽는 표제 (Title Case). 같은 영미권 어휘.

| # | title-en |
|---|---|
| 01 | Prime Factorization |
| 02 | Integers and Rational Numbers |
| 03 | Algebraic Expressions |
| 04 | Linear Equations |
| 05 | The Coordinate Plane |
| 06 | Direct and Inverse Variation |
| 07 | Points, Lines, and Angles |
| 08 | Constructions and Congruence |
| 09 | Polygons |
| 10 | Circles and Sectors |
| 11 | Polyhedra and Solids of Revolution |
| 12 | Surface Area and Volume |
| 13 | Data Analysis and Statistics |

### 2.A.4 산출물 (이 라운드에서 실행)

- 이 chatlog Round 2.A 기록 (지금)
- `30_content/units/01/meta.json` 시범 갱신 (schema v2 적용 — 다른 단원 작성 reference)
- `00_project_hub/20_plan/260522_plan_math_chapter.md` slug-en 확정 표 반영

13단원 meta.json 일괄 작성은 Round 2.D (인물 풀 결정 후).

### 2.A.5 다음 라운드

Round 2.B — 13단원 인물 풀 제안 (NCC가 풍부하게 채움. Nick은 추가만, 솎아내지 않음).

---

## Round 2.B — 13단원 인물 풀 제안 (NCC 풍부 채움)

### 2.B.1 제안 원칙

- **단원당 primary 1명 + secondary 1명**: 두 인물이 단원의 핵 episode 둘로 묶임. Nick R1-D 답("한 단원에 여러 인물") 충족.
- **인물 재출현 OK**: 같은 인물이 여러 단원에 등장. 단 episode-key는 다르게 (인물의 서로 다른 이야기).
- **시대순 흐름 1순위 아님**: 개념 적합성 우선. 시대 다양성은 era-palette로 표현.
- **cameo (3번째 인물)**: 인물 md 없어도 됨. UNIT_PAGE_STANDARD에서 "참고" 정도 노출 — Round 2.E에서 결정. 이번 풀에는 미포함.

### 2.B.2 13단원 인물·episode 풀

| # | 단원 (slug-en) | role | person (ref) | era-palette | episode-key | story-hook (1줄) |
|---|---|---|---|---|---|---|
| **01** | prime-factorization | primary | eratosthenes ✓ | era-ancient | `sieve-of-eratosthenes` | 알렉산드리아의 도서관장이 만든 소수를 걸러내는 체 |
| 01 | prime-factorization | secondary | euclid ✓ | era-ancient | `fundamental-theorem-of-arithmetic` | 모든 정수는 소수의 곱으로 유일하게 분해된다 (Elements VII) |
| **02** | integers-and-rational-numbers | primary | **brahmagupta** ✗ | era-ancient | `zero-and-negatives` | 0과 음수를 정식 수로 다룬 첫 수학자 (628 인도) |
| 02 | integers-and-rational-numbers | secondary | al-khwarizmi ✓ | era-medieval | `restoration-and-balancing` | "al-jabr" — 음수 항을 양변으로 옮기는 균형의 기술 |
| **03** | algebraic-expressions | primary | al-khwarizmi ✓ | era-medieval | `birth-of-algebra` | "Al-Kitāb al-mukhtaṣar" — 대수학의 탄생 (820) |
| 03 | algebraic-expressions | secondary | **viete** ✗ | era-modern | `letters-for-numbers` | 미지수=모음·상수=자음으로 표기한 첫 수학자 (1591) |
| **04** | linear-equations | primary | **diophantus** ✗ | era-ancient | `arithmetica-and-epitaph` | 디오판토스 묘비 문제 — 그의 인생을 방정식으로 |
| 04 | linear-equations | secondary | al-khwarizmi ✓ | era-medieval | `six-types-of-equations` | 일차·이차방정식 6유형의 체계적 해법 |
| **05** | coordinate-plane | primary | descartes ✓ | era-modern | `dream-of-the-fly` | 침대의 파리 → 좌표의 발견 (1619, La Géométrie) |
| 05 | coordinate-plane | secondary | **fermat** ✗ | era-modern | `independent-coordinates` | 데카르트와 독립적으로 해석기하 발견한 변호사 |
| **06** | direct-and-inverse-variation | primary | **kepler** ✗ | era-modern | `equal-areas-in-equal-times` | 행성이 같은 시간에 휩쓰는 면적은 일정 — 반비례 (1609) |
| 06 | direct-and-inverse-variation | secondary | **boyle** ✗ | era-modern | `pressure-volume-inverse` | 압력×부피 = 일정 (Boyle's law, 1662) |
| **07** | points-lines-and-angles | primary | euclid ✓ | era-ancient | `elements-five-postulates` | 5개 공준으로 시작하는 기하학의 토대 |
| 07 | points-lines-and-angles | secondary | **thales** ✗ | era-ancient | `shadow-of-pyramid` | 그림자로 피라미드 높이를 잰 최초의 닮음 정리 (BC 6세기) |
| **08** | constructions-and-congruence | primary | euclid ✓ | era-ancient | `compass-and-straightedge` | 두 도구만으로 작도하는 그리스 전통 |
| 08 | constructions-and-congruence | secondary | **gauss** ✗ | era-modern | `regular-17-gon` | 19살 가우스의 정17각형 작도 (1796) |
| **09** | polygons | primary | **pythagoras** ✗ | era-ancient | `pentagon-and-golden-ratio` | 정오각형 속 황금비 — 피타고라스 학파의 비밀 |
| 09 | polygons | secondary | kepler (재출현) | era-modern | `tiling-the-plane` | 정다각형으로 평면을 채우는 11가지 방법 |
| **10** | circles-and-sectors | primary | **archimedes** ✗ | era-ancient | `measurement-of-circle` | 96각형으로 추정한 π — 측정의 거장 (BC 3세기) |
| 10 | circles-and-sectors | secondary | **liu-hui** ✗ | era-ancient | `chinese-pi-refinement` | 3072각형으로 π=3.14159 (263년 중국) |
| **11** | polyhedra-and-solids-of-revolution | primary | **plato** ✗ | era-ancient | `five-platonic-solids` | 우주의 다섯 원소 = 다섯 정다면체 (Timaeus) |
| 11 | polyhedra-and-solids-of-revolution | secondary | kepler (재출현) | era-modern | `mysterium-cosmographicum` | 정다면체 안에 행성 궤도를 끼워 넣다 (1596) |
| **12** | surface-area-and-volume | primary | archimedes (재출현) | era-ancient | `sphere-and-cylinder` | 구·원기둥 부피비 2:3 — 묘비에 새겨진 발견 |
| 12 | surface-area-and-volume | secondary | **cavalieri** ✗ | era-modern | `indivisibles-principle` | 같은 단면적 → 같은 부피 (적분의 시초, 1635) |
| **13** | data-analysis-and-statistics | primary | nightingale ✓ | era-contemporary | `coxcomb-and-crimea` | 크림 전쟁 사망 원인 빛낸 색채 통계 차트 (1858) |
| 13 | data-analysis-and-statistics | secondary | **playfair** ✗ | era-modern | `invention-of-bar-chart` | 막대·선·원 그래프를 발명한 스코틀랜드 엔지니어 (1786) |

`✓` = `30_content/people/`에 이미 사실 md 존재.
`✗` = **추가 작성 필요** (Round 2.C 대상).

### 2.B.3 인물 통계

**기존 5인 사용 위치**:
- eratosthenes: 01 (primary)
- euclid: 01·07·08 (이미 작성됨, episode 분리)
- al-khwarizmi: 02·03·04 (이미 작성됨, episode 분리)
- descartes: 05 (primary)
- nightingale: 13 (primary)

**Round 2.C 추가 작성 필요 인물 14인**:
1. brahmagupta (02 primary) — 7세기 인도, 0·음수
2. viete (03 secondary) — 16세기 프랑스, 변수 표기
3. diophantus (04 primary) — 3세기 알렉산드리아, Arithmetica
4. fermat (05 secondary) — 17세기 프랑스, 해석기하·정수론
5. kepler (06 primary, 09·11 secondary) — 17세기 독일, 천문·정다면체
6. boyle (06 secondary) — 17세기 아일랜드, 기체 법칙
7. thales (07 secondary) — BC 6세기 그리스, 그림자 측정
8. gauss (08 secondary) — 19세기 독일, 정17각형
9. pythagoras (09 primary) — BC 6세기 그리스, 정오각형·황금비
10. archimedes (10 primary, 12 primary) — BC 3세기, 원·구
11. liu-hui (10 secondary) — 3세기 중국, π 정밀화
12. plato (11 primary) — BC 4세기 그리스, 정다면체 우주관
13. cavalieri (12 secondary) — 17세기 이탈리아, 적분 원리
14. playfair (13 secondary) — 18세기 스코틀랜드, 그래프 발명

### 2.B.4 era-palette 분포

| era-palette | 단원·인물 (occurrences) |
|---|---|
| era-ancient | 13인 13회 (eratosthenes, euclid×3, brahmagupta, diophantus, thales, pythagoras, archimedes×2, liu-hui, plato) |
| era-medieval | 3회 (al-khwarizmi×3) |
| era-modern | 8회 (viete, descartes, fermat, kepler×3, boyle, gauss, cavalieri, playfair) |
| era-contemporary | 1회 (nightingale) |

→ Ancient 색채가 두드러짐. Season 1 (Ancient) 컨셉과 일치. modern은 Season 2 후보로도 활용 가능.

### 2.B.5 산출물 (이 라운드 결정)

위 풀을 **Round 2.C / 2.D의 입력**으로 사용:
- **Round 2.C**: 14인 사실 md 작성 (`30_content/people/<person>.md`) + 각 인물의 episode md (`30_content/people/<person>/episodes/<episode-key>.md`)
- **Round 2.D**: 13단원 `meta.json` 일괄 작성 (이 풀 그대로 반영)

### 2.B.6 다음 라운드

Round 2.C — 14인 인물 사실 md + 26개 episode md 작성 시작.

> 분량이 큼. NCC가 자율 진행 (Nick R1-D "풍부하게 다 사용" 정신). 한 라운드에 다 끝내거나 인물 그룹별로 나눠 진행. 작성 후 push.

---

## Round 2.C — 14인 인물 사실 md 작성

### 2.C.1 정책 결정 — episode md 분리 시점 미룸

schema v2 의도는 `30_content/people/<person>/episodes/<episode-key>.md` 분리지만, 다음 사정 고려:

1. **기존 5인 md (eratosthenes·euclid·al-khwarizmi·descartes·nightingale)** 도 episode를 본문 "핵심 일화 N"으로 통합 보유 — 형식 일관성을 위해 신규 14인도 동일 형식 채택.
2. **episode md 본격 분리는 영상 작업(C) 시점에 함**. 영상 단위로 storyboard·image_prompts와 같이 묶이는 게 자연스러움. `50_channel/people/<person>/<episode>/storyboard_v1_5.md` 가 사실상의 episode md 역할.
3. meta.json의 `videos: ["<episode-key>"]` 는 ref-only — 파일 부재여도 OK. 영상 생성 시점에 50_channel 안에서 등장.

→ **이번 라운드: 인물 사실 md 14개 (단일 파일에 episode 일화 통합) 작성.** episode md 분리는 C에서 영상 작업과 같이.

### 2.C.2 14인 md 작성 (이 라운드 산출물)

각 md 구조 (기존 5인 패턴 답습):
- frontmatter (id·name-ko·name-en·era·period·origin·activity·unit·topic·signature-color·signature-object·era-palette·source)
- 한 줄 메시지 (인용형)
- 기본 정보 표
- 핵심 일화 1~2 (Round 2.B에서 매핑한 episode-key 명시)
- 딸에게 줄 메시지
- 출처

frontmatter의 `unit` 필드: 인물이 여러 단원 등장 시 primary 단원만 적고 본문에 "다른 단원에서도 등장" 언급.

산출물: 다음 14개 파일을 한꺼번에 작성 → commit.

```
30_content/people/brahmagupta.md   (02)
30_content/people/viete.md          (03)
30_content/people/diophantus.md     (04)
30_content/people/fermat.md         (05)
30_content/people/kepler.md         (06, 09, 11)
30_content/people/boyle.md          (06)
30_content/people/thales.md         (07)
30_content/people/gauss.md          (08)
30_content/people/pythagoras.md     (09)
30_content/people/archimedes.md     (10, 12)
30_content/people/liu-hui.md        (10)
30_content/people/plato.md          (11)
30_content/people/cavalieri.md      (12)
30_content/people/playfair.md       (13)
```

### 2.C.3 다음 라운드

Round 2.D — 13단원 `30_content/units/NN/meta.json` 일괄 작성 (schema v2 + persons 풀 반영).

---

## Round 2.D — 13단원 meta.json 일괄 작성

### 2.D.1 산출물

12개 신규 meta.json 작성 (01은 Round 2.A에서 적용 완료, 동일 schema):

```
30_content/units/02/meta.json   integers-and-rational-numbers   (brahmagupta + al-khwarizmi)
30_content/units/03/meta.json   algebraic-expressions           (al-khwarizmi + viete)
30_content/units/04/meta.json   linear-equations                (diophantus + al-khwarizmi)
30_content/units/05/meta.json   coordinate-plane                (descartes + fermat)
30_content/units/06/meta.json   direct-and-inverse-variation    (kepler + boyle)
30_content/units/07/meta.json   points-lines-and-angles         (euclid + thales)
30_content/units/08/meta.json   constructions-and-congruence    (euclid + gauss)
30_content/units/09/meta.json   polygons                        (pythagoras + kepler)
30_content/units/10/meta.json   circles-and-sectors             (archimedes + liu-hui)
30_content/units/11/meta.json   polyhedra-and-solids-of-revolution (plato + kepler)
30_content/units/12/meta.json   surface-area-and-volume         (archimedes + cavalieri)
30_content/units/13/meta.json   data-analysis-and-statistics    (nightingale + playfair)
```

### 2.D.2 채움 정확도

- `id·slug-en·title-{ko,en}·grade·chapter·persons`: **확정** (Round 2.A·2.B 정신 그대로)
- `key-concepts`: 한국 중1 교과과정 표준 + 각 단원 `problems/types.md` 헤더 참조하여 7~8 항목씩
- `problem-types`: 각 단원 `problems/types.md` 의 7유형 그대로 (Q1-3 검토에서 walk_01 누락 외엔 일관성 확인됨)
- `pages`: 새 repo 경로 `40_grades/middle/math1/NN_*/...` (mathtelling apps 옛 경로 모두 갱신)

`key-concepts`·`problem-types`는 Phase 1·5-b에서 더 정밀화 가능. 지금 단계는 schema 채움 완성도 우선.

### 2.D.3 다음 라운드

Round 2.E — `10_system/10_principles/UNIT_PAGE_STANDARD.md` 신규 작성 (인물 카드 + 영상 link UI + 단원 페이지 4파일 표준).

---

## Round 2.E — UNIT_PAGE_STANDARD.md 작성

### 2.E.1 산출물

`10_system/10_principles/UNIT_PAGE_STANDARD.md` v0.1 (약 200줄, 11 섹션).

### 2.E.2 핵심 내용

1. 단원 폴더 표준 (4 root + 2 dir)
2. `index.html` (단원 hub) — 4축 진입 + 인물 카드
3. `story.html` — 인물 카드 + 영상 link + 글쓰기 미션
4. `concepts.html` — 개념 맵 + 인터랙티브 위젯
5. `problems/` — 4-mode (basic + types/type_NN + deep + walk) — mid_eun 검증 구조
6. **영상 주소트리 이중 트리**: 원본 `50_channel/people/<ref>/<ep>/` + view `50_channel/seasons/season-N/unit-NN/` (Round 2.B 합의)
7. design-system 융합: CSS var `--mt-person-color` 로 시그니처 컬러 주입, era-palette 보조색 매핑
8. **빈칸·미완성 슬롯** (CLAUDE.md 절대 원칙 5번 반영)
9. URL 변환 — 폴더명 `NN_<한글>` → URL `NN_<slug-en>` 빌드 시 (E 배포 매핑 단계)
10. audit 도구 — 현 `/se_ncc_audit_app` + 향후 `se_ncc_audit_unit_page` 신설 검토

### 2.E.3 다음 라운드

Round 2.F — `01_소인수분해/problems/walk_01` 누락 확인 (단발).
Round 2.G — `40_grades/middle/math1/index.html` (math1 hub) 재정비 + B 마무리.

---

## Round 2.F — walk_01 누락 확인 (단발)

### 2.F.1 사실

01단원 `problems/`에 `walk_01_H{1,2,3}.html` 부재.
다른 단원 (02·03·…) 은 모두 `walk_01_H{1,2,3}.html` 존재.

01단원 `types.md` 의 유형 1 (소수·합성수 판별):
> 난이도 분포: L(소수/합성수 판별), M(범위 내 소수 개수), **H(조건을 만족하는 소수 찾기)**

→ H가 있다고 적혀 있고, type_01_app.html 도 H 문제 포함하나, walk 풀이 3개가 누락.

### 2.F.2 판정

**의도 아닌 누락.** mid_eun 작업 시 unit-01만 walk_01 단계 빠뜨림 (가장 먼저 작업한 단원이라 walk 표준 정립 전).

### 2.F.3 조치

지금은 보강 미실시. **후속 단발 commission** 으로 분리. 시점: B 마무리 후 또는 단원별 영상 작업(D) 단원 진입 시.

작업 명세 (참조용):
- `problems/type_01_app.html` 의 H 난이도 3문제 추출
- 각 문제별 `walk_01_H1.html`, `walk_01_H2.html`, `walk_01_H3.html` step-by-step 풀이 작성
- `/se_math_practice` 또는 `/se_math_error_note` skill 활용 가능

---

## Round 2.G — math1 hub (`index.html`) 재정비

### 2.G.1 진단

mathtelling 시드 디자인은 좋음. 단 3가지 옛 정보:
1. **design-system 경로** `../../mathtelling-design-system/dist/all.css` ← 새 repo에 없음
2. **카드 link URL** `unit-NN/index.html` ← 새 폴더명 `NN_<한글>/index.html`
3. **인물·era·시그니처 컬러** 매핑 일부 오류 (06 데카르트→케플러, 09 유클리드→피타고라스, 11 케플러→플라톤 등 Round 2.B 풀과 불일치)

### 2.G.2 재작성 (완료)

- design-system 경로 갱신: `../../../20_packages/design-system/dist/all.css` (3 레벨 up: math1 → middle → grades → root)
- 13개 카드 모두 link URL 새 폴더명으로
- 인물 매핑 Round 2.B 풀과 정확히 일치 (primary + secondary 함께 표기, secondary는 작은 글씨)
- 각 카드에 `slug-en` 표기 추가 (kebab-case English, 작은 회색 글씨)
- 시그니처 컬러 = primary 인물의 signature-color (meta.persons[0].signature-color)
- era 라벨 갱신 (Classical India, Islamic Golden Age, Late Antiquity, Early Modern 등 정확화)
- `Ready`/`Soon` 배지 모두 제거 — 13단원 모두 진입 가능한 상태이므로 통일 (단원 페이지 내부의 완성도는 별 표시 안 함)
- topbar/footer link `../../../` (repo root)

### 2.G.3 design-system 검증

`20_packages/design-system/dist/all.css` 존재 확인. `subjects/math.css` 존재 확인. 경로 정상.

페이지 dev 확인은 별도 (Nick이 브라우저에서 열어 검토).

---

## Round 2 — 종합 마무리

### 2.X.1 B 작업 완료 산출물 요약

| sub-round | 산출물 | 위치 |
|---|---|---|
| 2.A | schema v2 + slug-en 표 + unit 01 meta 시범 | chatlog + `30_content/units/01/meta.json` |
| 2.B | 13단원 인물 풀 (26 entry) | chatlog 표 |
| 2.C | 14인 사실 md (총 19인) | `30_content/people/` |
| 2.D | 12 신규 meta.json (총 13) | `30_content/units/NN/meta.json` |
| 2.E | UNIT_PAGE_STANDARD.md v0.1 | `10_system/10_principles/` |
| 2.F | walk_01 누락 후속 작업 명세 | chatlog (보강은 후속 commission) |
| 2.G | math1 hub `index.html` 재정비 | `40_grades/middle/math1/index.html` |

### 2.X.2 후속 작업 항목 (B 외부)

- **walk_01 보강** (01단원 problems/walk_01_H{1,2,3}.html × 3) — 단발 commission
- **`30_content/concepts/`** 13단원 폴더의 개념 검수·보완 (Phase 1 작업, `/se_concept_review` skill) — 이번 B 범위 외
- **C. 영상 v1.5 표준화** — 다음 큰 작업
- **E. 배포 매핑** — slug-en 변환 빌드 스크립트 (`60_deploy/` 출력 정의)
- **D. 13단원 영상 일괄 확장** — C/B/E 표준 확정 후

### 2.X.3 다음 큰 작업

**C. 영상 v1.5 표준화** — 별도 chatlog (`260523_video_v1_5_standardize.md` 같은) 시작.
Nick 의도 "그림 프롬프트 → 그림 → 영상" 파이프라인 정교화가 여기서.
