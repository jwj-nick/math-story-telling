<!-- 11_video_gen_process/README.md -->

# 11_video_gen_process

> Sub-project: **영상 잘 만들기에 특화한 R&D 작업 공간.**
> 본격 시작: 2026-05-23 (math-story-telling C R0+R1 zoom out 후 sub-project 분리)

---

## 한 줄

"수학자 인물 영상" 제작 파이프라인을 **단계별로 sandbox·실험·평가·표준화**하는 R&D 공간.
최종 산출물(검증된 영상)은 `../50_channel/` 로 promote. 여기서는 **R&D만**.

---

## 디렉토리

| dir | 역할 |
|---|---|
| `00_charter/` | sub-project 헌장 — `VISION.md` / `GOALS.md` / `DECISIONS.md` |
| `10_reference/` | 외부 자료 발췌 (chatlog/plan/baseline). `_origin.md` 에 원본 path. |
| `20_principles/` | 영상 표준 (`../10_system/10_principles/STORY_VIDEO_v1_5.md` mirror + 확장) |
| `30_pipeline/` | 단계별 sandbox: `1_storyboard` → `2_narration` → `3_image` → `4_motion` → `5_render` → `6_final` |
| `40_experiments/` | 실험 단위 (`exp-NNN-주제/`). 각 실험: 가설·setup·결과·회고. |
| `50_sessions/` | 라운드 기반 세션 log (chatlog 패턴, 본 sub-project 한정) |
| `60_evaluation/` | 비교 평가 결과·회고 누적. 정제분만 `../10_system/50_insights/` 로 promote |
| `70_tools/` | 자동화 스크립트 (TTS·ffmpeg·render·dry-run length 측정 등) |
| `90_archive/` | 폐기 실험·옛 버전 안전망 |

---

## 새 세션 entry point

1. `../CLAUDE.md` (전체 프로젝트)
2. `../00_project_hub/20_plan/current-plan.md` (math-story-telling 큰 그림 + 본 sub-project 진입 안내)
3. **이 README + `00_charter/VISION.md` + `00_charter/GOALS.md`** ← 본 sub-project entry
4. `10_reference/_origin.md` (외부 자료가 어디서 왔는지)
5. `50_sessions/_index.md` (최근 라운드)

---

## 외부 의존 (참조만, 발췌 X — `10_reference/_origin.md` 참조)

| 종류 | 원본 path |
|---|---|
| 표준 SSOT | `../10_system/10_principles/STORY_VIDEO_v1_5.md` (R2에서 v1.6 갱신 예정) |
| skill (점검 대상) | `../.claude/skills/se_story_video_v1_5/` |
| 인물 19인 | `../30_content/people/*.md` |
| 단원 13 메타 | `../30_content/units/NN/meta.json` |
| baseline 산출물 | `../50_channel/season-1-ancient/unit-01/` |
| unit-01 v1.5 회고 | `../10_system/50_insights/260520_unit01_story_video_v1_5.md` |
| insights index | `../10_system/50_insights/_index.md` |
| Nick_TODO | `../00_project_hub/30_history/Nick_TODO.md` (T1 ElevenLabs / T2 AI 이미지) |

---

## 산출물 흐름 (R&D → promote)

```
[40_experiments/exp-NNN/]   실험 산출물 (mp4·이미지·로그)
        │
        ▼ (검증·평가 통과)
[60_evaluation/]            비교 평가 + 회고
        │
        ▼ (정제·일반화)
[20_principles/]            본 sub-project 의 갱신된 표준 (v1.6 시드)
        │
        ▼ (math-story-telling SSOT 로 promote)
[../10_system/10_principles/STORY_VIDEO_v1_5.md]
[../10_system/50_insights/<date>_<unit>_v1_5.md]
        │
        ▼ (단원 본격 빌드)
[../50_channel/people/<ref>/<ep>/]  최종 산출물 원본
[../50_channel/seasons/season-N/unit-NN/]  view
```

---

## 변경 이력

- 2026-05-23: 신규. C R1 §1.4 (시즌1 5편 zoom in) 후 sub-project로 분리. 풀세팅 9 sub-dir.
