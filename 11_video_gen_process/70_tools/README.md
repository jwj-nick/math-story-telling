<!-- 70_tools/README.md -->

# 70_tools — 자동화 스크립트

이 프로젝트의 빌드·검증·평가 자동화 도구.

단일 진입점: [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md)

## 분류

- **빌드 도구**: 음성 합성·렌더·ffmpeg 파이프라인 자동화
- **검증 도구**: 길이 사전 검증, sync 오차 측정, audit
- **변환 도구**: 단원 메타 → 스토리보드 시드, 프롬프트 → Midjourney 사양

## 외부 스킬과의 관계

- 스킬 SSOT: `../../.claude/skills/se_story_video_v1_5/` (mirror) / `../../10_system/30_skills/se_story_video_v1_5/` (canonical)
- 본 폴더는 스킬 보조 도구 (스킬 자체는 외부 SSOT 유지)
- 본 폴더에서 새 도구 시드 → 검증 후 스킬 단계 또는 새 스킬로 승격

## 후보

- `length_check.sh` — 나레이션 텍스트 → 음성 합성 → ffprobe → 길이 ± 범위 검증
- `mj_prompt_convert.py` — `image_prompts.md` → Midjourney `--style raw --ar 16:9 --v 6.1 --cref ...`
- `storyboard_seed_from_meta.py` — `meta.json` + `people/<인물>.md` → 스토리보드 시드
- `narration_seed_from_storyboard.py` — 스토리보드 → 나레이션 텍스트 시드 (SSML 포함)
- `audit_video.sh` — final mp4 메트릭 audit (`se_ncc_audit_video` 시드)
- `promote_to_channel.sh` — `40_experiments/exp-NNN/outputs/final.mp4` → `50_channel/people/<인물>/<에피소드>/`
