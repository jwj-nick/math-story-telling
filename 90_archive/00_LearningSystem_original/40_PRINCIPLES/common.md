# 40_PRINCIPLES/common — 모든 앱·작업 공통 원칙

> 이 원칙은 수학·수행평가·글쓰기·과학·기타 모든 영역에 적용된다.

## A. 학습 설계 원칙

### A1. 점진적 공개 (Progressive Disclosure)
- 학생이 스스로 풀어나가는 흐름을 막지 않는다
- 답·힌트·결과를 미리 보여주지 않는다
- 모범답안은 별도 페이지 또는 별도 앱 (마지막 탭)

### A2. 빈칸 유지
- form-mirror, think-box, simulator 모든 컴포넌트는 학생이 채울 칸을 비워둔다
- 학생 답안과 모범답안을 한 화면에 동시 노출 X

### A3. 학생의 글·답안·반응은 수정 금지
- 학생 본인이 쓴 것은 절대 자동 수정 없음
- 피드백은 별도 파일 (예: MathTelling `feedback/` 폴더)

## B. 기술 원칙

### B1. 단일 HTML 파일
- 빌드·번들 금지, npm·node 의존 금지
- 의존성: KaTeX (수학), JSXGraph (수학 그래프) 만 허용
- 학생이 코드를 직접 열어볼 수 있도록

### B2. 모바일 대응
- max-width 680~720px
- tab-bar overflow-x: auto (스크롤 가능)
- @media (max-width: 400px) 에서 grid → 1열

### B3. 색·아이콘
- Step·페이지·과제별로 일관된 색 매핑 (사회 메가시티: 주황→빨강→청록→보라)
- 이모지는 영역 식별용으로만, 본문 가독성 해치지 않게

## C. 자료·근거 원칙

### C1. 출처 신뢰도 등급

| 등급 | 출처 |
|---|---|
| ★★★ 高 | 통계청 (kosis.kr), 한국은행, 국토부, 교과서, 학술 자료 |
| ★★ 中 | 주요 일간지, KBS·MBC 시사다큐, 공신력 있는 단체 |
| ★ 低 | 개인 블로그, 위키, 출처 불명 |

### C2. 학생용 자료는 ★★★ 또는 ★★ 만

### C3. 추측 금지
- OCR·이미지 판독에서 불확실하면 `⚠️OCR?` 표시
- 미해결 사항은 `issue.md`에 기록

## D. 안전 원칙

### D1. 원본 캡쳐 jpg 수정·삭제 금지
- `01_capture/` 폴더는 read-only로 취급

### D2. git 작업
- 파괴적 작업(`reset --hard`, `push --force`) 사용자 명시 없이 금지
- 한국어 commit 메시지 OK
- 과목별 commit 분리 (2026-05-11 확정)

## E. Skill 관리 (Q02 응답 반영)

### E1. 현행: 프로젝트별 복제
- skill·agent 정의는 각 자식 프로젝트 `.claude/skills/` 와 `.claude/agents/`에 위치
- 동기화 부담은 인지하되, 당분간 감수

### E2. Naming (Q07 응답)
- Skill 명령: `se_<기능명>` (예: `/se_perf_eval_step`)
- Agent 이름: `se_agent_<역할>` (예: `se_agent_subject_helper`)
- prefix `se_` = Nick의 자식 이름 관련 마커

### E3. 변경·신규 절차
1. `50_BLUEPRINTS.md` 에 canonical 설계 먼저
2. 자식 프로젝트의 `.claude/`에 구현
3. 1회 이상 검증 후 BLUEPRINTS에 "검증" 마크
4. 변경 시 모든 자식 프로젝트 동기화 (수동, 현행)

### E4. 향후 (Q01 응답)
- 충분히 안정되면 → plugin 형태로 분리 (Claude Code plugin)

---

## 원칙 변경 절차
1. `70_OPEN_QUESTIONS/` 질문 파일 생성
2. Nick 응답 → 이 문서 갱신
3. `00_chatlog/` 에 변경 라운드 기록

## 변경 이력
- 2026-05-11: 초안 (단일 파일)
- 2026-05-12: 영역별 분리 구조로 재편 (Q06 B 응답)
