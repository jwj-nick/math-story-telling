<!-- 5_render/README.md -->

# 5_render — HyperFrames + GSAP 렌더

**입력**: `seeds/<단원>_index.html` + `../4_motion/seeds/<단원>_config.json` + `../3_image/_assets/*.png`
**출력**: `seeds/<단원>_raw.mp4` (영상만, 음성 없음)

## 현 표준 (1편 = 에라토스테네스 기준, 이미 검증됨)

- index.html = 마스터 템플릿 + 단원 데이터
- HyperFrames CLI 로 렌더
- data-duration 자동 갱신 (음성 길이 + 2초)
- 도구: 이미 작동 중

## 작성 후보

- `INDEX_HTML_TEMPLATE.md` — 마스터 템플릿 구조 명세
- `RENDER_PIPELINE.md` — HyperFrames 실행 절차
- (필요 시) `seeds/unit_02_index.html`
