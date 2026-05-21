<!-- 260512_R2_master_plan.md -->

# Round 2 — Master Plan 작성

> 작성: 2026-05-12 | NCC + Nick

## Round 1 회고 (정합성 점검)

R1에서 Q01~Q07 응답을 반영했지만, **두 가지 약점**이 남았다:

1. **"Round 2 후보"라고 적었지만 실제 Round 2 내용은 정의 안 됨** — Nick 지적
   - "지금 당신이 말하는 round2 는 무엇이고 어디 적혀있나요?"
   - → 본 Round 2가 답.

2. **세부 빌드 플랜이 50_BLUEPRINTS.md 안에 흩어져 있고, 링크 다이어그램·시퀀스가 부재**
   - 개별 skill 명세는 있으나, "전체 시스템 그림" + "어떤 순서로 만드나"는 별도 문서 필요
   - → `51_MASTER_PLAN.md` 신규 작성.

3. **Q05 응답 해석 오해 가능성**
   - 원 응답: "우선순위는 없고 그때 그때 만들어 쓸 예정. 기본 시스템이 중요함"
   - NCC 해석 (R1): "다음 과목 앱 만드는 순서는 없음" → 일부만 맞음
   - **정확한 해석**: 과목 앱 X. 일반화된 agent/skill 시스템 자체가 산출물.
   - → 51_MASTER_PLAN.md §0 에 명시.

---

## Nick 추가 지시 (Round 2 트리거)

> "지금 전체 agent/skill master plan, link diagram 을 현재 갖춘 자료들 만 갖고 한번 만들어 봅시다.
> '다음 과목 확장 우선순위' 는 어떤 과목 앱을 만들자... 에 대한 우선순위는 없다는거고..
> 일반화된 agent/skill system 을 만듭시다.
> 세부 계획을 뭘 보면 알수있나요?
> 지금 당신이 말하는 round2 는 무엇이고 어디 적혀있나요?
> 세부 plan 을 별도 파일로 정리 해봅시다."

---

## NCC 실행 (Round 2)

### 산출: `51_MASTER_PLAN.md`

9 섹션 구조:
1. 이 파일이 답하는 것 (Nick의 질문 매핑)
2. 인벤토리 — 현존 + 계획 (skill 24·agent 7 추산)
3. 링크 다이어그램 (ASCII + Mermaid 양식)
4. 4-Layer 모델 (Agent → Composite Skill → Atomic Skill → 자산)
5. 빌드 순서 Phase A~G
6. 의존 관계 표 (skill↔skill, agent→skill, 자산 참조)
7. Phase 진입·종료 조건
8. "지금 당장" 할 일 (Phase A rename)
9. 참조 + Round 변경 이력

### 핵심 결정

**4-Layer 구조 도입**:
- Agent (L3) — 자연어·orchestration
- Composite Skill (L2) — 도메인 특화
- Atomic Skill (L1) — 재사용 부품
- 자산 (L0) — 패턴·원칙·컴포넌트 .md
- 규칙: L3→L2→L1 (단방향), L0은 모두가 참조

**빌드 순서 Phase A~F**:
- A: Prefix rename (1~2주) ⭐ 즉시 가능
- B: subject_helper 라이트 (2주)
- C: perf_eval_step (수행평가 의뢰 시)
- D: app_reviewer 비수학 확장
- E: person_research 분리
- F: pattern_extractor

**Phase 순차 실행**:
- 병렬 X — 자식 프로젝트 동기화 부담 큼
- 각 Phase 종료 조건 명시 → 다음 진입 게이트

---

## Q05 명확화 (Round 1 해석 보정)

`70_OPEN_QUESTIONS/Q05_과목_확장_우선순위.md` 의 응답 의미:
- ❌ "다음에 만들 과목 앱 우선순위가 없다"
- ✅ "과목 앱 만드는 게 우선이 아니라, 일반화된 시스템 빌드가 우선"

→ 이 chatlog 에 기록. Q05 파일 자체 수정은 안 함 (Nick의 원문 유지). 51_MASTER_PLAN 이 해석의 정본.

---

## 다음 라운드 후보 (Round 3)

Phase A 시작 신호 받으면:
- Round 3 = MathTelling + HighSchool 자식 프로젝트의 skill/agent rename 작업
- 두 프로젝트 동시 처리 vs 한 프로젝트씩 — Nick 결정 받기

> (Nick): 51_MASTER_PLAN.md 검토 후 응답 부탁
> - Phase 순서·시기 OK?
> - "지금 당장" Phase A 시작할까, 아니면 다른 작업 의뢰 받을 때까지 대기?
> - 빠진 skill/agent 있나? (예: 영상·video 영역?)
