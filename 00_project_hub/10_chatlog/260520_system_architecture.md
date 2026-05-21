<!-- 260520_system_architecture.md -->

# 시스템 구조 아이디어 정리 — 원칙 진화 메커니즘

> Nick 질문(2026-05-20):
> 1. `mathtelling-design-system` vs `mathtelling` 차이?
> 2. design-system이 더 많은 context/prompt/skill/workflow를 가져야?
> 3. 아니면 mathtelling 아래에 skill/workflow/context 체계적 정리?
> 4. **영상 하나하나 고치는 게 아니라, 원칙/규칙을 고쳐나갈 수 있도록**

라운드 1 — NCC 정리·권고. 결정은 Nick.

---

## Round 1 — 현재 구조 진단 + 3 옵션

### 1.1 현재 두 repo의 실제 내용물

| | `mathtelling-design-system/` | `mathtelling/` |
|---|---|---|
| 공개성 | Public (OSS-able) | Private |
| 빌드 | 없음 (순수 CSS) | 없음 |
| 디렉토리 수 | 3 (`tokens/`, `subjects/`, `dist/`) | 4 (`content/`, `apps/`, `channel/`, `_docs(분산)`) |
| 파일 수 | 6 | 30+ |
| 의존성 | 없음 | design-system을 CSS import |
| 핵심 자원 | CSS 변수·토큰 | 콘텐츠 + 앱 + 영상 + Nick_TODO |

**한 줄 요약**:
- design-system = **디자인 어휘** (색·여백·타입·모션의 표준)
- mathtelling = **콘텐츠 + 제작물** (인물·단원·앱·영상)

### 1.2 현재 구조의 4가지 갭

#### 갭 A — 원칙·표준이 분산
- `APP_PRINCIPLES.md` → base repo (mid_eun, 30_MiddleSchool/...)
- `PIPELINE_v1_5.md` → mathtelling/channel/_docs/
- `STORY_VIDEO_GUIDE.md (v1)` → base repo (90_video/_docs/)
- `learner-profile.md` → base repo (10_docs/)
- ⇒ **원칙이 3개 repo에 흩어져 있음**

#### 갭 B — Skill의 위치 모호
- Claude Code Skill은 `.claude/skills/`에서 로드됨 (base repo)
- 하지만 skill 내용은 mathtelling/ 작업물을 다룸 (channel/, apps/)
- ⇒ **mathtelling의 일부인데 base repo에 거주**

#### 갭 C — Context 부재
NCC가 매 세션 시작 시 알아야 하는 것:
- 학습자(딸) 프로필
- 인물 톤 가이드
- 시대 팔레트
- 현재 진행 phase
- 과거 결정·feedback

⇒ 일부는 CLAUDE.md, 일부는 chatlog, 일부는 흩어져 있음. **체계적이지 않음**.

#### 갭 D — 원칙 진화 메커니즘 부재 ⭐ Nick의 핵심 질문
- 영상 1편 만들고 나서 "이건 다음에 고쳐야지" → **어디에 기록? 누가 정리?**
- 3편 만들고 나서 발견한 패턴 → **자동으로 PIPELINE.md에 반영되는 흐름 없음**
- 결과: 같은 실수 반복 또는 원칙이 정체

---

### 1.3 세 가지 옵션

#### Option A — design-system을 "Production System"으로 격상
design-system이 CSS뿐 아니라 모든 원칙·스킬·워크플로우 포함.

```
mathtelling-design-system/ (Public)
├── tokens/ (현재)
├── subjects/ (현재)
├── docs/
│   ├── APP_PRINCIPLES.md
│   ├── STORY_VIDEO_GUIDE.md
│   ├── PIPELINE_v1_5.md
│   └── LEARNER_PROFILE.md
├── skills/ (Claude Code skill 정의)
└── workflows/

mathtelling/ — 콘텐츠만
```

- **장점**: 깨끗한 분리 (시스템 vs 콘텐츠)
- **단점**: design-system 이름과 안 맞음. OSS 가치 떨어짐 (학습자 프로필이 public?). public/private 경계 모호.

#### Option B — mathtelling 안에 `system/` 디렉토리 신설 (권장)

```
mathtelling/
├── content/        콘텐츠 (인물·단원 데이터)
├── apps/           앱
├── channel/        영상 소스
├── system/         ★ NEW — 모든 메타 (원칙·스킬·워크플로우·context)
│   ├── principles/
│   │   ├── CORE.md                  공통 (앱·영상 모두 적용)
│   │   ├── APP_PRINCIPLES.md        (base에서 이관/링크)
│   │   ├── PIPELINE_v1_5.md         (channel/_docs에서 이관)
│   │   ├── STORY_TONE.md
│   │   └── ...
│   ├── context/
│   │   ├── LEARNER_PROFILE.md       딸의 프로필
│   │   ├── PERSON_CAST.md           13단원 인물 캐스팅 표
│   │   ├── ERA_PALETTES.md          시대별 시각 톤
│   │   └── TONE_GUIDE.md            글·말투 표준
│   ├── skills/                       Claude Code skill 정의
│   │   ├── se_story_video_v1_5/
│   │   ├── se_math_practice/
│   │   └── ...
│   ├── workflows/
│   │   ├── unit-pipeline.md         Phase 0~5d
│   │   ├── video-evolution.md       v1→v1.5→v2
│   │   └── retrospective-cycle.md   회고·증류 사이클
│   └── playbooks/
│       ├── retrospectives/          영상·앱마다 회고 기록
│       │   ├── 260520_unit01_v1_5.md
│       │   └── ...
│       └── distilled/               회고 → 패턴 정제본
└── CLAUDE.md       (system/을 anchor로 참조)
```

- **장점**:
  - 원칙·스킬·context가 한 곳
  - mathtelling repo 안에서 자기완결
  - skill을 `.claude/skills/`에 symlink (또는 sync 스크립트)로 노출
  - retrospective 디렉토리로 **원칙 진화의 입력 자료 누적**
- **단점**:
  - skill의 두 위치 (mathtelling/system/skills/ + .claude/skills/) 동기화 부담
  - base repo의 기존 자료(APP_PRINCIPLES.md 등) 이관·중복 정리 필요

#### Option C — 미니멀 (현재 구조 유지 + 진화 메커니즘만 추가)
지금 구조 그대로, 흩어진 그대로 두되:
- `mathtelling/_retrospectives/` 추가 (영상·앱 회고 기록)
- 매 5편마다 `/se_distill_principles` skill로 PIPELINE.md/APP_PRINCIPLES.md 자동 업데이트

- **장점**: 이동·중복 없음. 가장 가볍게 시작
- **단점**: 갭 A·B·C 그대로. 시간이 지나면 더 흩어짐.

---

## Round 1 권고

### NCC 권고: **Option B (mathtelling/system/) + 진화 메커니즘**

이유:
1. **자기완결성**: NCC가 mathtelling repo 하나만 읽으면 모든 context 획득
2. **갭 A·B·C 동시 해결**: 원칙·스킬·context가 한 지붕
3. **갭 D (진화 메커니즘)는 `system/playbooks/`로 해결**
4. design-system은 그대로 — OSS 가치·역할 명확

### 진화 메커니즘 — 4단계 사이클

```
[1] Build         단원 영상·앱 제작 (NCC + skill)
       ↓
[2] Retrospect    제작 후 자동 회고 작성
                  → system/playbooks/retrospectives/YYMMDD_unitNN.md
                  · 잘 된 것 / 아쉬운 것 / 다음에 다르게 / 일반 원칙 후보
       ↓
[3] Distill       3~5편 누적 후 패턴 추출 (NCC + /se_distill_principles)
                  → system/principles/ 의 해당 .md 업데이트
                  → 변경 이력 (CHANGELOG.md 또는 각 파일 끝 변경 이력)
       ↓
[4] Apply         다음 단원부터 자동 적용 (skill이 system/principles/를 항상 읽음)
       ↓
       (다시 [1]로)
```

각 단계의 핵심 산출물:
- **Retrospect**: 빠르고 부담 없이. 5~10줄 짜리 회고 ← NCC가 자동 생성
- **Distill**: 회고 5편 모이면 패턴 1개씩 정제 ← NCC가 패턴 발견, Nick 확정
- **Principles**: SSOT 문서, 버전 관리됨 ← 모든 skill이 시작 시 읽음

### 추가 권고 — Skill 정의의 새 표준

skill 정의(`SKILL.md`)에 명시적 섹션:
```
## 이 skill이 읽는 원칙
- system/principles/CORE.md
- system/principles/PIPELINE_v1_5.md (이 skill 전용)
- system/context/LEARNER_PROFILE.md

## 이 skill이 생성하는 retrospective
system/playbooks/retrospectives/{date}_{unit}_{skill}.md
```

→ skill이 어떤 원칙을 읽고 어떤 회고를 쓰는지 명시 = **시스템이 자기 자신을 추적**.

---

## 작업 분량 추정 (Option B 채택 시)

| 작업 | 노력 | 위험 |
|---|---|---|
| `mathtelling/system/` 디렉토리 신설 + README | 5분 | 낮음 |
| base의 APP_PRINCIPLES.md 등 system/principles/로 복사 | 30분 | 낮음 (base는 그대로 둠, 점진적 마이그레이션) |
| `.claude/skills/`와 `system/skills/` 동기화 방식 결정 (symlink vs sync 스크립트) | 30분 | 중간 (Windows에서 symlink 권한 이슈) |
| `system/context/` 신규 작성 (LEARNER_PROFILE 등) | 1~2시간 | 낮음 |
| `se_distill_principles` skill 신규 정의 | 1시간 | 낮음 |
| retrospective 템플릿 + 첫 회고 (unit-01 v1.5) 시연 | 30분 | 낮음 |

→ 총 ~4시간. 1세션 내 완수 가능.

---

## Nick 결정 대기 항목

- [ ] **D1**: Option B 채택? (또는 A/C, 혹은 수정안) -> B
- [ ] **D2**: skill 동기화 방식 (symlink / sync 스크립트 / 그냥 양쪽 복사) -> sync script
- [ ] **D3**: 진화 사이클 트리거 — 매 영상 후 자동? 매 N편 후? Nick 수동 호출? -> 자동으로 insight file 생성... insight 파일 모아서 진화시키기... 진화 시키면 insight 파일에 반영완료 표시해두기
- [ ] **D4**: base repo(mid_eun)의 기존 자료 처리 — 그대로 두기 / 점진 이관 / 일괄 이관 -> 그대로 두고, mathtelling 쪽에 하나씩 만들어 가기

각 항목 선택 후 Round 2에서 실행 계획.

---

## 변경 이력
- R1 (2026-05-20): NCC 진단 + 3옵션 + Option B 권고
