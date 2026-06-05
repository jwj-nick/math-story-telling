<!-- 50_channel/season-1-ancient/unit-05-descartes/5-image_prompts.md / STEP 5 / se-video-image -->

# 단원 5 이미지 프롬프트 — 데카르트 / Nano Banana 네이티브 16:9

> **스킬**: se-video-image v0.2 / **도구**: Nano Banana(Tier1), `gen_images.py` / **출력**: `5-images/` 7장(1344×768) / **실행**: 2026-05-30

## 0. STYLE (17세기 유럽 서재, era-renaissance)
```
early 17th-century Europe, candle-lit wood-paneled study, warm chiaroscuro,
palette walnut-brown/candle-gold/sky-blue/teal, books·quill·celestial globe,
16:9, NO text/letters/numerals/modern, caption space, 시대정확(레이스 칼라·코트·촛불)
```
- 네이티브 16:9 + 인물 headroom

## 1. CHAR_DESCARTES (ref→S1·S5)
```
르네 데카르트: 17세기 유럽 학자 40대, 어깨까지 짙은 갈색 곱슬머리, 콧수염, 흰 레이스 칼라+짙은 코트, 사색적이고 나른한 표정, 촛불.
```

## 2. 장면별 (전체=gen_images.py)
| ID | 주체 | ref |
|---|---|---|
| ref-descartes | 인물 정면+headroom | 기준 |
| S1 | 침대에 누운 데카르트(게으른 천재) | ref |
| S2 | 천장의 파리 + 두 거리 점선(추상) | — |
| S3 | x·y축 좌표평면 격자+원점(숫자X) | — |
| S4 | 좌표 위 직선+원(식↔그림, 숫자X) | — |
| S5 | 데카르트 깃펜으로 쓰는 손(글자 질감) | ref |
| S6 | 다섯 빛점 수렴 좌표평면(피날레, 추상) | — |

7장 네이티브 16:9 · no-text. 수식(y=2x 등)·한글 = drawtext. 인물 headroom.

## 3. 검증
- [x] 7장 16:9(1344×768) 크롭손실0 / 캐릭터 일관(ref→S1·S5) / headroom
- [x] 시대정확(17C 유럽) / no-text / 좌표축 모티프(S3·S4·S6)
