<!-- retro-4-narration.md / STEP 4 [영상 2] 나레이션 회고 -->

# STEP 4 회고 — se-video-narration (v0.1 → v0.5.2)

> exp-002 STEP 4 진행 회고. 스킬 자체 개선점 + 다음 단원 적용 교훈.
> 합성 config SSOT = [`../../70_tools/se-video-narration/voice-pool.md`](../../70_tools/se-video-narration/voice-pool.md) §0.

---

## 1. 결과물

- `4-narration.mp3` (단원 1 = **Kanna+Kyle**, 140s)
- `4-narration-mina-mike.mp3` (대안, 152s)
- `4-narration.{txt,xml,jsonl}` — 38 turn dialog (Q 존댓말 + A 친절 반말)

## 2. 가장 큰 교훈 — TTS 도구·voice 선정은 반복 탐색

도구·voice 가 1-shot 으로 안 정해짐. 실제 청취 → 폐기 → 교체 반복이 본질.

### 도구 우여곡절
edge-tts (한국어 3 voice, 청소년 X) → ElevenLabs Free (library voice HTTP 402 차단) → Google Cloud TTS (결제 SMS 막힘 보류) → **ElevenLabs API $10 credits 충전** (확정).

### voice 폐기 연쇄
Jessica/Will (미국식) → Mono Beige (음량 과대) → Annie/Onyu (느림) → Yura (별로) → **Mina/Kanna 확정**.

→ **다음 단원 교훈**: voice-pool §0 의 확정 config (Mina/Kanna/Mike/Kyle) 로 바로 시작. 단 신규 voice 는 "실제 합성 청취" 없이 확정 금지.

## 3. 핵심 기술 발견 (시스템 자산)

| 발견 | 내용 |
|---|---|
| **`speed` 파라미터** | `voice_settings.speed` (0.7~1.2, multilingual_v2). 합성 시 직접 가속 → ffmpeg atempo 후처리 폐기 (더 자연). Q=1.15 |
| **음량 balance** | voice 마다 default 음량 다름. ffmpeg `volumedetect` 측정 → 낮은 쪽 boost (Mike +8dB, Kyle +3.8dB) |
| **pause 설계** | Q/A turn 사이 300ms + scene 경계 1000ms silence concat → 길이 보강 + 호흡 |
| **text 정련** | 의문문 `?` (style 0.7 끝 올림) + 중요단어 쉼표 `,` + 감탄 `~~` elongation + 여운 `...` |
| **key 권한** | ElevenLabs key `user_read` 없으면 /v1/voices 401 → **voice_id 직접 사용** (voice-pool §0 에 박음) |
| **연결 안정** | ConnectionReset(10054) 빈발 → retry 4회 (timeout 60, sleep 2×attempt) |
| **노이즈 대응** | 특정 turn 합성 아티팩트 → 그 turn 만 재합성 + concat (전체 재합성 X) |

## 4. config SSOT 구조 (Nick 요청 — cross-session 재현)

`voice-pool.md §0` = 다른 세션·다른 NCC 도 이것만 읽으면 동일 음성 재현. 메모리 `reference-elevenlabs-synthesis-config` 가 위치 안내.

## 5. SKILL.md v0.5.2 정련 항목 (다음 단원 반영)

- NR6 = ElevenLabs 1차 (config = voice-pool §0)
- speed 파라미터 합성 (atempo 폐기)
- 단원별 Q/A 성별 randomize (voice-pool §3.1)
- turn 별 합성 + post-proc(A volume) + concat(silence) 6-step

## 6. 미해결 / 다음

- Onyu 속도 미세조정 (대안 풀)
- 인물별 voice 고정 (시리즈 정체성) — 다음 단원 검토
- BGM/효과음 (STEP 8 합성 시)
