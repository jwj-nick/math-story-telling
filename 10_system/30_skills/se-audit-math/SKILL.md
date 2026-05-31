---
name: se-audit-math
description: 수학 문제·풀이·정답의 정확성을 검증한다. NCC가 직접 풀이 전개 후 Wolfram Alpha MCP로 독립 확인. 호출 예시 — "/se-audit-math unit01 basic_app.html", "/se-audit-math Q3".
---

# /se-audit-math — 수학 정확성 검증 Skill

## 역할
생성된 수학 문제와 정답이 올바른지 검증.
NCC가 직접 풀이를 전개한 후 Wolfram Alpha MCP로 독립 확인.
동일 모델 self-audit의 편향을 최소화.

> 도입 배경: Unit 1 제작 중 self-audit으로 잡지 못한 수학 버그 3건 발생.

---

## 인자 형태

```
/se-audit-math [파일경로]
/se-audit-math unit01 basic_app.html
/se-audit-math 50_units/01_소인수분해/problems/basic_app.html
/se-audit-math Q3   # 특정 문제번호
```

---

## 실행 절차

### 1. 대상 파일/문제 읽기
HTML 파일 또는 MD 파일에서 문제 목록, 정답, 풀이 추출.

### 2. NCC 독립 풀이
각 문제를 **처음 보는 것처럼** 독립적으로 풀이 전개:
- 풀이 과정 단계별 전개 (숫자 계산 포함)
- 도출한 답과 파일의 정답 비교
- 보기(선택지)가 있으면: 정답 보기 확인 + 오답 보기도 왜 틀렸는지 확인
- 단위·표기가 APP_PRINCIPLES.md 기준과 일치하는지 확인

### 3. Wolfram Alpha MCP 독립 검증
- 계산이 포함된 문제: Wolfram Alpha로 계산식 검증
- 수식 풀이 결과 확인 (인수분해, 방정식, 약수 등)
- MCP 사용 불가 시: NCC 풀이 2회 반복으로 대체 (이 경우 chatlog에 명시)

참조: `10_docs/15_wolfram_alpha_guide.md`

### 4. 판정

| 판정 | 기준 | 처리 |
|---|---|---|
| Pass | NCC 풀이 + Wolfram 모두 일치 | 문제 확정 |
| Warn | 계산 과정 불명확, 해석 여지 있음 | **chatlog 메모 후 Pass 처리. 재풀이 금지** |
| Fail | 정답 오류 또는 문제 오류 확인 | **1회 수정 후 종료. 재검토 금지** |

## ⚠️ 1-shot 원칙 (필수)

- 각 문제는 **1회 NCC 풀이 + 1회 Wolfram 검증**으로 종료
- 동일 문제에 Wolfram MCP 2회 이상 호출 금지 (rate limit·시간 절약)
- 수정 후 **재검산 금지** — 수정한 정답 자체가 새 검증을 거치지 않음 (수정 시 풀이 명확히 chatlog에 기록)
- 모든 문제를 한 번에 batch 검증, 발견된 모든 오류를 일괄 수정

### 5. 보고 형식

```
## /se-audit-math 결과: [파일명]

| 문제번호 | NCC 풀이 결과 | Wolfram 결과 | 파일 정답 | 판정 |
|---|---|---|---|---|
| Q1 | 12 | 12 | 12 | ✅ Pass |
| Q2 | 6 | 6 | 7 | ❌ Fail — 정답 수정 |

### 수정 완료
- Q2: 정답 7 → 6 수정 (풀이: ...)

### 최종 판정: Pass / Fail [N건 수정]
```

---

## 주의

- 풀이를 보지 않고 문제만 보고 독립 풀이할 것
- "아마 맞겠지"로 넘기지 말 것 — 반드시 계산 전개
- 중1 범위 벗어난 풀이 방식 사용 금지
- 수식 검증 불가 케이스 (서술형 판단 문제 등)는 chatlog에 명시 후 Pass 처리
