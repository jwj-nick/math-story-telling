# Q02 — Skill·Agent 중앙화 vs 프로젝트별 복제

> 상태: 🔴 미결. 향후 시스템 전체 구조에 영향 큼.

## 질문

skill / agent 정의 파일(`.claude/skills/*/SKILL.md`, `.claude/agents/*.md`)을:

- (A) **중앙**에 두고 자식 프로젝트에서 link / symlink / 참조?
- (B) **각 프로젝트별로 복제**? (현재 상태)
- (C) **하이브리드** — 공통 skill은 중앙, 프로젝트 특화는 로컬?

## 현재 상태 (2026-05-11)

- MathTelling `.claude/`: 13 skill + 1 agent (꽤 많음)
- HighSchool 2604 `.claude/`: 5 skill + 2 agent
- 동명 skill: `math-error-note`, `math-figure`, `math-practice` — 둘 다 존재. 내용 동기화 안 됨 (확인 필요)

## (A) 중앙화의 장점·단점

장점:
- 한 곳에서 수정 → 모든 프로젝트에 반영
- 패턴·컴포넌트·원칙과 묶기 자연스러움 (이 디렉토리)

단점:
- Claude Code의 `.claude/` 가 프로젝트별 인식 → 중앙 위치를 인식시키기 위한 설정 필요
- symlink는 Windows 에서 권한·동작 비표준 (가능은 함)
- 프로젝트별 특수 동작이 필요할 때 복잡

## (B) 프로젝트별 복제의 장점·단점

장점:
- 현재 동작. 추가 설정 불필요.
- 프로젝트별 자유도 보장

단점:
- 동기화 부담. 한 곳 수정하면 다른 곳도 따라가야 함.
- 어느 게 "최신·정본"인지 추적 어려움

## (C) 하이브리드

- 중앙: `00_LearningSystem/_canonical/skills/`, `_canonical/agents/`
- 각 프로젝트의 `.claude/skills/` 에는 "이 skill은 _canonical에서 복제됨, 변경하지 마세요" 헤더 + 자동 동기화 스크립트

## NCC 제안 (default)

당분간 **(B) 프로젝트별 복제** 유지. 단:
1. 이 디렉토리(`50_BLUEPRINTS.md`)에 **canonical 설계서**를 둠
2. 새 skill 만들 때 항상 BLUEPRINTS 먼저 작성 → 그 다음 자식 프로젝트에 구현
3. 동기화 필요 발생 시 (C) 검토

## (Nick) 응답

> (Nick): B

---

## 결정 후 적용
- 40_PRINCIPLES.md 의 "B. 배포 / D. 자료" 사이에 "Skill 관리" 섹션 추가
- 50_BLUEPRINTS.md 의 모든 항목에 "canonical 위치" 명시
