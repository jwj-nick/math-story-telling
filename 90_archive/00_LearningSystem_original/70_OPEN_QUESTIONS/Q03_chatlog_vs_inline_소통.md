# Q03 — chatlog 라운드 vs (Nick)/(Claude) 인라인 — 통일할 것인가?

> 상태: 🟡 두 방식 공존 중. 통일 vs 공존 결정 필요.

## 두 방식

### A. chatlog 라운드 (MathTelling)

- 위치: `00_project_hub/chatlog/YYMMDD_주제.md`
- 형식:
  ```
  # Round 0 — Commission Brief
  ...
  > (Nick):
  
  # Round 1 — ...
  ```
- Claude는 화면 출력 최소, 모든 내용을 파일에 append
- 한 주제 = 한 chatlog 파일

### B. (Nick) / (Claude) 인라인 (HighSchool)

- 위치: 어떤 .md든 (todo.md, study.md, 02_prep_*.md 등)
- 형식:
  ```markdown
  ## 다음 액션
  1. 채점 결과 받기
  2. (Nick) Q14 배점 확인 — [5.3점] 맞음
     → (Claude 2026-04-27) issue.md 해당 항목 closed
  ```
- 자유로운 위치, 자유로운 시점

## 비교

| | chatlog (A) | inline (B) |
|---|---|---|
| 흐름 추적 | 시간순 명확 | 흐름이 파일별 분산 |
| 결정 기록 | 라운드 단위 명확 | 파일 위치별 명확 |
| 검색 | "이 주제 어떻게 됐지" → 한 파일 | "이 항목 결정됐나" → 위치 빠르게 |
| 진입 비용 | 새 파일 만들어야 함 | 그냥 한 줄 추가 |
| 적합한 작업 | 단원 파이프라인처럼 긴 작업 | 산발적 결정·수정 요청 |

## (NCC 가설)

- 작업 종류에 따라 적합한 방식이 다름
- 강제 통일하면 한쪽이 불편해짐
- 단, **메타 시스템(이 디렉토리)** 내부에서는 어떤 방식을 쓸지 결정 필요

## NCC 제안

| 작업 종류 | 추천 방식 |
|---|---|
| 단원 / 학기 단위 큰 작업 | A (chatlog) |
| 시험·수행평가 단발 도우미 | B (inline) |
| 메타 시스템 의사결정 (이 디렉토리) | B (inline) — Q01 같은 질문 파일 안에서 |

자식 프로젝트는 현행 유지 (MathTelling = A, HighSchool = B).

## (Nick) 응답

> (Nick): 항상 A 가 원칙임. 다만 inline 으로 내가 답변을 줄 때도 있음. 그래도 NCC 는 chatlog 기록해두길 

---

## 결정 후 적용
- 40_PRINCIPLES.md "C. 소통" 섹션 갱신
- 각 자식 프로젝트 CLAUDE.md에 명시
