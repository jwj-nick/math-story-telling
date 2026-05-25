<!-- 70_tools/README.md -->

# 70_tools — 본 프로젝트가 자체 정의하는 스킬 + 자동화 보조

이 폴더는 본 프로젝트 (`11_video_gen_process/`) 가 자체 정의·진화시키는 스킬의 SSOT 와 자동화 보조 스크립트가 함께 사는 자리.

단일 진입점: [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md)

## 분류

### 1. 본 프로젝트가 자체 정의하는 스킬 (SKILL.md)

INTEGRATED_PLAN §5 의 단계별로 한 폴더씩. SKILL.md 는 [agentskills.io spec](https://agentskills.io/specification) 준수 — `name` 필드는 lowercase + 숫자 + hyphen 만 (underscore 불가).

| 단계 | 스킬 폴더 | 상태 |
|---|---|---|
| [선정] | `se-people-pick/` | 시드 (시범 실행 대기) |
| [서사] | `se-people-narrate/` | (다음 단계) |
| [스토리] | `se-video-story/` | — |
| [영상 1~6] | `se-video-storyboard/` / `se-video-narration/` / `se-video-image/` / `se-video-motion/` / `se-video-render/` / `se-video-compose/` | — |

본 프로젝트 진행 중에는 SKILL.md 를 NCC 가 참조하여 동작 수행. 외부 `.claude/skills/` 슬래시 명령 등록은 단계 [이전] 에서.

### 2. 자동화 보조 스크립트 (후보)

- `length_check.sh` — 나레이션 텍스트 → 음성 합성 → ffprobe → 길이 ± 범위 검증
- `mj_prompt_convert.py` — `image_prompts.md` → Midjourney `--style raw --ar 16:9 --v 6.1 --cref ...`
- `storyboard_seed_from_meta.py` — `meta.json` + `people/<인물>.md` → 스토리보드 시드
- `narration_seed_from_storyboard.py` — 스토리보드 → 나레이션 텍스트 시드 (SSML 포함)
- `audit_video.sh` — final mp4 메트릭 audit
- `promote_to_channel.sh` — `40_experiments/exp-NNN/outputs/final.mp4` → `50_channel/people/<인물>/<에피소드>/`

## 외부 옛 자산과의 관계

본 프로젝트 안의 신규 스킬은 외부 옛 스킬 `se_story_video_v1_5/` (canonical: `../../10_system/30_skills/`, mirror: `../../.claude/skills/`) 의 6단계를 분해·대체 (§12.1). 본 프로젝트 완료 후 단계 [이전] 에서 외부 덮어쓰기 + sync.

본 프로젝트 진행 중 외부는 **참조만**. 변경 X (자체완결·외부 의존 0 원칙, §3.1).
