<!-- 0525_step2_skill_draft.md -->

# exp-002 / STEP 2 / Issue — `se-video-story` SKILL.md draft + 통검토

> **issue**: STEP 1 learning 적용 — frontmatter 통째 draft + Nick 통검토 1회 → 즉시 시범 실행.
> **step**: STEP 2 (CHECKLIST.md §2)
> **선행**: STEP 1 종료 ([`retro-1-narrative.md`](../40_experiments/exp-002-build-unit01/retro-1-narrative.md))
> **frame**: reverse-engineering 패턴 (frontmatter 통째 + body 시범 후)
> **선행 양식**: [`../70_tools/se-people-narrate/SKILL.md`](../70_tools/se-people-narrate/SKILL.md)
> **시작**: 2026-05-25

---

## Draft — `se-video-story` frontmatter (NCC 작성)

`se-people-narrate` 양식 모방 + STEP 2 [스토리] 특화.

```yaml
---
name: se-video-story
description: 영상 제작 시스템의 단계 [스토리] 스킬. 단계 [서사] 결과인 인물 서사 (원료 분량, ~1500~2000자) 을 받아 영상 1편 분량의 스토리 시드 (장면 단위) 로 압축한다. 입력 (서사 원료 / 정체성 = 시청자·약속 3겹·톤 / A3 영상 길이 / A4 장면 수 / 한 단어 압축 / (옵션) 옛 1편 baseline 참조) 을 받아 동작 (입력 align → Q&A 보강 → 서사 §→장면 매핑 → 장면 카드 초안 → 약속 3겹 장면 배치 검증 → 자체 평가 → 출력) 진행. math-story-telling 의 인물 서사 → 영상 스토리 시드 변환, 6장면 약속 운반 배치, A3·A4·A6 (시청 후 행동) 결정 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료 (`40_experiments/exp-NNN/1-narrative.md`, INTEGRATED_PLAN §5.1.2·§8, `50_channel/season-1-ancient/unit-NN/` baseline 참조) 를 참조만 함.
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 스토리 (S1~S7)
  ssot: 11_video_gen_process/70_tools/se-video-story/SKILL.md
  version: "0.1"
  status: 시드 (시범 실행 후 retrospective 로 정련 예정)
allowed-tools: Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch
---
```

---

## 잠정 입력 (5 필수 + 1 옵션)

| # | 입력 | 형식 | 예시 (단원 1) |
|---|---|---|---|
| 1 | 서사 원료 | `1-narrative.md` path | `40_experiments/exp-002-build-unit01/1-narrative.md` |
| 2 | 정체성 | 시청자 + 약속 3겹 + 톤 (A5) | 결정 1·2 + A5 잠정 |
| 3 | A3 영상 길이 | 초 + 글자수 | 110초 / ~550자 (잠정) |
| 4 | A4 장면 수 | 정수 | 6 (잠정) |
| 5 | 한 단어 압축 | 인물 한 단어 | "정리" |
| 6 (옵션) | 옛 1편 baseline | 경로 | `50_channel/season-1-ancient/unit-01/storyboard_v1_5.md` |

---

## NCC 추천 결정 (STEP 1 양식 통일)

| 항목 | 결정 | 비고 |
|---|---|---|
| name | `se-video-story` | kebab-case |
| stage prefix | **S** (Story) | STEP 3+ 스킬 (storyboard 등) prefix 충돌은 *STEP 3 진입 시* 정리 (예: storyboard = SB) |
| 동작 수 잠정 | 7 (S1~S7) | reverse-engineering 후 변동 가능 |
| 입력 수 | 5 필수 + 1 옵션 | se-people-narrate 6 과 비슷 |
| 양식 통일 | ✅ se-people-narrate 와 동일 패턴 | |

---

## Nick 통검토 요청

위 frontmatter + 입력 + stage prefix 결정 — **모두 OK** 인가?

OK 받으면 즉시 다음 작업 진행:
1. `70_tools/se-video-story/` 디렉토리 신설 + SKILL.md (frontmatter + body placeholder)
2. **시범 실행** = `1-narrative.md` → `2-story-seed.md` draft 생성
3. body reverse-engineering (시범 동작 정형화)
4. NCC 자동 검증 + Nick 통검토 ("all ok" 패턴 가능)
5. `retro-2-story.md` 작성
6. CHECKLIST 대시보드 STEP 2 ✅
7. STEP 3 진입

## Nick 답변

**모두 OK — 즉시 시범 실행** (옵션 1 채택).

## 결정

frontmatter 확정 (위 draft 그대로) + 입력 5+1 + stage `스토리 (S1~S7)`.

---

# 시범 실행 (2026-05-25)

## 작업

1. ✅ `70_tools/se-video-story/` 디렉토리 신설 + SKILL.md (frontmatter + body placeholder)
2. ✅ 시범 실행 = `1-narrative.md` (~1900자) → `2-story-seed.md` (110초 6장면) draft 생성
3. ➡️ body reverse-engineering (다음 turn 에서 Nick "all ok" 후 진행)

## 시범 결과물

[`../40_experiments/exp-002-build-unit01/2-story-seed.md`](../40_experiments/exp-002-build-unit01/2-story-seed.md)

핵심 구조:
- S1~S6 = 6 장면 (15·15·25·20·20·15s = 110s)
- 각 장면 = 시각 단서 / 나레이션 시드 / 운반 약속 / 전환
- 부록 A — 약속 3겹 장면 배치 검증
- 부록 B — 나레이션 글자수 합계 (550자 = 정확히 기준 부합)
- 부록 C — 다음 단계 스토리보드 입력 명세
- 부록 D — 본 시범의 한계 + retrospective 시드 9건

## NCC 자체 평가 (Nick 검토 필요 핵심 3 항목)

| # | 항목 | NCC 발견 |
|---|---|---|
| 1 | 약속 2 (인물 정서) S2 1 장면만 운반 | 보강 필요? 또는 영상 본질이 *시대+발견* 중심이라 정서 1 장면 적정? |
| 2 | §3 NCC 해석 (도서관→수 분류) S3 에 그대로 반영 | STEP 1 미해결, S3 핵심 → 학설 확인 / 그대로 / 다른 동기 서사? |
| 3 | §5 노년 시력 상실 (전승) 영상 *생략* | 어두움 + 후세 전승 회피. 정서 약화의 한 원인. |

(Nick 검토 답 ↓ — "all ok" 또는 항목별 수정 지시)
