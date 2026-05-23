<!-- 30_pipeline/README.md -->

# 30_pipeline — 영상 빌드 6단계 sandbox

영상 1편 빌드 파이프라인의 각 단계를 독립적으로 실험·튜닝하는 공간.

단일 진입점: [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md) — 이 프로젝트의 전체 맥락.

## 6단계

| dir | 단계 | 입력 | 출력 |
|---|---|---|---|
| `1_storyboard/` | 6장면 마스터 작성 | 단원 메타 + 인물 사실 | 스토리보드 MD |
| `2_narration/` | 나레이션 텍스트·음성 합성 | 스토리보드 | 텍스트 + SSML + 음성 mp3 |
| `3_image/` | AI 이미지 프롬프트·생성·캐릭터 일관성 | 스토리보드 + 캐릭터 시트 | 프롬프트 MD + 이미지 파일들 |
| `4_motion/` | ken burns / pan / 장면 시간 | 스토리보드 + 이미지 | config.json (모션 + 장면 시간) |
| `5_render/` | HyperFrames + GSAP 렌더 | index.html + config + assets | raw mp4 (음성 없음) |
| `6_final/` | ffmpeg 합성 (영상 + 음성) | raw mp4 + 음성 mp3 | final mp4 + 표지 jpg |

## 운영 규칙

- 각 단계 폴더 = 그 단계의 독립 sandbox
- 단계 간 인터페이스는 명확한 파일 (스토리보드 MD / 나레이션 텍스트 등)
- 단계별 실험은 `../40_experiments/exp-NNN-주제/` 에서 실행. 본 폴더는 표준·도구 보관소
- 단계별 README 에 "현재 표준 절차 + 도구 후보 + 알려진 함정" 정리

## 단계별 진행 우선순위

INTEGRATED_PLAN §4 (품질 강화 5요소) 채택 시 우선순위:

| 우선 | 단계 | 작업 |
|---|---|---|
| 🔴 | `2_narration/` | 고급 음성 합성 (ElevenLabs) + 길이 사전 검증 + 5인 음성 매핑 |
| 🔴 | `3_image/` | Midjourney `--cref` + 캐릭터 시트 분리 + 시즌1 5인 시트 |
| 🟡 | `1_storyboard/` | 단원 메타 기반 스토리보드 시드 자동 생성 |
| 🟡 | `4_motion/` | 모션 시드 + ken burns 표준화 + 배경음·효과음 트랙 추가 |
| 🟢 | `5_render/` | HyperFrames 안정 (이미 검증됨) |
| 🟢 | `6_final/` | ffmpeg 안정 (이미 검증됨) |
