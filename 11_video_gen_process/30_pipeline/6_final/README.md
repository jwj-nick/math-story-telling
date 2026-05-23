<!-- 6_final/README.md -->

# 6_final — ffmpeg 합성 + 포스터

**입력**: `raw_v1_x.mp4` + `narration_v1_x.mp3`
**출력**: `final_v1_x.mp4` + `poster_v1_x.jpg`

## 현 표준 (baseline = unit-01)
- ffmpeg: `-map 0:v -map 1:a -c:v copy -c:a aac -shortest`
- 파일 < 25MB (1280×720, AAC 128k)
- sync 오차 ±0.3s 이내
- poster.jpg = S1 화면 추출
- 도구: 이미 검증됨

## promote 흐름
검증 완료 → `../../../50_channel/people/<ref>/<ep>/` (원본) + `../../../50_channel/seasons/season-N/unit-NN/` (view)

## 작성 후보 (compact 후)
- `FFMPEG_RECIPE.md` — 합성 옵션 표준
- `POSTER_EXTRACT.md` — 포스터 추출 절차
- `PROMOTE_TO_CHANNEL.md` — 50_channel/ 로 이동 절차
