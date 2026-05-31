---
name: se-audit-app
description: HTML 앱이 APP_PRINCIPLES.md를 따르는지 검토하고 위반 항목을 수정한다. app-reviewer Agent를 대체하는 Skill. 호출 예시 — "/se-audit-app 50_units/01/app/concepts.html", "/se-audit-app unit01 전체".
---

# /se-audit-app — HTML 앱 품질 검토 Skill

## 역할
생성된 HTML 앱이 `APP_PRINCIPLES.md` 기준을 충족하는지 항목별로 검토하고,
단순 위반은 즉시 수정, 구조적 변경이 필요한 것은 chatlog에 보고.

> 구 `app-reviewer` Agent의 역할을 이 Skill이 대체함.

---

## 인자 형태

```
/se-audit-app [파일경로]
/se-audit-app [단원번호] [범위: 전체|app|problems]
/se-audit-app 50_units/01_소인수분해/app/concepts.html
/se-audit-app unit01 전체
```

---

## 실행 절차

### 1. 기준 파일 읽기
`APP_PRINCIPLES.md` 읽기 (최신 기준 확인)

### 2. 대상 파일 결정
- 파일 경로 명시 시: 해당 파일만
- `unit01 전체` 형태: `50_units/NN/app/*.html` + `50_units/NN/problems/*.html` 전체
- `unit01 app`: `50_units/NN/app/*.html`만
- `unit01 problems`: `50_units/NN/problems/*.html`만

### 3. 항목별 체크리스트 검토

APP_PRINCIPLES.md의 검토 항목:
- [ ] KaTeX 수식 렌더링 설정 올바름
- [ ] 정답/풀이가 탭 전환 또는 details로만 공개
- [ ] prob 필드에 문제만 (슬라이더·입력 금지)
- [ ] why 필드가 정답판에만 표시
- [ ] 모바일 뷰포트 설정
- [ ] 색상·폰트 원칙 준수
- [ ] 단원 고유 기능 (체 등) APP_PRINCIPLES 예외 기준 충족
- [ ] 수식 표기 규칙 (×, ÷, 단위 표기 등)

### 4. 판정

| 판정 | 기준 | 처리 |
|---|---|---|
| Pass | 모든 항목 통과 | 완료 보고 |
| Warn | 권고 수준 (필수 아님) | chatlog에 메모, 진행 |
| Fail-단순 | 텍스트·속성 수정으로 해결 가능 | **1회 일괄 수정 후 종료. 재감사 사이클 금지** |
| Fail-구조 | 레이아웃·기능 구조 변경 필요 | chatlog에 보고 후 Nick 확인 대기 |

## ⚠️ 1-shot 원칙 (필수)

- 모든 위반 사항을 **한 번에 발견·기록·수정**한다
- 수정 후 **재감사 사이클 금지** — "고쳐서 다시 검토" 패턴 금지
- 동일 파일을 audit 목적으로 2회 이상 Read 금지 (Edit 결과 신뢰)
- 재감사가 정말 필요한 본질적 변경(레이아웃 재설계 등)은 Fail-구조로 분류하여 Nick에 위임

### 5. 보고 형식

```
## /se-audit-app 결과: [파일명]

### Pass 항목
- KaTeX 설정 ✅
- ...

### 수정 완료 (Fail-단순)
| 항목 | 수정 전 | 수정 후 |
|---|---|---|

### Nick 확인 필요 (Fail-구조)
| 항목 | 문제 | 권장 |
|---|---|---|

### 최종 판정: Pass / Warn / Fail-구조
```
