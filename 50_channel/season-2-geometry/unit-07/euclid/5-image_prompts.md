<!-- 50_channel/season-2-geometry/unit-07-euclid/5-image_prompts.md / STEP 5 / se-video-image -->

# 단원 7 이미지 프롬프트 — 유클리드 / Nano Banana 네이티브 16:9

> **스킬**: se-video-image v0.2 / **도구**: Nano Banana(Tier1), `gen_images.py` / **출력**: `5-images/` 7장(1344×768) / **실행**: 2026-05-30

## 0. STYLE (고대 그리스/알렉산드리아, era-ancient)
```
ancient Greece / Hellenistic Alexandria, golden hour, palette terracotta/ochre/bronze/
sage-green, weathered marble + papyrus, 16:9, NO text/letters/numerals/modern, caption
space, 시대정확(히마티온·파피루스·나무 컴퍼스·자·알렉산드리아 도서관)
```
- 네이티브 16:9 + 인물 headroom

## 1. CHAR_EUCLID (ref→S1·S5)
```
유클리드: 고대 그리스 학자 50대 후반, 흰 수염, 흰 히마티온, 나무 컴퍼스+두루마리, 차분·단정, 황금빛.
```

## 2. 장면별 (전체=gen_images.py)
| ID | 주체 | ref | 비고 |
|---|---|---|---|
| ref-euclid | 인물 정면+headroom | 기준 | |
| S1 | 알렉산드리아 도서관+원론+컴퍼스+유클리드 | ref | |
| S2 | 이집트 피라미드+탈레스+막대기 그림자(닮은꼴) | — | |
| **S3** | **점→선→면 생성(좌 점·중 선·우 면)** | — | ⭐ **재생성**(첫 생성 손 아티팩트→깔끔 점선면) |
| S4 | 5약속 블록 위 정리 탑 | — | |
| S5 | 프톨레마이오스 왕 + 유클리드(왕도 거부) | ref | |
| S6 | 점→데카르트 좌표격자+컴퍼스·자(추상) | — | |

7장 네이티브 16:9 · no-text. 정의·수식·한글 = drawtext. 인물 headroom.

## 3. 검증
- [x] 7장 16:9(1344×768) 크롭손실0 / 캐릭터 일관(ref→S1·S5) / headroom
- [x] **S3 점→선→면 명확**(첫 생성 모호→재생성) / 시대정확(고대 그리스) / no-text
