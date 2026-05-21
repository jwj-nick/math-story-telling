<!-- story_video_pipeline_overview.md -->

# MathTelling Story Video Pipeline — 기술 종합 정리

> **용도**: Claude Desktop Deep Research 입력 자료
> **날짜**: 2026-05-15
> **목표**: 현재 구현 전체 정리 + 품질 향상·자동화를 위한 research 방향 제시

---

## 1. 프로젝트 컨텍스트

### 1.1 목적

중학교 1학년 딸을 위한 수학 학습 시스템 "MathTelling"의 한 축.
각 수학 단원이 시작되기 전, **역사 속 수학자의 이야기를 50초 영상으로** 보여줌으로써 감성적 흥미를 유발한다.

- 수업용 설명 영상이 아님. **감성적 인트로** (관심 점화가 목적)
- 단원별 수학자 1인 — 에라토스테네스(소인수분해), 브라마굽타(정수·유리수), 알콰리즈미(문자·식) 등 13명
- 완성된 final.mp4 13개: 평균 43초, 합계 ~19MB

### 1.2 학습자 프로필

- 중1, 감성적·내성적, 국어·영어 강세, 수학 중하위
- 짧은 attention span → 50초 제한
- 강의체 설명 거부반응 → 이야기체 1인칭 내레이션

### 1.3 영상 포맷

| 항목 | 값 |
|---|---|
| 해상도 | 1280×720 |
| 컨테이너 | MP4 |
| 비디오 코덱 | H.264 |
| 오디오 코덱 | AAC |
| 프레임 레이트 | 24fps |
| 길이 | 45~55초 (목표 50초) |

---

## 2. 영상 구조 — 5장면 (Five-Act)

| 장면 | 시간 | 길이 | 목적 | 시각 구성 |
|---|---|---|---|---|
| **S1** | 0:00–0:05 | 5s | 타이틀 — 인물·시대·단원 | 중앙 명조 인물명, 부제 시대·장소, 우하단 단원번호 |
| **S2** | 0:05–0:15 | 10s | 인물 등장 — 시대·장소·역할 | 좌측 SVG 심볼 + 우측 소개 텍스트 2~3줄 |
| **S3** | 0:15–0:32 | 17s | 결정적 순간 — 발견·문제의 메타포 | 전체 화면, 핵심 SVG, 텍스트 최소 |
| **S4** | 0:32–0:45 | 13s | 수학과의 연결 — 오늘 배울 개념 | 수학 다이어그램 SVG + "오늘 우리는 ___ 를 배웁니다" |
| **S5** | 0:45–0:50 | 5s | 마무리 — 단원 안내 | "이 단원에서 그를 만나봅시다" + 단원명 |

**나레이션 분량**: 한국어 240~270자 (TTS 5~5.5자/초 기준)
**톤**: 이야기체 현재 진행형. "강의"가 아닌 "이야기".

---

## 3. 현재 기술 스택 (v1)

### 3.1 도구 버전

| 단계 | 도구 | 버전 |
|---|---|---|
| TTS | edge-tts | 7.2.8 |
| 나레이션 보이스 | ko-KR-SunHiNeural | (edge-tts 기본) |
| 애니메이션 컴포지션 | GSAP 3.14 | CDN |
| 브라우저→영상 렌더 | HyperFrames | 0.4.42 |
| 영상+음성 합성 | FFmpeg | 8.1 |
| 빌드 스크립트 | Python | 3.x |
| OS | Windows 11 | PowerShell / bash |

### 3.2 디렉토리 구조

```
90_video/
├── _docs/STORY_VIDEO_GUIDE.md    ← SSOT 명세
├── _templates/story-master.html  ← 5장면 마스터 템플릿 ({{PLACEHOLDER}} 16개)
├── _assets/
│   ├── palettes.css              ← 13단원 × 5 컬러 토큰 (CSS class .unit-NN)
│   └── symbols/                  ← 14개 SVG (currentColor, theme 자동 적용)
│       ├── star.svg, scroll.svg, book.svg, sun.svg
│       ├── compass.svg, balance.svg, coord-axes.svg, ruler.svg
│       ├── circle-sector.svg, polyhedra.svg, infinity.svg
│       ├── lamp.svg, sieve-grid.svg, coxcomb.svg
├── _plan/
│   ├── build_index.py            ← config.json + 템플릿 → index.html
│   └── render_all.py             ← 전체 파이프라인 실행
└── unit01~13/
    ├── storyboard.md             ← 5장면 설계 (NCC 작성)
    ├── narration.txt             ← 한국어 나레이션 텍스트
    ├── config.json               ← 템플릿 주입 데이터
    ├── index.html                ← build_index.py 출력 (자동 생성)
    ├── narration.mp3             ← edge-tts 출력
    ├── raw.mp4                   ← HyperFrames 출력 (영상만)
    ├── final.mp4                 ← FFmpeg 합성 최종 ⭐
    └── feedback_hitl.md          ← Nick 검토용 작업판
```

---

## 4. 전체 파이프라인 — 단계별 구현

### 4.1 Phase 0 — 콘텐츠 기획

**입력**: 단원 번호, 인물명, story.md (인물 배경 리서치 문서)
**출력**: `storyboard.md`, `narration.txt`, `config.json`

#### storyboard.md 구조
```markdown
# Unit NN Storyboard — 인물명

## S1 타이틀 (0~5s)
...
## S2 인물 등장 (5~15s)
...
## S3 결정적 순간 (15~32s)
...
## S4 수학 연결 (32~45s)
...
## S5 마무리 (45~50s)
...
```

#### config.json 구조 (빌드 주입용)
```json
{
  "person": "에라토스테네스",
  "era": "BCE 3세기 · 알렉산드리아",
  "unit_title": "Unit 01 — 소인수분해",
  "duration": 46,
  "s2_head": "도서관에서 일하던 한 학자",
  "s2_body": "그는 세상의 모든 책을 읽었습니다...",
  "s2_symbol": "scroll",
  "s3_keyword": "체로 거르다",
  "s3_text": "수를 체로 거르면, 소수만 남는다",
  "s3_symbol": "sieve-grid",
  "s4_head": "오늘 우리는",
  "s4_text": "수를 소인수로 분해하는 방법을 배웁니다",
  "s4_symbol": "star",
  "s5_text": "이 단원에서, 에라토스테네스를 만나봅시다"
}
```

### 4.2 Phase 1 — HTML 컴포지션 생성 (`build_index.py`)

**입력**: `config.json` + `_templates/story-master.html` + `_assets/symbols/*.svg`
**출력**: `unitNN/index.html`

핵심 구현:
- 템플릿의 `{{PLACEHOLDER}}` 16개를 config.json 값으로 치환
- SVG 심볼을 파일에서 읽어 인라인으로 주입 (외부 의존성 없음)
- 단원 팔레트 클래스 (`class="unit-01"`) 적용

#### story-master.html 핵심 구조

```html
<!DOCTYPE html>
<html>
<head>
  <!-- palettes.css + GSAP CDN -->
</head>
<body class="{{UNIT_NN}}">
<div id="root" data-duration="{{DURATION}}" data-id="{{COMPOSITION_ID}}">

  <!-- S1: 타이틀 -->
  <div class="scene s1">
    <h1 class="person-name">{{PERSON}}</h1>
    <p class="era">{{ERA}}</p>
    <p class="unit-label">{{UNIT_TITLE}}</p>
  </div>

  <!-- S2: 인물 등장 -->
  <div class="scene s2">
    <div class="symbol">{{S2_SYMBOL}}</div>
    <div class="text-block">
      <h2>{{S2_HEAD}}</h2>
      <p>{{S2_BODY}}</p>
    </div>
  </div>

  <!-- S3: 결정적 순간 -->
  <div class="scene s3">
    <div class="metaphor">{{S3_METAPHOR}}</div>
    <p class="keyword">{{S3_KEYWORD}}</p>
    <p class="text">{{S3_TEXT}}</p>
  </div>

  <!-- S4: 수학 연결 -->
  <div class="scene s4">
    <div class="diagram">{{S4_DIAGRAM}}</div>
    <h2>{{S4_HEAD}}</h2>
    <p>{{S4_TEXT}}</p>
  </div>

  <!-- S5: 마무리 -->
  <div class="scene s5">
    <p class="closing">{{S5_TEXT}}</p>
  </div>
</div>

<script>
  const DUR = parseFloat(document.getElementById('root').dataset.duration) || 50;
  const SCALE = DUR / 51;   // 실제 오디오 길이에 비례 타이밍 조정
  const T = {
    s1: 0.0,
    s2: 5.0 * SCALE,
    s3: 15.0 * SCALE,
    s4: 32.0 * SCALE,
    s5: 45.0 * SCALE,
    end: 50.0 * SCALE
  };

  const tl = gsap.timeline();
  // 각 장면 fade-in, 이전 장면 fade-out
  tl.to(".s1", { opacity: 1, duration: 1 }, T.s1)
    .to(".s1", { opacity: 0, duration: 1 }, T.s2 - 1)
    .to(".s2", { opacity: 1, duration: 1 }, T.s2)
    ...
</script>
</body>
</html>
```

**핵심 설계 결정**: `SCALE = DUR / 51`
- TTS 실제 길이(45~47초)가 예상(50초)과 다를 때 타이밍 자동 보정
- HyperFrames seek 호환을 위해 `tl.call()` 미사용

### 4.3 Phase 2 — TTS (`edge-tts`)

```bash
python -m edge_tts \
  --voice ko-KR-SunHiNeural \
  --file narration.txt \
  --write-media narration.mp3
```

**실제 측정치**: 250자 → 약 45초 (5.5자/초)

### 4.4 Phase 3 — 오디오 길이 측정 + config 갱신

```python
# ffprobe로 정확한 초 단위 길이 측정
r = subprocess.run(
    ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
     "-of", "csv=p=0", str(mp3_path)],
    capture_output=True, text=True
)
dur = float(r.stdout.strip())
target_dur = math.ceil(dur) + 1  # 1초 여백

# config.json 업데이트 → index.html 재빌드
cfg["duration"] = target_dur
config_json.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))
subprocess.run(["python", "build_index.py", unit_num], shell=True)
```

### 4.5 Phase 4 — 영상 렌더 (`HyperFrames`)

```bash
hyperframes render ./unit01 -o ./unit01/raw.mp4 -f 24 -q standard
```

- HyperFrames = Puppeteer 기반 브라우저 렌더러 (HTML+CSS+JS → MP4)
- GSAP 타임라인을 프레임 단위로 seek하며 캡쳐
- **Windows 이슈**: subprocess PATH 미인식 → `shell=True` 우회

```python
def run(cmd: list, **kwargs):
    shell_cmd = " ".join(f'"{c}"' if " " in str(c) else str(c) for c in cmd)
    return subprocess.run(shell_cmd, shell=True, **kwargs)
```

### 4.6 Phase 5 — 영상+음성 합성 (`FFmpeg`)

```bash
ffmpeg -y \
  -i raw.mp4 \
  -i narration.mp3 \
  -map 0:v -map 1:a \
  -c:v copy -c:a aac \
  -shortest \
  final.mp4
```

- `-shortest`: 영상/오디오 중 짧은 쪽에서 종료 (sync 보장)
- `-c:v copy`: 재인코딩 없이 비디오 스트림 복사 (속도 최적화)

---

## 5. v1 결과물 요약

| Unit | 인물 | 길이 | 파일 크기 |
|---|---|---|---|
| 01 | 에라토스테네스 | 45.07s | 1.22MB |
| 02 | 브라마굽타 | 42.46s | 1.50MB |
| 03 | 알콰리즈미 | 41.81s | 1.46MB |
| 04 | 디오판토스 | 43.20s | 1.32MB |
| 05 | 데카르트 | 41.69s | 1.35MB |
| 06 | 데카르트(2) | 45.05s | 1.36MB |
| 07 | 유클리드 | 46.82s | 1.32MB |
| 08 | 유클리드(2) | 39.43s | 1.42MB |
| 09 | 가우스 | 44.23s | 1.44MB |
| 10 | 아르키메데스 | 45.26s | 1.63MB |
| 11 | 케플러 | 47.52s | 1.57MB |
| 12 | 카발리에리 | 39.17s | 1.53MB |
| 13 | 나이팅게일 | 44.11s | 1.40MB |

**합계**: 13개 · ~19MB · 평균 43초

---

## 6. v1 한계 진단

| 차원 | 현 상태 | 문제 |
|---|---|---|
| **시각 품질** | 텍스트 + 14종 SVG 심볼 | 정적, 시대 분위기·인물감 없음 |
| **나레이션** | edge-tts SunHiNeural 1보이스 | 단조로움, 감정 없음, 13명 동일 목소리 |
| **길이** | 평균 43초 | story.md 본문의 ~10%만 담김 |
| **음악·SFX** | 없음 | 분위기 형성 불가 |
| **화면 구성** | 5장면 고정 | 단원별 차별화 없음, 유연성 낮음 |
| **렌더러** | HyperFrames | Windows 경로 이슈, inline-asset만 지원 |
| **검수** | NCC 단독 | 교육자·학습자 시점 부재 |

---

## 7. 품질 향상·자동화를 위한 Research 방향

### 7.1 렌더러 교체 — HyperFrames 대안

**현재 문제**: HyperFrames는 내부 HTML+JS 렌더링에는 적합하지만:
- Windows에서 subprocess PATH 문제 (shell=True 우회)
- inline asset만 지원 (외부 이미지 참조 불가)
- 라이브 프리뷰 없음 → 개발 사이클 느림

**Research 후보**:

1. **Motion Canvas** (TypeScript, https://motioncanvas.io)
   - Manim의 JS/TS 변형. React 아님. 자체 렌더러 + 라이브 프리뷰
   - 코드로 장면을 선언적으로 작성. ffmpeg 출력 내장
   - 현 GSAP HTML 자산 재작성 필요하지만 API 훨씬 더 깔끔
   - **Research 포인트**: Windows 지원 여부, 한국어 폰트 렌더링, ffmpeg 파이프라인 통합 방법

2. **Remotion** (React+TypeScript, https://www.remotion.dev)
   - React 컴포넌트로 영상 작성. Remotion Studio로 라이브 프리뷰
   - HyperFrames와 동일 원리(브라우저 렌더)지만 훨씬 성숙
   - 현 palettes.css 등 CSS 자산 재사용 가능
   - **Research 포인트**: @remotion/player로 웹 임베드 동시 가능 여부, Windows 성능

3. **Puppeteer 직접** (Node.js)
   - HyperFrames 내부도 Puppeteer 사용. 직접 제어 = 더 유연
   - 외부 이미지/폰트 처리, 커스텀 렌더 루프 가능
   - **Research 포인트**: ffmpeg pipe 연동, 24fps seek 정밀도

4. **Manim Community** (Python, https://github.com/ManimCommunity/manim)
   - 수학 시각화 최강. 3Blue1Brown 스타일
   - 한글 폰트 설정 + LaTeX 필요
   - **우리 케이스**: Story 영상(인물 서사)보다 Concept 영상(수학 시각화)에 적합
   - **Research 포인트**: 한국어 폰트 통합, 인물 일러스트 이미지 포함 방법, Windows 설치

### 7.2 TTS 업그레이드

**현재 문제**: edge-tts SunHiNeural은 품질 6/10. 모든 단원 동일 목소리.

**Research 후보**:

1. **ElevenLabs** (https://elevenlabs.io)
   - 한국어 Multilingual v2 모델
   - 감정 표현, 속도·톤 조절 가능
   - 캐릭터별 보이스 커스텀 가능 (노년 학자 vs 청년 등)
   - **Research 포인트**: 한국어 자연스러움 수준, API 가격, 월 무료 tier, Python SDK 통합

2. **OpenAI TTS** (GPT-4o Audio, https://platform.openai.com/docs/guides/audio)
   - onyx, nova, shimmer 등 다중 보이스
   - 한국어 자연도 높음
   - **Research 포인트**: 감정 프롬프팅 가능 여부, 한국어 전용 최적화 여부

3. **Bark** (OSS, https://github.com/suno-ai/bark)
   - 감정 표현 + SFX 통합
   - 로컬 실행 가능 (GPU 있으면 빠름)
   - **Research 포인트**: Windows GPU 없을 때 CPU 실행 속도, 한국어 품질

4. **Tortoise TTS** (OSS, 음성 클로닝)
   - 특정 화자 음성 클로닝 가능
   - **Research 포인트**: 로컬 실행 환경 요구사항, 한국어 지원

**핵심 Research 질문**: 인물별 다른 보이스 적용 시 파이프라인 수정 범위?
- config.json에 `"voice": "ElevenLabs_voice_id"` 추가로 단순 확장 가능

### 7.3 AI 이미지 생성 — 인물·배경 일러스트

**현재 문제**: 14개 SVG 심볼만 사용. 인물 얼굴·시대 배경 이미지 없음.

**Research 후보**:

1. **Stable Diffusion + ControlNet + LoRA** (로컬)
   - 캐릭터 일관성 유지 최강 (LoRA 학습)
   - 스타일 통일 (13명이 같은 일러스트 스타일)
   - **Research 포인트**: 역사 인물 레퍼런스 이미지 없을 때 프롬프트 전략, 한복/이슬람/고대 그리스 의상 정확도, Windows에서 ComfyUI 설치

2. **OpenAI GPT-4o Image** (API)
   - 프롬프트만으로 빠른 결과
   - 일관성은 LoRA보다 낮음
   - **Research 포인트**: 캐릭터 참조 이미지 없이 동일 스타일 유지 방법

3. **Adobe Firefly Custom Models** (유료)
   - 2026 기준 캐릭터·스타일 일관성 크게 향상
   - **Research 포인트**: API 접근 방법, 커스텀 모델 학습 cost

4. **SVG 생성** (AI → SVG 변환)
   - 이미지 → potrace → SVG 트레이스
   - 또는 직접 SVG 코드 생성 (Claude 사용)
   - **Research 포인트**: 인물 실루엣 SVG 자동 생성 파이프라인

### 7.4 배경음악·SFX 자동화

**현재**: 없음. 정적.

**Research 방향**:

1. **Mubert API** — 텍스트 프롬프트 → 배경음악 자동 생성
   - `"ambient ancient egypt"` → 5~10초 루프
   - **Research 포인트**: API 가격, Python SDK, 라이선스 명확성

2. **Freesound.org API** — 키워드 검색 → CC 효과음 다운로드
   - **Research 포인트**: Python 클라이언트, 자동화 파이프라인

3. **FFmpeg 음악 믹싱**
   - 배경음악 -30dB + 나레이션 0dB 믹스
   - `ffmpeg -i voice.mp3 -i bgm.mp3 -filter_complex amix=inputs=2:duration=shortest`

### 7.5 파이프라인 자동화 개선

**현재 제약**:
- HyperFrames가 Windows subprocess에서 PATH 인식 불안정
- 단계별 오류 시 중간 상태 추적 어려움
- 렌더 중 진행 상황 모니터링 없음

**Research 방향**:

1. **Makefile / Task runner (Just, Taskfile.yml)**
   - 단계별 의존성 선언 → 중간 산출물 있으면 skip
   - `just render unit=01` 같은 인터페이스

2. **상태 추적 DB (SQLite 또는 JSON)**
   - 각 단원 × 단계 상태 기록 (pending/running/done/failed)
   - 재시도 시 이어서 시작

3. **병렬 렌더링**
   - Python `concurrent.futures` 또는 `asyncio`
   - TTS 13개 동시 실행 (API I/O bound)
   - 렌더는 CPU bound → GPU 있으면 Manim/Motion Canvas 병렬 가능

4. **Docker 컨테이너화**
   - edge-tts + ffmpeg + HyperFrames/Puppeteer 환경 재현
   - Windows 종속성 문제 해결
   - **Research 포인트**: Puppeteer in Docker headless Chrome, ffmpeg GPU 가속

### 7.6 스토리 스크립트 품질 향상

**현재**: NCC(Claude) 단독 작성. 1인 시점, 검수 없음.

**Research 방향**:

1. **멀티 페르소나 검수 (즉시 구현 가능)**
   - `/se_audit_storyteller` — 내러티브 전문가 관점
   - `/se_audit_educator` — 수학 교사 관점 (교육 정확성)
   - `/se_audit_designer` — 시각 구성 관점
   - `/se_audit_learner` — 학습자(중1 여학생) 관점 시뮬레이션

2. **story.md → 영상 스크립트 확장 자동화**
   - 현재: 200줄 story.md → 250자 나레이션 (90% 손실)
   - 목표: 600~800자 → 90~120초 영상
   - Claude API로 스타일 가이드 따른 자동 확장

3. **대화체 전환**
   - 에라토스테네스 ↔ 아르키메데스 (실제 편지 교환 기록)
   - 유클리드 ↔ 프톨레마이오스 왕 (왕도 없다)
   - 2인 대화 = 학생 몰입 증가

### 7.7 영상 길이 정책 재검토

**현재**: 50초 목표 (실제 43초 평균)

| 옵션 | 특징 | 적합성 |
|---|---|---|
| 50초 유지 | 현재 인프라 그대로 | attention span 최우선 |
| **90~120초** | story.md 30%까지 담음 | 권장 — 호흡 자연스러움 |
| 2분 이상 | story.md 50%+ | 섹션 단위로 유연하게 |
| 시리즈 (3~4편) | 단원당 여러 클립 | 추후 (v2+) |

**Research 포인트**: 중학생 교육 영상 최적 길이 연구 (30s vs 60s vs 120s 학습 효과 비교)

---

## 8. 권장 진화 로드맵

| 버전 | 핵심 변화 | 기간 | 품질 |
|---|---|---|---|
| **v1** | 현재 (완료) | — | 6/10 |
| **v1.5** | AI 이미지 인물 일러스트 + ElevenLabs TTS + 90~120초 | 1~2주 | 7.5/10 |
| **v2** | 멀티 페르소나 검수 + 배경음악 + story.md 확장 | 2~3주 | 8/10 |
| **v3** | Motion Canvas / Remotion 렌더러 교체 (파일럿: 1단원) | 3~4주 | 9/10 |
| **v4** | Manim 도입 (Concept 영상 별도 트랙) | 4~6주 | 9.5/10 |
| **v5** | 단원당 시리즈 3~5편 + 인터랙티브 요소 | 분기 단위 | 10/10 |

---

## 9. Deep Research 질문 목록

Claude Desktop에 다음 질문들을 던지기 위한 입력 자료:

### Q1. 렌더러 비교
```
Motion Canvas vs Remotion vs Puppeteer 직접 사용 비교:
- 교육용 단편 영상(50~120초) 제작 파이프라인으로 어느 것이 더 적합?
- Windows 환경 지원, 한국어 폰트 처리, ffmpeg 통합 용이성, 학습곡선 비교
- HyperFrames(HTML+GSAP → ffmpeg) 대비 Migration 비용 추정
```

### Q2. TTS 한국어 품질
```
ElevenLabs vs OpenAI TTS vs edge-tts: 한국어 교육 콘텐츠용 비교
- 감성 표현(속도 조절, 감정톤), API 가격, Python 통합 용이성
- 역사 인물 페르소나(노년 학자, 청년 수학자 등) 다른 목소리로 구현 방법
```

### Q3. AI 이미지 일관성
```
교육 영상용 역사 인물 일러스트 생성:
- 특정 시대(BCE, 중세, 17세기)·지역(알렉산드리아, 인도, 프랑스) 배경 이미지 품질
- 13개 단원 전체 동일 아트스타일 유지 방법 (LoRA vs style transfer)
- Stable Diffusion ComfyUI workflow vs OpenAI API 비교 (로컬 GPU 없을 때)
```

### Q4. 파이프라인 자동화
```
영상 제작 파이프라인 자동화 best practice 2026:
- storyboard.md → narration → 이미지 생성 → 렌더 → 합성의 각 단계 캐싱
- 병렬 처리 (TTS API는 I/O bound, 렌더는 CPU bound)
- Windows 환경에서 Makefile 대안 (Just, Taskfile, Poetry scripts)
```

### Q5. 교육 영상 길이 최적값
```
중학생(12~13세) 대상 수학 개념 소개 영상의 최적 길이:
- 30초 vs 60초 vs 2분 영상의 학습 동기 유발 효과 비교 연구
- 인트로/흥미 유발 목적(개념 설명 아님)에서 적정 길이
- 유튜브 교육 채널 데이터 (시청 완료율 vs 길이 상관관계)
```

### Q6. Manim 한국어 워크플로우
```
Manim Community Python 라이브러리:
- Windows 11에서 설치·셋업 (LaTeX + 한국어 폰트)
- 역사 인물 이미지를 포함한 Manim 씬 작성 방법
- 수학 애니메이션(소인수분해 과정 시각화)과 인물 서사 혼합 방법
- 생성된 영상을 ffmpeg으로 후처리 방법
```

---

## 10. 참고 파일 위치

| 파일 | 설명 |
|---|---|
| `90_video/_docs/STORY_VIDEO_GUIDE.md` | v1 SSOT 명세 (전체 원칙·구조) |
| `90_video/_templates/story-master.html` | 5장면 마스터 템플릿 |
| `90_video/_assets/palettes.css` | 13단원 컬러 토큰 |
| `90_video/_plan/build_index.py` | 빌드 스크립트 |
| `90_video/_plan/render_all.py` | 렌더 파이프라인 |
| `90_video/unit01/config.json` | 단원 데이터 예시 |
| `80_professional_idea/260515_pro_video_pipeline_brainstorm.md` | 브레인스토밍 (OSS 지도, NCC 의견) |
| `90_video/_docs/REVIEW_GUIDE.md` | Nick 검토 가이드 (v1 품질 평가 기준) |
