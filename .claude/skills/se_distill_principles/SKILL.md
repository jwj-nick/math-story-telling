---
name: se_distill_principles
description: insights/ 누적분에서 패턴을 추출해 principles/ 또는 context/를 업데이트한다. 수동 호출. 호출 예시 — "/se_distill_principles", "/se_distill_principles 영상", "/se_distill_principles --since 2026-05".
---

# se_distill_principles — Insight → Principle 진화 스킬

> **이 skill의 SSOT**: `C:/Kids/90_Workspace/mathtelling/system/skills/se_distill_principles/SKILL.md`
>
> `.claude/skills/se_distill_principles/`은 `system/sync-skills.sh`로 복제된 거울. 수정 금지.
>
> 진화 사이클 [3] Distill 단계를 담당. [1] Build [2] Retrospect [4] Apply는 다른 skill이 맡음.

## 역할

- `mathtelling/system/insights/`의 **미반영** insight 파일들을 스캔
- 반복되는 패턴·일반 원칙 후보를 추출
- 어느 `system/principles/*.md` 또는 `system/context/*.md`에 어떻게 반영할지 제안
- Nick 승인 후 해당 문서 업데이트 + insight에 "반영완료 → ..." 마크
- `insights/_index.md`도 갱신

## 인자

```
/se_distill_principles               # 모든 미반영 insight
/se_distill_principles 영상          # 영상 관련 insight만 (skill 이름 필터)
/se_distill_principles --since 2026-05    # 특정 기간 이후
/se_distill_principles --dry          # 분석만, 실제 업데이트 X
```

## 입력 자료

| 파일 | 용도 |
|---|---|
| `system/insights/_index.md` | 미반영 목록 |
| `system/insights/{date}_*.md` | 개별 회고 본문 |
| `system/principles/*.md` | 업데이트 대상 |
| `system/context/*.md` | 업데이트 대상 |

## 절차

### Phase A — 스캔 (자동)

1. `_index.md` 미반영 섹션 파싱
2. 각 insight 파일 읽기, "일반 원칙 후보" 섹션 추출
3. 필터 적용 (skill 이름, 날짜 등)

### Phase B — 패턴 추출 (자동, NCC 판단)

4. 후보들을 의미별 그룹화 (예: "narration 길이", "이미지 명세", "audit timing")
5. 반복도 평가:
   - **즉시 반영**: 1개 후보라도 명확한 규칙이면 OK (1차 운영 기준)
   - **N편 모이면**: 같은 패턴 2회 이상이면 강한 신호
6. 각 그룹에 대해:
   - 어느 문서에 반영? (principles/ vs context/ vs 신규 파일)
   - 어느 섹션에? (§N 명시)
   - 어떤 표현으로? (제안 문장 작성)

### Phase C — Nick 승인 (대화)

7. 다음 양식으로 chat에 제시:
```
## 제안 N: {규칙 한 줄}
- 출처: insights/{file}.md "{후보 N}"
- 대상: principles/STORY_VIDEO_v1_5.md §{N}
- 변경 전: "{기존 문장}"
- 변경 후: "{새 문장}"
- 적용 예: {언제 이 규칙이 발동되나}
```
8. Nick: yes / no / 수정 / 보류

### Phase D — 적용 (자동)

9. 승인된 항목:
   - `Edit`로 principles/ 또는 context/ 업데이트
   - 해당 .md의 "변경 이력"에 한 줄 추가
   - insight 파일의 "반영 상태"를 `[x] 반영완료 → principles/XXX.md §N`로 변경
   - `_index.md`의 미반영 → 반영완료 이동, 링크 갱신
10. 보류된 항목: insight 그대로 둠. 다음 distill에서 다시.

### Phase E — 보고

11. 요약 chat 출력:
   - 처리된 insight 개수
   - 반영된 원칙 개수
   - 다음 distill 권장 시점 (insight N편 더 누적 후 등)

## 신규 principle 파일 생성 기준

- 기존 파일에 안 맞으면 신규 생성 가능
- 신규 파일도 `system/principles/<NAME>.md`에. 시리즈가 아니면 단일 파일.
- 변경 이력 섹션 필수.

## 안전

- `--dry` 옵션으로 변경 없이 분석만 가능
- 모든 Edit는 Nick 승인 후
- principles/ context/ 변경 시 반드시 변경 이력 추가
- 같은 원칙이 이미 있으면 중복 X, "강화" 또는 "보강" 표시

## 호출 빈도 가이드

- **1차 운영**: insight 1편이라도 명확한 원칙 후보 있으면 즉시 호출 가능
- **권장**: 같은 skill의 insight 3편 누적 후 (패턴 신뢰도 ↑)
- **금기**: 자동 호출 X. Nick 수동 트리거.

## 변경 이력

- 2026-05-21 v0.1 — 진화 사이클 [3] Distill 단계 정의. 1편이라도 명확한 원칙은 즉시 반영.
