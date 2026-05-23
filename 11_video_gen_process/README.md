<!-- 11_video_gen_process/README.md -->

# 11_video_gen_process — 영상 제작 프로젝트

수학자 인물 영상을 만드는 일을, **단계별 sandbox·실험·평가·표준화** 하는 작업 공간.

최종 산출물(검증된 영상)은 `../50_channel/` 로 옮긴다. 여기서는 **연구·실험** 만.

---

## 단일 진입점

⭐ **[`00_charter/PURPOSE.md`](./00_charter/PURPOSE.md)** — 절대 변하지 않는 이 프로젝트의 목적
⭐ **[`00_charter/INTEGRATED_PLAN.md`](./00_charter/INTEGRATED_PLAN.md)** — 현재 통합 계획

**이 디렉토리는 영상을 양산하는 곳이 아니다.** 영상 제작 시스템 (프로세스 + 자동화) 을 구축하는 곳이다. 디렉토리 이름 `video_gen_process` 가 말하는 그대로 — process 가 핵심.

INTEGRATED_PLAN 한 편으로 프로젝트 전체를 이해할 수 있다: 시스템 정의, 3단계 진화 모델 (수동 깊이 → 반복 적용 → 자동화), 1편 출발점, 흡수할 능력 5가지, 진화 원칙 7가지, 결정 질문들, 자율 작업 5건, 검증 가설.

다른 charter 문서 (`VISION.md` / `GOALS.md` / `DECISIONS.md`) 는 INTEGRATED_PLAN 으로 통합되어 deprecated. 이력 보존용.

---

## 디렉토리

| dir | 역할 |
|---|---|
| `00_charter/` | **단일 진입점 `INTEGRATED_PLAN.md`** + deprecated 보존 (`VISION` / `GOALS` / `DECISIONS`) |
| `10_reference/` | 외부 자료 발췌. `_origin.md` 에 모든 원본 path 인덱스 |
| `20_principles/` | 영상 제작 표준 — 외부 표준 (`../10_system/10_principles/STORY_VIDEO_v1_5.md`) 의 갱신 시드 |
| `30_pipeline/` | 6단계 sandbox: `1_storyboard` → `2_narration` → `3_image` → `4_motion` → `5_render` → `6_final` |
| `40_experiments/` | 실험 단위 (`exp-NNN-주제/`). 각 실험: 가설·setup·결과·회고 |
| `50_sessions/` | 본 프로젝트 내 세션 기록 (라운드 기반) |
| `60_evaluation/` | 비교 평가·회고 누적. 정제분은 `../10_system/50_insights/` 로 promote |
| `70_tools/` | 자동화 스크립트 (음성 합성·이미지·렌더·검증 등) |
| `90_archive/` | 폐기 실험·옛 버전 안전망 |

---

## 새 세션 진입 순서

1. `../CLAUDE.md` — math-story-telling 전체 큰 그림
2. `../00_project_hub/20_plan/current-plan.md` — 큰 그림 현재 계획
3. **`00_charter/INTEGRATED_PLAN.md`** ← 본 프로젝트 단일 진입점
4. (필요 시) `10_reference/_origin.md` — 외부 자료가 어디서 왔는지
5. (필요 시) `50_sessions/_index.md` — 최근 라운드

---

## 외부 의존

상세 인덱스는 [`10_reference/_origin.md`](./10_reference/_origin.md). 본 프로젝트가 참조하는 영상 표준·스킬·인물 자료·산출물 위치가 한 곳에 정리되어 있다.

---

## 산출물 흐름 — 연구에서 본 배포까지

```
[40_experiments/exp-NNN/]       실험 산출물 (영상·이미지·로그)
        │
        ▼ (검증·평가 통과)
[60_evaluation/]                비교 평가 + 회고
        │
        ▼ (정제·일반화)
[20_principles/]                본 프로젝트의 갱신된 표준 시드
        │
        ▼ (외부 표준으로 승격)
[../10_system/10_principles/STORY_VIDEO_v1_5.md]
[../10_system/50_insights/<date>_<unit>.md]
        │
        ▼ (단원 본격 빌드)
[../50_channel/people/<인물>/<에피소드>/]      최종 산출물 원본
[../50_channel/seasons/<시즌>/<단원>/]         시청자 진입 view
```

---

## 변경 이력

- 2026-05-23: 신규. 풀세팅 9 디렉토리.
- 2026-05-24: 단일 진입점 `INTEGRATED_PLAN.md` 로 재정렬. 옛 표기 (sub-project, R-NNN, v1.5/v1.6) 폐기.
