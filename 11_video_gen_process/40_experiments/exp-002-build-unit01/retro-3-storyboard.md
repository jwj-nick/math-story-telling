<!-- retro-3-storyboard.md / exp-002 STEP 3 retrospective -->

# exp-002 STEP 3 — `se-video-storyboard` v0.1 retrospective

> **스킬**: se-video-storyboard v0.1
> **시범 결과물**: [`3-storyboard.md`](./3-storyboard.md) (6 장면 정밀 카드 + reference 2종 + 부록 4)
> **시범 일자**: 2026-05-25
> **시범 호출자**: NCC 직접
> **본 retrospective 의 결과물**: SKILL.md v0.2 정련 시드 5항목

---

## 1. 본 시범 패턴 — STEP 1·2 frame 단축 적용 *3회 연속 성공*

STEP 2 의 단축 frame (frontmatter 5라운드 → 1 통검토 → 즉시 시범 → reverse-engineering → retro) 을 STEP 3 에 그대로 적용. 정상 작동.

→ **패턴 안정화 확인**. STEP 4~8 도 동일 frame 권장.

## 2. SKILL.md v0.2 정련 항목

| # | 항목 | 정련안 |
|---|---|---|
| 1 | 캐릭터 일관성 reference 양식 | description vs 이미지 — 단원별 가이드. 본 시범 = description 만. STEP 5 이미지 생성 후 시각 일관성 검증 결과로 정련 |
| 2 | 카메라 워크 종류 표준화 | 본 시범 = 6종 (static / push in / pan / zoom / swipe / fade). 표준 4~5종 vs 무제한 결정 — 일관성 vs 다양성 trade-off |
| 3 | 자막 폰트·color | 본 시범 = gold serif 화면 중앙. A7 시리즈 정체 확정 시 표준화 |
| 4 | SVG 가능 장면 vs AI 이미지 결정 가이드 | S3 격자 = SVG 가능. 어떤 장면이 SVG, 어떤 게 이미지인지 패턴 명문화 (비용 절감 + 정확성) |
| 5 | 음향 단서 양식 정밀화 | 본 시범 = 잠정 (배경음 + 효과음). STEP 8 합성 입력으로 충분한지 검증 |

## 3. 본 시범의 한계

- **NCC 직접 동작** — 외부 호출 패턴 검증 X
- **캐릭터 reference = description 만** — STEP 5 이미지 생성 시 시각 일관성 실증 필요
- **음향 = 잠정 명시만** — 본 단계 적절 (정밀은 STEP 8)
- **자막 자수 ±10% 검증 미수행** — SB5 글자수 검증 형식적

## 4. 자산

- ✅ `se-video-storyboard` SKILL.md v0.1 (frontmatter + body)
- ✅ `3-storyboard.md` 1편 (6 장면 카드 + reference 2종 + 부록 4)
- ✅ 캐릭터 일관성 reference 양식 (description 기반) 검증
- ✅ STEP 1·2·3 frame *3회 연속 안정 적용* — 패턴 안정화
- ✅ 부록 A·B·C 가 STEP 4·5·6 직접 입력으로 사용 가능 — chain efficiency

## 5. 다음 작업

- ➡️ STEP 4 [영상 2] 나레이션 진입 — `se-video-narration` (prefix NR)
- **STEP 4 특이점**: *외부 도구 호출 필요* (TTS 엔진) — NCC 직접 시범 실행 가능 여부 결정
- CHECKLIST §0 대시보드 STEP 3 ✅ 갱신 완료
