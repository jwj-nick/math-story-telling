<!-- 6_final/README.md -->

# 6_final — ffmpeg 합성 + 표지

**입력**: `../5_render/seeds/<단원>_raw.mp4` + `../2_narration/seeds/<단원>_narration.mp3`
**출력**: `seeds/<단원>_final.mp4` + `seeds/<단원>_poster.jpg`

## 현 표준 (1편 = 에라토스테네스 기준, 이미 검증됨)

- ffmpeg: `-map 0:v -map 1:a -c:v copy -c:a aac -shortest`
- 파일 < 25MB (1280×720, AAC 128k)
- 음성·영상 sync 오차 ±0.3초 이내
- 표지 jpg = S1 화면 추출
- 도구: 이미 작동 중

## 본 배포로의 승격 흐름

검증 완료 → `../../../50_channel/people/<인물>/<에피소드>/` (원본) + `../../../50_channel/seasons/<시즌>/<단원>/` (시청자 진입)

→ INTEGRATED_PLAN §7 결정 ⑥ (디렉토리 이중 트리 재배치) 와 연동.

## 작성 후보

- `FFMPEG_RECIPE.md` — 합성 옵션 표준
- `POSTER_EXTRACT.md` — 표지 추출 절차
- `PROMOTE_TO_CHANNEL.md` — `50_channel/` 로 이동 절차
