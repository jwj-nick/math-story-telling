<!-- 20_step_guides/05_step5_image.md / STEP 5 [영상 3] 이미지 심화 가이드 -->

# STEP 5 — 이미지 (영상 3) 심화 가이드

> **STEP**: 5 / 8 · **단계**: [영상 3] 이미지 · **skill**: `se-video-image` v0.1
> **상위 frame**: [`../00_charter/PURPOSE.md`](../00_charter/PURPOSE.md) · [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md)
> **실제 산출물(exp-002)**: [`5-image_prompts.md`](../40_experiments/exp-002-build-unit01/5-image_prompts.md) + `5-images/` (PNG 7장)
> **본 문서는 단독으로 읽혀도 완결되도록 작성되었다.**

---

## 1. Step 개요

STEP 5는 STEP 3에서 만든 **스토리보드의 시각 단서**(부록 B 이미지 명세 + §0.1 캐릭터 description + §0.2 시대 풍경 팔레트)를 받아, 이를 **장면별 이미지 프롬프트**로 번역하고, AI 이미지 도구로 **실제 장면 이미지**를 생성하는 단계다. 핵심은 두 가지 — (1) 어떤 도구를 쓰더라도 통하는 **도구 무관 자연어 프롬프트**를 먼저 만들고, (2) 같은 인물(에라토스테네스)이 여러 장면(S2·S4)에서 **동일한 얼굴**로 나오도록 하는 **캐릭터 일관성 2단계 기법**(고정 묘사 블록 + reference 이미지 우선 생성)을 적용하는 것이다.

**4축 기여**: 본 step은 **B축(흥미 유발)**에 직접 기여한다. 중1 딸이 에라토스테네스라는 인물을 "한 사람"으로 인식하려면, 장면이 바뀌어도 같은 얼굴이어야 한다. 일관성이 깨지면 인물 몰입(흥미)이 무너진다. 부차적으로 **A축(개념)**에도 닿는다 — S3의 1~30 소수의 체 격자는 *이미지가 아니라 SVG*로 렌더해 개념의 정확성을 지킨다(이미지 생성에 맡기면 숫자가 깨진다).

**파이프라인 위치**:
```
STEP 3 스토리보드 ──(부록 B 이미지 명세 + §0.1 캐릭터 + §0.2 팔레트)──▶ STEP 5 이미지
                                                                          │
                                          STEP 5 산출 PNG ──▶ STEP 6 모션(ken burns/pan) ──▶ STEP 7 렌더(FFmpeg zoompan)
```
- **선행**: STEP 3 스토리보드(시각 명세 제공). 단, STEP 4 나레이션과는 **병렬 독립** — 음성과 이미지는 서로 입력이 아니다.
- **후행**: STEP 6 모션(이 PNG에 카메라 워크 부여) → STEP 7 렌더(클립화). STEP 5의 PNG는 모션·렌더의 **직접 원소스**다.

**본질적 난제**:
1. **캐릭터 일관성** — AI 이미지 모델은 매 생성마다 다른 얼굴을 그린다. "에라토스테네스 S2·S4 동일 얼굴"은 본 단계 최대 난제이며, 도구 선택을 좌우하는 결정 요인이다.
2. **시대 정확성(anachronism 차단)** — 헬레니즘기 알렉산드리아 장면에 현대 물체·잘못된 의복·잘못된 건축이 끼어들면 고증이 무너진다. 자연어 프롬프트만으로 모델의 "상상"을 통제해야 한다.

---

## 2. Workflow (절차) — IM1~IM6

`se-video-image` 스킬은 6개 액션(IM1~IM6)으로 동작한다. 입력 align → 공통 블록 → 캐릭터 블록 → 장면별 프롬프트 → 도구별 변형 → (도구 결정 시) 생성·검증의 흐름이다.

| 액션 | 무엇 | 입력 → 출력 |
|---|---|---|
| **IM1** 입력 align | 스토리보드 부록 B + §0.1 캐릭터 + §0.2 팔레트 확인. 재사용/SVG 장면 식별 | 스토리보드 → 이미지 장수·생성 우선순위 |
| **IM2** 공통 스타일 블록 | 매 프롬프트 최상단에 넣을 STYLE 블록(시대·팔레트·16:9·no text·여백·anachronism 차단) | 팔레트 → STYLE 블록 |
| **IM3** ⭐ 캐릭터 일관성 블록 | 인물별 고정 묘사 블록(CHAR_*) 정의 + reference 우선 생성 전략 | §0.1 description → CHAR_* 블록 |
| **IM4** 장면별 프롬프트 | [STYLE]+[CHAR_*]+장면 고유 묘사(구도·광원·여백). 영어 + 한국어 병기 | 부록 B → 장면 프롬프트 N개 |
| **IM5** 도구별 변형 | 도구 결정 시 변환(자연어 그대로 / 키워드+파라미터) | 도구 무관 프롬프트 → 도구 특화 |
| **IM6** 생성 + 검증 | API 자동 또는 수동 생성 → 일관성/시대/no text/16:9/여백 검증 | 프롬프트 → PNG + 검증 |

**실제 동작 순서(생성 우선순위)** — 이것이 일관성의 핵심:
```
① reference(에라토 정면 1장)  ──▶ ② 그 reference로 S2 생성  ──▶ ③ 같은 reference로 S4 생성
   (얼굴 기준 확정)                 (S2 = ref 얼굴)                (S4 = ref 얼굴 → S2와 동일)
                                                                              │
④ S1 무세이온(인물 무관)  ⑤ S5 유클리드+류후이(별개 인물)  ⑥ S3 손 배경(격자는 SVG)
   ⑦ S6 = S1 재사용(생성 X, 자막만 오버레이)
```
인물이 들어가는 장면은 **reference를 먼저 만들고 그 다음에** 생성한다. 인물 무관 장면(S1)·별개 인물 장면(S5)은 순서가 자유롭다.

**의사결정 포인트(분기)**:
1. **이미지 vs SVG** — 격자·다이어그램(S3 1~30 소수의 체)은 이미지 생성이 아니라 `se-math-figure`의 네이티브 SVG/JSXGraph로. 이유: 숫자 정확성 + 비용. → exp-002에서 S3 격자 = SVG 처리 결정.
2. **신규 생성 vs 재사용** — 동일 풍경(S6 = S1 도서관 echo)은 재사용 + 자막 오버레이. → 비용·일관성 절감.
3. **split 장면** — 좌우 인물(S5 유클리드/류후이)은 한 장에 합성하지 않고 **2장 별도 생성** → STEP 6/7에서 swipe 합성.
4. **도구 무관 → 도구 특화** — 1차는 항상 도구 무관 자연어 프롬프트. 도구 결정 후 IM5에서 변형(STEP 4 narration.txt가 도구 무관 텍스트를 먼저 만드는 패턴과 동일).

---

## 3. Skill / Agent / Tools / Context

### 사용 skill
- **`se-video-image` v0.1** (status: 시드 — exp-002 STEP 5 시범 후 reverse-engineering 정형화)
- SSOT: `11_video_gen_process/70_tools/se-video-image/SKILL.md`
- 핵심 동작: 입력 align → 공통 STYLE 블록 → 캐릭터 일관성 블록 → 장면별 프롬프트 → 도구별 변형 → (옵션) 생성·검증
- allowed-tools: `Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch`

### 외부 이미지 도구 (선택 근거)
도구 비교 SSOT: [`image-tools-guide.md`](../70_tools/se-video-image/image-tools-guide.md). 본 프로젝트 결정 요인은 **비용이 아니라 캐릭터 일관성 + API 자동화**다(연 100장 미만 → 어느 도구든 시즌당 $0.5~19로 비용 미미).

| 우선 | 도구 | API | 장당 요금 | 일관성 | NCC 자동 | 선택 근거 |
|---|---|---|---|---|---|---|
| 🥇 | **Google Nano Banana** (Gemini 2.5 Flash Image) | ✅ Gemini API/AI Studio/Vertex | **$0.039** (1290 tok) | ★★★★★ (멀티이미지 blend) | ✅ | 일관성 최강 + 자연어 그대로 + 저렴 |
| 🥈 | **GPT Image 1.5 / 2** (OpenAI) | ✅ OpenAI | $0.005~0.25 | ★★★ (reference 입력) | ✅ | OpenAI key 있으면 자연어 그대로 + 품질 우수 |
| 🥉 | **Flux.2** (FAL/Replicate) | ✅ | $0.008~0.10 | ★★★ (IPAdapter/Kontext) | ✅ | open-weight 저렴, 단 일관성 setup 필요 |
| 참고 | **Midjourney V8** | ❌ Discord 수동 | 구독 $10~120/월 | ★★★★ (`--cref`) | ❌ | 예술성 최고지만 공식 API 없음 → 양산 부적합 |
| 참고 | **Stable Diffusion 3.5** | ✅/로컬 무료 | $0.008~0.04 / $0 | ★★★★ (LoRA 시 ★★★★★) | ✅(setup 후) | 완전 제어·무료, 단 ComfyUI 설정 복잡 |

> ⚠️ **DALL-E 3는 2026-05-12 OpenAI API에서 제거** → GPT Image 1.5로 대체. (옛 프롬프트의 "DALL-E" 언급 = GPT Image로 해석)

### 참조 context (SSOT)
- **스토리보드 부록 B** (`3-storyboard.md`) — 이미지 장수·주체·재사용/SVG 명세
- **스토리보드 §0.1** — 캐릭터 description (에라토/유클리드/류후이 외형)
- **스토리보드 §0.2 / era-ancient 팔레트** — 테라코타 #C2683E / 황토 #D4A574 / 청동 #876A4E / 등대 화염 #E89B4F + 도리아식 기둥·파로스 등대·죽간

### agent 활용
- 본 step은 단독 skill 호출(`se-video-image`). orchestrator는 STEP 3 부록 B를 입력으로 넘기고 산출 PNG를 STEP 6에 연결한다.

---

## 4. User Input (Nick 입력)

| 입력 | 시점 | 형식 | 필수/선택 | HITL |
|---|---|---|---|---|
| **이미지 도구 결정** | IM5 전 | "도구 무관 먼저" / "Nano Banana" / "GPT Image" / "MJ" / "SD" | 선택(1차는 도구 무관) | ✅ 분기 결정 |
| **reference 이미지** | IM3 | 인물 사진 1장 (일관성 기준) | 선택(없으면 description만) | — |
| **reference 얼굴 OK?** | IM6 중 | reference 1장 생성 후 확인 | — | ✅ **핵심 게이트** |
| **S3 SVG / S6 재사용 동의** | IM1 | yes/no | 선택 | ✅ |
| **(billing 결정)** | Nano Banana 사용 시 | Google Cloud 결제 연결 / web 수동 / 타 도구 | 선택 | ✅ 비용 게이트 |

**가장 중요한 HITL = reference 게이트**: 에라토 reference 1장을 먼저 생성하고, Nick이 "이 얼굴 OK?"를 확인한 **다음에** S2·S4를 그린다. reference가 틀린 채 후속을 생성하면 6장 전체가 잘못된 얼굴이 된다. exp-002 §5 Nick 검증 항목에도 "캐릭터 일관성(에라토 S2·S4 동일 얼굴) — 도구로 생성 후 확인"이 명시되어 있다.

---

## 5. Step Output (산출물)

### 파일 형식 + 위치 규약
```
40_experiments/exp-NNN/
├── 5-image_prompts.md      ← 프롬프트 (도구 무관 + §6 도구별 변형 + §6.5 web copy&paste)
└── 5-images/               ← PNG (gitignore)
    ├── 1-Eratosthenes.png   (reference)
    ├── 2-S2-Close-up.png
    ├── 3-S4-Syracuse.png
    ├── 4-S1-Museion.png
    ├── 5-S5-Euclid.png
    ├── 6-S5-LiuHui.png
    └── 7-S3-Hands.png
```

### 다음 step 연결
- `5-images/*.png` → **STEP 6 모션**: 각 PNG에 카메라 워크 부여(S1 push in, S2 zoom out, S4 pan/zoom, S5 swipe). 부록 C(모션 명세)와 짝.
- split 2장(S5좌·우) → STEP 6/7에서 horizontal swipe로 합성.
- S6은 PNG 없음 → STEP 7/8에서 S1(`4-S1-Museion.png`) 재사용 + "정리" 자막 오버레이.

### 품질 검증 기준 (자동 + Nick)
| 항목 | 합격 기준 | 검증 주체 |
|---|---|---|
| 이미지 장수 | 부록 B 부합 (재사용·SVG 반영) | NCC 자동 |
| **캐릭터 일관성** | 인물 묘사 블록 분리 + reference 우선 생성 + S2·S4 동일 얼굴 | NCC(블록) + **Nick(얼굴)** |
| 시대 정확성 | anachronism 차단 (chiton·도리아식·파피루스·죽간, 현대 물체 없음) | NCC + Nick |
| 텍스트 없음 | no text/letters (자막은 렌더 오버레이) | NCC |
| 종횡비 | 16:9 | NCC |
| 여백 | caption space 30%+ (하늘/벽/바닥) | NCC |
| 팔레트 | era-ancient 일관 | NCC + Nick |

---

## 6. 현재 구현 (exp-002 실제 사례)

### unit01 에라토스테네스 — 실제로 어떻게 했는가

**IM1 입력 align**: 스토리보드 부록 B = "총 8장(S1 재사용 시 7장)". S3 격자 = SVG(이미지 X), S6 = S1 재사용 식별. → 실제 신규 생성 = reference 포함 **7장**.

**IM2 공통 STYLE 블록** (모든 프롬프트 최상단):
```
STYLE: cinematic painterly illustration, ancient Alexandria / Hellenistic era,
golden hour warm lighting, terracotta (#C2683E) + ochre (#D4A574) + bronze (#876A4E)
+ lighthouse-flame (#E89B4F) color palette, soft depth, 16:9 aspect ratio,
NO text / NO letters / NO modern objects, ample empty space for caption overlay,
historically accurate (no anachronism in clothing/architecture/tools)
```

**IM3 ⭐ 캐릭터 일관성 2단계 기법** — 본 step의 핵심:
- **1단계 = 고정 묘사 블록(CHAR_*)**: 같은 인물이 여러 장면에 나오면, 동일 묘사 블록을 매 프롬프트 앞에 **그대로 재삽입**. exp-002의 CHAR_ERATO:
  > *Eratosthenes: a Greek scholar in his late 40s, dignified scholarly bearing, short curly beard flecked with grey, wearing a white chiton draped over the left shoulder, holding a rolled papyrus, calm thoughtful serious expression, warm-toned skin under golden light*
- **2단계 = reference 이미지 우선 생성**: ① CHAR_ERATO로 정면 reference 1장 → ② 그 reference를 입력으로 S2·S4 생성(얼굴 일관) → ③ S1·S5·S6. 묘사 블록만으로는 얼굴이 매번 미세하게 달라지므로 reference 입력이 결정적이다.

**IM4 장면별 프롬프트** — 영어 프롬프트(이미지 모델 영어 우수) + 한국어 설명 병기. 7개 장면 + reference. split(S5)은 좌·우 2장 별도(`composed for the LEFT/RIGHT half`).

### 실제 겪은 시행착오·결정

1. **도구 결정 = "도구 무관 먼저"** — Nick이 1차로 도구 비확정. 그래서 본 문서는 도구 무관 자연어 + §6 도구별 변형 표 구조로 작성됨.

2. **⭐ Nano Banana free tier = 0 (billing 장벽)** — 가장 큰 실전 발견. Gemini API key 발급(AI Studio 무료)·SDK import·API 도달은 ✅이지만, **이미지 생성 모델(`gemini-2.5-flash-image`)의 free tier 할당량 = 0**. 2026-05-29 실측 결과 `429 limit: 0` — 텍스트는 무료지만 **이미지 생성은 Google Cloud billing 연결 필수**다. 이는 이전 Google Cloud TTS 결제 SMS 장벽과 **동일 패턴**의 장벽이다. 장당 ~1290 tok = $0.039(billing 연결 시). 모델 ID는 `gemini-2.5-flash-image`(내부 `gemini-2.5-flash-preview-image`로 라우팅).

3. **우회 = Gemini web 수동 생성** — billing 검토에 며칠 소요되므로, 그동안 **gemini.google.com 웹**에서 수동 생성. 5-image_prompts.md §6.5에 copy&paste용 프롬프트 7개를 자기완결 문장으로 정리. 일관성 비법: **같은 대화 창에서 ① reference → ② S2 → ③ S4를 이어서 붙여넣기**(Nano Banana가 이전 이미지를 기억). S1·S5는 인물 무관이라 순서 자유. 팁: 16:9 안 나오면 "make it 16:9 wide", 글자 나오면 "remove all text".

4. **NCC python 환경 주의** — NCC Bash의 python = `Python314`. Nick이 PowerShell에서 pip install하면 다른 환경일 수 있어, NCC 자동 생성하려면 `python -m pip install google-genai`로 동일 환경에 설치해야 함.

### 생성 결과 (7장 PNG)

`5-images/`에 실제 7장 생성 성공 (각 ~1.9~2.2MB PNG):

| 파일 | 장면 | 주체 |
|---|---|---|
| `1-Eratosthenes.png` | reference | 에라토 정면 (일관성 기준) |
| `2-S2-Close-up.png` | S2 | 에라토 클로즈업 (ref 활용) |
| `3-S4-Syracuse.png` | S4 | 두루마리 + 시러큐스 (에라토 reuse) |
| `4-S1-Museion.png` | S1 | 무세이온 외관 (S6 재사용) |
| `5-S5-Euclid.png` | S5좌 | 유클리드 |
| `6-S5-LiuHui.png` | S5우 | 류후이 |
| `7-S3-Hands.png` | S3 | 책 분류 손 (배경, 격자는 SVG) |

→ S3 격자 = SVG, S6 = S1 재사용으로 **신규 생성 7장**(reference 포함). 부록 B 명세와 정확히 부합.

### 강점과 한계
- **강점**: 도구 무관 프롬프트라 도구를 바꿔도 재작성 불필요. 캐릭터 일관성 2단계 기법이 명문화됨. SVG/재사용 경계로 비용·정확성 절감. web 수동 우회로 billing 장벽을 뚫고 실제 7장 생산.
- **한계**:
  - 일관성 **실측 검증이 도구 생성 전까지 불가** — 2단계 기법이 실제로 S2·S4 동일 얼굴을 보장하는지는 생성 후에야 안다.
  - **billing 장벽으로 API 자동화 미달성** — web 수동은 NCC가 클릭할 수 없어 Nick의 수작업 의존. v0.2 자동 생성 패턴 미완.
  - 시대 정확성 audit이 **체크리스트 수준**(정밀 고증 자동 검증 도구 없음).

---

## 7. 개선 방향 탐색 / 아이디어 (단기 실현 가능)

현재 한계를 단기에 줄일 실현 가능한 개선들:

### 7.1 billing 장벽 우회 — "도구 사다리"
free tier 0 장벽을 회피하는 우선순위 사다리. **NCC 자동화를 잃지 않으면서** 비용·결제 장벽을 피한다.
| 우선 | 경로 | 장벽 | NCC 자동 |
|---|---|---|---|
| 1 | **GPT Image 1.5** (OpenAI key) | OpenAI 종량 결제 (이미 ElevenLabs 패턴 검증) | ✅ |
| 2 | **Flux via Replicate/FAL** | API 종량(저렴) + IPAdapter setup | ✅ |
| 3 | **Nano Banana (billing 연결 후)** | Google Cloud 결제(며칠 검토) | ✅ |
| 4 | **Gemini web 수동** | NCC 클릭 불가, Nick 수작업 | ❌ |

→ 단기 결론: **OpenAI key 1개로 GPT Image 자동화**가 billing 장벽 없이 NCC 자동을 회복하는 최단 경로. 일관성은 ★★★(Nano Banana ★★★★★보다 약함)이지만 reference 멀티이미지 입력으로 보완.

### 7.2 일관성 정량 검증 자동화
"S2·S4 동일 얼굴"을 사람 눈이 아니라 **face embedding 거리**로 자동 측정. reference와 각 장면의 얼굴 임베딩 cosine 유사도 < 임계값이면 재생성. → IM6 검증을 정량 게이트로 승격. (face-recognition / InsightFace 임베딩, 로컬 무료)

### 7.3 시대 정확성 audit 체크리스트 정밀화
현재 "no modern objects" 한 줄 → **항목별 화이트리스트/블랙리스트**로:
- 의복: chiton ✅ / himation ✅ / 단추·지퍼·바느질 솔기 ❌
- 건축: 도리아식/이오니아식 기둥 ✅ / 아치(로마 후대)·유리창 ❌
- 도구: 파피루스 두루마리/죽간/석판 ✅ / 종이책·금속펜·안경 ❌
→ 생성 후 VLM(GPT-4V급)에게 체크리스트로 자기검증 시킨 뒤 위반 시 재프롬프트.

### 7.4 프롬프트 단위 재사용 라이브러리
STYLE 블록·CHAR_* 블록을 단원마다 다시 쓰지 않도록 **블록 라이브러리**로 분리(era-ancient STYLE, CHAR_ERATO …). 다음 단원(브라마굽타 등)은 era 블록 교체 + 신규 CHAR만 추가.

### 7.5 실패/리스크 + 대응
| 리스크 | 대응 |
|---|---|
| reference 얼굴 미스 → 6장 전부 오류 | reference 게이트(Nick OK) 필수 통과 후에만 후속 생성 |
| billing 검토 지연 | web 수동 우회 프롬프트(§6.5) 상비 |
| 일관성 미달(미세 얼굴 차이) | face embedding 게이트(7.2) + reference 입력 강제 |
| split 합성 시 톤 불일치 | 좌·우 동일 STYLE 블록 + 동일 lighting 명시 |
| 텍스트 누출(글자 생성) | "remove all text" 재프롬프트 + no-text negative |

---

## 8. 고급 Workflow (상상력·창의력)

현재를 뛰어넘는 미래형 설계. "이상적이라면 이렇게."

### 8.1 캐릭터 일관성의 차세대 — reference 임베딩 / LoRA / IPAdapter 3층
2단계 기법(블록 + reference)은 시작점일 뿐. 차세대는 **3층 일관성 스택**:

| 층 | 기법 | 강도 | 적용 도구 | 본 프로젝트 의미 |
|---|---|---|---|---|
| L1 | **묘사 블록 재삽입** (현행) | ★★ | 전 도구 | 텍스트만으로 약한 일관 |
| L2 | **reference 이미지 입력** (현행) | ★★★★ | Nano Banana / GPT Image / Flux Kontext | 한 장 기준 얼굴 고정 |
| L3 | **인물 LoRA / IPAdapter 임베딩** | ★★★★★ | SD/Flux(LoRA), IPAdapter | 인물의 *정체성 자체*를 모델에 주입 |

- **인물 LoRA**: 에라토 reference 10~20장으로 소형 LoRA를 학습 → 이후 모든 장면에서 *프롬프트에 trigger word만* 넣어도 동일 얼굴. 단원이 늘어날수록 **인물 LoRA 풀**이 자산이 된다(에라토·브라마굽타·알콰리즈미 …). SKILL v0.3의 "인물 reference 풀 재사용"의 종착점.
- **IPAdapter**: 학습 없이 reference 이미지의 *정체성 특징*만 추출해 주입. ControlNet으로 포즈·구도까지 동시 제어 → "에라토가 *터미스에 앉아* 두루마리를 *왼손에* 든" 식의 세밀 통제.
- **face-swap 후처리**: 구도가 좋은 장면을 reference 얼굴로 사후 교체(InsightFace inswapper) — 일관성 최후 보정.

→ 이상: **인물 1명 = LoRA 1개 + reference 세트 1개**가 시리즈 자산. 신규 장면은 trigger word로 0.01초 일관.

### 8.2 시대 고증 자동 검증 파이프라인
프롬프트 → 생성 → **VLM 고증 심판** → 위반 시 자동 재프롬프트의 폐루프:
```
프롬프트 ──생성──▶ 이미지 ──VLM 심판(체크리스트 7.3)──▶ {합격 / 위반 항목}
                                                          │ 위반
                                                          ▼
                                          위반 항목을 negative로 추가해 재생성
```
- VLM이 "지퍼 발견 / 로마 아치 발견"을 텍스트로 보고 → NCC가 negative 보강 → 재생성. 사람 고증 검수를 자동화.
- 더 나아가 **박물관/논문 reference 이미지 RAG** — 알렉산드리아 복원도·헬레니즘 의복 도판을 검색해 reference로 동봉(고증 정확도↑).

### 8.3 장면 간 시각 연속성 (continuity)
영화 미술의 "180도 법칙"·"매칭 컷"을 차용:
- **광원 연속성**: 전 장면 golden hour → 다음 장면도 동일 광원 각도. STYLE 블록에 `light from upper-left, golden hour` 고정.
- **컬러 그레이딩 통일**: 7장 생성 후 동일 LUT 적용(테라코타 워밍) → 시리즈 룩 통일. 렌더(STEP 7) 직전 일괄 그레이딩.
- **매칭 컷 설계**: S2 에라토의 두루마리 → S4 에라토의 두루마리(같은 소품 위치) → 시청자가 "같은 시간선"으로 인식.
- **공간 일관성**: 도서관 내부 구도를 S1·S2·S3·S6에서 공유(같은 책장 배치) → 한 공간이라는 감각.

### 8.4 멀티 도구 하이브리드 파이프라인
한 도구로 전부 하지 않고, **장면 성격별 최적 도구 분담**:
| 장면 성격 | 최적 도구 | 이유 |
|---|---|---|
| 인물 일관 장면 (S2·S4) | Nano Banana / 인물 LoRA | 일관성 최강 |
| 풍경·표지 1장 고품질 (S1) | Midjourney V8 (수동) | 예술성 최고 |
| 양산·반복 장면 | GPT Image / Flux(API) | 자동·저렴 |
| 격자·다이어그램 (S3) | se-math-figure SVG | 정확성·무한 수정 |
→ NCC가 장면 메타데이터(인물 유무·다이어그램 유무)를 보고 도구를 **자동 라우팅**. 산출을 동일 LUT로 통일해 화풍 봉합.

### 8.5 컨셉아트 룩북 차용 (game/film art bible)
영화·애니메이션 제작의 **art bible(룩북)**을 단원 착수 시 먼저 생성:
- 무드보드(색·질감·광원), 캐릭터 시트(에라토 정/측/후면 + 표정 8종), 로케이션 시트(무세이온 평면·입면), 소품 시트(두루마리·죽간).
- 모든 장면 프롬프트가 이 룩북을 reference로 참조 → **단원 = 하나의 미술 세계**. 픽사/지브리의 "이 영화는 이 팔레트"처럼 시리즈 정체성을 박는다.

---

## 9. 고급 Contents 생성 방법 (품질 도약)

이 step에서만 가능한, 콘텐츠 질을 한 단계 올리는 구체 기법.

### 9.1 일러스트 화풍 통일 = 시리즈 정체성
중1 딸에게 "수학자 시리즈"가 한 세계로 느껴지려면 화풍이 통일돼야 한다.
- **고정 art direction 어휘**: `cinematic painterly illustration` + `golden hour` + 시대 팔레트를 **전 단원 공통 STYLE 헤더**로 박는다(현행 exp-002 STYLE 블록의 확장).
- **시대별 팔레트 변주, 화풍은 고정**: 고대(에라토)=테라코타/황토/청동, 중세(알콰리즈미)=사파이어/금박, 르네상스(데카르트)=차분한 그린/세피아 — **팔레트는 시대로 바뀌되 painterly 화풍·구도 문법은 고정**. 시청자가 "아, 이 시리즈"라고 즉시 안다.
- **룩북(9의 8.5)을 SSOT로**: 단원별 무드보드를 `era-palettes`에 누적 → 다음 단원 0초 출발.

### 9.2 정서 연결 — "한 사람"으로 보이게
일관성은 기술이 아니라 **정서**의 문제다. 같은 얼굴이 반복돼야 딸이 에라토를 *한 인물*로 사랑한다.
- **표정 아크**: S2(차분한 호기심) → S3(발견의 집중) → S4(도전 받은 긴장) → S6(평온한 마무리). reference는 중립, 장면마다 **감정만 변주**(얼굴 정체성 고정).
- **시선 설계**: 인물 시선이 *다음 장면 방향*을 가리키게(S2 에라토가 화면 오른쪽 → S3로 이끔). 영화의 eyeline match.
- **여백 = 자막의 무대**: caption space 30%를 단순 빈칸이 아니라 **하늘·바다·벽** 같은 정서적 공간으로(S4 지중해 수평선의 "거리감"이 아르키메데스와의 거리감 은유).

### 9.3 개념을 그림에 심기 (A축 강화)
이미지가 흥미(B)만이 아니라 **개념(A)**도 운반하게:
- S3 손이 두루마리를 *분류*하는 동작 = "분류 본능"의 시각 메타포 → 곧 1~30 격자(소수의 체)로 전환. 동작 자체가 개념의 복선.
- S5 split(유클리드 ↔ 류후이) = "인류, 같은 답에 두 번"이라는 메시지를 *구도*로 전달(좌우 대칭 = 동·서 독립 도달의 시각적 등가).

### 9.4 확장성 — 인물 reference 풀 (자산화)
- 각 인물의 reference + (장기) LoRA를 `people/<인물>/reference/`에 누적. 단원 2편, 시즌 2로 가도 **에라토가 카메오로 재등장**할 때 0초에 동일 얼굴.
- STYLE/CHAR 블록 라이브러리 → 신규 단원은 "era 교체 + 신규 인물 블록 추가"만. PURPOSE의 3단계 진화(수동 깊이 → 반복 적용 → 자동화)에서 **반복 적용 비용을 급감**시키는 자산.

### 9.5 이 step만의 차별화 포인트
- **SVG/이미지 하이브리드**: 정확성이 필요한 수학 객체(격자·그래프)는 SVG, 정서가 필요한 장면은 painterly 이미지. 양쪽의 장점만 — 다른 영상 채널이 흉내 못 내는 본 프로젝트의 정체성(`se-math-figure`와의 결합).
- **고증 + 정서의 동시 달성**: 헬레니즘 chiton·죽간의 정확성과 golden hour의 따뜻함을 한 프레임에. "공부 영상"이 아니라 "이야기"로 보이는 결정적 층위가 바로 이 이미지 단계다.

---

## 변경 이력

- 2026-05-29: 신규. STEP 5 [영상 3] 이미지 심화 가이드 9섹션 작성. exp-002 시범(7장 PNG 생성 성공, Nano Banana free tier 0 billing 장벽, web 수동 우회) 인용. 섹션 7~9 = 일관성 차세대(LoRA/IPAdapter/face-swap)·시대 고증 자동 검증·시각 연속성·멀티 도구 하이브리드·룩북/화풍 통일.
