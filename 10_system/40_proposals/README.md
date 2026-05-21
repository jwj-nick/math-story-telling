<!-- README.md -->

# system/proposals/ — Skill 명세 Incubation

> chatlog 라운드에서 **확정 직전**의 skill·기능 명세를 두는 곳.
> 확정되면 `system/skills/<name>/SKILL.md`로 승격되고 이 디렉토리에서 제거.

---

## 흐름

```
00_project_hub/chatlog/ (대화 라운드)
   ↓ (Nick 결정 후)
system/proposals/<skill-name>.md (incubation — 다듬기·구체화)
   ↓ (Nick 최종 승인)
system/skills/<skill-name>/SKILL.md (SSOT)
   ↓ (bash system/sync-skills.sh)
.claude/skills/<skill-name>/SKILL.md (거울)
```

## 무엇이 들어가나

- Skill 명세 초안 (frontmatter + 절차 + Phase + 참조 파일)
- 기존 skill의 **major upgrade** 제안 (v0.x → v1.0 같은)
- 신규 context 파일 제안 (`system/context/<name>.md` 초안)

## 무엇이 들어가지 않나

- 일회성 작업 (chatlog로 충분)
- 단순 버그 fix (skill 직접 수정)
- 토론·아이디어 단계 (chatlog가 적합)

## 명명 규칙

- skill 제안: `<skill-name>.md` (예: `se_image_prompts_pro.md`)
- context 제안: `context_<name>.md`
- 일반 기능 제안: `feature_<name>.md`

## 라이프사이클

| 상태 | 표기 | 의미 |
|---|---|---|
| draft | 파일 헤더에 `> Status: draft` | 작성 중, Nick 검토 대기 |
| review | `> Status: review` | Nick 검토 라운드 |
| approved | `> Status: approved` | 승인. SKILL.md로 승격 준비 |
| promoted | (파일 삭제) | system/skills/로 승격 완료. proposals에서 제거 |
| dropped | (파일 삭제 또는 archive) | 무산. archive/에 보관 가능 |

---

## 현재 incubation 중

(없음 — 2026-05-21 디렉토리 신설)

대기 중인 아이디어:
- 3개 신규 skill — `00_project_hub/chatlog/260521_skill_ideas_3new.md` Round 1에서 논의 중. Nick D1-D4 결정 후 이 디렉토리로 이동.

---

## 변경 이력
- 2026-05-21 v0.1 — 디렉토리 신설. chatlog → proposals → skills 흐름 정의.
