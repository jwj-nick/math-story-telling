<!-- google-cloud-tts-guide.md / Google Cloud TTS setup + 사용 가이드 -->

# Google Cloud TTS 상세 가이드 (한국어 영상 나레이션)

> **목적**: `se-video-narration` 스킬의 **현행 1차 TTS 도구** Google Cloud TTS 의 setup, voice 사용, SSML, Python 호출 패턴.
> **상위 frame**: [SKILL.md](./SKILL.md) NR6 / [tts-tools-guide.md](./tts-tools-guide.md) §3 / [TONE_STRUCTURE.md](../../00_charter/TONE_STRUCTURE.md) §7.
> **본 가이드의 결정 효과**: ElevenLabs Free tier 차단 (HTTP 402, library voice X) 의 해결책. exp-002 STEP 4 v3.2 시범.
> **최근 갱신**: 2026-05-26 (옵션 B 선정 후 작성)

---

## 0. 왜 Google Cloud TTS 1차 인가?

| 항목 | edge-tts | ElevenLabs Free | **Google Cloud TTS** |
|---|---|---|---|
| 한국어 voice 다양성 | 3개만 | 21 premade (영문 한국어 portable) | **ko-KR 14+ Neural2/Wavenet/Standard** |
| 청소년 voice | ❌ 부재 | ❌ library voice = paid only | ⚠️ 표준 voice 위주 (Neural2 검증 필요) |
| 무료 한도 | 무제한 | 10,000 chars/월 | **Neural2 100만 chars/월** (본 영상 1편 = 550 chars → 1,800 편/월 무료) |
| SSML 풀 | 부분 | ❌ | ✅ **풀 지원** (prosody, break, emphasis, phoneme, mark) |
| Multi-voice | ❌ | ❌ | ❌ (turn 별 합성 + ffmpeg concat) |
| 안정성 | Microsoft 비공식 backend | Free tier API 제약 | **Google Cloud SLA** |
| NCC 호출 | Python CLI 1줄 | HTTP API | Python SDK |
| setup 복잡도 | 0 (pip 만) | API key 1개 | 서비스 계정 JSON (3단계) |

본 sub-project 선정 이유:
1. ElevenLabs Free tier 가 library voice (Mono Beige/Onyu/Kyle/Mike) API 호출 차단 → 결제 없이 진행 가능한 도구 필요
2. 한국어 *Neural2* voice = ElevenLabs 영문-한국어 portable 보다 자연
3. 무료 한도 매우 큼 → 본 sub-project (시즌 1 ~ 13 단원) 0 비용
4. SSML 풀 지원 → `4-narration.xml` 의 prosody/break 직접 활용 가능

---

## 1. 계정 + 프로젝트 만들기

### 1.1 Google Cloud 가입
1. https://console.cloud.google.com/ 접속
2. 기존 Google 계정 로그인 (Gmail 주소 — Nick: `jwookj@gmail.com` 사용 가능)
3. 약관 동의 + 국가 선택 → 콘솔 진입

### 1.2 새 프로젝트 생성
1. 콘솔 상단 "프로젝트 선택" 드롭다운 → "새 프로젝트"
2. 프로젝트 이름: `math-story-telling` (또는 자유)
3. 위치: 조직 없음 (개인 계정)
4. "만들기" → 1~2분 대기 → 프로젝트 활성화

### 1.3 결제 계정 (필요)
1. 좌측 메뉴 → "결제"
2. "결제 계정 연결" → 신용카드 등록
3. **무료 한도 안에서는 0원 청구**. 그러나 카드 등록은 API 활성화의 필수 조건
4. (옵션) 알림 예산 설정 ($1) → 한도 초과 시 메일 알림

> **무료 한도 확인**: https://cloud.google.com/text-to-speech/pricing — Neural2 100만 chars/월 = 본 sub-project 사용량의 1,800배. 사실상 0원.

---

## 2. Text-to-Speech API 활성화

1. 콘솔 좌측 메뉴 → "API 및 서비스" → "라이브러리"
2. 검색창에 `Text-to-Speech` 입력
3. **"Cloud Text-to-Speech API"** 클릭 (Google 제공)
4. "사용 설정" 클릭 → 1분 대기 → 활성화 완료

---

## 3. 서비스 계정 + JSON 키 발급

### 3.1 서비스 계정 만들기
1. 콘솔 좌측 메뉴 → "IAM 및 관리자" → "서비스 계정"
2. 상단 "+ 서비스 계정 만들기"
3. 입력:
   - 이름: `tts-narration` (자유)
   - ID: 자동 채워짐
   - 설명: `math-story-telling TTS 합성용`
4. "만들고 계속하기"
5. 역할: **"Cloud Text-to-Speech 사용자"** 선택 (검색: text-to-speech) — 최소 권한 원칙
   - 광범 권한 필요 시 "편집자" 가능하지만 본 sub-project 는 사용자 권한 충분
6. "계속" → "완료"

### 3.2 JSON 키 다운로드
1. 서비스 계정 목록에서 `tts-narration@...` 클릭
2. 상단 "키" 탭
3. "키 추가" → "새 키 만들기"
4. 키 유형: **JSON** 선택 → "만들기"
5. JSON 파일 자동 다운로드 (예: `math-story-telling-XXXXX-XXXXXX.json`)

### 3.3 JSON 파일 보안 저장
```powershell
# 권장 위치: C:\Users\admin\.gcloud\
New-Item -ItemType Directory -Force -Path "C:\Users\admin\.gcloud" | Out-Null
# 다운로드 폴더의 JSON 을 위 경로로 이동 + 이름 변경 (간결)
Move-Item -Path "$env:USERPROFILE\Downloads\math-story-telling-*.json" -Destination "C:\Users\admin\.gcloud\tts-key.json"
```

> ⚠️ **본 JSON 파일은 절대 git 에 commit X / chat 에 출력 X.**
> JSON 안에 `private_key` 필드 = 도용 시 결제 발생 가능.
> 본 sub-project `.gitignore` 에 `*.gcloud-key.json` 자동 추가.

---

## 4. 환경 변수 설정 (PowerShell User scope 영구)

### 4.1 PowerShell 영구 설정
```powershell
[System.Environment]::SetEnvironmentVariable('GOOGLE_APPLICATION_CREDENTIALS', 'C:\Users\admin\.gcloud\tts-key.json', 'User')
```

### 4.2 확인 (새 터미널 열기 또는 reload)
```powershell
[System.Environment]::GetEnvironmentVariable('GOOGLE_APPLICATION_CREDENTIALS', 'User')
# → C:\Users\admin\.gcloud\tts-key.json
```

### 4.3 NCC 자동 인식 (PowerShell 경유 패턴 — 기존 ElevenLabs 와 동일)
```bash
GCRED=$(powershell -NoProfile -Command "[System.Environment]::GetEnvironmentVariable('GOOGLE_APPLICATION_CREDENTIALS', 'User')" 2>/dev/null | tr -d '\r\n')
if [ -z "$GCRED" ] || [ ! -f "$GCRED" ]; then
  echo "ERROR: GOOGLE_APPLICATION_CREDENTIALS not set or file missing"
  exit 1
fi
export GOOGLE_APPLICATION_CREDENTIALS="$GCRED"
export PYTHONIOENCODING=utf-8
```

`google-cloud-texttospeech` SDK 가 `$GOOGLE_APPLICATION_CREDENTIALS` 환경 변수 자동 인식.

---

## 5. Python SDK 설치

```bash
pip install google-cloud-texttospeech
# 또는 venv 권장
```

검증:
```python
from google.cloud import texttospeech
client = texttospeech.TextToSpeechClient()
voices = client.list_voices(language_code="ko-KR")
for v in voices.voices:
    print(v.name, v.ssml_gender)
```

---

## 6. 한국어 voice 목록 (2026-05 기준)

> 공식 청취 페이지: https://cloud.google.com/text-to-speech/docs/voices

### 6.1 voice 등급별 카탈로그

| 등급 | voice 이름 | 성별 | 톤 | 본 sub-project 추천 |
|---|---|---|---|---|
| **Neural2** (최신, 추천) | `ko-KR-Neural2-A` | FEMALE | 표준, 따뜻 | ★ Q 청소년 1차 |
| **Neural2** | `ko-KR-Neural2-B` | FEMALE | 가벼움, 활기 | Q 청소년 후보 2 |
| **Neural2** | `ko-KR-Neural2-C` | MALE | 차분, 친절 | ★ A 대학원생 1차 |
| **Wavenet** | `ko-KR-Wavenet-A` | FEMALE | 표준 | Q 후보 |
| **Wavenet** | `ko-KR-Wavenet-B` | FEMALE | 표준 | Q 후보 |
| **Wavenet** | `ko-KR-Wavenet-C` | MALE | 표준 | A 후보 |
| **Wavenet** | `ko-KR-Wavenet-D` | MALE | 차분 | A 후보 |
| **Standard** (낮은 품질) | `ko-KR-Standard-A~D` | F/F/M/M | 기본 | (Neural2 무료 한도 큼 — Standard 사용 X) |
| **Chirp 3 HD** (최신 베타) | `ko-KR-Chirp3-HD-*` | 다양 | 자연성 ↑ | (검증 필요, voice 목록 동적) |

> Studio voice = 1인 cloning 용 (본 sub-project X).

### 6.2 본 sub-project 1차 매핑

| 화자 | voice | 이유 |
|---|---|---|
| **Q (여, 청소년, 존댓말)** | `ko-KR-Neural2-A` | Neural2 등급 (최신) + 여성 + 표준 따뜻 톤 |
| **A (남, 대학원생, 친절 반말)** | `ko-KR-Neural2-C` | Neural2 + 남성 + 차분 친절 |

(Nick 청취 후 평가 → `voice-pool.md` Google section 갱신)

### 6.3 voice 변경 시 Nick 의 청취 흐름

1. https://cloud.google.com/text-to-speech/docs/voices 접속
2. ko-KR voice 목록 (Neural2 / Wavenet) 클릭
3. 샘플 텍스트 입력 (예: "안녕! 나는 에라토스테네스라고 해.") → 청취
4. 마음에 든 voice 이름 NCC 에 알림 → `voice-pool.md` 갱신

---

## 7. 가격 + 무료 한도 (2026-05)

| 등급 | 무료 한도 (매월) | 초과 시 |
|---|---|---|
| **Standard** | 400만 chars | $4 / 100만 chars |
| **WaveNet** | 100만 chars | $16 / 100만 chars |
| **Neural2** | 100만 chars | $16 / 100만 chars |
| **Studio** | 100,000 chars | $160 / 100만 chars |
| **Journey/Polyglot** | (있는 경우 별도) | (공식 확인) |

본 sub-project 영상 1편 ≈ 550 chars:
- Neural2 100만 / 550 ≈ **1,818 편/월 무료**
- 시즌 1 (13 단원) = 0.7% 사용
- → **사실상 0 원**

공식 가격: https://cloud.google.com/text-to-speech/pricing

---

## 8. NCC 합성 패턴 (turn 별 + ffmpeg concat)

본 sub-project 의 `4-narration.jsonl` 형식 그대로 사용. ElevenLabs 패턴과 동일 구조, voice 만 ko-KR-Neural2-* 로 교체.

### 8.1 합성 Python 스크립트

```python
import os, json, sys
from pathlib import Path
from google.cloud import texttospeech

sys.stdout.reconfigure(encoding='utf-8')

EXP = Path("11_video_gen_process/40_experiments/exp-002-build-unit01")
TURNS = EXP / "turns"
TURNS.mkdir(exist_ok=True)

# Q/A → Google voice 매핑 (voice-pool.md Google section 참조)
VOICE_MAP = {
    "Q": "ko-KR-Neural2-A",  # 여, 청소년
    "A": "ko-KR-Neural2-C",  # 남, 대학원생
}

client = texttospeech.TextToSpeechClient()  # GOOGLE_APPLICATION_CREDENTIALS 자동 인식

with open(EXP / "4-narration.jsonl", encoding="utf-8") as f:
    turns = [json.loads(l) for l in f if l.strip()]

for t in turns:
    voice_name = VOICE_MAP[t["speaker"]]
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name=voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,   # 1.0 = 자연. 빠르면 1.15~1.25
        pitch=0.0,
    )
    input_text = texttospeech.SynthesisInput(text=t["text"])
    resp = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    out = TURNS / f"turn-{t['id']:03d}.mp3"
    out.write_bytes(resp.audio_content)
    print(f"[OK] turn-{t['id']:03d} ({t['speaker']}, {voice_name}, {len(t['text'])} chars)")

print("\n[DONE] all turns synthesized.")
```

### 8.2 concat + 길이 검증

```bash
# concat.txt 생성
python -c "
from pathlib import Path
turns = sorted(Path('11_video_gen_process/40_experiments/exp-002-build-unit01/turns').glob('turn-*.mp3'))
with open('11_video_gen_process/40_experiments/exp-002-build-unit01/concat.txt','w') as f:
    for t in turns:
        f.write(f\"file '{t.resolve().as_posix()}'\n\")
"

# ffmpeg concat
cd 11_video_gen_process/40_experiments/exp-002-build-unit01
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy 4-narration.mp3

# 길이 측정
ffprobe -v error -show_entries format=duration -of csv=p=0 4-narration.mp3
```

### 8.3 속도 조정 (필요 시)

```bash
# 1.25배 가속 (TONE_STRUCTURE v3 목표 150~180s)
ffmpeg -y -i 4-narration.mp3 -filter:a "atempo=1.25" 4-narration-fast.mp3
```

또는 Python 스크립트의 `speaking_rate=1.25` 옵션 직접 사용 (TTS-side 가속).

### 8.4 turn 사이 silence padding (옵션)

```bash
# Q→A 사이 300ms 추가
ffmpeg -i turn-001.mp3 -af "apad=pad_dur=0.3" -ar 24000 turn-001-padded.mp3
```

또는 concat.txt 에 silence file 끼워넣기.

---

## 9. SSML 사용 (옵션 — multi-voice X)

Google Cloud TTS `text:synthesize` endpoint = 1 voice 단일 호출.

SSML 단일 호출 시 입력:
```python
input_text = texttospeech.SynthesisInput(ssml="""
<speak xml:lang="ko-KR">
  <prosody rate="-5%" pitch="+5Hz">
    들어봤어요? <break time="300ms"/>
  </prosody>
</speak>
""")
```

**`<voice name="...">` 태그는 Google standard endpoint 에서 무시됨**. multi-speaker 는 turn 별 합성 (§8) 이 표준.

> 참고: Google `synthesizeLongAudio` (Long Audio) = LRO 비동기, 1분 이상 콘텐츠용. 본 sub-project 110~180초 = 일반 endpoint 충분.

---

## 10. 본 sub-project 합성 흐름 (정리)

```
1. Nick: Google Cloud 계정 + 프로젝트 + 결제 연결
2. Nick: Text-to-Speech API 활성화
3. Nick: 서비스 계정 생성 + JSON key 다운로드
4. Nick: PowerShell setx GOOGLE_APPLICATION_CREDENTIALS
5. Nick: pip install google-cloud-texttospeech
6. Nick: NCC 에 "Google Cloud TTS setup 완료" 알림
7. NCC: PowerShell 경유 GOOGLE_APPLICATION_CREDENTIALS 자동 추출
8. NCC: 4-narration.jsonl 의 voice 필드 = ko-KR-Neural2-A/C 갱신
9. NCC: 8.1 합성 → 8.2 concat → 8.3 길이 측정
10. Nick: 청취 + 평가 → voice-pool.md Google section 갱신
```

---

## 11. ElevenLabs vs Google 비교 흐름 (2 도구 운영)

본 sub-project 는 *도구 비교 자산* 도 시스템 자산. 양쪽 결과:

| 시범 | 결과 |
|---|---|
| ElevenLabs Jessica/Will (premade) | 127.6s, 미국식 한국말 부자연 |
| ElevenLabs Mono Beige/Mike (library) | HTTP 402 Free tier 차단 |
| **Google Neural2-A/C** (현 시범) | (Nick 청취 평가 대기) |

향후 Nick 가 ElevenLabs Starter $5 결제 시 Mono Beige/Mike 도 시범 가능. 본 sub-project 는 두 결과 비교로 결정 기록 (INTEGRATED_PLAN §8 결정 12 후보).

---

## 12. 보안 노트

- JSON key 파일 = registry/file system 보관, **chat 노출 0**
- PowerShell setx 경유 = NCC 가 path 만 추출, 파일 안의 `private_key` 직접 X
- `.gitignore` 에 `*.gcloud-key.json` 추가 (외부 노출 차단)
- API 사용량 = Google Cloud 콘솔에서 매일 확인 (이상 사용 발견 시 service account 비활성화)

---

## 13. 변경 이력

- 2026-05-26 v1: 신규. ElevenLabs Free tier 차단 발견 → 옵션 B 선정 후 작성. exp-002 STEP 4 v3.2 시범 진입.
