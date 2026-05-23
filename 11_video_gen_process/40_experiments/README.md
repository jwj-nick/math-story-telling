<!-- 40_experiments/README.md -->

# 40_experiments — 실험 단위

각 실험 = `exp-NNN-주제/` 폴더. 가설·setup·결과·회고 4섹션.

## 명명 규약

```
exp-001-elevenlabs-voice-compare/
exp-002-mj-cref-character-consistency/
exp-003-length-dry-run-automation/
exp-004-storyboard-seed-from-meta-json/
exp-005-unit02-brahmagupta-pilot/
```

## 폴더 구조 표준

각 실험 폴더:
```
exp-NNN-주제/
├── README.md           가설 + setup + 결과 + 회고
├── inputs/             실험 입력 자료
├── outputs/            실험 산출물 (mp3, png, log 등)
└── _evaluation.md      평가 → 60_evaluation/ 로 promote 시드
```

## 실험 → 표준 promote 흐름

```
exp-NNN/_evaluation.md
   │
   ▼ (가치 있는 발견)
60_evaluation/<주제>.md (정제·일반화)
   │
   ▼ (검증된 표준)
20_principles/<주제>.md (sub-project 시드)
   │
   ▼ (math-story-telling SSOT 로)
../../10_system/10_principles/STORY_VIDEO_v1_5.md 갱신
```

## 인덱스

`_index.md` 에 모든 실험 한 줄씩 (상태: planned / running / done / archived).

## 후보 (compact 후 시작)

- exp-001: ElevenLabs voice 5인 비교 (Korean voices)
- exp-002: MJ `--cref` 캐릭터 일관성 검증 (5장 같은 인물)
- exp-003: length dry run 스크립트 (narration → mp3 → ffprobe → ±range 검증)
- exp-004: meta.json → storyboard seed 자동 변환 시도
- exp-005: unit-02 (브라마굽타) 파일럿 풀빌드
