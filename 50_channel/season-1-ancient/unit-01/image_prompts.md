# Unit 01 — AI 이미지 프롬프트 시트 (v1.5)

> Nick 작업 매뉴얼:
> 1. 아래 각 프롬프트를 Claude/ChatGPT 이미지 생성에 그대로 입력
> 2. 16:9 종횡비 옵션 명시 (영문 프롬프트에 포함됨)
> 3. 저장: `channel/season-1-ancient/unit-01/_assets/{파일명}`
> 4. 한 장 생성 후 다음으로 — 시대 일관성·인물 일관성 체크
>
> **공통 캐릭터 시트** (S3·S4 인물 일관성 유지):
> `An elderly Hellenistic Greek scholar around 70, gentle weathered face,
> short grey curly hair, light beard, wearing a simple white linen chiton
> with a worn ochre wool mantle. Calm, observing eyes. Sun-bronzed skin.`

---

## Image 1 — S2 알렉산드리아 풍경
**파일명**: `s2-alexandria-vista.jpg`
**해상도**: 1920×1080 (16:9)

### Prompt (영문)
```
Wide cinematic landscape of ancient Alexandria, Egypt, around 240 BCE, golden hour just before sunset.
Mediterranean harbor in foreground with a few wooden Greek ships, the tall Lighthouse of Pharos rising on the right with smoke at its top, the great Library of Alexandria complex visible in the middle distance with columns and palm trees.
Warm sand tones and deep teal sea, soft hazy atmosphere, dust motes in the air, painterly cinematic style, no people in close-up, vast and quiet scene.
Generous empty sky on the upper left for text overlay.
Aspect ratio 16:9.
```

### Negative
```
no modern boats, no skyscrapers, no electric lights, no text or letters in image,
no watermarks, no anachronistic clothing or items
```

### Style notes
- 톤: sand + night sky 팔레트 ("warm sand + deep teal")
- 시각적 무게: 우측의 등대 1/3 + 좌측 빈 하늘 2/3
- 학습자가 "그 시대에 있는 듯한" 감각 유발

---

## Image 2 — S3 도서관 학자
**파일명**: `s3-library-scholar.jpg`
**해상도**: 1920×1080 (16:9)

### Prompt (영문)
```
Interior of the ancient Library of Alexandria, dim warm light from oil lamps falling on tall scroll shelves filled with papyrus rolls.
In the medium-shot center-right: [공통 캐릭터 시트 — elderly Hellenistic Greek scholar around 70, gentle weathered face,
short grey curly hair, light beard, wearing a simple white linen chiton with a worn ochre wool mantle, calm observing eyes].
He is unrolling a long papyrus scroll on a wooden table, focused.
A few astronomical instruments and a small celestial globe rest on the table.
Painterly cinematic style, deep amber and bronze tones, soft chiaroscuro lighting.
Generous empty space on the left for text overlay.
Aspect ratio 16:9.
```

### Negative
```
no modern items, no books with spines, no glasses, no glass lenses, no clocks, no text in image
```

### Style notes
- 인물 캐릭터 시트 — S4와 외모 일치 필수
- 중년 아닌 노년 (BCE 194년 사망 시 80대) 묘사

---

## Image 3 — S4 막대기 실험
**파일명**: `s4-shadow-experiment.jpg`
**해상도**: 1920×1080 (16:9)

### Prompt (영문)
```
Ancient Egypt sun-baked stone plaza in Alexandria, intense midday sunlight.
A tall vertical wooden stick (gnomon) planted upright in the ground, casting a short crisp shadow on the sandy stone floor.
Geometric chalk marks faintly visible around the shadow indicating angle measurement, drawn by hand in white chalk.
In the soft background: a low stone wall with a partial map of Egypt sketched on parchment leaning against it, a brass astrolabe nearby.
The light is harsh and almost vertical, evoking the moment of solar noon.
[공통 캐릭터 시트 — elderly Hellenistic Greek scholar] partially visible in the right edge, kneeling and observing the shadow.
Painterly cinematic style, ochre and bone-white palette, dramatic high-contrast lighting.
Aspect ratio 16:9.
```

### Negative
```
no protractors, no modern measurement tools, no people in foreground,
no clouds (it should look like solar noon), no text or numbers, no compasses
```

### Style notes
- 핵심: 막대기 + 그림자 + 각도 측정 흔적
- 인물은 부분적으로만 (관찰자 시점)
- 학습자가 "측정의 순간"을 직관적으로 이해

---

## Image 4 — S5 숫자에서 현대로
**파일명**: `s5-numbers-bridge.jpg`
**해상도**: 1920×1080 (16:9)

### Prompt (영문)
```
Extreme close-up of weathered ancient papyrus laid on a wooden table.
On the papyrus: a hand-drawn grid of numbers from 1 to 30 in ancient Greek-Hellenistic numerical script,
with some numbers circled in red ink (representing primes — 2, 3, 5, 7, 11, 13, 17, 19, 23, 29),
others crossed out gently with diagonal strokes.
A thin elderly hand (just fingertips visible) is pointing to one circled number.
A small modern element subtly placed in the corner: a faint reflection of a contemporary computer chip or a glowing thin line, hinting at a 2000-year bridge from ancient mathematics to modern computing.
Warm amber light, painterly cinematic style, deep brown ink on cream parchment.
Aspect ratio 16:9.
```

### Negative
```
no modern numerals (use ancient Greek style), no English letters,
no full screen/monitor, no jarring modern objects in foreground
```

### Style notes
- 학습자에게 "옛것이 지금까지 이어진다"는 시간 다리감각
- 너무 노골적 현대 요소 X, 은유적으로만

---

## Image 5 — S6 마무리 (선택)
**파일명**: `s6-closing-light.jpg`
**해상도**: 1920×1080 (16:9)

### Prompt (영문)
```
Intimate close-up shot in a dark room: a single small oil lamp flickers warm gold,
illuminating a tightly rolled papyrus scroll on a wooden table.
The background is almost entirely black except for the warm halo of the flame.
A few floating dust motes catch the light.
Painterly cinematic style, deep blacks with golden highlights, intimate and contemplative mood.
Generous black space surrounding the lit area for text overlay.
Aspect ratio 16:9.
```

### Negative
```
no faces, no full lamp visible, no other objects, no text in image
```

### Style notes
- 여운·정적 — 다음 단원으로의 전환
- 텍스트가 잘 들어가도록 검은 여백 충분히

---

## 검수 체크리스트 (생성 후)

- [ ] 5장 모두 16:9 종횡비
- [ ] 인물(S3·S4): 외모 일관성 (같은 노년 학자)
- [ ] 시대 정확성: 토가·등대·두루마리 OK / 시계·안경·종이책 NG
- [ ] 이미지 안에 글자 없음
- [ ] 텍스트 들어갈 여백 충분
- [ ] 톤: 모래·금색·밤하늘 팔레트 일관

## 향후 (SD/MJ 전환 시)
- `image_prompts_sd.md` — Stable Diffusion 포맷 (steps, CFG, sampler)
- `image_prompts_mj.md` — Midjourney 포맷 (`--style raw --ar 16:9 --v 6.1 --cref ...`)
