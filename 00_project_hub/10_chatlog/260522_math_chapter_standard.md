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

→ Nick 동의? 수정 의견?

#### R1-B. 영상 주소트리 — 두 가지 큐레이션
권장 = **이중 트리** (원본 1곳, view 1곳):
- **원본 (재사용 친화)**: `50_channel/people/<person>/<episode>/`
- **view (시즌/단원 진열)**: `50_channel/seasons/season-1-ancient/unit-01/` → 원본에 symlink 또는 빌드시 copy

이렇게 하면 Nick 의도 ("영상은 재사용 가능, 다른 데서 쓸 수 있음") 충족 + 시즌 큐레이션도 가능.

또는 단순화: 원본만 (`people/<person>/<episode>/`), `seasons/`는 meta로만 표현 (디렉토리 없음).

→ Nick 선호?

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

→ Nick OK? 수정 의견?

#### R1-D. 인물 풀 — Round 2에서 NCC가 13단원 풍부 제안 + Nick 선택?
Nick 의도: 풍부하게. NCC가 단원당 1~3명 후보 + 각 인물 episode 핵을 적극 제안하고, Nick은 솎아내는 방식 — 동의?

→ Yes 면 Round 2에서 13단원 인물 풀 제안 (큰 작업).

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

### 1.5 다음

Nick R1-A~E 답변 → Round 2 (NCC가 schema 확정 + 인물 풀 작성 시작) ……
