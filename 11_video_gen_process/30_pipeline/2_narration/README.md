<!-- 2_narration/README.md -->

# 2_narration — 나레이션 텍스트 + SSML + TTS

**입력**: `1_storyboard/seeds/<unit>.md`
**출력**: `narration_v1_x.txt` (TTS 입력) + `narration_v1_x.xml` (SSML 풀스펙) + `narration_v1_x.mp3` (TTS 산출)

## 현 표준 (baseline = unit-01)
- 단문 + 빈줄 (edge-tts pause 우회)
- SSML 풀스펙: break ~40회 + prosody rate=-5% + pitch+5% 1회 (극강조) + pitch+3% 1회 (키워드)
- 글자수 480~620 / 속도 4.5~5.5 자/초
- 어미: 다정한 어조 ("는요/이에요/거예요/답니다")
- baseline: `../../10_reference/02_baseline_unit01.md` §2

## 진행 우선순위 (compact 후)

### 🔴 ElevenLabs 전환 (D-005)
- baseline `narration_v1_5.xml` SSML 풀스펙 → ElevenLabs 직접 input
- 5인 voice 매핑 (D-005 보조)
- 무료 quota 10000자 / 시즌1 3000자 충분
- 도구: `python-elevenlabs` SDK 또는 REST API

### 🔴 length dry run 분기 (D5 from 260520 insight)
- narration 작성 직후 TTS 1회 합성 → ffprobe 길이 측정 → 95~120s 벗어나면 narration 재조정
- 빌드 진입 전에 처리
- 도구: `70_tools/length_check.sh`

## 작성 후보
- `ELEVENLABS_INTEGRATION.md` — 가입·키·SDK 사용·voice 매핑
- `SSML_PATTERN_GUIDE.md` — unit-01 패턴 정리 + 13단원 적용 표준
- `VOICE_MAPPING_5인.md` — 시즌1 인물별 voice 후보·시청 결과
- `LENGTH_DRY_RUN.md` — 검증 절차 표준
- `seeds/unit_02_brahmagupta.{txt,xml}` (첫 신규)
