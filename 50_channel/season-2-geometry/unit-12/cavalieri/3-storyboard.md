<!-- 50_channel/season-2-geometry/unit-12/cavalieri/3-storyboard.md / STEP 3 [스토리보드] / se-video-storyboard -->

# unit-12 카발리에리 — 스토리보드

| S | turns | 모션 | 이미지 (5-images) | 자막 (color·위치) |
|---|---|---|---|---|
| S1 | 1–5 | push_in | S1.png 수도사 카발리에리가 빵을 똑바로/비스듬히 두 더미로 쌓음 (★ref 생성) | "모양이 달라도 부피는 같다" (gold, 하단) |
| S2 | 6–9 | ken_burns | S2.png 입체가 무수히 얇은 단면(불가분량)으로 분해되는 다이어그램 | "불가분량 — 두께 없는 단면"(상단) / "입체는 단면이 쌓인 것"(gold 하단) |
| S3 | 10–15 | ken_burns | S3.png 모양 다른 두 입체, 같은 높이 단면 넓이 같음 비교 | "카발리에리의 원리 (1635)"(상단) / "단면이 같으면 부피도 같다"(gold 하단) |
| S4 | 16–20 | ken_burns | S4.png 책 「Geometria」 펼친 옆에 카발리에리(★ref 전달) | "스승 갈릴레오의 길을 잇다"(gold 하단) |
| S5 | 21–25 | ken_burns | S5.png 좌(중국 죽간/주판)·우(유럽 양피지) 대칭, 가운데 같은 단면 도형 | "1400년 앞서 — 류후이"(상단) / "동서양이 같은 통찰에"(gold 하단) |
| S6 | 26–30 | zoom_in | S6.png 단면 슬라이스 엠블럼(좌측, 우측 어두움) | "단면 쌓기가 적분이 되다"(우측) / "단면"(대형 gold 우측) |

## 캐릭터 (신규)
- **카발리에리**: 17C 이탈리아 예수회 수도사. 검은/짙은 자주(#6C5B7B 톤) 수도복, 40대, 통풍으로 야윈 손, 사색적 표정. era-modern 팔레트.
- S1 에서 **ref-cavalieri.png** 먼저 생성 → S4 에 reference 로 전달(얼굴 일관성). S2·S3·S5·S6 은 diagram(인물 없음).

## 캡션 타이밍 원칙
- scene end = 다음 scene 첫 turn 음성 시작(synth 실측 매핑 — EXECUTE 시 6-motion-config.json 으로 갱신, 현재 draft 는 rel 0~1).
- "1635"·"1400"·연도/숫자 자막은 아라비아 숫자 그대로(NotoSerifCJKkr 정상, R44). 발화는 한글 음차.
- S6 한 단어 "단면"은 우측 어두운 영역(x≈0.62) 대형(아르키메데스 S6 "쌓기" 패턴 재현).
- era 대비: 아르키메데스=gold/terracotta(고대), 카발리에리=gold + 자주빛(#6C5B7B) 17C 유럽 톤.
