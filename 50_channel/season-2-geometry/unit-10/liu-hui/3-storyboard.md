<!-- 50_channel/season-2-geometry/unit-10/liu-hui/3-storyboard.md / STEP 3 [스토리보드] / se-video-storyboard -->

# unit-10 류후이 — 스토리보드

> 6장면 정밀 카드. 이미지(5-images) + 자막(6-motion-config) 명세의 근거.
> ★ 류후이 = **신규 캐릭터**. gen_images.py S1 에서 `ref-liuhui.png` 먼저 생성 → S1/S6 에 reference 전달(얼굴 일관성). era-ancient(중국, 죽간·#A04D4D).

| S | turns | 모션 | 이미지 (5-images) | 자막 (color·위치) |
|---|---|---|---|---|
| S1 | 1–4 | push_in | S1.png 등잔불 아래 죽간 펼치고 글 쓰는 류후이(서재) | "옛 책에 주석을 달던 사람, 류후이" (gold, 하단) |
| S2 | 5–8 | ken_burns | S2.png 원 다이어그램(중심·반지름·굽은 둘레 강조) | "굽은 둘레를 어떻게 잴까" (white, 상단) / "곧은 자로는 잴 수 없다" (gold, 중앙) |
| S3 | 9–16 | ken_burns | S3.png 원 안 다각형이 6→많은 변으로 잘게 쪼개져 원에 합쳐짐(할원술) | "할원술 · 끊임없이 더 잘게"(white 상단) / "삼천칠십이 각형 → 원과 하나"(gold 중앙) |
| S4 | 17–22 | ken_burns | S4.png 다각형이 원과 거의 합쳐진 다이어그램 + 둘레/넓이 느낌 | "원주율 = 삼점일사일오구" (gold, 하단) |
| S5 | 23–28 | ken_burns | S5.png 또 다른 중국 학자(조충지) 죽간에 더 미세한 원 분할 | "더 잘게 자른 사람들 · 조충지" (white, 하단) |
| S6 | 29–32 | zoom_in | S6.png 황혼 서재, 죽간 위 손 멈춘 류후이(주석가) — 우측 여백 | "주석가의 자리 — 왜?를 멈추지 않다"(white 하단) / "더 잘게"(대형 gold) |

## 부록 — 캡션 타이밍 원칙
- 각 scene end = 다음 scene 첫 turn 음성 시작(synth 실측). 자막은 해당 개념을 말한 직후 등장, scene end 직전까지.
- 한 단어 "더 잘게" 는 S6 우측 여백에 대형 표시(이미지 구도가 우측을 비움). era-ancient(중국) 톤 #A04D4D 계열은 STYLE_CN 프롬프트로 운반.
- S2~S4 는 사람 없는 GEOMETRY DIAGRAM(아르키메데스 템플릿 패턴 재사용), S1/S5/S6 은 인물 장면.
