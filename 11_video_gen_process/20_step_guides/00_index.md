<!-- 20_step_guides/00_index.md / STEP별 심화 가이드 인덱스 + 템플릿 + 계획 -->

# STEP별 심화 가이드 — 인덱스 · 템플릿 · 생성 계획

> **목적**: 영상 제작 시스템(11_video_gen_process)의 8단계 각각을 **깊이 있게** 문서화한다.
> 단순 사용법이 아니라 — workflow / 사용 자원 / 입출력 + **개선 아이디어 + 창의적 고급 workflow + 고급 콘텐츠 생성법**까지.
> **상위 frame**: [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md), [`../00_charter/PURPOSE.md`](../00_charter/PURPOSE.md)
> **생성 방식**: STEP별 background agent 1개씩 (각 문서 독립 심화)
> **생성 일자**: 2026-05-29

---

## 1. 문서 목록 (8 STEP)

| 문서 | STEP | 단계 | skill | 실제 산출물 (exp-002) | 상태 |
|---|---|---|---|---|---|
| [01_step1_narrative.md](./01_step1_narrative.md) | 1 | 서사 | `se-people-narrate` | 1-narrative.md | ✅ 완료 |
| [02_step2_story.md](./02_step2_story.md) | 2 | 스토리 | `se-video-story` | 2-story-seed.md | ✅ 완료 |
| [03_step3_storyboard.md](./03_step3_storyboard.md) | 3 | 스토리보드 | `se-video-storyboard` | 3-storyboard.md | ✅ 완료 |
| [04_step4_narration.md](./04_step4_narration.md) | 4 | 나레이션(음성) | `se-video-narration` | 4-narration.* + voice-pool §0 | ✅ 완료 |
| [05_step5_image.md](./05_step5_image.md) | 5 | 이미지 | `se-video-image` | 5-image_prompts.md + 5-images/ | ✅ 완료 |
| [06_step6_motion.md](./06_step6_motion.md) | 6 | 모션 | `se-video-motion` | 6-motion-config.json | ✅ 완료 |
| [07_step7_render.md](./07_step7_render.md) | 7 | 렌더 | `se-video-render` | clips/ (FFmpeg zoompan) | ✅ 완료 |
| [08_step8_compose.md](./08_step8_compose.md) | 8 | 합성 | `se-video-compose` | 8-final.mp4 (예정) | ✅ 완료 |

---

## 2. 공통 문서 템플릿 (9 섹션)

각 문서는 아래 9개 섹션을 **정확히** 따른다.

### 1. Step 개요
- 이 step이 무엇을 하는가 (한 문단)
- 4축(A 개념 / B 흥미 / C 언어 / D 문제) 중 어디에 기여
- 8단계 파이프라인에서의 위치 (선행/후행 step)
- 이 step의 *본질적 난제* 1~2개

### 2. Workflow (절차)
- 입력 align → 처리 → 출력의 단계별 흐름
- 실제 동작 순서 (skill의 NR/IM/… 액션 또는 시범 절차)
- 의사결정 포인트 (분기)

### 3. Skill / Agent / Tools / Context
- 사용하는 skill (SKILL.md) + version + 핵심 동작
- 사용하는 외부 도구 (TTS/이미지/FFmpeg 등) + 선택 근거
- 참조 context (SSOT 파일: voice-pool §0, TONE_STRUCTURE, storyboard 등)
- agent 활용 여부

### 4. User Input (Nick 입력)
- Nick이 무엇을 / 언제 / 어떤 형식으로 입력하는가
- 필수 vs 선택 입력
- HITL(사람 개입) 지점

### 5. Step Output (산출물)
- 산출 파일 형식 + 위치 규약
- 다음 step의 입력으로 어떻게 연결되는가
- 품질 검증 기준 (자동 + Nick)

### 6. 현재 구현 (exp-002 실제 사례)
- unit01(에라토스테네스) 에서 실제로 어떻게 했는가 — 구체적 인용
- 실제 겪은 시행착오·결정 (예: TTS 도구 변천, voice 교체, billing 장벽)
- 현재 구현의 강점과 한계

### 7. 개선 방향 탐색 / 아이디어
- 현재 한계를 어떻게 줄일까 (실현 가능한 단기 개선)
- 자동화·효율·품질 관점 아이디어
- 실패/리스크 요소와 대응

### 8. 고급 Workflow (상상력·창의력)
- 현재를 뛰어넘는 *더 정교한* workflow 설계 (미래형)
- AI·에이전트·파이프라인 자동화의 고급 활용
- 다른 도메인/기법 차용 (영화·게임·교육공학 등)
- "이상적이라면 이렇게" 비전

### 9. 고급 Contents 생성 방법 (품질 도약)
- 콘텐츠 자체의 질을 한 단계 올리는 구체 기법
- 학습 효과·몰입·정서 연결 강화 방법
- 시리즈 정체성·일관성·확장성 관점
- 이 step에서만 가능한 "차별화 포인트"

---

## 3. 작성 원칙

- **구체성**: 실제 파일(SKILL.md, 산출물)을 읽고 인용. 추상론 금지.
- **창의성**: 섹션 7~9는 현재 한계를 넘는 아이디어를 적극 발휘.
- **독립성**: 각 문서는 단독으로 읽혀도 완결.
- **한국어**, 표·예시 적극 활용.
- **외부 의존 0**: 본 sub-project 안에서만 작성, 외부 디렉토리 변경 금지.

---

## 4. 생성 방법 (background agent)

각 STEP마다 background agent 1개:
- 입력: 본 템플릿(00_index) + 해당 skill + 실제 산출물 + INTEGRATED_PLAN/PURPOSE
- 출력: `NN_stepN_name.md` (9섹션)
- 8개 병렬 background → 완료 시 본 인덱스 상태 ✅ 갱신

---

## 5. 변경 이력

- 2026-05-29: 신규. 8 STEP 심화 가이드 디렉토리 + 템플릿 + 계획 수립. background agent 생성 시작.
