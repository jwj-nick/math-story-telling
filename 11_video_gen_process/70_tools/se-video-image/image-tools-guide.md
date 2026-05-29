<!-- image-tools-guide.md / AI 이미지 생성 도구 비교 + setup 가이드 -->

# AI 이미지 생성 도구 가이드 (영상 장면 이미지)

> **목적**: `se-video-image` 스킬이 호출 가능한 이미지 생성 도구들의 API·요금·품질·프롬프트 특성 비교.
> **단일 진입점**: [SKILL.md](./SKILL.md) / 프롬프트 = [5-image_prompts.md](../../40_experiments/exp-002-build-unit01/5-image_prompts.md)
> **본 프로젝트 핵심 요구**: **캐릭터 일관성** (에라토스테네스가 S2·S4 동일 얼굴) + 시대 정확성 + 16:9 + API 자동화 가능성.
> **최근 갱신**: 2026-05-29 (가격은 공식 사이트 확인 필수 — 분기마다 변동)

---

## 0. 한 줄 요약 (본 프로젝트 기준)

| 우선 | 도구 | 핵심 | 본 프로젝트 적합 |
|---|---|---|---|
| 🥇 1차 | **Google Nano Banana** (Gemini 2.5 Flash Image) | 캐릭터 일관성 강력 + $0.039/장 + API + NCC 자동 | ⭐ 에라토 일관성에 최적 |
| 🥈 2차 | **GPT Image 1.5 / 2** (OpenAI) | 자연어 + reference 입력 + 품질 우수 | API 자동, 약간 비쌈 |
| 🥉 3차 | **Flux** (via FAL/Replicate API) | open-weight 저렴 + API | 일관성 IPAdapter 필요 |
| 참고 | **Midjourney V8** | 품질 최고지만 **공식 API 없음** | Discord 수동 |
| 참고 | **Stable Diffusion** (로컬) | 무료 + 완전 제어 | GPU + ComfyUI 설정 |

> ⚠️ **DALL-E 3 는 2026-05-12 OpenAI API 에서 제거됨** → GPT Image 1.5 로 대체. (5-image_prompts.md 의 DALL-E 언급 = GPT Image 로 해석)

---

## 1. 옵션 비교 표

| 도구 | API | 요금 (장당) | 기본 품질 | 캐릭터 일관성 | 프롬프트 특성 |
|---|---|---|---|---|---|
| **Nano Banana** (Gemini 2.5 Flash Image) | ✅ Gemini API / AI Studio / Vertex | **$0.039** (1290 tok) | ★★★★ | ★★★★★ (멀티이미지 blend, 핵심 강점) | 자연어 + 이미지 입력 (대화형 편집) |
| **Nano Banana 2** | ✅ | $0.045(0.5K)~$0.151(4K) / Batch $0.022~0.076 | ★★★★★ | ★★★★★ | 동일 + 고해상도 |
| **GPT Image 1.5** | ✅ OpenAI | $0.009~0.20 (tier×해상도) | ★★★★ | ★★★ (reference 입력) | 자연어 (서술형) |
| **GPT Image 2** (flagship) | ✅ OpenAI | $0.005~0.211 | ★★★★★ | ★★★★ | 자연어 |
| **GPT Image 1 Mini** | ✅ OpenAI | $0.005~0.052 | ★★★ | ★★ | 자연어 (저가) |
| **Midjourney V8** | ❌ (Discord 수동, API limited) | 구독 $10~120/월 | ★★★★★ | ★★★★ (`--cref`) | 키워드 + 파라미터 |
| **Flux.2 Pro** | ✅ FAL/Replicate/WaveSpeed | $0.02~0.10 (creator) / $0.008~0.04 (aggregator) | ★★★★ | ★★★ (IPAdapter/Kontext) | 키워드 + negative |
| **Stable Diffusion 3.5** | ✅ (hosted) / 로컬 무료 | $0.008~0.04 / 로컬 $0 | ★★★ | ★★★★ (IPAdapter/ControlNet) | 키워드 + negative + 시드 |

---

## 2. 도구별 상세

### 2.1 ⭐ Google Nano Banana (Gemini 2.5 Flash Image) — 1차 추천

- **정체**: Gemini 2.5 Flash 의 이미지 생성·편집 모델. 코드명 "Nano Banana". 2025-10 GA.
- **API**: ✅ Gemini API / Google AI Studio / Vertex AI
  - **key 발급 = Google AI Studio (https://aistudio.google.com) 에서 무료**.
  - ⚠️ **이미지 생성(gemini-2.5-flash-image)은 free tier 할당량 0** → **유료 등급(Tier1) 필수**.
  - ✅ **해결법 (2026-05-29 검증)**: AI Studio `api-keys` 페이지에서 해당 프로젝트의 **"결제 활성화" 클릭 → Tier1 후불 전환**. ⚠️ Cloud Console 결제계정 연결만으론 부족 — AI Studio에서 유료등급 전환이 별도 단계. "무료 체험" 누르면 free tier 유지(0)이라 안 됨. 멀티계정(/u/N/)이면 결제·key 같은 계정이어야 함.
  - 전환 후 NCC가 동일 key로 이미지 직접 생성 가능 (자율).
- **요금**: $30/1M output tokens, 이미지 1장 = 1290 tokens = **$0.039/장**. (Nano Banana 2 = 해상도별 $0.045~0.151, Batch 반값)
- **품질**: ★★★★ 자연스러운 일러스트·사실. world knowledge 반영.
- **⭐ 캐릭터 일관성**: 최강. "같은 인물/사물을 여러 프롬프트·편집에서 일관 유지", 멀티이미지 blend. **본 프로젝트 에라토 S2·S4 일관성에 직접 부합.**
- **프롬프트**: 자연어 + (옵션) 입력 이미지. 대화형 편집 ("이 인물로 다른 장면").

### 2.2 GPT Image (OpenAI) — 2차

- **정체**: DALL-E 3 후속 (DALL-E 3 = 2026-05-12 제거). GPT Image 1 Mini / 1.5 / 2.
- **API**: ✅ OpenAI (Nick 이 OpenAI key 주면 NCC 자동 — ElevenLabs 패턴)
- **요금**: quality tier (Low/Medium/High) × 해상도 (1024² / 1024×1536 / 1536×1024). $0.005~0.25.
- **품질**: ★★★★ (1.5) ~ ★★★★★ (2). 자연어 이해 우수.
- **캐릭터 일관성**: ★★★ — reference 이미지 입력 지원 (멀티). Nano Banana 보다 약함.
- **프롬프트**: 자연어 서술형 (5-image_prompts.md 그대로 사용 가능).

### 2.3 Midjourney V8 — 참고 (API 없음)

- **API**: ❌ 공식 없음 (2026-04 limited release, 상업 조건 제한적). **Discord 수동**.
- **요금**: 구독 — Basic $10/월(~200 fast), Standard $30(~900 fast + unlimited relax), Pro $60(stealth), Mega $120.
- **품질**: ★★★★★ 예술성 최고.
- **캐릭터 일관성**: ★★★★ `--cref <URL> --cw 100`.
- **프롬프트**: 키워드 + `--ar 16:9 --style raw`. NCC 가 프롬프트만 작성, 생성은 Nick 이 Discord 에서.

### 2.4 Flux / Stable Diffusion — 참고 (open-weight)

- **Flux.2**: open-weight 최강. API (FAL/Replicate/WaveSpeed) $0.008~0.10. Kontext = 편집·일관성.
- **SD 3.5**: 로컬 무료 (GPU) 또는 hosted $0.008~0.04. ControlNet/IPAdapter 일관성 강.
- **프롬프트**: 키워드 + negative prompt (`text, watermark, modern, deformed`) + 시드 고정. 설정 난이도 높음.

---

## 3. 요금 상세 + 요금별 제한 (quality / quantity)

본 프로젝트 1편 = 이미지 6~7장. 시즌 1 (13 단원) ≈ 90장.

| 도구 | 1편(7장) | 시즌1(90장) | quality 제한 | quantity 제한 |
|---|---|---|---|---|
| **Nano Banana** | ~$0.27 | ~$3.5 | 해상도/품질 tier 없이 균일 (1290 tok) | free tier 일 한도 후 종량 |
| **Nano Banana 2** | $0.32~1.06 | $4~13.6 | 0.5K~4K 해상도별 | Batch 반값 |
| **GPT Image 1.5** | $0.06~1.4 | $0.8~18 | Low/Med/High tier | tier 낮추면 저가·저품질 |
| **GPT Image 2** | $0.04~1.5 | $0.5~19 | tier | — |
| **Midjourney Standard** | (구독 $30/월 내) | 월 ~900장 fast | 구독 tier | Fast 한도 후 Relax(느림) |
| **Flux (aggregator)** | $0.06~0.28 | $0.7~3.6 | 모델 variant (Klein~Pro) | API rate limit |
| **SD 로컬** | $0 | $0 | GPU·모델 의존 | 무제한 (시간) |

→ 본 프로젝트 규모(연 100장 미만) = **어느 도구든 비용 미미** ($0.5~19/시즌). 비용보다 **캐릭터 일관성 + API 자동화**가 결정 요인.

---

## 4. 알려진 기본 품질 (특성)

| 도구 | 강점 | 약점 |
|---|---|---|
| **Nano Banana** | 일관성·편집·world knowledge·대화형 | 초고해상도는 v2 필요 |
| **GPT Image** | 자연어 이해·프롬프트 충실도·텍스트 렌더 | 일관성 보통, 화풍 다소 평이 |
| **Midjourney** | 예술성·미적 완성도 최고 | API 없음, 프롬프트 충실도 낮음(해석 강함) |
| **Flux** | 사실성·해부학·open-weight | 일관성 추가 setup 필요 |
| **SD** | 완전 제어·무료·확장(LoRA) | 품질 모델 의존, 설정 복잡 |

---

## 5. 프롬프트 변환 난이도 + 특성 (기본 → 툴 특화)

> 본 프로젝트 기본 프롬프트 = [5-image_prompts.md](../../40_experiments/exp-002-build-unit01/5-image_prompts.md) (도구 무관 자연어 + STYLE/CHAR 블록).

| 도구 | 변환 난이도 | 변환 작업 |
|---|---|---|
| **Nano Banana** | ⭐ 매우 낮음 | 자연어 그대로. 일관성 = CHAR reference 이미지를 입력으로 첨부 (대화형) |
| **GPT Image** | ⭐ 낮음 | 자연어 그대로. 일관성 = reference 멀티이미지 입력 |
| **Midjourney** | 중간 | 문장 → 키워드 압축 + `--ar 16:9 --cref <URL> --cw 100 --style raw`. negative 대신 `--no` |
| **Flux** | 중간 | 키워드화 + negative prompt 추가 |
| **SD** | 높음 | 키워드화 + negative + 시드 + IPAdapter/ControlNet 워크플로우(ComfyUI) |

→ **자연어 기반(Nano Banana / GPT Image) = 본 프로젝트 프롬프트 거의 그대로 사용.** 키워드 기반(MJ/SD)은 압축·파라미터화 필요.

---

## 6. NCC 추천 (본 프로젝트)

| 우선 | 도구 | 이유 |
|---|---|---|
| 🥇 | **Nano Banana** | 캐릭터 일관성 최강(본 프로젝트 핵심) + $0.039 저렴 + Gemini API key 무료(Cloud 결제 무관) + 자연어 프롬프트 그대로 + NCC 자동 |
| 🥈 | **GPT Image 1.5/2** | OpenAI key 있으면 자연어 그대로 + reference 입력 + 품질 우수 |
| 🥉 | **Flux (API)** | 저렴 + open-weight, 단 일관성 IPAdapter setup |
| 보조 | **Midjourney** | 표지/핵심 1장만 수동 고품질 (API 없어 양산 부적합) |

**본 프로젝트 결론**: Nano Banana 1순위. 에라토 reference 1장 생성 → 멀티이미지 입력으로 S2·S4 일관성. Gemini API key = AI Studio 무료 발급 (이전 Google Cloud TTS 결제 SMS 막힘과 **별개**).

---

## 7. 캐릭터 일관성 비교 (본 프로젝트 핵심)

에라토스테네스 S2·S4 동일 얼굴 = 본 단계의 최대 난제.

| 도구 | 일관성 기법 | 강도 | NCC 자동 |
|---|---|---|---|
| **Nano Banana** | reference 이미지 입력 + "같은 인물" 자연어 + 멀티이미지 blend | ★★★★★ | ✅ |
| **GPT Image** | reference 멀티이미지 입력 | ★★★ | ✅ |
| **Midjourney** | `--cref <URL> --cw 100` | ★★★★ | ❌ (수동) |
| **Flux Kontext** | 편집 기반 일관성 | ★★★ | ✅ |
| **SD** | IPAdapter / ControlNet / LoRA 학습 | ★★★★ (LoRA 시 ★★★★★) | ✅ (setup 후) |

→ **Nano Banana = 자동 + 최강 일관성** 조합. 본 프로젝트 최적.

---

## 8. setup 가이드 (Nano Banana, 1차)

```
1. https://aistudio.google.com 접속 (Google 계정 — Gmail)
2. "Get API key" → 새 key 생성 (무료)
3. ⚠️ 이미지 생성 = Google Cloud billing 연결 필수 (free tier 0)
   → AI Studio / Cloud Console 에서 결제 계정 연결
4. PowerShell 영구 설정:
   [System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY','<key>','User')
5. python -m pip install google-genai  (NCC python = 3.14 에 설치 — Nick PowerShell pip 와 환경 다름 주의)
6. NCC 에 알림 → NCC 자동 생성 (PowerShell 경유 key 추출)
```

> **2026-05-29 실측 상태**: key 발급·SDK import·API 도달 = ✅. 단 이미지 생성 = 429 `limit: 0` (billing 미연결). 모델 ID = `gemini-2.5-flash-image` (내부적으로 `gemini-2.5-flash-preview-image` 라우팅). 장당 ~1290 tok = $0.039 (billing 시).
> **NCC python 주의**: NCC Bash 의 python = `C:\Users\admin\AppData\Local\Programs\Python\Python314`. Nick 이 PowerShell 에서 pip install 하면 다른 환경일 수 있음 → NCC 가 `python -m pip install` 로 동일 환경에 설치해야 NCC 자동 생성 가능.

생성 흐름 (NCC):
```
1. 에라토 reference 1장 생성 (CHAR_ERATO 프롬프트)
2. Nick 확인 (얼굴 OK?)
3. reference 입력 + S2/S4 프롬프트 → 일관 생성
4. S1/S5/S6 장면 생성
5. 16:9 / no text / 시대 정확성 검증
```

---

## 9. 변경 이력

- 2026-05-29 v1: 신규. exp-002 STEP 5 도구 비교. DALL-E 3 제거(2026-05-12) 반영, Nano Banana 1차 추천. Nick 요청(API/요금/품질/프롬프트 변환 난이도).
