<!-- 10_docs/15_wolfram_alpha_guide.md -->
# Wolfram Alpha MCP — 도입 가이드

> MathTelling 프로젝트에서 수학 검증 보조 도구로 사용.
> 마지막 업데이트: 2026-05-09

---

## 1. Wolfram Alpha란?

Wolfram Alpha는 수식 계산, 수학 풀이, 데이터 분석을 처리하는 **계산 지식 엔진**이다.
일반 검색 엔진과 달리 웹페이지를 찾는 게 아니라 **직접 계산·풀이 결과를 반환**한다.

예시:
- `factor 360` → 소인수분해 결과
- `solve 3x + 5 = 20` → 방정식 풀이
- `gcd(48, 36)` → 최대공약수
- `lcm(12, 18, 24)` → 최소공배수

---

## 2. 왜 이 프로젝트에서 사용하는가?

### 문제

NCC(Claude)가 수학 문제를 만들고 NCC가 검증하면 **동일 모델, 동일 편향**이 발생한다.
Unit 1 제작 시 self-audit으로 잡지 못한 수학 오류 3건이 실제로 발생했다.

### 해결책

`/ncc_audit_math` Skill 실행 시 Wolfram Alpha MCP로 **독립적으로** 계산 결과를 확인한다.

```
NCC 풀이 결과 = 6
  ↓
Wolfram Alpha 검증: factor(48) → 2^4 × 3 → 정답 6 ✅
  ↓
두 결과 일치 → Pass
두 결과 불일치 → Warn/Fail
```

---

## 3. Wolfram Alpha MCP 설정 방법

### MCP란?
MCP(Model Context Protocol)는 Claude Code가 외부 도구와 연결하는 방식이다.
Wolfram Alpha MCP는 Claude가 Wolfram Alpha API를 직접 호출할 수 있게 해준다.

### 설정 절차

**Step 1: API 키 발급**
- https://developer.wolframalpha.com 에서 무료 계정 생성
- "Get an AppID" 클릭 → App 이름 입력 → API 키 발급
- 무료 플랜: 월 2,000회 호출 가능

**Step 2: Claude Code 설정**
Claude Code 설정 파일에 MCP 추가:

```json
// .claude/settings.json 또는 ~/.claude/settings.json
{
  "mcpServers": {
    "wolfram": {
      "command": "npx",
      "args": ["-y", "wolfram-mcp"],
      "env": {
        "WOLFRAM_APP_ID": "YOUR_APP_ID_HERE"
      }
    }
  }
}
```

**Step 3: 확인**
Claude Code를 재시작 후 `wolfram` 도구가 사용 가능한지 확인.

> **현재 상태**: 설정 필요. Nick이 API 키 발급 후 위 설정 추가.

---

## 4. 이 프로젝트에서의 활용처

| 활용 상황 | 입력 예시 | 목적 |
|---|---|---|
| 소인수분해 검증 | `factor 360` | 정답 독립 확인 |
| 최대공약수 | `gcd(48, 36)` | 계산 결과 확인 |
| 최소공배수 | `lcm(12, 18)` | 계산 결과 확인 |
| 일차방정식 | `solve 2x-3=7` | 풀이 결과 확인 |
| 약수 목록 | `divisors 24` | 약수 목록 확인 |
| 거듭제곱 | `2^5` | 단순 계산 확인 |

---

## 5. 무료 플랜으로 충분한가?

| 항목 | 무료 플랜 | 유료 플랜 |
|---|---|---|
| 월 호출 횟수 | 2,000회 | 무제한 |
| 결과 형식 | 텍스트 위주 | 이미지, 단계별 풀이 포함 |
| 이 프로젝트 적합성 | ✅ 충분 | 불필요 |

단원당 문제 약 20~30개, 단원 4개 = 80~120회 호출 예상.
무료 2,000회로 충분히 커버 가능.

---

## 6. Wolfram Alpha MCP 사용 불가 시 대처

MCP 미설치 또는 API 키 미설정 시 `/ncc_audit_math`의 동작:

1. chatlog에 "Wolfram Alpha MCP 미사용 — NCC 풀이 2회 반복으로 대체" 명시
2. 동일 문제를 다른 방식(다른 숫자, 역방향 검증)으로 2회 풀어 교차 확인
3. 수학 버그 위험이 높은 문제는 chatlog에 "Nick 수동 확인 권고" 표시

---

## 7. 대체 도구 비교

| 도구 | 특징 | MathTelling 적합성 |
|---|---|---|
| **Wolfram Alpha** | 수식 계산 특화, API 제공 | ✅ 최적 |
| Desmos | 그래프 시각화 전용 | ⚠️ 계산 검증 불가 (그래프용으로 따로 활용 가능) |
| Khan Academy | 교육용 설명 콘텐츠 | ❌ API 없음, 계산 검증 불가 |
| Python (sympy) | 코드 기반 계산 검증 | ⚠️ 가능하지만 설정 복잡 |
| WolframScript | 로컬 Wolfram 실행 | ❌ 유료, 설치 복잡 |

---

*관련 Skill: `/ncc_audit_math` — 수학 정확성 검증 시 Wolfram Alpha 호출*
