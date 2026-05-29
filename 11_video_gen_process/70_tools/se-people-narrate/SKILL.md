---
name: se-people-narrate
description: 영상 제작 시스템의 단계 [서사] 스킬. 단계 [선정] 결과로 정해진 인물의 사실 자료를 받아 영상 1편 분량의 인물 서사 (narrative) 를 작성한다. 입력 (선정 결과 / 인물 사실 자료원 / 정체성 = 시청자·약속 3겹·톤 / 단원 frame / 영상 길이 잠정 / 한 단어 압축 후보) 을 받아 동작 (입력 align → Q&A 보강 → 자료원 재확인·리서치 → 약속 3겹 운반 서사 초안 → 자체 평가 → Q&A 검토 → 출력) 진행. math-story-telling 의 영상 단원 인물 서사 작성, 약속 3겹 운반 텍스트 시드, 한 단어 압축 도출 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료 (`30_content/people/`, `40_experiments/exp-NNN/output.md`, INTEGRATED_PLAN §8) 를 참조만 함.
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 서사 (N1~N7)
  ssot: 11_video_gen_process/70_tools/se-people-narrate/SKILL.md
  version: "0.1"
  status: 시드 (시범 실행 후 retrospective 로 정련 예정)
allowed-tools: Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch
---

# se-people-narrate — 인물 서사 스킬

본 스킬은 영상 제작 시스템의 단계 [서사]. 단계 [선정] (`se-people-pick`) 의 결과로 정해진 인물의 사실 자료를 받아 영상 1편 분량의 인물 서사 (narrative) 를 작성한다. 출력은 다음 단계 [스토리] (`se-video-story`) 의 직접 입력.

상위 frame: [INTEGRATED_PLAN](../../00_charter/INTEGRATED_PLAN.md) §5.0 skill chain / §5.3 단계 [서사] / §8 결정 1·2.

원칙:
- 본 스킬은 외부 자료를 **참조** 한다. 외부를 변경 X.
- 호출자가 입력 일부만 줘도 됨 — 동작 초기 단계에서 보강.
- 동작 중 Q&A. 답변이 다음 동작을 바꿀 수 있다.

본 v0.1 body 는 **exp-002 STEP 1 시범 실행의 reverse-engineering** 으로 작성됨 (2026-05-25). 시범 결과: [`../../40_experiments/exp-002-build-unit01/1-narrative.md`](../../40_experiments/exp-002-build-unit01/1-narrative.md). 시범에서 실제로 한 동작을 정형화.

---

## 입력 (6개)

호출자가 제공. 부족 시 동작 N2 에서 Q&A.

| # | 입력 | 형식 | 출처 예시 |
|---|---|---|---|
| 1 | 선정 결과 | 인물 ID + 선정 이유 텍스트 | `40_experiments/exp-NNN/output.md` §2~§3 |
| 2 | 인물 사실 자료원 | URL + 인용 가능 텍스트 (자산 N개) | exp-NNN output.md §4 |
| 3 | 정체성 | 시청자 + 약속 3겹 + 톤 | INTEGRATED_PLAN §8 결정 1·2 + A5 잠정 |
| 4 | 단원 frame | 단원 번호 + 핵심 개념 | `30_content/units/NN/meta.json` |
| 5 | 영상 길이 잠정 | 초 + 글자수 (5자/초) | INTEGRATED_PLAN §5.1.2 A3 (잠정 110초/550자) |
| 6 | 한 단어 압축 후보 | 인물을 한 단어로 (영상 클로징) | NCC 가 자산 분석 후 제안 가능 |

---

## 동작 (N1~N7)

### N1. 입력 align

- 입력 6개 확인. 누락·모호 항목 식별.
- 자료원 위치 (선정 결과 파일 / 인물 파일 / 정체성 결정) 확인.
- 정체성 명시 확인 — 모호 시 N2 로.

### N2. (필요 시) Q&A 보강

- 부족 입력은 호출자에게 1~3회 Q&A. 답변이 N4 매핑을 바꿀 수 있음.
- 모든 입력 충분 시 생략.

### N3. 자료원 재확인·리서치

- 입력 #2 의 자료원 *inline 인용 텍스트* 모음.
- 부족 시 fallback 순서: (리서치 패턴 시드 참고)
- 모든 인용 → URL 및 직접 인용문 표기 (N6 fabrication 체크 입력).

### N4. 자산 식별 + 약속 3겹 매핑

- 자료원에서 **N개 핵심 자산** 식별 (보통 3~5). 자산 = 한 영상 장면을 채울 수 있는 사실 단위.
- 각 자산을 약속 3겹 (시대 감각 / 인물 정서 / 발견의 필연성 서사) 에 매핑.
- 약속 3 (필연성 서사) 자산이 0개면 ⚠️ 경고 — 입력 #1 의 선정 이유가 약속 3 자료 명시 불충분. N2 로 돌아감.
- (시범 결과 §1+§3+§4 가 약속 3 운반 — *도서관 사명* + *아르키메데스 서신* 2개 축)

### N5. 서사 초안 작성

- 본문 = §1~§N (N = 자산 수 + 클로징 1~2). 각 §은 1~2 자산 운반.
- 약속 3 핵심 자산 §에 ★ 마크.
- 마지막 또는 끝-1 §에 *클로징 § = 본인 시대 이후 (200/500/1000년 뒤) 의 남은 것* + 카메오 인물 연결.
- 마지막 § = **한 단어 압축** (입력 #6, 본문 끝 confirm).
- 톤: *원료 톤* (사실 + 서사 통합). 발화용 정제 X (그건 STEP 4 [나레이션]). 학술 톤도 X.
- 정서 묘사 ("그가 어떻게 느꼈는지") = *기록 없음/추정* 인라인 명시.
- NCC 해석 (자료에 직접 없는 인과) = 인라인 *fabrication 주의* 박스 표기.

### N6. 자체 평가 (부록 A·B·C·D)

- **부록 A — 약속 3겹 운반 자체 평가 표**: 각 약속별 운반 § + 강도 (★1~5).
- **부록 B — 다음 단계 [스토리] 입력 명세**: §단위 → 영상 장면 (S1~S6) 매핑 표. 시간 합 = 입력 #5.
- **부록 C — fabrication 체크표**: 모든 항목 4분류 (사실 / NCC 해석 / 후세 전승 / 기록 없음) + 인라인 처리 확인.
- **부록 D — 본 시범의 한계 + retrospective 시드**: 동작 중 발견한 정련 항목.

### N7. 출력

- 위치: `<exp 경로>/N-narrative.md` (기본 `40_experiments/exp-NNN/1-narrative.md`).
- 양식: 아래 *출력 양식* 참고.

---

## 출력 양식

```text
<!-- <path> / step N [서사] 출력 / se-people-narrate 실행 결과 -->

# <인물 이름> — <한 단어 압축>

> 메타 (스킬 / 단원 / 인물 / 약속 / 시청자 / 다음 단계 / 일자)

## 1. <자산 1 제목>
...

## 2. <자산 2 제목>
...

## N. 한 단어 압축
**<단어>**.
<짧은 정당화 1~2줄>

---

## 부록 A — 약속 3겹 운반 자체 평가
## 부록 B — 다음 단계 [스토리] 입력 명세
## 부록 C — fabrication 체크
## 부록 D — 본 시범의 한계 + retrospective 시드
```

---

## QnA 패턴 시드

### N2 보강 시
- 입력 #2 자료원 빈약: *"이 자산의 1차 자료 URL 을 알려주거나, WebFetch 허용 범위를 정해주시겠습니까?"*
- 입력 #3 정체성 톤 (A5) 미정: *"톤 (이야기 톤 / 다큐 톤 / 혼합) 잠정 결정 1개 골라주시겠습니까? 본 단계는 원료 톤 유지하나, §정서 묘사 강도가 영향받습니다."*
- 입력 #6 한 단어 압축 후보 없음: *"NCC 가 자산 분석 후 N5 단계에서 후보 제안할까요?"*

### N6 후 (선택)
- *"§X 의 정서 묘사 강도가 fabrication 경계입니다. 유지 / 약화 / 제거?"*
- *"§X 의 NCC 해석 (예: 도서관 분류 본능 → 수의 분류) 은 1차 자료 직접 명시 없음. 학설 확인 / 다른 동기 서사 교체 / 그대로 진행?"*

---

## 리서치 패턴 시드

자료 부족 시 fallback 순서 (동작 N3):

1. `30_content/people/<name>.md` — 본 프로젝트 인물 파일 (참조만)
2. `40_experiments/exp-NNN/output.md` §4 — 선정 단계 자료원 표
3. **MacTutor** (mathshistory.st-andrews.ac.uk) — 학술 1차 reference
4. **Wikipedia (en)** — 일반 2차, 검증된 영문
5. **Britannica** — 학술 2차
6. **WebSearch** — 위 모두 부족 시 fallback (검색결과의 1차 자료 URL 도출 → WebFetch 재시도)

**주의**: 한국어 자료 *번역 인용* 시 원문 (영문/한문) 인용 함께 표기.

---

## 평가 기준

| 항목 | 합격 기준 |
|---|---|
| 약속 3겹 운반도 | 세 약속 모두 ★3 이상. 약속 3 (필연성 서사) ★4 이상 권장 |
| fabrication 분리 표기 | 모든 추정·해석·전승은 인라인 명시 (부록 C 와 일치) |
| 광범 시청자 가독성 | 이름 모르는 시청자도 알아들을 수준 |
| 학습자 (중1) 어휘 | 학술 용어 사용 시 풀어 설명 |
| 자료원 인용 | 모든 사실은 URL 또는 출처 명시 |
| 한 단어 압축 도출 | 제목 + 마지막 § + 부록 B 클로징 일치 |
| 길이 | 입력 #5 의 ~3배 이상 (110초 영상 = ~1500~2000자 원료) |

---

## 진화 메커니즘

- **v0.1** = exp-002 STEP 1 시범 (단원 1 / 에라토스테네스) 의 reverse-engineering. 2026-05-25.
- **v0.2** (정련 예정 — exp-002 STEP 1 retrospective + STEP 4 결정 10 후):
  - N4 자산-약속 매핑 표 정형화
  - fabrication 4분류 (사실 / NCC 해석 / 후세 전승 / 기록 없음) 정밀화
  - 출력 양식 §N 개수 결정 패턴 (자산 수 + 클로징)
  - 길이 기준 (원료 vs 노이즈 경계)
  - N2 Q&A 트리거 조건 정밀화
  - **N5 서사 초안에 호기심 chain 가능 sequence 식별** (v1) — TONE_STRUCTURE §2. 자산을 *질문→답변* 순서로 배치 가능한지 검토.
  - **친근 톤 가능 자산 명시** (v1) — TONE_STRUCTURE §1. 친근 별명 / 일상 사실 우선 식별.
  - **풍부한 시대 배경 자산** (v1) — TONE_STRUCTURE §3. S1 풍경 시드 별도 명시.
  - **🔥 N5 서사 원료에 dialog 가능 sequence 시드 명시 (v2)** — TONE_STRUCTURE v2 §1·§4. Q (청소년 호기심) 의 자연 질문 가능 sequence 예시 + A (대학원생) 의 *"나도 찾아봤는데..."* / *"내가 알기로는..."* 가능 사실 어디서 삽입 가능한지 시드 명시. 다음 단계 [스토리] 가 dialog turn 으로 분리 가능하도록.
- **v0.3+** = 다음 단원 (브라마굽타 등) 시범 후 일반화 검증.

---

## 호출 방법

CHECKLIST.md (`40_experiments/exp-NNN/CHECKLIST.md`) STEP 1 에서 호출:

```yaml
스킬: se-people-narrate
입력:
  1. 선정 결과: 40_experiments/exp-NNN/output.md §2~§3
  2. 인물 사실 자료원: 40_experiments/exp-NNN/output.md §4
  3. 정체성: INTEGRATED_PLAN §8 결정 1·2 + A5 톤 잠정
  4. 단원 frame: 30_content/units/NN/meta.json
  5. 영상 길이 잠정: 110초 (A3 잠정) / ~550자 (5자/초)
  6. 한 단어 압축 후보: <NCC 제안 또는 호출자 지정>
출력: 40_experiments/exp-NNN/1-narrative.md
다음 단계: se-video-story (STEP 2)
```

본 시범 호출 예시: [`../../40_experiments/exp-002-build-unit01/1-narrative.md`](../../40_experiments/exp-002-build-unit01/1-narrative.md).
