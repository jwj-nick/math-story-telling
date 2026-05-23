<!-- 40_experiments/README.md -->

# 40_experiments — 실험 단위

각 실험 = `exp-NNN-주제/` 폴더. 가설·setup·결과·회고 4섹션.

단일 진입점: [`../00_charter/INTEGRATED_PLAN.md`](../00_charter/INTEGRATED_PLAN.md) — 검증 가설 (§9) 과 직접 연동.

## 명명 규약

```
exp-001-elevenlabs-voice-compare/
exp-002-mj-cref-character-consistency/
exp-003-length-dry-run-automation/
exp-004-storyboard-seed-from-meta/
exp-005-unit02-brahmagupta-pilot/
```

## 폴더 구조 표준

각 실험 폴더:
```
exp-NNN-주제/
├── README.md           가설 + setup + 결과 + 회고
├── inputs/             실험 입력 자료
├── outputs/            실험 산출물 (음성, 이미지, 로그 등)
└── _evaluation.md      평가 → 60_evaluation/ 로 승격 시드
```

## 실험 → 표준 승격 흐름

```
exp-NNN/_evaluation.md
   │
   ▼ (가치 있는 발견)
60_evaluation/<주제>.md (정제·일반화)
   │
   ▼ (검증된 표준)
20_principles/<주제>.md (이 프로젝트 시드)
   │
   ▼ (math-story-telling SSOT 로)
../../10_system/10_principles/STORY_VIDEO_v1_5.md 갱신
```

## 인덱스

`_index.md` 에 모든 실험 한 줄씩 (상태: planned / running / done / archived).

## 실험 후보 (INTEGRATED_PLAN §9 검증 가설 연동)

- 검증 가설 1 (표준 일반화) → 1단계 완료 후 다음 단원 빌드 실험
- 검증 가설 2 (핵심 시각화 30초가 영상 천장을 올리는가) → 1편 S4 30초만 재제작 실험
- 검증 가설 3 (음향 추가가 영상 톤을 격상시키는가) → 1편 영상에 음향만 추가 실험
- ElevenLabs 음성 비교 → `exp-001-elevenlabs-voice-compare/`
- Midjourney 캐릭터 일관성 검증 → `exp-002-mj-cref-character-consistency/`
- 길이 사전 검증 자동화 → `exp-003-length-dry-run-automation/`
- 단원 메타 → 스토리보드 시드 자동 변환 → `exp-004-storyboard-seed-from-meta/`
