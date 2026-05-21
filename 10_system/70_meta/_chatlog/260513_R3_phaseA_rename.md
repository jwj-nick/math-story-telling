<!-- 260513_R3_phaseA_rename.md -->

# Round 3 — Phase A: Skill/Agent prefix rename

> 작성: 2026-05-13 | NCC
> 트리거: Nick "계획 명확, 진행" + Sonnet 전환 가능 (기계적 작업)

## Round 2 회고

R2에서 마스터 플랜 (51_MASTER_PLAN.md) 완성. Phase A~F 정의.
- Phase A = `se_*` / `se_agent_*` prefix 적용 (rename)
- "지금 당장" 할 수 있는 작업으로 명시 (§7)

Nick의 R3 신호: "compact 이후 모든 할 수 있는 작업 진행. Sonnet 전환 OK."

## Phase A 작업 범위

### MathTelling (`C:/Kids/30_MiddleSchool/260426_MathTelling_Idea/.claude/`)

- 12 skills (skills/) — 모두 `se_*` prefix
- 1 agent (agents/unit-orchestrator) → `se_agent_unit_orchestrator`
- 1 command (commands/video-make) → `se_video_make`

### HighSchool 2604 (`C:/Kids/70_HighSchool/2604_고1_중간고사/.claude/`)

- 5 skills — 모두 `se_*` prefix
- 2 agents → `se_agent_*`

### 변경 작업 (각 skill/agent마다)

1. 디렉토리/파일 rename (`mv`)
2. `SKILL.md` frontmatter `name:` 갱신
3. 프로젝트 CLAUDE.md 의 skill 호출 예시 갱신
4. agent .md 안에서 다른 skill 참조하는 부분 갱신 (예: unit-orchestrator 가 호출하는 skill 이름들)

### 의도적 제한
- `science-chem-card` → `se_science_chem_card` (단순 rename). 일반화 (`se_concept_card`)는 Phase G에서 별도.
- `app-reviewer` → `se_agent_app_reviewer` (단순 rename). 비수학 확장 (B07)은 Phase D.

## 실행 순서

1. ✅ Round 3 chatlog (이 파일)
2. ✅ 인벤토리 정밀 점검 (각 .claude/ 내부 확인)
3. ✅ MathTelling rename 실행 → SKILL.md frontmatter 갱신 → CLAUDE.md 갱신 → commit `40ddad5` → push
4. ✅ HighSchool 2604 rename → 동일 → commit `d288935` → push
5. ✅ Round 3 closure (아래)

---

## Round 3 결과 (2026-05-13)

### MathTelling (`jwj-nick/mid_eun` — commit `40ddad5`, pushed)

| 변경 전 | 변경 후 | 비고 |
|---|---|---|
| `skills/ncc-qa-pair` | `se_ncc_qa_pair` | git mv |
| `skills/ncc-unit-story` | `se_ncc_unit_story` | git mv |
| `skills/ncc-worksheet` | `se_ncc_worksheet` | git mv |
| `skills/ncc-audit-app` | `se_ncc_audit_app` | git mv |
| `skills/ncc-audit-content` | `se_ncc_audit_content` | git mv |
| `skills/ncc-story-video` | `se_ncc_story_video` | git mv |
| `skills/ncc-card-game` | `se_ncc_card_game` | git mv |
| `skills/ncc-math-story` | `se_ncc_math_story` | git mv |
| `skills/ncc-quiz-set` | `se_ncc_quiz_set` | git mv |
| `skills/ncc-sim-scene` | `se_ncc_sim_scene` | git mv |
| `skills/ncc-concept-map` | `se_ncc_concept_map` | git mv |
| `skills/ncc-worksheet-gen` | `se_ncc_worksheet_gen` | git mv |
| `skills/unit-review` (untracked) | `se_unit_review` | plain mv → create mode |
| `agents/unit-orchestrator.md` | `se_agent_unit_orchestrator.md` | git mv |
| `commands/video-make.md` | `se_video_make.md` | git mv |
- SKILL.md frontmatter `name:` 전체 갱신 (sed)
- 에이전트 내부 skill 참조 갱신 (sed, word-boundary)
- CLAUDE.md skill 테이블 갱신 (sed) — Nick WIP(4축 구조) 미충돌 확인 후 적용

**특이사항**: MathTelling CLAUDE.md에 Nick WIP 있음. `.claude/` 디렉토리만 스테이징하여 충돌 회피. Nick이 별도 commit 예정.

### HighSchool 2604 (`jwj-nick/high_son` — commit `d288935`, pushed)

| 변경 전 | 변경 후 |
|---|---|
| `skills/figcrop` | `se_figcrop` |
| `skills/math-error-note` | `se_math_error_note` |
| `skills/math-figure` | `se_math_figure` |
| `skills/math-practice` | `se_math_practice` |
| `skills/science-chem-card` | `se_science_chem_card` |
| `agents/app-reviewer.md` | `se_agent_app_reviewer.md` |
| `agents/math-error-workflow.md` | `se_agent_math_error_workflow.md` |

### Phase A 완료 선언

- ✅ 두 프로젝트 모두 `se_*` / `se_agent_*` prefix 적용
- ✅ SKILL.md frontmatter, 내부 참조, CLAUDE.md 모두 갱신
- ✅ 두 remote push 완료
- ➡️ Phase B 진입 가능: `se_agent_subject_helper` 설계

