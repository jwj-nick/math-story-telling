---
name: se-video-image
description: 영상 제작 시스템의 단계 [영상 3] 이미지 스킬. 단계 [영상 1] 스토리보드의 이미지 명세(부록 B)와 캐릭터 reference·시대 풍경을 받아 장면별 이미지 프롬프트(도구 무관) + 캐릭터 일관성 기법 + (도구 결정 시) 실제 AI 이미지 생성을 수행한다. 입력(스토리보드 부록 B / 캐릭터 description / 시대 팔레트 / 이미지 도구 선택 / (옵션) reference 이미지)을 받아 동작(입력 align → 공통 스타일·캐릭터 블록 정의 → 장면별 프롬프트 → 도구별 변형 → (옵션) 생성 → 검증)을 진행. math-story-telling 영상의 이미지 프롬프트 작성, 캐릭터 일관성 기법, 시대 정확성 검증, AI 이미지 생성 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료(40_experiments/exp-NNN/3-storyboard.md 부록 B, era-ancient 팔레트)를 참조만 함. 외부 도구: DALL-E 3 / gpt-image-1 (OpenAI API) / Midjourney (Discord) / Stable Diffusion (로컬 ComfyUI).
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 영상 3 이미지 (IM1~IM6)
  ssot: 11_video_gen_process/70_tools/se-video-image/SKILL.md
  version: "0.1"
  status: 시드 (exp-002 STEP 5 시범 실행 후 reverse-engineering 정형화)
allowed-tools: Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch
---

# se-video-image — 영상 3 이미지 스킬

본 스킬은 영상 제작 시스템의 단계 [영상 3]. 단계 [영상 1] 스토리보드의 이미지 명세(부록 B)를 받아 *장면별 이미지 프롬프트* + 캐릭터 일관성 기법 + (도구 결정 시) 실제 AI 이미지를 생성한다. 출력은 다음 단계 [영상 4] 모션 + [영상 5] 렌더의 직접 입력.

상위 frame: [INTEGRATED_PLAN](../../../11_video_gen_process/00_charter/INTEGRATED_PLAN.md) §5.0 skill chain.

원칙:
- 본 스킬은 외부 자료를 **참조**만 한다.
- **도구 무관 프롬프트 우선** (STEP 4 narration.txt 패턴 동일) → 도구 결정 후 변형.
- 도구 비교는 [`image-tools-guide.md`](./image-tools-guide.md) 참조 (API/요금/품질/캐릭터 일관성/프롬프트 변환 난이도).
- **1차 추천 도구**: Google Nano Banana (Gemini 2.5 Flash Image) — 캐릭터 일관성 최강 + API + 자연어 프롬프트.

---

본 v0.1 body 는 **exp-002 STEP 5 시범** 으로 작성됨 (2026-05-28). 시범 결과: [`../../../11_video_gen_process/40_experiments/exp-002-build-unit01/5-image_prompts.md`](../../../11_video_gen_process/40_experiments/exp-002-build-unit01/5-image_prompts.md).

---

## 입력 (2 필수 + 3 옵션)

| # | 입력 | 형식 | 출처 |
|---|---|---|---|
| 1 | 스토리보드 이미지 명세 | `3-storyboard.md` 부록 B + §0.1 캐릭터 + §0.2 풍경 | 40_experiments/exp-NNN/ |
| 2 | 시대 팔레트 | era-ancient 등 색·건축·의복 | storyboard §0.2 |
| 3 (옵션) | 이미지 도구 | DALL-E3 / gpt-image-1 / Midjourney / SD | 1차 = 도구 무관 프롬프트 |
| 4 (옵션) | reference 이미지 | 인물 1장 (일관성 기준) | 없으면 description 만 |
| 5 (옵션) | 옛 baseline 프롬프트 | 경로 | 외부 의존 0 |

---

## 동작 (IM1~IM6)

### IM1. 입력 align
- storyboard 부록 B (이미지 N장 명세) + §0.1 캐릭터 description + §0.2 풍경·팔레트 확인
- 재사용/대체 식별: SVG 가능 장면(격자 등), 이미지 재사용 장면(S6=S1)

### IM2. 공통 스타일 블록 정의
- 매 프롬프트 최상단 삽입할 STYLE 블록: 시대·팔레트·16:9·**no text**·여백·anachronism 차단
- **16:9 는 STYLE 텍스트뿐 아니라 생성 API `image_config.aspect_ratio="16:9"` 로도 강제** (IM6 ⭐). 텍스트만으로는 정사각 반환됨 → 크롭 손실.

### IM3. ⭐ 캐릭터 일관성 블록 정의 (핵심)
- 인물별 **고정 묘사 블록** (CHAR_*): 나이·의복·소지품·표정·톤
- 같은 인물 여러 장면 = 블록 **그대로 재삽입**
- **reference 이미지 1장 우선 생성** → 후속 장면 일관성 기준 (cref/IPAdapter/멀티이미지 입력)
- 생성 순서: reference → 그 인물 장면 → 풍경 장면

### IM4. 장면별 프롬프트
- [STYLE] + [CHAR_*] (해당 시) + 장면 고유 묘사 (구도·광원·여백)
- **영어 프롬프트** (이미지 모델 우수) + 한국어 설명 병기
- split 장면(좌우 인물) = 2장 별도, 렌더에서 합성

### IM5. 도구별 변형 (도구 결정 시)
- DALL-E3/gpt-image-1: 자연어 그대로 (gpt-image-1 = reference 멀티이미지 입력)
- Midjourney: 키워드화 + `--ar 16:9 --cref <URL> --cw 100`
- SD: 키워드 + negative + 시드 고정 + IPAdapter/ControlNet

### IM6. 생성 + 검증 (NCC 자율 — Nano Banana, 2026-05-29 검증)
- 검증: 캐릭터 일관성 / 시대 정확성 / no text / 16:9 / 여백 (NCC 멀티모달로 직접 Read해 1차 스크리닝)
- **NCC 자율 생성 패턴** (Gemini Tier1 활성 후):
```python
# key: PowerShell 경유 GEMINI_API_KEY 추출 (User scope). NCC python 3.14 + google-genai.
import os, pathlib
from google import genai
from google.genai import types
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def gen(prompt, out, ref_paths=None):
    contents = [prompt]
    if ref_paths:  # 캐릭터 일관성: reference 이미지 함께 전달
        for rp in ref_paths:
            contents.append(types.Part.from_bytes(data=pathlib.Path(rp).read_bytes(), mime_type="image/png"))
    resp = client.models.generate_content(
        model="gemini-2.5-flash-image", contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=['Text','Image'],
            image_config=types.ImageConfig(aspect_ratio="16:9")))  # ⭐ 네이티브 16:9
    for p in resp.candidates[0].content.parts:
        if getattr(p,"inline_data",None) and p.inline_data.data:
            pathlib.Path(out).write_bytes(p.inline_data.data); return True
    return False

# 순서: ① ref(인물) 생성 → ② 인물 장면 = gen(prompt, out, ref_paths=[ref]) 로 일관성
```
- 도구 대안: gpt-image-1(자연어) / Midjourney(--cref, 수동) / SD(IPAdapter)

> ⭐ **네이티브 16:9 필수 (unit-02 학습, 2026-05-30)**: `image_config=types.ImageConfig(aspect_ratio="16:9")` 를 **반드시 지정**. 미지정 시 Nano Banana 가 1024×1024 정사각을 반환 → 렌더의 center-crop 이 상하 21.9% 잘라내 **인물 머리/얼굴이 잘림**. 16:9 지정 시 1344×768 → 렌더 crop 무손실(~1.5%). exp-002(unit-01)는 정사각 생성 후 크롭이라 인물 클로즈업에서 머리 잘림 발생 → unit-02부터 표준.
> ⭐ **인물 클로즈업 = 머리 위 여백(headroom) 명시**: 프롬프트에 *"frame so the ENTIRE head and face are fully visible with comfortable headroom ABOVE the head — do NOT crop the top of the head"* 삽입. 16:9 생성 + headroom 지시 2중 안전장치.

---

## 출력

- `<exp>/5-image_prompts.md` (프롬프트 — 도구 무관 + §도구별 변형)
- `<exp>/5-images/ref-*.png`, `s1-*.png` ... (이미지, gitignore)

---

## 평가 기준

| 항목 | 합격 |
|---|---|
| 이미지 장수 | storyboard 부록 B 부합 (재사용·SVG 반영) |
| **캐릭터 일관성** | 인물 묘사 블록 분리 + reference 우선 생성 |
| 시대 정확성 | anachronism 차단 (의복·건축·도구) |
| 텍스트 없음 | no text/letters (자막은 렌더 오버레이) |
| 종횡비 | 16:9 (생성 시 `aspect_ratio="16:9"` 강제, 정사각 반환 금지) |
| 인물 프레이밍 | 머리/얼굴 온전 + headroom (크롭에 잘리지 않음) |
| **수학 그래프 정확성** | 그래프·다이어그램 = **개념과 모양 일치 필수** NCC 멀티모달 검증. 예: 반비례 = 감소 쌍곡선(S자·증가 금지), 정비례 = 원점 통과 직선 (unit-06 학습: 첫 S4가 S자곡선 오류 → 재생성) |
| **🔥 추상 다이어그램 강제구문** | 기하·통계 개념도/데이터그래픽을 그냥 요청하면 Nano Banana가 *장면(courtyard 등)* 으로 렌더 → 개념 흐려짐. **"a clean minimal GEOMETRY DIAGRAM / DATA-GRAPHIC, flat, NO people, NO scene, NO landscape, dark charcoal bg, glowing thin gold wireframe lines, like an elegant textbook figure"** 강제. 개수·배치·색을 명시("EXACTLY FIVE distinct solids in a row", "blue wedges dominating")해야 정확 (u10·11·13 학습) |
| **🔥 클로징 한 단어 구성** | 한 단어 오버레이가 인물 얼굴/밝은 영역과 충돌 → 클로징 이미지는 **"인물(또는 엠블럼)을 좌측 1/3 에, 우측 2/3 는 빈 어두운 하늘/배경, NOTHING in that area"** 로 생성하고 단어를 `x≈0.62~0.66` 우측 어두운 영역에 배치 (u10·12·13 학습) |
| 여백 | caption space 30%+ |
| 팔레트 | 시대 팔레트 일관 |
| 도구 비교 | 도구별 변형 § 작성 |

---

## QnA 패턴 시드

- *"이미지 도구 = 도구 무관 프롬프트 먼저 / DALL-E / MJ / SD?"*
- *"격자·다이어그램 = 이미지 생성 / SVG(se-math-figure)?"*
- *"reference 이미지 = 생성 / 기존 / description 만?"*

## 리서치 패턴 시드

1. 시대 시각 자료 (의복·건축·도구) — Wikipedia/박물관 (anachronism 검증)
2. 도구별 프롬프트 문법 — 공식 docs
3. 캐릭터 일관성 기법 — cref/IPAdapter/seed

---

## 진화 메커니즘

- **v0.1** (2026-05-28) — exp-002 STEP 5 시범. 도구 무관 프롬프트 + 캐릭터 일관성 2단계(블록+reference) + SVG/재사용 식별. 현행.
- **v0.2** (예정 — 도구 결정 + 실제 생성 후):
  - 캐릭터 일관성 실측 (도구별 cref/IPAdapter 효과)
  - gpt-image-1 API 자동 생성 패턴 (OpenAI key)
  - 시대 정확성 audit 체크리스트 정밀화
  - `image-tools-guide.md` 신설 (DALL-E/MJ/SD 비교 + 가격)
- **v0.3+** = 다음 단원 일반화 + 인물 reference 풀 (재사용).

---

## 호출 방법

```yaml
스킬: se-video-image
입력:
  1. 스토리보드 부록 B: 40_experiments/exp-NNN/3-storyboard.md
  2. 시대 팔레트: storyboard §0.2 (era-*)
  3. (옵션) 이미지 도구: 도구 무관(1차) / DALL-E / MJ / SD
  4. (옵션) reference 이미지: 인물 1장
출력:
  - 40_experiments/exp-NNN/5-image_prompts.md
  - 40_experiments/exp-NNN/5-images/*.png (gitignore)
다음 단계: se-video-motion (STEP 6) + se-video-render (STEP 7)
```

본 시범 호출 예시: [`../../../11_video_gen_process/40_experiments/exp-002-build-unit01/5-image_prompts.md`](../../../11_video_gen_process/40_experiments/exp-002-build-unit01/5-image_prompts.md).
