<!-- 5_render/README.md -->

# 5_render — HyperFrames + GSAP 렌더

**입력**: `index_v1_x.html` + `config_v1_x.json` + `_assets/*.png`
**출력**: `raw_v1_x.mp4` (영상만, 음성 없음)

## 현 표준 (baseline = unit-01)
- index.html = v1.5 마스터 템플릿 + 단원 데이터
- HyperFrames CLI 로 render
- data-duration 자동 갱신 (audio + 2s)
- 도구: 이미 검증됨

## 작성 후보 (compact 후)
- `INDEX_HTML_TEMPLATE.md` — v1.5 마스터 템플릿 구조 명세
- `RENDER_PIPELINE.md` — HyperFrames 실행 절차
- (필요 시) `seeds/unit_02_index.html`
