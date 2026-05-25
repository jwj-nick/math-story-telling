---
name: se-video-narration
description: 영상 제작 시스템의 단계 [영상 2] 나레이션 스킬. 단계 [영상 1] 스토리보드의 나레이션 시드를 받아 실제 발화용 텍스트 + SSML 풀스펙 + 음성 합성 (mp3) 을 작성한다. 입력 (스토리보드 / 정체성 = 시청자·약속·톤 / TTS 도구 선택 / (옵션) 음성 매핑 / (옵션) 옛 baseline SSML) 을 받아 동작 (입력 align → Q&A → 나레이션 정련 → SSML 마크업 → TTS 합성 → 길이 검증 → 자체 평가 → 출력) 진행. math-story-telling 의 영상 나레이션 작성, SSML 마크업, TTS 합성 + 길이 사전 검증, 인물별 음성 매핑 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료 (`40_experiments/exp-NNN/3-storyboard.md`, INTEGRATED_PLAN §5.1.2·§8, `50_channel/season-1-ancient/unit-NN/narration_v1_5.xml` baseline) 를 참조만 함. 외부 도구 호출: edge-tts (Python CLI) 또는 ElevenLabs API.
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 영상 2 나레이션 (NR1~NR7)
  ssot: 11_video_gen_process/70_tools/se-video-narration/SKILL.md
  version: "0.1"
  status: 시드 (시범 실행 후 retrospective 로 정련 예정)
allowed-tools: Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch
---

# se-video-narration — 영상 2 나레이션 스킬

본 스킬은 영상 제작 시스템의 단계 [영상 2]. 단계 [영상 1] 스토리보드의 나레이션 시드를 받아 *실제 발화용 텍스트* + SSML 풀스펙 + 음성 합성 (mp3) 을 작성한다. 출력은 다음 단계 [영상 5] 렌더 (`se-video-render`) 및 [영상 6] 합성 (`se-video-compose`) 의 직접 입력.

상위 frame: [INTEGRATED_PLAN](../../00_charter/INTEGRATED_PLAN.md) §5.0 skill chain / §5.5 단계 [영상 2] / §8 결정 1·2.

원칙:
- 본 스킬은 외부 자료를 **참조** 한다. 외부를 변경 X.
- 호출자가 입력 일부만 줘도 됨 — 동작 초기 단계에서 보강.
- **외부 도구 호출 첫 단계** — TTS 엔진 (edge-tts / ElevenLabs / etc).
- 도구 비교는 [`tts-tools-guide.md`](./tts-tools-guide.md) 참조.

---

## body 시범 진행 중

본 스킬의 body 는 STEP 1·2·3 패턴 동일 — *시범 실행 후 reverse-engineering* 으로 정형화 예정.

- 시범 결과물 (예정):
  - `40_experiments/exp-002-build-unit01/4-narration.txt` (텍스트)
  - `40_experiments/exp-002-build-unit01/4-narration.xml` (SSML)
  - `40_experiments/exp-002-build-unit01/4-narration.mp3` (음성, gitignore)
- 도구 가이드: [`tts-tools-guide.md`](./tts-tools-guide.md)
- 진행 session log: [`../../50_sessions/0525_step4_skill_draft.md`](../../50_sessions/0525_step4_skill_draft.md)
