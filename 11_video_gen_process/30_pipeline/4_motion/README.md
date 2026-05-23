<!-- 4_motion/README.md -->

# 4_motion — ken burns / pan / scene_times

**입력**: `1_storyboard/seeds/<unit>.md` + `3_image/_assets/*.png`
**출력**: `config_v1_x.json` (motion 부분 + scene textbox + image path + scene_times)

## 현 표준 (baseline = unit-01)
- ken burns: scale_from 1.0 → scale_to 1.04~1.06
- pan_x: -3 ~ +2 %
- scene_times: s1=0 / s2=5 / s3=25 / s4=50 / s5=80 / s6=105 / end=115
- S4 중간 spike (65s) 강조
- baseline: `../../10_reference/02_baseline_unit01.md` §5

## 작성 후보 (compact 후)
- `MOTION_TEMPLATE.md` — 6장면 ken burns + scene_times 표준
- `CONFIG_SCHEMA.md` — config_v1_x.json schema 명세
- `seeds/unit_02_config.json` (첫 신규)
