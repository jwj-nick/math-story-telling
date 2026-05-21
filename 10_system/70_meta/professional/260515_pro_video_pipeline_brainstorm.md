<!-- 260515_pro_video_pipeline_brainstorm.md -->

# Story 영상 — "전문화" 브레인스토밍

> NCC 자유 의견, 2026-05-15
> 트리거: Nick — "지금 전체적으로 너무 단순함. story.md 확장, 화면 구성 전문화. 플러그인/OSS/우리 스킬?"
> 외부 research 일부 반영. 단정문 아닌 brainstorm 톤.

---

## 0. 한 줄 정리 (먼저 결론부터)

세 가지 길이 있다.

1. **현 v1 확장형** — 같은 GSAP/HTML 스택에서 story.md 깊이만 확장, 길이 2~3분, AI 이미지 추가
2. **Manim/Motion Canvas 도입** — 수학 시각화 표준에 맞추기 (3Blue1Brown 톤)
3. **Hybrid 멀티 에이전트** — 작가/디자이너/검수자 에이전트를 우리 스킬로 만들기

각각 학습 곡선·결과 품질·작업 시간이 크게 다르다. 아래에서 하나씩.

---

## 1. 현재 v1 한계 진단

| 차원 | 현 상태 | 문제 |
|---|---|---|
| 길이 | 50초 | story.md 본문의 ~10%만 담김. 인물 깊이 얕음 |
| 시각 | 텍스트 + SVG 14종 | 정적, 인물·시대·장소 분위기 약함 |
| 나레이션 | edge-tts SunHiNeural | 단조로움, 감정 표현 없음 |
| 화면 구성 | 5장면 hardcoded | 유연성 낮음. 단원별 차별화 적음 |
| 작가 | NCC 1인 | 시점 단일. 검수 부재 |
| 음악·SFX | 없음 | 분위기 형성 어려움 |

**근본 원인**: 우리는 "최소 가능한 워크플로우"를 만들었음. 의도된 v1. 진화의 출발점.

---

## 2. 외부 OSS / 도구 지도 (2026 기준)

### 2.1 모션그래픽 프로그래밍 라이브러리

| 도구 | 언어 | 특징 | 우리 적합성 |
|---|---|---|---|
| **Manim Community** | Python | 3Blue1Brown 원조. LaTeX 통합, 수학 시각화 최강 | ★★★★☆ — 수학 강함, 한글 폰트는 별도 설정 |
| **ManimGL** | Python (OpenGL) | Grant Sanderson 본인이 쓰는 fork | ★★★☆☆ — 더 빠르지만 less stable |
| **Motion Canvas** | TypeScript | Manim의 JS판. 더 깔끔한 API, 라이브 프리뷰 | ★★★★★ — HyperFrames 대체 후보 |
| **Remotion** | React/TypeScript | 컴포넌트 기반, Remotion Studio 라이브 프리뷰 | ★★★★★ — 개발자 친화, 우리 HTML 자산 재사용 가능 |
| **panim** | Python | Manim 경량판 (OSS) | ★★☆☆☆ |
| **Reanimate** | Haskell | 수학 시각화 | ★☆☆☆☆ (학습곡선) |
| **Makie.jl** | Julia | 과학 시각화 | ★☆☆☆☆ |

### 2.2 화면 구성 / 시각 보강

| 도구 | 용도 | 비고 |
|---|---|---|
| **Lottie (Airbnb)** | After Effects → JSON 애니메이션 | 가벼움, 웹 호환. 인물 표정·동작 가능 |
| **Three.js / Pixi.js** | 3D / GPU 2D | 케플러(우주)·아르키메데스(부력) 등에 유용 |
| **Reveal.js** + 캡쳐 | 슬라이드 → 영상 | 매우 단순. Story 영상엔 부족 |
| **Blender** + Grease Pencil | 2D/3D 통합 | 강력. 학습곡선 ↑ |

### 2.3 AI 이미지 생성 (인물·배경 일러스트)

| 도구 | 특징 | 한국 사용 적합성 |
|---|---|---|
| **Stable Diffusion + ControlNet** | OSS, 로컬 실행 가능. 캐릭터 일관성 위해 LoRA 학습 가능 | ★★★★★ |
| **Adobe Firefly (Custom Models)** | 2026년 캐릭터·일러스트·사진 스타일 커스텀 모델 | ★★★★☆ (유료) |
| **OpenAI DALL-E 3 / GPT-4 image** | API 통합 쉬움 | ★★★★☆ |
| **Veo 3 (Google)** | 이미지 참조 워크플로우 — 캐릭터 일관성 유지 | ★★★☆☆ (preview) |
| **Pika / Runway Gen-3** | 이미지→영상 5초 클립 | ★★☆☆☆ — 비싸지만 가능성 |

**2026년 트렌드**: "Hybrid Workflows" — AI는 배경/시뮬레이션/조명, 핵심 요소는 사람 손/3D. 우리도 이 방향.

### 2.4 TTS 업그레이드 옵션

| 도구 | 품질 | 한국어 |
|---|---|---|
| **edge-tts** (현재) | 6/10 | OK (SunHi, InJoon) |
| **ElevenLabs** | 9/10 | 좋음 (Korean Multilingual) |
| **OpenAI TTS** (Onyx/Nova) | 8/10 | 한국어 자연스러움 ↑ |
| **Tortoise-TTS** (OSS) | 7/10 | 음성 클로닝 (Nick 음성?) |
| **Bark** (OSS) | 7/10 | 감정 + 효과음 |

**제안**: ElevenLabs 한국어 보이스 1~2개 트라이얼 후 결정. (단원별 인물에 따라 보이스 다르게 — 에라토스테네스는 노년 학자, 가우스는 청년 등)

### 2.5 음악·SFX

| 출처 | 라이선스 |
|---|---|
| **Freesound.org** | CC, 효과음 다수 |
| **YouTube Audio Library** | YT용 무료 |
| **Pixabay Music** | CC, 배경음악 |
| **Mubert (AI)** | 텍스트→음악, 라이선스 명확 |

---

## 3. story.md 확장 방향

현 unit01.md (5장 ~200줄) → 영상 50초로 **90% 손실**. 확장 전략:

### 3.1 다층 narrative 분할
한 단원 = 여러 짧은 영상 (each 60~90s):
```
unit01/
├── intro.mp4     (인물 소개, 60s)
├── moment.mp4    (결정적 순간, 90s)
├── concept.mp4   (수학 연결, 60s)
└── legacy.mp4    (오늘의 영향, 45s)
```
총 4~5분. 학생이 한 번에 다 보거나, 시리즈로 한 화씩.

### 3.2 인물 대화체
역사적 친구·라이벌·제자 등장:
- 에라토스테네스 ↔ 아르키메데스 (실제 편지 교환)
- 데카르트 ↔ 페르마 (좌표계 논쟁)
- 유클리드 ↔ 프톨레마이오스 왕 (왕도 없다)
2인 대화는 학생 몰입 ↑

### 3.3 "지금 이 순간" 트랙
인물의 발견 직전 internal monologue. 1인칭:
- "막대기에 그림자가 졌다… 시에네에는 없다는데… 잠깐, 그렇다면…"

### 3.4 시각 메타포 5배 확장
현재 SVG 1개/장면 → 다층:
- 배경 일러스트 (시대 분위기)
- 인물 실루엣 (정적 or 미세 모션)
- 핵심 메타포 (애니메이션)
- 수학 다이어그램 (정확함)
- 텍스트 오버레이

---

## 4. 우리가 만들 수 있는 스킬 (제안)

기존 `/se_story_video`는 v1. 추가 스킬 후보:

### 4.1 작가 트랙 — 글 확장
- `/se_story_expand` — story.md 한 장을 5분 영상용 디테일 스크립트로 확장
- `/se_dialogue_compose` — 2인 대화체 변환
- `/se_narration_polish` — 문장 리듬·낭독 적합성 다듬기

### 4.2 디자이너 트랙 — 시각
- `/se_scene_design` — 한 장면 시각 구성을 디테일 설계 (배경/인물/메타포/텍스트)
- `/se_storyboard_visual` — 텍스트 storyboard → ASCII/SVG 스케치
- `/se_palette_propose` — 인물·시대에 맞는 컬러 팔레트 자동 제안
- `/se_image_brief` — AI 이미지 생성용 프롬프트 작성 (스타일 가이드 포함)

### 4.3 연출 트랙 — 타이밍·페이스
- `/se_animatic` — 풀 렌더 전 저해상도 미리보기 영상 (5초/장면 더미)
- `/se_pacing_check` — 나레이션 vs 시각 동기 검토

### 4.4 검수 트랙 — 멀티 페르소나
- `/se_audit_storyteller` — 스토리텔러 관점 검수
- `/se_audit_educator` — 교육자(수학 교사) 관점 검수
- `/se_audit_designer` — 디자이너 관점 검수
- `/se_audit_learner` — 학습자(딸) 관점 시뮬레이션

→ 단원당 4명의 페르소나가 자동 리뷰 + 종합 의견.

### 4.5 통합 워크플로우
```
/se_story_pro unit=01 length=180
  Stage 1: /se_story_expand → expanded.md (3분 분량)
  Stage 2: /se_scene_design (6~8장면) → scenes.md
  Stage 3: /se_image_brief → AI image prompts
  Stage 4: [Nick 검토 라운드]
  Stage 5: /se_narration_polish → narration.txt
  Stage 6: TTS (ElevenLabs)
  Stage 7: /se_animatic → preview.mp4 (60s 저해상도)
  Stage 8: [Nick 검토 라운드]
  Stage 9: Manim/Motion Canvas 풀 렌더 → final.mp4
  Stage 10: 4명 페르소나 audit → feedback.md
```

---

## 5. 권장 진화 단계 (구체)

| 버전 | 변화 | 기술 | 작업량 | 결과 품질 |
|---|---|---|---|---|
| v1 | 현재 | GSAP + edge-tts + HyperFrames | (완료) | 6/10 |
| **v1.5** | AI 이미지 + 길이 90~120초 + 단원별 보이스 | + Stable Diffusion + ElevenLabs | 1~2주 | 7.5/10 |
| **v2** | story.md 확장 + 멀티 페르소나 검수 + 음악 | + /se_story_expand + /se_audit_* | 2~3주 | 8/10 |
| **v3** | Motion Canvas / Remotion 도입 (1개 단원 파일럿) | + TypeScript 스택 | 3~4주 | 9/10 |
| **v4** | Manim 풀 도입 (수학 시각화 강화) | + Python 스택 | 4~6주 | 9.5/10 |
| **v5** | 시리즈 영상 (단원당 3~5개) + 인터랙티브 | + Lottie / Pixi | 분기 단위 | 10/10 |

---

## 6. NCC 개인 의견 (자유)

### 6.1 가장 효과적인 첫 진화: **v1.5**

이유:
- v1 인프라 그대로 활용 (GSAP, HyperFrames, ffmpeg)
- 핵심 가치 추가: **인물 일러스트** + **다양한 보이스** + **길이 1.5~2배**
- 1~2주 안에 결과
- v2, v3 결정을 위한 좋은 베이스

작업 내용:
1. `90_video/_assets/portraits/` 에 13인 일러스트 (AI 생성, 단원당 1~2장)
2. ElevenLabs 한국어 보이스 13개 매핑 (인물 나이·성별 반영)
3. 마스터 템플릿 v2: 8장면 → 90~120초 형식
4. `_assets/backgrounds/` 시대 배경 SVG/이미지

### 6.2 야심 있게 가고 싶다면: **Motion Canvas**

이유:
- Manim의 학습곡선보다 가벼움 (TypeScript = JS와 친숙)
- 라이브 프리뷰가 GSAP보다 훨씬 강력
- React 컴포넌트 재사용 (Remotion도 같은 강점)
- HyperFrames의 inline-asset 한계 우회

단점: 현 HyperFrames 자산 (template, palettes) 재작성 필요.

### 6.3 Manim은? — 신중

- 결과는 압도적. 하지만:
  - 수학 시각화엔 좋지만 **인물 서사엔 약함**
  - Python 학습 + LaTeX 환경 셋업 = 진입장벽
  - 우리 Story 영상의 본질(인물·감성)과 톤이 다름
- **권고**: Story 영상엔 Motion Canvas/Remotion, **Concept 영상엔 Manim** (멀리서 봤을 때 별개 트랙)

### 6.4 멀티 페르소나 audit은 무조건 도입

비용 거의 없음 (스킬 4개 작성). 효과 큼:
- 한 사람 NCC의 시점 편향 보완
- Nick 검토 부담 ↓ (자동 1차 검수 후 Nick은 종합만)
- 학습자(딸) 관점 시뮬레이션 → 진짜 학습 효과 예측

---

## 7. 실험 계획 — Nick이 결정할 사항

| 결정 | 옵션 | NCC 권고 |
|---|---|---|
| A. 다음 진화 단계 | v1.5 / v2 / v3(Motion Canvas) | **v1.5** (빠른 가치) |
| B. 길이 정책 | 50s 유지 / 90s / 2min / 시리즈 분할 | **90~120s** (호흡 ↑, 시리즈는 v2+) |
| C. AI 이미지 도구 | SD 로컬 / Firefly / DALL-E API | **SD + ControlNet** (로컬, 무료, 일관성 LoRA) |
| D. TTS 업그레이드 | edge-tts 유지 / ElevenLabs / OpenAI | **ElevenLabs 트라이얼 후 결정** |
| E. 멀티 페르소나 audit | 도입 / 보류 | **도입** (저비용 고효과) |
| F. Manim/Motion Canvas | 도입 / 보류 | **Motion Canvas 파일럿** (Unit 01 한 개만 재제작 테스트) |

---

## 8. 외부 참고 자료 (research 결과)

- **Manim Community**: https://github.com/3b1b/manim
  - 원조 Python 수학 애니메이션. 3Blue1Brown 사용. LaTeX 통합.
- **Motion Canvas**: TypeScript 기반 Manim 변형. 라이브 프리뷰. React 컴포넌트.
- **Remotion**: React 기반. Remotion Studio (개발자 도구로 인기). HyperFrames와 직접 경쟁/우월 후보.
- **2026 AI 영상 트렌드**: "Hybrid Workflows" — AI는 배경·시뮬레이션·조명, 핵심 요소는 사람 제작.
- **캐릭터 일관성**: Veo 3 image reference, Adobe Firefly Custom Models, SD + LoRA — 캐릭터 visual drift 문제 해결됨.
- **단편 교육 애니메이션 효과**: 짧은 애니메이션은 언어·문화 장벽을 넘는 데 효과 (nature.com 보고서).
- **AI 영상 파이프라인** (2026): 스토리보드 → 애니메틱 → 풀 렌더 단계화 + AI 보조 (etvbharat).

(Source URLs는 chatlog response의 Sources 섹션에 포함)

---

## 9. 다음 단계 — Nick 결정 대기

§7의 6가지 결정 (A~F) 답변 받으면 NCC가:
- 그에 맞는 detail plan 작성 (별도 chatlog 라운드)
- 첫 마일스톤 (예: Unit 01 v1.5 재제작) 자율 진행
- 작업 결과를 비교용으로 v1 옆에 보관 (회귀 비교 가능)

---

## 10. 변경 이력

- v1.0 (2026-05-15): 초안. Nick의 브레인스토밍 요청에 응답.
