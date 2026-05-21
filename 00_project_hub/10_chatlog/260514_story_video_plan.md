<!-- 260514_story_video_plan.md -->

# Story 영상 제작 — 기획 및 Q&A 세션

---

## 현황 스냅샷 (2026-05-14)

### 소재 현황

| 항목 | 상태 |
|---|---|
| story.html | 13단원 전부 완비 |
| story/unitNN.md | 13단원 전부 완비 |
| 90_video/ | 디렉토리 신규 생성 (비어있음) |
| 90_video/_templates/ | 신규 (템플릿 미작성) |

### se_video_make 스킬 파이프라인

```
narration.txt  →  edge-tts (ko-KR-SunHiNeural)
                    ↓ narration.mp3
90_video/_templates/{visual_type}.html  →  GSAP 애니메이션 index.html
                    ↓ HyperFrames 렌더
                  raw.mp4  +  narration.mp3
                    ↓ FFmpeg
                  final.mp4  (1280×720, 24fps)
```

### Visual type 매핑 (스킬 정의 기준)

| concept 슬러그 | visual_type | 해당 단원 |
|---|---|---|
| sieve | number-grid | Unit 01 소인수분해 |
| prime_factorization | number-grid | Unit 01 |
| number_line | number-line | Unit 02 정수·유리수 |
| balance_scale | balance-scale | Unit 04 일차방정식 |
| coordinate | coordinate-plane | Unit 05 좌표·그래프 |
| proportional | coordinate-plane | Unit 06 정비례·반비례 |
| inversely_proportional | coordinate-plane | Unit 06 |
| bar_chart | bar-chart | Unit 13 자료 |
| geometry | geometry-sketch | Unit 07~12 도형 영역 |

---

## Round 1 — 기획 착수 (NCC, 2026-05-14)

### 배경 정리

- 13개 단원 각각 `story.html` (인터랙티브 인물 서사)과 `story/unitNN.md` (원문 텍스트) 완비
- `se_video_make` 스킬 존재: STAGE 1~6 (스크립트→TTS→GSAP→HyperFrames→FFmpeg)
- `90_video/` 디렉토리 오늘 신규 생성. 템플릿 아직 없음.

### 시작 전 결정이 필요한 질문들

**Q1. 영상의 용도와 배포 채널은?**
- (a) 딸이 공부 시작 전 유튜브처럼 보는 "흥미 유발 영상" (30~60초)
- (b) 각 단원 페이지에 임베드되는 "소개 영상" (story.html 상단에 위치)
- (c) 둘 다

Nick : (c) - 일단 각 story 에 대한 영상들을 만들어서 그것끼리 묶을수도, 지금 unit app 에 임배드 시킬수도 있음. 하나 하나 잘 만들어 보는 것이 중요.

**Q2. 도구 설치 현황?**
스킬 실행 전 확인 필요:
```powershell
ffmpeg -version
python -m edge_tts --version
hyperframes --version
```
→ Nick이 확인 후 결과 공유 요청

(Nick) 당신이 확인 바람. 이미 우리는 경험들이 있음. archive/50_units/01_소인수분해/ 내부의 파일들 깊게 확인하기 바람

**Q3. 파일럿 단원은?**
- Unit 01 (에라토스테네스, 소인수분해) — 가장 완성도 높음
- Unit 02 (브라마굽타, 정수·유리수) — 스토리 임팩트 강함
- 어느 단원으로 파일럿 시작할지 선택 필요

(Nick) unit 01 부터.. 다만 절대 서두르지 말기. 지금은 영상 제작 workflow setup 이 먼저임. 목표 자체가 flow setup 이라고 생각하기. 아주 detail plan 이 먼저임. 기술스택/시나리오/총 길이/video-audio sync/실제 학생이 볼떄 흥미가 있을건지... 이에 대한 skill setup 부터 먼저 할지.. 

**Q4. 영상 스타일 방향?**
- GSAP 애니메이션만 (현재 스킬 기본): 텍스트 + 단순 도형
- 좀 더 풍부한 시각화: 인물 일러스트, 배경 이미지 등 (추가 작업 필요)

(Nick) simple to complex but  better 로 계속 진화 시키기. 관련한 기술들을 익히고 싶음.

**Q5. 13개 전부 vs 1-2개 파일럿 먼저?**
- 파이프라인 검증 후 일괄 제작이 현실적

(Nick) unit 1 only first

### NCC 권장안

1. **도구 설치 확인** 먼저 → 없는 것 설치
2. **Unit 01 파일럿** → 스크립트 검토 → 렌더링 테스트
3. 파일럿 OK 후 나머지 12개 순차 or 배치

다음 라운드: Nick의 Q1~Q5 답변

---

(Nick)

---

## Round 2 — 기존 자산 전수 조사 결과 (NCC, 2026-05-14)

### 발견한 것

**1. 툴 모두 설치됨 ✅**

| 도구 | 버전 |
|---|---|
| ffmpeg | 8.1 |
| edge-tts | 7.2.8 |
| hyperframes | 0.4.42 |

파이프라인 실행 가능.

---

**2. archive/50_units/01_소인수분해/video/sieve-video/ — 완성된 영상 존재**

```
sieve-video/
├── narration.txt           ← 7줄 한국어 스크립트
├── narration.mp3           ← edge-tts 생성 오디오
├── index.html              ← GSAP 애니메이션 (232줄, number-grid)
├── sieve_final.mp4         ← 완성본 28.2초 / 764KB
├── sieve_with_audio.mp4    ← 오디오 합본 (782KB)
├── sieve.mp4, sieve_v3.mp4, sieve_29s.mp4  ← 이전 버전들
└── work-xxx/
    ├── compiled/index.html ← HyperFrames 인라인 컴파일본 (9164줄)
    └── audio-work/narration-trimmed.wav
```

`sieve_final.mp4` — 1280×720, 28.2초, number-grid 에라토스테네스 체 시각화.

---

**3. narration.txt 내용 (7줄, ~190자)**

```
기원전 240년, 에라토스테네스는 소수를 찾는 방법을 생각해냈습니다.
2는 소수입니다. 2의 배수를 모두 지웁니다.
3은 소수, 3의 배수를 지웁니다.
5도, 7도 소수입니다.
체에 남은 수들은 모두 소수.
2부터 50까지, 소수는 모두 열다섯 개.
이것이 에라토스테네스의 체입니다.
```

→ 개념 설명 위주. 인물 서사(이집트 도서관, 호기심, 발견의 순간)는 거의 없음.

---

**4. index.html 구조 — number-grid 템플릿 수준**

- 1280×720, dark bg (#0f172a), Noto Sans KR
- 숫자 그리드 (2~50), GSAP 타임라인 29초
- `window.__timelines['sieve']` 패턴 (HyperFrames 호환)
- 이 파일이 사실상 **number-grid 템플릿**의 원형

---

### 핵심 발견 — "Story 영상"의 정의 문제

archive의 sieve-video는 **수학 알고리즘 시각화** 영상.  
Nick이 원하는 **story 영상** (인물 이야기 기반)과는 성격이 다름.

현재 story.html 은 5장으로 구성:
1. 도서관의 수학자 (인물 등장)
2. 소수란 무엇인가 (개념)
3. 에라토스테네스의 체 (발견)
4. 알렉산드리아에서 세상으로 (영향)
5. 오늘날 (현대 연결)

→ **영상의 포지션 선택이 필요**:

| 옵션 | 설명 | 길이 |
|---|---|---|
| A. Story 영상 | 인물 서사 (감성, 인트로 역할) | 45~60초 |
| B. Concept 영상 | 알고리즘/수학 시각화 (sieve-video 기존 방식) | 25~35초 |
| C. 통합 영상 | 인물 도입 → 개념 시각화 → 마무리 | 60~90초 |

sieve_final.mp4는 B에 해당. 이미 완성됨.

---

### 90_video 템플릿 구조 제안

archive index.html → `90_video/_templates/number-grid.html` 로 추출 가능.
스킬이 요구하는 템플릿 위치: `90_video/_templates/{visual_type}.html`

Visual type별 템플릿 필요 목록:
- `number-grid.html` ← archive에서 추출 가능 (✅)
- `number-line.html` ← 신규 작성 필요 (Unit 02)
- `balance-scale.html` ← 신규 (Unit 04)
- `coordinate-plane.html` ← 신규 (Unit 05~06)
- `geometry-sketch.html` ← 신규 (Unit 07~12)
- `bar-chart.html` ← 신규 (Unit 13)

---

### 다음 결정 사항 (Nick에게)

**D1. 영상 포지션: A(Story), B(Concept), C(통합)?**

sieve_final.mp4는 이미 B 완성. C를 만들려면 인물 도입 파트 추가.

(Nick) 나는 지금 A 만 모든 unit 에 대해서 쭉 진행하면 어떨까 생각하고 있음. 이후 B 전체도 생각해볼수있겠지만 미래의 이야기임. 

**D2. Unit 01 기존 sieve_final.mp4를 어떻게 할까?**
- (a) 그대로 90_video/unit01/ 에 이전 후 활용
- (b) 스크립트 개선해서 새 버전 제작
- (c) 일단 두고 나중에 개선

(Nick) 현재 archive 에 있는걸 꺼내올 필요는 없음. 사실 그 영상은 테스트용이고, 다시 concept 에 대한 unit 1 만든다고 해도  똑같이 만들고 싶지는 않음.

**D3. workflow setup 목표 — 무엇을 "완성"으로 볼까?**
- 스킬(se_video_make) + 템플릿 세트 완비?
- Unit 01 영상 1개 완성 후 story.html 임베드까지?

(Nick) "스킬(se_video_make) + 템플릿 세트 완비" --> OK, but skill , context, tool 더 필요하면 셋업합시다.

---

## Round 3 — 워크플로우 제안 (NCC, 2026-05-14)

### Nick 답변 해석

| 결정 | 결과 | 의미 |
|---|---|---|
| D1 | A(Story 영상) 13개 일괄 | 인물 서사 중심, Concept 영상은 미래 과제 |
| D2 | archive 영상 미사용 | 새 시각 언어 정립 필요 |
| D3 | 스킬+템플릿 세트 완비 | "재사용 가능한 도구" 자체가 산출물 |

→ 이는 기존 `se_video_make` 스킬의 본질적 재설계를 의미함.

---

### 🔑 본질적 차이 — Concept 영상 vs Story 영상

| 항목 | Concept 영상 (기존 se_video_make) | **Story 영상 (신규 방향)** |
|---|---|---|
| 핵심 | 알고리즘/수학 시각화 | 인물·시대·발견의 서사 |
| 주된 시각 | 그리드, 그래프, 도형 (도식) | 인물 일러스트, 시대 배경, 상징 |
| 톤 | 명료, 분석적 | 감성적, 호기심 유발 |
| 길이 | 25~35초 | **45~60초** |
| Visual type | number-grid, balance-scale 등 9개 | **단일 마스터 템플릿 (장면 전환식)** |
| 사용 시점 | 개념 학습 단계 | 단원 진입 전 흥미 유발 |

→ 기존 9개 visual_type 매핑은 Story에 적용 안 됨. **새로운 템플릿 시스템 필요.**

---

### 🎬 Story 영상 표준 구조 (안)

총 길이 **50초** (한국어 TTS 250자 분량) 기준 5장면:

```
[0:00-0:05]  Scene 1 — 타이틀
             "에라토스테네스 · BCE 240년 알렉산드리아"
             단원명 함께 노출

[0:05-0:15]  Scene 2 — 인물 등장
             시대·장소·역할 (도서관장, 수학자)
             상징적 시각 (도서관, 두루마리, 별)

[0:15-0:32]  Scene 3 — 결정적 순간
             그 인물이 마주한 문제·호기심
             핵심 발견의 메타포

[0:32-0:45]  Scene 4 — 수학과의 연결
             "이것이 오늘날 우리가 배우는 ___ 의 시작입니다"

[0:45-0:50]  Scene 5 — 마무리
             "이번 단원에서 만날 이야기" 인트로 멘트
```

각 장면 전환은 1초 fade. 나레이션과 정밀 동기화.

---

### 🧰 기술 스택 (재검토 후 결론)

| 단계 | 도구 | 변경 |
|---|---|---|
| 나레이션 | edge-tts (ko-KR-SunHiNeural / ko-KR-InJoonNeural) | 기존 유지 |
| 컴포지션 | HTML + GSAP | 기존 유지 |
| 렌더 | HyperFrames | 기존 유지 |
| 합성 | FFmpeg | 기존 유지 |
| **시각 자원** | **SVG 일러스트 (시작)** → **AI 이미지 → SVG (진화)** | **신규** |
| **폰트** | Noto Sans KR + Nanum Myeongjo (제목용 명조) | 기존 + α |

**진화 단계 (Nick의 "simple to complex but better" 원칙):**

| 단계 | 시각 수준 | Unit |
|---|---|---|
| v1 | 텍스트 + 단순 SVG 심볼 (별, 책, 도형) | 01 |
| v2 | 인물 실루엣 + 시대 배경 SVG | 02~03 |
| v3 | 컬러 일러스트 (AI 생성 → SVG 트레이스) | 04~06 |
| v4 | 장면 전환 효과 강화, 시네마틱 | 07~13 |

각 단계 끝에 학습 정리. Nick의 기술 학습 욕구도 반영.

---

### 🛠️ Workflow 단계 (Phase 0~5)

```
Phase 0 — 인프라 셋업 (1회) ⭐
  ├─ 90_video/_templates/story-master.html (마스터 템플릿, 5장면 구조)
  ├─ 90_video/_assets/fonts/ (Noto + Nanum Myeongjo)
  ├─ 90_video/_assets/symbols/ (공통 SVG: 별, 두루마리, 책 등)
  ├─ 90_video/_assets/palettes.css (단원별 색감 정의)
  ├─ 90_video/_docs/STORY_VIDEO_GUIDE.md (제작 가이드)
  └─ 신규 skill: /se_story_video (Phase 1~5 자동화)

Phase 1 — 스토리보드 작성 (단원별, ~10분)
  ├─ story.html + story/unitNN.md 읽기
  ├─ 5장면 추출, 핵심 메타포 결정
  └─ 90_video/unitNN/storyboard.md

Phase 2 — Narration 작성 (단원별, ~10분)
  ├─ 5장면별 시간 할당 (50초)
  ├─ 학생 눈높이 (중1) 검토
  └─ 90_video/unitNN/narration.txt (250자 ± 20)

Phase 3 — Visual Composition (단원별, ~30분)
  ├─ master 템플릿 복사
  ├─ 단원 데이터 주입 (인물명, 텍스트, SVG 심볼)
  ├─ GSAP 타임라인 narration 동기화
  └─ 90_video/unitNN/index.html

Phase 4 — Render (자동, ~3분)
  ├─ edge-tts → narration.mp3
  ├─ hyperframes → raw.mp4
  └─ ffmpeg → final.mp4

Phase 5 — Review (Nick·딸)
  ├─ 시청 → 흥미·이해도 평가
  ├─ 필요 시 narration 수정 → Phase 4 재실행
  └─ story.html 상단 임베드 (<video> 태그)
```

---

### 📋 Phase 0 인프라 셋업 — 구체 산출물

**0-A. 마스터 템플릿** `90_video/_templates/story-master.html`
- 1280×720, dark/sepia 옵션 가능한 CSS 변수 설계
- 5개 `<div class="scene scene-N">` 구조 미리 마련
- GSAP 타임라인 5장면 골격 (각 장면 fade in/out)
- 데이터 주입 자리: `{{PERSON}}`, `{{ERA}}`, `{{CONCEPT}}`, `{{SCENE1_TEXT}}` 등

**0-B. 공통 SVG 자산** `90_video/_assets/symbols/`
- star.svg, scroll.svg, book.svg, sun.svg, geometry-shapes.svg
- 단원별 메타포에 재사용

**0-C. 단원별 색 팔레트** `90_video/_assets/palettes.css`
- unit01 (에라토스테네스, 알렉산드리아): warm sand + night sky
- unit02 (브라마굽타, 인도): saffron + indigo
- ... (13개)

**0-D. 신규 스킬** `.claude/commands/se_story_video.md`
- 인수: `unit=NN`
- 자동: story.md 읽기 → 스토리보드 제안 → Nick 검토 → narration → 렌더
- 기존 se_video_make는 보존 (Concept 영상 미래용)

**0-E. 제작 가이드** `90_video/_docs/STORY_VIDEO_GUIDE.md`
- 5장면 구조, 길이 정책, 톤 원칙
- 진화 단계 (v1~v4) 기준

---

### 🎯 첫 마일스톤 (workflow 검증)

**M1**: Phase 0 셋업 완료 (마스터 템플릿 + 신규 스킬)
**M2**: Unit 01 (에라토스테네스) 영상 v1 완성 — 50초, simple text+SVG
**M3**: Nick·딸 시청 → 피드백
**M4**: 피드백 반영 → v1 확정 → story.html 임베드 테스트
**M5**: Unit 02 영상 진행 (v2 시각 진화 적용)

M1~M4가 Nick이 말한 "workflow setup" 의 본체.

---

### ⚠️ 결정 필요 사항 (Nick에게)

**N1. 시각 컨셉의 첫 방향 (v1)**
- (a) 미니멀 텍스트 중심 (Apple 키노트 스타일, 검정/흰색)
- (b) 따뜻한 sepia 톤 + 손그림 풍 SVG (옛 문서 느낌)
- (c) 단원별 시대 분위기 (에라토스테네스=고대 그리스, 브라마굽타=인도)
- 추천: (c) — 인물별 색감 다양화가 13단원에 활기 줌

**N2. 신규 스킬을 만들까, 기존 se_video_make에 mode 추가?**
- (a) 신규 `/se_story_video` 작성 (깔끔, 권장)
- (b) `/se_video_make mode=story` 확장 (DRY)
- 추천: (a) — 서로 다른 시각 언어, 분리가 명확

**N3. 인물 일러스트 처리 방식 (v1)**
- (a) v1은 일러스트 없이 텍스트+심볼만 (가장 빠름)
- (b) v1부터 인물 실루엣 SVG (간단한 윤곽)
- (c) v1부터 AI 이미지 생성 도전 (DALL-E/Imagen)
- 추천: (a) — workflow 검증이 우선, 시각은 v2부터 진화

**N4. 신규 스킬 작성 작업 — 누가?**
- (a) 이번 세션에서 NCC가 작성 → Nick 리뷰
- (b) Phase 0 본격 착수 후 별도 세션
- 추천: (a) — 본 세션은 plan, 다음 세션부터 실행

---

### 📝 정리 — 무엇을 하자는 건지

1. **기존 se_video_make는 보존** (Concept 영상 미래용)
2. **새로운 Story 영상 전용 워크플로우 정립** — 다른 시각 언어
3. **Phase 0**가 핵심 — 마스터 템플릿, 자산, 스킬, 가이드 4종 세트
4. **Unit 01을 simple v1으로 먼저** — 텍스트+심볼, 50초
5. **시각은 점진적으로 진화** — Nick의 학습 욕구와 결합

오늘은 plan 확정. 다음 세션에서 N1~N4 답변 받아 Phase 0 착수.

---

(Nick) N1. c, N2. a, N3. a, N4. a,

---

## Round 4 — 확정안 및 실행 시퀀스 (NCC, 2026-05-14)

### 확정된 결정

| # | 선택 | 의미 |
|---|---|---|
| N1 | (c) 단원별 시대 분위기 | 13단원 각각 고유 컬러 팔레트 정의 필요 |
| N2 | (a) 신규 `/se_story_video` 스킬 | 기존 se_video_make와 분리, 깔끔한 분리 |
| N3 | (a) v1은 텍스트+심볼만 | 인물 일러스트는 v2부터 (workflow 검증 우선) |
| N4 | (a) 이번 세션에서 NCC 작성 | 본 세션 = 실행 세션 |

### Phase 0 산출물 (확정) — 5종

| 코드 | 산출물 | 역할 |
|---|---|---|
| 0-E | `90_video/_docs/STORY_VIDEO_GUIDE.md` | **단일 진실 원본** (모든 결정 기록) |
| 0-C | `90_video/_assets/palettes.css` | 13단원 시대 분위기 색 (N1=c) |
| 0-A | `90_video/_templates/story-master.html` | 5장면 마스터 템플릿 |
| 0-B | `90_video/_assets/symbols/` | 공통 SVG 심볼 (5~6개 시작) |
| 0-D | `.claude/commands/se_story_video.md` | 신규 스킬 정의 |

---

### 🔄 작업 시퀀스 (Nick의 "서두르지 말기" 원칙 반영)

**순서 결정 원리**: 의존 관계 따라 위→아래.
가이드(0-E)가 모든 후속 작업의 기준이 됨. 한 산출물 완료 후 Nick 리뷰 → 다음.

```
Step 1 ⭐ STORY_VIDEO_GUIDE.md  (0-E)
        ← 톤·길이·5장면 구조·진화 단계 명세 (기준 문서)
        
Step 2   palettes.css  (0-C)
        ← 13단원 인물·시대별 색 정의 (N1=c)
        
Step 3   story-master.html  (0-A)
        ← 가이드+팔레트 따라 5장면 골격, GSAP 타임라인, 데이터 주입 자리
        
Step 4   symbols/ SVG 5~6개  (0-B)
        ← 최소 자산 (star/scroll/book/sun/geometry-shapes), 단원별 추가는 점진
        
Step 5   se_story_video.md  (0-D)
        ← 위 4개를 활용하는 스킬 (Phase 1~5 단계별)
```

각 Step 완료 후:
- chatlog에 산출물 요약 기록
- Nick 검토 사인 (👍 또는 수정 요청)
- 다음 Step 착수

---

### ⏭️ 지금 착수: Step 1 — STORY_VIDEO_GUIDE.md

이 문서가 모든 후속 작업의 기준이 되므로 첫번째.

**포함될 섹션:**
1. 영상의 목적·청중·사용 시점
2. 표준 길이 정책 (50초 ± 5)
3. 5장면 구조 상세 (장면별 목적·길이·시각·내레이션 분량)
4. 톤 & 시각 원칙 (단원별 시대 분위기)
5. 진화 단계 (v1~v4)
6. 기술 스택 & 파이프라인
7. 디렉토리 구조 & 파일 명명 규칙
8. 임베드 정책 (story.html 통합 방식)
9. 품질 체크리스트

→ 작성 후 별도 메시지로 보고.

---

### Step 1 완료 보고 (NCC, 2026-05-14)

**산출물**: `90_video/_docs/STORY_VIDEO_GUIDE.md` (10개 섹션)

**핵심 결정 기록**:
- 목표 길이: 50초 ± 5 (한국어 240~270자)
- 5장면 구조: 타이틀(5s) → 인물(10s) → 결정적 순간(17s) → 수학 연결(13s) → 마무리(5s)
- 진화 v1~v4 (텍스트+심볼 → 시네마틱)
- 단원별 시대 분위기 매핑 (13개 키워드)
- 디렉토리/파일명 규칙 고정
- story.html 임베드 정책 (autoplay X, 클릭 재생)
- 품질 체크리스트 4분류 × 19항목

**Nick 검토 요청**:
- 50초 길이 정책 OK?
- 5장면 시간 배분 (5/10/17/13/5) OK?
- 단원별 톤 키워드 (sand+night sky 등) 방향 OK?
- 진화 단계 v1~v4 적용 단원 매핑 OK?
- 임베드 정책 (autoplay off, controls visible) OK?

**다음 Step (2)**: `_assets/palettes.css` — 가이드의 §4.3 키워드를 실제 CSS 변수로 구체화. 13단원 × 4~5개 색상 토큰.

---

(Nick)

N1. c,
N2. a,
N3. a,
N4. a,
