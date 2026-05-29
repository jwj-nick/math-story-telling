<!-- TONE_STRUCTURE.md / 영상 톤·구조 시스템 결정 v3.2 -->

# 영상 톤·구조 시스템 결정 v3.2 — Dialog + 존댓말 + Google Cloud TTS

> **v3.2 결정 일자**: 2026-05-26 (exp-002 STEP 4 v3.1 시범 + ElevenLabs Free tier 차단 발견)
> **v3 → v3.2 핵심 변경**:
>   1. **TTS 도구 재마이그**: ElevenLabs → **Google Cloud TTS** 1차
>      - 이유: ElevenLabs Free tier 의 library voice (Mono Beige/Onyu/Kyle/Mike) = HTTP 402 차단
>      - Google = 무료 한도 100만 chars/월 (본 영상 1편 = 550 chars → 1,800편/월) + ko-KR-Neural2 우수 + SSML 풀
>   2. **voice 매핑 갱신**: ko-KR-Neural2-A (Q) + ko-KR-Neural2-C (A)
>   3. **2차 옵션 유지**: ElevenLabs Starter $5/월 결제 시 library voice (Mono Beige/Mike) 사용 가능

> **v2 → v3 기존 변경 (유지)**:
>   1. **화자 어투 분화**: Q = 존댓말 ("~요?", "~예요?", "~어요!") / A = 친절 반말 (친구·형/오빠/언니/누나)
>   2. **의문/감탄/평문 다양화** — 단조 X (연속 평문 ≤ 2)
>   3. **속도 1.25배** (default 너무 느림)

---

## 1. 형식 — 2 화자 dialog (v2 유지 + 어투 분화)

| 화자 | 정체 | 어투 (v3) | 역할 |
|---|---|---|---|
| **Q** | 초등 고학년 ~ 중1 청소년 | **존댓말** ("들어봤어요?", "왜요?", "어떻게요?", "~예요!") | 끊임없는 호기심, 어른 학자에게 묻는 톤 |
| **A** | 20대 후반 대학원생 | **친절 반말** ("응, 알지", "잘 봐", "내가 찾아봤는데...") | 공감 + 학습 친화 답변 + 되묻기 |

자연 한국어 dynamic = 어린이-어른 대화. Q 의 호기심이 더 두드러짐.

본 단원 1 = Q 여 + A 남. 다음 단원 = 반대.

## 2. 다양화 — 의문 / 감탄 / 평문 (v3 신설)

본 결정의 *핵심*. 단조 X.

| 유형 | 끝 마커 | TTS 효과 | 사용 위치 |
|---|---|---|---|
| **의문** | `?` | rising intonation | Q 의 호기심 / A 의 되묻기 |
| **감탄** | `!` | 강조 + 활기 | Q 의 반응 ("와!", "어!") / A 의 강조 ("그러게!") |
| **평문** | `.` | 일반 falling | A 의 설명 / 사실 진술 |

규칙:
- **연속 평문 ≤ 2** turn (3개 이상 = 단조 ❌)
- Q turn = 의문 + 감탄 위주
- A turn = 평문 + 의문 (설명 + 되묻기) + 감탄 (강조)
- **한 turn 안에 의문 + 평문 + 감탄 섞기 가능** (예: "잘 봐. 6은 2 곱하기 3이지? 진짜네!")

## 3. 톤 — 친근 + 어투 분화 (v2 유지 + v3 분화)

- **Q 존댓말 + 친근** — 호기심 어린이가 어른 선생님에게 묻는 톤
- **A 친절 반말** — 친근 어른 학자 (형/오빠/언니/누나 분위기)
- 학술 톤 X / 강의 톤 X / *함께 발견하는 톤* ✓

## 4. 답변자 (A) 의 특별 요소 (v2 유지)

- "나도 찾아봤는데..." / "내가 알기로는..." (학습 친화)
- 공감 ("그러게!", "맞아!", "오 좋은 질문!")
- 되묻기 ≥ 1회 (예: "한 단어로 표현하면 뭘까?")

## 5. 풍부한 배경 (v2 유지)

- S1 시대 풍경 풍부 (이집트 항구 / 50만 권 / 학자 다국 등 ≥ 3 사실)
- *왜 중요한지* 함께 발견

## 6. 마무리 (v2 유지)

- 마지막 장면 = Q 시도 + A 확인 패턴
- 끊김 X — A 의 마지막 짧은 정리 멘트로 닫음

## 7. TTS 합성 — ElevenLabs 우선 (v3.3 현행)

> **⭐ 정확한 합성 config (voice_id / voice_settings / post-processing / pause / text 규칙) = [`voice-pool.md`](../70_tools/se-video-narration/voice-pool.md) §0 SSOT.**
> v3.3 (2026-05-28): Nick $10 API credits 충전 → ElevenLabs 1차 복귀. 조합 A = Annie(Q, atempo 1.1) + Mike(A, +8dB). 조합 B = Onyu + Kyle. Google = 2차 백업.

### v3 → v3.2 재마이그 이유 (이력 — 현재는 v3.3 으로 복귀)

| 항목 | edge-tts (v2) | ElevenLabs (v3) | **Google Cloud TTS (v3.2)** |
|---|---|---|---|
| 한국어 voice 수 | 3개 | premade 21 + library | **ko-KR-Neural2 3+ / Wavenet 4 / Standard 4** |
| 청소년 voice | ❌ 부재 | library 제약 (Free X) | ⚠️ Neural2 청취 평가 |
| 표현력 | 기본 | ★★★★★ | ★★★★ |
| SSML | 부분 | ❌ | ✅ **풀 지원** (prosody/break/emphasis 등) |
| 가격 | 무료 | Free 10,000자/월 (library voice X) | **Neural2 100만 chars/월 무료 (영상 1,800편/월)** |
| Multi-voice | ❌ (turn 별) | ❌ (turn 별) | ❌ (turn 별 + concat) |
| 속도 제어 | --rate flag | ffmpeg atempo | speaking_rate (TTS-side) + ffmpeg atempo |
| **Free tier 차단** | 없음 | ✅ library voice = HTTP 402 | 없음 (무료 한도 안에서 풀 사용) |
| 결제 안정성 | 비공식 backend | Free → paid 게이트 엄격 | Google Cloud SLA |

### voice 매핑 (단원 1, v3.2 Google Cloud TTS 1차)

본 프로젝트 voice 풀 = [`70_tools/se-video-narration/voice-pool.md`](../70_tools/se-video-narration/voice-pool.md) 참조.

**시범 이력**:
- v3 시범 1 (2026-05-26 오후) — ElevenLabs Jessica + Will (premade) = ❌ "미국식 한국말" → 폐기
- v3.1 시범 (2026-05-26 저녁) — ElevenLabs Mono Beige + Mike (library) = ❌ HTTP 402 Free tier 차단

**v3.2 풀 (Google Cloud TTS 1차)**:

| 화자 | voice | 비고 |
|---|---|---|
| **Q (여, 청소년, 존댓말)** | `ko-KR-Neural2-A` | Google Neural2, 표준 따뜻 톤 |
| **A (남, 대학원생, 친절 반말)** | `ko-KR-Neural2-C` | Google Neural2, 차분 친절 톤 |

setup 가이드 = [`google-cloud-tts-guide.md`](../70_tools/se-video-narration/google-cloud-tts-guide.md)

**2차 풀 (ElevenLabs Starter $5 결제 시)**:

| 화자 | 후보 | 비고 |
|---|---|---|
| **Q (여, 청소년)** | **Mono Beige** 또는 **Onyu** | Nick 추천, Voice Library |
| **A (남, 대학원생)** | **Kyle** 또는 **Mike** | Nick 추천, Voice Library |

(model = `eleven_multilingual_v2`, 결제 후 사용 가능)

### voice 풀 진화 (v3.1)

- 단원별 randomize (Q/A 성별 반대, voice-pool.md §2.1)
- 풀 평가 기준 (voice-pool.md §4)
- 새 voice 진입 흐름 (elevenlabs-detailed-guide.md §4.4)

### voice 설정 (v3.2 — 2 도구 병기)

**Google Cloud TTS (1차)** — `AudioConfig`:

| 화자 | speaking_rate | pitch | volume_gain_db | 효과 |
|---|---|---|---|---|
| **Q (활기, 청소년)** | 1.0 (시범 후 1.15) | +1.0 (살짝 높임) | 0 | 청소년 톤 |
| **A (차분, 대학원생)** | 1.0 | 0.0 | 0 | 일관성 + 친절 |

**ElevenLabs (2차)** — `voice_settings`:

| 화자 | stability | similarity_boost | style | 효과 |
|---|---|---|---|---|
| **Q (활기)** | 0.3 | 0.75 | 0.4 | 표현력 ↑ (감탄·의문 강조) |
| **A (차분)** | 0.5 | 0.75 | 0.2 | 일관성 + 친절 |

### 속도 1.25배 (v3.2)

**Google Cloud TTS** = `speaking_rate=1.25` 직접 지원 (TTS-side 가속, 자연도 우수).

**ElevenLabs** = `voice_settings` 에 speed X → ffmpeg `atempo=1.25` post-processing.

본 시범 1차: Google `speaking_rate=1.0` → 길이 측정 → 너무 느리면 1.15~1.25 조정.

### 합성 방식 (v3.2)

```python
# Google Cloud TTS — turn 별 SDK + ffmpeg concat
# (상세 = google-cloud-tts-guide.md §8 + se-video-narration SKILL.md NR6)
from google.cloud import texttospeech
client = texttospeech.TextToSpeechClient()  # GOOGLE_APPLICATION_CREDENTIALS 자동 인식

for t in turns:  # 4-narration.jsonl loop
    voice = texttospeech.VoiceSelectionParams(language_code="ko-KR", name=VOICE_MAP[t["speaker"]])
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    resp = client.synthesize_speech(input=texttospeech.SynthesisInput(text=t["text"]), voice=voice, audio_config=audio_config)
    # turn-NNN.mp3 저장 → ffmpeg concat → 4-narration.mp3
```

## 8. 호흡 — pause (v2 유지)

| 유형 | 시간 |
|---|---|
| Q→A 응답 (turn 사이) | 200~400ms |
| 생각할 시간 | 700~900ms |
| 결정적 순간 후 | 500~700ms |
| 일반 turn 내 sentence | 300~400ms |

Google Cloud TTS 자동 처리 (마침표 + 줄바꿈). SSML `<break time="300ms"/>` 직접 사용 가능. Q→A 응답은 ffmpeg silence padding 으로 추가 가능.

## 9. 영상 길이 (v3 갱신)

- v1 = 150~180s (단일 voice)
- v2 = 150~210s (dialog edge-tts)
- **v3 = 150~180s** (1.25배 속도 → 동일 텍스트 짧음)
- 본 단원 v3 시범 측정 후 확정 (결정 11 후보)

## 10. 적용 스킬 (v2 유지, v3 시드 추가)

| 스킬 | v3 시드 |
|---|---|
| `se-people-narrate` | 원료에 의문/감탄/평문 다양 가능 자산 |
| `se-video-story` | 장면 카드에 의문/감탄/평문 sequence + 어투 (Q 존댓말 / A 반말) |
| `se-video-storyboard` | 나레이션 시드 = 어투 + 다양화 마커 |
| `se-video-narration` | Google Cloud TTS 1차 합성 + Neural2-A/C + speaking_rate / ElevenLabs Starter 2차 |

## 11. 결정의 진화

- **v1** (2026-05-25) — 단일 voice narration + 호기심 chain (edge-tts)
- **v2** (2026-05-26 오전) — 2 화자 dialog (edge-tts)
- **v3** (2026-05-26 오후) — Q 존댓말 + A 친절 반말 + 의문/감탄/평문 다양 + ElevenLabs 1차 (Jessica/Will = 미국식 한국말 → 폐기)
- **v3.1** (2026-05-26 저녁) — ElevenLabs Mono Beige/Mike (library voice) 시도 → HTTP 402 Free tier 차단
- **v3.2** (2026-05-26 야간) — Google Cloud TTS 1차 마이그 (임시). Neural2-A/C.
- **v3.3 (2026-05-28) — ElevenLabs 1차 복귀** (Nick $10 API credits 충전). 조합 A Annie+Mike / 조합 B Onyu+Kyle. 합성 config SSOT = voice-pool §0. post-processing (atempo/volume) + text 정련 규칙 + pause 정립. 현행.
- v4 = 다음 단원 시범 후 (단원별 어투 다양 / 인물별 voice / 속도 미세조정)

## 12. 본 결정의 자산 (단원 1 v3 시범 예정)

- `4-narration.jsonl` v3 — Q 존댓말 + A 친절 반말 + 다양화 + ElevenLabs voice 매핑
- `4-narration.txt` v3 — 평문 (참조 + marker)
- `4-narration.xml` v3 — SSML 풀스펙 (Azure/Google reference, ElevenLabs 미사용)
- `4-narration.mp3` v3 — ElevenLabs 합성 결과 (Nick API key 연결 후)

## 13. 변경 이력

- 2026-05-25 v1: 단일 voice 친근 톤
- 2026-05-26 오전 v2: 2 화자 dialog (edge-tts)
- 2026-05-26 오후 v3: Nick redirect 3 — Q 존댓말 + A 친절 반말 + 의문/감탄/평문 다양 + ElevenLabs 마이그 1차

---

## 14. v3 → ElevenLabs 시범 연결 흐름

```
1. Nick 의 ElevenLabs API key 발급 + 환경 변수 설정
   → elevenlabs-detailed-guide.md §2~3 참조
2. NCC: env 변수 존재 확인 ([ -n "$ELEVENLABS_API_KEY" ])
3. NCC: voice ID 조회 (Bella / Adam)
4. NCC: 4-narration.jsonl 의 voice 필드 = 실제 voice_id 로 갱신
5. NCC: Python script (ElevenLabs API + ffmpeg concat) 실행
6. NCC: ffprobe 길이 측정
7. Nick 청취 + 평가
```
