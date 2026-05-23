<!-- 70_tools/README.md -->

# 70_tools — 자동화 스크립트

본 sub-project 의 빌드·검증·평가 자동화 도구.

## 분류
- **빌드 도구**: TTS·render·ffmpeg pipeline 자동화
- **검증 도구**: length dry run, sync 오차 측정, audit
- **변환 도구**: meta.json → storyboard seed, 프롬프트 → MJ 사양

## 외부 skill 과의 관계
- skill SSOT: `../../.claude/skills/se_story_video_v1_5/` (mirror) / `../../10_system/30_skills/se_story_video_v1_5/` (canonical)
- 본 폴더는 skill 보조 도구 (skill 자체는 외부 SSOT 유지)
- 본 폴더에서 새 도구 시드 → 검증 후 skill Phase 또는 신규 skill 로 promote

## 후보 (compact 후)
- `length_check.sh` — narration.txt → edge-tts/ElevenLabs → ffprobe → ±range
- `mj_prompt_convert.py` — `image_prompts.md` → MJ `--style raw --ar 16:9 --v 6.1 --cref ...`
- `storyboard_seed_from_meta.py` — `meta.json` + `people/<ref>.md` → storyboard 시드
- `narration_seed_from_storyboard.py` — storyboard → narration.txt 시드 (SSML 포함)
- `audit_video.sh` — final.mp4 메트릭 audit (`se_ncc_audit_video` 시드)
- `promote_to_channel.sh` — `40_experiments/exp-NNN/outputs/final.mp4` → `50_channel/people/<ref>/<ep>/`
