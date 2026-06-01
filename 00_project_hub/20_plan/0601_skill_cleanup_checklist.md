<!-- 0601_skill_cleanup_checklist.md -->

# 0601 스킬·에이전트 정리 — 실행 체크리스트

> ✅ **완료 (2026-06-01)**: v1_5 아카이브 + 13 skill + 1 agent kebab rename + frontmatter/cross-ref 일괄 치환 + .claude 미러 청소·재동기화 + CLAUDE.md 갱신. 검증: SSOT·미러 underscore 0, forward 잔존 0. (se_story_write는 결정대로 se-story-write로 보존.)

> `0601_next_phase.md` §4의 실행본. 작업하며 [x] 체크. SSOT=`10_system/30_skills`·`35_agents` → `.claude/`(sync).
> ⚠️ sync-skills.sh = 비-mirror → rename 후 `.claude/`의 **옛 디렉터리 수동 삭제** 필수.

## 결정 (확정)
- **se_story_video_v1_5** → 🔴 `90_archive/` 이관 (8-STEP 완전 대체). skills·mirror에서 제거.
- **se_story_write** → 🟢 **유지+kebab**(`se-story-write`). story.html(축B 앱) 산문 입력으로 실사용 → 삭제 위험, 보존. (se-people-narrate 흡수는 추후 Nick 결정.)
- **audit 5종** → `se-audit-*` (ncc 접두 제거, TODO 선례). 
- **나머지 math/meta** → 단순 kebab. agent `se_agent_unit_orchestrator`→`se-unit-orchestrator`.

## 이름 맵 (old → new)
| old | new |
|---|---|
| se_story_video_v1_5 | (archive) |
| se_story_write | se-story-write |
| se_unit_plan | se-unit-plan |
| se_concept_review | se-concept-review |
| se_math_figure | se-math-figure |
| se_math_practice | se-math-practice |
| se_math_error_note | se-math-error-note |
| se_type_explorer | se-type-explorer |
| se_unit_review | se-unit-review |
| se_ncc_audit_app | se-audit-app |
| se_ncc_audit_math | se-audit-math |
| se_ncc_audit_concept | se-audit-concept |
| se_ncc_audit_problem | se-audit-problem |
| se_ncc_audit_story | se-audit-story |
| se_distill_principles | se-distill-principles |
| se_agent_unit_orchestrator (agent) | se-unit-orchestrator |

## 체크리스트
### 1. v1_5 아카이브
- [x] `10_system/30_skills/se_story_video_v1_5/` → `90_archive/skills_legacy/` (git mv)
- [x] `.claude/skills/se_story_video_v1_5/` 삭제

### 2. 디렉터리 rename (SSOT) — 14개 (story-write 포함 13 skill + 1 agent)
- [x] 13 skill dir git mv (old→new)
- [x] agent file git mv se_agent_unit_orchestrator.md → se-unit-orchestrator.md

### 3. frontmatter `name:` kebab 갱신 (각 skill/agent)
- [x] 13 skill `name:` + ssot 경로 라인
- [x] agent `name:`

### 4. 참조 일괄 치환 (forward 파일)
- [x] skills 내부 cross-link [[..]]·경로·/명령
- [x] agents (se-unit-orchestrator 내부 스킬 호출, se-video-orchestrator)
- [x] CLAUDE.md 스킬표·agent표
- [x] 10_system/README.md, principles(STORY_VIDEO_v1_5·UNIT_PAGE_STANDARD)
- [x] (70_meta = outdated, skip — §4.5에서 별도 정리)

### 5. mirror 재동기화
- [x] `.claude/skills` 옛 디렉터리 14개 삭제
- [x] `.claude/agents/se_agent_unit_orchestrator.md` 삭제
- [x] bash 70_tools/sync-skills.sh

### 6. 검증·커밋
- [x] 잔존 underscore 스킬명 grep 0 (forward 파일)
- [x] skill 디렉터리 전부 kebab
- [x] commit (`f811346` push 완료)

---

## 실제 결과 (2026-06-01 종료 기록)
- **최종 인벤토리:** 23 skill + 2 agent, 전부 kebab. (영상 9 + math/audit/meta 13 + se-story-write 1 / orchestrator 2)
- **검증:** SSOT underscore 0 · `.claude` 미러 underscore 0 · forward 잔존 0 (v1_5는 "폐기·아카이브" 노트로만 잔존).
- **커밋:** `f811346` ("refactor(skills): 옛 underbar 스킬 14개 + agent 1개 최신 kebab 스타일로 정리") → origin push 완료.
- **available-skills 목록**에 새 kebab 스킬 정상 등록 확인.
- 남은 후속 논의는 `00_project_hub/10_chatlog/0602_skill_cleanup_retro_and_open.md` 참조.
