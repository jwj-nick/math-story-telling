# CLAUDE.md — Kids 학습 시스템 진입 규칙

> 새 Claude 세션이 `C:/Kids/00_LearningSystem/` 작업으로 시작되면 이 파일을 먼저 읽는다.

## 이 디렉토리의 본질

**메타 레이어**. 실제 학생용 산출물(앱, .md 자료)은 만들지 않는다.
대신 **패턴·원칙·청사진·미해결 질문**을 정리한다.

학생용 산출물은 자식 프로젝트에서:
- `C:/Kids/30_MiddleSchool/260426_MathTelling_Idea/` (딸/중1/수학)
- `C:/Kids/70_HighSchool/2604_고1_중간고사/` (아들/고1/시험·수행평가)

---

## 작업 원칙

1. **chatlog 원칙 (Q03 확정)**: 모든 작업·결정·진행을 `00_chatlog/YYMMDD_R<N>_주제.md` 에 기록. Nick의 inline 응답도 NCC가 chatlog로 옮긴다. 화면 출력은 최소.
2. **새 패턴을 발견하면 추출한다.** 자식 프로젝트에서 작업 끝난 후, 일반화 가능한 부분만 `20_PATTERNS/`에 정리. 본문 복사 금지, 참조만.
3. **의문은 질문 파일로.** 답을 추측해서 적지 말고 `70_OPEN_QUESTIONS/QXX_*.md`에 질문으로 남긴다. Nick의 `(Nick)` 응답을 받은 후 원칙 문서에 반영.
4. **간결하게.** 각 파일은 50~200줄. 길어지면 분리.
5. **두 프로젝트의 차이를 인정한다.** MathTelling·HighSchool 각자의 작업 방식 유지. NCC는 자기 의사결정 기록만 chatlog 원칙 적용.
6. **Naming 규약 (Q07 확정)**: skill = `se_*`, agent = `se_agent_*`.

---

## 진입 절차

1. `00_chatlog/` 최근 5개 파일 훑어 진행 중 라운드 확인
2. 자식 프로젝트의 `(Nick)` 미처리 항목 스캔
3. `README.md` → `10_VISION.md` 읽기
4. 작업 종류에 따라:
   - **패턴 추가/검토** → `20_PATTERNS/README.md`
   - **컴포넌트 추가** → `30_COMPONENTS.md`
   - **원칙 결정** → `40_PRINCIPLES/<영역>.md` + 관련 OPEN_QUESTION
   - **다음 스킬·에이전트 설계** → 개별 명세 `50_BLUEPRINTS.md`, 전체 그림·빌드 순서 `51_MASTER_PLAN.md`
   - **로드맵 갱신** → `80_ROADMAP.md`
5. 새 작업이면 → 새 chatlog 파일 생성, chat window에 파일명 명시
6. 이어가는 작업이면 → 기존 chatlog에 Round N+1 추가
7. 작업 끝나면 `70_OPEN_QUESTIONS/` 에 새 질문이 생겼는지 검토 후 추가

---

## 절대 금지

- 자식 프로젝트 파일을 이 디렉토리로 **복사·이동하지 않는다** (참조만)
- MathTelling의 chatlog 방식을 HighSchool에 강제 이식하지 않는다 (Q03 미결)
- 학생 본인이 만든 글·앱은 절대 자동 수정 없음 (자식 프로젝트의 원칙을 그대로 상속)
