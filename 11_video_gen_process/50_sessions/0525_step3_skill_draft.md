<!-- 0525_step3_skill_draft.md -->

# exp-002 / STEP 3 / Issue — `se-video-storyboard` SKILL.md draft + 통검토

> **issue**: STEP 1 frame 단축 적용 (STEP 2 패턴 동일) — frontmatter 통째 draft + Nick 통검토 1회 → 즉시 시범 실행.
> **step**: STEP 3 (CHECKLIST.md §3)
> **선행**: STEP 2 종료 ([`retro-2-story.md`](../40_experiments/exp-002-build-unit01/retro-2-story.md))
> **선행 양식**: [`../70_tools/se-video-story/SKILL.md`](../70_tools/se-video-story/SKILL.md)
> **시작**: 2026-05-25

---

## 사전 결정 — stage prefix 규칙 (Nick 합의: 옵션 A)

| 스킬 | prefix | 이유 |
|---|---|---|
| pick | P | 첫 글자 (충돌 X) |
| narrate | N | 첫 글자 (충돌 X) |
| story | S | 첫 글자 (충돌 X) |
| **storyboard** | **SB** | story 와 충돌 → 2글자 |
| **narration** | **NR** | narrate 와 충돌 → 2글자 |
| image | I | 첫 글자 (충돌 X) |
| motion | M | 첫 글자 (충돌 X) |
| render | R | 첫 글자 (충돌 X) |
| compose | C | 첫 글자 (충돌 X) |

---

## Draft — `se-video-storyboard` frontmatter (NCC 작성)

```yaml
---
name: se-video-storyboard
description: 영상 제작 시스템의 단계 [영상 1] 스토리보드 스킬. 단계 [스토리] 결과인 스토리 시드 (장면 단위) 를 받아 각 장면별 정밀 카드 (시각 단서 + 텍스트 + 나레이션 시드 + 카메라 워크 + 자막 + 음향) 를 작성한다. 입력 (스토리 시드 / 정체성 = 시청자·약속 3겹·톤 / (옵션) 캐릭터 일관성 reference / (옵션) 옛 1편 baseline / (옵션) 시대 풍경 reference) 을 받아 동작 (입력 align → Q&A 보강 → 장면 카드 정밀화 → 캐릭터 일관성 / 카메라 워크 / 자막 / 음향 결정 → 검증 → 자체 평가 → 출력) 진행. math-story-telling 의 영상 스토리보드 작성, 다음 단계 [영상 2~6] (나레이션·이미지·모션·렌더·합성) 의 직접 입력 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료 (`40_experiments/exp-NNN/2-story-seed.md`, INTEGRATED_PLAN §5.1.2·§8, `50_channel/season-1-ancient/unit-NN/storyboard_v1_5.md` baseline) 를 참조만 함.
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 영상 1 스토리보드 (SB1~SB7)
  ssot: 11_video_gen_process/70_tools/se-video-storyboard/SKILL.md
  version: "0.1"
  status: 시드 (시범 실행 후 retrospective 로 정련 예정)
allowed-tools: Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch
---
```

---

## 잠정 입력 (2 필수 + 3 옵션)

| # | 입력 | 형식 | 예시 (단원 1) |
|---|---|---|---|
| 1 | 스토리 시드 | `2-story-seed.md` path/내용 (필수) | `40_experiments/exp-002-build-unit01/2-story-seed.md` |
| 2 | 정체성 | 시청자 + 약속 + 톤 (필수) | INTEGRATED_PLAN §8 + A5 |
| 3 (옵션) | 캐릭터 일관성 reference | 인물 시각 reference (이미지 또는 description) | 본 시범에서는 description (40~50대 학자 풍모 등) |
| 4 (옵션) | 옛 1편 baseline | 경로 | `50_channel/season-1-ancient/unit-01/storyboard_v1_5.md` |
| 5 (옵션) | 시대 풍경 reference | URL 또는 description | era-ancient 팔레트, Wikipedia 알렉산드리아 |

---

## NCC 추천 결정

| 항목 | 결정 |
|---|---|
| name | `se-video-storyboard` |
| stage | `영상 1 스토리보드 (SB1~SB7)` |
| 동작 수 잠정 | 7 (reverse-engineering 후 변동 가능) |
| 입력 수 | 2 필수 + 3 옵션 |
| 양식 통일 | ✅ `se-video-story` 와 동일 패턴 |
| prefix | SB (Nick 합의 옵션 A) |

---

## Nick 통검토 요청

위 frontmatter + 입력 + stage prefix SB — **모두 OK** 인가?

OK 받으면 즉시 진행:
1. `70_tools/se-video-storyboard/` 디렉토리 신설 + SKILL.md (frontmatter + body placeholder)
2. 시범 실행 = `2-story-seed.md` → `3-storyboard.md` draft 생성
3. body reverse-engineering
4. 검증 + retro + STEP 4 진입

## Nick 답변

**모두 OK — 즉시 시범 실행** (옵션 1).

## 결정

frontmatter 확정 (위 draft 그대로) + 입력 2+3 + stage `영상 1 스토리보드 (SB1~SB7)`.

---

# 시범 실행 (2026-05-25)

## 작업

1. ✅ `70_tools/se-video-storyboard/` + SKILL.md (frontmatter + body placeholder)
2. ✅ 시범 실행 = `2-story-seed.md` → `3-storyboard.md` draft 생성
3. ➡️ body reverse-engineering (Nick "all ok" 후 진행)

## 시범 결과물

[`../40_experiments/exp-002-build-unit01/3-storyboard.md`](../40_experiments/exp-002-build-unit01/3-storyboard.md)

핵심 구조:
- §0 장면 카드 요약 표 + §0.1 캐릭터 일관성 reference + §0.2 시대 풍경 reference
- S1~S6 = 6장 정밀 카드 (시각 / 카메라 / 자막 / 나레이션 / 음향 / 전환)
- 부록 A — 다음 [영상 2] 나레이션 입력 명세 (SSML 권장 포함)
- 부록 B — 다음 [영상 3] 이미지 입력 명세 (7~8장)
- 부록 C — 다음 [영상 4] 모션 입력 명세
- 부록 D — 한계 + retrospective 시드 9건

## NCC 자체 평가 (Nick 검토 필요 핵심 3 항목)

| # | 항목 | NCC 발견 |
|---|---|---|
| 1 | 캐릭터 일관성 reference = description 만 | 다음 단계 [영상 3] 에서 reference 이미지 생성 시 시각 일관성 검증 필요 |
| 2 | S3 격자 = SVG 가능 (이미지 생성 X) | 비용 절감 + 정확성. 다음 단계 [영상 3] 결정 항목 |
| 3 | 자막 폰트·color (gold serif 화면 중앙) | A7 시리즈 정체 결정 시 표준화 |

(Nick 검토 답 ↓ — "all ok" 또는 항목별 수정)
