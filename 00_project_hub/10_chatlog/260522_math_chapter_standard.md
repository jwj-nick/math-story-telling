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

→ Nick의 선호·아이디어?

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

→ 어느 게 Nick 의도?

#### Q3. 폴더명 vs URL slug
현 폴더: `01_소인수분해/` (한글). 옛 GH Pages URL: `mid1/math1/01_prime-factorization/` (영문 slug).

권장:
- **(a)** 폴더 한글 유지 + `30_content/units/NN/meta.json`에 `slug-en` 필드 추가 → 빌드시 URL 변환
- (b) 폴더를 영문 rename + 한글 title은 meta에만
- (c) 둘 다 유지 (한글 폴더 + symlink/build redirect)

→ (a) 권장 (폴더는 작업자 가독성, URL은 배포용 분리). Nick 선호?

#### Q4. math1/index.html (hub) 처리
- 지금 재정비할지 vs B 마무리 단계에서 한꺼번에?
- 권장: B 마무리 단계 — 모든 단원 메타·인물 정해진 후 hub에 반영

#### Q5. walk_01 누락 (01단원만)
- 누락 vs 의도? 검토 필요
- 권장: Round 2에서 빠르게 확인 (다른 단원과 type_01의 난이도 분포 비교)

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
