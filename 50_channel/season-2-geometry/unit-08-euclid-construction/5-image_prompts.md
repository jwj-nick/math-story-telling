<!-- 50_channel/season-2-geometry/unit-08-euclid-construction/5-image_prompts.md / STEP 5 / se-video-image -->

# 단원 8 이미지 프롬프트 — 유클리드(작도) / Nano Banana 네이티브 16:9

> **스킬**: se-video-image v0.2 / **도구**: Nano Banana(Tier1), `gen_images.py` / **출력**: `5-images/` 7장(1344×768) / **실행**: 2026-05-31

## 0. STYLE
- 유클리드(S1~S4·S6): era-ancient(테라코타·황토·세이지 #8FAE7B), 히마티온·나무 컴퍼스·눈금없는 자.
- 가우스(S5): era-modern(슬레이트 #3E5A6E·촛불), 18세기말 독일 청년.
- 네이티브 16:9 + headroom + no-text.

## 1. CHAR
- `ref-euclid2`: 유클리드(흰 수염·히마티온·컴퍼스·자) → S1·(S2·S4 추상은 인물 less)
- 가우스: 19세 청년(S5 단독)

## 2. 장면별 (전체=gen_images.py)
| ID | 주체 |
|---|---|
| ref-euclid2 | 유클리드 컴퍼스·자 상반신+headroom |
| S1 | 유클리드+눈금없는 자·컴퍼스+도형 양피지 |
| S2 | 수직이등분·각이등분 작도(호, 추상) |
| S3 | 합동 삼각형 두 개(포개짐, 추상) |
| S4 | 같은 도형 여러 개 정확히 겹침(추상) |
| S5 | 열아홉 살 가우스 + 정17각형 작도(촛불 책상) |
| S6 | 컴퍼스+정17각형 빛나는 마무리(추상) |

7장 16:9 · no-text. 합동기호·정17각형·한글 = drawtext. 인물 headroom.

## 3. 검증
- [x] 7장 16:9(1344×768) / 캐릭터 일관 / headroom
- [x] S5 가우스 청년+컴퍼스 / S3 합동 삼각형 / no-text
- [x] 길이 145.94s (R24 ≤180 달성)
