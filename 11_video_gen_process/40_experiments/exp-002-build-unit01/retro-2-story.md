<!-- retro-2-story.md / exp-002 STEP 2 retrospective -->

# exp-002 STEP 2 — `se-video-story` v0.1 retrospective

> **스킬**: se-video-story v0.1
> **시범 결과물**: [`2-story-seed.md`](./2-story-seed.md) (110초 6장면 + 부록 4)
> **시범 일자**: 2026-05-25
> **시범 호출자**: NCC 직접 (외부 호출자 X — STEP 1 패턴 동일)
> **본 retrospective 의 결과물**: SKILL.md v0.2 정련 시드 (4항목) + STEP 3 진입 시 정리 항목 (1건)

---

## 1. 본 시범 패턴 — STEP 1 frame 적용 검증

STEP 1 의 learning = "추상 설계 X / 즉시 시범 실행 → reverse-engineering → retrospective" 패턴을 STEP 2 에 **단축 적용**:

| 단계 | STEP 1 | STEP 2 (단축) |
|---|---|---|
| frontmatter | 5 라운드 Q&A | 1 라운드 통검토 ✅ |
| 시범 실행 | Nick redirect 후 진행 | 통검토 통과 즉시 진행 ✅ |
| body reverse-engineering | 시범 후 정형화 | 동일 ✅ |
| 검증 | NCC 자동 + Nick 통검토 | Nick "all ok" ✅ |
| retrospective | 정련 5항목 | 정련 4항목 + STEP 3 진입 시 정리 1건 |

→ **STEP 1 frame 정상 작동 확인**. STEP 3~8 도 동일 frame 적용 권장.

## 2. SKILL.md v0.2 정련 항목 (예정)

본 시범에서 발견된 정련 시드 (2-story-seed.md 부록 D 에서 정리):

| # | 항목 | 정련안 |
|---|---|---|
| 1 | 출력 양식 장면 카드 sub-section 수 | 본 시범 = 4~5 요소 (시각 / 나레이션 / 약속 / 전환 / [선택] 자막). 정식 4 또는 5 중 결정. |
| 2 | 약속 2 (인물 정서) 최소 운반 장면 수 | 본 시범 = S2 1 장면만. Nick "all ok" 통과 — 1 장면도 적정 (영상 본질이 *시대+발견* 중심). 다음 단원 시범 후 확정. |
| 3 | 옛 baseline 참조 옵션의 효과 측정 | 본 시범에서는 *미참조* (외부 의존 0 frame). 다음 단원에서 baseline 참조 vs 미참조 비교 시범 필요. |
| 4 | S3 통합·분할 규칙 정밀화 | 본 시범 = §6+§7 → S6 통합 (§6 후반 + §7 한 단어 압축). 단원별로 §-S 매핑 패턴 다양 — 규칙 명문화 필요. |

## 3. STEP 3 진입 시 정리 항목 (1건)

**stage prefix 충돌**:
- 현재: pick=P / narrate=N / story=**S**
- STEP 3 = `se-video-storyboard` — storyboard 도 S 시작 → 충돌
- STEP 4 = `se-video-narration` — narration 도 N 시작 (narrate 와 충돌)
- STEP 5~8 = image/motion/render/compose — I/M/R/C (현재 충돌 X)
- STEP 3 진입 시 prefix 규칙 명문화 필요 (예: storyboard=B, narration=R 등)

## 4. 본 시범의 한계

- **NCC 직접 동작** — 외부 호출 패턴 검증 X (STEP 1 동일). 다음 단원 (exp-003) 에서 실증.
- **§3 "도서관→수 분류" NCC 해석** — STEP 1 에서 미해결, S3 에 그대로 반영 + Nick "all ok" 통과. 학설 확인 미수행. *영상 완성 후 시청자 반응 보고 retrospective 정밀화*.
- **§5 노년 시력 상실 영상 *생략*** — Nick 통과. 약속 2 (정서) 약화의 한 원인이나 *어두움 회피* 가 우선. 단원별 단원 패턴 (생략 / 추상화 / 명시) 가이드 필요 — 다음 인물 (브라마굽타 등) 시범 후.
- **약속 2 (정서) S2 1 장면만 운반** — 본 시범 통과. 그러나 *영상 본질* 정의 (시대+발견 중심 vs 인물 정서 동등 중심) 가 다음 인물에서 다를 수 있음. 정체성 §5.1.2 보강 검토.

## 5. 자산 (본 시범으로 얻은 것)

- ✅ `se-video-story` SKILL.md v0.1 (frontmatter + body)
- ✅ `2-story-seed.md` 1편 (단원 1 / 110초 6장면)
- ✅ STEP 1 frame 단축 적용 검증 (frontmatter 5 라운드 → 1 통검토)
- ✅ 본 retrospective (v0.2 정련 4항목 + STEP 3 진입 시 정리 1건)
- ✅ session log 양식 검증 (`0525_step2_skill_draft.md` 단일 파일, STEP 1 의 frontmatter+body 2 파일 → 1 파일 통합)

## 6. 다음 작업

- ➡️ STEP 3 [영상 1] 스토리보드 진입 — `se-video-storyboard` SKILL.md + `3-storyboard.md`
- **선행**: stage prefix 규칙 결정 (storyboard / narration / image / motion / render / compose 의 prefix 일관 패턴)
- STEP 1 frame 단축 적용 (frontmatter 통검토 + 즉시 시범)
- CHECKLIST.md §0 대시보드 STEP 2 ✅ 갱신 완료
