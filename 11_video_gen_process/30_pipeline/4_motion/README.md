<!-- 4_motion/README.md -->

# 4_motion — ken burns / pan / 장면 시간

**입력**: `../1_storyboard/seeds/<단원>.md` + `../3_image/_assets/*.png`
**출력**: `seeds/<단원>_config.json` (모션 부분 + 장면 텍스트박스 + 이미지 path + 장면 시간)

## 현 표준 (1편 = 에라토스테네스 기준)

- ken burns: 시작 스케일 1.0 → 끝 스케일 1.04~1.06
- pan_x: -3 ~ +2 %
- 장면 시간: s1=0 / s2=5 / s3=25 / s4=50 / s5=80 / s6=105 / end=115
- S4 중간 spike (65초) 강조
- 1편 정밀 데이터: `../../10_reference/02_baseline_unit01.md` §5

## 진행 우선순위

### 🟡 핵심 시각화 30초 (집중 단원만)

(INTEGRATED_PLAN §4.1 + §7 결정 ⑬ — 채택 시)

- S4 (결정적 순간) 30초를 AI 이미지가 아니라 JSXGraph / D3.js 동적 다이어그램으로 교체
- 1편 후보: 막대기+그림자 + 시에네 우물 + 지구 곡률 + 7.2°=1/50바퀴 + 둘레 풀려나옴

### 🟡 배경음 + 효과음

(INTEGRATED_PLAN §4.3 + §7 결정 ⑭ — 채택 시)

- 시대 팔레트별 배경음 1곡 (고대 그리스·중세 인도·중세 이슬람·근세 초) — CC0 무료 출처
- 결정적 순간 효과음 (sting) — 집중 단원만 1~2회
- 도구: ffmpeg 음향 합성

## 작성 후보

- `MOTION_TEMPLATE.md` — 6장면 ken burns + 장면 시간 표준
- `CONFIG_SCHEMA.md` — config.json schema 명세
- `BGM_SFX_SPEC.md` — 배경음·효과음 표준 + CC0 출처 라이브러리
- `seeds/unit_02_brahmagupta_config.json` (첫 신규)
