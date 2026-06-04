<!-- 50_channel/season-2-geometry/unit-09/kepler/5-image_prompts.md / STEP 5 / se-video-image -->

# 단원 9 케플러(테셀레이션) 이미지 프롬프트 — Nano Banana 네이티브 16:9

> **스킬**: se-video-image / **도구**: Nano Banana(gemini-2.5-flash-image, Tier1), `gen_images.py` / **출력**: `5-images/` 6장 / **실행**: 2026-06-04
> ★ **캐릭터 재사용**: S1·S6 = u06 `ref-kepler.png` 를 reference 로 전달 → 동일 얼굴/복장 일관성. 신규 ref 생성 안 함.

## 0. STYLE (17C era-modern)
```
early 17th-century astronomer's candle-lit study/observatory at night, deep starry
night-blue, palette night-blue/brass/candle-gold/brown, armillary sphere, 16:9,
NO text/letters/numerals/modern objects, ample caption space, historically accurate
(ruff collar, dark gown, brass instruments). 인물 headroom.
```

## 1. CHAR_KEPLER (ref 전달 대상)
```
요하네스 케플러: 17세기 독일 천문학자 40대, 짧은 곱슬 갈색머리+수염, 흰 러프 칼라+짙은 가운, 따뜻한 표정.
= season-1 unit-06 ref-kepler.png 와 동일 인물 (얼굴/복장 유지).
```

## 2. 장면별 (전체 = gen_images.py)
| ID | 주체 | ref | 비고 |
|---|---|---|---|
| S1 | 케플러+황동 천체모형+별밤, 책상 위 정다각형 타일 스케치 | **ref-kepler** | 인물 일관 |
| S2 | 정육각형(벌집류) 빈틈없는 타일 평면(추상) | — | 따뜻한 황동빛 |
| S3 | 한 점에 모인 각 wedge → 완전한 원 360°(추상) | — | 한 꼭짓점=한 바퀴 |
| S4 | 정삼각형6·정사각형4·정육각형3 각각 한 점 채움(추상 3구획) | — | 60·90·120 시각 필연 |
| S5 | 정오각형들이 한 점에 모이려다 빈틈/겹침 어긋남(추상) | — | "안 되는 이유" |
| S6 | 케플러+위 별궤도/아래 쪽맞춤 바닥 = 같은 기하 | **ref-kepler** | 인물 일관, 피날레 |

6장 네이티브 16:9 · no-text. 360도·숫자·한글 = drawtext. 인물 headroom.

## 3. 검증
- [ ] 6장 16:9 / S1·S6 케플러 얼굴 = ref-kepler 일관 / headroom
- [ ] 정육각형 쪽맞춤(S2)·360°원(S3)·3종 채움(S4)·정오각형 어긋남(S5) 개념 정확
- [ ] 시대정확(17C 천문, 러프칼라·황동) / no-text
