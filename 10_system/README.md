<!-- README.md -->

# mathtelling/system/ — 메타 자원 (원칙·스킬·컨텍스트·진화)

> mathtelling repo의 self-contained 메타 레이어.
> NCC가 매 작업 시 읽고, 매 작업 후 누적시키는 곳.
>
> 시작일: 2026-05-21

---

## 디렉토리 역할

| 디렉토리 | 무엇이 들어가나 | 누가 읽고/쓰나 |
|---|---|---|
| `principles/` | 위반 시 audit fail 수준의 **규칙·명세** | 모든 skill이 시작 시 읽음. distill이 업데이트 |
| `context/` | 학습자·인물·시대 등 **고정 사실/가이드** | skill이 참조 |
| `skills/` | 이 repo가 SSOT인 skill 정의 | sync-skills.sh로 `.claude/skills/`에 복사 |
| `proposals/` | 확정 직전 skill·기능 명세 incubation | chatlog → proposals → skills 흐름. 승격 시 제거 |
| `workflows/` | 다단계 작업 절차 | skill이 참조 |
| `insights/` | 매 작업 후 회고 (자동 누적) | skill이 종료 시 작성. distill이 모아서 진화 |
| `playbooks/` | (예약) 운영 가이드 | — |

---

## 진화 사이클 (4단계)

```
[1] Build          단원 영상·앱 제작 (skill 실행)
       ↓
[2] Retrospect     skill 종료 직전, insight 자동 작성
                   → insights/YYMMDD_unitNN_<skill>.md
                   양식: _template.md (잘 된 것 / 아쉬운 것 / 원칙 후보)
       ↓
[3] Distill        /se_distill_principles 수동 호출
                   → insights/_index.md에서 미반영 항목 스캔
                   → principles/*.md 또는 context/*.md 업데이트 제안
                   → Nick 승인 후 적용 + 해당 insight에 "반영완료 → ..." 마크
       ↓
[4] Apply          다음 작업부터 자동 적용 (skill이 principles/를 항상 읽음)
       ↓
       (다시 [1]로)
```

---

## Skill 동기화 (단방향)

- **SSOT**: `mathtelling/system/skills/<skill>/`
- **거울**: `C:/Kids/30_MiddleSchool/260426_MathTelling_Idea/.claude/skills/<skill>/`
- **동기화**: `bash system/sync-skills.sh` 수동 실행 (system → .claude)
- 역방향 X. `.claude/`에서 임의 수정 금지 — 다음 sync 때 덮어쓰임.
- 현재 sync 대상: 없음 (base의 skill들은 그대로 둠 — D4). 신규 skill만 system/skills/에 생성.

---

## Insight 파일 명명

```
insights/{YYMMDD}_{unit-or-target}_{skill-name}.md
```

예:
- `260520_unit01_story_video_v1_5.md`
- `260601_unit02_math_practice.md`

`_index.md`에 한 줄씩 등록. 반영 완료 시 체크박스 + 어느 principle에 반영했는지 링크.

---

## 첫 입주자 (2026-05-21)

| 파일 | 출처 | 비고 |
|---|---|---|
| `principles/STORY_VIDEO_v1_5.md` | `channel/_docs/PIPELINE_v1_5.md` 이동 | v1.5 영상 SSOT |
| `context/TONE_GUIDE.md` | Unit 01 v1.5 narration 정제 경험 | 신규 |
| `context/ERA_PALETTES.md` | era-ancient 검증분 + 슬롯 | 신규 (ancient만 확정) |
| `insights/_template.md` | 회고 양식 | 신규 |
| `insights/_index.md` | 회고 목록 | 신규 |
| `insights/260520_unit01_story_video_v1_5.md` | 첫 회고 시연 | 신규 |
| `sync-skills.sh` | skills 단방향 동기화 | 신규 |

---

## NCC가 작업 시작 시 읽어야 할 우선순위

1. `mathtelling/CLAUDE.md` 또는 base CLAUDE.md (anchor)
2. 해당 skill의 SKILL.md (어느 principle을 읽어야 하는지 명시되어 있음)
3. `system/principles/<해당 파일>` (SSOT 규칙)
4. `system/context/<관련 파일>` (배경 정보)
5. `system/insights/_index.md`의 미반영 항목 — "다음에 다르게 해볼 것" 참조

---

## 변경 이력

- 2026-05-21 v0.1 — skeleton + 첫 입주자 5종 배치. D1=B, D2=sync script, D3=insight 누적+반영완료 마크, D4=base 그대로.
