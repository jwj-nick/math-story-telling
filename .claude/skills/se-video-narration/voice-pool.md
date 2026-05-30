<!-- voice-pool.md / TTS voice 풀 + 합성 Configuration SSOT -->

# Voice Pool + 합성 Configuration — ElevenLabs (1차) + Google Cloud TTS (2차 백업)

> **목적**: `se-video-narration` 스킬의 voice 풀 **+ 정확한 합성 설정 SSOT**.
> **이 파일이 SSOT**: 다른 세션·다른 NCC 가 와도 이 파일만 읽으면 동일 음성을 재현한다.
> **상위 frame**: [TONE_STRUCTURE.md](../../../11_video_gen_process/00_charter/TONE_STRUCTURE.md) §7.
> **상세 가이드**: [elevenlabs-detailed-guide.md](./elevenlabs-detailed-guide.md) (1차) / [google-cloud-tts-guide.md](./google-cloud-tts-guide.md) (2차 백업).
> **최근 갱신**: 2026-05-28 v3 (ElevenLabs API credits $10 충전 → 1차 복귀, 합성 config SSOT 신설)

---

## 0. ⭐ 확정 합성 Configuration (재현용 SSOT)

> **이 섹션이 핵심.** 아래 설정 그대로 재현하면 Nick 이 승인한 음성이 나온다.

### 0.1 도구 + 모델 + 키

| 항목 | 값 |
|---|---|
| 도구 | **ElevenLabs API** (Nick $10 credits 충전, 2026-05-28) |
| 모델 | `eleven_multilingual_v2` |
| 키 | 환경 변수 `ELEVENLABS_API_KEY` (PowerShell User scope) — [reference_powershell_key_extraction](추출 패턴) |
| ⚠️ 키 권한 | TTS 가능 / **`user_read` 없음** → `/v1/voices`·`/v1/user/subscription` 호출 시 HTTP 401. **voice_id 를 본 표에서 직접 사용** (조회 X) |
| 출력 spec | mp3 44100Hz **mono** 128k |
| 1편 사용량 | ~1,000 chars (38 turn) ≈ $10 의 ~4% |

### ⭐ 속도 제어 = `speed` 파라미터 (v3.4, atempo 폐기)

ElevenLabs `voice_settings` 에 **`speed`** 지원 (범위 0.7~1.2, `eleven_multilingual_v2` 포함 전 모델). **합성 시점에 직접 적용 → ffmpeg atempo 후처리 폐기** (더 자연). Q 청소년 = **`speed: 1.15`** (빠르게). A 남자 = speed 미지정 (1.0, 적당).

### 0.2 ★ 확정 조합 — Mina(Q)+Mike(A) / Kanna(Q)+Kyle(A) (v3.5, 2026-05-28 Nick 확정)

여 voice = **Mina / Kanna** 확정 (Yura 청취 후 별로 → Mina 교체). 남 voice = Mike / Kyle 유지.

| 항목 | Q = **Mina** | Q = **Kanna** | A = **Mike** | A = **Kyle** |
|---|---|---|---|---|
| voice_id | `aiUUgjHa4mpHf6UenZuf` | `5I7B1di44aCL15NkP0jn` | `mgugV8tLa3KQE4mfYTw5` | `RU7aSi6lT4uQBXMLgDxK` |
| stability | 0.2 | 0.2 | 0.5 | 0.5 |
| similarity_boost | 0.75 | 0.75 | 0.75 | 0.75 |
| style | 0.7 | 0.7 | 0.2 | 0.2 |
| **speed** (합성) | **1.15** | **1.15** | 1.0 | 1.0 |
| **post-processing** | 없음 (재인코딩만) | 없음 | **`volume=+8dB`** | **`volume=+3.8dB`** |
| 역할 | 청소년 Q | 청소년 Q | 대학원생 A | 대학원생 A |

확정 mp3: `4-narration-mina-mike.mp3` / `4-narration-kanna-kyle.mp3`

### 0.4 공통 pause / concat

| 위치 | silence | 비고 |
|---|---|---|
| Q/A turn 사이 (일반) | **300ms** | 모든 인접 turn |
| scene 경계 (S1→S2 등) | **1000ms** | jsonl `scene` 필드 변화 지점 (5곳) |

- silence 파일: `ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t <초> -acodec libmp3lame -b:a 128k silence_<N>ms.mp3`
- concat: `ffmpeg -f concat -safe 0 -i concat.txt -c copy 4-narration.mp3`
- 길이 목표: **150~180s** (TONE_STRUCTURE §9)

### 0.5 text 정련 규칙 (음성 표현 ↑)

| 규칙 | 방법 | 예 |
|---|---|---|
| 의문문 끝 올림 | `?` + style 0.7 | "들어봤어요?", "왜요?" |
| 중요 단어 강조 | 앞뒤 **쉼표** `,` 로 호흡 | "기원전 3세기," / "그럼, 그 도서관은," / "다재다능 한 거," |
| 감탄 elongation | 물결 **`~~`** 로 길게 | "헐~~ 그 유명한, 아르키메데스요?" |
| 여운 | 줄임표 **`...`** | "음... ~니까...", "오..." |

> ⚠️ **bare filler 회피 (unit-02 학습, 2026-05-30)**: 문장 **맨 앞 단독 필러** ("음...", "어...") 는 남성 youth Q voice(Kyle, style 0.7 + speed 1.15)에서 *이상한 감탄사*로 뭉개짐(예: "음..."→정체불명 소리). → 단독 필러 대신 **실질 단어로 시작**하거나("0보다 작은 수요?") 필러를 짧은 감탄("어!")+쉼표로. 줄임표 여운은 *문장 중간·끝*에서만. 남성 Q에 특히 주의.

### 0.6 합성 절차 (재현 — 6 step)

```bash
# 1. key 추출 (PowerShell 경유 — NCC Bash 가 setx registry 직접 못 읽음)
KEY=$(powershell -NoProfile -Command "[System.Environment]::GetEnvironmentVariable('ELEVENLABS_API_KEY','User')" | tr -d '\r\n')
export ELEVENLABS_API_KEY="$KEY"; export PYTHONIOENCODING=utf-8

# 2. turn 별 합성 → turns_<voice>/turn-NNN.mp3
#    - voice_id 직접 (§0.2), model=eleven_multilingual_v2, voice_settings 화자별
#    - Q 는 voice_settings 에 speed=1.15 포함 (합성 시 가속, atempo 폐기)
#    - A(Mike/Kyle) turn 은 재사용 가능 (speed 1.0 — 기존 turns/ 와 동일)
#    - retry 4회 (ConnectionReset 10054 대비, timeout=60, sleep 2*attempt)

# 3. post-processing → turns_norm/turn-NNN.mp3
#    - Q(Yura/Kanna): 없음 (재인코딩만 — speed 는 이미 합성에 반영)
#    - A: volume (Mike +8dB / Kyle +3.8dB)
#    - 공통 재인코딩 libmp3lame 128k -ar 44100 -ac 1

# 4. concat.txt 생성 (Q/A 300ms, scene 경계 1000ms silence 삽입)

# 5. ffmpeg concat → 4-narration.mp3

# 6. ffprobe 길이 측정 (목표 150~180s)
```

---

## 1. ElevenLabs 풀 (1차, 현행)

### 여 voice (Q 청소년) — Mina / Kanna 확정

| voice | voice_id | 상태 | 평가 |
|---|---|---|---|
| **Mina** | `aiUUgjHa4mpHf6UenZuf` | 🟢 확정 (v3.5) | 청소년, speed 1.15 (Yura 대체) |
| **Kanna** | `5I7B1di44aCL15NkP0jn` | 🟢 확정 (v3.4) | 청소년, speed 1.15 |
| ~~Yura~~ | ~~`F7wT70V3u09d2rY9pNa6`~~ | ❌ 교체 (v3.5) | 실제 청취 후 별로 |
| ~~Annie~~ | ~~`Lb7qkOn5hF8p7qfCDH8q`~~ | ❌ 교체 (느림) | atempo 해도 느림 |
| ~~Onyu~~ | ~~`NaQdbkW5gNZD8wfwXeTV`~~ | ❌ 교체 | — |
| ~~Mono Beige~~ | ~~`SE9upoSoM2ipDUdAVW8q`~~ | ❌ 폐기 | 음량 과대 + 의문문 표현 부족 |

### 남 voice (A 대학원생) — Mike / Kyle 유지

| voice | voice_id | 상태 | 평가 |
|---|---|---|---|
| **Mike** | `mgugV8tLa3KQE4mfYTw5` | 🟢 확정 | 친절 톤 자연, default 음량 작음 → +8dB |
| **Kyle** | `RU7aSi6lT4uQBXMLgDxK` | 🟢 확정 | default 음량 작음 → +3.8dB |

### 폐기 / 비추천

| voice | 평가 | 이유 |
|---|---|---|
| Jessica / Will | ❌ | 미국식 한국말 |
| Bella / Adam | ❌ | middle_aged / 권위적 |
| Mono Beige | ❌ | 음량 과대 + 의문문 표현 부족 |
| Annie / Onyu | ❌ 교체 | 발화 느림 |
| Yura | ❌ 교체 | 실제 청취 후 별로 (Mina 로 대체) |

---

## 2. Google Cloud TTS 풀 (2차 백업)

> ElevenLabs credit 소진 또는 무료 운영 전환 시 백업. setup = [google-cloud-tts-guide.md](./google-cloud-tts-guide.md).

| voice | 성별 | 추천 | AudioConfig |
|---|---|---|---|
| `ko-KR-Neural2-A` | F | Q 청소년 | speaking_rate 1.0~1.15, pitch +1.0 |
| `ko-KR-Neural2-B` | F | Q 후보 | — |
| `ko-KR-Neural2-C` | M | A 대학원생 | speaking_rate 1.0, pitch 0.0 |
| `ko-KR-Wavenet-A~D` | F/F/M/M | 대안 | — |

Google 은 SSML 풀 지원 (`<break time="300ms"/>`) + `speaking_rate` 직접 (atempo 불필요) + 무료 한도 100만 chars/월.

---

## 3. 사용 패턴

### 3.1 단원별 randomize (시즌 1)

| 단원 | Q | A | ElevenLabs 조합 예 |
|---|---|---|---|
| 1 소인수분해 / 에라토 | 여 | 남 | **Mina(Q) + Mike(A)** 또는 **Kanna(Q) + Kyle(A)** (확정) |
| 2 정수·유리수 / 브라마굽타 | 남 | 여 | Kyle(Q) + Mina(A) |
| 3 문자·식 / 알콰리즈미 | 여 | 남 | Kanna(Q) + Mike(A) |
| 4 일차방정식 / 디오판토스 | 남 | 여 | Mike(Q) + Kanna(A) |
| 5~6 좌표·함수 / 데카르트 | 여/남 | 남/여 | (시범 후 확정) |

규칙:
- Q/A 성별 = 단원마다 반대 (시즌 내 균형)
- 같은 성별 Q↔A 금지 (풀 내 다른 voice)

### 3.2 인물별 voice 고정 (옵션, 향후)

특정 인물 = 특정 voice (시리즈 정체성 ↑). 다음 단원 시범 후 검토.

---

## 4. voice 추가·평가 흐름 (Nick)

```
1. ElevenLabs Voice Library (https://elevenlabs.io/app/voice-library)
   또는 My Voices 에서 voice 청취 (한국어 샘플)
2. 마음에 들면 "Add to My Voices"
3. NCC 에게 알림 + voice_id (Nick 이 직접 복사 — key user_read 없어 NCC 조회 X)
4. NCC: §0/§1 풀 갱신 + 시범 합성
5. Nick 청취 → 평가 (상태 🟢/🟡/❌) + post-processing 조정 (atempo/dB)
```

---

## 5. 풀 평가 기준

- 한국어 자연도 (외국인 한국말 X)
- 성별·연령 라벨 정확 (청소년/대학원생)
- 의문문·감탄 표현 자연 (style 조정 후)
- 음량 balance (측정 → atempo/volume 보정)
- 속도 (느리면 atempo 보정)

---

## 6. 변경 이력

- 2026-05-26 v1: 신규. Jessica/Will/Bella/Adam 폐기, Mono Beige/Yuna/Kyle/Mike 추가 대기.
- 2026-05-26 v1.1: voice_id 등록 (Yuna → Onyu 교체).
- 2026-05-26 v2: Google Cloud TTS 1차 마이그 (ElevenLabs Free tier library voice 차단 발견 후).
- 2026-05-28 v3: ElevenLabs 1차 복귀 (Nick $10 credits). §0 합성 config SSOT 신설 — Annie+Mike / Onyu+Kyle (atempo 보정). Mono Beige 폐기.
- 2026-05-28 v3.4: 여 voice = Yura/Kanna (Annie/Onyu 느림 → 교체). **`speed` 파라미터 도입** (Q=1.15, atempo 폐기). 남 Mike/Kyle 유지.
- 2026-05-28 v3.5: **Yura → Mina 교체** (`aiUUgjHa4mpHf6UenZuf`, Yura 실제 청취 후 별로). 확정 여 voice = **Mina/Kanna**. 확정 mp3 = mina-mike (152s) / kanna-kyle (140s).
