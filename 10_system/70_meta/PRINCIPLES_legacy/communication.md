# 40_PRINCIPLES/communication — NCC ↔ Nick 소통 원칙

> Q03 응답으로 2026-05-12에 확정.

## C1. chatlog 원칙 (A) — 모든 작업의 기본

- **NCC는 모든 의사결정·진행을 chatlog 파일에 기록**한다
- 위치: `00_LearningSystem/00_chatlog/YYMMDD_R<N>_주제.md`
- 형식:
  ```markdown
  <!-- 260512_R1_주제.md -->
  # Round 1 — 라운드 제목
  
  ## Round 0 회고
  ## NCC 분석
  ## 실행 항목
  
  > (Nick): (응답 영역)
  ```
- 한 주제 = 한 파일. 시간순으로 Round N 누적

## C2. Nick의 응답 위치는 자유

- Nick은 편의에 따라:
  - chatlog 파일에 직접 `(Nick):` 추가
  - 또는 자식 프로젝트의 .md 파일 어디든 인라인 답변
  - 또는 chat window에서 짧게
- **NCC는 어디에 받든 chatlog에 옮겨 통합 기록**한다 (정본은 chatlog)

## C3. 화면 출력 최소

- chat window에는 작업 시작·끝·핵심 질문만
- 본문·분석·결정은 모두 chatlog에 (Nick이 나중에 검색 가능하게)

## C4. 자식 프로젝트의 기존 소통 방식

- MathTelling: `00_project_hub/chatlog/` 라운드 기반 (현행 유지, NCC 동일 원칙)
- HighSchool 2604: `(Nick)` / `(Claude)` 인라인 (현행 유지)
- 두 자식 프로젝트의 작업 결과·결정은 **이 메타 chatlog에도 회고 기록**

## C5. 세션 시작 시

NCC는 새 세션에서:
1. `00_chatlog/` 최근 파일 5개 훑어보기 (진행 중 라운드 있나)
2. 자식 프로젝트의 `(Nick)` 미처리 항목 스캔
3. 이번 작업이 새 주제이면 → 새 chatlog 파일 생성, chat window에 파일명 명시
4. 이어가는 작업이면 → 기존 chatlog에 Round N+1 추가

## C6. (Nick) 미처리 우선

- 새 세션 진입 시: 자식 프로젝트의 todo/issue/study .md 스캔
- 답하지 않은 `(Nick)` 항목 있으면 그것부터 처리

## C7. 학생이 직접 사용하게 될 때 (L2 이후)

- Q04 응답: 한동안 L0 유지, L2 진입은 Nick이 control
- L2 진입하면: 학생용 chat window 출력 톤 다듬기 (어휘·길이·아이콘 비중)
- 안전장치 (자료 신뢰도·자율 시간·디바이스 시간) 별도 설계 필요

## C8. NCC ID

- NCC = Nick's Claude Co-worker
- chatlog에서 화자: `NCC` 또는 `(Claude YYYY-MM-DD)`
- prefix `se_` 도 NCC 일부분이 아니라 자식 이름 마커 (Q07)
