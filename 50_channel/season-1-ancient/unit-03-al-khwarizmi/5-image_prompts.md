<!-- 50_channel/season-1-ancient/unit-03-al-khwarizmi/5-image_prompts.md / STEP 5 [이미지] / se-video-image -->

# 단원 3 이미지 프롬프트 — 알콰리즈미 / Nano Banana 네이티브 16:9

> **스킬**: se-video-image v0.2 (unit-02 학습 R8 적용 — `aspect_ratio="16:9"` + headroom)
> **입력**: 3-storyboard.md 부록 B (7장) + §0.1 캐릭터 + §0.2 이슬람 황금기 팔레트
> **도구**: Nano Banana(gemini-2.5-flash-image, Tier1). 실행 스크립트=`gen_images.py`
> **출력**: `5-images/` (7장, 전부 1344×768 네이티브 16:9, no-text)
> **실행**: 2026-05-30

---

## 0. 공통 STYLE (이슬람 황금기)
```
9th-century Baghdad, Islamic Golden Age, House of Wisdom, warm golden lamplight,
palette of turquoise-teal/gold/sandstone/deep-blue/terracotta, Islamic geometric
tile patterns and horseshoe arches, 16:9, NO text/letters/numerals/modern objects,
caption space, 시대정확(터번·로브·청동 천칭·양피지·아스트롤라베)
```
- ⭐ **네이티브 16:9**: API `image_config.aspect_ratio="16:9"` 강제 (정사각 반환·크롭 손실 방지)
- ⭐ **인물 클로즈업 headroom**: "ENTIRE head/face visible with headroom above — do NOT crop top"

## 1. CHAR_ALKHWARIZMI (ref→S2·S5)
```
Al-Khwarizmi: 50대 페르시아 학자, 갈색 피부, 단정한 검은 수염, 흰 터번 + 청록/사암 로브,
양피지 두루마리, 차분하고 지적인 표정, 따뜻한 등불.
```
→ ref 1장 우선 생성 → S2·S5에 ref_paths로 전달(일관성).

## 2. 장면별 (요약 — 전체 프롬프트는 gen_images.py)
| ID | 주체 | reference |
|---|---|---|
| ref-alkhwarizmi | 인물 정면 + headroom | 기준 |
| S1 | 지혜의 집(돔·아치·타일·책·천구의 + 동방 책 유입) | — |
| S2 | 알콰리즈미 + 청동 저울 + 양피지(headroom) | ref |
| S3 | 청동 천칭 저울, 양접시 수평(균형) | — |
| S4 | 0~9 동→서 지도 전파(숫자 렌더 X, 빛 흐름) | — |
| S5 | 긴 문단 양피지 ↔ 빈 면 split(글자=발명품) | ref(좌) |
| S6 | 이어달리기 실루엣 3 + 빛나는 천칭(균형) | — |

## 3. 검증 (NCC 멀티모달)
- [x] 7장 네이티브 16:9 (1344×768) — 크롭 무손실
- [x] 캐릭터 일관성 (ref→S2·S5 동일 인물)
- [x] headroom (인물 머리 온전)
- [x] 시대 정확(이슬람 황금기, anachronism 0)
- [x] no-text (수식·숫자·한글 = drawtext)
- [x] 저울 모티프 일관(S2·S3·S6)
