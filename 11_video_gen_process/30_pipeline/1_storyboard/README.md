<!-- 1_storyboard/README.md -->

# 1_storyboard — 6장면 마스터 작성

**입력**: `30_content/units/NN/meta.json` (persons[], key-concepts, story-hook) + `30_content/people/<ref>.md`
**출력**: `storyboard_v1_x.md` (6장면 × 시간·시각·이미지·모션·텍스트·나레이션 글자수)

## 현 표준
- 6장면 = S1(타이틀) / S2(시대) / S3(인물) / S4(결정적 순간) / S5(수학연결) / S6(마무리)
- 합계 95~120s, narration 480~620자
- baseline: `../../10_reference/02_baseline_unit01.md` §3

## 알려진 함정
- S2 (시대 풍경) 에 인물 미포함 원칙 — unit-01 에서 우연히 그렇게 됨, 표준화 필요
- S4 길이 25~30s + 중간 강조 spike 1회
- 새 문장 시작 = 새 장면 또는 새 강조

## 작성 후보 (compact 후)
- `STORYBOARD_TEMPLATE.md` — meta.json → storyboard 시드 변환 표준
- `seeds/unit_02_brahmagupta.md` (시즌1 첫 신규)
- `seeds/unit_03_al-khwarizmi.md`
- `seeds/unit_04_diophantus.md`
- `seeds/unit_05_descartes.md`
