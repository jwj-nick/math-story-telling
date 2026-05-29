<!-- elevenlabs-detailed-guide.md / ElevenLabs 상세 가이드 (Nick 용) -->

# ElevenLabs 상세 가이드

> **목적**: ElevenLabs API 를 본 프로젝트 (`se-video-narration`) 의 *2차 시범 도구* 로 사용하기 위한 step-by-step 가이드.
> **선행**: [`tts-tools-guide.md`](./tts-tools-guide.md) §4 (간단 setup) — 본 문서는 *상세 + 사용 + 문제 해결*.
> **단일 진입점**: [SKILL.md](./SKILL.md)
> **최근 갱신**: 2026-05-25

---

## 0. 본 가이드의 5 단계

1. 계정 가입 + 무료 한도 이해
2. API key 발급 + 환경 변수 설정
3. NCC 가 key 환경 확인
4. 한국어 voice 선택 + 자연도 테스트
5. 실제 사용 (Python API 또는 curl) + 사용량 모니터링

---

## 1. 계정 가입 + 무료 한도

### 가입
1. https://elevenlabs.io/ 접속
2. 우측 상단 **"Sign Up"** 클릭
3. 이메일 + 비밀번호 (또는 Google/Apple SSO)
4. 이메일 인증 클릭

### 무료 한도 (Free Tier)
- **매월 10,000 글자** 발화 가능
- 한국어 영상 1편 (약 550자) 기준 → **약 18편/월** 무료
- 매월 1일 한도 reset (UTC 기준)
- voice clone 불가 (Creator $22/월부터)
- API 호출 가능 (key 발급 가능)

### 한도 초과 시
- 자동 차단 (API 응답 429 "rate limit")
- Upgrade 옵션:
  - **Starter $5/월**: 30,000 자
  - **Creator $22/월**: 100,000 자 + voice cloning
  - **Pro $99/월**: 500,000 자
- 본 프로젝트 (단원당 1편) = Free 충분. 시즌 1 (5편) ≈ 무료 한도 28%.

---

## 2. API key 발급 + 환경 변수 설정

### 2.1 API key 발급
1. 로그인 후 우측 상단 프로필 아이콘 클릭
2. **"Profile + API Key"** 메뉴
3. **"Generate API Key"** 버튼 클릭
4. 표시된 키 `sk_xxx...` 복사
   - ⚠️ **1회만 표시됨**. 안전한 곳에 저장 (예: 1Password / Bitwarden)
   - 분실 시 새 key 발급 (구 key 자동 무효화)

### 2.2 환경 변수 설정 (Windows)

#### PowerShell — 영구 (User 환경 변수)
```powershell
[System.Environment]::SetEnvironmentVariable('ELEVENLABS_API_KEY', 'sk_xxx...', 'User')
```

검증 (새 PowerShell 열고):
```powershell
echo $env:ELEVENLABS_API_KEY
```

#### MINGW64 Bash — 한 세션만
```bash
export ELEVENLABS_API_KEY="sk_xxx..."
```

영구 적용은 PowerShell 명령 사용 (재시작 후 유지).

#### `.bashrc` / `.zshrc` 영구 (Linux/Mac)
```bash
echo 'export ELEVENLABS_API_KEY="sk_xxx..."' >> ~/.bashrc
source ~/.bashrc
```

### 2.3 보안 주의
- key 는 *github / 공유 파일 / chat 출력* 절대 X
- `.env` 파일 사용 시 `.gitignore` 등록 필수
- key 노출 의심 시: ElevenLabs 사이트에서 **즉시 revoke** + 새 key 발급

---

## 3. NCC 가 key 환경 확인

설정 완료 후 Nick → NCC: *"ElevenLabs key 설정 완료"* 알림.

NCC 는 *변수 존재만* 확인 (값 X):
```bash
[ -n "$ELEVENLABS_API_KEY" ] && echo "SET" || echo "unset"
```

키 값 자체는 chat 출력 절대 X.

---

## 4. 한국어 voice 선택

### 4.1 Voice Library 사용법

1. https://elevenlabs.io/app/voice-library 접속 (로그인 필요)
2. 필터:
   - **Language**: Korean / Multilingual
   - **Category**: Conversational / Narrative
   - **Gender / Age**: 원하는 조합
3. voice 카드 클릭 → 청취 (한국어 sample 입력 가능)
4. **"Add to My Voices"** 또는 **"Use Voice"** 클릭
5. NCC 에게 알림 — NCC 가 `/v1/voices` API 호출로 voice_id 조회 + voice-pool.md 갱신

### 4.2 Premade vs Community

| 구분 | 위치 | API access |
|---|---|---|
| Premade (21개) | `/v1/voices` 자동 표시 | 즉시 가능 |
| Community / Professional | Voice Library → Add to My Voices 후 | Add 후 `/v1/voices` 표시 |

### 4.3 현재 풀 (voice-pool.md)

본 프로젝트의 voice 풀 = [`voice-pool.md`](./voice-pool.md) 의 *현재 풀* 표 참조.

**1차 시범 폐기** (영문 voice 한국어 portable 어색):
- Jessica / Will / Bella / Adam — 미국 사람이 한국말 하는 듯한 톤

**Nick 추천 (2026-05-26, Community / library 검증 voice)**:
- 여: **Mono Beige**, **Yuna**
- 남: **Kyle**, **Mike**

→ Nick 의 My Voices 에 추가 → NCC 가 ID 조회 → 풀 진입.

### 4.4 voice 추가 → NCC 인식 흐름

```
[Nick] Voice Library → 검색 → 청취 → Add to My Voices
   ↓
[Nick → NCC] "voice X 추가 완료"
   ↓
[NCC] curl /v1/voices → voice_id 추출
   ↓
[NCC] voice-pool.md 갱신 + 시범 jsonl 의 voice 필드 업데이트
   ↓
[NCC] 시범 합성 → mp3 → Nick 청취 → 풀 평가
```

### 4.3 자연도 테스트

웹 인터페이스에서 직접:
1. https://elevenlabs.io/app/speech-synthesis
2. voice 선택 → 한국어 짧은 문장 입력 (예: "기원전 3세기, 알렉산드리아.")
3. **Generate** 클릭 → mp3 다운로드
4. 청취 후 자연도 판정

NCC 가 API 로 자동 테스트도 가능 (key 설정 후).

---

## 5. 실제 사용

### 5.1 Python (공식 SDK)

```bash
pip install elevenlabs
```

```python
import os
from elevenlabs import generate, save, set_api_key

set_api_key(os.environ["ELEVENLABS_API_KEY"])

with open("4-narration.txt", "r", encoding="utf-8") as f:
    text = f.read()

audio = generate(
    text=text,
    voice="Charlotte",
    model="eleven_multilingual_v2"
)
save(audio, "4-narration-elevenlabs.mp3")
```

### 5.2 curl (직접 API)

```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/<VOICE_ID>" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"...","model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.5,"similarity_boost":0.75}}' \
  --output 4-narration-elevenlabs.mp3
```

`<VOICE_ID>` 확인:
```bash
curl "https://api.elevenlabs.io/v1/voices" -H "xi-api-key: $ELEVENLABS_API_KEY" | python -m json.tool | grep -B1 "Charlotte"
```

### 5.3 voice_settings 튜닝

| 설정 | 범위 | 효과 |
|---|---|---|
| `stability` | 0~1 | 낮음 = 표현력 ↑ (변동) / 높음 = 일관성 ↑ (단조) |
| `similarity_boost` | 0~1 | 높음 = 원본 voice 충실도 ↑ |
| `style` | 0~1 (V2 only) | 감정 강도 (높을수록 dramatic) |

본 프로젝트 추천:
- 일반 = stability 0.5, similarity 0.75, style 0.0
- 결정적 순간 (S3·S4) = stability 0.3, similarity 0.75, style 0.5 (감정 ↑)

---

## 6. 사용량 모니터링

### 웹
- https://elevenlabs.io/usage
- 월별 사용량 그래프 + 남은 한도

### API
```bash
curl "https://api.elevenlabs.io/v1/user/subscription" -H "xi-api-key: $ELEVENLABS_API_KEY"
```

응답 (예시):
```json
{
  "character_count": 1234,
  "character_limit": 10000,
  "tier": "free",
  ...
}
```

---

## 7. 문제 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| 401 Unauthorized | key 무효 / 만료 | 새 key 발급 + 환경 변수 갱신 |
| 429 Rate Limit | 무료 한도 초과 | 다음 달 reset 대기 OR upgrade |
| 한국어 어색 | 영문 voice 사용 (multilingual_v2 X) | model_id="eleven_multilingual_v2" 명시 |
| 길이 너무 빠름/느림 | voice settings X | stability 조절 (낮을수록 변동) |
| 발음 오류 (예: 류후이 → ryu hwi) | 비표준 외래어 | 텍스트 한국어 발음 변환 (예: "리우 후이") 또는 SSML phoneme (단, ElevenLabs SSML 미지원이라 텍스트 변환만) |

---

## 8. ElevenLabs 시범 진입 시 NCC 작업 (체크리스트)

Nick 의 key 설정 완료 알림 후:

- [ ] `[ -n "$ELEVENLABS_API_KEY" ] && echo "SET"` 확인
- [ ] `pip install elevenlabs` 또는 curl 가능 확인
- [ ] voice ID 조회 (Charlotte / Bella / Adam / Rachel)
- [ ] Python script `4-narration-elevenlabs.py` 작성
- [ ] 4-narration.txt → 4-narration-elevenlabs.mp3 생성
- [ ] ffprobe 길이 측정
- [ ] tts-tools-guide.md §7 비교 표 채움
- [ ] retrospective 시드 추가 (감정 표현 / 자연도 / 비용 / 호출 복잡도)

---

## 9. 변경 이력

- 2026-05-25: 신규. tts-tools-guide.md §4 의 상세화. Nick 의 ElevenLabs guide 요청에 응답.
