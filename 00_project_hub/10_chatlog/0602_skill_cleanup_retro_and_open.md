<!-- 0602_skill_cleanup_retro_and_open.md -->

# 0602 — 스킬 정리 회고 + 열린 항목 정리

> NCC 자율 종료 기록. 직전 작업 = `0601_skill_cleanup_checklist.md` 실행(완료·push). 본 파일은 그 회고 + 앞으로 더 논의/불확실/개선/궁금/추가작업할 항목을 한곳에 모은 것.
> 후속 결정은 이 파일에 `# Round N` 누적. 마스터 플랜 = `00_project_hub/20_plan/0601_next_phase.md`.

---

## 0. 직전 라운드 결과 (스킬·에이전트 정리 — 완료)

- **최종 인벤토리:** 23 skill + 2 agent, 전부 kebab.
  - 영상 9 (se-people-pick·se-people-narrate·se-video-story·se-video-storyboard·se-video-narration·se-video-image·se-video-motion·se-video-render·se-video-compose)
  - math/audit/meta 13 (se-unit-plan·se-concept-review·se-math-figure·se-math-practice·se-math-error-note·se-type-explorer·se-unit-review·se-audit-{app,math,concept,problem,story}·se-distill-principles)
  - story 1 (se-story-write — 보존 결정)
  - agent 2 (se-unit-orchestrator·se-video-orchestrator)
- **폐기:** se_story_video_v1_5 → `90_archive/skills_legacy/` (8-STEP 완전 대체).
- **검증:** SSOT·미러 underscore 0 / forward 참조 잔존 0 / `name:` 전부 kebab / available-skills 등록 확인.
- **커밋:** `f811346` push 완료. 1차 배포(jwj-nick.github.io/mid1)도 라이브.

---

## 1. 🟡 더 논의할 것 (Nick 결정 대기)

1. **se-story-write 흡수 여부** — 현재 보존. 영상 파이프라인의 `se-people-narrate`와 역할 겹침(인물 산문). story.html(축B 앱) 입력으로 실사용 중이라 즉시 삭제 위험 → 보류. *추후: 두 스킬 입력/출력 스펙 비교 후 통합 or 분리 확정.*
2. **audit 접두 "ncc" 제거 수용 확인** — `se_ncc_audit_*` → `se-audit-*`로 줄임(TODO 선례). 호칭 NCC는 chatlog에서 유지, 스킬명에서만 탈락. 문제없으면 확정.
3. **nav app 위치** — `mid1/` 통합 vs 새 앱/새 배포. (0601 §5-2)
4. **연결망(connection-graph) 범위** — 중1 13단원만 vs 중2~고1 골격까지. (0601 §5-3) → 데이터 모델 SSOT 위치(`30_content/` graph)와 직결.
5. **감싼 설명(wrapping) 톤** — 딸용 짧은 감성 vs 참고형, 빈칸 남길지(절대원칙 5). (0601 §5-4)

---

## 2. ❓ 불확실한 것

- **sync-skills.sh 비-mirror 위험** — 삭제 동기화 안 됨. rename·폐기마다 `.claude/` 옛 디렉터리 수동 삭제 필요. → *개선안 §3-1.*
- **70_meta/ outdated 3종**(VISION·MASTER_PLAN·ROADMAP) — 옛 00_LearningSystem 시절 표기 잔존. 이번 정리에서 의도적으로 skip. 폐기 vs 갱신 미정.
- **.claude/settings.local.json 추적 상태** — git status에 계속 M으로 뜸. untrack(.gitignore) 할지 (0601 G1).
- **se-story-write 실제 호출 경로** — 축B 앱 제작이 현재 수동인지 스킬 경유인지 재확인 필요(흡수 결정의 전제).

---

## 3. 🔧 개선할 것

1. **sync-skills.sh를 mirror 모드로** — `--delete` 옵션 또는 rsync식 미러로 바꿔 옛 디렉터리 자동 청소. (수동 rm 실수 방지)
2. **영상 web 재인코딩** — 현 mp4 NO faststart → 폰 스트리밍 시 전체 다운로드 후 재생. `-movflags +faststart` + AAC mono 112k 재인코딩(option1, ~110MB). (0601 B4)
3. **lower-third(인물명 자막)·지도(maps)** — 영상 품질 개선 백로그. (0601 B1·B2)
4. **13편 전수 리뷰** — 일관성·길이·이미지 품질 최종 점검 1회. (0601 B3)
5. **70_meta 정리** — outdated 3종 폐기/갱신 결정 후 처리.

---

## 4. 🤔 궁금한 것 (0601 §5 Open Decisions 재게시)

1. **시작 작업** — A1(인물 배정 정본통일·즉효) / C(스킬 정리=완료) / A3(nav app·비전검증) 중 다음 첫 타?
2. **인물 추가 우선** — 옛 애니 4인 승격 vs meta 조연(thales·viete·fermat·boyle·liu-hui·playfair)?
3. **스킬 정리 시점 철학** — (이번엔 일괄 청소로 진행함) 앞으로 새 스킬은 새 콘텐츠 작업과 묶어 점진 도입할지.

---

## 5. ➕ 추가로 할 것 (백로그, 우선순위 미정)

| ID | 작업 | 디렉터리 | 스킬/에이전트 |
|---|---|---|---|
| A1 | 인물 배정 정본 통일(앱↔영상↔meta 불일치 4건: u06·u09·u11·u12) | `mid1/`, `30_content/units/` | — |
| A2 | 연결망 데이터 모델 | `30_content/` (graph SSOT) | 신규 스킬 후보 |
| A3 | navigation app | `20_packages/navigator/` + `mid1/`(or 신규) | 신규 |
| A4 | 인물이야기 감싼 설명 레이어 | story 앱/페이지 | se-story-write? |
| A5 | 단원당 인물 2~3인 풀 확장 | `30_content/people/` | se-people-pick |
| B4 | web 재인코딩(faststart) | `70_tools/`, `mid1/story/_video/` | — |
| F1 | Concept/Manim 영상 트랙(별개) | 신규 | 신규 |
| G1 | settings.local.json untrack | repo root | — |

> 불일치 4건 메모: u06 데카르트→케플러, u09 가우스→피타고라스, u11 케플러→플라톤, u12 카발리에리→아르키메데스. (영상·meta.json 기준이 정본, 옛 앱 애니는 `anim.html`로 보존 = 단원당 2인 보너스 콘텐츠.)

---

## 6. 다음 액션

- Nick이 §1·§4의 결정(특히 "다음 첫 타")을 정하면 해당 Round 착수.
- 기본 추천: **A1(정본 통일)** = 즉효·저위험, 6월 학습 시작 전 정합성 확보.
