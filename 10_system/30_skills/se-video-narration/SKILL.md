---
name: se-video-narration
description: 영상 제작 시스템의 단계 [영상 2] 나레이션 스킬. 단계 [영상 1] 스토리보드의 나레이션 시드를 받아 실제 발화용 텍스트 + SSML 풀스펙 + 음성 합성 (mp3) 을 작성한다. 입력 (스토리보드 / 정체성 = 시청자·약속·톤 / TTS 도구 선택 / (옵션) 음성 매핑 / (옵션) 옛 baseline SSML) 을 받아 동작 (입력 align → Q&A → 나레이션 정련 → SSML 마크업 → TTS 합성 → 길이 검증 → 자체 평가 → 출력) 진행. math-story-telling 의 영상 나레이션 작성, SSML 마크업, TTS 합성 + 길이 사전 검증, 인물별 음성 매핑 시 사용.
compatibility: Designed for Claude Code in C:/Kids/math-story-telling/11_video_gen_process/. 본 프로젝트 외부 자료 (`40_experiments/exp-NNN/3-storyboard.md`, INTEGRATED_PLAN §5.1.2·§8, `50_channel/season-1-ancient/unit-NN/narration_v1_5.xml` baseline) 를 참조만 함. 외부 도구 호출: edge-tts (Python CLI) 또는 ElevenLabs API.
metadata:
  project: math-story-telling
  sub-project: 11_video_gen_process
  stage: 영상 2 나레이션 (NR1~NR7)
  ssot: 11_video_gen_process/70_tools/se-video-narration/SKILL.md
  version: "0.5"
  status: 시드 (시범 실행 후 retrospective 로 정련 예정)
allowed-tools: Read Write Grep Glob Bash AskUserQuestion WebFetch WebSearch
---

# se-video-narration — 영상 2 나레이션 스킬

본 스킬은 영상 제작 시스템의 단계 [영상 2]. 단계 [영상 1] 스토리보드의 나레이션 시드를 받아 *실제 발화용 텍스트* + SSML 풀스펙 + 음성 합성 (mp3) 을 작성한다. 출력은 다음 단계 [영상 5] 렌더 (`se-video-render`) 및 [영상 6] 합성 (`se-video-compose`) 의 직접 입력.

상위 frame: [INTEGRATED_PLAN](../../../11_video_gen_process/00_charter/INTEGRATED_PLAN.md) §5.0 skill chain / §5.5 단계 [영상 2] / §8 결정 1·2.

원칙:
- 본 스킬은 외부 자료를 **참조** 한다. 외부를 변경 X.
- 호출자가 입력 일부만 줘도 됨 — 동작 초기 단계에서 보강.
- **외부 도구 호출 첫 단계** — TTS 엔진 (edge-tts / ElevenLabs / etc).
- 도구 비교는 [`tts-tools-guide.md`](./tts-tools-guide.md) 참조.
- **⭐ 1차 도구 (v0.5 현행)**: ElevenLabs API (Nick $10 credits 충전). **정확한 합성 config = [`voice-pool.md`](./voice-pool.md) §0 (SSOT)**. 다른 세션·다른 NCC 도 voice-pool §0 만 읽으면 동일 음성 재현.
- 2차 백업: Google Cloud TTS ([`google-cloud-tts-guide.md`](./google-cloud-tts-guide.md)) — credit 소진/무료 전환 시.

---

본 v0.2 body 는 **exp-002 STEP 4 시범 + Nick redirect 2 (dialog 형식)** 으로 작성됨 (2026-05-26). 시범 결과 (예정): [`../../../11_video_gen_process/40_experiments/exp-002-build-unit01/4-narration.{txt,xml,jsonl,mp3}`](../../../11_video_gen_process/40_experiments/exp-002-build-unit01/).

**시스템 톤·구조 결정 (v2 dialog)**: [`../../../11_video_gen_process/00_charter/TONE_STRUCTURE.md`](../../../11_video_gen_process/00_charter/TONE_STRUCTURE.md) (결정 10 v2 — 2 화자 dialog: Q 청소년 + A 대학원생).

---

## 입력 (3 필수 + 2 옵션)

| # | 입력 | 형식 | 출처 예시 |
|---|---|---|---|
| 1 | 스토리보드 | `3-storyboard.md` (특히 부록 A) | `40_experiments/exp-NNN/3-storyboard.md` |
| 2 | 정체성 + 톤·구조 결정 | 시청자 + 약속 + TONE_STRUCTURE | INTEGRATED_PLAN §8 + TONE_STRUCTURE.md |
| 3 | TTS 도구 | ElevenLabs / Google Cloud TTS / edge-tts | **1차 = ElevenLabs (v0.5 현행), config = voice-pool §0** |
| 4 (옵션) | 음성 매핑 | 인물별 voice | 본 단원 = 1 voice |
| 5 (옵션) | 옛 baseline SSML | 경로 | (외부 의존 0 frame) |

---

## 동작 (NR1~NR7) — v2 dialog

### NR1. 입력 align
- 입력 3 필수 + 옵션 확인
- 스토리보드 부록 A (Q/A turn 분리 + 자수) 확인
- TONE_STRUCTURE.md v2 (2 화자 dialog / voice 매핑 / 합성 방식) 확인

### NR2. (필요 시) Q&A 보강
- **Q/A 성별 결정** (단원 1 = Q 여 + A 남, 다음 단원 = 반대 — 시즌 내 균형)
- **voice 선택** (v0.4 — Google Cloud TTS 1차):
  - Q 청소년 (여) = `ko-KR-Neural2-A` 또는 `ko-KR-Neural2-B` 청취 평가
  - A 대학원생 (남) = `ko-KR-Neural2-C`
  - 풀 전체 = [`voice-pool.md`](./voice-pool.md)
- speaking_rate / pitch: 화자별 차등 가능 (Q rate 1.0 + pitch 0.5, A rate 1.0 + pitch 0.0)
- 도구 선택: **Google Cloud TTS** (turn 별 + ffmpeg concat) 1차 / ElevenLabs (Starter) 2차 / edge-tts (fallback)

### NR3. Dialog 정련 (TONE_STRUCTURE v3 부합)
스토리보드 부록 A 의 dialog 시드를 *실제 발화용* 으로 정련:
- **2 화자 turn 분리** (Q/A 명확)
- **🔥 Q = 존댓말** ("들어봤어요?", "왜요?", "어떻게요?", "~예요!") — v3
- **🔥 A = 친절 반말** ("응, 알지", "잘 봐", "내가 찾아봤는데...") — v3
- **🔥 의문/감탄/평문 다양화** (TONE_STRUCTURE v3 §2) — v3:
  - 연속 평문 ≤ 2 turn
  - Q turn = 의문 + 감탄 위주
  - A turn = 평문 + 의문 + 감탄 섞기
  - 한 turn 안에 여러 마커 가능
- **A 의 "나도 찾아봤는데..." / "내가 알기로는..."** 표현 ≥ 1 회
- **Q 의 자연 반응** ("어!", "와!", "오!", "헐!", "어 진짜네요!")
- **A 의 되묻기** ≥ 1 회 (예: "한 단어로 표현하면 뭘까?")
- **풍부 배경**: A 의 첫 답변 (S1) 에 시대 풍경 풍부 (≥ 3 사실)
- **마무리**: 마지막 장면 = Q 시도 + A 확인 + A 의 짧은 정리 (끊김 X)
- **turn 평균 자수 10~30** (자연 호흡)

### NR4. SSML 마크업 (`<step>-narration.xml`)
**multi-voice 풀스펙** (Azure / Google / Amazon 호환):

```xml
<speak xml:lang="ko-KR">
  <voice name="ko-KR-YuJinNeural">
    <prosody rate="-5%" pitch="+5Hz">
      [Q turn 텍스트]<break time="300ms"/>
    </prosody>
  </voice>
  <voice name="ko-KR-InJoonNeural">
    <prosody rate="-5%">
      [A turn 텍스트]<break time="500ms"/>
    </prosody>
  </voice>
  <!-- ... turn 반복 -->
</speak>
```

→ edge-tts 미사용 (single voice CLI). Azure / Google 의 단일 SSML 호출 reference.

### NR5. Dialog jsonl 분할 (`<step>-narration.jsonl`)
edge-tts 합성용 turn 별 분할:

```jsonl
{"speaker":"Q","voice":"ko-KR-YuJinNeural","rate":"-5%","pitch":"+5Hz","text":"..."}
{"speaker":"A","voice":"ko-KR-InJoonNeural","rate":"-5%","pitch":"+0Hz","text":"..."}
```

또한 평문 (`<step>-narration.txt`) = jsonl text 만 연결 (참조용, marker `[Q]` `[A]` 포함).

### NR6. TTS 합성 — multi-voice (v0.5: ElevenLabs 1차)

> **⭐ 정확한 합성 설정 (voice_id / voice_settings / post-processing / pause) = [`voice-pool.md`](./voice-pool.md) §0 SSOT.**
> 아래는 흐름 요약. 실제 값은 항상 voice-pool §0 에서 가져온다.

**ElevenLabs 합성 (v0.5 1차)** — voice-pool §0.6 절차:
1. key 추출 (PowerShell 경유, §0.1)
2. turn 별 합성 (voice_id 직접 — key `user_read` 권한 없어 /v1/voices 조회 X), retry 4회. **Q 는 voice_settings 에 `speed=1.15` 포함** (atempo 폐기)
3. post-processing: Q 없음 (speed 합성 반영) + A `volume` (Mike +8dB / Kyle +3.8dB) — §0.2
4. concat: Q/A 300ms + scene 1000ms silence — §0.4
5. ffprobe 길이 (150~180s)

```python
import os, sys, json, time, requests
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
API_KEY = os.environ["ELEVENLABS_API_KEY"]
H = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
# voice_id 는 voice-pool §0.2/0.3 에서 (조회 X — user_read 권한 없음)
VOICE_ID = {"Mina": "aiUUgjHa4mpHf6UenZuf", "Kanna": "5I7B1di44aCL15NkP0jn",
            "Mike": "mgugV8tLa3KQE4mfYTw5", "Kyle": "RU7aSi6lT4uQBXMLgDxK"}
# Q voice_settings 예: {"stability":0.2,"similarity_boost":0.75,"style":0.7,"speed":1.15}

def synth(t, tries=4):  # ConnectionReset 10054 대비 retry
    for a in range(1, tries+1):
        try:
            r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID[t['voice']]}",
                headers=H, json={"text": t["text"], "model_id": "eleven_multilingual_v2",
                "voice_settings": t["voice_settings"]}, timeout=60)
            if r.status_code == 200: return r.content
        except Exception: pass
        time.sleep(2*a)
    return None
# turn loop → turns/ → post-processing(atempo/volume) → turns_norm/ → ffmpeg concat
```

**Google Cloud TTS 합성 (v0.5 2차 백업)** — 상세 = [`google-cloud-tts-guide.md`](./google-cloud-tts-guide.md) §8:

```python
import os, json, sys
from pathlib import Path
from google.cloud import texttospeech

sys.stdout.reconfigure(encoding='utf-8')

EXP = Path("<exp 경로>")
TURNS = EXP / "turns"
TURNS.mkdir(exist_ok=True)

# Q/A → Google voice 매핑 (voice-pool.md Google section)
VOICE_MAP = {
    "Q": "ko-KR-Neural2-A",  # 여, 청소년
    "A": "ko-KR-Neural2-C",  # 남, 대학원생
}

client = texttospeech.TextToSpeechClient()

with open(EXP / "4-narration.jsonl", encoding="utf-8") as f:
    turns = [json.loads(l) for l in f if l.strip()]

for t in turns:
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name=VOICE_MAP[t["speaker"]],
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,
        pitch=0.0,
    )
    input_text = texttospeech.SynthesisInput(text=t["text"])
    resp = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    (TURNS / f"turn-{t['id']:03d}.mp3").write_bytes(resp.audio_content)

# concat (ffmpeg) → 4-narration.mp3
# 속도 조정 시 atempo=1.25 또는 speaking_rate=1.25 (TTS-side)
```

**ElevenLabs 합성 (v0.3 = 2차 — Starter $5 결제 시)**:
```python
# Python — turn 별 ElevenLabs API + ffmpeg concat
import os, json, requests, subprocess
from pathlib import Path

API_KEY = os.environ["ELEVENLABS_API_KEY"]
EXP = Path("<exp 경로>")
TURNS = EXP / "turns"
TURNS.mkdir(exist_ok=True)

# voice ID 조회 (1회)
r = requests.get("https://api.elevenlabs.io/v1/voices", headers={"xi-api-key": API_KEY})
VOICE_IDS = {v["name"]: v["voice_id"] for v in r.json()["voices"]}

# turn loop
with open(EXP / "4-narration.jsonl", encoding="utf-8") as f:
    turns = [json.loads(l) for l in f if l.strip()]

for t in turns:
    voice_id = VOICE_IDS[t["voice"]]
    resp = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json={
            "text": t["text"],
            "model_id": "eleven_multilingual_v2",
            "voice_settings": t.get("voice_settings", {})
        }
    )
    (TURNS / f"turn-{t['id']:03d}.mp3").write_bytes(resp.content)

# concat (silence padding 300ms)
# ffmpeg -f concat -safe 0 -i concat.txt -c copy 4-narration.mp3

# 속도 1.25배 post-processing (필요 시)
# ffmpeg -i 4-narration.mp3 -filter:a "atempo=1.25" 4-narration-fast.mp3
```

**edge-tts 합성 (v2 = 2차 비교 옵션)**:
```bash
# turn 별 mp3 생성 (jsonl 파싱 → loop)
mkdir -p turns
N=$(wc -l < 4-narration.jsonl)
for i in $(seq 1 $N); do
  ROW=$(sed -n "${i}p" 4-narration.jsonl)
  VOICE=$(echo "$ROW" | python -c "import sys,json; print(json.loads(sys.stdin.read())['voice'])")
  TEXT=$(echo "$ROW" | python -c "import sys,json; print(json.loads(sys.stdin.read())['text'])")
  RATE=$(echo "$ROW" | python -c "import sys,json; print(json.loads(sys.stdin.read()).get('rate','+0%'))")
  PITCH=$(echo "$ROW" | python -c "import sys,json; print(json.loads(sys.stdin.read()).get('pitch','+0Hz'))")
  edge-tts -v "$VOICE" --rate="$RATE" --pitch="$PITCH" --text "$TEXT" \
    --write-media "turns/turn-$(printf '%03d' $i).mp3"
done

# concat (silence padding 200ms between turns)
python <<'EOF'
from pathlib import Path
turns = sorted(Path("turns").glob("turn-*.mp3"))
with open("concat.txt","w") as f:
    for t in turns:
        f.write(f"file '{t.as_posix()}'\n")
EOF
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy 4-narration.mp3
```

**Azure / Google 단일 SSML 호출** (2차 시범 옵션) — `4-narration.xml` 직접 입력.

길이 측정:
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 <step>-narration.mp3
```

합격 기준 (TONE_STRUCTURE v2 §9): **150~210s** 범위.

### NR7. 자체 평가 + 출력
TONE_STRUCTURE v2 부합도 체크리스트:
- [ ] 2 화자 dialog (Q/A 명확 turn 분리)
- [ ] A 의 "나도 찾아봤는데..." 또는 비슷 표현 ≥ 1
- [ ] Q 의 자연 반응 다양 (3종 이상)
- [ ] A 의 되묻기 ≥ 1
- [ ] S1 풍부 배경 (시대 사실 ≥ 3)
- [ ] 마지막 장면 = Q 시도 + A 확인 (끊김 X)
- [ ] turn 평균 자수 10~30
- [ ] 길이 150~210s 범위
- [ ] voice 매핑 표 + 도구 비교 (`tts-tools-guide.md` §7)

출력:
- `<exp>/<step>-narration.txt` (평문 + marker)
- `<exp>/<step>-narration.xml` (SSML multi-voice)
- `<exp>/<step>-narration.jsonl` (turn 별)
- `<exp>/<step>-narration.mp3` (concat, gitignore)
- `<exp>/turns/turn-NNN.mp3` (turn 별 중간, gitignore)

---

## 출력 양식

```text
<exp>/
├── 4-narration.txt   ← 평문 (edge-tts/ElevenLabs 입력)
├── 4-narration.xml   ← SSML 풀스펙 (Azure/Google/Amazon 호환 reference)
├── 4-narration.mp3   ← 음성 (gitignore)
└── 4-narration.vtt   ← 자막 (edge-tts 자동 생성)
```

---

## QnA 패턴 시드

### NR2 보강 시
- *"voice = ko-KR-SunHiNeural (TONE_STRUCTURE 기본) / 다른 voice / 인물별 매핑?"*
- *"rate/pitch = TONE_STRUCTURE 기본 (-5% / +5Hz) / 단원 특화?"*
- *"ElevenLabs 도구 추가 시범? (API key 환경 가능 시)"*

### NR7 후 (선택)
- *"길이 ±10% 외 → rate 조절 / 텍스트 재정련?"*
- *"톤 청취 후 변경 (voice / pitch)?"*

---

## 리서치 패턴 시드

본 스킬은 입력 풍부 (스토리보드 + TONE_STRUCTURE) 하면 외부 리서치 *불필요*. 다음 경우만:

1. voice 한국어 자연도 검증 — Azure voice 카탈로그 (`edge-tts -l | grep ko-KR`)
2. ElevenLabs voice — https://elevenlabs.io/voice-library
3. SSML 호환성 확인 — 도구별 spec 페이지

---

## 평가 기준 (v3 dialog + 존댓말 + 다양화)

| 항목 | 합격 기준 |
|---|---|
| 길이 | TONE_STRUCTURE v3 §9 = **150~180s** (1.25배 속도) |
| **🔥 길이의 진짜 레버 = narrative 자수** | A화자 speed는 ±10s 미세조정용일 뿐, **길이는 narrative 분량이 결정**. 밀도 높은 단원은 설계 단계서 **≈1650자(≤30 turn)** 로 압축. A speed 권장값: Q=1.15 고정 / A=Mina 1.13·Kyle 1.14·Mike 1.10(화자별 기본 페이스 차이). 압축+A speed 적용 시 145~180s 안착 (u10 196→184, u11 197→188, u12 145, u13 177 학습 R39·R43·R48) |
| **🔥 PYTHONIOENCODING=utf-8** | 모든 python 합성/렌더 호출(synth.py·render_compile.py·gen_images.py)에 `PYTHONIOENCODING=utf-8` 선행. PowerShell·Bash의 cp949 콘솔이 `✓`·`π` 출력에서 UnicodeEncodeError로 **스크립트 크래시**(파일은 print 前 기록되어 보존되나 잡 실패 처리) (u10 학습 R35) |
| turn 평균 자수 | 10~30 |
| **2 화자 dialog** | Q/A turn 분리 + 성별 매핑 |
| **🔥 Q = 존댓말** | "~요?", "~예요?", "~어요!" 일관 (v3) |
| **🔥 A = 친절 반말** | "응, 알지", "잘 봐" 일관 (v3) |
| **🔥 의문/감탄/평문 다양** | 연속 평문 ≤ 2 turn / Q = 의문·감탄 위주 / A = 평·의·감 섞기 (v3) |
| A "나도 찾아봤는데..." | ≥ 1 회 |
| **🔥 논리 인과 정합** | turn 간 인과 비약 0. 인물 *발견* 과 *설명 언어* 분리 ([[se-people-narrate]] "직업 ≠ 설명 언어" 규칙 운반). 예: "천문 계산 → 회계 필요" 같은 거짓 인과 금지 (unit-02 학습) |
| **🔥 bare filler 회피** | 문장 맨 앞 단독 "음.../어..." 금지 → 실질 단어 시작 (남성 Q voice 뭉개짐, voice-pool §0.5) |
| **🔥 단원 번호 = 한글 단어** | "단원 2" 같은 *아라비아 숫자*는 TTS가 모호 발음(2→5 오인). 단원 참조는 **"두 번째 이야기"** 등 한글 서수로 (unit-04 학습) |
| **🔥 letter·숫자 = 한글 음차** | 발화는 "x"→**"엑스"**, "84"→**"여든네 살/팔십사"**. TTS가 로마자·큰 숫자를 못 읽어 깨짐. **자막은 시각 기호 유지**(보이는 x / 들리는 엑스) (unit-04 학습, voice-pool §0.5) |
| **🔥 부스트 클리핑** | A 음량 부스트(+8dB 등) 시 alimiter 필수(voice-pool §0.6). 감탄문 피크 하드클립=소리 깨짐 방지 |
| Q 자연 반응 다양 | "어!", "와!", "오!", "헐!" 등 ≥ 3 종 |
| A 되묻기 | ≥ 1 회 |
| 풍부 배경 | S1 시대 사실 ≥ 3 |
| 마무리 | Q 시도 + A 확인 + 짧은 정리 (끊김 X) |
| SSML multi-voice (reference) | `<voice>` × 2 + break + emphasis |
| **🔥 TTS 도구** | ElevenLabs 1차 (v0.5, config = voice-pool §0) / Google Cloud TTS 2차 백업 |
| 도구 비교 | tts-tools-guide.md §7 채움 |

---

## 진화 메커니즘

- **v0.1** (2026-05-26 오전) — 단일 voice 친근 톤 + 호기심 chain. 진화 (폐기 X).
- **v0.2** (2026-05-26 오전) — 2 화자 dialog (edge-tts). 한계 발견: 청소년 voice 부재, 211s 길이, 부자연 톤.
- **v0.3** (2026-05-26 오후) — **Nick redirect 3: Q 존댓말 + A 친절 반말 + 의문/감탄/평문 다양 + ElevenLabs 1차**. 현행.
- **v0.4** (2026-05-26 저녁) — ElevenLabs Free tier 차단 (HTTP 402) → Google Cloud TTS 1차 마이그 (임시).
- **v0.5** (2026-05-28) — ElevenLabs 1차 복귀 (Nick $10 credits). Annie/Mike, Onyu/Kyle 시범 (atempo 보정).
- **v0.5.1** (2026-05-28) — voice + speed 파라미터 도입 (Yura/Kanna 시범).
- **v0.5.2 (2026-05-28) — 여 voice 최종 확정 = Mina/Kanna**. 현행.
  - **합성 config SSOT = [voice-pool.md](./voice-pool.md) §0**
  - 여 voice 확정: **Mina** (`aiUUgjHa4mpHf6UenZuf`, Yura 청취 후 별로 → 교체) / **Kanna**. 남: Mike / Kyle
  - **속도 = `voice_settings.speed=1.15`** (Q) — ffmpeg atempo 폐기 (합성 시 직접)
  - post-processing: Q 없음 / A volume (Mike +8dB, Kyle +3.8dB)
  - text 규칙: 의문문 `?` + 중요단어 쉼표 `,` + 감탄 `~~` + 여운 `...` (voice-pool §0.5)
  - pause: Q/A 300ms + scene 1000ms (voice-pool §0.4)
  - 확정 mp3: 4-narration-mina-mike.mp3 (152s) / 4-narration-kanna-kyle.mp3 (140s)
- **v0.6+** = 다음 단원 시범 후 일반화 + 단원별 어투 다양 + Q/A 성별 randomize + 인물별 voice 고정.

---

## 호출 방법

```yaml
스킬: se-video-narration
입력:
  1. 스토리보드: 40_experiments/exp-NNN/3-storyboard.md (특히 부록 A)
  2. 정체성 + 톤·구조: INTEGRATED_PLAN §8 + TONE_STRUCTURE.md
  3. TTS 도구: **ElevenLabs** (1차, v0.5 현행 — config = voice-pool §0) / Google Cloud TTS (2차 백업)
  4. (옵션) 음성 매핑: 인물별 voice (단원 1 = 1 voice)
  5. (옵션) baseline SSML: <외부 의존 0>
출력:
  - 40_experiments/exp-NNN/<step>-narration.txt (평문)
  - 40_experiments/exp-NNN/<step>-narration.xml (SSML)
  - 40_experiments/exp-NNN/<step>-narration.mp3 (음성, gitignore)
  - 40_experiments/exp-NNN/<step>-narration.vtt (자막)
다음 단계: se-video-render (STEP 7) + se-video-compose (STEP 8)
```

본 시범 호출 예시: [`../../../11_video_gen_process/40_experiments/exp-002-build-unit01/4-narration.{txt,xml,mp3}`](../../../11_video_gen_process/40_experiments/exp-002-build-unit01/).
