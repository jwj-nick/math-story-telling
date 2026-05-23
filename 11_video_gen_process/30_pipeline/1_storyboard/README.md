<!-- 1_storyboard/README.md -->

# 1_storyboard — 6장면 마스터 작성

**입력**: `../../../30_content/units/NN/meta.json` (인물·핵심 개념·이야기 후크) + `../../../30_content/people/<인물>.md`
**출력**: `seeds/<단원>_storyboard.md` (6장면 × 시간·시각 구성·이미지·모션·텍스트·나레이션 글자수)

## 현 표준 (1편 = 에라토스테네스 기준)

- 6장면 구조: S1 (타이틀) / S2 (시대) / S3 (인물) / S4 (결정적 순간) / S5 (수학 연결) / S6 (마무리)
- 합계 95~120초, 나레이션 480~620자
- 1편 정밀 데이터: `../../10_reference/02_baseline_unit01.md` §3

## 알려진 함정

- S2 (시대 풍경) 에 인물 미포함 원칙 — 1편에서 우연히 그렇게 됨, 표준화 필요
- S4 길이 25~30초 + 중간 강조 spike 1회
- 새 문장 시작 = 새 장면 또는 새 강조

## 작성 후보

- `STORYBOARD_TEMPLATE.md` — 단원 메타 → 스토리보드 시드 변환 표준
- `seeds/unit_02_brahmagupta.md` (브라마굽타)
- `seeds/unit_03_al-khwarizmi.md` (알콰리즈미)
- `seeds/unit_04_diophantus.md` (디오판토스)
- `seeds/unit_05_descartes.md` (데카르트)

→ INTEGRATED_PLAN §7 결정 ⑨ (시드 동시 작성 vs 순차) 와 연동.
