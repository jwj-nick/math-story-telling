<!-- 0525_step1_skill_frontmatter.md -->

# exp-002 / STEP 1 / Issue — `se-people-narrate` SKILL.md frontmatter 설계

> **issue**: 단계 [서사] 첫 스킬의 frontmatter 7 필드 확정.
> **step**: STEP 1 (CHECKLIST.md §1)
> **산출물 (이 issue)**: `70_tools/se-people-narrate/SKILL.md` 의 frontmatter 부분
> **단일 진입점**: [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md)
> **상위 체크리스트**: [`../40_experiments/exp-002-build-unit01/CHECKLIST.md`](../40_experiments/exp-002-build-unit01/CHECKLIST.md)
> **선행 양식**: [`../70_tools/se-people-pick/SKILL.md`](../70_tools/se-people-pick/SKILL.md) frontmatter
> **spec 근거**: agentskills.io/specification (kebab-case 강제, name ≤64자, description ≤1024자, allowed-tools 공백 구분)
> **시작**: 2026-05-25

---

## 이 issue 의 micro-step 흐름 (예정)

| Round | 결정할 것 |
|---|---|
| 1 | `name` (스킬 이름 kebab-case) |
| 2 | `description` (1024자 이내, 무엇을 입력받아 무엇을 출력하는 스킬인지) |
| 3 | `compatibility` (적용 환경 1줄) |
| 4 | `metadata` (project / sub-project / stage / ssot / version / status) |
| 5 | `allowed-tools` (필요한 tool 목록) |

각 Round 결정 → 다음 Round Q&A 의 답이 바뀔 수 있음.

---

# Round 1 — `name` 확정 (2026-05-25)

## NCC 질문

단계 [서사] 스킬의 이름을 무엇으로 할까요?

**문맥**:
- 단계 [선정] = `se-people-pick` (인물 발굴·선정)
- 단계 [서사] = 선정된 인물의 사실 자료 → 약속 3겹을 운반하는 텍스트 서사 (영상 1편 분량의 시드)
- 다음 단계 [스토리] = `se-video-story` (서사 → 110초 영상 스토리 시드)

**spec 제약**:
- kebab-case 강제 (underscore X)
- ≤ 64자
- 본 프로젝트 prefix = `se-` (story-engine 단축)

**옵션** (NCC 추천 = 1번):

1. `se-people-narrate` — 동사형 (CHECKLIST.md / INTEGRATED_PLAN 에 잠정 기재됨, `se-people-pick` 와 짝)
2. `se-people-story` — 일상어 (단계 [스토리] 와 혼동 우려)
3. `se-narrative` — people 빼고 (다음 단계가 `se-video-story` 라 일관성 X)
4. `se-people-narrative` — 명사형 (다른 스킬과 동사형 통일성 깨짐)

**NCC 추천 이유**:
- `se-people-pick` (동사 pick) 과 같이 동사형 `narrate` 통일
- "people 의 narrative 를 만든다" 가 정확한 동작 표현
- 다음 단계 `se-video-story` 와 명확히 분리 (대상 = people, output = narrative)

## Nick 답변

**`se-people-narrate`** (NCC 추천 채택).

## 결정

단계 [서사] 스킬 name = `se-people-narrate`.

## 영향

- 디렉토리 = `70_tools/se-people-narrate/`
- 다음 단계 `se-video-story` 와 대상 명확히 분리 (people → video)
- description (Round 2) 의 "무엇을 받아 무엇을 만드는가" 가 *people 사실 → narrative* 임을 명시해야

---

# Round 2 — `description` 확정 (2026-05-25)

## NCC 질문

`description` 필드의 텍스트를 무엇으로 할까요?

**spec 제약**:
- ≤ 1024자
- "스킬이 무엇을 하는가" + "언제 사용하는가" 두 축 포함 권장
- `se-people-pick` 양식 참고: "영상 제작 시스템의 단계 [선정] 스킬. [동작 요약]. 입력 N개 (...) 를 받아 동작 M단계 (...) 진행. [언제 사용]."

**문맥**:
- 본 스킬 입력 (잠정, body 설계 Round 에서 확정) — 선정 결과 (인물 ID + 선정 이유) / 인물 사실 자료원 (URL + 인용 가능 텍스트) / 정체성 (시청자·약속 3겹·톤) / 단원 frame / 영상 길이 잠정 / 다른 인물과의 분리 단서 등
- 본 스킬 동작 (잠정) — 입력 align → Q&A (부족 입력 보강) → 자료원 재확인 + 부족 시 리서치 → 약속 3겹 운반 서사 초안 → 자체 평가 (3겹 운반도) → Q&A (Nick 검토) → 출력 + 한 단어 압축
- 본 스킬 출력 = `1-narrative.md` (영상 1편 분량의 인물 서사 텍스트, 다음 단계 [스토리] 의 직접 입력)

**옵션** (NCC 추천 = 1번):

### 옵션 1 — `se-people-pick` 동일 패턴 따름 (Recommended)

> 영상 제작 시스템의 단계 [서사] 스킬. 단계 [선정] 결과로 정해진 인물의 사실 자료를 받아 영상 1편 분량의 인물 서사 (narrative) 를 작성한다. 입력 (선정 결과 / 인물 사실 자료원 / 정체성 = 시청자·약속 3겹·톤 / 단원 frame / 영상 길이 잠정 / 한 단어 압축 후보) 을 받아 동작 (입력 align → Q&A 보강 → 자료원 재확인·리서치 → 약속 3겹 운반 서사 초안 → 자체 평가 → Q&A 검토 → 출력) 진행. math-story-telling 의 영상 단원 인물 서사 작성, 약속 3겹 운반 텍스트 시드, 한 단어 압축 도출 시 사용.

### 옵션 2 — 간결형

> 영상 제작 시스템 단계 [서사] 스킬. 선정된 인물의 사실 자료 → 약속 3겹 (시대 감각 / 인물 정서 / 발견의 필연성 서사) 을 운반하는 서사 텍스트 작성. 다음 단계 [스토리] (`se-video-story`) 의 입력. math-story-telling 의 인물 서사 작성 시 사용.

### 옵션 3 — 입력·동작 수 명시형

> 영상 제작 시스템 단계 [서사] 스킬. 선정된 인물 사실 → 약속 3겹 운반 서사. 입력 6개 (선정 결과 / 인물 사실 자료원 / 정체성 / 단원 frame / 길이 잠정 / 한 단어 압축 후보), 동작 7단계 (align → Q&A → 자료원 재확인 → 초안 → 평가 → 검토 → 출력) 진행. math-story-telling 인물 서사 작성 시 사용.

**NCC 추천 이유**:
- `se-people-pick` 와 양식 통일 → 다음 6개 스킬도 동일 패턴 적용 (확장 일관성)
- 입력·동작은 잠정이므로 body 설계 단계에서 변동 가능. description 은 본 spec 의 1024자 한계 내 "충분히 검색·이해 가능" 정도
- "math-story-telling 의 ... 시 사용" 패턴 = agentskills.io 가 권장하는 "when to use" 명시

## Nick 답변

**옵션 1** (양식 통일형) 채택.

## 결정

description (확정 텍스트) =

> 영상 제작 시스템의 단계 [서사] 스킬. 단계 [선정] 결과로 정해진 인물의 사실 자료를 받아 영상 1편 분량의 인물 서사 (narrative) 를 작성한다. 입력 (선정 결과 / 인물 사실 자료원 / 정체성 = 시청자·약속 3겹·톤 / 단원 frame / 영상 길이 잠정 / 한 단어 압축 후보) 을 받아 동작 (입력 align → Q&A 보강 → 자료원 재확인·리서치 → 약속 3겹 운반 서사 초안 → 자체 평가 → Q&A 검토 → 출력) 진행. math-story-telling 의 영상 단원 인물 서사 작성, 약속 3겹 운반 텍스트 시드, 한 단어 압축 도출 시 사용.

(글자수 측정 = body 작성 단계에서 spec 1024자 한계 검증)

## 영향

- 입력 6개 항목 잠정 확정 (body 설계 Round 에서 정련)
- 동작 7단계 잠정 확정 (body 설계 Round 에서 정련)
- 다음 Round (compatibility) 는 `se-people-pick` 양식 짧게 따라감

---

# Round 3 — `compatibility` 확정 (2026-05-25)

## NCC 질문

`compatibility` 필드 텍스트는 무엇으로?

**문맥**:
- `se-people-pick` 의 compatibility = "Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료 (30_content/, .private/feedback/, INTEGRATED_PLAN §8) 를 참조만 함."
- 본 스킬은 *선정 결과* + *인물 사실 자료* 를 받음. `30_content/people/<name>.md` 도 참조 (변경 X)

**옵션** (NCC 추천 = 1번):

### 옵션 1 — `se-people-pick` 양식 그대로 (Recommended)

> Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료 (`30_content/people/`, `40_experiments/exp-NNN/output.md`, INTEGRATED_PLAN §8) 를 참조만 함.

### 옵션 2 — 짧게

> Designed for Claude Code in 11_video_gen_process/. 외부 자료 참조만.

### 옵션 3 — 상세 (입력 출처 명시)

> Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 입력 출처: 단계 [선정] 결과 (`40_experiments/exp-NNN-selection-*/output.md`) + 인물 사실 자료 (`30_content/people/<name>.md` 참조) + 정체성 결정 (INTEGRATED_PLAN §8). 외부 자료 변경 X.

**NCC 추천 이유**:
- 옵션 1 이 `se-people-pick` 와 정확히 같은 패턴 → 양식 통일
- 외부 참조 위치 (`30_content/people/`, `40_experiments/`, INTEGRATED_PLAN) 모두 명시
- 옵션 3 은 너무 상세 → SKILL.md body 에서 다룰 내용

## Nick 답변

**옵션 1** (`se-people-pick` 패턴) 채택.

## 결정

compatibility =

> Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료 (`30_content/people/`, `40_experiments/exp-NNN/output.md`, INTEGRATED_PLAN §8) 를 참조만 함.

---

# Round 4 — `metadata` 확정 (2026-05-25)

## NCC 질문

`metadata` 의 6개 sub-field 텍스트는?

**문맥**:
- `se-people-pick` 의 metadata 양식:
  ```yaml
  metadata:
    project: math-story-telling
    sub-project: 11_video_gen_process
    stage: 선정 (P1~P7)
    ssot: 11_video_gen_process/70_tools/se-people-pick/SKILL.md
    version: "0.1"
    status: 시드 (시범 실행 후 retrospective 로 정련 예정)
  ```
- 본 스킬은 `se-people-pick` 와 동일 sub-project, 다른 stage

**옵션** (NCC 추천 = 1번, 4개 필드 자동 결정 + 2개 합의):

| field | 값 | 결정 방식 |
|---|---|---|
| `project` | `math-story-telling` | 자동 (`se-people-pick` 동일) |
| `sub-project` | `11_video_gen_process` | 자동 |
| `ssot` | `11_video_gen_process/70_tools/se-people-narrate/SKILL.md` | 자동 (디렉토리 규약) |
| `version` | `"0.1"` | 자동 (시드 = 0.1) |
| `stage` | **결정 필요** | 아래 옵션 |
| `status` | **결정 필요** | 아래 옵션 |

### 결정 필요 ① — `stage`

- 옵션 A `서사 (N1~N?)` — `se-people-pick` 의 `선정 (P1~P7)` 양식 따름. ? 자리는 body 동작 단계 수 (잠정 7)
- 옵션 B `서사` — 한글만, 동작 수 생략
- 옵션 C `서사 (P2)` — chain 위치 (1=선정, 2=서사) 명시

**NCC 추천 = A**: `se-people-pick` 와 양식 통일 (`(N1~N7)` 형태). N = narrate prefix.

### 결정 필요 ② — `status`

- 옵션 A `시드 (시범 실행 후 retrospective 로 정련 예정)` — `se-people-pick` 와 동일 표현
- 옵션 B `시드 v0.1 (exp-002 시범 후 정련)` — 더 구체적
- 옵션 C `draft` — 영문 짧게

**NCC 추천 = A**: 양식 통일.

---

**종합 metadata (NCC 추천안 = 옵션 1)**:

```yaml
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 서사 (N1~N7)
  ssot: 11_video_gen_process/70_tools/se-people-narrate/SKILL.md
  version: "0.1"
  status: 시드 (시범 실행 후 retrospective 로 정련 예정)
```

## Nick 답변

**stage = A** (`서사 (N1~N7)`).
**status = A** (`시드 (시범 실행 후 retrospective 로 정련 예정)`).

## 결정

```yaml
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 서사 (N1~N7)
  ssot: 11_video_gen_process/70_tools/se-people-narrate/SKILL.md
  version: "0.1"
  status: 시드 (시범 실행 후 retrospective 로 정련 예정)
```

## 영향

- body 동작 단계 수가 잠정 7. 설계 단계에서 변동 시 stage 값도 갱신 (예: N1~N6)
- status 는 exp-002 STEP 1 retrospective 작성 시점에 `정련 v0.2` 로 갱신 예정

---

# Round 5 — `allowed-tools` 확정 (2026-05-25)

## NCC 질문

`allowed-tools` 필드는 본 스킬이 호출 가능한 Claude Code tool 목록 (공백 구분).

**문맥**:
- `se-people-pick` 의 allowed-tools = `Read Grep Glob Bash AskUserQuestion WebFetch WebSearch`
- 본 스킬 [서사] 의 예상 동작:
  - 입력 align — Read (선정 결과 파일, 인물 사실 파일)
  - Q&A 보강·검토 — AskUserQuestion
  - 자료원 재확인·리서치 — Read (`30_content/people/`), WebFetch / WebSearch (부족 시 fallback)
  - 서사 텍스트 작성 — Write (`1-narrative.md` 신설)
  - 글자 수·약속 3겹 운반도 자체 평가 — Read 후 분석
  - (선택) 파일 검색 — Grep / Glob
  - (선택) shell 작업 — Bash

**`se-people-pick` 와의 차이**:
- 본 스킬은 **Write** 가 필요 (서사 텍스트 파일 신설). `se-people-pick` 는 Write 없이도 가능했나? → output.md 작성 시 Write 사용함. 그런데 allowed-tools 에 명시 안 되어 있음. **누락**.
- 본 스킬은 명확히 Write 가 핵심 동작이므로 명시 필수

**옵션** (NCC 추천 = 1번):

### 옵션 1 — pick 양식 + Write 추가 (Recommended)

```
Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch
```

### 옵션 2 — 최소

```
Read Write AskUserQuestion WebSearch
```

### 옵션 3 — pick 와 정확히 동일 (Write 없음)

```
Read Grep Glob Bash AskUserQuestion WebFetch WebSearch
```

(Write 누락. `se-people-pick` 와 동일하지만 본 스킬 동작 X)

**NCC 추천 이유**:
- 옵션 1 = pick 양식 따라가되 Write 만 추가. pick 의 누락도 동일하게 보정 (다음 Round 에서 pick SKILL.md 도 Write 추가하는 미세 fix 제안 가능)
- Grep/Glob/Bash 는 자료원 검색·길이 측정 등에 *가끔* 필요 → 보존
- WebFetch + WebSearch 양쪽 보존 = pick retrospective 의 fallback 순서 정련 사항 반영 가능

## Nick 답변

**옵션 1** 채택.

## 결정

```yaml
allowed-tools: Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch
```

## 영향 + 후속 작업 발견

- 본 스킬 frontmatter 5 라운드 완료
- **별도 fix 항목 (병행)**: `se-people-pick/SKILL.md` 의 allowed-tools 도 Write 누락 → 동일하게 추가 필요. 본 issue 종료 직전에 같이 처리.

---

# 종합 — frontmatter 최종

```yaml
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
```

---

# 본 issue 종료 (2026-05-25)

## 완료 작업

1. ✅ `70_tools/se-people-narrate/` 디렉토리 신설
2. ✅ `70_tools/se-people-narrate/SKILL.md` 신설 (frontmatter 확정 + body placeholder, body 설계 session log link 포함)
3. ✅ `se-people-pick/SKILL.md` allowed-tools 에 Write 추가 (병행 fix)
4. ✅ 본 session log 마무리
5. ➡️ 다음 issue session log 신설: [`0525_step1_skill_body.md`](./0525_step1_skill_body.md)

## 결정 누적 (frontmatter 5건)

- Round 1: name = `se-people-narrate`
- Round 2: description = 양식 통일형 (옵션 1)
- Round 3: compatibility = pick 패턴 (옵션 1)
- Round 4: metadata = stage `서사 (N1~N7)` + status `시드 (...)`
- Round 5: allowed-tools = `Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch`

## 다음 issue 로 이월

- body 6 sub-section 설계 (입력 6개 / 동작 7단계 / 출력 양식 / QnA 패턴 / 리서치 패턴 / 평가 기준)
- body 설계 완료 시 SKILL.md placeholder 정식 body 로 교체
- exp-002 STEP 1 §1.1 의 "스킬 시드 작성" 단계 완료 신호 = body 까지 작성된 시점

## 부가 발견 (process 학습)

- `se-people-pick` allowed-tools 에 Write 누락 — 본 issue 진행 중 발견 + 즉시 fix
- → 다음 스킬 작성 시에도 *입력에 Write 가 필요한가* 자동 점검 항목으로 (retrospective 시드)
