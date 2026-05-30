<!-- 50_channel/season-1-ancient/unit-04-diophantus/5-image_prompts.md / STEP 5 [이미지] / se-video-image -->

# 단원 4 이미지 프롬프트 — 디오판토스 / Nano Banana 네이티브 16:9

> **스킬**: se-video-image v0.2 (네이티브 16:9 + headroom) / **도구**: Nano Banana(Tier1), `gen_images.py`
> **출력**: `5-images/` 7장 (1344×768, no-text) / **실행**: 2026-05-30

## 0. STYLE (3세기 알렉산드리아, era-ancient)
```
3rd-century Alexandria, Roman Egypt, aged Hellenistic harbor city, warm low evening
light, palette terracotta/ochre/bronze/slate-blue, weathered stone + papyrus,
16:9, NO text/letters/numerals/modern, caption space, 시대정확(그리스 himation·
파피루스 두루마리·석조 묘비·알렉산드리아 도서관)
```
- ⭐ 네이티브 16:9(`aspect_ratio="16:9"`) + 인물 headroom(IM6 학습)

## 1. CHAR_DIOPHANTUS (ref→S5)
```
디오판토스: 3세기 알렉산드리아 학자, 50대 후반, 흰 그리스 himation, 짧은 회색 수염,
파피루스 두루마리, 사색적·약간 신비로운 표정(거의 알려지지 않은 인물), 따뜻한 등불.
```

## 2. 장면별 (전체=gen_images.py)
| ID | 주체 | ref |
|---|---|---|
| ref-diophantus | 인물 정면 + headroom | 기준 |
| S1 | 알렉산드리아 황혼 항구·도서관·등대 + 학자 실루엣 | — |
| S2 | 그리스 석조 묘비(조각·월계관, 글자X) | — |
| S3 | 인생 띠(분수 분할) + 물음표→glyph (추상) | — |
| S4 | 저울 + 빛으로 채워진 인생 띠(추상, x=84는 drawtext) | — |
| S5 | 디오판토스 + 아리스메티카 두루마리(prose 질감) | ref |
| S6 | 오래된 책 여백 + 깃펜 손(얼굴X, 페르마) | — |

7장 네이티브 16:9 · no-text. 수식(x=84 등)·한글 = drawtext.

## 3. 검증 (NCC)
- [x] 7장 16:9(1344×768) 크롭손실0 / 캐릭터 일관(ref→S5) / headroom
- [x] 시대 정확(3세기 알렉산드리아, anachronism 0) / no-text
- [x] 인생 띠 모티프(S2·S3·S4) — 분수→x→84
