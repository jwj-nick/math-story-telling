<!-- 00_project_hub/plan/unit_walkthrough_batch_plan.md -->
# Unit 02~13 — Walkthrough 일괄 작업 계획

> 생성: 2026-05-12
> 목적: Unit 01에서 확립한 패턴을 나머지 12개 단원에 일괄 적용
> 작업 주체: Sonnet 기반 Agent (병렬 X — 단원당 순차 진행 권장, 단원 내부 일괄)

---

## 0. 작업 컨텍스트 (compact 후에도 유지해야 할 핵심)

### Unit 01 완성 산출물 (참고 모델)
모든 단원이 다음 구조를 따라야 함:
```
50_units/NN_단원명/
├── index.html          ← 단원 허브, 백링크 + 카드 그리드
├── story.html
├── concepts.html
├── problems/
│   ├── basic_app.html
│   ├── types.html      ← ⭐ navigation 페이지 (현재 .md만 있음, 신규 필요)
│   ├── type_01~07_app.html (7개)
│   ├── deep_*.html (2~4개)
│   └── walk_NN_HX.html (★ 신규, H 문제당 1개) ← ⭐ 일괄 작업 대상
│   └── (참조용 .md 파일들 유지)
```

### 확립된 walkthrough 패턴
**캐노니컬 참조 파일**: `50_units/01_소인수분해/problems/walk_07_H2.html`

구조 (6 페이지):
- **Page 0**: 문제 원문 + think-box ("스스로 풀어봐요"), 정답 절대 노출 X
- **Page 1~N**: 단계별 풀이 (보통 3~5단계)
  - 각 페이지: page-label + page-title + page-why (이탤릭 보라 박스)
  - card → derive-box (도출 결과) → 필요 시 think-box / warn-box
- **Page ★ (마지막)**: 정답 (큰 그라데이션 박스) + 전체 흐름 5단계 요약 + 함정 warn-box + 다음 학습 링크

**디자인 토큰** (모든 walkthrough 동일):
- 색상: primary `#4361EE`, deep accent `#7c3aed`, 배경 `#eef2ff`
- 폰트: `Malgun Gothic`, max-width `700px`
- KaTeX CDN, 진행 도트 sticky top, no-cache 헤더 자동 적용 (dev 서버)

**필수 요소 (Nick 확정)**:
- 모든 페이지에 `.legend` 박스 — 영문 약자(gcd/lcm/`d|n` 등) 한국어 병기
- `gcd` → "최대공약수(gcd)" 또는 그 반대 병기
- `$d \mid n$` 정수론 기호 → 우선 텍스트로 "$d$는 $n$의 약수" 풀어쓰기, 보조로 기호
- 따뜻한 말투: "~해요", "~봐요"

---

## 1. 단원별 작업 범위

각 단원별 작업 항목 (4가지):

### A. types.html 신규 생성 (12개)
- 기존 `types.md` 내용을 HTML 카드 그리드로 변환
- 7개 유형 카드 + 깊이 탐구 deep_*.html 카드 + 단계별 풀이 walk_*.html 링크
- Unit 01의 types.html 디자인 그대로 사용 (walk-section/walk-group/walk-link 클래스 등)

### B. index.html 링크 업데이트 (12개)
- 카드 그리드의 "유형 목록" 링크: `problems/types.md` → `problems/types.html`
- 카드 제목: "유형 목록" → "유형별 연습 · 깊이 탐구" (Unit 01과 동일)

### C. walkthrough HTML 신규 생성 (단원당 약 18개, 총 약 216개)
- 각 유형의 H 문제 3개에 대해 walk_NN_HX.html 생성
- 단원의 type_NN_app.html 파일에서 H 문제 원문·정답 추출 → 단계별 풀이 작성
- 유형 1(소수/합성수 판별류)은 단원에 따라 스킵 결정:
  - **Unit 01**: 유형 1 스킵 → 6 유형 × 3 H = **18개** (이미 완료)
  - **Unit 02~13**: 단원별 첫 번째 유형이 "L 위주 기초"라면 스킵, 그렇지 않으면 포함
  - 유형 수가 7과 다를 수 있음 → 단원별 실제 H 문제 수 확인 후 작업
- 예상 총량: 12 × 약 18 = **약 216개 walkthrough**

### D. (선택) deep_*.html 링크 추가
- 각 deep_*.html에 해당 유형 walk_NN_HX 링크 추가 가능 (현재는 types.html에서 진입)
- 우선순위 낮음 — 사용자 요청 시에만

---

## 2. 진행 순서 (병렬 금지, 순차 권장)

```
Unit 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13
```

단원 1개 작업 흐름 (Agent 1회 호출):
1. 해당 단원 `problems/type_NN_app.html` 모두 Read → H 문제 원문 + 정답 추출
2. `walk_07_H2.html` 템플릿 Read (참조)
3. **단원당 약 18개 walkthrough HTML 일괄 작성** (Edit/Write)
4. 해당 단원 `types.html` 신규 생성 (Unit 01 types.html 참고)
5. 해당 단원 `index.html`에서 types.md → types.html 링크 수정
6. 완료 chatlog 1줄 기록

단원 1개 예상 시간: 1~2시간 (Unit 01 batch agent가 18개 + types.html을 약 17분에 완료)

---

## 3. Sonnet vs Opus — 모델 선택 권장 (Nick 질문에 대한 의견)

### 결론: **Sonnet 4.6으로 충분**

### 근거

**Sonnet으로 충분한 이유**
1. **패턴 확립됨**: walk_07_H2.html이 캐노니컬 참조. Agent는 패턴 복제 + 콘텐츠 치환만 수행.
2. **수학 수준 중1**: Sonnet은 중1 수학(소인수분해/방정식/도형 등)을 충분히 정확하게 다룸.
3. **단계 분해 — 일정 패턴**: H 문제 단계는 보통 3~5단계로 매우 정형화됨.
4. **검증 자동화 가능**: 정답은 원본 `type_NN_app.html`에 이미 있음 → 일치 확인만.
5. **속도/비용**: Sonnet이 Opus 대비 2~3배 빠르고 4~5배 저렴. 216개 × 단가 차이 크게 누적됨.

**위험 요소**
- 미묘한 수학 실수: Sonnet도 단계별 풀이에서 소수점 자리 등 미스 가능
- 일관성: 216개 파일이 톤·디자인·legend 등 일관해야 함

**위험 완화책**
- 캐노니컬 참조 walk_07_H2.html 강제 (Agent 첫 단계에서 반드시 Read)
- 각 walkthrough 정답이 원본 type_NN_app.html과 일치하는지 확인 (Agent 자체 검증)
- 단원 완료 후 Nick 샘플링 검토 (단원당 3~4개 무작위 점검 권장)
- Wolfram MCP는 의심 시에만 호출 (자동 호출 X — 토큰·시간 절약)

**Opus가 더 좋을 케이스 (이 작업엔 해당 안 됨)**
- 패턴이 없거나 새 디자인 결정 필요한 경우
- 깊은 수학적 통찰이 필요한 경우 (대학 수학 등)
- 모호한 자연어 명세 해석이 필요한 경우

### 모델 호출 권장
- **단원 작업**: Sonnet 4.6 Agent
- **검증 (의심 시)**: Sonnet 4.6 + ncc_audit_math (Wolfram MCP)
- **메타 결정 (다음 단원 패턴 등)**: 이 대화의 메인 Claude (현재 Opus 4.7)

---

## 4. 단원별 인물·핵심 메모 (compact 시 자동 압축 방지)

| Unit | 인물 | 핵심 주의사항 |
|---|---|---|
| 02 | 브라마굽타 | 절댓값 `|x|` 기호 — legend에 추가. 음수·양수 부호 처리 함정 |
| 03 | 알콰리즈미 | 곱셈기호 생략 (3x = 3·x), 동류항 분류 — 표기 함정 |
| 04 | 디오판토스 | 이항 부호 반전 — 가장 흔한 실수, warn-box 필수 |
| 05 | 데카르트 | 좌표 표기 P(a,b), 사분면 로마자 (Ⅰ~Ⅳ) |
| 06 | 데카르트 (Unit 5 연계) | y=a/x, a=-2 → y=-2/x 표기 변환 (★ 학습자 결정적 사례) |
| 07 | 유클리드 | 도형 기호 6종 (`AB`, `→AB`, `−AB`, `∠`, `⊥`, `∥`) — legend 필수 |
| 08 | 유클리드 (Unit 7 연계) | 합동 `≡` 기호, SSA 반례 함정 |
| 09 | 가우스 | 다각형 내각합·외각합 공식 (n-2)·180° |
| 10 | 아르키메데스 | π 표기, 호·현 비례 함정 (★) |
| 11 | 케플러 | V-E+F=2, 정다면체 두 조건, 수직 단면 vs 축단면 |
| 12 | 카발리에리 | 1/3 빼먹기, h vs l (모선), 반구 평면원, 단위 cm² vs cm³ |
| 13 | 나이팅게일 | 도수분포·히스토그램·상대도수·누적도수 — 데이터 표 SVG 자주 등장 |

---

## 5. compact 후 첫 작업 메시지 템플릿

```
unit-walkthrough-batch 시작.

참조:
- 계획: 00_project_hub/plan/unit_walkthrough_batch_plan.md
- 템플릿: 50_units/01_소인수분해/problems/walk_07_H2.html
- types.html 모델: 50_units/01_소인수분해/problems/types.html

Unit 02부터 순차 진행.
각 단원: Sonnet Agent 1회 호출 → walkthroughs + types.html + index.html 링크 수정.
단원 완료 시 마스터 플랜에 ✅ 표시 후 다음 단원으로.

이 메시지를 받으면:
1. 위 계획 파일을 Read
2. Unit 02 Agent 호출 (Sonnet)
3. 완료 보고 후 Unit 03로 자동 진행
```

---

## 6. 완료 체크리스트 (각 단원당)

- [ ] H 문제 N개 추출 완료 (단원별 변동)
- [ ] walk_NN_HX.html N개 생성 완료 (캐노니컬 디자인 준수)
- [ ] types.html 신규 생성 (walk-section 포함)
- [ ] index.html에서 types.md → types.html 링크 수정
- [ ] 모든 walkthrough 정답이 원본 type_NN_app.html과 일치
- [ ] legend 박스 모든 페이지에 존재
- [ ] 단원 chatlog 기록 1줄 (선택)
- [ ] master_plan.md에 walkthrough 상태 업데이트

---

## 7. 미해결 결정 사항 (compact 시 잃지 말 것)

- **유형 1 walkthrough 포함 여부**: Unit 01에서는 스킵. 단원별로 판단 (첫 번째 유형이 정의·식별 위주면 스킵). Agent가 스스로 판단하거나 일괄 "스킵" 정책.
- **deep_*.html에 walkthrough 링크 추가**: 우선순위 낮음, 사용자 요청 시
- **삭제할 것**: 없음 (기존 types.md, Q*_source.md는 참조용으로 유지)

---

## 8. 사후 작업 (Unit 02~13 완료 후)

- master_plan.md 최종 업데이트 (13단원 모두 walkthrough 완비)
- unit-review skill v0.3 업데이트 (다음 단원 점검 사이클용)
- 배포 가이드: types.html, walk_*.html, deep_*.html 모두 GitHub Pages 푸시 대상
- /unit-review skill로 사용자 검수 시작
