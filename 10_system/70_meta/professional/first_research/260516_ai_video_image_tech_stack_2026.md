<!-- 260516_ai_video_image_tech_stack_2026.md -->

# AI 영상·이미지 생성 — 전문가 Tech Stack 지도 (2026-05 기준)

> 작성: 2026-05-16
> 상태: 기반 지식 문서. 정기 업데이트 필요 (도구·가격 6개월마다 변함)
> 사용법: 한번에 다 이해하려 하지 말 것. 필요할 때 해당 섹션 참조.
> 출처: 2026-02~05월 공개 자료 종합

---

## 0. 큰 그림 — Layer Cake로 본 AI 영상 제작

```
┌─────────────────────────────────────────────┐
│  Layer 6: 편집·합성 (Editing & Compositing) │  DaVinci, Premiere, AE, CapCut
├─────────────────────────────────────────────┤
│  Layer 5: 오디오 (Audio)                    │  TTS, Music, SFX
├─────────────────────────────────────────────┤
│  Layer 4: 영상 생성 (Video Gen)             │  Veo, Sora, Kling, Runway...
├─────────────────────────────────────────────┤
│  Layer 3: 이미지 생성 (Image Gen)           │  Nano Banana, MJ, Flux...
├─────────────────────────────────────────────┤
│  Layer 2: 오케스트레이션 (Orchestration)    │  ComfyUI, n8n, custom Python
├─────────────────────────────────────────────┤
│  Layer 1: 모델·API 게이트웨이               │  fal.ai, Replicate, OpenRouter
└─────────────────────────────────────────────┘
```

**핵심 통찰**: 2026년 프로 워크플로우는 *한 도구로 끝나지 않음*. Layer 마다 다른 도구를 쓰고, 그 도구들을 *워크플로우 엔진*으로 묶음. 이게 "AI 영상 엔지니어"의 본질적 일.

---

## 1. Layer 3: 이미지 생성 (Image Generation)

### 1.1 왜 이미지 생성을 먼저 이해해야 하나

**프로 워크플로우의 80%는 "Image-to-Video"**.

이유: 영상 모델에 텍스트만 주면 매 생성마다 캐릭터가 다르게 나옴 (character drift). 해법 = 이미지로 캐릭터 *고정* 후, 그 이미지를 영상 모델에 reference로 줌. 따라서 *이미지 생성 능력이 영상 품질의 천장*이 됨.

### 1.2 주요 모델 비교 (2026-04 기준)

| 모델 | 제작사 | 강점 | 약점 | 가격 (API) |
|---|---|---|---|---|
| **Nano Banana 2** (Gemini 3.1 Flash Image) | Google | 텍스트 렌더링, 편집·일관성, 4K, 속도 (3~5초) | 예술적 스타일은 MJ에 못 미침 | $0.02 (512px) ~ $0.151 (4K) |
| **Nano Banana Pro** (Gemini 3 Pro Image) | Google | NB2 상위. 더 정밀 | 가격 ↑ | $0.05~$0.134 |
| **Midjourney v8** | Midjourney | **예술 미·시네마틱 톤** 최강 | API 제한적, 구독제 | $10~$120/월 |
| **GPT Image 1.5** (gpt-image-1.5) | OpenAI | 포토리얼리즘 87%, 텍스트 렌더링 | 검열 빡빡 | $0.04/장 (표준) |
| **Flux 2 Pro** | Black Forest Labs | **오픈소스 자체 호스팅 가능**, API도 좋음 | 셋업 복잡 | $0.025~$0.05 (호스팅) / 로컬은 0원 |
| **Ideogram v3** | Ideogram | 텍스트(글자) 정확도 | 일반 이미지는 평범 | $7~$48/월 |
| **Recraft v4** | Recraft | 벡터·로고·디자인 특화 | 일반 일러스트 약함 | $0~$48/월 |
| **Adobe Firefly** | Adobe | 상업 라이선스 깨끗, 브랜드 안전 | 품질은 MJ 미만 | 구독 ($4.99~/월) |

### 1.3 모델 선택 패턴 (프로의 실제 사용)

**한 도구만 쓰지 않음.** 다음 *조합*이 표준:

```
[기획 단계]  Midjourney → 무드보드·컨셉 아트 (예술적 영감)
                ↓
[캐릭터 디자인]  Flux + ControlNet → 캐릭터 reference sheet
                ↓
[일관성 유지]  Nano Banana 2 → 같은 캐릭터 다양한 포즈 (편집 강함)
                ↓
[최종 자산]  Photoshop AI / Firefly → 최종 정리·합성
```

**왜 이렇게 분리?** 각 모델이 잘하는 게 다름.
- MJ는 "처음 보는 아름다운 이미지" 생성에 강함 (창의)
- Nano Banana는 "기존 이미지를 변형"에 강함 (일관성)
- Flux는 *로컬 실행 가능* → 무제한 반복 (비용 0)

### 1.4 캐릭터 일관성 (Character Consistency) — 핵심 스킬

13인 인물 시리즈를 만들 때 가장 어려운 문제. 해법 3단계:

**Level 1 — Prompt 일관성**: 텍스트 묘사를 모든 장면에서 동일하게. 한계 명확.

**Level 2 — Reference Image + IP-Adapter**: 캐릭터 reference 한 장을 모델에 줌. ComfyUI에서 IP-Adapter 노드 사용. 단기 사용에 충분.

**Level 3 — LoRA Training**: 캐릭터별 *소형 모델* 학습. 15~50장 reference로 1000~3000 step 학습. 한 캐릭터 = 1~2시간 학습 (GPU 24GB+). 가장 강력·재사용 가능.
- 도구: Kohya_ss, ComfyUI-FluxTrainer
- 비용: 로컬은 전기료, 클라우드는 ~$5/LoRA
- **Nick 적용성**: DGX V100 보유 → 로컬 학습 비용 0

### 1.5 SynthID와 워터마킹

Google Imagen/Nano Banana는 *보이지 않는 워터마크* (SynthID) 자동 삽입. EU AI Act 호환. 상업용 사용 시 라벨링 의무 (YouTube, TikTok, Meta).

---

## 2. Layer 4: 영상 생성 (Video Generation)

### 2.1 현재 시장 — 6대 진영 (2026-04)

| 모델 | 제작사 | 강점 | 길이 | 오디오 | 가격 |
|---|---|---|---|---|---|
| **Veo 3.1 Standard** | Google | **4K, 최고 lip-sync, native audio** | 8s (체이닝 140s+) | ✅ 동기 생성 | $0.40/초 ($3.20/8초) |
| **Veo 3.1 Fast** | Google | 빠른 초안용 | 8s | ✅ | $0.15/초 ($1.20/8초) |
| **Veo 3.1 Lite** | Google | 가장 저렴 | 8s | ❌ | $0.05/초 |
| **Sora 2 Pro** | OpenAI | **물리 시뮬레이션, 25초 클립** | up to 25s | ✅ | $0.30~$0.50/초 |
| **Sora 2** (base) | OpenAI | 표준 | up to 25s | ✅ | $0.10/초 |
| **Kling 3.0** | Kuaishou | **4K native, 캐릭터 일관성, multi-shot storyboard** | 10s | ✅ Omni | $0.07~$0.10/초 |
| **Seedance 2.0** | ByteDance | **시네마 톤, 통합 audio-video 아키텍처** | 5~10s | ✅ | $0.05~$0.26/생성 |
| **Runway Gen-4.5** | Runway | **편집 도구, motion brush, video-to-video** | 10s | ✅ | $0.15/초, $12~$76/월 |
| **Hailuo 2.3** | MiniMax | **저렴, 자연스러운 인물 모션** | 6~10s | ✅ | $0.28~$0.49/생성 |
| **Wan 2.6** | Alibaba | **오픈소스 가능, 가장 저렴** | 5~10s | ✅ | $0.05/초 (호스팅) / 로컬은 0 |
| **Pika 2.5** | Pika | 스타일 효과, lip-sync 특화 | 5~10s | ✅ Pikaformance | $8~$76/월 |
| **Luma Ray3** | Luma | **시네마틱, keyframe 제어, modify 기능** | 5s | ❌ | $7.99~/월 |

> ⚠️ **Sora 단종 예고**: OpenAI가 2026-03 발표 — Sora 웹·앱은 2026-04-26 종료, API는 2026-09-24 종료. 장기 프로젝트는 피할 것.

### 2.2 가격 — 8초 클립 1편 비교

| 모델 | 1클립 비용 |
|---|---|
| Wan 2.6 / Veo 3.1 Lite | **$0.40** |
| Veo 3.1 Fast | **$1.20** |
| Kling 3.0 | **$0.56~$0.80** |
| Sora 2 base | **$0.80** |
| Hailuo 2.3 Pro | **$0.49 (6초)** |
| Veo 3.1 Standard | **$3.20** |
| Sora 2 Pro 1080p | **$4.00** |

→ 60초 영상 = 8초 클립 7~8개. **저렴 조합 $3 / 표준 $10~$15 / 프리미엄 $25~$30** 수준.

### 2.3 핵심 워크플로우 패턴

#### 패턴 A. Text-to-Video (T2V) — 가장 단순
프롬프트만으로 영상 생성. 단점: 캐릭터 일관성 ↓, 통제력 ↓.
**용도**: 배경·풍경·추상 모션.

#### 패턴 B. Image-to-Video (I2V) — **프로의 표준**
1. 이미지 모델로 첫 프레임 생성 (캐릭터·구도 고정)
2. 그 이미지를 영상 모델에 reference로 → 모션만 생성
**용도**: 인물·캐릭터 영상의 사실상 전부.

#### 패턴 C. First-Last Frame (FLF)
시작 프레임 + 끝 프레임 모두 지정. 모델이 사이를 interpolation.
**용도**: 정확한 모션 통제 (Luma keyframes, Veo 3.1).

#### 패턴 D. Video-to-Video (V2V) — "Reskin"
저화질 실사 영상의 *모션 구조*를 추출 + AI로 외관 재생성.
**용도**: 사람 움직임을 캐릭터로 변환. Runway가 강함.

#### 패턴 E. Multi-Shot Storyboard
여러 샷을 일관된 캐릭터·톤으로 *한번에* 생성.
**용도**: 짧은 내러티브. Kling 3.0이 선도.

### 2.4 길이 한계와 체이닝 (Chaining)

모든 모델 클립 한도가 5~25초. 장편은 *체이닝*:
- Veo 3.1: scene extension 20클립까지 = 140초+
- Sora 2: 25초 단일 클립 (가장 김)
- 일반: 5~10초 클립을 *연결*해서 1분~ 영상 제작

**체이닝의 도전**: 클립 간 캐릭터·조명·환경 일관성 유지. 이게 long-form AI 영상의 가장 큰 기술 장벽.

### 2.5 캐릭터 일관성 (영상에서)

장편 영상의 진짜 어려움. 표준 해법:

1. **Character Reference Sheet** 먼저 만들기: 같은 캐릭터의 정면·측면·뒷면·표정 5~10장 (이미지 모델로)
2. **Style 고정**: 컬러 팔레트·조명·렌즈 등 메타데이터 일관
3. **Persistent ID**: LTX Studio, Higgsfield Popcorn 등은 캐릭터를 *재사용 가능 자산*으로 관리
4. **Pre-Frame Conditioning**: 직전 클립 마지막 프레임을 다음 클립 시작점으로

### 2.6 실패율과 비용 계획

> *"5초 사용 가능한 영상이 필요하면, 20초 생성하고 솎아내야 함."*

프로 워크플로우의 *실패율 가정* = 3:1 ~ 5:1. 이것 모르면 비용 계산이 틀어짐.
60초 영상 *실사용* 분량을 위해 → 180~300초 생성 비용을 예상.

---

## 3. Layer 5: 오디오 (Audio)

### 3.1 TTS (Text-to-Speech) — 나레이션

| 도구 | 강점 | 한국어 | 가격 |
|---|---|---|---|
| **ElevenLabs v3** | **품질 최고, 70+ 언어, 감정 표현** | ★★★★★ | $5(Starter)~$330/월 |
| **ElevenLabs Flash v2.5** | 75ms 저지연 | ★★★★ | 위와 동일 플랜 |
| **OpenAI TTS (gpt-4o-tts)** | **Instructable** (캐릭터 지시 가능) | ★★★★ | $0.015/1k chars |
| **Cartesia Sonic-2** | **최저 지연 <100ms**, 실시간 음성 | ★★ (15개 언어) | ElevenLabs의 1/5 가격 |
| **Hume EVI** | **감정 인식·표현** | ★★★ | 무료 tier 있음 |
| **Google Gemini TTS** | Google 생태계 | ★★★★ | Gemini API 기준 |
| **PlayHT** | 대화·롱폼 특화 | ★★★ | $39~/월 |
| **XTTS-v2 (Coqui)** | **오픈소스, 자체 호스팅** | ★★★ | 로컬은 0원 |
| **Bark (Suno)** | 음성+SFX+비언어 | ★★ | OSS |
| **Kokoro** | **경량 OSS**, 의외로 좋음 | ★★ | 로컬 0원 |

**한국어 권고**: ElevenLabs 시작 → 사용량 늘면 Gemini TTS 또는 self-hosted XTTS-v2 검토. ElevenLabs Voice Library에 한국어 화자 풍부 (Voice Cloning으로 본인 음성도 가능).

### 3.2 음악 생성 (Music Generation)

| 도구 | 품질 | 라이선스 | 가격 |
|---|---|---|---|
| **Suno v5** | **품질 1위, 보컬 포함 풀송** | ⚠️ Sony 소송 진행 중 | $10~$30/월 |
| **Udio v2** | Suno 견줌, 재즈·R&B 강함 | ⚠️ UMG 합의 | $10~$30/월 |
| **ElevenLabs Music** | **라이선스 깨끗 (상업안전)** | ✅ 라이선스 학습 데이터 | $0.80/2분곡 |
| **Stable Audio** | 사운드 디자인·악기 강함 | ✅ AudioSparx 라이선스 | $11.99~/월 |
| **AIVA** | 클래식·시네마틱 스코어 | ✅ Pro에서 풀 소유권 | $11~$33/월 |
| **MiniMax Music 2.5** | **API 가장 저렴** | ⚠️ | $0.035/생성 |
| **Google Lyria 3** | Google 생태계, 실시간 streaming | ✅ | Gemini API 기준 |

**상업용 → ElevenLabs Music 또는 Stable Audio.** Suno/Udio는 소송 리스크.

### 3.3 SFX (효과음)

- **ElevenLabs Sound Effects**: 텍스트→짧은 효과음. ElevenLabs 구독에 포함.
- **Freesound.org**: CC 라이선스 효과음 무료
- **YouTube Audio Library**: YT 사용 무료
- **Soundly** / **Boom Library**: 프로 SFX 라이브러리 (유료, 일회성)

---

## 4. Layer 2: 오케스트레이션 (Orchestration)

### 4.1 ComfyUI — 노드 기반 워크플로우 표준

**왜 중요한가**: 위 모든 도구를 *연결*해 자동화. AI 영상 엔지니어의 핵심 스킬.

```
[이미지 1 입력]→[IP-Adapter]→[Flux SDXL]→[Upscale]→[I2V 모델]→[비디오 출력]
                       ↑
                  [LoRA: 캐릭터]
```

**ComfyUI 활용 영역**:
- 이미지 생성 (Flux, SDXL)
- LoRA 학습·로딩
- 캐릭터 일관성 (IP-Adapter, FaceID)
- I2V 워크플로우 (WanVideo, Hunyuan 등)
- 배치 생성·자동화

**필요 HW**: 12GB+ VRAM 권장, 24GB+ 이상적. **Nick: V100 32GB × 4 → 충분 이상**.

**학습 시간**: 기본 사용 ~10h. 전문 활용 ~50h. 깊이 마스터 ~200h+.

### 4.2 클라우드 ComfyUI / SaaS 워크플로우 도구

로컬 ComfyUI 셋업이 부담스러우면:

| 서비스 | 특징 | 가격 |
|---|---|---|
| **RunComfy** | 브라우저 ComfyUI, 워크플로우 마켓 | $0.10~/분 GPU |
| **fal.ai** | API 우선, 빠른 실험 | pay-as-you-go |
| **Replicate** | 모델 카탈로그 + API | pay-as-you-go |
| **WaveSpeed** | 통합 영상 파이프라인 | 구독제 |
| **MindStudio** | No-code 워크플로우 chain | 구독제 |

### 4.3 자체 워크플로우 코딩

ComfyUI도 결국 추상화. 더 깊이 가면:

```python
# 의사 코드 — 실제 영상 파이프라인
script = llm.generate_scenes(brief)
for scene in script:
    ref_img = nano_banana.generate(scene.character_prompt)
    video_clip = veo3.image_to_video(ref_img, scene.motion_prompt)
    narration = elevenlabs.tts(scene.narration, voice_id)
    final = ffmpeg.combine(video_clip, narration, bgm)
```

**이게 hw-agent-core의 영상 버전.** Nick에게 자연스러운 영역.

### 4.4 워크플로우 자동화 도구 (No-code/Low-code)

- **n8n** (OSS, self-host): API들을 노드로 연결. 영상 파이프라인 자동화.
- **Make.com** (Integromat): SaaS, 더 사용자 친화적
- **Zapier**: 가장 단순, 가장 제한적
- **Apify**: 웹 스크래핑 + AI 결합

---

## 5. Layer 6: 편집·합성 (Post-Production)

AI 생성 영상은 그대로 못 씀. *후처리*가 프로의 필수:

### 5.1 비디오 편집 도구

| 도구 | 특징 | 가격 |
|---|---|---|
| **DaVinci Resolve** | **무료 버전이 압도적**, 컬러 그레이딩 최강 | 무료 / $295 (Studio) |
| **Adobe Premiere Pro** | 업계 표준, Adobe 생태계 | $20.99/월 |
| **Final Cut Pro** | Mac 전용, 빠름 | $299 일회성 |
| **CapCut** | **무료, 모바일 친화**, AI 기능 풍부 | 무료 / Pro $7.99/월 |

### 5.2 합성·VFX

| 도구 | 특징 | 가격 |
|---|---|---|
| **After Effects** | 모션그래픽·합성 업계 표준 | $20.99/월 |
| **Nuke** | 영화급 합성 | $499/월~ |
| **DaVinci Fusion** | Resolve 내장 합성 도구 | 무료 |
| **Motion Canvas / Remotion** | **코드 기반** (TS/React) | OSS 무료 |
| **Manim** | **수학 시각화 특화** Python | OSS 무료 |

### 5.3 업스케일·복원

AI 생성 영상은 보통 720p~1080p. 4K 배포 시 업스케일 필요:
- **Topaz Video AI**: 업계 표준 ($299 일회성)
- **HitPaw VikPea**: AI 업스케일러 (구독제)
- **Real-ESRGAN**: OSS

### 5.4 AI 합성 특수 도구

| 도구 | 용도 | 가격 |
|---|---|---|
| **HeyGen / Synthesia** | 아바타 talking-head, 다국어 더빙 | $24~/월 |
| **D-ID** | 사진→말하는 얼굴 | $5.99~/월 |
| **Rask AI** | 다국어 음성 더빙·번역 | $50~/월 |
| **Captions** | 자동 자막·립싱크 | 구독제 |

---

## 6. 통합 워크플로우 — 프로 패턴

### 6.1 패턴 1: "단편 광고" 워크플로우 (15초 광고)
```
LLM (Claude/GPT) → 스크립트
   ↓
Nano Banana 2 → 메인 시각 자산 (제품샷, 모델)
   ↓
Veo 3.1 Fast → 8초 × 2 클립 ($2.40)
   ↓
ElevenLabs → 나레이션 ($0.10)
   ↓
ElevenLabs Music → BGM ($0.80)
   ↓
DaVinci Resolve → 편집·자막·컬러 (무료)
   ↓
완성: 15초 광고, 총 비용 ~$5, 시간 ~2시간
```

### 6.2 패턴 2: "교육 영상" 워크플로우 (60~90초)
Nick의 경우에 정확히 매핑되는 패턴:

```
[기획]    Claude → 스크립트 + 장면 분할
[자산]    Nano Banana (또는 SD+LoRA) → 인물·배경 시퀀스 (13장)
[모션]    Veo 3.1 Fast → 8초 × 8클립 = 64초 ($9.60)
          또는 Kling 3.0 → 더 저렴 ($5.60)
          또는 정적 이미지 + Motion Canvas 모션 → $0 (현재 방식)
[나레]    ElevenLabs (인물별 다른 보이스) → ($1~$2)
[음악]    Stable Audio → 라이선스 안전 ($1)
[합성]    DaVinci Resolve / Motion Canvas → 무료
[배포]    YouTube + 자막 (Captions AI)

월 4편 제작 시: ~$50~$80
```

### 6.3 패턴 3: "장편 내러티브" 워크플로우 (10~20분)
Long-form 콘텐츠. 가장 어려움.

```
[Pre-Production]
  - 스크립트 작성 (LLM 협업)
  - Character Reference Sheet (인물 5~10명 × 다각도)
  - Style Bible (컬러·조명·렌즈 일관성 가이드)
  - Shot List (200~400 컷)

[Production - 배치 생성]
  - 컷별 키프레임 생성 (Image gen, 일관성 LoRA 적용)
  - I2V로 모션 입히기 (병렬 처리)
  - **실패율 3~5배 가정** → 1200~2000 컷 생성

[Post-Production]
  - 일관성 review (사람 검수, AI 도움)
  - 편집·컬러 그레이딩 (Resolve)
  - 사운드 디자인·믹싱
  - 4K 업스케일

월 1편 제작 가정 시: $500~$2000 (도구·API)
인력: 1~3인 (혼자도 가능하나 시간 ↑↑)
```

### 6.4 패턴 4: "실시간 인터랙티브" 워크플로우
Cartesia + 실시간 영상 모델 + 백엔드 = 실시간 AI 캐릭터 (게임, 챗봇 아바타).
아직 실험적이나 빠르게 발전 중. Nick의 vLLM 사내 서비스와 시너지 가능.

---

## 7. 비용 시나리오 — 사용량별

### 7.1 취미·실험 (월 5~10 영상)
- 도구: Veo 3.1 Fast + ElevenLabs Starter + Nano Banana
- Google AI Pro $19.99/월 + ElevenLabs Starter $5/월
- **총 월 비용: $25~$50**

### 7.2 진지한 1인 크리에이터 (월 15~30 영상)
- 도구: 위 + Midjourney + Stable Audio
- Google AI Pro $19.99 + ElevenLabs Creator $22 + MJ Pro $30 + Stable Audio $11.99
- API 추가 사용량 $30~$80
- **총 월 비용: $120~$200**

### 7.3 프로 스튜디오 (월 50+ 영상, 광고·시리즈)
- Google AI Ultra $249.99 + ElevenLabs Pro $99 + Runway Unlimited $76 + MJ Mega $120
- API 추가 ($200~$500)
- ComfyUI 인프라 (RunComfy 또는 자체 GPU 클라우드)
- **총 월 비용: $800~$2000+**

### 7.4 엔터프라이즈
- Vertex AI Enterprise (Veo)
- ElevenLabs Enterprise ($1500+/월)
- Adobe Firefly Enterprise
- 자체 ComfyUI 클러스터 (GPU 서버)
- **총 월 비용: $5000~$50000+**

---

## 8. 익혀야 할 스킬 지도

전문가가 되려면 다음 *순서대로*:

### 8.1 기초 스킬 (3~6개월)
1. **프롬프트 엔지니어링**: 이미지·영상 모델별 프롬프트 문법
2. **이미지 생성 도구 1개 마스터**: Nano Banana 또는 MJ 중 택1
3. **영상 생성 도구 1개 마스터**: Veo 또는 Kling 중 택1
4. **편집 기초**: DaVinci Resolve 기본
5. **TTS 기초**: ElevenLabs 인터페이스

### 8.2 중급 스킬 (6~12개월)
6. **ComfyUI 노드 구성**: 기본 워크플로우 작성 가능
7. **Image-to-Video 통합 워크플로우**: I2V 패턴 자유롭게
8. **캐릭터 일관성**: IP-Adapter, reference image 활용
9. **음악·SFX 통합**: 영상-오디오 동기화
10. **시각 정체성 일관성**: 같은 스타일 N편 유지

### 8.3 전문 스킬 (12~24개월)
11. **LoRA 학습**: 자체 캐릭터 모델
12. **API 자동화**: Python으로 파이프라인 코딩
13. **배치 처리**: 수십 컷 동시 생성·관리
14. **컬러 그레이딩**: 영화급 톤 통일
15. **체이닝 마스터**: 장편 일관성

### 8.4 마스터 스킬 (24개월+)
16. **자체 워크플로우 엔진 구축**: 자기 만의 자동화 시스템
17. **모델 fine-tuning**: 캐릭터·스타일 전용 모델
18. **실시간·인터랙티브**: 라이브 AI 캐릭터
19. **다국어 글로벌 배포**: 더빙 자동화
20. **새 모델 빠른 평가·도입**: 트렌드 선도

---

## 9. Nick 적용 관점에서의 핵심 통찰

(별도 의견 — 본인 채널 비전에 비추어)

### 9.1 본인 강점이 비대칭적으로 큰 영역
- **DGX V100 보유**: 자체 ComfyUI + Flux + LoRA = 사실상 무제한 이미지 생성. 큰 비대칭 우위.
- **HW/RTL 엔지니어 + AI 워크플로우 경험**: ComfyUI 노드 구성·자동화에 빠르게 적응 가능.
- **Claude Code 워크플로우 숙련**: API 기반 자동화에 강함.

### 9.2 60~90초 영상에 *과한* 도구들
- Sora 2 Pro (광고급 사실감) — 불필요
- Runway Unlimited ($76/월) — 양이 안 나옴
- 4K 업스케일 — YouTube에선 1080p 충분

### 9.3 권장 진화 경로 (현재 기반에 비추어)
```
Phase 0-A (지금~3개월): 
  Edge-TTS → ElevenLabs Starter ($5)
  정적 SVG → Nano Banana 이미지 (월 $5~$10)
  
Phase 0-B (3~6개월):
  Motion Canvas 도입 (코드 기반 영상)
  Stable Audio BGM ($12)
  
Phase 1 (6~12개월):
  DGX에 ComfyUI 셋업 (무료, 시간만)
  Flux + LoRA 자체 학습 (캐릭터 일관성)
  Veo 3.1 Fast 또는 Kling 3.0 I2V 실험 (월 $20~$50)
  
Phase 2 (12~24개월):
  자체 워크플로우 엔진 (Python + ComfyUI API)
  멀티 페르소나 + AI 영상 통합 시스템
  실험적 long-form 또는 인터랙티브
```

### 9.4 *피해야* 할 함정
- **새 모델 따라가기 충동**: 매주 SOTA 새로 나옴. v1.5 안정화 전엔 봉인.
- **너무 비싼 도구**: Sora 2 Pro, Runway Unlimited는 1년차에 ROI 안 나옴.
- **로컬 vs 클라우드 양다리**: ComfyUI 로컬에 익숙해진 후 클라우드도 같은 패턴으로.
- **자동화 우선 → 손작업 무시**: 한 번은 *전 과정 손으로* 해봐야 자동화의 진가 보임.

---

## 10. 정기 업데이트 영역

이 문서는 6개월마다 다음을 점검해야 함:

| 영역 | 변화 속도 | 주시할 것 |
|---|---|---|
| 영상 모델 | **매우 빠름** | 신모델·가격 인하 |
| 이미지 모델 | 빠름 | 신모델·일관성 개선 |
| TTS | 중간 | 한국어 품질 |
| ComfyUI 생태계 | 빠름 | 새 노드·워크플로우 |
| 라이선스·법규 | 느림 | EU AI Act, 한국 AI법 |

---

## 11. 출처 (2026-02~05 검색 기반)

- Veo 3.1 pricing: ai.google.dev, Vertex AI docs
- Sora 2 단종: OpenAI 2026-03 발표
- Kling 3.0, Seedance 2.0, Wan 2.6: 각 사 공식
- ComfyUI: comfy.org, RunComfy 가이드
- ElevenLabs, Cartesia 비교: 각 사 vs page, sureprompts.com
- Suno/Udio/ElevenLabs Music: chartlex.com, aimagicx.com
- 캐릭터 일관성: neolemon, apatero, magichour AI 가이드

→ 모든 가격·기능은 2026-04 시점. 변경 가능성 큼.

## 12. 변경 이력

- v0.1 (2026-05-16): 초안. Layer Cake 구조 + 6 패턴 + Nick 적용 의견.
