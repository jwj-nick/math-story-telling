<!-- 260513_R5_system_guide.md -->

# Round 5 — 전체 시스템 가이드 문서 생성

> 작성: 2026-05-13 | NCC
> 트리거: Nick "F 작업완료후 전체 시스템(agent/skill)에 대한 가이드 문서 생성 바람"

## Round 4 회고

Phase A~D 완료, Phase C/E/F 뼈대 완성:
- Phase B: se_agent_subject_helper 구현 (commit 155baa2)
- Phase C/E: se_perf_eval_step, se_perf_eval_person, se_person_research SKILL.md (commit 199d1e3)
- Phase D: se_agent_app_reviewer 비수학 확장 (commit bb6405c)
- Phase F 뼈대: se_agent_pattern_extractor.md (00_LearningSystem/.claude/agents/)

## Phase F 완료 처리

Phase F의 "완료" = se_agent_pattern_extractor.md 작성 + 51_MASTER_PLAN 갱신.
실제 검증(P05 초안 자동 생성)은 다음 국어 글쓰기 작업 시 수행.

## NCC 실행 (Round 5)

### 산출: `SYSTEM_GUIDE.md`

`C:/Kids/00_LearningSystem/SYSTEM_GUIDE.md` 생성 — 9개 섹션:

1. **전체 그림** — ASCII 4-Layer 다이어그램
2. **빠른 참조** — HS 2604 + MathTelling 상황별 명령어 전체
3. **HS 2604 Agent 상세** — subject_helper (라우팅 테이블) + math_error_workflow + app_reviewer
4. **HS 2604 Skill 상세** — 구현 완료 5종 + 뼈대 3종
5. **MathTelling Agent+Skill 상세** — orchestrator Phase 순서 + 13 skill
6. **공통 자산** — 40_PRINCIPLES (6개) + 20_PATTERNS (P01~P06) + 30_COMPONENTS
7. **호출 흐름 예시** — 4개 시나리오 (수학 오답 배치, 수행평가 신규, MathTelling 단원, 패턴 추출)
8. **배포 구조** — jwj-nick.github.io/high1/ 폴더 트리
9. **현재 상태** — Phase A~G 완료 현황 + 다음 단계

### 부가 작업

- `README.md` 디렉토리 표에 `SYSTEM_GUIDE.md` 항목 추가
- `51_MASTER_PLAN.md` R5 기록 추가
- memory/ `project_phase_progress.md` 최종 업데이트

## 전체 Phase 최종 현황 (2026-05-13 기준)

| Phase | 내용 | 상태 |
|---|---|---|
| A | Prefix rename (se_*) | ✅ 양 프로젝트 push |
| B | se_agent_subject_helper | ✅ HS 2604 push |
| C | se_perf_eval_step | ⏳ 뼈대 (의뢰 시 즉시) |
| D | se_agent_app_reviewer 확장 | ✅ HS 2604 push |
| E | se_person_research, se_perf_eval_person | ⏳ 뼈대 (의뢰 시 즉시) |
| F | se_agent_pattern_extractor | ✅ 뼈대 완성 (00_LS) |
| G | B03·B04·B08 | 청사진 (패턴 추출 대기) |

## 다음 라운드 후보 (Round 6)

새 수행평가 또는 오답 의뢰가 올 때:
- 사회/도덕 Step형 → se_perf_eval_step 실제 실행 검증 (Phase C 완료 조건)
- 인물 수행평가 → se_perf_eval_person 실제 실행 검증 (Phase E 완료 조건)
- 국어 글쓰기 → P05 패턴 분석 + se_writing_essay B03 구현

또는 SYSTEM_GUIDE 보완:
- se_agent_pattern_extractor 실제 실행 예시 추가
- Phase G (B03/B04/B08) 청사진 보강
