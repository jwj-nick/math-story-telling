---
name: se_math_practice
description: 중1 수학 연습 문제를 3카테고리(쉬운/비슷한/응용) x 3문제씩 생성한다. 호출 예시 — "Q3 연습문제", "/se_math_practice Q3", "/se_math_practice Q3 unit01".
---

# se_math_practice — 중1 수학 연습 문제 생성 스킬

## 인자 형태
```
/se_math_practice               # 인터랙티브
/se_math_practice Q3            # 기본
/se_math_practice Q3 unit01     # 단원 명시
```

## 절차

### 1. 준비
- 해당 문제의 오답노트 .md 읽기 (없으면 40_BaseDocs에서 개념 직접 읽기)
- 중1 범위 확인

### 2. 연습 문제 생성 — 3카테고리 x 3문제

| 카테고리 | 의미 |
|---|---|
| L (쉬운) | 핵심 개념 하나씩 분리 연습 |
| M (비슷한 레벨) | 같은 사고 흐름, 다른 형태 |
| H (응용) | 확장, 융합, 역방향 |

각 문제 필수 포함:
1. **문제 번호** (L1/L2/L3, M1/M2/M3, H1/H2/H3)
2. **[연결 개념]** 태그
3. **문제 본문** (KaTeX 수식)
4. **풀이 전략** (힌트 수준)
5. **정답**
6. **왜 이 문제인가** (정답판에 표시)
7. **단계별 힌트** (`<details>` 접기 3단계)

### 3. 파일 저장

**파일 1**: `50_units/NN_단원명/problems/Q<번호>_practice.md`
**파일 2**: `50_units/NN_단원명/problems/Q<번호>_practice_app.html`

**APP_PRINCIPLES.md 준수:**
- prob 필드: 문제만, 슬라이더 금지
- why: 정답판에만 표시
- 정답·풀이는 탭 전환으로만 공개

### 4. 보고
> Q3 연습문제 → `50_units/01_소인수분해/problems/Q3_practice.md` + `Q3_practice_app.html` 생성 완료. L3 / M3 / H3.

## 문제 생성 원칙
- 수학적 정확성 최우선 — 검산 후 기재
- 단순 숫자 변환 금지 — 각 문제는 다른 사고 요구
- **중1 범위** — 고등 내용 제외
- 카테고리 내 3문제는 서로 다른 각도
