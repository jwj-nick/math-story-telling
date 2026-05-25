<!-- retro-1-narrative.md / exp-002 STEP 1 retrospective -->

# exp-002 STEP 1 — `se-people-narrate` v0.1 retrospective

> **스킬**: se-people-narrate v0.1
> **시범 결과물**: [`1-narrative.md`](./1-narrative.md) (에라토스테네스, 약 1900자)
> **시범 일자**: 2026-05-25
> **시범 호출자**: NCC 직접 (외부 호출자 X — body reverse-engineering 패턴)
> **본 retrospective 의 결과물**: SKILL.md v0.2 정련 시드 (5항목)

---

## 1. 본 시범 패턴 — *reverse-engineering frame 검증*

본 STEP 1 의 핵심 발견 = **추상 설계 X / 즉시 시범 실행 → reverse-engineering 으로 SKILL.md 정형화 → retrospective 정련** 패턴 검증.

흐름:
- frontmatter 5 라운드 Q&A (입력 합의 + 양식 통일) = ✅ 효율
- body 6 라운드 추상 Q&A = ❌ 비효율 (Nick redirect: *"실행결과를 봐야 하는 거 아닌가?"*)
- 시범 실행 → SKILL.md body 정형화 → retrospective = ✅ 본 프로젝트 frame 일치

→ **STEP 2~8 도 동일 frame 적용 권장**.

## 2. SKILL.md v0.2 정련 항목 (예정)

본 시범에서 발견된 정련 시드:

| # | 항목 | 정련안 |
|---|---|---|
| 1 | N4 자산-약속 매핑 표 정형화 | 행=자산 / 열=약속 1/2/3 + 강도 ★ — 정형 표 양식 명문화 |
| 2 | fabrication 4분류 처리 패턴 정밀화 | 사실 = URL 인용 / NCC 해석 = 인라인 *fabrication 주의* 박스 / 후세 전승 = "전승에 따르면" / 기록 없음 = "기록이 없다" |
| 3 | 출력 양식 §N 개수 결정 패턴 | §N = 자산 수 + 클로징 1~2 + 한 단어 압축 § + 부록 A·B·C·D. 명문화 |
| 4 | 길이 기준 (원료 vs 노이즈 경계) | 본 시범 ~1900자 = 영상 길이의 ~3.5배. 적정 기준 = 3~5배. 다음 단원 검증 후 정식 |
| 5 | N2 Q&A 트리거 조건 정밀화 | 본 시범은 NCC 직접 동작이라 Q&A 발동 X. 실제 호출 시 어떤 입력이 어느 수준일 때 Q&A 발동할지 명시 |

## 3. 본 시범의 한계

- **NCC 직접 동작** — 실제 외부 호출 패턴 (다른 NCC 세션이 본 스킬 호출) 검증 X. 다음 단원 (exp-003 = 단원 2) 에서 외부 호출 시범 필요.
- **Nick 통검토 (all ok) 로 통과** — 본 시범의 4 자체 평가 질문 (서사 품질 / §3 NCC 해석 / 출력 양식 / fabrication 표현) 에 대한 *개별 답* 없이 통과. 동일 항목이 STEP 2~ 에서 재등장 가능 — 그 때 정밀 검토.
- **§3 도서관 분류 본능 → 소수의 체 인과** — NCC 해석. 1차 자료 학설 확인 미수행. STEP 2 [스토리] 압축 시 이 인과를 어떻게 다룰지 결정.

## 4. 자산 (본 시범으로 얻은 것)

- ✅ `se-people-narrate` SKILL.md v0.1 (frontmatter + body)
- ✅ `1-narrative.md` 1편 (에라토스테네스, STEP 2 입력으로 사용)
- ✅ **reverse-engineering frame 검증** (STEP 2~8 적용 가능)
- ✅ 본 retrospective (SKILL.md v0.2 정련 시드 5건)
- ✅ Issue 별 session log 패턴 검증 (`0525_step1_skill_frontmatter.md` + `0525_step1_skill_body.md`)

## 5. 다음 작업

- ➡️ STEP 2 [스토리] 진입 — `se-video-story` SKILL.md + `2-story-seed.md`
- reverse-engineering frame 그대로 적용 권장
- CHECKLIST.md §0 대시보드 STEP 1 ✅ 갱신 완료
