<!-- 30_pipeline/README.md -->

# 30_pipeline — 단계별 sandbox

영상 1편 빌드 파이프라인의 **각 단계를 독립적으로 실험·튜닝**하는 공간.

## 단계

| dir | 단계 | 입력 | 출력 |
|---|---|---|---|
| `1_storyboard/` | 6장면 마스터 작성 | meta.json + 인물.md | storyboard_v1_x.md |
| `2_narration/` | 나레이션 텍스트·SSML | storyboard | narration.txt + narration.xml + (TTS) .mp3 |
| `3_image/` | AI 이미지 프롬프트·생성·캐릭터 시트 | storyboard + 인물 시트 | image_prompts.md + _assets/*.png |
| `4_motion/` | ken burns / pan / scene_times | storyboard + 이미지 | config.json (motion 부분) |
| `5_render/` | HyperFrames + GSAP 렌더 | index.html + config + assets | raw.mp4 |
| `6_final/` | ffmpeg 합성 (영상 + TTS) | raw.mp4 + narration.mp3 | final.mp4 + poster.jpg |

## 운영 규칙

- 각 단계 폴더는 **그 단계 독립 sandbox**
- 단계 간 인터페이스는 명확한 파일 (storyboard.md / narration.txt 등)
- 단계별 실험은 `40_experiments/exp-NNN-주제/` 에서 실행, 본 폴더는 표준·도구 보관소
- 단계별 README 에 "현재 표준 절차 + 도구 후보 + 알려진 함정" 정리

## 단계별 진행 우선순위 (compact 후)

R0+R1 발견 기반:

1. 🔴 **2_narration**: ElevenLabs 전환 + length dry run + 5인 voice 매핑
2. 🔴 **3_image**: MJ `--cref` + 캐릭터 시트 분리 + 19인 시트
3. 🟡 **1_storyboard**: meta.json 기반 시드 자동 생성
4. 🟡 **4_motion**: config 시드 + ken burns 표준
5. 🟢 **5_render**: HyperFrames 안정 (이미 검증됨)
6. 🟢 **6_final**: ffmpeg 안정 (이미 검증됨)
