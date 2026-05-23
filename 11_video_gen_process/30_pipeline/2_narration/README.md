<!-- 2_narration/README.md -->

# 2_narration — 나레이션 텍스트 + SSML + 음성 합성

**입력**: `../1_storyboard/seeds/<단원>.md`
**출력**: `seeds/<단원>_narration.txt` (텍스트) + `seeds/<단원>_narration.xml` (SSML 풀스펙) + `seeds/<단원>_narration.mp3` (음성 산출)

## 현 표준 (1편 = 에라토스테네스 기준)

- 단문 + 빈줄 (edge-tts 의 pause 우회 기법)
- SSML 풀스펙: break (쉼) 약 40회 + prosody (속도 -5%) + pitch +5% 1회 (극강조) + pitch +3% 1회 (키워드)
- 글자수 480~620 / 속도 4.5~5.5 자/초
- 어미: 다정한 어조 ("는요/이에요/거예요/답니다")
- 1편 정밀 데이터: `../../10_reference/02_baseline_unit01.md` §2

## 진행 우선순위

### 🔴 고급 음성 합성 (ElevenLabs) 전환

(INTEGRATED_PLAN §7 결정 ④ — 채택 시)

- 1편의 SSML 풀스펙 → ElevenLabs 직접 입력 가능
- 시즌1 5인 음성 매핑 결정 필요
- 무료 quota 10000자 / 시즌1 합계 약 3000자 → 무료 충분
- 도구: `python-elevenlabs` SDK 또는 REST API

### 🔴 길이 사전 검증

(INTEGRATED_PLAN §3.3 4가지 갱신 중 하나 — 자율 작업 1)

- 나레이션 작성 직후 음성 1회 테스트 합성 → ffprobe 길이 측정 → 95~120초 벗어나면 나레이션 재조정
- 본 빌드 진입 전에 처리
- 도구: `../../70_tools/length_check.sh`

## 작성 후보

- `ELEVENLABS_INTEGRATION.md` — 가입·키·SDK 사용·음성 매핑
- `SSML_PATTERN_GUIDE.md` — 1편 패턴 정리 + 단원별 적용 표준
- `VOICE_MAPPING_5인.md` — 시즌1 인물별 음성 후보·시청 결과
- `LENGTH_DRY_RUN.md` — 검증 절차 표준
- `seeds/unit_02_brahmagupta_narration.{txt,xml}` (첫 신규)
