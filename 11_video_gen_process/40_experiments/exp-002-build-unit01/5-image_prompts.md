<!-- exp-002 / step 5 [영상 3] 이미지 프롬프트 / se-video-image 시범 실행 결과 -->

# 단원 1 이미지 프롬프트 — 도구 무관 + 캐릭터 일관성

> **스킬**: se-video-image v0.1 시범 실행
> **입력**: [`3-storyboard.md`](./3-storyboard.md) 부록 B (이미지 8장 명세) + §0.1 캐릭터 reference + §0.2 시대 풍경
> **출력 = 다음 단계 [영상 4] 모션 + [영상 5] 렌더 의 이미지 소스**
> **도구 결정**: Nick = "프롬프트 먼저 (도구 무관)" → 본 문서 = 도구 무관 프롬프트 + §6 도구별 변형
> **실행 일자**: 2026-05-28

---

## 0. 공통 스타일 블록 (모든 프롬프트 최상단 삽입)

```
STYLE: cinematic painterly illustration, ancient Alexandria / Hellenistic era,
golden hour warm lighting, terracotta (#C2683E) + ochre (#D4A574) + bronze (#876A4E)
+ lighthouse-flame (#E89B4F) color palette, soft depth, 16:9 aspect ratio,
NO text / NO letters / NO modern objects, ample empty space for caption overlay,
historically accurate (no anachronism in clothing/architecture/tools)
```

- **16:9** 종횡비 고정
- **이미지 내 텍스트 없음** (자막은 렌더 단계 오버레이)
- **여백 30%+** (자막 공간 — 하늘/벽/바닥)
- **시대 정확성**: 그리스 의복(chiton), 도리아식 기둥, 파피루스 두루마리, 죽간. 현대 물체 금지.

## 1. ⭐ 캐릭터 일관성 reference 블록 (핵심 기법)

> 같은 인물이 여러 장면에 = **동일 묘사 블록을 매 프롬프트 앞에 그대로 삽입**. + reference 이미지 1장 우선 생성 후 재사용.

### CHAR_ERATO (에라토스테네스 — S2·S4 공유, ★ reference 우선 생성)
```
Eratosthenes: a Greek scholar in his late 40s, dignified scholarly bearing,
short curly beard flecked with grey, wearing a white chiton (ancient Greek robe)
draped over the left shoulder, holding a rolled papyrus, calm thoughtful serious
expression, warm-toned skin under golden light
```

### CHAR_EUCLID (유클리드 — S5 좌)
```
Euclid: a Greek scholar in his 60s, long flowing white beard, balding with white
hair at sides, holding a bound book (the Elements), contemplative wise expression,
white chiton, seated posture
```

### CHAR_LIUHUI (류후이 — S5 우, 동방)
```
Liu Hui: a Chinese scholar of the 3rd-century Wei dynasty, black hair tied in a
topknot, thin dark beard, holding bamboo slips (jiandu) with vertical characters,
serious focused expression, traditional Han-era dark robe, eastern aesthetic
```

→ **생성 순서**: ① CHAR_ERATO reference 1장 (정면 인물) → ② 그 reference 로 S2·S4 생성 (얼굴 일관) → ③ S1·S5·S6.

---

## 2. 장면별 프롬프트

### S1 — 무세이온 외관 (이미지 1)
```
[STYLE]
Wide establishing shot of the ancient Library and Museion of Alexandria.
Six tall Doric columns at the entrance, blurred rows of papyrus scroll shelves
inside, 3 to 5 robed scholar silhouettes walking while carrying scrolls,
the Pharos lighthouse faint on the distant coastline, long evening shadows,
vast warm sky in upper third (caption space).
```

### S2 — 에라토 클로즈업 (이미지 2, reference 활용)
```
[STYLE]
[CHAR_ERATO]
Close-up portrait of Eratosthenes, hands unrolling a papyrus scroll,
blurred library bookshelves behind him (shallow depth of field),
warm interior lamplight, calm scholarly mood, empty space to one side.
```

### S3 — 책 분류 손 (이미지 3, **배경만** — 격자는 SVG)
> 부록 B: S3 1~30 격자 = **네이티브 SVG/JSXGraph 렌더** (이미지 생성 X — 정확성+비용). 배경 이미지 1장만 옵션.
```
[STYLE]
Close-up of a scholar's hands carefully sorting and arranging rolled papyrus
scrolls on a wooden shelf in an ancient library, warm focused light,
top-down angle, plain area in frame for number-grid overlay.
```

### S4 — 두루마리 + 시러큐스 (이미지 4, 에라토 reuse)
```
[STYLE]
[CHAR_ERATO]
Eratosthenes standing on a stone terrace holding an open papyrus letter,
the blue Mediterranean sea stretching out and the distant city of Syracuse
visible across the water under afternoon light, sense of vast distance,
horizon space in upper frame.
```

### S5 — 유클리드 + 류후이 (이미지 5·6, 좌우 split)
좌(이미지 5):
```
[STYLE]
[CHAR_EUCLID]
Euclid in an ancient Greek library, holding the Elements, soft contemplative
light, composed for the LEFT half of a split frame, neutral space on right.
```
우(이미지 6):
```
[STYLE]
[CHAR_LIUHUI]
Liu Hui in a 3rd-century Chinese study, holding bamboo slips, eastern muted
warm tones, composed for the RIGHT half of a split frame, neutral space on left.
```

### S6 — 도서관 echo (S1 재사용)
> 부록 B: **S1 이미지 재사용** (fade in/out + "정리" 자막 오버레이). 신규 생성 X.
> (옵션) S1 variant — 동일 무세이온, 더 어두운 황혼 톤:
```
[STYLE]
Same Museion of Alexandria wide shot as S1, deeper dusk tones, quieter mood,
large central empty space for a single gold word overlay.
```

---

## 3. 이미지 목록 (생성 우선순위)

| # | 파일 | 장면 | 주체 | 비고 |
|---|---|---|---|---|
| ref | (1-Eratosthenes.png) | — | 에라토 정면 reference | S2·S4 일관성 기준 |
| 1 | 4-S1-Museion.png | S1 | 무세이온 외관 | S6 재사용 |
| 2 | 2-S2-Close-up.png | S2 | 에라토 클로즈업 | reference 활용 |
| 3 | 7-S3-Hands.png | S3a | 책 분류 손 | 분류 본능 (전반) |
| **8** | **8-S3.5-Sieve.png** | **S3b** | **소수의 체 (체+숫자 이중 메타포)** | **소수 2·3·5·7·11 남고 합성수 떨어짐 (후반)** |
| 4 | 3-S4-Syracuse.png | S4 | 두루마리+시러큐스 | 에라토 reuse |
| 5 | 5-S5-Euclid.png | S5a | 유클리드 | split 좌 |
| 6 | 6-S5-LiuHui.png | S5b | 류후이 | split 우 |
| (7) | (=S1 재사용) | S6 | 도서관 echo | 자막만 |

**실제 생성 8장** (ref + S1·S2·S3손·S3체·S4·S5좌·S5우, S6=S1 재사용). S3는 손→체 2장으로 내러티브 전환(2026-05-29 Nick 아이디어 = '소수의 체' 이중 메타포).

---

## 4. NCC 자동 검증

- [x] 장면별 이미지 6~7장 (부록 B 부합)
- [x] 공통 인물 묘사 블록 분리 (캐릭터 일관성 기법)
- [x] 16:9 종횡비 명시
- [x] 시대 anachronism 차단 문구 (no modern objects)
- [x] 이미지 내 텍스트 없음 (no text/letters)
- [x] 여백 (caption space) 명시
- [x] era-ancient 팔레트 일관

## 5. Nick 검증 항목

- 캐릭터 일관성 (에라토 S2·S4 동일 얼굴) — 도구로 생성 후 확인
- 시대·풍경 적합도 (의복·건축)
- S3 격자 = SVG 처리 동의 / S6 = S1 재사용 동의

## 6. 도구별 프롬프트 변형 (도구 결정 시)

| 도구 | 변형 | 캐릭터 일관성 |
|---|---|---|
| **DALL-E 3 / gpt-image-1** | 위 자연어 그대로. gpt-image-1 은 reference 이미지 입력(멀티) 지원 | 묘사 블록 반복 (약) + gpt-image reference 입력 (강) |
| **Midjourney** | 키워드화 + `--ar 16:9 --style raw`. 인물 = `--cref <ref URL> --cw 100` | --cref (강) |
| **Stable Diffusion** | 키워드 + negative: `text, watermark, modern, blurry, extra fingers, deformed`. 시드 고정 | IPAdapter / ControlNet reference (강) |

→ NCC 가 OpenAI key 받으면 gpt-image-1 로 reference→장면 자동 생성 가능 (ElevenLabs 패턴).

## 6.5 ⭐ Gemini web 수동 생성 copy&paste (2026-05-29)

> **배경**: Gemini API 이미지 생성 = free tier 0, Google billing 검토 며칠 소요 → 그동안 **Gemini web(gemini.google.com) 수동 생성**.
> **캐릭터 일관성**: 같은 대화 창에서 ① reference → ② S2 → ③ S4 *이어서* 붙여넣기 (Nano Banana 가 이전 이미지 기억). S1·S5 는 인물 무관(순서 자유).
> **팁**: 16:9 안 나오면 "make it 16:9 wide", 글자 나오면 "remove all text".

### ① 에라토 reference (먼저)
```
Create a 16:9 cinematic painterly illustration. Ancient Alexandria, Hellenistic era, golden hour warm lighting, palette of terracotta, ochre, and bronze. Historically accurate, no modern objects, no text or letters anywhere in the image.
Subject: Eratosthenes, a Greek scholar in his late 40s, dignified bearing, short curly beard flecked with grey, wearing a white chiton draped over the left shoulder, holding a rolled papyrus, calm thoughtful expression.
Composition: front-facing reference portrait, clear view of face and clothing, simple neutral background.
```

### ② S2 에라토 클로즈업 (①에 이어서)
```
Using the SAME Eratosthenes character from the previous image (same face, same beard, same white chiton):
16:9 cinematic painterly illustration, same ancient palette and lighting. Close-up of Eratosthenes unrolling a papyrus scroll with his hands, blurred library bookshelves behind him (shallow depth of field), warm interior lamplight, calm scholarly mood. Leave empty space on one side. No text in the image.
```

### ③ S4 에라토 + 시러큐스 (이어서)
```
Using the SAME Eratosthenes character (same face, beard, white chiton):
16:9 cinematic painterly illustration, same palette. Eratosthenes standing on a stone terrace holding an open papyrus letter, the blue Mediterranean sea and the distant city of Syracuse visible across the water in afternoon light, a sense of vast distance. Keep horizon/sky space in the upper frame. No text in the image.
```

### ④ S1 무세이온 외관 (인물 무관)
```
16:9 cinematic painterly illustration. Ancient Alexandria, golden hour, palette of terracotta/ochre/bronze, historically accurate, no text.
Wide establishing shot of the Library and Museion of Alexandria: six tall Doric columns, blurred rows of papyrus scrolls inside, 3 to 5 robed scholar silhouettes walking with scrolls, the Pharos lighthouse faint on the distant coast, long golden evening shadows. Large empty sky in the upper third for a caption.
```

### ⑤ S5 좌 유클리드
```
16:9 cinematic painterly illustration, ancient Greek palette (terracotta/ochre/bronze), golden lighting, historically accurate, no text.
Subject: Euclid, a Greek scholar in his 60s, long flowing white beard, holding a bound book (the Elements), contemplative wise expression, white chiton. Composed for the LEFT half of the frame, with neutral empty space on the right.
```

### ⑥ S5 우 류후이
```
16:9 cinematic painterly illustration, warm muted eastern palette, golden lighting, historically accurate, no text.
Subject: Liu Hui, a Chinese scholar of the 3rd-century Wei dynasty, black hair in a topknot, thin dark beard, holding bamboo slips with vertical characters, serious focused expression, traditional Han-era dark robe. Composed for the RIGHT half of the frame, with neutral empty space on the left.
```

### ⑦ S3 책 분류 손 (배경, 옵션 — 격자는 SVG)
```
16:9 cinematic painterly illustration, ancient library, warm palette, no text.
Close-up of a scholar's hands carefully sorting and arranging rolled papyrus scrolls on a wooden shelf, top-down angle, warm focused light. Keep a plain area in the frame for a number-grid overlay to be added later.
```

> **S6 = S1 재사용** (생성 X, 자막만 오버레이).

### ⑧ S3 보강 — "소수의 체" 이중 메타포 (2026-05-29 Nick 아이디어)
> 진짜 체(sieve) + 숫자의 체가 한 컷에. S3(분류→소수의 체)의 핵심 은유 시각화. 영상 S3 후반에 사용(손 이미지→체 이미지 전환).
```
A 16:9 cinematic painterly illustration, ancient Greek / Hellenistic setting, warm golden light, terracotta-ochre-bronze palette.
Central subject: a real ancient grain sieve — a round wooden-rimmed sieve with a woven mesh (or a bronze strainer) — tilted in dramatic warm side light.
Concept (the Sieve of Eratosthenes as a visual metaphor): numbers are being sifted like grain. Resting ON TOP of the mesh, a few glowing golden numerals — the primes 2, 3, 5, 7, 11 — stay. Falling THROUGH the holes into soft shadow below, dimmed and grey, the composite numbers 4, 6, 8, 9, 10 drop away.
The double meaning must be clear: a literal sieve AND a sieve that filters numbers. Clean legible numerals, few in number. Minimal uncluttered background. No other text.
```
> **팁**: 숫자가 너무 많으면 AI가 깨뜨림 → 소수 5개·합성수 5개로 제한. 숫자 부정확하면 "make the numerals clean and legible" 추가 지시. 16:9 안 되면 "16:9 wide".
> 변형: 숫자 대신 **점/조약돌(고대식 calculus)**로 표현하면 시대 고증↑ 교육 명확성↓ — 본 컨셉은 숫자 직접이 목적에 맞음.

---

## 7. 본 시범 한계 + retrospective 시드

| 항목 | 발견 |
|---|---|
| 캐릭터 일관성 = 묘사 블록 + reference 2단계 | 실제 생성 전까지 검증 불가 → 도구 결정 후 |
| S3 격자 = SVG (se-math-figure 영역) | 이미지/SVG 경계 — 비용·정확성 |
| S6 = S1 재사용 | 비용 절감 |
| split (S5) = 2장 별도 생성 후 렌더 합성 | 모션 단계 swipe 와 연계 |
| 프롬프트 영어 | 이미지 모델 영어 우수. 한국어 설명 병기 |
| 도구 무관 작성 → 도구별 §6 변형 | STEP 4 narration.txt 패턴 동일 |
