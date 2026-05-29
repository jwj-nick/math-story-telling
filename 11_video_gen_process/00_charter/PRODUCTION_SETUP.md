<!-- PRODUCTION_SETUP.md / 양산 환경 정리 설계 (졸업 + 디렉토리 + batch run) -->

# 양산 환경 설계 — 샌드박스 졸업 + 정식 구조 + Batch Run

> **문제 (Nick)**: 영상 8 스킬이 `11_video_gen_process/70_tools/`(빌드 샌드박스)에 갇혀 있어 `.claude/`로 정식 호출 불가. 디렉토리 전체가 기형적. 프로세스를 갖춘 지금, 제대로된 구조에서 batch run 양산 체계로.
> **원칙 (CLAUDE.md 기존)**: SSOT = `10_system/30_skills/` → mirror = `.claude/skills/` (sync-skills.sh 단방향). 11_video_gen_process = "시스템 구축" 샌드박스(양산 X).
> **작성**: 2026-05-29. 실행 전 Nick 결정 필요 (구조 이동 = 되돌리기 어려움).

---

## 1. 현재 상태 (기형 진단)

```
10_system/30_skills/        ← 정식 SSOT (15개, math/content 스킬, underscore)
  └─ se_concept_review/ ... se_unit_review/
.claude/skills/             ← 미러 (sync-skills.sh로 10개 동기화됨)
10_system/35_agents/        ← agent SSOT
  └─ (se_agent_unit_orchestrator)
11_video_gen_process/       ← ⚠️ 빌드 샌드박스
  ├─ 70_tools/              ← ⚠️ 영상 9 스킬 (kebab, 정식 아님)
  │   └─ se-people-narrate, se-people-pick, se-video-{story,storyboard,
  │      narration,image,motion,render,compose}/
  ├─ 20_step_guides/        ← 심화 가이드 8개
  ├─ 00_charter/            ← PURPOSE, INTEGRATED_PLAN, TONE_STRUCTURE, ROADMAP
  └─ 40_experiments/exp-002-build-unit01/  ← ⚠️ 영상 1편 산출물 (실험 폴더)
50_channel/season-1-ancient/  ← 정식 영상 소스 위치 (CLAUDE.md)
40_grades/middle/math1/NN_*/  ← 단원별 4축 산출물 (video/ 포함 가능)
```

**기형 3가지**:
1. 영상 스킬이 SSOT(`10_system/30_skills/`) 밖 → `.claude/` 미러 안 됨 → 정식 호출 불가
2. 영상 1편이 `40_experiments/`(실험)에 → 양산 산출물 위치 아님
3. 네이밍 불일치: 기존 underscore(se_concept_review) vs 영상 kebab(se-video-*)

---

## 2. 목표 구조 (양산 체계)

```
10_system/
  30_skills/                ← 모든 스킬 SSOT (math + video 통합)
    se_video_narrate/ ...   ← 영상 8 스킬 졸업 (네이밍 = 결정 1)
  35_agents/
    se_agent_video_orchestrator.md  ← 영상 batch orchestrator (신설)
  60_workflows/
    video_unit_pipeline.md  ← 8 STEP 워크플로우 정식 문서 (step_guides 졸업)
  20_context/
    voice-pool.md, tts/image-tools-guide  ← 합성 config SSOT 졸업
.claude/skills/             ← sync로 영상 스킬도 미러 (정식 호출 가능)
.claude/agents/
50_channel/season-1-ancient/  ← 양산 산출물 (결정 2)
  unit-01-eratosthenes/
    1-narrative.md ... 8-final.mp4, 5-images/
  _manifest.md              ← batch run 대상 단원 목록
11_video_gen_process/       ← 빌드 기록으로 보존 or 아카이브 (결정 3)
```

---

## 3. Batch Run 메커니즘 (핵심)

Nick 목표 = "중간 관여 없는 자율 + batch". 두 층:

### 3.1 단원 1개 orchestrator (자율)
`se_agent_video_orchestrator`: `"unit NN [인물]"` 한 줄 → STEP 1~8 자동 실행.
- 각 STEP = 해당 스킬 호출, 산출물을 `50_channel/.../unit-NN/`에 기록
- 이미지 = Nano Banana NCC 자율 생성 (Tier1 활성됨)
- HITL 게이트(옵션): 인물 확정 / 최종 확인 — batch 모드에선 생략 가능

### 3.2 다단원 batch (manifest 기반)
`_manifest.md`에 단원·인물 목록:
```
unit-02 | 정수와유리수 | 브라마굽타 | pending
unit-03 | 문자와식    | 알콰리즈미 | pending
```
batch runner(스크립트 or Workflow)가 manifest를 읽어 단원마다 orchestrator 호출.
- 단원당 독립 (병렬 가능, API rate limit 주의)
- 완료 시 manifest 상태 갱신 + 산출물 + retro
- 실패 단원 격리 (나머지 진행)

### 3.3 재현성 (batch 안정성)
- voice-pool §0 = 음성 config 고정 (단원별 randomize 규칙 포함)
- 렌더 파이프라인 = config→mp4 스크립트화 (FFmpeg 재사용)
- 이미지 = 프롬프트 템플릿(STYLE/CHAR 블록) + reference 일관성

---

## 4. 결정 필요 항목 (Nick)

### 결정 1 — 스킬 네이밍
- (A) **영상 스킬도 underscore로 통일** (se_video_narrate) — 기존 15개와 일관, sync-skills.sh 그대로
- (B) **kebab 유지** (se-video-narrate) — agentskills.io 표준(메모리), 단 기존과 혼재
- (C) 전부 kebab으로 통일 (기존 15개도 rename) — 가장 깨끗하나 작업 큼 + agent/orchestrator 참조 갱신

### 결정 2 — 양산 산출물 위치
- (A) **`50_channel/season-1-ancient/unit-NN/`** — 채널/시리즈 정체성 중심 (CLAUDE.md 영상 소스 위치)
- (B) **`40_grades/middle/math1/NN_*/video/`** — 단원별 4축 묶음 (개념·문제와 한 폴더)
- (C) 둘 다 — 마스터는 50_channel, 40_grades엔 링크/임베드

### 결정 3 — 11_video_gen_process 처리
- (A) **빌드 기록으로 보존** (졸업 후 read-only 참고, step_guides·charter 유지)
- (B) **90_archive로 이동** (졸업물만 정식 위치에, 샌드박스 아카이브)
- (C) 일부만 졸업 + 나머지 보존 (charter·step_guides는 10_system으로, experiments는 archive)

### 결정 4 — 실행 시점
- (A) **지금 단원2 자율 시범을 먼저** → 검증 후 구조 졸업 (시범에서 또 바뀔 수 있음)
- (B) **구조 졸업 먼저** → 정식 구조에서 단원2 batch (깨끗하나 시범 미검증 상태 졸업)

---

## 5. 권장안 (NCC 의견)

| 결정 | 권장 | 이유 |
|---|---|---|
| 1 네이밍 | **A (underscore 통일)** | 기존 15개·sync-skills.sh·orchestrator 참조와 무마찰. agentskills name은 frontmatter로 별도 표기 가능 |
| 2 위치 | **A (50_channel)** | 영상은 채널 자산. 4축 통합은 배포 단계(60_deploy)에서 링크 |
| 3 샌드박스 | **C (일부 졸업 + 보존)** | charter/step_guides = 시스템 자산(졸업), experiments = 기록(보존), 스킬 = SSOT 졸업 |
| 4 시점 | **A (단원2 시범 먼저)** | 단원2가 분수령 — 시범에서 orchestrator·batch 형태가 확정된 뒤 졸업해야 재작업 없음 |

→ **권장 흐름**: 단원2를 *현 샌드박스에서* 자율 시범 (orchestrator 시드 도출) → 형태 확정 → 한 번에 정식 졸업(스킬→10_system, 산출물→50_channel, 워크플로우 문서화) → 단원3+ batch.

---

## 6. 졸업 실행 체크리스트 (결정 후)

- [ ] 영상 8 스킬 → `10_system/30_skills/` (네이밍 결정 반영)
- [ ] se_agent_video_orchestrator → `10_system/35_agents/`
- [ ] step_guides 8개 → `10_system/60_workflows/` (또는 유지+링크)
- [ ] voice-pool/tts/image 가이드 → `10_system/20_context/`
- [ ] sync-skills.sh 실행 → `.claude/` 미러 갱신
- [ ] exp-002 산출물 → `50_channel/season-1-ancient/unit-01-eratosthenes/`
- [ ] `_manifest.md` 신설 (단원 목록)
- [ ] CLAUDE.md 스킬 표 갱신 (영상 스킬 등록)
- [ ] 11_video_gen_process 처리 (결정 3)
- [ ] git commit (구조 졸업)

---

## 7. 다음 액션

Nick이 결정 1~4 정해주면 → 졸업 실행. 권장은 **결정4=A(단원2 시범 먼저)** 이므로, 우선 단원2 자율 시범으로 orchestrator 형태를 확정한 뒤 일괄 졸업.
