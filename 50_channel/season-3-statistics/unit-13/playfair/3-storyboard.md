<!-- 50_channel/season-3-statistics/unit-13/playfair/3-storyboard.md / STEP 3 [스토리보드] / se-video-storyboard -->

# unit-13 플레이페어 — 스토리보드

| S | turns | 모션 | 이미지 (5-images) | 자막 (color·위치) |
|---|---|---|---|---|
| S1 | 1–4 | push_in | S1.png 18C 책상·끝없는 숫자 표 더미·플레이페어 | "아무도 표를 안 봤다" (gold, 하단) |
| S2 | 5–8 | ken_burns | S2.png 막대그래프(18C engraving, 길이로 비교) | "숫자를 길이로"(상단) / "막대그래프"(gold 하단) |
| S3 | 9–12 | ken_burns | S3.png 꺾은선그래프(시간축·오르내림 추세) | "시간을 선으로"(상단) / "꺾은선그래프"(gold 하단) |
| S4 | 13–18 | ken_burns | S4.png 원그래프(색 조각·비율) | "전체를 조각으로 · 상대도수"(상단) / "정치인도 그림은 본다"(gold 하단) |
| S5 | 19–22 | ken_burns | S5.png 막대·선·원 3종 한 화면(18C plate) | "막대 · 선 · 원 — 한 사람의 발명"(gold 하단) |
| S6 | 23–26 | zoom_in | S6.png 차트 계보 montage(좌측, 우측 어두움) | "표를 안 본다면, 보이게 만들자"(우측) / "그림"(대형 gold 우측) |

## 캐릭터
- **신규 캐릭터** William Playfair: 18~19C 스코틀랜드 엔지니어. 30~40대 남성, 짧은 단발/묶은 머리(조지언 시대), 진한 코트·크라바트(목수건), 깃펜·잉크·제도(製圖) 도구. **gen_images.py S1에서 ref-playfair.png 먼저 생성 → S1 장면·후속 인물 장면에 reference 전달** (일관성). 나이팅게일과 완전히 다른 인물·시대·복장.
- era-modern 팔레트: signature-color #8E7E3C (올리브-카키 골드). gold 자막 = 동일 0xD9A441 유지(가독성), 이미지 톤만 era-modern.

## 캡션 타이밍 원칙
- scene end = 다음 scene 첫 turn 음성 시작(synth 실측 매핑).
- "·" 중점 안전. S6 한 단어 "그림"은 우측 어두운 영역(x≈0.62) 대형.
- S2~S4 = 발명 3박자: 막대=길이 / 선=시간흐름 / 원=비율. 시즌3 시그니처 비주얼(차트 자체).
- S4 원그래프 색 조각 = 상대도수 시각화 강조. S5 = 3종 그래프 한 화면(발명 총합).
