<!-- TODO_skill_architecture.md / 스킬·에이전트 정리·마이그레이션 계획 (네이밍 일원화) -->

# TODO — 스킬·에이전트 아키텍처 정리

> **발단 (Nick, 2026-05-29)**: "기존 underbar style skill, agent 중 person/video 관련된 것들은 더 이상 필요없을 것 같은데. 수학문제 만들어내는 쪽은 agentskills style(kebab)로 수정하고 새로 컨텐츠 만들어보자."
> **배경**: 영상 8-STEP 파이프라인이 kebab(agentskills.io 표준)으로 정식 졸업. 기존 math/story 스킬은 underscore. 네이밍 혼재 + 레거시 중복 발생.
> **원칙**: agentskills.io spec 준수 = name kebab-case ([[reference_agentskills_spec]]). 본 프로젝트 신규 스킬 표준.

---

## 1. 현재 스킬 전수 (24 skills + 2 agents)

### 1.1 영상 신 파이프라인 — kebab ✅ (졸업 완료, 유지)
| 스킬 | 역할 |
|---|---|
| se-people-pick | 단원 인물 발굴·선정 |
| se-people-narrate | 인물 서사(약속 3겹) |
| se-video-story | 서사 → 6장면 시드 |
| se-video-storyboard | 정밀 카드(부록 A/B/C) |
| se-video-narration | 2화자 dialog + ElevenLabs |
| se-video-image | 캐릭터 일관 프롬프트 + Nano Banana |
| se-video-motion | scene 모션 + 자막 타이밍 |
| se-video-render | FFmpeg zoompan+자막 |
| se-video-compose | A/V mux + 표지 |

### 1.2 person/video 레거시 — underscore ⚠️ (정리 대상)
| 스킬 | 판정 | 사유 |
|---|---|---|
| **se_story_video_v1_5** | 🔴 **폐기(아카이브)** | v1.5 6장면 110s edge-tts 단일 스킬. 8-STEP kebab 파이프라인이 완전 대체. 재사용 가치 = 레거시 기록뿐 → 90_archive |
| **se_story_write** | 🟡 **재평가 후 흡수** | 인물 서사 프로즈 작성. `se-people-narrate`(서사)와 역할 중복. 단, 단원 앱 `story.html`(축 B)용 산문 서사는 여전히 필요 → se-people-narrate 산출(1-narrative.md)을 story.html 입력으로 재사용 가능한지 확인 후, 가능하면 폐기 / 불가하면 kebab으로 흡수 |
| **se_ncc_audit_story** | 🟢 **유지(audit 계열로)** | 영상은 orchestrator 품질 게이트가 커버. 앱 story.html 검수에는 여전히 유효 → audit 계열 일괄 마이그레이션에 포함 |

### 1.3 math/concept/audit — underscore (kebab 마이그레이션 대상)
| 스킬 | Phase | 마이그레이션 후보명 |
|---|---|---|
| se_unit_plan | 0 | se-unit-plan |
| se_concept_review | 1 | se-concept-review |
| se_math_figure | 3,5 | se-math-figure |
| se_math_practice | 5c | se-math-practice |
| se_math_error_note | 5 | se-math-error-note |
| se_type_explorer | 5d | se-type-explorer |
| se_unit_review | — | se-unit-review |
| se_ncc_audit_app | audit | se-audit-app |
| se_ncc_audit_math | audit | se-audit-math |
| se_ncc_audit_concept | audit | se-audit-concept |
| se_ncc_audit_problem | audit | se-audit-problem |
| se_ncc_audit_story | audit | se-audit-story |
| se_distill_principles | meta | se-distill-principles |

### 1.4 Agents
| 에이전트 | 판정 |
|---|---|
| se-video-orchestrator | ✅ kebab, 유지 |
| **se_agent_unit_orchestrator** | 🟡 kebab 마이그레이션 → `se-unit-orchestrator` (또는 `se-math-orchestrator`). 내부 스킬 참조도 kebab으로 갱신 필요 |

---

## 2. 결정 필요 항목

### 결정 A — se_story_write 처리
- (1) **폐기** — se-people-narrate 산출을 story.html에 직접 재사용
- (2) **흡수** — story.html 전용 산문이 영상 서사와 다르면 se-story-write(kebab)로 별도 유지
- **확인 방법**: 기존 단원(unit01~04) story.html이 무엇을 입력으로 쓰는지 / se-people-narrate 산출과 톤·길이 차이 점검

### 결정 B — math 스킬 마이그레이션 범위·시점
- (1) **전수 일괄** — 13개 스킬 + 1 agent 한 번에 rename + 참조 갱신 + sync (작업 큼, 깨끗)
- (2) **점진** — 새 단원 제작에 쓰는 순서대로 마이그레이션 (실사용 검증하며)
- **권장**: (2) 점진 — "새로 컨텐츠 만들어보는" 실작업과 묶어서, 쓰는 스킬부터 kebab화 + 검증

### 결정 C — "새 컨텐츠" 정의
- 영상 양산(단원2~6)과 별개로, **math 4축 콘텐츠(개념·문제)** 신규 제작 대상 단원 = ?
  - 후보: 영상이 끝난 단원의 문제 연습 보강 / 미완성 단원(unit05+)의 개념·문제
  - → 영상 양산 일단락 후 결정

---

## 3. 마이그레이션 표준 절차 (스킬 1개당)

```
1. 10_system/30_skills/se_xxx_yyy/ → se-xxx-yyy/ (디렉토리 rename)
2. SKILL.md frontmatter: name: se-xxx-yyy (kebab), description 점검 (agentskills spec)
3. 내부 cross-link·경로 참조 갱신 (../se_xxx → ../se-xxx)
4. 이 스킬을 참조하는 agent/CLAUDE.md/workflow 갱신
5. bash 70_tools/sync-skills.sh → .claude/skills 미러
6. 호출 테스트 (available-skills 목록 등록 확인)
```

---

## 4. 우선순위 (제안)

| 순위 | 작업 | 비고 |
|---|---|---|
| 1 | **se_story_video_v1_5 → 90_archive** | 즉시 가능, 무위험 (영상 신 파이프라인이 대체 완료) |
| 2 | 영상 양산(단원2~6) 완주 | 본 TODO와 병행 — 영상이 분수령 |
| 3 | 결정 A (se_story_write) 확정 | story.html 입력 점검 후 |
| 4 | math 스킬 점진 kebab화 + 새 콘텐츠 | 결정 B(2)·C |
| 5 | se_agent_unit_orchestrator → kebab | math 스킬 마이그레이션 후 일괄 |

---

## 5. 진행 로그

| 날짜 | 항목 | 메모 |
|---|---|---|
| 2026-05-29 | 신설 | 영상 8-STEP kebab 졸업 직후. person/video 레거시 판정 + math 마이그레이션 계획 기록. 즉시 착수 X — 영상 양산 우선, 마이그레이션은 새 콘텐츠 작업과 묶어 점진. |
