<!-- STORY_VIDEO_v1_5.md -->

# Story Video Pipeline — v1.5

> **이전 위치**: `channel/_docs/PIPELINE_v1_5.md` (2026-05-21 이동).
> 이 문서가 v1.5 영상의 SSOT. 모든 단원 v1.5 영상은 여기 명세를 따른다.
>
> v1(50초·SVG)에서 v1.5(110초·AI 이미지)로의 진화. v2(Motion Canvas)까지의 중간 단계.

---

## 0. v1과의 차이

| 항목 | v1 | v1.5 | v2 (예정) |
|---|---|---|---|
| 길이 | 50초 | **110초 (95~120)** | 90~180s 자유 |
| 장면 수 | 5 | **6** | 자유 |
| 시각 자원 | SVG 심볼 5종 | **AI 이미지 4~6장** + SVG | 컴포넌트 |
| 모션 | fade only | **fade + ken burns + parallax** | timeline framework |
| 나레이션 | edge-tts | edge-tts (→ ElevenLabs 예정) | ElevenLabs |
| 나레이션 분량 | 240~270자 | **480~600자** | 가변 |
| 엔진 | HTML+GSAP / HyperFrames | 동일 | Motion Canvas |
| 표준 시간 | 1주/단원 | 2~3일/단원 | 1주/단원 |

**v1.5의 정체성**: "시대를 보여주고, 인물을 천천히 만나게 하는 호흡". 시각이 SVG 추상에서 사진/일러스트로 진화하면서 학습자가 "그 시대에 있는 듯한" 감각을 얻는다.

---

## 1. 6-Scene 구조

| 장면 | 시간 | 길이 | 목적 | 시각 주체 | 나레이션 |
|---|---|---|---|---|---|
| **S1** | 0:00–0:05 | 5s | 타이틀 — 인물·시대·단원 노출 | 텍스트 (정적 배경) | 20~25자 |
| **S2** | 0:05–0:25 | 20s | 시대·장소 풍경 (**v1.5 NEW**) | AI 이미지 1 (ken burns) | 80~100자 |
| **S3** | 0:25–0:50 | 25s | 인물 등장 — 일과·고민 | AI 이미지 2 + 텍스트 | 110~130자 |
| **S4** | 0:50–1:20 | 30s | 결정적 순간 — 발견·실험 | AI 이미지 3 (또는 2장 cross) | 140~160자 |
| **S5** | 1:20–1:45 | 25s | 수학과의 연결 — "오늘 우리는" | 다이어그램 SVG + AI 이미지 4 | 110~130자 |
| **S6** | 1:45–1:55 | 10s | 마무리 — "이 단원에서 만남" | 텍스트 + 작은 AI 이미지 | 30~40자 |

**합계**: 110초 / 490~585자.

### 1.1 v1 → v1.5 매핑
```
v1  S1 ──────────────── v1.5 S1   (변화 없음, 길이 동일)
                  ↓ NEW
                  v1.5 S2   (시대 풍경, 호흡)
v1  S2 ──────────────── v1.5 S3   (길이 1.5배, AI 이미지로 강화)
v1  S3 ──────────────── v1.5 S4   (길이 ~2배, 2장면처럼 길게)
v1  S4 ──────────────── v1.5 S5   (길이 2배, 더 자세히)
v1  S5 ──────────────── v1.5 S6   (길이 2배, 여운)
```

### 1.2 장면 전환 규칙
- 모든 전환: **1초 fade**
- 장면 내 ken burns: 이미지 `scale: 1.0 → 1.08` 또는 `x: 0 → -3%` 천천히
- S4가 가장 긴 장면 — 중간에 텍스트 강조구절 1회 (스파이크)
- 나레이션 새 문장 시작 = 새 장면 또는 새 강조

---

## 2. AI 이미지 명세

### 2.1 장면당 이미지 수
- S2: 1장 (시대 풍경 wide, 16:9, 1280×720)
- S3: 1장 (인물 medium shot, 16:9 또는 인물 cutout)
- S4: 1~2장 (결정적 순간; 2장이면 cross-dissolve)
- S5: 1장 (현대로의 연결 — 칠판, 책, 도구 등)
- S6: 0~1장 (선택, 작게)

→ **단원당 4~6장 표준**

### 2.2 프롬프트 작성 원칙
1. **시대 정확성**: 의상·소품·건축 양식 키워드 명시
2. **인물 일관성**: 같은 단원 내 인물은 같은 외모 묘사 (나이·복장·머리색)
3. **톤 일관성**: `system/context/ERA_PALETTES.md` 시대 팔레트와 맞게
4. **여백 확보**: 텍스트가 들어갈 좌측/우측/상단/하단 공간 — 프롬프트에 `negative space on left` 등 명시
5. **16:9 종횡비**: 모든 프롬프트에 `aspect ratio 16:9` 또는 도구별 옵션
6. **금기**: 텍스트(글자), 시계 같은 시대 anachronism, 현대 의상, AI 워터마크

### 2.3 프롬프트 시트 위치
- 단원별: `channel/season-X/unit-NN/image_prompts.md`
- 각 프롬프트마다: scene 번호 · 파일명 · 영문 프롬프트 · negative · style notes

### 2.4 이미지 저장 위치
```
channel/season-1-ancient/unit-01/
└── _assets/
    ├── s2-alexandria-vista.png
    ├── s3-library-scholar.png
    ├── s4-shadow-experiment.png
    ├── s5-numbers-bridge.png
    └── s6-closing-light.png
```
- 포맷: PNG (Claude/ChatGPT 생성 기본), JPG도 허용
- 해상도: 1280×720 또는 1920×1080 (다운스케일 허용)
- 파일명: `s{장면번호}-{slug}.{ext}` snake-kebab

### 2.5 ε storage 적용
- `.jpg/.png`는 **gitignore** (재생성 가능한 자산으로 간주)
- 단, `image_prompts.md`는 git에 포함 (재생성 가능하게 함)
- 최종 적용된 final.mp4는 GitHub Releases

---

## 3. Tech Stack (v1과 동일)

| 단계 | 도구 | 비고 |
|---|---|---|
| 이미지 | Claude/ChatGPT 이미지 생성 | (Nick) 향후 SD/MJ 전환 — Nick_TODO 참조 |
| TTS | edge-tts ko-KR-SunHiNeural | (향후) ElevenLabs — Nick_TODO 참조 |
| 컴포지션 | HTML + GSAP 3.14 + AI 이미지 | CDN |
| 렌더 | HyperFrames | 영상만 (raw.mp4) |
| 합성 | FFmpeg | 영상 + TTS 음성 → final.mp4 |

### 3.1 edge-tts 운영 노트 (Unit 01 검증)
- SSML(`<break>`, `<prosody>`)은 **edge-tts CLI에서 동작하지 않음** — 태그가 그대로 읽힘
- 휴지(pause)는 **단문 + 빈 줄**로 자연스럽게 확보
- 천천히 읽기: `--rate=-5%` (5자/초보다 약간 느려져 110초 안에 480~620자 안착)
- 음성: ko-KR-SunHiNeural (다정한 어조). ko-KR-InJoonNeural은 강의 톤.
- 자세한 톤 가이드: `system/context/TONE_GUIDE.md`

---

## 4. 파이프라인 단계

```
[1] storyboard.md (v1.5, 6장면)
    │
[2] narration.txt (480~600자, 6장면 분량)
    │
[3] image_prompts.md (AI 이미지 4~6장 프롬프트)
    │
    ▼ (3a) Nick이 Claude/ChatGPT에 프롬프트 복붙 → 이미지 생성 → _assets/ 저장
    │
[4] config.json (장면별 텍스트 + 이미지 파일명 + 팔레트)
    │
[5] index.html (v1.5 템플릿 + 단원 데이터)
    │
    ▼ edge-tts --rate=-5% narration.txt > narration.mp3
[6] narration.mp3
    │
    ▼ ffprobe로 길이 측정 → AUDIO_DURATION
    │
    ▼ index.html data-duration 자동 갱신 (audio + 2s 여유)
    │
    ▼ hyperframes render
[7] raw.mp4 (영상만, 95~120초)
    │
    ▼ ffmpeg -map 0:v -map 1:a -c:v copy -c:a aac -shortest
[8] final.mp4 ⭐
    │
    ▼ retrospective 자동 작성
[9] system/insights/{YYMMDD}_unitNN_story_video_v1_5.md
```

---

## 5. Rules (위반 시 audit fail)

### 5.1 시간·길이
- [ ] 총 길이 95~120초 범위
- [ ] 6장면 모두 존재, 시간이 누락 없이 흐름
- [ ] S4(결정적 순간)가 가장 김 (25~30s)

### 5.2 이미지
- [ ] AI 이미지 4장 이상
- [ ] 모든 이미지 16:9 종횡비
- [ ] 이미지 안에 글자(텍스트) 없음
- [ ] 시대·문화·복식 anachronism 없음
- [ ] 인물 일관성 — 같은 단원 안 인물은 같은 얼굴

### 5.3 텍스트·나레이션
- [ ] 한국어 나레이션 480~620자
- [ ] 한자어·전문용어 최소
- [ ] 영문 약자 첫 등장 시 한국어 병기
- [ ] 5자/초 기준 TTS 속도 정상 (95~120초 안에 들어옴)
- [ ] 강의 톤 X, 이야기 톤 ✓
- [ ] SSML 태그 사용 금지 (edge-tts에서 동작 X)

### 5.4 시각 디자인
- [ ] 시대 팔레트 일관 적용 (`era-ancient`, `era-india` 등 — ERA_PALETTES.md)
- [ ] 한 화면에 텍스트 + 강한 시각 = 3개 이하 요소
- [ ] 여백 30% 이상 유지

### 5.5 기술 산출물
- [ ] final.mp4 < 25MB (1280×720, AAC 128k)
- [ ] sync 오차 ±0.3초 이내
- [ ] poster.jpg 추출 가능 (S1 화면)

### 5.6 진화 메커니즘
- [ ] retrospective 작성 (`system/insights/`)
- [ ] insights/_index.md에 한 줄 등록

---

## 6. Skill 호출

- **자동화**: `/se_story_video_v1_5 unit-01`
- **수동 단계**: storyboard → narration → 프롬프트 → (Nick 이미지 생성) → config → 빌드
- **참고 skill**:
  - `/se-people-narrate` — 내러티브 텍스트 작성 (구 `/se-story-write` 폐기, 일원화)
  - `/se_video_make` — 영상 빌드 (v1 호환)

---

## 7. 디렉토리 구조

```
channel/
├── _templates/
│   └── story-master-v1_5.html     (6장면 마스터)
├── _assets/                       (공용 자원 — 폰트, 팔레트)
│   └── palettes.css
└── season-1-ancient/
    └── unit-01/
        ├── storyboard_v1_5.md
        ├── narration_v1_5.txt
        ├── image_prompts.md       (v1.5 NEW)
        ├── config_v1_5.json
        ├── index_v1_5.html
        ├── _assets/               (v1.5 NEW — gitignored 이미지)
        │   ├── s2-*.png
        │   └── ...
        ├── narration_v1_5.mp3     (gitignored)
        ├── raw_v1_5.mp4           (gitignored)
        └── final_v1_5.mp4         (gitignored — Releases)
```

---

## 8. 변경 이력

| 버전 | 날짜 | 변경 |
|---|---|---|
| v1.5.0 | 2026-05-20 | 초안. v1 → v1.5 진화 명세. 6장면 구조 확정, AI 이미지 명세 추가. |
| v1.5.1 | 2026-05-21 | system/principles/로 이동. SSML 사용 금지 명시, --rate=-5% 표준화, retrospective 의무화 (§5.6). TONE_GUIDE / ERA_PALETTES 참조 분리. |
