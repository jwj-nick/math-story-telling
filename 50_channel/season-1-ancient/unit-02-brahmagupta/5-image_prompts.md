<!-- 50_channel/season-1-ancient/unit-02-brahmagupta/5-image_prompts.md / STEP 5 [이미지] 프롬프트 / se-video-image -->

# 단원 2 이미지 프롬프트 — 캐릭터 일관성 + Nano Banana

> **스킬**: se-video-image v0.1 (정식 구조 양산)
> **입력**: [`3-storyboard.md`](./3-storyboard.md) 부록 B (이미지 7장) + §0.1 캐릭터 + §0.2 팔레트
> **도구**: Google Nano Banana (gemini-2.5-flash-image, Tier1) — NCC 자율 생성 (SKILL §IM6)
> **출력 = STEP 6 모션 + STEP 7 렌더 이미지 소스** (`5-images/`)
> **실행 일자**: 2026-05-29

---

## 0. 공통 스타일 블록 (STYLE)

```
STYLE: cinematic painterly illustration, 7th-century classical India,
warm dusk / lamplit night mood, palette of saffron, ochre, plum-purple,
warm clay-brown and deep night-blue, soft warm lamplight, 16:9 aspect ratio,
NO text, NO letters, NO numerals, NO modern objects, ample empty space for
caption overlay, historically accurate (7th-century Indian dress: dhoti and
draped shoulder cloth; stone observatory; clay tablets and palm-leaf manuscripts)
```

- 16:9 고정 / **이미지 내 텍스트·숫자 없음** (모든 수식·라벨·한글은 렌더 drawtext 오버레이)
- 여백 30%+ (자막 공간)
- 시대 정확성: 7세기 인도 복식·석조 천문대·점토판. 현대 물체·아라비아 숫자 금지.

## 1. ⭐ 캐릭터 일관성 reference 블록

### CHAR_BRAHMA (브라마굽타 — S2·S3 공유, ★ reference 우선)
```
Brahmagupta: an Indian astronomer-mathematician in his late 50s, warm brown skin,
short greying beard, wearing a white-and-saffron dhoti with a draped shoulder cloth,
a faint tilak mark on the forehead, holding a clay tablet (or palm-leaf manuscript),
serene thoughtful gentle expression, warm lamplight on the face
```

→ **생성 순서**: ① CHAR_BRAHMA reference 1장 → ② reference로 S2·S3 (얼굴 일관) → ③ S1·S4·S5·S6 (인물 무관/실루엣).

---

## 2. 장면별 프롬프트

### ① ref-brahmagupta (먼저)
```
[STYLE]
[CHAR_BRAHMA]
Composition: front-facing reference portrait, clear view of face and clothing,
simple neutral warm background, no text.
```

### ② S2 — 브라마굽타 + 점토판 (ref 활용)
```
[STYLE]
Using the SAME Brahmagupta character from the previous image (same face, same
greying beard, same white-saffron dhoti):
Close-up of Brahmagupta seated, holding a clay tablet, a warm oil lamp beside him,
blurred stone observatory interior behind (shallow depth of field), calm scholarly
mood, generous empty space on one side for caption. No text, no numerals.
```

### ③ S3 — 점토판 규칙판 (ref 손, 규칙은 drawtext)
```
[STYLE]
Using the SAME Brahmagupta character (same hands, same dhoti):
Top-down close-up of Brahmagupta's hands inscribing a blank clay tablet with a
stylus by warm lamplight, the tablet surface mostly empty and clean (space for
overlaid rule lines later), focused intent. No text, no numerals, no symbols.
```

### ④ S1 — 우자인 천문대 야경 (인물 무관)
```
[STYLE]
Wide establishing shot of a 7th-century Indian stone astronomical observatory in
the city of Ujjain at night, a sky full of stars, warm oil lamps glowing on the
stone terraces, one or two distant robed scholar silhouettes observing the sky,
deep night-blue sky meeting warm saffron lamplight, vast starry sky in the upper
third for caption space. No text.
```

### ⑤ S4 — 빛나는 0 + 수직선 (어둑, 숫자는 drawtext)
```
[STYLE]
A glowing single point of golden light resting at the center of a long horizontal
luminous line that stretches left and right into soft darkness, abstract and
contemplative, the right side warm and the left side cooler, faint evenly-spaced
tick marks along the line (but NO numerals, NO text), a quiet mysterious mood with
deep shadow around, central composition with empty space. No text, no numbers.
```

### ⑥ S5 — 그리스 vs 인도 split (composite)
```
[STYLE-modified: split composition]
A 16:9 split-screen composition. LEFT half: cool white Greek marble setting with
geometric line segments and a measuring rod, cold pale daylight, classical Greek
aesthetic. RIGHT half: warm Indian setting with a clay accounting tablet and warm
saffron lamplight, a horizontal line extending both directions. The right half is
brighter and warmer than the left. Clear vertical division down the middle. No
text, no numerals anywhere.
```

### ⑦ S6 — 책 인도→바그다드 + 학자 실루엣 (알콰리즈미 얼굴 X)
```
[STYLE]
A palm-leaf manuscript / bound book glowing softly, with a faint old-map feeling
of travel from India westward toward Baghdad (suggested by warm directional light
and distance, NOT by any written labels). On the far right, the dim silhouette of
a robed scholar opening the book in a Baghdad study — face hidden in shadow
(identity concealed). Warm, hopeful, cinematic. Large empty central space for a
single word overlay. No text, no letters.
```

---

## 3. 이미지 목록 (생성 우선순위)

| # | 파일 | 장면 | 주체 | reference |
|---|---|---|---|---|
| ref | `ref-brahmagupta.png` | — | 브라마굽타 정면 | 기준 생성 |
| 1 | `S1.png` | S1 | 우자인 천문대 야경 | — |
| 2 | `S2.png` | S2 | 브라마굽타 + 점토판 | ref |
| 3 | `S3.png` | S3 | 점토판 새기는 손 | ref |
| 4 | `S4.png` | S4 | 빛나는 0 + 수직선 | — |
| 5 | `S5.png` | S5 | 그리스 vs 인도 split | — |
| 6 | `S6.png` | S6 | 책→바그다드 + 실루엣 | — |

**생성 7장** (ref + S1~S6). 모두 no-text. 수식·숫자·한글 자막 = 렌더 drawtext.

## 4. NCC 자동 검증

- [x] 장면별 7장 (부록 B 부합)
- [x] 캐릭터 묘사 블록 분리 + reference 2단계 (S2·S3 일관성)
- [x] 16:9 명시
- [x] anachronism 차단 (no modern objects, 7th-c Indian dress)
- [x] 이미지 내 텍스트·숫자 없음 (자막/수식 = drawtext)
- [x] era-ancient(인도) 팔레트 일관 + 수직선 모티프
