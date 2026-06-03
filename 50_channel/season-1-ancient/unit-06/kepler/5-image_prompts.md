<!-- 50_channel/season-1-ancient/unit-06-kepler/5-image_prompts.md / STEP 5 / se-video-image -->

# 단원 6 이미지 프롬프트 — 케플러 / Nano Banana 네이티브 16:9

> **스킬**: se-video-image v0.2 / **도구**: Nano Banana(Tier1), `gen_images.py` / **출력**: `5-images/` 7장(1344×768) / **실행**: 2026-05-30

## 0. STYLE (17세기 천문대, era-modern)
```
early 17th-century astronomer's candle-lit study/observatory at night, deep starry
night-blue, palette night-blue/brass/candle-gold/brown, armillary sphere + observation
logs, 16:9, NO text/letters/numerals/modern, caption space, 시대정확(러프 칼라·가운·황동 기구)
```
- 네이티브 16:9 + 인물 headroom

## 1. CHAR_KEPLER (ref→S1·S2·S6류)
```
요하네스 케플러: 17세기 독일 천문학자 40대, 짧은 곱슬 갈색머리+수염, 흰 러프 칼라+짙은 가운, 따뜻한 표정, 별밤 촛불.
```

## 2. 장면별 (전체=gen_images.py)
| ID | 주체 | ref | 비고 |
|---|---|---|---|
| ref-kepler | 인물 정면+headroom | 기준 | |
| S1 | 천문대+천체모형+별+케플러 | ref | |
| S2 | 정다면체 끼운 행성궤도(틀린 가설) | — | |
| S3 | 타원궤도+부채꼴 면적+시소(반비례) | — | |
| **S4** | **좌 정비례 직선 / 우 반비례 감소 쌍곡선** | — | ⭐ **재생성**(첫 생성 S자곡선 오류→정확 쌍곡선). 딸 약점 정확도 |
| S5 | 공기압축 실험(보일, 얼굴X) | — | |
| S6 | 빛나는 행성 조화+천체모형(조화) | — | |

7장 네이티브 16:9 · no-text. 수식·한글 = drawtext. 인물 headroom.

## 3. 검증
- [x] 7장 16:9(1344×768) 크롭손실0 / 캐릭터 일관(ref→S1·S2) / headroom
- [x] **S4 반비례 = 감소 쌍곡선 정확**(정비례 직선 대비) — 딸 약점 핵심
- [x] 시대정확(17C 천문) / no-text / 시소·궤도 모티프
