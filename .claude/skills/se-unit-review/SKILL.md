---
name: se-unit-review
description: 단원 1개를 Nick과 함께 체계적으로 둘러보고 갭(missing/부적합)을 발견·기록하고 어떤 skill로 보완할지 결정한다. 라운드 기반 대화로 진행. 호출 예시 — "/se-unit-review unit01", "/se-unit-review 01_소인수분해".
---

# /se-unit-review — 단원 상세 리뷰 Skill (v0.1, draft)

> **상태**: 초안. Unit 01 리뷰 진행 중 채워나가는 중.
> Nick과의 대화 라운드마다 이 SKILL.md 업데이트.

## 역할
완성된(또는 진행 중인) 단원 1개에 대해:
1. 디렉토리 구조 정합성 확인
2. 각 페이지를 차례로 둘러보며 Nick 의견 수집
3. 발견된 갭·개선점을 chatlog에 기록
4. 갭 종류별로 어떤 skill/agent를 호출할지 결정
5. 패턴 발견 시 모든 단원에 적용할 일괄 작업으로 정리

---

## 인자 형태

```
/se-unit-review [단원번호 또는 단원명]
/se-unit-review unit01
/se-unit-review 01_소인수분해
```

---

## 단원의 이상적 구성 (Template)

리뷰 시 이 템플릿과 대조:

| # | 파일/경로 | 역할 | 필수 | 형식 |
|---|---|---|---|---|
| 1 | `index.html` | 단원 허브, 모든 페이지로의 진입점 | ✅ | HTML |
| 2 | `story.html` | 인물 서사 인터랙티브 | ✅ | HTML |
| 3 | `concepts.html` | 개념 탐구 (슬라이더, 다이어그램) | ✅ | HTML |
| 4 | `problems/basic_app.html` | 기본 문제 8~10개 (단원 전체 커버) | ✅ | HTML |
| 5 | `problems/types.html` | 유형 목록 landing 페이지 | ✅ | HTML |
| 6 | `problems/type_01~07_app.html` | 유형별 연습 (L/M/H × 3) | ✅ | HTML |
| 7 | `problems/deep_*.html` | 깊이 탐구 (관련 유형 통합) | ✅ | HTML |
| 보조 | `story/unitNN.md` | 인물 서사 텍스트 (참조용) | ⬜ | MD |
| 보조 | `problems/Q*_source.md` | 기본문제 출처 (참조용) | ⬜ | MD |

**원칙**: 학습 흐름 중 보이는 것은 모두 HTML. MD는 참조용으로만 디렉토리에 남김.

---

## 진행 절차

### Phase A: 상태 점검 (자동)
- 디렉토리 inventory 생성
- 위 템플릿과 대조 → 누락 파일 목록
- index.html의 링크 grep → 노출되지 않은 페이지 식별
- 각 페이지 백링크 확인 (← 중1 수학 홈, ← 단원으로 등)

### Phase B: 인터랙티브 리뷰 (Nick과 라운드 기반)
순서대로 둘러보면서 의견 수집. 각 단계 chatlog에 기록.

1. `index.html` — 카드 구성, 디자인, 모든 페이지 노출 여부
2. `story.html` — 톤, 길이, 학습자 적합성, 수학 연결
3. `concepts.html` — 인터랙티브 적절성, 인지 부담
4. `problems/basic_app.html` — 커버리지, 난이도
5. `problems/types.html` — 유형 분류 적절성, 시각화
6. 각 `type_NN_app.html` — 9문제 구성, L/M/H 비율
7. 각 `deep_*.html` — 통합 적절성, 깊이

### Phase C: 갭 정리 및 보완 작업 배정
chatlog에 정리:
- 누락 파일/링크: 어떤 skill로 보완? (아래 매핑 참조)
- 디자인 개선: Edit 직접 or `/se-audit-app`
- 수학 오류: `/se-audit-math`
- 톤·내용 부적합: 해당 skill 재호출

### Phase D: 패턴 추출 (선택)
1단원 리뷰에서 반복 패턴 발견 → 전 단원 일괄 적용 작업 기획.

---

## 갭 종류 → 담당 skill/agent 매핑

| 갭 | 담당 |
|---|---|
| `types.html` 없음 (현재 .md만 있음) | Edit (신규 HTML 생성 — 단순) |
| `index.html`에 링크 누락 | Edit 직접 |
| `type_NN_app.html` 없음 | `/se-math-practice` |
| `deep_*.html` 없음 | `/se-type-explorer` |
| `story.html` 없음 | 영상 1-narrative.md(se-people-narrate) + 영상 임베드 → HTML (orchestrator) |
| `concepts.html` 없음 | se-unit-orchestrator (전용 skill 없음) |
| 수학 오류 | `/se-audit-math` |
| 디자인 위반 | `/se-audit-app` |
| 개념 수준 부적합 | `/se-audit-concept` |
| 문제 커버리지 미흡 | `/se-audit-problem` |
| 스토리 부적합 | `/se-audit-story` |

---

## 리뷰 진행 중 발견된 패턴 (누적)

### 2026-05-12 — Unit 01 리뷰

#### 구조 갭
- **갭 1**: `types.md`는 학습 흐름에 노출 안 됨 (raw markdown). `types.html` 신규 필요.
- **갭 2**: `index.html`이 `type_NN`/`deep_*` 페이지로 직접 링크 누락 → `types.html` 카드로 진입하도록 정리.
- **갭 3**: 참조용 `.md` (types.md, Q*_source.md)는 디렉토리에 유지하되 앱에선 노출 X.

#### 심화(deep) 앱의 본질적 미스 — **중요**
- **현재 deep_*.html의 문제**: 한 페이지에 정답 토글들이 나열 → 학생이 단계별로 사고할 흐름 없음
- **원래 의도**: `se-math-error-note` skill + `APP_PRINCIPLES.md` page-0~N 패턴
  - 학생이 page-0 (문제만 보임) → 스스로 시도 → page-1 (1단계) → ... → page-N (정답)
  - 각 단계마다 "왜 이 단계인가" 명시
- **해결 (Solution B)**: deep_*.html은 navigation/요약 유지 + 각 H 문제마다 별도 `walk_*.html` 단계별 풀이 앱
- **샘플**: `walk_07_H2.html` (2026-05-12 생성, Nick 검토 진행 중)

#### Walkthrough 페이지 작성 원칙 (v0.2 신규)
- 페이지 구조: page-0 (문제) → page-1~N (단계별, 각 단계마다 "왜 이 단계?") → page-★ (정답+요약)
- 상단 진행 도트로 페이지 이동 + 점프 가능
- **용어 노트 박스 (legend) 모든 페이지에 항상 표시**
  - `gcd`, `lcm` 등 영문 약자는 항상 "최대공약수", "최소공배수" 등 한국어 병기
  - $d \mid n$ 같은 정수론 기호는 첫 등장 시 "$d$는 $n$의 약수"라는 텍스트로 풀어쓰고, 보조로 기호 표시
  - 한국 중·고 교과서에 등장하지 않는 영문 약자/기호는 자주 노트로 상기시킬 것
- think-box (파랑): 학생에게 "잠깐, 손으로" 격려하는 박스
- warn-box (노랑): 흔한 실수는 별도 섹션이 아니라 **해당 단계에 인라인**
- 정답은 page-★ (마지막 페이지)에만 노출 (한 클릭 다 보이기 금지)

#### Walkthrough 일괄 작업 계획
- 대상: 13단원 × 약 18개 H 문제 = **약 234개 walk_NN_H*.html** (추정)
- Unit 01: 7유형 중 H 있는 6유형 × 3 = **약 18개**
- 패턴 확정 후 차후 일괄 진행

---

## chatlog 기록 형식

```markdown
# /se-unit-review unitNN — 라운드 N

## 둘러본 페이지
[페이지명]

## Nick 의견
[원문 또는 요약]

## 액션 아이템
- [ ] [구체적 변경] — 담당: [skill명 or Edit]

## 다음 라운드
[다음 볼 페이지]
```

---

## 변경 이력 (skill 자체)
- v0.1 (2026-05-12): Unit 01 리뷰 시작 시 초안 생성
